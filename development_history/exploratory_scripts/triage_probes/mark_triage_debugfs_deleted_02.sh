#!/usr/bin/env bash
set -euo pipefail

PROBE_NAME="mark_triage_debugfs_deleted_02"
LOG="/root/Desktop/${PROBE_NAME}.txt"

{
echo "========================================"
echo "${PROBE_NAME}"
echo "debugfs deleted inode reconnaissance"
echo "Started: $(date -Is)"
echo "Host: $(hostname)"
echo "========================================"
echo

echo "[filesystem]"
mount | grep ' / ' || true
echo

echo "[debugfs deleted inode scan]"
echo "THIS MAY TAKE A FEW MINUTES"
echo

debugfs -R "lsdel" /dev/rbd1 2>/dev/null | head -200

echo
echo "[grep likely VAP signatures from deleted inode table]"
echo

debugfs -R "lsdel" /dev/rbd1 2>/dev/null | grep -Ei "vap|variant|result|run_2026|err106|hg002" || true

echo
echo "Finished: $(date -Is)"
} > "${LOG}" 2>&1

echo "Wrote ${LOG}"