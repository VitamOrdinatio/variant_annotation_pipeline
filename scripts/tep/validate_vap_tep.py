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
import csv
import hashlib
import json
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from pipeline.genotype_projection import GENOTYPE_COLUMNS


VALIDATOR_VERSION = "0.4.0"

REQUIRED_ENTITY_ROLES = [
    "observation_entity",
    "normalization_entity",
    "routing_entity",
    "coding_interpretation_overlay",
    "noncoding_interpretation_overlay",
    "prioritization_overlay",
    "validation_overlay",
    "context_sidecar",
    "package_metadata",
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

SEMANTIC_SURFACE_REQUIREMENTS = {
    "AC-040": {
        "description": "Stage08 normalization semantic surface preserved",
        "artifact_roles": [
            "stage08_selected_transcript_consequences",
            "stage08_vdb_ready_variants",
        ],
        "required_columns": {
            "annotation_source",
            "annotation_version",
            "gene_mapping_status",
            "variant_context",
            "variant_effect_severity",
            "qc_status",
            "interpretability_status",
            "frequency_status",
            "clinical_status",
        },
    },
    "AC-041": {
        "description": "Stage09 coding interpretation semantic surface preserved",
        "artifact_roles": ["stage09_coding_interpreted"],
        "required_columns": {
            "functional_impact",
            "rarity_flag",
            "clinical_evidence",
            "qc_reliability",
            "coding_interpretation_label",
            "is_lof_candidate",
            "is_rare_candidate",
            "is_clinically_supported",
            "is_high_quality",
            "is_potential_artifact",
        },
    },
    "AC-042": {
        "description": "Stage10 noncoding interpretation semantic surface preserved",
        "artifact_roles": ["stage10_noncoding_interpreted"],
        "required_columns": {
            "noncoding_functional_context",
            "rarity_flag",
            "clinical_evidence",
            "qc_reliability",
            "noncoding_interpretation_label",
            "is_regulatory_candidate",
            "is_rare_candidate",
            "is_clinically_supported",
            "is_high_quality",
            "is_potential_artifact",
        },
    },
    "AC-043": {
        "description": "Stage11 prioritization semantic surface preserved",
        "artifact_roles": ["stage11_prioritized_variants"],
        "required_columns": {
            "variant_origin",
            "source_interpretation_label",
            "priority_tier",
            "priority_rank",
            "priority_reason",
            "is_high_priority_candidate",
            "is_moderate_priority_candidate",
            "is_low_priority_candidate",
            "is_uninterpretable",
        },
    },
    "AC-044": {
        "description": "Stage12 validation semantic surface preserved",
        "artifact_roles": ["stage12_validation_candidates"],
        "required_columns": {
            "validation_required",
            "validation_priority",
            "suggested_validation_method",
            "validation_reason",
        },
    },
}

GENOTYPE_ENTITY_ROLE = "genotype_observation_entity"

GENOTYPE_ARTIFACT_CONTRACT = {
    "genotype_observations": "entities/genotype/genotype_observations.tsv",
    "genotype_projection_summary": "entities/genotype/genotype_projection_summary.json",
    "genotype_source_header_context": "entities/genotype/genotype_source_header_context.json",
}

ACCEPTABLE_GENOTYPE_PROJECTION_STATUSES = {
    "pass",
    "pass_with_advisory",
    "pass_with_warnings",
}



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
        "package_metadata": "AC-045",
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


def check_semantic_surfaces(manifest: dict[str, Any]) -> list[ValidationCheck]:
    checks: list[ValidationCheck] = []

    artifact_metrics_by_role: dict[str, dict[str, Any]] = {}

    for entity in manifest.get("entities", []):
        artifact_metrics = entity.get("artifact_metrics", {})
        if isinstance(artifact_metrics, dict):
            for artifact_role, metrics in artifact_metrics.items():
                if isinstance(metrics, dict):
                    artifact_metrics_by_role[str(artifact_role)] = metrics

    for criterion, requirement in SEMANTIC_SURFACE_REQUIREMENTS.items():
        description = str(requirement["description"])
        artifact_roles = requirement["artifact_roles"]
        required_columns = set(requirement["required_columns"])

        failures: list[str] = []

        for artifact_role in artifact_roles:
            metrics = artifact_metrics_by_role.get(artifact_role)

            if metrics is None:
                failures.append(f"{artifact_role}: missing artifact_metrics")
                continue

            observed_columns = metrics.get("observed_columns")

            if not isinstance(observed_columns, list):
                failures.append(f"{artifact_role}: missing observed_columns")
                continue

            observed_column_set = set(str(column) for column in observed_columns)
            missing_columns = sorted(required_columns - observed_column_set)

            if missing_columns:
                failures.append(
                    f"{artifact_role}: missing columns {missing_columns}"
                )

        if failures:
            checks.append(
                fail_check(
                    criterion,
                    description,
                    "; ".join(failures),
                )
            )
        else:
            checks.append(
                pass_check(
                    criterion,
                    description,
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
        "AC-045": "package_metadata",
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



def _genotype_artifacts_by_role(entity: dict[str, Any]) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for artifact in entity.get("source_artifacts", []):
        if isinstance(artifact, dict):
            role = str(artifact.get("source_artifact_role", ""))
            if role:
                result[role] = artifact
    return result


def _read_genotype_tsv(path: Path) -> tuple[list[str], int, set[str], set[str]]:
    with path.open("r", encoding="utf-8", errors="replace", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        header = list(reader.fieldnames or [])
        rows = 0
        sample_ids: set[str] = set()
        run_ids: set[str] = set()
        for row in reader:
            rows += 1
            sample_id = str(row.get("sample_id", "")).strip()
            run_id = str(row.get("run_id", "")).strip()
            if sample_id:
                sample_ids.add(sample_id)
            if run_id:
                run_ids.add(run_id)
    return header, rows, sample_ids, run_ids


def check_genotype_capability(manifest: dict[str, Any], package_root: Path) -> list[ValidationCheck]:
    """Validate optional genotype capability; legacy packages emit no checks."""
    entities = entity_by_role(manifest).get(GENOTYPE_ENTITY_ROLE, [])
    if not entities:
        return []
    if len(entities) != 1:
        return [fail_check("AC-050", "Exactly one genotype observation entity exists", f"Observed: {len(entities)}")]

    checks: list[ValidationCheck] = []
    entity = entities[0]
    artifacts = _genotype_artifacts_by_role(entity)
    expected_roles = set(GENOTYPE_ARTIFACT_CONTRACT)
    failures: list[str] = []
    if entity.get("entity_id") != GENOTYPE_ENTITY_ROLE:
        failures.append(f"entity_id={entity.get('entity_id')}")
    if entity.get("artifact_count") != 3:
        failures.append(f"artifact_count={entity.get('artifact_count')}")
    if set(artifacts) != expected_roles:
        failures.append(f"artifact_roles={sorted(artifacts)}")
    checks.append(fail_check("AC-050", "Genotype entity structure is valid", "; ".join(failures)) if failures else pass_check("AC-050", "Genotype entity structure is valid"))

    path_failures: list[str] = []
    paths: dict[str, Path] = {}
    for role, expected in GENOTYPE_ARTIFACT_CONTRACT.items():
        artifact = artifacts.get(role)
        if artifact is None:
            path_failures.append(f"{role}: missing")
            continue
        observed = artifact.get("transport_path")
        if observed != expected:
            path_failures.append(f"{role}: expected {expected}, observed {observed}")
            continue
        path = package_root / expected
        paths[role] = path
        if not path.is_file():
            path_failures.append(f"{role}: transport file missing")
    if path_failures:
        checks.append(fail_check("AC-051", "Genotype artifact roles and transport paths are valid", "; ".join(path_failures)))
        return checks
    checks.append(pass_check("AC-051", "Genotype artifact roles and transport paths are valid"))

    observations = paths["genotype_observations"]
    summary_path = paths["genotype_projection_summary"]
    context_path = paths["genotype_source_header_context"]
    try:
        header, row_count, sample_ids, run_ids = _read_genotype_tsv(observations)
    except Exception as exc:
        checks.append(fail_check("AC-052", "Genotype observation schema is readable", str(exc)))
        return checks
    checks.append(pass_check("AC-052", "Genotype observation schema is canonical", f"columns={len(header)}") if header == GENOTYPE_COLUMNS else fail_check("AC-052", "Genotype observation schema is canonical", "Observed header differs from GENOTYPE_COLUMNS"))

    try:
        summary = load_json(summary_path)
        context = load_json(context_path)
    except Exception as exc:
        checks.append(fail_check("AC-053", "Genotype companion JSON artifacts are readable", str(exc)))
        return checks

    counts = summary.get("counts", {})
    source_count = counts.get("source_record_count")
    if source_count is None:
        source_count = summary.get("source_vcf", {}).get("source_record_count")
    summary_rows = counts.get("genotype_observation_row_count")
    count_failures=[]
    if summary_rows != row_count:
        count_failures.append(f"summary rows={summary_rows}; TSV rows={row_count}")
    if source_count != row_count:
        count_failures.append(f"source records={source_count}; TSV rows={row_count}")
    checks.append(fail_check("AC-053", "Genotype artifact row counts reconcile", "; ".join(count_failures)) if count_failures else pass_check("AC-053", "Genotype artifact row counts reconcile", f"rows={row_count}"))

    outputs = summary.get("outputs", {})
    checksum_failures=[]
    if outputs.get("genotype_observations_sha256") != sha256_file(observations):
        checksum_failures.append("genotype_observations checksum mismatch")
    if outputs.get("header_context_sha256") != sha256_file(context_path):
        checksum_failures.append("header_context checksum mismatch")
    checks.append(fail_check("AC-054", "Genotype summary checksums reconcile", "; ".join(checksum_failures)) if checksum_failures else pass_check("AC-054", "Genotype summary checksums reconcile"))

    source_run = manifest.get("source_run", {})
    package_sample = str(source_run.get("sample_id", ""))
    package_run = str(source_run.get("run_id", ""))
    identity_failures=[]
    if sample_ids != {package_sample}:
        identity_failures.append(f"TSV sample_ids={sorted(sample_ids)}; package={package_sample}")
    if run_ids != {package_run}:
        identity_failures.append(f"TSV run_ids={sorted(run_ids)}; package={package_run}")
    sample_resolution = summary.get("sample_resolution", {})
    if str(sample_resolution.get("sample_id", "")) != package_sample:
        identity_failures.append("summary sample_id mismatch")
    if str(sample_resolution.get("run_id", "")) != package_run:
        identity_failures.append("summary run_id mismatch")
    checks.append(fail_check("AC-055", "Genotype sample and run identity are coherent", "; ".join(identity_failures)) if identity_failures else pass_check("AC-055", "Genotype sample and run identity are coherent"))

    context_failures=[]
    if summary.get("schema_version") != "genotype_projection_summary_v1":
        context_failures.append("unexpected summary schema_version")
    if context.get("schema_version") != "genotype_source_header_context_v1":
        context_failures.append("unexpected header-context schema_version")
    reference_build = summary.get("projection", {}).get("reference_build")
    source_vcf = summary.get("source_vcf", {})
    if not reference_build:
        context_failures.append("reference_build missing")
    if not source_vcf.get("sha256"):
        context_failures.append("source VCF sha256 missing")
    if not source_vcf.get("header_hash"):
        context_failures.append("source header hash missing")
    checks.append(fail_check("AC-056", "Genotype source and header context are preserved", "; ".join(context_failures)) if context_failures else pass_check("AC-056", "Genotype source and header context are preserved", f"reference_build={reference_build}"))

    status = summary.get("projection", {}).get("projection_status")
    warning_count = counts.get("projection_warning_count", 0)
    checks.append(pass_check("AC-057", "Genotype projection status is transportable", f"status={status}; warning_count={warning_count}") if status in ACCEPTABLE_GENOTYPE_PROJECTION_STATUSES else fail_check("AC-057", "Genotype projection status is transportable", f"Observed: {status}"))

    required_edges = {
        ("observation_entity", "genotype_observation_entity", "projects_genotype"),
        ("genotype_observation_entity", "lineage_manifest", "indexed_by"),
    }
    missing = sorted(required_edges - edge_set(manifest))
    checks.append(fail_check("AC-058", "Genotype lineage branch is present", f"Missing edges: {missing}") if missing else pass_check("AC-058", "Genotype lineage branch is present"))
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
    checks.extend(check_semantic_surfaces(manifest))
    checks.extend(check_preservation_context(manifest))
    checks.extend(check_genotype_capability(manifest, package_root))

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