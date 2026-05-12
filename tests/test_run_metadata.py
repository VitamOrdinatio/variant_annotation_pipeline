import json
from src.pipeline_runner import write_run_metadata

def test_write_run_metadata(tmp_path):
    output = tmp_path / "run_metadata.json"
    state = {
        "run": {
            "run_id": "run_2099_01_01_000000",
            "status": "completed",
            "pipeline_name": "variant_annotation_pipeline",
            "pipeline_version": "v1.0",
            "execution_mode": "full_pipeline",
            "machine_id": "test-host",
            "start_time": "2099-01-01T00:00:00+00:00",
            "end_time": "2099-01-01T00:00:10+00:00",
            "config_path": "config/config.yaml",
            "config_snapshot_path": "results/run/metadata/config_snapshot.yaml",
        },
        "stage_outputs": {
            "stage_01_load_data": {"status": "success"},
            "stage_02_align_data": {"status": "success"},
            "stage_03_process_bam": {"status": "skipped"},
        },
        "warnings": ["warning one"],
        "errors": [],
        "reports": {
            "run_summary_report": "reports/stage_13_run_report.md",
            "gene_summary_table": "processed/stage_11_gene_variant_counts.tsv",
        },
        "artifacts": {
            "prioritized_table": "processed/stage_11_prioritized_variants.tsv",
            "validation_notes": None,
        },
    }

    write_run_metadata(state, str(output))

    data = json.loads(output.read_text(encoding="utf-8"))

    assert data["run"]["run_id"] == "run_2099_01_01_000000"
    assert data["run"]["status"] == "completed"
    assert data["summary"]["stage_count"] == 3
    assert data["summary"]["stage_status_counts"]["success"] == 2
    assert data["summary"]["stage_status_counts"]["skipped"] == 1
    assert data["summary"]["warning_count"] == 1
    assert data["summary"]["error_count"] == 0
    assert data["artifacts"]["prioritized_table"] == "processed/stage_11_prioritized_variants.tsv"
