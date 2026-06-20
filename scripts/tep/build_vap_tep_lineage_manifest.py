#!/usr/bin/env python3
"""
Build VAP-TEP lineage manifest from entity_inventory.json.

Input:
    <vap_tep_package>/entity_inventory.json

Output:
    <vap_tep_package>/lineage_manifest.json

    
Example usage on MARK:

```bash
cd ~/dev/portfolio_projects/variant_annotation_pipeline
git pull --ff-only

python scripts/tep/build_vap_tep_lineage_manifest.py \
  --inventory results/run_2026_06_03_010030/tep/vap_tep_HG002_run_2026_06_03_010030_v1/entity_inventory.json
```        
    
"""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


MANIFEST_SCHEMA_VERSION = "0.1.0"
LINEAGE_BUILDER_VERSION = "0.1.0"

REQUIRED_ENTITY_ROLES = [
    "observation_entity",
    "normalization_entity",
    "routing_entity",
    "coding_interpretation_overlay",
    "noncoding_interpretation_overlay",
    "prioritization_overlay",
    "validation_overlay",
    "context_sidecar",
]

LINEAGE_EDGES = [
    ("observation_entity", "normalization_entity", "normalizes"),
    ("normalization_entity", "routing_entity", "routes"),
    ("routing_entity", "coding_interpretation_overlay", "interprets_coding"),
    ("routing_entity", "noncoding_interpretation_overlay", "interprets_noncoding"),
    ("coding_interpretation_overlay", "prioritization_overlay", "prioritizes"),
    ("noncoding_interpretation_overlay", "prioritization_overlay", "prioritizes"),
    ("prioritization_overlay", "validation_overlay", "prepares_validation"),
    ("validation_overlay", "context_sidecar", "contextualizes"),
]


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


def update_lineage_manifest_entity_sha256(
    manifest: dict[str, Any],
    manifest_sha256: str,
) -> None:
    for entity in manifest["entities"]:
        if entity.get("entity_id") == "lineage_manifest":
            entity["sha256"] = manifest_sha256
            return

    raise ValueError("lineage_manifest entity not found.")


def validate_inventory(inventory: dict[str, Any], inventory_path: Path) -> None:
    if inventory.get("inventory_type") != "vap_tep_entity_inventory":
        raise ValueError(
            f"Invalid inventory_type in {inventory_path}: "
            f"{inventory.get('inventory_type')}"
        )

    for key in ["tep_id", "tep_schema_version", "source_run", "package", "entities", "artifacts"]:
        if key not in inventory:
            raise ValueError(f"Missing required inventory key: {key}")

    entities = inventory.get("entities")
    if not isinstance(entities, list):
        raise ValueError("Inventory field 'entities' must be a list.")

    observed_roles = {
        entity.get("entity_role")
        for entity in entities
        if isinstance(entity, dict)
    }

    missing_roles = [
        role for role in REQUIRED_ENTITY_ROLES
        if role not in observed_roles
    ]

    if missing_roles:
        raise ValueError(f"Missing required entity roles: {missing_roles}")

    missing_artifacts = [
        artifact
        for artifact in inventory.get("artifacts", [])
        if artifact.get("required") is True
        and artifact.get("source_artifact_exists") is not True
    ]

    if missing_artifacts:
        roles = [
            artifact.get("source_artifact_role", "unknown")
            for artifact in missing_artifacts
        ]
        raise ValueError(f"Missing required source artifacts: {roles}")


def entity_sha256(entity: dict[str, Any]) -> str | None:
    artifacts = entity.get("artifacts", [])
    if not isinstance(artifacts, list) or len(artifacts) != 1:
        return None
    value = artifacts[0].get("sha256")
    return str(value) if value else None


def entity_transport_paths(entity: dict[str, Any]) -> list[str]:
    paths: list[str] = []
    for artifact in entity.get("artifacts", []):
        path = artifact.get("transport_path")
        if path:
            paths.append(str(path))
    return paths


def entity_source_artifacts(entity: dict[str, Any]) -> list[dict[str, Any]]:
    source_artifacts: list[dict[str, Any]] = []

    for artifact in entity.get("artifacts", []):
        source_artifacts.append(
            {
                "source_artifact": artifact.get("source_artifact"),
                "source_artifact_role": artifact.get("source_artifact_role"),
                "source_artifact_sha256": artifact.get("sha256"),
                "source_artifact_exists": artifact.get("source_artifact_exists"),
                "source_artifact_rows": artifact.get("row_count"),
                "source_artifact_columns": artifact.get("column_count"),
                "source_artifact_variant_id_count": artifact.get("variant_id_count"),
                "transport_path": artifact.get("transport_path"),
                "size_bytes": artifact.get("size_bytes"),
            }
        )

    return source_artifacts


def build_manifest_entities(inventory: dict[str, Any]) -> list[dict[str, Any]]:
    manifest_entities: list[dict[str, Any]] = []

    for entity in inventory["entities"]:
        manifest_entities.append(
            {
                "entity_id": entity["entity_id"],
                "entity_role": entity["entity_role"],
                "source_stage": entity["source_stage"],
                "required": entity["required"],
                "artifact_count": entity["artifact_count"],
                "transport_paths": entity_transport_paths(entity),
                "source_artifacts": entity_source_artifacts(entity),
                "row_count": entity.get("row_count"),
                "column_count": entity.get("column_count"),
                "variant_id_count": entity.get("variant_id_count"),
                "metric_semantics": entity.get("metric_semantics"),
                "artifact_metrics": entity.get("artifact_metrics"),
                "total_size_bytes": entity.get("total_size_bytes"),
                "sha256": entity_sha256(entity),
            }
        )

    manifest_entities.append(
        {
            "entity_id": "lineage_manifest",
            "entity_role": "lineage_manifest",
            "source_stage": "tep_construction",
            "required": True,
            "artifact_count": 1,
            "transport_paths": ["lineage_manifest.json"],
            "source_artifacts": [],
            "row_count": None,
            "column_count": None,
            "variant_id_count": None,
            "metric_semantics": "metadata_entity",
            "artifact_metrics": {},
            "total_size_bytes": None,
            "sha256": None,
        }
    )

    return manifest_entities


def build_lineage_edges() -> list[dict[str, str]]:
    edges: list[dict[str, str]] = []

    for parent, child, relationship in LINEAGE_EDGES:
        edges.append(
            {
                "parent_entity_id": parent,
                "child_entity_id": child,
                "relationship": relationship,
                "validation_basis": "vap_tep_contract_v1",
            }
        )

    for role in REQUIRED_ENTITY_ROLES:
        edges.append(
            {
                "parent_entity_id": role,
                "child_entity_id": "lineage_manifest",
                "relationship": "indexed_by",
                "validation_basis": "vap_tep_transport_requirements_v1",
            }
        )

    return edges


def build_lineage_manifest(inventory: dict[str, Any], inventory_path: Path) -> dict[str, Any]:
    package_root = inventory_path.parent

    return {
        "manifest_type": "vap_tep_lineage_manifest",
        "manifest_schema_version": MANIFEST_SCHEMA_VERSION,
        "lineage_builder_version": LINEAGE_BUILDER_VERSION,
        "tep_id": inventory["tep_id"],
        "tep_schema_version": inventory["tep_schema_version"],
        "producer": {
            "repository": "variant_annotation_pipeline",
            "pipeline": "VAP",
            "producer_version": inventory.get("entity_builder_version", "unknown"),
            "created_utc": utc_now(),
        },
        "source_run": inventory["source_run"],
        "package": {
            "package_root": str(package_root),
            "package_format": inventory.get("package", {}).get("package_format", "directory"),
            "self_describing": True,
        },
        "entities": build_manifest_entities(inventory),
        "lineage_edges": build_lineage_edges(),
        "validation_summary": {
            "validation_status": "not_validated",
            "criteria_version": "vap_tep_acceptance_criteria_v1",
            "criteria_passed": [],
            "criteria_failed": [],
            "validated_utc": None,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build VAP-TEP lineage_manifest.json from entity_inventory.json."
    )
    parser.add_argument(
        "--inventory",
        type=Path,
        required=True,
        help="Path to entity_inventory.json",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Optional output path. Defaults to <package_root>/lineage_manifest.json",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing lineage_manifest.json.",
    )
    args = parser.parse_args()

    inventory_path = args.inventory.expanduser().resolve()
    output_path = (
        args.output.expanduser().resolve()
        if args.output
        else inventory_path.parent / "lineage_manifest.json"
    )

    if output_path.exists() and not args.overwrite:
        raise FileExistsError(
            f"Output already exists: {output_path}. Use --overwrite to replace it."
        )

    inventory = load_json(inventory_path)
    validate_inventory(inventory, inventory_path)

    manifest = build_lineage_manifest(inventory, inventory_path)
    write_json(output_path, manifest)

    manifest_sha256 = sha256_file(output_path)
    update_lineage_manifest_entity_sha256(manifest, manifest_sha256)
    write_json(output_path, manifest)

    print("VAP-TEP lineage manifest construction complete.")
    print(f"  inventory: {inventory_path}")
    print(f"  output: {output_path}")
    print(f"  tep_id: {manifest['tep_id']}")
    print(f"  entities: {len(manifest['entities'])}")
    print(f"  lineage_edges: {len(manifest['lineage_edges'])}")
    print(f"  validation_status: {manifest['validation_summary']['validation_status']}")


if __name__ == "__main__":
    main()