#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="${REPO_ROOT:-$HOME/dev/portfolio_projects/variant_annotation_pipeline}"
OUT_FILE="${OUT_FILE:-/root/Desktop/stage08_partition_integrity_forensics.md}"

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

row_count() {
    awk 'END {print NR > 0 ? NR - 1 : 0}' "$1"
}

pct() {
    awk -v n="$1" -v d="$2" 'BEGIN { if (d > 0) printf "%.6f", (n/d)*100; else print "NA" }'
}

variant_ids() {
    local file="$1"
    awk -F'\t' '
        NR == 1 {
            for (i = 1; i <= NF; i++) if ($i == "variant_id") idx = i
            next
        }
        idx { print $idx }
    ' "$file" | sort -u
}

{
echo "# Stage08 Partition Integrity Forensics"
echo
echo "Generated: $(date -u +"%Y-%m-%dT%H:%M:%SZ")"
echo
echo "Question:"
echo
echo '```text'
echo "Does coding_candidates + splice_region_candidates + noncoding_candidates exactly reconstruct Stage08?"
echo '```'
echo

GLOBAL_S8=0
GLOBAL_CODING=0
GLOBAL_SPLICE=0
GLOBAL_NONCODING=0
GLOBAL_DELTA=0

for RUN_ID in "${RUNS[@]}"; do
    PROC="results/${RUN_ID}/processed"

    S8="$PROC/stage_08_vdb_ready_variants.tsv"
    CODING="$PROC/coding_candidates.tsv"
    SPLICE="$PROC/splice_region_candidates.tsv"
    NONCODING="$PROC/noncoding_candidates.tsv"
    STAGE09="$PROC/stage_09_coding_interpreted.tsv"
    STAGE10="$PROC/stage_10_noncoding_interpreted.tsv"

    echo "## ${RUN_ID}"
    echo

    if [[ ! -f "$S8" || ! -f "$CODING" || ! -f "$SPLICE" || ! -f "$NONCODING" ]]; then
        echo "Missing one or more required Stage08 partition files."
        echo
        echo "---"
        echo
        continue
    fi

    S8_ROWS=$(row_count "$S8")
    CODING_ROWS=$(row_count "$CODING")
    SPLICE_ROWS=$(row_count "$SPLICE")
    NONCODING_ROWS=$(row_count "$NONCODING")
    PARTITION_SUM=$((CODING_ROWS + SPLICE_ROWS + NONCODING_ROWS))
    DELTA=$((S8_ROWS - PARTITION_SUM))

    CODING_PCT=$(pct "$CODING_ROWS" "$S8_ROWS")
    SPLICE_PCT=$(pct "$SPLICE_ROWS" "$S8_ROWS")
    NONCODING_PCT=$(pct "$NONCODING_ROWS" "$S8_ROWS")

    GLOBAL_S8=$((GLOBAL_S8 + S8_ROWS))
    GLOBAL_CODING=$((GLOBAL_CODING + CODING_ROWS))
    GLOBAL_SPLICE=$((GLOBAL_SPLICE + SPLICE_ROWS))
    GLOBAL_NONCODING=$((GLOBAL_NONCODING + NONCODING_ROWS))
    GLOBAL_DELTA=$((GLOBAL_DELTA + DELTA))

    TMPDIR_RUN=$(mktemp -d)
    trap 'rm -rf "$TMPDIR_RUN"' EXIT

    variant_ids "$S8" > "$TMPDIR_RUN/stage08.ids"
    variant_ids "$CODING" > "$TMPDIR_RUN/coding.ids"
    variant_ids "$SPLICE" > "$TMPDIR_RUN/splice.ids"
    variant_ids "$NONCODING" > "$TMPDIR_RUN/noncoding.ids"

    cat "$TMPDIR_RUN/coding.ids" "$TMPDIR_RUN/splice.ids" "$TMPDIR_RUN/noncoding.ids" \
        | sort \
        | uniq -d > "$TMPDIR_RUN/overlap.ids"

    cat "$TMPDIR_RUN/coding.ids" "$TMPDIR_RUN/splice.ids" "$TMPDIR_RUN/noncoding.ids" \
        | sort -u > "$TMPDIR_RUN/partition_union.ids"

    comm -23 "$TMPDIR_RUN/stage08.ids" "$TMPDIR_RUN/partition_union.ids" > "$TMPDIR_RUN/stage08_not_partitioned.ids"
    comm -13 "$TMPDIR_RUN/stage08.ids" "$TMPDIR_RUN/partition_union.ids" > "$TMPDIR_RUN/partition_not_stage08.ids"

    S8_IDS=$(wc -l < "$TMPDIR_RUN/stage08.ids")
    UNION_IDS=$(wc -l < "$TMPDIR_RUN/partition_union.ids")
    OVERLAP_IDS=$(wc -l < "$TMPDIR_RUN/overlap.ids")
    S8_NOT_PARTITIONED=$(wc -l < "$TMPDIR_RUN/stage08_not_partitioned.ids")
    PARTITION_NOT_S8=$(wc -l < "$TMPDIR_RUN/partition_not_stage08.ids")

    echo "### Files"
    echo
    echo "Stage08: \`$S8\`"
    echo "Coding partition: \`$CODING\`"
    echo "Splice partition: \`$SPLICE\`"
    echo "Noncoding partition: \`$NONCODING\`"
    echo

    echo "### Partition Row Accounting"
    echo
    echo "| Metric | Count | Percent of Stage08 |"
    echo "|---|---:|---:|"
    echo "| Stage08 rows | ${S8_ROWS} | 100.000000 |"
    echo "| Coding rows | ${CODING_ROWS} | ${CODING_PCT} |"
    echo "| Splice-region rows | ${SPLICE_ROWS} | ${SPLICE_PCT} |"
    echo "| Noncoding rows | ${NONCODING_ROWS} | ${NONCODING_PCT} |"
    echo "| Coding + splice + noncoding | ${PARTITION_SUM} | $(pct "$PARTITION_SUM" "$S8_ROWS") |"
    echo "| Delta: Stage08 - partitions | ${DELTA} | $(pct "$DELTA" "$S8_ROWS") |"
    echo

    if [[ "$DELTA" -eq 0 ]]; then
        echo "**Row accounting result:** Perfect row reconstruction."
    else
        echo "**Row accounting result:** Partition row sum does not reconstruct Stage08."
    fi
    echo

    echo "### Variant-ID Set Accounting"
    echo
    echo "| Metric | Count |"
    echo "|---|---:|"
    echo "| Stage08 distinct variant_ids | ${S8_IDS} |"
    echo "| Union partition distinct variant_ids | ${UNION_IDS} |"
    echo "| Variant_ids appearing in more than one partition | ${OVERLAP_IDS} |"
    echo "| Stage08 ids absent from partitions | ${S8_NOT_PARTITIONED} |"
    echo "| Partition ids absent from Stage08 | ${PARTITION_NOT_S8} |"
    echo

    if [[ "$S8_NOT_PARTITIONED" -eq 0 && "$PARTITION_NOT_S8" -eq 0 ]]; then
        echo "**Set accounting result:** Partition union exactly reconstructs Stage08 variant_id set."
    else
        echo "**Set accounting result:** Partition union does not exactly reconstruct Stage08 variant_id set."
    fi
    echo

    echo "### Stage09 / Stage10 Downstream Check"
    echo
    if [[ -f "$STAGE09" ]]; then
        STAGE09_ROWS=$(row_count "$STAGE09")
        EXPECTED_STAGE09=$((CODING_ROWS + SPLICE_ROWS))
        STAGE09_DELTA=$((EXPECTED_STAGE09 - STAGE09_ROWS))
        echo "- stage_09_coding_interpreted rows: ${STAGE09_ROWS}"
        echo "- expected coding + splice rows: ${EXPECTED_STAGE09}"
        echo "- expected - observed delta: ${STAGE09_DELTA}"
    else
        echo "- stage_09_coding_interpreted.tsv missing"
    fi

    if [[ -f "$STAGE10" ]]; then
        STAGE10_ROWS=$(row_count "$STAGE10")
        STAGE10_DELTA=$((NONCODING_ROWS - STAGE10_ROWS))
        echo "- stage_10_noncoding_interpreted rows: ${STAGE10_ROWS}"
        echo "- expected noncoding rows: ${NONCODING_ROWS}"
        echo "- expected - observed delta: ${STAGE10_DELTA}"
    else
        echo "- stage_10_noncoding_interpreted.tsv missing"
    fi
    echo

    echo "### First Row Previews"
    echo
    echo "Coding:"
    head -n 2 "$CODING" | tail -n 1
    echo
    echo "Splice-region:"
    head -n 2 "$SPLICE" | tail -n 1
    echo
    echo "Noncoding:"
    head -n 2 "$NONCODING" | tail -n 1
    echo

    rm -rf "$TMPDIR_RUN"
    trap - EXIT

    echo "---"
    echo
done

echo "# Global Summary"
echo
GLOBAL_PARTITION_SUM=$((GLOBAL_CODING + GLOBAL_SPLICE + GLOBAL_NONCODING))
echo "| Metric | Count | Percent of Stage08 |"
echo "|---|---:|---:|"
echo "| Aggregated Stage08 rows | ${GLOBAL_S8} | 100.000000 |"
echo "| Aggregated coding rows | ${GLOBAL_CODING} | $(pct "$GLOBAL_CODING" "$GLOBAL_S8") |"
echo "| Aggregated splice-region rows | ${GLOBAL_SPLICE} | $(pct "$GLOBAL_SPLICE" "$GLOBAL_S8") |"
echo "| Aggregated noncoding rows | ${GLOBAL_NONCODING} | $(pct "$GLOBAL_NONCODING" "$GLOBAL_S8") |"
echo "| Aggregated partition rows | ${GLOBAL_PARTITION_SUM} | $(pct "$GLOBAL_PARTITION_SUM" "$GLOBAL_S8") |"
echo "| Aggregated delta | ${GLOBAL_DELTA} | $(pct "$GLOBAL_DELTA" "$GLOBAL_S8") |"
echo

} > "$OUT_FILE"

echo "Wrote:"
echo "  $OUT_FILE"