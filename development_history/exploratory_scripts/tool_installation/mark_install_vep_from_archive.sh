#!/usr/bin/env bash
set -euo pipefail

TS="$(date +%Y%m%d_%H%M%S)"
LOG="/root/Desktop/mark_install_vep_from_archive_${TS}.log"
REPO_ROOT="$HOME/dev/portfolio_projects/variant_annotation_pipeline"
VEP_ARCHIVE="/root/Desktop/ensembl-vep-release-115.0.tar.gz"

exec > >(tee "$LOG") 2>&1

echo "[INFO] Mark VEP install-from-archive test started at $(date)"
echo "[INFO] Log file: $LOG"
echo "[INFO] Initial working directory: $(pwd)"
echo "[INFO] Target repo root: $REPO_ROOT"
echo "[INFO] VEP_ARCHIVE=$VEP_ARCHIVE"
echo

echo "[STEP] Changing into VAP repo root"
cd "$REPO_ROOT"
echo "[INFO] Current working directory: $(pwd)"
echo

echo "[STEP] Activating VAP .venv"
if [[ ! -f ".venv/bin/activate" ]]; then
  echo "[ERROR] Missing virtual environment activate script: $REPO_ROOT/.venv/bin/activate"
  exit 1
fi
# shellcheck disable=SC1091
source .venv/bin/activate
echo "[INFO] Venv activated."
echo

echo "=== PRECHECKS ==="
echo "[CMD] ls -lah $VEP_ARCHIVE"
ls -lah "$VEP_ARCHIVE"
echo

echo "=== BEFORE PROVISION ==="
echo "[CMD] TARGET_ENV=mark MODE=status bash scripts/tools/setup_pipeline_tools.sh"
TARGET_ENV=mark MODE=status bash scripts/tools/setup_pipeline_tools.sh || true
echo

echo "=== RUN VEP PROVISION THROUGH REPO SCRIPT ==="
echo "[CMD] TARGET_ENV=mark MODE=provision VEP_SOURCE_ARCHIVE=$VEP_ARCHIVE bash scripts/tools/setup_pipeline_tools.sh"
TARGET_ENV=mark MODE=provision VEP_SOURCE_ARCHIVE="$VEP_ARCHIVE" bash scripts/tools/setup_pipeline_tools.sh || true
echo

echo "=== AFTER PROVISION ==="
echo "[CMD] TARGET_ENV=mark MODE=status bash scripts/tools/setup_pipeline_tools.sh"
TARGET_ENV=mark MODE=status bash scripts/tools/setup_pipeline_tools.sh || true
echo

echo "=== POST-RUN VEP LAYOUT ==="
echo "[CMD] tree -L 4 /root/tools/vep"
tree -L 4 /root/tools/vep || true
echo

echo "[CMD] find /root/tools/vep -maxdepth 6 -name vep -type f"
find /root/tools/vep -maxdepth 6 -name vep -type f 2>/dev/null || true
echo

echo "[CMD] ls -lah /root/tools/vep/vep"
ls -lah /root/tools/vep/vep || true
echo

echo "[CMD] file /root/tools/vep/vep"
file /root/tools/vep/vep || true
echo

echo "[CMD] /root/tools/vep/vep --help | head"
"/root/tools/vep/vep" --help | head || true
echo

echo "[INFO] Mark VEP install-from-archive test completed at $(date)"
echo "[INFO] Log file saved to: $LOG"