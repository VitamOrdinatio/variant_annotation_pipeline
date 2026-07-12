import csv
import json
import logging
from pathlib import Path

from src.config_loader import load_config, validate_config
from src.pipeline_runner import STAGE_ORDER, run_pipeline

def test_post_vep_fixture_outputs_exist_and_statuses_are_correct(tmp_path):
    config = load_config("config/templates/config.example.post_vep.yaml")
    validate_config(config)
    config["output"]["base_results_dir"] = str(tmp_path / "results")

    logger = logging.getLogger("post_vep_fixture_output_test")
    state, paths = run_pipeline(
        config=config,
        config_path="config/templates/config.example.post_vep.yaml",
        logger=logger,
    )

    run_dir = Path(paths["run_dir"])
    metadata_dir = run_dir / "metadata"
    stage_summary_dir = metadata_dir / "stage_summaries"
    processed_dir = run_dir / "processed"

    assert state["run"]["status"] == "completed"
    assert (run_dir / "logs" / "pipeline.log").exists()
    assert (metadata_dir / "config_snapshot.yaml").exists()
    assert (metadata_dir / "run_fingerprint.json").exists()
    assert (metadata_dir / "run_metadata.json").exists()
    assert (metadata_dir / "runtime_profile.tsv").exists()
    assert (run_dir / "metadata.json").exists()

    expected_processed = [
        "genotype_observations.tsv",
        "genotype_projection_summary.json",
        "genotype_source_header_context.json",
        "stage_08_selected_transcript_consequences.tsv",
        "stage_08_variant_summary.tsv",
        "stage_08_vdb_ready_variants.tsv",
        "stage_08_rdgp_gene_evidence_seed.tsv",
        "stage_08_summary.json",
        "stage_09_coding_interpreted.tsv",
        "stage_09_summary.json",
        "stage_10_noncoding_interpreted.tsv",
        "stage_10_summary.json",
        "stage_11_prioritized_variants.tsv",
        "stage_11_gene_variant_counts.tsv",
        "stage_11_summary.json",
        "stage_12_validation_candidates.tsv",
        "stage_12_summary.json",
        "stage_13_final_summary.json",
        "stage_13_artifact_manifest.json",
        "stage_13_run_report.md",
    ]

    for filename in expected_processed:
        assert (processed_dir / filename).exists(), filename

    for stage in STAGE_ORDER:
        stage_number = stage.split("_")[1]
        assert (stage_summary_dir / f"stage_{stage_number}_summary.json").exists()

    skipped = {
        "stage_01_load_data",
        "stage_02_align_data",
        "stage_03_process_bam",
        "stage_04_qc_aligned_reads",
        "stage_05_call_variants",
        "stage_06_normalize_vcf",
        "stage_07_annotate_variants",
    }

    for stage in skipped:
        assert state["stage_outputs"][stage]["status"] == "skipped"

    for stage in STAGE_ORDER:
        if stage not in skipped:
            assert state["stage_outputs"][stage]["status"] == "success"

    projection = state["stage_outputs"]["genotype_observation_projection"]
    assert projection["status"] == "success"
    assert projection["genotype_observation_row_count"] == 8
    assert state["qc"]["genotype_projection_qc"]["artifact_set_complete"] is True

    manifest = json.loads(
        (processed_dir / "stage_13_artifact_manifest.json").read_text(
            encoding="utf-8"
        )
    )
    manifested_names = {
        record["artifact_name"]
        for record in manifest["artifacts"]
    }
    assert "genotype_observations.tsv" in manifested_names
    assert "genotype_projection_summary.json" in manifested_names
    assert "genotype_source_header_context.json" in manifested_names

    with (metadata_dir / "runtime_profile.tsv").open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))

    assert len(rows) == len(STAGE_ORDER)
    assert rows[0]["stage"] == STAGE_ORDER[0]

    run_metadata = json.loads((metadata_dir / "run_metadata.json").read_text(encoding="utf-8"))
    assert run_metadata["run"]["status"] == "completed"
    assert run_metadata["summary"]["stage_status_counts"]["skipped"] == 7
    assert run_metadata["summary"]["stage_status_counts"]["success"] == 6
    assert run_metadata["summary"]["stage_count"] == len(STAGE_ORDER)
    assert run_metadata["summary"]["projection_count"] == 1
    assert run_metadata["summary"]["projection_status_counts"]["success"] == 1
    assert run_metadata["genotype_projection"]["status"] == "success"
    assert run_metadata["genotype_projection"]["artifact_set_complete"] is True
