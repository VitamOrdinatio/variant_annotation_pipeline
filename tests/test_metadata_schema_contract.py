import json
from src.pipeline_runner import write_run_metadata

def test_run_metadata_schema_contract(tmp_path):
    output = tmp_path / "run_metadata.json"

    state = {
        "run": {
            "run_id": "run_2099",
            "status": "completed",
            "pipeline_name": "vap",
            "pipeline_version": "v1",
            "execution_mode": "full_pipeline",
            "machine_id": "host",
            "start_time": "2099-01-01T00:00:00+00:00",
            "end_time": "2099-01-01T00:01:00+00:00",
            "config_path": "config.yaml",
            "config_snapshot_path": "snapshot.yaml",
        },
        "stage_outputs": {
            "stage_01_load_data": {"status": "success"},
        },
        "warnings": [],
        "errors": [],
        "reports": {},
        "artifacts": {},
    }

    write_run_metadata(state, str(output))

    data = json.loads(output.read_text(encoding="utf-8"))

    assert set(data.keys()) == {
        "artifacts",
        "genotype_projection",
        "run",
        "summary",
    }

    assert set(data["run"].keys()) == {
        "config_path",
        "config_snapshot_path",
        "end_time",
        "execution_mode",
        "machine_id",
        "pipeline_name",
        "pipeline_version",
        "run_id",
        "start_time",
        "status",
    }

    assert set(data["genotype_projection"].keys()) == {
        "artifact_set_complete",
        "genotype_observation_row_count",
        "projection_complete",
        "projection_status",
        "source_record_count",
        "status",
    }
    assert data["genotype_projection"]["status"] == "not_recorded"
    assert data["genotype_projection"]["projection_complete"] is False
    assert data["genotype_projection"]["artifact_set_complete"] is False

    assert set(data["summary"].keys()) == {
        "error_count",
        "projection_count",
        "projection_status_counts",
        "stage_count",
        "stage_status_counts",
        "warning_count",
    }
