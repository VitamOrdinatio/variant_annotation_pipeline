#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="${REPO_ROOT:-$HOME/dev/portfolio_projects/variant_annotation_pipeline}"
OUT_FILE="${OUT_FILE:-/root/Desktop/stage08_artifact_equivalence_forensics.md}"

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
echo "# Stage08 Artifact Equivalence Forensics"
echo
echo "Generated: $(date -u +"%Y-%m-%dT%H:%M:%SZ")"
echo

for RUN_ID in "${RUNS[@]}"; do
    PROC="results/${RUN_ID}/processed"

    SELECTED="$PROC/stage_08_selected_transcript_consequences.tsv"
    VDB="$PROC/stage_08_vdb_ready_variants.tsv"

    echo "## ${RUN_ID}"
    echo

    if [[ ! -f "$SELECTED" || ! -f "$VDB" ]]; then
        echo "Missing one or both Stage08 files."
        echo
        echo "---"
        echo
        continue
    fi

    echo "### Files"
    echo
    echo "Selected: \`$SELECTED\`"
    echo "VDB-ready: \`$VDB\`"
    echo

    echo "### Byte Sizes"
    echo
    wc -c "$SELECTED" "$VDB"
    echo

    echo "### Line Counts"
    echo
    wc -l "$SELECTED" "$VDB"
    echo

    echo "### SHA256"
    echo
    sha256sum "$SELECTED" "$VDB"
    echo

    echo "### Headers Identical?"
    if diff -q <(head -n 1 "$SELECTED") <(head -n 1 "$VDB") >/dev/null; then
        echo "YES"
    else
        echo "NO"
    fi
    echo

    echo "### Whole-File Identical?"
    if cmp -s "$SELECTED" "$VDB"; then
        echo "YES"
    else
        echo "NO"
        echo
        echo "First differing byte:"
        cmp "$SELECTED" "$VDB" | head -n 1 || true
        echo
        echo "First 5 textual diffs:"
        diff -u "$SELECTED" "$VDB" | head -n 80 || true
    fi

    echo
    echo "---"
    echo

done

} > "$OUT_FILE"

echo "Wrote:"
echo "  $OUT_FILE"