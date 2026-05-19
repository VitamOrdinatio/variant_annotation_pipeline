#!/usr/bin/env bash
set -euo pipefail

TS="$(date +%Y%m%d_%H%M%S)"
LOG="/root/Desktop/mark_run_stage13_checkpoint_${TS}.log"
REPO_ROOT="$HOME/dev/portfolio_projects/variant_annotation_pipeline"

exec > >(tee "$LOG") 2>&1

echo "[INFO] Mark Stage 13 checkpoint run started at $(date)"
echo "[INFO] Log file: $LOG"
echo "[INFO] Repo root: $REPO_ROOT"
echo

cd "$REPO_ROOT"
source .venv/bin/activate

echo "=== PYTHON ENV CHECK ==="
which python
python --version
echo

echo "=== REPO STATUS ==="
git status --short || true
echo

echo "=== FIND REQUIRED STAGE 13 INPUTS ==="
STAGE11_TSV="$(find "$REPO_ROOT/results" -type f -name "stage_11_prioritized_variants.tsv" | sort | tail -n 1 || true)"
STAGE11_JSON="$(find "$REPO_ROOT/results" -type f -name "stage_11_summary.json" | sort | tail -n 1 || true)"
STAGE11_GENE_COUNTS="$(find "$REPO_ROOT/results" -type f -name "stage_11_gene_variant_counts.tsv" | sort | tail -n 1 || true)"
STAGE12_TSV="$(find "$REPO_ROOT/results" -type f -name "stage_12_validation_candidates.tsv" | sort | tail -n 1 || true)"
STAGE12_JSON="$(find "$REPO_ROOT/results" -type f -name "stage_12_summary.json" | sort | tail -n 1 || true)"

for f in "$STAGE11_TSV" "$STAGE11_JSON" "$STAGE11_GENE_COUNTS" "$STAGE12_TSV" "$STAGE12_JSON"; do
  if [[ -z "${f:-}" ]]; then
    echo "[ERROR] Missing one or more required Stage 13 inputs."
    exit 1
  fi
done

echo "[INFO] STAGE11_TSV=$STAGE11_TSV"
echo "[INFO] STAGE11_JSON=$STAGE11_JSON"
echo "[INFO] STAGE11_GENE_COUNTS=$STAGE11_GENE_COUNTS"
echo "[INFO] STAGE12_TSV=$STAGE12_TSV"
echo "[INFO] STAGE12_JSON=$STAGE12_JSON"
ls -lh "$STAGE11_TSV" "$STAGE11_JSON" "$STAGE11_GENE_COUNTS" "$STAGE12_TSV" "$STAGE12_JSON"
echo

echo "=== VERIFY STAGE 13 IMPORTS ==="
python -m py_compile pipeline/stage_13_write_summary.py
grep -n "pandas\|pd\.|yaml" pipeline/stage_13_write_summary.py || true
echo

echo "=== RUN STAGE 13 FROM CHECKPOINT ==="
python - <<'PY'
import json
from pathlib import Path

from pipeline.stage_13_write_summary import run_stage

class ProbeLogger:
    def info(self, msg): print(f"[LOGGER][INFO] {msg}")
    def warning(self, msg): print(f"[LOGGER][WARN] {msg}")
    def error(self, msg): print(f"[LOGGER][ERROR] {msg}")

repo_root = Path("/root/dev/portfolio_projects/variant_annotation_pipeline")
results_root = repo_root / "results"

stage11_tsv = sorted(results_root.rglob("stage_11_prioritized_variants.tsv"))[-1]
stage11_json = sorted(results_root.rglob("stage_11_summary.json"))[-1]
stage11_gene_counts = sorted(results_root.rglob("stage_11_gene_variant_counts.tsv"))[-1]
stage12_tsv = sorted(results_root.rglob("stage_12_validation_candidates.tsv"))[-1]
stage12_json = sorted(results_root.rglob("stage_12_summary.json"))[-1]

run_dir = stage11_tsv.parent.parent
processed_dir = run_dir / "processed"

state = {
    "artifacts": {
        "stage_11_prioritized_variants": str(stage11_tsv),
        "stage_11_summary_json": str(stage11_json),
        "stage_11_gene_variant_counts": str(stage11_gene_counts),
        "stage_12_validation_candidates": str(stage12_tsv),
        "stage_12_summary_json": str(stage12_json),
    },
    "qc": {},
    "stage_outputs": {},
    "warnings": [],
}

paths = {"processed_dir": str(processed_dir)}
logger = ProbeLogger()

print("[PYTHON][INFO] PROCESSED_DIR=", processed_dir)

updated_state = run_stage(config={}, paths=paths, logger=logger, state=state)

print()
print("=== STAGE 13 RESULT SUMMARY ===")
print(json.dumps({
    "stage_13_qc": updated_state["qc"].get("stage_13_qc"),
    "stage_output": updated_state["stage_outputs"].get("stage_13_write_summary"),
    "artifacts": {
        key: value for key, value in updated_state["artifacts"].items()
        if key.startswith("stage_13")
    },
    "warnings": updated_state.get("warnings", []),
}, indent=2))
PY
echo

echo "=== STAGE 13 OUTPUT FILES ==="
find "$REPO_ROOT/results" -type f \( \
  -name "stage_13_final_summary.json" -o \
  -name "stage_13_artifact_manifest.json" -o \
  -name "stage_13_run_report.md" \
\) -exec ls -lh {} \; | sort
echo

echo "=== FINAL SUMMARY JSON ==="
FINAL_SUMMARY="$(find "$REPO_ROOT/results" -type f -name "stage_13_final_summary.json" | sort | tail -n 1 || true)"
if [[ -n "${FINAL_SUMMARY:-}" ]]; then
  echo "[INFO] FINAL_SUMMARY=$FINAL_SUMMARY"
  cat "$FINAL_SUMMARY" || true
else
  echo "[WARN] No stage_13_final_summary.json found."
fi
echo

echo "=== RUN REPORT HEAD ==="
RUN_REPORT="$(find "$REPO_ROOT/results" -type f -name "stage_13_run_report.md" | sort | tail -n 1 || true)"
if [[ -n "${RUN_REPORT:-}" ]]; then
  echo "[INFO] RUN_REPORT=$RUN_REPORT"
  head -n 120 "$RUN_REPORT" || true
else
  echo "[WARN] No stage_13_run_report.md found."
fi
echo

echo "=== ARTIFACT MANIFEST QUICK CHECK ==="
MANIFEST="$(find "$REPO_ROOT/results" -type f -name "stage_13_artifact_manifest.json" | sort | tail -n 1 || true)"
if [[ -n "${MANIFEST:-}" ]]; then
  echo "[INFO] MANIFEST=$MANIFEST"
  python - <<PY
import json
from pathlib import Path
p = Path("$MANIFEST")
data = json.loads(p.read_text())
print("artifact_count:", data.get("artifact_count"))
required = [a for a in data.get("artifacts", []) if a.get("required")]
print("required_count:", len(required))
print("missing_required:", [a["artifact_name"] for a in required if not a.get("exists")])
PY
else
  echo "[WARN] No stage_13_artifact_manifest.json found."
fi
echo

echo "[INFO] Mark Stage 13 checkpoint run completed at $(date)"
echo "[INFO] Log file saved to: $LOG"