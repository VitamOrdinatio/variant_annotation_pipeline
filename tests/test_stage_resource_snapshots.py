import csv
from src.pipeline_runner import append_stage_resource_snapshot

def test_append_stage_resource_snapshot_schema(tmp_path):
    output = tmp_path / "stage_resource_snapshots.tsv"
    snapshot = {
        "timestamp": "2099-01-01T00:00:00+00:00",
        "hostname": "test-host",
        "cpu_count": 8,
        "loadavg_1m": 1.0,
        "loadavg_5m": 1.0,
        "loadavg_15m": 1.0,
        "mem_total": "1000 kB",
        "mem_available": "500 kB",
        "disk_free_gb": 123.45,
    }

    append_stage_resource_snapshot(
        stage_name="stage_08_filter_and_partition",
        phase="start",
        snapshot=snapshot,
        output_path=str(output),
    )

    with output.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        rows = list(reader)

    assert reader.fieldnames == [
        "timestamp",
        "stage",
        "phase",
        "hostname",
        "cpu_count",
        "loadavg_1m",
        "loadavg_5m",
        "loadavg_15m",
        "mem_total",
        "mem_available",
        "disk_free_gb",
    ]
    assert len(rows) == 1
    assert rows[0]["stage"] == "stage_08_filter_and_partition"
    assert rows[0]["phase"] == "start"
