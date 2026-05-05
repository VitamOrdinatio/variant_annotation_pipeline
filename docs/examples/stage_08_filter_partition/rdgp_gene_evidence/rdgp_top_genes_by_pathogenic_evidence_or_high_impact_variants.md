# rdgp_top_genes_by_pathogenic_evidence_or_high_impact_variants

## Source

- Source file: `/mnt/storage/vap_runs/HG002/run_2026_04_17_082417/raw_mark_outputs/processed/stage_08_rdgp_gene_evidence_seed.tsv`
- Run ID: `run_2026_04_17_082417`
- Sample/Dataset: `HG002`

## Method

Artifacts are generated using a config-driven extraction system ("Artificer") and curated for clarity.

## Output

```text
=== Genes with pathogenic evidence or HIGH-impact variants, top 50 ===

pathogenic_count  high_impact_count  rare_count  variant_count  gene_id          gene_symbol  max_severity  low_quality
5                 0                  9           185            ENSG00000229989  MIR181A1HG   MODIFIER      False      
3                 0                  0           11             ENSG00000149922  TBX6         LOW           False      
2                 0                  75          1832           ENSG00000171094  ALK          MODERATE      True       
2                 0                  4           110            ENSG00000143772  ITPKB        MODERATE      True       
2                 0                  3           135            ENSG00000109501  WFS1         MODERATE      True       
2                 0                  0           23             ENSG00000163464  CXCR1        MODERATE      False      
2                 0                  0           3              ENSG00000167397  VKORC1       MODIFIER      False      
1                 3                  47          431            ENSG00000204983  PRSS1        HIGH          True       
1                 1                  3           173            ENSG00000111424  VDR          HIGH          True       
1                 1                  0           47             ENSG00000088926  F11          HIGH          True       
1                 0                  21          724            ENSG00000160145  KALRN        LOW           True       
1                 0                  11          315            ENSG00000155966  AFF2         LOW           True       
1                 0                  9           83             ENSG00000116062  MSH6         MODERATE      False      
1                 0                  8           205            ENSG00000105929  ATP6V0A4     MODERATE      False      
1                 0                  6           347            ENSG00000065675  PRKCQ        MODERATE      True       
1                 0                  6           205            ENSG00000183873  SCN5A        MODERATE      True       
1                 0                  5           160            ENSG00000157404  KIT          MODERATE      True       
1                 0                  4           110            ENSG00000006611  USH1C        MODERATE      True       
1                 0                  3           70             ENSG00000064687  ABCA7        MODERATE      True       
1                 0                  3           17             ENSG00000108691  CCL2         LOW           True       
1                 0                  3           106            ENSG00000134759  ELP2         MODERATE      True       
1                 0                  3           147            ENSG00000136574  GATA4        MODERATE      True       
1                 0                  3           103            ENSG00000141458  NPC1         MODERATE      False      
1                 0                  3           23             ENSG00000141510  TP53         MODERATE      True       
1                 0                  3           47             ENSG00000147894  C9ORF72      MODIFIER      True       
1                 0                  3           178            ENSG00000163554  SPTA1        MODERATE      True       
1                 0                  2           54             ENSG00000084674  APOB         MODERATE      False      
1                 0                  2           100            ENSG00000116218  NPHS2        MODERATE      True       
1                 0                  2           31             ENSG00000124587  PEX6         MODERATE      True       
1                 0                  2           32             ENSG00000132518  GUCY2D       MODERATE      True       
1                 0                  2           26             ENSG00000233953  NA           MODIFIER      False      
1                 0                  1           150            ENSG00000006744  ELAC2        MODERATE      True       
1                 0                  1           62             ENSG00000007933  FMO3         MODERATE      False      
1                 0                  1           51             ENSG00000073861  TBX21        LOW           True       
1                 0                  1           27             ENSG00000110244  APOA4        MODERATE      True       
1                 0                  1           65             ENSG00000129170  CSRP3        LOW           True       
1                 0                  1           18             ENSG00000150594  ADRA2A       MODIFIER      True       
1                 0                  1           46             ENSG00000167207  NOD2         MODERATE      False      
1                 0                  1           143            ENSG00000171759  PAH          LOW           False      
1                 0                  1           38             ENSG00000173432  SAA1         MODERATE      False      
1                 0                  0           33             ENSG00000051523  CYBA         MODERATE      True       
1                 0                  0           3              ENSG00000116014  KISS1R       MODERATE      False      
1                 0                  0           17             ENSG00000130203  APOE         MODERATE      False      
1                 0                  0           22             ENSG00000148218  ALAD         MODERATE      True       
1                 0                  0           20             ENSG00000157017  GHRL         MODERATE      True       
1                 0                  0           43             ENSG00000157895  C12ORF43     LOW           True       
1                 0                  0           14             ENSG00000158874  APOA2        MODIFIER      False      
1                 0                  0           24             ENSG00000160791  CCR5         MODIFIER      True       
1                 0                  0           77             ENSG00000162747  FCGR3B       MODERATE      True       
1                 0                  0           20             ENSG00000164867  NOS3         MODERATE      False      
```

## Interpretation

Genes with pathogenic annotations or high-impact variants include well-known disease-associated genes (e.g., TP53, SCN5A, NPC1).

### Key Insight

> Presence of pathogenic annotations in a healthy genome reflects:

- benign or low-penetrance variants  
- database annotation limitations  
- context-dependent pathogenicity  

This demonstrates that:

- clinical annotation alone is insufficient  
- interpretation requires phenotype context  

These results are NOT indicative of disease in HG002.

## Notes

- No additional notes.

## Limitations

- Excerpt or summary only.
- Not the full dataset unless explicitly stated.
- No new inference performed.
