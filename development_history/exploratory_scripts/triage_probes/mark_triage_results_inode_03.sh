#!/usr/bin/env bash
set -euo pipefail

PROBE_NAME="mark_triage_results_inode_03"
LOG="/root/Desktop/${PROBE_NAME}.txt"

{
echo "========================================"
echo "${PROBE_NAME}"
echo "results inode and orphan reconnaissance"
echo "Started: $(date -Is)"
echo "Host: $(hostname)"
echo "========================================"
echo

REPO="/root/dev/portfolio_projects/variant_annotation_pipeline"

echo "[repo listing]"
ls -la "${REPO}" || true
echo

echo "[results symlink metadata]"
stat "${REPO}/results" || true
echo

echo "[parent inode info]"
stat "${REPO}" || true
echo

echo "[search nearby orphan-like directories]"
find "${REPO}" -maxdepth 3 \( -type d -o -type l \) | sort
echo

echo "[search entire filesystem for known run names]"
find /root -type d \( -name "run_2026_*" -o -name "*063040*" -o -name "*082417*" \) 2>/dev/null
echo

echo "[search for large VAP TSV artifacts]"
find /root -type f \( -name "stage_11_prioritized_variants.tsv" -o -name "stage_12_validation_candidates.tsv" -o -name "coding_candidates.tsv" \) 2>/dev/null
echo

echo "Finished: $(date -Is)"
} > "${LOG}" 2>&1

echo "Wrote ${LOG}"