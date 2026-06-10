# `data/reference/sra_support/`

Manifest-oriented SRA acquisition infrastructure and cohort-governance support surfaces for VAP.

---

# Overview

The `sra_support/` namespace contains BioProject-derived operational infrastructure supporting deterministic sequencing acquisition workflows within VAP.

This ecosystem intentionally separates:

1. provenance-safe BioProject manifest harvesting,
2. scientific cohort-selection logic,
3. and operational FASTQ acquisition activity.

Large sequencing payloads themselves are intentionally excluded from repository storage and instead reside on external MARK execution infrastructure.

The repository preserves only lightweight control-plane artifacts including:

* provenance manifests,
* cohort-selection surfaces,
* operational telemetry,
* acquisition logs,
* and reproducibility-oriented orchestration substrates.

---

# Architectural Philosophy

The `sra_support/` ecosystem treats sequencing acquisition as:

```text
governed operational infrastructure
```

rather than ad hoc preprocessing.

This design preserves:

* provenance continuity,
* reproducible cohort construction,
* deterministic selection logic,
* acquisition transparency,
* and operational telemetry continuity.

The subsystem therefore emphasizes:

* manifest-oriented orchestration,
* immutable provenance preservation,
* lightweight repository portability,
* and controlled external resource usage.

---

# External Payload Storage

Large FASTQ payloads are intentionally stored outside the repository on MARK shared storage infrastructure:

```text
/data/storage/fastq/
```

The repository itself instead preserves lightweight orchestration and provenance surfaces governing:

* how runs were harvested,
* how cohorts were selected,
* and how acquisition workflows were executed.

---

# Directory Topology

```text
sra_support/
├── download_logs/
├── manifests/
└── selections/
```

| Directory        | Purpose                                                |
| ---------------- | ------------------------------------------------------ |
| `manifests/`     | authoritative provenance manifests harvested from ENA  |
| `selections/`    | cohort-selection and scientific run-selection surfaces |
| `download_logs/` | operational FASTQ acquisition telemetry                |

---

# `manifests/`

Contains authoritative provenance manifests harvested directly from ENA/BioProject infrastructure.

Primary generation workflow:

```text
scripts/resources/harvest_bioproject_run_manifest.sh
```

Representative contents include:

* raw BioProject manifests,
* minimally normalized topology manifests,
* ENA field inventories,
* manifest harvest telemetry,
* and provenance-preserving logs.

Timestamped manifest files are intentionally treated as:

```text
immutable provenance artifacts.
```

Stable latest-copy manifests may be refreshed following successful validation workflows.

---

# Provenance Boundaries

The authoritative provenance boundary for cohort construction remains the harvested ENA manifest topology generated within:

```text
manifests/
```

This separation helps prevent:

* provenance drift,
* topology mutation,
* accidental selection corruption,
* and downstream operational ambiguity.

---

# `selections/`

Contains scientific cohort-selection substrates derived from harvested provenance manifests.

Primary generation workflow:

```text
scripts/resources/select_bioproject_runs_by_depth.sh
```

Representative contents include:

* selected-run manifests,
* depth-stratified cohorts,
* selection telemetry,
* cohort-construction logs,
* and targeted acquisition subsets.

These manifests function as:

```text
deterministic cohort-governance surfaces
```

driving downstream FASTQ acquisition workflows.

---

# Cohort Construction Philosophy

Selection workflows intentionally preserve:

* transparent selection criteria,
* reproducible cohort topology,
* depth-aware balancing,
* and explicit operational reasoning.

This architecture enables VAP cohort studies to maintain:

* reproducibility,
* provenance continuity,
* and deterministic acquisition behavior

across repeated execution workflows.

---

# `download_logs/`

Contains operational telemetry generated during FASTQ acquisition workflows.

Primary generation workflow:

```text
scripts/resources/download_selected_fastqs_polite.sh
```

Representative contents include:

* acquisition session logs,
* failed download reports,
* gzip integrity validation logs,
* and operational transfer telemetry.

FASTQ payloads themselves are intentionally not stored within this namespace.

---

# Polite Acquisition Strategy

Acquisition workflows intentionally emphasize:

* controlled download behavior,
* infrastructure politeness,
* bounded I/O pressure,
* and reproducible transfer governance.

This design helps prevent:

* excessive external resource usage,
* unstable acquisition behavior,
* and uncontrolled HPC resource consumption.

---

# Relationship to the Broader Ecosystem

The `sra_support/` ecosystem acts as foundational cohort-governance infrastructure supporting:

* HG002 benchmarking workflows,
* heterogeneous WES cohort construction,
* cross-run governance analysis,
* reproducibility assessment,
* and future interoperability-oriented execution studies.

This infrastructure therefore serves as an important upstream coordination layer for the broader VAP ecosystem.

---

# Manifest-Oriented Orchestration

A recurring architectural principle throughout this namespace is deterministic manifest-oriented orchestration.

Rather than embedding cohort logic directly into acquisition scripts, VAP increasingly separates:

* provenance harvesting,
* scientific selection,
* and operational acquisition

into independent lightweight orchestration surfaces.

This design improves:

* transparency,
* reproducibility,
* portability,
* auditability,
* and semantic continuity.

---

# Summary

The `data/reference/sra_support/` namespace provides lightweight operational infrastructure supporting:

* deterministic SRA acquisition,
* reproducible cohort construction,
* provenance-aware orchestration,
* and telemetry-preserving acquisition governance

within the broader VAP semantic infrastructure ecosystem.
