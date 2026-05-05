# Stage 13 Summary

Final run-level summary for VAP Stage 13.

## Source

- Source file: `/mnt/storage/vap_runs/HG002/run_2026_04_17_082417/raw_mark_outputs/processed/stage_13_final_summary.json`
- Run ID: `run_2026_04_17_082417`
- Sample/Dataset: `HG002`

## Output

### Key run metrics

- `run_id`: `run_2026_04_17_082417`
- `sample_id`: `HG002`
- `source_pipeline`: `variant_annotation_pipeline`
- `total_variants_processed`: `4636584`
- `prioritized_variant_count`: `4636584`
- `variants_evaluated_for_validation`: `4636584`
- `validation_required_count`: `113363`
- `gene_id_count_unique`: `50231`
- `high_priority_candidate_count`: `0`
- `moderate_priority_candidate_count`: `113363`
- `low_priority_candidate_count`: `3369755`
- `uninterpretable_count`: `1153466`

### Priority tier distribution

| priority_tier | count |
| --- | --- |
| tier_2_moderate_candidate | 113363 |
| tier_3_low_support_or_common | 3369755 |
| tier_4_uninterpretable_or_qc_limited | 1153466 |

### Validation-required distribution

| validation_required | count |
| --- | --- |
| False | 4523221 |
| True | 113363 |

### Top gene variant counts

| gene_id | variant_count |
| --- | --- |
| NA | 1107793 |
| ENSG00000183117 | 8781 |
| ENSG00000078328 | 7094 |
| ENSG00000153707 | 4738 |
| ENSG00000174469 | 4577 |
| ENSG00000168702 | 3963 |
| ENSG00000185053 | 3473 |
| ENSG00000188107 | 3452 |
| ENSG00000150275 | 3371 |
| ENSG00000186153 | 3249 |

## Interpretation

This summary consolidates the full VAP pipeline output and reflects system behavior across prioritization (Stage 11) and validation (Stage 12).

### Key Observations

- All variants were processed and assigned a priority tier
- No high-priority variants were identified
- Tier 2 variants (~2.4%) were consistently selected for validation
- The majority of variants were classified as low-support or uninterpretable

### System Insight

> The pipeline demonstrates controlled prioritization and validation, avoiding overrepresentation of weak or common signals.

### Biological Context

The observed distribution is consistent with expectations for a healthy genome, where:

- rare coding variants are present but not disease-causing
- most variants are common or noncoding
- high-confidence pathogenic signals are absent

### Bottom Line

> Stage 13 confirms that upstream prioritization and validation stages operate coherently and produce biologically plausible results.

## Limitations

- This summary consolidates upstream results and does not introduce new interpretation.
- Gene counts are descriptive only and are not RDGP ranking.
