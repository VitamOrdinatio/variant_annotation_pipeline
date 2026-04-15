"""
Configuration loading and validation for variant_annotation_pipeline v1.0.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


def load_config(config_path: str) -> dict[str, Any]:
    path = Path(config_path)
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")
    if not path.is_file():
        raise FileNotFoundError(f"Config path is not a file: {path}")

    with path.open("r", encoding="utf-8") as handle:
        config = yaml.safe_load(handle)

    if not isinstance(config, dict) or not config:
        raise ValueError(f"Config file is empty or invalid: {path}")

    return config


def _require_nested(config: dict[str, Any], path: list[str]) -> Any:
    current: Any = config
    dotted = ".".join(path)

    for key in path:
        if not isinstance(current, dict) or key not in current:
            raise ValueError(f"Missing required config key: {dotted}")
        current = current[key]

    return current


def validate_config(config: dict[str, Any]) -> None:
    required_keys = [
        ["project", "name"],
        ["project", "pipeline_name"],
        ["project", "version"],
        ["mode", "execution_mode"],
        ["input", "bioproject_accession"],
        ["input", "sample_id"],
        ["input", "sample_alias"],
        ["input", "sra_accession"],
        ["input", "fastq", "r1"],
        ["input", "fastq", "r2"],
        ["input", "fastq", "compressed"],
        ["input", "fastq", "paired_end"],
        ["reference", "genome_build"],
        ["reference", "fasta_path"],
        ["reference", "fasta_index"],
        ["reference", "bwa_index_prefix"],
        ["reference", "sequence_dictionary"],
        ["validation", "enable_validation"],
        ["validation", "enable_manual_igv_review_prep"],
        ["validation", "giab_benchmark_vcf"],
        ["validation", "giab_benchmark_index"],
        ["validation", "giab_benchmark_bed"],
        ["tools", "bwa", "executable"],
        ["tools", "samtools", "executable"],
        ["tools", "gatk", "executable"],
        ["tools", "vep", "executable"],
        ["annotation", "engine"],
        ["annotation", "include_clinvar"],
        ["annotation", "include_population_frequencies"],
        ["annotation", "population_sources"],
        ["gene_sets", "mitocarta_path"],
        ["gene_sets", "genes4epilepsy_path"],
        ["gene_sets", "required_flags"],
        ["filtering", "max_af_gnomad"],
        ["filtering", "max_af_exac"],
        ["filtering", "max_af_1000genomes"],
        ["prioritization", "enable_gene_set_overlays"],
        ["output", "base_results_dir"],
        ["logging", "level"],
        ["logging", "log_to_file"],
        ["logging", "log_filename"],
        ["runtime", "fail_fast"],
        ["runtime", "record_tool_versions"],
        ["runtime", "deterministic_mode"],
    ]

    for key_path in required_keys:
        _require_nested(config, key_path)

    execution_mode = config["mode"]["execution_mode"]
    if execution_mode not in {"full_pipeline", "annotation_only"}:
        raise ValueError(
            f"Unsupported mode.execution_mode: {execution_mode}. "
            "Expected one of: full_pipeline, annotation_only"
        )

    if config["project"]["pipeline_name"] != "variant_annotation_pipeline":
        raise ValueError(
            "project.pipeline_name must be 'variant_annotation_pipeline' for Repo 2 v1.0"
        )

    if config["input"]["bioproject_accession"] != "PRJNA200694":
        raise ValueError("Repo 2 v1.0 is locked to input.bioproject_accession = PRJNA200694")

    if config["input"]["sample_id"] != "HG002":
        raise ValueError("Repo 2 v1.0 is locked to input.sample_id = HG002")

    if config["input"]["sra_accession"] != "SRR12898354":
        raise ValueError("Repo 2 v1.0 is locked to input.sra_accession = SRR12898354")

    if config["reference"]["genome_build"] != "GRCh38":
        raise ValueError("Repo 2 v1.0 is locked to reference.genome_build = GRCh38")

    if config["annotation"]["engine"].lower() != "vep":
        raise ValueError("Repo 2 v1.0 requires annotation.engine = vep")

    if sorted(config["gene_sets"]["required_flags"]) != ["epilepsy_flag", "mito_flag"]:
        raise ValueError(
            "gene_sets.required_flags must contain exactly: mito_flag, epilepsy_flag"
        )

    if not isinstance(config["annotation"]["population_sources"], list):
        raise ValueError("annotation.population_sources must be a list")

    if not isinstance(config["gene_sets"]["required_flags"], list):
        raise ValueError("gene_sets.required_flags must be a list")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Validate Repo 2 YAML configuration.")
    parser.add_argument("--config", required=True, help="Path to config YAML")
    args = parser.parse_args()

    loaded = load_config(args.config)
    validate_config(loaded)
    print("Config loaded and validated successfully.")