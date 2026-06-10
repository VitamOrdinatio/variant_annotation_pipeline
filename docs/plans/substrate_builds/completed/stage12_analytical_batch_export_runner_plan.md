# Implementation Plan — Stage 12 Analytical Batch Export Runner

## Purpose

Implement a lightweight Python wrapper that reads a TSV manifest of VAP runs and executes the Stage 12 DuckDB export harness once per listed run.

This enables deterministic batch harvesting across multiple WES SRAs without manually invoking the single-run exporter repeatedly.

---

# Target Script

```text
scripts/analysis/run_stage12_duckdb_exports_from_manifest.py
```

---

# Canonical Invocation

From VAP repo root:

```bash
python scripts/analysis/run_stage12_duckdb_exports_from_manifest.py \
  data/reference/stage12_analytical_batch_exports/manifests/stage12_analytical_batch_export_manifest.tsv
```

---

# Directory Setup

Create the tracked reference directory structure:

```text
data/reference/stage12_analytical_batch_exports/
├── manifests/
├── summaries/
└── logs/
```

The user-created manifest should live in:

```text
data/reference/stage12_analytical_batch_exports/manifests/
```

---

# Manifest Format

Required columns:

```text
SRA_accn
VAP_run_id
```

Recommended column:

```text
Depth_Category
```

The script should tolerate missing `Depth_Category` by writing an empty value in the summary.

---

# Execution Flow

## Step 1 — Parse Arguments

Accept one required positional argument:

```text
manifest_tsv
```

Resolve it to an absolute path and confirm it exists.

---

## Step 2 — Create Batch Timestamp

Create one UTC timestamp at script start.

Recommended format:

```text
YYYY_MM_DD_HHMMSS
```

Use the same timestamp for:

```text
<manifest_stem>_<timestamp>.tsv
<manifest_stem>_summary_<timestamp>.tsv
<manifest_stem>_<timestamp>.log
```

---

## Step 3 — Create Batch Output Paths

These paths are resolved relative to the current VAP repo root / current working directory. The batch runner should be executed from VAP repo root.

Given:

```text
manifest_stem = input manifest filename without .tsv
```

write:

```text
data/reference/stage12_analytical_batch_exports/manifests/<manifest_stem>_<timestamp>.tsv
data/reference/stage12_analytical_batch_exports/summaries/<manifest_stem>_summary_<timestamp>.tsv
data/reference/stage12_analytical_batch_exports/logs/<manifest_stem>_<timestamp>.log
```

---

## Step 4 — Snapshot Input Manifest

Copy the user-provided manifest into:

```text
data/reference/stage12_analytical_batch_exports/manifests/<manifest_stem>_<timestamp>.tsv
```

This preserves the exact input used for the batch run.

Do not modify the original manifest.

---

## Step 5 — Read Manifest Rows

Read the manifest as TSV.

Validate required columns:

```text
SRA_accn
VAP_run_id
```

For each row, derive:

```text
input_tsv = results/<VAP_run_id>/processed/stage_12_validation_candidates.tsv
stage12_exploration_dir = results/<VAP_run_id>/logs/stage12_exploration/
```

---

## Step 6 — Preflight Per Row

Before execution, check whether the input TSV exists.

If missing:

```text
status = missing_input_tsv
action_taken = skipped
```

Log the missing input and continue.

---

## Step 7 — Existing Output Detection

Before execution, check for existing per-run completion artifacts.

Expected completion artifacts include:

- `results/<VAP_run_id>/logs/stage12_exploration/stage12_exploration_manifest.tsv`
- `results/<VAP_run_id>/logs/stage12_exploration/stage12_exploration_duckdb.log`

Optional additional check:

- `results/<VAP_run_id>/logs/stage12_exploration/<SRA_accn>_stage12_exploration.duckdb`

If key completion artifacts already exist, default behavior is:

```text
status = skipped_existing_outputs
action_taken = skipped
```

Record this in the summary and log.

Do not overwrite by default.

---

## Step 8 — Execute Single-Run Exporter

If no existing outputs are detected, run:

```bash
python scripts/analysis/export_stage12_duckdb_exploration.py \
  results/<VAP_run_id>/processed/stage_12_validation_candidates.tsv
```

Use `subprocess.run(check=False)`.

Capture:

```text
return_code
stdout
stderr
```

Write stdout/stderr to the batch log.

---

## Step 9 — Determine Row Status

If return code is nonzero:

status = failed
action_taken = attempted

If return code is 0, attempt to inspect the per-run manifest if it exists: 

- `results/<VAP_run_id>/logs/stage12_exploration/stage12_exploration_manifest.tsv`

If the per-run manifest contains a `status` value, propagate it into:

single_run_status

Then set batch-level status:

- completed if single_run_status == completed
- completed_with_warnings if single_run_status == completed_with_warnings
- completed if the manifest is unavailable but return code is 0

Continue to the next manifest row regardless.

---

## Step 10 — Write Batch Summary TSV

Write one row per manifest entry.

Recommended columns:

```text
SRA_accn
VAP_run_id
Depth_Category
input_tsv
stage12_exploration_dir
expected_duckdb
expected_run_manifest
expected_run_log
single_run_manifest_path
single_run_status
status
action_taken
reason
return_code
timestamp_utc
```

For `expected_duckdb`, the batch runner may not know the sample-derived DuckDB filename before execution unless it reads per-run metadata. Acceptable first implementation options:

1. Leave `expected_duckdb` blank.
2. Infer from `SRA_accn` as `<SRA_accn>_stage12_exploration.duckdb`.
3. Read `metadata/config_snapshot.yaml` to determine `sample_id`.

Preferred implementation:

```text
expected_duckdb = results/<VAP_run_id>/logs/stage12_exploration/<SRA_accn>_stage12_exploration.duckdb
```

because current SRA accession and sample ID are expected to match.

---

# Logging Requirements

The batch log must record:

1. Script start timestamp.
2. Manifest path.
3. Manifest snapshot path.
4. Summary path.
5. Number of rows in manifest.
6. Each row processed.
7. Input TSV path for each row.
8. Existing output detection result.
9. Command executed.
10. Return code.
11. stdout/stderr from the single-run exporter.
12. Final batch counts:

    * completed
    * skipped_existing_outputs
    * missing_input_tsv
    * failed
    * completed_with_warnings

---

# Overwrite Policy

First implementation default:

```text
no overwrite
```

If outputs already exist, skip.

Future optional enhancement:

```bash
--force
```

which would rerun the single-run exporter even if outputs already exist.

Do not implement `--force` unless needed.

---

# Git Tracking Policy

Track:

```text
scripts/analysis/run_stage12_duckdb_exports_from_manifest.py
data/reference/stage12_analytical_batch_exports/manifests/stage12_analytical_batch_export_manifest.tsv
```

Generated timestamped manifests, summaries, and logs may be tracked if they are small and useful as execution records.

Do not track bulky per-run outputs under:

```text
results/run_<id>/logs/stage12_exploration/
```

---

# Acceptance Criteria

The implementation is complete when:

1. The script runs from VAP repo root.
2. The script accepts a manifest TSV path.
3. The script snapshots the input manifest with a timestamp.
4. The script creates a timestamped batch log.
5. The script creates a timestamped batch summary TSV.
6. The script loops over all manifest rows.
7. The script invokes the existing single-run exporter for rows without prior outputs.
8. The script skips rows with existing outputs by default.
9. The script records skipped rows in both log and summary.
10. The script records failed rows without aborting the batch.
11. The script preserves the original user-created manifest.
12. The script does not duplicate Stage 12 SQL export logic.
