#!/usr/bin/env bash
set -euo pipefail

TS="$(date +%Y%m%d_%H%M%S)"
LOG="/root/Desktop/mark_vep_probe_${TS}.log"
REPO_ROOT="$HOME/dev/portfolio_projects/variant_annotation_pipeline"

exec > >(tee "$LOG") 2>&1

echo "[INFO] Mark VEP probe started at $(date)"
echo "[INFO] Log file: $LOG"
echo "[INFO] Initial working directory: $(pwd)"
echo "[INFO] Target repo root: $REPO_ROOT"
echo

cd "$REPO_ROOT"
echo "[INFO] Current working directory: $(pwd)"
echo

echo "[STEP] Activating VAP .venv"
# shellcheck disable=SC1091
source .venv/bin/activate
echo "[INFO] Venv activated."
echo

echo "=== BASIC TOOL CHECKS ==="
echo "[CMD] which perl"
which perl || true
echo

echo "[CMD] perl -v | head -n 5"
perl -v | head -n 5 || true
echo

echo "[CMD] which vep"
which vep || true
echo

echo "[CMD] vep --help | head"
vep --help | head || true
echo

echo "=== PACKAGE / PATH DISCOVERY ==="
echo "[CMD] find /root/tools /usr/local /usr/bin /opt -maxdepth 4 -name vep 2>/dev/null"
find /root/tools /usr/local /usr/bin /opt -maxdepth 4 -name vep 2>/dev/null || true
echo

echo "[CMD] apt-cache policy ensembl-vep"
apt-cache policy ensembl-vep || true
echo

echo "[CMD] apt-cache search ensembl-vep"
apt-cache search ensembl-vep || true
echo

echo "=== TARGET LAYOUT CHECK ==="
echo "[CMD] ls -lah /root/tools"
ls -lah /root/tools || true
echo

echo "[CMD] ls -lah /root/tools/vep"
ls -lah /root/tools/vep || true
echo

echo "[CMD] ls -lah /data/storage/reference/vep"
ls -lah /data/storage/reference/vep || true
echo

echo "[CMD] ls -lah /data/storage/reference/vep/cache"
ls -lah /data/storage/reference/vep/cache || true
echo

echo "=== VAP RESOURCE SCRIPT STATUS ==="
echo "[CMD] TARGET_ENV=mark MODE=status bash scripts/resources/setup_annotation_resources.sh"
TARGET_ENV=mark MODE=status bash scripts/resources/setup_annotation_resources.sh || true
echo

echo "[INFO] Mark VEP probe completed at $(date)"
echo "[INFO] Log file saved to: $LOG"