#!/usr/bin/env bash
set -euo pipefail

TS="$(date +%Y%m%d_%H%M%S)"
LOG="/root/Desktop/mark_install_vep_htslib_deps_${TS}.log"
REPO_ROOT="$HOME/dev/portfolio_projects/variant_annotation_pipeline"
VEP_ROOT="/root/tools/vep/ensembl-vep-release-115.2"

exec > >(tee "$LOG") 2>&1

echo "[INFO] Mark VEP HTS dependency install started at $(date)"
echo "[INFO] Log file: $LOG"
echo "[INFO] Repo root: $REPO_ROOT"
echo "[INFO] VEP root: $VEP_ROOT"
echo

cd "$REPO_ROOT"
source .venv/bin/activate

echo "=== INSTALL SYSTEM LIBRARIES ==="
echo "[CMD] apt-get update"
apt-get update
echo

echo "[CMD] apt-get install -y libbz2-dev liblzma-dev zlib1g-dev"
apt-get install -y libbz2-dev liblzma-dev zlib1g-dev
echo

echo "=== VERIFY HEADERS ==="
echo "[CMD] ls /usr/include | grep -E 'bz|lzma'"
ls /usr/include | grep -E 'bz|lzma' || true
echo

echo "=== RERUN INSTALL.PL ==="
cd "$VEP_ROOT"
echo "[CMD] printf 'n\n' | perl INSTALL.pl --NO_TEST"
printf 'n\n' | perl INSTALL.pl --NO_TEST || true
echo

echo "=== POST-INSTALL HELP CHECK ==="
echo "[CMD] /root/tools/vep/vep --help | head"
"/root/tools/vep/vep" --help | head || true
echo

echo "[INFO] Mark VEP HTS dependency install completed at $(date)"
echo "[INFO] Log file saved to: $LOG"