# rdgp_summary_counts

## Source

- Source file: `/mnt/storage/vap_runs/HG002/run_2026_04_17_082417/raw_mark_outputs/processed/stage_08_rdgp_gene_evidence_seed.tsv`
- Run ID: `run_2026_04_17_082417`
- Sample/Dataset: `HG002`

## Method

Artifacts are generated using a config-driven extraction system ("Artificer") and curated for clarity.

## Output

| metric | value |
| --- | --- |
| gene_rows | 50230 |
| summed_variant_count | 3528791 |
| summed_high_impact_variant_count | 791 |
| summed_rare_variant_count | 99427 |
| summed_pathogenic_variant_count | 66 |
| genes_with_max_HIGH | 614 |
| genes_with_low_quality_evidence | 10723 |

## Interpretation

- ~50k genes represented across the genome  
- ~3.5M variants aggregated at gene level  
- ~99k rare variants (~2.8% of total)  
- ~791 high-impact variants (extremely rare)  

### Key Insight

> Most genes accumulate many variants, but very few contain rare or high-impact variants.

This reflects expected genome-wide variation patterns and highlights the importance of filtering strategies.

### Important Note

These counts represent **raw aggregation**, not prioritization.

## Notes

- No additional notes.

## Limitations

- Excerpt or summary only.
- Not the full dataset unless explicitly stated.
- No new inference performed.
