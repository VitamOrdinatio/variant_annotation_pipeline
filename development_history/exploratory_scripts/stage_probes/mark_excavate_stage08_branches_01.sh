#!/usr/bin/env bash
set -euo pipefail

PROBE_NAME="mark_excavate_stage08_branches_01"
LOG="/root/Desktop/${PROBE_NAME}.log"
VAP_REPO="/root/Desktop/variant_annotation_pipeline"
RUN_DIR="${VAP_REPO}/results/run_2026_05_15_063040"
PROCESSED="${RUN_DIR}/processed"

{
echo "========================================"
echo "${PROBE_NAME}"
echo "Stage 08 branch overlap and conservation"
echo "Started: $(date -Is)"
echo "Host: $(hostname)"
echo "========================================"
echo

cd "${VAP_REPO}"
source .venv/bin/activate

echo "[probe metadata]"
echo "vap_repo=${VAP_REPO}"
echo "run_dir=${RUN_DIR}"
echo "processed_dir=${PROCESSED}"
echo "python=$(which python)"
echo

python - <<'PY'
from pathlib import Path
import csv
from itertools import combinations

processed=Path("/root/Desktop/variant_annotation_pipeline/results/run_2026_05_15_063040/processed")

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
for label,name in files.items():
    path=processed/name
    print(f"{label}\t{name}\texists={path.exists()}\tsize_bytes={path.stat().st_size if path.exists() else 'NA'}")
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
print("[row counts and unique variant_id counts]")
for label,name in files.items():
    path=processed/name
    vals=read_variant_ids(path)
    ids[label]=set(vals)
    duplicate_count=len(vals)-len(set(vals))
    print(f"{label}\trows={len(vals)}\tunique_variant_ids={len(set(vals))}\tduplicate_variant_id_rows={duplicate_count}")
print()

branch_labels=["coding","splice","noncoding"]
print("[branch overlaps]")
for a,b in combinations(branch_labels,2):
    overlap=ids[a] & ids[b]
    print(f"{a}_AND_{b}\tunique_variant_ids={len(overlap)}")
print()

print("[branch union]")
branch_union=set().union(*(ids[label] for label in branch_labels))
print(f"coding_OR_splice_OR_noncoding\tunique_variant_ids={len(branch_union)}")
print(f"selected_unique_variant_ids\tunique_variant_ids={len(ids['selected'])}")
print(f"vdb_ready_unique_variant_ids\tunique_variant_ids={len(ids['vdb_ready'])}")
print(f"variant_summary_unique_variant_ids\tunique_variant_ids={len(ids['variant_summary'])}")
print()

print("[qc overlay intersections]")
for label in branch_labels:
    overlap=ids[label] & ids["qc_flagged"]
    print(f"qc_flagged_AND_{label}\tunique_variant_ids={len(overlap)}")
print(f"qc_flagged_total\tunique_variant_ids={len(ids['qc_flagged'])}")
print()

print("[reconciliation checks]")
checks=[]
checks.append(("selected_equals_vdb_ready",ids["selected"]==ids["vdb_ready"]))
checks.append(("selected_equals_variant_summary",ids["selected"]==ids["variant_summary"]))
checks.append(("branch_union_equals_selected",branch_union==ids["selected"]))
checks.append(("coding_noncoding_disjoint",len(ids["coding"] & ids["noncoding"])==0))
checks.append(("splice_noncoding_disjoint",len(ids["splice"] & ids["noncoding"])==0))
checks.append(("qc_subset_of_selected",ids["qc_flagged"].issubset(ids["selected"])))
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