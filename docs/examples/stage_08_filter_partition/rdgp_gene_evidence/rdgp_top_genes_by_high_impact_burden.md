# rdgp_top_genes_by_high_impact_burden.md


## folder path:

`steelsparrow@pop-os:/mnt/storage/delme/stage_08_out_HG002_run$`


## bash cmd:

```bash
echo "=== Top 25 genes by high_impact_variant_count ==="
awk -F'\t' '
NR==1 {next}
$5 > 0 {
  print $5 "\t" $4 "\t" $2 "\t" $3 "\t" $8 "\t" $9
}
' stage_08_rdgp_gene_evidence_seed.tsv \
| sort -k1,1nr -k2,2nr \
| head -n 25 \
| awk -F'\t' 'BEGIN{print "high_impact_count\tvariant_count\tgene_id\tgene_symbol\tmax_severity\tlow_quality"} {print}' \
| column -t -s $'\t' > docs/examples/rdgp_gene_evidence/rdgp_top_genes_by_high_impact_burden.md
```

## output:

```text

=== Top 25 genes by high_impact_variant_count ===

high_impact_count  variant_count  gene_id  gene_symbol  max_severity  low_quality
18                 1198           NA       MUC3A        HIGH          True
11                 526            NA       MUC19        HIGH          True
10                 1115           NA       ZNF717       HIGH          True
9                  1500           NA       HLA-DRB5     HIGH          True
8                  523            NA       FCGBP        HIGH          False
7                  2113           NA       HLA-DRB1     HIGH          True
7                  815            NA       MUC16        HIGH          False
6                  812            NA       ANKRD36C     HIGH          True
6                  366            NA       HLA-B        HIGH          True
6                  125            NA       OR8U1        HIGH          False
6                  80             NA       PABPC3       HIGH          True
5                  629            NA       PKD1L2       HIGH          False
5                  174            NA       SERPINA1     HIGH          True
4                  252            NA       WNK1         HIGH          True
4                  238            NA       KIR2DL4      HIGH          False
4                  152            NA       LILRB1       HIGH          True
4                  78             NA       CYP2D7       HIGH          True
3                  1090           NA       HLA-DQB1     HIGH          True
3                  696            NA       ANKRD36      HIGH          False
3                  431            NA       PRSS1        HIGH          True
3                  307            NA       GSTT4        HIGH          True
3                  178            NA       MUC6         HIGH          False
3                  144            NA       TRBV3-1      HIGH          True
3                  83             NA       GOLGA6L2     HIGH          True
3                  71             NA       CRYBG2       HIGH          False
```

Notes:

- `gene_id` may be NA for certain records due to mapping limitations or annotation source constraints.
- `low_quality` indicates presence of QC flags in contributing variants (e.g., caution flags from Stage 08).