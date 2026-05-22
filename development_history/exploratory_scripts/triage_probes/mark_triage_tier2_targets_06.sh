#!/usr/bin/env bash
set -euo pipefail

PROBE_NAME="mark_triage_tier2_targets_06"
LOG="/root/Desktop/${PROBE_NAME}.txt"

{
echo "========================================"
echo "${PROBE_NAME}"
echo "Tier 2 recovery probe excluding Desktop and geneID_fix"
echo "Started: $(date -Is)"
echo "Host: $(hostname)"
echo "========================================"
echo

echo "[target run IDs]"
cat <<'EOF'
run_2026_04_17_082417
run_2026_05_13_060859
run_2026_05_14_083044
run_2026_05_14_231247
run_2026_05_14_164444
run_2026_05_15_063040
EOF
echo

echo "[trashinfo original paths mentioning target runs or processed]"
grep -R -n -E "run_2026_04_17_082417|run_2026_05_13_060859|run_2026_05_14_083044|run_2026_05_14_231247|run_2026_05_14_164444|run_2026_05_15_063040|processed|variant_annotation_pipeline/results" \
  /root/.local/share/Trash/info 2>/dev/null | grep -v "geneID_fix" || true
echo

echo "[non-Desktop target run directories]"
find /root \
  -path "/root/Desktop" -prune -o \
  -path "/root/Desktop/*" -prune -o \
  -path "*/geneID_fix/*" -prune -o \
  -type d \( \
    -name "run_2026_04_17_082417" -o \
    -name "run_2026_05_13_060859" -o \
    -name "run_2026_05_14_083044" -o \
    -name "run_2026_05_14_231247" -o \
    -name "run_2026_05_14_164444" -o \
    -name "run_2026_05_15_063040" \
  \) -print 2>/dev/null
echo

echo "[non-Desktop processed directories]"
find /root \
  -path "/root/Desktop" -prune -o \
  -path "/root/Desktop/*" -prune -o \
  -path "*/geneID_fix/*" -prune -o \
  -type d -name "processed" -print 2>/dev/null
echo

echo "[non-Desktop high-value processed filenames]"
find /root \
  -path "/root/Desktop" -prune -o \
  -path "/root/Desktop/*" -prune -o \
  -path "*/geneID_fix/*" -prune -o \
  -type f \( \
    -name "stage_08_selected_transcript_consequences.tsv" -o \
    -name "stage_08_vdb_ready_variants.tsv" -o \
    -name "stage_08_variant_summary.tsv" -o \
    -name "stage_08_rdgp_gene_evidence_seed.tsv" -o \
    -name "coding_candidates.tsv" -o \
    -name "noncoding_candidates.tsv" -o \
    -name "splice_region_candidates.tsv" -o \
    -name "qc_flagged.tsv" -o \
    -name "stage_09_coding_interpreted.tsv" -o \
    -name "stage_10_noncoding_interpreted.tsv" -o \
    -name "stage_11_prioritized_variants.tsv" -o \
    -name "stage_11_gene_variant_counts.tsv" -o \
    -name "stage_12_validation_candidates.tsv" \
  \) -printf "%p\t%k KB\n" 2>/dev/null
echo

echo "[trash files excluding Desktop-derived and geneID_fix]"
find /root/.local/share/Trash/files \
  -path "*/geneID_fix/*" -prune -o \
  -type f \( \
    -name "stage_08_selected_transcript_consequences.tsv" -o \
    -name "stage_08_vdb_ready_variants.tsv" -o \
    -name "stage_08_variant_summary.tsv" -o \
    -name "stage_08_rdgp_gene_evidence_seed.tsv" -o \
    -name "coding_candidates.tsv" -o \
    -name "noncoding_candidates.tsv" -o \
    -name "splice_region_candidates.tsv" -o \
    -name "qc_flagged.tsv" -o \
    -name "stage_09_coding_interpreted.tsv" -o \
    -name "stage_10_noncoding_interpreted.tsv" -o \
    -name "stage_11_prioritized_variants.tsv" -o \
    -name "stage_11_gene_variant_counts.tsv" -o \
    -name "stage_12_validation_candidates.tsv" \
  \) -printf "%p\t%k KB\n" 2>/dev/null
echo

echo "Finished: $(date -Is)"
} > "${LOG}" 2>&1

echo "Wrote ${LOG}"