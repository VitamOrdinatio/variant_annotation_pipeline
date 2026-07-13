\
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

import pytest

from scripts.tep.build_vap_tep_lineage_manifest import (
    LINEAGE_EDGES,
    build_lineage_edges,
    build_lineage_manifest,
    entity_bundle_sha256,
    validate_inventory,
)


def _artifact(
    *,
    role: str,
    transport_path: str,
    sha256: str,
) -> dict:
    return {
        "entity_id": role,
        "entity_role": role,
        "source_stage": "fixture",
        "source_artifact_role": role,
        "source_artifact": f"/source/{Path(transport_path).name}",
        "transport_path": transport_path,
        "source_artifact_exists": True,
        "copied": True,
        "required": True,
        "size_bytes": 1,
        "row_count": None,
        "column_count": None,
        "variant_id_count": None,
        "observed_columns": None,
        "sha256": sha256,
    }


def _entity(
    role: str,
    *,
    artifacts: list[dict] | None = None,
    artifact_count: int = 1,
) -> dict:
    artifacts = artifacts or [
        _artifact(
            role=role,
            transport_path=f"entities/{role}/{role}.dat",
            sha256=hashlib.sha256(role.encode()).hexdigest(),
        )
    ]
    return {
        "entity_id": role,
        "entity_role": role,
        "source_stage": "fixture",
        "required": True,
        "artifact_count": artifact_count,
        "copied_artifacts": artifact_count,
        "missing_required_artifacts": 0,
        "metric_semantics": (
            "single_artifact_entity_metrics"
            if artifact_count == 1
            else "multi_artifact_entity_metrics_available_per_artifact"
        ),
        "total_size_bytes": artifact_count,
        "row_count": None,
        "column_count": None,
        "variant_id_count": None,
        "artifacts": artifacts,
        "artifact_metrics": {
            artifact["source_artifact_role"]: {
                "row_count": artifact["row_count"],
                "column_count": artifact["column_count"],
                "variant_id_count": artifact["variant_id_count"],
                "size_bytes": artifact["size_bytes"],
                "observed_columns": artifact["observed_columns"],
            }
            for artifact in artifacts
        },
    }


def _inventory(include_genotype: bool = False) -> dict:
    roles = [
        "observation_entity",
        "normalization_entity",
        "routing_entity",
        "coding_interpretation_overlay",
        "noncoding_interpretation_overlay",
        "prioritization_overlay",
        "validation_overlay",
        "context_sidecar",
        "package_metadata",
    ]
    entities = [_entity(role) for role in roles]

    if include_genotype:
        genotype_artifacts = [
            _artifact(
                role="genotype_observation_entity",
                transport_path="entities/genotype/genotype_observations.tsv",
                sha256="a" * 64,
            ),
            _artifact(
                role="genotype_observation_entity",
                transport_path=(
                    "entities/genotype/genotype_projection_summary.json"
                ),
                sha256="b" * 64,
            ),
            _artifact(
                role="genotype_observation_entity",
                transport_path=(
                    "entities/genotype/genotype_source_header_context.json"
                ),
                sha256="c" * 64,
            ),
        ]
        for index, artifact in enumerate(genotype_artifacts):
            artifact["source_artifact_role"] = [
                "genotype_observations",
                "genotype_projection_summary",
                "genotype_source_header_context",
            ][index]
        entities.append(
            _entity(
                "genotype_observation_entity",
                artifacts=genotype_artifacts,
                artifact_count=3,
            )
        )

    artifacts = [
        artifact
        for entity in entities
        for artifact in entity["artifacts"]
    ]

    return {
        "inventory_type": "vap_tep_entity_inventory",
        "inventory_schema_version": "0.1.0",
        "entity_builder_version": "0.3.0",
        "tep_id": "vap_tep_fixture",
        "tep_schema_version": "vap_tep_v1",
        "source_run": {
            "sample_id": "HG002",
            "run_id": "run_fixture",
            "run_directory": "/run",
            "processed_directory": "/run/processed",
            "metadata_directory": "/run/metadata",
        },
        "package": {
            "package_root": "/package",
            "package_format": "directory",
        },
        "entities": entities,
        "artifacts": artifacts,
    }


def _edge_tuples(edges: list[dict[str, str]]) -> set[tuple[str, str, str]]:
    return {
        (
            edge["parent_entity_id"],
            edge["child_entity_id"],
            edge["relationship"],
        )
        for edge in edges
    }


def test_legacy_lineage_remains_unchanged() -> None:
    roles = [
        "observation_entity",
        "normalization_entity",
        "routing_entity",
        "coding_interpretation_overlay",
        "noncoding_interpretation_overlay",
        "prioritization_overlay",
        "validation_overlay",
        "context_sidecar",
        "package_metadata",
    ]
    edges = build_lineage_edges(roles)
    observed = _edge_tuples(edges)

    assert (
        "observation_entity",
        "genotype_observation_entity",
        "projects_genotype",
    ) not in observed
    assert (
        "genotype_observation_entity",
        "lineage_manifest",
        "indexed_by",
    ) not in observed
    assert len(edges) == len(LINEAGE_EDGES) + len(roles)


def test_genotype_lineage_adds_exactly_two_edges() -> None:
    inventory = _inventory(include_genotype=True)
    roles = [entity["entity_role"] for entity in inventory["entities"]]
    edges = build_lineage_edges(roles)
    observed = _edge_tuples(edges)

    assert (
        "observation_entity",
        "genotype_observation_entity",
        "projects_genotype",
    ) in observed
    assert (
        "genotype_observation_entity",
        "lineage_manifest",
        "indexed_by",
    ) in observed
    assert len(edges) == len(LINEAGE_EDGES) + len(roles) + 1


def test_genotype_manifest_entity_is_complete(tmp_path: Path) -> None:
    inventory = _inventory(include_genotype=True)
    inventory_path = tmp_path / "entity_inventory.json"
    inventory_path.write_text(
        json.dumps(inventory),
        encoding="utf-8",
    )

    validate_inventory(inventory, inventory_path)
    manifest = build_lineage_manifest(inventory, inventory_path)

    genotype_entities = [
        entity
        for entity in manifest["entities"]
        if entity["entity_role"] == "genotype_observation_entity"
    ]
    assert len(genotype_entities) == 1

    genotype = genotype_entities[0]
    assert genotype["entity_id"] == "genotype_observation_entity"
    assert genotype["source_stage"] == "fixture"
    assert genotype["artifact_count"] == 3
    assert genotype["transport_paths"] == [
        "entities/genotype/genotype_observations.tsv",
        "entities/genotype/genotype_projection_summary.json",
        "entities/genotype/genotype_source_header_context.json",
    ]

    source_entity = next(
        entity
        for entity in inventory["entities"]
        if entity["entity_role"] == "genotype_observation_entity"
    )
    assert genotype["sha256"] == entity_bundle_sha256(source_entity)


def test_duplicate_genotype_entity_is_rejected(tmp_path: Path) -> None:
    inventory = _inventory(include_genotype=True)
    genotype = next(
        entity
        for entity in inventory["entities"]
        if entity["entity_role"] == "genotype_observation_entity"
    )
    duplicate = copy.deepcopy(genotype)
    inventory["entities"].append(duplicate)
    inventory["artifacts"].extend(copy.deepcopy(duplicate["artifacts"]))

    inventory_path = tmp_path / "entity_inventory.json"

    with pytest.raises(
        ValueError,
        match="Expected at most one genotype_observation_entity",
    ):
        validate_inventory(inventory, inventory_path)


def test_genotype_entity_requires_exactly_three_artifacts(
    tmp_path: Path,
) -> None:
    inventory = _inventory(include_genotype=True)
    genotype = next(
        entity
        for entity in inventory["entities"]
        if entity["entity_role"] == "genotype_observation_entity"
    )
    genotype["artifact_count"] = 2

    with pytest.raises(
        ValueError,
        match="exactly three artifacts",
    ):
        validate_inventory(
            inventory,
            tmp_path / "entity_inventory.json",
        )
