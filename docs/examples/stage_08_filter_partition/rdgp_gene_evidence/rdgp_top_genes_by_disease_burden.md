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
' stage_08_rdgp_gene_evidence_seed.tsv | sort -k1,1nr | head -n 25 | awk -F'\t' 'BEGIN{print "variant_count\tgene_id\tgene_symbol\tmax_severity\tlow_quality"} {print}' | column -t -s $'\t' > docs/examples/rdgp_gene_evidence/rdgp_top_genes_by_disease_burden.md
```


## output:

```text
variant_count  gene_id  gene_symbol      max_severity  low_quality
8781           NA       CSMD1            MODERATE      True
7094           NA       RBFOX1           MODIFIER      True
4738           NA       PTPRD            LOW           True
4577           26047    CNTNAP2          MODIFIER      True
3963           NA       LRP1B            LOW           True
3473           NA       SGCZ             LOW           True
3452           NA       EYS              MODERATE      False
3371           NA       PCDH15           MODERATE      False
3249           51741    WWOX             MODERATE      True
3237           NA       CDH13            LOW           True
3236           NA       CNTN5            HIGH          True
3024           NA       CTNNA3           LOW           True
2981           2272     FHIT             LOW           True
2857           NA       MACROD2          LOW           True
2850           NA       MAGI2            LOW           True
2848           NA       ROBO2            MODIFIER      True
2754           5071     PRKN             MODERATE      True
2590           NA       DLG2             MODIFIER      True
2523           NA       PWRN1            LOW           False
2493           NA       PTPRN2           MODERATE      True
2456           NA       NAALADL2         MODERATE      True
2447           NA       LINC02055        MODIFIER      False
2388           NA       DCC              MODERATE      True
2383           NA       ENSG00000229618  MODIFIER      False
2382           NA       LSAMP            MODIFIER      True
```

Notes:

- `gene_id` may be NA for certain records due to mapping limitations or annotation source constraints.
- `low_quality` indicates presence of QC flags in contributing variants (e.g., caution flags from Stage 08).