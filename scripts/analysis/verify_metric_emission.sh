#!/usr/bin/env bash
set -euo pipefail

NEW_RUN="${1:-/tmp/vap_metric_fixture_runs/run_2026_05_21_233529}"
OLD_RUN="${2:-results/run_2026_04_17_082417/raw_mark_outputs}"

echo "[config]"
echo "NEW_RUN=${NEW_RUN}"
echo "OLD_RUN=${OLD_RUN}"
echo

echo "[metrics files]"
find "$NEW_RUN/metrics" -maxdepth 1 -type f -print | sort
echo

echo "[processed files]"
find "$NEW_RUN/processed" -maxdepth 1 -type f -print | sort
echo

echo "[metric long TSV rows]"
wc -l "$NEW_RUN/metrics/stage_metrics_long.tsv"
echo

echo "[old annotated input rows]"
wc -l "$OLD_RUN/processed/HG002_run_2026_04_17_082417.annotated_variants.tsv"
echo

echo "[new stage 08 selected rows]"
wc -l "$NEW_RUN/processed/stage_08_selected_transcript_consequences.tsv"
echo

echo "[new stage 11 prioritized rows]"
wc -l "$NEW_RUN/processed/stage_11_prioritized_variants.tsv"
echo

echo "[new stage 12 validation rows]"
wc -l "$NEW_RUN/processed/stage_12_validation_candidates.tsv"
echo

echo "[stage summaries]"
cat "$NEW_RUN/processed/stage_08_summary.json"
echo
cat "$NEW_RUN/processed/stage_11_summary.json"
echo
cat "$NEW_RUN/processed/stage_12_summary.json"
echo