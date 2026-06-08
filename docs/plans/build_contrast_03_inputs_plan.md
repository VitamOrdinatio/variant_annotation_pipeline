# Implementation Plan — `scripts/analysis/build_contrast_03_inputs.py`

## Objective

Build a deterministic sys76-local script that prepares the governed input substrate for:

```text
Contrast 03 — Runtime Telemetry vs Sequencing Depth
```

The script will re-array selected VAP runtime/provenance artifacts and cross-run telemetry tables into:

```text
docs/case_studies/cross_runs/contrasts/contrast_03_inputs/
```

The purpose is to create a compact, self-contained, high-semantic-density input substrate suitable for downstream JEN runtime telemetry synthesis.

This script prepares the input substrate only. It does not create synthesis outputs, does not compress a bundle, and does not perform interpretation.

---

## Contrast 03 Scope

Contrast 03 evaluates VAP as an infrastructure system by asking how runtime telemetry and execution observability behave across sequencing depth strata.

Primary analytical questions include:

* Which stages scale most strongly with sequencing depth?
* Are runtime bottlenecks preserved across runs?
* Does telemetry behavior appear predictable across Q1, median, and Q3 WES executions?
* Are any runs operational outliers?
* Does stage-level observability remain stable?

---

## Required Inputs

Contrast 03 input substrate requires four compact artifact classes.

### Cross-run global tables requiring SRA-specific subsetting

```text
docs/case_studies/cross_runs/cross_run_tables/runtime_stage_summary.tsv
docs/case_studies/cross_runs/cross_run_tables/provenance_summary.tsv
```

These tables are subset by exact `run_id` and written to each SRA-specific `tables/` directory.

### Cross-run depth metadata requiring SRA-specific subsetting

```text
docs/case_studies/cross_runs/cross_run_tables/sra_run_depth_metadata.tsv
```

This table is subset by exact `SRA` and written to each SRA-specific `metadata/` directory as:

```text
sra_run_depth_metadata.tsv
```

Expected source columns:

```text
SRA
Read Count
Rank
Rank_%
Depth Category
```

### Run-specific metadata files copied directly from `results/<run_id>/metadata/`

```text
config_snapshot.yaml
run_fingerprint.json
run_metadata.json
runtime_profile.tsv
```

These files are copied without modification into each SRA-specific `metadata/` directory.

### Continuity probe outputs copied from Stage 12 exploration

Continuity probe files are copied without renaming and without content modification. Missing gene-symbol canonicalization is not performed here because Contrast 03 uses these files as continuity probes rather than gene-symbol analysis substrate.

Source:

```text
results/<run_id>/logs/stage12_exploration/unique_genes/
```

Required files:

```text
<SRA>_tier1_unique_genes.tsv
<SRA>_tier2_unique_genes.tsv
<SRA>_tier3_unique_genes.tsv
```

Destination:

```text
contrast_03_inputs/<SRA>/continuity_probes/
```

Files should be copied without renaming unless a later contract revision explicitly requires normalized destination names.

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
docs/case_studies/cross_runs/contrasts/contrast_03_inputs/
```

---

## Script Location

```text
scripts/analysis/build_contrast_03_inputs.py
```

---

## Execution Context

Run from VAP repository root on sys76:

```bash
python scripts/analysis/build_contrast_03_inputs.py
```

The script assumes the sys76 repository contains the required lightweight `results/run_<id>/` directories and global cross-run tables.

---

## Source Immutability Rule

The script may read and copy/subset from:

```text
results/
docs/case_studies/cross_runs/cross_run_tables/runtime_stage_summary.tsv
docs/case_studies/cross_runs/cross_run_tables/provenance_summary.tsv
docs/case_studies/cross_runs/cross_run_tables/sra_run_depth_metadata.tsv
docs/case_studies/cross_runs/contrasts/contrast_03_inputs/cohort_manifest.tsv
```

The script must never modify, overwrite, delete, move, or patch anything inside:

```text
results/
```

The script may write only inside:

```text
docs/case_studies/cross_runs/contrasts/contrast_03_inputs/
```

Within `contrast_03_inputs/`, the script may create or overwrite derived files that it owns.

The script must not overwrite:

```text
contrast_03_inputs/cohort_manifest.tsv
```

---

## Canonical Manifest

The script is manifest-driven.

Input manifest:

```text
docs/case_studies/cross_runs/contrasts/contrast_03_inputs/cohort_manifest.tsv
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

Contrast 03 currently includes 12 WES epilepsy SRAs and intentionally excludes HG002 WGS.

The script must not auto-discover additional runs.

The script should enforce:

```text
len(manifest) == 12
```

---

## Output Directory Structure

The generated input substrate should have this structure:

```text
docs/case_studies/cross_runs/contrasts/contrast_03_inputs/
├── cohort_manifest.tsv
├── contrast_03_input_build_audit.tsv
├── README.md
│
├── ERR10619203/
│   ├── tables/
│   │   ├── runtime_stage_summary.tsv
│   │   └── provenance_summary.tsv
│   │
│   ├── metadata/
│   │   ├── config_snapshot.yaml
│   │   ├── run_fingerprint.json
│   │   ├── run_metadata.json
│   │   ├── runtime_profile.tsv
│   │   └── sra_run_depth_metadata.tsv
│   │
│   └── continuity_probes/
│       ├── ERR10619203_tier1_unique_genes.tsv
│       ├── ERR10619203_tier2_unique_genes.tsv
│       └── ERR10619203_tier3_unique_genes.tsv
│
├── ERR10619207/
│   └── [same structure]
│
└── ERR10619330/
    └── [same structure]
```

Each SRA directory should contain only selected Contrast 03 input substrate.

---

## Required Per-SRA Table Layer

The following global cross-run tables should be subset by `run_id` and written into each SRA-specific `tables/` directory without renaming:

```text
runtime_stage_summary.tsv
provenance_summary.tsv
```

Source directory:

```text
docs/case_studies/cross_runs/cross_run_tables/
```

Destination pattern:

```text
contrast_03_inputs/<SRA>/tables/<same_filename>
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

## Required Per-SRA Metadata Layer

Copy the following files from:

```text
results/<run_id>/metadata/
```

to:

```text
contrast_03_inputs/<SRA>/metadata/
```

Required copied files:

```text
config_snapshot.yaml
run_fingerprint.json
run_metadata.json
runtime_profile.tsv
```

Also subset:

```text
docs/case_studies/cross_runs/cross_run_tables/sra_run_depth_metadata.tsv
```

by exact `SRA`, and write:

```text
contrast_03_inputs/<SRA>/metadata/sra_run_depth_metadata.tsv
```

If any metadata file is missing, record `missing_source` in the audit.

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
contrast_03_inputs/cohort_manifest.tsv
```

The script should read this file but must not rewrite it.

### `README.md`

If missing, the script may create a compact placeholder README.

If already present, the script should not overwrite it by default.

### `contrast_03_input_build_audit.tsv`

The script should write:

```text
contrast_03_inputs/contrast_03_input_build_audit.tsv
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

* subset runtime stage summary
* subset provenance summary
* subset SRA read-depth metadata
* copied config snapshot
* copied run fingerprint
* copied run metadata
* copied runtime profile
* copied tier1/tier2/tier3 continuity probe
* ensured SRA directory
* zero-row subset

---

## Safety and Rebuild Behavior

The script may safely overwrite files it previously generated inside:

```text
contrast_03_inputs/<SRA>/
contrast_03_inputs/contrast_03_input_build_audit.tsv
```

The script must not delete the whole `contrast_03_inputs/` directory.

The script must not delete or modify:

```text
contrast_03_inputs/cohort_manifest.tsv
```

The script must not write outside:

```text
docs/case_studies/cross_runs/contrasts/contrast_03_inputs/
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
python scripts/analysis/build_contrast_03_inputs.py
```

Expected root files:

```text
contrast_03_inputs/cohort_manifest.tsv
contrast_03_inputs/contrast_03_input_build_audit.tsv
contrast_03_inputs/README.md
```

Expected per-SRA directories:

```text
12 SRA directories
```

Expected per-SRA subdirectories:

```text
tables/
metadata/
continuity_probes/
```

Expected per-SRA tables:

```text
2 files
```

Expected per-SRA metadata files:

```text
5 files
```

Expected per-SRA continuity probe files:

```text
3 files
```

Quick validation commands:

```bash
find docs/case_studies/cross_runs/contrasts/contrast_03_inputs \
  -maxdepth 1 -type d | sort

find docs/case_studies/cross_runs/contrasts/contrast_03_inputs \
  -path "*/tables/*.tsv" | wc -l

find docs/case_studies/cross_runs/contrasts/contrast_03_inputs \
  -path "*/metadata/*" -type f | wc -l

find docs/case_studies/cross_runs/contrasts/contrast_03_inputs \
  -path "*/continuity_probes/*.tsv" | wc -l

column -t -s $'\t' \
  docs/case_studies/cross_runs/contrasts/contrast_03_inputs/contrast_03_input_build_audit.tsv \
  | less -S
```

Expected counts:

```text
tables: 24
metadata files: 60
continuity probe TSVs: 36
```

No F2 figures are required for the current Contrast 03 input substrate.

---

## Non-Goals

This script does not:

* create `contrast_03_outputs/`
* generate synthesis seed outputs
* compress a final `.tar.gz`
* modify source global cross-run tables
* modify `results/`
* perform biological interpretation
* perform clinical interpretation
* infer missing runtime telemetry
* include unrelated figures such as F3, F4, or F5
* include unrelated tables from other contrast domains

---

## Future Follow-Up

After validating `contrast_03_inputs/`, a separate packaging step may create:

```text
contrast_03_analysis_bundle.tar.gz
```

or a transport-ready input bundle.

That packaging step should consume only the governed `contrast_03_inputs/` directory, not raw `results/`.



After validation, a separate packaging step may copy or package `contrast_03_inputs/` into a transport-ready `contrast_03_analysis_bundle/` or `.tar.gz` without returning to raw `results/`.


```bash
tar -czf \
docs/case_studies/cross_runs/contrasts/contrast_03_analysis_bundle.tar.gz \
-C docs/case_studies/cross_runs/contrasts \
contrast_03_inputs
```

Inspect it:

```bash
tar -tzf docs/case_studies/cross_runs/contrasts/contrast_03_analysis_bundle.tar.gz | less
```

Quick size check:

```bash
ls -lh docs/case_studies/cross_runs/contrasts/contrast_03_analysis_bundle.tar.gz
```