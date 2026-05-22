#!/usr/bin/env bash
set -euo pipefail

# ============================================================
# MARK Probe: ERR10619281 Pipeline Logs
#
# Purpose:
#   Locate all VAP runs associated with ERR10619281
#   using ONLY pipeline.log files.
#
# Output:
#   /root/Desktop/err10619281_pipeline_runs.txt
# ============================================================

REPO_DIR="/root/dev/portfolio_projects/variant_annotation_pipeline"
OUTFILE="/root/Desktop/err10619281_pipeline_runs.txt"

echo "==================================================" > "$OUTFILE"
echo "ERR10619281 Pipeline Log Probe" >> "$OUTFILE"
echo "==================================================" >> "$OUTFILE"
echo >> "$OUTFILE"

cd "$REPO_DIR"

for LOG in results/run_*/logs/pipeline.log; do

    if grep -q "ERR10619281" "$LOG"; then

        RUN_DIR=$(dirname "$(dirname "$LOG")")

        echo "RUN DIRECTORY: $RUN_DIR" >> "$OUTFILE"

        echo >> "$OUTFILE"
        echo "START:" >> "$OUTFILE"
        grep -m1 "Config loaded successfully" "$LOG" >> "$OUTFILE" || true

        echo >> "$OUTFILE"
        echo "STOP:" >> "$OUTFILE"
        grep "Pipeline completed successfully" "$LOG" | tail -n1 >> "$OUTFILE" || true

        echo >> "$OUTFILE"
        echo "--------------------------------------------------" >> "$OUTFILE"
        echo >> "$OUTFILE"

    fi

done

echo "Probe complete."
echo "Output written to:"
echo "$OUTFILE"