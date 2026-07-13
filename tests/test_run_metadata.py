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
            "genotype_observation_projection": {
                "status": "success",
                "projection_status": "pass",
            },
        },
        "qc": {
            "genotype_projection_qc": {
                "projection_complete": True,
                "artifact_set_complete": True,
                "projection_status": "pass",
                "source_record_count": 8,
                "genotype_observation_row_count": 8,
            }
        },
        "warnings": ["warning one"],
        "errors": [],
        "reports": {
            "run_summary_report": "reports/stage_13_run_report.md",
            "gene_summary_table": "processed/stage_11_gene_variant_counts.tsv",
        },
        "tep": {
            "attempted": True,
            "status": "success",
            "tep_id": "vap_tep_HG002_run_test_v1",
            "validation_status": "pass",
        },
        "artifacts": {
            "prioritized_table": "processed/stage_11_prioritized_variants.tsv",
            "validation_notes": None,
            "genotype_observations": "processed/genotype_observations.tsv",
            "genotype_projection_summary": (
                "processed/genotype_projection_summary.json"
            ),
            "genotype_source_header_context": (
                "processed/genotype_source_header_context.json"
            ),
        },
    }

    write_run_metadata(state, str(output))

    data = json.loads(output.read_text(encoding="utf-8"))

    assert data["run"]["run_id"] == "run_2099_01_01_000000"
    assert data["run"]["status"] == "completed"
    assert data["summary"]["stage_count"] == 13
    assert data["summary"]["stage_status_counts"]["success"] == 2
    assert data["summary"]["stage_status_counts"]["skipped"] == 1
    assert data["summary"]["stage_status_counts"]["unknown"] == 10
    assert data["summary"]["projection_count"] == 1
    assert data["summary"]["projection_status_counts"]["success"] == 1
    assert data["genotype_projection"]["status"] == "success"
    assert data["genotype_projection"]["projection_status"] == "pass"
    assert data["genotype_projection"]["artifact_set_complete"] is True
    assert data["tep"]["status"] == "success"
    assert data["tep"]["validation_status"] == "pass"
    assert data["summary"]["stage_status_counts"]["skipped"] == 1
    assert data["summary"]["warning_count"] == 1
    assert data["summary"]["error_count"] == 0
    assert data["artifacts"]["prioritized_table"] == "processed/stage_11_prioritized_variants.tsv"
