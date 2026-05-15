#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="/root/dev/portfolio_projects/variant_annotation_pipeline"
RUN_A="results/run_2026_05_14_083044"
RUN_B="results/run_2026_05_14_231247"
LABEL_A="ERR10619281_pre_patch"
LABEL_B="ERR10619281_post_patch"
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
OUT_MD="/root/Desktop/vap_compare_ERR10619281_${STAMP}.md"
OUT_JSON="/root/Desktop/vap_compare_ERR10619281_${STAMP}.json"
OUT_LOG="/root/Desktop/vap_compare_ERR10619281_${STAMP}.txt"

{
echo "===== MARK VAP Run Comparison Harness ====="
echo "UTC timestamp: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo "Host: $(hostname)"
echo
echo "===== Repository Context ====="
cd "$REPO_DIR"
echo "PWD: $(pwd)"
echo "Git branch: $(git branch --show-current)"
echo "Git commit: $(git rev-parse HEAD)"
echo
echo "===== Python Environment ====="
if [[ -f ".venv/bin/activate" ]]; then
  source .venv/bin/activate
  echo "Activated venv: ${VIRTUAL_ENV:-UNKNOWN}"
else
  echo "ERROR: .venv/bin/activate not found"
  exit 1
fi
echo "python: $(command -v python)"
python --version
echo
echo "===== Run Directory Checks ====="
for d in "$RUN_A" "$RUN_B"; do
  if [[ -d "$d" ]]; then
    echo "PRESENT: $d"
  else
    echo "MISSING: $d"
    exit 1
  fi
done
echo
echo "===== Running Comparator ====="
python scripts/analysis/compare_vap_runs.py \
  --run-a "$RUN_A" \
  --run-b "$RUN_B" \
  --label-a "$LABEL_A" \
  --label-b "$LABEL_B" \
  --out "$OUT_MD" \
  --json-out "$OUT_JSON"
echo
echo "===== Output Files ====="
ls -lh "$OUT_MD" "$OUT_JSON"
echo
echo "Markdown report: $OUT_MD"
echo "JSON summary: $OUT_JSON"
echo "Harness log: $OUT_LOG"
} > "$OUT_LOG" 2>&1

cat "$OUT_LOG"
