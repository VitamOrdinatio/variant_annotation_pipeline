# Implementation Plan — `scripts/build_contrast_02_inputs.py`

## Objective

Build a deterministic sys76-local script that prepares the governed input substrate for:

```text
Contrast 02 — Interoperability Substrate Stability
```

The script will re-array selected VAP outputs and cross-run tables into:

```text
docs/case_studies/cross_runs/contrasts/contrast_02_inputs/
```

The purpose is to create a compact, self-contained, high-semantic-density input substrate suitable for downstream JEN contrast synthesis.

This script prepares the input substrate only. It does not create final synthesis outputs and does not perform interpretation.

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
docs/case_studies/cross_runs/contrasts/contrast_02_inputs/
```

---

## Script Location

```text
scripts/build_contrast_02_inputs.py
```

---

## Execution Context

Run from VAP repository root on sys76:

```bash
python scripts/build_contrast_02_inputs.py
```

The script assumes the sys76 repository contains the required lightweight `results/run_<id>/` directories and global cross-run tables.

---

## Source Immutability Rule

The script may read and copy from:

```text
results/
docs/case_studies/cross_runs/cross_run_tables/
docs/case_studies/cross_runs/contrasts/contrast_02_inputs/cohort_manifest.tsv
```

The script must never modify, overwrite, delete, move, or patch anything inside:

```text
results/
```

The script may write only inside:

```text
docs/case_studies/cross_runs/contrasts/contrast_02_inputs/
```

Within `contrast_02_inputs/`, the script may create or overwrite derived files that it owns.

---

## Canonical Manifest

The script is manifest-driven.

Input manifest:

```text
docs/case_studies/cross_runs/contrasts/contrast_02_inputs/cohort_manifest.tsv
```

Expected uploaded/current columns:

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

Contrast 02 currently includes 12 WES epilepsy SRAs and intentionally excludes HG002 WGS.

The script must not auto-discover additional runs.

---

## Output Directory Structure

The generated input substrate should have this structure:

```text
docs/case_studies/cross_runs/contrasts/contrast_02_inputs/
├── cohort_manifest.tsv
├── contrast_02_input_build_audit.tsv
├── README.md
│
├── ERR10619203/
│   ├── figures/
│   ├── tables/
│   └── sql_outputs/
│       ├── targeted_semantic_buckets/
│       └── tiered_gene_outputs/
│
├── ERR10619207/
│   └── ...
│
└── ERR10619330/
    └── ...
```

Each SRA directory should contain only the selected Contrast 02 input substrate.

---

## Required Per-SRA Figure Layer

Note: the contract uses the shorthand singular filename `f5_interoperability_substrate.png`, but current VAP figure exports use:

```text
<SRA>_f5_interoperability_substrates.png
```

The script should preserve the actual source filename and must not rename it.

For each manifest row, copy the F5 interoperability figure:

Source:

```text
results/<run_id>/figures/<SRA>_f5_interoperability_substrates.png
```

Destination:

```text
contrast_02_inputs/<SRA>/figures/<SRA>_f5_interoperability_substrates.png
```

Do not rename the file.

If missing, record absence in the audit.

---

## Required Per-SRA Table Layer

The following global cross-run tables should be subset by `run_id` and written into each SRA-specific `tables/` directory without renaming:

```text
candidate_reviewability_readiness.tsv
overlay_gene_coding_clinical_evidence.tsv
overlay_gene_coding_frequency_profiles.tsv
overlay_gene_coding_functional_impact.tsv
substrate_dimension_summary.tsv
gene_list_overlay_intersections.tsv
```

Source directory:

```text
docs/case_studies/cross_runs/cross_run_tables/
```

Destination pattern:

```text
contrast_02_inputs/<SRA>/tables/<same_filename>
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

## SQL Output Layer

Each SRA should have:

```text
sql_outputs/
├── targeted_semantic_buckets/
└── tiered_gene_outputs/
```

---

## Targeted Semantic Buckets

Copy available semantic bucket TSVs from:

```text
results/<run_id>/logs/stage12_exploration/lane_candidate_slices/
```

to:

```text
contrast_02_inputs/<SRA>/sql_outputs/targeted_semantic_buckets/
```

Expected first-pass bucket classes include:

```text
<SRA>_bucket_1a_validation_routed_epilepsy_mito.tsv
<SRA>_bucket_1b_clinically_contextualized_epilepsy_mito.tsv
<SRA>_bucket_2a_rare_impact_coding_triage_summary.tsv
<SRA>_bucket_2b_rare_impact_tier2.tsv
<SRA>_bucket_2c_rare_impact_deprioritized.tsv
```

Provisional later-stage bucket classes may also be copied if present:

```text
<SRA>_bucket_3a_candidate_reviewability.tsv
<SRA>_bucket_3b_overlay_density.tsv
<SRA>_bucket_4a_interoperability_substrate_summary.tsv
```

Current source runs may instead contain legacy/existing names such as:

```text
<SRA>_bucket_3a_clinvar_supported_deprioritized.tsv
<SRA>_bucket_3b_tier3_background_summary.tsv
<SRA>_bucket_4a_representative_noncoding_semantic_exemplars.tsv
```

The script should copy all `.tsv` files present in `lane_candidate_slices/` without renaming them, while the audit records which expected/provisional bucket classes are present or absent.

Do not fail if provisional bucket classes are absent.

---

## Tiered Gene Outputs

Copy tier-specific unique-gene outputs from:

```text
results/<run_id>/logs/stage12_exploration/unique_genes/
```

to:

```text
contrast_02_inputs/<SRA>/sql_outputs/tiered_gene_outputs/
```

Required source files:

```text
<SRA>_tier1_unique_genes.tsv
<SRA>_tier2_unique_genes.tsv
<SRA>_tier3_unique_genes.tsv
```

Destination filenames should be normalized to the contract-facing names:

```text
tier1_unique_genes.tsv
tier2_unique_genes.tsv
tier3_unique_genes.tsv
```

Rationale:

* These are contract-defined per-SRA exports.
* The SRA identity is already encoded by the destination directory.
* This improves artifact isomorphism across SRA folders.

If any required tier file is missing, record absence in the audit.

Optional overlay-specific tier files may be ignored for first-pass Contrast 02 unless explicitly required later.

---

## Root-Level Files

### `cohort_manifest.tsv`

The manifest may retain its current source column names. The script normalizes these names internally for execution, but does not rewrite the manifest.

Preserve the existing manifest at:

```text
contrast_02_inputs/cohort_manifest.tsv
```

The script should read this file but should not rewrite it unless a future normalization option is explicitly added.

### `README.md`

If missing, the script may create a compact placeholder README.

If already present, the script should not overwrite it by default.

### `contrast_02_input_build_audit.tsv`

The script should write:

```text
contrast_02_inputs/contrast_02_input_build_audit.tsv
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

* copied F5 figure
* subset candidate reviewability table
* subset overlay clinical table
* copied tier1 unique genes
* missing tier3 unique genes
* copied bucket TSV
* skipped optional provisional bucket

---

## Safety and Rebuild Behavior

The script may safely overwrite files it previously generated inside:

```text
contrast_02_inputs/<SRA>/
contrast_02_inputs/contrast_02_input_build_audit.tsv
```

The script must not delete the whole `contrast_02_inputs/` directory.

The script must not delete or modify:

```text
contrast_02_inputs/cohort_manifest.tsv
```

The script must not write outside:

```text
docs/case_studies/cross_runs/contrasts/contrast_02_inputs/
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
python scripts/build_contrast_02_inputs.py
```

Expected root files:

```text
contrast_02_inputs/cohort_manifest.tsv
contrast_02_inputs/contrast_02_input_build_audit.tsv
contrast_02_inputs/README.md
```

Expected per-SRA directories:

```text
12 SRA directories
```

Expected per-SRA subdirectories:

```text
figures/
tables/
sql_outputs/targeted_semantic_buckets/
sql_outputs/tiered_gene_outputs/
```

Expected per-SRA tables:

```text
6 tables
```

Expected per-SRA tiered gene files:

```text
3 files
```

Expected per-SRA F5 figures:

```text
1 PNG figure
```

Expected targeted semantic bucket files:

```text
copy all available .tsv files from lane_candidate_slices/
```

Quick validation commands:

```bash
find docs/case_studies/cross_runs/contrasts/contrast_02_inputs \
  -maxdepth 1 -type d | sort

find docs/case_studies/cross_runs/contrasts/contrast_02_inputs \
  -path "*/tables/*.tsv" | wc -l

find docs/case_studies/cross_runs/contrasts/contrast_02_inputs \
  -path "*/figures/*f5_interoperability_substrates.png" | wc -l

find docs/case_studies/cross_runs/contrasts/contrast_02_inputs \
  -path "*/sql_outputs/tiered_gene_outputs/*.tsv" | wc -l

column -t -s $'\t' \
  docs/case_studies/cross_runs/contrasts/contrast_02_inputs/contrast_02_input_build_audit.tsv \
  | less -S
```

Expected counts:

```text
tables: 72
F5 figures: 12
tiered gene outputs: 36
```

Targeted semantic bucket count may vary depending on which bucket classes exist in current run exports.

---

## Non-Goals

This script does not:

* create `contrast_02_outputs/`
* generate synthesis seed outputs
* compress the final `.tar.gz`
* modify source global cross-run tables
* modify `results/`
* perform biological interpretation
* perform clinical interpretation
* rename global cross-run table files
* infer missing biological data

---

## Future Follow-Up

After validating `contrast_02_inputs/`, a separate packaging step may create:

```text
contrast_02_analysis_bundle.tar.gz
```

or a transport-ready input bundle.

That packaging step should consume only the governed `contrast_02_inputs/` directory, not raw `results/`.


## Relationship to Contract Bundle Root

The Contrast 02 I/O contract describes the transport-ready root as:

```text
contrast_02_analysis_bundle/
```

This implementation intentionally prepares the upstream governed input substrate first:

```text
contrast_02_inputs/
```

After validation, a separate packaging step may copy or package `contrast_02_inputs/` into a transport-ready `contrast_02_analysis_bundle/` or `.tar.gz` without returning to raw `results/`.


```bash
tar -czf \
docs/case_studies/cross_runs/contrasts/contrast_02_analysis_bundle.tar.gz \
-C docs/case_studies/cross_runs/contrasts \
contrast_02_inputs
```

Inspect it:

```bash
tar -tzf docs/case_studies/cross_runs/contrasts/contrast_02_analysis_bundle.tar.gz | less
```

Quick size check:

```bash
ls -lh docs/case_studies/cross_runs/contrasts/contrast_02_analysis_bundle.tar.gz
```