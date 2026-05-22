#!/usr/bin/env bash
set -euo pipefail

PROBE_NAME="mark_triage_tarball_inspect_05"
LOG="/root/Desktop/${PROBE_NAME}.txt"

{
echo "========================================"
echo "${PROBE_NAME}"
echo "tarball reconnaissance"
echo "Started: $(date -Is)"
echo "Host: $(hostname)"
echo "========================================"
echo

TARGET="/root/.local/share/Trash/files/run_2026_04_17_082417.tar.gz"

echo "[existence]"
ls -lh "${TARGET}" || true
echo

echo "[file type]"
file "${TARGET}" || true
echo

echo "[tarball top-level listing]"
tar -tzf "${TARGET}" | head -200
echo

echo "[processed subtree glimpse]"
tar -tzf "${TARGET}" | grep "processed/" | head -200 || true
echo

echo "[stage artifact glimpse]"
tar -tzf "${TARGET}" | grep -E "stage_0|stage_1|coding_candidates|noncoding|prioritized|validation" | head -300 || true
echo

echo "Finished: $(date -Is)"
} > "${LOG}" 2>&1

echo "Wrote ${LOG}"