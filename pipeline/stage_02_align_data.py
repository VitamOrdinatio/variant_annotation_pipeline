"""
Stage 02: Align paired-end FASTQ reads to the reference genome.

Repo 2 v1.0 design notes:
- real-tool stage using BWA-MEM
- inputs are external compressed FASTQ files validated in Stage 01
- outputs are written under results/<run_id>/interim/
- alignment BAM is unsorted; sorting/indexing occur in Stage 03
"""

from __future__ import annotations

import gzip
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


def _count_fastq_reads(path_str: str) -> int:
    """
    Count reads in a FASTQ or FASTQ.GZ file.

    Parameters
    ----------
    path_str : str
        Path to FASTQ file.

    Returns
    -------
    int
        Number of reads.

    Raises
    ------
    ValueError
        If the FASTQ structure is malformed.
    """
    path = Path(path_str)
    opener = gzip.open if str(path).endswith(".gz") else open

    line_count = 0
    with opener(path, "rt", encoding="utf-8", errors="replace") as handle:
        for _ in handle:
            line_count += 1

    if line_count % 4 != 0:
        raise ValueError(f"Malformed FASTQ structure detected for {path}: line count {line_count} not divisible by 4")

    return line_count // 4


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
    return path


def _record_bwa_version(config: dict[str, Any], state: dict[str, Any], logger) -> None:
    """
    Record BWA version string in run metadata if possible.
    """
    bwa_executable = config["tools"]["bwa"]["executable"]
    try:
        result = subprocess.run(
            [bwa_executable],
            capture_output=True,
            text=True,
            check=False,
        )
        version_text = (result.stderr or result.stdout or "").strip().splitlines()
        if version_text:
            state["run"].setdefault("tool_versions", {})
            state["run"]["tool_versions"]["bwa"] = version_text[0]
            logger.info(f"Recorded BWA version: {version_text[0]}")
    except Exception as exc:  # pragma: no cover - defensive only
        state["warnings"].append(f"Unable to record BWA version: {exc}")
        logger.warning(f"Unable to record BWA version: {exc}")


def run_stage(
    config: dict[str, Any],
    paths: dict[str, Any],
    logger,
    state: dict[str, Any],
) -> dict[str, Any]:
    """
    Execute Stage 02.

    Responsibilities
    ----------------
    - validate FASTQ inputs and reference resources
    - count input reads
    - run BWA-MEM alignment
    - write unsorted aligned BAM
    - update state, QC, and stage output summaries
    """
    logger.info("Stage 02: aligning sequencing reads.")

    execution_mode = state["run"]["execution_mode"]
    if execution_mode != "full_pipeline":
        logger.info("Stage 02 skipped internally because execution mode is not full_pipeline.")
        state["stage_outputs"]["stage_02_align_data"] = {"status": "skipped"}
        return state

    fastq_1 = _validate_required_artifact(state["inputs"].get("fastq_1"), "FASTQ R1")
    fastq_2 = _validate_required_artifact(state["inputs"].get("fastq_2"), "FASTQ R2")

    reference_fasta = _validate_required_artifact(
        config["reference"].get("fasta_path"),
        "reference.fasta_path",
    )
    _validate_required_artifact(
        config["reference"].get("fasta_index"),
        "reference.fasta_index",
    )

    bwa_index_prefix = config["reference"].get("bwa_index_prefix")
    if not bwa_index_prefix:
        raise ValueError("Missing required config key: reference.bwa_index_prefix")

    bwa_index_prefix_path = Path(bwa_index_prefix)
    expected_bwa_index_suffixes = [".amb", ".ann", ".bwt", ".pac", ".sa"]
    missing_index_files = []
    for suffix in expected_bwa_index_suffixes:
        candidate = Path(f"{bwa_index_prefix}{suffix}")
        if not candidate.exists():
            missing_index_files.append(str(candidate))
    if missing_index_files:
        raise FileNotFoundError(
            "Missing required BWA index files: " + ", ".join(missing_index_files)
        )

    read_count_r1 = _count_fastq_reads(str(fastq_1))
    read_count_r2 = _count_fastq_reads(str(fastq_2))

    if read_count_r1 != read_count_r2:
        raise ValueError(
            f"FASTQ pair read-count mismatch: R1={read_count_r1}, R2={read_count_r2}"
        )

    logger.info(f"FASTQ R1 reads detected: {read_count_r1}")
    logger.info(f"FASTQ R2 reads detected: {read_count_r2}")

    run_id = state["run"]["run_id"]
    sample_id = state["sample"]["sample_id"]
    aligned_bam = Path(paths["interim_dir"]) / f"{sample_id}_{run_id}.aligned.bam"
    sam_output = Path(paths["interim_dir"]) / f"{sample_id}_{run_id}.aligned.sam"

    bwa_executable = config["tools"]["bwa"]["executable"]
    samtools_executable = config["tools"]["samtools"]["executable"]
    bwa_threads = str(config["tools"]["bwa"]["threads"])

    read_group = (
        f"@RG\\tID:{sample_id}\\tSM:{sample_id}"
        f"\\tPL:ILLUMINA\\tLB:{sample_id}_lib1\\tPU:{state['sample']['sra_accession']}"
    )

    bwa_command = [
        bwa_executable,
        config["tools"]["bwa"]["mode"],
        "-t",
        bwa_threads,
        "-R",
        read_group,
        bwa_index_prefix,
        str(fastq_1),
        str(fastq_2),
    ]

    logger.info(f"Temporary SAM output path: {sam_output}")
    with sam_output.open("w", encoding="utf-8") as sam_handle:
        bwa_result = subprocess.run(
            bwa_command,
            stdout=sam_handle,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )

    if bwa_result.stderr and bwa_result.stderr.strip():
        logger.info(f"BWA stderr: {bwa_result.stderr.strip()}")

    if bwa_result.returncode != 0:
        if sam_output.exists():
            sam_output.unlink()
        raise RuntimeError(f"BWA-MEM alignment failed with exit code {bwa_result.returncode}")

    view_command = [
        samtools_executable,
        "view",
        "-bS",
        "-o",
        str(aligned_bam),
        str(sam_output),
    ]
    _run_command(view_command, logger, "samtools view")

    if sam_output.exists():
        sam_output.unlink()

    if not aligned_bam.exists():
        raise FileNotFoundError(f"Aligned BAM was not created: {aligned_bam}")

    aligned_bam_size = aligned_bam.stat().st_size
    if aligned_bam_size == 0:
        raise ValueError(f"Aligned BAM is empty: {aligned_bam}")

    state["artifacts"]["aligned_bam"] = str(aligned_bam)

    state["qc"]["alignment_qc"] = {
        "alignment_completed": True,
        "read_count_r1": read_count_r1,
        "read_count_r2": read_count_r2,
        "paired_read_count_match": True,
        "aligned_bam_exists": True,
        "aligned_bam_size_bytes": aligned_bam_size,
        "reference_fasta": str(reference_fasta),
        "bwa_index_prefix": bwa_index_prefix,
    }

    state["stage_outputs"]["stage_02_align_data"] = {
        "status": "success",
        "tool": "bwa mem",
        "aligned_bam": str(aligned_bam),
        "read_count_r1": read_count_r1,
        "read_count_r2": read_count_r2,
    }

    if config["runtime"]["record_tool_versions"]:
        _record_bwa_version(config, state, logger)

    logger.info(f"Aligned BAM written to: {aligned_bam}")

    return state