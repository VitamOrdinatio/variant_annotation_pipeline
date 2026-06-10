# Implementation Plan — `scripts/analysis/build_contrast_07_inputs.py`

## Objective

Build a deterministic sys76-local script that prepares the governed input substrate for:

```text
Contrast 07 — Provenance Transition Determinism
```

The script will re-array selected VAP provenance tables, runtime telemetry tables, stage-funnel transition summaries, read-depth metadata, and stage-specific metrics JSON files into:

```text
docs/case_studies/cross_runs/contrasts/contrast_07_inputs/
```

The purpose is to create a compact, self-contained input substrate suitable for downstream JEN synthesis focused on execution determinism, provenance continuity, stage-transition behavior, and semantic routing stability across the 12 epilepsy WES runs.

This script prepares the input substrate only. It does not create synthesis outputs, does not compress a bundle, and does not perform interpretation.

---

## Contrast 07 Scope

Contrast 07 evaluates how VAP execution provenance and stage-transition behavior behave across independent epilepsy WES executions.

Primary analytical questions include:

* Are provenance structures stable across runs?
* Are stage-transition funnels conserved?
* Does runtime telemetry track with sequencing depth?
* Are stage-level metrics deterministic across repeated semantic transformations?
* Which stages dominate semantic narrowing behavior?
* Are transition structures preserved across Q1, median, and Q3 sequencing depth strata?

---

## Required Inputs

Contrast 07 input substrate requires two compact artifact classes.

### Cross-run global tables requiring SRA-specific subsetting

```text
docs/case_studies/cross_runs/cross_run_tables/provenance_summary.tsv
docs/case_studies/cross_runs/cross_run_tables/runtime_stage_summary.tsv
docs/case_studies/cross_runs/cross_run_tables/sra_run_depth_metadata.tsv
docs/case_studies/cross_runs/cross_run_tables/stage_funnel_summary.tsv
```

These tables are subset into each SRA-specific `tables/` directory.

Subsetting rules:

```text
provenance_summary.tsv              subset by run_id
runtime_stage_summary.tsv           subset by run_id
stage_funnel_summary.tsv            subset by run_id
sra_run_depth_metadata.tsv          subset by SRA
```

### Stage-specific metrics JSON files copied from each run

Source directory:

```text
results/<run_id>/metrics/
```

Required files:

```text
stage_05_variant_calling_metrics.json
stage_06_normalization_metrics.json
stage_07_annotation_metrics.json
stage_08_partition_metrics.json
stage_09_coding_interpretation_metrics.json
stage_10_noncoding_interpretation_metrics.json
stage_11_prioritization_metrics.json
stage_12_validation_metrics.json
```

Destination:

```text
contrast_07_inputs/<SRA>/metrics/
```

Metrics JSON files should be copied without renaming or content modification.

---

## Governance Context

This script implements the cross-run governance principles of:

* contrast isolation
* artifact isomorphism
* source immutability
* high semantic density with low ingestion noise
* recoverable semantic compression
* strict separation between raw VAP outputs, governed contrast inputs, and future synthesis outputs

The script treats:

```text
results/run_<id>/
```

as immutable governed substrate.

The script writes only to:

```text
docs/case_studies/cross_runs/contrasts/contrast_07_inputs/
```

---

## Script Location

```text
scripts/analysis/build_contrast_07_inputs.py
```

---

## Execution Context

Run from VAP repository root on sys76:

```bash
python scripts/analysis/build_contrast_07_inputs.py
```

The script assumes the sys76 repository contains the required lightweight `results/run_<id>/` directories and global cross-run tables.

---

## Source Immutability Rule

The script may read and copy/subset from:

```text
results/
docs/case_studies/cross_runs/cross_run_tables/provenance_summary.tsv
docs/case_studies/cross_runs/cross_run_tables/runtime_stage_summary.tsv
docs/case_studies/cross_runs/cross_run_tables/sra_run_depth_metadata.tsv
docs/case_studies/cross_runs/cross_run_tables/stage_funnel_summary.tsv
docs/case_studies/cross_runs/contrasts/contrast_07_inputs/cohort_manifest.tsv
```

The script must never modify, overwrite, delete, move, or patch anything inside:

```text
results/
```

The script may write only inside:

```text
docs/case_studies/cross_runs/contrasts/contrast_07_inputs/
```

Within `contrast_07_inputs/`, the script may create or overwrite derived files that it owns.

The script must not overwrite:

```text
contrast_07_inputs/cohort_manifest.tsv
```

---

## Canonical Manifest

The script is manifest-driven.

Input manifest:

```text
docs/case_studies/cross_runs/contrasts/contrast_07_inputs/cohort_manifest.tsv
```

Expected current/source columns may be:

```text
SRA_accn
VAP_run_id
Depth_Category
```

The script should normalize these internally to:

```text
SRA
run_id
depth_category
```

The manifest is the source of truth for which runs are included.

Contrast 07 currently includes 12 WES epilepsy SRAs and intentionally excludes HG002 WGS.

The script must not auto-discover additional runs.

The script should enforce:

```text
len(manifest) == 12
```

---

## Output Directory Structure

The generated input substrate should have this structure:

```text
docs/case_studies/cross_runs/contrasts/contrast_07_inputs/
├── cohort_manifest.tsv
├── contrast_07_input_build_audit.tsv
├── README.md
│
├── ERR10619203/
│   ├── tables/
│   │   ├── provenance_summary.tsv
│   │   ├── runtime_stage_summary.tsv
│   │   ├── sra_run_depth_metadata.tsv
│   │   └── stage_funnel_summary.tsv
│   │
│   └── metrics/
│       ├── stage_05_variant_calling_metrics.json
│       ├── stage_06_normalization_metrics.json
│       ├── stage_07_annotation_metrics.json
│       ├── stage_08_partition_metrics.json
│       ├── stage_09_coding_interpretation_metrics.json
│       ├── stage_10_noncoding_interpretation_metrics.json
│       ├── stage_11_prioritization_metrics.json
│       └── stage_12_validation_metrics.json
│
├── ERR10619207/
│   └── [same structure]
│
└── ERR10619330/
    └── [same structure]
```

Each SRA directory should contain only selected Contrast 07 input substrate.

---

## Required Per-SRA Table Layer

The following global cross-run tables should be subset into each SRA-specific `tables/` directory without renaming:

```text
provenance_summary.tsv
runtime_stage_summary.tsv
sra_run_depth_metadata.tsv
stage_funnel_summary.tsv
```

Source directory:

```text
docs/case_studies/cross_runs/cross_run_tables/
```

Subsetting rules:

```text
provenance_summary.tsv              subset by run_id
runtime_stage_summary.tsv           subset by run_id
stage_funnel_summary.tsv            subset by run_id
sra_run_depth_metadata.tsv          subset by SRA
```

Rules:

* Preserve original column order.
* Preserve original values.
* Do not rename files.
* Do not alter source global tables.
* If a subset returns zero rows, still write the file with header only and record `zero_rows` in the audit.

---

## Required Metrics Output Layer

Copy the following JSON files from:

```text
results/<run_id>/metrics/
```

Required files:

```text
stage_05_variant_calling_metrics.json
stage_06_normalization_metrics.json
stage_07_annotation_metrics.json
stage_08_partition_metrics.json
stage_09_coding_interpretation_metrics.json
stage_10_noncoding_interpretation_metrics.json
stage_11_prioritization_metrics.json
stage_12_validation_metrics.json
```

Destination:

```text
contrast_07_inputs/<SRA>/metrics/
```

Rules:

* Copy without renaming.
* Copy without content modification.
* Preserve provenance-faithful structure.
* If any file is missing, record `missing_source` in the audit.

---

## Run Identity Guardrail

For each manifest row, validate that:

```text
results/<run_id>/metadata/figure_set_resolved.yaml
```

exists and agrees with the manifest.

Required checks:

```text
manifest SRA == figure_set_resolved.yaml sample_id
manifest run_id == figure_set_resolved.yaml run_id
```

If either check fails, abort with `SystemExit`.

This guardrail prevents accidental SRA/run mismatches during re-arraying.

---

## Root-Level Files

### `cohort_manifest.tsv`

Preserve the existing manifest at:

```text
contrast_07_inputs/cohort_manifest.tsv
```

The script should read this file but must not rewrite it.

### `README.md`

If missing, the script may create a compact placeholder README.

If already present, the script should not overwrite it by default.

### `contrast_07_input_build_audit.tsv`

The script should write:

```text
contrast_07_inputs/contrast_07_input_build_audit.tsv
```

This file is owned by the builder and may be overwritten on rebuild.

---

## Audit Schema

The audit should contain one row per expected or discovered artifact operation.

Recommended columns:

```text
SRA
run_id
depth_category
artifact_group
artifact_name
source_path
destination_path
operation
status
rows_written
notes
```

Allowed `operation` values:

```text
copy
subset
mkdir
skip
```

Allowed `status` values:

```text
ok
missing_source
zero_rows
error
skipped_optional
```

Audit examples:

* subset provenance summary
* subset runtime stage summary
* subset stage-funnel summary
* subset SRA depth metadata
* copied stage metrics JSON
* ensured SRA directory
* zero-row subset

---

## Safety and Rebuild Behavior

The script may safely overwrite files it previously generated inside:

```text
contrast_07_inputs/<SRA>/
contrast_07_inputs/contrast_07_input_build_audit.tsv
```

The script must not delete the whole `contrast_07_inputs/` directory.

The script must not delete or modify:

```text
contrast_07_inputs/cohort_manifest.tsv
```

The script must not write outside:

```text
docs/case_studies/cross_runs/contrasts/contrast_07_inputs/
```

except for normal console output.

Recommended behavior:

* create missing directories with `mkdir(parents=True, exist_ok=True)`
* overwrite owned copied/subsetted files in place
* never remove unrelated user-created files

---

## Validation Expectations

After running:

```bash
python scripts/analysis/build_contrast_07_inputs.py
```

Expected root files:

```text
contrast_07_inputs/cohort_manifest.tsv
contrast_07_inputs/contrast_07_input_build_audit.tsv
contrast_07_inputs/README.md
```

Expected per-SRA directories:

```text
12 SRA directories
```

Expected per-SRA subdirectories:

```text
tables/
metrics/
```

Expected per-SRA tables:

```text
4 files
```

Expected per-SRA metrics JSON files:

```text
8 files
```

Quick validation commands:

```bash
find docs/case_studies/cross_runs/contrasts/contrast_07_inputs \
  -path "*/tables/*.tsv" | wc -l

find docs/case_studies/cross_runs/contrasts/contrast_07_inputs \
  -path "*/metrics/*.json" | wc -l

column -t -s $'\t' \
  docs/case_studies/cross_runs/contrasts/contrast_07_inputs/contrast_07_input_build_audit.tsv \
  | less -S
```

Expected minimum counts:

```text
tables: 48
metrics JSONs: 96
```

---

## Non-Goals

This script does not:

* create `contrast_07_outputs/`
* generate synthesis seed outputs
* compress a final `.tar.gz`
* modify source global cross-run tables
* modify `results/`
* perform biological interpretation
* perform clinical interpretation
* infer missing provenance structures
* canonicalize missing values
* rename provenance-bearing metrics files

---

## Future Follow-Up

After validation, a separate packaging step may copy or package `contrast_07_inputs/` into a transport-ready `contrast_07_analysis_bundle/` or `.tar.gz` without returning to raw `results/`.


```bash
tar -czf \
docs/case_studies/cross_runs/contrasts/contrast_07_analysis_bundle.tar.gz \
-C docs/case_studies/cross_runs/contrasts \
contrast_07_inputs
```

Inspect it:

```bash
tar -tzf docs/case_studies/cross_runs/contrasts/contrast_07_analysis_bundle.tar.gz | less
```

Quick size check:

```bash
ls -lh docs/case_studies/cross_runs/contrasts/contrast_07_analysis_bundle.tar.gz
```
