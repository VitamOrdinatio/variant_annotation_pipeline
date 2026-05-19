#!/usr/bin/env bash
set -euo pipefail

# ============================================================
# MARK Probe: Locate ERR10619300 Pipeline Runs
#
# Purpose:
#   Count and summarize all VAP run directories associated
#   with ERR10619300 using ONLY:
#
#     results/<run_id>/logs/pipeline.log
#
# Output:
#   /root/Desktop/err10619300_pipeline_runs.txt
# ============================================================

REPO_DIR="/root/dev/portfolio_projects/variant_annotation_pipeline"
OUTFILE="/root/Desktop/err10619300_pipeline_runs.txt"

echo "==================================================" > "$OUTFILE"
echo "ERR10619300 Pipeline Log Probe" >> "$OUTFILE"
echo "==================================================" >> "$OUTFILE"
echo >> "$OUTFILE"

cd "$REPO_DIR"

COUNT=0

for LOG in results/run_*/logs/pipeline.log; do
    if grep -q "ERR10619300" "$LOG"; then
        COUNT=$((COUNT + 1))
        RUN_DIR=$(dirname "$(dirname "$LOG")")
        RUN_ID=$(basename "$RUN_DIR")

        echo "RUN DIRECTORY: $RUN_DIR" >> "$OUTFILE"
        echo "RUN ID: $RUN_ID" >> "$OUTFILE"
        echo >> "$OUTFILE"

        echo "KEY SAMPLE LINES:" >> "$OUTFILE"
        grep -E "Sample ID:|SRA accession:|FASTQ R1|FASTQ R2" "$LOG" >> "$OUTFILE" || true
        echo >> "$OUTFILE"

        echo "START / STOP LINES:" >> "$OUTFILE"
        grep -E "Pipeline run started|Pipeline run finished|Run status|Pipeline execution complete" "$LOG" >> "$OUTFILE" || true
        echo >> "$OUTFILE"

        echo "FIRST TIMESTAMP:" >> "$OUTFILE"
        head -n 1 "$LOG" >> "$OUTFILE" || true
        echo >> "$OUTFILE"

        echo "LAST TIMESTAMP:" >> "$OUTFILE"
        tail -n 5 "$LOG" >> "$OUTFILE" || true
        echo >> "$OUTFILE"

        echo "--------------------------------------------------" >> "$OUTFILE"
        echo >> "$OUTFILE"
    fi
done

echo "TOTAL ERR10619300 RUNS FOUND: $COUNT" >> "$OUTFILE"

echo "Probe complete."
echo "Output written to:"
echo "$OUTFILE"