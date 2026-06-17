#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="${REPO_ROOT:-$HOME/dev/portfolio_projects/variant_annotation_pipeline}"
OUT_FILE="${OUT_FILE:-/root/Desktop/stage07_stage08_boundary_forensics.md}"

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
echo "# Stage07 → Stage08 Boundary Forensics"
echo
echo "Generated: $(date -u +"%Y-%m-%dT%H:%M:%SZ")"
echo

for RUN_ID in "${RUNS[@]}"; do

    PROC="results/${RUN_ID}/processed"

    echo "## ${RUN_ID}"
    echo

    if [[ ! -d "$PROC" ]]; then
        echo "processed directory missing"
        echo
        continue
    fi

    STAGE07=$(find "$PROC" -maxdepth 1 -name "*.annotated_variants.tsv" | head -n 1)
    STAGE08_SELECTED="$PROC/stage_08_selected_transcript_consequences.tsv"
    STAGE08_VDB="$PROC/stage_08_vdb_ready_variants.tsv"

    echo "### Files"
    echo

    echo "Stage07:"
    echo "\`$STAGE07\`"
    echo

    echo "Stage08 selected:"
    echo "\`$STAGE08_SELECTED\`"
    echo

    echo "Stage08 vdb:"
    echo "\`$STAGE08_VDB\`"
    echo

    echo "### Line Counts"
    echo

    wc -l \
        "$STAGE07" \
        "$STAGE08_SELECTED" \
        "$STAGE08_VDB"

    echo
    echo "### Header Field Counts"
    echo

    echo -n "Stage07: "
    head -n 1 "$STAGE07" | awk -F'\t' '{print NF}'

    echo -n "Stage08 selected: "
    head -n 1 "$STAGE08_SELECTED" | awk -F'\t' '{print NF}'

    echo -n "Stage08 vdb: "
    head -n 1 "$STAGE08_VDB" | awk -F'\t' '{print NF}'

    echo
    echo "### Stage07 Header"
    echo

    head -n 1 "$STAGE07" | tr '\t' '\n' | nl -ba

    echo
    echo "### Stage08 Selected Header"
    echo

    head -n 1 "$STAGE08_SELECTED" | tr '\t' '\n' | nl -ba

    echo
    echo "### Stage08 VDB Header"
    echo

    head -n 1 "$STAGE08_VDB" | tr '\t' '\n' | nl -ba

    echo
    echo "### First Data Row Preview"
    echo

    echo "Stage07:"
    head -n 2 "$STAGE07" | tail -n 1

    echo
    echo "Stage08 selected:"
    head -n 2 "$STAGE08_SELECTED" | tail -n 1

    echo
    echo "Stage08 vdb:"
    head -n 2 "$STAGE08_VDB" | tail -n 1

    echo
    echo "---"
    echo

done

} > "$OUT_FILE"

echo "Wrote:"
echo "  $OUT_FILE"