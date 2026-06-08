# Implementation Plan — `scripts/analysis/build_contrast_05_inputs.py`

## Objective

Build a deterministic sys76-local script that prepares the governed input substrate for:

```text
Contrast 05 — Coding vs Noncoding Semantic Composition
```

The script will re-array selected VAP semantic-composition figures, Stage 12 semantic bucket outputs, value-count telemetry outputs, and cross-run semantic summary tables into:

```text
docs/case_studies/cross_runs/contrasts/contrast_05_inputs/
```

The purpose is to create a compact, self-contained input substrate suitable for downstream JEN synthesis focused on semantic composition behavior across coding and noncoding variant space.

This script prepares the input substrate only. It does not create synthesis outputs, does not compress a bundle, and does not perform interpretation.

---

## Contrast 05 Scope

Contrast 05 evaluates how VAP semantic composition differs across coding and noncoding search space.

Primary analytical questions include:

* How do coding and noncoding semantic distributions differ across runs?
* Are ClinVar significance profiles conserved across runs?
* Do molecular consequence distributions remain stable?
* Are population-frequency semantic structures conserved?
* How does semantic branching differ between coding and noncoding substrate?
* Which semantic buckets dominate candidate routing behavior?

---

## Required Inputs

Contrast 05 input substrate requires four compact artifact classes.

### Cross-run global tables requiring SRA-specific subsetting

```text
docs/case_studies/cross_runs/cross_run_tables/clinical_status_summary.tsv
docs/case_studies/cross_runs/cross_run_tables/variant_consequence_summary.tsv
docs/case_studies/cross_runs/cross_run_tables/coding_noncoding_consequence_summary.tsv
```

These tables are subset by exact `run_id` and written to each SRA-specific `tables/` directory.

### F4 semantic-composition figures copied from each run

Source directory:

```text
results/<run_id>/figures/
```

Required figure files:

```text
<SRA>_f4a_clinvar_significance.png
<SRA>_f4a_consequence.png
<SRA>_f4a_pop_freq_bins.png
<SRA>_f4b_clinvar_significance.png
<SRA>_f4b_consequence.png
<SRA>_f4b_pop_freq_bins.png
```

Destination:

```text
contrast_05_inputs/<SRA>/figures/
```

Figures should be copied without renaming or content modification.

### Value-count telemetry outputs copied from Stage 12 exploration

Source:

```text
results/<run_id>/logs/stage12_exploration/value_counts/
```

Destination:

```text
contrast_05_inputs/<SRA>/sql_outputs/value_counts/
```

All `.tsv` files found in the source directory should be copied without renaming or content modification.

### Semantic bucket outputs copied from Stage 12 exploration

Source:

```text
results/<run_id>/logs/stage12_exploration/lane_candidate_slices/
```

Destination:

```text
contrast_05_inputs/<SRA>/sql_outputs/targeted_semantic_buckets/
```

All `.tsv` files found in the source directory should be copied without renaming or content modification.

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
docs/case_studies/cross_runs/contrasts/contrast_05_inputs/
```

---

## Script Location

```text
scripts/analysis/build_contrast_05_inputs.py
```

---

## Execution Context

Run from VAP repository root on sys76:

```bash
python scripts/analysis/build_contrast_05_inputs.py
```

The script assumes the sys76 repository contains the required lightweight `results/run_<id>/` directories and global cross-run tables.

---

## Source Immutability Rule

The script may read and copy/subset from:

```text
results/
docs/case_studies/cross_runs/cross_run_tables/clinical_status_summary.tsv
docs/case_studies/cross_runs/cross_run_tables/variant_consequence_summary.tsv
docs/case_studies/cross_runs/cross_run_tables/coding_noncoding_consequence_summary.tsv
docs/case_studies/cross_runs/contrasts/contrast_05_inputs/cohort_manifest.tsv
```

The script must never modify, overwrite, delete, move, or patch anything inside:

```text
results/
```

The script may write only inside:

```text
docs/case_studies/cross_runs/contrasts/contrast_05_inputs/
```

Within `contrast_05_inputs/`, the script may create or overwrite derived files that it owns.

The script must not overwrite:

```text
contrast_05_inputs/cohort_manifest.tsv
```

---

## Canonical Manifest

The script is manifest-driven.

Input manifest:

```text
docs/case_studies/cross_runs/contrasts/contrast_05_inputs/cohort_manifest.tsv
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

Contrast 05 currently includes 12 WES epilepsy SRAs and intentionally excludes HG002 WGS.

The script must not auto-discover additional runs.

The script should enforce:

```text
len(manifest) == 12
```

---

## Output Directory Structure

The generated input substrate should have this structure:

```text
docs/case_studies/cross_runs/contrasts/contrast_05_inputs/
├── cohort_manifest.tsv
├── contrast_05_input_build_audit.tsv
├── README.md
│
├── ERR10619203/
│   ├── figures/
│   │   ├── ERR10619203_f4a_clinvar_significance.png
│   │   ├── ERR10619203_f4a_consequence.png
│   │   ├── ERR10619203_f4a_pop_freq_bins.png
│   │   ├── ERR10619203_f4b_clinvar_significance.png
│   │   ├── ERR10619203_f4b_consequence.png
│   │   └── ERR10619203_f4b_pop_freq_bins.png
│   │
│   ├── tables/
│   │   ├── clinical_status_summary.tsv
│   │   ├── variant_consequence_summary.tsv
│   │   └── coding_noncoding_consequence_summary.tsv
│   │
│   └── sql_outputs/
│       ├── targeted_semantic_buckets/
│       └── value_counts/
│
├── ERR10619207/
│   └── [same structure]
│
└── ERR10619330/
    └── [same structure]
```

Each SRA directory should contain only selected Contrast 05 input substrate.

---

## Required Per-SRA Figure Layer

Copy the following figures from:

```text
results/<run_id>/figures/
```

Required files:

```text
<SRA>_f4a_clinvar_significance.png
<SRA>_f4a_consequence.png
<SRA>_f4a_pop_freq_bins.png
<SRA>_f4b_clinvar_significance.png
<SRA>_f4b_consequence.png
<SRA>_f4b_pop_freq_bins.png
```

Destination:

```text
contrast_05_inputs/<SRA>/figures/
```

Rules:

* Copy PNG only.
* Do not rename files.
* Copy without content modification.
* If any file is missing, record `missing_source` in the audit.

---

## Required Per-SRA Table Layer

The following global cross-run tables should be subset by `run_id` and written into each SRA-specific `tables/` directory without renaming:

```text
clinical_status_summary.tsv
variant_consequence_summary.tsv
coding_noncoding_consequence_summary.tsv
```

Source directory:

```text
docs/case_studies/cross_runs/cross_run_tables/
```

Destination pattern:

```text
contrast_05_inputs/<SRA>/tables/<same_filename>
```

Subsetting key:

```text
run_id
```

Rules:

* Use the exact manifest `run_id`.
* Preserve original column order.
* Preserve original values.
* Do not rename files.
* Do not alter source global tables.
* If a subset returns zero rows, still write the file with header only and record `zero_rows` in the audit.

---

## Required Value-Count Output Layer

Copy all `.tsv` files from:

```text
results/<run_id>/logs/stage12_exploration/value_counts/
```

to:

```text
contrast_05_inputs/<SRA>/sql_outputs/value_counts/
```

Rules:

* Copy without renaming.
* Copy without content modification.
* Preserve provenance-faithful structure.
* If the directory is missing, record `missing_source` in the audit.

---

## Required Semantic Bucket Output Layer

Copy all `.tsv` files from:

```text
results/<run_id>/logs/stage12_exploration/lane_candidate_slices/
```

to:

```text
contrast_05_inputs/<SRA>/sql_outputs/targeted_semantic_buckets/
```

Rules:

* Copy without renaming.
* Copy without content modification.
* Preserve provenance-faithful structure.
* If the directory is missing, record `missing_source` in the audit.

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
contrast_05_inputs/cohort_manifest.tsv
```

The script should read this file but must not rewrite it.

### `README.md`

If missing, the script may create a compact placeholder README.

If already present, the script should not overwrite it by default.

### `contrast_05_input_build_audit.tsv`

The script should write:

```text
contrast_05_inputs/contrast_05_input_build_audit.tsv
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

* copied F4 semantic figure
* subset clinical status summary
* subset variant consequence summary
* subset coding/noncoding consequence summary
* copied semantic bucket TSV
* copied value-count TSV
* ensured SRA directory
* zero-row subset

---

## Safety and Rebuild Behavior

The script may safely overwrite files it previously generated inside:

```text
contrast_05_inputs/<SRA>/
contrast_05_inputs/contrast_05_input_build_audit.tsv
```

The script must not delete the whole `contrast_05_inputs/` directory.

The script must not delete or modify:

```text
contrast_05_inputs/cohort_manifest.tsv
```

The script must not write outside:

```text
docs/case_studies/cross_runs/contrasts/contrast_05_inputs/
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
python scripts/analysis/build_contrast_05_inputs.py
```

Expected root files:

```text
contrast_05_inputs/cohort_manifest.tsv
contrast_05_inputs/contrast_05_input_build_audit.tsv
contrast_05_inputs/README.md
```

Expected per-SRA directories:

```text
12 SRA directories
```

Expected per-SRA subdirectories:

```text
figures/
tables/
sql_outputs/value_counts/
sql_outputs/targeted_semantic_buckets/
```

Expected per-SRA tables:

```text
3 files
```

Expected per-SRA figures:

```text
6 PNG files
```

Expected semantic bucket and value-count TSV totals vary depending on run exports.

Quick validation commands:

```bash
find docs/case_studies/cross_runs/contrasts/contrast_05_inputs \
  -path "*/tables/*.tsv" | wc -l

find docs/case_studies/cross_runs/contrasts/contrast_05_inputs \
  -path "*/figures/*.png" | wc -l

find docs/case_studies/cross_runs/contrasts/contrast_05_inputs \
  -path "*/sql_outputs/value_counts/*.tsv" | wc -l

find docs/case_studies/cross_runs/contrasts/contrast_05_inputs \
  -path "*/sql_outputs/targeted_semantic_buckets/*.tsv" | wc -l

column -t -s $'\t' \
  docs/case_studies/cross_runs/contrasts/contrast_05_inputs/contrast_05_input_build_audit.tsv \
  | less -S
```

Expected minimum counts:

```text
tables: 36
figures: 72
```

---

## Non-Goals

This script does not:

* create `contrast_05_outputs/`
* generate synthesis seed outputs
* compress a final `.tar.gz`
* modify source global cross-run tables
* modify `results/`
* perform biological interpretation
* perform clinical interpretation
* infer missing semantic structures
* canonicalize missing gene symbols
* rename provenance-bearing SQL outputs

---

## Future Follow-Up

After validation, a separate packaging step may copy or package `contrast_05_inputs/` into a transport-ready `contrast_05_analysis_bundle/` or `.tar.gz` without returning to raw `results/`.


```bash
tar -czf \
docs/case_studies/cross_runs/contrasts/contrast_05_analysis_bundle.tar.gz \
-C docs/case_studies/cross_runs/contrasts \
contrast_05_inputs
```

Inspect it:

```bash
tar -tzf docs/case_studies/cross_runs/contrasts/contrast_05_analysis_bundle.tar.gz | less
```

Quick size check:

```bash
ls -lh docs/case_studies/cross_runs/contrasts/contrast_05_analysis_bundle.tar.gz
```
