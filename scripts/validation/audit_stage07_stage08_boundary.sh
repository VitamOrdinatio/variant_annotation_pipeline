#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="${REPO_ROOT:-$HOME/dev/portfolio_projects/variant_annotation_pipeline}"
OUT_DIR="${OUT_DIR:-/root/Desktop}"
OUT_TSV="$OUT_DIR/stage07_stage08_boundary_audit.tsv"
OUT_MD="$OUT_DIR/stage07_stage08_boundary_audit_summary.md"

cd "$REPO_ROOT"

row_count() {
  local file="$1"
  if [[ ! -f "$file" ]]; then
    echo "NA"
    return
  fi
  awk 'END {print NR > 0 ? NR - 1 : 0}' "$file"
}

col_count() {
  local file="$1"
  if [[ ! -f "$file" ]]; then
    echo "NA"
    return
  fi
  head -n 1 "$file" | awk -F'\t' '{print NF}'
}

header_fields() {
  local file="$1"
  if [[ ! -f "$file" ]]; then
    echo ""
    return
  fi
  head -n 1 "$file" | tr '\t' '\n'
}

field_diff() {
  local left="$1"
  local right="$2"
  comm -23 \
    <(header_fields "$left" | sort -u) \
    <(header_fields "$right" | sort -u) \
    | paste -sd "," -
}

field_added() {
  local left="$1"
  local right="$2"
  comm -13 \
    <(header_fields "$left" | sort -u) \
    <(header_fields "$right" | sort -u) \
    | paste -sd "," -
}

printf "sample_id\trun_id\tdepth_category\tstage07_tsv\tstage08_selected_tsv\tstage08_vdb_tsv\tstage07_rows\tstage08_selected_rows\tstage08_vdb_rows\tstage07_cols\tstage08_selected_cols\tstage08_vdb_cols\tselected_ratio\tvdb_ratio\trow_preserving_selected\trow_preserving_vdb\tlost_fields_selected\tlost_fields_vdb\tadded_fields_selected\tadded_fields_vdb\n" > "$OUT_TSV"

while IFS=$'\t' read -r sample_id run_id depth_category; do
  [[ "$sample_id" == "sample_id" ]] && continue

  processed="results/${run_id}/processed"

  stage07_tsv="${processed}/${sample_id}_${run_id}.annotated_variants.tsv"
  stage08_selected="${processed}/stage_08_selected_transcript_consequences.tsv"
  stage08_vdb="${processed}/stage_08_vdb_ready_variants.tsv"

  s7_rows=$(row_count "$stage07_tsv")
  s8_selected_rows=$(row_count "$stage08_selected")
  s8_vdb_rows=$(row_count "$stage08_vdb")

  s7_cols=$(col_count "$stage07_tsv")
  s8_selected_cols=$(col_count "$stage08_selected")
  s8_vdb_cols=$(col_count "$stage08_vdb")

  if [[ "$s7_rows" != "NA" && "$s7_rows" -gt 0 && "$s8_selected_rows" != "NA" ]]; then
    selected_ratio=$(awk -v a="$s8_selected_rows" -v b="$s7_rows" 'BEGIN {printf "%.10f", a/b}')
  else
    selected_ratio="NA"
  fi

  if [[ "$s7_rows" != "NA" && "$s7_rows" -gt 0 && "$s8_vdb_rows" != "NA" ]]; then
    vdb_ratio=$(awk -v a="$s8_vdb_rows" -v b="$s7_rows" 'BEGIN {printf "%.10f", a/b}')
  else
    vdb_ratio="NA"
  fi

  row_preserving_selected="False"
  row_preserving_vdb="False"
  [[ "$s7_rows" == "$s8_selected_rows" ]] && row_preserving_selected="True"
  [[ "$s7_rows" == "$s8_vdb_rows" ]] && row_preserving_vdb="True"

  lost_selected=$(field_diff "$stage07_tsv" "$stage08_selected")
  lost_vdb=$(field_diff "$stage07_tsv" "$stage08_vdb")
  added_selected=$(field_added "$stage07_tsv" "$stage08_selected")
  added_vdb=$(field_added "$stage07_tsv" "$stage08_vdb")

  [[ -z "$lost_selected" ]] && lost_selected="NONE"
  [[ -z "$lost_vdb" ]] && lost_vdb="NONE"
  [[ -z "$added_selected" ]] && added_selected="NONE"
  [[ -z "$added_vdb" ]] && added_vdb="NONE"

  printf "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" \
    "$sample_id" "$run_id" "$depth_category" \
    "$stage07_tsv" "$stage08_selected" "$stage08_vdb" \
    "$s7_rows" "$s8_selected_rows" "$s8_vdb_rows" \
    "$s7_cols" "$s8_selected_cols" "$s8_vdb_cols" \
    "$selected_ratio" "$vdb_ratio" \
    "$row_preserving_selected" "$row_preserving_vdb" \
    "$lost_selected" "$lost_vdb" "$added_selected" "$added_vdb" \
    >> "$OUT_TSV"

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
HG002	run_2026_06_03_010030	hg002
EOF

{
  echo "# Stage 07 / Stage 08 Boundary Audit"
  echo
  echo "Generated: $(date -u +"%Y-%m-%dT%H:%M:%SZ")"
  echo
  echo "TSV: $OUT_TSV"
  echo
  echo "## Row preservation summary"
  echo
  awk -F'\t' '
    NR > 1 {
      total++;
      if ($15 == "True") selected++;
      if ($16 == "True") vdb++;
      if ($17 != "NONE") lost_selected++;
      if ($18 != "NONE") lost_vdb++;
    }
    END {
      print "- total_runs: " total;
      print "- stage08_selected_row_preserving_runs: " selected;
      print "- stage08_vdb_row_preserving_runs: " vdb;
      print "- runs_with_lost_fields_selected: " lost_selected + 0;
      print "- runs_with_lost_fields_vdb: " lost_vdb + 0;
    }
  ' "$OUT_TSV"
  echo
  echo "## Per-run compact view"
  echo
  echo "| sample_id | run_id | depth | stage07_rows | stage08_selected_rows | stage08_vdb_rows | selected_ratio | vdb_ratio | selected_preserving | vdb_preserving |"
  echo "|---|---|---:|---:|---:|---:|---:|---:|---|---|"
  awk -F'\t' '
    NR > 1 {
      printf "| %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |\n", $1,$2,$3,$7,$8,$9,$13,$14,$15,$16
    }
  ' "$OUT_TSV"
} > "$OUT_MD"

echo "Wrote:"
echo "  $OUT_TSV"
echo "  $OUT_MD"