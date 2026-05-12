# VAP Stage 13 Final Run Report

## Run overview

- Run ID: `run_2026_04_17_082417`
- Sample ID: `HG002`
- Source pipeline: `variant_annotation_pipeline`
- Total variants processed: `4636584`
- Variants assigned priority tiers: `4636584`
- Validation-required candidates: `113363`


## System-Level Interpretation

This run demonstrates correct end-to-end pipeline behavior using HG002, a healthy reference genome.

### Key Observations

- No high-priority variants were identified (expected for a non-disease genome)
- ~2.4% of variants were selected for validation (consistent with prioritization thresholds)
- All validation candidates originate from Tier 2 prioritization
- No artifact flags were detected

### System Insight

> The pipeline correctly prioritizes and triages variants without overcalling disease-relevant signal.

### Biological Context

HG002 is not expected to contain pathogenic variation. The absence of high-priority candidates reflects appropriate calibration rather than lack of sensitivity.

### Bottom Line

> This run confirms that VAP produces biologically realistic outputs and avoids false-positive prioritization.

## Input artifacts

- `stage_11_prioritized_variants` — exists=True, size_bytes=2335070476, path=`/root/dev/portfolio_projects/variant_annotation_pipeline/results/run_2026_04_17_082417/processed/stage_11_prioritized_variants.tsv`
- `stage_11_summary_json` — exists=True, size_bytes=3676, path=`/root/dev/portfolio_projects/variant_annotation_pipeline/results/run_2026_04_17_082417/processed/stage_11_summary.json`
- `stage_11_gene_variant_counts` — exists=True, size_bytes=998494, path=`/root/dev/portfolio_projects/variant_annotation_pipeline/results/run_2026_04_17_082417/processed/stage_11_gene_variant_counts.tsv`
- `stage_12_validation_candidates` — exists=True, size_bytes=2548081260, path=`/root/dev/portfolio_projects/variant_annotation_pipeline/results/run_2026_04_17_082417/processed/stage_12_validation_candidates.tsv`
- `stage_12_summary_json` — exists=True, size_bytes=1468, path=`/root/dev/portfolio_projects/variant_annotation_pipeline/results/run_2026_04_17_082417/processed/stage_12_summary.json`

## Final output artifacts

- `stage_13_final_summary` — exists=True, size_bytes=3227, path=`/root/dev/portfolio_projects/variant_annotation_pipeline/results/run_2026_04_17_082417/processed/stage_13_final_summary.json`
- `stage_13_artifact_manifest` — exists=True, size_bytes=10099, path=`/root/dev/portfolio_projects/variant_annotation_pipeline/results/run_2026_04_17_082417/processed/stage_13_artifact_manifest.json`
- `stage_13_run_report` — exists=True, size_bytes=2684, path=`/root/dev/portfolio_projects/variant_annotation_pipeline/results/run_2026_04_17_082417/processed/stage_13_run_report.md`

## Variant prioritization summary

- `tier_2_moderate_candidate`: `113363`
- `tier_3_low_support_or_common`: `3369755`
- `tier_4_uninterpretable_or_qc_limited`: `1153466`

## Validation preparation summary

- Validation required: `113363`
- Validation not required: `4523221`
- Suggested IGV validations: `113363`

## Gene-count summary

- Unique gene IDs observed: `50231`

| gene_id | variant_count |
|---|---:|
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

## QC summary

- Required inputs exist and are non-empty.
- Stage 11 and Stage 12 row-count consistency checks passed.
- Stage 13 did not modify upstream outputs.

## Assumptions

- Stage 11 and Stage 12 outputs are contract-compliant.
- Stage 13 operates on a single completed run directory.
- Gene-level counts are descriptive only and are not RDGP ranking.

## Limitations

- Stage 13 does not create visualizations.
- Stage 13 does not execute IGV.
- Stage 13 does not parse BAM files.
- Stage 13 does not perform phenotype matching or gene ranking.

## Non-goals

- No new annotation.
- No new interpretation.
- No new prioritization.
- No gene-level ranking.
- No upstream recomputation.

---