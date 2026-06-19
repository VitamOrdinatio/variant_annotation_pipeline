# VAP Transitional Evidence Product (VAP-TEP) Contract

The `vap_tep_contract.md` defines what a VAP-TEP is and is supported by the following:

```text
vap_tep_contract.md (this document)
        ↓
vap_tep_transport_requirements.md
        ↓
vap_tep_acceptance_criteria.md
        ↓
implementation
```

See also:

- [VAP TEP Transport Requirements](../interfaces/vap_tep_transport_requirements.md)
- [VAP TEP Acceptance Criteria](../validation/vap_tep_acceptance_criteria.md)

---

## Purpose

This contract defines the minimum required structure, preservation requirements, lineage requirements, and validation expectations for a VAP Transitional Evidence Product (VAP-TEP).

A VAP-TEP is the canonical evidence transport artifact produced by VAP for downstream ecosystem consumers.

The primary purpose of a VAP-TEP is preservation.

A VAP-TEP must preserve the evidence lifecycle produced by VAP without collapsing observation, normalization, interpretation, prioritization, or validation context.

This contract defines the minimum preservation-compliant VAP-TEP.

---

# 1. Scope

This contract applies to:

```text
VAP
    →
VAP-TEP
    →
VDB
```

transport operations.

This contract does not define:

* VDB persistence behavior
* VDB query behavior
* RDGP consumption behavior
* downstream materialized views

Those systems consume VAP-TEPs but are governed by separate contracts.

---

# 2. Preservation Philosophy

A VAP-TEP is an evidence-preservation artifact.

A VAP-TEP is not:

* a candidate report
* a prioritization report
* a validation report

Those artifacts may be derived from a VAP-TEP but do not replace it.

Preservation must maintain traceability across the complete evidence lifecycle:

```text
Observation
    ↓
Normalization
    ↓
Interpretation
    ↓
Prioritization
    ↓
Validation
```

---

# 3. Required Entities

A preservation-compliant VAP-TEP must contain the following logical entities.

## 3.1 Observation Entity

### Source

```text
Stage07
```

### Role

Preserves the earliest biologically interpretable observation boundary.

### Required Characteristics

Must preserve:

* variant identity
* sample identity
* genotype context
* gene mappings
* transcript mappings
* consequence annotations
* population-frequency annotations
* clinical annotations

### Canonical Role

```text
Observation Entity
```

---

## 3.2 Normalization Entity

### Source

```text
Stage08
```

### Role

Preserves semantic normalization context.

### Required Characteristics

Must preserve normalized context including:

```text
annotation_source
annotation_version
gene_mapping_status

variant_context
variant_effect_severity

qc_status
interpretability_status

frequency_status
clinical_status
```

### Canonical Role

```text
Normalization Entity
```

---

## 3.3 Routing Entity

### Source

```text
Stage08
```

### Role

Preserves deterministic routing behavior.

### Required Characteristics

Must preserve routing surfaces used by downstream interpretation.

Examples include:

```text
coding candidates
splice candidates
noncoding candidates
```

### Canonical Role

```text
Routing Entity
```

### Rationale

Routing behavior represents evidence lineage and must remain auditable.

Routing surfaces are not required to be mutually exclusive.

In VAP v1, splice-region candidates function as a routing overlay that is subsequently consumed by coding interpretation.

Consumers MUST NOT assume routing surfaces represent disjoint partitions.

---

## 3.4 Coding Interpretation Overlay

### Source

```text
Stage09
```

### Role

Preserves coding-specific interpretation context.

### Required Characteristics

Examples include:

```text
functional_impact
coding_interpretation_label

rarity_flag
clinical_evidence
qc_reliability

is_lof_candidate
is_rare_candidate
is_clinically_supported
```

### Canonical Role

```text
Coding Interpretation Overlay
```

---

## 3.5 Noncoding Interpretation Overlay

### Source

```text
Stage10
```

### Role

Preserves noncoding-specific interpretation context.

### Required Characteristics

Examples include:

```text
noncoding_functional_context
noncoding_interpretation_label

rarity_flag
clinical_evidence
qc_reliability

is_regulatory_candidate
is_rare_candidate
is_clinically_supported
```

### Canonical Role

```text
Noncoding Interpretation Overlay
```

---

## 3.6 Prioritization Overlay

### Source

```text
Stage11
```

### Role

Preserves deterministic prioritization context.

### Required Characteristics

Examples include:

```text
priority_tier
priority_rank
priority_reason

variant_origin
source_interpretation_label
```

### Canonical Role

```text
Prioritization Overlay
```

---

## 3.7 Validation Overlay

### Source

```text
Stage12
```

### Role

Preserves validation-preparation context.

### Required Characteristics

Examples include:

```text
validation_required
validation_priority

suggested_validation_method
validation_reason
```

### Canonical Role

```text
Validation Overlay
```

---

## 3.8 Lineage Manifest

### Source

Generated during TEP construction.

### Role

Binds all preserved entities into a coherent evidence lineage.

### Canonical Role

```text
Lineage Manifest
```

---

## 3.9 Context Sidecar

### Source

```text
Stage13
```

and associated run metadata.

### Role

Preserves audit and execution context.

### Canonical Role

```text
Context Sidecar
```

### Important

The Context Sidecar is not a primary evidence entity.

The Context Sidecar supplements preserved evidence entities.

---

# 4. Required Identifiers

Every VAP-TEP must preserve:

```text
tep_id
tep_schema_version

sample_id
run_id

variant_id
```

as authoritative identifiers.

---

# 5. Required Lineage

A VAP-TEP must preserve artifact-level lineage.

At minimum:

```text
source_artifact

source_artifact_sha256

row_count
column_count

parent_artifacts
child_artifacts

entity_role
```

must be preserved.

---

# 6. Stage07–Stage08 Preservation Linkage

The relationship between Stage07 and Stage08 is mandatory.

A VAP-TEP must preserve:

```text
Stage07 Observation Entity
```

and

```text
Stage08 Normalization Entity
```

as distinct entities.

Stage07 observation lineage
must remain traceable into Stage08 normalization lineage.

For VAP v1, empirical forensics demonstrate:

```text
Stage07 row count
=
Stage08 row count

Stage07 distinct variant_ids
=
Stage08 distinct variant_ids
```

Future VAP versions are not required to preserve row-count parity provided observation identity and lineage continuity remain intact.

---

# 7. Preservation Requirements

A VAP-TEP must:

* preserve observation context
* preserve normalization context
* preserve interpretation context
* preserve prioritization context
* preserve validation context

A VAP-TEP must not rely solely upon candidate-oriented outputs.

---

# 8. Canonical Preservation Model

The canonical VAP-TEP model is:

```text
Observation Entity
    ↓

Normalization Entity
    ↓

Routing Entity
    ↓

Coding Interpretation Overlay
Noncoding Interpretation Overlay
    ↓

Prioritization Overlay
    ↓

Validation Overlay
```

with explicit lineage connecting all entities.

---

# 9. Explicit Exclusions

The following are not canonical VAP-TEP entities:

## Candidate Reports

Candidate reports are derived views.

They do not replace preserved evidence entities.

## Merged Evidence Views

Merged evidence views may be materialized for convenience.

Merged evidence views are not canonical preservation entities.

## Stage13 Evidence Substitution

Stage13 metadata must not replace preserved evidence entities.

Stage13 exists as contextual support only.

---

# 10. Future Compatibility

Future VAP releases may introduce:

* alternative transcript models
* multi-transcript interpretation
* expanded noncoding interpretation
* additional downstream interoperability surfaces

VAP-TEP implementations must preserve evidence lineage in a manner that remains compatible with future expansion.

Accordingly, preservation entities should not assume that current Stage08 surfaces remain semantically identical in future VAP versions.
