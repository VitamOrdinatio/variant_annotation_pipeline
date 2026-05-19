#!/usr/bin/env bash
set -euo pipefail

TS="$(date +%Y%m%d_%H%M%S)"
LOG="/root/Desktop/mark_run_stage11_checkpoint_${TS}.log"
REPO_ROOT="$HOME/dev/portfolio_projects/variant_annotation_pipeline"
CONFIG_PATH="$REPO_ROOT/config/config.mark.local.yaml"

exec > >(tee "$LOG") 2>&1

echo "[INFO] Mark Stage 11 checkpoint run started at $(date)"
echo "[INFO] Log file: $LOG"
echo "[INFO] Repo root: $REPO_ROOT"
echo "[INFO] Config path: $CONFIG_PATH"
echo

cd "$REPO_ROOT"
source .venv/bin/activate

echo "=== REPO STATUS ==="
git status --short || true
echo

echo "=== FIND LATEST STAGE 09/10 OUTPUTS ==="
CODING_INTERPRETED="$(find "$REPO_ROOT/results" -type f -name "stage_09_coding_interpreted.tsv" | sort | tail -n 1 || true)"
NONCODING_INTERPRETED="$(find "$REPO_ROOT/results" -type f -name "stage_10_noncoding_interpreted.tsv" | sort | tail -n 1 || true)"

if [[ -z "${CODING_INTERPRETED:-}" ]]; then
  echo "[ERROR] No stage_09_coding_interpreted.tsv found."
  exit 1
fi

if [[ -z "${NONCODING_INTERPRETED:-}" ]]; then
  echo "[ERROR] No stage_10_noncoding_interpreted.tsv found."
  exit 1
fi

echo "[INFO] CODING_INTERPRETED=$CODING_INTERPRETED"
echo "[INFO] NONCODING_INTERPRETED=$NONCODING_INTERPRETED"
ls -lh "$CODING_INTERPRETED" "$NONCODING_INTERPRETED"
echo

echo "=== RUN STAGE 11 FROM CHECKPOINT ==="
python - <<'PY'
import json
from pathlib import Path
import yaml

from pipeline.stage_11_prioritize_variants import run_stage

class ProbeLogger:
    def info(self, msg): print(f"[LOGGER][INFO] {msg}")
    def warning(self, msg): print(f"[LOGGER][WARN] {msg}")
    def error(self, msg): print(f"[LOGGER][ERROR] {msg}")

repo_root = Path("/root/dev/portfolio_projects/variant_annotation_pipeline")
config_path = repo_root / "config" / "config.mark.local.yaml"

with config_path.open("r", encoding="utf-8") as fh:
    config = yaml.safe_load(fh)

results_root = repo_root / "results"
coding_files = sorted(results_root.rglob("stage_09_coding_interpreted.tsv"))
noncoding_files = sorted(results_root.rglob("stage_10_noncoding_interpreted.tsv"))

if not coding_files:
    raise SystemExit("No stage_09_coding_interpreted.tsv found")
if not noncoding_files:
    raise SystemExit("No stage_10_noncoding_interpreted.tsv found")

coding_path = coding_files[-1]
noncoding_path = noncoding_files[-1]
run_dir = coding_path.parent.parent
processed_dir = run_dir / "processed"

state = {
    "artifacts": {
        "stage_09_coding_interpreted": str(coding_path),
        "stage_10_noncoding_interpreted": str(noncoding_path),
    },
    "qc": {},
    "stage_outputs": {},
    "warnings": [],
}

paths = {"processed_dir": str(processed_dir)}
logger = ProbeLogger()

print("[PYTHON][INFO] CODING_INTERPRETED=", coding_path)
print("[PYTHON][INFO] NONCODING_INTERPRETED=", noncoding_path)
print("[PYTHON][INFO] PROCESSED_DIR=", processed_dir)

updated_state = run_stage(config=config, paths=paths, logger=logger, state=state)

print()
print("=== STAGE 11 RESULT SUMMARY ===")
print(json.dumps({
    "stage_11_qc": updated_state["qc"].get("stage_11_qc"),
    "stage_output": updated_state["stage_outputs"].get("stage_11_prioritize_variants"),
    "artifacts": {
        key: value for key, value in updated_state["artifacts"].items()
        if key.startswith("stage_11")
    },
    "warnings": updated_state.get("warnings", []),
}, indent=2))
PY
echo

echo "=== STAGE 11 OUTPUT FILES ==="
find "$REPO_ROOT/results" -type f \( \
  -name "stage_11_prioritized_variants.tsv" -o \
  -name "stage_11_summary.json" \
\) -exec ls -lh {} \; | sort
echo

echo "=== SUMMARY JSON HEAD ==="
SUMMARY_JSON="$(find "$REPO_ROOT/results" -type f -name "stage_11_summary.json" | sort | tail -n 1 || true)"
if [[ -n "${SUMMARY_JSON:-}" ]]; then
  echo "[INFO] SUMMARY_JSON=$SUMMARY_JSON"
  head -n 160 "$SUMMARY_JSON" || true
else
  echo "[WARN] No stage_11_summary.json found."
fi
echo

echo "=== FIRST STAGE 11 ROWS ==="
STAGE11_TSV="$(find "$REPO_ROOT/results" -type f -name "stage_11_prioritized_variants.tsv" | sort | tail -n 1 || true)"
if [[ -n "${STAGE11_TSV:-}" ]]; then
  echo "[INFO] STAGE11_TSV=$STAGE11_TSV"
  head -n 5 "$STAGE11_TSV" | column -t -s $'\t' || true
else
  echo "[WARN] No stage_11_prioritized_variants.tsv found."
fi
echo

echo "=== PRIORITY DISTRIBUTION QUICK CHECK ==="
if [[ -n "${STAGE11_TSV:-}" ]]; then
  awk -F'\t' '
  NR==1 {
    for (i=1; i<=NF; i++) {
      if ($i=="priority_tier") tier_col=i
      if ($i=="priority_rank") rank_col=i
      if ($i=="variant_origin") origin_col=i
      if ($i=="source_interpretation_label") label_col=i
    }
    next
  }
  {
    tier[$tier_col]++
    rank[$rank_col]++
    origin[$origin_col]++
    label[$label_col]++
  }
  END {
    print "priority_tier"
    for (k in tier) print k "\t" tier[k]
    print ""
    print "priority_rank"
    for (k in rank) print k "\t" rank[k]
    print ""
    print "variant_origin"
    for (k in origin) print k "\t" origin[k]
    print ""
    print "source_interpretation_label"
    for (k in label) print k "\t" label[k]
  }
  ' "$STAGE11_TSV" || true
fi
echo

echo "=== HIGH-VALUE EXAMPLES ==="
if [[ -n "${STAGE11_TSV:-}" ]]; then
  echo "--- Tier 1 examples ---"
  awk -F'\t' 'NR==1 || $0 ~ /tier_1_high_confidence_candidate/' "$STAGE11_TSV" | head -n 6 | column -t -s $'\t' || true
  echo
  echo "--- Tier 2 examples ---"
  awk -F'\t' 'NR==1 || $0 ~ /tier_2_moderate_candidate/' "$STAGE11_TSV" | head -n 6 | column -t -s $'\t' || true
  echo
  echo "--- Tier 4 examples ---"
  awk -F'\t' 'NR==1 || $0 ~ /tier_4_uninterpretable_or_qc_limited/' "$STAGE11_TSV" | head -n 6 | column -t -s $'\t' || true
fi
echo

echo "[INFO] Mark Stage 11 checkpoint run completed at $(date)"
echo "[INFO] Log file saved to: $LOG"