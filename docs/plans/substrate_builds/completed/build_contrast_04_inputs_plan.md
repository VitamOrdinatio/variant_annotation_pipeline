# Implementation Plan — `scripts/analysis/build_contrast_04_inputs.py`

## Objective

Build a deterministic sys76-local script that prepares the governed input substrate for:

```text
Contrast 04 — Tiered Overlay Convergence / Divergence
```

The script will re-array selected VAP overlay-tier artifacts and cross-run overlay tables into:

```text
docs/case_studies/cross_runs/contrasts/contrast_04_inputs/
```

The purpose is to create a compact, self-contained input substrate suitable for downstream JEN synthesis focused on overlay-constrained tiered gene convergence and divergence across the 12 epilepsy WES runs.

This script prepares the input substrate only. It does not create synthesis outputs, does not compress a bundle, and does not perform interpretation.

---

## Contrast 04 Scope

Contrast 04 evaluates whether overlay-constrained tiered gene topology is shared or individualized across independent epilepsy WES executions.

Primary analytical questions include:

* Which tiered overlay genes recur across multiple runs?
* Which overlay-tier genes remain individualized?
* Are mitochondrial and epilepsy overlays preserved across tiered outputs?
* Does sequencing depth appear associated with overlay convergence or divergence?
* Does VAP preserve individualized topology under shared semantic governance?

---

## Required Inputs

Contrast 04 input substrate requires three compact artifact classes.

### Cross-run global tables requiring SRA-specific subsetting

```text
docs/case_studies/cross_runs/cross_run_tables/gene_list_overlay_intersections.tsv
docs/case_studies/cross_runs/cross_run_tables/overlay_gene_coding_clinical_evidence.tsv
```

These tables are subset by exact `run_id` and written to each SRA-specific `tables/` directory.

### F5 interoperability figure copied from each run

Source:

```text
results/<run_id>/figures/<SRA>_f5_interoperability_substrates.png
```

Destination:

```text
contrast_04_inputs/<SRA>/figures/<SRA>_f5_interoperability_substrates.png
```

The figure is copied without renaming or content modification.

### Overlay-tiered gene outputs copied from Stage 12 exploration

Source:

```text
results/<run_id>/logs/stage12_exploration/unique_genes/
```

Required files:

```text
<SRA>_tier1_unique_genes_mito_epi_overlay.tsv
<SRA>_tier2_unique_genes_mito_epi_overlay.tsv
<SRA>_tier3_unique_genes_mito_epi_overlay.tsv
```

Destination:

```text
contrast_04_inputs/<SRA>/sql_outputs/overlay_tiered_gene_outputs/
```

Files should be copied without renaming and without content modification.

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
docs/case_studies/cross_runs/contrasts/contrast_04_inputs/
```

---

## Script Location

```text
scripts/analysis/build_contrast_04_inputs.py
```

---

## Execution Context

Run from VAP repository root on sys76:

```bash
python scripts/analysis/build_contrast_04_inputs.py
```

The script assumes the sys76 repository contains the required lightweight `results/run_<id>/` directories and global cross-run tables.

---

## Source Immutability Rule

The script may read and copy/subset from:

```text
results/
docs/case_studies/cross_runs/cross_run_tables/gene_list_overlay_intersections.tsv
docs/case_studies/cross_runs/cross_run_tables/overlay_gene_coding_clinical_evidence.tsv
docs/case_studies/cross_runs/contrasts/contrast_04_inputs/cohort_manifest.tsv
```

The script must never modify, overwrite, delete, move, or patch anything inside:

```text
results/
```

The script may write only inside:

```text
docs/case_studies/cross_runs/contrasts/contrast_04_inputs/
```

Within `contrast_04_inputs/`, the script may create or overwrite derived files that it owns.

The script must not overwrite:

```text
contrast_04_inputs/cohort_manifest.tsv
```

---

## Canonical Manifest

The script is manifest-driven.

Input manifest:

```text
docs/case_studies/cross_runs/contrasts/contrast_04_inputs/cohort_manifest.tsv
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

Contrast 04 currently includes 12 WES epilepsy SRAs and intentionally excludes HG002 WGS.

The script must not auto-discover additional runs.

The script should enforce:

```text
len(manifest) == 12
```

---

## Output Directory Structure

The generated input substrate should have this structure:

```text
docs/case_studies/cross_runs/contrasts/contrast_04_inputs/
├── cohort_manifest.tsv
├── contrast_04_input_build_audit.tsv
├── README.md
│
├── ERR10619203/
│   ├── figures/
│   │   └── ERR10619203_f5_interoperability_substrates.png
│   │
│   ├── tables/
│   │   ├── gene_list_overlay_intersections.tsv
│   │   └── overlay_gene_coding_clinical_evidence.tsv
│   │
│   └── sql_outputs/
│       └── overlay_tiered_gene_outputs/
│           ├── ERR10619203_tier1_unique_genes_mito_epi_overlay.tsv
│           ├── ERR10619203_tier2_unique_genes_mito_epi_overlay.tsv
│           └── ERR10619203_tier3_unique_genes_mito_epi_overlay.tsv
│
├── ERR10619207/
│   └── [same structure]
│
└── ERR10619330/
    └── [same structure]
```

Each SRA directory should contain only selected Contrast 04 input substrate.

---

## Required Per-SRA Figure Layer

Copy the F5 interoperability figure from:

```text
results/<run_id>/figures/<SRA>_f5_interoperability_substrates.png
```

to:

```text
contrast_04_inputs/<SRA>/figures/<same_filename>
```

Rules:

* Copy PNG only.
* Do not copy SVG unless explicitly required later.
* Do not rename the file.
* If missing, record `missing_source` in the audit.

---

## Required Per-SRA Table Layer

The following global cross-run tables should be subset by `run_id` and written into each SRA-specific `tables/` directory without renaming:

```text
gene_list_overlay_intersections.tsv
overlay_gene_coding_clinical_evidence.tsv
```

Source directory:

```text
docs/case_studies/cross_runs/cross_run_tables/
```

Destination pattern:

```text
contrast_04_inputs/<SRA>/tables/<same_filename>
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

## Required Overlay-Tiered Gene Output Layer

Copy the following files from:

```text
results/<run_id>/logs/stage12_exploration/unique_genes/
```

to:

```text
contrast_04_inputs/<SRA>/sql_outputs/overlay_tiered_gene_outputs/
```

Required copied files:

```text
<SRA>_tier1_unique_genes_mito_epi_overlay.tsv
<SRA>_tier2_unique_genes_mito_epi_overlay.tsv
<SRA>_tier3_unique_genes_mito_epi_overlay.tsv
```

Rules:

* Copy without renaming.
* Copy without content modification.
* Do not canonicalize missing gene symbols in this contrast.
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
contrast_04_inputs/cohort_manifest.tsv
```

The script should read this file but must not rewrite it.

### `README.md`

If missing, the script may create a compact placeholder README.

If already present, the script should not overwrite it by default.

### `contrast_04_input_build_audit.tsv`

The script should write:

```text
contrast_04_inputs/contrast_04_input_build_audit.tsv
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

* copied F5 interoperability figure
* subset gene-list overlay intersections
* subset overlay clinical evidence
* copied tier1/tier2/tier3 overlay-tiered gene output
* ensured SRA directory
* zero-row subset

---

## Safety and Rebuild Behavior

The script may safely overwrite files it previously generated inside:

```text
contrast_04_inputs/<SRA>/
contrast_04_inputs/contrast_04_input_build_audit.tsv
```

The script must not delete the whole `contrast_04_inputs/` directory.

The script must not delete or modify:

```text
contrast_04_inputs/cohort_manifest.tsv
```

The script must not write outside:

```text
docs/case_studies/cross_runs/contrasts/contrast_04_inputs/
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
python scripts/analysis/build_contrast_04_inputs.py
```

Expected root files:

```text
contrast_04_inputs/cohort_manifest.tsv
contrast_04_inputs/contrast_04_input_build_audit.tsv
contrast_04_inputs/README.md
```

Expected per-SRA directories:

```text
12 SRA directories
```

Expected per-SRA subdirectories:

```text
figures/
tables/
sql_outputs/overlay_tiered_gene_outputs/
```

Expected per-SRA tables:

```text
2 files
```

Expected per-SRA F5 figures:

```text
1 PNG file
```

Expected per-SRA overlay-tiered gene output files:

```text
3 files
```

Quick validation commands:

```bash
find docs/case_studies/cross_runs/contrasts/contrast_04_inputs \
  -maxdepth 1 -type d | sort

find docs/case_studies/cross_runs/contrasts/contrast_04_inputs \
  -path "*/tables/*.tsv" | wc -l

find docs/case_studies/cross_runs/contrasts/contrast_04_inputs \
  -path "*/figures/*f5_interoperability_substrates.png" | wc -l

find docs/case_studies/cross_runs/contrasts/contrast_04_inputs \
  -path "*/sql_outputs/overlay_tiered_gene_outputs/*.tsv" | wc -l

column -t -s $'\t' \
  docs/case_studies/cross_runs/contrasts/contrast_04_inputs/contrast_04_input_build_audit.tsv \
  | less -S
```

Expected counts:

```text
tables: 24
F5 figures: 12
overlay-tiered gene TSVs: 36
```

---

## Non-Goals

This script does not:

* create `contrast_04_outputs/`
* generate synthesis seed outputs
* compress a final `.tar.gz`
* modify source global cross-run tables
* modify `results/`
* perform biological interpretation
* perform clinical interpretation
* infer missing overlay data
* include unrelated F3/F4 figures
* include unrelated runtime/provenance tables
* canonicalize missing gene symbols

---

## Future Follow-Up

After validation, a separate packaging step may copy or package `contrast_04_inputs/` into a transport-ready `contrast_04_analysis_bundle/` or `.tar.gz` without returning to raw `results/`.


```bash
tar -czf \
docs/case_studies/cross_runs/contrasts/contrast_04_analysis_bundle.tar.gz \
-C docs/case_studies/cross_runs/contrasts \
contrast_04_inputs
```

Inspect it:

```bash
tar -tzf docs/case_studies/cross_runs/contrasts/contrast_04_analysis_bundle.tar.gz | less
```

Quick size check:

```bash
ls -lh docs/case_studies/cross_runs/contrasts/contrast_04_analysis_bundle.tar.gz
```
