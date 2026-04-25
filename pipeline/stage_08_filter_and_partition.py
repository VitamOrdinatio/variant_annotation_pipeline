"""
Stage 08: Apply global filtering and partition variants into coding / non-coding tracks.

Repo 2 v1.0 design notes:

- input:
  - annotated_variants.tsv from Stage 07
- outputs:
  - filtered_variants.tsv
  - coding_variants.tsv
  - noncoding_variants.tsv
- filtering is intentionally conservative and config-driven
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


def _normalize_numeric_series(series: pd.Series) -> pd.Series:
    """
    Convert a string-like allele-frequency column into numeric values.

    Missing or non-numeric values become NaN.

    Parameters
    ----------
    series : pd.Series
        Input series.

    Returns
    -------
    pd.Series
        Numeric series.
    """
    normalized = (
        series.fillna("NA")
        .astype(str)
        .str.strip()
        .replace({"NA": pd.NA, "": pd.NA, ".": pd.NA, "-": pd.NA})
    )
    return pd.to_numeric(normalized, errors="coerce")


def _passes_af_filter(
    row: pd.Series,
    max_af_gnomad: float,
    max_af_exac: float,
    max_af_1000genomes: float,
) -> bool:
    """
    Evaluate allele-frequency thresholds for a single variant row.

    Missing frequencies are treated as passing.

    Parameters
    ----------
    row : pd.Series
        Variant row.
    max_af_gnomad : float
        Maximum allowed gnomAD AF.
    max_af_exac : float
        Maximum allowed ExAC AF.
    max_af_1000genomes : float
        Maximum allowed 1000 Genomes AF.

    Returns
    -------
    bool
        True if the row passes AF filtering.
    """
    checks = [
        ("gnomad_af_numeric", max_af_gnomad),
        ("exac_af_numeric", max_af_exac),
        ("thousand_genomes_af_numeric", max_af_1000genomes),
    ]

    for column, threshold in checks:
        value = row[column]
        if pd.notna(value) and float(value) > threshold:
            return False

    return True


def _build_filter_reason(
    row: pd.Series,
    max_af_gnomad: float,
    max_af_exac: float,
    max_af_1000genomes: float,
) -> str:
    """
    Build a semicolon-delimited filter reason string for rows that fail.

    Parameters
    ----------
    row : pd.Series
        Variant row.
    max_af_gnomad : float
        Maximum allowed gnomAD AF.
    max_af_exac : float
        Maximum allowed ExAC AF.
    max_af_1000genomes : float
        Maximum allowed 1000 Genomes AF.

    Returns
    -------
    str
        Reason string or PASS.
    """
    reasons: list[str] = []

    checks = [
        ("gnomad_af_numeric", max_af_gnomad, "gnomAD_AF"),
        ("exac_af_numeric", max_af_exac, "ExAC_AF"),
        ("thousand_genomes_af_numeric", max_af_1000genomes, "1000Genomes_AF"),
    ]

    for column, threshold, label in checks:
        value = row[column]
        if pd.notna(value) and float(value) > threshold:
            reasons.append(f"{label}>{threshold}")

    return "PASS" if not reasons else ";".join(reasons)


def run_stage(
    config: dict[str, Any],
    paths: dict[str, Any],
    logger,
    state: dict[str, Any],
) -> dict[str, Any]:
    """
    Execute Stage 08.

    Responsibilities
    ----------------
    - read annotated_variants.tsv
    - apply config-driven global AF filtering
    - create filtered variant table
    - partition retained variants into coding and non-coding tracks
    - update artifacts, QC, and stage outputs
    """
    logger.info("Stage 08: filtering and partitioning annotated variants.")

    annotated_table = _validate_required_artifact(
        state["artifacts"].get("annotated_table"),
        "annotated variant table",
    )

    filtered_table = Path(paths["final_dir"]) / "filtered_variants.tsv"
    coding_table = Path(paths["final_dir"]) / "coding_variants.tsv"
    noncoding_table = Path(paths["final_dir"]) / "noncoding_variants.tsv"

    df = pd.read_csv(annotated_table, sep="\t", dtype=str).fillna("NA")

    if df.empty:
        logger.warning("Annotated variant table is empty. Writing empty downstream tables.")

    required_columns = [
        "chromosome",
        "position",
        "reference_allele",
        "alternate_allele",
        "gene_symbol",
        "consequence",
        "variant_type",
        "gnomad_af",
        "exac_af",
        "thousand_genomes_af",
        "mito_flag",
        "epilepsy_flag",
    ]
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(
            "Annotated variant table is missing required columns: "
            + ", ".join(missing_columns)
        )

    max_af_gnomad = float(config["filtering"]["max_af_gnomad"])
    max_af_exac = float(config["filtering"]["max_af_exac"])
    max_af_1000genomes = float(config["filtering"]["max_af_1000genomes"])

    df["gnomad_af_numeric"] = _normalize_numeric_series(df["gnomad_af"])
    df["exac_af_numeric"] = _normalize_numeric_series(df["exac_af"])
    df["thousand_genomes_af_numeric"] = _normalize_numeric_series(df["thousand_genomes_af"])

    df["filter_pass"] = df.apply(
        _passes_af_filter,
        axis=1,
        max_af_gnomad=max_af_gnomad,
        max_af_exac=max_af_exac,
        max_af_1000genomes=max_af_1000genomes,
    )
    df["filter_reason"] = df.apply(
        _build_filter_reason,
        axis=1,
        max_af_gnomad=max_af_gnomad,
        max_af_exac=max_af_exac,
        max_af_1000genomes=max_af_1000genomes,
    )

    filtered_df = df[df["filter_pass"]].copy()

    coding_df = filtered_df[filtered_df["variant_type"].astype(str) == "coding"].copy()
    noncoding_df = filtered_df[filtered_df["variant_type"].astype(str) == "non-coding"].copy()

    cleanup_columns = [
        col
        for col in [
            "gnomad_af_numeric",
            "exac_af_numeric",
            "thousand_genomes_af_numeric",
        ]
        if col in df.columns
    ]

    filtered_df = filtered_df.drop(columns=cleanup_columns, errors="ignore")
    coding_df = coding_df.drop(columns=cleanup_columns, errors="ignore")
    noncoding_df = noncoding_df.drop(columns=cleanup_columns, errors="ignore")

    filtered_df.to_csv(filtered_table, sep="\t", index=False)
    coding_df.to_csv(coding_table, sep="\t", index=False)
    noncoding_df.to_csv(noncoding_table, sep="\t", index=False)

    state["artifacts"]["filtered_table"] = str(filtered_table)
    state["artifacts"]["coding_table"] = str(coding_table)
    state["artifacts"]["noncoding_table"] = str(noncoding_table)

    state["qc"]["filtering_qc"] = {
        "filtering_completed": True,
        "input_annotated_variant_count": int(len(df)),
        "filtered_count": int(len(filtered_df)),
        "coding_count": int(len(coding_df)),
        "noncoding_count": int(len(noncoding_df)),
        "max_af_gnomad": max_af_gnomad,
        "max_af_exac": max_af_exac,
        "max_af_1000genomes": max_af_1000genomes,
    }

    state["stage_outputs"]["stage_08_filter_and_partition"] = {
        "status": "success",
        "input_annotated_table": str(annotated_table),
        "filtered_table": str(filtered_table),
        "coding_table": str(coding_table),
        "noncoding_table": str(noncoding_table),
        "filtered_count": int(len(filtered_df)),
        "coding_count": int(len(coding_df)),
        "noncoding_count": int(len(noncoding_df)),
    }

    logger.info(f"Filtered variant table written to: {filtered_table}")
    logger.info(f"Coding variant table written to: {coding_table}")
    logger.info(f"Non-coding variant table written to: {noncoding_table}")
    logger.info(f"Variants before filtering: {len(df)}")
    logger.info(f"Variants after filtering: {len(filtered_df)}")
    logger.info(f"Coding variants retained: {len(coding_df)}")
    logger.info(f"Non-coding variants retained: {len(noncoding_df)}")

    return state