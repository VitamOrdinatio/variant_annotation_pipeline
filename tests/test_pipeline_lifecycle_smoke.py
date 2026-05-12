import logging
from types import SimpleNamespace
from src import pipeline_runner

def test_pipeline_lifecycle_smoke_emits_phase0_artifacts(tmp_path, monkeypatch):
    reference = tmp_path / "reference.fa"
    reference.write_text(">chr1\nACGT\n", encoding="utf-8")
    config_path = tmp_path / "config.yaml"
    config_path.write_text("test: true\n", encoding="utf-8")

    config = {
        "project": {"pipeline_name": "variant_annotation_pipeline", "version": "v1.0"},
        "mode": {"execution_mode": "full_pipeline"},
        "output": {"base_results_dir": str(tmp_path / "results")},
        "logging": {"level": "INFO", "log_filename": "pipeline.log"},
        "reference": {"genome_build": "GRCh38", "fasta_path": str(reference)},
        "annotation": {
            "engine": "vep",
            "include_clinvar": False,
            "population_sources": [],
        },
        "gene_sets": {
            "mitocarta_path": "NA",
            "genes4epilepsy_path": "NA",
            "required_flags": ["mito_flag", "epilepsy_flag"],
        },
        "runtime": {"record_tool_versions": False},
    }

    def fake_run_stage(config, paths, logger, state):
        state["sample"]["sample_id"] = "SMOKE"
        return state

    monkeypatch.setattr(
        pipeline_runner,
        "STAGE_ORDER",
        ["stage_01_load_data", "stage_02_align_data"],
    )
    monkeypatch.setattr(
        pipeline_runner,
        "get_stage_module",
        lambda stage_name: SimpleNamespace(run_stage=fake_run_stage),
    )

    logger = logging.getLogger("vap_smoke_test")
    state, paths = pipeline_runner.run_pipeline(
        config=config,
        config_path=str(config_path),
        logger=logger,
    )

    run_dir = tmp_path / "results" / state["run"]["run_id"]

    assert state["run"]["status"] == "completed"
    assert (run_dir / "logs" / "pipeline.log").exists()
    assert (run_dir / "metadata" / "config_snapshot.yaml").exists()
    assert (run_dir / "metadata" / "run_fingerprint.json").exists()
    assert (run_dir / "metadata" / "run_metadata.json").exists()
    assert (run_dir / "metadata" / "runtime_profile.tsv").exists()
    assert (run_dir / "metadata" / "stage_summaries" / "stage_01_summary.json").exists()
    assert (run_dir / "metadata" / "stage_summaries" / "stage_02_summary.json").exists()
    assert (run_dir / "metadata.json").exists()
    assert "bootstrap_logs" not in paths["log_path"]
