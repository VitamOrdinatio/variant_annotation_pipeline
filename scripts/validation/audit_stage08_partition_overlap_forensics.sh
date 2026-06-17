#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="${REPO_ROOT:-$HOME/dev/portfolio_projects/variant_annotation_pipeline}"
OUT_FILE="${OUT_FILE:-/root/Desktop/stage08_partition_overlap_forensics.md}"

cd "$REPO_ROOT"

RUN_ID="${RUN_ID:-run_2026_06_03_010030}"
PROC="results/${RUN_ID}/processed"

CODING="$PROC/coding_candidates.tsv"
SPLICE="$PROC/splice_region_candidates.tsv"
NONCODING="$PROC/noncoding_candidates.tsv"

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

TMPDIR_RUN=$(mktemp -d)
trap 'rm -rf "$TMPDIR_RUN"' EXIT

variant_ids "$CODING" > "$TMPDIR_RUN/coding.ids"
variant_ids "$SPLICE" > "$TMPDIR_RUN/splice.ids"
variant_ids "$NONCODING" > "$TMPDIR_RUN/noncoding.ids"

comm -12 "$TMPDIR_RUN/coding.ids" "$TMPDIR_RUN/splice.ids" > "$TMPDIR_RUN/coding_splice.ids"
comm -12 "$TMPDIR_RUN/coding.ids" "$TMPDIR_RUN/noncoding.ids" > "$TMPDIR_RUN/coding_noncoding.ids"
comm -12 "$TMPDIR_RUN/splice.ids" "$TMPDIR_RUN/noncoding.ids" > "$TMPDIR_RUN/splice_noncoding.ids"

cat "$TMPDIR_RUN/coding.ids" "$TMPDIR_RUN/splice.ids" "$TMPDIR_RUN/noncoding.ids" \
  | sort \
  | uniq -d > "$TMPDIR_RUN/any_overlap.ids"

extract_rows_by_ids "$TMPDIR_RUN/coding_splice.ids" "$SPLICE" > "$TMPDIR_RUN/coding_splice_rows.tsv"
extract_rows_by_ids "$TMPDIR_RUN/coding_noncoding.ids" "$CODING" > "$TMPDIR_RUN/coding_noncoding_rows.tsv"
extract_rows_by_ids "$TMPDIR_RUN/splice_noncoding.ids" "$SPLICE" > "$TMPDIR_RUN/splice_noncoding_rows.tsv"

{
echo "# Stage08 Partition Overlap Forensics"
echo
echo "Generated: $(date -u +"%Y-%m-%dT%H:%M:%SZ")"
echo
echo "Run audited: \`${RUN_ID}\`"
echo
echo "Purpose:"
echo
echo '```text'
echo "Determine whether Stage08 partition overlap is primarily coding ∩ splice,"
echo "or whether overlap also involves noncoding partition membership."
echo '```'
echo

echo "## Files"
echo
echo "- Coding: \`$CODING\`"
echo "- Splice: \`$SPLICE\`"
echo "- Noncoding: \`$NONCODING\`"
echo

echo "## Overlap Counts"
echo
echo "| Intersection | Distinct variant_ids |"
echo "|---|---:|"
echo "| coding ∩ splice | $(wc -l < "$TMPDIR_RUN/coding_splice.ids") |"
echo "| coding ∩ noncoding | $(wc -l < "$TMPDIR_RUN/coding_noncoding.ids") |"
echo "| splice ∩ noncoding | $(wc -l < "$TMPDIR_RUN/splice_noncoding.ids") |"
echo "| any overlap | $(wc -l < "$TMPDIR_RUN/any_overlap.ids") |"
echo

echo "## Coding ∩ Splice Characterization"
echo
echo "### variant_context"
echo '```text'
summarize_column "$TMPDIR_RUN/coding_splice_rows.tsv" "variant_context"
echo '```'
echo
echo "### variant_class"
echo '```text'
summarize_column "$TMPDIR_RUN/coding_splice_rows.tsv" "variant_class"
echo '```'
echo
echo "### consequence"
echo '```text'
summarize_column "$TMPDIR_RUN/coding_splice_rows.tsv" "consequence"
echo '```'
echo
echo "### impact_class"
echo '```text'
summarize_column "$TMPDIR_RUN/coding_splice_rows.tsv" "impact_class"
echo '```'
echo

echo "## Coding ∩ Noncoding Characterization"
echo
echo "### First 20 rows"
echo '```text'
head -n 21 "$TMPDIR_RUN/coding_noncoding_rows.tsv"
echo '```'
echo

echo "## Splice ∩ Noncoding Characterization"
echo
echo "### First 20 rows"
echo '```text'
head -n 21 "$TMPDIR_RUN/splice_noncoding_rows.tsv"
echo '```'
echo

echo "## Coding ∩ Splice First 20 Rows"
echo
echo '```text'
head -n 21 "$TMPDIR_RUN/coding_splice_rows.tsv"
echo '```'
echo

} > "$OUT_FILE"

echo "Wrote:"
echo "  $OUT_FILE"