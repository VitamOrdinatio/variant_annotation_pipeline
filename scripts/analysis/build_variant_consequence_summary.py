#!/usr/bin/env python3

# run from VAP repo root:
# python scripts/analysis/build_variant_consequence_summary.py

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


OUTPUT_COLUMNS = [
    "sample_id",
    "run_id",
    "assay_type",
    "run_classification",
    "interpretation_domain",
    "molecular_consequence",
    "count",
]


CANONICAL_CONSEQUENCES = [
    "loss_of_function",
    "missense",
    "other_coding",
    "splice_relevant",
    "synonymous",
    "utr_regulatory",
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


CONSEQUENCE_PREFIX = "consequence_distribution__"

STAGE_TO_DOMAIN = {
    "stage_09": "coding",
    "stage_10": "noncoding",
}


def classify_consequence(raw: str) -> str:
    terms = set(str(raw).split("&"))

    if terms & {
        "frameshift_variant",
        "stop_gained",
        "stop_lost",
        "start_lost",
        "splice_acceptor_variant",
        "splice_donor_variant",
    }:
        return "loss_of_function"

    if "missense_variant" in terms:
        return "missense"

    if "synonymous_variant" in terms or "stop_retained_variant" in terms:
        return "synonymous"

    if terms & {
        "splice_region_variant",
        "splice_donor_region_variant",
        "splice_donor_5th_base_variant",
        "splice_polypyrimidine_tract_variant",
    }:
        return "splice_relevant"

    if terms & {
        "3_prime_UTR_variant",
        "5_prime_UTR_variant",
        "upstream_gene_variant",
        "downstream_gene_variant",
    }:
        return "utr_regulatory"

    return "other_coding"


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
        raise ValueError(f"{metrics_path} missing required columns: {sorted(missing)}")

    rows: list[dict] = []

    for stage_id, interpretation_domain in STAGE_TO_DOMAIN.items():
        domain_df = df[
            (df["stage_id"] == stage_id)
            & df["metric_name"].str.startswith(CONSEQUENCE_PREFIX, na=False)
        ].copy()

        if domain_df.empty:
            raise ValueError(
                f"No {CONSEQUENCE_PREFIX} metrics found for {stage_id} in {metrics_path}"
            )

        domain_df["raw_consequence"] = domain_df["metric_name"].str.replace(
            CONSEQUENCE_PREFIX,
            "",
            regex=False,
        )

        domain_df["molecular_consequence"] = domain_df["raw_consequence"].map(
            classify_consequence
        )

        domain_df["metric_value_int"] = domain_df["metric_value"].map(
            lambda value: int(float(value))
        )

        grouped = (
            domain_df.groupby("molecular_consequence", as_index=False)["metric_value_int"]
            .sum()
            .rename(columns={"metric_value_int": "count"})
        )

        observed = sorted(grouped["molecular_consequence"].unique().tolist())
        expected = sorted(CANONICAL_CONSEQUENCES)

        missing_consequences = sorted(set(expected) - set(observed))
        if missing_consequences:
            for consequence in missing_consequences:
                grouped.loc[len(grouped)] = {
                    "molecular_consequence": consequence,
                    "count": 0,
                }

        unexpected = sorted(set(observed) - set(expected))
        if unexpected:
            raise ValueError(
                f"{run_id} {interpretation_domain} unexpected consequence buckets: {unexpected}"
            )

        grouped = grouped.sort_values("molecular_consequence")

        for _, row in grouped.iterrows():
            count = int(row["count"])

            if count < 0:
                raise ValueError(
                    f"Negative count detected for {run_id} "
                    f"{interpretation_domain} {row['molecular_consequence']}"
                )

            rows.append(
                {
                    "sample_id": sample_id,
                    "run_id": run_id,
                    "assay_type": assay_type,
                    "run_classification": run_classification,
                    "interpretation_domain": interpretation_domain,
                    "molecular_consequence": row["molecular_consequence"],
                    "count": count,
                }
            )

    return rows


def validate_output(df: pd.DataFrame) -> None:
    if df.columns.tolist() != OUTPUT_COLUMNS:
        raise ValueError(
            "Schema mismatch.\n"
            f"Expected: {OUTPUT_COLUMNS}\n"
            f"Observed: {df.columns.tolist()}"
        )

    expected_rows = (
        len(MANIFEST_ROWS)
        * len(STAGE_TO_DOMAIN)
        * len(CANONICAL_CONSEQUENCES)
    )
    if len(df) != expected_rows:
        raise ValueError(f"Expected {expected_rows} rows, observed {len(df)}")

    duplicate_mask = df.duplicated(
        subset=["run_id", "interpretation_domain", "molecular_consequence"],
        keep=False,
    )
    if duplicate_mask.any():
        duplicates = df.loc[
            duplicate_mask,
            ["run_id", "interpretation_domain", "molecular_consequence"],
        ]
        raise ValueError(
            "Duplicate semantic consequence rows detected:\n"
            f"{duplicates.to_string(index=False)}"
        )

    for run_id, run_group in df.groupby("run_id"):
        observed_domains = sorted(run_group["interpretation_domain"].unique().tolist())
        expected_domains = sorted(STAGE_TO_DOMAIN.values())

        if observed_domains != expected_domains:
            raise ValueError(
                f"{run_id} domain mismatch.\n"
                f"Expected: {expected_domains}\n"
                f"Observed: {observed_domains}"
            )

        for domain, domain_group in run_group.groupby("interpretation_domain"):
            observed = sorted(domain_group["molecular_consequence"].tolist())
            expected = sorted(CANONICAL_CONSEQUENCES)

            if observed != expected:
                raise ValueError(
                    f"{run_id} {domain} consequence mismatch.\n"
                    f"Expected: {expected}\n"
                    f"Observed: {observed}"
                )

    if df["count"].isna().any():
        raise ValueError("Null count values detected.")

    if (df["count"] < 0).any():
        raise ValueError("Negative count values detected.")

    hg002_df = df[df["sample_id"] == "HG002"]

    if hg002_df.empty:
        raise ValueError("Missing HG002 rows.")

    if not (hg002_df["assay_type"] == "WGS").all():
        raise ValueError("HG002 rows must use assay_type=WGS")

    if not (hg002_df["run_classification"] == "benchmark_wgs").all():
        raise ValueError("HG002 rows must use run_classification=benchmark_wgs")


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Build append-ready variant_consequence_summary.new.tsv "
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
            "variant_consequence_summary.new.tsv"
        ),
        help="Output append-ready TSV path.",
    )
    args = parser.parse_args()

    all_rows: list[dict] = []

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

        all_rows.extend(
            build_rows_for_run(
                sample_id=sample_id,
                run_id=run_id,
                assay_type=assay_type,
                run_classification=run_classification,
                metrics_path=metrics_path,
            )
        )

    out_df = pd.DataFrame(all_rows, columns=OUTPUT_COLUMNS)
    out_df["count"] = out_df["count"].astype(int)

    validate_output(out_df)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    out_df.to_csv(args.out, sep="\t", index=False)

    print(f"Wrote: {args.out}")
    print(f"Rows: {len(out_df)}")
    print(f"Runs: {out_df['run_id'].nunique()}")

    print("\nDomains per run:")
    print(out_df.groupby("run_id")["interpretation_domain"].nunique().to_string())

    print("\nConsequence classes per run/domain:")
    print(
        out_df.groupby(["run_id", "interpretation_domain"])["molecular_consequence"]
        .nunique()
        .to_string()
    )


if __name__ == "__main__":
    main()