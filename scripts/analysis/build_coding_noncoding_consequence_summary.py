#!/usr/bin/env python3

# Run within the VAP repository root:
    # python scripts/analysis/build_coding_noncoding_consequence_summary.py

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
    "summary_axis",
    "consequence_label",
    "count",
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


STAGE_TO_DOMAIN = {
    "stage_09": "coding",
    "stage_10": "noncoding",
}


FREQUENCY_LABELS = [
    "common",
    "low_frequency",
    "missing",
    "rare",
    "unknown",
]

CLINICAL_LABELS = [
    "benign",
    "conflicting",
    "likely_benign",
    "likely_pathogenic",
    "missing",
    "pathogenic",
    "vus",
]

VARIANT_FUNCTION_LABELS = [
    "loss_of_function",
    "missense",
    "other_coding",
    "splice_relevant",
    "synonymous",
    "unknown",
]

CONTEXT_LABELS = [
    "intergenic",
    "intronic",
    "proximal",
    "regulatory",
    "transcript_associated",
    "unknown",
]


# Historical public-artifact topology.
# The May 22 artifact is not fully rectangular across every domain/axis.
TOPOLOGY_TEMPLATE = {
    ("coding", "clinical_status"): CLINICAL_LABELS,
    ("noncoding", "clinical_status"): CLINICAL_LABELS,
    ("coding", "frequency_class"): FREQUENCY_LABELS,
    ("noncoding", "frequency_class"): FREQUENCY_LABELS,
    ("coding", "interpretation_label"): [
        "coding_common_or_low_support",
        "coding_uninterpretable",
        "lof_or_missense_rare",
        "lof_rare_clinically_supported",
    ],
    ("noncoding", "interpretation_label"): [
        "noncoding_common_or_low_support",
        "noncoding_uninterpretable",
        "regulatory_or_transcript_rare",
        "regulatory_rare_supported",
    ],
    ("noncoding", "context"): CONTEXT_LABELS,
    ("coding", "variant_function"): VARIANT_FUNCTION_LABELS,
}


def metric_rows(df: pd.DataFrame, stage_id: str | None, prefix: str) -> pd.DataFrame:
    mask = df["metric_name"].str.startswith(prefix, na=False)
    if stage_id is not None:
        mask &= df["stage_id"].eq(stage_id)
    out = df.loc[mask].copy()
    if out.empty:
        raise ValueError(f"No metrics found for stage_id={stage_id}, prefix={prefix}")
    out["label"] = out["metric_name"].str.replace(prefix, "", regex=False)
    out["count"] = out["metric_value"].map(lambda x: int(float(x)))
    return out[["label", "count"]]


def add_rows(
    rows: list[dict],
    sample_id: str,
    run_id: str,
    assay_type: str,
    run_classification: str,
    interpretation_domain: str,
    summary_axis: str,
    counts: dict[str, int],
) -> None:
    expected_labels = TOPOLOGY_TEMPLATE[(interpretation_domain, summary_axis)]

    for label in expected_labels:
        count = int(counts.get(label, 0))
        if count < 0:
            raise ValueError(
                f"Negative count for {run_id} {interpretation_domain} "
                f"{summary_axis} {label}"
            )

        rows.append(
            {
                "sample_id": sample_id,
                "run_id": run_id,
                "assay_type": assay_type,
                "run_classification": run_classification,
                "interpretation_domain": interpretation_domain,
                "summary_axis": summary_axis,
                "consequence_label": label,
                "count": count,
            }
        )


def classify_variant_function(raw: str) -> str:
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

    if terms & {
        "splice_region_variant",
        "splice_donor_region_variant",
        "splice_donor_5th_base_variant",
        "splice_polypyrimidine_tract_variant",
    }:
        return "splice_relevant"

    if "synonymous_variant" in terms or "stop_retained_variant" in terms:
        return "synonymous"

    if raw in {"", "missing", "unknown"}:
        return "unknown"

    return "other_coding"


def classify_clinical_status(raw: str) -> str:
    value = str(raw).strip().lower()

    if value in {"", ".", "nan", "none", "missing", "not_provided"}:
        return "missing"

    value = value.replace(" ", "_").replace("-", "_")

    if "conflicting" in value:
        return "conflicting"

    if "likely_pathogenic" in value:
        return "likely_pathogenic"

    if "pathogenic" in value:
        return "pathogenic"

    if "uncertain_significance" in value or value == "vus" or "vus" in value:
        return "vus"

    if "likely_benign" in value:
        return "likely_benign"

    if "benign" in value:
        return "benign"

    return "missing"


def collect_stage_distribution(
    df: pd.DataFrame,
    stage_id: str,
    prefix: str,
    classifier,
) -> dict[str, int]:
    metric_df = metric_rows(df, stage_id=stage_id, prefix=prefix)
    metric_df["collapsed_label"] = metric_df["label"].map(classifier)

    grouped = metric_df.groupby("collapsed_label")["count"].sum().to_dict()
    return {str(k): int(v) for k, v in grouped.items()}


def collect_direct_stage_distribution(
    df: pd.DataFrame,
    stage_id: str,
    prefix: str,
) -> dict[str, int]:
    metric_df = metric_rows(df, stage_id=stage_id, prefix=prefix)
    return {
        str(row["label"]): int(row["count"])
        for _, row in metric_df.iterrows()
    }


def collect_interpretation_labels(df: pd.DataFrame) -> dict[str, dict[str, int]]:
    metric_df = metric_rows(
        df,
        stage_id=None,
        prefix="counts_by_source_interpretation_label__",
    )

    counts = {"coding": {}, "noncoding": {}}

    for _, row in metric_df.iterrows():
        label = str(row["label"])
        count = int(row["count"])

        if label.startswith("coding_") or label.startswith("lof_"):
            counts["coding"][label] = counts["coding"].get(label, 0) + count
        elif label.startswith("noncoding_") or label.startswith("regulatory_"):
            counts["noncoding"][label] = counts["noncoding"].get(label, 0) + count

    return counts


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

    required_columns = {"stage_id", "metric_name", "metric_value"}
    missing = required_columns - set(df.columns)
    if missing:
        raise ValueError(f"{metrics_path} missing required columns: {sorted(missing)}")

    rows: list[dict] = []

    # frequency_class
    for stage_id, domain in STAGE_TO_DOMAIN.items():
        counts = collect_direct_stage_distribution(
            df,
            stage_id=stage_id,
            prefix="population_frequency_bin__",
        )
        add_rows(
            rows,
            sample_id,
            run_id,
            assay_type,
            run_classification,
            domain,
            "frequency_class",
            counts,
        )

    # interpretation_label
    label_counts = collect_interpretation_labels(df)
    for domain in ["coding", "noncoding"]:
        add_rows(
            rows,
            sample_id,
            run_id,
            assay_type,
            run_classification,
            domain,
            "interpretation_label",
            label_counts[domain],
        )

    # context, noncoding only
    context_counts = collect_direct_stage_distribution(
        df,
        stage_id="stage_10",
        prefix="noncoding_functional_context_distribution__",
    )
    add_rows(
        rows,
        sample_id,
        run_id,
        assay_type,
        run_classification,
        "noncoding",
        "context",
        context_counts,
    )

    # variant_function
    for stage_id, domain in STAGE_TO_DOMAIN.items():
        if domain != "coding":
            continue
        counts = collect_stage_distribution(
            df,
            stage_id=stage_id,
            prefix="consequence_distribution__",
            classifier=classify_variant_function,
        )
        add_rows(
            rows,
            sample_id,
            run_id,
            assay_type,
            run_classification,
            domain,
            "variant_function",
            counts,
        )

    # clinical_status
    for stage_id, domain in STAGE_TO_DOMAIN.items():
        counts = collect_stage_distribution(
            df,
            stage_id=stage_id,
            prefix="clinical_significance_distribution__",
            classifier=classify_clinical_status,
        )
        add_rows(
            rows,
            sample_id,
            run_id,
            assay_type,
            run_classification,
            domain,
            "clinical_status",
            counts,
        )

    return rows


def validate_output(df: pd.DataFrame) -> None:
    if df.columns.tolist() != OUTPUT_COLUMNS:
        raise ValueError(
            "Schema mismatch.\n"
            f"Expected: {OUTPUT_COLUMNS}\n"
            f"Observed: {df.columns.tolist()}"
        )

    expected_rows_per_run = sum(len(labels) for labels in TOPOLOGY_TEMPLATE.values())
    expected_rows = expected_rows_per_run * len(MANIFEST_ROWS)

    if len(df) != expected_rows:
        raise ValueError(f"Expected {expected_rows} rows, observed {len(df)}")

    duplicate_mask = df.duplicated(
        subset=[
            "run_id",
            "interpretation_domain",
            "summary_axis",
            "consequence_label",
        ],
        keep=False,
    )
    if duplicate_mask.any():
        raise ValueError(
            "Duplicate semantic rows detected:\n"
            + df.loc[
                duplicate_mask,
                [
                    "run_id",
                    "interpretation_domain",
                    "summary_axis",
                    "consequence_label",
                ],
            ].to_string(index=False)
        )

    if df["count"].isna().any():
        raise ValueError("Null count values detected.")

    if (df["count"] < 0).any():
        raise ValueError("Negative count values detected.")

    for run_id, run_group in df.groupby("run_id"):
        for (domain, axis), expected_labels in TOPOLOGY_TEMPLATE.items():
            observed = sorted(
                run_group.loc[
                    (run_group["interpretation_domain"] == domain)
                    & (run_group["summary_axis"] == axis),
                    "consequence_label",
                ].tolist()
            )
            expected = sorted(expected_labels)

            if observed != expected:
                raise ValueError(
                    f"{run_id} topology mismatch for {domain}/{axis}.\n"
                    f"Expected: {expected}\n"
                    f"Observed: {observed}"
                )

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
            "Build append-ready coding_noncoding_consequence_summary.new.tsv "
            "from stage_metrics_long.tsv files using legacy-compatible flattening."
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
            "coding_noncoding_consequence_summary.new.tsv"
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
            args.results_dir / run_id / "metrics" / "stage_metrics_long.tsv"
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

    print("\nRows per run:")
    print(out_df.groupby("run_id").size().to_string())

    print("\nRows per run/domain/axis:")
    print(
        out_df.groupby(
            ["run_id", "interpretation_domain", "summary_axis"]
        ).size().to_string()
    )


if __name__ == "__main__":
    main()