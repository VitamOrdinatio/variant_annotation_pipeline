# Script Contract — Stage 12 Analytical Batch Export Runner

## Purpose

Define a manifest-driven batch runner that executes the existing single-run Stage 12 DuckDB export script across multiple VAP run directories.

The batch runner coordinates repeated execution of:

```text
scripts/analysis/export_stage12_duckdb_exploration.py
```

against many completed VAP runs listed in a TSV manifest.

This script does not perform Stage 12 SQL export logic itself. It only orchestrates per-run execution, tracks provenance, prevents accidental overwrites, and writes batch-level logs and summaries.

---

# Target Script

```text
scripts/analysis/run_stage12_duckdb_exports_from_manifest.py
```

---

# Input Manifest Contract

The script accepts one required positional argument:

```text
path/to/stage12_analytical_batch_export_manifest.tsv
```

Recommended location:

```text
data/reference/stage12_analytical_batch_exports/manifests/
```

Required manifest columns:

```text
SRA_accn
VAP_run_id
```

Recommended optional column:

```text
Depth_Category
```

Example:

```tsv
SRA_accn	VAP_run_id	Depth_Category
ERR10619203	run_2026_05_30_071639	q3
ERR10619281	run_2026_05_27_233524	median
ERR10619330	run_2026_06_01_203130	q1
```

---

# Canonical Invocation

From VAP repo root:

```bash
python scripts/analysis/run_stage12_duckdb_exports_from_manifest.py \
  data/reference/stage12_analytical_batch_exports/manifests/stage12_analytical_batch_export_manifest.tsv
```

---

# Batch Output Directory Contract

The batch runner writes batch-level artifacts to:

```text
data/reference/stage12_analytical_batch_exports/
```

with this structure:

```text
data/reference/stage12_analytical_batch_exports/
├── manifests/
│   ├── stage12_analytical_batch_export_manifest.tsv
│   └── <manifest_stem>_<timestamp>.tsv
├── summaries/
│   └── <manifest_stem>_summary_<timestamp>.tsv
└── logs/
    └── <manifest_stem>_<timestamp>.log
```

The timestamp must be shared across all three generated batch artifacts.

---

# Per-Run Output Contract

The batch runner must not choose per-run output paths directly.

Instead, for each manifest row, it calls:

```bash
python scripts/analysis/export_stage12_duckdb_exploration.py \
  results/<VAP_run_id>/processed/stage_12_validation_candidates.tsv
```

The single-run exporter remains responsible for writing:

```text
results/<VAP_run_id>/logs/stage12_exploration/
```

including:

* DuckDB file
* value counts
* unique genes
* LANE candidate slices
* per-run manifest
* per-run log

---

# Overwrite Policy

Default behavior must be conservative.

Before running a row, the batch runner checks for key completion artifacts, not merely the existence of the `stage12_exploration/` directory.

A row is considered already exported only if these completion artifacts exist:

- `results/<VAP_run_id>/logs/stage12_exploration/stage12_exploration_manifest.tsv`
- `results/<VAP_run_id>/logs/stage12_exploration/stage12_exploration_duckdb.log`

Optionally, the batch runner may also check for the expected DuckDB file:

- `results/<VAP_run_id>/logs/stage12_exploration/<SRA_accn>_stage12_exploration.duckdb`

If key completion artifacts already exist, the row is skipped by default and logged.

Recommended status values:

```text
completed
skipped_existing_outputs
failed
missing_input_tsv
completed_with_warnings
```

A future optional `--force` flag may allow rerunning and overwriting generated per-run outputs, but this is not required for the first implementation.

---

# Batch Provenance Contract

For every batch execution, the script must write:

1. A timestamped copy of the input manifest.
2. A batch summary TSV.
3. A batch log.

The timestamped manifest snapshot preserves the exact input request.

The summary TSV records the outcome of every manifest row.

The log records operational detail, including skipped rows, executed commands, return codes, and detected existing outputs.

---

# Batch Summary Required Columns

The batch summary TSV should include:

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

---

# Safety Guarantees

The batch runner must:

1. Never modify original Stage 12 TSVs.
2. Never duplicate single-run SQL logic.
3. Never silently overwrite existing per-run outputs.
4. Continue processing remaining rows if one row fails.
5. Preserve the exact input manifest used for each batch execution.
6. Never modify the original user-created manifest TSV.

---

# Design Principle

The single-run exporter is the authoritative export engine.

The batch runner is only a manifest-driven coordinator.

```text
manifest TSV
→ batch runner
→ repeated single-run exporter calls
→ per-run Stage12 exports
→ batch summary/log/provenance snapshot
```
