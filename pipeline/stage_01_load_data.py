"""
Stage 01: Load data, validate external inputs, and initialize sample-aware state.

Repo 2 v1.0 contract highlights:
- locked dataset metadata:
  - BioProject: PRJNA200694
  - Sample: HG002
  - Sample alias: NA24385
  - SRA: SRR12898354
  - Reference: GRCh38
- real pipeline inputs live outside the repo
- v1 primary mode is full_pipeline using paired compressed FASTQ inputs
- annotation_only remains a future-compatible extension point
"""

from __future__ import annotations

from pathlib import Path
from typing import Any


EXPECTED_V1_DATASET = {
    "bioproject_accession": "PRJNA200694",
    "sample_id": "HG002",
    "sample_alias": "NA24385",
    "sra_accession": "SRR12898354",
    "reference_genome": "GRCh38",
}


def _validate_required_string(value: str | None, label: str) -> str:
    if value is None or str(value).strip() == "":
        raise ValueError(f"Missing required configuration value: {label}")
    return str(value).strip()


def _validate_existing_file(path_str: str | None, label: str) -> dict[str, Any]:
    path_value = _validate_required_string(path_str, label)
    path = Path(path_value)

    if not path.exists():
        raise FileNotFoundError(f"Required file not found for {label}: {path}")
    if not path.is_file():
        raise FileNotFoundError(f"Expected file for {label}, but found non-file path: {path}")

    return {
        "label": label,
        "path": str(path),
        "exists": True,
        "size_bytes": path.stat().st_size,
    }


def _validate_existing_directory(path_str: str | None, label: str) -> dict[str, Any]:
    path_value = _validate_required_string(path_str, label)
    path = Path(path_value)

    if not path.exists():
        raise FileNotFoundError(f"Required directory not found for {label}: {path}")
    if not path.is_dir():
        raise FileNotFoundError(f"Expected directory for {label}, but found non-directory path: {path}")

    return {
        "label": label,
        "path": str(path),
        "exists": True,
    }


def _validate_fastq_path(path_str: str | None, label: str, compressed: bool) -> dict[str, Any]:
    summary = _validate_existing_file(path_str, label)
    path = Path(summary["path"])

    if compressed and not str(path).endswith(".fastq.gz"):
        raise ValueError(
            f"{label} is expected to be compressed (.fastq.gz) but got: {path}"
        )
    if not compressed and str(path).endswith(".gz"):
        raise ValueError(
            f"{label} is expected to be uncompressed FASTQ, but appears gzipped: {path}"
        )

    summary["compressed"] = compressed
    return summary


def _check_locked_dataset_metadata(
    bioproject_accession: str,
    sample_id: str,
    sample_alias: str,
    sra_accession: str,
    reference_genome: str,
    warnings: list[str],
) -> None:
    required_pairs = {
        "bioproject_accession": bioproject_accession,
        "sample_id": sample_id,
        "sra_accession": sra_accession,
        "reference_genome": reference_genome,
    }

    for key, observed in required_pairs.items():
        expected = EXPECTED_V1_DATASET[key]
        if observed != expected:
            raise ValueError(
                f"Repo2 v1.0 is locked to {key}={expected}, but config provided {observed}"
            )

    if sample_alias != EXPECTED_V1_DATASET["sample_alias"]:
        warnings.append(
            "sample_alias differs from locked v1 expectation "
            f"({EXPECTED_V1_DATASET['sample_alias']}); continuing because alias is non-critical."
        )


def run_stage(
    config: dict[str, Any],
    paths: dict[str, Any],
    logger,
    state: dict[str, Any],
) -> dict[str, Any]:
    logger.info("Stage 01: loading input data context.")

    mode = config["mode"]["execution_mode"]
    logger.info(f"Stage 01 operating in {mode} mode.")

    if mode not in {"full_pipeline", "annotation_only"}:
        raise ValueError(f"Unsupported execution mode: {mode}")

    input_cfg = config["input"]
    fastq_cfg = input_cfg["fastq"]
    sra_cfg = input_cfg["sra"]
    reference_cfg = config["reference"]
    validation_cfg = config["validation"]
    gene_set_cfg = config["gene_sets"]

    bioproject_accession = _validate_required_string(
        input_cfg.get("bioproject_accession"), "input.bioproject_accession"
    )
    sample_id = _validate_required_string(input_cfg.get("sample_id"), "input.sample_id")
    sample_alias = _validate_required_string(input_cfg.get("sample_alias"), "input.sample_alias")
    sra_accession = _validate_required_string(input_cfg.get("sra_accession"), "input.sra_accession")
    reference_genome = _validate_required_string(
        reference_cfg.get("genome_build"), "reference.genome_build"
    )

    state.setdefault("warnings", [])
    state.setdefault("errors", [])
    warnings = state["warnings"]

    _check_locked_dataset_metadata(
        bioproject_accession=bioproject_accession,
        sample_id=sample_id,
        sample_alias=sample_alias,
        sra_accession=sra_accession,
        reference_genome=reference_genome,
        warnings=warnings,
    )

    files_checked: list[dict[str, Any]] = []
    provenance_checked: list[dict[str, Any]] = []
    validation_checked: list[dict[str, Any]] = []
    gene_sets_checked: list[dict[str, Any]] = []

    if mode == "full_pipeline":
        compressed = bool(fastq_cfg.get("compressed", True))
        paired_end = bool(fastq_cfg.get("paired_end", True))
        if not paired_end:
            raise ValueError("Repo2 v1.0 expects paired-end WGS FASTQ input.")

        fastq_1_summary = _validate_fastq_path(
            fastq_cfg.get("r1"), "input.fastq.r1", compressed=compressed
        )
        fastq_2_summary = _validate_fastq_path(
            fastq_cfg.get("r2"), "input.fastq.r2", compressed=compressed
        )
        files_checked.extend([fastq_1_summary, fastq_2_summary])

        logger.info(f"Validated FASTQ R1: {fastq_1_summary['path']}")
        logger.info(f"Validated FASTQ R2: {fastq_2_summary['path']}")

        state["inputs"] = {
            "fastq_1": fastq_1_summary["path"],
            "fastq_2": fastq_2_summary["path"],
            "input_vcf": None,
            "sra_dir": None,
            "sra_file": None,
            "compressed_fastq": compressed,
            "paired_end": paired_end,
        }

        sra_enabled = bool(sra_cfg.get("enabled", False))
        if sra_enabled:
            sra_dir = sra_cfg.get("sra_dir")
            sra_file = sra_cfg.get("sra_file")

            if sra_dir:
                try:
                    sra_dir_summary = _validate_existing_directory(sra_dir, "input.sra.sra_dir")
                    provenance_checked.append(sra_dir_summary)
                    state["inputs"]["sra_dir"] = sra_dir_summary["path"]
                    logger.info(f"Validated SRA directory: {sra_dir_summary['path']}")
                except FileNotFoundError as exc:
                    warnings.append(str(exc))
                    logger.warning(str(exc))

            if sra_file:
                try:
                    sra_file_summary = _validate_existing_file(sra_file, "input.sra.sra_file")
                    provenance_checked.append(sra_file_summary)
                    state["inputs"]["sra_file"] = sra_file_summary["path"]
                    logger.info(f"Validated SRA file: {sra_file_summary['path']}")
                except FileNotFoundError as exc:
                    warnings.append(str(exc))
                    logger.warning(str(exc))

    else:
        input_vcf = input_cfg["vcf"].get("input_vcf")
        input_vcf_summary = _validate_existing_file(input_vcf, "input.vcf.input_vcf")
        files_checked.append(input_vcf_summary)

        state["inputs"] = {
            "fastq_1": None,
            "fastq_2": None,
            "input_vcf": input_vcf_summary["path"],
            "sra_dir": None,
            "sra_file": None,
            "compressed_fastq": None,
            "paired_end": None,
        }

        logger.info(f"Validated input VCF: {input_vcf_summary['path']}")

    if bool(validation_cfg.get("enable_validation", False)):
        benchmark_vcf = _validate_existing_file(
            validation_cfg.get("giab_benchmark_vcf"),
            "validation.giab_benchmark_vcf",
        )
        benchmark_index = _validate_existing_file(
            validation_cfg.get("giab_benchmark_index"),
            "validation.giab_benchmark_index",
        )
        benchmark_bed = _validate_existing_file(
            validation_cfg.get("giab_benchmark_bed"),
            "validation.giab_benchmark_bed",
        )
        validation_checked.extend([benchmark_vcf, benchmark_index, benchmark_bed])

    mitocarta_summary = _validate_existing_file(
        gene_set_cfg.get("mitocarta_path"),
        "gene_sets.mitocarta_path",
    )
    genes4epilepsy_summary = _validate_existing_file(
        gene_set_cfg.get("genes4epilepsy_path"),
        "gene_sets.genes4epilepsy_path",
    )
    gene_sets_checked.extend([mitocarta_summary, genes4epilepsy_summary])

    state["sample"] = {
        "sample_id": sample_id,
        "sample_alias": sample_alias,
        "bioproject_accession": bioproject_accession,
        "sra_accession": sra_accession,
        "reference_genome": reference_genome,
        "assay_type": "WGS",
    }

    state["gene_sets"]["mitocarta_path"] = mitocarta_summary["path"]
    state["gene_sets"]["genes4epilepsy_path"] = genes4epilepsy_summary["path"]
    state["gene_sets"]["overlay_completed"] = False
    state["gene_sets"]["flags_added"] = ["mito_flag", "epilepsy_flag"]

    state["qc"]["input_qc"] = {
        "input_validation_passed": True,
        "execution_mode": mode,
        "files_checked": files_checked,
        "file_count": len(files_checked),
        "provenance_checked": provenance_checked,
        "provenance_check_count": len(provenance_checked),
        "validation_checked": validation_checked,
        "validation_check_count": len(validation_checked),
        "gene_sets_checked": gene_sets_checked,
        "gene_set_check_count": len(gene_sets_checked),
    }

    state["stage_outputs"]["stage_01_load_data"] = {
        "status": "success",
        "execution_mode": mode,
        "sample_id": sample_id,
        "sra_accession": sra_accession,
        "reference_genome": reference_genome,
        "file_count": len(files_checked),
        "validation_check_count": len(validation_checked),
        "gene_set_check_count": len(gene_sets_checked),
        "warning_count": len(warnings),
    }

    return state