# VAP → VDB Entity Mapping Matrix

## Purpose

This document defines the conceptual mapping between VAP-TEP entities and their expected persistence domains within VDB.

This document does not define:

```text
physical database schemas
table names
SQL definitions
indexing strategies
query APIs
```

Instead, it defines the preservation expectations required for faithful VAP evidence ingestion.

This document should be read alongside:

- [VAP -> VDB: TEP Ingestion Interface](../contracts/system/interfaces/vap_to_vdb_tep_ingestion_interface.md)

- [VAP -> VDB: TEP Ingestion Readiness Checklist](../contracts/system/validation/vap_to_vdb_tep_ingestion_readiness_checklist.md)


---

# Governing Principle

The governing principle of this mapping is:

```text
Preserve evidence topology.

Do not flatten evidence.
```

VDB is permitted to create derived query surfaces.

VDB is not permitted to destroy source topology.

---

# Mapping Overview

```text
VAP Stage07 Observation Entity
    ↓
VDB Variant Observation Domain

VAP Stage08 Normalization Entity
    ↓
VDB Annotation Domain

VAP Stage08 Routing Entity
    ↓
VDB Semantic Partition Domain

VAP Stage09 Coding Overlay
    ↓
VDB Interpretation Domain

VAP Stage10 Noncoding Overlay
    ↓
VDB Interpretation Domain

VAP Stage11 Prioritization Overlay
    ↓
VDB Prioritization Domain

VAP Stage12 Validation Overlay
    ↓
VDB Validation Domain

VAP Context Sidecar
    ↓
VDB Provenance Domain
```

---

# Entity Mapping Matrix

| VAP Entity             | Source Stage | VDB Persistence Domain | Required Preserved Identity   | Required Lineage                  |
| ---------------------- | ------------ | ---------------------- | ----------------------------- | --------------------------------- |
| Observation Entity     | Stage07      | Variant Observation    | sample_id, run_id, variant_id | root entity                       |
| Normalization Entity   | Stage08      | Annotation             | entity_id, source_stage       | Stage07 → Stage08                 |
| Routing Entity         | Stage08      | Semantic Partition     | entity_id, route_id           | Stage08 → Routing                 |
| Coding Overlay         | Stage09      | Interpretation         | variant_id                    | Routing → Coding                  |
| Noncoding Overlay      | Stage10      | Interpretation         | variant_id                    | Routing → Noncoding               |
| Prioritization Overlay | Stage11      | Prioritization         | variant_id                    | Coding/Noncoding → Prioritization |
| Validation Overlay     | Stage12      | Validation             | variant_id                    | Prioritization → Validation       |
| Context Sidecar        | Stage13      | Provenance             | run_id, tep_id                | package-level                     |

---

# Variant Observation Domain

## Purpose

Represents the earliest preserved biological observation boundary.

Authoritative source:

```text
Stage07
```

Expected content:

```text
variant identity
genomic coordinates
alleles
genotypes
gene mappings
transcript mappings
consequence annotations
population annotations
clinical annotations
```

Preservation requirements:

```text
MUST preserve source identities.
MUST preserve Stage07 recoverability.
MUST remain queryable independently.
```

---

# Annotation Domain

## Purpose

Represents semantic normalization applied by Stage08.

Expected content:

```text
mapping status
annotation source
annotation versions
frequency classifications
clinical classifications
quality classifications
```

Preservation requirements:

```text
MUST remain linked to Stage07.
MUST preserve annotation provenance.
```

---

# Semantic Partition Domain

## Purpose

Represents deterministic routing surfaces.

Examples:

```text
coding
noncoding
splice
review-ready
RDGP-compatible
```

Preservation requirements:

```text
Routes may overlap.
Routes are not mutually exclusive.
```

---

## Future Splice Compatibility

Current VAP releases route splice-associated biology through
coding interpretation pathways.

Accordingly, splice-associated observations currently enter
VDB through the same preservation pathways used for coding
interpretation surfaces.

Future VAP releases may elevate splice evidence to a first-class
semantic overlay.

VDB persistence domains should therefore remain compatible with:

```text
coding interpretation

noncoding interpretation

splice interpretation
```

without requiring:

```text
identity replacement

lineage restructuring

entity remapping
```

Splice-aware expansion should be achievable through additive
semantic surface preservation.

---

# Interpretation Domain

## Purpose

Represents biological interpretation overlays.

Sources:

```text
Stage09
Stage10
```

Expected content:

```text
functional impact
clinical support
rarity interpretation
reviewability signals
semantic labels
```

Preservation requirements:

```text
Coding and noncoding interpretations
must coexist.
```

---

# Prioritization Domain

## Purpose

Represents ranking and triage context.

Source:

```text
Stage11
```

Expected content:

```text
priority tier
priority rank
review rationale
candidate readiness
```

Preservation requirements:

```text
Prioritization is an overlay.
Not a replacement for evidence.
```

---

# Validation Domain

## Purpose

Represents validation-preparation context.

Source:

```text
Stage12
```

Expected content:

```text
validation required
validation rationale
validation priority
recommended validation method
```

Preservation requirements:

```text
Validation is an overlay.
Not a replacement for evidence.
```

---

# Provenance Domain

## Purpose

Represents transport, execution, and audit context.

Expected content:

```text
tep_id
source_package_id
run_id
sample_id
source_artifact
artifact checksums
validator version
validation summaries
```

Preservation requirements:

```text
All persisted entities must remain attributable
to source artifacts.
```

---

# Identity Mapping Expectations

## Source Identities

The following identities originate from VAP:

```text
sample_id
run_id
variant_id
entity_id
tep_id
source_package_id
```

These identities MUST remain recoverable.

---

## Canonical Identities

VDB MAY create:

```text
canonical_variant_id
canonical_gene_id
canonical_transcript_id
canonical_entity_id
```

Canonical identifiers are additive.

They MUST NOT replace source identifiers.

---

# Required Lineage Preservation

Minimum lineage recoverability:

```text
Stage07 Observation
        ↓
Stage08 Normalization
        ↓
Stage08 Routing
       ↙ ↘
Stage09  Stage10
       ↘ ↙
Stage11
        ↓
Stage12
```

VDB MAY materialize lineage differently.

The topology itself must remain reconstructable.

---

# Future Compatibility Requirements

The mapping model MUST remain compatible with:

```text
multi-transcript interpretation
multi-gene mappings
expanded noncoding annotation
future semantic overlays
future validation overlays
future VAP releases
```

No persistence decision should assume current VAP outputs represent the final complexity boundary.

---

# Success Condition

A successful VDB ingestion implementation can answer:

```text
Where did this variant originate?

Which run produced it?

Which artifact produced it?

Which semantic overlays touched it?

Which prioritization decision affected it?

Which validation state affected it?

Can the original Stage07 observation
still be reconstructed?
```

If all six questions can be answered, the mapping model is functioning correctly.
