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
import hashlib
import importlib
import json
import logging
import os
import platform
import shutil
import socket
import subprocess
import sys
import traceback

from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from pipeline.genotype_projection import project_genotype_observations
from src.tep_orchestration import build_and_validate_fresh_vap_tep
from src.metrics.stage_metric_emitters import emit_metrics_for_stage
from src.metrics.metric_aggregation import (
    build_f3a_flow_table,
    build_f3a_flow_table_v2,
    build_f3b_semantic_branching_table,
    build_f4a_coding_semantic_composition_table,
    build_f4a_coding_semantic_composition_collapsed_table,
    build_f4b_noncoding_semantic_composition_table,
    build_f4b_noncoding_semantic_composition_collapsed_table,
)

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
    metrics_dir = ensure_directory(run_dir / "metrics")

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
        "metrics_dir": str(metrics_dir),
        "legacy_config_snapshot_path": str(run_dir / "config_used.yaml"),
        "legacy_metadata_path": str(run_dir / "metadata.json"),
        "config_snapshot_path": str(metadata_dir / "config_snapshot.yaml"),
        "run_metadata_path": str(metadata_dir / "run_metadata.json"),
        "run_fingerprint_path": str(metadata_dir / "run_fingerprint.json"),
        "runtime_profile_path": str(metadata_dir / "runtime_profile.tsv"),
        "stage_resource_snapshot_path": str(metadata_dir / "stage_resource_snapshots.tsv"),
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
            "genotype_observations": None,
            "genotype_projection_summary": None,
            "genotype_source_header_context": None,
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
            "genotype_projection_qc": {},
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
        "tep": {
            "attempted": False,
            "status": "not_attempted",
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


def collect_resource_snapshot(run_dir: str | Path) -> dict[str, Any]:
    """
    Collect lightweight runtime resource telemetry.

    Parameters
    ----------
    run_dir : str | Path
        Current run directory.

    Returns
    -------
    dict[str, Any]
        Lightweight runtime resource snapshot.
    """
    run_path = Path(run_dir)

    try:
        load1, load5, load15 = os.getloadavg()
    except Exception:
        load1, load5, load15 = ("NA", "NA", "NA")

    try:
        meminfo = {}
        with open("/proc/meminfo", "r", encoding="utf-8") as handle:
            for line in handle:
                parts = line.split(":")
                if len(parts) >= 2:
                    meminfo[parts[0].strip()] = parts[1].strip()

        mem_available = meminfo.get("MemAvailable", "NA")
        mem_total = meminfo.get("MemTotal", "NA")

    except Exception:
        mem_available = "NA"
        mem_total = "NA"

    try:
        disk = shutil.disk_usage(run_path)
        disk_free_gb = round(disk.free / (1024 ** 3), 2)
    except Exception:
        disk_free_gb = "NA"

    return {
        "timestamp": utc_now_iso(),
        "hostname": socket.gethostname(),
        "cpu_count": os.cpu_count(),
        "loadavg_1m": load1,
        "loadavg_5m": load5,
        "loadavg_15m": load15,
        "mem_total": mem_total,
        "mem_available": mem_available,
        "disk_free_gb": disk_free_gb,
    }


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


def build_sidecar_figure_substrates(stage_name:str, run_paths:dict[str,str], logger) -> None:
    if stage_name!="stage_12_validate_variants":
        return

    metrics_dir=Path(run_paths["metrics_dir"])
    metrics_long=metrics_dir/"stage_metrics_long.tsv"

    f3a_out=metrics_dir/"figure_f3a_flow.tsv"
    f3a_v2_out=metrics_dir/"figure_f3a_flow_v2.tsv"
    f3b_out=metrics_dir/"figure_f3b_semantic_branching.tsv"

    stage09_json=metrics_dir/"stage_09_coding_interpretation_metrics.json"
    stage10_json=metrics_dir/"stage_10_noncoding_interpretation_metrics.json"

    f4a_out=metrics_dir/"figure_f4a_coding_semantic_composition.tsv"
    f4a_collapsed_out=metrics_dir/"figure_f4a_coding_semantic_composition_collapsed.tsv"

    f4b_out=metrics_dir/"figure_f4b_noncoding_semantic_composition.tsv"
    f4b_collapsed_out=metrics_dir/"figure_f4b_noncoding_semantic_composition_collapsed.tsv"


    try:
        build_f3a_flow_table(metrics_long,f3a_out)
        logger.info(f"F3A sidecar flow substrate written to: {f3a_out}")

        build_f3a_flow_table_v2(metrics_long,f3a_v2_out)
        logger.info(f"F3A v2 sidecar flow substrate written to: {f3a_v2_out}")

        build_f3b_semantic_branching_table(metrics_long,f3b_out)
        logger.info(f"F3B semantic branching substrate written to: {f3b_out}")

        build_f4a_coding_semantic_composition_table(stage09_json,f4a_out)
        logger.info(f"F4A coding semantic composition substrate written to: {f4a_out}")

        build_f4a_coding_semantic_composition_collapsed_table(
            f4a_out,
            f4a_collapsed_out,
        )
        logger.info(
            f"F4A collapsed coding semantic composition substrate written to: "
            f"{f4a_collapsed_out}"
        )

        build_f4b_noncoding_semantic_composition_table(stage10_json,f4b_out)
        logger.info(f"F4B noncoding semantic composition substrate written to: {f4b_out}")

        build_f4b_noncoding_semantic_composition_collapsed_table(
            f4b_out,
            f4b_collapsed_out,
        )
        logger.info(
            f"F4B collapsed noncoding semantic composition substrate written to: "
            f"{f4b_collapsed_out}"
        )

    except Exception as exc:
        logger.warning(f"Sidecar figure substrate generation failed: {exc}")


def write_resolved_figure_set_config(config, run_id, run_paths, logger):
    import yaml

    figures_cfg=config.get("figures",{})
    template_path=figures_cfg.get("figure_set_template")

    if not template_path:
        return None

    template_path=Path(template_path)
    if not template_path.exists():
        raise FileNotFoundError(f"Figure-set template not found: {template_path}")

    with template_path.open("r",encoding="utf-8") as handle:
        template=handle.read()

    context={
        "sample_id":config["input"]["sample_id"],
        "run_id":run_id,
        "run_dir":run_paths["run_dir"],
        "strict":str(bool(figures_cfg.get("strict",False))).lower(),
    }

    resolved_text=template.format(**context)
    resolved_path=Path(run_paths["metadata_dir"])/"figure_set_resolved.yaml"

    with resolved_path.open("w",encoding="utf-8") as handle:
        handle.write(resolved_text)

    logger.info(f"Resolved figure-set config written to: {resolved_path}")
    return resolved_path


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


def append_stage_resource_snapshot(
    stage_name: str,
    phase: str,
    snapshot: dict[str, Any],
    output_path: str,
) -> None:
    """
    Append lightweight stage resource telemetry snapshot.

    Parameters
    ----------
    stage_name : str
        Pipeline stage name.
    phase : str
        start or end.
    snapshot : dict[str, Any]
        Resource snapshot payload.
    output_path : str
        TSV output path.
    """
    fieldnames = [
        "timestamp",
        "stage",
        "phase",
        "hostname",
        "cpu_count",
        "loadavg_1m",
        "loadavg_5m",
        "loadavg_15m",
        "mem_total",
        "mem_available",
        "disk_free_gb",
    ]

    output_file = Path(output_path)
    write_header = not output_file.exists()

    with output_file.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t")

        if write_header:
            writer.writeheader()

        row = {
            "stage": stage_name,
            "phase": phase,
            **snapshot,
        }

        writer.writerow(row)


def stable_json_dumps(payload: dict[str, Any]) -> str:
    return json.dumps(payload, indent=2, sort_keys=True)


def write_run_metadata(state: dict[str, Any], run_metadata_path: str) -> None:
    stage_outputs = state.get("stage_outputs", {})
    numbered_stage_outputs = {
        stage_name: stage_outputs.get(stage_name, {})
        for stage_name in STAGE_ORDER
    }

    stage_status_counts: dict[str, int] = {}
    for stage_data in numbered_stage_outputs.values():
        status = stage_data.get("status", "unknown")
        stage_status_counts[status] = stage_status_counts.get(status, 0) + 1

    projection_name = "genotype_observation_projection"
    projection_data = stage_outputs.get(projection_name)
    projection_status_counts: dict[str, int] = {}
    if projection_data is not None:
        projection_status = projection_data.get("status", "unknown")
        projection_status_counts[projection_status] = 1

    genotype_qc = state.get("qc", {}).get("genotype_projection_qc", {})
    artifacts = state.get("artifacts", {})
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
            "stage_count": len(numbered_stage_outputs),
            "stage_status_counts": stage_status_counts,
            "projection_count": 1 if projection_data is not None else 0,
            "projection_status_counts": projection_status_counts,
            "warning_count": len(state.get("warnings", [])),
            "error_count": len(state.get("errors", [])),
        },
        "genotype_projection": {
            "status": (
                projection_data.get("status")
                if projection_data is not None
                else "not_recorded"
            ),
            "projection_status": genotype_qc.get("projection_status"),
            "projection_complete": genotype_qc.get(
                "projection_complete",
                False,
            ),
            "artifact_set_complete": genotype_qc.get(
                "artifact_set_complete",
                False,
            ),
            "source_record_count": genotype_qc.get("source_record_count"),
            "genotype_observation_row_count": genotype_qc.get(
                "genotype_observation_row_count"
            ),
        },
        "tep": dict(
            state.get(
                "tep",
                {
                    "attempted": False,
                    "status": "not_attempted",
                },
            )
        ),
        "artifacts": {
            "run_summary_report": state.get("reports", {}).get("run_summary_report"),
            "gene_summary_table": state.get("reports", {}).get("gene_summary_table"),
            "prioritized_table": artifacts.get("prioritized_table"),
            "validation_notes": artifacts.get("validation_notes"),
            "genotype_observations": artifacts.get("genotype_observations"),
            "genotype_projection_summary": artifacts.get(
                "genotype_projection_summary"
            ),
            "genotype_source_header_context": artifacts.get(
                "genotype_source_header_context"
            ),
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

    if execution_mode == "post_vep_fixture":
        skipped_stages = {
            "stage_01_load_data",
            "stage_02_align_data",
            "stage_03_process_bam",
            "stage_04_qc_aligned_reads",
            "stage_05_call_variants",
            "stage_06_normalize_vcf",
            "stage_07_annotate_variants",
        }
        return stage_name not in skipped_stages

    return True



def _read_annotated_table_identity(
    annotated_table_path: str | Path,
) -> dict[str, str]:
    """
    Read producer identity from the first annotated-TSV data row.

    This is used only when replaying a retained post-VEP fixture, where the
    source evidence run identity is distinct from the current orchestration
    run directory.
    """
    path = Path(annotated_table_path)
    if not path.is_file():
        raise FileNotFoundError(
            f"Annotated TSV identity source not found: {path}"
        )

    with path.open("r", encoding="utf-8", errors="replace", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        if reader.fieldnames is None:
            raise ValueError(f"Annotated TSV has no header: {path}")

        required = {"sample_id", "run_id", "source_pipeline"}
        missing = sorted(required - set(reader.fieldnames))
        if missing:
            raise ValueError(
                "Annotated TSV is missing producer identity columns: "
                + ", ".join(missing)
            )

        first_row = next(reader, None)

    if first_row is None:
        raise ValueError(f"Annotated TSV contains no data rows: {path}")

    identity = {
        key: str(first_row.get(key, "")).strip()
        for key in required
    }
    empty = sorted(key for key, value in identity.items() if not value)
    if empty:
        raise ValueError(
            "Annotated TSV has empty producer identity values: "
            + ", ".join(empty)
        )

    return identity


def resolve_genotype_projection_context(
    config: dict[str, Any],
    state: dict[str, Any],
    run_paths: dict[str, str],
) -> dict[str, Any]:
    """
    Resolve the complete producer context required for genotype projection.
    """
    sample_state = state.get("sample", {})
    run_state = state.get("run", {})
    artifacts = state.get("artifacts", {})
    execution_mode = config["mode"]["execution_mode"]

    sample_id = sample_state.get("sample_id") or config["input"].get("sample_id")
    run_id = run_state.get("run_id")
    source_pipeline = (
        run_state.get("pipeline_name")
        or config["project"].get("pipeline_name")
    )

    if execution_mode == "post_vep_fixture":
        annotated_table = artifacts.get("annotated_table")
        if not annotated_table:
            raise ValueError(
                "Post-VEP fixture mode requires an annotated TSV identity source."
            )
        source_identity = _read_annotated_table_identity(annotated_table)

        configured_sample = str(config["input"].get("sample_id", "")).strip()
        configured_alias = str(
            config["input"].get("sample_alias", "")
        ).strip()
        source_sample = source_identity["sample_id"]

        if source_sample not in {configured_sample, configured_alias}:
            raise ValueError(
                "Post-VEP fixture sample identity mismatch: "
                f"TSV={source_sample}; config_sample={configured_sample}; "
                f"config_alias={configured_alias}"
            )

        configured_pipeline = str(
            config["project"].get("pipeline_name", "")
        ).strip()
        if source_identity["source_pipeline"] != configured_pipeline:
            raise ValueError(
                "Post-VEP fixture source pipeline mismatch: "
                f"TSV={source_identity['source_pipeline']}; "
                f"config={configured_pipeline}"
            )

        sample_id = source_sample
        run_id = source_identity["run_id"]
        source_pipeline = source_identity["source_pipeline"]

    source_vcf = artifacts.get("annotated_vcf")
    source_label = str(source_vcf) if source_vcf else None

    return {
        "annotated_vcf_path": source_vcf,
        "output_directory": run_paths["processed_dir"],
        "sample_id": sample_id,
        "sample_alias": (
            sample_state.get("sample_alias")
            or config["input"].get("sample_alias")
        ),
        "sra_accession": (
            sample_state.get("sra_accession")
            or config["input"].get("sra_accession")
        ),
        "run_id": run_id,
        "reference_build": (
            sample_state.get("reference_genome")
            or config["reference"].get("genome_build")
        ),
        "source_pipeline": source_pipeline,
        "assay_type": (
            sample_state.get("assay_type")
            or config["input"].get("assay_type")
        ),
        "explicit_vcf_sample_name": sample_id,
        "source_vcf_path_label": source_label,
        "normalization_policy_id": (
            "post_vep_fixture_source_policy_v1"
            if execution_mode == "post_vep_fixture"
            else "vap_stage06_normalization_policy_v1"
        ),
        "normalization_state": (
            "retained_post_vep_fixture"
            if execution_mode == "post_vep_fixture"
            else "normalized_annotated_vcf"
        ),
    }


def genotype_projection_is_eligible(
    context: dict[str, Any],
) -> tuple[bool, str]:
    """
    Determine whether the resolved context can support projection.
    """
    source_value = context.get("annotated_vcf_path")
    if not source_value:
        return False, "annotated_vcf_not_registered"

    source = Path(str(source_value))
    if not source.exists():
        return False, "annotated_vcf_missing"
    if not source.is_file():
        return False, "annotated_vcf_not_file"
    if source.stat().st_size == 0:
        return False, "annotated_vcf_empty"

    for key, reason in [
        ("sample_id", "sample_identity_unavailable"),
        ("run_id", "run_identity_unavailable"),
        ("reference_build", "reference_build_unavailable"),
        ("source_pipeline", "source_pipeline_unavailable"),
    ]:
        value = context.get(key)
        if value is None or str(value).strip() == "":
            return False, reason

    return True, "eligible"


def run_genotype_projection_if_ready(
    *,
    config: dict[str, Any],
    state: dict[str, Any],
    run_paths: dict[str, str],
    logger,
) -> dict[str, Any]:
    """
    Invoke genotype projection exactly once without blocking Stages 08-13.
    """
    projection_name = "genotype_observation_projection"
    existing = state.get("stage_outputs", {}).get(projection_name)
    if existing is not None and existing.get("status") in {
        "success",
        "failed",
        "not_eligible",
    }:
        return state

    state.setdefault("stage_outputs", {})
    state.setdefault("artifacts", {})
    state.setdefault("qc", {})
    state.setdefault("errors", [])

    try:
        context = resolve_genotype_projection_context(
            config=config,
            state=state,
            run_paths=run_paths,
        )
        eligible, reason = genotype_projection_is_eligible(context)

        if not eligible:
            logger.info(
                "Genotype projection not eligible: "
                f"{reason}"
            )
            state["stage_outputs"][projection_name] = {
                "status": "not_eligible",
                "reason": reason,
            }
            state["qc"]["genotype_projection_qc"] = {
                "projection_attempted": False,
                "projection_complete": False,
                "artifact_set_complete": False,
                "projection_status": "not_eligible",
                "reason": reason,
            }
            return state

        logger.info(
            "Starting non-numbered genotype observation projection."
        )
        result = project_genotype_observations(**context)

        state["artifacts"]["genotype_observations"] = result[
            "genotype_observations"
        ]
        state["artifacts"]["genotype_projection_summary"] = result[
            "genotype_projection_summary"
        ]
        state["artifacts"]["genotype_source_header_context"] = result[
            "genotype_source_header_context"
        ]

        state["qc"]["genotype_projection_qc"] = {
            "projection_attempted": True,
            "projection_complete": True,
            "artifact_set_complete": True,
            "projection_status": result["projection_status"],
            "source_record_count": result["source_record_count"],
            "genotype_observation_row_count": result["row_count"],
        }
        state["stage_outputs"][projection_name] = {
            "status": "success",
            "projection_status": result["projection_status"],
            "source_record_count": result["source_record_count"],
            "genotype_observation_row_count": result["row_count"],
            "output_artifacts": [
                result["genotype_observations"],
                result["genotype_projection_summary"],
                result["genotype_source_header_context"],
            ],
        }
        logger.info(
            "Completed genotype observation projection: "
            f"rows={result['row_count']}; "
            f"status={result['projection_status']}"
        )
        return state

    except Exception as exc:
        message = f"Genotype projection failed: {exc}"
        logger.error(message)
        logger.error(traceback.format_exc())

        state["errors"].append(message)
        state["stage_outputs"][projection_name] = {
            "status": "failed",
            "error_type": type(exc).__name__,
            "error": str(exc),
        }
        state["qc"]["genotype_projection_qc"] = {
            "projection_attempted": True,
            "projection_complete": False,
            "artifact_set_complete": False,
            "projection_status": "failed",
            "error_type": type(exc).__name__,
            "error": str(exc),
        }
        return state


def run_fresh_tep_if_ready(
    *,
    state: dict[str, Any],
    run_paths: dict[str, str],
    logger,
) -> dict[str, Any]:
    """
    Emit and validate a fresh TEP exactly once after stage completion.
    """
    existing = state.get("tep", {})
    if existing.get("status") in {"success", "failed"}:
        return state

    if state.get("run", {}).get("status") != "completed":
        state["tep"] = {
            "attempted": False,
            "status": "not_attempted",
            "reason": "numbered_pipeline_not_completed",
        }
        return state

    projection = state.get("stage_outputs", {}).get(
        "genotype_observation_projection",
        {},
    )
    if projection.get("status") == "failed":
        state["tep"] = {
            "attempted": False,
            "status": "failed",
            "reason": "genotype_projection_failed",
        }
        state.setdefault("errors", []).append(
            "Fresh TEP emission blocked because genotype projection failed."
        )
        return state

    try:
        logger.info("Starting native fresh TEP-VAP emission.")
        state["tep"] = build_and_validate_fresh_vap_tep(
            state=state,
            run_paths=run_paths,
        )
        logger.info(
            "Fresh TEP-VAP emission completed: "
            f"{state['tep']['package_root']}"
        )
    except Exception as exc:
        message = f"Fresh TEP-VAP emission failed: {exc}"
        logger.error(message)
        logger.error(traceback.format_exc())
        state.setdefault("errors", []).append(message)
        state["tep"] = {
            "attempted": True,
            "status": "failed",
            "error_type": type(exc).__name__,
            "error": str(exc),
        }

    return state

def render_run_figures_if_enabled(config:dict[str,Any], run_paths:dict[str,str], logger) -> None:
    # Check if auto-rendering is enabled in the config.
    figures_cfg=config.get("figures",{})
    if not figures_cfg.get("auto_render",False):
        return
    # If enabled, attempt to resolve the figure set config from the template and context.
    resolved_figure_set=write_resolved_figure_set_config(
        config=config,
        run_id=Path(run_paths["run_dir"]).name,
        run_paths=run_paths,
        logger=logger,
    )
    # If no template was provided or resolution failed, fall back to the figure_set_config directly from the config.
    figure_set_config=resolved_figure_set or figures_cfg.get("figure_set_config")
    if not figure_set_config:
        logger.warning(
            "Figure auto-render requested but no figure_set_template "
            "or figure_set_config was provided."
        )
        return
    # If we have a figure set config at this point, attempt to run the rendering script.
    command=[
        sys.executable,
        "scripts/figures/render_case_study_figures.py",
        "--config",
        str(figure_set_config),
    ]

    strict=bool(figures_cfg.get("strict",False))

    try:
        logger.info(f"Starting optional figure auto-render: {' '.join(command)}")
        subprocess.run(command,check=True,capture_output=True,text=True)
        logger.info("Optional figure auto-render completed successfully.")
    except subprocess.CalledProcessError as exc:
        message=(exc.stderr or exc.stdout or str(exc)).replace("\n"," ")[:1000]
        if strict:
            raise RuntimeError(f"Figure auto-render failed: {message}") from exc
        logger.warning(f"Optional figure auto-render failed but pipeline will continue: {message}")


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

    if config["mode"]["execution_mode"] == "post_vep_fixture":
        state["artifacts"]["annotated_table"] = config["input"]["annotated_tsv"]
        state["artifacts"]["annotated_vcf"] = config["input"]["vcf"]["input_vcf"]

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

            if stage_name == "stage_08_filter_and_partition":
                state = run_genotype_projection_if_ready(
                    config=config,
                    state=state,
                    run_paths=run_paths,
                    logger=logger,
                )

            stage_start = utc_now_iso()
            state["stage_outputs"][stage_name] = {
                "status": "running",
                "start_time": stage_start,
                "end_time": None,
                "elapsed_seconds": None,
            }
            logger.info(f"Starting stage: {stage_name}")
            start_snapshot = collect_resource_snapshot(run_paths["run_dir"])

            append_stage_resource_snapshot(
                stage_name=stage_name,
                phase="start",
                snapshot=start_snapshot,
                output_path=run_paths["stage_resource_snapshot_path"],
            )            
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
            stage_output = state["stage_outputs"].get(stage_name, {})
            stage_output.update({
                "status": "success",
                "start_time": stage_start,
                "end_time": stage_end,
                "elapsed_seconds": elapsed_seconds(stage_start, stage_end),
            })
            state["stage_outputs"][stage_name] = stage_output
            logger.info(f"Completed stage: {stage_name}")
            end_snapshot = collect_resource_snapshot(run_paths["run_dir"])

            append_stage_resource_snapshot(
                stage_name=stage_name,
                phase="end",
                snapshot=end_snapshot,
                output_path=run_paths["stage_resource_snapshot_path"],
            )            
            write_stage_summary(
                stage_name=stage_name,
                stage_data=state["stage_outputs"][stage_name],
                stage_summaries_dir=run_paths["stage_summaries_dir"],
            )
            emit_metrics_for_stage(
                stage_name=stage_name,
                config=config,
                paths=run_paths,
                state=state,
                logger=logger,
            )            
            build_sidecar_figure_substrates(
                stage_name=stage_name,
                run_paths=run_paths,
                logger=logger,
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
                "tep",
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
        logger.info(
            "Initial run metadata written before TEP emission: "
            f"{run_paths['run_metadata_path']}"
        )
        write_metadata(state, run_paths["legacy_metadata_path"])

        state = run_fresh_tep_if_ready(
            state=state,
            run_paths=run_paths,
            logger=logger,
        )

        write_run_metadata(state, run_paths["run_metadata_path"])
        logger.info(
            f"Final run metadata written to: "
            f"{run_paths['run_metadata_path']}"
        )
        write_metadata(state, run_paths["legacy_metadata_path"])
        logger.info(
            f"Final legacy metadata written to: "
            f"{run_paths['legacy_metadata_path']}"
        )
        render_run_figures_if_enabled(
            config=config,
            run_paths=run_paths,
            logger=logger,
        )        
        logger.info("Pipeline run finished.")

    return state, run_paths