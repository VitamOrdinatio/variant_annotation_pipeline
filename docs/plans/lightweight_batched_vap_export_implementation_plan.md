# Lightweight Batched VAP Export Implementation Plan

## Goal

Implement a manifest-driven workflow for lightweight extraction of completed VAP runs from MARK and safe restoration into the sys76 VAP repository.

The workflow is intended to support cohort-scale analysis where many completed VAP run folders exist on MARK, but only lightweight artifacts should be moved to sys76.

The attached example run tree shows why this is necessary: many useful artifacts are small, while BAM, VCF, and large TSV outputs can range from hundreds of MB to many GB. `.duckdb` files may be under the size threshold but must still be excluded by policy.

---

## Deliverables

Implement two scripts:

```text
scripts/mark/export_lightweight_vap_runs.py
scripts/local/restore_lightweight_vap_exports.py
```

Add supporting documentation:

```text
docs/contracts/lightweight_batched_vap_export_contract.md
docs/plans/lightweight_batched_vap_export_implementation_plan.md
```

Optional future tests:

```text
tests/test_lightweight_vap_export.py
tests/test_lightweight_vap_restore.py
```

---

# Phase 1: MARK Export Script

## Step 1. Add CLI argument parsing

The script should accept one required positional argument:

`python scripts/mark/export_lightweight_vap_runs.py path/to/manifest.tsv`

Optional future arguments may include:

```bash
--max-file-mb 50
--max-batch-mb 100
--export-root /root/Desktop/vap/batched_exports
```

For first implementation, defaults should be hardcoded or exposed as constants.

---

## Step 2. Establish export timestamp

Create one timestamp per script execution:

```python
YYYY_MM_DD_HHMMSS
```

Use this timestamp for all output manifests, logs, and compressed archive names.

---

## Step 3. Create export directories

Ensure these directories exist:

```text
/root/Desktop/vap/batched_exports/lightweight_runs/
/root/Desktop/vap/batched_exports/compressed/
/root/Desktop/vap/batched_exports/manifests/
/root/Desktop/vap/batched_exports/logs/
```

Do not delete or clean existing directories.

---

## Step 4. Copy input manifest

Copy the passed-in manifest unchanged to:

`/root/Desktop/vap/batched_exports/manifests/input_manifest_<timestamp>.tsv`

---

## Step 5. Initialize logging

Write a timestamped log to:

`/root/Desktop/vap/batched_exports/logs/export_<timestamp>.log`

Log:

- script invocation
- repo root
- input manifest path
- copied manifest path
- export root
- file-size threshold
- batch-size threshold
- each run status
- warnings
- failures

---

## Step 6. Read and validate manifest

Read the input TSV.

Required columns:

```text
SRA_accn
VAP_run_id
```

Optional columns:

```text
Depth_Category
```

If required columns are missing, fail early with a clear error message.

Do not silently infer missing fields.

---

## Step 7. Process each manifest row

For each row:

1. Resolve source directory:

`results/<VAP_run_id>/`

2. Resolve destination directory:

`/root/Desktop/vap/batched_exports/lightweight_runs/<VAP_run_id>/`

3. If source directory is missing:
   - record `missing_source`
   - continue to next row

4. If destination directory already exists:
   - print warning
   - log warning
   - record skipped_existing_destination
   - continue to next row

5. Otherwise, create destination directory and begin recursive lightweight copy.

---

## Step 8. Recursive lightweight copy

Walk the source run directory recursively.

For each file:

- if not regular file: skip
- if filename ends with `.duckdb`: skip
- if size is greater than or equal to 50 MB: skip
- otherwise copy to destination while preserving relative path

Use standard-library tools only:

```python
pathlib
shutil
tarfile
csv
logging
datetime
```

Recommended copy method:

```python
shutil.copy2()
```

This preserves file metadata where possible.

---

## Step 9. Track copied and skipped files

Run-level skip events must be recorded in `export_summary_<timestamp>.tsv`, not in `export_skipped_files_<timestamp>.tsv`.

Specifically:

- `missing_source` belongs in `export_summary.run_status`
- `skipped_existing_destination` belongs in `export_summary.run_status`

The skipped-files manifest should contain only file-level skips encountered during recursive traversal.

Populate in-memory records for:

```text
export_summary
export_file_manifest
export_skipped_files
```

Track per run:

```text
files_copied
files_skipped_size
files_skipped_duckdb
files_skipped_other
bytes_copied
```

---

## Step 10. Write initial manifests

After copy phase, write:

```text
export_summary_<timestamp>.tsv
export_file_manifest_<timestamp>.tsv
export_skipped_files_<timestamp>.tsv
```

The export summary may be updated after compression to include archive paths and sizes.

---

## Step 11. Create per-run compressed archives

For each successfully copied run directory:

Input:

`/root/Desktop/vap/batched_exports/lightweight_runs/<VAP_run_id>/`

Output:

`/root/Desktop/vap/batched_exports/compressed/<VAP_run_id>_<timestamp>.tar.gz`

Important archive structure:

The archive should contain:

`run_<id>/`

not the absolute MARK path.

Example archive contents:

- `run_2026_05_27_233524/metadata/run_metadata.json`
- `run_2026_05_27_233524/metrics/stage_metrics_long.tsv`
- `run_2026_05_27_233524/figures/figure_manifest.tsv`

---

## Step 12. Create 100 MB transport batches

Pack run-level `.tar.gz` archives into `.tar` batch archives.

Output format:

- `vap_lightweight_batch_<timestamp>_001.tar`
- `vap_lightweight_batch_<timestamp>_002.tar`

Batching behavior:

- Add run-level archives sequentially.
- Keep total batch size less than or equal to 100 MB where possible.
- If adding an archive would exceed 100 MB, start a new batch.
- If a single run-level archive exceeds 100 MB, place it alone in its own batch and record a warning.

---

## Step 13. Finalize export summary

Update export summary with:

```text
compressed_run_archive
compressed_run_archive_bytes
batch_archive
warning
```

Rewrite:

`export_summary_<timestamp>.tsv`

---

## Step 14. Console summary

Print a concise final summary:

```text
Export complete.
Timestamp: <timestamp>
Runs copied: N
Runs skipped: N
Batch archives written: N
Download from: /root/Desktop/vap/batched_exports/compressed/
Manifests: /root/Desktop/vap/batched_exports/manifests/
Log: /root/Desktop/vap/batched_exports/logs/export_<timestamp>.log
```

---

# Phase 2: sys76 Restore Script

## Step 1. Add CLI argument parsing

The restore script accepts one required positional argument:

```bash
python scripts/local/restore_lightweight_vap_exports.py path/to/downloaded/compressed/
```

This path should contain one or more batch `.tar` files.

Upon script invocation, check machine hostname:

```bash
hostname
```

If `hostname` returns `VandPyMolGPUResearch`, abort the sys76 Restore Script, and write to console.

---

## Step 2. Establish restore timestamp

Create one restore timestamp:

```text
YYYY_MM_DD_HHMMSS
```

Use it for:

```text
logs/lightweight_restore/restore_<timestamp>.log
logs/lightweight_restore/restore_summary_<timestamp>.tsv
```

---

## Step 3. Validate restore context

The script should be run from the sys76 VAP repository root.

Confirm that the current directory contains expected repo markers, such as:

```text
results/
scripts/
```

If not, warn or fail clearly.

---

## Step 4. Discover batch archives

Find files matching:

```text
vap_lightweight_batch_*.tar
```

inside the provided input directory.

Process in sorted order.

---

## Step 5. Extract batch archives to temporary staging

Create a temporary staging directory, preferably under:

```text
/tmp/
```

Example:

```text
/tmp/vap_lightweight_restore_<timestamp>/
```

Extract each batch `.tar` there.

Expected extracted files:

`run_<id>.tar.gz`

---

## Step 5A. Enforce safe archive extraction

Before extracting either a batch `.tar` archive or a run-level `.tar.gz` archive, inspect all archive members.

Reject archive members if:

- the member path is absolute
- the member path contains `..`
- the resolved destination path would fall outside the intended extraction directory

If unsafe archive contents are detected:

- do not extract that archive
- print a warning
- log the warning
- record restore status as `failed`

---

## Step 6. Restore each run archive

For each run-level `.tar.gz` archive:

1. Infer `VAP_run_id` from archive name.
2. Set destination:

`results/<VAP_run_id>/`

3. If destination already exists:
   - print warning
   - log warning
   - record skipped_existing_destination
   - do not extract

4. Otherwise, extract archive into:

`results/`

Expected final structure:

`results/run_<id>/`

---

## Step 7. Write restore summary

Write:

`logs/lightweight_restore/restore_summary_<timestamp>.tsv`

Recommended columns:

```text
restore_timestamp
batch_archive
compressed_run_archive
VAP_run_id
destination_run_dir
restore_status
warning
```

Allowed restore statuses:

```text
restored
skipped_existing_destination
failed
```

---

## Step 8. Console summary

Print:

```text
Restore complete.
Timestamp: <timestamp>
Runs restored: N
Runs skipped: N
Summary: logs/lightweight_restore/restore_summary_<timestamp>.tsv
Log: logs/lightweight_restore/restore_<timestamp>.log
```

---

# Phase 3: Minimal Testing Strategy

## Test 1. Export preserves relative structure

Create a fixture run directory:

```text
results/run_test_001/metadata/a.json
results/run_test_001/metrics/b.tsv
```

Confirm export creates:

```text
/root/Desktop/vap/batched_exports/lightweight_runs/run_test_001/metadata/a.json
/root/Desktop/vap/batched_exports/lightweight_runs/run_test_001/metrics/b.tsv
```

---

## Test 2. Export excludes large files

Create a file at or above the threshold.

Confirm it is skipped and recorded in:

`export_skipped_files_<timestamp>.tsv`

---

## Test 3. Export excludes .duckdb

Create:

`results/run_test_001/logs/stage12_exploration/test.duckdb`

Confirm it is skipped even if below 50 MB.

---

## Test 4. Export refuses overwrite

Create destination directory before export:

`/root/Desktop/vap/batched_exports/lightweight_runs/run_test_001/`

Confirm the script skips the run and records:

`skipped_existing_destination`

---

## Test 5. Restore refuses overwrite

Create:

`results/run_test_001/`

Then attempt restore.

Confirm the restore script skips extraction and records:

`skipped_existing_destination`

---

# Phase 4: Recommended Commit

After implementing scripts and docs:

```bash
git add scripts/mark/export_lightweight_vap_runs.py \
        scripts/local/restore_lightweight_vap_exports.py \
        docs/contracts/lightweight_batched_vap_export_contract.md \
        docs/plans/lightweight_batched_vap_export_implementation_plan.md

git commit -m "Add lightweight batched VAP export design"
```

If implementation is included in the same commit:

```bash
git commit -m "Add lightweight batched VAP export workflow"
```

---

# Design Notes

The export and restore responsibilities should remain separated.

The MARK-side script should not attempt to manage sys76 filesystem behavior.

The sys76-side script should enforce local no-overwrite behavior during restore.

The passed-in manifest, export summaries, skipped-file reports, logs, run archives, and batch archives should all share a common timestamp to preserve auditability.

The outer batch archive should be a `.tar`, while each run-level archive should be `.tar.gz`. This keeps run-level compression lossless and makes 100 MB batching easier to reason about.