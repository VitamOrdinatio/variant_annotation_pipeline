#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import pandas as pd


REPO_ROOT = Path(".")
OUT_DIR = Path("/root/Desktop/mark_probes")
OUT_PATH = OUT_DIR / "probe_metric_inventory.txt"

TARGET_RUN = "run_2026_05_27_172531"

METRICS_PATH = (
    REPO_ROOT
    / "results"
    / TARGET_RUN
    / "metrics"
    / "stage_metrics_long.tsv"
)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    if not METRICS_PATH.exists():
        raise SystemExit(f"Missing metrics file: {METRICS_PATH}")

    df = pd.read_csv(METRICS_PATH, sep="\t", dtype=str)

    lines = []

    lines.append("=== PROBE: METRIC INVENTORY ===")
    lines.append("")
    lines.append(f"metrics_path: {METRICS_PATH}")
    lines.append(f"rows: {len(df)}")
    lines.append(f"columns: {len(df.columns)}")
    lines.append("")

    lines.append("=== COLUMN NAMES ===")
    for col in df.columns:
        lines.append(col)

    lines.append("")
    lines.append("=== UNIQUE metric_name VALUES ===")

    metric_names = sorted(
        df["metric_name"]
        .astype(str)
        .str.strip()
        .dropna()
        .unique()
    )

    for name in metric_names:
        lines.append(name)

    lines.append("")
    lines.append("=== metric_name FREQUENCIES ===")

    counts = (
        df["metric_name"]
        .astype(str)
        .str.strip()
        .value_counts()
        .sort_index()
    )

    for metric_name, count in counts.items():
        lines.append(f"{metric_name}\t{count}")

    lines.append("")
    lines.append("=== SAMPLE ROWS ===")

    preview_cols = [
        c for c in [
            "sample_id",
            "run_id",
            "stage_id",
            "metric_name",
            "metric_value",
            "source_artifact",
            "source_column_or_rule",
        ]
        if c in df.columns
    ]

    preview = df[preview_cols].head(50)

    lines.append(preview.to_string(index=False))

    with open(OUT_PATH, "w") as handle:
        handle.write("\n".join(lines))

    print(f"Wrote: {OUT_PATH}")


if __name__ == "__main__":
    main()