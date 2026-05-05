# rdgp_top_genes_by_disease_burden

## Source

- Source file: `/mnt/storage/vap_runs/HG002/run_2026_04_17_082417/raw_mark_outputs/processed/stage_08_rdgp_gene_evidence_seed.tsv`
- Run ID: `run_2026_04_17_082417`
- Sample/Dataset: `HG002`

## Method

Artifacts are generated using a config-driven extraction system ("Artificer") and curated for clarity.

## Output

```text
=== Top 25 genes by variant_count ===

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

## Interpretation

Genes with high total variant counts often:

- have large genomic size  
- contain many noncoding regions  
- act as mutation "sinks"  

### Key Insight

> High variant burden does NOT imply disease relevance.

These rankings reflect genomic architecture, not biological importance.

## Notes

- No additional notes.

## Limitations

- Excerpt or summary only.
- Not the full dataset unless explicitly stated.
- No new inference performed.
