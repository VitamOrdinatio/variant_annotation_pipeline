"""
Pipeline runner for variant_annotation_pipeline v1.0.

Responsibilities:
- initialize run metadata and state
- resolve run directories
- load stage modules
- execute stages in strict order
- record failures and final metadata
"""

from __future__ import annotations

import csv
import importlib
import json
import logging
import socket
import traceback

from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
import hashlib
import platform
import subprocess
import sys



STAGE_ORDER = [
    "stage_01_load_data",
    "stage_02_align_data",
    "stage_03_process_bam",
    "stage_04_qc_aligned_reads",
    "stage_05_call_variants",
    "stage_06_normalize_vcf",
    "stage_07_annotate_variants",
    "stage_08_filter_and_partition",
    "stage_09_interpret_coding",
    "stage_10_interpret_noncoding",
    "stage_11_prioritize_variants",
    "stage_12_validate_variants",
    "stage_13_write_summary",
]


def generate_run_id() -> str:
    """
    Generate a deterministic-format timestamp-based run identifier.

    Returns
    -------
    str
        Run identifier of the form run_YYYY_MM_DD_HHMMSS.
    """
    return datetime.now(timezone.utc).strftime("run_%Y_%m_%d_%H%M%S")


def ensure_directory(path: str | Path) -> Path:
    """
    Create a directory if it does not already exist.

    Parameters
    ----------
    path : str | Path
        Directory path.

    Returns
    -------
    Path
        Resolved Path object.
    """
    directory = Path(path)
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def sha256_file(path: str | Path) -> str:
    file_path = Path(path)
    digest = hashlib.sha256()
    with file_path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()

def get_git_commit(repo_root: str | Path = ".") -> str:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=repo_root,
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout.strip()
    except Exception:
        return "unknown"

def write_run_fingerprint(
    config: dict[str, Any],
    config_path: str,
    run_id: str,
    run_paths: dict[str, str],
) -> None:
    reference_fasta = config["reference"]["fasta_path"]
    fingerprint = {
        "run_id": run_id,
        "pipeline_name": config["project"]["pipeline_name"],
        "pipeline_version": config["project"]["version"],
        "git_commit": get_git_commit(),
        "config_hash": sha256_file(config_path),
        "config_path": str(config_path),
        "reference_genome": config["reference"]["genome_build"],
        "reference_fasta_path": reference_fasta,
        "reference_fasta_hash_or_size": Path(reference_fasta).stat().st_size if Path(reference_fasta).exists() else "unavailable",
        "hostname": socket.gethostname(),
        "execution_mode": config["mode"]["execution_mode"],
        "execution_profile": config.get("execution_profile", {}).get("name", "default"),
        "python_version": sys.version,
        "platform": platform.platform(),
        "created_at": utc_now_iso(),
    }
    with Path(run_paths["run_fingerprint_path"]).open("w", encoding="utf-8") as handle:
        handle.write(stable_json_dumps(fingerprint))


def reconfigure_run_logger(
    logger,
    log_path: str,
    level: str = "INFO",
):
    """
    Rebind an existing logger to the canonical run log path.

    Parameters
    ----------
    logger : logging.Logger
        Existing bootstrap logger.
    log_path : str
        Canonical run log path.
    level : str
        Logging level.

    Returns
    -------
    logging.Logger
        Reconfigured logger.
    """
    logger.handlers.clear()

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    file_handler = logging.FileHandler(log_path)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    logger.setLevel(getattr(logging, level.upper(), logging.INFO))
    logger.propagate = False

    return logger


def initialize_run_paths(config: dict[str, Any], run_id: str) -> dict[str, str]:
    """
    Initialize the run directory structure for a single execution.

    Parameters
    ----------
    config : dict[str, Any]
        Parsed pipeline configuration.
    run_id : str
        Run identifier.

    Returns
    -------
    dict[str, str]
        Dictionary of resolved run paths.
    """
    base_results_dir = ensure_directory(config["output"]["base_results_dir"])
    run_dir = ensure_directory(base_results_dir / run_id)
    logs_dir = ensure_directory(run_dir / "logs")
    metadata_dir = ensure_directory(run_dir / "metadata")
    stage_summaries_dir = ensure_directory(metadata_dir / "stage_summaries")
    interim_dir = ensure_directory(run_dir / "interim")
    processed_dir = ensure_directory(run_dir / "processed")
    reports_dir = ensure_directory(run_dir / "reports")
    final_dir = ensure_directory(run_dir / "final")
    validation_dir = ensure_directory(run_dir / "validation")

    return {
        "base_results_dir": str(base_results_dir),
        "run_dir": str(run_dir),
        "logs_dir": str(logs_dir),
        "metadata_dir": str(metadata_dir),
        "stage_summaries_dir": str(stage_summaries_dir),
        "interim_dir": str(interim_dir),
        "processed_dir": str(processed_dir),
        "reports_dir": str(reports_dir),
        "final_dir": str(final_dir),
        "validation_dir": str(validation_dir),
        "legacy_config_snapshot_path": str(run_dir / "config_used.yaml"),
        "legacy_metadata_path": str(run_dir / "metadata.json"),
        "config_snapshot_path": str(metadata_dir / "config_snapshot.yaml"),
        "run_metadata_path": str(metadata_dir / "run_metadata.json"),
        "run_fingerprint_path": str(metadata_dir / "run_fingerprint.json"),
        "runtime_profile_path": str(metadata_dir / "runtime_profile.tsv"),
        "log_path": str(logs_dir / config["logging"]["log_filename"]),
    }


def initialize_state(
    config: dict[str, Any],
    config_path: str,
    run_id: str,
    run_paths: dict[str, str],
) -> dict[str, Any]:
    """
    Initialize the shared runtime state object.

    Parameters
    ----------
    config : dict[str, Any]
        Parsed pipeline configuration.
    config_path : str
        Original config path.
    run_id : str
        Run identifier.
    run_paths : dict[str, str]
        Resolved run paths.

    Returns
    -------
    dict[str, Any]
        Initialized state object.
    """
    now = utc_now_iso()
    execution_mode = config["mode"]["execution_mode"]
    machine_id = socket.gethostname()

    return {
        "run": {
            "run_id": run_id,
            "status": "initialized",
            "execution_mode": execution_mode,
            "pipeline_name": config["project"]["pipeline_name"],
            "pipeline_version": config["project"]["version"],
            "config_path": config_path,
            "config_snapshot_path": run_paths["config_snapshot_path"],
            "start_time": now,
            "end_time": None,
            "machine_id": machine_id,
        },
        "sample": {},
        "inputs": {},
        "artifacts": {
            "aligned_bam": None,
            "aligned_bam_index": None,
            "sorted_bam": None,
            "sorted_bam_index": None,
            "aligned_qc_report": None,
            "raw_vcf": None,
            "normalized_vcf": None,
            "annotated_vcf": None,
            "annotated_table": None,
            "filtered_table": None,
            "coding_table": None,
            "noncoding_table": None,
            "interpreted_coding_table": None,
            "interpreted_noncoding_table": None,
            "prioritized_table": None,
            "validation_notes": None,
            "igv_review_candidates": None,
            "gene_summary_table": None,
            "run_summary_report": None,
        },
        "annotations": {
            "annotation_engine": config["annotation"]["engine"],
            "annotation_completed": False,
            "resources_used": [],
            "clinvar_enabled": bool(config["annotation"]["include_clinvar"]),
            "population_frequency_sources": list(config["annotation"]["population_sources"]),
        },
        "gene_sets": {
            "mitocarta_path": config["gene_sets"]["mitocarta_path"],
            "genes4epilepsy_path": config["gene_sets"]["genes4epilepsy_path"],
            "overlay_completed": False,
            "flags_added": list(config["gene_sets"]["required_flags"]),
        },
        "qc": {
            "input_qc": {},
            "alignment_qc": {},
            "bam_processing_qc": {},
            "variant_calling_qc": {},
            "normalization_qc": {},
            "annotation_qc": {},
            "filtering_qc": {},
            "interpretation_qc": {},
            "validation_qc": {},
        },
        "stage_outputs": {stage_name: {"status": "not_started"} for stage_name in STAGE_ORDER},
        "warnings": [],
        "errors": [],
        "reports": {
            "run_summary_report": None,
            "summary_table": None,
            "gene_summary_table": None,
            "report_line_count": None,
        },
    }


def get_stage_module(stage_name: str):
    """
    Import a stage module dynamically.

    Parameters
    ----------
    stage_name : str
        Stage module base name.

    Returns
    -------
    module
        Imported Python module.
    """
    return importlib.import_module(f"pipeline.{stage_name}")


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def elapsed_seconds(start_iso: str, end_iso: str) -> float:
    start = datetime.fromisoformat(start_iso)
    end = datetime.fromisoformat(end_iso)
    return round((end - start).total_seconds(), 3)


def write_stage_summary(stage_name: str, stage_data: dict[str, Any], stage_summaries_dir: str) -> None:
    stage_number = stage_name.split("_")[1]
    output_path = Path(stage_summaries_dir) / f"stage_{stage_number}_summary.json"
    summary = {
        "stage": stage_name,
        "status": stage_data.get("status", "not_started"),
        "start_time": stage_data.get("start_time"),
        "end_time": stage_data.get("end_time"),
        "elapsed_seconds": stage_data.get("elapsed_seconds"),
        "input_artifacts": stage_data.get("input_artifacts", []),
        "output_artifacts": stage_data.get("output_artifacts", []),
        "warning_count": stage_data.get("warning_count", 0),
        "error_count": stage_data.get("error_count", 0),
    }
    with output_path.open("w", encoding="utf-8") as handle:
        handle.write(stable_json_dumps(summary))


def write_runtime_profile(state: dict[str, Any], runtime_profile_path: str) -> None:
    fieldnames = ["stage", "status", "start_time", "end_time", "elapsed_seconds"]
    output_path = Path(runtime_profile_path)
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        for stage_name in STAGE_ORDER:
            stage_data = state.get("stage_outputs", {}).get(stage_name, {})
            writer.writerow({
                "stage": stage_name,
                "status": stage_data.get("status", "not_started"),
                "start_time": stage_data.get("start_time", "NA"),
                "end_time": stage_data.get("end_time", "NA"),
                "elapsed_seconds": stage_data.get("elapsed_seconds", "NA"),
            })


def stable_json_dumps(payload: dict[str, Any]) -> str:
    return json.dumps(payload, indent=2, sort_keys=True)


def write_run_metadata(state: dict[str, Any], run_metadata_path: str) -> None:
    stage_outputs = state.get("stage_outputs", {})
    stage_status_counts: dict[str, int] = {}
    for stage_data in stage_outputs.values():
        status = stage_data.get("status", "unknown")
        stage_status_counts[status] = stage_status_counts.get(status, 0) + 1

    run = state.get("run", {})
    run_metadata = {
        "run": {
            "run_id": run.get("run_id"),
            "status": run.get("status"),
            "pipeline_name": run.get("pipeline_name"),
            "pipeline_version": run.get("pipeline_version"),
            "execution_mode": run.get("execution_mode"),
            "machine_id": run.get("machine_id"),
            "start_time": run.get("start_time"),
            "end_time": run.get("end_time"),
            "config_path": run.get("config_path"),
            "config_snapshot_path": run.get("config_snapshot_path"),
        },
        "summary": {
            "stage_count": len(stage_outputs),
            "stage_status_counts": stage_status_counts,
            "warning_count": len(state.get("warnings", [])),
            "error_count": len(state.get("errors", [])),
        },
        "artifacts": {
            "run_summary_report": state.get("reports", {}).get("run_summary_report"),
            "gene_summary_table": state.get("reports", {}).get("gene_summary_table"),
            "prioritized_table": state.get("artifacts", {}).get("prioritized_table"),
            "validation_notes": state.get("artifacts", {}).get("validation_notes"),
        },
    }

    with Path(run_metadata_path).open("w", encoding="utf-8") as handle:
        handle.write(stable_json_dumps(run_metadata))


def write_metadata(state: dict[str, Any], metadata_path: str) -> None:
    """
    Write the current state to metadata JSON.

    Parameters
    ----------
    state : dict[str, Any]
        Runtime state.
    metadata_path : str
        Metadata output path.
    """
    metadata_file = Path(metadata_path)
    with metadata_file.open("w", encoding="utf-8") as handle:
        handle.write(stable_json_dumps(state))


def save_config_snapshot(config: dict[str, Any], snapshot_path: str) -> None:
    """
    Save the config dictionary to the run directory.

    Parameters
    ----------
    config : dict[str, Any]
        Parsed pipeline configuration.
    snapshot_path : str
        Destination config snapshot path.
    """
    import yaml

    with Path(snapshot_path).open("w", encoding="utf-8") as handle:
        yaml.safe_dump(config, handle, sort_keys=False)


def should_run_stage(config: dict[str, Any], stage_name: str) -> bool:
    """
    Determine whether a stage should execute for the current mode.

    Parameters
    ----------
    config : dict[str, Any]
        Parsed pipeline configuration.
    stage_name : str
        Stage name.

    Returns
    -------
    bool
        True if the stage should run.
    """
    execution_mode = config["mode"]["execution_mode"]

    if execution_mode == "annotation_only":
        skipped_stages = {
            "stage_02_align_data",
            "stage_03_process_bam",
            "stage_04_qc_aligned_reads",
            "stage_05_call_variants",
        }
        return stage_name not in skipped_stages

    return True


def run_pipeline(
    config: dict[str, Any],
    config_path: str,
    logger,
) -> tuple[dict[str, Any], dict[str, str]]:
    """
    Execute the full pipeline in strict stage order.

    Parameters
    ----------
    config : dict[str, Any]
        Parsed pipeline configuration.
    config_path : str
        Original config path.
    logger : logging.Logger
        Configured logger.

    Returns
    -------
    tuple[dict[str, Any], dict[str, str]]
        Final state and run path dictionary.
    """
    run_id = generate_run_id()
    run_paths = initialize_run_paths(config, run_id)
    logger = reconfigure_run_logger(
        logger=logger,
        log_path=run_paths["log_path"],
        level=config["logging"]["level"],
    )

    logger.info("Transitioned from bootstrap logger to canonical run logger.")
    logger.info(f"Canonical log path: {run_paths['log_path']}")    
    save_config_snapshot(config, run_paths["config_snapshot_path"])
    write_run_fingerprint(
        config=config,
        config_path=config_path,
        run_id=run_id,
        run_paths=run_paths,
    )
    logger.info(f"Run fingerprint written to: {run_paths['run_fingerprint_path']}")
    state = initialize_state(
        config=config,
        config_path=config_path,
        run_id=run_id,
        run_paths=run_paths,
    )

    state["run"]["status"] = "running"

    logger.info("Pipeline run started.")
    logger.info(f"Run ID: {run_id}")
    logger.info(f"Execution mode: {config['mode']['execution_mode']}")
    logger.info(f"Run directory: {run_paths['run_dir']}")

    try:
        for stage_name in STAGE_ORDER:
            if not should_run_stage(config, stage_name):
                logger.info(f"Skipping stage: {stage_name}")
                skip_time = utc_now_iso()
                state["stage_outputs"][stage_name] = {
                    "status": "skipped",
                    "start_time": skip_time,
                    "end_time": skip_time,
                    "elapsed_seconds": 0.0,
                }
                write_stage_summary(
                    stage_name=stage_name,
                    stage_data=state["stage_outputs"][stage_name],
                    stage_summaries_dir=run_paths["stage_summaries_dir"],
                )                
                continue

            stage_start = utc_now_iso()
            state["stage_outputs"][stage_name] = {
                "status": "running",
                "start_time": stage_start,
                "end_time": None,
                "elapsed_seconds": None,
            }
            logger.info(f"Starting stage: {stage_name}")
            stage_module = get_stage_module(stage_name)

            if not hasattr(stage_module, "run_stage"):
                raise AttributeError(f"{stage_name} does not define run_stage().")

            stage_state_before = deepcopy(state)
            state = stage_module.run_stage(config, run_paths, logger, state)

            if not isinstance(state, dict):
                raise TypeError(f"{stage_name} returned non-dict state.")

            if stage_name not in state.get("stage_outputs", {}):
                state.setdefault("stage_outputs", {})
                state["stage_outputs"][stage_name] = {"status": "success"}

            if state["stage_outputs"][stage_name].get("status") == "not_started":
                state["stage_outputs"][stage_name]["status"] = "success"

            stage_end = utc_now_iso()
            state["stage_outputs"][stage_name].update({
                "status": "success",
                "end_time": stage_end,
                "elapsed_seconds": elapsed_seconds(stage_start, stage_end),
            })
            logger.info(f"Completed stage: {stage_name}")
            write_stage_summary(
                stage_name=stage_name,
                stage_data=state["stage_outputs"][stage_name],
                stage_summaries_dir=run_paths["stage_summaries_dir"],
            )
            if config["runtime"]["record_tool_versions"]:
                state.setdefault("run", {})
                state["run"].setdefault("tool_versions_recorded", False)

            # Basic safeguard against accidental state erasure.
            for required_key in [
                "run",
                "sample",
                "inputs",
                "artifacts",
                "annotations",
                "gene_sets",
                "qc",
                "stage_outputs",
                "warnings",
                "errors",
                "reports",
            ]:
                if required_key not in state:
                    state = stage_state_before
                    raise KeyError(f"{stage_name} removed required top-level state key: {required_key}")

        state["run"]["status"] = "completed"

    except Exception as exc:
        logger.error(f"Pipeline run failed: {exc}")
        logger.error(traceback.format_exc())

        state["errors"].append(str(exc))
        state["run"]["status"] = "failed"

        # Mark the currently failing stage if possible.
        last_started = None
        for stage_name in STAGE_ORDER:
            if state["stage_outputs"].get(stage_name, {}).get("status") in {"success", "skipped"}:
                continue
            last_started = stage_name
            break
        if last_started is not None:
            fail_time = utc_now_iso()
            prior_start = state["stage_outputs"].get(last_started, {}).get("start_time", fail_time)
            state["stage_outputs"][last_started] = {
                "status": "failed",
                "start_time": prior_start,
                "end_time": fail_time,
                "elapsed_seconds": elapsed_seconds(prior_start, fail_time),
                "error": str(exc),
            }
            write_stage_summary(
                stage_name=last_started,
                stage_data=state["stage_outputs"][last_started],
                stage_summaries_dir=run_paths["stage_summaries_dir"],
            )            

    finally:
        state["run"]["end_time"] = utc_now_iso()
        write_runtime_profile(state, run_paths["runtime_profile_path"])
        logger.info(f"Runtime profile written to: {run_paths['runtime_profile_path']}")        
        write_run_metadata(state, run_paths["run_metadata_path"])
        logger.info(f"Run metadata written to: {run_paths['run_metadata_path']}")        
        write_metadata(state, run_paths["legacy_metadata_path"])
        logger.info(
            f"Legacy metadata written to: "
            f"{run_paths['legacy_metadata_path']}"
        )
        logger.info("Pipeline run finished.")

    return state, run_paths