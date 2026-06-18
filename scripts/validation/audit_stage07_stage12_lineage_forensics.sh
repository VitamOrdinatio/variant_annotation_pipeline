#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="${REPO_ROOT:-$HOME/dev/portfolio_projects/variant_annotation_pipeline}"
OUT_FILE="${OUT_FILE:-/root/Desktop/stage07_stage12_lineage_forensics.md}"

cd "$REPO_ROOT"

row_count() {
    local file="$1"
    awk 'END {print NR > 0 ? NR - 1 : 0}' "$file"
}

col_count() {
    local file="$1"
    head -n 1 "$file" | awk -F'\t' '{print NF}'
}

header_fields() {
    local file="$1"
    head -n 1 "$file" | tr '\t' '\n'
}

header_checksum() {
    local file="$1"
    head -n 1 "$file" | sha256sum | awk '{print $1}'
}

has_column() {
    local file="$1"
    local column="$2"
    head -n 1 "$file" | tr '\t' '\n' | grep -Fxq "$column" && echo "yes" || echo "no"
}

variant_id_count() {
    local file="$1"
    if [[ "$(has_column "$file" "variant_id")" != "yes" ]]; then
        echo "NA"
        return
    fi
    awk -F'\t' '
        NR == 1 {
            for (i = 1; i <= NF; i++) if ($i == "variant_id") idx = i
            next
        }
        idx { print $idx }
    ' "$file" | sort -u | wc -l
}

sample_row() {
    local file="$1"
    head -n 2 "$file" | tail -n 1 | cut -c 1-500
}

field_diff_left_only() {
    local left="$1"
    local right="$2"
    comm -23 <(header_fields "$left" | sort -u) <(header_fields "$right" | sort -u) | paste -sd "," -
}

field_diff_right_only() {
    local left="$1"
    local right="$2"
    comm -13 <(header_fields "$left" | sort -u) <(header_fields "$right" | sort -u) | paste -sd "," -
}

field_shared() {
    local left="$1"
    local right="$2"
    comm -12 <(header_fields "$left" | sort -u) <(header_fields "$right" | sort -u) | paste -sd "," -
}

file_size() {
    local file="$1"
    stat -c%s "$file"
}

find_stage07() {
    local proc="$1"
    find "$proc" -maxdepth 1 -type f -name "*.annotated_variants.tsv" | sort | head -n 1
}

emit_artifact_block() {
    local label="$1"
    local file="$2"

    echo "### ${label}"
    echo
    if [[ -z "$file" || ! -f "$file" ]]; then
        echo "- status: MISSING"
        echo
        return
    fi

    echo "- path: \`$file\`"
    echo "- size_bytes: $(file_size "$file")"
    echo "- rows: $(row_count "$file")"
    echo "- columns: $(col_count "$file")"
    echo "- header_sha256: \`$(header_checksum "$file")\`"
    echo "- has_variant_id: $(has_column "$file" "variant_id")"
    echo "- distinct_variant_ids: $(variant_id_count "$file")"
    echo
    echo "Header:"
    echo '```text'
    header_fields "$file" | nl -ba
    echo '```'
    echo
    echo "First data row preview:"
    echo '```text'
    sample_row "$file"
    echo
    echo '```'
    echo
}

emit_transition_block() {
    local from_label="$1"
    local from_file="$2"
    local to_label="$3"
    local to_file="$4"

    echo "### ${from_label} → ${to_label}"
    echo

    if [[ -z "$from_file" || -z "$to_file" || ! -f "$from_file" || ! -f "$to_file" ]]; then
        echo "Transition cannot be evaluated because one or both artifacts are missing."
        echo
        return
    fi

    local from_rows to_rows from_ids to_ids
    from_rows=$(row_count "$from_file")
    to_rows=$(row_count "$to_file")
    from_ids=$(variant_id_count "$from_file")
    to_ids=$(variant_id_count "$to_file")

    echo "| Metric | ${from_label} | ${to_label} |"
    echo "|---|---:|---:|"
    echo "| rows | ${from_rows} | ${to_rows} |"
    echo "| columns | $(col_count "$from_file") | $(col_count "$to_file") |"
    echo "| distinct_variant_ids | ${from_ids} | ${to_ids} |"
    echo

    echo "Removed columns:"
    echo '```text'
    removed=$(field_diff_left_only "$from_file" "$to_file")
    [[ -n "$removed" ]] && echo "$removed" || echo "NONE"
    echo '```'
    echo

    echo "Added columns:"
    echo '```text'
    added=$(field_diff_right_only "$from_file" "$to_file")
    [[ -n "$added" ]] && echo "$added" || echo "NONE"
    echo '```'
    echo

    echo "Shared columns:"
    echo '```text'
    shared=$(field_shared "$from_file" "$to_file")
    [[ -n "$shared" ]] && echo "$shared" || echo "NONE"
    echo '```'
    echo
}

{
echo "# Stage07–Stage12 Lineage Forensics"
echo
echo "Generated: $(date -u +"%Y-%m-%dT%H:%M:%SZ")"
echo
echo "Purpose:"
echo
echo '```text'
echo "Audit row, variant_id, and column lineage from Stage07 through Stage12"
echo "across 12 epilepsy WES runs and 1 HG002 WGS run."
echo '```'
echo

while IFS=$'\t' read -r SAMPLE_ID RUN_ID DEPTH; do
    [[ "$SAMPLE_ID" == "sample_id" ]] && continue

    PROC="results/${RUN_ID}/processed"

    STAGE07="$(find_stage07 "$PROC")"
    S8_SELECTED="$PROC/stage_08_selected_transcript_consequences.tsv"
    S8_VDB="$PROC/stage_08_vdb_ready_variants.tsv"
    S8_CODING="$PROC/coding_candidates.tsv"
    S8_SPLICE="$PROC/splice_region_candidates.tsv"
    S8_NONCODING="$PROC/noncoding_candidates.tsv"
    S8_VARIANT_SUMMARY="$PROC/stage_08_variant_summary.tsv"
    S8_RDGP="$PROC/stage_08_rdgp_gene_evidence_seed.tsv"
    S9="$PROC/stage_09_coding_interpreted.tsv"
    S10="$PROC/stage_10_noncoding_interpreted.tsv"
    S11="$PROC/stage_11_prioritized_variants.tsv"
    S11_GENE_COUNTS="$PROC/stage_11_gene_variant_counts.tsv"
    S12="$PROC/stage_12_validation_candidates.tsv"

    echo "## ${SAMPLE_ID} / ${RUN_ID} / ${DEPTH}"
    echo

    if [[ ! -d "$PROC" ]]; then
        echo "Processed directory missing: \`$PROC\`"
        echo
        continue
    fi

    echo "# Artifact Inventory"
    echo

    emit_artifact_block "Stage07 annotated_variants.tsv" "$STAGE07"
    emit_artifact_block "Stage08 selected_transcript_consequences.tsv" "$S8_SELECTED"
    emit_artifact_block "Stage08 vdb_ready_variants.tsv" "$S8_VDB"
    emit_artifact_block "Stage08 coding_candidates.tsv" "$S8_CODING"
    emit_artifact_block "Stage08 splice_region_candidates.tsv" "$S8_SPLICE"
    emit_artifact_block "Stage08 noncoding_candidates.tsv" "$S8_NONCODING"
    emit_artifact_block "Stage08 variant_summary.tsv" "$S8_VARIANT_SUMMARY"
    emit_artifact_block "Stage08 rdgp_gene_evidence_seed.tsv" "$S8_RDGP"
    emit_artifact_block "Stage09 coding_interpreted.tsv" "$S9"
    emit_artifact_block "Stage10 noncoding_interpreted.tsv" "$S10"
    emit_artifact_block "Stage11 prioritized_variants.tsv" "$S11"
    emit_artifact_block "Stage11 gene_variant_counts.tsv" "$S11_GENE_COUNTS"
    emit_artifact_block "Stage12 validation_candidates.tsv" "$S12"

    echo "# Transition Lineage"
    echo

    emit_transition_block "Stage07 annotated" "$STAGE07" "Stage08 selected" "$S8_SELECTED"
    emit_transition_block "Stage08 selected" "$S8_SELECTED" "Stage08 VDB-ready" "$S8_VDB"
    emit_transition_block "Stage08 VDB-ready" "$S8_VDB" "Stage09 coding interpreted" "$S9"
    emit_transition_block "Stage08 VDB-ready" "$S8_VDB" "Stage10 noncoding interpreted" "$S10"
    emit_transition_block "Stage09 coding interpreted" "$S9" "Stage11 prioritized" "$S11"
    emit_transition_block "Stage10 noncoding interpreted" "$S10" "Stage11 prioritized" "$S11"
    emit_transition_block "Stage11 prioritized" "$S11" "Stage12 validation candidates" "$S12"

    echo "---"
    echo

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

echo "# Cross-Run Column First Appearance Map"
echo
echo "Generated from all available audited artifacts."
echo

TMP_COLUMNS=$(mktemp)
trap 'rm -f "$TMP_COLUMNS"' EXIT

while IFS=$'\t' read -r SAMPLE_ID RUN_ID DEPTH; do
    [[ "$SAMPLE_ID" == "sample_id" ]] && continue
    PROC="results/${RUN_ID}/processed"

    STAGE07="$(find_stage07 "$PROC")"
    FILES=(
        "stage07|$STAGE07"
        "stage08_selected|$PROC/stage_08_selected_transcript_consequences.tsv"
        "stage08_vdb|$PROC/stage_08_vdb_ready_variants.tsv"
        "stage08_coding|$PROC/coding_candidates.tsv"
        "stage08_splice|$PROC/splice_region_candidates.tsv"
        "stage08_noncoding|$PROC/noncoding_candidates.tsv"
        "stage08_variant_summary|$PROC/stage_08_variant_summary.tsv"
        "stage08_rdgp_seed|$PROC/stage_08_rdgp_gene_evidence_seed.tsv"
        "stage09|$PROC/stage_09_coding_interpreted.tsv"
        "stage10|$PROC/stage_10_noncoding_interpreted.tsv"
        "stage11|$PROC/stage_11_prioritized_variants.tsv"
        "stage11_gene_counts|$PROC/stage_11_gene_variant_counts.tsv"
        "stage12|$PROC/stage_12_validation_candidates.tsv"
    )

    for item in "${FILES[@]}"; do
        label="${item%%|*}"
        file="${item#*|}"
        [[ -f "$file" ]] || continue
        header_fields "$file" | awk -v sample="$SAMPLE_ID" -v run="$RUN_ID" -v label="$label" \
            '{print $0 "\t" label "\t" sample "\t" run}'
    done

done <<'EOF' > "$TMP_COLUMNS"
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

echo "| column | observed_surfaces |"
echo "|---|---|"
cut -f1 "$TMP_COLUMNS" | sort -u | while read -r col; do
    surfaces=$(awk -F'\t' -v c="$col" '$1 == c {print $2}' "$TMP_COLUMNS" | sort -u | paste -sd "," -)
    echo "| ${col} | ${surfaces} |"
done

} > "$OUT_FILE"

echo "Wrote:"
echo "  $OUT_FILE"