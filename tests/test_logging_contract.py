from pathlib import Path
from src.pipeline_runner import initialize_run_paths

def test_run_log_path_is_canonical(tmp_path):
    config = {
        "output": {"base_results_dir": str(tmp_path / "results")},
        "logging": {"log_filename": "pipeline.log"},
    }

    paths = initialize_run_paths(
        config=config,
        run_id="run_2099_01_01_000000",
    )

    log_path = Path(paths["log_path"])

    assert "bootstrap_logs" not in str(log_path)
    assert "logs" in str(log_path)
    assert log_path.name == "pipeline.log"
