# VAP → VDB Architecture Walkthrough

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

Namespace Brokerage Model
    ↓
How does VDB create a unified discovery surface?

HG002 Architecture Walkthrough (this doc)
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

This document provides an end-to-end architectural walkthrough illustrating how a VAP observation moves from:

```text
VAP Execution
        ↓
VAP-TEP Construction
        ↓
VDB Ingestion
        ↓
Identity Preservation
        ↓
Lineage Projection
        ↓
Namespace Brokerage
        ↓
Discovery
```

The objective is to validate that the VAP→VDB architecture preserves:

```text
identity

lineage

provenance

interpretation history

future reinterpretability
```

throughout the evidence lifecycle.

This document serves as a conceptual validation artifact.

It is not an implementation specification.

---

# Validation Scenario

## Source Run

Representative execution:

```text
HG002

run_2026_06_03_010030
```

The walkthrough uses a hypothetical variant from the HG002 evidence substrate.

The specific biological interpretation is not important.

The preservation behavior is.

---

# Stage 1: Observation Creation

## VAP Stage07

At Stage07 VAP establishes the earliest scientifically interpretable observation boundary.

Observation:

```text
sample_id = HG002

run_id = run_2026_06_03_010030

variant_id = VAR_001
```

Associated context:

```text
genotype

genomic coordinates

gene association

transcript association

consequence annotation

clinical annotation

population annotation
```

At this point VAP has answered:

```text
What was observed?
```

The observation becomes the preservation anchor.

---

# Stage 2: Normalization

## VAP Stage08

The Stage07 observation is projected into the Stage08 interoperability substrate.

The observation receives:

```text
variant_context

variant_effect_severity

frequency_status

clinical_status

gene_mapping_status

annotation_version
```

Result:

```text
Observation Entity
        ↓
Normalization Entity
```

The underlying observation remains unchanged.

The observation is organized.

Not replaced.

---

# Stage 3: Interpretation

The normalized observation enters interpretation workflows.

---

## Coding Path

Stage09 may contribute:

```text
functional_impact

coding_interpretation_label

clinical_evidence

rarity_flag
```

Result:

```text
Observation
        ↓
Normalization
        ↓
Coding Interpretation
```

---

## Noncoding Path

Stage10 may contribute:

```text
regulatory_context

noncoding_interpretation_label

clinical_evidence

rarity_flag
```

Result:

```text
Observation
        ↓
Normalization
        ↓
Noncoding Interpretation
```

The original observation still exists.

Interpretation remains additive.

---

# Stage 4: Prioritization

## VAP Stage11

Interpreted evidence enters prioritization.

Examples:

```text
priority_tier

priority_rank

priority_reason
```

Result:

```text
Observation
        ↓
Normalization
        ↓
Interpretation
        ↓
Prioritization
```

At this point VAP answers:

```text
What did VAP consider important?
```

VAP has not forgotten:

```text
What was observed?
```

---

# Stage 5: Validation Preparation

## VAP Stage12

The observation receives validation context.

Examples:

```text
validation_required

validation_priority

validation_reason
```

Result:

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

The evidence lifecycle is now complete.

---

# Stage 6: VAP-TEP Construction

The completed evidence lifecycle is projected into a VAP-TEP.

The TEP preserves:

```text
Observation Entity

Normalization Entity

Interpretation Overlays

Prioritization Overlay

Validation Overlay

Provenance

Lineage Manifest
```

The TEP does not collapse evidence.

The TEP transports evidence.

---

# Stage 7: VDB Receipt

The VAP-TEP arrives at VDB.

VDB receives:

```text
tep_id

source_package_id

sample_id

run_id

variant_id

entity lineage
```

At this stage:

```text
No brokerage occurs.
```

```text
No canonicalization occurs.
```

The package remains producer-authored evidence.

---

# Stage 8: Identity Validation

VDB verifies:

```text
sample_id present

run_id present

variant_id present

entity_id present

tep_id present
```

The observation remains attributable to:

```text
HG002

run_2026_06_03_010030

VAR_001
```

Identity remains intact.

---

# Stage 9: Lineage Validation

VDB verifies:

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

is reconstructable.

The lineage graph survives ingestion.

---

# Stage 10: Persistence Projection

The observation is projected into VDB persistence domains.

Examples:

```text
Observation Domain

Annotation Domain

Interpretation Domain

Prioritization Domain

Validation Domain

Provenance Domain
```

Projection preserves:

```text
identity

lineage

entity role

source authority
```

Projection does not flatten evidence.

---

# Stage 11: Canonical Registration

VDB creates discovery-oriented identities.

Example:

```text
variant_id = VAR_001
```

may become:

```text
canonical_variant_id = CAN_VAR_847
```

Required relationship:

```text
CAN_VAR_847
        ↔
VAR_001
```

Source identity remains recoverable.

---

# Stage 12: Namespace Brokerage

VDB identifies relationships.

Example:

```text
VAR_001
        ↓
Gene X
```

Gene X may also appear in:

```text
GSC

RDGP

RSP
```

Brokerage establishes connections:

```text
Variant
        ↓
Canonical Gene
        ↓
Phenotype Evidence

Expression Evidence

Prioritization Evidence
```

No producer identity is replaced.

---

# Stage 13: Discovery

A future user searches VDB.

Entry point:

```text
Gene X
```

Discovery surfaces reveal:

```text
VAP Variant Evidence

GSC Phenotype Evidence

RDGP Prioritization Evidence

RSP Expression Evidence
```

The repositories become connected.

Not merged.

---

# Provenance Validation

At every stage the user can determine:

```text
Who produced this?
```

Answer:

```text
VAP
```

---

```text
Which run produced it?
```

Answer:

```text
run_2026_06_03_010030
```

---

```text
Which sample produced it?
```

Answer:

```text
HG002
```

---

```text
Which package transported it?
```

Answer:

```text
tep_id
```

---

# Lineage Validation

Starting from:

```text
Validation Overlay
```

the user can reconstruct:

```text
Prioritization Overlay
        ↓

Interpretation Overlay
        ↓

Normalization Entity
        ↓

Observation Entity
```

without requiring the original VAP repository.

---

# Identity Validation

Starting from:

```text
canonical_variant_id
```

the user can recover:

```text
variant_id

run_id

sample_id

source_package_id

tep_id
```

without ambiguity.

---

# Reinterpretation Validation

A future system discovers a new biological mechanism.

The system identifies:

```text
VAR_001
```

as potentially relevant.

The system can reconstruct:

```text
What VAP observed

What VAP knew

What VAP did not know

Why VAP prioritized it

Why VAP did not prioritize it

Which uncertainty existed
```

because the evidence lifecycle was preserved.

---

# Architecture Validation Questions

The architecture should answer:

```text
Can source identity be recovered?
```

```text
YES
```

---

```text
Can lineage be reconstructed?
```

```text
YES
```

---

```text
Can provenance be reconstructed?
```

```text
YES
```

---

```text
Can interpretation history be reconstructed?
```

```text
YES
```

---

```text
Can future reinterpretation occur?
```

```text
YES
```

---

# Success Condition

The architecture is considered successful if a future user can begin with:

```text
Variant

Gene

Phenotype

Sample

Interpretation

Validation State
```

and deterministically reconstruct:

```text
Observation

Identity

Lineage

Provenance

Interpretation History

Validation History
```

without requiring access to the original VAP execution environment.

---

# Final Principle

```text
VAP creates evidence.

TEP preserves evidence.

VDB brokers evidence.

Future systems reinterpret evidence.
```
