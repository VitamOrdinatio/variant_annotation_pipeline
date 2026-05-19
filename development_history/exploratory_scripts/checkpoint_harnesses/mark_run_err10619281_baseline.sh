#!/usr/bin/env bash
set -euo pipefail

source .venv/bin/activate

CONFIG="config/config.mark.err10619281.baseline.yaml"
LOGFILE="/root/Desktop/mark_err10619281_baseline_$(date -u +%Y%m%dT%H%M%SZ).txt"

{
  echo "===== CONFIG VALIDATION ====="
  python src/config_loader.py --config "$CONFIG"

  echo
  echo "===== VERIFY LOCK BYPASS ====="
  grep -n "allow_non_hg002" pipeline/stage_01_load_data.py

  echo
  echo "===== VERIFY FASTQ INPUTS ====="
  python - <<'PY'
import yaml
from pathlib import Path
config_path = "config/config.mark.err10619281.baseline.yaml"
with open(config_path, "r", encoding="utf-8") as handle:
    cfg = yaml.safe_load(handle)
for label in ["r1", "r2"]:
    path = Path(cfg["input"]["fastq"][label])
    print(f"{label.upper()}: {path}")
    print(f"{label.upper()} exists: {path.exists()}")
PY

  echo
  echo "===== PYTEST PREFLIGHT ====="
  python -m pytest -q

  echo
  echo "===== STARTING ERR10619281 BASELINE RUN ====="
  python run_pipeline.py --config "$CONFIG"

} 2>&1 | tee "$LOGFILE"

echo "Log written to: $LOGFILE"
