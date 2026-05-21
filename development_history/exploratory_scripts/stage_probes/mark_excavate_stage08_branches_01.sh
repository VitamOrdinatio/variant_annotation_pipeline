#!/usr/bin/env bash
set -euo pipefail

PROBE_NAME="mark_excavate_stage08_branches_01"
LOG="/root/Desktop/${PROBE_NAME}.log"
RUN_ID="run_2026_05_15_063040"

{
echo "========================================"
echo "${PROBE_NAME}"
echo "Stage 08 branch overlap and conservation"
echo "Started: $(date -Is)"
echo "Host: $(hostname)"
echo "========================================"
echo

VAP_REPO="$(git rev-parse --show-toplevel)"
cd "${VAP_REPO}"
source .venv/bin/activate

RUN_DIR="${VAP_REPO}/results/${RUN_ID}"
PROCESSED="${RUN_DIR}/processed"

echo "[probe metadata]"
echo "vap_repo=${VAP_REPO}"
echo "run_id=${RUN_ID}"
echo "run_dir=${RUN_DIR}"
echo "processed_dir=${PROCESSED}"
echo "python=$(which python)"
echo

python - <<'PY'
from pathlib import Path
import csv
from itertools import combinations

run_id="run_2026_05_15_063040"
repo=Path.cwd()
processed=repo/"results"/run_id/"processed"

files={
    "selected":"stage_08_selected_transcript_consequences.tsv",
    "vdb_ready":"stage_08_vdb_ready_variants.tsv",
    "variant_summary":"stage_08_variant_summary.tsv",
    "coding":"coding_candidates.tsv",
    "splice":"splice_region_candidates.tsv",
    "noncoding":"noncoding_candidates.tsv",
    "qc_flagged":"qc_flagged.tsv",
}

print("[artifact existence]")
missing=[]
for label,name in files.items():
    path=processed/name
    exists=path.exists()
    if not exists:
        missing.append(str(path))
    print(f"{label}\t{name}\texists={exists}\tsize_bytes={path.stat().st_size if exists else 'NA'}")
if missing:
    raise FileNotFoundError("Missing required artifacts: " + "; ".join(missing))
print()

def read_variant_ids(path):
    ids=[]
    with path.open("r",encoding="utf-8",errors="replace",newline="") as handle:
        reader=csv.DictReader(handle,delimiter="\t")
        if "variant_id" not in (reader.fieldnames or []):
            raise ValueError(f"Missing variant_id column in {path}")
        for row in reader:
            ids.append(row["variant_id"])
    return ids

ids={}
print("[row counts]")
for label,name in files.items():
    vals=read_variant_ids(processed/name)
    ids[label]=set(vals)
    print(f"{label}\trows={len(vals)}")
print()

print("[unique variant_id counts]")
for label,name in files.items():
    vals=read_variant_ids(processed/name)
    duplicate_count=len(vals)-len(set(vals))
    print(f"{label}\tunique_variant_ids={len(set(vals))}\tduplicate_variant_id_rows={duplicate_count}")
print()

branch_labels=["coding","splice","noncoding"]
print("[branch overlaps]")
for a,b in combinations(branch_labels,2):
    overlap=ids[a] & ids[b]
    print(f"{a}_AND_{b}\tunique_variant_ids={len(overlap)}")
print()

print("[QC overlay intersections]")
for label in branch_labels:
    overlap=ids[label] & ids["qc_flagged"]
    print(f"qc_flagged_AND_{label}\tunique_variant_ids={len(overlap)}")
print(f"qc_flagged_total\tunique_variant_ids={len(ids['qc_flagged'])}")
print()

print("[reconciliation checks]")
branch_union=set().union(*(ids[label] for label in branch_labels))
checks=[
    ("selected_equals_vdb_ready",ids["selected"]==ids["vdb_ready"]),
    ("selected_equals_variant_summary",ids["selected"]==ids["variant_summary"]),
    ("branch_union_equals_selected",branch_union==ids["selected"]),
    ("coding_noncoding_disjoint",len(ids["coding"] & ids["noncoding"])==0),
    ("splice_noncoding_disjoint",len(ids["splice"] & ids["noncoding"])==0),
    ("qc_subset_of_selected",ids["qc_flagged"].issubset(ids["selected"])),
]
for name,status in checks:
    print(f"{name}\t{'PASS' if status else 'WARN'}")
print()

print("[summary verdict]")
if all(status for _,status in checks):
    print("PASS\tStage 08 branch model reconciles under current probe assumptions.")
else:
    print("WARN\tOne or more Stage 08 reconciliation checks failed; inspect overlap/reconciliation sections.")
PY

echo
echo "Finished: $(date -Is)"
} > "${LOG}" 2>&1

echo "Wrote ${LOG}"