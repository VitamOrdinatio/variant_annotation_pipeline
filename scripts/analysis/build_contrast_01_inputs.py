#!/usr/bin/env python3
import json
import shutil
import pandas as pd
from pathlib import Path

DEST = Path("docs/case_studies/cross_runs/contrasts/contrast_01_inputs")
MANIFEST = DEST / "cohort_manifest.tsv"
CROSS = Path("docs/case_studies/cross_runs/cross_run_tables")
RESULTS = Path("results")

GLOBAL_TABLES = [
    "stage_funnel_summary.tsv",
    "priority_tier_summary.tsv",
    "interpretation_label_summary.tsv",
]

audit = []

def read_simple_yaml(path):
    data = {}
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        k, v = line.split(":", 1)
        data[k.strip()] = v.strip().strip('"').strip("'")
    return data

def copy_file(src, dst, required=False, label=""):
    if src.exists():
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        audit.append({"status": "copied", "label": label, "src": str(src), "dst": str(dst)})
    elif required:
        audit.append({"status": "missing_required", "label": label, "src": str(src), "dst": str(dst)})
        raise SystemExit(f"Missing required file: {src}")
    else:
        audit.append({"status": "missing_optional", "label": label, "src": str(src), "dst": str(dst)})

def subset_table(table_name, sample_id, run_id, out_dir):
    src = CROSS / table_name
    if not src.exists():
        raise SystemExit(f"Missing global table: {src}")

    df = pd.read_csv(src, sep="\t", dtype=str)

    if "sample_id" not in df.columns or "run_id" not in df.columns:
        raise SystemExit(f"{src} must contain sample_id and run_id columns")

    sub = df[(df["sample_id"] == sample_id) & (df["run_id"] == run_id)].copy()

    if sub.empty:
        raise SystemExit(f"No rows found in {src} for sample_id={sample_id}, run_id={run_id}")

    dst = out_dir / table_name
    dst.parent.mkdir(parents=True, exist_ok=True)
    sub.to_csv(dst, sep="\t", index=False)

    audit.append({
        "status": "subset_written",
        "label": table_name,
        "src": str(src),
        "dst": str(dst),
        "rows": len(sub),
    })

manifest = pd.read_csv(MANIFEST, sep="\t", dtype=str)

required_cols = {"SRA_accn", "VAP_run_id", "Depth_Category"}
missing = required_cols - set(manifest.columns)
if missing:
    raise SystemExit(f"cohort_manifest.tsv missing columns: {sorted(missing)}")

if len(manifest) != 12:
    raise SystemExit(f"Expected 12 WES rows in cohort_manifest.tsv, found {len(manifest)}")

for _, row in manifest.iterrows():
    sample_id = row["SRA_accn"]
    run_id = row["VAP_run_id"]
    depth = row["Depth_Category"]

    run_dir = RESULTS / run_id
    fig_yaml = run_dir / "metadata" / "figure_set_resolved.yaml"

    if not fig_yaml.exists():
        raise SystemExit(f"Missing figure_set_resolved.yaml: {fig_yaml}")

    y = read_simple_yaml(fig_yaml)

    if y.get("sample_id") != sample_id:
        raise SystemExit(f"Sample mismatch in {fig_yaml}: manifest={sample_id}, yaml={y.get('sample_id')}")

    if y.get("run_id") != run_id:
        raise SystemExit(f"Run mismatch in {fig_yaml}: manifest={run_id}, yaml={y.get('run_id')}")

    sra_dir = DEST / sample_id

    for subdir in ["metadata", "tables", "figures", "sql_outputs", "notes"]:
        (sra_dir / subdir).mkdir(parents=True, exist_ok=True)

    pd.DataFrame([{
        "sample_id": sample_id,
        "run_id": run_id,
        "depth_category": depth,
    }]).to_csv(sra_dir / "metadata" / "sra_run_depth_metadata.tsv", sep="\t", index=False)

    copy_file(fig_yaml, sra_dir / "metadata" / fig_yaml.name, required=True, label="figure_set_resolved.yaml")
    copy_file(run_dir / "metadata" / "run_metadata.json", sra_dir / "metadata" / "run_metadata.json", required=False, label="run_metadata.json")

    for table in GLOBAL_TABLES:
        subset_table(table, sample_id, run_id, sra_dir / "tables")

    f3a = list((run_dir / "figures").glob(f"{sample_id}_f3a_deterministic_evidence_lineage.png"))
    f3b = list((run_dir / "figures").glob(f"{sample_id}_f3b_semantic_branching.png"))

    if len(f3a) != 1:
        raise SystemExit(f"Expected 1 F3A figure for {sample_id}, found {len(f3a)}")
    if len(f3b) != 1:
        raise SystemExit(f"Expected 1 F3B figure for {sample_id}, found {len(f3b)}")

    copy_file(f3a[0], sra_dir / "figures" / f3a[0].name, required=True, label="F3A")
    copy_file(f3b[0], sra_dir / "figures" / f3b[0].name, required=True, label="F3B")

    for optional_fig in (run_dir / "figures").glob(f"{sample_id}_f4*.png"):
        copy_file(optional_fig, sra_dir / "figures" / optional_fig.name, required=False, label="optional_f4")

    for optional_fig in (run_dir / "figures").glob(f"{sample_id}_f5*.png"):
        copy_file(optional_fig, sra_dir / "figures" / optional_fig.name, required=False, label="optional_f5")

    stage12 = run_dir / "logs" / "stage12_exploration"
    if stage12.exists():
        for p in stage12.rglob("*.tsv"):
            rel = p.relative_to(stage12)
            copy_file(p, sra_dir / "sql_outputs" / rel, required=False, label="stage12_exploration_tsv")

audit_path = DEST / "contrast_01_input_build_audit.tsv"
pd.DataFrame(audit).to_csv(audit_path, sep="\t", index=False)

print(f"Completed contrast input build.")
print(f"Wrote audit: {audit_path}")
print(f"Processed SRAs: {len(manifest)}")
