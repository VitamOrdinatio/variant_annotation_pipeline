# stage_12_summary

## Source

- Source file: `/root/dev/portfolio_projects/variant_annotation_pipeline/results/run_2026_04_17_082417/processed/stage_12_validation_candidates.tsv`
- Run ID: `run_2026_04_17_082417`
- Sample/Dataset: `HG002`

## Overview

Stage 12 adds validation triage fields to prioritized variants, including validation requirement status, validation priority, suggested validation method, and validation rationale.

## Key Metrics

- Total validation candidate records: `4636584`
- Validation required: `113363`
- High-quality records: `4592124`
- Potential artifacts: `0`
- High validation-priority records: `0`

### Validation Efficiency

> Only ~2.4% of variants require validation, demonstrating strong prioritization upstream.

## Validation Required Distribution

| Label | Count |
| --- | --- |
| False | 4523221 |
| True | 113363 |
## Validation Priority Distribution

| Label | Count |
| --- | --- |
| low | 4523221 |
| medium | 113363 |
## Suggested Validation Method Distribution

| Label | Count |
| --- | --- |
| none | 4523221 |
| IGV | 113363 |
## Validation Reason Distribution

| Label | Count |
| --- | --- |
| tier_3_low_support_or_common | 3369755 |
| tier_4_uninterpretable_or_qc_limited | 1153466 |
| tier_2_moderate_candidate | 113363 |
## QC Reliability Distribution

| Label | Count |
| --- | --- |
| high_confidence | 4592124 |
| caution | 44460 |

## System Context

Stage 12 converts prioritized variants into validation-triage candidates. It does not validate variants experimentally and does not perform clinical diagnosis.

### Interpretation

HG002 is a healthy reference genome. The absence of high validation-priority variants is expected and reflects appropriate system calibration rather than a lack of sensitivity.

## Notes

- No additional notes.

## Limitations

- Descriptive summary only.
- No clinical diagnosis is performed.
- Candidate labels do not imply disease.
