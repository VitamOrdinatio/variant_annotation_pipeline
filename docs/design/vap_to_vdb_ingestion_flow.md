# VAP → VDB Ingestion Flow

```text
Identity Preservation Model
    ↓
What identities exist?

Lineage Projection Model
    ↓
How are entities connected?

Ingestion Flow (this doc)
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

This document defines the conceptual ingestion flow used when VDB receives a VAP Transitional Evidence Product (VAP-TEP).

This document does not define:

```text
database schemas

physical storage structures

API implementations

query interfaces
```

Instead, this document defines the sequence of preservation-oriented operations required to safely ingest VAP evidence into VDB.

This document should be read alongside:

```text
vap_to_vdb_tep_ingestion_interface.md

vap_to_vdb_entity_mapping_matrix.md

vap_to_vdb_identity_preservation_model.md

vap_to_vdb_lineage_projection_model.md
```

---

# Governing Principle

```text
Ingestion must preserve
identity,
lineage,
provenance,
and reinterpretability.
```

Ingestion is not merely data loading.

Ingestion is the process through which VDB accepts custodianship of evidence originally produced by VAP.

---

# High-Level Flow

```text
Receive TEP
        ↓
Package Validation
        ↓
Identity Validation
        ↓
Lineage Validation
        ↓
Entity Registration
        ↓
Namespace Registration
        ↓
Persistence Projection
        ↓
Discovery Registration
        ↓
Trusted Ingestion Complete
```

---

# Stage 1: Receive TEP

## Purpose

Establish receipt of a transport package.

Inputs:

```text
VAP-TEP package

TEP metadata

source artifact manifest

validation metadata
```

Outputs:

```text
ingestion event

package registration candidate
```

---

## Required Discoverability

The ingestion process must be able to identify:

```text
tep_id

source_repository

source_package_id

sample_id

run_id
```

before proceeding.

---

# Stage 2: Package Validation

## Purpose

Verify package integrity.

This stage answers:

```text
Is the package complete?
```

---

## Required Checks

### PKG-001

```text
TEP present
```

### PKG-002

```text
lineage manifest present
```

### PKG-003

```text
required entities present
```

### PKG-004

```text
required metadata present
```

### PKG-005

```text
source artifact manifest present
```

### PKG-006

```text
checksums present
```

---

## Outcome

Valid package:

```text
continue
```

Invalid package:

```text
reject

or

quarantine
```

---

# Stage 3: Identity Validation

## Purpose

Verify preservation-critical identities.

This stage answers:

```text
Can evidence origins be reconstructed?
```

---

## Required Checks

### ID-001

```text
sample_id present
```

### ID-002

```text
run_id present
```

### ID-003

```text
variant_id recoverable
```

### ID-004

```text
entity_id recoverable
```

### ID-005

```text
tep_id recoverable
```

### ID-006

```text
source_package_id recoverable
```

---

## Outcome

All preservation-critical identities must be discoverable before persistence.

---

# Stage 4: Lineage Validation

## Purpose

Verify reconstructable evidence history.

This stage answers:

```text
Can evidence evolution be reconstructed?
```

---

## Required Checks

### LIN-001

```text
Observation Entity present
```

### LIN-002

```text
Normalization Entity present
```

### LIN-003

```text
Interpretation Overlays present
```

### LIN-004

```text
Prioritization Overlay present
```

### LIN-005

```text
Validation Overlay present
```

---

## Required Edge Validation

```text
Observation
        →
Normalization

Normalization
        →
Interpretation

Interpretation
        →
Prioritization

Prioritization
        →
Validation
```

must be reconstructable.

---

## Outcome

Broken lineage:

```text
reject

or

quarantine
```

---

# Stage 5: Entity Registration

## Purpose

Register incoming VAP entities.

This stage establishes VDB awareness of:

```text
Observation Entities

Normalization Entities

Interpretation Entities

Prioritization Entities

Validation Entities
```

without yet assigning canonical identities.

---

## Preservation Rule

Registration must preserve:

```text
source identity
```

before any namespace brokerage occurs.

---

# Stage 6: Namespace Registration

## Purpose

Prepare entities for future brokerage.

This stage does not perform identity replacement.

Instead it records:

```text
known source namespaces
```

Examples:

```text
VAP variant identity

Ensembl gene identity

RefSeq transcript identity

ClinVar identifiers
```

---

## Preservation Rule

Source identities remain authoritative.

Namespace registration is additive.

---

# Stage 7: Persistence Projection

## Purpose

Project entities into VDB persistence domains.

Examples include:

```text
Observation Domain

Annotation Domain

Interpretation Domain

Prioritization Domain

Validation Domain

Provenance Domain
```

---

## Projection Rule

Projection must preserve:

```text
identity

lineage

entity role

provenance
```

Projection must not flatten evidence topology.

---

# Stage 8: Provenance Registration

## Purpose

Register evidence provenance.

This stage establishes:

```text
where evidence originated

which package transported it

which artifacts contributed it

which run generated it
```

---

## Required Provenance

Examples:

```text
source_repository

source_package_id

source_artifact

source_artifact_sha256

run_id

sample_id
```

---

## Preservation Rule

Every persisted entity must remain attributable to a source artifact.

---

# Stage 9: Discovery Registration

## Purpose

Make preserved evidence discoverable.

This stage creates discovery-facing metadata.

Examples:

```text
entity classifications

semantic categories

evidence domains

search surfaces

routing surfaces
```

---

## Preservation Rule

Discovery metadata must not replace source evidence.

Discovery is additive.

---

# Stage 10: Trusted Ingestion Certification

## Purpose

Determine whether evidence is eligible for trusted VDB status.

This stage answers:

```text
Can VDB safely become
custodian of this evidence?
```

---

## Certification Requirements

All of the following must succeed:

```text
Package Validation

Identity Validation

Lineage Validation

Entity Registration

Persistence Projection

Provenance Registration
```

---

## Outcome

Successful:

```text
Trusted Ingestion Approved
```

Failed:

```text
Trusted Ingestion Denied
```

or

```text
Quarantine Ingestion
```

---

# Quarantine Flow

## Purpose

Allow inspection of incomplete packages without polluting trusted evidence stores.

Flow:

```text
Receive Package
        ↓
Validation Failure
        ↓
Quarantine Registration
        ↓
Diagnostic Review
```

---

## Quarantine Restrictions

Quarantined entities must not appear in:

```text
normal discovery surfaces

review workflows

trusted query results
```

until validation issues are resolved.

---

# Relationship to Preservation Doctrine

The VAP preservation package establishes:

```text
What must survive.
```

This ingestion flow establishes:

```text
How survival is verified.
```

The ingestion flow must not weaken preservation doctrine.

---

# Relationship to Identity Preservation

Identity preservation answers:

```text
What is this?
```

The ingestion flow ensures:

```text
identity remains intact
during persistence.
```

---

# Relationship to Lineage Projection

Lineage projection answers:

```text
How did this become this?
```

The ingestion flow ensures:

```text
that history remains reconstructable.
```

---

# Relationship to Namespace Brokerage

Namespace brokerage occurs after trusted ingestion.

Brokerage may add:

```text
canonical identities

brokered identities

cross-repository mappings
```

Brokerage must not replace source identities.

Accordingly:

```text
Trusted Ingestion
        ↓
Namespace Brokerage
```

rather than:

```text
Namespace Brokerage
        ↓
Trusted Ingestion
```

---

# Future Multi-Repository Flow

The ingestion sequence should remain compatible with:

```text
VAP

GSC

RDGP

RSP

future repositories
```

Each repository should follow:

```text
Receive
        ↓
Validate
        ↓
Register
        ↓
Persist
        ↓
Discover
```

while preserving repository-specific identity and lineage models.

---

# Success Condition

A successful ingestion flow allows a future consumer to begin with any persisted entity and determine:

```text
Who produced this?

Which package transported it?

Which run generated it?

Which observation originated it?

Which overlays affected it?

Why was it prioritized?

Why was it validation-ready?
```

without requiring access to the original VAP repository.

---

# Final Principle

```text
Receive faithfully.

Validate rigorously.

Persist conservatively.

Broker additively.

Discover safely.
```
