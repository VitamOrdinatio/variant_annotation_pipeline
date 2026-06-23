# VAP → VDB Identity Preservation Model

```text
Identity Preservation Model (this doc)
    ↓
What identities exist?

Lineage Projection Model
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

This document defines the identity preservation model governing ingestion of VAP Transitional Evidence Products (VAP-TEPs) into VDB.

The objective is to ensure that VDB can perform:

```text
canonicalization
normalization
namespace brokerage
entity discovery
cross-repository integration
```

without destroying source identity.

---

# Core Principle

The governing principle is:

```text
Canonical identity may be added.

Source identity must never be replaced.
```

VDB exists to discover relationships.

VDB does not exist to rewrite history.

---

# Identity Preservation Mission

The preservation mission is:

```text
Maintain the ability to reconstruct
the original producer-emitted identity
at any future time.
```

For every entity ingested into VDB, a user must be able to answer:

```text
Who created this?

When was it created?

Where did it originate?

What identifier did the producer assign?

What evidence package transported it?

What transformations occurred afterward?
```

If these questions cannot be answered, identity preservation has failed.

---

# Identity Classes

The VAP → VDB interface contains multiple distinct identity classes.

These identities are not interchangeable.

---

# Source Identity

## Definition

Identity assigned by the producing repository.

Examples:

```text
sample_id
run_id
variant_id
entity_id
tep_id
source_package_id
```

Source identities are authoritative.

Source identities MUST remain recoverable.

---

# Canonical Identity

## Definition

Identity created by VDB to support cross-package integration.

Examples:

```text
canonical_variant_id
canonical_gene_id
canonical_transcript_id
canonical_sample_id
canonical_entity_id
```

Canonical identities are secondary.

Canonical identities are never authoritative for provenance reconstruction.

---

# Transport Identity

## Definition

Identity associated with the transported evidence package.

Examples:

```text
tep_id
entity_id
lineage_entity_id
artifact_id
```

Transport identities describe movement.

They do not redefine evidence meaning.

---

# Persistence Identity

## Definition

Identity associated with VDB storage.

Examples:

```text
record_id
row_id
graph_node_id
storage_key
```

Persistence identities exist solely for implementation purposes.

Persistence identities are not scientific identities.

---

# Identity Hierarchy

The identity hierarchy is:

```text
Source Identity
        ↓
Transport Identity
        ↓
Canonical Identity
        ↓
Persistence Identity
```

Authority decreases as one moves downward.

The producer remains the ultimate source of truth.

---

# Identity Authority Model

## VAP Authority

VAP owns:

```text
sample_id
run_id
variant_id
```

Only VAP may define these identities.

VDB must preserve them exactly as emitted.

---

## TEP Authority

TEP owns:

```text
tep_id
entity_id
lineage relationships
```

TEP identities govern transport.

---

## VDB Authority

VDB owns:

```text
canonical identities
brokered identities
storage identities
```

VDB may create additional identities.

VDB may not replace producer identities.

---

# Identity Preservation Requirements

## Requirement IP-001

Source identifiers MUST be persisted.

Examples:

```text
sample_id
run_id
variant_id
```

must remain queryable.

---

## Requirement IP-002

Source identifiers MUST remain recoverable even when canonical identifiers exist.

Example:

```text
canonical_variant_id
    →
variant_id
```

must always be traversable.

---

## Requirement IP-003

Identity mappings MUST be auditable.

Example:

```text
canonical_variant_id
        →
source_variant_id
```

must record:

```text
mapping method
mapping timestamp
mapping version
```

when applicable.

---

## Requirement IP-004

Namespace brokerage MUST be additive.

Allowed:

```text
variant_id
+
canonical_variant_id
```

Not allowed:

```text
canonical_variant_id
replaces
variant_id
```

---

# Identity Mapping Model

## Acceptable Pattern

```text
VAP Variant

variant_id = VAP_VAR_001

        ↓

VDB

canonical_variant_id = CAN_VAR_847

        ↓

Mapping Table

CAN_VAR_847
    ↔
VAP_VAR_001
```

Both identities remain recoverable.

---

## Prohibited Pattern

```text
VAP Variant

variant_id = VAP_VAR_001

        ↓

VDB

canonical_variant_id = CAN_VAR_847

        ↓

discard source identifier
```

The original identity is lost.

This is prohibited.

---

# Variant Identity Preservation

The following identities must remain recoverable:

```text
sample_id
run_id
variant_id
```

These three identities collectively define the primary VAP evidence origin.

Future reinterpretation depends upon preserving all three.

---

# Run Identity Preservation

Run identity is particularly important.

Example:

```text
HG002
```

may appear in multiple runs.

Therefore:

```text
sample_id
```

alone is insufficient.

The pair:

```text
sample_id
+
run_id
```

must remain recoverable.

---

# Entity Identity Preservation

Every transported entity must retain:

```text
entity_id
entity_role
source_stage
```

These identities are required for lineage reconstruction.

---

# Package Identity Preservation

The following identities define package provenance:

```text
tep_id
source_package_id
```

These identities must remain recoverable for all persisted entities.

---

# Namespace Brokerage Model

Namespace brokerage is expected.

Examples include:

```text
Ensembl Gene
→ Canonical Gene

RefSeq Transcript
→ Canonical Transcript

Producer Variant
→ Canonical Variant
```

Brokerage is beneficial.

Brokerage is not ownership transfer.

The source identity remains authoritative.

---

# Cross-Repository Identity Model

Future VDB ingestion will likely include:

```text
VAP
GSC
RDGP
RSP
```

Each repository owns its source identities.

VDB serves as an identity broker.

VDB does not become the owner of producer identities.

---

# Identity Collision Handling

Identity collisions should never be resolved through identifier replacement.

Instead:

```text
collision detected
        ↓
new canonical identity
        ↓
mapping records
        ↓
preserve all source identities
```

Collision resolution must be additive.

---

# Identity Auditability

Every canonical identity should support reconstruction of:

```text
source repository
source package
source run
source identifier
mapping history
```

A user should be able to move from:

```text
canonical identity
```

back to:

```text
original producer identity
```

without ambiguity.

---

# Identity Preservation Validation Questions

A compliant VDB implementation should be able to answer:

```text
Can I recover the original variant_id?

Can I recover the original run_id?

Can I recover the original sample_id?

Can I recover the original tep_id?

Can I determine which repository created this?

Can I determine how canonicalization occurred?
```

If any answer is "no", identity preservation is incomplete.

---

# Relationship to Lineage Preservation

Identity preservation and lineage preservation are complementary.

Identity answers:

```text
What is this?
```

Lineage answers:

```text
How did it become this?
```

Both are required for future reinterpretation.

Neither is sufficient alone.

---

# Success Condition

Identity preservation is successful when VDB can provide:

```text
Canonical identities for discovery.

Source identities for provenance.

Transport identities for reconstruction.

Persistence identities for implementation.
```

simultaneously.

The presence of one identity class must never require destruction of another.

---

# Final Principle

```text
Discover broadly.

Canonicalize carefully.

Preserve origins completely.
```
