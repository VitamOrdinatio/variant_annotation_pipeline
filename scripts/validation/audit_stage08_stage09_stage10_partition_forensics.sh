#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="${REPO_ROOT:-$HOME/dev/portfolio_projects/variant_annotation_pipeline}"
OUT_FILE="${OUT_FILE:-/root/Desktop/stage08_stage09_stage10_partition_forensics.md}"

cd "$REPO_ROOT"

RUNS=(
run_2026_05_30_071639
run_2026_06_01_124134
run_2026_05_30_151355
run_2026_05_30_214724
run_2026_05_31_091242
run_2026_06_01_004903
run_2026_06_02_052302
run_2026_05_27_233524
run_2026_06_02_124300
run_2026_05_27_172531
run_2026_06_02_181024
run_2026_06_01_203130
run_2026_06_03_010030
)

{
echo "# Stage08 → Stage09 → Stage10 Partition Forensics"
echo
echo "Generated: $(date -u +"%Y-%m-%dT%H:%M:%SZ")"
echo

for RUN_ID in "${RUNS[@]}"; do

    PROC="results/${RUN_ID}/processed"

    echo "## ${RUN_ID}"
    echo

    if [[ ! -d "$PROC" ]]; then
        echo "Processed directory missing."
        echo
        echo "---"
        echo
        continue
    fi

    STAGE08=$(find "$PROC" -maxdepth 1 -name "stage_08_vdb_ready_variants.tsv" | head -n 1)

    STAGE09=$(find "$PROC" -maxdepth 1 \
        \( -name "*stage*09*.tsv" -o -name "*coding*.tsv" \) \
        | sort | head -n 1)

    STAGE10=$(find "$PROC" -maxdepth 1 \
        \( -name "*stage*10*.tsv" -o -name "*noncoding*.tsv" \) \
        | sort | head -n 1)

    echo "### Files"
    echo

    echo "Stage08:"
    echo "\`${STAGE08:-MISSING}\`"
    echo

    echo "Stage09:"
    echo "\`${STAGE09:-MISSING}\`"
    echo

    echo "Stage10:"
    echo "\`${STAGE10:-MISSING}\`"
    echo

    if [[ -z "${STAGE08:-}" || -z "${STAGE09:-}" || -z "${STAGE10:-}" ]]; then
        echo "One or more required files missing."
        echo
        echo "---"
        echo
        continue
    fi

    S8_ROWS=$(awk 'END {print NR-1}' "$STAGE08")
    S9_ROWS=$(awk 'END {print NR-1}' "$STAGE09")
    S10_ROWS=$(awk 'END {print NR-1}' "$STAGE10")

    SUM_ROWS=$((S9_ROWS + S10_ROWS))
    DELTA=$((S8_ROWS - SUM_ROWS))

    S8_COLS=$(head -n 1 "$STAGE08" | awk -F'\t' '{print NF}')
    S9_COLS=$(head -n 1 "$STAGE09" | awk -F'\t' '{print NF}')
    S10_COLS=$(head -n 1 "$STAGE10" | awk -F'\t' '{print NF}')

    echo "### Row Counts"
    echo

    echo "| Artifact | Rows |"
    echo "|----------|------|"
    echo "| Stage08 | ${S8_ROWS} |"
    echo "| Stage09 | ${S9_ROWS} |"
    echo "| Stage10 | ${S10_ROWS} |"
    echo "| Stage09 + Stage10 | ${SUM_ROWS} |"
    echo

    echo "Partition Delta:"
    echo

    echo "\`${S8_ROWS} - (${S9_ROWS} + ${S10_ROWS}) = ${DELTA}\`"
    echo

    if [[ "$DELTA" -eq 0 ]]; then
        echo "**Result:** Perfect partition reconstruction."
    elif [[ "$DELTA" -gt 0 ]]; then
        echo "**Result:** Stage08 contains rows not represented by Stage09/10."
    else
        echo "**Result:** Stage09/10 contain more rows than Stage08."
    fi

    echo
    echo "### Column Counts"
    echo

    echo "| Artifact | Columns |"
    echo "|----------|---------|"
    echo "| Stage08 | ${S8_COLS} |"
    echo "| Stage09 | ${S9_COLS} |"
    echo "| Stage10 | ${S10_COLS} |"
    echo

    echo "### First Data Row Preview"
    echo

    echo "Stage08:"
    head -n 2 "$STAGE08" | tail -n 1
    echo

    echo "Stage09:"
    head -n 2 "$STAGE09" | tail -n 1
    echo

    echo "Stage10:"
    head -n 2 "$STAGE10" | tail -n 1
    echo

    echo "---"
    echo

done

echo "# Global Summary"
echo

awk '
/\| Stage08 \|/ {s8 += $4}
/\| Stage09 \|/ {s9 += $4}
/\| Stage10 \|/ {s10 += $4}
END {
    print "Aggregated Stage08 rows: " s8
    print "Aggregated Stage09 rows: " s9
    print "Aggregated Stage10 rows: " s10
    print "Aggregated Stage09+10 rows: " s9+s10
    print "Global Delta: " s8-(s9+s10)
}
' "$OUT_FILE" 2>/dev/null || true

} > "$OUT_FILE"

echo "Wrote:"
echo "  $OUT_FILE"