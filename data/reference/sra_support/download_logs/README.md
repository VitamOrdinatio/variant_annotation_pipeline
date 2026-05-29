# `data/reference/sra_support/download_logs/README.md`

# download_logs/

This directory contains operational telemetry generated during FASTQ acquisition.

Each BioProject receives its own nested lowercase subdirectory:

```text
download_logs/<bioproject_lower>/
```

Example:

```text
download_logs/prjeb57558/
```

Logs are generated primarily by:

```text
scripts/resources/download_selected_fastqs_polite.sh
```

Expected logs may include:

* download session logs,
* failed download reports,
* gzip integrity validation logs.

FASTQ files themselves are intentionally stored outside the repository on MARK shared storage:

```text
/data/storage/fastq/
```

This separation helps preserve:

* repository cleanliness,
* provenance organization,
* operational reproducibility,
* shared-storage hygiene.
