# Proposed Structure for `docs/architecture/storage_strategy.md`

## 1. Purpose

Short opening:

* VAP performs provenance-preserving genomics execution.
* Storage lifecycle management is therefore a first-class architectural concern.
* This document describes:

  * retained artifacts,
  * transient artifacts,
  * reproducibility philosophy,
  * and downstream integration strategy.

---

## 2. Quick Terminology

Tiny reviewer-oriented glossary.

| Term | Meaning                                                                   |
| ---- | ------------------------------------------------------------------------- |
| VAP  | Variant Annotation Pipeline                                               |
| VDB  | Variant Database                                                          |
| RSP  | RNA Sequencing Pipeline                                                   |
| MARK | Primary 40-core Linux HPC execution node used for empirical VAP telemetry |

```text
VAP remains portable across Linux-based computational environments with appropriate dependencies and storage access.
```

---

## 3. Provenance-First Storage Philosophy

Core conceptual section.

Introduce:

| Layer                             | Meaning                                |
| --------------------------------- | -------------------------------------- |
| FASTQ.gz substrate                | immutable biological acquisition layer |
| VAP execution artifacts           | reproducible computational derivatives |
| normalized downstream derivatives | VDB-ingestable semantic products       |

Key message:

```text
Raw biological substrates are treated as immutable provenance anchors.
```

VAP effectively operates with:

* deterministic rerun philosophy,
* provenance preservation,
* reproducibility,
* auditability.

---

## 4. Future-Facing Biological Substrate Preservation

VAP intentionally favors preservation of biological substrate over aggressive early-stage information reduction.

This design choice is motivated by the observation that biological interpretation models evolve continuously, particularly for:

* noncoding variants,
* regulatory elements,
* enhancer/promoter interactions,
* chromatin topology,
* and context-dependent genotype–environment interactions.

Consequently, variants that may currently appear uninterpretable or clinically uncertain may become biologically meaningful as future annotation frameworks mature.

Examples may include:

* latent regulatory burden near disease-associated loci,
* combinatorial noncoding effects,
* or environmental interaction models that are not yet fully characterized.

VAP therefore prioritizes deterministic preservation of richly annotated variant substrate whenever practical, allowing future computational frameworks and downstream relational systems (such as VDB) to revisit previously unresolved biological patterns without requiring reacquisition or resequencing of biological material.

This philosophy directly influences:

* storage architecture,
* provenance retention,
* artifact lifecycle management,
* and downstream interoperability strategy.

VAP intentionally avoids irreversible early-stage reduction of biological substrate whenever practical, particularly for noncoding and context-dependent variant classes whose significance may evolve as biological interpretation frameworks mature.

---

## 5. Empirical Execution Footprints

Real telemetry governs storage reality in modern bioinformatics workflows. VAP's prioritization of traceability, metadata preservation, provenance, and deterministic reproducibility means that VAP outputs are intentionally larger than many aggressively filtering genomics workflows.

Examples:

```text
Observed WES compressed FASTQ footprint:
10 SRAs ≈ 86.2 GB

Observed completed WES VAP run:
~20 GB/run

Observed HG002 WGS VAP run:
~80 GB/run
```

```text
Execution footprints are dominated primarily by:
- BAMs,
- sorted BAMs,
- annotated VCFs,
- semantic interpretation artifacts,
- and telemetry outputs.
```

---

## 6. Runtime vs Retained Artifacts

| Artifact Class                        | Lifecycle             |
| ------------------------------------- | --------------------- |
| FASTQ.gz                              | retained              |
| telemetry/provenance summaries        | retained              |
| normalized semantic outputs           | retained              |
| BAMs/intermediate execution artifacts | potentially transient |

VAP's key philosophy:

```text
Large execution artifacts may eventually become regenerable transient infrastructure once downstream ingestion, provenance stabilization, and normalized derivative retention mature sufficiently.
```

---

## 7. Future VDB Integration

* VDB is expected to ingest normalized derivative products from VAP.
* VDB should avoid duplicating raw FASTQ/BAM artifacts.
* VDB acts as a relational integration layer rather than a second raw-data archive.

VAP interfaces with VDB while adhering to:

* provenance retention,
* normalized semantic derivatives,
* deterministic regeneration.

---

## 8. Git-Tracked vs Runtime Artifacts

Explain:

| Git-tracked     | Runtime-only                |
| --------------- | --------------------------- |
| scripts         | timestamped manifests       |
| contracts/docs  | execution logs              |
| schema examples | generated execution outputs |

Mention:

* provenance-safe runtime handling,
* operational manifests,
* lightweight schema examples,
* runtime artifact isolation.

---

## 9. Summary


VAP treats storage architecture as part of reproducible computational genomics infrastructure rather than as an afterthought of execution.

>The VAP storage strategy reflects a broader philosophy that reproducible computational genomics infrastructure should preserve biological substrate whenever practical while remaining provenance-aware, interoperable, and deterministically regenerable.

---