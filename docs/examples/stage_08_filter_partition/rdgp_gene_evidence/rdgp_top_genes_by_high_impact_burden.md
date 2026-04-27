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
| column -t -s $'\t' > docs/examples/stage_08_filter_partition/rdgp_gene_evidence/rdgp_top_genes_by_high_impact_burden.md
```

## output:

```text

=== Top 25 genes by high_impact_variant_count ===

high_impact_count  variant_count  gene_id          gene_symbol  max_severity  low_quality
18                 1198           ENSG00000169894  MUC3A        HIGH          True
11                 526            ENSG00000205592  MUC19        HIGH          True
10                 1115           ENSG00000227124  ZNF717       HIGH          True
9                  1500           ENSG00000198502  HLA-DRB5     HIGH          True
8                  523            ENSG00000275395  FCGBP        HIGH          False
7                  2113           ENSG00000196126  HLA-DRB1     HIGH          True
7                  815            ENSG00000181143  MUC16        HIGH          False
6                  812            ENSG00000174501  ANKRD36C     HIGH          True
6                  366            ENSG00000234745  HLA-B        HIGH          True
6                  125            ENSG00000172199  OR8U1        HIGH          False
6                  80             ENSG00000151846  PABPC3       HIGH          True
5                  629            ENSG00000166473  PKD1L2       HIGH          False
5                  174            ENSG00000197249  SERPINA1     HIGH          True
4                  252            ENSG00000060237  WNK1         HIGH          True
4                  238            ENSG00000189013  KIR2DL4      HIGH          False
4                  152            ENSG00000104972  LILRB1       HIGH          True
4                  78             ENSG00000205702  CYP2D7       HIGH          True
3                  1090           ENSG00000179344  HLA-DQB1     HIGH          True
3                  696            ENSG00000135976  ANKRD36      HIGH          False
3                  431            ENSG00000204983  PRSS1        HIGH          True
3                  307            ENSG00000276950  GSTT4        HIGH          True
3                  178            ENSG00000184956  MUC6         HIGH          False
3                  144            ENSG00000237702  TRBV3-1      HIGH          True
3                  83             ENSG00000174450  GOLGA6L2     HIGH          True
3                  71             ENSG00000176092  CRYBG2       HIGH          False
```

Notes:

- `low_quality` indicates presence of QC flags in contributing variants (e.g., caution flags from Stage 08).