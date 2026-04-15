"""
Stage 04: QC aligned reads from sorted BAM.

Repo 2 v1.0 design notes:
- inputs:
  - sorted BAM
  - sorted BAM index
- tool: samtools flagstat
- output:
  - aligned-read QC report
- writes outputs under results/<run_id>/reports/
"""

from __future__ import annotations

import re
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


def _extract_first_integer(text: str) -> int | None:
    """
    Extract the first integer from a line of text.

    Parameters
    ----------
    text : str
        Input line.

    Returns
    -------
    int | None
        Parsed integer or None if no integer is found.
    """
    match = re.search(r"^\s*(\d+)", text)
    return int(match.group(1)) if match else None


def _parse_flagstat(flagstat_text: str) -> dict[str, Any]:
    """
    Parse selected QC metrics from samtools flagstat output.

    Parameters
    ----------
    flagstat_text : str
        Full stdout text from samtools flagstat.

    Returns
    -------
    dict[str, Any]
        Parsed metrics dictionary.
    """
    total_reads = None
    mapped_reads = None
    paired_reads = None
    properly_paired_reads = None
    singleton_reads = None

    for raw_line in flagstat_text.splitlines():
        line = raw_line.strip()

        if "in total" in line and total_reads is None:
            total_reads = _extract_first_integer(line)
        elif "mapped (" in line and mapped_reads is None:
            mapped_reads = _extract_first_integer(line)
        elif "paired in sequencing" in line and paired_reads is None:
            paired_reads = _extract_first_integer(line)
        elif "properly paired (" in line and properly_paired_reads is None:
            properly_paired_reads = _extract_first_integer(line)
        elif "singletons (" in line and singleton_reads is None:
            singleton_reads = _extract_first_integer(line)

    mapping_rate = None
    if total_reads and mapped_reads is not None and total_reads > 0:
        mapping_rate = round(mapped_reads / total_reads, 6)

    properly_paired_rate = None
    if paired_reads and properly_paired_reads is not None and paired_reads > 0:
        properly_paired_rate = round(properly_paired_reads / paired_reads, 6)

    return {
        "total_reads": total_reads,
        "mapped_reads": mapped_reads,
        "paired_reads": paired_reads,
        "properly_paired_reads": properly_paired_reads,
        "singleton_reads": singleton_reads,
        "mapping_rate": mapping_rate,
        "properly_paired_rate": properly_paired_rate,
    }


def run_stage(
    config: dict[str, Any],
    paths: dict[str, Any],
    logger,
    state: dict[str, Any],
) -> dict[str, Any]:
    """
    Execute Stage 04.

    Responsibilities
    ----------------
    - validate sorted BAM + index from Stage 03
    - run samtools flagstat
    - write aligned-read QC report
    - update QC summaries and stage outputs
    """
    logger.info("Stage 04: QC aligned reads.")

    execution_mode = state["run"]["execution_mode"]
    if execution_mode != "full_pipeline":
        logger.info("Stage 04 skipped internally because execution mode is not full_pipeline.")
        state["stage_outputs"]["stage_04_qc_aligned_reads"] = {"status": "skipped"}
        return state

    sorted_bam = _validate_required_artifact(
        state["artifacts"].get("sorted_bam"),
        "sorted BAM",
    )
    sorted_bam_index = _validate_required_artifact(
        state["artifacts"].get("sorted_bam_index"),
        "sorted BAM index",
    )

    samtools_executable = config["tools"]["samtools"]["executable"]
    flagstat_command = [
        samtools_executable,
        "flagstat",
        str(sorted_bam),
    ]
    result = _run_command(flagstat_command, logger, "samtools flagstat")

    flagstat_text = result.stdout.strip()
    if not flagstat_text:
        raise ValueError("samtools flagstat produced empty output")

    metrics = _parse_flagstat(flagstat_text)

    sample_id = state["sample"]["sample_id"]
    run_id = state["run"]["run_id"]
    qc_report_path = Path(paths["reports_dir"]) / f"{sample_id}_{run_id}.aligned_read_qc_report.txt"

    with qc_report_path.open("w", encoding="utf-8") as handle:
        handle.write("Aligned Read QC Report\n")
        handle.write("======================\n\n")
        handle.write(f"sample_id: {sample_id}\n")
        handle.write(f"run_id: {run_id}\n")
        handle.write(f"sorted_bam: {sorted_bam}\n")
        handle.write(f"sorted_bam_index: {sorted_bam_index}\n\n")
        handle.write("Parsed metrics\n")
        handle.write("--------------\n")
        for key, value in metrics.items():
            handle.write(f"{key}: {value}\n")
        handle.write("\nRaw samtools flagstat output\n")
        handle.write("----------------------------\n")
        handle.write(flagstat_text)
        handle.write("\n")

    if not qc_report_path.exists():
        raise FileNotFoundError(f"Aligned-read QC report was not created: {qc_report_path}")

    state["artifacts"]["aligned_qc_report"] = str(qc_report_path)

    alignment_qc = state["qc"].setdefault("alignment_qc", {})
    alignment_qc.update(
        {
            "alignment_completed": True,
            "sorted_bam_exists": True,
            "sorted_bam_index_exists": True,
            "qc_report_exists": True,
            "qc_report_path": str(qc_report_path),
            "total_reads": metrics["total_reads"],
            "mapped_reads": metrics["mapped_reads"],
            "paired_reads": metrics["paired_reads"],
            "properly_paired_reads": metrics["properly_paired_reads"],
            "singleton_reads": metrics["singleton_reads"],
            "mapping_rate": metrics["mapping_rate"],
            "properly_paired_rate": metrics["properly_paired_rate"],
        }
    )

    state["stage_outputs"]["stage_04_qc_aligned_reads"] = {
        "status": "success",
        "tool": "samtools flagstat",
        "sorted_bam": str(sorted_bam),
        "sorted_bam_index": str(sorted_bam_index),
        "qc_report": str(qc_report_path),
        "total_reads": metrics["total_reads"],
        "mapped_reads": metrics["mapped_reads"],
        "mapping_rate": metrics["mapping_rate"],
    }

    logger.info(f"Aligned-read QC report written to: {qc_report_path}")

    return state