# rdgp_top_genes_by_rare_variant_burden.md


## folder path:

`steelsparrow@pop-os:/mnt/storage/delme/stage_08_out_HG002_run$`


## bash cmd:

echo "=== Top 25 genes by rare_variant_count ==="
awk -F'\t' '
NR==1 {next}
$6 > 0 {
  print $6 "\t" $4 "\t" $2 "\t" $3 "\t" $8 "\t" $9
}
' stage_08_rdgp_gene_evidence_seed.tsv \
| sort -k1,1nr -k2,2nr \
| head -n 25 \
| awk -F'\t' 'BEGIN{print "rare_count\tvariant_count\tgene_id\tgene_symbol\tmax_severity\tlow_quality"} {print}' \
| column -t -s $'\t' > docs/examples/rdgp_gene_evidence/rdgp_top_genes_by_rare_variant_burden.md


## output:

```text

=== Top 25 genes by rare_variant_count ===

rare_count  variant_count  gene_id  gene_symbol      max_severity  low_quality
270         767            NA       SLC9B1P1         LOW           False
202         7094           NA       RBFOX1           MODIFIER      True
194         503            NA       KIR3DL1          MODERATE      True
188         2113           NA       HLA-DRB1         HIGH          True
181         815            NA       MUC16            HIGH          False
174         3473           NA       SGCZ             LOW           True
173         563            NA       DUX4L18          MODIFIER      False
168         1800           NA       ENSG00000307923  MODIFIER      False
168         1500           NA       HLA-DRB5         HIGH          True
166         287            NA       DUX4L19          MODIFIER      False
146         8781           NA       CSMD1            MODERATE      True
143         2288           NA       ERBB4            LOW           True
133         403            NA       ENSG00000291032  MODIFIER      False
129         444            NA       KIR2DL1          MODERATE      True
125         962            NA       CEP128           MODERATE      True
113         238            NA       KIR2DL4          HIGH          False
112         1491           NA       CADM2            MODIFIER      True
110         174            NA       SERPINA1         HIGH          True
109         4577           26047    CNTNAP2          MODIFIER      True
108         1111           NA       ENSG00000230676  LOW           False
103         4738           NA       PTPRD            LOW           True
99          2315           NA       NRXN3            MODERATE      True
99          364            NA       DUX4L17          MODIFIER      False
98          772            NA       LINC02241        MODIFIER      False
98          762            NA       SCFD2            MODIFIER      False
```

Notes:

- `gene_id` may be NA for certain records due to mapping limitations or annotation source constraints.
- `low_quality` indicates presence of QC flags in contributing variants (e.g., caution flags from Stage 08).