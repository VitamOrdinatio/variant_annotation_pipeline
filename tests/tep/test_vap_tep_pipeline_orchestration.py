\
from __future__ import annotations

import csv
import json
import logging
from copy import deepcopy
from pathlib import Path

from src.config_loader import load_config, validate_config
from src.pipeline_runner import STAGE_ORDER, run_pipeline


def test_post_vep_pipeline_emits_validated_genotype_tep(
    tmp_path: Path,
    monkeypatch,
) -> None:
    config = deepcopy(
        load_config("config/templates/config.example.post_vep.yaml")
    )
    config["output"]["base_results_dir"] = str(tmp_path / "results")
    validate_config(config)

    monkeypatch.setattr(
        "src.pipeline_runner.generate_run_id",
        lambda: "run_2099_01_01_000000",
    )

    logger = logging.getLogger("tep_pipeline_orchestration_test")
    logger.handlers.clear()
    logger.addHandler(logging.NullHandler())

    state, paths = run_pipeline(
        config=config,
        config_path="config/templates/config.example.post_vep.yaml",
        logger=logger,
    )

    assert state["run"]["status"] == "completed"
    assert state["tep"]["status"] == "success"
    assert state["tep"]["validation_status"] == "pass"
    assert state["tep"]["genotype_capability"] == "available"
    assert state["tep"]["source_sample_id"] == "EXAMPLE"
    assert state["tep"]["source_run_id"] == "run_example_fixture"
    assert state["tep"]["execution_run_id"] == "run_2099_01_01_000000"

    package = Path(state["tep"]["package_root"])
    assert package.parent == Path(paths["run_dir"]) / "tep"
    assert package.name == "vap_tep_EXAMPLE_run_example_fixture_v1"

    genotype_dir = package / "entities" / "genotype"
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
        (package / "entity_inventory.json").read_text(
            encoding="utf-8"
        )
    )
    assert inventory["source_run"]["run_id"] == "run_example_fixture"
    assert inventory["source_run"]["execution_run_id"] == (
        "run_2099_01_01_000000"
    )
    assert inventory["summary"]["genotype_capability"] == "available"

    lineage = json.loads(
        (package / "lineage_manifest.json").read_text(
            encoding="utf-8"
        )
    )
    edges = {
        (
            edge["parent_entity_id"],
            edge["child_entity_id"],
            edge["relationship"],
        )
        for edge in lineage["lineage_edges"]
    }
    assert (
        "observation_entity",
        "genotype_observation_entity",
        "projects_genotype",
    ) in edges
    assert lineage["validation_summary"]["validation_status"] == "pass"

    report = (
        package / "validation_report.md"
    ).read_text(encoding="utf-8")
    assert "Validation status: `pass`" in report

    materialized = Path(
        state["tep"]["materialized_observation_table"]
    )
    assert materialized.is_file()
    assert materialized.parent == Path(paths["processed_dir"])

    with Path(paths["runtime_profile_path"]).open(
        "r",
        encoding="utf-8",
        newline="",
    ) as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    assert len(rows) == len(STAGE_ORDER)

    metadata = json.loads(
        Path(paths["run_metadata_path"]).read_text(
            encoding="utf-8"
        )
    )
    assert metadata["tep"]["status"] == "success"
    assert metadata["tep"]["validation_status"] == "pass"

    receipt_json = Path(state["tep"]["emission_summary_json"])
    receipt_markdown = Path(
        state["tep"]["emission_summary_markdown"]
    )
    assert receipt_json == (
        Path(paths["metadata_dir"]) / "tep_emission_summary.json"
    )
    assert receipt_markdown == (
        Path(paths["reports_dir"]) / "tep_emission_summary.md"
    )
    assert receipt_json.is_file()
    assert receipt_markdown.is_file()

    receipt = json.loads(
        receipt_json.read_text(encoding="utf-8")
    )
    assert receipt["receipt_type"] == "vap_tep_emission_summary"
    assert receipt["execution_run_id"] == "run_2099_01_01_000000"
    assert receipt["source_run_id"] == "run_example_fixture"
    assert receipt["emission_status"] == "success"
    assert receipt["validation_status"] == "pass"
    assert receipt["genotype_capability"] == "available"

    report_text = receipt_markdown.read_text(encoding="utf-8")
    assert "# TEP-VAP Emission Summary" in report_text
    assert "Emission status: `success`" in report_text
    assert "Validation status: `pass`" in report_text
    assert "Genotype capability: `available`" in report_text


def test_fresh_tep_failure_is_recorded_separately(
    tmp_path: Path,
    monkeypatch,
) -> None:
    from src import pipeline_runner

    state = {
        "run": {"status": "completed"},
        "stage_outputs": {
            "genotype_observation_projection": {"status": "success"}
        },
        "errors": [],
        "tep": {
            "attempted": False,
            "status": "not_attempted",
        },
    }

    def fail_orchestration(**kwargs):
        raise RuntimeError("fixture TEP failure")

    monkeypatch.setattr(
        pipeline_runner,
        "build_and_validate_fresh_vap_tep",
        fail_orchestration,
    )

    logger = logging.getLogger("tep_failure_test")
    logger.handlers.clear()
    logger.addHandler(logging.NullHandler())

    result = pipeline_runner.run_fresh_tep_if_ready(
        state=state,
        run_paths={"run_dir": str(tmp_path)},
        logger=logger,
    )

    assert result["run"]["status"] == "completed"
    assert result["tep"]["status"] == "failed"
    assert result["tep"]["error_type"] == "RuntimeError"
    assert result["errors"] == [
        "Fresh TEP-VAP emission failed: fixture TEP failure"
    ]
