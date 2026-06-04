#!/usr/bin/env bash
set -euo pipefail

# Use this script to extract the stage funnel metrics from the long format files and
# create a single long format file with all runs. The output file will have columns: 
# run_id, metric_name, stage_funnel_summary_col_name, metric_value. 
#
# The stage_funnel_summary_col_name is a more human-readable name for the metric, 
# which can be used in the stage funnel summary table. The mapping from metric_name 
# to stage_funnel_summary_col_name is defined in the awk script below.

# Example usage:

# Make sure to run this script from the root of the project, and that the results directory is in place.
# Make sure to have the necessary permissions to read the input files and write the output file.

# ./extract_stage_funnel_long.sh


out="stage_funnel_extracted_long.tsv"

printf "run_id\tmetric_name\tstage_funnel_summary_col_name\tmetric_value\n" > "$out"

for f in results/run_2026_*/metrics/stage_metrics_long.tsv; do
  run_id="$(basename "$(dirname "$(dirname "$f")")")"

  awk -F'\t' -v OFS='\t' -v run_id="$run_id" '
  BEGIN {
    map["raw_called_variants"]="raw_variant_count"
    map["normalized_variants"]="normalized_variant_count"
    map["annotated_variants_vcf"]="annotated_variant_count"
    map["annotated_variants_tsv"]="stage08_total_variants"
    map["rdgp_gene_evidence_seed_rows"]="rdgp_gene_evidence_seed_rows"
    map["coding_candidates"]="coding_candidates"
    map["noncoding_candidates"]="noncoding_candidates"
    map["qc_flagged"]="qc_flagged"
    map["splice_region_candidates"]="splice_region_candidates"
    map["coding_interpreted_rows"]="stage09_coding_interpreted"
    map["noncoding_interpreted_rows"]="stage10_noncoding_interpreted"
    map["prioritized_variants_rows"]="stage11_prioritized_rows"
    map["gene_variant_counts_rows"]="unique_gene_ids"
    map["validation_candidates_rows"]="stage12_validation_rows"
  }
  NR==1 {
    for (i=1; i<=NF; i++) h[$i]=i
    next
  }
  ($h["metric_name"] in map) {
    print run_id, $h["metric_name"], map[$h["metric_name"]], $h["metric_value"]
  }
  ' "$f" >> "$out"
done

echo "Wrote: $out"
