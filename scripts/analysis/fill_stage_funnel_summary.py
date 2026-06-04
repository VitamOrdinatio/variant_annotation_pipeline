#!/usr/bin/env python3

# This script fills in missing values in stage_funnel_summary.tsv using data from stage_funnel_extracted_long.tsv.
#
# Make sure that stage_funnel_extracted_long.tsv has the following columns:
# - run_id
# - stage_funnel_summary_col_name
# - metric_value
#
# The script will pivot the long data to wide format, then update the summary file with any new values. 
# It also creates an audit log of all changes made.
#
# Usage:
#  1. Ensure you have the required input files (stage_funnel_summary.tsv and stage_funnel_extracted_long.tsv) 
#        in the same directory as this script.
#  2. Run the script:
#
#   python fill_stage_funnel_summary.py


import pandas as pd
from pathlib import Path

summary_path = Path("stage_funnel_summary.tsv")
long_path = Path("stage_funnel_extracted_long.tsv")
out_path = Path("stage_funnel_summary.completed.tsv")
audit_path = Path("stage_funnel_summary.fill_audit.tsv")

summary = pd.read_csv(summary_path, sep="\t", dtype=str)
long = pd.read_csv(long_path, sep="\t", dtype=str)

required = {"run_id", "stage_funnel_summary_col_name", "metric_value"}
missing = required - set(long.columns)
if missing:
    raise SystemExit(f"Missing required columns in {long_path}: {sorted(missing)}")

wide = (
    long
    .pivot_table(
        index="run_id",
        columns="stage_funnel_summary_col_name",
        values="metric_value",
        aggfunc="first",
    )
    .reset_index()
)

audit_rows = []

for _, row in wide.iterrows():
    run_id = row["run_id"]
    mask = summary["run_id"].eq(run_id)

    if not mask.any():
        audit_rows.append({
            "run_id": run_id,
            "status": "run_id_not_found_in_summary",
            "column": "",
            "old_value": "",
            "new_value": "",
        })
        continue

    for col in wide.columns:
        if col == "run_id":
            continue
        if col not in summary.columns:
            audit_rows.append({
                "run_id": run_id,
                "status": "column_not_found_in_summary",
                "column": col,
                "old_value": "",
                "new_value": row[col],
            })
            continue

        new_value = row[col]
        old_values = summary.loc[mask, col].fillna("").astype(str)

        for old_value in old_values:
            if old_value != str(new_value):
                audit_rows.append({
                    "run_id": run_id,
                    "status": "updated",
                    "column": col,
                    "old_value": old_value,
                    "new_value": new_value,
                })

        summary.loc[mask, col] = new_value

summary.to_csv(out_path, sep="\t", index=False)
pd.DataFrame(audit_rows).to_csv(audit_path, sep="\t", index=False)

print(f"Wrote: {out_path}")
print(f"Wrote: {audit_path}")
print(f"Updated run_ids: {wide['run_id'].nunique()}")
