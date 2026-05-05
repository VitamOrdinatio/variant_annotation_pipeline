# stage_09_summary

## Source

- Source file: `/root/dev/portfolio_projects/variant_annotation_pipeline/results/run_2026_04_17_082417/processed/stage_09_coding_interpreted.tsv`
- Run ID: `run_2026_04_17_082417`
- Sample/Dataset: `HG002`

## Method

Artifacts are generated using a config-driven extraction system ("Artificer") and curated for clarity.

## Output

## Overview

Stage 09 performs rule-based interpretation of coding variants and assigns deterministic categorical labels.

## Key Metrics

- Total coding variants processed: `27486`
- Rare variants identified: `1335`
- Loss-of-function variants: `789`
- Missense variants: `11573`
- Synonymous variants: `11601`

## Interpretation Labels

| Label | Count |
| --- | --- |
| coding_common_or_low_support | 25169 |
| coding_uninterpretable | 1196 |
| lof_or_missense_rare | 1121 |

## Functional Impact Breakdown

| Functional Class | Count |
|------------------|--------|
| synonymous       | 11,601 |
| missense         | 11,573 |
| splice_relevant  | 3,154 |
| loss_of_function | 789 |
| other_coding     | 369 |

## Clinical Evidence

| Label | Count |
| --- | --- |
| missing | 19758 |
| benign | 6712 |
| likely_benign | 738 |
| vus | 184 |
| conflicting | 61 |
| pathogenic | 20 |
| likely_pathogenic | 13 |

## System Context

Stage 09 converts Stage 08 coding candidates into structured interpretation evidence for downstream Stage 11 prioritization.

## Interpretation

- Most coding variants are synonymous or missense  
- Loss-of-function variants are rare (~789)  
- Rare variants (~1,335) represent a small subset of total coding variation  

### Key Insight

> Only a small fraction of coding variants meet criteria for potential biological relevance.

This demonstrates the importance of filtering strategies in variant interpretation.

## Notes

- No additional notes.

## Limitations

- Descriptive summary only.
- No clinical diagnosis is performed.
- HG002 is a reference individual; candidate labels do not imply disease.
