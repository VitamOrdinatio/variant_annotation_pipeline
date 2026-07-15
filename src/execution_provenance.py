\
"""
Canonical execution provenance resolution for VAP.

This module resolves toolchain, annotation, and scientific-resource identity.
It is intentionally independent of pipeline orchestration so its behavior can
be unit-tested before becoming a pre-Stage-01 execution gate.
"""

from __future__ import annotations

import hashlib
import os
import platform
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Iterable, Sequence


PROVENANCE_SCHEMA_VERSION = "1.0.0"
BWA_INDEX_SUFFIXES = (".amb", ".ann", ".bwt", ".pac", ".sa")

CommandRunner = Callable[..., subprocess.CompletedProcess[bytes]]
WhichResolver = Callable[[str], str | None]


class ExecutionProvenanceError(RuntimeError):
    """Raised when required execution provenance cannot be resolved."""


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def sha256_file(path: str | Path) -> str:
    file_path = Path(path)
    digest = hashlib.sha256()
    with file_path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def resolve_config_value(config: dict[str, Any], dotted_path: str) -> Any:
    current: Any = config
    for key in dotted_path.split("."):
        if not isinstance(current, dict) or key not in current:
            raise ExecutionProvenanceError(
                f"Configured provenance source is missing: {dotted_path}"
            )
        current = current[key]
    return current


def resolve_executable(
    configured_executable: str,
    *,
    which_resolver: WhichResolver = shutil.which,
) -> str:
    value = str(configured_executable).strip()
    if not value:
        raise ExecutionProvenanceError("Configured executable is empty")

    candidate = Path(value).expanduser()
    if candidate.is_absolute() or os.sep in value:
        if not candidate.is_file():
            raise ExecutionProvenanceError(
                f"Configured executable does not exist: {candidate}"
            )
        if not os.access(candidate, os.X_OK):
            raise ExecutionProvenanceError(
                f"Configured executable is not executable: {candidate}"
            )
        return str(candidate.resolve())

    resolved = which_resolver(value)
    if resolved is None:
        raise ExecutionProvenanceError(
            f"Executable not found on PATH: {value}"
        )
    return str(Path(resolved).resolve())


def _decode_probe_stream(
    value: bytes | str | None,
) -> str:
    """
    Decode external tool output without assuming valid UTF-8.

    Real toolchains may emit locale-specific or package-build bytes in
    otherwise ASCII-compatible version output. Invalid UTF-8 bytes remain
    visible as replacement characters rather than aborting provenance
    resolution.
    """
    if value is None:
        return ""

    if isinstance(value, str):
        # Compatibility with synthetic command runners and older tests.
        return value

    return value.decode(
        "utf-8",
        errors="replace",
    )


def _run_probe(
    command: Sequence[str],
    *,
    command_runner: CommandRunner = subprocess.run,
) -> str:
    result = command_runner(
        list(command),
        capture_output=True,
        text=False,
        check=False,
    )

    stdout = _decode_probe_stream(result.stdout)
    stderr = _decode_probe_stream(result.stderr)

    text = "\n".join(
        part.strip()
        for part in (stdout, stderr)
        if part.strip()
    )

    if not text:
        raise ExecutionProvenanceError(
            "Version probe returned no output: "
            + " ".join(command)
            + f"; exit_code={result.returncode}"
        )

    return text


def _first_match(text: str, patterns: Iterable[str], label: str) -> str:
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE | re.MULTILINE)
        if match:
            return match.group(1)
    raise ExecutionProvenanceError(
        f"Unable to parse {label} version from probe output"
    )


def parse_bwa_version(text: str) -> str:
    return _first_match(
        text,
        (
            r"\bVersion:\s*([0-9]+(?:\.[0-9]+)+(?:-[A-Za-z0-9._-]+)?)",
            r"\bbwa\s+([0-9]+(?:\.[0-9]+)+(?:-[A-Za-z0-9._-]+)?)",
        ),
        "BWA",
    )


def parse_samtools_version(text: str) -> str:
    return _first_match(
        text,
        (r"^\s*samtools\s+([0-9]+(?:\.[0-9]+)+)",),
        "samtools",
    )


def parse_gatk_version(text: str) -> str:
    return _first_match(
        text,
        (
            r"Genome Analysis Toolkit \(GATK\)\s+v?([0-9]+(?:\.[0-9]+)+)",
            r"^\s*([0-9]+(?:\.[0-9]+){2,})\s*$",
            r"\bGATK\s+v?([0-9]+(?:\.[0-9]+)+)",
        ),
        "GATK",
    )


def parse_java_version(text: str) -> str:
    return _first_match(
        text,
        (
            r'version\s+"([^"]+)"',
            r"openjdk\s+([0-9]+(?:\.[0-9]+)+)",
        ),
        "Java",
    )


def parse_perl_version(text: str) -> str:
    return _first_match(
        text,
        (
            r"\(v([0-9]+(?:\.[0-9]+)+)\)",
            r"This is perl .*? version\s+([0-9]+(?:\.[0-9]+)+)",
        ),
        "Perl",
    )


def parse_vep_version(text: str) -> str:
    return _first_match(
        text,
        (
            r"\bensembl-vep:\s*([0-9]+(?:\.[0-9]+)*)",
            r"\bVEP(?:\s+version)?\s*[:v]?\s*([0-9]+(?:\.[0-9]+)*)",
            r"\brelease[-_\s]?([0-9]+(?:\.[0-9]+)*)",
        ),
        "VEP",
    )


def compare_version(
    *,
    declared_version: str | None,
    declared_major_version: str | None,
    observed_version: str,
    policy: str,
) -> tuple[str, str]:
    if policy == "record_only":
        return "pass", "record_only"

    if policy == "exact":
        if observed_version == declared_version:
            return "pass", "exact_match"
        return (
            "fail",
            f"expected={declared_version}; observed={observed_version}",
        )

    if policy == "major":
        observed_major = observed_version.split(".", 1)[0]
        if observed_major == declared_major_version:
            return "pass", "major_match"
        return (
            "fail",
            f"expected_major={declared_major_version}; "
            f"observed={observed_version}",
        )

    raise ExecutionProvenanceError(
        f"Unsupported version policy: {policy}"
    )



def assert_contract_pass(
    provenance: dict[str, Any],
) -> dict[str, Any]:
    """
    Return provenance when the overall contract passes; otherwise fail.
    """
    status = provenance.get("contract_status")
    if status == "pass":
        return provenance

    failed_surfaces = provenance.get("failed_surfaces", [])
    details: list[str] = []

    toolchain = provenance.get("toolchain_environment", {})
    for tool_name in toolchain.get("failed_tools", []):
        record = toolchain.get("tools", {}).get(tool_name, {})
        details.append(
            f"{tool_name}: {record.get('version_status_detail')}"
        )

    annotation = provenance.get("annotation_environment", {})
    details.extend(annotation.get("failures", []))

    message = "Execution provenance contract failed"
    if failed_surfaces:
        message += ": " + ", ".join(failed_surfaces)
    if details:
        message += "; " + "; ".join(details)

    raise ExecutionProvenanceError(message)

def _tool_record(
    *,
    name: str,
    configured_executable: str,
    resolved_executable: str,
    observed_version: str,
    declaration: dict[str, Any],
    probe_command: Sequence[str],
) -> dict[str, Any]:
    status, detail = compare_version(
        declared_version=declaration.get("declared_version"),
        declared_major_version=declaration.get(
            "declared_major_version"
        ),
        observed_version=observed_version,
        policy=declaration["version_policy"],
    )
    return {
        "tool_name": name,
        "configured_executable": configured_executable,
        "resolved_executable": resolved_executable,
        "declared_version": declaration.get("declared_version"),
        "declared_major_version": declaration.get(
            "declared_major_version"
        ),
        "observed_version": observed_version,
        "version_policy": declaration["version_policy"],
        "version_status": status,
        "version_status_detail": detail,
        "probe_command": list(probe_command),
    }


def resolve_toolchain_environment(
    config: dict[str, Any],
    *,
    command_runner: CommandRunner = subprocess.run,
    which_resolver: WhichResolver = shutil.which,
) -> dict[str, Any]:
    provenance = config["execution_provenance"]
    declarations = provenance["toolchain"]
    records: dict[str, dict[str, Any]] = {}

    executable_specs = {
        "bwa": (
            ["--version"],
            parse_bwa_version,
        ),
        "samtools": (
            ["--version"],
            parse_samtools_version,
        ),
        "gatk": (
            ["--version"],
            parse_gatk_version,
        ),
        "vep": (
            ["--help"],
            parse_vep_version,
        ),
    }

    # BWA commonly writes its version when invoked without arguments.
    executable_specs["bwa"] = ([], parse_bwa_version)

    for name in ("bwa", "samtools", "gatk", "vep"):
        declaration = declarations[name]
        configured = str(
            resolve_config_value(
                config,
                declaration["configured_from"],
            )
        )
        resolved = resolve_executable(
            configured,
            which_resolver=which_resolver,
        )
        args, parser = executable_specs[name]
        command = [resolved, *args]
        observed = parser(
            _run_probe(command, command_runner=command_runner)
        )
        records[name] = _tool_record(
            name=name,
            configured_executable=configured,
            resolved_executable=resolved,
            observed_version=observed,
            declaration=declaration,
            probe_command=command,
        )

    java_decl = declarations["java"]
    java_resolved = resolve_executable(
        "java",
        which_resolver=which_resolver,
    )
    java_command = [java_resolved, "-version"]
    java_observed = parse_java_version(
        _run_probe(java_command, command_runner=command_runner)
    )
    records["java"] = _tool_record(
        name="java",
        configured_executable="java",
        resolved_executable=java_resolved,
        observed_version=java_observed,
        declaration=java_decl,
        probe_command=java_command,
    )
    records["java"]["configured_options"] = (
        config.get("tools", {}).get("gatk", {}).get("java_options")
    )

    perl_decl = declarations["perl"]
    perl_resolved = resolve_executable(
        "perl",
        which_resolver=which_resolver,
    )
    perl_command = [perl_resolved, "-v"]
    perl_observed = parse_perl_version(
        _run_probe(perl_command, command_runner=command_runner)
    )
    records["perl"] = _tool_record(
        name="perl",
        configured_executable="perl",
        resolved_executable=perl_resolved,
        observed_version=perl_observed,
        declaration=perl_decl,
        probe_command=perl_command,
    )

    python_decl = declarations["python"]
    python_observed = platform.python_version()
    records["python"] = _tool_record(
        name="python",
        configured_executable=sys.executable,
        resolved_executable=str(Path(sys.executable).resolve()),
        observed_version=python_observed,
        declaration=python_decl,
        probe_command=[sys.executable, "--version"],
    )
    records["python"]["virtual_environment"] = os.environ.get(
        "VIRTUAL_ENV"
    )

    failed = sorted(
        name
        for name, record in records.items()
        if record["version_status"] != "pass"
    )
    return {
        "contract_status": "pass" if not failed else "fail",
        "failed_tools": failed,
        "tools": records,
    }



def parse_vep_cache_directory_name(name: str) -> tuple[str, str]:
    """
    Parse a VEP cache directory name such as 115_GRCh38.
    """
    match = re.fullmatch(r"([0-9]+)_([A-Za-z0-9._-]+)", name)
    if not match:
        raise ExecutionProvenanceError(
            f"Unparseable VEP cache directory name: {name}"
        )
    return match.group(1), match.group(2)


def discover_vep_cache(
    *,
    cache_dir: str | Path,
    species: str,
    release: str,
    assembly: str,
) -> dict[str, Any]:
    root = Path(cache_dir).expanduser()
    if not root.is_dir():
        raise ExecutionProvenanceError(
            f"VEP cache directory not found: {root}"
        )

    expected_name = f"{release}_{assembly}"
    candidate_roots = [
        root / species,
        root,
    ]
    direct_matches = [
        base / expected_name
        for base in candidate_roots
        if (base / expected_name).is_dir()
    ]

    recursive_matches = sorted(
        path
        for path in root.rglob(expected_name)
        if path.is_dir()
        and (
            path.parent.name == species
            or species in path.parts
        )
    )

    all_matches = sorted(
        {path.resolve() for path in [*direct_matches, *recursive_matches]}
    )

    if not all_matches:
        raise ExecutionProvenanceError(
            "Expected VEP cache not found: "
            f"species={species}; release={release}; assembly={assembly}; "
            f"root={root}"
        )

    if len(all_matches) > 1:
        raise ExecutionProvenanceError(
            "Multiple matching VEP cache directories found: "
            + ", ".join(str(path) for path in all_matches)
        )

    matched = all_matches[0]
    observed_release, observed_assembly = (
        parse_vep_cache_directory_name(matched.name)
    )

    observed_species = (
        species
        if species in matched.parts
        else matched.parent.name
    )

    return {
        "configured_cache_directory": str(root),
        "resolved_cache_directory": str(matched),
        "declared_cache_release": release,
        "observed_cache_release": observed_release,
        "declared_species": species,
        "observed_species": observed_species,
        "declared_assembly": assembly,
        "observed_assembly": observed_assembly,
        "cache_directory_name": matched.name,
        "cache_identity_status": (
            "pass"
            if (
                observed_release == release
                and observed_assembly == assembly
                and observed_species == species
            )
            else "fail"
        ),
    }


def resolve_annotation_environment(
    config: dict[str, Any],
    toolchain_environment: dict[str, Any],
) -> dict[str, Any]:
    declaration = config["execution_provenance"][
        "annotation_environment"
    ]
    vep_record = toolchain_environment["tools"]["vep"]

    cache = discover_vep_cache(
        cache_dir=config["tools"]["vep"]["cache_dir"],
        species=declaration["cache_species"],
        release=declaration["cache_release"],
        assembly=declaration["cache_assembly"],
    )

    comparisons = {
        "software_version": {
            "declared": declaration["software_version"],
            "observed": vep_record["observed_version"],
        },
        "cache_release": {
            "declared": declaration["cache_release"],
            "observed": cache["observed_cache_release"],
        },
        "species": {
            "declared": declaration["cache_species"],
            "observed": cache["observed_species"],
        },
        "assembly": {
            "declared": declaration["cache_assembly"],
            "observed": cache["observed_assembly"],
        },
    }

    failures: list[str] = []
    for field, values in comparisons.items():
        if values["declared"] != values["observed"]:
            failures.append(
                f"{field}: expected={values['declared']}; "
                f"observed={values['observed']}"
            )

    configured_offline = bool(config["tools"]["vep"].get("offline"))
    if declaration["execution_mode"] == "offline" and not configured_offline:
        failures.append(
            "offline execution declared but tools.vep.offline=false"
        )

    if vep_record["version_status"] != "pass":
        failures.append(
            "VEP software version contract failed: "
            f"{vep_record['version_status_detail']}"
        )

    return {
        "engine": declaration["engine"],
        "software": {
            "declared_version": declaration["software_version"],
            "observed_version": vep_record["observed_version"],
            "version_status": vep_record["version_status"],
            "version_status_detail": vep_record[
                "version_status_detail"
            ],
            "configured_executable": vep_record[
                "configured_executable"
            ],
            "resolved_executable": vep_record[
                "resolved_executable"
            ],
        },
        "cache": {
            **cache,
            "cache_type": declaration["cache_type"],
        },
        "execution": {
            "declared_mode": declaration["execution_mode"],
            "offline_configured": configured_offline,
            "perl_version": toolchain_environment["tools"]["perl"][
                "observed_version"
            ],
        },
        "comparisons": comparisons,
        "contract_status": "pass" if not failures else "fail",
        "failures": failures,
    }


def require_annotation_environment(
    state: dict[str, Any],
) -> dict[str, Any]:
    """
    Return the centralized annotation environment for Stage 07 consumption.
    """
    provenance = state.get("execution_provenance")
    if not isinstance(provenance, dict):
        raise ExecutionProvenanceError(
            "execution_provenance is missing from runtime state"
        )

    annotation = provenance.get("annotation_environment")
    if not isinstance(annotation, dict):
        raise ExecutionProvenanceError(
            "annotation_environment is missing from execution provenance"
        )

    if annotation.get("contract_status") != "pass":
        raise ExecutionProvenanceError(
            "annotation environment contract has not passed"
        )

    return annotation

def resource_record(
    *,
    role: str,
    configured_path: str | Path,
    declared_sha256: str | None = None,
) -> dict[str, Any]:
    path = Path(configured_path).expanduser()
    if not path.is_file():
        raise ExecutionProvenanceError(
            f"Required resource does not exist: {role}: {path}"
        )
    resolved = path.resolve()
    observed_sha256 = sha256_file(resolved)

    if declared_sha256 is None:
        checksum_status = "recorded"
        checksum_detail = "no_declared_checksum"
        contract_status = "pass"
    elif observed_sha256 == declared_sha256:
        checksum_status = "pass"
        checksum_detail = "exact_match"
        contract_status = "pass"
    else:
        checksum_status = "fail"
        checksum_detail = (
            f"expected={declared_sha256}; observed={observed_sha256}"
        )
        contract_status = "fail"

    return {
        "resource_role": role,
        "configured_path": str(path),
        "resolved_path": str(resolved),
        "size_bytes": resolved.stat().st_size,
        "declared_sha256": declared_sha256,
        "observed_sha256": observed_sha256,
        "sha256": observed_sha256,
        "checksum_status": checksum_status,
        "checksum_status_detail": checksum_detail,
        "contract_status": contract_status,
    }



def resolve_bwa_index(
    prefix: str | Path,
    *,
    declared_aggregate_sha256: str | None = None,
) -> dict[str, Any]:
    prefix_path = Path(prefix).expanduser()
    constituents = []
    missing = []

    for suffix in BWA_INDEX_SUFFIXES:
        path = Path(str(prefix_path) + suffix)
        if not path.is_file():
            missing.append(str(path))
            continue
        constituents.append(
            resource_record(
                role=f"bwa_index{suffix}",
                configured_path=path,
            )
        )

    if missing:
        raise ExecutionProvenanceError(
            "Missing BWA index constituents: " + ", ".join(missing)
        )

    aggregate = hashlib.sha256()
    for record in sorted(
        constituents,
        key=lambda item: item["resource_role"],
    ):
        aggregate.update(record["resource_role"].encode("utf-8"))
        aggregate.update(b"\0")
        aggregate.update(record["observed_sha256"].encode("ascii"))
        aggregate.update(b"\n")

    observed = aggregate.hexdigest()

    if declared_aggregate_sha256 is None:
        status = "recorded"
        detail = "no_declared_checksum"
        contract = "pass"
    elif observed == declared_aggregate_sha256:
        status = "pass"
        detail = "exact_match"
        contract = "pass"
    else:
        status = "fail"
        detail = (
            f"expected={declared_aggregate_sha256}; observed={observed}"
        )
        contract = "fail"

    return {
        "resource_role": "bwa_index",
        "configured_prefix": str(prefix_path),
        "resolved_prefix": str(prefix_path.resolve()),
        "checksum_policy": "sha256_constituents",
        "constituent_count": len(constituents),
        "constituents": constituents,
        "declared_aggregate_sha256": declared_aggregate_sha256,
        "observed_aggregate_sha256": observed,
        "aggregate_sha256": observed,
        "checksum_status": status,
        "checksum_status_detail": detail,
        "contract_status": contract,
    }


def _fasta_contigs(path: Path) -> list[str]:
    values = []
    with path.open("r", encoding="utf-8", errors="replace") as handle:
        for line in handle:
            if line.startswith(">"):
                values.append(line[1:].strip().split()[0])
    if not values:
        raise ExecutionProvenanceError(
            f"Reference FASTA contains no contigs: {path}"
        )
    return values


def _fai_contigs(path: Path) -> list[str]:
    values = []
    with path.open("r", encoding="utf-8", errors="replace") as handle:
        for line in handle:
            if line.strip():
                values.append(line.split("\t", 1)[0].strip())
    if not values:
        raise ExecutionProvenanceError(
            f"FASTA index contains no contigs: {path}"
        )
    return values


def _dictionary_contigs(path: Path) -> list[str]:
    values = []
    pattern = re.compile(r"(?:^|\t)SN:([^\t]+)")
    with path.open("r", encoding="utf-8", errors="replace") as handle:
        for line in handle:
            if not line.startswith("@SQ"):
                continue
            match = pattern.search(line.rstrip("\n"))
            if match:
                values.append(match.group(1))
    if not values:
        raise ExecutionProvenanceError(
            f"Sequence dictionary contains no @SQ contigs: {path}"
        )
    return values


def validate_reference_set_coherence(
    *,
    fasta_path: str | Path,
    fai_path: str | Path,
    dictionary_path: str | Path,
) -> dict[str, Any]:
    fasta = _fasta_contigs(Path(fasta_path))
    fai = _fai_contigs(Path(fai_path))
    dictionary = _dictionary_contigs(Path(dictionary_path))

    failures = []
    if fasta != fai:
        failures.append("FASTA and FAI contig order differ")
    if fasta != dictionary:
        failures.append(
            "FASTA and sequence dictionary contig order differ"
        )

    return {
        "fasta_contig_count": len(fasta),
        "fai_contig_count": len(fai),
        "dictionary_contig_count": len(dictionary),
        "contract_status": "pass" if not failures else "fail",
        "failures": failures,
    }


def resolve_resource_environment(
    config: dict[str, Any],
) -> dict[str, Any]:
    declarations = config["execution_provenance"][
        "resource_environment"
    ]
    records = {}

    for name in (
        "reference_fasta",
        "fasta_index",
        "sequence_dictionary",
        "mitocarta",
        "genes4epilepsy",
    ):
        declaration = declarations[name]
        value = resolve_config_value(
            config,
            declaration["configured_from"],
        )
        records[name] = resource_record(
            role=name,
            configured_path=value,
            declared_sha256=declaration.get("declared_sha256"),
        )
        records[name]["checksum_policy"] = declaration[
            "checksum_policy"
        ]

    bwa_decl = declarations["bwa_index"]
    bwa_prefix = resolve_config_value(
        config,
        bwa_decl["configured_from"],
    )
    records["bwa_index"] = resolve_bwa_index(
        bwa_prefix,
        declared_aggregate_sha256=bwa_decl.get(
            "declared_aggregate_sha256"
        ),
    )

    coherence = validate_reference_set_coherence(
        fasta_path=records["reference_fasta"]["resolved_path"],
        fai_path=records["fasta_index"]["resolved_path"],
        dictionary_path=records["sequence_dictionary"][
            "resolved_path"
        ],
    )

    failed_resources = sorted(
        name
        for name, record in records.items()
        if record["contract_status"] != "pass"
    )
    failures = [
        f"{name}: {records[name].get('checksum_status_detail')}"
        for name in failed_resources
    ]
    failures.extend(coherence["failures"])

    return {
        "contract_status": "pass" if not failures else "fail",
        "failed_resources": failed_resources,
        "failures": failures,
        "reference_set_coherence": coherence,
        "resources": records,
    }


def write_execution_provenance_receipt(
    *,
    provenance: dict[str, Any],
    output_path: str | Path,
) -> Path:
    """
    Write the authoritative execution provenance receipt as stable JSON.
    """
    import json

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(
        provenance,
        indent=2,
        sort_keys=True,
    ) + "\n"

    temporary = path.with_name(f".{path.name}.tmp")
    temporary.write_text(payload, encoding="utf-8")
    temporary.replace(path)
    return path


def resolve_execution_provenance(
    config: dict[str, Any],
    *,
    command_runner: CommandRunner = subprocess.run,
    which_resolver: WhichResolver = shutil.which,
) -> dict[str, Any]:
    execution_mode = config["mode"]["execution_mode"]

    if execution_mode == "post_vep_fixture":
        return {
            "schema_version": PROVENANCE_SCHEMA_VERSION,
            "generated_utc": utc_now_iso(),
            "resolution_mode": "retained_source_provenance",
            "provenance_completeness": "legacy_partial",
            "contract_status": "not_applicable",
            "toolchain_environment": {
                "contract_status": "not_applicable",
                "tools": {},
            },
            "annotation_environment": {
                "contract_status": "not_applicable",
            },
            "resource_environment": {
                "contract_status": "not_applicable",
                "resources": {},
            },
        }

    toolchain = resolve_toolchain_environment(
        config,
        command_runner=command_runner,
        which_resolver=which_resolver,
    )
    annotation = resolve_annotation_environment(config, toolchain)
    resources = resolve_resource_environment(config)

    failed_surfaces = [
        name
        for name, surface in (
            ("toolchain_environment", toolchain),
            ("annotation_environment", annotation),
            ("resource_environment", resources),
        )
        if surface["contract_status"] != "pass"
    ]

    return {
        "schema_version": PROVENANCE_SCHEMA_VERSION,
        "generated_utc": utc_now_iso(),
        "resolution_mode": "live_runtime_resolution",
        "provenance_completeness": "complete",
        "contract_status": "pass" if not failed_surfaces else "fail",
        "failed_surfaces": failed_surfaces,
        "host_environment": {
            "hostname": platform.node(),
            "platform": platform.platform(),
            "system": platform.system(),
            "release": platform.release(),
            "machine": platform.machine(),
            "python_executable": str(Path(sys.executable).resolve()),
            "virtual_environment": os.environ.get("VIRTUAL_ENV"),
        },
        "toolchain_environment": toolchain,
        "annotation_environment": annotation,
        "resource_environment": resources,
    }
