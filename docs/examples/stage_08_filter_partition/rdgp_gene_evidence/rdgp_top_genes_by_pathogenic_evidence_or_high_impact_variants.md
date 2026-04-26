# rdgp_top_genes_by_pathogenic_evidence_or_high_impact_variants.md

## folder path:

`steelsparrow@pop-os:/mnt/storage/delme/stage_08_out_HG002_run$`


## bash cmd:

```bash
echo "=== Genes with pathogenic evidence or HIGH-impact variants, top 50 ==="
awk -F'\t' '
NR==1 {next}
($5 > 0 || $7 > 0) {
  print $7 "\t" $5 "\t" $6 "\t" $4 "\t" $2 "\t" $3 "\t" $8 "\t" $9
}
' stage_08_rdgp_gene_evidence_seed.tsv \
| sort -k1,1nr -k2,2nr -k3,3nr \
| head -n 50 \
| awk -F'\t' 'BEGIN{print "pathogenic_count\thigh_impact_count\trare_count\tvariant_count\tgene_id\tgene_symbol\tmax_severity\tlow_quality"} {print}' \
| column -t -s $'\t' > docs/examples/rdgp_gene_evidence/rdgp_top_genes_by_pathogenic_evidence_or_high_impact_variants.md
```

## output:

```text

=== Genes with pathogenic evidence or HIGH-impact variants, top 50 ===

pathogenic_count  high_impact_count  rare_count  variant_count  gene_id  gene_symbol      max_severity  low_quality
5                 0                  9           185            NA       MIR181A1HG       MODIFIER      False
3                 0                  0           11             NA       TBX6             LOW           False
2                 0                  75          1832           NA       ALK              MODERATE      True
2                 0                  4           110            NA       ITPKB            MODERATE      True
2                 0                  3           135            NA       WFS1             MODERATE      True
2                 0                  0           23             NA       CXCR1            MODERATE      False
2                 0                  0           3              NA       VKORC1           MODIFIER      False
1                 3                  47          431            NA       PRSS1            HIGH          True
1                 1                  3           173            NA       VDR              HIGH          True
1                 1                  0           47             NA       F11              HIGH          True
1                 0                  21          724            NA       KALRN            LOW           True
1                 0                  11          315            NA       AFF2             LOW           True
1                 0                  9           83             NA       MSH6             MODERATE      False
1                 0                  8           205            NA       ATP6V0A4         MODERATE      False
1                 0                  6           205            NA       SCN5A            MODERATE      True
1                 0                  6           347            NA       PRKCQ            MODERATE      True
1                 0                  5           160            NA       KIT              MODERATE      True
1                 0                  4           110            NA       USH1C            MODERATE      True
1                 0                  3           103            4864     NPC1             MODERATE      False
1                 0                  3           106            NA       ELP2             MODERATE      True
1                 0                  3           147            NA       GATA4            MODERATE      True
1                 0                  3           178            NA       SPTA1            MODERATE      True
1                 0                  3           17             NA       CCL2             LOW           True
1                 0                  3           23             NA       TP53             MODERATE      True
1                 0                  3           47             NA       C9ORF72          MODIFIER      True
1                 0                  3           70             NA       ABCA7            MODERATE      True
1                 0                  2           100            NA       NPHS2            MODERATE      True
1                 0                  2           26             NA       ENSG00000233953  MODIFIER      False
1                 0                  2           31             5190     PEX6             MODERATE      True
1                 0                  2           32             NA       GUCY2D           MODERATE      True
1                 0                  2           54             NA       APOB             MODERATE      False
1                 0                  1           143            5053     PAH              LOW           False
1                 0                  1           150            60528    ELAC2            MODERATE      True
1                 0                  1           18             NA       ADRA2A           MODIFIER      True
1                 0                  1           27             NA       APOA4            MODERATE      True
1                 0                  1           38             NA       SAA1             MODERATE      False
1                 0                  1           46             NA       NOD2             MODERATE      False
1                 0                  1           51             NA       TBX21            LOW           True
1                 0                  1           62             NA       FMO3             MODERATE      False
1                 0                  1           65             NA       CSRP3            LOW           True
1                 0                  0           14             NA       APOA2            MODIFIER      False
1                 0                  0           17             NA       APOE             MODERATE      False
1                 0                  0           20             NA       GHRL             MODERATE      True
1                 0                  0           20             NA       NOS3             MODERATE      False
1                 0                  0           20             NA       PLEKHN1          MODERATE      True
1                 0                  0           22             NA       ALAD             MODERATE      True
1                 0                  0           2              4519     MT-CYB           MODERATE      False
1                 0                  0           24             NA       CCR5             MODIFIER      True
1                 0                  0           28             5621     PRNP             MODERATE      False
1                 0                  0           33             NA       CYBA             MODERATE      True
```

Notes:

- `gene_id` may be NA for certain records due to mapping limitations or annotation source constraints.
- `low_quality` indicates presence of QC flags in contributing variants (e.g., caution flags from Stage 08).