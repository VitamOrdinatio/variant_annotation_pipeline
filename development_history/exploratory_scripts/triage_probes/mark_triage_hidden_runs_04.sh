#!/usr/bin/env bash
set -euo pipefail

PROBE_NAME="mark_triage_hidden_runs_04"
LOG="/root/Desktop/${PROBE_NAME}.txt"

{
echo "========================================"
echo "${PROBE_NAME}"
echo "hidden/orphan VAP run reconnaissance"
echo "Started: $(date -Is)"
echo "Host: $(hostname)"
echo "========================================"
echo

echo "[trash inventory]"
find /root/.local/share/Trash/files \
    \( -type d -o -type f \) \
    \( -iname "*run_2026*" \
    -o -iname "*processed*" \
    -o -iname "*coding_candidates*" \
    -o -iname "*stage_11*" \
    -o -iname "*stage_12*" \
    -o -iname "*variant*" \) \
    2>/dev/null
echo

echo "[non-desktop run search]"
find /root \
    -path "/root/Desktop" -prune -o \
    -path "/root/Desktop/*" -prune -o \
    \( -type d -o -type f \) \
    \( -iname "*run_2026*" \
    -o -iname "*processed*" \
    -o -iname "*coding_candidates*" \
    -o -iname "*stage_11_prioritized_variants.tsv" \
    -o -iname "*stage_12_validation_candidates.tsv" \) \
    -print 2>/dev/null
echo

echo "[large surviving TSV search outside Desktop]"
find /root \
    -path "/root/Desktop" -prune -o \
    -path "/root/Desktop/*" -prune -o \
    -type f -name "*.tsv" -size +50M \
    -print 2>/dev/null
echo

echo "[recently modified filesystem objects near incident window]"
find /root/dev/portfolio_projects/variant_annotation_pipeline \
    -not -path "*/.git/*" \
    -newermt "2026-05-20 20:20:00" \
    ! -newermt "2026-05-20 20:40:00" \
    -ls 2>/dev/null
echo

echo "Finished: $(date -Is)"
} > "${LOG}" 2>&1

echo "Wrote ${LOG}"