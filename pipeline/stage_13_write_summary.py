"""
Stage 13: Write final run summary outputs.

Repo 2 v1.0 design notes:
- inputs:
  - accumulated state
  - prioritized_variants.tsv
  - gene_summary.tsv
  - validation outputs
- outputs:
  - run_summary.md
  - prioritized_variant_summary.tsv
- this is the terminal stage of the single-sample pipeline
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd


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


def _safe_int(value: Any) -> int:
    """
    Convert a value to int where possible, else 0.
    """
    try:
        return int(value)
    except Exception:
        return 0


def _load_table_if_present(path_str: str | None) -> pd.DataFrame:
    """
    Load a TSV if present, else return empty DataFrame.
    """
    path = _optional_file(path_str)
    if path is None:
        return pd.DataFrame()
    return pd.read_csv(path, sep="\t", dtype=str).fillna("NA")


def _write_summary_markdown(
    output_path: Path,
    state: dict[str, Any],
    prioritized_df: pd.DataFrame,
    gene_df: pd.DataFrame,
) -> int:
    """
    Write human-readable markdown summary.

    Returns
    -------
    int
        Number of lines written.
    """
    run_info = state["run"]
    sample_info = state["sample"]
    qc = state.get("qc", {})
    stage_outputs = state.get("stage_outputs", {})
    warnings = state.get("warnings", [])
    errors = state.get("errors", [])

    input_qc = qc.get("input_qc", {})
    alignment_qc = qc.get("alignment_qc", {})
    bam_qc = qc.get("bam_processing_qc", {})
    variant_qc = qc.get("variant_calling_qc", {})
    normalization_qc = qc.get("normalization_qc", {})
    annotation_qc = qc.get("annotation_qc", {})
    filtering_qc = qc.get("filtering_qc", {})
    interpretation_qc = qc.get("interpretation_qc", {})
    validation_qc = qc.get("validation_qc", {})

    priority_counts = {}
    if not prioritized_df.empty and "priority_label" in prioritized_df.columns:
        priority_counts = prioritized_df["priority_label"].value_counts(dropna=False).to_dict()

    lines: list[str] = []
    lines.append("# Run Summary")
    lines.append("")
    lines.append("## Run Metadata")
    lines.append("")
    lines.append(f"- run_id: {run_info.get('run_id', 'NA')}")
    lines.append(f"- status: {run_info.get('status', 'NA')}")
    lines.append(f"- pipeline_name: {run_info.get('pipeline_name', 'NA')}")
    lines.append(f"- pipeline_version: {run_info.get('pipeline_version', 'NA')}")
    lines.append(f"- execution_mode: {run_info.get('execution_mode', 'NA')}")
    lines.append(f"- machine_id: {run_info.get('machine_id', 'NA')}")
    lines.append(f"- start_time: {run_info.get('start_time', 'NA')}")
    lines.append(f"- end_time: {run_info.get('end_time', 'NA')}")
    lines.append("")

    lines.append("## Sample Metadata")
    lines.append("")
    lines.append(f"- sample_id: {sample_info.get('sample_id', 'NA')}")
    lines.append(f"- sample_alias: {sample_info.get('sample_alias', 'NA')}")
    lines.append(f"- bioproject_accession: {sample_info.get('bioproject_accession', 'NA')}")
    lines.append(f"- sra_accession: {sample_info.get('sra_accession', 'NA')}")
    lines.append(f"- reference_genome: {sample_info.get('reference_genome', 'NA')}")
    lines.append(f"- assay_type: {sample_info.get('assay_type', 'NA')}")
    lines.append("")

    lines.append("## Input Summary")
    lines.append("")
    lines.append(f"- input_validation_passed: {input_qc.get('input_validation_passed', 'NA')}")
    lines.append(f"- file_count: {input_qc.get('file_count', 'NA')}")
    lines.append(f"- validation_check_count: {input_qc.get('validation_check_count', 'NA')}")
    lines.append(f"- gene_set_check_count: {input_qc.get('gene_set_check_count', 'NA')}")
    lines.append("")

    lines.append("## Alignment and BAM Processing")
    lines.append("")
    lines.append(f"- read_count_r1: {alignment_qc.get('read_count_r1', 'NA')}")
    lines.append(f"- read_count_r2: {alignment_qc.get('read_count_r2', 'NA')}")
    lines.append(f"- mapping_rate: {alignment_qc.get('mapping_rate', 'NA')}")
    lines.append(f"- properly_paired_rate: {alignment_qc.get('properly_paired_rate', 'NA')}")
    lines.append(f"- aligned_bam_exists: {alignment_qc.get('aligned_bam_exists', 'NA')}")
    lines.append(f"- sorted_bam_exists: {bam_qc.get('sorted_bam_exists', 'NA')}")
    lines.append(f"- bam_index_exists: {bam_qc.get('bam_index_exists', 'NA')}")
    lines.append("")

    lines.append("## Variant Calling and Normalization")
    lines.append("")
    lines.append(f"- variant_count: {variant_qc.get('variant_count', 'NA')}")
    lines.append(f"- normalized_variant_count: {normalization_qc.get('normalized_variant_count', 'NA')}")
    lines.append(f"- malformed_records_skipped: {normalization_qc.get('malformed_records_skipped', 'NA')}")
    lines.append("")

    lines.append("## Annotation Summary")
    lines.append("")
    lines.append(f"- annotation_completed: {annotation_qc.get('annotation_completed', 'NA')}")
    lines.append(f"- annotated_variant_count: {annotation_qc.get('annotated_variant_count', 'NA')}")
    lines.append(f"- required_fields_present: {annotation_qc.get('required_fields_present', 'NA')}")
    lines.append(f"- mitocarta_gene_count: {annotation_qc.get('mitocarta_gene_count', 'NA')}")
    lines.append(f"- genes4epilepsy_gene_count: {annotation_qc.get('genes4epilepsy_gene_count', 'NA')}")
    lines.append(f"- unresolved_symbol_count: {annotation_qc.get('unresolved_symbol_count', 'NA')}")
    lines.append("")

    lines.append("## Filtering and Track Partitioning")
    lines.append("")
    lines.append(f"- filtered_count: {filtering_qc.get('filtered_count', 'NA')}")
    lines.append(f"- coding_count: {filtering_qc.get('coding_count', 'NA')}")
    lines.append(f"- noncoding_count: {filtering_qc.get('noncoding_count', 'NA')}")
    lines.append("")

    lines.append("## Interpretation and Prioritization")
    lines.append("")
    lines.append(f"- coding_variant_count: {interpretation_qc.get('coding_variant_count', 'NA')}")
    lines.append(f"- noncoding_variant_count: {interpretation_qc.get('noncoding_variant_count', 'NA')}")
    lines.append(f"- prioritized_variant_count: {interpretation_qc.get('prioritized_variant_count', 'NA')}")
    lines.append(f"- prioritized_gene_count: {interpretation_qc.get('prioritized_gene_count', 'NA')}")
    lines.append("")

    lines.append("### Priority Label Counts")
    lines.append("")
    if priority_counts:
        for key, value in priority_counts.items():
            lines.append(f"- {key}: {value}")
    else:
        lines.append("- none")
    lines.append("")

    lines.append("## Validation Summary")
    lines.append("")
    lines.append(f"- validation_completed: {validation_qc.get('validation_completed', 'NA')}")
    lines.append(f"- manual_igv_review_required: {validation_qc.get('manual_igv_review_required', 'NA')}")
    lines.append(f"- candidate_count: {validation_qc.get('candidate_count', 'NA')}")
    lines.append(f"- benchmark_comparison_completed: {validation_qc.get('benchmark_comparison_completed', 'NA')}")
    lines.append(f"- benchmark_variant_count: {validation_qc.get('benchmark_variant_count', 'NA')}")
    lines.append("")

    lines.append("## Stage Status")
    lines.append("")
    for stage_name, payload in stage_outputs.items():
        lines.append(f"- {stage_name}: {payload.get('status', 'NA')}")
    lines.append("")

    lines.append("## Artifact Paths")
    lines.append("")
    for key, value in state.get("artifacts", {}).items():
        lines.append(f"- {key}: {value}")
    lines.append("")

    lines.append("## Warnings")
    lines.append("")
    if warnings:
        for warning in warnings:
            lines.append(f"- {warning}")
    else:
        lines.append("- none")
    lines.append("")

    lines.append("## Errors")
    lines.append("")
    if errors:
        for error in errors:
            lines.append(f"- {error}")
    else:
        lines.append("- none")
    lines.append("")

    with output_path.open("w", encoding="utf-8") as handle:
        handle.write("\n".join(lines) + "\n")

    return len(lines)


def _build_prioritized_variant_summary(prioritized_df: pd.DataFrame) -> pd.DataFrame:
    """
    Build a compact summary table from prioritized variants.

    Returns
    -------
    pd.DataFrame
        Summary dataframe.
    """
    if prioritized_df.empty:
        return pd.DataFrame(
            columns=[
                "metric",
                "value",
            ]
        )

    summary_rows: list[dict[str, Any]] = []

    summary_rows.append({"metric": "variant_count_total", "value": len(prioritized_df)})

    if "priority_label" in prioritized_df.columns:
        counts = prioritized_df["priority_label"].value_counts(dropna=False).to_dict()
        for label, value in counts.items():
            summary_rows.append({"metric": f"priority_label_{label}", "value": value})

    if "track" in prioritized_df.columns:
        track_counts = prioritized_df["track"].value_counts(dropna=False).to_dict()
        for label, value in track_counts.items():
            summary_rows.append({"metric": f"track_{label}", "value": value})

    if "gene_symbol" in prioritized_df.columns:
        gene_count = prioritized_df["gene_symbol"].replace("NA", pd.NA).dropna().nunique()
        summary_rows.append({"metric": "unique_gene_count", "value": gene_count})

    if "mito_flag" in prioritized_df.columns:
        mito_count = int((prioritized_df["mito_flag"] == "True").sum())
        summary_rows.append({"metric": "mitochondrial_flagged_variants", "value": mito_count})

    if "epilepsy_flag" in prioritized_df.columns:
        epilepsy_count = int((prioritized_df["epilepsy_flag"] == "True").sum())
        summary_rows.append({"metric": "epilepsy_flagged_variants", "value": epilepsy_count})

    return pd.DataFrame(summary_rows)


def run_stage(
    config: dict[str, Any],
    paths: dict[str, Any],
    logger,
    state: dict[str, Any],
) -> dict[str, Any]:
    """
    Execute Stage 13.

    Responsibilities
    ----------------
    - collect run outputs and QC summaries
    - write human-readable run_summary.md
    - write compact prioritized_variant_summary.tsv
    - update reports, artifacts, QC, and stage outputs
    """
    logger.info("Stage 13: writing final summary outputs.")

    reports_dir = Path(paths["reports_dir"])
    run_summary_report = reports_dir / "run_summary.md"
    prioritized_variant_summary = reports_dir / "prioritized_variant_summary.tsv"

    prioritized_df = _load_table_if_present(state["artifacts"].get("prioritized_table"))
    gene_df = _load_table_if_present(state["artifacts"].get("gene_summary_table"))

    report_line_count = _write_summary_markdown(
        output_path=run_summary_report,
        state=state,
        prioritized_df=prioritized_df,
        gene_df=gene_df,
    )

    summary_df = _build_prioritized_variant_summary(prioritized_df)
    summary_df.to_csv(prioritized_variant_summary, sep="\t", index=False)

    state["artifacts"]["run_summary_report"] = str(run_summary_report)
    state["reports"]["run_summary_report"] = str(run_summary_report)
    state["reports"]["summary_table"] = str(prioritized_variant_summary)
    state["reports"]["report_line_count"] = report_line_count

    state["stage_outputs"]["stage_13_write_summary"] = {
        "status": "success",
        "run_summary_report": str(run_summary_report),
        "prioritized_variant_summary": str(prioritized_variant_summary),
        "report_line_count": report_line_count,
        "summary_row_count": int(len(summary_df)),
    }

    logger.info(f"Run summary report written to: {run_summary_report}")
    logger.info(f"Prioritized variant summary written to: {prioritized_variant_summary}")
    logger.info(f"Run summary line count: {report_line_count}")

    return state