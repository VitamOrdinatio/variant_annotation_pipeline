# rdgp_top_genes_by_disease_burden.md

HG002 is a benchmark genome (GIAB) and not a disease case; these outputs represent variant burden distributions, not clinical diagnoses.

## folder path:

`steelsparrow@pop-os:/mnt/storage/delme/stage_08_out_HG002_run$`

## bash cmd:

```bash
awk -F'\t' '
NR==1 {next}
{
  print $4 "\t" $2 "\t" $3 "\t" $8 "\t" $9
}
' stage_08_rdgp_gene_evidence_seed.tsv | sort -k1,1nr | head -n 25 | awk -F'\t' 'BEGIN{print "variant_count\tgene_id\tgene_symbol\tmax_severity\tlow_quality"} {print}' | column -t -s $'\t' > docs/examples/stage_08_filter_partition/rdgp_gene_evidence/rdgp_top_genes_by_disease_burden.md
```


## output:

```text
variant_count  gene_id          gene_symbol  max_severity  low_quality
8781           ENSG00000183117  CSMD1        MODERATE      True
7094           ENSG00000078328  RBFOX1       MODIFIER      True
4738           ENSG00000153707  PTPRD        LOW           True
4577           ENSG00000174469  CNTNAP2      MODIFIER      True
3963           ENSG00000168702  LRP1B        LOW           True
3473           ENSG00000185053  SGCZ         LOW           True
3452           ENSG00000188107  EYS          MODERATE      False
3371           ENSG00000150275  PCDH15       MODERATE      False
3249           ENSG00000186153  WWOX         MODERATE      True
3237           ENSG00000140945  CDH13        LOW           True
3236           ENSG00000149972  CNTN5        HIGH          True
3024           ENSG00000183230  CTNNA3       LOW           True
2981           ENSG00000189283  FHIT         LOW           True
2857           ENSG00000172264  MACROD2      LOW           True
2850           ENSG00000187391  MAGI2        LOW           True
2848           ENSG00000185008  ROBO2        MODIFIER      True
2754           ENSG00000185345  PRKN         MODERATE      True
2590           ENSG00000150672  DLG2         MODIFIER      True
2523           ENSG00000259905  PWRN1        LOW           False
2493           ENSG00000155093  PTPRN2       MODERATE      True
2456           ENSG00000177694  NAALADL2     MODERATE      True
2447           ENSG00000254101  LINC02055    MODIFIER      False
2388           ENSG00000187323  DCC          MODERATE      True
2383           ENSG00000229618  NA           MODIFIER      False
2382           ENSG00000185565  LSAMP        MODIFIER      True

```

Notes:

- `low_quality` indicates presence of QC flags in contributing variants (e.g., caution flags from Stage 08).