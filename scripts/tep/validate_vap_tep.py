#!/usr/bin/env python3
"""
Validate a VAP Transitional Evidence Product (VAP-TEP) package.

Validation source of truth:
    lineage_manifest.json

This v0.1 validator checks:
  - manifest structure
  - required identifiers
  - required entity roles
  - entity role cardinality
  - source artifact provenance
  - transport path existence
  - transported artifact SHA256 integrity
  - required lineage edges
  - Stage07 -> Stage08 continuity using artifact-level metrics
  - validation_summary update

This validator does not yet inspect TSV headers for required semantic fields.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


VALIDATOR_VERSION = "0.1.0"

REQUIRED_ENTITY_ROLES = [
    "observation_entity",
    "normalization_entity",
    "routing_entity",
    "coding_interpretation_overlay",
    "noncoding_interpretation_overlay",
    "prioritization_overlay",
    "validation_overlay",
    "context_sidecar",
    "lineage_manifest",
]

REQUIRED_LINEAGE_EDGES = [
    ("observation_entity", "normalization_entity", "normalizes"),
    ("normalization_entity", "routing_entity", "routes"),
    ("routing_entity", "coding_interpretation_overlay", "interprets_coding"),
    ("routing_entity", "noncoding_interpretation_overlay", "interprets_noncoding"),
    ("coding_interpretation_overlay", "prioritization_overlay", "prioritizes"),
    ("noncoding_interpretation_overlay", "prioritization_overlay", "prioritizes"),
    ("prioritization_overlay", "validation_overlay", "prepares_validation"),
    ("validation_overlay", "context_sidecar", "contextualizes"),
]

REQUIRED_INDEXED_BY_EDGES = [
    (role, "lineage_manifest", "indexed_by")
    for role in REQUIRED_ENTITY_ROLES
    if role != "lineage_manifest"
]


@dataclass
class ValidationCheck:
    criterion: str
    description: str
    status: str
    details: str


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise ValueError(f"Expected JSON object: {path}")
    return payload


def write_json(path: Path, payload: dict[str, Any]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
        handle.write("\n")


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while True:
            chunk = handle.read(chunk_size)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def pass_check(criterion: str, description: str, details: str = "") -> ValidationCheck:
    return ValidationCheck(
        criterion=criterion,
        description=description,
        status="PASS",
        details=details,
    )


def fail_check(criterion: str, description: str, details: str) -> ValidationCheck:
    return ValidationCheck(
        criterion=criterion,
        description=description,
        status="FAIL",
        details=details,
    )


def entity_by_role(manifest: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for entity in manifest.get("entities", []):
        if isinstance(entity, dict):
            role = str(entity.get("entity_role", ""))
            grouped.setdefault(role, []).append(entity)
    return grouped


def edge_set(manifest: dict[str, Any]) -> set[tuple[str, str, str]]:
    edges: set[tuple[str, str, str]] = set()
    for edge in manifest.get("lineage_edges", []):
        if isinstance(edge, dict):
            edges.add(
                (
                    str(edge.get("parent_entity_id", "")),
                    str(edge.get("child_entity_id", "")),
                    str(edge.get("relationship", "")),
                )
            )
    return edges


def check_manifest_structure(manifest: dict[str, Any]) -> list[ValidationCheck]:
    checks: list[ValidationCheck] = []

    required_keys = [
        "manifest_type",
        "manifest_schema_version",
        "tep_id",
        "tep_schema_version",
        "producer",
        "source_run",
        "package",
        "entities",
        "lineage_edges",
        "validation_summary",
    ]

    missing = [key for key in required_keys if key not in manifest]
    if missing:
        checks.append(
            fail_check(
                "STRUCTURE-001",
                "Required top-level manifest keys present",
                f"Missing keys: {missing}",
            )
        )
    else:
        checks.append(
            pass_check(
                "STRUCTURE-001",
                "Required top-level manifest keys present",
            )
        )

    if manifest.get("manifest_type") == "vap_tep_lineage_manifest":
        checks.append(pass_check("STRUCTURE-002", "Manifest type is valid"))
    else:
        checks.append(
            fail_check(
                "STRUCTURE-002",
                "Manifest type is valid",
                f"Observed: {manifest.get('manifest_type')}",
            )
        )

    if isinstance(manifest.get("entities"), list):
        checks.append(pass_check("STRUCTURE-003", "Entities field is a list"))
    else:
        checks.append(
            fail_check(
                "STRUCTURE-003",
                "Entities field is a list",
                "entities is not a list",
            )
        )

    if isinstance(manifest.get("lineage_edges"), list):
        checks.append(pass_check("STRUCTURE-004", "Lineage edges field is a list"))
    else:
        checks.append(
            fail_check(
                "STRUCTURE-004",
                "Lineage edges field is a list",
                "lineage_edges is not a list",
            )
        )

    return checks


def check_required_identifiers(manifest: dict[str, Any]) -> list[ValidationCheck]:
    checks: list[ValidationCheck] = []

    for criterion, key in [
        ("AC-010", "tep_id"),
        ("AC-013A", "tep_schema_version"),
    ]:
        value = manifest.get(key)
        if isinstance(value, str) and value:
            checks.append(pass_check(criterion, f"{key} present", value))
        else:
            checks.append(fail_check(criterion, f"{key} present", f"Observed: {value}"))

    source_run = manifest.get("source_run", {})
    if not isinstance(source_run, dict):
        source_run = {}

    for criterion, key in [
        ("AC-011", "sample_id"),
        ("AC-012", "run_id"),
    ]:
        value = source_run.get(key)
        if isinstance(value, str) and value:
            checks.append(pass_check(criterion, f"{key} present", value))
        else:
            checks.append(fail_check(criterion, f"{key} present", f"Observed: {value}"))

    return checks


def check_required_entities(manifest: dict[str, Any]) -> list[ValidationCheck]:
    checks: list[ValidationCheck] = []
    grouped = entity_by_role(manifest)

    criterion_map = {
        "observation_entity": "AC-001",
        "normalization_entity": "AC-002",
        "routing_entity": "AC-003",
        "coding_interpretation_overlay": "AC-004",
        "noncoding_interpretation_overlay": "AC-005",
        "prioritization_overlay": "AC-006",
        "validation_overlay": "AC-007",
        "lineage_manifest": "AC-008",
        "context_sidecar": "AC-009",
    }

    for role in REQUIRED_ENTITY_ROLES:
        criterion = criterion_map.get(role, "ENTITY")
        observed = grouped.get(role, [])
        if observed:
            checks.append(pass_check(criterion, f"{role} present"))
        else:
            checks.append(fail_check(criterion, f"{role} present", "Missing"))

    cardinality_failures = {
        role: len(grouped.get(role, []))
        for role in REQUIRED_ENTITY_ROLES
        if len(grouped.get(role, [])) != 1
    }

    if cardinality_failures:
        checks.append(
            fail_check(
                "AC-017A",
                "Exactly one instance of each required entity role exists",
                f"Cardinality failures: {cardinality_failures}",
            )
        )
    else:
        checks.append(
            pass_check(
                "AC-017A",
                "Exactly one instance of each required entity role exists",
            )
        )

    return checks


def check_entity_roles(manifest: dict[str, Any]) -> list[ValidationCheck]:
    checks: list[ValidationCheck] = []

    missing_entity_role = [
        entity.get("entity_id", "unknown")
        for entity in manifest.get("entities", [])
        if not entity.get("entity_role")
    ]

    if missing_entity_role:
        checks.append(
            fail_check(
                "AC-017",
                "Every entity declares entity_role",
                f"Missing entity_role for: {missing_entity_role}",
            )
        )
    else:
        checks.append(pass_check("AC-017", "Every entity declares entity_role"))

    return checks


def check_provenance(manifest: dict[str, Any]) -> list[ValidationCheck]:
    checks: list[ValidationCheck] = []
    failures: list[str] = []

    for entity in manifest.get("entities", []):
        role = entity.get("entity_role")
        if role == "lineage_manifest":
            continue

        source_artifacts = entity.get("source_artifacts")
        if not isinstance(source_artifacts, list) or not source_artifacts:
            failures.append(f"{role}: missing source_artifacts")
            continue

        for artifact in source_artifacts:
            if not artifact.get("source_artifact"):
                failures.append(f"{role}: missing source_artifact")
            if not artifact.get("source_artifact_role"):
                failures.append(f"{role}: missing source_artifact_role")
            if not artifact.get("source_artifact_sha256"):
                failures.append(f"{role}: missing source_artifact_sha256")

    if failures:
        checks.append(
            fail_check(
                "AC-014",
                "Every entity preserves source artifact provenance",
                "; ".join(failures),
            )
        )
    else:
        checks.append(
            pass_check(
                "AC-014",
                "Every entity preserves source artifact provenance",
            )
        )

    return checks


def check_transport_paths_and_hashes(
    manifest: dict[str, Any],
    package_root: Path,
) -> list[ValidationCheck]:
    checks: list[ValidationCheck] = []
    path_failures: list[str] = []
    hash_failures: list[str] = []

    for entity in manifest.get("entities", []):
        for transport_path in entity.get("transport_paths", []):
            path = package_root / transport_path
            if not path.exists():
                path_failures.append(str(transport_path))

    for entity in manifest.get("entities", []):
        if entity.get("entity_role") == "lineage_manifest":
            continue

        for artifact in entity.get("source_artifacts", []):
            transport_path = artifact.get("transport_path")
            expected_sha = artifact.get("source_artifact_sha256")

            if not transport_path or not expected_sha:
                continue

            path = package_root / str(transport_path)
            if not path.exists():
                continue

            observed_sha = sha256_file(path)
            if observed_sha != expected_sha:
                hash_failures.append(
                    f"{transport_path}: expected {expected_sha}, observed {observed_sha}"
                )

    if path_failures:
        checks.append(
            fail_check(
                "AC-026",
                "Transport paths exist within package",
                f"Missing paths: {path_failures}",
            )
        )
    else:
        checks.append(pass_check("AC-026", "Transport paths exist within package"))

    if hash_failures:
        checks.append(
            fail_check(
                "AC-024",
                "Transported artifact SHA256 values match manifest",
                "; ".join(hash_failures),
            )
        )
    else:
        checks.append(
            pass_check(
                "AC-024",
                "Transported artifact SHA256 values match manifest",
            )
        )

    return checks


def check_lineage_edges(manifest: dict[str, Any]) -> list[ValidationCheck]:
    checks: list[ValidationCheck] = []
    observed = edge_set(manifest)

    missing_required = [
        edge for edge in REQUIRED_LINEAGE_EDGES
        if edge not in observed
    ]

    missing_indexed = [
        edge for edge in REQUIRED_INDEXED_BY_EDGES
        if edge not in observed
    ]

    if missing_required:
        checks.append(
            fail_check(
                "AC-015/AC-016",
                "Required parent/child lineage edges present",
                f"Missing lineage edges: {missing_required}",
            )
        )
    else:
        checks.append(
            pass_check(
                "AC-015/AC-016",
                "Required parent/child lineage edges present",
            )
        )

    if missing_indexed:
        checks.append(
            fail_check(
                "AC-027",
                "Lineage manifest indexes all required entities",
                f"Missing indexed_by edges: {missing_indexed}",
            )
        )
    else:
        checks.append(
            pass_check(
                "AC-027",
                "Lineage manifest indexes all required entities",
            )
        )

    return checks


def get_entity(manifest: dict[str, Any], role: str) -> dict[str, Any] | None:
    matches = [
        entity for entity in manifest.get("entities", [])
        if entity.get("entity_role") == role
    ]
    if len(matches) != 1:
        return None
    return matches[0]


def check_stage07_stage08_continuity(manifest: dict[str, Any]) -> list[ValidationCheck]:
    checks: list[ValidationCheck] = []

    observation = get_entity(manifest, "observation_entity")
    normalization = get_entity(manifest, "normalization_entity")

    if observation is None or normalization is None:
        return [
            fail_check(
                "AC-018",
                "Observation and normalization entities remain linked",
                "Observation or normalization entity missing",
            )
        ]

    obs_metrics = observation.get("artifact_metrics", {}).get("stage07_annotated_variants")
    norm_metrics = normalization.get("artifact_metrics", {})

    if not isinstance(obs_metrics, dict):
        return [
            fail_check(
                "AC-018",
                "Observation and normalization entities remain linked",
                "Missing stage07_annotated_variants metrics",
            )
        ]

    required_norm_roles = [
        "stage08_selected_transcript_consequences",
        "stage08_vdb_ready_variants",
    ]

    missing_norm = [
        role for role in required_norm_roles
        if role not in norm_metrics
    ]

    if missing_norm:
        return [
            fail_check(
                "AC-018",
                "Observation and normalization entities remain linked",
                f"Missing normalization metrics: {missing_norm}",
            )
        ]

    failures: list[str] = []

    for role in required_norm_roles:
        metrics = norm_metrics[role]
        for key in ["row_count", "variant_id_count"]:
            if obs_metrics.get(key) != metrics.get(key):
                failures.append(
                    f"{role}.{key}: observed {metrics.get(key)} "
                    f"!= stage07 {obs_metrics.get(key)}"
                )

    if failures:
        checks.append(
            fail_check(
                "AC-018",
                "Stage07 observation lineage remains traceable into Stage08 normalization lineage",
                "; ".join(failures),
            )
        )
    else:
        checks.append(
            pass_check(
                "AC-018",
                "Stage07 observation lineage remains traceable into Stage08 normalization lineage",
                "VAP v1 row_count and variant_id_count parity confirmed",
            )
        )

    return checks


def check_preservation_context(manifest: dict[str, Any]) -> list[ValidationCheck]:
    checks: list[ValidationCheck] = []

    required_roles = {
        "AC-029": "observation_entity",
        "AC-030": "normalization_entity",
        "AC-031A": "coding_interpretation_overlay",
        "AC-032": "prioritization_overlay",
        "AC-033": "validation_overlay",
    }

    grouped = entity_by_role(manifest)

    for criterion, role in required_roles.items():
        if grouped.get(role):
            checks.append(pass_check(criterion, f"{role} preserved"))
        else:
            checks.append(fail_check(criterion, f"{role} preserved", "Missing"))

    if grouped.get("coding_interpretation_overlay") and grouped.get("noncoding_interpretation_overlay"):
        checks.append(
            pass_check(
                "AC-031B",
                "Coding and noncoding interpretation overlays remain present",
            )
        )
    else:
        checks.append(
            fail_check(
                "AC-031B",
                "Coding and noncoding interpretation overlays remain present",
                "One or both interpretation overlays missing",
            )
        )

    if (
        not grouped.get("observation_entity")
        and not grouped.get("normalization_entity")
        and grouped.get("prioritization_overlay")
        and grouped.get("validation_overlay")
    ):
        checks.append(
            fail_check(
                "AC-028",
                "Candidate-only preservation prohibited",
                "Package appears candidate-only.",
            )
        )
    else:
        checks.append(
            pass_check(
                "AC-028",
                "Candidate-only preservation prohibited",
            )
        )

    return checks


def update_validation_summary(
    manifest: dict[str, Any],
    checks: list[ValidationCheck],
) -> None:
    passed = [check.criterion for check in checks if check.status == "PASS"]
    failed = [check.criterion for check in checks if check.status == "FAIL"]

    manifest["validation_summary"] = {
        "validation_status": "pass" if not failed else "fail",
        "criteria_version": "vap_tep_acceptance_criteria_v1",
        "criteria_passed": passed,
        "criteria_failed": failed,
        "validated_utc": utc_now(),
        "validator_version": VALIDATOR_VERSION,
    }


def write_validation_report(
    path: Path,
    checks: list[ValidationCheck],
    status: str,
) -> None:
    lines = [
        "# VAP-TEP Validation Report",
        "",
        f"Validation status: `{status}`",
        "",
        "| Criterion | Status | Description | Details |",
        "|---|---|---|---|",
    ]

    for check in checks:
        details = check.details.replace("|", "\\|") if check.details else ""
        lines.append(
            f"| {check.criterion} | {check.status} | {check.description} | {details} |"
        )

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def validate_vap_tep(
    manifest_path: Path,
    write_updated_manifest: bool,
) -> tuple[dict[str, Any], list[ValidationCheck]]:
    manifest = load_json(manifest_path)

    package_root = manifest_path.parent

    checks: list[ValidationCheck] = []
    checks.extend(check_manifest_structure(manifest))
    checks.extend(check_required_identifiers(manifest))
    checks.extend(check_required_entities(manifest))
    checks.extend(check_entity_roles(manifest))
    checks.extend(check_provenance(manifest))
    checks.extend(check_transport_paths_and_hashes(manifest, package_root))
    checks.extend(check_lineage_edges(manifest))
    checks.extend(check_stage07_stage08_continuity(manifest))
    checks.extend(check_preservation_context(manifest))

    update_validation_summary(manifest, checks)

    if write_updated_manifest:
        write_json(manifest_path, manifest)

    return manifest, checks


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate a VAP-TEP package using lineage_manifest.json."
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        required=True,
        help="Path to lineage_manifest.json",
    )
    parser.add_argument(
        "--write-updated-manifest",
        action="store_true",
        help="Write validation_summary back into lineage_manifest.json.",
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=None,
        help="Optional Markdown validation report output path.",
    )
    args = parser.parse_args()

    manifest_path = args.manifest.expanduser().resolve()
    manifest, checks = validate_vap_tep(
        manifest_path=manifest_path,
        write_updated_manifest=args.write_updated_manifest,
    )

    status = manifest["validation_summary"]["validation_status"]

    if args.report:
        write_validation_report(args.report.expanduser().resolve(), checks, status)

    failed = [check for check in checks if check.status == "FAIL"]

    print("VAP-TEP validation complete.")
    print(f"  manifest: {manifest_path}")
    print(f"  validation_status: {status}")
    print(f"  checks: {len(checks)}")
    print(f"  passed: {len(checks) - len(failed)}")
    print(f"  failed: {len(failed)}")

    if failed:
        print("\nFailed checks:")
        for check in failed:
            print(f"  - {check.criterion}: {check.description} :: {check.details}")
        sys.exit(1)


if __name__ == "__main__":
    main()