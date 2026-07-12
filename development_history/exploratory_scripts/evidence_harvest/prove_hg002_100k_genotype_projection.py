#!/usr/bin/env python3
"""
Run the HG002 100k real-data genotype projection proof on sys76.

Run from the VAP repository root:

    python development_history/exploratory_scripts/evidence_harvest/prove_hg002_100k_genotype_projection.py
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import resource
import shutil
import sys
import time
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parents[3]

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


from pipeline.genotype_projection import project_genotype_observations


DEFAULT_FIXTURE_ROOT = Path(
    "/mnt/storage/vap_genotype_fixture/hg002_frankenstein_v1"
)
DEFAULT_SOURCE = (
    DEFAULT_FIXTURE_ROOT
    / "source"
    / "lightweight"
    / "HG002_genotype_development_100k.vcf"
)
DEFAULT_CONFIG = DEFAULT_FIXTURE_ROOT / "run_context" / "config_snapshot.yaml"
DEFAULT_RECEIPTS = DEFAULT_FIXTURE_ROOT / "receipts"

ARTIFACT_NAMES = (
    "genotype_observations.tsv",
    "genotype_projection_summary.json",
    "genotype_source_header_context.json",
)


@dataclass(frozen=True)
class RunReceipt:
    label: str
    output_directory: str
    elapsed_seconds: float
    peak_rss_kib: int
    source_record_count: int
    genotype_observation_row_count: int
    projection_status: str
    artifact_sha256: dict[str, str]
    artifact_size_bytes: dict[str, int]


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def local_stamp() -> str:
    return datetime.now().strftime("%Y_%m_%d_%H%M%S")


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(chunk_size), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        payload = yaml.safe_load(handle)
    if not isinstance(payload, dict):
        raise ValueError(f"Expected YAML object: {path}")
    return payload


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise ValueError(f"Expected JSON object: {path}")
    return payload


def count_vcf_records(path: Path) -> int:
    count = 0
    with path.open("r", encoding="utf-8", errors="replace") as handle:
        for line in handle:
            if line and not line.startswith("#"):
                count += 1
    return count


def count_tsv_rows(path: Path) -> int:
    with path.open("r", encoding="utf-8", errors="replace", newline="") as handle:
        reader = csv.reader(handle, delimiter="\t")
        try:
            next(reader)
        except StopIteration:
            return 0
        return sum(1 for _ in reader)


def artifact_hashes(output_directory: Path) -> dict[str, str]:
    return {
        name: sha256_file(output_directory / name)
        for name in ARTIFACT_NAMES
    }


def artifact_sizes(output_directory: Path) -> dict[str, int]:
    return {
        name: (output_directory / name).stat().st_size
        for name in ARTIFACT_NAMES
    }


def ensure_clean_directory(path: Path, overwrite: bool) -> None:
    if path.exists():
        if not overwrite:
            raise FileExistsError(
                f"Output directory already exists: {path}. "
                "Use --overwrite-proof-output to replace it."
            )
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=False)


def run_projection(
    *,
    label: str,
    source: Path,
    output_directory: Path,
    config: dict[str, Any],
) -> RunReceipt:
    started = time.perf_counter()

    result = project_genotype_observations(
        annotated_vcf_path=source,
        output_directory=output_directory,
        sample_id=str(config["input"]["sample_id"]),
        sample_alias=str(config["input"].get("sample_alias") or "") or None,
        sra_accession=str(config["input"].get("sra_accession") or "") or None,
        run_id="engineering_fixture_hg002_100k_v1",
        reference_build=str(config["reference"]["genome_build"]),
        source_pipeline=str(
            config.get("project", {}).get(
                "pipeline_name",
                "variant_annotation_pipeline",
            )
        ),
        assay_type=str(config["input"].get("assay_type") or "") or None,
        explicit_vcf_sample_name="HG002",
        source_vcf_path_label=(
            "source/lightweight/HG002_genotype_development_100k.vcf"
        ),
        normalization_policy_id="vap_stage06_normalization_policy_v1",
        normalization_state="normalized_annotated_vcf",
    )

    elapsed = time.perf_counter() - started
    usage = resource.getrusage(resource.RUSAGE_SELF)

    return RunReceipt(
        label=label,
        output_directory=str(output_directory),
        elapsed_seconds=round(elapsed, 6),
        peak_rss_kib=int(usage.ru_maxrss),
        source_record_count=int(result["source_record_count"]),
        genotype_observation_row_count=int(result["row_count"]),
        projection_status=str(result["projection_status"]),
        artifact_sha256=artifact_hashes(output_directory),
        artifact_size_bytes=artifact_sizes(output_directory),
    )


def validate_run(
    *,
    source_record_count: int,
    receipt: RunReceipt,
) -> list[dict[str, Any]]:
    output_directory = Path(receipt.output_directory)
    summary = load_json(
        output_directory / "genotype_projection_summary.json"
    )
    tsv_rows = count_tsv_rows(
        output_directory / "genotype_observations.tsv"
    )

    checks: list[dict[str, Any]] = []

    def add(check: str, passed: bool, details: str) -> None:
        checks.append(
            {
                "check": check,
                "status": "PASS" if passed else "FAIL",
                "details": details,
            }
        )

    add(
        "source_record_count_matches_fixture",
        receipt.source_record_count == source_record_count,
        f"projector={receipt.source_record_count}; fixture={source_record_count}",
    )
    add(
        "tsv_row_count_matches_fixture",
        tsv_rows == source_record_count,
        f"tsv_rows={tsv_rows}; fixture={source_record_count}",
    )
    add(
        "summary_row_count_matches_fixture",
        summary["counts"]["genotype_observation_row_count"] == source_record_count,
        (
            "summary_rows="
            f"{summary['counts']['genotype_observation_row_count']}; "
            f"fixture={source_record_count}"
        ),
    )
    add(
        "summary_source_count_matches_fixture",
        summary["source_vcf"]["source_record_count"] == source_record_count,
        (
            "summary_source_records="
            f"{summary['source_vcf']['source_record_count']}; "
            f"fixture={source_record_count}"
        ),
    )
    add(
        "no_irreparably_malformed_records",
        summary["source_vcf"]["irreparably_malformed_record_count"] == 0,
        (
            "irreparably_malformed_record_count="
            f"{summary['source_vcf']['irreparably_malformed_record_count']}"
        ),
    )
    add(
        "three_artifact_set_complete",
        all(
            (output_directory / name).is_file()
            and (output_directory / name).stat().st_size > 0
            for name in ARTIFACT_NAMES
        ),
        ", ".join(
            f"{name}={(output_directory / name).stat().st_size}"
            for name in ARTIFACT_NAMES
        ),
    )
    add(
        "summary_tsv_checksum_matches",
        (
            summary["outputs"]["genotype_observations_sha256"]
            == receipt.artifact_sha256["genotype_observations.tsv"]
        ),
        (
            "summary="
            f"{summary['outputs']['genotype_observations_sha256']}; "
            "observed="
            f"{receipt.artifact_sha256['genotype_observations.tsv']}"
        ),
    )
    add(
        "summary_header_context_checksum_matches",
        (
            summary["outputs"]["header_context_sha256"]
            == receipt.artifact_sha256["genotype_source_header_context.json"]
        ),
        (
            "summary="
            f"{summary['outputs']['header_context_sha256']}; "
            "observed="
            f"{receipt.artifact_sha256['genotype_source_header_context.json']}"
        ),
    )

    return checks


def write_tsv(path: Path, rows: list[dict[str, Any]]) -> None:
    fields = ["check", "status", "details"]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run the HG002 100k genotype projection proof."
    )
    parser.add_argument(
        "--fixture-root",
        type=Path,
        default=DEFAULT_FIXTURE_ROOT,
    )
    parser.add_argument(
        "--source-vcf",
        type=Path,
        default=DEFAULT_SOURCE,
    )
    parser.add_argument(
        "--config-snapshot",
        type=Path,
        default=DEFAULT_CONFIG,
    )
    parser.add_argument(
        "--receipts-dir",
        type=Path,
        default=DEFAULT_RECEIPTS,
    )
    parser.add_argument(
        "--overwrite-proof-output",
        action="store_true",
    )
    args = parser.parse_args()

    if not Path("pipeline/genotype_projection.py").exists():
        raise FileNotFoundError(
            "Run from the VAP repository root after Wave 2."
        )

    source = args.source_vcf.expanduser().resolve()
    config_path = args.config_snapshot.expanduser().resolve()
    receipts_root = args.receipts_dir.expanduser().resolve()

    if not source.is_file():
        raise FileNotFoundError(f"Source fixture not found: {source}")
    if not config_path.is_file():
        raise FileNotFoundError(f"Config snapshot not found: {config_path}")

    proof_root = (
        args.fixture_root.expanduser().resolve()
        / "processed"
        / "hg002_100k_projection_proof"
    )
    run_one = proof_root / "run_1"
    run_two = proof_root / "run_2"

    ensure_clean_directory(
        proof_root,
        overwrite=args.overwrite_proof_output,
    )
    run_one.mkdir()
    run_two.mkdir()

    receipts_dir = (
        receipts_root
        / f"hg002_100k_projection_proof_{local_stamp()}"
    )
    receipts_dir.mkdir(parents=True, exist_ok=False)

    source_sha_before = sha256_file(source)
    source_size_before = source.stat().st_size
    source_record_count = count_vcf_records(source)
    config = load_yaml(config_path)

    first = run_projection(
        label="run_1",
        source=source,
        output_directory=run_one,
        config=config,
    )
    second = run_projection(
        label="run_2",
        source=source,
        output_directory=run_two,
        config=config,
    )

    source_sha_after = sha256_file(source)
    source_size_after = source.stat().st_size

    checks: list[dict[str, Any]] = []
    checks.extend(validate_run(
        source_record_count=source_record_count,
        receipt=first,
    ))
    checks.extend(validate_run(
        source_record_count=source_record_count,
        receipt=second,
    ))

    deterministic = first.artifact_sha256 == second.artifact_sha256
    checks.append(
        {
            "check": "three_artifact_outputs_are_byte_deterministic",
            "status": "PASS" if deterministic else "FAIL",
            "details": json.dumps(
                {
                    "run_1": first.artifact_sha256,
                    "run_2": second.artifact_sha256,
                },
                sort_keys=True,
            ),
        }
    )

    source_unchanged = (
        source_sha_before == source_sha_after
        and source_size_before == source_size_after
    )
    checks.append(
        {
            "check": "source_fixture_unchanged",
            "status": "PASS" if source_unchanged else "FAIL",
            "details": (
                f"sha_before={source_sha_before}; "
                f"sha_after={source_sha_after}; "
                f"size_before={source_size_before}; "
                f"size_after={source_size_after}"
            ),
        }
    )

    failures = [row for row in checks if row["status"] != "PASS"]
    overall = "PASS" if not failures else "FAIL"

    payload = {
        "proof_type": "hg002_100k_genotype_projection",
        "created_utc": utc_now(),
        "overall_status": overall,
        "fixture": {
            "source_vcf": str(source),
            "source_vcf_sha256_before": source_sha_before,
            "source_vcf_sha256_after": source_sha_after,
            "source_size_bytes": source_size_before,
            "source_record_count": source_record_count,
            "config_snapshot": str(config_path),
        },
        "runs": [asdict(first), asdict(second)],
        "checks": checks,
    }

    (receipts_dir / "hg002_100k_projection_proof.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    write_tsv(
        receipts_dir / "hg002_100k_projection_checks.tsv",
        checks,
    )

    summary_lines = [
        "# HG002 100k Genotype Projection Proof",
        "",
        f"Overall status: `{overall}`",
        "",
        "## Fixture",
        "",
        f"- Source VCF: `{source}`",
        f"- Source SHA-256: `{source_sha_before}`",
        f"- Source records: `{source_record_count}`",
        f"- Source size bytes: `{source_size_before}`",
        "",
        "## Projection Runs",
        "",
        "| Run | Seconds | Peak RSS KiB | Rows | Status |",
        "|---|---:|---:|---:|---|",
        (
            f"| {first.label} | {first.elapsed_seconds} | "
            f"{first.peak_rss_kib} | "
            f"{first.genotype_observation_row_count} | "
            f"{first.projection_status} |"
        ),
        (
            f"| {second.label} | {second.elapsed_seconds} | "
            f"{second.peak_rss_kib} | "
            f"{second.genotype_observation_row_count} | "
            f"{second.projection_status} |"
        ),
        "",
        "## Determinism",
        "",
        (
            "- Three-artifact SHA-256 equality: "
            f"`{'PASS' if deterministic else 'FAIL'}`"
        ),
        (
            "- Source fixture immutability: "
            f"`{'PASS' if source_unchanged else 'FAIL'}`"
        ),
        "",
        "## Artifact Sizes",
        "",
        "| Artifact | Size bytes |",
        "|---|---:|",
    ]
    for name in ARTIFACT_NAMES:
        summary_lines.append(
            f"| {name} | {first.artifact_size_bytes[name]} |"
        )

    summary_lines.extend([
        "",
        "## Interpretation",
        "",
        (
            "This is an engineering-fixture proof. It demonstrates "
            "real-data projection behavior, deterministic artifact "
            "generation, source immutability, and count reconciliation."
        ),
        "",
        (
            "It does not certify the canonical MARK HG002 VCF or the "
            "13-run production corpus."
        ),
        "",
    ])

    (receipts_dir / "hg002_100k_projection_summary.md").write_text(
        "\n".join(summary_lines),
        encoding="utf-8",
    )

    print("HG002 100k genotype projection proof complete.")
    print(f"  overall_status: {overall}")
    print(f"  source_records: {source_record_count}")
    print(f"  run_1_seconds: {first.elapsed_seconds}")
    print(f"  run_2_seconds: {second.elapsed_seconds}")
    print(f"  run_1_peak_rss_kib: {first.peak_rss_kib}")
    print(f"  run_2_peak_rss_kib: {second.peak_rss_kib}")
    print(f"  proof_outputs: {proof_root}")
    print(f"  receipts: {receipts_dir}")

    if failures:
        print("\nFailed checks:")
        for row in failures:
            print(f"  - {row['check']}: {row['details']}")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
