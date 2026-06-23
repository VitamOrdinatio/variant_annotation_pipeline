# VAP-TEP Consumer Guide

## Purpose

This document provides guidance for downstream consumers of VAP Transitional Evidence Products (VAP-TEPs).

The intended audience includes:

```text
VDB

RDGP

Future analytical repositories

Audit systems

Discovery systems

Evidence preservation systems
```

This guide explains how VAP-TEPs should be interpreted, what preservation guarantees they provide, and how consumers should interact with preserved evidence.

This document is not an implementation specification.

This document does not prescribe database schemas, storage models, or query architectures.

Its purpose is semantic interpretation of VAP-produced evidence packages.

---

# What A VAP-TEP Is

A VAP-TEP is a preservation package.

A VAP-TEP is not:

```text
a summary package

a report package

a candidate-only package

a presentation package
```

A VAP-TEP exists to preserve the evidentiary lifecycle produced by VAP.

The objective is to enable future systems to reconstruct, audit, reinterpret, and reason over preserved evidence without requiring access to the original VAP repository.

Accordingly:

```text
TEP
=
Preservation
```

not:

```text
TEP
=
Summarization
```

---

# Preservation Mission

The preservation mission of a VAP-TEP is:

```text
Preserve observation.

Preserve transformation.

Preserve interpretation.

Preserve prioritization.

Preserve validation context.

Preserve provenance.

Preserve lineage.

Preserve future reinterpretability.
```

Consumers should therefore assume:

```text
Evidence was preserved.

Evidence was not collapsed.
```

unless certification evidence demonstrates otherwise.

---

# Evidence Lifecycle

A VAP-TEP preserves the evidence lifecycle produced by VAP.

Current lifecycle:

```text
Stage07
Observation
    ↓
Stage08
Normalization
    ↓
Routing
    ↓
Stage09
Coding Interpretation
    ↓
Stage10
Noncoding Interpretation
    ↓
Stage11
Prioritization
    ↓
Stage12
Validation
    ↓
Stage13
Context
```

Each preserved entity represents a distinct evidence state.

Consumers should not assume that later stages replace earlier stages.

Instead:

```text
Later stages augment earlier stages.
```

---

# Stage07 Observation

Entity:

```text
entities/observation/
```

Role:

```text
Authoritative observation substrate
```

Contains:

```text
Observed variants

Coordinates

Alleles

Annotations

Sample identity

Run identity
```

Stage07 represents the preserved observation universe.

For scientific evidence state:

```text
Stage07 is authoritative.
```

---

# Stage08 Normalization

Entity:

```text
entities/normalization/
```

Role:

```text
Normalized representation
of the observation universe
```

Current VAP releases preserve:

```text
stage_08_selected_transcript_consequences.tsv

stage_08_vdb_ready_variants.tsv
```

These artifacts may be physically identical in current VAP releases.

Consumers should not assume they will remain identical indefinitely.

Both identities should be preserved independently.

---

# Routing Semantics

Entity:

```text
entities/routing/
```

Role:

```text
Biological routing context
```

Current routing structure:

```text
Coding Partition

Noncoding Partition

Splice Overlay
```

Consumers should not model routing as a simple mutually exclusive partition.

Current observed topology:

```text
coding ∩ splice > 0

coding ∩ noncoding = 0

splice ∩ noncoding = 0
```

Accordingly:

```text
Splice
=
Overlay
```

rather than:

```text
Splice
=
Independent partition
```

Future VAP releases may elevate splice-associated biology to a first-class semantic overlay.

Consumers should preserve compatibility with future splice-aware evolution.

---

# Stage09 Coding Interpretation

Entity:

```text
entities/coding_interpretation/
```

Role:

```text
Coding interpretation overlay
```

Provides interpretation context associated with coding variants.

This entity does not replace Stage07.

This entity augments Stage07.

---

# Stage10 Noncoding Interpretation

Entity:

```text
entities/noncoding_interpretation/
```

Role:

```text
Noncoding interpretation overlay
```

Provides interpretation context associated with noncoding variants.

This entity does not replace Stage07.

This entity augments Stage07.

---

# Interpretation Doctrine

Coding interpretation and noncoding interpretation should be treated as:

```text
First-class overlays
```

Consumers should preserve the distinction between:

```text
Observation

Interpretation
```

These are not equivalent evidence states.

---

# Stage11 Prioritization

Entity:

```text
entities/prioritization/
```

Role:

```text
Reviewability overlay
```

Provides:

```text
Priority tiers

Priority ranks

Priority reasoning

Reviewability context
```

Stage11 is additive.

Stage11 is not authoritative observation state.

Stage11 is not a candidate subset.

---

# Stage12 Validation

Entity:

```text
entities/validation/
```

Role:

```text
Validation planning overlay
```

Provides:

```text
Validation requirements

Validation priority

Validation methods

Validation rationale
```

Stage12 is additive.

Stage12 does not replace earlier evidence.

Stage12 is not authoritative observation state.

---

# Candidate-Collapse Warning

Consumers must not assume:

```text
Stage11
=
the evidence universe
```

or:

```text
Stage12
=
the evidence universe
```

Certification audits have demonstrated:

```text
Stage11 preserves
the complete evidence universe.

Stage12 preserves
the complete evidence universe.
```

Accordingly:

```text
Prioritized
≠
All evidence

Validation-required
≠
All evidence
```

Future reinterpretation depends on preservation of non-prioritized and non-validation-required evidence.

---

# Stage13 Context

Entity:

```text
entities/context/
```

Role:

```text
Run-context provenance
```

Contains:

```text
Artifact manifests

Execution summaries

Run reports

Execution metadata
```

Stage13 is authoritative for:

```text
Execution context

Audit context

Run context
```

Stage13 is not authoritative for:

```text
Scientific evidence state
```

Stage13 complements preserved evidence.

Stage13 does not replace preserved evidence.

---

# Identity Preservation

VAP-TEPs preserve producer identities.

Examples include:

```text
sample_id

run_id

variant_id

artifact identity
```

Consumers should preserve producer identities exactly as emitted.

Consumers should not replace producer identities with consumer-generated identifiers.

Consumer-side identities may be added.

Consumer-side identities should not replace producer identities.

---

# Lineage Preservation

Every VAP-TEP contains:

```text
entity_inventory.json

lineage_manifest.json
```

These artifacts provide:

```text
Entity identity

Artifact identity

Checksums

Lineage relationships

Parent-child transitions

Lifecycle reconstruction
```

Consumers should treat lineage information as preservation-critical metadata.

Lineage is not optional documentation.

Lineage is part of the preserved evidence lifecycle.

---

# Transport Fidelity

Certified VAP-TEPs have demonstrated:

```text
Source artifact SHA256
=
TEP artifact SHA256
```

for transported entities.

Accordingly:

```text
TEP transport
=
Preservation
```

rather than:

```text
TEP transport
=
Transformation
```

Consumers should assume that preserved entities are authoritative representations of producer outputs.

---

# Producer Authority

VAP remains authoritative for:

```text
Variant observation

Variant normalization

Variant routing

Variant interpretation

Variant prioritization

Validation planning
```

Consumers may:

```text
Persist

Index

Broker

Discover

Cross-reference
```

Consumers should not redefine producer evidence.

---

# Certified Reference Producer Specimens

The following VAP-TEPs have undergone formal preservation certification.

## HG002

```text
vap_tep_HG002_run_2026_06_03_010030_v1
```

Represents:

```text
WGS reference specimen
```

---

## ERR10619212

```text
vap_tep_ERR10619212_run_2026_05_30_214724_v1
```

Represents:

```text
q1 epilepsy WES specimen
```

---

## ERR10619300

```text
vap_tep_ERR10619300_run_2026_05_27_172531_v1
```

Represents:

```text
median epilepsy WES specimen
```

---

## ERR10619225

```text
vap_tep_ERR10619225_run_2026_05_31_091242_v1
```

Represents:

```text
q3 epilepsy WES specimen
```

These specimens collectively demonstrate preservation behavior across:

```text
WGS

q1 WES

median WES

q3 WES
```

and should be considered the reference VAP producer corpus for early VDB development.

---

# Guidance To Consumers

Consumers should approach VAP-TEPs using the following principle:

```text
Preserve what VAP preserved.
```

Do not assume:

```text
Later stages replace earlier stages.

Prioritization replaces observation.

Validation replaces interpretation.

Context replaces evidence.
```

Instead:

```text
Observation remains authoritative.

Later stages add meaning.

Lineage explains transitions.

Context explains execution.
```

A VAP-TEP is best understood as a preserved evidence lifecycle rather than a collection of independent files.

Consumers that preserve this distinction will be able to fully exploit the evidentiary value of VAP-produced evidence packages.
