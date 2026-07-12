"""
Stage 13: Write final VAP run summary.

Stage 13 produces final run-level outputs for reporting, reproducibility,
auditability, and portfolio evidence. It does not rerun upstream stages,
filter variants, reinterpret evidence, reprioritize variants, execute IGV,
parse BAM files, or perform gene-level ranking.
"""

from __future__ import annotations

import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


REQUIRED_ARTIFACT_KEYS = [
    "stage_11_prioritized_variants",
    "stage_11_summary_json",
    "stage_11_gene_variant_counts",
    "stage_12_validation_candidates",
    "stage_12_summary_json",
]


def _log(logger, level: str, message: str) -> None:
    method = getattr(logger, level, None)
    if method is None:
        print(f"[{level.upper()}] {message}")
    else:
        method(message)


def _read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
        handle.write("\n")


def _validate_required_file(path: Path, label: str) -> None:
    if not path.exists():
        raise FileNotFoundError(f"Required Stage 13 input missing: {label}: {path}")
    if not path.is_file():
        raise FileNotFoundError(f"Required Stage 13 input is not a file: {label}: {path}")
    if path.stat().st_size == 0:
        raise ValueError(f"Required Stage 13 input is empty: {label}: {path}")


def _get_required_inputs(state: dict[str, Any]) -> dict[str, Path]:
    artifacts = state.get("artifacts", {})
    paths: dict[str, Path] = {}

    for key in REQUIRED_ARTIFACT_KEYS:
        value = artifacts.get(key)
        if not value:
            raise ValueError(f"Missing required Stage 13 artifact key in state['artifacts']: {key}")
        path = Path(value)
        _validate_required_file(path, key)
        paths[key] = path

    return paths


def _prepare_output_paths(processed_dir: Path) -> dict[str, Path]:
    return {
        "final_summary": processed_dir / "stage_13_final_summary.json",
        "artifact_manifest": processed_dir / "stage_13_artifact_manifest.json",
        "run_report": processed_dir / "stage_13_run_report.md",
    }


def _file_type(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix == ".tsv":
        return "tsv"
    if suffix == ".json":
        return "json"
    if suffix == ".vcf":
        return "vcf"
    if suffix == ".md":
        return "markdown"
    if suffix in {".log", ".txt"}:
        return "text"
    return suffix.lstrip(".") or "unknown"


def _infer_stage_from_name(name: str) -> str:
    for token in name.split("_"):
        if token.startswith("stage") and token[5:].isdigit():
            return token
    if name.startswith("stage_"):
        parts = name.split("_")
        if len(parts) >= 2 and parts[1].isdigit():
            return f"stage_{parts[1]}"
    return "unknown"


def _artifact_record(name: str, path: Path, required: bool) -> dict[str, Any]:
    exists = path.exists()
    stat = path.stat() if exists else None
    return {
        "artifact_name": name,
        "stage": _infer_stage_from_name(path.name),
        "path": str(path),
        "file_type": _file_type(path),
        "exists": exists,
        "size_bytes": stat.st_size if stat else 0,
        "modified_timestamp": datetime.fromtimestamp(stat.st_mtime).isoformat() if stat else None,
        "required": required,
    }


def _discover_optional_artifacts(run_dir: Path, required_paths: set[Path], output_paths: set[Path]) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    patterns = [
        "stage_*_summary.json",
        "*.tsv",
        "*.vcf",
        "*.log",
        "genotype_projection_summary.json",
        "genotype_source_header_context.json",
    ]

    seen: set[Path] = set(required_paths | output_paths)
    for pattern in patterns:
        for path in sorted(run_dir.rglob(pattern)):
            if path in seen:
                continue
            seen.add(path)
            records.append(_artifact_record(path.name, path, required=False))

    return records


def _write_artifact_manifest(
    path: Path,
    required_inputs: dict[str, Path],
    output_paths: dict[str, Path],
    run_dir: Path,
) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []

    for name, artifact_path in required_inputs.items():
        records.append(_artifact_record(name, artifact_path, required=True))

    for name, artifact_path in output_paths.items():
        records.append(_artifact_record(f"stage_13_{name}", artifact_path, required=True))

    records.extend(
        _discover_optional_artifacts(
            run_dir=run_dir,
            required_paths=set(required_inputs.values()),
            output_paths=set(output_paths.values()),
        )
    )

    payload = {
        "stage": "stage_13_write_summary",
        "status": "success",
        "artifact_count": len(records),
        "artifacts": records,
    }
    _write_json(path, payload)
    return records


def _read_first_data_row(path: Path) -> dict[str, str]:
    with path.open("r", encoding="utf-8", errors="replace", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        for row in reader:
            return dict(row)
    return {}


def _read_top_gene_counts(path: Path, limit: int = 10) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    with path.open("r", encoding="utf-8", errors="replace", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        for row in reader:
            rows.append(dict(row))
            if len(rows) >= limit:
                break
    return rows


def _collect_annotation_provenance(first_row: dict[str, str]) -> tuple[list[str], list[str]]:
    source = str(first_row.get("annotation_source", "")).strip()
    version = str(first_row.get("annotation_version", "")).strip()
    sources = [source] if source and source not in {"NA", "None", "null"} else []
    versions = [version] if version and version not in {"NA", "None", "null"} else []
    return sources, versions


def _build_qc_status_by_stage(stage11_summary: dict[str, Any], stage12_summary: dict[str, Any]) -> dict[str, Any]:
    return {
        "stage_08": {"status": "not_collected", "input_rows": None, "output_rows": None},
        "stage_09": {"status": "not_collected", "input_rows": None, "output_rows": None},
        "stage_10": {"status": "not_collected", "input_rows": None, "output_rows": None},
        "stage_11": {
            "status": stage11_summary.get("status", "unknown"),
            "input_rows": stage11_summary.get("input_rows"),
            "output_rows": stage11_summary.get("output_rows"),
        },
        "stage_12": {
            "status": stage12_summary.get("status", "unknown"),
            "input_rows": stage12_summary.get("input_rows"),
            "output_rows": stage12_summary.get("output_rows"),
        },
    }


def _validate_cross_stage_counts(stage11_summary: dict[str, Any], stage12_summary: dict[str, Any]) -> None:
    stage11_output_rows = stage11_summary.get("output_rows")
    stage12_input_rows = stage12_summary.get("input_rows")
    stage12_output_rows = stage12_summary.get("output_rows")

    if stage11_output_rows != stage12_input_rows:
        raise ValueError(
            f"Stage 11 output_rows ({stage11_output_rows}) != Stage 12 input_rows ({stage12_input_rows})"
        )

    if stage11_output_rows != stage12_output_rows:
        raise ValueError(
            f"Stage 11 output_rows ({stage11_output_rows}) != Stage 12 output_rows ({stage12_output_rows})"
        )

    validation_required_counts = stage12_summary.get("counts_by_validation_required", {})
    validation_required_count = int(validation_required_counts.get("True", 0))
    igv_count = int(stage12_summary.get("counts_by_suggested_validation_method", {}).get("IGV", 0))

    if validation_required_count != igv_count:
        raise ValueError(
            f"Validation-required count ({validation_required_count}) != IGV method count ({igv_count})"
        )


def _build_final_summary(
    stage11_summary: dict[str, Any],
    stage12_summary: dict[str, Any],
    first_row: dict[str, str],
    top_gene_rows: list[dict[str, str]],
    output_paths: dict[str, Path],
) -> dict[str, Any]:
    annotation_sources, annotation_versions = _collect_annotation_provenance(first_row)
    counts_by_validation_required = stage12_summary.get("counts_by_validation_required", {})

    return {
        "stage": "stage_13_write_summary",
        "status": "success",
        "run_id": first_row.get("run_id", "NA"),
        "sample_id": first_row.get("sample_id", "NA"),
        "source_pipeline": first_row.get("source_pipeline", "NA"),
        "total_variants_processed": stage11_summary.get("output_rows"),
        "prioritized_variant_count": stage11_summary.get("output_rows"),
        "validation_candidate_count": stage12_summary.get("output_rows"),
        "validation_required_count": int(counts_by_validation_required.get("True", 0)),
        "counts_by_priority_tier": stage11_summary.get("counts_by_priority_tier", {}),
        "counts_by_priority_rank": stage11_summary.get("counts_by_priority_rank", {}),
        "counts_by_variant_origin": stage11_summary.get("counts_by_variant_origin", {}),
        "counts_by_source_interpretation_label": stage11_summary.get("counts_by_source_interpretation_label", {}),
        "counts_by_validation_required": counts_by_validation_required,
        "counts_by_validation_priority": stage12_summary.get("counts_by_validation_priority", {}),
        "counts_by_suggested_validation_method": stage12_summary.get("counts_by_suggested_validation_method", {}),
        "high_priority_candidate_count": stage11_summary.get("high_priority_candidate_count", 0),
        "moderate_priority_candidate_count": stage11_summary.get("moderate_priority_candidate_count", 0),
        "low_priority_candidate_count": stage11_summary.get("low_priority_candidate_count", 0),
        "uninterpretable_count": stage11_summary.get("uninterpretable_count", 0),
        "gene_id_count_unique": stage11_summary.get("gene_id_count_unique"),
        "top_gene_variant_counts": top_gene_rows,
        "qc_status_by_stage": _build_qc_status_by_stage(stage11_summary, stage12_summary),
        "artifact_manifest_path": str(output_paths["artifact_manifest"]),
        "run_report_path": str(output_paths["run_report"]),
        "annotation_sources_present": annotation_sources,
        "annotation_versions_present": annotation_versions,
    }


def _write_run_report(path: Path, final_summary: dict[str, Any], manifest_records: list[dict[str, Any]]) -> None:
    priority_counts = final_summary.get("counts_by_priority_tier", {})
    validation_counts = final_summary.get("counts_by_validation_required", {})
    top_genes = final_summary.get("top_gene_variant_counts", [])

    lines = [
        "# VAP Stage 13 Final Run Report",
        "",
        "## Run overview",
        "",
        f"- Run ID: `{final_summary.get('run_id')}`",
        f"- Sample ID: `{final_summary.get('sample_id')}`",
        f"- Source pipeline: `{final_summary.get('source_pipeline')}`",
        f"- Total variants processed: `{final_summary.get('total_variants_processed')}`",
        f"- Prioritized variants: `{final_summary.get('prioritized_variant_count')}`",
        f"- Validation candidates: `{final_summary.get('validation_candidate_count')}`",
        "",
        "## Input artifacts",
        "",
    ]

    for record in manifest_records:
        if record["required"] and not record["artifact_name"].startswith("stage_13_"):
            lines.append(
                f"- `{record['artifact_name']}` — exists={record['exists']}, "
                f"size_bytes={record['size_bytes']}, path=`{record['path']}`"
            )

    lines.extend(["", "## Final output artifacts", ""])

    for record in manifest_records:
        if record["artifact_name"].startswith("stage_13_"):
            lines.append(
                f"- `{record['artifact_name']}` — exists={record['exists']}, "
                f"size_bytes={record['size_bytes']}, path=`{record['path']}`"
            )

    lines.extend([
        "",
        "## Variant prioritization summary",
        "",
    ])

    for key, value in sorted(priority_counts.items()):
        lines.append(f"- `{key}`: `{value}`")

    lines.extend([
        "",
        "## Validation preparation summary",
        "",
        f"- Validation required: `{validation_counts.get('True', 0)}`",
        f"- Validation not required: `{validation_counts.get('False', 0)}`",
        f"- Suggested IGV validations: `{final_summary.get('counts_by_suggested_validation_method', {}).get('IGV', 0)}`",
        "",
        "## Gene-count summary",
        "",
        f"- Unique gene IDs observed: `{final_summary.get('gene_id_count_unique')}`",
        "",
        "| gene_id | variant_count |",
        "|---|---:|",
    ])

    for row in top_genes[:10]:
        lines.append(f"| {row.get('gene_id', 'NA')} | {row.get('variant_count', 'NA')} |")

    lines.extend([
        "",
        "## QC summary",
        "",
        "- Required inputs exist and are non-empty.",
        "- Stage 11 and Stage 12 row-count consistency checks passed.",
        "- Stage 13 did not modify upstream outputs.",
        "",
        "## Assumptions",
        "",
        "- Stage 11 and Stage 12 outputs are contract-compliant.",
        "- Stage 13 operates on a single completed run directory.",
        "- Gene-level counts are descriptive only and are not RDGP ranking.",
        "",
        "## Limitations",
        "",
        "- Stage 13 does not create visualizations.",
        "- Stage 13 does not execute IGV.",
        "- Stage 13 does not parse BAM files.",
        "- Stage 13 does not perform phenotype matching or gene ranking.",
        "",
        "## Non-goals",
        "",
        "- No new annotation.",
        "- No new interpretation.",
        "- No new prioritization.",
        "- No gene-level ranking.",
        "- No upstream recomputation.",
        "",
    ])

    path.write_text("\n".join(lines), encoding="utf-8")


def run_stage(
    config: dict[str, Any],
    paths: dict[str, Any],
    logger,
    state: dict[str, Any],
) -> dict[str, Any]:
    _log(logger, "info", "Stage 13: writing final summary and manifest.")

    required_inputs = _get_required_inputs(state)
    processed_dir = Path(paths["processed_dir"])
    processed_dir.mkdir(parents=True, exist_ok=True)
    output_paths = _prepare_output_paths(processed_dir)

    stage11_summary = _read_json(required_inputs["stage_11_summary_json"])
    stage12_summary = _read_json(required_inputs["stage_12_summary_json"])
    _validate_cross_stage_counts(stage11_summary, stage12_summary)

    first_row = _read_first_data_row(required_inputs["stage_11_prioritized_variants"])
    top_gene_rows = _read_top_gene_counts(required_inputs["stage_11_gene_variant_counts"], limit=10)

    final_summary = _build_final_summary(
        stage11_summary=stage11_summary,
        stage12_summary=stage12_summary,
        first_row=first_row,
        top_gene_rows=top_gene_rows,
        output_paths=output_paths,
    )

    _write_json(output_paths["final_summary"], final_summary)

    preliminary_manifest_records = [
        _artifact_record(name, path, required=True)
        for name, path in required_inputs.items()
    ]

    _write_run_report(output_paths["run_report"], final_summary, preliminary_manifest_records)

    manifest_records = _write_artifact_manifest(
        path=output_paths["artifact_manifest"],
        required_inputs=required_inputs,
        output_paths=output_paths,
        run_dir=processed_dir.parent,
    )

    _write_run_report(output_paths["run_report"], final_summary, manifest_records)

    state.setdefault("artifacts", {})
    state["artifacts"]["stage_13_final_summary"] = str(output_paths["final_summary"])
    state["artifacts"]["stage_13_artifact_manifest"] = str(output_paths["artifact_manifest"])
    state["artifacts"]["stage_13_run_report"] = str(output_paths["run_report"])

    state.setdefault("qc", {})
    state["qc"]["stage_13_qc"] = {
        "required_inputs_validated": True,
        "row_count_consistency_passed": True,
        "final_summary_exists": output_paths["final_summary"].exists(),
        "artifact_manifest_exists": output_paths["artifact_manifest"].exists(),
        "run_report_exists": output_paths["run_report"].exists(),
    }

    state.setdefault("stage_outputs", {})
    state["stage_outputs"]["stage_13_write_summary"] = {
        "status": "success",
        "final_summary": str(output_paths["final_summary"]),
        "artifact_manifest": str(output_paths["artifact_manifest"]),
        "run_report": str(output_paths["run_report"]),
    }

    _log(logger, "info", f"Stage 13 final summary written to: {output_paths['final_summary']}")
    _log(logger, "info", f"Stage 13 artifact manifest written to: {output_paths['artifact_manifest']}")
    _log(logger, "info", f"Stage 13 run report written to: {output_paths['run_report']}")

    return state