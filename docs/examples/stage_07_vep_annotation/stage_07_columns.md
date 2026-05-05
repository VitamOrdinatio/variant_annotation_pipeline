# stage_07_columns

## Source

- Source file: `/mnt/storage/vap_runs/HG002/run_2026_04_17_082417/raw_mark_outputs/processed/HG002_run_2026_04_17_082417.annotated_variants.tsv`
- Run ID: `run_2026_04_17_082417`
- Sample/Dataset: `HG002`

## Method

Artifacts are generated using a config-driven extraction system ("Artificer") and curated for clarity.

## Output

| index | column |
| --- | --- |
| 1 | sample_id |
| 2 | run_id |
| 3 | source_pipeline |
| 4 | variant_id |
| 5 | chromosome |
| 6 | position |
| 7 | reference_allele |
| 8 | alternate_allele |
| 9 | quality_flag |
| 10 | gene_id |
| 11 | gene_symbol |
| 12 | transcript_id |
| 13 | consequence |
| 14 | impact_class |
| 15 | impact |
| 16 | variant_class |
| 17 | variant_type |
| 18 | clinical_significance |
| 19 | clinvar_significance |
| 20 | population_frequency |
| 21 | gnomad_af |
| 22 | exac_af |
| 23 | thousand_genomes_af |
| 24 | mito_flag |
| 25 | epilepsy_flag |

## Interpretation

This schema defines the structured representation of annotated variants used throughout downstream stages (Stage 08–13).

Key features:

- integration of gene, transcript, and consequence annotations  
- inclusion of population frequency data (gnomAD, ExAC, 1000G)  
- support for downstream filtering (impact_class, variant_type)  
- flags enabling disease-focused analysis (mito_flag, epilepsy_flag)  

## Notes

- No additional notes.

## Limitations

- Excerpt or summary only.
- Not the full dataset unless explicitly stated.
- No new inference performed.
