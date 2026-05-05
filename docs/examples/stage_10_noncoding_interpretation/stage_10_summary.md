# stage_10_summary

## System Insight

Stage 10 does not attempt to fully interpret noncoding variants.

Instead, it:

- classifies variants into interpretable vs uninterpretable groups  
- identifies candidates for downstream analysis  
- preserves uncertainty where biological knowledge is incomplete  

This is a deliberate design choice.

## Source

- Source file: `/root/dev/portfolio_projects/variant_annotation_pipeline/results/run_2026_04_17_082417/processed/stage_10_noncoding_interpreted.tsv`
- Run ID: `run_2026_04_17_082417`
- Sample/Dataset: `HG002`

## Method

Artifacts are generated using a config-driven extraction system ("Artificer") and curated for clarity.

## Output

## Overview

Stage 10 performs rule-based interpretation of noncoding variants and assigns deterministic categorical labels.

## Key Metrics

- Total noncoding variants processed: `4,609,098`
- Candidate noncoding variants (regulatory or rare): ~`112,242`
- Common or low-support variants: `3,344,586`
- ClinVar pathogenic evidence: `28`

## Noncoding Interpretation Labels

| Label | Count |
| --- | --- |
| noncoding_common_or_low_support | 3344586 |
| noncoding_uninterpretable | 1152270 |
| regulatory_or_transcript_rare | 112242 |
## Functional Context

| Label | Count |
| --- | --- |
| intronic | 1615376 |
| transcript_associated | 1253498 |
| intergenic | 1107793 |
| proximal | 587954 |
| unknown | 44477 |
## Rarity Flag

| Label | Count |
| --- | --- |
| common | 4206244 |
| low_frequency | 156992 |
| rare | 128469 |
| missing | 117393 |
## Clinical Evidence

| Label | Count |
| --- | --- |
| missing | 4576020 |
| benign | 31605 |
| likely_benign | 1071 |
| vus | 356 |
| pathogenic | 28 |
| conflicting | 13 |
| likely_pathogenic | 5 |

## System Context

Stage 10 converts Stage 08 noncoding candidates into structured noncoding interpretation evidence for downstream Stage 11 prioritization.

## Interpretation

- Most noncoding variants are common (~4.2M) and unlikely to be functionally relevant  
- A subset (~128k) are rare and may warrant further investigation  
- ~1.15M variants remain uninterpretable with current annotation  

### Key Insight

> Noncoding interpretation is inherently limited and requires integration with additional data sources.

These include:

- gene expression (RSP)  
- regulatory annotation  
- functional genomics datasets  

## Notes

- No additional notes.

## Limitations

- Descriptive summary only.
- No clinical diagnosis is performed.
- Candidate labels do not imply disease.
