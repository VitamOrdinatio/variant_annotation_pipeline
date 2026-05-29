# `data/reference/sra_support/selections/README.md`

# selections/

This directory contains scientific run-selection manifests derived from BioProject provenance manifests.

Each BioProject receives its own nested lowercase subdirectory:

```text
selections/<bioproject_lower>/
```

Example:

```text
selections/prjeb57558/
```

These manifests are generated primarily by:

```text
scripts/resources/select_bioproject_runs_by_depth.sh
```

Selection manifests are intended to:

* stratify sequencing depth/breadth,
* support reproducible VAP substrate acquisition,
* preserve operational download compatibility,
* document scientific selection rationale.

Selection manifests may be consumed directly by:

```text
scripts/resources/download_selected_fastqs_polite.sh
```

This directory represents the scientific-selection boundary of the acquisition trilogy.
