#!/usr/bin/env bash
set -euo pipefail

TS="$(date +%Y%m%d_%H%M%S)"
LOG="/root/Desktop/mark_bootstrap_vep_install_${TS}.log"
REPO_ROOT="$HOME/dev/portfolio_projects/variant_annotation_pipeline"
VEP_ROOT="/root/tools/vep/ensembl-vep-release-115.0"

exec > >(tee "$LOG") 2>&1

echo "[INFO] Mark VEP bootstrap started at $(date)"
echo "[INFO] Log file: $LOG"
echo "[INFO] Repo root: $REPO_ROOT"
echo "[INFO] VEP root: $VEP_ROOT"
echo

cd "$REPO_ROOT"
source .venv/bin/activate

echo "=== PRECHECKS ==="
echo "[CMD] ls -lah /root/tools/vep"
ls -lah /root/tools/vep || true
echo

echo "[CMD] ls -lah $VEP_ROOT"
ls -lah "$VEP_ROOT" || true
echo

echo "[CMD] ls -lah $VEP_ROOT/INSTALL.pl"
ls -lah "$VEP_ROOT/INSTALL.pl" || true
echo

echo "=== RUN INSTALL.PL ==="
cd "$VEP_ROOT"
echo "[CMD] perl INSTALL.pl --NO_TEST"
perl INSTALL.pl --NO_TEST || true
echo

echo "=== POST-INSTALL HELP CHECK ==="
echo "[CMD] /root/tools/vep/vep --help | head"
"/root/tools/vep/vep" --help | head || true
echo

echo "[INFO] Mark VEP bootstrap completed at $(date)"
echo "[INFO] Log file saved to: $LOG"