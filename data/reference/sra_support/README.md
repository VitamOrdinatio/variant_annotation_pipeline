# `data/reference/sra_support/README.md`

# SRA Support

This directory contains BioProject-derived sequencing support artifacts used by VAP acquisition workflows.

The goal of this subsystem is to separate:

1. provenance-safe BioProject manifest harvesting,
2. scientific run-selection logic,
3. operational FASTQ download activity.

Large FASTQ substrates are intentionally stored outside the repository on MARK shared storage:

```text
/data/storage/fastq/
```

This directory instead preserves:

* manifest provenance,
* scientific selection manifests,
* operational logs,
* reproducible acquisition telemetry.

---

# Directory Overview

## `manifests/`

Authoritative provenance manifests harvested directly from ENA.

Generated primarily by:

```text
scripts/resources/harvest_bioproject_run_manifest.sh
```

Contains:

* raw run manifests,
* minimally cleaned topology manifests,
* harvested ENA field inventories,
* manifest harvest logs.

Timestamped files are immutable provenance artifacts.

Stable latest-copy manifests are intentionally refreshed after successful validation.

---

## `selections/`

Scientific run-selection manifests derived from provenance manifests.

Generated primarily by:

```text
scripts/resources/select_bioproject_runs_by_depth.sh
```

Contains:

* selected-run manifests,
* depth-stratified run subsets,
* selection telemetry,
* scientific design logs.

These manifests are intended to drive downstream FASTQ acquisition.

---

## `download_logs/`

Operational download telemetry produced during FASTQ acquisition.

Generated primarily by:

```text
scripts/resources/download_selected_fastqs_polite.sh
```

Contains:

* download session logs,
* failed download reports,
* gzip integrity validation logs.

FASTQ files themselves are not stored here.

---

# Design Philosophy

This subsystem intentionally prevents:

1. provenance drift,
2. pretty-table operational drift,
3. downloader overreach.

The authoritative provenance boundary remains the harvested ENA manifest topology generated under `manifests/`.
