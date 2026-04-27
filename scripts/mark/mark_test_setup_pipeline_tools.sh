#!/usr/bin/env bash
set -euo pipefail

TS="$(date +%Y%m%d_%H%M%S)"
LOG="/root/Desktop/mark_test_setup_pipeline_tools_${TS}.log"
REPO_ROOT="$HOME/dev/portfolio_projects/variant_annotation_pipeline"

exec > >(tee "$LOG") 2>&1

echo "[INFO] Mark setup_pipeline_tools test started at $(date)"
echo "[INFO] Log file: $LOG"
echo "[INFO] Initial working directory: $(pwd)"
echo "[INFO] Target repo root: $REPO_ROOT"
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

echo "=== REPO STATUS ==="
echo "[CMD] git status"
git status || true
echo

echo "=== CONFIG SNAPSHOT ==="
echo "[CMD] grep -n 'gatk\\|vep\\|annovar' config/config.mark.local.yaml"
grep -n 'gatk\|vep\|annovar' config/config.mark.local.yaml || true
echo

echo "=== TOOL SCRIPT STATUS MODE ==="
echo "[CMD] TARGET_ENV=mark MODE=status bash scripts/tools/setup_pipeline_tools.sh"
TARGET_ENV=mark MODE=status bash scripts/tools/setup_pipeline_tools.sh || true
echo

echo "=== TOOL SCRIPT PROVISION MODE ==="
echo "[CMD] TARGET_ENV=mark MODE=provision bash scripts/tools/setup_pipeline_tools.sh"
TARGET_ENV=mark MODE=provision bash scripts/tools/setup_pipeline_tools.sh || true
echo

echo "=== POST-RUN TOOL LAYOUT ==="
echo "[CMD] tree -L 3 /root/tools"
tree -L 3 /root/tools || true
echo

echo "[CMD] ls -lah /root/tools/gatk"
ls -lah /root/tools/gatk || true
echo

echo "[CMD] ls -lah /root/tools/vep"
ls -lah /root/tools/vep || true
echo

echo "[CMD] ls -lah /root/tools/annovar"
ls -lah /root/tools/annovar || true
echo

echo "=== DIRECT GATK CHECK ==="
echo "[CMD] /root/tools/gatk/gatk --version"
"/root/tools/gatk/gatk" --version || true
echo

echo "[INFO] Mark setup_pipeline_tools test completed at $(date)"
echo "[INFO] Log file saved to: $LOG"