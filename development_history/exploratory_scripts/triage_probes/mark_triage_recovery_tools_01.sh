#!/usr/bin/env bash
set -euo pipefail

PROBE_NAME="mark_triage_recovery_tools_01"
LOG="/root/Desktop/${PROBE_NAME}.txt"

{
echo "========================================"
echo "${PROBE_NAME}"
echo "VAP results recovery triage: tool and filesystem survey"
echo "Started: $(date -Is)"
echo "Host: $(hostname)"
echo "========================================"
echo

echo "[tool availability]"
for tool in extundelete testdisk photorec debugfs e2fsck dumpe2fs lsblk findmnt lsof strings grep awk sed stat file git; do
    if command -v "${tool}" >/dev/null 2>&1; then
        echo "FOUND	${tool}	$(command -v "${tool}")"
    else
        echo "MISSING	${tool}"
    fi
done
echo

echo "[root mount]"
mount | grep ' / ' || true
echo

echo "[findmnt root]"
findmnt / || true
echo

echo "[block devices]"
lsblk -f || true
echo

echo "[filesystem usage]"
df -h || true
echo

echo "[repo results symlink]"
REPO="/root/dev/portfolio_projects/variant_annotation_pipeline"
if [ -e "${REPO}" ] || [ -L "${REPO}" ]; then
    echo "repo_exists=true"
    cd "${REPO}"
    pwd
    ls -ld results || true
    file results || true
    readlink results || true
    readlink -f results || true
    git status --short || true
    git ls-files -s results || true
else
    echo "repo_exists=false"
fi
echo

echo "[deleted open files]"
lsof +L1 2>/dev/null | grep -E "run_2026|variant_annotation_pipeline|vap|results" || true
echo

echo "[recent shell history hints]"
history 2>/dev/null | grep -E "results|vap_runs|ln -s|rm |git pull|git checkout" | tail -80 || true
echo

echo "Finished: $(date -Is)"
} > "${LOG}" 2>&1

echo "Wrote ${LOG}"