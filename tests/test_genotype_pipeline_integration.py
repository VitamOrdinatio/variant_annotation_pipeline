\
from __future__ import annotations

import logging
from pathlib import Path

from src import pipeline_runner


def _write_vcf(path: Path) -> Path:
    path.write_text(
        "##fileformat=VCFv4.2\n"
        "##FORMAT=<ID=GT,Number=1,Type=String,Description=\"Genotype\">\n"
        "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tEXAMPLE\n"
        "1\t100\t.\tA\tC\t60\tPASS\t.\tGT\t0/1\n",
        encoding="utf-8",
        newline="\n",
    )
    return path


def _base_config(tmp_path: Path) -> dict:
    return {
        "project": {
            "pipeline_name": "variant_annotation_pipeline",
            "version": "v1.0",
        },
        "mode": {"execution_mode": "full_pipeline"},
        "input": {
            "sample_id": "EXAMPLE",
            "sample_alias": "EXAMPLE",
            "sra_accession": "SRR_EXAMPLE",
            "assay_type": "WES",
        },
        "reference": {"genome_build": "GRCh38"},
    }


def _base_state(source: Path) -> dict:
    return {
        "run": {
            "run_id": "run_test",
            "pipeline_name": "variant_annotation_pipeline",
        },
        "sample": {
            "sample_id": "EXAMPLE",
            "sample_alias": "EXAMPLE",
            "sra_accession": "SRR_EXAMPLE",
            "assay_type": "WES",
            "reference_genome": "GRCh38",
        },
        "artifacts": {"annotated_vcf": str(source)},
        "qc": {},
        "stage_outputs": {},
        "errors": [],
    }


def test_genotype_projection_success_registers_artifacts_and_qc(
    tmp_path: Path,
) -> None:
    source = _write_vcf(tmp_path / "fixture.vcf")
    processed = tmp_path / "processed"
    processed.mkdir()
    state = _base_state(source)

    result = pipeline_runner.run_genotype_projection_if_ready(
        config=_base_config(tmp_path),
        state=state,
        run_paths={"processed_dir": str(processed)},
        logger=logging.getLogger("genotype_integration_success"),
    )

    projection = result["stage_outputs"]["genotype_observation_projection"]
    assert projection["status"] == "success"
    assert projection["genotype_observation_row_count"] == 1

    for key in [
        "genotype_observations",
        "genotype_projection_summary",
        "genotype_source_header_context",
    ]:
        assert Path(result["artifacts"][key]).is_file()

    qc = result["qc"]["genotype_projection_qc"]
    assert qc["projection_complete"] is True
    assert qc["artifact_set_complete"] is True


def test_genotype_projection_hook_is_idempotent(
    tmp_path: Path,
    monkeypatch,
) -> None:
    source = _write_vcf(tmp_path / "fixture.vcf")
    processed = tmp_path / "processed"
    processed.mkdir()
    state = _base_state(source)
    calls = {"count": 0}
    original = pipeline_runner.project_genotype_observations

    def counting_projector(**kwargs):
        calls["count"] += 1
        return original(**kwargs)

    monkeypatch.setattr(
        pipeline_runner,
        "project_genotype_observations",
        counting_projector,
    )

    for _ in range(2):
        state = pipeline_runner.run_genotype_projection_if_ready(
            config=_base_config(tmp_path),
            state=state,
            run_paths={"processed_dir": str(processed)},
            logger=logging.getLogger("genotype_integration_idempotent"),
        )

    assert calls["count"] == 1


def test_missing_annotated_vcf_is_not_eligible(tmp_path: Path) -> None:
    state = _base_state(tmp_path / "missing.vcf")
    result = pipeline_runner.run_genotype_projection_if_ready(
        config=_base_config(tmp_path),
        state=state,
        run_paths={"processed_dir": str(tmp_path / "processed")},
        logger=logging.getLogger("genotype_integration_not_eligible"),
    )

    projection = result["stage_outputs"]["genotype_observation_projection"]
    assert projection["status"] == "not_eligible"
    assert projection["reason"] == "annotated_vcf_missing"
    assert result["qc"]["genotype_projection_qc"][
        "projection_attempted"
    ] is False


def test_projection_failure_is_recorded_without_raising(
    tmp_path: Path,
    monkeypatch,
) -> None:
    source = _write_vcf(tmp_path / "fixture.vcf")
    state = _base_state(source)

    def fail_projection(**kwargs):
        raise RuntimeError("fixture projection failure")

    monkeypatch.setattr(
        pipeline_runner,
        "project_genotype_observations",
        fail_projection,
    )

    result = pipeline_runner.run_genotype_projection_if_ready(
        config=_base_config(tmp_path),
        state=state,
        run_paths={"processed_dir": str(tmp_path / "processed")},
        logger=logging.getLogger("genotype_integration_failure"),
    )

    projection = result["stage_outputs"]["genotype_observation_projection"]
    assert projection["status"] == "failed"
    assert projection["error_type"] == "RuntimeError"
    assert result["qc"]["genotype_projection_qc"][
        "artifact_set_complete"
    ] is False
    assert any(
        message.startswith("Genotype projection failed:")
        for message in result["errors"]
    )
