#!/usr/bin/env bash
set -euo pipefail

TS="$(date +%Y%m%d_%H%M%S)"
LOG="/root/Desktop/mark_finalize_vep_install_${TS}.log"
REPO_ROOT="$HOME/dev/portfolio_projects/variant_annotation_pipeline"
VEP_ROOT="/root/tools/vep/ensembl-vep-release-115.2"

exec > >(tee "$LOG") 2>&1

echo "[INFO] Mark VEP final bootstrap started at $(date)"
echo "[INFO] Log file: $LOG"
echo "[INFO] Repo root: $REPO_ROOT"
echo "[INFO] VEP root: $VEP_ROOT"
echo

cd "$REPO_ROOT"
source .venv/bin/activate

echo "=== RUN INSTALL.PL (MULTI-PROMPT HANDLING) ==="
cd "$VEP_ROOT"

echo "[CMD] printf 'n\ny\n' | perl INSTALL.pl --NO_TEST"
printf 'n\ny\n' | perl INSTALL.pl --NO_TEST || true
echo

echo "=== VERIFY CORE MODULE ==="
echo "[CMD] perl -MBio::EnsEMBL::Registry -e 'print \"OK\n\"'"
perl -MBio::EnsEMBL::Registry -e 'print "OK\n"' || true
echo

echo "=== FINAL VEP TEST ==="
echo "[CMD] /root/tools/vep/vep --help | head"
"/root/tools/vep/vep" --help | head || true
echo

echo "=== DIRECTORY CHECK ==="
echo "[CMD] ls -lah $VEP_ROOT/Bio"
ls -lah "$VEP_ROOT/Bio" || true
echo

echo "[INFO] Mark VEP final bootstrap completed at $(date)"
echo "[INFO] Log file saved to: $LOG"