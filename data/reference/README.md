# `data/reference/`

Persistent operational reference substrates and lightweight orchestration surfaces for VAP.

---

# Overview

The `data/reference/` namespace contains lightweight operational artifacts used to support:

* deterministic orchestration,
* semantic overlay workflows,
* cohort acquisition,
* lightweight transfer coordination,
* and analytical extraction infrastructure.

Unlike large genomic payloads, these artifacts function primarily as:

* control-plane infrastructure,
* manifest-oriented coordination surfaces,
* and lightweight semantic support substrates.

---

# Directory Topology

```text
reference/
├── gene_lists/
├── lightweight_transfer/
├── sra_support/
└── stage12_analytical_batch_exports/
```

| Directory                           | Purpose                                                |
| ----------------------------------- | ------------------------------------------------------ |
| `gene_lists/`                       | lightweight semantic overlay substrates                |
| `lightweight_transfer/`             | transfer orchestration manifests                       |
| `sra_support/`                      | SRA acquisition and cohort-construction infrastructure |
| `stage12_analytical_batch_exports/` | manifest-driven analytical extraction infrastructure   |

---

# Architectural Role

The `reference/` ecosystem acts as persistent operational support infrastructure for VAP.

These artifacts support workflows involving:

* cohort selection,
* reproducible orchestration,
* semantic contextualization,
* SQL-oriented analytical extraction,
* lightweight artifact transfer,
* and interoperability experimentation.

The directory therefore functions primarily as:

```text
lightweight semantic coordination infrastructure
```

rather than static biological payload storage.

---

# `gene_lists/`

Contains lightweight semantic overlay substrates used for post-VAP contextualization workflows.

Current overlays support:

* epilepsy-oriented enrichment,
* mitochondrial disease contextualization,
* targeted SQL slicing,
* and lightweight interoperability experimentation.

These overlays are intentionally transitional and currently bridge VAP outputs toward future VDB/GSC interoperability workflows.

---

# `lightweight_transfer/`

Contains manifest-oriented coordination surfaces supporting lightweight export workflows from large MARK execution environments.

These manifests are used by:

```text
scripts/mark/export_lightweight_vap_runs.py
```

to selectively extract lightweight operational artifacts for downstream analysis on external systems.

This infrastructure preserves:

* portability,
* reproducibility,
* and lightweight execution transfer governance.

---

# `sra_support/`

Contains operational infrastructure supporting deterministic SRA acquisition and cohort construction workflows.

This namespace supports:

* BioProject manifest harvesting,
* run topology analysis,
* depth-aware cohort selection,
* provenance preservation,
* and polite acquisition orchestration.

Associated workflows intentionally emphasize:

* reproducibility,
* transparent cohort selection,
* and controlled external resource usage.

---

# `stage12_analytical_batch_exports/`

Contains manifest-oriented orchestration substrates supporting SQL-mediated analytical extraction from large Stage 12 validation surfaces.

Primary workflows are driven through:

```text
scripts/analysis/run_stage12_duckdb_exports_from_manifest.py
```

This infrastructure enables:

* deterministic extraction,
* reproducible analytical harvesting,
* and scalable validation-surface interrogation

without requiring direct manipulation of full cohort-scale payloads.

---

# Manifest-Oriented Infrastructure

A recurring architectural theme throughout `data/reference/` is deterministic manifest-oriented orchestration.

Rather than hardcoding execution topology, VAP increasingly coordinates workflows through lightweight TSV control surfaces.

This design enables:

* reproducible execution,
* deterministic routing,
* scalable orchestration,
* semantic continuity,
* and lightweight portability.

---

# Relationship to the Broader Ecosystem

The `reference/` ecosystem increasingly supports interoperability-oriented repository architecture across:

* VAP,
* GSC,
* VDB,
* RDGP,
* and future downstream semantic infrastructure systems.

Many of the lightweight substrates contained here are intentionally transitional and are expected to evolve toward more formal interoperability routing once the broader repository ecosystem matures.

---

# Summary

The `data/reference/` namespace functions as persistent lightweight operational infrastructure supporting:

* semantic coordination,
* reproducible orchestration,
* interoperability experimentation,
* cohort construction,
* and scalable analytical governance workflows

across the broader VAP ecosystem.
