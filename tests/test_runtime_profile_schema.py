import csv
from src.pipeline_runner import STAGE_ORDER, write_runtime_profile

def test_runtime_profile_schema(tmp_path):
    output = tmp_path / "runtime_profile.tsv"
    state = {
        "stage_outputs": {
            stage: {
                "status": "success",
                "start_time": "2099-01-01T00:00:00+00:00",
                "end_time": "2099-01-01T00:00:01+00:00",
                "elapsed_seconds": 1.0,
            }
            for stage in STAGE_ORDER
        }
    }

    write_runtime_profile(state, str(output))

    with output.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        assert reader.fieldnames == [
            "stage",
            "status",
            "start_time",
            "end_time",
            "elapsed_seconds",
        ]
        rows = list(reader)

    assert len(rows) == len(STAGE_ORDER)
    assert rows[0]["stage"] == STAGE_ORDER[0]
    assert rows[0]["elapsed_seconds"] == "1.0"
