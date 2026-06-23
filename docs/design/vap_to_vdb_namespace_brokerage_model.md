# VAP → VDB Namespace Brokerage Model

```text
Identity Preservation Model
    ↓
What identities exist?

Lineage Projection Model
    ↓
How are entities connected?

Ingestion Flow
    ↓
How does evidence enter VDB?

Namespace Brokerage Model (this doc)
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

This document defines the namespace brokerage model governing VAP evidence after trusted ingestion into VDB.

The objective is to enable:

```text
cross-repository discovery

cross-package interoperability

identity reconciliation

future evidence federation
```

while preserving producer authority and source identity.

This document should be interpreted as a brokerage doctrine rather than an implementation specification.

---

# Governing Principle

```text
Brokerage is additive.

Brokerage is not replacement.
```

VDB may create new identities.

VDB may create new mappings.

VDB may create new discovery surfaces.

VDB must not erase producer identities.

---

# Why Namespace Brokerage Exists

Independent repositories naturally develop independent identity systems.

Examples include:

```text
VAP
    variant-centric

GSC
    phenotype-gene-centric

RDGP
    sample-gene-centric

RSP
    transcript/gene-expression-centric
```

All four repositories may refer to related biological entities.

They do not necessarily refer to them in the same way.

Namespace brokerage exists to connect these perspectives without forcing repositories to abandon their own identities.

---

# Core Thesis

VDB is not the owner of producer identities.

VDB is the broker of relationships between identities.

The distinction is critical.

Producer authority remains with the producing repository.

VDB provides discoverability.

---

# Authority Hierarchy

## Producer Authority

The producer owns source identity.

Examples:

```text
VAP
    variant_id
    sample_id
    run_id

GSC
    gene_id
    phenotype_id

RDGP
    prioritized_gene_id
    sample_id

RSP
    transcript_id
    gene_id
```

Producer identities are authoritative.

---

## Transport Authority

TEP owns transport identities.

Examples:

```text
tep_id

entity_id

artifact_id
```

Transport identities describe movement.

They do not redefine evidence.

---

## Brokerage Authority

VDB owns:

```text
canonical identities

brokered identities

cross-repository mappings
```

Brokered identities exist to connect evidence.

Not to replace evidence.

---

# Namespace Classes

VDB operates over multiple namespace classes.

These classes must remain distinguishable.

---

# Source Namespace

## Definition

Identifiers emitted by producers.

Examples:

```text
variant_id

sample_id

run_id

gene_id

phenotype_id
```

Characteristics:

```text
authoritative

repository-owned

immutable
```

---

# Transport Namespace

## Definition

Identifiers emitted by TEP construction.

Examples:

```text
tep_id

entity_id

lineage_entity_id
```

Characteristics:

```text
transport-oriented

repository-independent

preservation-focused
```

---

# Canonical Namespace

## Definition

Identifiers created by VDB.

Examples:

```text
canonical_variant_id

canonical_gene_id

canonical_transcript_id

canonical_sample_id
```

Characteristics:

```text
discovery-oriented

cross-repository

broker-managed
```

---

# Persistence Namespace

## Definition

Identifiers created by storage systems.

Examples:

```text
record_id

graph_node_id

storage_key
```

Characteristics:

```text
implementation-oriented

non-scientific

replaceable
```

---

# Brokerage Objectives

The brokerage layer should support:

```text
identity reconciliation

cross-repository traversal

evidence federation

discovery acceleration
```

without altering source identities.

---

# Variant Brokerage

## Example

VAP emits:

```text
variant_id = VAP_VAR_001
```

VDB may create:

```text
canonical_variant_id = CAN_VAR_847
```

Required relationship:

```text
CAN_VAR_847
        ↔
VAP_VAR_001
```

Both identities remain recoverable.

---

# Gene Brokerage

## Example

Multiple repositories may reference:

```text
ENSG00000100150
```

using different contexts.

Examples:

```text
GSC
    phenotype-gene relevance

RDGP
    sample-gene priority

RSP
    expression signal

VAP
    variant-gene relationship
```

VDB may broker all of these relationships through:

```text
canonical_gene_id
```

while preserving original producer identifiers.

---

# Sample Brokerage

## Example

Multiple repositories may reference:

```text
HG002
```

through different evidence products.

VDB may create:

```text
canonical_sample_id
```

to connect evidence.

However:

```text
sample_id
```

must remain recoverable.

---

# Phenotype Brokerage

## Example

Future repositories may emit:

```text
epilepsy

DEE

GGE

NAFE
```

using differing ontologies.

VDB may broker:

```text
canonical_phenotype_id
```

while preserving source phenotype representations.

---

# Cross-Repository Federation

## Objective

Enable discovery such as:

```text
Variant
        ↓
Gene
        ↓
Phenotype
        ↓
Expression
        ↓
Prioritization
```

without forcing repositories into a shared internal identity model.

---

## Example Federation Path

```text
VAP Variant
        ↓

Canonical Variant
        ↓

Canonical Gene
        ↓

GSC Phenotype-Gene Evidence
        ↓

RDGP Sample-Gene Priority
```

This relationship emerges through brokerage.

Not through identifier replacement.

---

# Mapping Requirements

Every brokered identity must maintain:

```text
source_repository

source_identifier

mapping_method

mapping_version

mapping_timestamp
```

where applicable.

Brokerage must be auditable.

---

# Identity Collision Handling

Namespace collisions are expected.

Collision handling must be additive.

---

## Allowed

```text
new canonical identity

mapping records

multiple source identities
```

---

## Prohibited

```text
replace source identity

discard source identity

rewrite producer identity
```

---

# Brokerage Validation Questions

A compliant brokerage model should answer:

```text
Which repository created this identity?
```

```text
Which canonical identity references it?
```

```text
How was the mapping generated?
```

```text
Which evidence packages contributed?
```

```text
Can the original source identity be recovered?
```

If any answer is unavailable, brokerage is incomplete.

---

# Relationship to Identity Preservation

Identity preservation defines:

```text
what identities exist
```

Brokerage defines:

```text
how identities relate
```

Brokerage must never violate identity preservation requirements.

---

# Relationship to Lineage Projection

Lineage explains:

```text
how evidence evolved
```

Brokerage explains:

```text
how evidence connects
```

Both are necessary.

They answer different questions.

---

# Relationship to Discovery

Discovery should operate primarily through:

```text
canonical identities
```

while retaining the ability to expose:

```text
source identities
```

when provenance inspection is required.

---

# Future Multi-Repository Ecosystem

The brokerage model should remain compatible with:

```text
VAP

GSC

RDGP

RSP

future repositories
```

without requiring any repository to adopt another repository's internal identity system.

---

# Success Condition

A successful brokerage model allows a user to begin with:

```text
variant

gene

phenotype

sample

transcript
```

and traverse evidence across repositories while still being able to recover:

```text
original producer identity

original producer package

original producer provenance
```

at every step.

---

# Future Brokerage Confidence States

Future VDB releases may support brokerage-confidence classifications.

Examples include:

```text
equivalent

likely_equivalent

possible_equivalent

conflicting

unresolved
```

These classifications represent brokerage metadata.

They do not alter producer identities.

They do not replace producer identities.

They do not transfer identity authority from producers to VDB.

Examples:

```text
VAP variant
        ↓
likely_equivalent
        ↓
canonical variant
```

or:

```text
RSP transcript
        ↓
possible_equivalent
        ↓
canonical transcript
```

Such relationships provide discovery guidance rather than
identity ownership.

Regardless of brokerage confidence state:

```text
source identities remain authoritative
```

and must remain recoverable.

Brokerage confidence classifications are additive metadata
attached to identity relationships and not modifications of
the identities themselves.

---

# Final Principle

```text
Repositories create identities.

TEPs transport identities.

VDB brokers identities.

Source authority remains with the producer.
```
