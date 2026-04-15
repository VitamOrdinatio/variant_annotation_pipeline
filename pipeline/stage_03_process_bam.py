"""
Stage 03: Process aligned BAM.

Repo 2 v1.0 design notes:
- input: unsorted aligned BAM from Stage 02
- tool: samtools
- outputs:
  - sorted BAM
  - sorted BAM index
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


def _record_samtools_version(config: dict[str, Any], state: dict[str, Any], logger) -> None:
    """
    Record samtools version string in run metadata if possible.
    """
    samtools_executable = config["tools"]["samtools"]["executable"]
    try:
        result = subprocess.run(
            [samtools_executable, "--version"],
            capture_output=True,
            text=True,
            check=False,
        )
        version_text = (result.stdout or result.stderr or "").strip().splitlines()
        if version_text:
            state["run"].setdefault("tool_versions", {})
            state["run"]["tool_versions"]["samtools"] = version_text[0]
            logger.info(f"Recorded samtools version: {version_text[0]}")
    except Exception as exc:  # pragma: no cover - defensive only
        state["warnings"].append(f"Unable to record samtools version: {exc}")
        logger.warning(f"Unable to record samtools version: {exc}")


def run_stage(
    config: dict[str, Any],
    paths: dict[str, Any],
    logger,
    state: dict[str, Any],
) -> dict[str, Any]:
    """
    Execute Stage 03.

    Responsibilities
    ----------------
    - validate aligned BAM from Stage 02
    - sort BAM using samtools
    - index sorted BAM using samtools
    - update artifacts, QC, and stage outputs
    """
    logger.info("Stage 03: processing aligned BAM.")

    execution_mode = state["run"]["execution_mode"]
    if execution_mode != "full_pipeline":
        logger.info("Stage 03 skipped internally because execution mode is not full_pipeline.")
        state["stage_outputs"]["stage_03_process_bam"] = {"status": "skipped"}
        return state

    aligned_bam = _validate_required_artifact(
        state["artifacts"].get("aligned_bam"),
        "aligned BAM",
    )

    samtools_executable = config["tools"]["samtools"]["executable"]
    samtools_threads = str(config["tools"]["samtools"]["threads"])

    sample_id = state["sample"]["sample_id"]
    run_id = state["run"]["run_id"]

    sorted_bam = Path(paths["interim_dir"]) / f"{sample_id}_{run_id}.aligned.sorted.bam"
    sorted_bam_index = Path(f"{sorted_bam}.bai")

    sort_command = [
        samtools_executable,
        "sort",
        "-@",
        samtools_threads,
        "-o",
        str(sorted_bam),
        str(aligned_bam),
    ]
    _run_command(sort_command, logger, "samtools sort")

    if not sorted_bam.exists():
        raise FileNotFoundError(f"Sorted BAM was not created: {sorted_bam}")

    sorted_bam_size = sorted_bam.stat().st_size
    if sorted_bam_size == 0:
        raise ValueError(f"Sorted BAM is empty: {sorted_bam}")

    index_command = [
        samtools_executable,
        "index",
        str(sorted_bam),
    ]
    _run_command(index_command, logger, "samtools index")

    if not sorted_bam_index.exists():
        raise FileNotFoundError(f"Sorted BAM index was not created: {sorted_bam_index}")

    sorted_bam_index_size = sorted_bam_index.stat().st_size
    if sorted_bam_index_size == 0:
        raise ValueError(f"Sorted BAM index is empty: {sorted_bam_index}")

    state["artifacts"]["sorted_bam"] = str(sorted_bam)
    state["artifacts"]["sorted_bam_index"] = str(sorted_bam_index)
    state["artifacts"]["aligned_bam_index"] = str(sorted_bam_index)

    state["qc"]["bam_processing_qc"] = {
        "bam_processing_completed": True,
        "aligned_bam_exists": True,
        "sorted_bam_exists": True,
        "bam_index_exists": True,
        "sorted_bam_size_bytes": sorted_bam_size,
        "sorted_bam_index_size_bytes": sorted_bam_index_size,
    }

    state["stage_outputs"]["stage_03_process_bam"] = {
        "status": "success",
        "tool": "samtools",
        "input_aligned_bam": str(aligned_bam),
        "sorted_bam": str(sorted_bam),
        "sorted_bam_index": str(sorted_bam_index),
    }

    if config["runtime"]["record_tool_versions"]:
        _record_samtools_version(config, state, logger)

    logger.info(f"Sorted BAM written to: {sorted_bam}")
    logger.info(f"Sorted BAM index written to: {sorted_bam_index}")

    return state