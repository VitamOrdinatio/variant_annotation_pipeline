#!/usr/bin/env bash
set -euo pipefail

# ============================================================
# MARK Probe: Rapid Epilepsy + MitoCarta Candidate Scan
#
# Purpose:
#   Quickly inspect Stage 11 prioritized variants for:
#   - EPI25-associated loci
#   - mitochondrial disease / MitoCarta-associated loci
#
# Intended Usage:
#   Save on MARK as:
#     /root/Desktop/mark_probe_epi_mito_hits.sh
#
#   Run from anywhere:
#     bash /root/Desktop/mark_probe_epi_mito_hits.sh
#
# Output:
#   Small TXT summaries written to /root/Desktop/
#
# Notes:
#   - Lightweight grep-only probe
#   - No TSV transfer required
#   - Designed for rapid biological signal triage
# ============================================================

REPO_DIR="/root/dev/portfolio_projects/variant_annotation_pipeline"

RUN_ERR10619281="results/run_2026_05_14_231247"
RUN_ERR10619300="results/run_2026_05_14_164444"

OUT1="/root/Desktop/err10619281_gene_hits.txt"
OUT2="/root/Desktop/err10619300_gene_hits.txt"

GENE_PATTERN="SCN1A|DEPDC5|NPRL3|NEXMIF|SYNGAP1|STX1B|WDR45|POLG|TWNK|OPA1|MFN2|DNA2|LONP1"

echo "=================================================="
echo "MARK Probe: EPI25 + MitoCarta Candidate Scan"
echo "=================================================="
echo

cd "$REPO_DIR"

echo "Repository:"
pwd
echo

echo "Gene pattern:"
echo "$GENE_PATTERN"
echo

echo "=================================================="
echo "Scanning ERR10619281"
echo "=================================================="

grep -Ei "$GENE_PATTERN" \
"${RUN_ERR10619281}/processed/stage_11_prioritized_variants.tsv" \
> "$OUT1" || true

echo "Output written:"
echo "$OUT1"
echo

echo "Hit count:"
wc -l "$OUT1"
echo

echo "=================================================="
echo "Scanning ERR10619300"
echo "=================================================="

grep -Ei "$GENE_PATTERN" \
"${RUN_ERR10619300}/processed/stage_11_prioritized_variants.tsv" \
> "$OUT2" || true

echo "Output written:"
echo "$OUT2"
echo

echo "Hit count:"
wc -l "$OUT2"
echo

echo "=================================================="
echo "Preview: ERR10619281"
echo "=================================================="

head -n 10 "$OUT1" || true
echo

echo "=================================================="
echo "Preview: ERR10619300"
echo "=================================================="

head -n 10 "$OUT2" || true
echo

echo "=================================================="
echo "Probe complete."
echo "=================================================="