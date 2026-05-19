#!/usr/bin/env bash
set -euo pipefail

TS="$(date +%Y%m%d_%H%M%S)"
LOG="/root/Desktop/mark_run_stage12_checkpoint_${TS}.log"
REPO_ROOT="$HOME/dev/portfolio_projects/variant_annotation_pipeline"
CONFIG_PATH="$REPO_ROOT/config/config.mark.local.yaml"

exec > >(tee "$LOG") 2>&1

echo "[INFO] Mark Stage 12 checkpoint run started at $(date)"
echo "[INFO] Log file: $LOG"
echo "[INFO] Repo root: $REPO_ROOT"
echo "[INFO] Config path: $CONFIG_PATH"
echo

cd "$REPO_ROOT"
source .venv/bin/activate

echo "=== REPO STATUS ==="
git status --short || true
echo

echo "=== FIND LATEST STAGE 11 OUTPUT ==="
PRIORITIZED_VARIANTS="$(find "$REPO_ROOT/results" -type f -name "stage_11_prioritized_variants.tsv" | sort | tail -n 1 || true)"

if [[ -z "${PRIORITIZED_VARIANTS:-}" ]]; then
  echo "[ERROR] No stage_11_prioritized_variants.tsv found."
  exit 1
fi

echo "[INFO] PRIORITIZED_VARIANTS=$PRIORITIZED_VARIANTS"
ls -lh "$PRIORITIZED_VARIANTS"
echo

echo "=== RUN STAGE 12 FROM CHECKPOINT ==="
python - <<'PY'
import json
from pathlib import Path
import yaml

from pipeline.stage_12_validate_variants import run_stage

class ProbeLogger:
    def info(self, msg): print(f"[LOGGER][INFO] {msg}")
    def warning(self, msg): print(f"[LOGGER][WARN] {msg}")
    def error(self, msg): print(f"[LOGGER][ERROR] {msg}")

repo_root = Path("/root/dev/portfolio_projects/variant_annotation_pipeline")
config_path = repo_root / "config" / "config.mark.local.yaml"

with config_path.open("r", encoding="utf-8") as fh:
    config = yaml.safe_load(fh)

results_root = repo_root / "results"
stage11_files = sorted(results_root.rglob("stage_11_prioritized_variants.tsv"))

if not stage11_files:
    raise SystemExit("No stage_11_prioritized_variants.tsv found")

stage11_path = stage11_files[-1]
run_dir = stage11_path.parent.parent
processed_dir = run_dir / "processed"

state = {
    "artifacts": {
        "stage_11_prioritized_variants": str(stage11_path),
    },
    "qc": {},
    "stage_outputs": {},
    "warnings": [],
}

paths = {"processed_dir": str(processed_dir)}
logger = ProbeLogger()

print("[PYTHON][INFO] PRIORITIZED_VARIANTS=", stage11_path)
print("[PYTHON][INFO] PROCESSED_DIR=", processed_dir)

updated_state = run_stage(config=config, paths=paths, logger=logger, state=state)

print()
print("=== STAGE 12 RESULT SUMMARY ===")
print(json.dumps({
    "stage_12_qc": updated_state["qc"].get("stage_12_qc"),
    "stage_output": updated_state["stage_outputs"].get("stage_12_validate_variants"),
    "artifacts": {
        key: value for key, value in updated_state["artifacts"].items()
        if key.startswith("stage_12")
    },
    "warnings": updated_state.get("warnings", []),
}, indent=2))
PY
echo

echo "=== STAGE 12 OUTPUT FILES ==="
find "$REPO_ROOT/results" -type f \( \
  -name "stage_12_validation_candidates.tsv" -o \
  -name "stage_12_summary.json" \
\) -exec ls -lh {} \; | sort
echo

echo "=== SUMMARY JSON HEAD ==="
SUMMARY_JSON="$(find "$REPO_ROOT/results" -type f -name "stage_12_summary.json" | sort | tail -n 1 || true)"
if [[ -n "${SUMMARY_JSON:-}" ]]; then
  echo "[INFO] SUMMARY_JSON=$SUMMARY_JSON"
  cat "$SUMMARY_JSON" || true
else
  echo "[WARN] No stage_12_summary.json found."
fi
echo

echo "=== FIRST STAGE 12 ROWS ==="
STAGE12_TSV="$(find "$REPO_ROOT/results" -type f -name "stage_12_validation_candidates.tsv" | sort | tail -n 1 || true)"
if [[ -n "${STAGE12_TSV:-}" ]]; then
  echo "[INFO] STAGE12_TSV=$STAGE12_TSV"
  head -n 5 "$STAGE12_TSV" | column -t -s $'\t' || true
else
  echo "[WARN] No stage_12_validation_candidates.tsv found."
fi
echo

echo "=== VALIDATION DISTRIBUTION QUICK CHECK ==="
if [[ -n "${STAGE12_TSV:-}" ]]; then
  awk -F'\t' '
  NR==1 {
    for (i=1; i<=NF; i++) {
      if ($i=="validation_required") req_col=i
      if ($i=="validation_priority") prio_col=i
      if ($i=="suggested_validation_method") method_col=i
      if ($i=="priority_tier") tier_col=i
    }
    next
  }
  {
    req[$req_col]++
    prio[$prio_col]++
    method[$method_col]++
    tier[$tier_col]++
  }
  END {
    print "validation_required"
    for (k in req) print k "\t" req[k]
    print ""
    print "validation_priority"
    for (k in prio) print k "\t" prio[k]
    print ""
    print "suggested_validation_method"
    for (k in method) print k "\t" method[k]
    print ""
    print "priority_tier"
    for (k in tier) print k "\t" tier[k]
  }
  ' "$STAGE12_TSV" || true
fi
echo

echo "=== VALIDATION-REQUIRED EXAMPLES ==="
if [[ -n "${STAGE12_TSV:-}" ]]; then
  awk -F'\t' 'NR==1 || $0 ~ /True/' "$STAGE12_TSV" | head -n 8 | column -t -s $'\t' || true
fi
echo

echo "[INFO] Mark Stage 12 checkpoint run completed at $(date)"
echo "[INFO] Log file saved to: $LOG"