#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$HOME/dev/portfolio_projects/variant_annotation_pipeline"
RUN_ID="run_2026_05_14_164444"
RUN_DIR="${REPO_DIR}/results/${RUN_ID}"
OUTFILE="/root/Desktop/stage11_schema_probe_${RUN_ID}.txt"

STAGE11="${RUN_DIR}/processed/stage_11_prioritized_variants.tsv"
GENE_COUNTS="${RUN_DIR}/processed/stage_11_gene_variant_counts.tsv"
VDB_READY="${RUN_DIR}/processed/stage_08_vdb_ready_variants.tsv"

{
echo "=================================================="
echo "Stage 11 / VDB Schema Probe"
echo "=================================================="
echo "REPO_DIR: ${REPO_DIR}"
echo "RUN_ID: ${RUN_ID}"
echo

for FILE in "$STAGE11" "$GENE_COUNTS" "$VDB_READY"; do
    echo "=================================================="
    echo "FILE: ${FILE}"
    echo "=================================================="

    if [[ ! -f "$FILE" ]]; then
        echo "[MISSING]"
        echo
        continue
    fi

    echo "SIZE:"
    ls -lh "$FILE"
    echo

    echo "LINE COUNT:"
    wc -l "$FILE"
    echo

    echo "COLUMN COUNT:"
    head -n 1 "$FILE" | awk -F'\t' '{print NF}'
    echo

    echo "HEADER FIELDS:"
    head -n 1 "$FILE" | tr '\t' '\n' | nl -ba
    echo

    echo "FIRST 3 DATA ROWS:"
    head -n 4 "$FILE" | tail -n 3
    echo

    echo "FIELDS OF INTEREST:"
    head -n 1 "$FILE" | tr '\t' '\n' | grep -Ein "gene|consequence|impact|clinical|priority|tier|rank|allele|frequency|variant|chrom|pos|ref|alt|symbol|id" || true
    echo
done

echo "=================================================="
echo "Stage 11 HIGH/MODERATE/MULTI-CONSEQUENCE SAMPLES"
echo "=================================================="

if [[ -f "$STAGE11" ]]; then
    echo "HIGH rows:"
    grep -m 3 "HIGH" "$STAGE11" || true
    echo

    echo "MODERATE rows:"
    grep -m 3 "MODERATE" "$STAGE11" || true
    echo

    echo "Rows with &:"
    grep -m 3 "&" "$STAGE11" || true
    echo
fi

echo "=================================================="
echo "COMPLETE"
echo "=================================================="
} > "$OUTFILE"

echo "Probe complete."
echo "Output written to:"
echo "$OUTFILE"