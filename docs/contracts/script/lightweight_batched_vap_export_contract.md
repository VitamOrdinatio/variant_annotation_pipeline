# Lightweight Batched VAP Export Contract

## Purpose

This contract defines a manifest-driven export/restore workflow for transferring lightweight VAP run artifacts from MARK to sys76 without copying large intermediate files.

The workflow is designed for cohort-scale VAP analysis where many completed `results/run_<id>/` directories exist on MARK, but only lightweight artifacts are needed locally for downstream comparative analysis.

---

## Scope

This contract covers two scripts:

1. MARK-side export script
2. sys76-side restore script

The MARK-side script prepares lightweight, compressed export bundles.

The sys76-side script restores those bundles into the local VAP repository without overwriting existing runs.

---

## MARK-Side Script

### Script Name

```text
scripts/mark/export_lightweight_vap_runs.py
```

---

### Invocation

The script must be run from the VAP repository root on MARK.

`python scripts/mark/export_lightweight_vap_runs.py path/to/manifest.tsv`

---

### Input Manifest

The script accepts a TSV manifest filepath as its required positional argument.

Required columns:

- SRA_accn
- VAP_run_id

Optional columns:

- Depth_Category

Example:

SRA_accn	VAP_run_id	Depth_Category
ERR10619203	run_2026_05_30_071639	q3
ERR10619207	run_2026_06_01_124134	q3
ERR10619208	run_2026_05_30_151355	median

---

### Source Directory

For each manifest row, the source directory is:

`results/<VAP_run_id>/`

Example:

`results/run_2026_05_27_233524/`

---

### Export Destination

The MARK-side export root is:

`/root/Desktop/vap/batched_exports/`

Per-run lightweight copies are written to:

`/root/Desktop/vap/batched_exports/lightweight_runs/<VAP_run_id>/`

Compressed exports are written to:

`/root/Desktop/vap/batched_exports/compressed/`

Timestamped manifests are written to:

`/root/Desktop/vap/batched_exports/manifests/`

Timestamped logs are written to:

`/root/Desktop/vap/batched_exports/logs/`

---

### Timestamp Policy

Each export execution must create one shared timestamp:

`YYYY_MM_DD_HHMMSS`

This timestamp must be applied consistently to all export-level files.

Example:

```text
input_manifest_2026_06_02_031500.tsv
export_summary_2026_06_02_031500.tsv
export_file_manifest_2026_06_02_031500.tsv
export_skipped_files_2026_06_02_031500.tsv
export_2026_06_02_031500.log
vap_lightweight_batch_2026_06_02_031500_001.tar
```

The passed-in manifest must be copied unchanged into the export manifest directory and renamed with the shared timestamp.

---

### File Inclusion Policy

A source file is eligible for export only if:

1. It is a regular file.
2. Its size is less than 50 MB.
3. Its filename does not end with .duckdb.

The script must always exclude .duckdb files, even if they are smaller than 50 MB.

The script must preserve the relative directory structure of copied files.

Example:

`results/run_<id>/metadata/run_metadata.json`

must become:

`/root/Desktop/vap/batched_exports/lightweight_runs/run_<id>/metadata/run_metadata.json`

---

### File Exclusion Policy

A file must be skipped if:

1. It is greater than or equal to 50 MB.
2. It ends with .duckdb.
3. The source path is not a regular file.

Skipped files and skipped runs must be recorded in the log and summary outputs.

---

### No-Overwrite Policy: MARK Export

If the destination directory already exists:

`/root/Desktop/vap/batched_exports/lightweight_runs/<VAP_run_id>/`

then the script must not overwrite, merge, delete, or modify that directory.

The script must:

1. Print a warning to console.
2. Write a warning to the log.
3. Record the skipped run in the export summary manifest.

---

### Compression Policy

After lightweight per-run copies are created, the script must compress each copied run directory losslessly into an individual `.tar.gz` archive.

Example:

`run_2026_05_27_233524.tar.gz`

The script must then pack as many run-level `.tar.gz` archives as possible into transport batch archives, each capped at 100 MB.

If a single run-level `.tar.gz` archive exceeds 100 MB, proceed with packing the `run_<id>.tar.gz`.  This is the only exception to the 100 MB cap policy.

Transport archives must be written as `.tar` files:

```text
vap_lightweight_batch_<timestamp>_001.tar
vap_lightweight_batch_<timestamp>_002.tar
```

The outer `.tar` files are transport containers. The run-level `.tar.gz` files provide lossless compression.

If a single run-level `.tar.gz` archive exceeds 100 MB, it must be placed alone in its own batch archive and flagged in the export summary and log.

---

### MARK-Side Output Files

The export script must write:

```text
/root/Desktop/vap/batched_exports/manifests/input_manifest_<timestamp>.tsv
/root/Desktop/vap/batched_exports/manifests/export_summary_<timestamp>.tsv
/root/Desktop/vap/batched_exports/manifests/export_file_manifest_<timestamp>.tsv
/root/Desktop/vap/batched_exports/manifests/export_skipped_files_<timestamp>.tsv
/root/Desktop/vap/batched_exports/logs/export_<timestamp>.log
/root/Desktop/vap/batched_exports/compressed/vap_lightweight_batch_<timestamp>_NNN.tar
```

---

### Export Summary Manifest

The export summary manifest must contain one row per input manifest row.

Recommended columns:

```text
export_timestamp
SRA_accn
VAP_run_id
Depth_Category
source_run_dir
destination_run_dir
run_status
files_copied
files_skipped_size
files_skipped_duckdb
files_skipped_other
bytes_copied
compressed_run_archive
compressed_run_archive_bytes
batch_archive
warning
```

Allowed run_status values:

```text
copied
skipped_existing_destination
missing_source
failed
```

---

### Export File Manifest

The export file manifest must contain one row per copied file.

Recommended columns:

```text
export_timestamp
SRA_accn
VAP_run_id
Depth_Category
source_path
relative_path
destination_path
file_size_bytes
copy_status
```

Allowed copy_status values:

```text
copied
failed
```

---

### Export Skipped Files Manifest

The skipped files manifest must contain one row per skipped file.

Recommended columns:

```text
export_timestamp
SRA_accn
VAP_run_id
Depth_Category
source_path
relative_path
file_size_bytes
skip_reason
```

Allowed skip_reason values:

```text
size_ge_50mb
duckdb_excluded
not_regular_file
copy_error
```

---

## sys76 Restore Script

### Script Name

`scripts/local/restore_lightweight_vap_exports.py`

---

### Invocation

The script must be run from the sys76 VAP repository root.

`python scripts/local/restore_lightweight_vap_exports.py path/to/downloaded/compressed/`

**Mission-Critical Invocation Note:**

> The script must check that the machineID is not VandPyMolGPUResearch (aka MARK).  If it is, then the restore script must fail loudly to prevent accidental overwrite of MARK's VAP repo's results/ folder.

---

### Restore Input

The restore input is a directory containing one or more batch archives:

`vap_lightweight_batch_<timestamp>_NNN.tar`

Each batch archive contains one or more run-level archives:

`run_<id>.tar.gz`

---

### Restore Destination

Restored runs are written to:

`results/<VAP_run_id>/`

Example:

`results/run_2026_05_27_233524/`

---

### Safe Extraction Policy

The restore script must perform safe extraction for both transport batch `.tar` archives and run-level `.tar.gz` archives.

Before extracting any archive member, the script must reject members that:

1. Use an absolute path.
2. Contain `..` path traversal.
3. Would resolve outside the intended extraction directory.

If any unsafe archive member is detected, the script must:

1. Abort extraction of that archive.
2. Print a warning to console.
3. Write the warning to the restore log.
4. Record the archive as `failed` in the restore summary manifest.

---

### No-Overwrite Policy: sys76 Restore

If the restore destination already exists:

`results/<VAP_run_id>/`

then the restore script must not overwrite, merge, delete, or modify that directory.

The script must:

1. Print a warning to console.
2. Write a warning to the restore log.
3. Record the skipped run in the restore summary manifest.

---

### sys76 Restore Output Files

The restore script must write timestamped restore logs and manifests.

Recommended location:

`logs/lightweight_restore/`

Required outputs:

`restore_summary_<timestamp>.tsv`
`restore_<timestamp>.log`

---

### Restore Summary Manifest

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

Allowed restore_status values:

```text
restored
skipped_existing_destination
failed
```

---

### Manual Restore Fallback

If needed, the user may manually inspect and extract batch archives.

Example:

```bash
mkdir -p /tmp/vap_restore_batches
tar -xf vap_lightweight_batch_2026_06_02_031500_001.tar -C /tmp/vap_restore_batches
```

Run-level archives may then be extracted into the VAP repo results/ directory:

```bash
for f in /tmp/vap_restore_batches/run_*.tar.gz; do
  tar -xzf "$f" -C /path/to/vap/repo/results
done
```

Manual extraction does not enforce the no-overwrite policy. The restore script is preferred.

---

## Invariants

The workflow must preserve MARK-side directory structure for copied files.

The workflow must not copy files greater than or equal to 50 MB.

The workflow must not copy `.duckdb` files.

The workflow must not overwrite existing export destinations on MARK.

The workflow must not overwrite existing restore destinations on sys76.

Each export execution must be auditable through timestamped manifests and logs.

Each restore execution must be auditable through timestamped manifests and logs.