# rdgp_seed_overview

## Source

- Source file: `/mnt/storage/vap_runs/HG002/run_2026_04_17_082417/raw_mark_outputs/processed/stage_08_rdgp_gene_evidence_seed.tsv`
- Run ID: `run_2026_04_17_082417`
- Sample/Dataset: `HG002`

## Method

Artifacts are generated using a config-driven extraction system ("Artificer") and curated for clarity.

## Output

| sample_id | gene_id | gene_symbol | variant_count | high_impact_variant_count | rare_variant_count | pathogenic_variant_count | max_variant_severity | has_low_quality_evidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| HG002 | ENSG00000000003 | TSPAN6 | 4 | 0 | 1 | 0 | MODIFIER | True |
| HG002 | ENSG00000000005 | TNMD | 11 | 0 | 0 | 0 | MODIFIER | True |
| HG002 | ENSG00000000419 | DPM1 | 5 | 0 | 0 | 0 | MODIFIER | False |
| HG002 | ENSG00000000457 | SCYL3 | 102 | 0 | 1 | 0 | LOW | False |
| HG002 | ENSG00000000460 | FIRRM | 375 | 0 | 2 | 0 | MODERATE | True |

## Interpretation

Representative gene-level records demonstrate:

- aggregation of multiple variants per gene  
- separation of:
  - total variant burden  
  - rare variant burden  
  - high-impact variant burden  

### Key Insight

> Gene-level evidence is multi-dimensional, not a single score.

This structure enables flexible prioritization strategies in downstream analysis.

## Notes

- No additional notes.

## Limitations

- Excerpt or summary only.
- Not the full dataset unless explicitly stated.
- No new inference performed.
