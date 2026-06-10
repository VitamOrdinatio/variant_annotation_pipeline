# `data/reference/stage12_analytical_batch_exports/`

Manifest-driven orchestration substrates for deterministic Stage 12 analytical extraction workflows.

---

# Overview

The `stage12_analytical_batch_exports/` namespace contains lightweight manifests used to coordinate analytical exports from large Stage 12 validation substrates.

These manifests support reproducible SQL-mediated harvesting of Stage 12 outputs, especially:

```text
stage_12_validation_candidates.tsv
```

Because Stage 12 candidate tables can be large, this subsystem enables targeted analytical extraction without requiring manual inspection or full-file movement.

---

# Directory Topology

```text
stage12_analytical_batch_exports/
└── manifests/
```

| Directory    | Purpose                                                                 |
| ------------ | ----------------------------------------------------------------------- |
| `manifests/` | run-selection manifests used to drive batch analytical export workflows |

---

# Primary Workflow

These manifests are used primarily by:

```text
scripts/analysis/run_stage12_duckdb_exports_from_manifest.py
```

The workflow is manifest-driven.

Each manifest identifies VAP runs by sample accession and run identifier, allowing the export runner to locate completed Stage 12 artifacts and execute deterministic DuckDB-mediated SQL extractions.

---

# Manifest Role

The manifests contained here function as lightweight control-plane artifacts.

They specify:

* which samples should be processed,
* which completed VAP run identifiers should be targeted,
* which Stage 12 substrates should be queried,
* and which analytical extraction batch should be executed.

This allows VAP to preserve reproducible extraction behavior without storing full Stage 12 payloads in Git.

---

# Current Manifest Examples

| Manifest                                                               | Purpose                                           |
| ---------------------------------------------------------------------- | ------------------------------------------------- |
| `stage12_analytical_batch_export_manifest_hg002.tsv`                   | HG002-focused Stage 12 analytical export manifest |
| `stage12_analytical_batch_export_manifest_prjeb57558_12sra.tsv`        | 12-SRA PRJEB57558 cohort export manifest          |
| `TESTRUN_stage12_analytical_batch_export_manifest_prjeb57558_3sra.tsv` | reduced test manifest for lightweight validation  |

---

# Architectural Role

This namespace supports the broader VAP strategy of separating:

```text
large biological payloads
```

from:

```text
lightweight orchestration surfaces
```

Stage 12 validation payloads remain outside normal Git storage, while the manifests controlling analytical extraction remain versioned and reviewable.

This design supports:

* deterministic extraction,
* cohort-scale analysis,
* reproducible SQL harvesting,
* lightweight portability,
* and provenance-aware analytical coordination.

---

# Relationship to Cross-Run Analysis

The Stage 12 analytical export workflow helped enable later cross-run case-study infrastructure by extracting targeted validation and reviewability surfaces from completed VAP runs.

These exported analytical substrates supported:

* candidate reviewability assessment,
* validation-surface comparison,
* cross-run governance analysis,
* and semantic evidence harvesting.

---

# Summary

The `data/reference/stage12_analytical_batch_exports/` namespace provides lightweight manifest infrastructure for reproducible analytical extraction from large Stage 12 validation outputs.

It is a control-plane layer for targeted SQL-mediated evidence harvesting, not a storage location for full Stage 12 payloads.
