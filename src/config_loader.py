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



EXECUTION_PROVENANCE_SCHEMA_VERSION = "1.0.0"

_ALLOWED_VERSION_POLICIES = {
    "exact",
    "major",
    "record_only",
}

_REQUIRED_TOOLCHAIN_KEYS = {
    "bwa",
    "samtools",
    "gatk",
    "java",
    "vep",
    "perl",
    "python",
}

_REQUIRED_RESOURCE_KEYS = {
    "reference_fasta",
    "fasta_index",
    "sequence_dictionary",
    "bwa_index",
    "mitocarta",
    "genes4epilepsy",
}


def _require_non_empty_string(value: Any, dotted: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{dotted} must be a non-empty string")
    return value.strip()


def _validate_toolchain_declaration(
    tool_name: str,
    declaration: Any,
) -> None:
    dotted = f"execution_provenance.toolchain.{tool_name}"
    if not isinstance(declaration, dict):
        raise ValueError(f"{dotted} must be a mapping")

    policy = _require_non_empty_string(
        declaration.get("version_policy"),
        f"{dotted}.version_policy",
    )
    if policy not in _ALLOWED_VERSION_POLICIES:
        raise ValueError(
            f"{dotted}.version_policy must be one of: "
            + ", ".join(sorted(_ALLOWED_VERSION_POLICIES))
        )

    if policy == "exact":
        _require_non_empty_string(
            declaration.get("declared_version"),
            f"{dotted}.declared_version",
        )
    elif policy == "major":
        _require_non_empty_string(
            declaration.get("declared_major_version"),
            f"{dotted}.declared_major_version",
        )

    configured_from = declaration.get("configured_from")
    if tool_name in {"bwa", "samtools", "gatk", "vep"}:
        _require_non_empty_string(
            configured_from,
            f"{dotted}.configured_from",
        )


def _validate_execution_provenance_config(
    config: dict[str, Any],
) -> None:
    provenance = config.get("execution_provenance")
    if provenance is None:
        # Transitional compatibility: legacy configs remain valid until
        # explicitly migrated to the provenance contract.
        return

    if not isinstance(provenance, dict):
        raise ValueError("execution_provenance must be a mapping")

    required = provenance.get("required")
    if not isinstance(required, bool):
        raise ValueError("execution_provenance.required must be a boolean")

    schema_version = _require_non_empty_string(
        provenance.get("schema_version"),
        "execution_provenance.schema_version",
    )
    if schema_version != EXECUTION_PROVENANCE_SCHEMA_VERSION:
        raise ValueError(
            "execution_provenance.schema_version must be "
            f"{EXECUTION_PROVENANCE_SCHEMA_VERSION}"
        )

    toolchain = provenance.get("toolchain")
    if not isinstance(toolchain, dict):
        raise ValueError("execution_provenance.toolchain must be a mapping")

    missing_tools = sorted(_REQUIRED_TOOLCHAIN_KEYS - set(toolchain))
    extra_tools = sorted(set(toolchain) - _REQUIRED_TOOLCHAIN_KEYS)
    if missing_tools or extra_tools:
        raise ValueError(
            "execution_provenance.toolchain must contain exactly: "
            + ", ".join(sorted(_REQUIRED_TOOLCHAIN_KEYS))
            + f"; missing={missing_tools}; extra={extra_tools}"
        )

    for tool_name in sorted(_REQUIRED_TOOLCHAIN_KEYS):
        _validate_toolchain_declaration(
            tool_name,
            toolchain[tool_name],
        )

    annotation = provenance.get("annotation_environment")
    if not isinstance(annotation, dict):
        raise ValueError(
            "execution_provenance.annotation_environment must be a mapping"
        )

    expected_annotation = {
        "engine": "ensembl_vep",
        "cache_species": "homo_sapiens",
        "cache_assembly": config["reference"]["genome_build"],
        "cache_type": "ensembl",
        "execution_mode": "offline",
    }
    for key, expected in expected_annotation.items():
        observed = _require_non_empty_string(
            annotation.get(key),
            f"execution_provenance.annotation_environment.{key}",
        )
        if observed != expected:
            raise ValueError(
                "execution_provenance.annotation_environment."
                f"{key} must be {expected!r}"
            )

    _require_non_empty_string(
        annotation.get("software_version"),
        "execution_provenance.annotation_environment.software_version",
    )
    _require_non_empty_string(
        annotation.get("cache_release"),
        "execution_provenance.annotation_environment.cache_release",
    )

    declared_vep = toolchain["vep"].get("declared_version")
    if annotation["software_version"] != declared_vep:
        raise ValueError(
            "VEP software version declarations disagree between "
            "execution_provenance.toolchain.vep.declared_version and "
            "execution_provenance.annotation_environment.software_version"
        )

    resources = provenance.get("resource_environment")
    if not isinstance(resources, dict):
        raise ValueError(
            "execution_provenance.resource_environment must be a mapping"
        )

    missing_resources = sorted(_REQUIRED_RESOURCE_KEYS - set(resources))
    extra_resources = sorted(set(resources) - _REQUIRED_RESOURCE_KEYS)
    if missing_resources or extra_resources:
        raise ValueError(
            "execution_provenance.resource_environment must contain exactly: "
            + ", ".join(sorted(_REQUIRED_RESOURCE_KEYS))
            + f"; missing={missing_resources}; extra={extra_resources}"
        )

    allowed_checksum_policies = {
        "sha256",
        "sha256_constituents",
    }
    for resource_name, declaration in resources.items():
        dotted = (
            "execution_provenance.resource_environment."
            f"{resource_name}"
        )
        if not isinstance(declaration, dict):
            raise ValueError(f"{dotted} must be a mapping")

        _require_non_empty_string(
            declaration.get("configured_from"),
            f"{dotted}.configured_from",
        )
        policy = _require_non_empty_string(
            declaration.get("checksum_policy"),
            f"{dotted}.checksum_policy",
        )
        if policy not in allowed_checksum_policies:
            raise ValueError(
                f"{dotted}.checksum_policy must be one of: "
                + ", ".join(sorted(allowed_checksum_policies))
            )

    if resources["bwa_index"]["checksum_policy"] != (
        "sha256_constituents"
    ):
        raise ValueError(
            "execution_provenance.resource_environment.bwa_index."
            "checksum_policy must be 'sha256_constituents'"
        )

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

    _validate_execution_provenance_config(config)

    execution_mode = config["mode"]["execution_mode"]
    if execution_mode not in {"full_pipeline", "annotation_only", "post_vep_fixture"}:
        raise ValueError(
            f"Unsupported mode.execution_mode: {execution_mode}. "
            "Expected one of: full_pipeline, annotation_only, post_vep_fixture"
        )

    if config["project"]["pipeline_name"] != "variant_annotation_pipeline":
        raise ValueError(
            "project.pipeline_name must be 'variant_annotation_pipeline' for Repo 2 v1.0"
        )

    allow_non_hg002 = config.get("execution_profile", {}).get("allow_non_hg002", False)

    if execution_mode in {"full_pipeline", "annotation_only"} and not allow_non_hg002:
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