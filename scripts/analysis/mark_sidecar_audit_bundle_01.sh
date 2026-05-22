#!/usr/bin/env bash
set -euo pipefail

SCRIPT_NAME="mark_sidecar_audit_bundle_01"
TIMESTAMP="$(date +%Y%m%d_%H%M%S)"
OUTFILE="/root/Desktop/${SCRIPT_NAME}_${TIMESTAMP}.txt"

exec > >(tee -a "$OUTFILE") 2>&1

echo "========================================"
echo "${SCRIPT_NAME}"
echo "Canonical sidecar audit bundle"
echo "Started: $(date --iso-8601=seconds)"
echo "Host: $(hostname)"
echo "========================================"
echo

cd ~/dev/portfolio_projects/variant_annotation_pipeline

RUN_DIR=$(ls -1dt results/run_* | head -1)

echo "[run_dir]"
echo "$RUN_DIR"
echo

echo "[run completion]"
tail -40 "$RUN_DIR/logs/pipeline.log"
echo

echo "[metrics files]"
find "$RUN_DIR/metrics" -maxdepth 1 -type f -print | sort
echo

echo "[metadata check]"
head -2 "$RUN_DIR/metrics/stage_metrics_long.tsv"
echo
cut -f6,8,9,10,11 "$RUN_DIR/metrics/stage_metrics_long.tsv" | head -20
echo

echo "[metric names]"
cut -f1 "$RUN_DIR/metrics/stage_metrics_long.tsv" | sort | uniq
echo

echo "[F3A flow]"
column -t -s $'\t' "$RUN_DIR/metrics/figure_f3a_flow.tsv"
echo

echo "[metrics TSV row counts]"
wc -l "$RUN_DIR"/metrics/*.tsv
echo

echo "[processed TSV row counts]"
wc -l "$RUN_DIR"/processed/stage_08_selected_transcript_consequences.tsv
wc -l "$RUN_DIR"/processed/stage_11_prioritized_variants.tsv
wc -l "$RUN_DIR"/processed/stage_12_validation_candidates.tsv
echo

echo "[stage summaries]"
echo "--- stage_08_summary.json ---"
cat "$RUN_DIR/processed/stage_08_summary.json"
echo
echo "--- stage_11_summary.json ---"
cat "$RUN_DIR/processed/stage_11_summary.json"
echo
echo "--- stage_12_summary.json ---"
cat "$RUN_DIR/processed/stage_12_summary.json"
echo

echo
echo "========================================"
echo "Audit complete"
echo "Output written to:"
echo "$OUTFILE"
echo "Finished: $(date --iso-8601=seconds)"
echo "========================================"