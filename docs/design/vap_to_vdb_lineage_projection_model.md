# VAP → VDB Lineage Projection Model

```text
Identity Preservation Model
    ↓
What identities exist?

Lineage Projection Model (this doc)
    ↓
How are entities connected?

Ingestion Flow
    ↓
How does evidence enter VDB?

Namespace Brokerage Model
    ↓
How does VDB create a unified discovery surface?

HG002 Architecture Walkthrough
    ↓
Can we validate end-to-end VAP to VDB exemplar movement?
```

See also:
- [Identity Preservation Model](./vap_to_vdb_identity_preservation_model.md)
- [Lineage Projection Model](./vap_to_vdb_lineage_projection_model.md)
- [Ingestion Flow](./vap_to_vdb_ingestion_flow.md)
- [Namespace Brokerage Model](./vap_to_vdb_namespace_brokerage_model.md)
- [VAP to VDB: HG002 Architecture Walkthrough](../validation/vap_to_vdb_architecture_walkthrough.md)

---

## Purpose

This document defines how VAP evidence lineage should be projected into VDB.

This document does not define lineage.

Lineage is already defined by:

```text
VAP Preservation Doctrine

VAP-TEP Preservation Lineage Model

VAP-TEP Evidence Lineage Forensics
```

The purpose of this document is to define how VDB preserves, persists, reconstructs, and exposes that lineage.

---

# Governing Principle

```text
VAP defines lineage.

VDB preserves lineage.
```

VDB is not the owner of evidence lineage.

VDB is the custodian of evidence lineage.

---

# Core Preservation Objective

A future consumer should be able to begin with any persisted VAP-derived entity and reconstruct:

```text
What observation originated this evidence?

What transformations occurred?

Which overlays contributed context?

Which prioritization decisions affected it?

Which validation decisions affected it?

Which run produced it?
```

without requiring access to the original VAP execution environment.

---

# Source Lineage Authority

The authoritative lineage model originates from VAP.

The canonical preservation hierarchy is:

```text
Stage07
    Observation Entity

Stage08
    Normalization Entity

Stage09
    Coding Interpretation Overlay

Stage10
    Noncoding Interpretation Overlay

Stage11
    Prioritization Overlay

Stage12
    Validation Overlay

Stage13
    Context Sidecar
```

VDB must preserve this hierarchy.

VDB must not redefine it.

---

# Projection Philosophy

Lineage projection is not duplication.

Lineage projection is preservation.

The objective is:

```text
Preserve lineage semantics

while allowing

implementation flexibility
```

Different VDB implementations may use:

```text
relational structures

graph structures

document structures

hybrid structures
```

The preservation requirement is reconstructability.

Not implementation uniformity.

---

# Lineage Classes

VAP-derived lineage contains multiple distinct classes.

These classes should remain distinguishable.

---

# Artifact Lineage

## Definition

Relationships between VAP-produced artifacts.

Example:

```text
stage_07_annotated_variants.tsv
        ↓
stage_08_vdb_ready_variants.tsv
```

Artifact lineage explains:

```text
which files produced which files
```

Artifact lineage is primarily provenance-oriented.

---

# Entity Lineage

## Definition

Relationships between evidence entities.

Example:

```text
Observation Entity
        ↓
Normalization Entity
```

Entity lineage explains:

```text
which evidence state
evolved into which evidence state
```

Entity lineage is the primary scientific lineage class.

---

# Overlay Lineage

## Definition

Relationships between an observation and accumulated context.

Example:

```text
Observation
        ↓
Coding Interpretation Overlay
```

Overlay lineage is additive.

It does not replace upstream entities.

---

# Transport Lineage

## Definition

Relationships introduced by TEP construction.

Example:

```text
Source Artifact
        ↓
Transport Entity
        ↓
Persisted Entity
```

Transport lineage explains:

```text
how evidence moved
```

rather than:

```text
how evidence evolved biologically
```

---

# Persistence Lineage

## Definition

Relationships created inside VDB.

Examples:

```text
entity_id
        ↓
record_id

entity_id
        ↓
graph_node_id
```

Persistence lineage supports implementation.

Persistence lineage is not scientific lineage.

---

# Minimum Reconstructable Path

A compliant VDB implementation must be able to reconstruct:

```text
Observation Entity
        ↓
Normalization Entity
        ↓
Interpretation Overlay
        ↓
Prioritization Overlay
        ↓
Validation Overlay
```

for every preserved variant entity.

---

# Observation Projection

## Source Authority

```text
Stage07
```

## VDB Requirement

The Observation Entity must remain identifiable.

Required recoverable attributes include:

```text
sample_id

run_id

variant_id

entity_role

source_stage
```

Observation lineage is the root lineage node.

All downstream lineage traces must ultimately terminate at an Observation Entity.

---

# Normalization Projection

## Source Authority

```text
Stage08
```

## VDB Requirement

Normalization must remain linked to:

```text
Observation Entity
```

Required projection:

```text
Observation
        ↓
Normalization
```

VDB must preserve proof that normalization did not sever observational identity.

---

# Coding Interpretation Projection

## Source Authority

```text
Stage09
```

## VDB Requirement

Coding interpretation must remain linked to:

```text
Normalization Entity
```

Required projection:

```text
Observation
        ↓
Normalization
        ↓
Coding Interpretation
```

Coding interpretation must remain recognizable as an overlay.

---

# Noncoding Interpretation Projection

## Source Authority

```text
Stage10
```

## VDB Requirement

Noncoding interpretation must remain linked to:

```text
Normalization Entity
```

Required projection:

```text
Observation
        ↓
Normalization
        ↓
Noncoding Interpretation
```

Noncoding interpretation must remain recognizable as an overlay.

---

# Prioritization Projection

## Source Authority

```text
Stage11
```

## VDB Requirement

Prioritization must remain linked to the interpretation lineage that produced it.

Required projection:

```text
Coding Interpretation
            ↘
             Prioritization
            ↗
Noncoding Interpretation
```

Prioritization must not become the root evidence node.

---

# Validation Projection

## Source Authority

```text
Stage12
```

## VDB Requirement

Validation must remain linked to:

```text
Prioritization
```

Required projection:

```text
Prioritization
        ↓
Validation
```

Validation status is operational context.

Not observational identity.

---

# Context Sidecar Projection

## Source Authority

```text
Stage13
```

## VDB Requirement

Stage13 should be projected as:

```text
run-level context
```

## Stage13 Authority Boundary

Stage13 is authoritative for:

```text
execution context

audit context

run-context provenance
```

Stage13 is not authoritative for:

```text
scientific evidence state

variant observation state

interpretation state

prioritization state
```

Stage13 complements preserved evidence.

Stage13 does not replace preserved evidence.

Scientific evidence authority remains anchored to the preserved
evidence lifecycle originating from Stage07.

Examples:

```text
execution metadata

summary artifacts

audit artifacts

runtime artifacts
```

Stage13 must not replace scientific evidence lineage.

---

# Required Lineage Edges

A compliant projection model should preserve:

```text
Observation
    →
Normalization

Normalization
    →
Coding Interpretation

Normalization
    →
Noncoding Interpretation

Coding Interpretation
    →
Prioritization

Noncoding Interpretation
    →
Prioritization

Prioritization
    →
Validation
```

These edges represent the minimum preservation graph.

---

# Lineage Query Requirements

VDB should support reconstruction queries such as:

```text
Show me the originating observation.
```

```text
Show me all overlays
applied to this variant.
```

```text
Show me the prioritization
history of this observation.
```

```text
Show me the validation
context associated with this variant.
```

```text
Show me every preserved
state associated with this observation.
```

The exact query mechanism is implementation-specific.

The reconstructability requirement is not.

---

# Lineage Integrity Validation

A compliant VDB implementation should verify:

```text
Every Normalization Entity
has an Observation parent.

Every Interpretation Overlay
has a Normalization parent.

Every Prioritization Overlay
has an Interpretation parent.

Every Validation Overlay
has a Prioritization parent.
```

Broken lineage should be treated as a preservation failure.

---

# Relationship to Identity Preservation

Identity and lineage are complementary.

Identity answers:

```text
What is this?
```

Lineage answers:

```text
How did it become this?
```

A VDB implementation requires both.

Identity without lineage loses evidence history.

Lineage without identity loses evidence ownership.

---

# Relationship to Entity Mapping

The Entity Mapping Matrix defines:

```text
Where entities persist.
```

This document defines:

```text
How entities remain connected.
```

Both are required.

Neither replaces the other.

---

# Success Condition

A lineage projection model is successful if a future consumer can begin with:

```text
Validation Overlay

or

Prioritization Overlay

or

Interpretation Overlay
```

and deterministically reconstruct:

```text
Observation Entity

Normalization Entity

Interpretation History

Prioritization History

Validation History

Run Context

Source Provenance
```

without requiring access to the original VAP repository.

---

# Final Principle

```text
VAP owns lineage.

TEP transports lineage.

VDB preserves lineage.

Future systems reconstruct lineage.
```
