#!/usr/bin/env python3


# Run from VAP repo root:
# python scripts/analysis/build_clinical_status_summary.py

# This script builds an append-ready clinical_status_summary.new.tsv file from
# stage_metrics_long.tsv files. The output TSV is intended to be appended to
# clinical_status_summary.tsv, which is used in the clinical_status_summary case
# study.



from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


OUTPUT_COLUMNS = [
    "sample_id",
    "run_id",
    "assay_type",
    "run_classification",
    "clinical_evidence",
    "clinical_status",
    "variant_count",
]


CANONICAL_BUCKETS = [
    "benign",
    "conflicting",
    "likely_benign",
    "likely_pathogenic",
    "missing",
    "pathogenic",
    "vus",
]


MANIFEST_ROWS = [
    ("ERR10619203", "ERR10619203", "run_2026_05_30_071639", "WES", "q3"),
    ("ERR10619207", "ERR10619207", "run_2026_06_01_124134", "WES", "q3"),
    ("ERR10619208", "ERR10619208", "run_2026_05_30_151355", "WES", "median"),
    ("ERR10619212", "ERR10619212", "run_2026_05_30_214724", "WES", "q1"),
    ("ERR10619225", "ERR10619225", "run_2026_05_31_091242", "WES", "q3"),
    ("ERR10619230", "ERR10619230", "run_2026_06_01_004903", "WES", "q3"),
    ("ERR10619241", "ERR10619241", "run_2026_06_02_052302", "WES", "q1"),
    ("ERR10619281", "ERR10619281", "run_2026_05_27_233524", "WES", "median"),
    ("ERR10619285", "ERR10619285", "run_2026_06_02_124300", "WES", "median"),
    ("ERR10619300", "ERR10619300", "run_2026_05_27_172531", "WES", "median"),
    ("ERR10619309", "ERR10619309", "run_2026_06_02_181024", "WES", "q1"),
    ("ERR10619330", "ERR10619330", "run_2026_06_01_203130", "WES", "q1"),
    ("SRR12898354", "HG002", "run_2026_06_03_010030", "WGS", "benchmark_wgs"),
]


def build_rows_for_run(
    sample_id: str,
    run_id: str,
    assay_type: str,
    run_classification: str,
    metrics_path: Path,
) -> list[dict]:
    if not metrics_path.exists():
        raise FileNotFoundError(f"Missing metrics file: {metrics_path}")

    df = pd.read_csv(metrics_path, sep="\t", dtype=str)

    required_columns = {"metric_name", "metric_value"}
    missing = required_columns - set(df.columns)

    if missing:
        raise ValueError(
            f"{metrics_path} missing required columns: {sorted(missing)}"
        )

    clinical_df = df[
        df["metric_name"].str.startswith("clinical_status__", na=False)
    ].copy()

    if clinical_df.empty:
        raise ValueError(
            f"No clinical_status__ metrics found in {metrics_path}"
        )

    clinical_df["clinical_status"] = (
        clinical_df["metric_name"]
        .str.replace("clinical_status__", "", regex=False)
    )

    clinical_df = clinical_df[
        clinical_df["clinical_status"].isin(CANONICAL_BUCKETS)
    ].copy()

    observed_buckets = sorted(clinical_df["clinical_status"].unique().tolist())
    expected_buckets = sorted(CANONICAL_BUCKETS)

    if observed_buckets != expected_buckets:
        raise ValueError(
            f"{run_id} bucket mismatch.\n"
            f"Expected: {expected_buckets}\n"
            f"Observed: {observed_buckets}"
        )

    rows = []

    for _, row in clinical_df.iterrows():
        variant_count = int(float(row["metric_value"]))

        if variant_count < 0:
            raise ValueError(
                f"Negative variant_count detected for {run_id}"
            )

        rows.append(
            {
                "sample_id": sample_id,
                "run_id": run_id,
                "assay_type": assay_type,
                "run_classification": run_classification,
                "clinical_evidence": "clinvar",
                "clinical_status": row["clinical_status"],
                "variant_count": variant_count,
            }
        )

    return rows


def validate_output(df: pd.DataFrame) -> None:
    observed_columns = df.columns.tolist()

    if observed_columns != OUTPUT_COLUMNS:
        raise ValueError(
            "Schema mismatch.\n"
            f"Expected: {OUTPUT_COLUMNS}\n"
            f"Observed: {observed_columns}"
        )

    expected_rows = len(MANIFEST_ROWS) * len(CANONICAL_BUCKETS)

    if len(df) != expected_rows:
        raise ValueError(
            f"Expected {expected_rows} rows, observed {len(df)}"
        )

    duplicate_mask = df.duplicated(
        subset=["run_id", "clinical_status"],
        keep=False,
    )

    if duplicate_mask.any():
        duplicates = df.loc[
            duplicate_mask,
            ["run_id", "clinical_status"],
        ]

        raise ValueError(
            "Duplicate run_id + clinical_status rows detected:\n"
            f"{duplicates.to_string(index=False)}"
        )

    for run_id, group in df.groupby("run_id"):
        observed = sorted(group["clinical_status"].tolist())

        if observed != sorted(CANONICAL_BUCKETS):
            raise ValueError(
                f"{run_id} missing canonical clinical-status buckets."
            )

    if df["variant_count"].isna().any():
        raise ValueError("Null variant_count values detected.")

    if (df["variant_count"] < 0).any():
        raise ValueError("Negative variant_count values detected.")

    hg002_df = df[df["sample_id"] == "HG002"]

    if hg002_df.empty:
        raise ValueError("Missing HG002 rows.")

    if not (hg002_df["assay_type"] == "WGS").all():
        raise ValueError("HG002 rows must use assay_type=WGS")

    if not (
        hg002_df["run_classification"] == "benchmark_wgs"
    ).all():
        raise ValueError(
            "HG002 rows must use run_classification=benchmark_wgs"
        )


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Build append-ready clinical_status_summary.new.tsv "
            "from stage_metrics_long.tsv files."
        )
    )

    parser.add_argument(
        "--results-dir",
        type=Path,
        default=Path("results"),
        help="Path to VAP results directory.",
    )

    parser.add_argument(
        "--out",
        type=Path,
        default=Path(
            "docs/case_studies/cross_runs/cross_run_tables/"
            "clinical_status_summary.new.tsv"
        ),
        help="Output append-ready TSV path.",
    )

    args = parser.parse_args()

    all_rows = []

    for (
        _source_accession,
        sample_id,
        run_id,
        assay_type,
        run_classification,
    ) in MANIFEST_ROWS:

        metrics_path = (
            args.results_dir
            / run_id
            / "metrics"
            / "stage_metrics_long.tsv"
        )

        run_rows = build_rows_for_run(
            sample_id=sample_id,
            run_id=run_id,
            assay_type=assay_type,
            run_classification=run_classification,
            metrics_path=metrics_path,
        )

        all_rows.extend(run_rows)

    out_df = pd.DataFrame(all_rows, columns=OUTPUT_COLUMNS)

    out_df["variant_count"] = out_df["variant_count"].astype(int)

    validate_output(out_df)

    args.out.parent.mkdir(parents=True, exist_ok=True)

    out_df.to_csv(
        args.out,
        sep="\t",
        index=False,
    )

    print(f"Wrote: {args.out}")
    print(f"Rows: {len(out_df)}")
    print(f"Runs: {out_df['run_id'].nunique()}")

    print("\nClinical-status buckets per run:")
    print(
        out_df.groupby("run_id")["clinical_status"]
        .nunique()
        .to_string()
    )


if __name__ == "__main__":
    main()