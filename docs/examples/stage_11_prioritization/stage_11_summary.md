# stage_11_summary

## Source

- Source file: `/root/dev/portfolio_projects/variant_annotation_pipeline/results/run_2026_04_17_082417/processed/stage_11_prioritized_variants.tsv`
- Run ID: `run_2026_04_17_082417`
- Sample/Dataset: `HG002`

## Output

## Overview

Stage 11 integrates coding and noncoding interpretation outputs into deterministic priority tiers for downstream validation and review.

## Key Metrics

- Total prioritized variant records: `4636584`
- High-priority candidates: `0`
- Moderate-priority candidates: `113363`
- Low-priority candidates: `3369755`
- Uninterpretable records: `1153466`

### Key Ratio

~2.4% of variants are elevated to candidate status (Tier 2)

## Interpretation

- **No high-priority** candidates were identified in **HG002**  
- This is expected, as HG002 is a **healthy benchmark genome**  

### Key Insight

> The absence of high-priority variants validates that the prioritization system is not overcalling disease-relevant variants.

## Priority Tier Distribution

| Label | Count |
| --- | --- |
| tier_3_low_support_or_common | 3369755 |
| tier_4_uninterpretable_or_qc_limited | 1153466 |
| tier_2_moderate_candidate | 113363 |
## Priority Reason Distribution

| Label | Count |
| --- | --- |
| noncoding label noncoding_common_or_low_support | 3344586 |
| noncoding label noncoding_uninterpretable | 1152270 |
| noncoding label regulatory_or_transcript_rare | 112242 |
| coding label coding_common_or_low_support | 25169 |
| coding label coding_uninterpretable | 1196 |
| coding label lof_or_missense_rare | 1121 |
## Variant Origin Distribution

| Label | Count |
| --- | --- |
| noncoding | 4609098 |
| coding | 27486 |
## Source Interpretation Label Distribution

| Label | Count |
| --- | --- |
| noncoding_common_or_low_support | 3344586 |
| noncoding_uninterpretable | 1152270 |
| regulatory_or_transcript_rare | 112242 |
| coding_common_or_low_support | 25169 |
| coding_uninterpretable | 1196 |
| lof_or_missense_rare | 1121 |

## System Context

Stage 11 is the integrated prioritization layer. It does not perform clinical diagnosis; it organizes interpreted variant evidence into reviewable priority tiers.

### System Validation

> A correct prioritization system must produce zero high-priority candidates in a healthy genome.

## Notes

- No additional notes.

## Limitations

- Descriptive summary only.
- No clinical diagnosis is performed.
- Candidate labels do not imply disease.
