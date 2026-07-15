#!/usr/bin/env python3
"""Asymmetric, version-aware comparison of current and historical VAP runs.

Run from VAP repo root:

python scripts/analysis/historical_run_reproducibility_comparison.py \
  --current-run results/run_2026_07_14_114546 \
  --historical-run results/run_2026_05_27_172531 \
  --case-study docs/case_studies/err10619300 \
  --output-dir \
  docs/validation/comparisons/err10619300_genotype_elevation_validation \
  --overwrite

"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
import re
import shutil
import sys
import tempfile
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

VERSION = "0.9.0"

MATCH = "MATCH"
DIFFERENT = "DIFFERENT"
EVOLUTION = "EXPECTED_ARCHITECTURE_EVOLUTION"
RUN_IDENTITY = "RUN_IDENTITY_DIFFERENCE"
HISTORICAL_UNAVAILABLE = "HISTORICAL_ARTIFACT_UNAVAILABLE"
NOT_COMPARABLE = "NOT_COMPARABLE"
UNDER_REVIEW = "UNDER_REVIEW"
CURRENT_PASS = "CURRENT_ONLY_VALIDATION_PASS"
CURRENT_FAIL = "CURRENT_ONLY_VALIDATION_FAIL"

OVERALL_AVAILABLE = "REPRODUCIBLE_WITHIN_AVAILABLE_SURFACES"
OVERALL_EVOLUTION = "REPRODUCIBLE_WITH_EXPECTED_ARCHITECTURE_EVOLUTION"
OVERALL_PARTIAL = "PARTIALLY_REPRODUCIBLE"
OVERALL_REVIEW = "SCIENTIFIC_DIFFERENCE_UNDER_REVIEW"
OVERALL_NOT_COMPARABLE = "NOT_COMPARABLE_WITH_AVAILABLE_EVIDENCE"
OVERALL_FAILED = "COMPARISON_FAILED"

STAGES = [*(f"stage_{i:02d}_summary.json" for i in range(1, 13)), "stage_13_final_summary.json"]
TABLES = [
    "stage_08_vdb_ready_variants.tsv",
    "stage_08_selected_transcript_consequences.tsv",
    "stage_09_coding_interpreted.tsv",
    "stage_10_noncoding_interpreted.tsv",
    "stage_11_prioritized_variants.tsv",
    "stage_12_validation_candidates.tsv",
]
CASE_TABLES = [
    "candidate_reviewability_readiness.tsv",
    "clinical_status_summary.tsv",
    "coding_noncoding_consequence_summary.tsv",
    "gene_burden_summary.tsv",
    "gene_list_overlay_intersections.tsv",
    "interpretation_label_summary.tsv",
    "priority_tier_summary.tsv",
    "provenance_summary.tsv",
    "run_reproducibility_summary.tsv",
    "runtime_stage_summary.tsv",
    "stage_funnel_summary.tsv",
    "variant_consequence_summary.tsv",
]

RUN_TOKENS = {
    "run_id", "execution_run_id", "source_run_id", "tep_id", "generated_utc",
    "generated_at", "timestamp", "start_time", "end_time", "config_path",
    "config_snapshot_path", "package_root", "run_directory", "processed_directory",
    "input_files", "output_files", "artifact_path", "transport_path", "path",
    "filename", "hostname", "machine_id",
}
EVOLUTION_TOKENS = {
    "execution_provenance", "genotype", "genotype_projection", "genotype_capability",
    "package_metadata", "metadata_entity", "lineage_manifest", "tep",
}
SCIENTIFIC_TOKENS = {
    "count", "row", "variant", "clinical", "frequency", "severity", "consequence",
    "priority", "validation", "gene", "malformed", "unassigned", "interpret",
    "candidate", "coding", "noncoding", "splice", "rare", "common", "pathogenic",
    "benign", "vus",
}
RUN_PATTERNS = [
    re.compile(r"run_\d{4}_\d{2}_\d{2}_\d{6}"),
    re.compile(r"vap_tep_[^/\s]+"),
]


class ComparisonError(RuntimeError):
    pass


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def atomic_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", newline="", dir=path.parent, delete=False) as fh:
        tmp = Path(fh.name)
        fh.write(text)
    try:
        os.replace(tmp, path)
    finally:
        tmp.unlink(missing_ok=True)


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    atomic_text(path, json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n")


def cell(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (dict, list)):
        return json.dumps(value, sort_keys=True, ensure_ascii=False)
    return str(value)


def write_tsv(path: Path, fields: Sequence[str], rows: Iterable[Mapping[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", newline="", dir=path.parent, delete=False) as fh:
        tmp = Path(fh.name)
        writer = csv.DictWriter(fh, fieldnames=list(fields), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: cell(row.get(field)) for field in fields})
    try:
        os.replace(tmp, path)
    finally:
        tmp.unlink(missing_ok=True)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ComparisonError(f"Cannot read JSON {path}: {exc}") from exc


def classify_artifact(path: Path) -> str:
    name = path.name.lower()
    if name.endswith("_summary.json") or name == "stage_13_final_summary.json":
        return "stage_summary"
    if path.suffix.lower() == ".tsv":
        return "table"
    if path.suffix.lower() == ".json":
        return "json"
    if path.suffix.lower() in {".yaml", ".yml"}:
        return "configuration"
    if path.suffix.lower() == ".md":
        return "markdown"
    if path.suffix.lower() in {".png", ".pdf", ".svg"}:
        return "figure"
    return "other"


def inventory(root: Path, source: str, max_hash_bytes: int) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in sorted((p for p in root.rglob("*") if p.is_file()), key=lambda p: p.as_posix()):
        size = path.stat().st_size
        rows.append({
            "source": source,
            "relative_path": path.relative_to(root).as_posix(),
            "filename": path.name,
            "suffix": path.suffix.lower(),
            "size_bytes": size,
            "sha256_status": "computed" if size <= max_hash_bytes else "deferred_large_file",
            "sha256": sha256(path) if size <= max_hash_bytes else "",
            "artifact_class": classify_artifact(path),
        })
    return rows


def identity(root: Path) -> dict[str, Any]:
    available_identity_files: list[str] = []
    result: dict[str, Any] = {
        "root": str(root),
        "available_identity_files": available_identity_files,
    }

    identity_keys = (
        "run_id",
        "sample_id",
        "status",
        "start_time",
        "end_time",
        "pipeline_version",
    )

    for path in [
        root / "metadata" / "run_metadata.json",
        root / "metadata.json",
        root / "processed" / "stage_13_final_summary.json",
        root / "metadata" / "run_fingerprint.json",
    ]:
        if not path.is_file():
            continue

        available_identity_files.append(
            str(path.relative_to(root))
        )

        loaded = load_json(path)
        if not isinstance(loaded, dict):
            continue

        data: dict[str, Any] = loaded
        run_value = data.get("run")

        run: dict[str, Any]
        if isinstance(run_value, dict):
            run = run_value
        else:
            run = {}

        for key in identity_keys:
            if key in result:
                continue

            if key in data:
                result[key] = data[key]
            elif key in run:
                result[key] = run[key]

        if "tep" in data and "tep" not in result:
            result["tep"] = data["tep"]

    return result


def find_summary(root: Path, filename: str) -> Path | None:
    for path in [
        root / "processed" / filename,
        root / "metadata" / "stage_summaries" / filename,
        root / "metadata" / filename,
    ]:
        if path.is_file():
            return path
    return None


def flatten(value: Any, prefix: str = "") -> dict[str, Any]:
    out: dict[str, Any] = {}
    if isinstance(value, dict):
        for key in sorted(value):
            child = f"{prefix}.{key}" if prefix else str(key)
            out.update(flatten(value[key], child))
    elif isinstance(value, list):
        out[prefix] = value if all(not isinstance(x, (dict, list)) for x in value) else json.dumps(value, sort_keys=True)
    else:
        out[prefix] = value
    return out


def field_class(path: str) -> str:
    """Classify a flattened JSON field or tabular column conservatively."""
    lower = path.lower()
    segments = set(re.split(r"[.\[\]/]+", lower))
    final_segment = lower.rsplit(".", 1)[-1]

    if (
        segments & RUN_TOKENS
        or final_segment.endswith(("_path", "_file", "_filename", "_directory"))
        or final_segment in {
            "artifact_manifest_path",
            "run_report_path",
            "input_path",
            "output_path",
        }
    ):
        return "run_identity"

    if segments & EVOLUTION_TOKENS:
        return "architecture_evolution"

    if any(token in lower for token in SCIENTIFIC_TOKENS):
        return "scientific"

    return "operational_or_other"


def normalize_identity(value: str) -> str:
    for pattern in RUN_PATTERNS:
        value = pattern.sub("<RUN_IDENTITY>", value)
    return value


def compare_values(
    path: str,
    historical: Any,
    current: Any,
    abs_tol: float,
    rel_tol: float,
) -> tuple[str, Any, Any, str]:
    cls = field_class(path)
    lower_path = path.lower()

    if cls == "run_identity":
        if historical == current:
            return MATCH, "", "", ""
        if (
            isinstance(historical, str)
            and isinstance(current, str)
            and normalize_identity(historical) == normalize_identity(current)
        ):
            return RUN_IDENTITY, "", "", "normalized run identity differs"
        return RUN_IDENTITY, "", "", "run-specific identity differs"

    if cls == "architecture_evolution":
        return (
            (MATCH, "", "", "")
            if historical == current
            else (
                EVOLUTION,
                "",
                "",
                "post-historical capability or schema field",
            )
        )

    # Historical VEP provenance occasionally captured the banner rather than
    # the numeric release. Treat the repaired numeric capture as provenance
    # hardening, not biological divergence.
    if "annotation_version" in lower_path:
        historical_text = str(historical).strip()
        current_text = str(current).strip()
        if (
            "VARIANT EFFECT PREDICTOR" in historical_text.upper()
            and re.fullmatch(r"\d+(?:\.\d+)*", current_text)
        ):
            return (
                EVOLUTION,
                "",
                "",
                "historical VEP banner capture replaced by explicit numeric version provenance",
            )

    if (
        isinstance(historical, (int, float))
        and not isinstance(historical, bool)
        and isinstance(current, (int, float))
        and not isinstance(current, bool)
    ):
        delta = float(current) - float(historical)
        relative = "" if float(historical) == 0 else delta / abs(float(historical))
        equal = (
            historical == current
            if isinstance(historical, int) and isinstance(current, int)
            else math.isclose(
                float(historical),
                float(current),
                abs_tol=abs_tol,
                rel_tol=rel_tol,
            )
        )
        return (
            MATCH if equal else UNDER_REVIEW,
            delta,
            relative,
            "" if equal else "comparable numeric value differs",
        )

    if historical == current:
        return MATCH, "", "", ""

    if isinstance(historical, str) and isinstance(current, str):
        historical_numeric = _parse_float(historical)
        current_numeric = _parse_float(current)
        if historical_numeric is not None and current_numeric is not None:
            delta = current_numeric - historical_numeric
            relative = (
                ""
                if historical_numeric == 0
                else delta / abs(historical_numeric)
            )
            equal = math.isclose(
                historical_numeric,
                current_numeric,
                abs_tol=abs_tol,
                rel_tol=rel_tol,
            )
            return (
                MATCH if equal else UNDER_REVIEW,
                delta,
                relative,
                "" if equal else "comparable numeric text value differs",
            )

    return UNDER_REVIEW, "", "", "comparable nonnumeric value differs"


def compare_summaries(current_root: Path, historical_root: Path, abs_tol: float, rel_tol: float) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    comparisons: list[dict[str, Any]] = []
    availability: list[dict[str, Any]] = []
    for filename in STAGES:
        current = find_summary(current_root, filename)
        historical = find_summary(historical_root, filename)
        if current is None or historical is None:
            availability.append({
                "artifact_role": filename,
                "current_path": str(current.relative_to(current_root)) if current else "",
                "historical_path": str(historical.relative_to(historical_root)) if historical else "",
                "classification": HISTORICAL_UNAVAILABLE if current and not historical else NOT_COMPARABLE,
                "notes": "historical lightweight extraction did not retain this summary" if current and not historical else "summary unavailable on one or both sides",
            })
            continue
        availability.append({
            "artifact_role": filename,
            "current_path": str(current.relative_to(current_root)),
            "historical_path": str(historical.relative_to(historical_root)),
            "classification": MATCH,
            "notes": "directly comparable summary discovered",
        })
        current_data = flatten(load_json(current))
        historical_data = flatten(load_json(historical))
        for path in sorted(set(current_data) | set(historical_data)):
            if path not in historical_data:
                comparisons.append({
                    "stage": filename.removesuffix(".json"),
                    "historical_source_path": str(historical.relative_to(historical_root)),
                    "current_source_path": str(current.relative_to(current_root)),
                    "field_path": path,
                    "field_class": field_class(path),
                    "historical_value": "",
                    "current_value": current_data[path],
                    "absolute_delta": "",
                    "relative_delta": "",
                    "classification": EVOLUTION if field_class(path) == "architecture_evolution" else HISTORICAL_UNAVAILABLE,
                    "notes": "field absent from historical schema or lightweight reference",
                })
                continue
            if path not in current_data:
                comparisons.append({
                    "stage": filename.removesuffix(".json"),
                    "historical_source_path": str(historical.relative_to(historical_root)),
                    "current_source_path": str(current.relative_to(current_root)),
                    "field_path": path,
                    "field_class": field_class(path),
                    "historical_value": historical_data[path],
                    "current_value": "",
                    "absolute_delta": "",
                    "relative_delta": "",
                    "classification": NOT_COMPARABLE,
                    "notes": "historical field absent from current schema",
                })
                continue
            classification, delta, relative, notes = compare_values(path, historical_data[path], current_data[path], abs_tol, rel_tol)
            comparisons.append({
                "stage": filename.removesuffix(".json"),
                "historical_source_path": str(historical.relative_to(historical_root)),
                "current_source_path": str(current.relative_to(current_root)),
                "field_path": path,
                "field_class": field_class(path),
                "historical_value": historical_data[path],
                "current_value": current_data[path],
                "absolute_delta": delta,
                "relative_delta": relative,
                "classification": classification,
                "notes": notes,
            })
    return comparisons, availability


def find_name(root: Path, filename: str) -> Path | None:
    candidates = sorted((p for p in root.rglob(filename) if p.is_file()), key=lambda p: (len(p.parts), p.as_posix()))
    return candidates[0] if candidates else None


def tsv_header(path: Path) -> list[str]:
    with path.open("r", encoding="utf-8", errors="replace", newline="") as fh:
        return next(csv.reader(fh, delimiter="\t"), [])


def tsv_rows(path: Path) -> int:
    with path.open("r", encoding="utf-8", errors="replace") as fh:
        return max(sum(1 for _ in fh) - 1, 0)


def parse_tsv(
    path: Path,
) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(
        "r",
        encoding="utf-8",
        errors="replace",
        newline="",
    ) as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        rows = [
            {
                str(key): str(value or "")
                for key, value in row.items()
                if key is not None
            }
            for row in reader
        ]
        return list(reader.fieldnames or []), rows


def stable_key(shared: Sequence[str]) -> list[str]:
    columns = set(shared)
    for candidate in (["variant_id"], ["chromosome", "position", "reference", "alternate"], ["chrom", "pos", "ref", "alt"]):
        if all(item in columns for item in candidate):
            return list(candidate)
    return []


def compare_tables(current_root: Path, historical_root: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    rows: list[dict[str, Any]] = []
    availability: list[dict[str, Any]] = []
    for filename in TABLES:
        current = find_name(current_root, filename)
        historical = find_name(historical_root, filename)
        if current is None or historical is None:
            availability.append({
                "artifact_role": filename,
                "current_path": str(current.relative_to(current_root)) if current else "",
                "historical_path": str(historical.relative_to(historical_root)) if historical else "",
                "classification": HISTORICAL_UNAVAILABLE if current and not historical else NOT_COMPARABLE,
                "notes": "historical lightweight extraction did not retain this table" if current and not historical else "table unavailable on one or both sides",
            })
            continue
        ch = tsv_header(current)
        hh = tsv_header(historical)
        shared = sorted(set(ch) & set(hh))
        cr = tsv_rows(current)
        hr = tsv_rows(historical)
        key = stable_key(shared)
        classification = MATCH if cr == hr else UNDER_REVIEW
        notes = []
        if cr != hr:
            notes.append("row counts differ")
        if set(ch) - set(hh):
            notes.append("current schema contains additional columns")
        if set(hh) - set(ch):
            notes.append("historical schema contains columns absent from current")
        if not key:
            notes.append("no verified stable key; row-level comparison deferred")
        availability.append({
            "artifact_role": filename,
            "current_path": str(current.relative_to(current_root)),
            "historical_path": str(historical.relative_to(historical_root)),
            "classification": classification,
            "notes": "; ".join(notes),
        })
        rows.append({
            "table": filename,
            "historical_path": str(historical.relative_to(historical_root)),
            "current_path": str(current.relative_to(current_root)),
            "historical_row_count": hr,
            "current_row_count": cr,
            "row_count_delta": cr - hr,
            "historical_column_count": len(hh),
            "current_column_count": len(ch),
            "shared_column_count": len(shared),
            "shared_columns": shared,
            "historical_only_columns": sorted(set(hh) - set(ch)),
            "current_only_columns": sorted(set(ch) - set(hh)),
            "stable_key_columns": key,
            "classification": classification,
            "notes": "; ".join(notes),
        })
    return rows, availability



def _key_to_text(values: Sequence[str]) -> str:
    return "|".join(values)


def _load_keyed_rows(
    path: Path,
    key_columns: Sequence[str],
    shared_columns: Sequence[str],
) -> tuple[dict[tuple[str, ...], dict[str, str]], int, int]:
    rows: dict[tuple[str, ...], dict[str, str]] = {}
    duplicate_count = 0
    null_key_count = 0

    with path.open("r", encoding="utf-8", errors="replace", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        for raw in reader:
            key = tuple((raw.get(column) or "").strip() for column in key_columns)
            if any(value == "" for value in key):
                null_key_count += 1
                continue
            if key in rows:
                duplicate_count += 1
                continue
            rows[key] = {
                column: (raw.get(column) or "").strip()
                for column in shared_columns
            }

    return rows, duplicate_count, null_key_count


def compare_keyed_tables(
    current_root: Path,
    historical_root: Path,
    schema_rows: Sequence[Mapping[str, Any]],
    *,
    abs_tol: float,
    rel_tol: float,
) -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
]:
    summaries: list[dict[str, Any]] = []
    unmatched: list[dict[str, Any]] = []
    all_differences: list[dict[str, Any]] = []
    scientific_differences: list[dict[str, Any]] = []

    for schema in schema_rows:
        table = str(schema.get("table", ""))
        key_columns = list(schema.get("stable_key_columns") or [])
        shared_columns = list(schema.get("shared_columns") or [])

        if not key_columns:
            continue

        current_path = current_root / str(schema["current_path"])
        historical_path = historical_root / str(schema["historical_path"])

        historical_rows, historical_duplicates, historical_null_keys = _load_keyed_rows(
            historical_path,
            key_columns,
            shared_columns,
        )
        current_rows, current_duplicates, current_null_keys = _load_keyed_rows(
            current_path,
            key_columns,
            shared_columns,
        )

        historical_keys = set(historical_rows)
        current_keys = set(current_rows)
        historical_only = sorted(historical_keys - current_keys)
        current_only = sorted(current_keys - historical_keys)
        shared_keys = sorted(historical_keys & current_keys)

        scientific_changed_rows = 0
        scientific_changed_fields = 0
        run_identity_changed_rows = 0
        run_identity_changed_fields = 0
        evolution_changed_rows = 0
        evolution_changed_fields = 0
        other_changed_rows = 0
        other_changed_fields = 0

        for key in historical_only:
            unmatched.append({
                "table": table,
                "key_columns": key_columns,
                "key": _key_to_text(key),
                "presence": "historical_only",
                "classification": UNDER_REVIEW,
                "notes": "variant key absent from current table",
            })

        for key in current_only:
            unmatched.append({
                "table": table,
                "key_columns": key_columns,
                "key": _key_to_text(key),
                "presence": "current_only",
                "classification": UNDER_REVIEW,
                "notes": "variant key absent from historical table",
            })

        for key in shared_keys:
            row_scientific = False
            row_identity = False
            row_evolution = False
            row_other = False

            historical_row = historical_rows[key]
            current_row = current_rows[key]

            for column in shared_columns:
                if column in key_columns:
                    continue

                historical_value = historical_row.get(column, "")
                current_value = current_row.get(column, "")
                if historical_value == current_value:
                    continue

                classification, delta, relative, notes = compare_values(
                    column,
                    historical_value,
                    current_value,
                    abs_tol,
                    rel_tol,
                )
                field_type = field_class(column)

                record = {
                    "table": table,
                    "key_columns": key_columns,
                    "key": _key_to_text(key),
                    "column": column,
                    "field_class": field_type,
                    "historical_value": historical_value,
                    "current_value": current_value,
                    "absolute_delta": delta,
                    "relative_delta": relative,
                    "classification": classification,
                    "notes": notes,
                }
                all_differences.append(record)

                if classification in {RUN_IDENTITY}:
                    run_identity_changed_fields += 1
                    row_identity = True
                elif classification in {EVOLUTION}:
                    evolution_changed_fields += 1
                    row_evolution = True
                elif (
                    field_type == "scientific"
                    and classification in {DIFFERENT, UNDER_REVIEW}
                ):
                    scientific_changed_fields += 1
                    row_scientific = True
                    scientific_differences.append(record)
                elif classification in {DIFFERENT, UNDER_REVIEW}:
                    other_changed_fields += 1
                    row_other = True

            scientific_changed_rows += int(row_scientific)
            run_identity_changed_rows += int(row_identity)
            evolution_changed_rows += int(row_evolution)
            other_changed_rows += int(row_other)

        if historical_duplicates or current_duplicates:
            classification = NOT_COMPARABLE
            notes = "duplicate stable keys prevent complete identity comparison"
        elif historical_null_keys or current_null_keys:
            classification = UNDER_REVIEW
            notes = "rows with incomplete stable keys were excluded"
        elif (
            not historical_only
            and not current_only
            and scientific_changed_rows == 0
        ):
            classification = MATCH
            notes = "all keyed scientific fields match; identity/evolution differences excluded"
        else:
            classification = UNDER_REVIEW
            notes = "variant key presence or shared scientific fields differ"

        summaries.append({
            "table": table,
            "key_columns": key_columns,
            "historical_unique_key_count": len(historical_rows),
            "current_unique_key_count": len(current_rows),
            "shared_key_count": len(shared_keys),
            "historical_only_key_count": len(historical_only),
            "current_only_key_count": len(current_only),
            "historical_duplicate_key_count": historical_duplicates,
            "current_duplicate_key_count": current_duplicates,
            "historical_null_key_count": historical_null_keys,
            "current_null_key_count": current_null_keys,
            "scientific_changed_shared_row_count": scientific_changed_rows,
            "scientific_changed_shared_field_count": scientific_changed_fields,
            "run_identity_changed_shared_row_count": run_identity_changed_rows,
            "run_identity_changed_shared_field_count": run_identity_changed_fields,
            "evolution_changed_shared_row_count": evolution_changed_rows,
            "evolution_changed_shared_field_count": evolution_changed_fields,
            "other_changed_shared_row_count": other_changed_rows,
            "other_changed_shared_field_count": other_changed_fields,
            "classification": classification,
            "notes": notes,
        })

    return summaries, unmatched, all_differences, scientific_differences


MISSING_LABEL = "<MISSING>"
OTHER_LABEL = "<OTHER>"

PREFERRED_DISTRIBUTION_TOKENS = (
    "clinvar",
    "significance",
    "clinical",
    "consequence",
    "impact",
    "severity",
    "frequency",
    "allele_freq",
    "allele_frequency",
    "gnomad",
    "af",
    "priority",
    "tier",
    "interpretation",
    "validation",
    "variant_type",
    "variant_class",
    "biotype",
    "coding",
    "noncoding",
    "splice",
    "qc",
    "status",
    "label",
)

AF_COLUMN_PATTERN = re.compile(
    r"(^|_)(af|allele_frequency|population_frequency|pop_freq|gnomad.*af)($|_)",
    re.IGNORECASE,
)

DEFAULT_AF_BINS: tuple[tuple[float | None, float | None, str], ...] = (
    (None, 0.0, "<=0"),
    (0.0, 0.0001, "(0,0.0001]"),
    (0.0001, 0.001, "(0.0001,0.001]"),
    (0.001, 0.01, "(0.001,0.01]"),
    (0.01, 0.05, "(0.01,0.05]"),
    (0.05, 1.0, "(0.05,1]"),
    (1.0, None, ">1"),
)


def _parse_float(value: str) -> float | None:
    stripped = value.strip()
    if stripped == "" or stripped.lower() in {
        "na", "nan", "none", "null", ".", "missing",
    }:
        return None
    try:
        parsed = float(stripped)
    except ValueError:
        return None
    if not math.isfinite(parsed):
        return None
    return parsed


def _af_bin(value: float | None) -> str:
    if value is None:
        return MISSING_LABEL
    for lower, upper, label in DEFAULT_AF_BINS:
        lower_ok = lower is None or value > lower
        upper_ok = upper is None or value <= upper
        if lower_ok and upper_ok:
            return label
    return ">1"


def _is_preferred_distribution_column(column: str) -> bool:
    lower = column.lower()
    return any(token in lower for token in PREFERRED_DISTRIBUTION_TOKENS)


def _scan_column_profiles(
    path: Path,
    columns: Sequence[str],
    *,
    max_categories: int,
) -> dict[str, dict[str, Any]]:
    profiles: dict[str, dict[str, Any]] = {
        column: {
            "row_count": 0,
            "missing_count": 0,
            "numeric_count": 0,
            "numeric_sum": 0.0,
            "numeric_min": None,
            "numeric_max": None,
            "categorical": Counter(),
            "category_overflow": False,
            "af_bins": Counter(),
        }
        for column in columns
    }

    with path.open("r", encoding="utf-8", errors="replace", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        for raw in reader:
            for column in columns:
                profile = profiles[column]
                profile["row_count"] += 1
                value = (raw.get(column) or "").strip()

                if value == "" or value.lower() in {
                    "na", "nan", "none", "null", ".", "missing",
                }:
                    profile["missing_count"] += 1
                    normalized = MISSING_LABEL
                else:
                    normalized = value

                numeric = _parse_float(value)
                if numeric is not None:
                    profile["numeric_count"] += 1
                    profile["numeric_sum"] += numeric
                    current_min = profile["numeric_min"]
                    current_max = profile["numeric_max"]
                    profile["numeric_min"] = (
                        numeric if current_min is None else min(current_min, numeric)
                    )
                    profile["numeric_max"] = (
                        numeric if current_max is None else max(current_max, numeric)
                    )

                if AF_COLUMN_PATTERN.search(column):
                    profile["af_bins"][_af_bin(numeric)] += 1

                if not profile["category_overflow"]:
                    profile["categorical"][normalized] += 1
                    if (
                        len(profile["categorical"]) > max_categories
                        and not _is_preferred_distribution_column(column)
                    ):
                        profile["category_overflow"] = True
                        profile["categorical"].clear()

    return profiles


def compare_column_distributions(
    current_root: Path,
    historical_root: Path,
    schema_rows: Sequence[Mapping[str, Any]],
    *,
    max_categories: int = 100,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    distribution_rows: list[dict[str, Any]] = []
    numeric_rows: list[dict[str, Any]] = []

    for schema in schema_rows:
        table = str(schema.get("table", ""))
        shared_columns = list(schema.get("shared_columns") or [])
        distribution_columns = [
            column
            for column in shared_columns
            if field_class(column) not in {"run_identity", "architecture_evolution"}
        ]
        if not distribution_columns:
            continue

        current_path = current_root / str(schema["current_path"])
        historical_path = historical_root / str(schema["historical_path"])

        historical_profiles = _scan_column_profiles(
            historical_path,
            distribution_columns,
            max_categories=max_categories,
        )
        current_profiles = _scan_column_profiles(
            current_path,
            distribution_columns,
            max_categories=max_categories,
        )

        for column in distribution_columns:
            historical = historical_profiles[column]
            current = current_profiles[column]

            numeric_possible = (
                historical["numeric_count"] > 0
                or current["numeric_count"] > 0
            )
            if numeric_possible:
                historical_mean = (
                    historical["numeric_sum"] / historical["numeric_count"]
                    if historical["numeric_count"]
                    else None
                )
                current_mean = (
                    current["numeric_sum"] / current["numeric_count"]
                    if current["numeric_count"]
                    else None
                )
                metrics = {
                    "row_count": (
                        historical["row_count"],
                        current["row_count"],
                    ),
                    "missing_count": (
                        historical["missing_count"],
                        current["missing_count"],
                    ),
                    "numeric_count": (
                        historical["numeric_count"],
                        current["numeric_count"],
                    ),
                    "minimum": (
                        historical["numeric_min"],
                        current["numeric_min"],
                    ),
                    "maximum": (
                        historical["numeric_max"],
                        current["numeric_max"],
                    ),
                    "mean": (
                        historical_mean,
                        current_mean,
                    ),
                }
                for metric, (historical_value, current_value) in metrics.items():
                    if historical_value is None or current_value is None:
                        delta = ""
                        classification = (
                            MATCH
                            if historical_value is None and current_value is None
                            else UNDER_REVIEW
                        )
                    else:
                        delta = float(current_value) - float(historical_value)
                        classification = (
                            MATCH
                            if math.isclose(
                                float(historical_value),
                                float(current_value),
                                abs_tol=1e-12,
                                rel_tol=1e-9,
                            )
                            else UNDER_REVIEW
                        )
                    numeric_rows.append({
                        "table": table,
                        "column": column,
                        "metric": metric,
                        "historical_value": historical_value,
                        "current_value": current_value,
                        "delta": delta,
                        "classification": classification,
                    })

            historical_counter: Counter[str]
            current_counter: Counter[str]
            distribution_type: str

            if AF_COLUMN_PATTERN.search(column):
                historical_counter = historical["af_bins"]
                current_counter = current["af_bins"]
                distribution_type = "allele_frequency_bin"
            elif (
                not historical["category_overflow"]
                and not current["category_overflow"]
            ):
                historical_counter = historical["categorical"]
                current_counter = current["categorical"]
                distribution_type = "categorical"
            else:
                continue

            categories = sorted(
                set(historical_counter) | set(current_counter),
                key=lambda value: (value == OTHER_LABEL, value),
            )
            historical_total = sum(historical_counter.values())
            current_total = sum(current_counter.values())

            for category in categories:
                historical_count = historical_counter.get(category, 0)
                current_count = current_counter.get(category, 0)
                historical_fraction = (
                    historical_count / historical_total
                    if historical_total
                    else 0.0
                )
                current_fraction = (
                    current_count / current_total
                    if current_total
                    else 0.0
                )
                count_delta = current_count - historical_count
                fraction_delta = current_fraction - historical_fraction
                classification = (
                    MATCH
                    if (
                        historical_count == current_count
                        and math.isclose(
                            historical_fraction,
                            current_fraction,
                            abs_tol=1e-12,
                            rel_tol=1e-9,
                        )
                    )
                    else UNDER_REVIEW
                )
                distribution_rows.append({
                    "table": table,
                    "column": column,
                    "distribution_type": distribution_type,
                    "category": category,
                    "historical_count": historical_count,
                    "current_count": current_count,
                    "count_delta": count_delta,
                    "historical_fraction": historical_fraction,
                    "current_fraction": current_fraction,
                    "fraction_delta": fraction_delta,
                    "classification": classification,
                })

    distribution_rows.sort(
        key=lambda row: (
            str(row["table"]),
            str(row["column"]),
            str(row["distribution_type"]),
            str(row["category"]),
        )
    )
    numeric_rows.sort(
        key=lambda row: (
            str(row["table"]),
            str(row["column"]),
            str(row["metric"]),
        )
    )
    return distribution_rows, numeric_rows



DOSSIER_FIELD_ALIASES: dict[str, tuple[str, ...]] = {
    "variant_id": (
        "variant_id", "canonical_variant_id", "normalized_variant_id",
    ),
    "chromosome": (
        "chromosome", "chrom", "chr", "contig",
    ),
    "position": (
        "position", "pos", "start", "variant_position",
    ),
    "reference": (
        "reference", "ref", "reference_allele",
    ),
    "alternate": (
        "alternate", "alt", "alternate_allele",
    ),
    "gene_id": (
        "gene_id", "ensembl_gene_id", "gene",
    ),
    "gene_symbol": (
        "gene_symbol", "symbol", "hgnc_symbol",
    ),
    "transcript_id": (
        "transcript_id", "feature", "feature_id", "selected_transcript_id",
    ),
    "consequence": (
        "consequence", "selected_consequence", "most_severe_consequence",
        "consequence_terms", "vep_consequence",
    ),
    "impact": (
        "impact", "selected_impact", "vep_impact",
    ),
    "severity": (
        "severity", "max_variant_severity", "consequence_severity",
    ),
    "clinvar_significance": (
        "clinvar_significance", "clinical_significance",
        "clin_sig", "clinvar_clinical_significance",
    ),
    "clinical_status": (
        "clinical_status", "clinvar_status",
    ),
    "allele_frequency": (
        "allele_frequency", "population_frequency", "pop_freq",
        "gnomad_af", "gnomadg_af", "gnomade_af", "max_af", "af",
    ),
    "frequency_status": (
        "frequency_status", "frequency_bin", "population_frequency_status",
    ),
    "variant_type": (
        "variant_type", "type",
    ),
    "variant_class": (
        "variant_class", "class",
    ),
    "interpretation_label": (
        "interpretation_label", "source_interpretation_label",
        "coding_interpretation_label", "noncoding_interpretation_label",
    ),
    "priority_tier": (
        "priority_tier", "tier",
    ),
    "validation_priority": (
        "validation_priority",
    ),
    "qc_status": (
        "qc_status", "quality_status", "quality_summary",
    ),
    "genotype": (
        "genotype", "gt", "genotype_string", "gt_raw",
    ),
    "genotype_call_state": (
        "genotype_call_state", "call_state",
    ),
    "depth": (
        "depth", "dp", "read_depth",
    ),
    "genotype_quality": (
        "genotype_quality", "gq",
    ),
    "allele_depths": (
        "allele_depths", "ad",
    ),
    "phase_state": (
        "phase_state",
    ),
    "relationship_status": (
        "variant_relationship_status", "relationship_status",
    ),
    "source_run_id": (
        "run_id", "source_run_id", "execution_run_id",
    ),
}

DOSSIER_SUMMARY_FIELDS = (
    "presence",
    "chromosome",
    "consequence",
    "impact",
    "severity",
    "clinvar_significance",
    "clinical_status",
    "frequency_status",
    "variant_type",
    "variant_class",
    "interpretation_label",
    "priority_tier",
    "validation_priority",
    "qc_status",
    "genotype_call_state",
    "phase_state",
    "relationship_status",
)


def _casefold_column_map(row: Mapping[str, str]) -> dict[str, str]:
    return {str(column).casefold(): str(column) for column in row}


def _first_alias_value(
    row: Mapping[str, str],
    aliases: Sequence[str],
) -> tuple[str, str]:
    column_map = _casefold_column_map(row)
    for alias in aliases:
        actual = column_map.get(alias.casefold())
        if actual is None:
            continue
        value = (row.get(actual) or "").strip()
        if value != "":
            return value, actual
    return "", ""


def _canonicalize_dossier_row(
    row: Mapping[str, str],
) -> tuple[dict[str, str], dict[str, str]]:
    canonical: dict[str, str] = {}
    sources: dict[str, str] = {}
    for field, aliases in DOSSIER_FIELD_ALIASES.items():
        value, source_column = _first_alias_value(row, aliases)
        canonical[field] = value
        sources[field] = source_column
    return canonical, sources


def _read_selected_keyed_rows(
    path: Path,
    key_columns: Sequence[str],
    target_keys: set[tuple[str, ...]],
) -> dict[tuple[str, ...], dict[str, str]]:
    selected: dict[tuple[str, ...], dict[str, str]] = {}
    if not target_keys:
        return selected

    with path.open("r", encoding="utf-8", errors="replace", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        for raw in reader:
            key = tuple((raw.get(column) or "").strip() for column in key_columns)
            if key in target_keys and key not in selected:
                selected[key] = {
                    str(column): (value or "").strip()
                    for column, value in raw.items()
                    if column is not None
                }
                if len(selected) == len(target_keys):
                    break
    return selected


def _find_genotype_observations(current_root: Path) -> Path | None:
    candidates = [
        current_root / "processed" / "genotype_observations.tsv",
        *current_root.glob("tep/*/entities/genotype/genotype_observations.tsv"),
    ]
    return next((path for path in candidates if path.is_file()), None)


def _read_genotype_rows_by_variant_id(
    path: Path | None,
    variant_ids: set[str],
) -> dict[str, dict[str, str]]:
    selected: dict[str, dict[str, str]] = {}
    if path is None or not variant_ids:
        return selected

    with path.open("r", encoding="utf-8", errors="replace", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        fieldnames = list(reader.fieldnames or [])
        variant_column = next(
            (
                column
                for column in fieldnames
                if column.casefold() in {
                    alias.casefold()
                    for alias in DOSSIER_FIELD_ALIASES["variant_id"]
                }
            ),
            None,
        )
        if variant_column is None:
            return selected

        for raw in reader:
            variant_id = (raw.get(variant_column) or "").strip()
            if variant_id in variant_ids and variant_id not in selected:
                selected[variant_id] = {
                    str(column): (value or "").strip()
                    for column, value in raw.items()
                    if column is not None
                }
                if len(selected) == len(variant_ids):
                    break

    return selected


def _merge_nonempty(
    primary: Mapping[str, str],
    secondary: Mapping[str, str],
) -> dict[str, str]:
    merged = dict(primary)
    for key, value in secondary.items():
        if not merged.get(key) and value:
            merged[key] = value
    return merged


def build_variant_delta_dossier(
    current_root: Path,
    historical_root: Path,
    schema_rows: Sequence[Mapping[str, Any]],
    unmatched_rows: Sequence[Mapping[str, Any]],
) -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    str,
]:
    dossier_rows: list[dict[str, Any]] = []
    field_inventory_rows: list[dict[str, Any]] = []

    unmatched_by_table: dict[str, list[Mapping[str, Any]]] = {}
    for record in unmatched_rows:
        unmatched_by_table.setdefault(str(record.get("table", "")), []).append(record)

    genotype_path = _find_genotype_observations(current_root)
    current_variant_ids_for_genotype: set[str] = set()

    prepared_tables: list[
        tuple[
            str,
            list[str],
            Path,
            Path,
            dict[tuple[str, ...], dict[str, str]],
            dict[tuple[str, ...], dict[str, str]],
            list[Mapping[str, Any]],
        ]
    ] = []

    for schema in schema_rows:
        table = str(schema.get("table", ""))
        records = unmatched_by_table.get(table, [])
        key_columns = list(schema.get("stable_key_columns") or [])
        if not records or not key_columns:
            continue

        historical_targets: set[tuple[str, ...]] = set()
        current_targets: set[tuple[str, ...]] = set()

        for record in records:
            key_values = tuple(str(record.get("key", "")).split("|"))
            if len(key_values) != len(key_columns):
                continue
            if record.get("presence") == "historical_only":
                historical_targets.add(key_values)
            elif record.get("presence") == "current_only":
                current_targets.add(key_values)
                if key_columns == ["variant_id"] and key_values[0]:
                    current_variant_ids_for_genotype.add(key_values[0])

        historical_path = historical_root / str(schema["historical_path"])
        current_path = current_root / str(schema["current_path"])

        historical_selected = _read_selected_keyed_rows(
            historical_path,
            key_columns,
            historical_targets,
        )
        current_selected = _read_selected_keyed_rows(
            current_path,
            key_columns,
            current_targets,
        )

        prepared_tables.append(
            (
                table,
                key_columns,
                historical_path,
                current_path,
                historical_selected,
                current_selected,
                records,
            )
        )

    genotype_rows = _read_genotype_rows_by_variant_id(
        genotype_path,
        current_variant_ids_for_genotype,
    )

    for (
        table,
        key_columns,
        historical_path,
        current_path,
        historical_selected,
        current_selected,
        records,
    ) in prepared_tables:
        for record in records:
            presence = str(record.get("presence", ""))
            key_values = tuple(str(record.get("key", "")).split("|"))
            if len(key_values) != len(key_columns):
                continue

            source_row = (
                historical_selected.get(key_values, {})
                if presence == "historical_only"
                else current_selected.get(key_values, {})
            )
            canonical, source_columns = _canonicalize_dossier_row(source_row)

            genotype_row: dict[str, str] = {}
            genotype_canonical: dict[str, str] = {}
            genotype_sources: dict[str, str] = {}

            variant_id = canonical.get("variant_id", "")
            if not variant_id and key_columns == ["variant_id"]:
                variant_id = key_values[0]
                canonical["variant_id"] = variant_id

            if presence == "current_only" and variant_id:
                genotype_row = genotype_rows.get(variant_id, {})
                if genotype_row:
                    genotype_canonical, genotype_sources = _canonicalize_dossier_row(
                        genotype_row
                    )
                    canonical = _merge_nonempty(canonical, genotype_canonical)
                    source_columns = _merge_nonempty(source_columns, genotype_sources)

            if not canonical.get("chromosome") and len(key_columns) == 4:
                key_map = dict(zip(key_columns, key_values))
                canonical["chromosome"] = (
                    key_map.get("chromosome")
                    or key_map.get("chrom")
                    or ""
                )
                canonical["position"] = (
                    key_map.get("position")
                    or key_map.get("pos")
                    or ""
                )
                canonical["reference"] = (
                    key_map.get("reference")
                    or key_map.get("ref")
                    or ""
                )
                canonical["alternate"] = (
                    key_map.get("alternate")
                    or key_map.get("alt")
                    or ""
                )

            populated_fields = sorted(
                field for field, value in canonical.items() if value != ""
            )
            missing_expected = sorted(
                field
                for field in DOSSIER_FIELD_ALIASES
                if canonical.get(field, "") == ""
            )

            notes: list[str] = [
                f"{presence.replace('_', ' ')} variant identity",
                "scientific fields for shared variants were unchanged"
                if presence in {"historical_only", "current_only"}
                else "",
            ]
            if presence == "historical_only":
                notes.append(
                    "historical lightweight evidence has no first-class genotype surface"
                )
            elif genotype_path is None:
                notes.append("current genotype observations unavailable")
            elif variant_id and not genotype_row:
                notes.append("current genotype row not located for variant_id")
            else:
                notes.append("current genotype context enriched from first-class genotype surface")

            dossier = {
                "table": table,
                "presence": presence,
                "variant_key": str(record.get("key", "")),
                **{field: canonical.get(field, "") for field in DOSSIER_FIELD_ALIASES},
                "source_table_path": str(
                    (
                        historical_path.relative_to(historical_root)
                        if presence == "historical_only"
                        else current_path.relative_to(current_root)
                    )
                ),
                "genotype_source_path": (
                    str(genotype_path.relative_to(current_root))
                    if presence == "current_only" and genotype_path is not None
                    else ""
                ),
                "available_field_count": len(populated_fields),
                "available_fields": populated_fields,
                "source_column_map": {
                    field: source_columns.get(field, "")
                    for field in populated_fields
                },
                "missing_expected_fields": missing_expected,
                "classification": UNDER_REVIEW,
                "notes": "; ".join(note for note in notes if note),
            }
            dossier_rows.append(dossier)

            for canonical_field in DOSSIER_FIELD_ALIASES:
                field_inventory_rows.append({
                    "table": table,
                    "presence": presence,
                    "variant_key": str(record.get("key", "")),
                    "canonical_field": canonical_field,
                    "source_column": source_columns.get(canonical_field, ""),
                    "value_present": canonical.get(canonical_field, "") != "",
                    "source_surface": (
                        "genotype_observations"
                        if (
                            source_columns.get(canonical_field, "")
                            and genotype_sources.get(canonical_field, "")
                        )
                        else "stage_table"
                    ),
                })

    dossier_rows.sort(
        key=lambda row: (
            str(row.get("presence", "")),
            str(row.get("chromosome", "")),
            str(row.get("position", "")),
            str(row.get("variant_id", "")),
            str(row.get("variant_key", "")),
        )
    )

    summary_rows: list[dict[str, Any]] = []
    for field in DOSSIER_SUMMARY_FIELDS:
        counter: Counter[tuple[str, str]] = Counter()
        for row in dossier_rows:
            presence = str(row.get("presence", ""))
            value = str(row.get(field, "") or MISSING_LABEL)
            counter[(presence, value)] += 1
        for (presence, value), count_value in sorted(counter.items()):
            summary_rows.append({
                "metric": field,
                "presence": presence,
                "value": value,
                "count": count_value,
            })

    historical_count = sum(
        1 for row in dossier_rows if row.get("presence") == "historical_only"
    )
    current_count = sum(
        1 for row in dossier_rows if row.get("presence") == "current_only"
    )
    genotype_enriched_count = sum(
        1
        for row in dossier_rows
        if row.get("presence") == "current_only"
        and row.get("genotype", "") != ""
    )

    report_lines = [
        "# Variant Delta Dossier",
        "",
        f"- Script version: `{VERSION}`",
        f"- Historical-only variant identities: `{historical_count}`",
        f"- Current-only variant identities: `{current_count}`",
        f"- Net current-minus-historical identity count: `{current_count - historical_count}`",
        f"- Current-only variants enriched with genotype: `{genotype_enriched_count}`",
        "",
        "## Interpretation Boundary",
        "",
        "This dossier describes only variant identities that are unmatched between the historical lightweight reference and the current complete execution. Shared variant identities are excluded because the current keyed comparison establishes zero shared-row scientific-field differences on the directly comparable coding table.",
        "",
        "Historical-only variants do not have first-class genotype evidence in the retained lightweight extraction. Their missing genotype fields are evidence limitations, not genotype failures.",
        "",
        "## Variant Inventory",
        "",
        "| Presence | Variant ID | Locus | Gene | Consequence | ClinVar | Frequency | Genotype |",
        "|---|---|---|---|---|---|---|---|",
    ]

    for row in dossier_rows:
        locus = ":".join(
            value
            for value in (
                str(row.get("chromosome", "")),
                str(row.get("position", "")),
                str(row.get("reference", "")),
                str(row.get("alternate", "")),
            )
            if value
        )
        report_lines.append(
            "| "
            + " | ".join(
                [
                    str(row.get("presence", "")),
                    str(row.get("variant_id", "") or row.get("variant_key", "")),
                    locus,
                    str(row.get("gene_symbol", "") or row.get("gene_id", "")),
                    str(row.get("consequence", "")),
                    str(
                        row.get("clinvar_significance", "")
                        or row.get("clinical_status", "")
                    ),
                    str(
                        row.get("frequency_status", "")
                        or row.get("allele_frequency", "")
                    ),
                    str(
                        row.get("genotype", "")
                        or (
                            "<HISTORICAL_GENOTYPE_UNAVAILABLE>"
                            if row.get("presence") == "historical_only"
                            else ""
                        )
                    ),
                ]
            )
            + " |"
        )

    report_lines.extend([
        "",
        "## Required Follow-Up",
        "",
        "The dossier localizes the comparison closure problem to explicit variant identities. Final attribution still requires determining whether each identity difference originated in the upstream VCF, transcript selection/annotation, or historical pipeline-version behavior.",
        "",
    ])

    return (
        dossier_rows,
        summary_rows,
        field_inventory_rows,
        "\n".join(report_lines),
    )



GENOTYPE_HARDENING_ALIASES: dict[str, tuple[str, ...]] = {
    "variant_id": (
        "variant_id", "canonical_variant_id", "normalized_variant_id",
        "source_variant_id",
    ),
    "chromosome": (
        "chromosome", "chrom", "chr", "contig", "source_chromosome",
    ),
    "position": (
        "position", "pos", "start", "variant_position", "source_position",
    ),
    "reference": (
        "reference", "ref", "reference_allele", "source_reference",
    ),
    "alternate": (
        "alternate", "alt", "alternate_allele", "source_alternate",
        "source_alt", "source_alt_set",
    ),
    "genotype": (
        "genotype", "gt", "genotype_string", "gt_raw", "raw_gt",
        "sample_gt", "format_gt", "gt_value",
    ),
    "allele_depths": (
        "allele_depths", "ad", "ad_raw", "raw_ad", "sample_ad",
        "format_ad", "ad_value", "ref_depth", "alt_depth",
        "alt_depths_raw",
    ),
    "depth": (
        "depth", "dp", "read_depth", "raw_dp", "sample_dp",
        "format_dp", "dp_value",
    ),
    "genotype_quality": (
        "genotype_quality", "gq", "raw_gq", "sample_gq",
        "format_gq", "gq_value",
    ),
    "phred_likelihoods": (
        "phred_likelihoods", "pl", "pl_raw", "raw_pl", "sample_pl",
        "format_pl", "pl_value", "pl_value_count",
    ),
    "filter_status": (
        "filter_status", "ft", "ft_raw", "raw_ft", "sample_ft",
        "format_ft", "sample_filter_raw", "site_filter_raw",
    ),
    "gt_arity": (
        "gt_arity", "genotype_arity", "allele_arity",
    ),
    "called_allele_indexes": (
        "called_allele_indexes", "called_allele_indices",
        "allele_indexes", "allele_indices",
    ),
    "genotype_call_state": (
        "genotype_call_state", "call_state",
    ),
    "phase_state": (
        "phase_state", "phasing_state",
    ),
    "relationship_status": (
        "variant_relationship_status", "relationship_status",
        "genotype_variant_relationship_status",
    ),
    "projection_status": (
        "projection_status", "genotype_projection_status",
    ),
    "projection_advisory": (
        "projection_advisory", "advisory_code", "projection_advisory_code",
        "relationship_advisory", "projection_advisory_codes",
        "projection_warning_codes", "relationship_reason",
    ),
    "record_parse_status": (
        "record_parse_status", "parse_status",
    ),
}


def _normalized_column_name(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", value.casefold())


def _resolve_columns(
    fieldnames: Sequence[str],
    aliases: Mapping[str, Sequence[str]],
) -> dict[str, str]:
    exact = {column.casefold(): column for column in fieldnames}
    normalized = {
        _normalized_column_name(column): column
        for column in fieldnames
    }
    resolved: dict[str, str] = {}

    for canonical, candidates in aliases.items():
        for candidate in candidates:
            actual = exact.get(candidate.casefold())
            if actual is None:
                actual = normalized.get(_normalized_column_name(candidate))
            if actual is not None:
                resolved[canonical] = actual
                break

    return resolved


def _variant_components(
    variant_id: str,
) -> tuple[str, str, str, str] | None:
    parts = variant_id.split(":", 3)
    if len(parts) != 4:
        return None
    chromosome, position, reference, alternate = (
        part.strip() for part in parts
    )
    if not chromosome or not position or not reference or not alternate:
        return None
    return chromosome, position, reference, alternate


def _locus_key_from_values(
    chromosome: str,
    position: str,
    reference: str,
) -> tuple[str, str, str] | None:
    values = (
        chromosome.strip(),
        position.strip(),
        reference.strip(),
    )
    return values if all(values) else None


def _locus_key_from_row(
    row: Mapping[str, str],
    column_map: Mapping[str, str],
) -> tuple[str, str, str] | None:
    chromosome = (
        row.get(column_map.get("chromosome", ""), "") or ""
    )
    position = (
        row.get(column_map.get("position", ""), "") or ""
    )
    reference = (
        row.get(column_map.get("reference", ""), "") or ""
    )
    return _locus_key_from_values(
        chromosome,
        position,
        reference,
    )


def _canonical_genotype_values(
    row: Mapping[str, str],
    column_map: Mapping[str, str],
) -> dict[str, str]:
    values: dict[str, str] = {}
    for canonical, column in column_map.items():
        values[canonical] = (row.get(column) or "").strip()
    return values


def _scan_genotype_evidence(
    path: Path | None,
    variant_ids: set[str],
    locus_keys: set[tuple[str, str, str]],
) -> tuple[
    dict[str, dict[str, str]],
    dict[tuple[str, str, str], list[dict[str, str]]],
    list[dict[str, Any]],
]:
    by_variant_id: dict[str, dict[str, str]] = {}
    by_locus: dict[
        tuple[str, str, str],
        list[dict[str, str]],
    ] = {}
    resolution_rows: list[dict[str, Any]] = []

    if path is None:
        return by_variant_id, by_locus, resolution_rows

    with path.open(
        "r",
        encoding="utf-8",
        errors="replace",
        newline="",
    ) as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        fieldnames = list(reader.fieldnames or [])
        column_map = _resolve_columns(
            fieldnames,
            GENOTYPE_HARDENING_ALIASES,
        )

        for canonical in GENOTYPE_HARDENING_ALIASES:
            resolution_rows.append({
                "canonical_field": canonical,
                "resolved_column": column_map.get(canonical, ""),
                "resolution_status": (
                    "RESOLVED"
                    if canonical in column_map
                    else "COLUMN_NOT_FOUND"
                ),
                "source_path": str(path),
            })

        variant_column = column_map.get("variant_id")

        for raw in reader:
            variant_id = (
                (raw.get(variant_column) or "").strip()
                if variant_column
                else ""
            )
            locus_key = _locus_key_from_row(raw, column_map)

            selected = (
                variant_id in variant_ids
                or (
                    locus_key is not None
                    and locus_key in locus_keys
                )
            )
            if not selected:
                continue

            canonical = _canonical_genotype_values(
                raw,
                column_map,
            )
            canonical["_source_row_variant_id"] = variant_id

            if variant_id and variant_id not in by_variant_id:
                by_variant_id[variant_id] = canonical

            if locus_key is not None:
                by_locus.setdefault(locus_key, []).append(canonical)

    return by_variant_id, by_locus, resolution_rows


def _presence_in_variant_table(
    path: Path | None,
    target_variant_ids: set[str],
) -> set[str]:
    found: set[str] = set()
    if path is None or not target_variant_ids:
        return found

    with path.open(
        "r",
        encoding="utf-8",
        errors="replace",
        newline="",
    ) as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        fieldnames = list(reader.fieldnames or [])
        resolved = _resolve_columns(
            fieldnames,
            {"variant_id": DOSSIER_FIELD_ALIASES["variant_id"]},
        )
        column = resolved.get("variant_id")
        if column is None:
            return found

        for raw in reader:
            variant_id = (raw.get(column) or "").strip()
            if variant_id in target_variant_ids:
                found.add(variant_id)
                if len(found) == len(target_variant_ids):
                    break

    return found


def _candidate_surface_path(
    root: Path,
    patterns: Sequence[str],
) -> Path | None:
    for pattern in patterns:
        direct = root / pattern
        if direct.is_file():
            return direct
        candidates = sorted(
            path
            for path in root.glob(pattern)
            if path.is_file()
        )
        if candidates:
            return candidates[0]
    return None


def _split_alt_set(alternate: str) -> set[str]:
    return {
        value.strip()
        for value in alternate.split(",")
        if value.strip()
    }


def _representation_relationship(
    historical_alt: str,
    current_alt: str,
) -> str:
    historical_set = _split_alt_set(historical_alt)
    current_set = _split_alt_set(current_alt)

    if not historical_set or not current_set:
        return "SAME_LOCUS_ALT_RELATIONSHIP_UNRESOLVED"

    if historical_set == current_set:
        return "SAME_LOCUS_SAME_ALT_SET"

    if historical_set.issubset(current_set) or current_set.issubset(historical_set):
        return "SAME_LOCUS_REPRESENTATION_COMPATIBLE"

    return "SAME_LOCUS_DIFFERENT_ALLELE_UNRESOLVED"


def _classify_delta_row(
    row: Mapping[str, Any],
    pairing_relationships: set[str],
    genotype_resolution: str,
) -> str:
    presence = str(row.get("presence", ""))
    alternate = str(row.get("alternate", ""))
    relationship = str(row.get("relationship_status", "")).lower()

    if "SAME_LOCUS_REPRESENTATION_COMPATIBLE" in pairing_relationships:
        return (
            "CURRENT_ONLY_REPRESENTATION_COMPATIBLE"
            if presence == "current_only"
            else "HISTORICAL_ONLY_REPRESENTATION_COMPATIBLE"
        )

    if "SAME_LOCUS_DIFFERENT_ALLELE_UNRESOLVED" in pairing_relationships:
        return (
            "CURRENT_ONLY_SAME_LOCUS_DIFFERENT_ALLELE_UNRESOLVED"
            if presence == "current_only"
            else "HISTORICAL_ONLY_SAME_LOCUS_DIFFERENT_ALLELE_UNRESOLVED"
        )

    complex_alt = "," in alternate or "*" in alternate
    complex_relationship = any(
        token in relationship
        for token in ("complex", "deferred", "multiallelic")
    )

    if presence == "current_only":
        if (
            complex_alt
            or complex_relationship
            or genotype_resolution.startswith("LOCUS_FALLBACK")
        ):
            return "CURRENT_ONLY_COMPLEX_MULTIALLELIC"
        if genotype_resolution == "EXACT_VARIANT_ID":
            return "CURRENT_ONLY_DIRECT_BIALLELIC"
        return "CURRENT_ONLY_UNEXPLAINED"

    return "HISTORICAL_ONLY_UNEXPLAINED"

def harden_variant_delta_dossier(
    current_root: Path,
    historical_root: Path,
    dossier_rows: Sequence[Mapping[str, Any]],
) -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    dict[str, Any],
    str,
]:
    hardened = [dict(row) for row in dossier_rows]

    variant_ids = {
        str(row.get("variant_id", "")).strip()
        for row in hardened
        if str(row.get("variant_id", "")).strip()
    }
    current_variant_ids = {
        str(row.get("variant_id", "")).strip()
        for row in hardened
        if row.get("presence") == "current_only"
        and str(row.get("variant_id", "")).strip()
    }

    locus_keys: set[tuple[str, str, str]] = set()
    for row in hardened:
        key = _locus_key_from_values(
            str(row.get("chromosome", "")),
            str(row.get("position", "")),
            str(row.get("reference", "")),
        )
        if key is not None:
            locus_keys.add(key)

    genotype_path = _find_genotype_observations(current_root)
    (
        genotype_by_id,
        genotype_by_locus,
        genotype_column_resolution,
    ) = _scan_genotype_evidence(
        genotype_path,
        current_variant_ids,
        locus_keys,
    )

    genotype_fields = (
        "genotype",
        "allele_depths",
        "depth",
        "genotype_quality",
        "phred_likelihoods",
        "filter_status",
        "gt_arity",
        "called_allele_indexes",
        "genotype_call_state",
        "phase_state",
        "relationship_status",
        "projection_status",
        "projection_advisory",
        "record_parse_status",
    )

    for row in hardened:
        if row.get("presence") != "current_only":
            row["genotype_resolution_status"] = (
                "HISTORICAL_GENOTYPE_UNAVAILABLE"
            )
            continue

        variant_id = str(row.get("variant_id", ""))
        exact = genotype_by_id.get(variant_id)
        selected: Mapping[str, str] | None = exact
        resolution_status = "EXACT_VARIANT_ID" if exact else ""

        if selected is None:
            locus_key = _locus_key_from_values(
                str(row.get("chromosome", "")),
                str(row.get("position", "")),
                str(row.get("reference", "")),
            )
            locus_candidates = (
                genotype_by_locus.get(locus_key, [])
                if locus_key is not None
                else []
            )
            if len(locus_candidates) == 1:
                selected = locus_candidates[0]
                resolution_status = "LOCUS_FALLBACK"
            elif len(locus_candidates) > 1:
                selected = locus_candidates[0]
                resolution_status = (
                    "LOCUS_FALLBACK_MULTIPLE_SOURCE_ROWS"
                )
                row["source_record_candidate_count"] = len(
                    locus_candidates
                )
            else:
                resolution_status = "SOURCE_ROW_NOT_FOUND"

        if selected is not None:
            for field in genotype_fields:
                value = str(selected.get(field, "")).strip()
                if value:
                    row[field] = value
            row["source_record_variant_id"] = str(
                selected.get("_source_row_variant_id", "")
            )
            row["source_record_alternate"] = str(
                selected.get("alternate", "")
            )

        row["genotype_resolution_status"] = resolution_status

        if resolution_status.startswith("LOCUS_FALLBACK"):
            existing = str(row.get("notes", ""))
            row["notes"] = (
                existing
                + "; exact allele identity unavailable; "
                + "source multiallelic record recovered by locus"
            ).strip("; ")

    # Pair historical/current identities at the same locus.
    historical_by_locus: dict[
        tuple[str, str, str],
        list[dict[str, Any]],
    ] = {}
    current_by_locus: dict[
        tuple[str, str, str],
        list[dict[str, Any]],
    ] = {}

    for row in hardened:
        locus_key = _locus_key_from_values(
            str(row.get("chromosome", "")),
            str(row.get("position", "")),
            str(row.get("reference", "")),
        )
        if locus_key is None:
            continue
        target = (
            historical_by_locus
            if row.get("presence") == "historical_only"
            else current_by_locus
        )
        target.setdefault(locus_key, []).append(row)

    pairing_rows: list[dict[str, Any]] = []
    paired_variant_ids: set[str] = set()

    for locus_key in sorted(
        set(historical_by_locus) & set(current_by_locus)
    ):
        historical_rows = historical_by_locus[locus_key]
        current_rows = current_by_locus[locus_key]
        for historical_row in historical_rows:
            for current_row in current_rows:
                historical_id = str(
                    historical_row.get("variant_id", "")
                    or historical_row.get("variant_key", "")
                )
                current_id = str(
                    current_row.get("variant_id", "")
                    or current_row.get("variant_key", "")
                )
                paired_variant_ids.update(
                    value
                    for value in (historical_id, current_id)
                    if value
                )
                historical_alt = str(
                    historical_row.get("alternate", "")
                )
                current_alt = str(
                    current_row.get("alternate", "")
                )
                pairing_rows.append({
                    "chromosome": locus_key[0],
                    "position": locus_key[1],
                    "reference": locus_key[2],
                    "historical_variant_id": historical_id,
                    "historical_alternate": historical_alt,
                    "current_variant_id": current_id,
                    "current_alternate": current_alt,
                    "relationship": _representation_relationship(
                        historical_alt,
                        current_alt,
                    ),
                    "current_genotype_resolution_status": (
                        current_row.get(
                            "genotype_resolution_status", ""
                        )
                    ),
                    "current_relationship_status": (
                        current_row.get("relationship_status", "")
                    ),
                })

    pairing_relationships_by_variant: dict[str, set[str]] = {}
    for pairing in pairing_rows:
        relationship = str(pairing.get("relationship", ""))
        for variant_identity in (
            str(pairing.get("historical_variant_id", "")),
            str(pairing.get("current_variant_id", "")),
        ):
            if variant_identity:
                pairing_relationships_by_variant.setdefault(
                    variant_identity,
                    set(),
                ).add(relationship)

    for row in hardened:
        variant_identity = str(
            row.get("variant_id", "")
            or row.get("variant_key", "")
        )
        relationships = pairing_relationships_by_variant.get(
            variant_identity,
            set(),
        )
        row["same_locus_pair_present"] = bool(relationships)
        row["same_locus_pair_relationships"] = sorted(relationships)
        row["delta_classification"] = _classify_delta_row(
            row,
            pairing_relationships=relationships,
            genotype_resolution=str(
                row.get("genotype_resolution_status", "")
            ),
        )

    # Earliest-divergence matrix across available row-level surfaces.
    surface_specs: list[
        tuple[str, str, Path | None, str]
    ] = [
        (
            "historical_stage08_selected_transcript",
            "historical",
            _candidate_surface_path(
                historical_root,
                (
                    "processed/stage_08_selected_transcript_consequences.tsv",
                    "**/stage_08_selected_transcript_consequences.tsv",
                ),
            ),
            "stage_08",
        ),
        (
            "historical_stage09_coding_interpreted",
            "historical",
            _candidate_surface_path(
                historical_root,
                (
                    "processed/stage_09_coding_interpreted.tsv",
                    "**/stage_09_coding_interpreted.tsv",
                ),
            ),
            "stage_09",
        ),
        (
            "current_stage07_annotated",
            "current",
            _candidate_surface_path(
                current_root,
                (
                    "processed/*annotated_variants.tsv",
                    "**/*annotated_variants.tsv",
                ),
            ),
            "stage_07",
        ),
        (
            "current_stage08_selected_transcript",
            "current",
            _candidate_surface_path(
                current_root,
                (
                    "processed/stage_08_selected_transcript_consequences.tsv",
                    "**/stage_08_selected_transcript_consequences.tsv",
                ),
            ),
            "stage_08",
        ),
        (
            "current_stage08_vdb_ready",
            "current",
            _candidate_surface_path(
                current_root,
                (
                    "processed/stage_08_vdb_ready_variants.tsv",
                    "**/stage_08_vdb_ready_variants.tsv",
                ),
            ),
            "stage_08",
        ),
        (
            "current_stage09_coding_interpreted",
            "current",
            _candidate_surface_path(
                current_root,
                (
                    "processed/stage_09_coding_interpreted.tsv",
                    "**/stage_09_coding_interpreted.tsv",
                ),
            ),
            "stage_09",
        ),
    ]

    presence_by_surface: dict[str, set[str]] = {}
    for surface_name, _, path, _ in surface_specs:
        presence_by_surface[surface_name] = (
            _presence_in_variant_table(path, variant_ids)
            if path is not None
            else set()
        )

    lineage_rows: list[dict[str, Any]] = []
    for row in hardened:
        variant_id = str(
            row.get("variant_id", "")
            or row.get("variant_key", "")
        )
        presence = str(row.get("presence", ""))
        matrix_row: dict[str, Any] = {
            "presence": presence,
            "variant_id": variant_id,
        }

        available_current_stages: list[str] = []
        available_historical_stages: list[str] = []

        for surface_name, source_kind, path, stage in surface_specs:
            if path is None:
                status = HISTORICAL_UNAVAILABLE if (
                    source_kind == "historical"
                ) else "CURRENT_ARTIFACT_UNAVAILABLE"
            else:
                status = (
                    "PRESENT"
                    if variant_id in presence_by_surface[surface_name]
                    else "ABSENT"
                )
                if status == "PRESENT":
                    (
                        available_historical_stages
                        if source_kind == "historical"
                        else available_current_stages
                    ).append(stage)

            matrix_row[surface_name] = status
            matrix_row[f"{surface_name}_path"] = (
                str(
                    path.relative_to(
                        historical_root
                        if source_kind == "historical"
                        else current_root
                    )
                )
                if path is not None
                else ""
            )

        if presence == "current_only":
            earliest_current = (
                sorted(set(available_current_stages))[0]
                if available_current_stages
                else ""
            )
            matrix_row["earliest_defensible_divergence_boundary"] = (
                f"present_by_{earliest_current}"
                if earliest_current
                else "current_row_level_origin_unresolved"
            )
        else:
            latest_historical = (
                sorted(set(available_historical_stages))[-1]
                if available_historical_stages
                else ""
            )
            matrix_row["earliest_defensible_divergence_boundary"] = (
                f"historically_present_through_{latest_historical}"
                if latest_historical
                else "historical_row_level_origin_unresolved"
            )

        lineage_rows.append(matrix_row)

    classification_counter = Counter(
        str(row.get("delta_classification", ""))
        for row in hardened
    )
    resolution_counter = Counter(
        str(row.get("genotype_resolution_status", ""))
        for row in hardened
        if row.get("presence") == "current_only"
    )

    current_only_count = sum(
        row.get("presence") == "current_only"
        for row in hardened
    )
    historical_only_count = sum(
        row.get("presence") == "historical_only"
        for row in hardened
    )
    direct_count = resolution_counter.get(
        "EXACT_VARIANT_ID", 0
    )
    locus_recovered_count = sum(
        count
        for status, count in resolution_counter.items()
        if status.startswith("LOCUS_FALLBACK")
    )
    unresolved_count = resolution_counter.get(
        "SOURCE_ROW_NOT_FOUND", 0
    )

    closure_status = (
        "PASS_WITH_BOUNDED_LIMITATIONS"
        if unresolved_count == 0
        else "UNDER_REVIEW"
    )

    pairing_relationship_counter = Counter(
        str(row.get("relationship", ""))
        for row in pairing_rows
    )

    current_complex_mediation_count = sum(
        1
        for row in hardened
        if row.get("presence") == "current_only"
        and (
            "COMPLEX_MULTIALLELIC"
            in str(row.get("delta_classification", ""))
            or str(
                row.get("genotype_resolution_status", "")
            ).startswith("LOCUS_FALLBACK")
        )
    )

    source_record_context_coverage_fraction = (
        (direct_count + locus_recovered_count)
        / current_only_count
        if current_only_count
        else 1.0
    )

    closure_summary: dict[str, Any] = {
        "schema_version": "genotype_elevation_closure_summary_v2",
        "script_version": VERSION,
        "closure_status": closure_status,
        "shared_coding_interpretation_invariance": {
            "status": "pass",
            "basis": (
                "v0.3 keyed comparison reported zero shared-row "
                "scientific-field differences"
            ),
        },
        "coding_identity_delta": {
            "historical_only_count": historical_only_count,
            "current_only_count": current_only_count,
            "net_current_minus_historical": (
                current_only_count - historical_only_count
            ),
            "localized": True,
        },
        "genotype_enrichment": {
            "current_only_count": current_only_count,
            "exact_variant_id_count": direct_count,
            "locus_fallback_count": locus_recovered_count,
            "unresolved_count": unresolved_count,
            "source_record_context_coverage_fraction": (
                source_record_context_coverage_fraction
            ),
            "allele_specific_relationship_resolution": {
                "direct_exact_count": direct_count,
                "source_record_context_only_count": locus_recovered_count,
                "unresolved_count": unresolved_count,
            },
            "source_path": (
                str(genotype_path.relative_to(current_root))
                if genotype_path is not None
                else None
            ),
        },
        "delta_classification_counts": dict(
            sorted(classification_counter.items())
        ),
        "same_locus_comparison": {
            "pair_count": len(pairing_rows),
            "relationship_counts": dict(
                sorted(pairing_relationship_counter.items())
            ),
        },
        "historical_noncoding_identity_evidence": {
            "status": "unavailable",
            "classification": HISTORICAL_UNAVAILABLE,
            "reason": (
                "historical lightweight extraction does not retain "
                "stage_10_noncoding_interpreted.tsv"
            ),
        },
        "vdb_handoff_readiness": {
            "status": (
                "ready_for_scientific_review"
                if closure_status
                in {"PASS", "PASS_WITH_BOUNDED_LIMITATIONS"}
                else "awaiting_adjustment"
            ),
            "current_direct_relationships_transportable": direct_count,
            "current_complex_source_records_recovered": (
                locus_recovered_count
            ),
            "current_relationships_requiring_vdb_mediation": (
                current_complex_mediation_count
            ),
            "historical_comparison_only_pair_count": len(pairing_rows),
            "same_locus_different_allele_unresolved_pair_count": (
                pairing_relationship_counter.get(
                    "SAME_LOCUS_DIFFERENT_ALLELE_UNRESOLVED",
                    0,
                )
            ),
        },
    }

    closure_lines = [
        "# Genotype Elevation Closure Summary",
        "",
        f"- Script version: `{VERSION}`",
        f"- Closure status: `{closure_status}`",
        f"- Historical-only coding identities: `{historical_only_count}`",
        f"- Current-only coding identities: `{current_only_count}`",
        f"- Exact genotype joins: `{direct_count}`",
        f"- Source-record locus recoveries: `{locus_recovered_count}`",
        f"- Unresolved current genotype relationships: `{unresolved_count}`",
        f"- Source-record context coverage: `{source_record_context_coverage_fraction:.6f}`",
        f"- Same-locus comparison pairs: `{len(pairing_rows)}`",
        f"- Current relationships requiring VDB mediation: `{current_complex_mediation_count}`",
        "",
        "## Certification Boundary",
        "",
        "Shared coding interpretation is invariant across all directly comparable shared variant identities. The coding identity delta is fully enumerated. Current-only genotype evidence is joined by exact variant identity where possible and recovered at source-record locus level for complex records. Locus recovery establishes preserved source-record context, not automatic allele-specific equivalence.",
        "",
        "Historical noncoding identity-level closure is not possible from the retained lightweight extraction and remains an explicit evidence limitation rather than a failed validation.",
        "",
        "## Delta Classifications",
        "",
        "| Classification | Count |",
        "|---|---:|",
    ]
    for classification, count in sorted(
        classification_counter.items()
    ):
        closure_lines.append(
            f"| {classification} | {count} |"
        )

    closure_lines.extend([
        "",
        "## VDB Relevance",
        "",
        "Direct biallelic relationships are transportable without inference. Representation-compatible same-locus ALT sets and complex multiallelic source records retain genotype context and remain appropriate targets for VDB identity mediation. Same-locus different-allele pairs remain unresolved comparison evidence and are not counted as modern VDB mediation obligations.",
        "",
    ])

    return (
        hardened,
        genotype_column_resolution,
        pairing_rows,
        lineage_rows,
        closure_summary,
        "\n".join(closure_lines),
    )



def _safe_nested_mapping(
    value: Any,
    *keys: str,
) -> Mapping[str, Any]:
    current = value
    for key in keys:
        if not isinstance(current, Mapping):
            return {}
        current = current.get(key)
    return current if isinstance(current, Mapping) else {}


def _current_case_study_surfaces(
    current_root: Path,
) -> dict[str, list[dict[str, str]]]:
    """Derive only surfaces with equivalent certified-table semantics."""
    derived: dict[str, list[dict[str, str]]] = {}

    def summary(stage: int) -> Mapping[str, Any]:
        filename = (
            f"stage_{stage:02d}_summary.json"
            if stage < 13
            else "stage_13_final_summary.json"
        )
        path = _candidate_surface_path(
            current_root,
            (
                f"processed/{filename}",
                f"metadata/stage_summaries/{filename}",
            ),
        )
        data = load_json(path) if path is not None else {}
        return data if isinstance(data, Mapping) else {}

    stage08 = summary(8)
    stage09 = summary(9)
    stage10 = summary(10)
    stage11 = summary(11)
    stage12 = summary(12)

    priority = stage11.get("counts_by_priority_tier")
    if isinstance(priority, Mapping):
        derived["priority_tier_summary.tsv"] = [
            {
                "priority_tier": str(key),
                "count": str(value),
            }
            for key, value in sorted(priority.items())
        ]

    readiness: list[dict[str, str]] = []
    for metric, source_key in (
        ("validation_required", "counts_by_validation_required"),
        ("validation_priority", "counts_by_validation_priority"),
        (
            "suggested_validation_method",
            "counts_by_suggested_validation_method",
        ),
    ):
        values = stage12.get(source_key)
        if isinstance(values, Mapping):
            readiness.extend(
                {
                    "metric": metric,
                    "category": str(category),
                    "count": str(count_value),
                }
                for category, count_value in sorted(values.items())
            )
    if readiness:
        derived["candidate_reviewability_readiness.tsv"] = readiness

    funnel = {
        "raw_variant_count": "",
        "normalized_variant_count": "",
        "annotated_variant_count": "",
        "stage08_total_variants": str(stage08.get("total_variants", "")),
        "coding_candidates": "",
        "noncoding_candidates": "",
        "splice_region_candidates": "",
        "qc_flagged": "",
        "stage09_coding_interpreted": str(
            stage09.get("output_rows", stage09.get("input_rows", ""))
        ),
        "stage10_noncoding_interpreted": str(
            stage10.get("output_rows", stage10.get("input_rows", ""))
        ),
        "stage11_prioritized_rows": str(
            stage11.get("output_rows", stage11.get("input_rows", ""))
        ),
        "stage12_validation_rows": str(
            stage12.get("output_rows", stage12.get("input_rows", ""))
        ),
        "rdgp_gene_evidence_seed_rows": "",
        "unique_gene_ids": "",
    }
    partition = stage08.get("partition_counts")
    if isinstance(partition, Mapping):
        funnel["coding_candidates"] = str(
            partition.get("coding_candidates", "")
        )
        funnel["noncoding_candidates"] = str(
            partition.get("noncoding_candidates", "")
        )
        funnel["splice_region_candidates"] = str(
            partition.get("splice_region_candidates", "")
        )
        funnel["qc_flagged"] = str(
            partition.get("qc_flagged", partition.get("unknown_candidates", ""))
        )
    derived["stage_funnel_summary.tsv"] = [funnel]

    runtime_path = current_root / "metadata" / "runtime_profile.tsv"
    if runtime_path.is_file():
        runtime_header, runtime_rows = parse_tsv(runtime_path)
        if runtime_rows:
            derived["runtime_stage_summary.tsv"] = [
                {
                    "stage": str(row.get("stage", "")),
                    "elapsed_seconds": str(row.get("elapsed_seconds", "")),
                    "status": str(row.get("status", "")),
                }
                for row in runtime_rows
            ]

    gene_counts_path = (
        current_root / "processed" / "stage_11_gene_variant_counts.tsv"
    )
    if gene_counts_path.is_file():
        _, gene_rows = parse_tsv(gene_counts_path)
        if gene_rows:
            derived["gene_burden_summary.tsv"] = [
                {
                    "gene_id": str(row.get("gene_id", "")),
                    "variant_count": str(row.get("variant_count", "")),
                }
                for row in gene_rows
                if str(row.get("gene_id", ""))
            ]

    # These surfaces do not have enough equivalent dimensions in current
    # stage summaries to support certification-grade comparisons.
    return derived


CASE_STUDY_ADAPTERS: dict[str, dict[str, Any]] = {
    "candidate_reviewability_readiness.tsv": {
        "key_columns": ("metric", "category"),
        "value_columns": ("count",),
    },
    "priority_tier_summary.tsv": {
        "key_columns": ("priority_tier",),
        "value_columns": ("count",),
    },
    "stage_funnel_summary.tsv": {
        "wide_value_columns": (
            "raw_variant_count",
            "normalized_variant_count",
            "annotated_variant_count",
            "stage08_total_variants",
            "coding_candidates",
            "noncoding_candidates",
            "splice_region_candidates",
            "qc_flagged",
            "stage09_coding_interpreted",
            "stage10_noncoding_interpreted",
            "stage11_prioritized_rows",
            "stage12_validation_rows",
            "rdgp_gene_evidence_seed_rows",
            "unique_gene_ids",
        ),
    },
    "runtime_stage_summary.tsv": {
        "key_columns": ("stage",),
        "value_columns": ("elapsed_seconds", "status"),
    },
    "gene_burden_summary.tsv": {
        "key_columns": ("gene_id",),
        "value_columns": ("variant_count",),
    },
}


def _group_rows_by_run(
    rows: Sequence[Mapping[str, str]],
) -> dict[str, list[dict[str, str]]]:
    grouped: dict[str, list[dict[str, str]]] = {}
    for row in rows:
        run_id = str(row.get("run_id", "")).strip() or "<UNSCOPED>"
        grouped.setdefault(run_id, []).append(dict(row))
    return grouped


def _numeric_or_text(value: str) -> float | str:
    parsed = _parse_float(value)
    return parsed if parsed is not None else value.strip()


def _compare_adapter_rows(
    filename: str,
    historical_run_id: str,
    historical_rows: Sequence[Mapping[str, str]],
    current_rows: Sequence[Mapping[str, str]],
    adapter: Mapping[str, Any],
    historical_source: str,
) -> list[dict[str, Any]]:
    comparisons: list[dict[str, Any]] = []

    wide_columns = tuple(adapter.get("wide_value_columns", ()))
    if wide_columns:
        historical_row = historical_rows[0] if historical_rows else {}
        current_row = current_rows[0] if current_rows else {}
        for column in wide_columns:
            historical_raw = str(historical_row.get(column, "")).strip()
            current_raw = str(current_row.get(column, "")).strip()
            if not historical_raw or not current_raw:
                comparisons.append({
                    "surface": filename,
                    "historical_run_id": historical_run_id,
                    "historical_source": historical_source,
                    "current_source": "derived_current_surface",
                    "metric": column,
                    "historical_value": historical_raw,
                    "current_value": current_raw,
                    "delta": "",
                    "classification": NOT_COMPARABLE,
                    "notes": "metric unavailable on one side",
                })
                continue
            historical_value = _numeric_or_text(historical_raw)
            current_value = _numeric_or_text(current_raw)
            if isinstance(historical_value, float) and isinstance(current_value, float):
                delta: float | str = current_value - historical_value
                classification = (
                    MATCH
                    if math.isclose(
                        historical_value,
                        current_value,
                        abs_tol=1e-12,
                        rel_tol=1e-9,
                    )
                    else UNDER_REVIEW
                )
            else:
                delta = ""
                classification = (
                    MATCH
                    if historical_value == current_value
                    else UNDER_REVIEW
                )
            comparisons.append({
                "surface": filename,
                "historical_run_id": historical_run_id,
                "historical_source": historical_source,
                "current_source": "derived_current_surface",
                "metric": column,
                "historical_value": historical_value,
                "current_value": current_value,
                "delta": delta,
                "classification": classification,
                "notes": "per-run wide-surface comparison",
            })
        return comparisons

    key_columns = tuple(adapter.get("key_columns", ()))
    value_columns = tuple(adapter.get("value_columns", ()))
    if not key_columns or not value_columns:
        return comparisons

    def keyed(
        rows: Sequence[Mapping[str, str]],
    ) -> dict[tuple[str, ...], Mapping[str, str]]:
        result: dict[tuple[str, ...], Mapping[str, str]] = {}
        for row in rows:
            key = tuple(str(row.get(column, "")).strip() for column in key_columns)
            if all(key):
                result[key] = row
        return result

    historical_map = keyed(historical_rows)
    current_map = keyed(current_rows)

    for key in sorted(set(historical_map) | set(current_map)):
        historical_row = historical_map.get(key)
        current_row = current_map.get(key)
        metric_key = "|".join(key)

        if historical_row is None or current_row is None:
            comparisons.append({
                "surface": filename,
                "historical_run_id": historical_run_id,
                "historical_source": historical_source,
                "current_source": "derived_current_surface",
                "metric": metric_key,
                "historical_value": (
                    dict(historical_row) if historical_row else ""
                ),
                "current_value": dict(current_row) if current_row else "",
                "delta": "",
                "classification": NOT_COMPARABLE,
                "notes": "composite metric absent from one side",
            })
            continue

        for value_column in value_columns:
            historical_raw = str(
                historical_row.get(value_column, "")
            ).strip()
            current_raw = str(current_row.get(value_column, "")).strip()
            metric = f"{metric_key}|{value_column}"

            if not historical_raw or not current_raw:
                classification = NOT_COMPARABLE
                delta = ""
                notes = "value unavailable on one side"
                historical_value: Any = historical_raw
                current_value: Any = current_raw
            else:
                historical_value = _numeric_or_text(historical_raw)
                current_value = _numeric_or_text(current_raw)
                if (
                    isinstance(historical_value, float)
                    and isinstance(current_value, float)
                ):
                    delta = current_value - historical_value
                    classification = (
                        MATCH
                        if math.isclose(
                            historical_value,
                            current_value,
                            abs_tol=1e-12,
                            rel_tol=1e-9,
                        )
                        else UNDER_REVIEW
                    )
                else:
                    delta = ""
                    classification = (
                        MATCH
                        if historical_value == current_value
                        else UNDER_REVIEW
                    )
                notes = "per-run composite-key comparison"

            comparisons.append({
                "surface": filename,
                "historical_run_id": historical_run_id,
                "historical_source": historical_source,
                "current_source": "derived_current_surface",
                "metric": metric,
                "historical_value": historical_value,
                "current_value": current_value,
                "delta": delta,
                "classification": classification,
                "notes": notes,
            })

    return comparisons


def compare_certified_case_study_surfaces(
    current_root: Path,
    case_study_root: Path | None,
) -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    dict[str, Any],
]:
    """Compare certified surfaces per historical run using explicit adapters."""
    if case_study_root is None:
        return [], [], {
            "status": "not_provided",
            "comparable_surface_count": 0,
        }

    derived = _current_case_study_surfaces(current_root)
    comparisons: list[dict[str, Any]] = []
    derivations: list[dict[str, Any]] = []

    for filename in CASE_TABLES:
        certified_path = find_name(case_study_root, filename)
        current_rows = derived.get(filename)
        adapter = CASE_STUDY_ADAPTERS.get(filename)

        if certified_path is None:
            comparisons.append({
                "surface": filename,
                "historical_run_id": "",
                "historical_source": "",
                "current_source": "",
                "metric": "artifact_availability",
                "historical_value": "",
                "current_value": "",
                "delta": "",
                "classification": HISTORICAL_UNAVAILABLE,
                "notes": "certified case-study table unavailable",
            })
            continue

        historical_header, historical_rows = parse_tsv(certified_path)
        historical_runs = _group_rows_by_run(historical_rows)

        if current_rows is None or adapter is None:
            comparisons.append({
                "surface": filename,
                "historical_run_id": "",
                "historical_source": str(
                    certified_path.relative_to(case_study_root)
                ),
                "current_source": "",
                "metric": "surface_derivation",
                "historical_value": historical_header,
                "current_value": "",
                "delta": "",
                "classification": NOT_COMPARABLE,
                "notes": (
                    "no certification-grade current adapter; "
                    "surface retained as explicitly not comparable"
                ),
            })
            derivations.append({
                "surface": filename,
                "historical_source": str(
                    certified_path.relative_to(case_study_root)
                ),
                "historical_run_count": len(historical_runs),
                "historical_row_count": len(historical_rows),
                "current_derived_row_count": (
                    len(current_rows) if current_rows else 0
                ),
                "adapter_status": "NOT_IMPLEMENTED",
                "adapter_key_columns": "",
                "adapter_value_columns": "",
            })
            continue

        derivations.append({
            "surface": filename,
            "historical_source": str(
                certified_path.relative_to(case_study_root)
            ),
            "historical_run_count": len(historical_runs),
            "historical_row_count": len(historical_rows),
            "current_derived_row_count": len(current_rows),
            "adapter_status": "IMPLEMENTED",
            "adapter_key_columns": adapter.get("key_columns", ()),
            "adapter_value_columns": (
                adapter.get("value_columns", ())
                or adapter.get("wide_value_columns", ())
            ),
        })

        for historical_run_id, run_rows in sorted(
            historical_runs.items()
        ):
            comparisons.extend(
                _compare_adapter_rows(
                    filename,
                    historical_run_id,
                    run_rows,
                    current_rows,
                    adapter,
                    str(certified_path.relative_to(case_study_root)),
                )
            )

    counts_by_class = counts(comparisons)
    comparable_records = [
        row
        for row in comparisons
        if row.get("classification") in {MATCH, UNDER_REVIEW}
    ]
    summary = {
        "status": "complete",
        "surface_count": len(CASE_TABLES),
        "implemented_adapter_count": sum(
            row.get("adapter_status") == "IMPLEMENTED"
            for row in derivations
        ),
        "not_comparable_surface_count": sum(
            row.get("classification") == NOT_COMPARABLE
            and row.get("metric") == "surface_derivation"
            for row in comparisons
        ),
        "comparable_record_count": len(comparable_records),
        "classification_counts": counts_by_class,
        "comparison_policy": (
            "each certified historical run is compared independently; "
            "independent runs are never aggregated"
        ),
    }
    return comparisons, derivations, summary


def _first_recursive_value(
    value: Any,
    keys: set[str],
) -> str:
    if isinstance(value, Mapping):
        for key, child in value.items():
            if str(key) in keys and isinstance(child, (str, int, float)):
                return str(child)
        for child in value.values():
            found = _first_recursive_value(child, keys)
            if found:
                return found
    elif isinstance(value, list):
        for child in value:
            found = _first_recursive_value(child, keys)
            if found:
                return found
    return ""


def _iter_transport_artifacts(
    value: Any,
    context: Mapping[str, str] | None = None,
) -> Iterable[dict[str, str]]:
    inherited = dict(context or {})

    if isinstance(value, Mapping):
        local = dict(inherited)
        for canonical, candidate_keys in {
            "entity_id": ("entity_id", "id"),
            "entity_role": ("entity_role", "role"),
            "source_artifact_role": (
                "source_artifact_role",
                "artifact_role",
                "role",
            ),
        }.items():
            for key in candidate_keys:
                child = value.get(key)
                if isinstance(child, str) and child:
                    local[canonical] = child
                    break

        transport_path = ""
        for key in (
            "transport_path",
            "package_path",
            "relative_path",
            "artifact_path",
        ):
            child = value.get(key)
            if isinstance(child, str) and child:
                transport_path = child
                break

        declared_sha = ""
        for key in (
            "sha256",
            "artifact_sha256",
            "checksum_sha256",
            "transport_sha256",
        ):
            child = value.get(key)
            if isinstance(child, str) and child:
                declared_sha = child
                break

        if transport_path and (
            declared_sha
            or Path(transport_path).suffix.lower()
            in {".tsv", ".json", ".yaml", ".yml", ".md", ".vcf", ".gz"}
        ):
            yield {
                **local,
                "transport_path": transport_path,
                "declared_sha256": declared_sha,
            }

        for child in value.values():
            yield from _iter_transport_artifacts(child, local)

    elif isinstance(value, list):
        for child in value:
            yield from _iter_transport_artifacts(child, inherited)


def _resolve_transport_path(
    tep_root: Path,
    transport_path: str,
) -> Path:
    candidate = Path(transport_path)
    if candidate.is_absolute():
        return candidate

    direct = tep_root / candidate
    if direct.exists():
        return direct

    # Some manifests store the package directory as the first component.
    if candidate.parts and candidate.parts[0] == tep_root.name:
        nested = tep_root.parent / candidate
        if nested.exists():
            return nested

    return direct


def build_tep_input_integrity(
    current_root: Path,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    tep_dirs = (
        sorted(
            path
            for path in (current_root / "tep").glob("vap_tep_*")
            if path.is_dir()
        )
        if (current_root / "tep").is_dir()
        else []
    )

    if not tep_dirs:
        return [], {
            "status": "fail",
            "reason": "native TEP-VAP package unavailable",
        }

    tep_root = tep_dirs[0]
    inventory_path = tep_root / "entity_inventory.json"
    validation_path = tep_root / "validation_report.md"
    lineage_path = tep_root / "lineage_manifest.json"

    if not inventory_path.is_file():
        return [], {
            "status": "fail",
            "reason": "TEP entity inventory unavailable",
            "tep_root": str(tep_root),
        }

    data = load_json(inventory_path)
    tep_id = _first_recursive_value(
        data,
        {"tep_id", "package_id", "transport_id"},
    ) or tep_root.name

    deduplicated: dict[tuple[str, str, str], dict[str, str]] = {}
    for record in _iter_transport_artifacts(data):
        key = (
            record.get("entity_id", ""),
            record.get("source_artifact_role", ""),
            record.get("transport_path", ""),
        )
        deduplicated[key] = record

    rows: list[dict[str, Any]] = []
    for record in sorted(
        deduplicated.values(),
        key=lambda row: (
            row.get("entity_id", ""),
            row.get("transport_path", ""),
        ),
    ):
        transport_path = record.get("transport_path", "")
        artifact_path = _resolve_transport_path(
            tep_root,
            transport_path,
        )
        exists = artifact_path.is_file()
        declared_sha = record.get("declared_sha256", "")
        observed_sha = sha256(artifact_path) if exists else ""

        if not exists:
            checksum_status = "ARTIFACT_MISSING"
        elif declared_sha:
            checksum_status = (
                "MATCH"
                if declared_sha == observed_sha
                else "CHECKSUM_MISMATCH"
            )
        else:
            checksum_status = "MISSING_DECLARED_SHA256"

        rows.append({
            "tep_id": tep_id,
            "entity_id": record.get("entity_id", ""),
            "entity_role": record.get("entity_role", ""),
            "source_artifact_role": record.get(
                "source_artifact_role", ""
            ),
            "transport_path": transport_path,
            "exists": exists,
            "size_bytes": (
                artifact_path.stat().st_size if exists else ""
            ),
            "declared_sha256": declared_sha,
            "observed_sha256": observed_sha,
            "checksum_status": checksum_status,
        })

    validation_pass = False
    if validation_path.is_file():
        validation_text = validation_path.read_text(
            encoding="utf-8",
            errors="replace",
        )
        validation_pass = (
            "Validation status: `pass`" in validation_text
            or "overall_status: PASS" in validation_text
            or "validation_status: pass" in validation_text.casefold()
        )

    failure_statuses = {
        "ARTIFACT_MISSING",
        "CHECKSUM_MISMATCH",
    }
    status = (
        "pass"
        if rows
        and not any(
            row["checksum_status"] in failure_statuses
            for row in rows
        )
        and validation_path.is_file()
        and lineage_path.is_file()
        and validation_pass
        else "fail"
    )

    summary = {
        "status": status,
        "tep_root": str(tep_root),
        "tep_id": tep_id,
        "entity_inventory_path": str(
            inventory_path.relative_to(current_root)
        ),
        "lineage_manifest_path": (
            str(lineage_path.relative_to(current_root))
            if lineage_path.is_file()
            else None
        ),
        "validation_report_path": (
            str(validation_path.relative_to(current_root))
            if validation_path.is_file()
            else None
        ),
        "validation_report_pass": validation_pass,
        "artifact_record_count": len(rows),
        "checksum_match_count": sum(
            row["checksum_status"] == "MATCH"
            for row in rows
        ),
        "missing_declared_sha256_count": sum(
            row["checksum_status"] == "MISSING_DECLARED_SHA256"
            for row in rows
        ),
        "checksum_failure_count": sum(
            row["checksum_status"] in failure_statuses
            for row in rows
        ),
        "inventory_traversal_policy": (
            "recursive transport-path and sha256 discovery"
        ),
    }
    return rows, summary


EXPLICIT_MISSING_SENTINELS = {
    ".",
    "na",
    "n/a",
    "none",
    "null",
    "missing",
    "not_provided",
    "not provided",
    "unavailable",
}

EXPLICIT_NOT_APPLICABLE_SENTINELS = {
    "not_applicable",
    "not applicable",
    "not-applicable",
}


def _missingness_state(value: str) -> str:
    stripped = value.strip()
    if stripped == "":
        return "EMPTY"

    lowered = stripped.casefold()
    if lowered in EXPLICIT_NOT_APPLICABLE_SENTINELS:
        return "EXPLICIT_NOT_APPLICABLE"

    if lowered in EXPLICIT_MISSING_SENTINELS:
        return "EXPLICIT_MISSING"

    return "SEMANTIC_VALUE"


def build_genotype_schema_inventory(
    current_root: Path,
) -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    dict[str, Any],
]:
    path = _find_genotype_observations(current_root)
    if path is None:
        return [], [], {
            "status": "fail",
            "reason": "genotype observations unavailable",
        }

    exemplars: list[dict[str, str]] = []
    lexical_nonempty: Counter[str] = Counter()
    semantic_values: Counter[str] = Counter()
    explicit_missing: Counter[str] = Counter()
    explicit_not_applicable: Counter[str] = Counter()
    empty_values: Counter[str] = Counter()
    scanned_rows = 0

    with path.open(
        "r",
        encoding="utf-8",
        errors="replace",
        newline="",
    ) as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        fieldnames = list(reader.fieldnames or [])

        for row in reader:
            scanned_rows += 1
            normalized_row = {
                str(key): str(value or "")
                for key, value in row.items()
                if key is not None
            }

            if len(exemplars) < 5:
                exemplars.append(normalized_row)

            for column, value in normalized_row.items():
                state = _missingness_state(value)

                if value.strip():
                    lexical_nonempty[column] += 1

                if state == "SEMANTIC_VALUE":
                    semantic_values[column] += 1
                elif state == "EXPLICIT_MISSING":
                    explicit_missing[column] += 1
                elif state == "EXPLICIT_NOT_APPLICABLE":
                    explicit_not_applicable[column] += 1
                else:
                    empty_values[column] += 1

    resolved = _resolve_columns(
        fieldnames,
        GENOTYPE_HARDENING_ALIASES,
    )

    schema_rows = [
        {
            "column_index": index,
            "column_name": column,
            "normalized_column_name": _normalized_column_name(column),
            "canonical_mappings": sorted(
                canonical
                for canonical, resolved_column in resolved.items()
                if resolved_column == column
            ),
            "lexically_nonempty_count": lexical_nonempty.get(column, 0),
            "semantic_value_count": semantic_values.get(column, 0),
            "explicit_missing_count": explicit_missing.get(column, 0),
            "explicit_not_applicable_count": (
                explicit_not_applicable.get(column, 0)
            ),
            "empty_count": empty_values.get(column, 0),
            "scanned_row_count": scanned_rows,
        }
        for index, column in enumerate(fieldnames, start=1)
    ]

    projection_summary_path = _candidate_surface_path(
        current_root,
        (
            "processed/genotype_projection_summary.json",
            "tep/*/entities/genotype/genotype_projection_summary.json",
        ),
    )
    projection = (
        load_json(projection_summary_path)
        if projection_summary_path is not None
        else {}
    )
    projection_counts = (
        projection.get("counts", {})
        if isinstance(projection, Mapping)
        else {}
    )

    expected_presence = {
        "allele_depths": int(
            projection_counts.get("ad_present_count", 0) or 0
        ),
        "depth": int(
            projection_counts.get("dp_present_count", 0) or 0
        ),
        "genotype_quality": int(
            projection_counts.get("gq_present_count", 0) or 0
        ),
        "phred_likelihoods": int(
            projection_counts.get("pl_present_count", 0) or 0
        ),
        "filter_status": int(
            projection_counts.get("ft_present_count", 0) or 0
        ),
    }

    resolution_rows: list[dict[str, Any]] = []
    for canonical in GENOTYPE_HARDENING_ALIASES:
        resolved_column = resolved.get(canonical, "")
        lexical_count = (
            lexical_nonempty.get(resolved_column, 0)
            if resolved_column
            else 0
        )
        semantic_count = (
            semantic_values.get(resolved_column, 0)
            if resolved_column
            else 0
        )
        missing_count = (
            explicit_missing.get(resolved_column, 0)
            if resolved_column
            else 0
        )
        not_applicable_count = (
            explicit_not_applicable.get(resolved_column, 0)
            if resolved_column
            else 0
        )
        empty_count = (
            empty_values.get(resolved_column, 0)
            if resolved_column
            else 0
        )
        expected_count = expected_presence.get(canonical)

        if resolved_column and semantic_count > 0:
            status = "RESOLVED_SEMANTIC_VALUES_PRESENT"
        elif (
            resolved_column
            and expected_count == 0
            and missing_count > 0
        ):
            status = (
                "COLUMN_PRESENT_EXPLICIT_MISSING_EXPECTED"
            )
        elif (
            resolved_column
            and expected_count == 0
            and not_applicable_count > 0
        ):
            status = (
                "COLUMN_PRESENT_NOT_APPLICABLE_EXPECTED"
            )
        elif resolved_column and expected_count == 0:
            status = (
                "COLUMN_PRESENT_NO_SEMANTIC_VALUES_EXPECTED"
            )
        elif resolved_column and expected_count and expected_count > 0:
            status = (
                "COLUMN_PRESENT_SEMANTIC_VALUES_MISSING_UNEXPECTED"
            )
        elif resolved_column:
            status = "COLUMN_PRESENT_NO_SEMANTIC_VALUES"
        elif expected_count and expected_count > 0:
            status = "SUMMARY_PRESENT_BUT_COLUMN_UNRESOLVED"
        elif expected_count == 0 and canonical in expected_presence:
            status = "EXPECTED_ABSENT_NO_CANONICAL_COLUMN"
        else:
            status = "COLUMN_NOT_FOUND"

        resolution_rows.append({
            "canonical_field": canonical,
            "resolved_column": resolved_column,
            "resolution_status": status,
            "observed_lexically_nonempty_count": lexical_count,
            "observed_semantic_value_count": semantic_count,
            "observed_explicit_missing_count": missing_count,
            "observed_explicit_not_applicable_count": (
                not_applicable_count
            ),
            "observed_empty_count": empty_count,
            "scanned_row_count": scanned_rows,
            "projection_summary_present_count": (
                expected_count if expected_count is not None else ""
            ),
        })

    blocking_statuses = {
        "SUMMARY_PRESENT_BUT_COLUMN_UNRESOLVED",
        "COLUMN_PRESENT_SEMANTIC_VALUES_MISSING_UNEXPECTED",
    }
    blocking = [
        row
        for row in resolution_rows
        if row["resolution_status"] in blocking_statuses
    ]
    status = "pass" if not blocking else "under_review"

    summary = {
        "status": status,
        "path": str(path.relative_to(current_root)),
        "column_count": len(fieldnames),
        "row_count": scanned_rows,
        "resolved_canonical_field_count": len(resolved),
        "unresolved_summary_present_fields": [
            row["canonical_field"] for row in blocking
        ],
        "expected_absent_fields": [
            row["canonical_field"]
            for row in resolution_rows
            if row["resolution_status"] in {
                "COLUMN_PRESENT_EXPLICIT_MISSING_EXPECTED",
                "COLUMN_PRESENT_NOT_APPLICABLE_EXPECTED",
                "COLUMN_PRESENT_NO_SEMANTIC_VALUES_EXPECTED",
                "EXPECTED_ABSENT_NO_CANONICAL_COLUMN",
            }
        ],
        "missingness_policy": {
            "states": [
                "EMPTY",
                "EXPLICIT_MISSING",
                "EXPLICIT_NOT_APPLICABLE",
                "SEMANTIC_VALUE",
            ],
            "explicit_missing_sentinels": sorted(
                EXPLICIT_MISSING_SENTINELS
            ),
            "explicit_not_applicable_sentinels": sorted(
                EXPLICIT_NOT_APPLICABLE_SENTINELS
            ),
            "unknown_is_treated_as_semantic_state": True,
            "lexical_nonempty_does_not_imply_semantic_presence": True,
        },
        "column_presence_is_distinct_from_semantic_value_presence": True,
        "exemplar_rows": exemplars,
    }
    return schema_rows, resolution_rows, summary


def _sage_review_status(
    closure_summary: Mapping[str, Any],
    tep_integrity_summary: Mapping[str, Any],
    genotype_schema_summary: Mapping[str, Any],
    case_study_summary: Mapping[str, Any],
) -> tuple[str, list[str]]:
    blockers: list[str] = []

    if tep_integrity_summary.get("status") != "pass":
        blockers.append("TEP_INPUT_INTEGRITY_UNRESOLVED")

    if genotype_schema_summary.get("status") != "pass":
        blockers.append("GENOTYPE_SCHEMA_UNRESOLVED")

    if closure_summary.get("closure_status") not in {
        "PASS",
        "PASS_WITH_BOUNDED_LIMITATIONS",
    }:
        blockers.append("GENOTYPE_ELEVATION_CLOSURE_UNRESOLVED")

    if case_study_summary.get("status") not in {
        "complete",
        "not_provided",
    }:
        blockers.append("CASE_STUDY_COMPARISON_INCOMPLETE")

    return (
        ("READY_FOR_SAGE_REVIEW", [])
        if not blockers
        else ("NOT_READY_FOR_SAGE_REVIEW", blockers)
    )


def build_sage_review_manifest(
    *,
    declared_artifacts: Sequence[str],
    comparison_id: str,
    overall_result: str,
    closure_summary: Mapping[str, Any],
    tep_integrity_summary: Mapping[str, Any],
    genotype_schema_summary: Mapping[str, Any],
    case_surface_rows: Sequence[Mapping[str, Any]],
    case_study_summary: Mapping[str, Any],
    limitations: Sequence[str],
) -> tuple[dict[str, Any], str]:
    review_status, blockers = _sage_review_status(
        closure_summary,
        tep_integrity_summary,
        genotype_schema_summary,
        case_study_summary,
    )

    manifest = {
        "schema_version": "sage_vap_comparison_review_manifest_v2",
        "script_version": VERSION,
        "comparison_id": comparison_id,
        "generated_utc": now_utc(),
        "review_status": review_status,
        "review_blockers": blockers,
        "overall_comparison_result": overall_result,
        "genotype_elevation_closure_status": closure_summary.get(
            "closure_status"
        ),
        "tep_input_integrity_status": tep_integrity_summary.get(
            "status"
        ),
        "genotype_schema_status": genotype_schema_summary.get(
            "status"
        ),
        "certified_case_study_summary": dict(case_study_summary),
        "certified_case_study_surface_counts": counts(
            case_surface_rows
        ),
        "included_artifacts": sorted(set(declared_artifacts)),
        "declared_limitations": list(limitations),
        "review_questions": [
            (
                "Does the evidence support certification that genotype "
                "elevation is transport-valid and scientifically coherent?"
            ),
            (
                "Is source-record context recovery with explicit "
                "complex-relationship deferral acceptable for "
                "multiallelic records?"
            ),
            (
                "Are the bounded historical noncoding and "
                "earliest-divergence limitations acceptable?"
            ),
            (
                "Are any additional scientific controls required "
                "before VDB ingestion?"
            ),
        ],
    }

    lines = [
        "# SAGE-VAP Comparison Review Manifest",
        "",
        f"- Comparison ID: `{comparison_id}`",
        f"- Script version: `{VERSION}`",
        f"- Review status: `{review_status}`",
        f"- Overall comparison result: `{overall_result}`",
        (
            "- Genotype elevation closure: "
            f"`{manifest['genotype_elevation_closure_status']}`"
        ),
        (
            "- TEP input integrity: "
            f"`{manifest['tep_input_integrity_status']}`"
        ),
        (
            "- Genotype schema status: "
            f"`{manifest['genotype_schema_status']}`"
        ),
        "",
    ]
    if blockers:
        lines.extend(["## Review Blockers", ""])
        lines.extend(f"- `{blocker}`" for blocker in blockers)
        lines.append("")

    lines.extend(["## Review Questions", ""])
    lines.extend(
        f"- {question}" for question in manifest["review_questions"]
    )
    lines.extend(["", "## Declared Limitations", ""])
    lines.extend(f"- {limitation}" for limitation in limitations)
    lines.extend(["", "## Included Evidence", ""])
    lines.extend(
        f"- `{filename}`"
        for filename in manifest["included_artifacts"]
    )
    lines.append("")
    return manifest, "\n".join(lines)


def case_inventory(root: Path | None) -> list[dict[str, Any]]:
    if root is None:
        return []
    rows: list[dict[str, Any]] = []
    for filename in CASE_TABLES:
        path = find_name(root, filename)
        if path is None:
            rows.append({
                "surface": filename,
                "historical_source": "",
                "current_source": "",
                "metric": "artifact_availability",
                "historical_value": "",
                "current_value": "",
                "delta": "",
                "classification": HISTORICAL_UNAVAILABLE,
                "notes": "certified case-study table unavailable",
            })
            continue
        rows.append({
            "surface": filename,
            "historical_source": str(path.relative_to(root)),
            "current_source": "",
            "metric": "certified_surface_inventory",
            "historical_value": {"size_bytes": path.stat().st_size, "sha256": sha256(path)},
            "current_value": "",
            "delta": "",
            "classification": NOT_COMPARABLE,
            "notes": "current equivalent derivation is not silently approximated in v0.1",
        })
    return rows


def current_capabilities(root: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(name: str, path: Path | None, passed: bool, details: str) -> None:
        rows.append({
            "capability": name,
            "path": str(path.relative_to(root)) if path and path.exists() else "",
            "classification": CURRENT_PASS if passed else CURRENT_FAIL,
            "details": details,
        })

    provenance = root / "metadata" / "execution_provenance.json"
    if provenance.is_file():
        data = load_json(provenance)
        add("execution_provenance", provenance, isinstance(data, dict) and data.get("contract_status") == "pass", f"contract_status={data.get('contract_status') if isinstance(data, dict) else None}")
    else:
        add("execution_provenance", None, False, "metadata execution provenance missing")

    genotype = next((p for p in [root / "processed" / "genotype_observations.tsv", *root.glob("tep/*/entities/genotype/genotype_observations.tsv")] if p.is_file()), None)
    add("genotype_observations", genotype, genotype is not None and genotype.stat().st_size > 0, f"size_bytes={genotype.stat().st_size if genotype else 0}")

    gsummary = next((p for p in [root / "processed" / "genotype_projection_summary.json", *root.glob("tep/*/entities/genotype/genotype_projection_summary.json")] if p.is_file()), None)
    if gsummary:
        data = load_json(gsummary)
        status: str | None = None
        status_source = "unresolved"

        if isinstance(data, dict):
            projection = data.get("projection")
            if isinstance(projection, dict):
                nested_status = projection.get("projection_status")
                if isinstance(nested_status, str):
                    status = nested_status
                    status_source = "projection.projection_status"

            if status is None:
                top_level_status = data.get("status")
                if isinstance(top_level_status, str):
                    status = top_level_status
                    status_source = "status"

        add(
            "genotype_projection_summary",
            gsummary,
            status in {"pass", "pass_with_advisory", "success"},
            f"status={status}; status_source={status_source}",
        )
    else:
        add("genotype_projection_summary", None, False, "genotype projection summary missing")

    tep_dirs = sorted(p for p in (root / "tep").glob("vap_tep_*") if p.is_dir()) if (root / "tep").is_dir() else []
    if not tep_dirs:
        add("native_tep_vap", None, False, "no native TEP-VAP package found")
    else:
        tep = tep_dirs[0]
        validation = tep / "validation_report.md"
        inventory_path = tep / "entity_inventory.json"
        lineage = tep / "lineage_manifest.json"
        passed = all(p.is_file() and p.stat().st_size > 0 for p in (validation, inventory_path, lineage))
        if validation.is_file():
            passed = passed and "Validation status: `pass`" in validation.read_text(encoding="utf-8", errors="replace")
        add("native_tep_vap", tep, passed, f"validation={validation.is_file()}; inventory={inventory_path.is_file()}; lineage={lineage.is_file()}")
        transported = tep / "entities" / "context" / "execution_provenance.json"
        add("tep_execution_provenance_transport", transported if transported.is_file() else None, transported.is_file() and transported.stat().st_size > 0, "canonical context transport path")
        metadata = tep / "entities" / "metadata" / "config_snapshot.yaml"
        add("tep_metadata_entity", metadata if metadata.is_file() else None, metadata.is_file() and metadata.stat().st_size > 0, "config snapshot transport")
    return rows


def counts(rows: Iterable[Mapping[str, Any]]) -> dict[str, int]:
    counter: Counter[str] = Counter(str(row.get("classification")) for row in rows if row.get("classification"))
    return dict(sorted(counter.items()))


def overall(stage_rows: Sequence[Mapping[str, Any]], capability_rows: Sequence[Mapping[str, Any]], availability: Sequence[Mapping[str, Any]]) -> str:
    if any(r.get("classification") == CURRENT_FAIL for r in capability_rows):
        return OVERALL_PARTIAL
    comparable = [r for r in stage_rows if r.get("classification") not in {RUN_IDENTITY, EVOLUTION, HISTORICAL_UNAVAILABLE, NOT_COMPARABLE}]
    if not comparable:
        return OVERALL_NOT_COMPARABLE
    if any(r.get("classification") in {DIFFERENT, UNDER_REVIEW} for r in comparable):
        return OVERALL_REVIEW
    if any(r.get("classification") in {EVOLUTION, HISTORICAL_UNAVAILABLE} for r in [*stage_rows, *availability]):
        return OVERALL_EVOLUTION
    return OVERALL_AVAILABLE


def report_text(comparison_id: str, generated: str, current_id: Mapping[str, Any], historical_id: Mapping[str, Any], case_root: Path | None, stage_rows: Sequence[Mapping[str, Any]], availability: Sequence[Mapping[str, Any]], table_rows: Sequence[Mapping[str, Any]], capabilities: Sequence[Mapping[str, Any]], semantic_rows: Sequence[Mapping[str, Any]], result: str, limitations: Sequence[str]) -> str:
    differences = [r for r in stage_rows if r.get("field_class") == "scientific" and r.get("classification") in {DIFFERENT, UNDER_REVIEW}]
    lines = [
        "# Historical Run Reproducibility Comparison Report", "",
        f"- Comparison ID: `{comparison_id}`",
        f"- Generated UTC: `{generated}`",
        f"- Script version: `{VERSION}`",
        f"- Overall bounded result: `{result}`", "",
        "## Evidence Sources", "",
        f"- Current execution: `{current_id.get('root', '')}`",
        f"- Current run ID: `{current_id.get('run_id', 'unknown')}`",
        f"- Historical lightweight reference: `{historical_id.get('root', '')}`",
        f"- Historical run ID: `{historical_id.get('run_id', 'unknown')}`",
        f"- Certified case-study reference: `{case_root if case_root else 'not provided'}`", "",
        "## Executive Interpretation", "",
        "The comparison is asymmetric by design. Missing historical artifacts are not mismatches, current-only architecture is validated independently, and unresolved scientific differences are not attributed to hardware without equivalent software, configuration, annotation, reference, and resource evidence.", "",
        "## Stage-Summary Classification Counts", "", "```text",
        *[f"{k}: {v}" for k, v in counts(stage_rows).items()], "```", "",
        "## Historical Availability Classification Counts", "", "```text",
        *[f"{k}: {v}" for k, v in counts(availability).items()], "```", "",
        "## Current-Only Capability Validation", "",
        "| Capability | Classification | Details |", "|---|---|---|",
        *[f"| {r.get('capability','')} | {r.get('classification','')} | {r.get('details','')} |" for r in capabilities], "",
        "## Scientific Differences Under Review", "",
    ]
    if differences:
        lines.extend(["| Stage | Field | Historical | Current | Delta | Classification |", "|---|---|---:|---:|---:|---|"])
        for row in differences[:200]:
            lines.append(f"| {row.get('stage','')} | `{row.get('field_path','')}` | {cell(row.get('historical_value'))} | {cell(row.get('current_value'))} | {cell(row.get('absolute_delta'))} | {row.get('classification','')} |")
        if len(differences) > 200:
            lines.extend(["", f"_Only the first 200 of {len(differences)} scientific differences are shown._"])
    else:
        lines.append("No comparable scientific differences were identified.")
    lines.extend(["", "## Shared Tabular Surfaces", ""])
    if table_rows:
        lines.extend(["| Table | Historical Rows | Current Rows | Delta | Shared Columns | Classification |", "|---|---:|---:|---:|---:|---|"])
        for row in table_rows:
            lines.append(f"| `{row.get('table','')}` | {row.get('historical_row_count','')} | {row.get('current_row_count','')} | {row.get('row_count_delta','')} | {row.get('shared_column_count','')} | {row.get('classification','')} |")
    else:
        lines.append("No shared tabular artifacts were available for schema-level comparison.")
    lines.extend([
        "", "## Certified Case-Study Surfaces", "",
        f"Recognized certified surfaces inventoried: {len(semantic_rows)}.", "",
        "Version 0.8 compares supported certified surfaces independently for each historical run and retains unsupported multidimensional surfaces as explicitly not comparable.", "",
        "## Historical Evidence Limitations", "",
        *[f"- {item}" for item in limitations], "",
        "## Bounded Conclusion", "",
        f"The comparison result is `{result}`.", "",
        "Operational validity, TEP validity, historical coverage, stage-summary reproducibility, semantic reproducibility, row-level reproducibility, and current-only capability validation remain distinct conclusions.", "",
        "## Output Artifacts", "",
        "- `comparison_manifest.json`", "- `comparison_receipt.json`",
        "- `current_artifact_inventory.tsv`", "- `historical_artifact_inventory.tsv`",
        "- `shared_artifact_inventory.tsv`", "- `historical_availability_report.tsv`",
        "- `stage_summary_comparison.tsv`", "- `tabular_schema_comparison.tsv`",
        "- `keyed_table_comparison_summary.tsv`", "- `unmatched_variant_keys.tsv`",
        "- `keyed_shared_row_differences.tsv`", "- `scientific_variant_differences.tsv`",
        "- `column_distribution_comparison.tsv`", "- `numeric_column_summary_comparison.tsv`",
        "- `semantic_surface_comparison.tsv`", "- `case_study_surface_derivation.tsv`",
        "- `case_study_comparison_summary.json`",
        "- `tep_comparison_input_integrity.tsv`",
        "- `tep_comparison_input_integrity_summary.json`",
        "- `genotype_schema_inventory.tsv`",
        "- `genotype_schema_resolution.tsv`",
        "- `genotype_schema_summary.json`",
        "- `sage_review_manifest.json`", "- `sage_review_manifest.md`",
        "- `current_only_capability_validation.tsv`",
        "- `comparison_report.md`", "",
    ])
    return "\n".join(lines)


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--current-run", required=True, type=Path)
    parser.add_argument("--historical-run", required=True, type=Path)
    parser.add_argument("--case-study", type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--comparison-id")
    parser.add_argument("--float-absolute-tolerance", type=float, default=1e-12)
    parser.add_argument("--float-relative-tolerance", type=float, default=1e-9)
    parser.add_argument("--max-hash-bytes", type=int, default=100 * 1024 * 1024)
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args(argv)


def validate(args: argparse.Namespace) -> None:
    for label, path in (("current run", args.current_run), ("historical run", args.historical_run)):
        if not path.is_dir():
            raise ComparisonError(f"Missing {label} directory: {path}")
    if args.case_study and not args.case_study.is_dir():
        raise ComparisonError(f"Missing case-study directory: {args.case_study}")
    if args.output_dir.exists():
        if not args.overwrite:
            raise ComparisonError(f"Output directory exists: {args.output_dir}; use --overwrite")
        resolved = args.output_dir.resolve()
        if resolved in {args.current_run.resolve(), args.historical_run.resolve()}:
            raise ComparisonError("Output directory cannot be an input directory")
        shutil.rmtree(args.output_dir)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    validate(args)
    current_root = args.current_run.resolve()
    historical_root = args.historical_run.resolve()
    case_root = args.case_study.resolve() if args.case_study else None
    output = args.output_dir.resolve()
    output.mkdir(parents=True, exist_ok=False)
    comparison_id = args.comparison_id or f"{current_root.name}_vs_{historical_root.name}"
    generated = now_utc()

    try:
        current_id = identity(current_root)
        historical_id = identity(historical_root)
        current_inventory = inventory(current_root, "current", args.max_hash_bytes)
        historical_inventory = inventory(historical_root, "historical", args.max_hash_bytes)
        stage_rows, stage_availability = compare_summaries(current_root, historical_root, args.float_absolute_tolerance, args.float_relative_tolerance)
        table_rows, table_availability = compare_tables(current_root, historical_root)
        (
            keyed_summary_rows,
            unmatched_key_rows,
            keyed_difference_rows,
            scientific_variant_difference_rows,
        ) = compare_keyed_tables(
            current_root,
            historical_root,
            table_rows,
            abs_tol=args.float_absolute_tolerance,
            rel_tol=args.float_relative_tolerance,
        )
        (
            column_distribution_rows,
            numeric_column_summary_rows,
        ) = compare_column_distributions(
            current_root,
            historical_root,
            table_rows,
        )
        (
            variant_delta_dossier_rows,
            variant_delta_summary_rows,
            variant_delta_field_inventory_rows,
            variant_delta_report,
        ) = build_variant_delta_dossier(
            current_root,
            historical_root,
            table_rows,
            unmatched_key_rows,
        )
        (
            variant_delta_dossier_rows,
            genotype_column_resolution_rows,
            variant_delta_locus_pairing_rows,
            variant_delta_lineage_matrix_rows,
            genotype_elevation_closure_summary,
            genotype_elevation_closure_report,
        ) = harden_variant_delta_dossier(
            current_root,
            historical_root,
            variant_delta_dossier_rows,
        )
        keyed_coding_summary = next(
            (
                row
                for row in keyed_summary_rows
                if row.get("table")
                == "stage_09_coding_interpreted.tsv"
            ),
            {},
        )
        genotype_elevation_closure_summary[
            "shared_coding_interpretation_invariance"
        ] = {
            "status": (
                "pass"
                if int(
                    keyed_coding_summary.get(
                        "scientific_changed_shared_row_count",
                        0,
                    )
                    or 0
                )
                == 0
                and int(
                    keyed_coding_summary.get(
                        "scientific_changed_shared_field_count",
                        0,
                    )
                    or 0
                )
                == 0
                else "under_review"
            ),
            "basis_source": "keyed_table_comparison_summary.tsv",
            "shared_key_count": keyed_coding_summary.get("shared_key_count", ""),
            "scientific_changed_shared_row_count": keyed_coding_summary.get(
                "scientific_changed_shared_row_count", ""
            ),
            "scientific_changed_shared_field_count": keyed_coding_summary.get(
                "scientific_changed_shared_field_count", ""
            ),
        }
        availability = sorted([*stage_availability, *table_availability], key=lambda r: (r.get("artifact_role", ""), r.get("current_path", "")))
        (
            semantic_rows,
            case_surface_derivation_rows,
            case_study_comparison_summary,
        ) = compare_certified_case_study_surfaces(
            current_root,
            case_root,
        )
        capability_rows = current_capabilities(current_root)
        tep_integrity_rows, tep_integrity_summary = (
            build_tep_input_integrity(current_root)
        )
        (
            genotype_schema_inventory_rows,
            genotype_schema_resolution_rows,
            genotype_schema_summary,
        ) = build_genotype_schema_inventory(current_root)
        result = overall(stage_rows, capability_rows, availability)

        limitations = [
            "The historical local run is a lightweight extraction, not a complete MARK execution snapshot.",
            "The current run includes execution provenance, elevated genotype, metadata transport, and fresh native TEP-VAP emission introduced after the historical run.",
            "Missing historical artifacts are classified as unavailable rather than mismatched.",
            "Case-study tables are curated surfaces and do not substitute for absent historical full-row artifacts.",
            "Hardware causality cannot be inferred unless software, configuration, annotation, reference, and resource identities are equivalent.",
            "Version 0.9 preserves ecosystem missingness semantics by distinguishing lexical nonemptiness, explicit missing sentinels, explicit not-applicable states, and true semantic value presence while retaining the v0.8 certification gates; historical noncoding identity evidence and complete upstream historical attribution remain unavailable.",
        ]

        inventory_fields = ["source", "relative_path", "filename", "suffix", "size_bytes", "sha256_status", "sha256", "artifact_class"]
        write_tsv(output / "current_artifact_inventory.tsv", inventory_fields, current_inventory)
        write_tsv(output / "historical_artifact_inventory.tsv", inventory_fields, historical_inventory)
        availability_fields = ["artifact_role", "current_path", "historical_path", "classification", "notes"]
        write_tsv(output / "shared_artifact_inventory.tsv", availability_fields, availability)
        write_tsv(output / "historical_availability_report.tsv", availability_fields, [r for r in availability if r.get("classification") != MATCH])
        write_tsv(output / "stage_summary_comparison.tsv", ["stage", "historical_source_path", "current_source_path", "field_path", "field_class", "historical_value", "current_value", "absolute_delta", "relative_delta", "classification", "notes"], sorted(stage_rows, key=lambda r: (r.get("stage", ""), r.get("field_path", ""))))
        write_tsv(output / "tabular_schema_comparison.tsv", ["table", "historical_path", "current_path", "historical_row_count", "current_row_count", "row_count_delta", "historical_column_count", "current_column_count", "shared_column_count", "shared_columns", "historical_only_columns", "current_only_columns", "stable_key_columns", "classification", "notes"], table_rows)
        write_tsv(
            output / "keyed_table_comparison_summary.tsv",
            [
                "table", "key_columns", "historical_unique_key_count",
                "current_unique_key_count", "shared_key_count",
                "historical_only_key_count", "current_only_key_count",
                "historical_duplicate_key_count", "current_duplicate_key_count",
                "historical_null_key_count", "current_null_key_count",
                "scientific_changed_shared_row_count",
                "scientific_changed_shared_field_count",
                "run_identity_changed_shared_row_count",
                "run_identity_changed_shared_field_count",
                "evolution_changed_shared_row_count",
                "evolution_changed_shared_field_count",
                "other_changed_shared_row_count",
                "other_changed_shared_field_count",
                "classification", "notes",
            ],
            keyed_summary_rows,
        )
        write_tsv(
            output / "unmatched_variant_keys.tsv",
            ["table", "key_columns", "key", "presence", "classification", "notes"],
            unmatched_key_rows,
        )
        write_tsv(
            output / "keyed_shared_row_differences.tsv",
            [
                "table", "key_columns", "key", "column", "field_class",
                "historical_value", "current_value", "absolute_delta",
                "relative_delta", "classification", "notes",
            ],
            keyed_difference_rows,
        )
        write_tsv(
            output / "scientific_variant_differences.tsv",
            [
                "table", "key_columns", "key", "column", "field_class",
                "historical_value", "current_value", "absolute_delta",
                "relative_delta", "classification", "notes",
            ],
            scientific_variant_difference_rows,
        )
        write_tsv(
            output / "column_distribution_comparison.tsv",
            [
                "table", "column", "distribution_type", "category",
                "historical_count", "current_count", "count_delta",
                "historical_fraction", "current_fraction",
                "fraction_delta", "classification",
            ],
            column_distribution_rows,
        )
        write_tsv(
            output / "numeric_column_summary_comparison.tsv",
            [
                "table", "column", "metric", "historical_value",
                "current_value", "delta", "classification",
            ],
            numeric_column_summary_rows,
        )
        write_tsv(
            output / "variant_delta_dossier.tsv",
            [
                "table", "presence", "variant_key",
                *DOSSIER_FIELD_ALIASES.keys(),
                "source_table_path", "genotype_source_path",
                "phred_likelihoods", "filter_status", "gt_arity",
                "called_allele_indexes", "projection_status",
                "projection_advisory", "record_parse_status",
                "source_record_variant_id", "source_record_alternate",
                "source_record_candidate_count",
                "genotype_resolution_status",
                "same_locus_pair_present", "same_locus_pair_relationships", "delta_classification",
                "available_field_count", "available_fields",
                "source_column_map", "missing_expected_fields",
                "classification", "notes",
            ],
            variant_delta_dossier_rows,
        )
        write_tsv(
            output / "variant_delta_dossier_summary.tsv",
            ["metric", "presence", "value", "count"],
            variant_delta_summary_rows,
        )
        write_tsv(
            output / "variant_delta_field_availability.tsv",
            [
                "table", "presence", "variant_key", "canonical_field",
                "source_column", "value_present", "source_surface",
            ],
            variant_delta_field_inventory_rows,
        )
        atomic_text(
            output / "variant_delta_dossier.md",
            variant_delta_report,
        )
        write_tsv(
            output / "genotype_column_resolution.tsv",
            [
                "canonical_field", "resolved_column",
                "resolution_status", "source_path",
            ],
            genotype_column_resolution_rows,
        )
        write_tsv(
            output / "variant_delta_locus_pairing.tsv",
            [
                "chromosome", "position", "reference",
                "historical_variant_id", "historical_alternate",
                "current_variant_id", "current_alternate",
                "relationship",
                "current_genotype_resolution_status",
                "current_relationship_status",
            ],
            variant_delta_locus_pairing_rows,
        )
        lineage_fields = [
            "presence", "variant_id",
            "historical_stage08_selected_transcript",
            "historical_stage08_selected_transcript_path",
            "historical_stage09_coding_interpreted",
            "historical_stage09_coding_interpreted_path",
            "current_stage07_annotated",
            "current_stage07_annotated_path",
            "current_stage08_selected_transcript",
            "current_stage08_selected_transcript_path",
            "current_stage08_vdb_ready",
            "current_stage08_vdb_ready_path",
            "current_stage09_coding_interpreted",
            "current_stage09_coding_interpreted_path",
            "earliest_defensible_divergence_boundary",
        ]
        write_tsv(
            output / "variant_delta_lineage_matrix.tsv",
            lineage_fields,
            variant_delta_lineage_matrix_rows,
        )
        write_json(
            output / "genotype_elevation_closure_summary.json",
            genotype_elevation_closure_summary,
        )
        atomic_text(
            output / "genotype_elevation_closure_summary.md",
            genotype_elevation_closure_report,
        )
        write_tsv(
            output / "case_study_surface_derivation.tsv",
            [
                "surface", "historical_source",
                "historical_run_count", "historical_row_count",
                "current_derived_row_count", "adapter_status",
                "adapter_key_columns", "adapter_value_columns",
            ],
            case_surface_derivation_rows,
        )
        write_json(
            output / "case_study_comparison_summary.json",
            case_study_comparison_summary,
        )
        write_tsv(
            output / "tep_comparison_input_integrity.tsv",
            [
                "tep_id", "entity_id", "entity_role",
                "source_artifact_role", "transport_path",
                "exists", "size_bytes", "declared_sha256",
                "observed_sha256", "checksum_status",
            ],
            tep_integrity_rows,
        )
        write_json(
            output / "tep_comparison_input_integrity_summary.json",
            tep_integrity_summary,
        )
        write_tsv(
            output / "genotype_schema_inventory.tsv",
            [
                "column_index", "column_name",
                "normalized_column_name", "canonical_mappings",
                "lexically_nonempty_count", "semantic_value_count",
                "explicit_missing_count",
                "explicit_not_applicable_count",
                "empty_count", "scanned_row_count",
            ],
            genotype_schema_inventory_rows,
        )
        write_tsv(
            output / "genotype_schema_resolution.tsv",
            [
                "canonical_field", "resolved_column",
                "resolution_status",
                "observed_lexically_nonempty_count",
                "observed_semantic_value_count",
                "observed_explicit_missing_count",
                "observed_explicit_not_applicable_count",
                "observed_empty_count",
                "scanned_row_count",
                "projection_summary_present_count",
            ],
            genotype_schema_resolution_rows,
        )
        write_json(
            output / "genotype_schema_summary.json",
            {
                key: value
                for key, value in genotype_schema_summary.items()
                if key != "exemplar_rows"
            },
        )
        exemplar_rows = genotype_schema_summary.get("exemplar_rows", [])
        if exemplar_rows:
            exemplar_fields = sorted(
                {
                    key
                    for row in exemplar_rows
                    for key in row
                }
            )
            write_tsv(
                output / "representative_genotype_exemplars.tsv",
                exemplar_fields,
                exemplar_rows,
            )
        write_tsv(
            output / "semantic_surface_comparison.tsv",
            [
                "surface", "historical_run_id", "historical_source",
                "current_source", "metric", "historical_value",
                "current_value", "delta", "classification", "notes",
            ],
            semantic_rows,
        )
        write_tsv(output / "current_only_capability_validation.tsv", ["capability", "path", "classification", "details"], capability_rows)
        atomic_text(output / "comparison_report.md", report_text(comparison_id, generated, current_id, historical_id, case_root, stage_rows, availability, table_rows, capability_rows, semantic_rows, result, limitations))
        manifest = {
            "schema_version": "1.0.0",
            "script_version": VERSION,
            "comparison_id": comparison_id,
            "generated_utc": generated,
            "overall_result": result,
            "inputs": {"current_run": str(current_root), "historical_run": str(historical_root), "case_study": str(case_root) if case_root else None},
            "identities": {"current": current_id, "historical": historical_id},
            "policies": {
                "float_absolute_tolerance": args.float_absolute_tolerance,
                "float_relative_tolerance": args.float_relative_tolerance,
                "max_hash_bytes": args.max_hash_bytes,
                "strict": args.strict,
                "historical_missing_artifacts_are_mismatches": False,
                "architecture_evolution_is_scientific_divergence": False,
            },
            "counts": {
                "current_artifacts": len(current_inventory),
                "historical_artifacts": len(historical_inventory),
                "stage_comparison_records": len(stage_rows),
                "availability_records": len(availability),
                "shared_table_records": len(table_rows),
                "keyed_table_records": len(keyed_summary_rows),
                "unmatched_key_records": len(unmatched_key_rows),
                "keyed_field_difference_records": len(keyed_difference_rows),
                "scientific_variant_difference_records": len(scientific_variant_difference_rows),
                "column_distribution_records": len(column_distribution_rows),
                "numeric_column_summary_records": len(numeric_column_summary_rows),
                "variant_delta_dossier_records": len(variant_delta_dossier_rows),
                "variant_delta_summary_records": len(variant_delta_summary_rows),
                "variant_delta_field_inventory_records": len(variant_delta_field_inventory_rows),
                "genotype_column_resolution_records": len(genotype_column_resolution_rows),
                "variant_delta_locus_pairing_records": len(variant_delta_locus_pairing_rows),
                "variant_delta_lineage_matrix_records": len(variant_delta_lineage_matrix_rows),
                "case_study_surface_derivation_records": len(case_surface_derivation_rows),
                "tep_integrity_records": len(tep_integrity_rows),
                "genotype_schema_inventory_records": len(genotype_schema_inventory_rows),
                "genotype_schema_resolution_records": len(genotype_schema_resolution_rows),
                "case_study_surface_records": len(semantic_rows),
                "current_only_capability_records": len(capability_rows),
            },
            "classification_counts": {
                "stage_summaries": counts(stage_rows),
                "availability": counts(availability),
                "current_only_capabilities": counts(capability_rows),
                "case_study_surfaces": counts(semantic_rows),
            },
            "certification_surfaces": {
                "genotype_elevation_closure": genotype_elevation_closure_summary,
                "tep_input_integrity": tep_integrity_summary,
                "genotype_schema": {
                    key: value
                    for key, value in genotype_schema_summary.items()
                    if key != "exemplar_rows"
                },
                "certified_case_study_comparison": (
                    case_study_comparison_summary
                ),
            },
            "limitations": limitations,
        }
        write_json(output / "comparison_manifest.json", manifest)

        receipt_targets = [
            "current_artifact_inventory.tsv", "historical_artifact_inventory.tsv",
            "shared_artifact_inventory.tsv", "historical_availability_report.tsv",
            "stage_summary_comparison.tsv", "tabular_schema_comparison.tsv",
            "keyed_table_comparison_summary.tsv", "unmatched_variant_keys.tsv",
            "keyed_shared_row_differences.tsv", "scientific_variant_differences.tsv",
            "column_distribution_comparison.tsv", "numeric_column_summary_comparison.tsv",
            "variant_delta_dossier.tsv", "variant_delta_dossier_summary.tsv",
            "variant_delta_field_availability.tsv", "variant_delta_dossier.md",
            "genotype_column_resolution.tsv", "variant_delta_locus_pairing.tsv",
            "variant_delta_lineage_matrix.tsv",
            "genotype_elevation_closure_summary.json",
            "genotype_elevation_closure_summary.md",
            "case_study_surface_derivation.tsv",
            "case_study_comparison_summary.json",
            "tep_comparison_input_integrity.tsv",
            "tep_comparison_input_integrity_summary.json",
            "genotype_schema_inventory.tsv",
            "genotype_schema_resolution.tsv",
            "genotype_schema_summary.json",
            "representative_genotype_exemplars.tsv",
            "sage_review_manifest.json", "sage_review_manifest.md",
            "semantic_surface_comparison.tsv", "current_only_capability_validation.tsv",
            "comparison_report.md", "comparison_manifest.json",
        ]
        declared_sage_artifacts = [
            *receipt_targets,
            "comparison_receipt.json",
            "sage_review_manifest.json",
            "sage_review_manifest.md",
        ]
        sage_review_manifest, sage_review_report = (
            build_sage_review_manifest(
                declared_artifacts=declared_sage_artifacts,
                comparison_id=comparison_id,
                overall_result=result,
                closure_summary=genotype_elevation_closure_summary,
                tep_integrity_summary=tep_integrity_summary,
                genotype_schema_summary=genotype_schema_summary,
                case_surface_rows=semantic_rows,
                case_study_summary=case_study_comparison_summary,
                limitations=limitations,
            )
        )
        write_json(
            output / "sage_review_manifest.json",
            sage_review_manifest,
        )
        atomic_text(
            output / "sage_review_manifest.md",
            sage_review_report,
        )

        write_json(output / "comparison_receipt.json", {
            "schema_version": "1.0.0",
            "comparison_id": comparison_id,
            "generated_utc": now_utc(),
            "output_sha256": {name: sha256(output / name) for name in receipt_targets},
        })

        print(f"comparison_id: {comparison_id}")
        print(f"overall_result: {result}")
        print(f"output_dir: {output}")
        print(f"stage_comparison_records: {len(stage_rows)}")
        print(f"availability_records: {len(availability)}")
        print(f"shared_table_records: {len(table_rows)}")
        print(f"keyed_table_records: {len(keyed_summary_rows)}")
        print(f"unmatched_key_records: {len(unmatched_key_rows)}")
        print(f"keyed_field_difference_records: {len(keyed_difference_rows)}")
        print(f"scientific_variant_difference_records: {len(scientific_variant_difference_rows)}")
        print(f"column_distribution_records: {len(column_distribution_rows)}")
        print(f"numeric_column_summary_records: {len(numeric_column_summary_rows)}")
        print(f"variant_delta_dossier_records: {len(variant_delta_dossier_rows)}")
        print(f"variant_delta_summary_records: {len(variant_delta_summary_rows)}")
        print(f"variant_delta_locus_pairing_records: {len(variant_delta_locus_pairing_rows)}")
        print(f"variant_delta_lineage_matrix_records: {len(variant_delta_lineage_matrix_rows)}")
        print(f"genotype_elevation_closure_status: {genotype_elevation_closure_summary.get('closure_status')}")
        print(f"tep_input_integrity_status: {tep_integrity_summary.get('status')}")
        print(f"genotype_schema_status: {genotype_schema_summary.get('status')}")
        print(f"case_study_surface_records: {len(semantic_rows)}")
        print(f"current_only_capability_records: {len(capability_rows)}")

        if args.strict and result in {OVERALL_PARTIAL, OVERALL_REVIEW, OVERALL_NOT_COMPARABLE, OVERALL_FAILED}:
            return 2
        return 0
    except Exception as exc:
        write_json(output / "comparison_failure.json", {
            "schema_version": "1.0.0",
            "comparison_id": comparison_id,
            "generated_utc": now_utc(),
            "overall_result": OVERALL_FAILED,
            "failure": {"type": type(exc).__name__, "message": str(exc)},
        })
        raise


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ComparisonError as exc:
        print(f"comparison failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
