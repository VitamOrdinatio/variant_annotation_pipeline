"""
Stage 12: Prepare variants for validation and optional manual IGV review.

Repo 2 v1.0 design notes:
- input:
  - prioritized_variants.tsv
  - sorted BAM / BAI
  - normalized VCF
  - optional GIAB benchmark resources
- outputs:
  - validation_notes.md
  - igv_review_candidates.tsv
- IGV review is not automated; this stage prepares a structured handoff
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd


def _validate_required_artifact(path_str: str | None, label: str) -> Path:
    """
    Validate that a required upstream artifact exists.
    """
    if not path_str:
        raise ValueError(f"Missing required upstream artifact for {label}")
    path = Path(path_str)
    if not path.exists():
        raise FileNotFoundError(f"Required upstream artifact not found for {label}: {path}")
    if not path.is_file():
        raise FileNotFoundError(f"Expected file for {label}, but found non-file path: {path}")
    return path


def _optional_file(path_str: str | None) -> Path | None:
    """
    Return a Path if present and existing, else None.
    """
    if not path_str:
        return None
    path = Path(path_str)
    if path.exists() and path.is_file():
        return path
    return None


def _count_vcf_variants(vcf_path: Path) -> int:
    """
    Count non-header VCF records.
    """
    count = 0
    with vcf_path.open("r", encoding="utf-8", errors="replace") as handle:
        for line in handle:
            if line.startswith("#"):
                continue
            if line.strip():
                count += 1
    return count


def _build_review_reason(row: pd.Series) -> str:
    """
    Build a compact validation reason for IGV review.
    """
    reasons: list[str] = []

    priority_label = str(row.get("priority_label", "NA"))
    if priority_label == "high":
        reasons.append("high_priority")
    elif priority_label == "medium":
        reasons.append("medium_priority")

    clinvar_bucket = str(row.get("clinvar_bucket", "unknown"))
    if clinvar_bucket in {"pathogenic", "likely_pathogenic", "vus"}:
        reasons.append(f"clinvar={clinvar_bucket}")

    if str(row.get("mito_flag", "False")) == "True":
        reasons.append("mitochondrial_gene")
    if str(row.get("epilepsy_flag", "False")) == "True":
        reasons.append("epilepsy_gene")

    functional_class = str(row.get("functional_class", "NA"))
    noncoding_class = str(row.get("noncoding_class", "NA"))

    if functional_class not in {"NA", "unknown"}:
        reasons.append(f"functional_class={functional_class}")
    elif noncoding_class not in {"NA", "unknown"}:
        reasons.append(f"noncoding_class={noncoding_class}")

    return ";".join(reasons) if reasons else "manual_review_recommended"


def _write_validation_notes(
    output_path: Path,
    state: dict[str, Any],
    candidate_count: int,
    benchmark_variant_count: int | None,
    benchmark_available: bool,
) -> None:
    """
    Write a human-readable validation note file.
    """
    run_info = state["run"]
    sample_info = state["sample"]

    with output_path.open("w", encoding="utf-8") as handle:
        handle.write("# Validation Notes\n\n")
        handle.write(f"- run_id: {run_info['run_id']}\n")
        handle.write(f"- sample_id: {sample_info['sample_id']}\n")
        handle.write(f"- sample_alias: {sample_info['sample_alias']}\n")
        handle.write(f"- sra_accession: {sample_info['sra_accession']}\n")
        handle.write(f"- reference_genome: {sample_info['reference_genome']}\n\n")

        handle.write("## Validation Scope\n\n")
        handle.write("- This stage prepares candidate variants for optional manual IGV review.\n")
        handle.write("- IGV review is not automated by the pipeline.\n")
        handle.write("- Candidate selection is driven by priority label, ClinVar context, and overlay membership.\n\n")

        handle.write("## Candidate Summary\n\n")
        handle.write(f"- IGV review candidates: {candidate_count}\n\n")

        handle.write("## Benchmark Context\n\n")
        if benchmark_available:
            handle.write("- GIAB benchmark resources detected.\n")
            handle.write(f"- Benchmark VCF variant count: {benchmark_variant_count}\n")
            handle.write("- v1 benchmark integration is currently summary-oriented and not yet a full concordance engine.\n\n")
        else:
            handle.write("- GIAB benchmark resources not available or not enabled.\n")
            handle.write("- Benchmark comparison was skipped.\n\n")

        handle.write("## Manual IGV Review Guidance\n\n")
        handle.write("Inspect the following when reviewing candidates in IGV:\n\n")
        handle.write("- read depth\n")
        handle.write("- allele balance\n")
        handle.write("- strand representation\n")
        handle.write("- local alignment context\n")
        handle.write("- nearby mapping artifacts\n\n")

        handle.write("## Upstream Artifacts\n\n")
        handle.write(f"- sorted_bam: {state['artifacts'].get('sorted_bam', 'NA')}\n")
        handle.write(f"- sorted_bam_index: {state['artifacts'].get('sorted_bam_index', 'NA')}\n")
        handle.write(f"- normalized_vcf: {state['artifacts'].get('normalized_vcf', 'NA')}\n")
        handle.write(f"- prioritized_table: {state['artifacts'].get('prioritized_table', 'NA')}\n")


def run_stage(
    config: dict[str, Any],
    paths: dict[str, Any],
    logger,
    state: dict[str, Any],
) -> dict[str, Any]:
    """
    Execute Stage 12.

    Responsibilities
    ----------------
    - read prioritized_variants.tsv
    - build IGV review candidate list
    - capture benchmark resource availability
    - write validation notes
    - update artifacts, QC, and stage outputs
    """
    logger.info("Stage 12: preparing validation outputs and IGV review handoff.")

    prioritized_table = _validate_required_artifact(
        state["artifacts"].get("prioritized_table"),
        "prioritized variant table",
    )
    sorted_bam = _validate_required_artifact(
        state["artifacts"].get("sorted_bam"),
        "sorted BAM",
    )
    sorted_bam_index = _validate_required_artifact(
        state["artifacts"].get("sorted_bam_index"),
        "sorted BAM index",
    )
    normalized_vcf = _validate_required_artifact(
        state["artifacts"].get("normalized_vcf"),
        "normalized VCF",
    )

    sample_id = state["sample"]["sample_id"]
    run_id = state["run"]["run_id"]

    validation_notes = Path(paths["validation_dir"]) / "validation_notes.md"
    igv_candidates = Path(paths["validation_dir"]) / "igv_review_candidates.tsv"

    df = pd.read_csv(prioritized_table, sep="\t", dtype=str).fillna("NA")

    if df.empty:
        logger.warning("Prioritized variant table is empty. Writing empty validation outputs.")

    required_columns = [
        "chromosome",
        "position",
        "reference_allele",
        "alternate_allele",
        "gene_symbol",
        "priority_label",
        "track",
        "mito_flag",
        "epilepsy_flag",
    ]
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(
            "Prioritized variant table is missing required columns: " + ", ".join(missing_columns)
        )

    if "clinvar_bucket" not in df.columns:
        df["clinvar_bucket"] = "unknown"
    if "functional_class" not in df.columns:
        df["functional_class"] = "NA"
    if "noncoding_class" not in df.columns:
        df["noncoding_class"] = "NA"
    if "priority_score" not in df.columns:
        df["priority_score"] = "NA"

    candidate_df = df[df["priority_label"].isin(["high", "medium"])].copy()

    if candidate_df.empty and not df.empty:
        logger.info("No high/medium priority variants found; no IGV review candidates will be emitted.")

    candidate_df["reason_for_review"] = candidate_df.apply(_build_review_reason, axis=1)
    candidate_df["bam_path"] = str(sorted_bam)
    candidate_df["bai_path"] = str(sorted_bam_index)
    candidate_df["normalized_vcf_path"] = str(normalized_vcf)
    candidate_df["sample_id"] = sample_id
    candidate_df["run_id"] = run_id

    candidate_columns = [
        "sample_id",
        "run_id",
        "chromosome",
        "position",
        "reference_allele",
        "alternate_allele",
        "gene_symbol",
        "gene_id" if "gene_id" in candidate_df.columns else None,
        "track",
        "priority_label",
        "priority_score",
        "reason_for_review",
        "bam_path",
        "bai_path",
        "normalized_vcf_path",
    ]
    candidate_columns = [col for col in candidate_columns if col is not None]

    candidate_df.to_csv(igv_candidates, sep="\t", index=False, columns=candidate_columns)

    benchmark_available = False
    benchmark_variant_count: int | None = None

    if bool(config["validation"].get("enable_validation", False)):
        benchmark_vcf = _optional_file(config["validation"].get("giab_benchmark_vcf"))
        benchmark_index = _optional_file(config["validation"].get("giab_benchmark_index"))
        benchmark_bed = _optional_file(config["validation"].get("giab_benchmark_bed"))

        if benchmark_vcf is not None and benchmark_index is not None and benchmark_bed is not None:
            benchmark_available = True
            benchmark_variant_count = _count_vcf_variants(benchmark_vcf)
            logger.info(f"GIAB benchmark resources detected: {benchmark_vcf}")
        else:
            logger.warning("GIAB benchmark validation enabled, but one or more benchmark files are missing.")
            state["warnings"].append(
                "GIAB benchmark validation enabled, but one or more benchmark files are missing."
            )

    _write_validation_notes(
        output_path=validation_notes,
        state=state,
        candidate_count=int(len(candidate_df)),
        benchmark_variant_count=benchmark_variant_count,
        benchmark_available=benchmark_available,
    )

    state["artifacts"]["validation_notes"] = str(validation_notes)
    state["artifacts"]["igv_review_candidates"] = str(igv_candidates)

    state["qc"]["validation_qc"] = {
        "validation_completed": True,
        "manual_igv_review_required": bool(int(len(candidate_df)) > 0),
        "candidate_count": int(len(candidate_df)),
        "benchmark_comparison_completed": benchmark_available,
        "benchmark_variant_count": benchmark_variant_count,
        "sorted_bam_exists": True,
        "sorted_bam_index_exists": True,
        "normalized_vcf_exists": True,
    }

    state["stage_outputs"]["stage_12_validate_variants"] = {
        "status": "success",
        "input_prioritized_table": str(prioritized_table),
        "validation_notes": str(validation_notes),
        "igv_review_candidates": str(igv_candidates),
        "candidate_count": int(len(candidate_df)),
        "benchmark_comparison_completed": benchmark_available,
        "benchmark_variant_count": benchmark_variant_count,
    }

    logger.info(f"Validation notes written to: {validation_notes}")
    logger.info(f"IGV review candidate table written to: {igv_candidates}")
    logger.info(f"IGV review candidate count: {len(candidate_df)}")

    return state