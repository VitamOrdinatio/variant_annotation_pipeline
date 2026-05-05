# rdgp_top_genes_by_rare_variant_burden

## Source

- Source file: `/mnt/storage/vap_runs/HG002/run_2026_04_17_082417/raw_mark_outputs/processed/stage_08_rdgp_gene_evidence_seed.tsv`
- Run ID: `run_2026_04_17_082417`
- Sample/Dataset: `HG002`

## Method

Artifacts are generated using a config-driven extraction system ("Artificer") and curated for clarity.

## Output

```text
=== Top 25 genes by rare_variant_count ===

rare_count  variant_count  gene_id          gene_symbol  max_severity  low_quality
270         767            ENSG00000183704  SLC9B1P1     LOW           False      
202         7094           ENSG00000078328  RBFOX1       MODIFIER      True       
194         503            ENSG00000167633  KIR3DL1      MODERATE      True       
188         2113           ENSG00000196126  HLA-DRB1     HIGH          True       
181         815            ENSG00000181143  MUC16        HIGH          False      
174         3473           ENSG00000185053  SGCZ         LOW           True       
173         563            ENSG00000259029  DUX4L18      MODIFIER      False      
168         1800           ENSG00000307923  NA           MODIFIER      False      
168         1500           ENSG00000198502  HLA-DRB5     HIGH          True       
166         287            ENSG00000258991  DUX4L19      MODIFIER      False      
146         8781           ENSG00000183117  CSMD1        MODERATE      True       
143         2288           ENSG00000178568  ERBB4        LOW           True       
133         403            ENSG00000291032  NA           MODIFIER      False      
129         444            ENSG00000125498  KIR2DL1      MODERATE      True       
125         962            ENSG00000100629  CEP128       MODERATE      True       
113         238            ENSG00000189013  KIR2DL4      HIGH          False      
112         1491           ENSG00000175161  CADM2        MODIFIER      True       
110         174            ENSG00000197249  SERPINA1     HIGH          True       
109         4577           ENSG00000174469  CNTNAP2      MODIFIER      True       
108         1111           ENSG00000230676  NA           LOW           False      
103         4738           ENSG00000153707  PTPRD        LOW           True       
99          2315           ENSG00000021645  NRXN3        MODERATE      True       
99          364            ENSG00000259154  DUX4L17      MODIFIER      False      
98          772            ENSG00000251629  LINC02241    MODIFIER      False      
98          762            ENSG00000184178  SCFD2        MODIFIER      False      
```

## Interpretation

Rare variants are distributed across many genes, with some enrichment in:

- large genes  
- highly variable genomic regions  

### Key Insight

> Rare variant burden is more informative than total variant count,
but still requires integration with functional and clinical data.

## Notes

- No additional notes.

## Limitations

- Excerpt or summary only.
- Not the full dataset unless explicitly stated.
- No new inference performed.
