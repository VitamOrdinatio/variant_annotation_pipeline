"""
Stage 11: Prioritize variants across coding and non-coding tracks.

Repo 2 v1.0 design notes:
- inputs:
  - interpreted_coding.tsv
  - interpreted_noncoding.tsv
- outputs:
  - prioritized_variants.tsv
  - gene_summary.tsv
- prioritization is rule-based and uses:
  - predicted severity
  - ClinVar bucket
  - rarity
  - mito/epilepsy overlays
- no AI tools are used in v1
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd


def _validate_required_artifact(path_str: str | None, label: str) -> Path:
    """
    Validate that a required upstream artifact exists.

    Parameters
    ----------
    path_str : str | None
        Path string.
    label : str
        Human-readable label.

    Returns
    -------
    Path
        Validated path.

    Raises
    ------
    ValueError
        If missing.
    FileNotFoundError
        If path does not exist.
    """
    if not path_str:
        raise ValueError(f"Missing required upstream artifact for {label}")
    path = Path(path_str)
    if not path.exists():
        raise FileNotFoundError(f"Required upstream artifact not found for {label}: {path}")
    if not path.is_file():
        raise FileNotFoundError(f"Expected file for {label}, but found non-file path: {path}")
    return path


def _severity_score(value: str) -> int:
    """
    Map predicted severity to a numeric base score.
    """
    mapping = {
        "high": 3,
        "medium": 2,
        "low": 1,
    }
    return mapping.get(str(value).strip().lower(), 0)


def _clinvar_bonus(value: str) -> int:
    """
    Map ClinVar bucket to a prioritization bonus.
    """
    mapping = {
        "pathogenic": 3,
        "likely_pathogenic": 2,
        "vus": 1,
        "unknown": 0,
        "other": 0,
        "likely_benign": -1,
        "benign": -2,
    }
    return mapping.get(str(value).strip().lower(), 0)


def _rarity_bonus(value: str) -> int:
    """
    Map rarity label to a prioritization bonus.
    """
    mapping = {
        "ultra_rare": 2,
        "rare": 2,
        "unknown": 1,
        "low_frequency": 0,
        "common": -2,
    }
    return mapping.get(str(value).strip().lower(), 0)


def _flag_bonus(value: str) -> int:
    """
    Convert boolean-like overlay flags to score contribution.
    """
    return 1 if str(value).strip() == "True" else 0


def _final_priority_label(score: int) -> str:
    """
    Convert numeric score to final priority label.
    """
    if score >= 7:
        return "high"
    if score >= 4:
        return "medium"
    return "low"


def _build_prioritization_basis(row: pd.Series) -> str:
    """
    Build a compact semicolon-delimited prioritization rationale.
    """
    parts: list[str] = []

    parts.append(f"track={row.get('track', 'unknown')}")
    parts.append(f"severity={row.get('predicted_severity', 'unknown')}")

    clinvar_bucket = str(row.get("clinvar_bucket", "unknown"))
    if clinvar_bucket not in {"unknown", "other"}:
        parts.append(f"clinvar={clinvar_bucket}")

    rarity = str(row.get("rarity_label", "unknown"))
    parts.append(f"rarity={rarity}")

    if str(row.get("mito_flag", "False")) == "True":
        parts.append("mitochondrial_gene")
    if str(row.get("epilepsy_flag", "False")) == "True":
        parts.append("epilepsy_gene")

    parts.append(f"score={row.get('priority_score', 'NA')}")

    return ";".join(parts)


def _ensure_column(df: pd.DataFrame, column: str, default: str = "NA") -> pd.DataFrame:
    """
    Ensure a column exists in a DataFrame.
    """
    if column not in df.columns:
        df[column] = default
    return df


def run_stage(
    config: dict[str, Any],
    paths: dict[str, Any],
    logger,
    state: dict[str, Any],
) -> dict[str, Any]:
    """
    Execute Stage 11.

    Responsibilities
    ----------------
    - read interpreted coding and non-coding tables
    - assign unified cross-track priority scores
    - emit prioritized_variants.tsv
    - emit gene_summary.tsv
    - update artifacts, QC, and stage outputs
    """
    logger.info("Stage 11: prioritizing variants across tracks.")

    interpreted_coding_table = _validate_required_artifact(
        state["artifacts"].get("interpreted_coding_table"),
        "interpreted coding table",
    )
    interpreted_noncoding_table = _validate_required_artifact(
        state["artifacts"].get("interpreted_noncoding_table"),
        "interpreted non-coding table",
    )

    prioritized_table = Path(paths["final_dir"]) / "prioritized_variants.tsv"
    gene_summary_table = Path(paths["final_dir"]) / "gene_summary.tsv"

    coding_df = pd.read_csv(interpreted_coding_table, sep="\t", dtype=str).fillna("NA")
    noncoding_df = pd.read_csv(interpreted_noncoding_table, sep="\t", dtype=str).fillna("NA")

    coding_df["track"] = "coding"
    noncoding_df["track"] = "non-coding"

    combined_df = pd.concat([coding_df, noncoding_df], ignore_index=True)

    if combined_df.empty:
        logger.warning("Both interpreted variant tables are empty. Writing empty prioritization outputs.")

    required_columns = [
        "gene_symbol",
        "predicted_severity",
        "clinvar_bucket",
        "rarity_label",
        "mito_flag",
        "epilepsy_flag",
        "track",
    ]
    missing_columns = [col for col in required_columns if col not in combined_df.columns]
    if missing_columns:
        raise ValueError(
            "Combined interpreted variant table is missing required columns: "
            + ", ".join(missing_columns)
        )

    optional_defaults = {
        "gene_id": "NA",
        "interpretation_notes": "NA",
        "severity_basis": "NA",
        "consequence": "NA",
        "variant_type": "NA",
        "chromosome": "NA",
        "position": "NA",
        "reference_allele": "NA",
        "alternate_allele": "NA",
    }
    for col, default in optional_defaults.items():
        combined_df = _ensure_column(combined_df, col, default=default)

    combined_df["priority_score"] = (
        combined_df["predicted_severity"].apply(_severity_score)
        + combined_df["clinvar_bucket"].apply(_clinvar_bonus)
        + combined_df["rarity_label"].apply(_rarity_bonus)
        + combined_df["mito_flag"].apply(_flag_bonus)
        + combined_df["epilepsy_flag"].apply(_flag_bonus)
    )

    combined_df["priority_label"] = combined_df["priority_score"].apply(_final_priority_label)
    combined_df["prioritization_basis"] = combined_df.apply(_build_prioritization_basis, axis=1)

    combined_df = combined_df.sort_values(
        by=[
            "priority_score",
            "predicted_severity",
            "gene_symbol",
            "chromosome",
            "position",
        ],
        ascending=[False, False, True, True, True],
        kind="mergesort",
    ).reset_index(drop=True)

    prioritized_columns = list(combined_df.columns)
    combined_df.to_csv(prioritized_table, sep="\t", index=False, columns=prioritized_columns)

    gene_df = combined_df.copy()
    gene_df["is_prioritized"] = gene_df["priority_label"].isin(["high", "medium"]).astype(int)

    grouped = (
        gene_df.groupby(["gene_symbol", "gene_id"], dropna=False)
        .agg(
            variant_count=("gene_symbol", "size"),
            prioritized_variant_count=("is_prioritized", "sum"),
            mito_flag=("mito_flag", lambda s: "True" if "True" in set(map(str, s)) else "False"),
            epilepsy_flag=("epilepsy_flag", lambda s: "True" if "True" in set(map(str, s)) else "False"),
        )
        .reset_index()
    )

    grouped = grouped.sort_values(
        by=["prioritized_variant_count", "variant_count", "gene_symbol"],
        ascending=[False, False, True],
        kind="mergesort",
    ).reset_index(drop=True)

    grouped.to_csv(gene_summary_table, sep="\t", index=False)

    prioritized_variant_count = int(len(combined_df))
    prioritized_gene_count = int(
        combined_df["gene_symbol"].replace("NA", pd.NA).dropna().nunique()
    )
    track_counts = combined_df["track"].value_counts(dropna=False).to_dict()
    priority_label_counts = combined_df["priority_label"].value_counts(dropna=False).to_dict()

    state["artifacts"]["prioritized_table"] = str(prioritized_table)
    state["artifacts"]["gene_summary_table"] = str(gene_summary_table)
    state["reports"]["gene_summary_table"] = str(gene_summary_table)

    interpretation_qc = state["qc"].setdefault("interpretation_qc", {})
    interpretation_qc.update(
        {
            "prioritization_completed": True,
            "prioritized_variant_count": prioritized_variant_count,
            "prioritized_gene_count": prioritized_gene_count,
            "track_counts": track_counts,
            "priority_label_counts": priority_label_counts,
        }
    )

    state["stage_outputs"]["stage_11_prioritize_variants"] = {
        "status": "success",
        "input_interpreted_coding_table": str(interpreted_coding_table),
        "input_interpreted_noncoding_table": str(interpreted_noncoding_table),
        "prioritized_table": str(prioritized_table),
        "gene_summary_table": str(gene_summary_table),
        "prioritized_variant_count": prioritized_variant_count,
        "prioritized_gene_count": prioritized_gene_count,
        "track_counts": track_counts,
        "priority_label_counts": priority_label_counts,
    }

    logger.info(f"Prioritized variant table written to: {prioritized_table}")
    logger.info(f"Gene summary table written to: {gene_summary_table}")
    logger.info(f"Prioritized variants: {prioritized_variant_count}")
    logger.info(f"Unique genes represented: {prioritized_gene_count}")

    return state