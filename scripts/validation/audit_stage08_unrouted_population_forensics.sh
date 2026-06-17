#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="${REPO_ROOT:-$HOME/dev/portfolio_projects/variant_annotation_pipeline}"
OUT_FILE="${OUT_FILE:-/root/Desktop/stage08_unrouted_population_forensics.md}"

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

summarize_column() {
    local file="$1"
    local column="$2"
    awk -F'\t' -v col="$column" '
        NR == 1 {
            for (i = 1; i <= NF; i++) {
                if ($i == col) idx = i
            }
            next
        }
        idx {
            value = $idx
            if (value == "") value = "EMPTY"
            counts[value]++
        }
        END {
            for (value in counts) {
                print counts[value] "\t" value
            }
        }
    ' "$file" | sort -nr | head -n 20
}

{
echo "# Stage08 Unrouted Population Forensics"
echo
echo "Generated: $(date -u +"%Y-%m-%dT%H:%M:%SZ")"
echo
echo "Definition:"
echo
echo '```text'
echo "unrouted_population = Stage08 variant_ids - union(Stage09 variant_ids, Stage10 variant_ids)"
echo '```'
echo

for RUN_ID in "${RUNS[@]}"; do
    PROC="results/${RUN_ID}/processed"

    STAGE08="$PROC/stage_08_vdb_ready_variants.tsv"
    STAGE09="$PROC/coding_candidates.tsv"
    STAGE10="$PROC/noncoding_candidates.tsv"

    echo "## ${RUN_ID}"
    echo

    if [[ ! -f "$STAGE08" || ! -f "$STAGE09" || ! -f "$STAGE10" ]]; then
        echo "Missing one or more required files."
        echo
        echo "---"
        echo
        continue
    fi

    TMPDIR_RUN=$(mktemp -d)
    trap 'rm -rf "$TMPDIR_RUN"' EXIT

    S8_IDS="$TMPDIR_RUN/stage08.ids"
    S9_IDS="$TMPDIR_RUN/stage09.ids"
    S10_IDS="$TMPDIR_RUN/stage10.ids"
    ROUTED_IDS="$TMPDIR_RUN/routed.ids"
    UNROUTED_IDS="$TMPDIR_RUN/unrouted.ids"
    UNROUTED_TSV="$TMPDIR_RUN/unrouted.tsv"

    awk -F'\t' '
        NR == 1 {
            for (i = 1; i <= NF; i++) if ($i == "variant_id") idx = i
            next
        }
        idx { print $idx }
    ' "$STAGE08" | sort -u > "$S8_IDS"

    awk -F'\t' '
        NR == 1 {
            for (i = 1; i <= NF; i++) if ($i == "variant_id") idx = i
            next
        }
        idx { print $idx }
    ' "$STAGE09" | sort -u > "$S9_IDS"

    awk -F'\t' '
        NR == 1 {
            for (i = 1; i <= NF; i++) if ($i == "variant_id") idx = i
            next
        }
        idx { print $idx }
    ' "$STAGE10" | sort -u > "$S10_IDS"

    cat "$S9_IDS" "$S10_IDS" | sort -u > "$ROUTED_IDS"

    comm -23 "$S8_IDS" "$ROUTED_IDS" > "$UNROUTED_IDS"

    awk -F'\t' '
        NR == FNR {
            keep[$1] = 1
            next
        }
        FNR == 1 {
            print
            for (i = 1; i <= NF; i++) if ($i == "variant_id") idx = i
            next
        }
        idx && ($idx in keep) {
            print
        }
    ' "$UNROUTED_IDS" "$STAGE08" > "$UNROUTED_TSV"

    S8_ROWS=$(awk 'END {print NR-1}' "$STAGE08")
    S9_ROWS=$(awk 'END {print NR-1}' "$STAGE09")
    S10_ROWS=$(awk 'END {print NR-1}' "$STAGE10")
    S8_IDS_N=$(wc -l < "$S8_IDS")
    ROUTED_IDS_N=$(wc -l < "$ROUTED_IDS")
    UNROUTED_IDS_N=$(wc -l < "$UNROUTED_IDS")
    UNROUTED_ROWS=$(awk 'END {print NR-1}' "$UNROUTED_TSV")

    echo "### Files"
    echo
    echo "Stage08: \`$STAGE08\`"
    echo "Stage09: \`$STAGE09\`"
    echo "Stage10: \`$STAGE10\`"
    echo

    echo "### Counts"
    echo
    echo "| Metric | Count |"
    echo "|---|---:|"
    echo "| Stage08 rows | ${S8_ROWS} |"
    echo "| Stage09 rows | ${S9_ROWS} |"
    echo "| Stage10 rows | ${S10_ROWS} |"
    echo "| Stage08 distinct variant_ids | ${S8_IDS_N} |"
    echo "| Routed distinct variant_ids | ${ROUTED_IDS_N} |"
    echo "| Unrouted distinct variant_ids | ${UNROUTED_IDS_N} |"
    echo "| Unrouted Stage08 rows | ${UNROUTED_ROWS} |"
    echo

    echo "### Unrouted Population: variant_context"
    echo
    echo '```text'
    summarize_column "$UNROUTED_TSV" "variant_context"
    echo '```'
    echo

    echo "### Unrouted Population: variant_class"
    echo
    echo '```text'
    summarize_column "$UNROUTED_TSV" "variant_class"
    echo '```'
    echo

    echo "### Unrouted Population: gene_mapping_status"
    echo
    echo '```text'
    summarize_column "$UNROUTED_TSV" "gene_mapping_status"
    echo '```'
    echo

    echo "### Unrouted Population: qc_status"
    echo
    echo '```text'
    summarize_column "$UNROUTED_TSV" "qc_status"
    echo '```'
    echo

    echo "### Unrouted Population: interpretability_status"
    echo
    echo '```text'
    summarize_column "$UNROUTED_TSV" "interpretability_status"
    echo '```'
    echo

    echo "### Unrouted Population: frequency_status"
    echo
    echo '```text'
    summarize_column "$UNROUTED_TSV" "frequency_status"
    echo '```'
    echo

    echo "### Unrouted Population: clinical_status"
    echo
    echo '```text'
    summarize_column "$UNROUTED_TSV" "clinical_status"
    echo '```'
    echo

    echo "### First 10 Unrouted Rows"
    echo
    echo '```text'
    head -n 11 "$UNROUTED_TSV"
    echo '```'
    echo

    rm -rf "$TMPDIR_RUN"
    trap - EXIT

    echo "---"
    echo

done

} > "$OUT_FILE"

echo "Wrote:"
echo "  $OUT_FILE"