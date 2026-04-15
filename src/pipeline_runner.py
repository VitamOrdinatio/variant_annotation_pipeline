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

import importlib
import json
import socket
import traceback
from copy import deepcopy
from datetime import datetime
from pathlib import Path
from typing import Any


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
    return datetime.now().strftime("run_%Y_%m_%d_%H%M%S")


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
    interim_dir = ensure_directory(run_dir / "interim")
    processed_dir = ensure_directory(run_dir / "processed")
    reports_dir = ensure_directory(run_dir / "reports")
    final_dir = ensure_directory(run_dir / "final")
    validation_dir = ensure_directory(run_dir / "validation")

    return {
        "base_results_dir": str(base_results_dir),
        "run_dir": str(run_dir),
        "logs_dir": str(logs_dir),
        "interim_dir": str(interim_dir),
        "processed_dir": str(processed_dir),
        "reports_dir": str(reports_dir),
        "final_dir": str(final_dir),
        "validation_dir": str(validation_dir),
        "config_snapshot_path": str(run_dir / "config_used.yaml"),
        "metadata_path": str(run_dir / "metadata.json"),
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
    now = datetime.now().isoformat(timespec="seconds")
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
        json.dump(state, handle, indent=2, sort_keys=True)


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
    save_config_snapshot(config, run_paths["config_snapshot_path"])

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
                state["stage_outputs"][stage_name] = {"status": "skipped"}
                continue

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

            logger.info(f"Completed stage: {stage_name}")

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
            state["stage_outputs"][last_started] = {
                "status": "failed",
                "error": str(exc),
            }

    finally:
        state["run"]["end_time"] = datetime.now().isoformat(timespec="seconds")
        write_metadata(state, run_paths["metadata_path"])
        logger.info(f"Metadata written to: {run_paths['metadata_path']}")
        logger.info("Pipeline run finished.")

    return state, run_paths