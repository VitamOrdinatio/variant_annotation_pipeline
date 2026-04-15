"""
Stage 05: Call variants from processed BAM.

Repo 2 v1.0 design notes:
- inputs:
  - sorted BAM
  - sorted BAM index
  - reference FASTA
  - reference sequence dictionary
- tool: GATK HaplotypeCaller
- output:
  - raw VCF
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


def _record_gatk_version(config: dict[str, Any], state: dict[str, Any], logger) -> None:
    """
    Record GATK version string in run metadata if possible.
    """
    gatk_executable = config["tools"]["gatk"]["executable"]
    try:
        result = subprocess.run(
            [gatk_executable, "--version"],
            capture_output=True,
            text=True,
            check=False,
        )
        version_text = (result.stdout or result.stderr or "").strip().splitlines()
        if version_text:
            state["run"].setdefault("tool_versions", {})
            state["run"]["tool_versions"]["gatk"] = version_text[0]
            logger.info(f"Recorded GATK version: {version_text[0]}")
    except Exception as exc:  # pragma: no cover
        state["warnings"].append(f"Unable to record GATK version: {exc}")
        logger.warning(f"Unable to record GATK version: {exc}")


def run_stage(
    config: dict[str, Any],
    paths: dict[str, Any],
    logger,
    state: dict[str, Any],
) -> dict[str, Any]:
    """
    Execute Stage 05.

    Responsibilities
    ----------------
    - validate sorted BAM and BAM index
    - validate reference FASTA and sequence dictionary
    - run GATK HaplotypeCaller
    - emit raw VCF
    - update artifacts, QC, and stage output summaries
    """
    logger.info("Stage 05: calling variants.")

    execution_mode = state["run"]["execution_mode"]
    if execution_mode != "full_pipeline":
        logger.info("Stage 05 skipped internally because execution mode is not full_pipeline.")
        state["stage_outputs"]["stage_05_call_variants"] = {"status": "skipped"}
        return state

    sorted_bam = _validate_required_artifact(
        state["artifacts"].get("sorted_bam"),
        "sorted BAM",
    )
    sorted_bam_index = _validate_required_artifact(
        state["artifacts"].get("sorted_bam_index"),
        "sorted BAM index",
    )
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
    raw_vcf = Path(paths["interim_dir"]) / f"{sample_id}_{run_id}.raw_variants.vcf"

    gatk_executable = config["tools"]["gatk"]["executable"]
    java_options = config["tools"]["gatk"].get("java_options", "")
    emit_mode = config["tools"]["gatk"].get("haplotypecaller_emit_mode", "discovery")

    gatk_command = [gatk_executable]
    if java_options:
        gatk_command.extend(["--java-options", java_options])

    gatk_command.extend(
        [
            "HaplotypeCaller",
            "-R",
            str(reference_fasta),
            "-I",
            str(sorted_bam),
            "-O",
            str(raw_vcf),
            "--emit-ref-confidence",
            "NONE",
        ]
    )

    # GATK uses standard discovery behavior by default; keep explicit extension point in config.
    if emit_mode.lower() != "discovery":
        logger.warning(
            f"Configured haplotypecaller_emit_mode={emit_mode} is not explicitly handled; "
            "proceeding with standard discovery mode."
        )
        state["warnings"].append(
            f"Unhandled haplotypecaller_emit_mode={emit_mode}; standard discovery mode used."
        )

    _run_command(gatk_command, logger, "GATK HaplotypeCaller")

    if not raw_vcf.exists():
        raise FileNotFoundError(f"Raw VCF was not created: {raw_vcf}")

    raw_vcf_size = raw_vcf.stat().st_size
    if raw_vcf_size == 0:
        raise ValueError(f"Raw VCF is empty: {raw_vcf}")

    variant_count = _count_vcf_variants(raw_vcf)

    state["artifacts"]["raw_vcf"] = str(raw_vcf)

    state["qc"]["variant_calling_qc"] = {
        "variant_calling_completed": True,
        "sorted_bam_exists": True,
        "sorted_bam_index_exists": True,
        "raw_vcf_exists": True,
        "raw_vcf_size_bytes": raw_vcf_size,
        "variant_count": variant_count,
        "caller": "GATK HaplotypeCaller",
        "reference_fasta": str(reference_fasta),
    }

    state["stage_outputs"]["stage_05_call_variants"] = {
        "status": "success",
        "tool": "GATK HaplotypeCaller",
        "input_sorted_bam": str(sorted_bam),
        "input_sorted_bam_index": str(sorted_bam_index),
        "raw_vcf": str(raw_vcf),
        "variant_count": variant_count,
    }

    if config["runtime"]["record_tool_versions"]:
        _record_gatk_version(config, state, logger)

    logger.info(f"Raw VCF written to: {raw_vcf}")
    logger.info(f"Variant count: {variant_count}")

    return state