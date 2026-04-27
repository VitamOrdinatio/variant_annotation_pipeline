"""
Stage 09: Interpret coding and splice-region variants.

Stage 09 consumes Stage 08 structured outputs and assigns deterministic,
non-ranking coding interpretation flags.

Contract notes:
- interpretation only; no ranking or prioritization
- preserve all Stage 08 fields
- consume Stage 08 structural fields as authoritative
- no external database queries
- no biological inference from missingness
"""

from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path
from typing import Any


MISSING_TOKENS = {"", "NA", "N/A", ".", "-", "NULL", "None", "none", "nan", "NaN"}

REQUIRED_FIELDS = [
    "sample_id",
    "variant_id",
    "gene_id",
    "gene_symbol",
    "consequence",
    "impact_class",
    "variant_context",
    "variant_type",
    "variant_class",
    "population_frequency",
    "gnomad_af",
    "exac_af",
    "thousand_genomes_af",
    "clinical_significance",
    "clinvar_significance",
    "qc_status",
    "quality_flag",
    "annotation_source",
    "annotation_version",
    "frequency_status",
    "clinical_status",
    "gene_mapping_status",
    "variant_effect_severity",
    "source_pipeline",
    "run_id",
]

ADDED_FIELDS = [
    "functional_impact",
    "rarity_flag",
    "clinical_evidence",
    "qc_reliability",
    "coding_interpretation_label",
    "is_lof_candidate",
    "is_rare_candidate",
    "is_clinically_supported",
    "is_high_quality",
    "is_potential_artifact",
]

FUNCTIONAL_IMPACT_VALUES = [
    "loss_of_function",
    "missense",
    "synonymous",
    "splice_relevant",
    "other_coding",
    "unknown",
]

RARITY_VALUES = ["rare", "low_frequency", "common", "missing", "unknown"]
QC_VALUES = ["high_confidence", "caution", "low_confidence"]
CLINICAL_VALUES = [
    "pathogenic",
    "likely_pathogenic",
    "vus",
    "likely_benign",
    "benign",
    "conflicting",
    "missing",
]
LABEL_VALUES = [
    "lof_rare_clinically_supported",
    "lof_or_missense_rare",
    "coding_common_or_low_support",
    "coding_uninterpretable",
]

LOF_TERMS = {
    "stop_gained",
    "frameshift_variant",
    "start_lost",
    "stop_lost",
    "splice_acceptor_variant",
    "splice_donor_variant",
}

MISSENSE_TERMS = {"missense_variant"}
SYNONYMOUS_TERMS = {"synonymous_variant"}
SPLICE_RELEVANT_TERMS = {"splice_region_variant"}
OTHER_CODING_TERMS = {
    "inframe_insertion",
    "inframe_deletion",
    "protein_altering_variant",
    "incomplete_terminal_codon_variant",
    "coding_sequence_variant",
}


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


def _split_consequence_terms(consequence: Any) -> set[str]:
    if _is_missing(consequence):
        return set()
    text = str(consequence).replace(",", "&")
    return {term.strip() for term in text.split("&") if term.strip()}


def _assign_functional_impact(consequence: Any, variant_context: Any) -> str:
    terms = _split_consequence_terms(consequence)
    context = _clean(variant_context, "unknown")

    if not terms:
        return "unknown"

    if terms & LOF_TERMS:
        return "loss_of_function"
    if terms & MISSENSE_TERMS:
        return "missense"
    if terms & SPLICE_RELEVANT_TERMS:
        return "splice_relevant"
    if terms & OTHER_CODING_TERMS:
        return "other_coding"
    if terms & SYNONYMOUS_TERMS:
        return "synonymous"

    if context == "coding":
        return "other_coding"

    return "unknown"


def _assign_rarity_flag(frequency_status: Any) -> str:
    value = _clean(frequency_status, "unknown").lower()
    return value if value in RARITY_VALUES else "unknown"


def _normalize_clinical_text(value: Any) -> str:
    if _is_missing(value):
        return ""
    return str(value).strip().lower().replace(" ", "_").replace("-", "_")


def _clinical_from_raw_clinvar(clinvar_significance: Any) -> str:
    text = _normalize_clinical_text(clinvar_significance)
    if not text:
        return "missing"
    if "conflicting" in text or "conflict" in text:
        return "conflicting"
    if "likely_pathogenic" in text:
        return "likely_pathogenic"
    if "pathogenic" in text:
        return "pathogenic"
    if "uncertain_significance" in text or text == "vus" or "uncertain" in text:
        return "vus"
    if "likely_benign" in text:
        return "likely_benign"
    if "benign" in text:
        return "benign"
    return "missing"


def _assign_clinical_evidence(clinical_status: Any, clinvar_significance: Any) -> str:
    status = _normalize_clinical_text(clinical_status)
    if status in CLINICAL_VALUES:
        return status
    return _clinical_from_raw_clinvar(clinvar_significance)


def _assign_qc_reliability(qc_status: Any) -> str:
    value = _clean(qc_status, "unknown").lower()
    if value == "pass":
        return "high_confidence"
    if value == "caution":
        return "caution"
    if value == "fail":
        return "low_confidence"
    return "low_confidence"


def _has_missing_key_fields(row: dict[str, str], functional_impact: str, rarity_flag: str, clinical_evidence: str) -> bool:
    key_fields = [
        "sample_id",
        "run_id",
        "source_pipeline",
        "variant_id",
        "gene_id",
        "gene_symbol",
        "consequence",
        "variant_context",
        "frequency_status",
        "clinical_status",
        "qc_status",
    ]
    if any(_is_missing(row.get(field)) for field in key_fields):
        return True
    if functional_impact == "unknown":
        return True
    if rarity_flag == "unknown":
        return True
    if clinical_evidence not in CLINICAL_VALUES:
        return True
    return False


def _assign_coding_interpretation_label(
    row: dict[str, str],
    functional_impact: str,
    rarity_flag: str,
    clinical_evidence: str,
    qc_reliability: str,
) -> str:
    gene_mapping_status = _clean(row.get("gene_mapping_status"), "unknown").lower()

    if (
        gene_mapping_status == "unmapped"
        or qc_reliability == "low_confidence"
        or _has_missing_key_fields(row, functional_impact, rarity_flag, clinical_evidence)
    ):
        return "coding_uninterpretable"

    if rarity_flag == "common" or clinical_evidence in {"benign", "likely_benign"}:
        return "coding_common_or_low_support"

    if (
        functional_impact == "loss_of_function"
        and rarity_flag == "rare"
        and clinical_evidence in {"pathogenic", "likely_pathogenic"}
        and qc_reliability == "high_confidence"
    ):
        return "lof_rare_clinically_supported"

    if (
        functional_impact in {"loss_of_function", "missense"}
        and rarity_flag in {"rare", "low_frequency"}
        and qc_reliability == "high_confidence"
        and clinical_evidence not in {"benign", "likely_benign"}
    ):
        return "lof_or_missense_rare"

    return "coding_common_or_low_support"


def _validate_header(fieldnames: list[str] | None, path: Path) -> list[str]:
    if fieldnames is None:
        raise ValueError(f"Could not read header from Stage 09 input: {path}")
    missing = [field for field in REQUIRED_FIELDS if field not in fieldnames]
    if missing:
        raise ValueError(f"Stage 09 input missing required fields {missing}: {path}")
    return list(fieldnames)


def _validate_file(path_str: str | None, label: str) -> Path:
    if not path_str:
        raise ValueError(f"Missing required Stage 09 input artifact: {label}")
    path = Path(path_str)
    if not path.exists():
        raise FileNotFoundError(f"Required Stage 09 input does not exist: {path}")
    if not path.is_file():
        raise FileNotFoundError(f"Required Stage 09 input is not a file: {path}")
    if path.stat().st_size == 0:
        raise ValueError(f"Required Stage 09 input is empty: {path}")
    return path


def _get_stage08_inputs(state: dict[str, Any]) -> tuple[Path, Path, Path, Path]:
    artifacts = state.get("artifacts", {})
    coding = _validate_file(artifacts.get("coding_candidates"), "coding_candidates")
    splice = _validate_file(artifacts.get("splice_region_candidates"), "splice_region_candidates")
    variant_summary = _validate_file(artifacts.get("stage_08_variant_summary"), "stage_08_variant_summary")
    selected = _validate_file(
        artifacts.get("stage_08_selected_transcript_consequences"),
        "stage_08_selected_transcript_consequences",
    )
    return coding, splice, variant_summary, selected


def _prepare_output_paths(processed_dir: Path) -> dict[str, Path]:
    return {
        "coding_interpreted": processed_dir / "stage_09_coding_interpreted.tsv",
        "summary_json": processed_dir / "stage_09_summary.json",
    }


def _init_summary_sets() -> dict[str, dict[str, set[str]]]:
    return {
        "functional_impact_distribution": {key: set() for key in FUNCTIONAL_IMPACT_VALUES},
        "rarity_flag_distribution": {key: set() for key in RARITY_VALUES},
        "qc_distribution": {key: set() for key in QC_VALUES},
        "clinical_evidence_distribution": {key: set() for key in CLINICAL_VALUES},
        "coding_interpretation_label_distribution": {key: set() for key in LABEL_VALUES},
        "scalar_sets": {
            "total_coding_variants": set(),
            "lof_variant_count": set(),
            "missense_variant_count": set(),
            "rare_variant_count": set(),
            "low_frequency_variant_count": set(),
            "common_variant_count": set(),
            "clinically_supported_count": set(),
            "benign_or_likely_benign_count": set(),
            "uninterpretable_count": set(),
        },
    }


def _update_summary_sets(summary_sets: dict[str, dict[str, set[str]]], row: dict[str, str]) -> None:
    variant_id = row["variant_id"]
    functional_impact = row["functional_impact"]
    rarity_flag = row["rarity_flag"]
    qc_reliability = row["qc_reliability"]
    clinical_evidence = row["clinical_evidence"]
    label = row["coding_interpretation_label"]

    summary_sets["scalar_sets"]["total_coding_variants"].add(variant_id)

    summary_sets["functional_impact_distribution"].setdefault(functional_impact, set()).add(variant_id)
    summary_sets["rarity_flag_distribution"].setdefault(rarity_flag, set()).add(variant_id)
    summary_sets["qc_distribution"].setdefault(qc_reliability, set()).add(variant_id)
    summary_sets["clinical_evidence_distribution"].setdefault(clinical_evidence, set()).add(variant_id)
    summary_sets["coding_interpretation_label_distribution"].setdefault(label, set()).add(variant_id)

    if functional_impact == "loss_of_function":
        summary_sets["scalar_sets"]["lof_variant_count"].add(variant_id)
    if functional_impact == "missense":
        summary_sets["scalar_sets"]["missense_variant_count"].add(variant_id)
    if rarity_flag == "rare":
        summary_sets["scalar_sets"]["rare_variant_count"].add(variant_id)
    if rarity_flag == "low_frequency":
        summary_sets["scalar_sets"]["low_frequency_variant_count"].add(variant_id)
    if rarity_flag == "common":
        summary_sets["scalar_sets"]["common_variant_count"].add(variant_id)
    if clinical_evidence in {"pathogenic", "likely_pathogenic"}:
        summary_sets["scalar_sets"]["clinically_supported_count"].add(variant_id)
    if clinical_evidence in {"benign", "likely_benign"}:
        summary_sets["scalar_sets"]["benign_or_likely_benign_count"].add(variant_id)
    if label == "coding_uninterpretable":
        summary_sets["scalar_sets"]["uninterpretable_count"].add(variant_id)


def _sets_to_counts(summary_sets: dict[str, dict[str, set[str]]]) -> dict[str, Any]:
    summary: dict[str, Any] = {}

    for key, value in summary_sets["scalar_sets"].items():
        summary[key] = len(value)

    for distribution_name in [
        "coding_interpretation_label_distribution",
        "rarity_flag_distribution",
        "qc_distribution",
        "functional_impact_distribution",
        "clinical_evidence_distribution",
    ]:
        summary[distribution_name] = {
            key: len(value)
            for key, value in summary_sets[distribution_name].items()
        }

    return summary


def _write_summary_json(path: Path, summary_sets: dict[str, dict[str, set[str]]], metadata: dict[str, Any]) -> None:
    summary = _sets_to_counts(summary_sets)
    summary.update(metadata)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2, sort_keys=True)
        handle.write("\n")


def _interpret_row(input_row: dict[str, str]) -> dict[str, str]:
    row = dict(input_row)
    functional_impact = _assign_functional_impact(row.get("consequence"), row.get("variant_context"))
    rarity_flag = _assign_rarity_flag(row.get("frequency_status"))
    clinical_evidence = _assign_clinical_evidence(row.get("clinical_status"), row.get("clinvar_significance"))
    qc_reliability = _assign_qc_reliability(row.get("qc_status"))

    row["functional_impact"] = functional_impact
    row["rarity_flag"] = rarity_flag
    row["clinical_evidence"] = clinical_evidence
    row["qc_reliability"] = qc_reliability
    row["is_lof_candidate"] = _bool_text(functional_impact == "loss_of_function")
    row["is_rare_candidate"] = _bool_text(rarity_flag == "rare")
    row["is_clinically_supported"] = _bool_text(clinical_evidence in {"pathogenic", "likely_pathogenic"})
    row["is_high_quality"] = _bool_text(qc_reliability == "high_confidence")
    row["is_potential_artifact"] = _bool_text(qc_reliability == "low_confidence")
    row["coding_interpretation_label"] = _assign_coding_interpretation_label(
        row=row,
        functional_impact=functional_impact,
        rarity_flag=rarity_flag,
        clinical_evidence=clinical_evidence,
        qc_reliability=qc_reliability,
    )
    return row


def _iter_stage09_candidate_rows(paths: list[Path], logger):
    seen_keys: set[tuple[str, str, str]] = set()
    output_fieldnames: list[str] | None = None

    for path in paths:
        _log(logger, "info", f"Reading Stage 09 input: {path}")
        with path.open("r", encoding="utf-8", errors="replace", newline="") as handle:
            reader = csv.DictReader(handle, delimiter="\t")
            fieldnames = _validate_header(reader.fieldnames, path)

            if output_fieldnames is None:
                output_fieldnames = fieldnames
            elif fieldnames != output_fieldnames:
                raise ValueError(
                    f"Stage 09 input header mismatch. First header={output_fieldnames}; "
                    f"mismatched file={path}; header={fieldnames}"
                )

            for row in reader:
                variant_context = _clean(row.get("variant_context"), "unknown")
                if variant_context not in {"coding", "splice_region"}:
                    _log(
                        logger,
                        "warning",
                        f"Skipping non-coding/non-splice row found in Stage 09 input: "
                        f"{path}; variant_id={row.get('variant_id')}; variant_context={variant_context}",
                    )
                    continue

                key = (
                    _clean(row.get("variant_id"), "NA"),
                    _clean(row.get("transcript_id"), "NA"),
                    _clean(row.get("consequence"), "NA"),
                )
                if key in seen_keys:
                    _log(logger, "warning", f"Skipping duplicate Stage 09 candidate row: {key}")
                    continue

                seen_keys.add(key)
                yield row, output_fieldnames

    if output_fieldnames is None:
        raise ValueError("No Stage 09 input rows were available.")


def run_stage(
    config: dict[str, Any],
    paths: dict[str, Any],
    logger,
    state: dict[str, Any],
) -> dict[str, Any]:
    _log(logger, "info", "Stage 09: interpreting coding and splice-region variants.")

    coding_path, splice_path, variant_summary_path, selected_path = _get_stage08_inputs(state)
    processed_dir = Path(paths["processed_dir"])
    processed_dir.mkdir(parents=True, exist_ok=True)
    output_paths = _prepare_output_paths(processed_dir)

    _log(logger, "info", f"Stage 09 coding input: {coding_path}")
    _log(logger, "info", f"Stage 09 splice-region input: {splice_path}")
    _log(logger, "info", f"Stage 09 Stage 08 variant summary validation input: {variant_summary_path}")
    _log(logger, "info", f"Stage 09 selected transcript validation input: {selected_path}")

    summary_sets = _init_summary_sets()
    input_rows = 0
    interpreted_rows = 0
    output_fieldnames: list[str] | None = None

    with output_paths["coding_interpreted"].open("w", encoding="utf-8", newline="") as out_handle:
        writer: csv.DictWriter | None = None

        for input_row, fieldnames in _iter_stage09_candidate_rows([coding_path, splice_path], logger):
            input_rows += 1

            if output_fieldnames is None:
                output_fieldnames = fieldnames + ADDED_FIELDS
                writer = csv.DictWriter(out_handle, fieldnames=output_fieldnames, delimiter="\t")
                writer.writeheader()

            interpreted_row = _interpret_row(input_row)
            assert writer is not None
            writer.writerow({field: interpreted_row.get(field, "NA") for field in output_fieldnames})
            _update_summary_sets(summary_sets, interpreted_row)
            interpreted_rows += 1

        if writer is None:
            output_fieldnames = REQUIRED_FIELDS + ADDED_FIELDS
            writer = csv.DictWriter(out_handle, fieldnames=output_fieldnames, delimiter="\t")
            writer.writeheader()

    metadata = {
        "stage": "stage_09_interpret_coding",
        "status": "success",
        "input_rows": input_rows,
        "interpreted_rows": interpreted_rows,
        "input_files": {
            "coding_candidates": str(coding_path),
            "splice_region_candidates": str(splice_path),
            "stage_08_variant_summary": str(variant_summary_path),
            "stage_08_selected_transcript_consequences": str(selected_path),
        },
        "output_files": {
            "stage_09_coding_interpreted": str(output_paths["coding_interpreted"]),
            "stage_09_summary_json": str(output_paths["summary_json"]),
        },
        "assumptions": [
            "Stage 09 consumes Stage 08 structural fields as authoritative.",
            "Stage 09 performs interpretation flagging only; it does not rank or prioritize variants.",
            "Summary counts are distinct variant_id counts implemented with sets.",
            "Duplicate candidate rows across coding and splice-region inputs are skipped by variant_id/transcript_id/consequence key.",
        ],
    }
    _write_summary_json(output_paths["summary_json"], summary_sets, metadata)

    state.setdefault("artifacts", {})
    state["artifacts"]["stage_09_coding_interpreted"] = str(output_paths["coding_interpreted"])
    state["artifacts"]["stage_09_summary_json"] = str(output_paths["summary_json"])

    state.setdefault("qc", {})
    summary_counts = _sets_to_counts(summary_sets)
    state["qc"]["stage_09_qc"] = {
        "input_rows": input_rows,
        "interpreted_rows": interpreted_rows,
        "total_coding_variants": summary_counts["total_coding_variants"],
        "uninterpretable_count": summary_counts["uninterpretable_count"],
        "output_exists": output_paths["coding_interpreted"].exists(),
        "summary_exists": output_paths["summary_json"].exists(),
    }

    state.setdefault("stage_outputs", {})
    state["stage_outputs"]["stage_09_interpret_coding"] = {
        "status": "success",
        "input_coding_candidates": str(coding_path),
        "input_splice_region_candidates": str(splice_path),
        "coding_interpreted": str(output_paths["coding_interpreted"]),
        "summary_json": str(output_paths["summary_json"]),
        "input_rows": input_rows,
        "interpreted_rows": interpreted_rows,
    }

    _log(logger, "info", f"Stage 09 interpreted coding variants written to: {output_paths['coding_interpreted']}")
    _log(logger, "info", f"Stage 09 summary JSON written to: {output_paths['summary_json']}")
    _log(logger, "info", f"Stage 09 input rows processed: {input_rows}")
    _log(logger, "info", f"Stage 09 interpreted rows written: {interpreted_rows}")

    return state