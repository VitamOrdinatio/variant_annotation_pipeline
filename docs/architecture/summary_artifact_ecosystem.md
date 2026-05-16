# VAP Summary Artifact Ecosystem

## Purpose

This document describes the layered summary-artifact architecture within the Variant Annotation Pipeline (VAP).

During development of the VAP case-study harvester, it became apparent that VAP stage summaries collectively form a lightweight evidence abstraction ecosystem suitable for:

- downstream reporting
- provenance auditing
- telemetry harvesting
- biological evidence summarization
- reviewability tracking
- systems integration workflows
- future persistence-layer integration

This document formalizes those observations.

---

# Core Architectural Insight

VAP does not merely emit:
- raw TSV outputs
- intermediate files
- and logs

Instead, VAP increasingly behaves as:

```text
multi-layer evidence infrastructure
```

where successive stage summaries progressively abstract:
- biological substrate
- interpretation structure
- prioritization structure
- validation readiness
- operational telemetry
- and provenance state

into deterministic machine-readable evidence layers.

This enables downstream tooling to harvest biologically meaningful summaries without repeatedly reparsing gigantic upstream TSV substrates.

---

# Architectural Layering

## High-Level Flow

```text
Raw substrate artifacts
    ↓
Stage-specific summary abstractions
    ↓
Stage 13 harmonized run abstraction
    ↓
Harvester cross-run reporting
    ↓
Case studies / VDB / RDGP / portfolio integration
```

---

# Design Goals

The summary-artifact ecosystem appears to support several architectural goals:

## 1. Deterministic Abstraction

Stage summaries expose:
- compact
- machine-readable
- deterministic

representations of large biological substrates.

---

## 2. Storage-Aware Reporting

Downstream systems can often:
- inspect summaries
- inspect manifests
- inspect counts

without opening:
- 400MB TSVs
- multi-GB variant tables
- BAM files
- VCFs

This is especially valuable for:
- telemetry systems
- case-study harvesters
- orchestration systems
- distributed compute environments

---

## 3. Provenance Preservation

Summary layers preserve:
- execution lineage
- artifact topology
- QC state
- run identity
- configuration state
- stage transition structure

without requiring replay of pipeline execution.

---

## 4. Modular Interpretation Routing

Interpretation pathways remain separable:
- coding interpretation
- noncoding interpretation
- prioritization
- validation preparation
- reporting abstraction

This supports future extensibility.

---

## 5. Future Ecosystem Integration

The architecture naturally supports future integration with:
- VDB
- RDGP
- telemetry aggregation
- future ML interpretation layers
- phenotype-aware systems
- coding/noncoding branch extensions

---

# Summary-Layer Ecosystem

## `metadata.json`

### Primary Role

Global provenance and operational traceability substrate.

### Major Responsibilities

- run identity
- sample identity
- stage-output lineage
- execution metadata
- QC aggregation
- artifact topology
- resource provenance
- tool provenance
- warning capture

### Strategic Value

`metadata.json` is currently the richest single operational artifact emitted by VAP.

It functions as:
- provenance ledger
- execution audit surface
- topology registry
- operational QC snapshot

---

# Stage-Specific Summary Layers

---

## Stage 08 — Structural Biological Partitioning

### Artifact

```text
stage_08_summary.json
```

### Primary Responsibilities

- biological partitioning
- context classification
- severity abstraction
- frequency abstraction
- QC partitioning
- RDGP seed preparation

### Examples

- coding vs intronic vs intergenic partitioning
- HIGH/MODERATE/LOW/MODIFIER severity structure
- SNV/deletion/insertion distributions
- rare/common frequency structure
- QC caution structure

### Strategic Importance

Stage 08 forms the first major:
```text
biological abstraction layer
```

within VAP.

It transforms raw annotated substrate into biologically partitioned evidence structures suitable for downstream interpretation systems.

---

## Stage 09 — Coding Interpretation Abstraction

### Artifact

```text
stage_09_summary.json
```

### Primary Responsibilities

- coding interpretation abstraction
- coding functional-impact structure
- coding rarity structure
- coding clinical-support structure

### Examples

- loss-of-function counts
- missense counts
- synonymous counts
- splice-relevant counts
- clinically supported coding evidence

### Strategic Importance

Stage 09 represents the primary:
```text
coding interpretation framework
```

within VAP.

Importantly:
- Stage 09 does not prioritize variants.
- Stage 09 performs interpretation flagging only.

This separation is architecturally important.

---

## Stage 10 — Noncoding Interpretation Abstraction

### Artifact

```text
stage_10_summary.json
```

### Primary Responsibilities

- noncoding interpretation abstraction
- transcript/regulatory contextualization
- noncoding rarity structure
- noncoding clinical-support structure

### Examples

- intergenic structure
- intronic structure
- proximal structure
- transcript-associated structure
- noncoding interpretation ontology

### Important Architectural Note

AlphaGenome integration is intentionally deferred in VAP v1.

This strongly supports future:
```text
noncoding interpretation extensibility
```

without destabilizing core evidence-routing architecture.

### Strategic Importance

Stage 10 represents the primary:
```text
noncoding interpretation framework
```

within VAP.

---

## Stage 11 — Interpretation Convergence and Prioritization

### Artifact

```text
stage_11_summary.json
```

### Primary Responsibilities

- interpretation convergence
- deterministic prioritization
- gene-burden abstraction
- interpretation-merging structure

### Examples

- priority tiers
- interpretation-label distributions
- variant-origin distributions
- top-gene burden structure
- unique gene-count structure

### Major Architectural Insight

Stage 11 merges:
- Stage 09 coding interpretation outputs
- with Stage 10 noncoding interpretation outputs

into a unified prioritization substrate.

This appears to be the primary:
```text
interpretation convergence layer
```

within VAP.

### Important Scope Boundary

Stage 11:
- prioritizes evidence
- but does NOT perform gene-level ranking.

This distinction is important for future RDGP integration.

---

## Stage 12 — Validation Preparation Abstraction

### Artifact

```text
stage_12_summary.json
```

### Primary Responsibilities

- validation preparation
- reviewability abstraction
- orthogonal-review readiness

### Examples

- IGV recommendation structure
- validation-priority structure
- validation-required structure

### Strategic Importance

Stage 12 exposes:
```text
reviewability substrate
```

rather than new biological interpretation.

This distinction is operationally important.

---

## Stage 13 — Harmonized Run Abstraction

### Artifacts

```text
stage_13_final_summary.json
stage_13_artifact_manifest.json
stage_13_run_report.md
```

### Primary Responsibilities

- harmonized run abstraction
- lightweight reporting substrate
- artifact topology auditing
- downstream reporting preparation

---

### `stage_13_final_summary.json`

Primary role:
- compact deterministic run abstraction

Examples:
- final priority structure
- final interpretation structure
- final validation structure
- compact top-gene summaries
- QC harmonization

### Major Insight

Stage 13 behaves almost like:
```text
lightweight run-level API surface
```

for downstream reporting systems.

This was a major discovery during harvester development.

---

### `stage_13_artifact_manifest.json`

Primary role:
- artifact topology auditing

Examples:
- artifact existence
- file size inspection
- stage association
- storage-aware orchestration

Strategically useful because downstream systems can determine:
```text
whether rich substrate exists
```

without opening massive files.

---

### `stage_13_run_report.md`

Primary role:
- human-readable reporting abstraction

Useful for:
- sanity checking
- lightweight reporting
- operational readability
- portfolio presentation

Less useful for machine harvesting because equivalent structured JSON substrate already exists.

---

# Variant-Origin Architecture

One of the most important abstractions surfaced during harvester development was:

```text
variant_origin
```

This does NOT simply mean:
- exon vs intron
- coding sequence vs regulatory DNA

Instead, it preserves:
```text
interpretation lineage
```

Specifically:

- `coding`
  - evidence processed through Stage 09 coding interpretation workflows
- `noncoding`
  - evidence processed through Stage 10 noncoding interpretation workflows

This separation is strategically important because future systems can attach:
- coding-specific interpretation engines
- or noncoding-specific interpretation engines

without redesigning evidence-routing architecture.

Examples:

### Potential Future Coding Extensions

- AlphaMissense
- REVEL
- LOFTEE
- protein-structure-aware interpretation

### Potential Future Noncoding Extensions

- AlphaGenome
- SpliceAI
- enhancer/promoter modeling
- chromatin-aware interpretation
- transcript-regulatory modeling

---

# Harvester Architectural Insight

A major discovery during case-study harvester development was:

```text
many biologically meaningful abstractions already exist inside summary layers.
```

Therefore:
- cross-run reporting
- reproducibility summaries
- interpretation summaries
- reviewability summaries
- telemetry summaries

can often be harvested directly from compact JSON layers rather than reparsing gigantic TSVs.

This provides:
- better portability
- better reproducibility
- simpler orchestration
- faster execution
- lower storage pressure

---

# Relationship to Future Ecosystem Components

## VDB

VDB is expected to become:
```text
long-term persistence infrastructure
```

while summary layers remain:
```text
lightweight execution abstractions.
```

---

## RDGP

RDGP may later consume:
- Stage 08 seed substrate
- Stage 11 prioritization substrate
- VDB-persisted evidence
- phenotype-aware overlays

to perform:
```text
sample-aware gene prioritization.
```

---

## GSC

GSC overlays may later enrich:
- interpretation pathways
- gene burden summaries
- prioritization substrate
- phenotype-aware evidence routing

without modifying summary-layer architecture itself.

---

# Important Scientific Guardrails

The summary-artifact ecosystem:
- summarizes evidence organization
- summarizes operational state
- summarizes prioritization structure

It does NOT:
- establish causality
- perform phenotype matching
- provide definitive clinical interpretation
- assign molecular mechanism
- perform diagnosis

The abstractions remain:
```text
deterministic evidence organization layers
```

rather than direct clinical decision systems.

---

# Future Opportunities

Potential future additions:

- telemetry dashboards
- Sankey interpretation-lineage diagrams
- stage-transition visualization
- cross-run reproducibility heatmaps
- coding/noncoding branch visualization
- VDB persistence integration
- orchestration-aware monitoring
- summary-layer APIs

---

# Final Architectural Positioning

The summary-artifact ecosystem increasingly positions VAP as:

```text
extensible evidence-routing infrastructure
```

rather than:
```text
single-purpose annotation tooling.
```

This distinction may become one of the strongest architectural narratives within the VAP ecosystem.