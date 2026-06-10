# `data/reference/lightweight_transfer/`

Manifest-oriented lightweight transfer coordination substrates for completed VAP runs.

---

# Overview

The `lightweight_transfer/` namespace contains lightweight orchestration manifests supporting selective export workflows from completed VAP executions on MARK HPC infrastructure.

These manifests are used to coordinate:

* lightweight artifact extraction,
* portable run transfer,
* downstream local analysis,
* and reproducible operational review workflows.

Rather than transferring full execution payloads, this subsystem selectively exports lightweight operational substrates suitable for downstream inspection and analysis on external systems such as `sys76`.

---

# Directory Topology

```text
lightweight_transfer/
└── manifests/
```

| Directory    | Purpose                                   |
| ------------ | ----------------------------------------- |
| `manifests/` | lightweight export coordination manifests |

---

# Primary Workflow

The manifests contained here are used primarily by:

```text
scripts/mark/export_lightweight_vap_runs.py
```

This workflow enables deterministic export of lightweight subsets from completed VAP runs residing on MARK infrastructure.

Representative exported artifacts may include:

* stage summaries,
* runtime telemetry,
* validation summaries,
* lightweight TSV substrates,
* metadata surfaces,
* and review-oriented operational artifacts.

Large payload-plane artifacts such as:

* FASTQs,
* BAMs,
* and full cohort-scale annotation payloads

remain external to repository storage.

---

# Architectural Role

The `lightweight_transfer/` subsystem supports VAP’s broader separation between:

```text
payload-plane artifacts
```

and:

```text
lightweight control-plane infrastructure.
```

This design enables:

* portable review workflows,
* lightweight reproducibility surfaces,
* downstream analysis on non-HPC systems,
* and deterministic artifact coordination

without requiring full payload migration.

---

# Manifest-Oriented Coordination

The transfer workflow is intentionally manifest-driven.

Each manifest specifies:

* which completed VAP runs should be exported,
* which samples are targeted,
* and which lightweight operational artifacts should be transferred.

This architecture improves:

* reproducibility,
* transparency,
* portability,
* and operational consistency.

---

# Current Manifest Examples

Representative manifests include:

| Manifest                                                        | Purpose                                        |
| --------------------------------------------------------------- | ---------------------------------------------- |
| `stage12_analytical_batch_export_manifest_hg002.tsv`            | HG002-oriented lightweight export coordination |
| `stage12_analytical_batch_export_manifest_prjeb57558_12sra.tsv` | 12-SRA cohort lightweight export coordination  |

These manifests help coordinate reproducible extraction from completed MARK executions.

---

# Relationship to Cross-Run Infrastructure

The lightweight transfer subsystem became especially important during:

* HG002 benchmarking workflows,
* cross-run governance analysis,
* cohort-scale reviewability assessment,
* and downstream case-study development.

Selective lightweight exports enabled rapid local iteration and analytical review without requiring repeated movement of large genomic payloads.

---

# Relationship to the Broader Ecosystem

This subsystem increasingly functions as lightweight operational infrastructure supporting:

* reproducible analysis portability,
* semantic substrate transfer,
* cross-system review workflows,
* and downstream interoperability experimentation.

It therefore acts as a bridge between:

* large-scale HPC execution environments,
* and lightweight local analytical environments.

---

# Summary

The `data/reference/lightweight_transfer/` namespace provides manifest-oriented lightweight transfer coordination infrastructure for completed VAP executions.

Its primary purpose is to enable reproducible, portable, and operationally efficient extraction of lightweight analytical substrates from large HPC-resident VAP runs.
