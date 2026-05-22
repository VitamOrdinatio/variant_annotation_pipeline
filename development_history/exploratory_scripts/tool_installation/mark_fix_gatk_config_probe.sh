#!/usr/bin/env bash
set -euo pipefail

TS="$(date +%Y%m%d_%H%M%S)"
LOG="/root/Desktop/mark_fix_gatk_config_probe_${TS}.log"
REPO_ROOT="$HOME/dev/portfolio_projects/variant_annotation_pipeline"

exec > >(tee "$LOG") 2>&1

echo "[INFO] Mark GATK config fix probe started at $(date)"
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

ACTIVE_CONFIG="config/config.mark.local.yaml"
if [[ ! -f "$ACTIVE_CONFIG" ]]; then
  echo "[ERROR] Missing $ACTIVE_CONFIG"
  exit 1
fi

echo "=== BEFORE EDIT ==="
echo "[CMD] grep -n 'gatk\\|java_options\\|haplotypecaller_emit_mode' $ACTIVE_CONFIG"
grep -n 'gatk\|java_options\|haplotypecaller_emit_mode' "$ACTIVE_CONFIG" || true
echo

echo "[STEP] Rewriting GATK executable in $ACTIVE_CONFIG"
python - <<'PY'
from pathlib import Path
import yaml

config_path = Path("config/config.mark.local.yaml")
with config_path.open("r", encoding="utf-8") as handle:
    cfg = yaml.safe_load(handle)

cfg["tools"]["gatk"]["executable"] = "/root/tools/gatk/gatk"

with config_path.open("w", encoding="utf-8") as handle:
    yaml.safe_dump(cfg, handle, sort_keys=False)

print(f"UPDATED_CONFIG={config_path}")
print(f"NEW_GATK_EXECUTABLE={cfg['tools']['gatk']['executable']}")
PY
echo

echo "=== AFTER EDIT ==="
echo "[CMD] grep -n 'gatk\\|java_options\\|haplotypecaller_emit_mode' $ACTIVE_CONFIG"
grep -n 'gatk\|java_options\|haplotypecaller_emit_mode' "$ACTIVE_CONFIG" || true
echo

echo "=== DIRECT EXECUTION CHECK ==="
echo "[CMD] /root/tools/gatk/gatk --version"
"/root/tools/gatk/gatk" --version || true
echo

echo "=== CONFIG-DRIVEN EXECUTION CHECK ==="
echo "[CMD] python - <<'PY' ..."
python - <<'PY'
from pathlib import Path
import subprocess
import yaml

config_path = Path("config/config.mark.local.yaml")
with config_path.open("r", encoding="utf-8") as handle:
    cfg = yaml.safe_load(handle)

gatk_executable = cfg["tools"]["gatk"]["executable"]
print(f"GATK_EXECUTABLE_FROM_CONFIG={gatk_executable}")

result = subprocess.run(
    [gatk_executable, "--version"],
    capture_output=True,
    text=True,
    check=False,
)
print(f"RETURN_CODE={result.returncode}")
print("STDOUT_BEGIN")
print(result.stdout.strip())
print("STDOUT_END")
print("STDERR_BEGIN")
print(result.stderr.strip())
print("STDERR_END")
PY
echo

echo "[INFO] Mark GATK config fix probe completed at $(date)"
echo "[INFO] Log file saved to: $LOG"
