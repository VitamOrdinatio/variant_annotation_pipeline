# stage_11_priority_tier_distribution

## Source

- Source file: `/root/dev/portfolio_projects/variant_annotation_pipeline/results/run_2026_04_17_082417/processed/stage_11_prioritized_variants.tsv`
- Run ID: `run_2026_04_17_082417`
- Sample/Dataset: `HG002`

## Output

| value | count |
| --- | --- |
| tier_3_low_support_or_common | 3369755 |
| tier_4_uninterpretable_or_qc_limited | 1153466 |
| tier_2_moderate_candidate | 113363 |

> Tier 2 candidates represent a manageable subset for downstream review.

## Interpretation

- Tier 2 (~113k): candidate variants for further review  
- Tier 3 (~3.3M): common or low-support variants  
- Tier 4 (~1.15M): uninterpretable or annotation-limited variants  

### Key Insight

> Only ~2.4% of variants are elevated to candidate status, reflecting effective filtering and prioritization.

## Notes

- No additional notes.

## Limitations

- Excerpt or summary only.
- Not the full dataset unless explicitly stated.
- No new inference performed.
