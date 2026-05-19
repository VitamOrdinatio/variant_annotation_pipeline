#!/usr/bin/env bash
set -euo pipefail

TS="$(date +%Y%m%d_%H%M%S)"
LOG="/root/Desktop/mark_run_stage09_checkpoint_${TS}.log"
REPO_ROOT="$HOME/dev/portfolio_projects/variant_annotation_pipeline"
CONFIG_PATH="$REPO_ROOT/config/config.mark.local.yaml"

exec > >(tee "$LOG") 2>&1

echo "[INFO] Mark Stage 09 checkpoint run started at $(date)"
echo "[INFO] Log file: $LOG"
echo "[INFO] Repo root: $REPO_ROOT"
echo "[INFO] Config path: $CONFIG_PATH"
echo

cd "$REPO_ROOT"
source .venv/bin/activate

echo "=== REPO STATUS ==="
git status --short || true
echo

echo "=== FIND LATEST STAGE 08 OUTPUTS ==="
CODING_TSV="$(find "$REPO_ROOT/results" -type f -name "coding_candidates.tsv" | sort | tail -n 1 || true)"
SPLICE_TSV="$(find "$REPO_ROOT/results" -type f -name "splice_region_candidates.tsv" | sort | tail -n 1 || true)"
VARIANT_SUMMARY_TSV="$(find "$REPO_ROOT/results" -type f -name "stage_08_variant_summary.tsv" | sort | tail -n 1 || true)"
SELECTED_TSV="$(find "$REPO_ROOT/results" -type f -name "stage_08_selected_transcript_consequences.tsv" | sort | tail -n 1 || true)"

for f in "$CODING_TSV" "$SPLICE_TSV" "$VARIANT_SUMMARY_TSV" "$SELECTED_TSV"; do
  if [[ -z "${f:-}" ]]; then
    echo "[ERROR] Missing one or more Stage 08 outputs."
    exit 1
  fi
done

echo "[INFO] CODING_TSV=$CODING_TSV"
echo "[INFO] SPLICE_TSV=$SPLICE_TSV"
echo "[INFO] VARIANT_SUMMARY_TSV=$VARIANT_SUMMARY_TSV"
echo "[INFO] SELECTED_TSV=$SELECTED_TSV"
ls -lh "$CODING_TSV" "$SPLICE_TSV" "$VARIANT_SUMMARY_TSV" "$SELECTED_TSV"
echo

echo "=== RUN STAGE 09 FROM CHECKPOINT ==="
python - <<'PY'
import json
from pathlib import Path
import yaml

from pipeline.stage_09_interpret_coding import run_stage

class ProbeLogger:
    def info(self, msg): print(f"[LOGGER][INFO] {msg}")
    def warning(self, msg): print(f"[LOGGER][WARN] {msg}")
    def error(self, msg): print(f"[LOGGER][ERROR] {msg}")

repo_root = Path("/root/dev/portfolio_projects/variant_annotation_pipeline")
config_path = repo_root / "config" / "config.mark.local.yaml"

with config_path.open("r", encoding="utf-8") as fh:
    config = yaml.safe_load(fh)

results_root = repo_root / "results"
coding_tsvs = sorted(results_root.rglob("coding_candidates.tsv"))
splice_tsvs = sorted(results_root.rglob("splice_region_candidates.tsv"))
variant_summary_tsvs = sorted(results_root.rglob("stage_08_variant_summary.tsv"))
selected_tsvs = sorted(results_root.rglob("stage_08_selected_transcript_consequences.tsv"))

if not coding_tsvs:
    raise SystemExit("No coding_candidates.tsv found")
if not splice_tsvs:
    raise SystemExit("No splice_region_candidates.tsv found")
if not variant_summary_tsvs:
    raise SystemExit("No stage_08_variant_summary.tsv found")
if not selected_tsvs:
    raise SystemExit("No stage_08_selected_transcript_consequences.tsv found")

coding_tsv = coding_tsvs[-1]
splice_tsv = splice_tsvs[-1]
variant_summary_tsv = variant_summary_tsvs[-1]
selected_tsv = selected_tsvs[-1]

run_dir = coding_tsv.parent.parent
processed_dir = run_dir / "processed"

state = {
    "artifacts": {
        "coding_candidates": str(coding_tsv),
        "splice_region_candidates": str(splice_tsv),
        "stage_08_variant_summary": str(variant_summary_tsv),
        "stage_08_selected_transcript_consequences": str(selected_tsv),
    },
    "qc": {},
    "stage_outputs": {},
    "warnings": [],
}

paths = {"processed_dir": str(processed_dir)}
logger = ProbeLogger()

print("[PYTHON][INFO] CODING_TSV=", coding_tsv)
print("[PYTHON][INFO] SPLICE_TSV=", splice_tsv)
print("[PYTHON][INFO] VARIANT_SUMMARY_TSV=", variant_summary_tsv)
print("[PYTHON][INFO] SELECTED_TSV=", selected_tsv)
print("[PYTHON][INFO] PROCESSED_DIR=", processed_dir)

updated_state = run_stage(config=config, paths=paths, logger=logger, state=state)

print()
print("=== STAGE 09 RESULT SUMMARY ===")
print(json.dumps({
    "stage_09_qc": updated_state["qc"].get("stage_09_qc"),
    "stage_output": updated_state["stage_outputs"].get("stage_09_interpret_coding"),
    "artifacts": {
        key: value for key, value in updated_state["artifacts"].items()
        if key.startswith("stage_09")
    },
    "warnings": updated_state.get("warnings", []),
}, indent=2))
PY
echo

echo "=== STAGE 09 OUTPUT FILES ==="
find "$REPO_ROOT/results" -type f \( \
  -name "stage_09_coding_interpreted.tsv" -o \
  -name "stage_09_summary.json" \
\) -exec ls -lh {} \; | sort
echo

echo "=== SUMMARY JSON HEAD ==="
SUMMARY_JSON="$(find "$REPO_ROOT/results" -type f -name "stage_09_summary.json" | sort | tail -n 1 || true)"
if [[ -n "${SUMMARY_JSON:-}" ]]; then
  echo "[INFO] SUMMARY_JSON=$SUMMARY_JSON"
  head -n 120 "$SUMMARY_JSON" || true
else
  echo "[WARN] No stage_09_summary.json found."
fi
echo

echo "=== FIRST STAGE 09 ROWS ==="
STAGE09_TSV="$(find "$REPO_ROOT/results" -type f -name "stage_09_coding_interpreted.tsv" | sort | tail -n 1 || true)"
if [[ -n "${STAGE09_TSV:-}" ]]; then
  echo "[INFO] STAGE09_TSV=$STAGE09_TSV"
  head -n 5 "$STAGE09_TSV" | column -t -s $'\t' || true
else
  echo "[WARN] No stage_09_coding_interpreted.tsv found."
fi
echo

echo "=== LABEL DISTRIBUTION QUICK CHECK ==="
if [[ -n "${STAGE09_TSV:-}" ]]; then
  awk -F'\t' '
  NR==1 {
    for (i=1; i<=NF; i++) {
      if ($i=="coding_interpretation_label") label_col=i
      if ($i=="functional_impact") impact_col=i
      if ($i=="rarity_flag") rarity_col=i
      if ($i=="clinical_evidence") clinical_col=i
    }
    next
  }
  {
    label[$label_col]++
    impact[$impact_col]++
    rarity[$rarity_col]++
    clinical[$clinical_col]++
  }
  END {
    print "coding_interpretation_label"
    for (k in label) print k "\t" label[k]
    print ""
    print "functional_impact"
    for (k in impact) print k "\t" impact[k]
    print ""
    print "rarity_flag"
    for (k in rarity) print k "\t" rarity[k]
    print ""
    print "clinical_evidence"
    for (k in clinical) print k "\t" clinical[k]
  }
  ' "$STAGE09_TSV" || true
fi
echo

echo "=== HIGH-VALUE EXAMPLES ==="
if [[ -n "${STAGE09_TSV:-}" ]]; then
  echo "--- loss_of_function examples ---"
  awk -F'\t' 'NR==1 || $0 ~ /loss_of_function/' "$STAGE09_TSV" | head -n 6 | column -t -s $'\t' || true
  echo
  echo "--- lof_or_missense_rare examples ---"
  awk -F'\t' 'NR==1 || $0 ~ /lof_or_missense_rare/' "$STAGE09_TSV" | head -n 6 | column -t -s $'\t' || true
  echo
  echo "--- clinically supported examples ---"
  awk -F'\t' 'NR==1 || $0 ~ /pathogenic|likely_pathogenic/' "$STAGE09_TSV" | head -n 6 | column -t -s $'\t' || true
fi
echo

echo "[INFO] Mark Stage 09 checkpoint run completed at $(date)"
echo "[INFO] Log file saved to: $LOG"