"""
Stage 06: Normalize and clean VCF output.

Repo 2 v1.0 design notes:
- input:
  - raw VCF from Stage 05
  - reference FASTA
- tool: GATK LeftAlignAndTrimVariants
- output:
  - normalized VCF
- writes outputs under results/<run_id>/interim/
"""

from __future__ import annotations

import shlex
import subprocess
from pathlib import Path
from typing import Any


def _run_command(command: list[str], logger, label: str) -> subprocess.CompletedProcess:
    """
    Execute a subprocess command with logging.

    Parameters
    ----------
    command : list[str]
        Command and arguments.
    logger : logging.Logger
        Configured logger.
    label : str
        Human-readable step label.

    Returns
    -------
    subprocess.CompletedProcess
        Completed process object.

    Raises
    ------
    RuntimeError
        If the command exits non-zero.
    """
    rendered = " ".join(shlex.quote(part) for part in command)
    logger.info(f"{label} command: {rendered}")

    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=False,
    )

    if result.stdout.strip():
        logger.info(f"{label} stdout: {result.stdout.strip()}")
    if result.stderr.strip():
        logger.info(f"{label} stderr: {result.stderr.strip()}")

    if result.returncode != 0:
        raise RuntimeError(f"{label} failed with exit code {result.returncode}")

    return result


def _validate_required_artifact(path_str: str | None, label: str) -> Path:
    """
    Validate that a required upstream artifact exists.

    Parameters
    ----------
    path_str : str | None
        Path string.
    label : str
        Human-readable label.

    Returns
    -------
    Path
        Validated path.

    Raises
    ------
    ValueError
        If missing.
    FileNotFoundError
        If path does not exist.
    """
    if not path_str:
        raise ValueError(f"Missing required upstream artifact for {label}")
    path = Path(path_str)
    if not path.exists():
        raise FileNotFoundError(f"Required upstream artifact not found for {label}: {path}")
    if not path.is_file():
        raise FileNotFoundError(f"Expected file for {label}, but found non-file path: {path}")
    return path


def _count_vcf_variants(vcf_path: Path) -> int:
    """
    Count non-header variant records in a VCF.

    Parameters
    ----------
    vcf_path : Path
        Path to VCF file.

    Returns
    -------
    int
        Variant record count.
    """
    count = 0
    with vcf_path.open("r", encoding="utf-8", errors="replace") as handle:
        for line in handle:
            if line.startswith("#"):
                continue
            if line.strip():
                count += 1
    return count


def _count_malformed_records(vcf_path: Path) -> int:
    """
    Count malformed non-header VCF records.

    A minimally valid VCF data line should contain at least 8 tab-delimited fields.

    Parameters
    ----------
    vcf_path : Path
        Path to VCF file.

    Returns
    -------
    int
        Count of malformed records.
    """
    malformed = 0
    with vcf_path.open("r", encoding="utf-8", errors="replace") as handle:
        for line in handle:
            if line.startswith("#"):
                continue
            if not line.strip():
                continue
            if len(line.rstrip("\n").split("\t")) < 8:
                malformed += 1
    return malformed


def run_stage(
    config: dict[str, Any],
    paths: dict[str, Any],
    logger,
    state: dict[str, Any],
) -> dict[str, Any]:
    """
    Execute Stage 06.

    Responsibilities
    ----------------
    - select the correct VCF input based on execution mode
    - validate reference FASTA
    - normalize variants with GATK LeftAlignAndTrimVariants
    - emit normalized VCF
    - update artifacts, QC, and stage output summaries
    """
    logger.info("Stage 06: normalizing VCF.")

    execution_mode = state["run"]["execution_mode"]

    if execution_mode == "full_pipeline":
        input_vcf = _validate_required_artifact(
            state["artifacts"].get("raw_vcf"),
            "raw VCF",
        )
    elif execution_mode == "annotation_only":
        input_vcf = _validate_required_artifact(
            state["inputs"].get("input_vcf"),
            "input VCF",
        )
    else:
        raise ValueError(f"Unsupported execution mode in Stage 06: {execution_mode}")

    reference_fasta = _validate_required_artifact(
        config["reference"].get("fasta_path"),
        "reference.fasta_path",
    )
    _validate_required_artifact(
        config["reference"].get("fasta_index"),
        "reference.fasta_index",
    )
    _validate_required_artifact(
        config["reference"].get("sequence_dictionary"),
        "reference.sequence_dictionary",
    )

    sample_id = state["sample"]["sample_id"]
    run_id = state["run"]["run_id"]
    normalized_vcf = Path(paths["interim_dir"]) / f"{sample_id}_{run_id}.normalized_variants.vcf"

    gatk_executable = config["tools"]["gatk"]["executable"]
    java_options = config["tools"]["gatk"].get("java_options", "")

    gatk_command = [gatk_executable]
    if java_options:
        gatk_command.extend(["--java-options", java_options])

    gatk_command.extend(
        [
            "LeftAlignAndTrimVariants",
            "-R",
            str(reference_fasta),
            "-V",
            str(input_vcf),
            "-O",
            str(normalized_vcf),
        ]
    )

    _run_command(gatk_command, logger, "GATK LeftAlignAndTrimVariants")

    if not normalized_vcf.exists():
        raise FileNotFoundError(f"Normalized VCF was not created: {normalized_vcf}")

    normalized_vcf_size = normalized_vcf.stat().st_size
    if normalized_vcf_size == 0:
        raise ValueError(f"Normalized VCF is empty: {normalized_vcf}")

    normalized_variant_count = _count_vcf_variants(normalized_vcf)
    malformed_records = _count_malformed_records(normalized_vcf)

    state["artifacts"]["normalized_vcf"] = str(normalized_vcf)

    state["qc"]["normalization_qc"] = {
        "normalization_completed": True,
        "execution_mode": execution_mode,
        "input_vcf": str(input_vcf),
        "normalized_vcf_exists": True,
        "normalized_vcf_size_bytes": normalized_vcf_size,
        "normalized_variant_count": normalized_variant_count,
        "malformed_records_skipped": malformed_records,
        "normalizer": "GATK LeftAlignAndTrimVariants",
        "reference_fasta": str(reference_fasta),
    }

    state["stage_outputs"]["stage_06_normalize_vcf"] = {
        "status": "success",
        "tool": "GATK LeftAlignAndTrimVariants",
        "execution_mode": execution_mode,
        "input_vcf": str(input_vcf),
        "normalized_vcf": str(normalized_vcf),
        "normalized_variant_count": normalized_variant_count,
        "malformed_records_skipped": malformed_records,
    }

    logger.info(f"Normalized VCF written to: {normalized_vcf}")
    logger.info(f"Normalized variant count: {normalized_variant_count}")
    logger.info(f"Malformed records skipped: {malformed_records}")

    return state