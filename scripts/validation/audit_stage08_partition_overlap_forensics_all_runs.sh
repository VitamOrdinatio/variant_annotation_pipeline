#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="${REPO_ROOT:-$HOME/dev/portfolio_projects/variant_annotation_pipeline}"
OUT_FILE="${OUT_FILE:-/root/Desktop/stage08_partition_overlap_forensics_all_runs.md}"

cd "$REPO_ROOT"

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

extract_rows_by_ids() {
    local ids="$1"
    local source="$2"
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
    ' "$ids" "$source"
}

summarize_column() {
    local file="$1"
    local column="$2"
    awk -F'\t' -v col="$column" '
        NR == 1 {
            for (i = 1; i <= NF; i++) if ($i == col) idx = i
            next
        }
        idx {
            value = $idx
            if (value == "") value = "EMPTY"
            counts[value]++
        }
        END {
            for (value in counts) print counts[value] "\t" value
        }
    ' "$file" | sort -nr | head -n 30
}

{
echo "# Stage08 Partition Overlap Forensics: All Runs"
echo
echo "Generated: $(date -u +"%Y-%m-%dT%H:%M:%SZ")"
echo
echo "Purpose:"
echo
echo '```text'
echo "Test whether Stage08 partition overlap is consistently limited to coding ∩ splice"
echo "across 12 epilepsy WES runs and 1 HG002 WGS run."
echo '```'
echo

TOTAL_CODING_SPLICE=0
TOTAL_CODING_NONCODING=0
TOTAL_SPLICE_NONCODING=0
TOTAL_ANY_OVERLAP=0

echo "## Compact Summary"
echo
echo "| sample_id | run_id | depth | coding ∩ splice | coding ∩ noncoding | splice ∩ noncoding | any overlap |"
echo "|---|---|---|---:|---:|---:|---:|"

while IFS=$'\t' read -r SAMPLE_ID RUN_ID DEPTH; do
    [[ "$SAMPLE_ID" == "sample_id" ]] && continue

    PROC="results/${RUN_ID}/processed"
    CODING="$PROC/coding_candidates.tsv"
    SPLICE="$PROC/splice_region_candidates.tsv"
    NONCODING="$PROC/noncoding_candidates.tsv"

    TMPDIR_RUN=$(mktemp -d)

    variant_ids "$CODING" > "$TMPDIR_RUN/coding.ids"
    variant_ids "$SPLICE" > "$TMPDIR_RUN/splice.ids"
    variant_ids "$NONCODING" > "$TMPDIR_RUN/noncoding.ids"

    comm -12 "$TMPDIR_RUN/coding.ids" "$TMPDIR_RUN/splice.ids" > "$TMPDIR_RUN/coding_splice.ids"
    comm -12 "$TMPDIR_RUN/coding.ids" "$TMPDIR_RUN/noncoding.ids" > "$TMPDIR_RUN/coding_noncoding.ids"
    comm -12 "$TMPDIR_RUN/splice.ids" "$TMPDIR_RUN/noncoding.ids" > "$TMPDIR_RUN/splice_noncoding.ids"

    cat "$TMPDIR_RUN/coding.ids" "$TMPDIR_RUN/splice.ids" "$TMPDIR_RUN/noncoding.ids" \
      | sort \
      | uniq -d > "$TMPDIR_RUN/any_overlap.ids"

    CS=$(wc -l < "$TMPDIR_RUN/coding_splice.ids")
    CN=$(wc -l < "$TMPDIR_RUN/coding_noncoding.ids")
    SN=$(wc -l < "$TMPDIR_RUN/splice_noncoding.ids")
    AO=$(wc -l < "$TMPDIR_RUN/any_overlap.ids")

    TOTAL_CODING_SPLICE=$((TOTAL_CODING_SPLICE + CS))
    TOTAL_CODING_NONCODING=$((TOTAL_CODING_NONCODING + CN))
    TOTAL_SPLICE_NONCODING=$((TOTAL_SPLICE_NONCODING + SN))
    TOTAL_ANY_OVERLAP=$((TOTAL_ANY_OVERLAP + AO))

    echo "| ${SAMPLE_ID} | ${RUN_ID} | ${DEPTH} | ${CS} | ${CN} | ${SN} | ${AO} |"

    rm -rf "$TMPDIR_RUN"

done <<'EOF'
sample_id	run_id	depth_category
ERR10619203	run_2026_05_30_071639	q3
ERR10619207	run_2026_06_01_124134	q3
ERR10619208	run_2026_05_30_151355	median
ERR10619212	run_2026_05_30_214724	q1
ERR10619225	run_2026_05_31_091242	q3
ERR10619230	run_2026_06_01_004903	q3
ERR10619241	run_2026_06_02_052302	q1
ERR10619281	run_2026_05_27_233524	median
ERR10619285	run_2026_06_02_124300	median
ERR10619300	run_2026_05_27_172531	median
ERR10619309	run_2026_06_02_181024	q1
ERR10619330	run_2026_06_01_203130	q1
hg002	run_2026_06_03_010030	hg002
EOF

echo
echo "## Aggregate Overlap Counts"
echo
echo "| Intersection | Total distinct overlap observations across runs |"
echo "|---|---:|"
echo "| coding ∩ splice | ${TOTAL_CODING_SPLICE} |"
echo "| coding ∩ noncoding | ${TOTAL_CODING_NONCODING} |"
echo "| splice ∩ noncoding | ${TOTAL_SPLICE_NONCODING} |"
echo "| any overlap | ${TOTAL_ANY_OVERLAP} |"
echo

echo "## Detailed Characterization Per Run"
echo

while IFS=$'\t' read -r SAMPLE_ID RUN_ID DEPTH; do
    [[ "$SAMPLE_ID" == "sample_id" ]] && continue

    PROC="results/${RUN_ID}/processed"
    CODING="$PROC/coding_candidates.tsv"
    SPLICE="$PROC/splice_region_candidates.tsv"
    NONCODING="$PROC/noncoding_candidates.tsv"

    TMPDIR_RUN=$(mktemp -d)

    variant_ids "$CODING" > "$TMPDIR_RUN/coding.ids"
    variant_ids "$SPLICE" > "$TMPDIR_RUN/splice.ids"
    variant_ids "$NONCODING" > "$TMPDIR_RUN/noncoding.ids"

    comm -12 "$TMPDIR_RUN/coding.ids" "$TMPDIR_RUN/splice.ids" > "$TMPDIR_RUN/coding_splice.ids"
    comm -12 "$TMPDIR_RUN/coding.ids" "$TMPDIR_RUN/noncoding.ids" > "$TMPDIR_RUN/coding_noncoding.ids"
    comm -12 "$TMPDIR_RUN/splice.ids" "$TMPDIR_RUN/noncoding.ids" > "$TMPDIR_RUN/splice_noncoding.ids"

    extract_rows_by_ids "$TMPDIR_RUN/coding_splice.ids" "$SPLICE" > "$TMPDIR_RUN/coding_splice_rows.tsv"
    extract_rows_by_ids "$TMPDIR_RUN/coding_noncoding.ids" "$CODING" > "$TMPDIR_RUN/coding_noncoding_rows.tsv"
    extract_rows_by_ids "$TMPDIR_RUN/splice_noncoding.ids" "$SPLICE" > "$TMPDIR_RUN/splice_noncoding_rows.tsv"

    echo "### ${SAMPLE_ID} / ${RUN_ID} / ${DEPTH}"
    echo

    echo "#### coding ∩ splice: variant_context"
    echo '```text'
    summarize_column "$TMPDIR_RUN/coding_splice_rows.tsv" "variant_context"
    echo '```'
    echo

    echo "#### coding ∩ splice: consequence"
    echo '```text'
    summarize_column "$TMPDIR_RUN/coding_splice_rows.tsv" "consequence"
    echo '```'
    echo

    echo "#### coding ∩ splice: impact_class"
    echo '```text'
    summarize_column "$TMPDIR_RUN/coding_splice_rows.tsv" "impact_class"
    echo '```'
    echo

    echo "#### coding ∩ noncoding preview"
    echo '```text'
    head -n 6 "$TMPDIR_RUN/coding_noncoding_rows.tsv"
    echo '```'
    echo

    echo "#### splice ∩ noncoding preview"
    echo '```text'
    head -n 6 "$TMPDIR_RUN/splice_noncoding_rows.tsv"
    echo '```'
    echo

    rm -rf "$TMPDIR_RUN"

done <<'EOF'
sample_id	run_id	depth_category
ERR10619203	run_2026_05_30_071639	q3
ERR10619207	run_2026_06_01_124134	q3
ERR10619208	run_2026_05_30_151355	median
ERR10619212	run_2026_05_30_214724	q1
ERR10619225	run_2026_05_31_091242	q3
ERR10619230	run_2026_06_01_004903	q3
ERR10619241	run_2026_06_02_052302	q1
ERR10619281	run_2026_05_27_233524	median
ERR10619285	run_2026_06_02_124300	median
ERR10619300	run_2026_05_27_172531	median
ERR10619309	run_2026_06_02_181024	q1
ERR10619330	run_2026_06_01_203130	q1
hg002	run_2026_06_03_010030	hg002
EOF

} > "$OUT_FILE"

echo "Wrote:"
echo "  $OUT_FILE"