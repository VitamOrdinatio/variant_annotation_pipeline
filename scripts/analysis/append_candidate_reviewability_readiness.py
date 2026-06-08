#!/usr/bin/env python3

# This script appends new rows to the candidate_reviewability_readiness.tsv file based on metrics extracted from the specified runs.
# Run from VAP repo root.  Make sure that a copy of the existing candidate_reviewability_readiness.tsv is present in the current directory, and that the results/ directory with run subdirectories is also present.
# The manifest_rows list specifies the sample_id, run_id, and depth_category for each run to be processed.  The expected_rows list specifies the metric_name, metric, and category for each metric to be extracted from the stage_metrics_long.tsv files for each run.
# For each run, the script checks for the presence of each expected metric.  If the metric is present, it extracts the count value.  If the metric is absent, it fills in a count of 0.  The script also creates an audit log indicating which metrics were present vs filled in, along with the sample_id, run_id, depth_category, metric_name, metric, category, count, and status for each expected metric.

import pandas as pd
from pathlib import Path

existing_path = Path("candidate_reviewability_readiness.tsv")
out_path = Path("candidate_reviewability_readiness.appended.tsv")
audit_path = Path("candidate_reviewability_readiness_append_audit.tsv")

manifest_rows = [
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
    ("HG002", "run_2026_06_03_010030", "hg002"),
]

expected_rows = [
    ("counts_by_validation_required__False", "validation_required", "False"),
    ("counts_by_validation_required__True", "validation_required", "True"),
    ("counts_by_validation_priority__high", "validation_priority", "high"),
    ("counts_by_validation_priority__low", "validation_priority", "low"),
    ("counts_by_validation_priority__medium", "validation_priority", "medium"),
    ("counts_by_suggested_validation_method__IGV", "suggested_validation_method", "IGV"),
    ("counts_by_suggested_validation_method__none", "suggested_validation_method", "none"),
]

existing = pd.read_csv(existing_path, sep="\t", dtype=str)

rows = []
audit_rows = []

for sample_id, run_id, depth_category in manifest_rows:
    metrics_path = Path("results") / run_id / "metrics" / "stage_metrics_long.tsv"

    if not metrics_path.exists():
        raise SystemExit(f"Missing source metrics file: {metrics_path}")

    df = pd.read_csv(metrics_path, sep="\t", dtype=str)

    required_cols = {"sample_id", "run_id", "metric_name", "metric_value"}
    missing_cols = required_cols - set(df.columns)
    if missing_cols:
        raise SystemExit(f"{metrics_path} missing required columns: {sorted(missing_cols)}")

    observed_sample_ids = sorted(set(df["sample_id"].dropna().astype(str)))
    observed_run_ids = sorted(set(df["run_id"].dropna().astype(str)))

    if observed_sample_ids != [sample_id]:
        raise SystemExit(f"{metrics_path} sample_id mismatch: manifest={sample_id}, observed={observed_sample_ids}")

    if observed_run_ids != [run_id]:
        raise SystemExit(f"{metrics_path} run_id mismatch: manifest={run_id}, observed={observed_run_ids}")

    for metric_name, metric, category in expected_rows:
        vals = sorted(set(df.loc[df["metric_name"] == metric_name, "metric_value"].dropna().astype(str)))

        if len(vals) > 1:
            raise SystemExit(f"{run_id} has conflicting values for {metric_name}: {vals}")

        if len(vals) == 1:
            count = vals[0]
            status = "source_metric_present"
        else:
            count = "0"
            status = "source_metric_absent_filled_zero"

        rows.append({
            "sample_id": sample_id,
            "run_id": run_id,
            "metric": metric,
            "category": category,
            "count": count,
        })

        audit_rows.append({
            "sample_id": sample_id,
            "run_id": run_id,
            "depth_category": depth_category,
            "metric_name": metric_name,
            "metric": metric,
            "category": category,
            "count": count,
            "status": status,
        })

new = pd.DataFrame(rows)
combined = pd.concat([existing, new], ignore_index=True)

combined.to_csv(out_path, sep="\t", index=False)
pd.DataFrame(audit_rows).to_csv(audit_path, sep="\t", index=False)

print(f"Existing rows : {len(existing)}")
print(f"Appended rows : {len(new)}")
print(f"Final rows    : {len(combined)}")
print(f"Wrote: {out_path}")
print(f"Wrote: {audit_path}")
