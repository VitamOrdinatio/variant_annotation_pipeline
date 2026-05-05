# Stage 13 Output Manifest

Git-safe summary of the VAP Stage 13 artifact manifest.

## Source

- Source file: `/mnt/storage/vap_runs/HG002/run_2026_04_17_082417/raw_mark_outputs/processed/stage_13_artifact_manifest.json`
- Run ID: `run_2026_04_17_082417`
- Sample/Dataset: `HG002`

### System Insight

> All required upstream artifacts are present, confirming a complete and reproducible pipeline run.

## Output

| artifact_name | stage | file_type | exists | required | size_bytes |
| --- | --- | --- | --- | --- | --- |
| stage_11_prioritized_variants | stage_11 | tsv | True | True | 2335070476 |
| stage_11_summary_json | stage_11 | json | True | True | 3676 |
| stage_11_gene_variant_counts | stage_11 | tsv | True | True | 998494 |
| stage_12_validation_candidates | stage_12 | tsv | True | True | 2548081260 |
| stage_12_summary_json | stage_12 | json | True | True | 1468 |
| stage_13_final_summary | stage_13 | json | True | True | 3227 |
| stage_13_artifact_manifest | stage_13 | json | True | True | 10099 |
| stage_13_run_report | stage_13 | markdown | True | True | 2684 |
| stage_08_summary.json | stage_08 | json | True | False | 2852 |
| stage_09_summary.json | stage_09 | json | True | False | 2685 |
| stage_10_summary.json | stage_10 | json | True | False | 2751 |
| HG002_run_2026_04_17_082417.annotated_variants.tsv | stage_07 | tsv | True | False | 1053663787 |
| coding_candidates.tsv | stage_08 | tsv | True | False | 6853227 |
| noncoding_candidates.tsv | stage_08 | tsv | True | False | 1371631690 |
| qc_flagged.tsv | stage_08 | tsv | True | False | 13176434 |
| splice_region_candidates.tsv | stage_08 | tsv | True | False | 1234010 |
| stage_08_rdgp_gene_evidence_seed.tsv | stage_08 | tsv | True | False | 60237527 |
| stage_08_selected_transcript_consequences.tsv | stage_08 | tsv | True | False | 1379554351 |
| stage_08_variant_summary.tsv | stage_08 | tsv | True | False | 1002799826 |
| stage_08_vdb_ready_variants.tsv | stage_08 | tsv | True | False | 1379554351 |
| stage_09_coding_interpreted.tsv | stage_09 | tsv | True | False | 10655243 |
| stage_10_noncoding_interpreted.tsv | stage_10 | tsv | True | False | 1848972536 |
| HG002_run_2026_04_17_082417.normalized_variants.vcf | stage_06 | vcf | True | False | 931362295 |
| HG002_run_2026_04_17_082417.raw_variants.vcf | stage_05 | vcf | True | False | 931352437 |
| HG002_run_2026_04_17_082417.annotated_variants.vcf | stage_07 | vcf | True | False | 1923830298 |

## Interpretation

This manifest documents which source and output artifacts were present for the completed VAP run.

## Limitations

- Paths are summarized for review.
- Large source outputs are not copied into Git.
