import json
from pathlib import Path
from src.pipeline_runner import initialize_run_paths, write_run_fingerprint

def test_write_run_fingerprint(tmp_path):
    config_path = tmp_path / "config.yaml"
    config_path.write_text("project:\n  name: test\n", encoding="utf-8")
    reference_fasta = tmp_path / "reference.fa"
    reference_fasta.write_text(">chr1\nACGT\n", encoding="utf-8")
    config = {
        "project": {
            "pipeline_name": "variant_annotation_pipeline",
            "version": "v1.0",
        },
        "reference": {
            "genome_build": "GRCh38",
            "fasta_path": str(reference_fasta),
        },
        "mode": {
            "execution_mode": "full_pipeline",
        },
        "output": {
            "base_results_dir": str(tmp_path / "results"),
        },
        "logging": {
            "log_filename": "pipeline.log",
        },
        "execution_profile": {
            "name": "test_profile",
        },
    }
    run_id = "run_2099_01_01_000000"
    run_paths = initialize_run_paths(config, run_id)

    write_run_fingerprint(
        config=config,
        config_path=str(config_path),
        run_id=run_id,
        run_paths=run_paths,
    )

    output = Path(run_paths["run_fingerprint_path"])
    assert output.exists()
    data = json.loads(output.read_text(encoding="utf-8"))

    required_fields = {
        "run_id",
        "pipeline_name",
        "pipeline_version",
        "git_commit",
        "config_hash",
        "config_path",
        "reference_genome",
        "reference_fasta_path",
        "reference_fasta_hash_or_size",
        "hostname",
        "execution_mode",
        "execution_profile",
        "python_version",
        "platform",
        "created_at",
    }
    assert required_fields.issubset(data)
    assert data["run_id"] == run_id
    assert data["pipeline_name"] == "variant_annotation_pipeline"
    assert data["reference_genome"] == "GRCh38"
    assert data["execution_profile"] == "test_profile"
