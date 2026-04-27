# rdgp_summary_counts_only.md

## folder path:

``steelsparrow@pop-os:/mnt/storage/delme/stage_08_out_HG002_run$``


## bash cmd:
```bash
echo "=== RDGP seed summary ==="
awk -F'\t' '
NR>1 {
  genes++
  variants += $4
  high += $5
  rare += $6
  pathogenic += $7
  if ($8=="HIGH") high_genes++
  if ($9=="True") lowq_genes++
}
END {
  print "gene_rows\t" genes
  print "summed_variant_count\t" variants
  print "summed_high_impact_variant_count\t" high
  print "summed_rare_variant_count\t" rare
  print "summed_pathogenic_variant_count\t" pathogenic
  print "genes_with_max_HIGH\t" high_genes
  print "genes_with_low_quality_evidence\t" lowq_genes
}
' stage_08_rdgp_gene_evidence_seed.tsv | column -t -s $'\t' > docs/examples/stage_08_filter_partition/rdgp_gene_evidence/rdgp_summary_counts_only.md
```

## output:


```text

=== RDGP seed summary ===

gene_rows                         50230
summed_variant_count              3528791
summed_high_impact_variant_count  791
summed_rare_variant_count         99427
summed_pathogenic_variant_count   66
genes_with_max_HIGH               614
genes_with_low_quality_evidence   10723
```

Notes:

- `low_quality` indicates presence of QC flags in contributing variants (e.g., caution flags from Stage 08).