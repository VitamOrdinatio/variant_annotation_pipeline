#!/usr/bin/env python3

# Run from VAP repo root:
# python scripts/analysis/build_runtime_stage_summary.py

# script will write to docs/case_studies/cross_runs/cross_run_tables/runtime_stage_summary.new.tsv
# script expects results/ directory with run_<id>/metadata/stage_resource_snapshots.tsv files for each run_id in MANIFEST_ROWS


from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


OUTPUT_COLUMNS = [
    "sample_id",
    "run_id",
    "stage",
    "elapsed_seconds",
    "status",
    "start_time",
    "end_time",
]


MANIFEST_ROWS = [
    ("ERR10619203", "run_2026_05_30_071639", "q3"),
    ("ERR10619207", "run_2026_06_01_124134", "q3"),
    ("ERR10619208", "run_2026_05_30_151355", "median"),
    ("ERR10619212", "run_2026_05_30_214724", "q1"),
    ("ERR10619225", "run_2026_05_31_091242", "q3"),
    ("ERR10619230", "run_2026_06_01_004903", "q3"),
    ("ERR10619241", "run_2026_06_02_052302", "q1"),
    ("ERR10619281", "run_2026_05_27_233524", "median"),
    ("ERR10619285", "run_2026_06_02_124300", "median"),
    ("ERR10619300", "run_2026_05_27_172531", "median"),
    ("ERR10619309", "run_2026_06_02_181024", "q1"),
    ("ERR10619330", "run_2026_06_01_203130", "q1"),
    ("SRR12898354", "run_2026_06_03_010030", "hg002"),
]


def build_stage_rows(sample_id: str, run_id: str, snapshot_path: Path) -> list[dict]:
    df = pd.read_csv(snapshot_path, sep="\t", dtype=str)

    required = {"timestamp", "stage", "phase"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"{snapshot_path} missing required columns: {sorted(missing)}")

    rows: list[dict] = []

    for stage, g in df.groupby("stage", sort=True):
        phase_counts = g["phase"].value_counts().to_dict()

        if phase_counts.get("start", 0) != 1 or phase_counts.get("end", 0) != 1:
            rows.append(
                {
                    "sample_id": sample_id,
                    "run_id": run_id,
                    "stage": stage,
                    "elapsed_seconds": pd.NA,
                    "status": "ambiguous",
                    "start_time": pd.NA,
                    "end_time": pd.NA,
                }
            )
            continue

        start_time = g.loc[g["phase"] == "start", "timestamp"].iloc[0]
        end_time = g.loc[g["phase"] == "end", "timestamp"].iloc[0]

        start_dt = pd.to_datetime(start_time, utc=True)
        end_dt = pd.to_datetime(end_time, utc=True)

        elapsed_seconds = (end_dt - start_dt).total_seconds()
        status = "success" if elapsed_seconds >= 0 else "ambiguous"

        rows.append(
            {
                "sample_id": sample_id,
                "run_id": run_id,
                "stage": stage,
                "elapsed_seconds": elapsed_seconds,
                "status": status,
                "start_time": start_time,
                "end_time": end_time,
            }
        )

    return rows


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build append-ready runtime_stage_summary.new.tsv from stage_resource_snapshots.tsv files."
    )
    parser.add_argument(
        "--results-dir",
        type=Path,
        default=Path("results"),
        help="Path to VAP results directory containing run_<id> folders.",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=Path(
            "docs/case_studies/cross_runs/cross_run_tables/runtime_stage_summary.new.tsv"
        ),
        help="Output append-ready TSV path.",
    )
    args = parser.parse_args()

    all_rows: list[dict] = []

    for sample_id, run_id, _depth_category in MANIFEST_ROWS:
        snapshot_path = args.results_dir / run_id / "metadata" / "stage_resource_snapshots.tsv"

        if not snapshot_path.exists():
            raise FileNotFoundError(f"Missing telemetry file: {snapshot_path}")

        all_rows.extend(build_stage_rows(sample_id, run_id, snapshot_path))

    out_df = pd.DataFrame(all_rows, columns=OUTPUT_COLUMNS)

    duplicate_pairs = out_df.duplicated(subset=["run_id", "stage"], keep=False)
    if duplicate_pairs.any():
        raise ValueError("Duplicate (run_id, stage) rows detected in output.")

    bad_status = out_df[out_df["status"] != "success"]
    if not bad_status.empty:
        print("WARNING: Non-success stage rows detected:")
        print(bad_status.to_string(index=False))

    expected_rows = len(MANIFEST_ROWS) * 13
    if len(out_df) != expected_rows:
        print(f"WARNING: expected {expected_rows} rows, observed {len(out_df)} rows.")

    args.out.parent.mkdir(parents=True, exist_ok=True)
    out_df.to_csv(args.out, sep="\t", index=False)

    print(f"Wrote: {args.out}")
    print(f"Rows: {len(out_df)}")
    print(f"Runs: {out_df['run_id'].nunique()}")
    print(f"Stages per run:")
    print(out_df.groupby("run_id")["stage"].nunique().to_string())


if __name__ == "__main__":
    main()