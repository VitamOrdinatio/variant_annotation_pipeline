#!/usr/bin/env bash
set -euo pipefail

TS="$(date -u +%Y%m%dT%H%M%SZ)"
LOG="mark_phase1a_hg002_baseline_${TS}.log"

echo "[INFO] Phase 1A HG002 baseline started at $(date -u)" | tee "$LOG"
echo "[INFO] Host: $(hostname)" | tee -a "$LOG"
echo "[INFO] Working directory: $(pwd)" | tee -a "$LOG"
echo "[INFO] Git commit: $(git rev-parse HEAD)" | tee -a "$LOG"

echo "[INFO] Running pytest preflight" | tee -a "$LOG"
pytest -q 2>&1 | tee -a "$LOG"

echo "[INFO] Running post-VEP fixture preflight" | tee -a "$LOG"
python run_pipeline.py --config config/config.example.post_vep.yaml 2>&1 | tee -a "$LOG"

echo "[INFO] Running HG002 Phase 1A baseline" | tee -a "$LOG"
python run_pipeline.py --config config/config.mark.baseline.yaml 2>&1 | tee -a "$LOG"

echo "[INFO] Phase 1A HG002 baseline finished at $(date -u)" | tee -a "$LOG"
