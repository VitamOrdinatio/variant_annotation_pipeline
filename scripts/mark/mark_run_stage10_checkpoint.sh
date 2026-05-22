#!/usr/bin/env bash
set -euo pipefail

TS="$(date +%Y%m%d_%H%M%S)"
LOG="/root/Desktop/mark_run_stage10_checkpoint_${TS}.log"
REPO_ROOT="$HOME/dev/portfolio_projects/variant_annotation_pipeline"
CONFIG_PATH="$REPO_ROOT/config/config.mark.local.yaml"

exec > >(tee "$LOG") 2>&1

echo "[INFO] Mark Stage 10 checkpoint run started at $(date)"
echo "[INFO] Log file: $LOG"
echo "[INFO] Repo root: $REPO_ROOT"
echo "[INFO] Config path: $CONFIG_PATH"
echo

cd "$REPO_ROOT"
source .venv/bin/activate

echo "=== REPO STATUS ==="
git status --short || true
echo

echo "=== FIND LATEST STAGE 08 NONCODING OUTPUTS ==="
NONCODING_TSV="$(find "$REPO_ROOT/results" -type f -name "noncoding_candidates.tsv" | sort | tail -n 1 || true)"
VARIANT_SUMMARY_TSV="$(find "$REPO_ROOT/results" -type f -name "stage_08_variant_summary.tsv" | sort | tail -n 1 || true)"
SELECTED_TSV="$(find "$REPO_ROOT/results" -type f -name "stage_08_selected_transcript_consequences.tsv" | sort | tail -n 1 || true)"

if [[ -z "${NONCODING_TSV:-}" ]]; then
  echo "[ERROR] No noncoding_candidates.tsv found."
  exit 1
fi

if [[ -z "${VARIANT_SUMMARY_TSV:-}" ]]; then
  echo "[ERROR] No stage_08_variant_summary.tsv found."
  exit 1
fi

if [[ -z "${SELECTED_TSV:-}" ]]; then
  echo "[ERROR] No stage_08_selected_transcript_consequences.tsv found."
  exit 1
fi

echo "[INFO] NONCODING_TSV=$NONCODING_TSV"
echo "[INFO] VARIANT_SUMMARY_TSV=$VARIANT_SUMMARY_TSV"
echo "[INFO] SELECTED_TSV=$SELECTED_TSV"
ls -lh "$NONCODING_TSV" "$VARIANT_SUMMARY_TSV" "$SELECTED_TSV"
echo

echo "=== RUN STAGE 10 FROM CHECKPOINT ==="
python - <<'PY'
import json
from pathlib import Path
import yaml

from pipeline.stage_10_interpret_noncoding import run_stage

class ProbeLogger:
    def info(self, msg): print(f"[LOGGER][INFO] {msg}")
    def warning(self, msg): print(f"[LOGGER][WARN] {msg}")
    def error(self, msg): print(f"[LOGGER][ERROR] {msg}")

repo_root = Path("/root/dev/portfolio_projects/variant_annotation_pipeline")
config_path = repo_root / "config" / "config.mark.local.yaml"

with config_path.open("r", encoding="utf-8") as fh:
    config = yaml.safe_load(fh)

results_root = repo_root / "results"
noncoding_tsvs = sorted(results_root.rglob("noncoding_candidates.tsv"))
variant_summary_tsvs = sorted(results_root.rglob("stage_08_variant_summary.tsv"))
selected_tsvs = sorted(results_root.rglob("stage_08_selected_transcript_consequences.tsv"))

if not noncoding_tsvs:
    raise SystemExit("No noncoding_candidates.tsv found")
if not variant_summary_tsvs:
    raise SystemExit("No stage_08_variant_summary.tsv found")
if not selected_tsvs:
    raise SystemExit("No stage_08_selected_transcript_consequences.tsv found")

noncoding_tsv = noncoding_tsvs[-1]
variant_summary_tsv = variant_summary_tsvs[-1]
selected_tsv = selected_tsvs[-1]

run_dir = noncoding_tsv.parent.parent
processed_dir = run_dir / "processed"

state = {
    "artifacts": {
        "noncoding_candidates": str(noncoding_tsv),
        "stage_08_variant_summary": str(variant_summary_tsv),
        "stage_08_selected_transcript_consequences": str(selected_tsv),
    },
    "qc": {},
    "stage_outputs": {},
    "warnings": [],
}

paths = {"processed_dir": str(processed_dir)}
logger = ProbeLogger()

print("[PYTHON][INFO] NONCODING_TSV=", noncoding_tsv)
print("[PYTHON][INFO] VARIANT_SUMMARY_TSV=", variant_summary_tsv)
print("[PYTHON][INFO] SELECTED_TSV=", selected_tsv)
print("[PYTHON][INFO] PROCESSED_DIR=", processed_dir)

updated_state = run_stage(config=config, paths=paths, logger=logger, state=state)

print()
print("=== STAGE 10 RESULT SUMMARY ===")
print(json.dumps({
    "stage_10_qc": updated_state["qc"].get("stage_10_qc"),
    "stage_output": updated_state["stage_outputs"].get("stage_10_interpret_noncoding"),
    "artifacts": {
        key: value for key, value in updated_state["artifacts"].items()
        if key.startswith("stage_10")
    },
    "warnings": updated_state.get("warnings", []),
}, indent=2))
PY
echo

echo "=== STAGE 10 OUTPUT FILES ==="
find "$REPO_ROOT/results" -type f \( \
  -name "stage_10_noncoding_interpreted.tsv" -o \
  -name "stage_10_summary.json" \
\) -exec ls -lh {} \; | sort
echo

echo "=== SUMMARY JSON HEAD ==="
SUMMARY_JSON="$(find "$REPO_ROOT/results" -type f -name "stage_10_summary.json" | sort | tail -n 1 || true)"
if [[ -n "${SUMMARY_JSON:-}" ]]; then
  echo "[INFO] SUMMARY_JSON=$SUMMARY_JSON"
  head -n 140 "$SUMMARY_JSON" || true
else
  echo "[WARN] No stage_10_summary.json found."
fi
echo

echo "=== FIRST STAGE 10 ROWS ==="
STAGE10_TSV="$(find "$REPO_ROOT/results" -type f -name "stage_10_noncoding_interpreted.tsv" | sort | tail -n 1 || true)"
if [[ -n "${STAGE10_TSV:-}" ]]; then
  echo "[INFO] STAGE10_TSV=$STAGE10_TSV"
  head -n 5 "$STAGE10_TSV" | column -t -s $'\t' || true
else
  echo "[WARN] No stage_10_noncoding_interpreted.tsv found."
fi
echo

echo "=== LABEL DISTRIBUTION QUICK CHECK ==="
if [[ -n "${STAGE10_TSV:-}" ]]; then
  awk -F'\t' '
  NR==1 {
    for (i=1; i<=NF; i++) {
      if ($i=="noncoding_interpretation_label") label_col=i
      if ($i=="noncoding_functional_context") context_col=i
      if ($i=="rarity_flag") rarity_col=i
      if ($i=="clinical_evidence") clinical_col=i
      if ($i=="qc_reliability") qc_col=i
    }
    next
  }
  {
    label[$label_col]++
    context[$context_col]++
    rarity[$rarity_col]++
    clinical[$clinical_col]++
    qc[$qc_col]++
  }
  END {
    print "noncoding_interpretation_label"
    for (k in label) print k "\t" label[k]
    print ""
    print "noncoding_functional_context"
    for (k in context) print k "\t" context[k]
    print ""
    print "rarity_flag"
    for (k in rarity) print k "\t" rarity[k]
    print ""
    print "clinical_evidence"
    for (k in clinical) print k "\t" clinical[k]
    print ""
    print "qc_reliability"
    for (k in qc) print k "\t" qc[k]
  }
  ' "$STAGE10_TSV" || true
fi
echo

echo "=== HIGH-VALUE EXAMPLES ==="
if [[ -n "${STAGE10_TSV:-}" ]]; then
  echo "--- regulatory examples ---"
  awk -F'\t' 'NR==1 || $0 ~ /regulatory/' "$STAGE10_TSV" | head -n 6 | column -t -s $'\t' || true
  echo
  echo "--- proximal examples ---"
  awk -F'\t' 'NR==1 || $0 ~ /proximal/' "$STAGE10_TSV" | head -n 6 | column -t -s $'\t' || true
  echo
  echo "--- transcript-associated examples ---"
  awk -F'\t' 'NR==1 || $0 ~ /transcript_associated/' "$STAGE10_TSV" | head -n 6 | column -t -s $'\t' || true
  echo
  echo "--- rare noncoding candidate examples ---"
  awk -F'\t' 'NR==1 || $0 ~ /regulatory_or_transcript_rare|regulatory_rare_supported/' "$STAGE10_TSV" | head -n 6 | column -t -s $'\t' || true
  echo
  echo "--- uninterpretable examples ---"
  awk -F'\t' 'NR==1 || $0 ~ /noncoding_uninterpretable/' "$STAGE10_TSV" | head -n 6 | column -t -s $'\t' || true
fi
echo

echo "[INFO] Mark Stage 10 checkpoint run completed at $(date)"
echo "[INFO] Log file saved to: $LOG"