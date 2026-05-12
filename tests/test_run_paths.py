from pathlib import Path
from src.pipeline_runner import initialize_run_paths

def test_initialize_run_paths_creates_phase0_metadata_dirs(tmp_path):
    config = {
        "output": {"base_results_dir": str(tmp_path / "results")},
        "logging": {"log_filename": "pipeline.log"},
    }
    run_id = "run_2099_01_01_000000"
    paths = initialize_run_paths(config, run_id)
    expected_dirs = [
        "run_dir",
        "logs_dir",
        "metadata_dir",
        "stage_summaries_dir",
        "interim_dir",
        "processed_dir",
        "reports_dir",
        "final_dir",
        "validation_dir",
    ]
    for key in expected_dirs:
        assert key in paths
        assert Path(paths[key]).exists()
        assert Path(paths[key]).is_dir()
    assert paths["log_path"].endswith("logs/pipeline.log")
    assert paths["legacy_config_snapshot_path"].endswith("config_used.yaml")
    assert paths["legacy_metadata_path"].endswith("metadata.json")
    assert paths["config_snapshot_path"].endswith("metadata/config_snapshot.yaml")
    assert paths["run_metadata_path"].endswith("metadata/run_metadata.json")
    assert paths["run_fingerprint_path"].endswith("metadata/run_fingerprint.json")
    assert paths["runtime_profile_path"].endswith("metadata/runtime_profile.tsv")
