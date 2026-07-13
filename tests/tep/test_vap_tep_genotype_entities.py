\
from __future__ import annotations

import json
from pathlib import Path

import pytest

from scripts.tep.build_vap_tep_entities import (
    BASE_ARTIFACT_SPECS,
    GENOTYPE_ARTIFACT_SPECS,
    build_entities,
    resolve_artifact_specs,
)


def _write_required_sources(run_dir: Path) -> None:
    processed = run_dir / "processed"
    metadata = run_dir / "metadata"
    processed.mkdir(parents=True)
    metadata.mkdir(parents=True)

    tsv_header = "sample_id\trun_id\tvariant_id\n"
    tsv_row = "HG002\trun_test\t1:100:A:C\n"

    sources = {
        "HG002_run_test.annotated_variants.tsv": tsv_header + tsv_row,
        "stage_08_selected_transcript_consequences.tsv": tsv_header + tsv_row,
        "stage_08_vdb_ready_variants.tsv": tsv_header + tsv_row,
        "coding_candidates.tsv": tsv_header + tsv_row,
        "splice_region_candidates.tsv": tsv_header + tsv_row,
        "noncoding_candidates.tsv": tsv_header + tsv_row,
        "stage_09_coding_interpreted.tsv": tsv_header + tsv_row,
        "stage_10_noncoding_interpreted.tsv": tsv_header + tsv_row,
        "stage_11_prioritized_variants.tsv": tsv_header + tsv_row,
        "stage_12_validation_candidates.tsv": tsv_header + tsv_row,
        "stage_13_final_summary.json": "{}\n",
        "stage_13_artifact_manifest.json": "{}\n",
        "stage_13_run_report.md": "# Run\n",
    }
    for filename, content in sources.items():
        (processed / filename).write_text(content, encoding="utf-8")

    (metadata / "config_snapshot.yaml").write_text(
        "reference:\n  genome_build: GRCh38\n",
        encoding="utf-8",
    )


def _write_genotype_set(processed: Path) -> None:
    (processed / "genotype_observations.tsv").write_text(
        "genotype_observation_id\tsample_id\trun_id\tvariant_id\n"
        "go_1\tHG002\trun_test\t1:100:A:C\n",
        encoding="utf-8",
    )
    (processed / "genotype_projection_summary.json").write_text(
        json.dumps(
            {
                "schema_version": "genotype_projection_summary_v1",
                "projection": {"projection_status": "pass"},
                "counts": {
                    "source_record_count": 1,
                    "genotype_observation_row_count": 1,
                },
            },
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    (processed / "genotype_source_header_context.json").write_text(
        json.dumps(
            {
                "schema_version": "genotype_source_header_context_v1",
                "sample_columns": ["HG002"],
            },
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )


def test_legacy_run_omits_optional_genotype_entity(tmp_path: Path) -> None:
    processed = tmp_path / "processed"
    processed.mkdir()

    specs = resolve_artifact_specs(processed)

    assert specs == list(BASE_ARTIFACT_SPECS)
    assert not any(
        spec.entity_role == "genotype_observation_entity"
        for spec in specs
    )


def test_partial_genotype_set_is_rejected(tmp_path: Path) -> None:
    processed = tmp_path / "processed"
    processed.mkdir()
    (processed / "genotype_observations.tsv").write_text(
        "genotype_observation_id\n",
        encoding="utf-8",
    )

    with pytest.raises(
        FileNotFoundError,
        match="Incomplete genotype projection artifact set",
    ):
        resolve_artifact_specs(processed)


def test_complete_genotype_set_selects_all_three_specs(
    tmp_path: Path,
) -> None:
    processed = tmp_path / "processed"
    processed.mkdir()
    _write_genotype_set(processed)

    specs = resolve_artifact_specs(processed)
    genotype_specs = [
        spec
        for spec in specs
        if spec.entity_role == "genotype_observation_entity"
    ]

    assert genotype_specs == list(GENOTYPE_ARTIFACT_SPECS)
    assert len(genotype_specs) == 3
    assert {
        spec.entity_subdir
        for spec in genotype_specs
    } == {"genotype"}


def test_fresh_build_copies_complete_genotype_entity(
    tmp_path: Path,
) -> None:
    run_dir = tmp_path / "run_test"
    _write_required_sources(run_dir)
    _write_genotype_set(run_dir / "processed")

    package_root = build_entities(
        run_dir=run_dir,
        output_root=tmp_path / "tep_output",
        dry_run=False,
        overwrite=False,
    )

    genotype_dir = package_root / "entities" / "genotype"
    assert {
        path.name
        for path in genotype_dir.iterdir()
        if path.is_file()
    } == {
        "genotype_observations.tsv",
        "genotype_projection_summary.json",
        "genotype_source_header_context.json",
    }

    inventory = json.loads(
        (package_root / "entity_inventory.json").read_text(
            encoding="utf-8"
        )
    )
    genotype_entities = [
        entity
        for entity in inventory["entities"]
        if entity["entity_role"] == "genotype_observation_entity"
    ]

    assert len(genotype_entities) == 1
    assert genotype_entities[0]["artifact_count"] == 3
    assert genotype_entities[0]["required"] is True
    assert inventory["summary"]["genotype_capability"] == "available"


def test_fresh_legacy_build_remains_valid_without_genotype(
    tmp_path: Path,
) -> None:
    run_dir = tmp_path / "run_test"
    _write_required_sources(run_dir)

    package_root = build_entities(
        run_dir=run_dir,
        output_root=tmp_path / "tep_output",
        dry_run=False,
        overwrite=False,
    )

    assert not (package_root / "entities" / "genotype").exists()

    inventory = json.loads(
        (package_root / "entity_inventory.json").read_text(
            encoding="utf-8"
        )
    )
    assert inventory["summary"]["genotype_capability"] == "not_available"
    assert not any(
        entity["entity_role"] == "genotype_observation_entity"
        for entity in inventory["entities"]
    )
