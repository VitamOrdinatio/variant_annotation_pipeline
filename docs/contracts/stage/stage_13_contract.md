# Stage 13 — Write Final Summary

## Purpose

Stage 13 produces final run-level outputs for VAP v1 reporting, reproducibility, auditability, and portfolio evidence.

This stage summarizes completed pipeline outputs without introducing new annotation, reinterpretation, prioritization, filtering, visualization, or upstream recomputation.

---

## Inputs

### Required Inputs

- `stage_11_prioritized_variants.tsv`
- `stage_11_summary.json`
- `stage_11_gene_variant_counts.tsv`
- `stage_12_validation_candidates.tsv`
- `stage_12_summary.json`

### Optional Inputs

If available, Stage 13 may also include:

- earlier `stage_*_summary.json` files
- earlier major TSV outputs
- earlier major VCF outputs
- log files
- run metadata files

Missing optional inputs must be reported in the artifact manifest but must not fail the stage.

---

## Outputs

Stage 13 must write:

- `stage_13_final_summary.json`
- `stage_13_artifact_manifest.json`
- `stage_13_run_report.md`

---

## Core Principles

- Preserve all upstream outputs unchanged
- Do not rerun upstream stages
- Do not filter variants
- Do not reinterpret variants
- Do not reprioritize variants
- Do not perform gene-level ranking
- Produce both machine-readable and human-readable run evidence

---

## Final Summary JSON

Output:

`stage_13_final_summary.json`

### Required Fields

- `stage`
- `status`
- `run_id`
- `sample_id`
- `source_pipeline`
- `total_variants_processed`
- `prioritized_variant_count`
- `validation_candidate_count`
- `validation_required_count`
- `counts_by_priority_tier`
- `counts_by_priority_rank`
- `counts_by_variant_origin`
- `counts_by_source_interpretation_label`
- `counts_by_validation_required`
- `counts_by_validation_priority`
- `counts_by_suggested_validation_method`
- `high_priority_candidate_count`
- `moderate_priority_candidate_count`
- `low_priority_candidate_count`
- `uninterpretable_count`
- `gene_id_count_unique`
- `top_gene_variant_counts`
- `qc_status_by_stage`
- `artifact_manifest_path`
- `run_report_path`
- `annotation_sources_present`
- `annotation_versions_present`

---

## Artifact Manifest JSON

Output:

`stage_13_artifact_manifest.json`

Each artifact record must include:

- `artifact_name`
- `stage`
- `path`
- `file_type`
- `exists`
- `size_bytes`
- `modified_timestamp`
- `required`

The manifest must include all required Stage 13 inputs and all Stage 13 outputs.

Optional upstream artifacts may be included when discoverable.

---

## Run Report Markdown

Output:

`stage_13_run_report.md`

The run report must be human-readable and suitable as portfolio evidence. 

This file must be suitable for direct human consumption without additional tooling.

### Required Sections

- Run overview
- Input artifacts
- Final output artifacts
- Variant prioritization summary
- Validation preparation summary
- Gene-count summary
- QC summary
- Assumptions
- Limitations
- Non-goals

---

## QC Requirements

Stage 13 must verify:

- Required inputs exist
- Required inputs are non-empty
- Stage 11 row counts match Stage 12 row counts
- Stage 11 prioritized variant count equals Stage 12 validation candidate count
- Validation-required count is consistent with Stage 12 summary
- Stage 11 and Stage 12 interpretation counts must match Stage 13 summary counts
- Artifact manifest records required files correctly
- Final summary and run report are written successfully

Failures in required input checks must fail Stage 13.

Missing optional artifacts must be recorded but must not fail Stage 13.



### QC Status By Stage

```yaml
qc_status_by_stage:
  stage_08:
    status: 
    input_rows:
    output_rows:
  stage_09:
    status: 
    input_rows:
    output_rows:
  stage_10:
    status: 
    input_rows:
    output_rows:
  stage_11:
    status: 
    input_rows:
    output_rows:
  stage_12:
    status: 
    input_rows:
    output_rows:
```

---

## Assumptions

- Stage 11 and Stage 12 outputs are contract-compliant
- Stage 13 operates on a single completed run directory
- Stage 13 reports the run as-is and does not correct upstream outputs
- Gene-level counts in Stage 13 are descriptive only and are not RDGP ranking

---

## Non-Goals

- No new annotation
- No new interpretation
- No new prioritization
- No gene-level ranking
- No phenotype matching
- No visualization
- No reporting UI
- No IGV execution
- No BAM parsing
- No upstream recomputation


## Success Criteria

Stage 13 succeeds when:

- `stage_13_final_summary.json` exists and is non-empty
- `stage_13_artifact_manifest.json` exists and is non-empty
- `stage_13_run_report.md` exists and is non-empty
- all required inputs are represented in the manifest
- row-count consistency checks pass
- final summary captures Stage 11 and Stage 12 results

---