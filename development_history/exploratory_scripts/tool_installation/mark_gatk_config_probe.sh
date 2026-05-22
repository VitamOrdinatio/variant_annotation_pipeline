#!/usr/bin/env bash
set -euo pipefail

TS="$(date +%Y%m%d_%H%M%S)"
LOG="/root/Desktop/mark_gatk_config_probe_${TS}.log"
REPO_ROOT="$HOME/dev/portfolio_projects/variant_annotation_pipeline"

exec > >(tee "$LOG") 2>&1

echo "[INFO] Mark GATK/config probe started at $(date)"
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

echo "=== VENV / PYTHON CONTEXT ==="
echo "[CMD] which python"
which python || true
echo
echo "[CMD] python --version"
python --version || true
echo
echo "[CMD] which python3"
which python3 || true
echo
echo "[CMD] python3 --version"
python3 --version || true
echo
echo "[CMD] echo \$PATH"
echo "$PATH"
echo

echo "=== CONFIG FILES ==="
echo "[CMD] ls -lah config"
ls -lah config || true
echo

ACTIVE_CONFIG="config/config.mark.local.yaml"
if [[ ! -f "$ACTIVE_CONFIG" ]]; then
  echo "[WARN] $ACTIVE_CONFIG not found. Falling back to config/config.yaml"
  ACTIVE_CONFIG="config/config.yaml"
fi

echo "[INFO] ACTIVE_CONFIG=$ACTIVE_CONFIG"
echo

echo "=== GATK CONFIG EXTRACTION ==="
echo "[CMD] python - <<'PY' ..."
python - <<'PY'
import yaml
from pathlib import Path

config_path = Path("config/config.mark.local.yaml")
if not config_path.exists():
    config_path = Path("config/config.yaml")

print(f"CONFIG_PATH={config_path}")

with config_path.open("r", encoding="utf-8") as handle:
    cfg = yaml.safe_load(handle)

gatk_cfg = cfg.get("tools", {}).get("gatk", {})
print(f"GATK_EXECUTABLE={gatk_cfg.get('executable')}")
print(f"GATK_JAVA_OPTIONS={gatk_cfg.get('java_options')}")
print(f"GATK_EMIT_MODE={gatk_cfg.get('haplotypecaller_emit_mode')}")
PY
echo

echo "=== RAW YAML GATK LINES ==="
echo "[CMD] grep -n 'gatk\\|java_options\\|haplotypecaller_emit_mode' \$ACTIVE_CONFIG"
grep -n 'gatk\|java_options\|haplotypecaller_emit_mode' "$ACTIVE_CONFIG" || true
echo

echo "=== GATK PATH RESOLUTION ==="
echo "[CMD] which gatk"
which gatk || true
echo

echo "[CMD] ls -lah /root/tools/gatk"
ls -lah /root/tools/gatk || true
echo

echo "[CMD] ls -lah /root/tools/gatk/gatk"
ls -lah /root/tools/gatk/gatk || true
echo

echo "[CMD] file /root/tools/gatk/gatk"
file /root/tools/gatk/gatk || true
echo

echo "=== GATK EXECUTION CHECKS ==="
echo "[CMD] /root/tools/gatk/gatk --help | head"
"/root/tools/gatk/gatk" --help | head || true
echo

echo "[CMD] gatk --help | head"
gatk --help | head || true
echo

echo "=== STAGE 05 FILE REFERENCE ==="
echo "[CMD] grep -n 'gatk_executable\\|tools\\[\"gatk\"\\]\\|HaplotypeCaller' pipeline/stage_05_call_variants.py"
grep -n 'gatk_executable\|tools\["gatk"\]\|HaplotypeCaller' pipeline/stage_05_call_variants.py || true
echo

echo "[INFO] Mark GATK/config probe completed at $(date)"
echo "[INFO] Log file saved to: $LOG"