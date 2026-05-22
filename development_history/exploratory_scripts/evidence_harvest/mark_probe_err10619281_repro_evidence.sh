#!/usr/bin/env bash
set -u

VAP_ROOT="/root/dev/portfolio_projects/variant_annotation_pipeline"
RUN_A="results/run_2026_05_14_083044"
RUN_B="results/run_2026_05_14_231247"
OUT="/root/Desktop/vap_repro_probe_ERR10619281_$(date -u +%Y%m%dT%H%M%SZ).txt"

{
echo "===== VAP Reproducibility Evidence Probe: ERR10619281 ====="
echo "UTC timestamp: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo "Host: $(hostname)"
echo

cd "$VAP_ROOT" || { echo "ERROR: Cannot cd to $VAP_ROOT"; exit 1; }

echo "===== Repository Context ====="
echo "PWD: $(pwd)"
echo "Git branch: $(git branch --show-current 2>/dev/null || echo UNKNOWN)"
echo "Git commit: $(git rev-parse HEAD 2>/dev/null || echo UNKNOWN)"
echo

echo "===== Compared Runs ====="
echo "Run A: $RUN_A  (ERR10619281 pre-assay-provenance patch)"
echo "Run B: $RUN_B  (ERR10619281 post-assay-provenance patch rerun)"
echo

for d in "$RUN_A" "$RUN_B"; do
  echo "===== Existence Check: $d ====="
  if [ -d "$d" ]; then echo "run_directory: PRESENT"; else echo "run_directory: MISSING"; fi
  for f in \
    "$d/logs/pipeline.log" \
    "$d/metadata/runtime_profile.tsv" \
    "$d/metadata/run_metadata.json" \
    "$d/metadata/run_fingerprint.json" \
    "$d/processed/stage_11_summary.json" \
    "$d/processed/stage_12_summary.json" \
    "$d/processed/stage_13_final_summary.json" \
    "$d/processed/stage_13_run_report.md" \
    "$d/processed/stage_11_prioritized_variants.tsv" \
    "$d/processed/stage_12_validation_candidates.tsv"; do
      if [ -f "$f" ]; then echo "PRESENT $f"; else echo "MISSING $f"; fi
  done
  echo
done

extract_from_log() {
  local d="$1"
  local log="$d/logs/pipeline.log"
  echo "--- log-derived summary: $d ---"
  if [ ! -f "$log" ]; then echo "pipeline.log missing"; echo; return; fi
  grep -E "Run ID:|FASTQ R1 reads detected:|FASTQ R2 reads detected:|Stage 11 input rows processed:|Stage 11 output rows written:|Stage 11 malformed/unassigned rows:|Stage 12 input rows processed:|Stage 12 output rows written:|Stage 12 unrecognized priority rows:|Pipeline run finished|Run status:|Pipeline execution complete|Starting stage:|Completed stage:" "$log" | tail -n 80
  echo
}

echo "===== Log-Derived Summaries ====="
extract_from_log "$RUN_A"
extract_from_log "$RUN_B"

summarize_runtime_profile() {
  local d="$1"
  local f="$d/metadata/runtime_profile.tsv"
  echo "--- runtime_profile summary: $d ---"
  if [ ! -f "$f" ]; then echo "runtime_profile.tsv missing"; echo; return; fi
  echo "line_count: $(wc -l < "$f")"
  echo "header: $(head -n 1 "$f")"
  echo "content:"
  cat "$f"
  echo
}

echo "===== Runtime Profiles ====="
summarize_runtime_profile "$RUN_A"
summarize_runtime_profile "$RUN_B"

summarize_json_like() {
  local d="$1"
  local label="$2"
  local f="$3"
  echo "--- $label: $d ---"
  if [ ! -f "$f" ]; then echo "missing: $f"; echo; return; fi
  echo "file_size_bytes: $(stat -c%s "$f" 2>/dev/null || wc -c < "$f")"
  echo "sha256: $(sha256sum "$f" | awk '{print $1}')"
  echo "first_80_lines:"
  sed -n '1,80p' "$f"
  echo
}

echo "===== Metadata and Summary Artifacts ====="
for d in "$RUN_A" "$RUN_B"; do
  summarize_json_like "$d" "run_metadata.json" "$d/metadata/run_metadata.json"
  summarize_json_like "$d" "run_fingerprint.json" "$d/metadata/run_fingerprint.json"
  summarize_json_like "$d" "stage_11_summary.json" "$d/processed/stage_11_summary.json"
  summarize_json_like "$d" "stage_12_summary.json" "$d/processed/stage_12_summary.json"
  summarize_json_like "$d" "stage_13_final_summary.json" "$d/processed/stage_13_final_summary.json"
done

echo "===== Selected Output File Sizes and Row Counts ====="
for d in "$RUN_A" "$RUN_B"; do
  echo "--- $d ---"
  for f in \
    "$d/processed/stage_11_prioritized_variants.tsv" \
    "$d/processed/stage_11_gene_variant_counts.tsv" \
    "$d/processed/stage_12_validation_candidates.tsv" \
    "$d/processed/stage_13_final_summary.json" \
    "$d/processed/stage_13_run_report.md"; do
      if [ -f "$f" ]; then
        echo "file: $f"
        echo "  size_bytes: $(stat -c%s "$f" 2>/dev/null || wc -c < "$f")"
        echo "  line_count: $(wc -l < "$f")"
        case "$f" in
          *.json|*.md)
            echo "  sha256: $(sha256sum "$f" | awk '{print $1}')"
            ;;
          *)
            echo "  sha256: SKIPPED_large_tabular_file"
            ;;
        esac
      else
        echo "missing: $f"
      fi
  done
  echo
done

echo "===== Lightweight Direct Comparisons ====="
echo "Stage 11 prioritized TSV line counts:"
if [ -f "$RUN_A/processed/stage_11_prioritized_variants.tsv" ] && [ -f "$RUN_B/processed/stage_11_prioritized_variants.tsv" ]; then
  echo "  Run A: $(wc -l < "$RUN_A/processed/stage_11_prioritized_variants.tsv")"
  echo "  Run B: $(wc -l < "$RUN_B/processed/stage_11_prioritized_variants.tsv")"
else
  echo "  unable_to_compare"
fi

echo "Stage 12 validation TSV line counts:"
if [ -f "$RUN_A/processed/stage_12_validation_candidates.tsv" ] && [ -f "$RUN_B/processed/stage_12_validation_candidates.tsv" ]; then
  echo "  Run A: $(wc -l < "$RUN_A/processed/stage_12_validation_candidates.tsv")"
  echo "  Run B: $(wc -l < "$RUN_B/processed/stage_12_validation_candidates.tsv")"
else
  echo "  unable_to_compare"
fi

echo

echo "Small artifact sha256 comparison:"
for rel in \
  "processed/stage_11_summary.json" \
  "processed/stage_12_summary.json" \
  "processed/stage_13_final_summary.json" \
  "processed/stage_13_run_report.md"; do
    a="$RUN_A/$rel"
    b="$RUN_B/$rel"
    echo "--- $rel ---"
    if [ -f "$a" ] && [ -f "$b" ]; then
      sha_a=$(sha256sum "$a" | awk '{print $1}')
      sha_b=$(sha256sum "$b" | awk '{print $1}')
      echo "Run A sha256: $sha_a"
      echo "Run B sha256: $sha_b"
      if [ "$sha_a" = "$sha_b" ]; then echo "comparison: IDENTICAL"; else echo "comparison: DIFFERENT"; fi
    else
      echo "comparison: missing artifact(s)"
    fi
  done

echo

echo "===== Interpretation Reminder ====="
echo "Expected stable: FASTQ counts, Stage 11/12 row counts, schema-level output structure."
echo "Expected variable: run IDs, timestamps, absolute paths, runtime durations, telemetry snapshots, provenance timestamps."
echo "Large BAM/SAM/VCF/TSV byte-level hashing intentionally skipped."
echo

echo "===== Desktop Output ====="
echo "$OUT"
} > "$OUT" 2>&1

cat "$OUT"
