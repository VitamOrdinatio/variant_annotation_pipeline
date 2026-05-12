import json
from src.pipeline_runner import write_stage_summary

def test_write_stage_summary_json(tmp_path):
    stage_dir = tmp_path / "stage_summaries"
    stage_dir.mkdir()
    stage_data = {
        "status": "success",
        "start_time": "2099-01-01T00:00:00+00:00",
        "end_time": "2099-01-01T00:00:01+00:00",
        "elapsed_seconds": 1.0,
    }

    write_stage_summary("stage_07_annotate_variants", stage_data, str(stage_dir))

    output = stage_dir / "stage_07_summary.json"
    assert output.exists()

    data = json.loads(output.read_text(encoding="utf-8"))
    assert data["stage"] == "stage_07_annotate_variants"
    assert data["status"] == "success"
    assert data["elapsed_seconds"] == 1.0
    assert data["input_artifacts"] == []
    assert data["output_artifacts"] == []
    assert data["warning_count"] == 0
    assert data["error_count"] == 0
