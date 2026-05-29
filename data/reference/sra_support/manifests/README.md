# `data/reference/sra_support/manifests/README.md`

# manifests/

This directory contains authoritative BioProject provenance manifests harvested directly from ENA.

Each BioProject receives its own nested lowercase subdirectory:

```text
manifests/<bioproject_lower>/
```

Example:

```text
manifests/prjeb57558/
```

These directories contain:

* raw ENA run manifests,
* minimally cleaned topology manifests,
* harvested ENA field inventories,
* manifest harvest logs.

Generated primarily by:

```text
scripts/resources/harvest_bioproject_run_manifest.sh
```

Timestamped files are immutable provenance artifacts.

Stable latest-copy manifests are intentionally refreshed after successful validation.
