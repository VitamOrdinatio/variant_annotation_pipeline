from src.config_loader import load_config, validate_config
from src.pipeline_runner import should_run_stage

def test_post_vep_fixture_config_validates():
    config = load_config("config/config.example.post_vep.yaml")
    validate_config(config)
    assert config["mode"]["execution_mode"] == "post_vep_fixture"

def test_post_vep_fixture_stage_skipping():
    config = load_config("config/config.example.post_vep.yaml")
    skipped = {
        "stage_01_load_data",
        "stage_02_align_data",
        "stage_03_process_bam",
        "stage_04_qc_aligned_reads",
        "stage_05_call_variants",
        "stage_06_normalize_vcf",
        "stage_07_annotate_variants",
    }
    for stage in skipped:
        assert should_run_stage(config, stage) is False
    assert should_run_stage(config, "stage_08_filter_and_partition") is True
    assert should_run_stage(config, "stage_13_write_summary") is True
