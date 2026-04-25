"""
Stage 08: Filter and partition annotated variants.

VAP v1 implementation notes
---------------------------
Authoritative specification: stage_08_contract.md

Stage 08 converts Stage 07 VEP annotation output into a biologically structured,
lossless, interpretation-ready dataset.

Key v1 assumptions:
- canonical input is Stage 07 annotated_variants.tsv
- annotated_variants.vcf is retained for validation/provenance only
- Stage 07 TSV is treated as selected-transcript truth:
  one row = one variant with one selected transcript annotation
- full CSQ expansion is deferred to a future VAP v2 mode
- no final pathogenicity scoring is performed
- no variants are dropped unless irreparably malformed
- source annotation fields are preserved
- RDGP seed counts are deduplicated by distinct variant_id per sample/gene
"""

from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


MISSING_TOKENS = {"", "NA", "N/A", ".", "NULL", "None", "none", "nan", "NaN"}

REQUIRED_INPUT_COLUMNS = [
    "sample_id",
    "run_id",
    "source_pipeline",
    "variant_id",
    "chromosome",
    "position",
    "reference_allele",
    "alternate_allele",
    "quality_flag",
    "gene_id",
    "gene_symbol",
    "transcript_id",
    "consequence",
    "impact_class",
    "variant_class",
    "clinical_significance",
    "clinvar_significance",
    "population_frequency",
    "gnomad_af",
    "exac_af",
    "thousand_genomes_af",
    "mito_flag",
    "epilepsy_flag",
]

DOWNSTREAM_COMPATIBILITY_FIELDS = [
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
]

STAGE08_COMMON_COLUMNS = DOWNSTREAM_COMPATIBILITY_FIELDS + [
    "variant_context",
    "variant_effect_severity",
    "qc_status",
    "interpretability_status",
    "frequency_status",
    "clinical_status",
]

SELECTED_TRANSCRIPT_COLUMNS = STAGE08_COMMON_COLUMNS

VDB_READY_COLUMNS = STAGE08_COMMON_COLUMNS

VARIANT_SUMMARY_COLUMNS = [
    "sample_id",
    "run_id",
    "source_pipeline",
    "variant_id",
    "chromosome",
    "position",
    "reference_allele",
    "alternate_allele",
    "gene_symbols",
    "gene_mapping_status",
    "worst_consequence",
    "highest_impact",
    "canonical_present",
    "coding_flag",
    "splice_flag",
    "noncoding_flag",
    "transcript_count",
    "variant_type",
    "variant_class",
    "quality_flag",
    "qc_status",
    "population_frequency",
    "frequency_status",
    "clinical_status",
    "annotation_source",
    "annotation_version",
]

RDGP_SEED_COLUMNS = [
    "sample_id",
    "gene_id",
    "gene_symbol",
    "variant_count",
    "high_impact_variant_count",
    "rare_variant_count",
    "pathogenic_variant_count",
    "max_variant_severity",
    "has_low_quality_evidence",
    "contributing_variant_ids",
]

SEVERITY_RANK = {
    "UNKNOWN": 0,
    "MODIFIER": 1,
    "LOW": 2,
    "MODERATE": 3,
    "HIGH": 4,
}

CONTEXT_PRIORITY = [
    "splice_region",
    "coding",
    "regulatory",
    "intronic",
    "intergenic",
    "noncoding_transcript",
    "unknown",
]

CODING_CONSEQUENCE_TERMS = {
    "missense_variant",
    "synonymous_variant",
    "stop_gained",
    "stop_lost",
    "start_lost",
    "frameshift_variant",
    "inframe_insertion",
    "inframe_deletion",
    "protein_altering_variant",
}

SPLICE_CONSEQUENCE_TERMS = {
    "splice_acceptor_variant",
    "splice_donor_variant",
    "splice_region_variant",
}

INTRONIC_CONSEQUENCE_TERMS = {
    "intron_variant",
}

INTERGENIC_CONSEQUENCE_TERMS = {
    "intergenic_variant",
}

REGULATORY_CONSEQUENCE_TERMS = {
    "regulatory_region_variant",
    "TF_binding_site_variant",
    "mature_miRNA_variant",
    "upstream_gene_variant",
    "downstream_gene_variant",
}

NONCODING_TRANSCRIPT_CONSEQUENCE_TERMS = {
    "non_coding_transcript_exon_variant",
    "non_coding_transcript_variant",
    "NMD_transcript_variant",
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
    if text == "":
        return null_value
    return text


def _safe_bool_text(value: Any) -> str:
    text = _clean(value, "False").strip().lower()
    if text in {"true", "1", "yes", "y"}:
        return "True"
    if text in {"false", "0", "no", "n", "na", "n/a", ".", "null"}:
        return "False"
    return "False"


def _parse_float(value: Any) -> float | None:
    if _is_missing(value):
        return None
    try:
        return float(str(value).strip())
    except ValueError:
        return None


def _format_float(value: float | None) -> str:
    if value is None:
        return "NULL"
    return f"{value:.10g}"


def _split_consequence_terms(consequence: str) -> set[str]:
    if _is_missing(consequence):
        return set()
    normalized = consequence.replace(",", "&")
    return {term.strip() for term in normalized.split("&") if term.strip()}


def _assign_variant_context(consequence: str) -> str:
    terms = _split_consequence_terms(consequence)
    contexts = _assign_partition_contexts(consequence)
    for context in CONTEXT_PRIORITY:
        if context in contexts:
            return context
    if not terms:
        return "unknown"
    return "unknown"


def _assign_partition_contexts(consequence: str) -> set[str]:
    terms = _split_consequence_terms(consequence)
    contexts: set[str] = set()

    if terms & CODING_CONSEQUENCE_TERMS:
        contexts.add("coding")
    if terms & SPLICE_CONSEQUENCE_TERMS:
        contexts.add("splice_region")
    if terms & INTRONIC_CONSEQUENCE_TERMS:
        contexts.add("intronic")
    if terms & INTERGENIC_CONSEQUENCE_TERMS:
        contexts.add("intergenic")
    if terms & REGULATORY_CONSEQUENCE_TERMS:
        contexts.add("regulatory")
    if terms & NONCODING_TRANSCRIPT_CONSEQUENCE_TERMS:
        contexts.add("noncoding_transcript")

    if not contexts:
        contexts.add("unknown")

    return contexts


def _normalize_variant_type(value: Any) -> str:
    text = _clean(value, "unknown").strip().lower().replace("-", "_")
    mapping = {
        "snv": "snv",
        "snp": "snv",
        "single_nucleotide_variant": "snv",
        "substitution": "snv",
        "insertion": "insertion",
        "ins": "insertion",
        "deletion": "deletion",
        "del": "deletion",
        "indel": "indel",
        "mnv": "complex",
        "mnp": "complex",
        "complex": "complex",
    }
    return mapping.get(text, "unknown")


def _derive_variant_type_from_alleles(ref: Any, alt: Any) -> str:
    ref_text = _clean(ref, "").strip()
    alt_text = _clean(alt, "").strip()

    if not ref_text or not alt_text or ref_text in MISSING_TOKENS or alt_text in MISSING_TOKENS:
        return "unknown"

    if "," in alt_text:
        return "complex"

    if len(ref_text) == 1 and len(alt_text) == 1:
        return "snv"

    if len(ref_text) < len(alt_text):
        return "insertion"

    if len(ref_text) > len(alt_text):
        return "deletion"

    if len(ref_text) == len(alt_text):
        return "complex"

    return "unknown"


def _normalize_variant_class(value: Any, variant_context: str) -> str:
    text = _clean(value, "unknown").strip().lower().replace("_", "-")
    if text in {"coding"}:
        return "coding"
    if text in {"non-coding", "noncoding"}:
        return "noncoding"
    if text in {"structural", "sv"}:
        return "structural"
    if variant_context in {"coding", "splice_region"}:
        return "coding"
    if variant_context in {"regulatory", "intronic", "intergenic", "noncoding_transcript"}:
        return "noncoding"
    return "unknown"


def _assign_effect_severity(impact_class: Any, consequence: Any) -> str:
    impact = _clean(impact_class, "UNKNOWN").strip().upper()
    if impact in {"HIGH", "MODERATE", "LOW", "MODIFIER"}:
        return impact

    terms = _split_consequence_terms(_clean(consequence, ""))
    if terms & {"stop_gained", "frameshift_variant", "splice_acceptor_variant", "splice_donor_variant", "start_lost", "stop_lost"}:
        return "HIGH"
    if terms & {"missense_variant", "inframe_insertion", "inframe_deletion", "protein_altering_variant"}:
        return "MODERATE"
    if terms & {"synonymous_variant"}:
        return "LOW"
    if terms:
        return "MODIFIER"
    return "UNKNOWN"


def _compute_population_frequency(row: dict[str, str]) -> tuple[str, float | None]:
    values = [
        _parse_float(row.get("gnomad_af")),
        _parse_float(row.get("exac_af")),
        _parse_float(row.get("thousand_genomes_af")),
    ]
    valid_values = [value for value in values if value is not None]
    if not valid_values:
        return "NULL", None
    max_value = max(valid_values)
    return _format_float(max_value), max_value


def _assign_frequency_status(population_frequency_value: float | None) -> str:
    if population_frequency_value is None:
        return "missing"
    if population_frequency_value >= 0.05:
        return "common"
    if population_frequency_value >= 0.01:
        return "low_frequency"
    if population_frequency_value >= 0:
        return "rare"
    return "unknown"


def _normalize_clinical_text(value: Any) -> str:
    if _is_missing(value):
        return ""
    return str(value).strip().lower().replace(" ", "_").replace("-", "_")


def _assign_clinical_status(row: dict[str, str]) -> str:
    clinical = _normalize_clinical_text(row.get("clinical_significance"))
    clinvar = _normalize_clinical_text(row.get("clinvar_significance"))

    observed = {value for value in [clinical, clinvar] if value}
    if not observed:
        return "missing"

    joined = "|".join(sorted(observed))
    if "conflicting" in joined or "conflict" in joined:
        return "conflicting"

    normalized_values = set()
    for value in observed:
        if "likely_pathogenic" in value:
            normalized_values.add("likely_pathogenic")
        elif "pathogenic" in value:
            normalized_values.add("pathogenic")
        elif "uncertain_significance" in value or value == "vus" or "uncertain" in value:
            normalized_values.add("vus")
        elif "likely_benign" in value:
            normalized_values.add("likely_benign")
        elif "benign" in value:
            normalized_values.add("benign")

    if not normalized_values:
        return "missing"

    pathogenic_side = normalized_values & {"pathogenic", "likely_pathogenic"}
    benign_side = normalized_values & {"benign", "likely_benign"}
    if pathogenic_side and benign_side:
        return "conflicting"

    precedence = ["pathogenic", "likely_pathogenic", "vus", "likely_benign", "benign"]
    for status in precedence:
        if status in normalized_values:
            return status

    return "missing"


def _assign_interpretability_status(variant_context: str, variant_effect_severity: str) -> str:
    if variant_context in {"coding", "splice_region"} and variant_effect_severity in {"HIGH", "MODERATE", "LOW", "MODIFIER"}:
        return "interpretable_now"
    if variant_context in {"regulatory", "intronic", "intergenic", "noncoding_transcript"}:
        return "needs_external_annotation"
    return "unsupported_currently"


def _assign_gene_mapping_status(row: dict[str, str]) -> str:
    gene_id = row.get("gene_id")
    gene_symbol = row.get("gene_symbol")
    if _is_missing(gene_id) and _is_missing(gene_symbol):
        return "unmapped"
    return "mapped"


def _assign_qc_status(row: dict[str, str], variant_context: str, variant_effect_severity: str) -> str:
    essential_fields = [
        "sample_id",
        "run_id",
        "source_pipeline",
        "variant_id",
        "chromosome",
        "position",
        "reference_allele",
        "alternate_allele",
        "quality_flag",
    ]
    if any(str(row.get(field, "")).strip() == "" for field in essential_fields):
        return "fail"

    if variant_context == "unknown" or variant_effect_severity == "UNKNOWN":
        return "caution"

    quality_flag = _clean(row.get("quality_flag"), "NA").strip().upper()
    if quality_flag not in {"PASS", "."}:
        return "caution"

    return "pass"


def _get_annotation_version(config: dict[str, Any], state: dict[str, Any]) -> str:
    candidates = [
        state.get("annotations", {}).get("annotation_version"),
        state.get("annotations", {}).get("vep_version"),
        state.get("run", {}).get("tool_versions", {}).get("vep"),
        config.get("annotation", {}).get("annotation_version"),
        config.get("tools", {}).get("vep", {}).get("version"),
        config.get("tools", {}).get("vep", {}).get("cache_version"),
        config.get("tools", {}).get("vep", {}).get("annotation_version"),
    ]

    for candidate in candidates:
        if not _is_missing(candidate):
            text = str(candidate).strip()
            if "ensembl-vep" in text.lower() or "version" in text.lower():
                parts = [part for part in text.replace(",", " ").split() if part.isdigit()]
                if parts:
                    return parts[0]
            return text

    runtime_mode = str(config.get("runtime", {}).get("mode", "")).strip().lower()
    if runtime_mode in {"dev", "development", "test", "testing"}:
        return "unknown"

    return "115"


def _validate_required_file(path_str: str | None, label: str) -> Path:
    if not path_str:
        raise ValueError(f"Missing required Stage 08 artifact path for {label}")
    path = Path(path_str)
    if not path.exists():
        raise FileNotFoundError(f"Required Stage 08 input not found for {label}: {path}")
    if not path.is_file():
        raise FileNotFoundError(f"Expected file for {label}, found non-file path: {path}")
    if path.stat().st_size == 0:
        raise ValueError(f"Required Stage 08 input is empty for {label}: {path}")
    return path


def _validate_input_header(fieldnames: list[str] | None, input_tsv: Path) -> None:
    if fieldnames is None:
        raise ValueError(f"Could not read header from Stage 08 input TSV: {input_tsv}")
    missing = [column for column in REQUIRED_INPUT_COLUMNS if column not in fieldnames]
    if missing:
        raise ValueError(
            f"Stage 08 canonical TSV is missing required columns: {missing}. "
            f"Input TSV: {input_tsv}"
        )


def _prepare_output_paths(processed_dir: Path) -> dict[str, Path]:
    return {
        "selected_transcript_consequences": processed_dir / "stage_08_selected_transcript_consequences.tsv",
        "variant_summary": processed_dir / "stage_08_variant_summary.tsv",
        "coding_candidates": processed_dir / "coding_candidates.tsv",
        "splice_region_candidates": processed_dir / "splice_region_candidates.tsv",
        "noncoding_candidates": processed_dir / "noncoding_candidates.tsv",
        "qc_flagged": processed_dir / "qc_flagged.tsv",
        "summary_json": processed_dir / "stage_08_summary.json",
        "vdb_ready_variants": processed_dir / "stage_08_vdb_ready_variants.tsv",
        "rdgp_gene_evidence_seed": processed_dir / "stage_08_rdgp_gene_evidence_seed.tsv",
    }


def _coerce_stage08_row(
    input_row: dict[str, str],
    annotation_source: str,
    annotation_version: str,
) -> tuple[dict[str, str], set[str]]:
    row = {field: _clean(input_row.get(field), "NA") for field in REQUIRED_INPUT_COLUMNS}

    variant_context = _assign_variant_context(row["consequence"])
    partition_contexts = _assign_partition_contexts(row["consequence"])
    variant_type = _normalize_variant_type(input_row.get("variant_type") or input_row.get("variant_class"))
    variant_class = _normalize_variant_class(row["variant_class"], variant_context)
    variant_effect_severity = _assign_effect_severity(row["impact_class"], row["consequence"])
    population_frequency, population_frequency_value = _compute_population_frequency(row)
    frequency_status = _assign_frequency_status(population_frequency_value)
    clinical_status = _assign_clinical_status(row)
    interpretability_status = _assign_interpretability_status(variant_context, variant_effect_severity)
    gene_mapping_status = _assign_gene_mapping_status(row)
    qc_status = _assign_qc_status(row, variant_context, variant_effect_severity)

    row["variant_type"] = variant_type
    row["variant_class"] = variant_class
    row["population_frequency"] = population_frequency
    row["mito_flag"] = _safe_bool_text(row["mito_flag"])
    row["epilepsy_flag"] = _safe_bool_text(row["epilepsy_flag"])
    row["annotation_source"] = annotation_source
    row["annotation_version"] = annotation_version
    row["gene_mapping_status"] = gene_mapping_status
    row["variant_context"] = variant_context
    row["variant_effect_severity"] = variant_effect_severity
    row["qc_status"] = qc_status
    row["interpretability_status"] = interpretability_status
    row["frequency_status"] = frequency_status
    row["clinical_status"] = clinical_status

    return row, partition_contexts


def _highest_severity(values: set[str]) -> str:
    if not values:
        return "UNKNOWN"
    return max(values, key=lambda value: SEVERITY_RANK.get(value, 0))


def _update_variant_aggregates(
    aggregates: dict[str, dict[str, Any]],
    row: dict[str, str],
    partition_contexts: set[str],
) -> None:
    variant_id = row["variant_id"]
    record = aggregates.setdefault(
        variant_id,
        {
            "sample_id": row["sample_id"],
            "run_id": row["run_id"],
            "source_pipeline": row["source_pipeline"],
            "variant_id": row["variant_id"],
            "chromosome": row["chromosome"],
            "position": row["position"],
            "reference_allele": row["reference_allele"],
            "alternate_allele": row["alternate_allele"],
            "gene_symbols": set(),
            "gene_mapping_statuses": set(),
            "consequences": set(),
            "severities": set(),
            "coding_flag": False,
            "splice_flag": False,
            "noncoding_flag": False,
            "transcript_ids": set(),
            "variant_type": row["variant_type"],
            "variant_class": row["variant_class"],
            "quality_flag": row["quality_flag"],
            "qc_statuses": set(),
            "population_frequency_values": [],
            "frequency_statuses": set(),
            "clinical_statuses": set(),
            "annotation_source": row["annotation_source"],
            "annotation_version": row["annotation_version"],
        },
    )

    if not _is_missing(row["gene_symbol"]):
        record["gene_symbols"].add(row["gene_symbol"])
    record["gene_mapping_statuses"].add(row["gene_mapping_status"])
    if not _is_missing(row["consequence"]):
        record["consequences"].add(row["consequence"])
    record["severities"].add(row["variant_effect_severity"])
    if not _is_missing(row["transcript_id"]):
        record["transcript_ids"].add(row["transcript_id"])

    if "coding" in partition_contexts:
        record["coding_flag"] = True
    if "splice_region" in partition_contexts:
        record["splice_flag"] = True
    if partition_contexts & {"regulatory", "intronic", "intergenic", "noncoding_transcript", "unknown"}:
        record["noncoding_flag"] = True

    record["qc_statuses"].add(row["qc_status"])

    parsed_af = _parse_float(row["population_frequency"])
    if parsed_af is not None:
        record["population_frequency_values"].append(parsed_af)

    record["frequency_statuses"].add(row["frequency_status"])
    record["clinical_statuses"].add(row["clinical_status"])


def _update_rdgp_aggregates(
    aggregates: dict[tuple[str, str, str], dict[str, Any]],
    row: dict[str, str],
) -> None:
    if row["gene_mapping_status"] != "mapped":
        return

    gene_id = row["gene_id"]
    gene_symbol = row["gene_symbol"]

    if _is_missing(gene_id) and _is_missing(gene_symbol):
        return

    grouping_gene_key = gene_id if not _is_missing(gene_id) else gene_symbol
    key = (row["sample_id"], grouping_gene_key, gene_symbol)

    record = aggregates.setdefault(
        key,
        {
            "sample_id": row["sample_id"],
            "gene_id": gene_id,
            "gene_symbol": gene_symbol,
            "variant_ids": set(),
            "high_impact_variant_ids": set(),
            "rare_variant_ids": set(),
            "pathogenic_variant_ids": set(),
            "severities": set(),
            "has_low_quality_evidence": False,
        },
    )

    variant_id = row["variant_id"]
    record["variant_ids"].add(variant_id)
    record["severities"].add(row["variant_effect_severity"])

    if row["variant_effect_severity"] == "HIGH":
        record["high_impact_variant_ids"].add(variant_id)
    if row["frequency_status"] == "rare":
        record["rare_variant_ids"].add(variant_id)
    if row["clinical_status"] in {"pathogenic", "likely_pathogenic"}:
        record["pathogenic_variant_ids"].add(variant_id)
    if row["qc_status"] != "pass":
        record["has_low_quality_evidence"] = True


def _write_variant_summary(path: Path, aggregates: dict[str, dict[str, Any]]) -> int:
    rows_written = 0
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=VARIANT_SUMMARY_COLUMNS, delimiter="\t")
        writer.writeheader()

        for variant_id in sorted(aggregates):
            record = aggregates[variant_id]
            highest_impact = _highest_severity(record["severities"])
            population_frequency_values = record["population_frequency_values"]
            population_frequency = _format_float(max(population_frequency_values)) if population_frequency_values else "NULL"

            qc_status = "pass"
            if "fail" in record["qc_statuses"]:
                qc_status = "fail"
            elif "caution" in record["qc_statuses"]:
                qc_status = "caution"

            clinical_status = "missing"
            clinical_statuses = record["clinical_statuses"]
            for status in ["conflicting", "pathogenic", "likely_pathogenic", "vus", "likely_benign", "benign", "missing"]:
                if status in clinical_statuses:
                    clinical_status = status
                    break

            frequency_status = "missing"
            frequency_statuses = record["frequency_statuses"]
            for status in ["unknown", "common", "low_frequency", "rare", "missing"]:
                if status in frequency_statuses:
                    frequency_status = status
                    break

            gene_mapping_status = "mapped" if "mapped" in record["gene_mapping_statuses"] else "unmapped"

            writer.writerow(
                {
                    "sample_id": record["sample_id"],
                    "run_id": record["run_id"],
                    "source_pipeline": record["source_pipeline"],
                    "variant_id": record["variant_id"],
                    "chromosome": record["chromosome"],
                    "position": record["position"],
                    "reference_allele": record["reference_allele"],
                    "alternate_allele": record["alternate_allele"],
                    "gene_symbols": ",".join(sorted(record["gene_symbols"])) if record["gene_symbols"] else "NA",
                    "gene_mapping_status": gene_mapping_status,
                    "worst_consequence": sorted(record["consequences"])[0] if record["consequences"] else "NA",
                    "highest_impact": highest_impact,
                    "canonical_present": "False",
                    "coding_flag": str(bool(record["coding_flag"])),
                    "splice_flag": str(bool(record["splice_flag"])),
                    "noncoding_flag": str(bool(record["noncoding_flag"])),
                    "transcript_count": len(record["transcript_ids"]) if record["transcript_ids"] else 1,
                    "variant_type": record["variant_type"],
                    "variant_class": record["variant_class"],
                    "quality_flag": record["quality_flag"],
                    "qc_status": qc_status,
                    "population_frequency": population_frequency,
                    "frequency_status": frequency_status,
                    "clinical_status": clinical_status,
                    "annotation_source": record["annotation_source"],
                    "annotation_version": record["annotation_version"],
                }
            )
            rows_written += 1

    return rows_written


def _write_rdgp_seed(path: Path, aggregates: dict[tuple[str, str, str], dict[str, Any]]) -> int:
    rows_written = 0
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=RDGP_SEED_COLUMNS, delimiter="\t")
        writer.writeheader()

        for key in sorted(aggregates):
            record = aggregates[key]
            writer.writerow(
                {
                    "sample_id": record["sample_id"],
                    "gene_id": record["gene_id"],
                    "gene_symbol": record["gene_symbol"],
                    "variant_count": len(record["variant_ids"]),
                    "high_impact_variant_count": len(record["high_impact_variant_ids"]),
                    "rare_variant_count": len(record["rare_variant_ids"]),
                    "pathogenic_variant_count": len(record["pathogenic_variant_ids"]),
                    "max_variant_severity": _highest_severity(record["severities"]),
                    "has_low_quality_evidence": str(bool(record["has_low_quality_evidence"])),
                    "contributing_variant_ids": ",".join(sorted(record["variant_ids"])),
                }
            )
            rows_written += 1

    return rows_written


def _write_summary_json(path: Path, summary: dict[str, Any]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2, sort_keys=True)
        handle.write("\n")


def _get_stage07_artifacts(state: dict[str, Any]) -> tuple[Path, Path]:
    artifacts = state.get("artifacts", {})
    annotated_table = artifacts.get("annotated_table") or artifacts.get("annotated_tsv")
    annotated_vcf = artifacts.get("annotated_vcf")

    input_tsv = _validate_required_file(annotated_table, "Stage 07 annotated TSV")
    input_vcf = _validate_required_file(annotated_vcf, "Stage 07 annotated VCF")

    return input_tsv, input_vcf


def run_stage(
    config: dict[str, Any],
    paths: dict[str, Any],
    logger,
    state: dict[str, Any],
) -> dict[str, Any]:
    _log(logger, "info", "Stage 08: filtering and partitioning annotated variants.")

    input_tsv, input_vcf = _get_stage07_artifacts(state)
    processed_dir = Path(paths["processed_dir"])
    processed_dir.mkdir(parents=True, exist_ok=True)

    output_paths = _prepare_output_paths(processed_dir)

    annotation_source = str(config.get("annotation", {}).get("engine", "VEP")).strip().upper()
    if annotation_source == "":
        annotation_source = "VEP"
    annotation_version = _get_annotation_version(config, state)

    _log(logger, "info", f"Stage 08 canonical input TSV: {input_tsv}")
    _log(logger, "info", f"Stage 08 validation/provenance VCF: {input_vcf}")
    _log(logger, "info", f"Stage 08 annotation_source: {annotation_source}")
    _log(logger, "info", f"Stage 08 annotation_version: {annotation_version}")

    summary_counts = {
        "variants_by_context": Counter(),
        "variants_by_severity": Counter(),
        "qc_status_counts": Counter(),
        "interpretability_counts": Counter(),
        "frequency_status": Counter(),
        "clinical_status": Counter(),
        "variants_by_variant_type": Counter(),
        "variants_by_variant_class": Counter(),
    }

    total_rows = 0
    irreparably_malformed_rows = 0
    partition_counts = Counter()

    variant_aggregates: dict[str, dict[str, Any]] = {}
    rdgp_aggregates: dict[tuple[str, str, str], dict[str, Any]] = {}

    with input_tsv.open("r", encoding="utf-8", errors="replace", newline="") as in_handle, \
        output_paths["selected_transcript_consequences"].open("w", encoding="utf-8", newline="") as selected_handle, \
        output_paths["vdb_ready_variants"].open("w", encoding="utf-8", newline="") as vdb_handle, \
        output_paths["coding_candidates"].open("w", encoding="utf-8", newline="") as coding_handle, \
        output_paths["splice_region_candidates"].open("w", encoding="utf-8", newline="") as splice_handle, \
        output_paths["noncoding_candidates"].open("w", encoding="utf-8", newline="") as noncoding_handle, \
        output_paths["qc_flagged"].open("w", encoding="utf-8", newline="") as qc_handle:

        reader = csv.DictReader(in_handle, delimiter="\t")
        _validate_input_header(reader.fieldnames, input_tsv)

        selected_writer = csv.DictWriter(selected_handle, fieldnames=SELECTED_TRANSCRIPT_COLUMNS, delimiter="\t")
        vdb_writer = csv.DictWriter(vdb_handle, fieldnames=VDB_READY_COLUMNS, delimiter="\t")
        coding_writer = csv.DictWriter(coding_handle, fieldnames=SELECTED_TRANSCRIPT_COLUMNS, delimiter="\t")
        splice_writer = csv.DictWriter(splice_handle, fieldnames=SELECTED_TRANSCRIPT_COLUMNS, delimiter="\t")
        noncoding_writer = csv.DictWriter(noncoding_handle, fieldnames=SELECTED_TRANSCRIPT_COLUMNS, delimiter="\t")
        qc_writer = csv.DictWriter(qc_handle, fieldnames=SELECTED_TRANSCRIPT_COLUMNS, delimiter="\t")

        for writer in [selected_writer, vdb_writer, coding_writer, splice_writer, noncoding_writer, qc_writer]:
            writer.writeheader()

        for input_row in reader:
            try:
                row, partition_contexts = _coerce_stage08_row(
                    input_row=input_row,
                    annotation_source=annotation_source,
                    annotation_version=annotation_version,
                )
            except Exception as exc:
                irreparably_malformed_rows += 1
                _log(logger, "warning", f"Irreparably malformed Stage 08 row skipped: {exc}")
                continue

            total_rows += 1

            selected_writer.writerow({column: row[column] for column in SELECTED_TRANSCRIPT_COLUMNS})
            vdb_writer.writerow({column: row[column] for column in VDB_READY_COLUMNS})

            if "coding" in partition_contexts:
                coding_writer.writerow({column: row[column] for column in SELECTED_TRANSCRIPT_COLUMNS})
                partition_counts["coding_candidates"] += 1

            if "splice_region" in partition_contexts:
                splice_writer.writerow({column: row[column] for column in SELECTED_TRANSCRIPT_COLUMNS})
                partition_counts["splice_region_candidates"] += 1

            if partition_contexts & {"regulatory", "intronic", "intergenic", "noncoding_transcript", "unknown"}:
                noncoding_writer.writerow({column: row[column] for column in SELECTED_TRANSCRIPT_COLUMNS})
                partition_counts["noncoding_candidates"] += 1

            if row["qc_status"] != "pass":
                qc_writer.writerow({column: row[column] for column in SELECTED_TRANSCRIPT_COLUMNS})
                partition_counts["qc_flagged"] += 1

            summary_counts["variants_by_context"][row["variant_context"]] += 1
            summary_counts["variants_by_severity"][row["variant_effect_severity"]] += 1
            summary_counts["qc_status_counts"][row["qc_status"]] += 1
            summary_counts["interpretability_counts"][row["interpretability_status"]] += 1
            summary_counts["frequency_status"][row["frequency_status"]] += 1
            summary_counts["clinical_status"][row["clinical_status"]] += 1
            summary_counts["variants_by_variant_type"][row["variant_type"]] += 1
            summary_counts["variants_by_variant_class"][row["variant_class"]] += 1

            _update_variant_aggregates(variant_aggregates, row, partition_contexts)
            _update_rdgp_aggregates(rdgp_aggregates, row)

    variant_summary_count = _write_variant_summary(
        output_paths["variant_summary"],
        variant_aggregates,
    )
    rdgp_seed_count = _write_rdgp_seed(
        output_paths["rdgp_gene_evidence_seed"],
        rdgp_aggregates,
    )

    summary = {
        "total_variants": total_rows,
        "irreparably_malformed_rows": irreparably_malformed_rows,
        "variants_by_context": dict(sorted(summary_counts["variants_by_context"].items())),
        "variants_by_severity": dict(sorted(summary_counts["variants_by_severity"].items())),
        "qc_status_counts": dict(sorted(summary_counts["qc_status_counts"].items())),
        "interpretability_counts": dict(sorted(summary_counts["interpretability_counts"].items())),
        "frequency_status": dict(sorted(summary_counts["frequency_status"].items())),
        "clinical_status": dict(sorted(summary_counts["clinical_status"].items())),
        "variants_by_variant_type": dict(sorted(summary_counts["variants_by_variant_type"].items())),
        "variants_by_variant_class": dict(sorted(summary_counts["variants_by_variant_class"].items())),
        "partition_counts": dict(sorted(partition_counts.items())),
        "variant_summary_rows": variant_summary_count,
        "rdgp_gene_evidence_seed_rows": rdgp_seed_count,
        "annotation_source": annotation_source,
        "annotation_version": annotation_version,
        "assumptions": [
            "VAP v1 treats Stage 07 annotated_variants.tsv as canonical selected-transcript truth.",
            "Full CSQ expansion from annotated_variants.vcf is deferred to a future VAP v2 mode.",
            "canonical_present is emitted as False because Stage 07 TSV does not expose CANONICAL in v1.",
            "RDGP gene evidence seed groups by gene_id when available, otherwise by gene_symbol when gene_id is missing but gene_symbol is mapped.",
            "population_frequency is recomputed as max(non-missing gnomad_af, exac_af, thousand_genomes_af).",
        ],
    }
    _write_summary_json(output_paths["summary_json"], summary)

    state.setdefault("artifacts", {})
    state["artifacts"]["stage_08_selected_transcript_consequences"] = str(output_paths["selected_transcript_consequences"])
    state["artifacts"]["stage_08_variant_summary"] = str(output_paths["variant_summary"])
    state["artifacts"]["coding_candidates"] = str(output_paths["coding_candidates"])
    state["artifacts"]["splice_region_candidates"] = str(output_paths["splice_region_candidates"])
    state["artifacts"]["noncoding_candidates"] = str(output_paths["noncoding_candidates"])
    state["artifacts"]["qc_flagged"] = str(output_paths["qc_flagged"])
    state["artifacts"]["stage_08_summary_json"] = str(output_paths["summary_json"])
    state["artifacts"]["stage_08_vdb_ready_variants"] = str(output_paths["vdb_ready_variants"])
    state["artifacts"]["stage_08_rdgp_gene_evidence_seed"] = str(output_paths["rdgp_gene_evidence_seed"])

    state.setdefault("qc", {})
    state["qc"]["stage_08_qc"] = {
        "total_variants": total_rows,
        "irreparably_malformed_rows": irreparably_malformed_rows,
        "selected_transcript_consequences_exists": output_paths["selected_transcript_consequences"].exists(),
        "variant_summary_exists": output_paths["variant_summary"].exists(),
        "vdb_ready_variants_exists": output_paths["vdb_ready_variants"].exists(),
        "rdgp_gene_evidence_seed_exists": output_paths["rdgp_gene_evidence_seed"].exists(),
        "qc_status_counts": dict(sorted(summary_counts["qc_status_counts"].items())),
    }

    state.setdefault("stage_outputs", {})
    state["stage_outputs"]["stage_08_filter_and_partition"] = {
        "status": "success",
        "input_annotated_table": str(input_tsv),
        "input_annotated_vcf": str(input_vcf),
        "outputs": {key: str(value) for key, value in output_paths.items()},
        "total_variants": total_rows,
        "variant_summary_rows": variant_summary_count,
        "rdgp_gene_evidence_seed_rows": rdgp_seed_count,
        "irreparably_malformed_rows": irreparably_malformed_rows,
    }

    _log(logger, "info", f"Stage 08 selected transcript consequences written to: {output_paths['selected_transcript_consequences']}")
    _log(logger, "info", f"Stage 08 variant summary written to: {output_paths['variant_summary']}")
    _log(logger, "info", f"Stage 08 VDB-ready variants written to: {output_paths['vdb_ready_variants']}")
    _log(logger, "info", f"Stage 08 RDGP gene evidence seed written to: {output_paths['rdgp_gene_evidence_seed']}")
    _log(logger, "info", f"Stage 08 summary JSON written to: {output_paths['summary_json']}")
    _log(logger, "info", f"Stage 08 total variants processed: {total_rows}")
    _log(logger, "info", f"Stage 08 irreparably malformed rows skipped: {irreparably_malformed_rows}")

    return state