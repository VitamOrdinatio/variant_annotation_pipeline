"""
Stage 12: Prepare variants for validation.

Stage 12 consumes Stage 11 prioritized variants and adds deterministic
validation-preparation fields. It does not execute IGV, parse BAM files,
filter variants, or reinterpret evidence.
"""

from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path
from typing import Any


REQUIRED_FIELDS = [
    "priority_tier",
    "priority_rank",
    "variant_id",
    "gene_id",
    "gene_symbol",
    "chromosome",
    "position",
]

ADDED_FIELDS = [
    "validation_required",
    "validation_priority",
    "suggested_validation_method",
    "validation_reason",
]


def _log(logger, level: str, message: str) -> None:
    method = getattr(logger, level, None)
    if method is None:
        print(f"[{level.upper()}] {message}")
    else:
        method(message)


def _validate_file(path_str: str | None, label: str) -> Path:
    if not path_str:
        raise ValueError(f"Missing required Stage 12 input artifact: {label}")
    path = Path(path_str)
    if not path.exists():
        raise FileNotFoundError(f"Required Stage 12 input does not exist: {path}")
    if not path.is_file():
        raise FileNotFoundError(f"Required Stage 12 input is not a file: {path}")
    if path.stat().st_size == 0:
        raise ValueError(f"Required Stage 12 input is empty: {path}")
    return path


def _get_stage_input(state: dict[str, Any]) -> Path:
    artifacts = state.get("artifacts", {})
    return _validate_file(
        artifacts.get("stage_11_prioritized_variants"),
        "stage_11_prioritized_variants",
    )


def _validate_header(fieldnames: list[str] | None, path: Path) -> list[str]:
    if fieldnames is None:
        raise ValueError(f"Could not read header from Stage 12 input: {path}")
    missing = [field for field in REQUIRED_FIELDS if field not in fieldnames]
    if missing:
        raise ValueError(f"Stage 12 input missing required fields {missing}: {path}")
    return list(fieldnames)


def _prepare_output_paths(processed_dir: Path) -> dict[str, Path]:
    return {
        "validation_candidates": processed_dir / "stage_12_validation_candidates.tsv",
        "summary_json": processed_dir / "stage_12_summary.json",
    }


def _assign_validation_fields(priority_tier: str, priority_rank: str) -> dict[str, str]:
    if priority_rank == "1" or priority_tier == "tier_1_high_confidence_candidate":
        return {
            "validation_required": "True",
            "validation_priority": "high",
            "suggested_validation_method": "IGV",
            "validation_reason": priority_tier,
        }

    if priority_rank == "2" or priority_tier == "tier_2_moderate_candidate":
        return {
            "validation_required": "True",
            "validation_priority": "medium",
            "suggested_validation_method": "IGV",
            "validation_reason": priority_tier,
        }

    if priority_rank == "3" or priority_tier == "tier_3_low_support_or_common":
        return {
            "validation_required": "False",
            "validation_priority": "low",
            "suggested_validation_method": "none",
            "validation_reason": priority_tier,
        }

    if priority_rank == "4" or priority_tier == "tier_4_uninterpretable_or_qc_limited":
        return {
            "validation_required": "False",
            "validation_priority": "low",
            "suggested_validation_method": "none",
            "validation_reason": priority_tier,
        }

    return {
        "validation_required": "False",
        "validation_priority": "low",
        "suggested_validation_method": "none",
        "validation_reason": f"unrecognized_priority:{priority_tier}|rank:{priority_rank}",
    }


def _init_summary() -> dict[str, Any]:
    return {
        "input_rows": 0,
        "output_rows": 0,
        "unrecognized_priority_rows": 0,
        "counts_by_validation_required": Counter(),
        "counts_by_validation_priority": Counter(),
        "counts_by_suggested_validation_method": Counter(),
        "counts_by_priority_tier": Counter(),
    }


def _update_summary(summary: dict[str, Any], row: dict[str, str]) -> None:
    summary["input_rows"] += 1
    summary["output_rows"] += 1
    summary["counts_by_validation_required"][row["validation_required"]] += 1
    summary["counts_by_validation_priority"][row["validation_priority"]] += 1
    summary["counts_by_suggested_validation_method"][row["suggested_validation_method"]] += 1
    summary["counts_by_priority_tier"][row["priority_tier"]] += 1
    if row["validation_reason"].startswith("unrecognized_priority:"):
        summary["unrecognized_priority_rows"] += 1


def _summary_to_jsonable(summary: dict[str, Any], metadata: dict[str, Any]) -> dict[str, Any]:
    payload = dict(metadata)
    for key, value in summary.items():
        if isinstance(value, Counter):
            payload[key] = dict(sorted(value.items()))
        else:
            payload[key] = value
    return payload


def _write_summary_json(path: Path, summary: dict[str, Any], metadata: dict[str, Any]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        json.dump(_summary_to_jsonable(summary, metadata), handle, indent=2, sort_keys=True)
        handle.write("\n")


def run_stage(
    config: dict[str, Any],
    paths: dict[str, Any],
    logger,
    state: dict[str, Any],
) -> dict[str, Any]:
    _log(logger, "info", "Stage 12: preparing validation candidates.")

    stage11_path = _get_stage_input(state)
    processed_dir = Path(paths["processed_dir"])
    processed_dir.mkdir(parents=True, exist_ok=True)
    output_paths = _prepare_output_paths(processed_dir)

    _log(logger, "info", f"Stage 12 prioritized variants input: {stage11_path}")

    summary = _init_summary()

    with stage11_path.open("r", encoding="utf-8", errors="replace", newline="") as in_handle:
        reader = csv.DictReader(in_handle, delimiter="\t")
        input_fieldnames = _validate_header(reader.fieldnames, stage11_path)
        output_fieldnames = input_fieldnames + [
            field for field in ADDED_FIELDS if field not in input_fieldnames
        ]

        with output_paths["validation_candidates"].open("w", encoding="utf-8", newline="") as out_handle:
            writer = csv.DictWriter(
                out_handle,
                fieldnames=output_fieldnames,
                delimiter="\t",
                extrasaction="ignore",
            )
            writer.writeheader()

            for input_row in reader:
                row = dict(input_row)
                row.update(
                    _assign_validation_fields(
                        priority_tier=str(row.get("priority_tier", "")).strip(),
                        priority_rank=str(row.get("priority_rank", "")).strip(),
                    )
                )
                writer.writerow({field: row.get(field, "NA") for field in output_fieldnames})
                _update_summary(summary, row)

    metadata = {
        "stage": "stage_12_validate_variants",
        "status": "success",
        "input_files": {
            "stage_11_prioritized_variants": str(stage11_path),
        },
        "output_files": {
            "stage_12_validation_candidates": str(output_paths["validation_candidates"]),
            "stage_12_summary_json": str(output_paths["summary_json"]),
        },
        "assumptions": [
            "Stage 12 prepares validation actions only.",
            "Stage 12 does not execute IGV, parse BAM files, filter variants, or reinterpret evidence.",
            "Tier 1 and Tier 2 variants are assigned IGV as the suggested validation method.",
            "manual_review is reserved for future edge-case workflows and is not used in v1.",
        ],
    }

    _write_summary_json(output_paths["summary_json"], summary, metadata)

    state.setdefault("artifacts", {})
    state["artifacts"]["stage_12_validation_candidates"] = str(output_paths["validation_candidates"])
    state["artifacts"]["stage_12_summary_json"] = str(output_paths["summary_json"])

    state.setdefault("qc", {})
    state["qc"]["stage_12_qc"] = {
        "input_rows": summary["input_rows"],
        "output_rows": summary["output_rows"],
        "unrecognized_priority_rows": summary["unrecognized_priority_rows"],
        "output_exists": output_paths["validation_candidates"].exists(),
        "summary_exists": output_paths["summary_json"].exists(),
    }

    state.setdefault("stage_outputs", {})
    state["stage_outputs"]["stage_12_validate_variants"] = {
        "status": "success",
        "input_prioritized_variants": str(stage11_path),
        "validation_candidates": str(output_paths["validation_candidates"]),
        "summary_json": str(output_paths["summary_json"]),
        "input_rows": summary["input_rows"],
        "output_rows": summary["output_rows"],
        "unrecognized_priority_rows": summary["unrecognized_priority_rows"],
    }

    _log(logger, "info", f"Stage 12 validation candidates written to: {output_paths['validation_candidates']}")
    _log(logger, "info", f"Stage 12 summary JSON written to: {output_paths['summary_json']}")
    _log(logger, "info", f"Stage 12 input rows processed: {summary['input_rows']}")
    _log(logger, "info", f"Stage 12 output rows written: {summary['output_rows']}")
    _log(logger, "info", f"Stage 12 unrecognized priority rows: {summary['unrecognized_priority_rows']}")

    return state