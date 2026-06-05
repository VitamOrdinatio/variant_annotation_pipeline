#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import pandas as pd


REPO_ROOT = Path(".")
OUT_DIR = Path("/root/Desktop/mark_probes")
OUT_PATH = OUT_DIR / "probe_metric_provenance_resolution.txt"

TARGET_RUN = "run_2026_05_27_172531"

METRICS_PATH = (
    REPO_ROOT
    / "results"
    / TARGET_RUN
    / "metrics"
    / "stage_metrics_long.tsv"
)

TARGET_PREFIXES = [
    "counts_by_",
    "clinical_status__",
    "frequency_status__",
    "functional_impact_distribution__",
    "population_frequency_bin__",
    "consequence_distribution__",
    "variants_by_",
]

TARGET_EXACT = [
    "gene_id_count_unique",
    "rdgp_gene_evidence_seed_rows",
    "rdgp_gene_evidence_seed_tsv_rows",
    "validation_candidates_rows",
    "coding_candidates_rows",
    "noncoding_candidates_rows",
    "prioritized_variants_rows",
    "vdb_ready_variants_rows",
    "coding_interpreted_rows",
    "noncoding_interpreted_rows",
    "high_priority_candidate_count",
    "moderate_priority_candidate_count",
    "low_priority_candidate_count",
    "uninterpretable_count",
]


def metric_selected(metric_name: str) -> bool:
    if metric_name in TARGET_EXACT:
        return True

    for prefix in TARGET_PREFIXES:
        if metric_name.startswith(prefix):
            return True

    return False


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    if not METRICS_PATH.exists():
        raise SystemExit(f"Missing metrics file: {METRICS_PATH}")

    df = pd.read_csv(METRICS_PATH, sep="\t", dtype=str)

    df["metric_name"] = df["metric_name"].astype(str).str.strip()

    selected = df[
        df["metric_name"].apply(metric_selected)
    ].copy()

    selected = selected[
        [
            "metric_name",
            "metric_value",
            "stage_id",
            "source_artifact",
            "source_column_or_rule",
            "derivation_rule",
            "metric_category",
            "intended_figure_support",
        ]
    ].drop_duplicates()

    selected = selected.sort_values(
        ["metric_name", "source_artifact"],
        kind="mergesort",
    )

    lines = []

    lines.append("=== PROBE: METRIC PROVENANCE RESOLUTION ===")
    lines.append("")
    lines.append(f"metrics_path: {METRICS_PATH}")
    lines.append(f"selected_rows: {len(selected)}")
    lines.append("")

    current_metric = None

    for _, row in selected.iterrows():
        metric_name = row["metric_name"]

        if metric_name != current_metric:
            lines.append("")
            lines.append("=" * 80)
            lines.append(metric_name)
            lines.append("=" * 80)
            current_metric = metric_name

        lines.append(f"metric_value: {row['metric_value']}")
        lines.append(f"stage_id: {row['stage_id']}")
        lines.append(f"metric_category: {row['metric_category']}")
        lines.append(f"source_artifact: {row['source_artifact']}")
        lines.append(f"source_column_or_rule: {row['source_column_or_rule']}")
        lines.append(f"derivation_rule: {row['derivation_rule']}")
        lines.append(f"intended_figure_support: {row['intended_figure_support']}")
        lines.append("")

    with open(OUT_PATH, "w") as handle:
        handle.write("\n".join(lines))

    print(f"Wrote: {OUT_PATH}")


if __name__ == "__main__":
    main()