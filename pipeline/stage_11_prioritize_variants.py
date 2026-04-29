"""
Stage 11: Prioritize interpreted variants.

Stage 11 integrates Stage 09 coding and Stage 10 noncoding interpreted variants
into one unified variant-level candidate table and assigns deterministic priority
tiers.

Contract notes:
- prioritization only
- no new annotation
- no gene-level aggregation
- no probabilistic scoring
- preserve upstream fields
"""

from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path
from typing import Any


MISSING_TOKENS = {"", "NA", "N/A", ".", "-", "NULL", "None", "none", "nan", "NaN"}

ADDED_FIELDS = [
    "variant_origin",
    "source_interpretation_label",
    "priority_tier",
    "priority_rank",
    "priority_reason",
    "is_high_priority_candidate",
    "is_moderate_priority_candidate",
    "is_low_priority_candidate",
    "is_uninterpretable",
]

CODING_LABEL_FIELD = "coding_interpretation_label"
NONCODING_LABEL_FIELD = "noncoding_interpretation_label"

CODING_LABELS = {
    "lof_rare_clinically_supported",
    "lof_or_missense_rare",
    "coding_common_or_low_support",
    "coding_uninterpretable",
}

NONCODING_LABELS = {
    "regulatory_rare_supported",
    "regulatory_or_transcript_rare",
    "noncoding_common_or_low_support",
    "noncoding_uninterpretable",
}

COMMON_REQUIRED_FIELDS = [
    "sample_id",
    "run_id",
    "source_pipeline",
    "variant_id",
    "chromosome",
    "position",
    "reference_allele",
    "alternate_allele",
    "variant_type",
    "variant_class",
    "quality_flag",
    "gene_id",
    "gene_symbol",
    "transcript_id",
    "consequence",
    "impact_class",
    "clinical_significance",
    "clinvar_significance",
    "population_frequency",
    "gnomad_af",
    "exac_af",
    "thousand_genomes_af",
    "mito_flag",
    "epilepsy_flag",
    "annotation_source",
    "annotation_version",
    "gene_mapping_status",
    "variant_context",
    "variant_effect_severity",
    "qc_status",
    "interpretability_status",
    "frequency_status",
    "clinical_status",
    "rarity_flag",
    "clinical_evidence",
    "qc_reliability",
]


def _log(logger, level: str, message: str) -> None:
    method = getattr(logger, level, None)
    if method is None:
        print(f"[{level.upper()}] {message}")
    else:
        method(message)


def _is_missing(value: Any) -> bool:
    if value is None:
        return True
    return str(value).strip() in MISSING_TOKENS


def _clean(value: Any, null_value: str = "NA") -> str:
    if value is None:
        return null_value
    text = str(value).strip()
    return text if text else null_value


def _bool_text(value: bool) -> str:
    return "True" if value else "False"


def _validate_file(path_str: str | None, label: str) -> Path:
    if not path_str:
        raise ValueError(f"Missing required Stage 11 input artifact: {label}")
    path = Path(path_str)
    if not path.exists():
        raise FileNotFoundError(f"Required Stage 11 input does not exist: {path}")
    if not path.is_file():
        raise FileNotFoundError(f"Required Stage 11 input is not a file: {path}")
    if path.stat().st_size == 0:
        raise ValueError(f"Required Stage 11 input is empty: {path}")
    return path


def _get_stage_inputs(state: dict[str, Any]) -> tuple[Path, Path]:
    artifacts = state.get("artifacts", {})
    coding = _validate_file(
        artifacts.get("stage_09_coding_interpreted"),
        "stage_09_coding_interpreted",
    )
    noncoding = _validate_file(
        artifacts.get("stage_10_noncoding_interpreted"),
        "stage_10_noncoding_interpreted",
    )
    return coding, noncoding


def _validate_header(fieldnames: list[str] | None, path: Path, origin: str) -> list[str]:
    if fieldnames is None:
        raise ValueError(f"Could not read header from Stage 11 input: {path}")

    missing_common = [field for field in COMMON_REQUIRED_FIELDS if field not in fieldnames]
    if missing_common:
        raise ValueError(f"Stage 11 {origin} input missing required fields {missing_common}: {path}")

    label_field = CODING_LABEL_FIELD if origin == "coding" else NONCODING_LABEL_FIELD
    if label_field not in fieldnames:
        raise ValueError(f"Stage 11 {origin} input missing interpretation label field {label_field}: {path}")

    return list(fieldnames)


def _prepare_output_paths(processed_dir: Path) -> dict[str, Path]:
    return {
        "prioritized_variants": processed_dir / "stage_11_prioritized_variants.tsv",
        "gene_variant_counts": processed_dir / "stage_11_gene_variant_counts.tsv",
        "summary_json": processed_dir / "stage_11_summary.json",
    }


def _assign_priority(origin: str, source_label: str) -> tuple[str, str, str]:
    if origin == "coding":
        if source_label == "lof_rare_clinically_supported":
            return (
                "tier_1_high_confidence_candidate",
                "1",
                "coding label lof_rare_clinically_supported",
            )
        if source_label == "lof_or_missense_rare":
            return (
                "tier_2_moderate_candidate",
                "2",
                "coding label lof_or_missense_rare",
            )
        if source_label == "coding_common_or_low_support":
            return (
                "tier_3_low_support_or_common",
                "3",
                "coding label coding_common_or_low_support",
            )
        if source_label == "coding_uninterpretable":
            return (
                "tier_4_uninterpretable_or_qc_limited",
                "4",
                "coding label coding_uninterpretable",
            )

    if origin == "noncoding":
        if source_label == "regulatory_rare_supported":
            return (
                "tier_1_high_confidence_candidate",
                "1",
                "noncoding label regulatory_rare_supported",
            )
        if source_label == "regulatory_or_transcript_rare":
            return (
                "tier_2_moderate_candidate",
                "2",
                "noncoding label regulatory_or_transcript_rare",
            )
        if source_label == "noncoding_common_or_low_support":
            return (
                "tier_3_low_support_or_common",
                "3",
                "noncoding label noncoding_common_or_low_support",
            )
        if source_label == "noncoding_uninterpretable":
            return (
                "tier_4_uninterpretable_or_qc_limited",
                "4",
                "noncoding label noncoding_uninterpretable",
            )

    return (
        "tier_4_uninterpretable_or_qc_limited",
        "4",
        f"unrecognized {origin} interpretation label: {source_label}",
    )


def _interpret_row(row: dict[str, str], origin: str) -> tuple[dict[str, str], bool]:
    out = dict(row)
    label_field = CODING_LABEL_FIELD if origin == "coding" else NONCODING_LABEL_FIELD
    source_label = _clean(row.get(label_field), "NA")

    malformed = False
    if _is_missing(row.get("variant_id")) or _is_missing(source_label):
        malformed = True

    priority_tier, priority_rank, priority_reason = _assign_priority(origin, source_label)

    out["variant_origin"] = origin
    out["source_interpretation_label"] = source_label
    out["priority_tier"] = priority_tier
    out["priority_rank"] = priority_rank
    out["priority_reason"] = priority_reason
    out["is_high_priority_candidate"] = _bool_text(priority_rank == "1")
    out["is_moderate_priority_candidate"] = _bool_text(priority_rank == "2")
    out["is_low_priority_candidate"] = _bool_text(priority_rank == "3")
    out["is_uninterpretable"] = _bool_text(priority_rank == "4")

    return out, malformed


def _init_summary() -> dict[str, Any]:
    return {
        "input_rows": 0,
        "output_rows": 0,
        "unassigned_or_malformed_rows": 0,
        "counts_by_priority_tier": Counter(),
        "counts_by_priority_rank": Counter(),
        "counts_by_variant_origin": Counter(),
        "counts_by_gene_id": Counter(),
        "counts_by_source_interpretation_label": Counter(),
        "high_priority_candidate_count": 0,
        "moderate_priority_candidate_count": 0,
        "low_priority_candidate_count": 0,
        "uninterpretable_count": 0,
    }


def _update_summary(summary: dict[str, Any], row: dict[str, str], malformed: bool) -> None:
    summary["input_rows"] += 1
    summary["output_rows"] += 1

    if malformed:
        summary["unassigned_or_malformed_rows"] += 1

    priority_tier = row["priority_tier"]
    priority_rank = row["priority_rank"]
    variant_origin = row["variant_origin"]
    gene_id = _clean(row.get("gene_id"), "NA")
    source_label = row["source_interpretation_label"]

    summary["counts_by_priority_tier"][priority_tier] += 1
    summary["counts_by_priority_rank"][priority_rank] += 1
    summary["counts_by_variant_origin"][variant_origin] += 1
    summary["counts_by_gene_id"][gene_id] += 1
    summary["counts_by_source_interpretation_label"][source_label] += 1

    if priority_rank == "1":
        summary["high_priority_candidate_count"] += 1
    elif priority_rank == "2":
        summary["moderate_priority_candidate_count"] += 1
    elif priority_rank == "3":
        summary["low_priority_candidate_count"] += 1
    elif priority_rank == "4":
        summary["uninterpretable_count"] += 1


def _summary_to_jsonable(summary: dict[str, Any], metadata: dict[str, Any]) -> dict[str, Any]:
    result = dict(metadata)

    for key, value in summary.items():
        if key == "counts_by_gene_id":
            result["gene_id_count_unique"] = len(value)
            result["counts_by_gene_id_top_50"] = dict(
                sorted(value.items(), key=lambda item: (-item[1], item[0]))[:50]
            )
        elif isinstance(value, Counter):
            result[key] = dict(sorted(value.items()))
        else:
            result[key] = value

    return result

def _write_summary_json(path: Path, summary: dict[str, Any], metadata: dict[str, Any]) -> None:
    payload = _summary_to_jsonable(summary, metadata)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
        handle.write("\n")

def _write_gene_variant_counts_tsv(path: Path, counts_by_gene_id: Counter) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["gene_id", "variant_count"],
            delimiter="\t",
        )
        writer.writeheader()
        for gene_id, count in sorted(counts_by_gene_id.items(), key=lambda item: (-item[1], item[0])):
            writer.writerow({"gene_id": gene_id, "variant_count": count})

def _iter_input_rows(path: Path, origin: str, logger):
    _log(logger, "info", f"Reading Stage 11 {origin} input: {path}")
    with path.open("r", encoding="utf-8", errors="replace", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        fieldnames = _validate_header(reader.fieldnames, path, origin)
        for row in reader:
            yield row, fieldnames


def run_stage(
    config: dict[str, Any],
    paths: dict[str, Any],
    logger,
    state: dict[str, Any],
) -> dict[str, Any]:
    _log(logger, "info", "Stage 11: prioritizing interpreted variants.")

    coding_path, noncoding_path = _get_stage_inputs(state)
    processed_dir = Path(paths["processed_dir"])
    processed_dir.mkdir(parents=True, exist_ok=True)
    output_paths = _prepare_output_paths(processed_dir)

    _log(logger, "info", f"Stage 11 coding input: {coding_path}")
    _log(logger, "info", f"Stage 11 noncoding input: {noncoding_path}")

    summary = _init_summary()
    output_fieldnames: list[str] | None = None

    with output_paths["prioritized_variants"].open("w", encoding="utf-8", newline="") as out_handle:
        writer: csv.DictWriter | None = None

        for origin, input_path in [("coding", coding_path), ("noncoding", noncoding_path)]:
            for input_row, fieldnames in _iter_input_rows(input_path, origin, logger):
                prioritized_row, malformed = _interpret_row(input_row, origin)

                if output_fieldnames is None:
                    output_fieldnames = fieldnames + [
                        field for field in ADDED_FIELDS if field not in fieldnames
                    ]
                    writer = csv.DictWriter(
                        out_handle,
                        fieldnames=output_fieldnames,
                        delimiter="\t",
                        extrasaction="ignore",
                    )
                    writer.writeheader()

                assert writer is not None
                writer.writerow({field: prioritized_row.get(field, "NA") for field in output_fieldnames})
                _update_summary(summary, prioritized_row, malformed)

    metadata = {
        "stage": "stage_11_prioritize_variants",
        "status": "success",
        "input_files": {
            "stage_09_coding_interpreted": str(coding_path),
            "stage_10_noncoding_interpreted": str(noncoding_path),
        },
        "output_files": {
            "stage_11_prioritized_variants": str(output_paths["prioritized_variants"]),
            "stage_11_gene_variant_counts": str(output_paths["gene_variant_counts"]),
            "stage_11_summary_json": str(output_paths["summary_json"]),
        },
        "assumptions": [
            "Stage 11 consumes Stage 09 and Stage 10 interpretation labels as authoritative.",
            "Stage 11 performs deterministic variant-level prioritization only.",
            "Stage 11 does not perform gene-level aggregation or ranking.",
            "Rows with unrecognized interpretation labels are routed to Tier 4.",
        ],
    }
    _write_gene_variant_counts_tsv(output_paths["gene_variant_counts"], summary["counts_by_gene_id"])
    _write_summary_json(output_paths["summary_json"], summary, metadata)

    state.setdefault("artifacts", {})
    state["artifacts"]["stage_11_prioritized_variants"] = str(output_paths["prioritized_variants"])
    state["artifacts"]["stage_11_gene_variant_counts"] = str(output_paths["gene_variant_counts"])
    state["artifacts"]["stage_11_summary_json"] = str(output_paths["summary_json"])

    state.setdefault("qc", {})
    state["qc"]["stage_11_qc"] = {
        "input_rows": summary["input_rows"],
        "output_rows": summary["output_rows"],
        "unassigned_or_malformed_rows": summary["unassigned_or_malformed_rows"],
        "high_priority_candidate_count": summary["high_priority_candidate_count"],
        "moderate_priority_candidate_count": summary["moderate_priority_candidate_count"],
        "low_priority_candidate_count": summary["low_priority_candidate_count"],
        "uninterpretable_count": summary["uninterpretable_count"],
        "output_exists": output_paths["prioritized_variants"].exists(),
        "gene_variant_counts_exists": output_paths["gene_variant_counts"].exists(),
        "summary_exists": output_paths["summary_json"].exists(),
}

    state.setdefault("stage_outputs", {})
    state["stage_outputs"]["stage_11_prioritize_variants"] = {
        "status": "success",
        "input_coding_interpreted": str(coding_path),
        "input_noncoding_interpreted": str(noncoding_path),
        "prioritized_variants": str(output_paths["prioritized_variants"]),
        "gene_variant_counts": str(output_paths["gene_variant_counts"]),
        "summary_json": str(output_paths["summary_json"]),
        "input_rows": summary["input_rows"],
        "output_rows": summary["output_rows"],
        "unassigned_or_malformed_rows": summary["unassigned_or_malformed_rows"],
    }

    _log(logger, "info", f"Stage 11 prioritized variants written to: {output_paths['prioritized_variants']}")
    _log(logger, "info", f"Stage 11 gene variant counts written to: {output_paths['gene_variant_counts']}")
    _log(logger, "info", f"Stage 11 summary JSON written to: {output_paths['summary_json']}")
    _log(logger, "info", f"Stage 11 input rows processed: {summary['input_rows']}")
    _log(logger, "info", f"Stage 11 output rows written: {summary['output_rows']}")
    _log(logger, "info", f"Stage 11 malformed/unassigned rows: {summary['unassigned_or_malformed_rows']}")

    return state