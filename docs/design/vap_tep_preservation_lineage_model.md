# VAP-TEP Preservation Lineage Model

## Purpose

This document formalizes the empirically observed evidence-lineage architecture of the Variant Annotation Pipeline (VAP) and establishes the preservation model that underpins VAP-TEP construction.

The goal of this document is not to define the final VAP-TEP payload contract. Rather, its purpose is to describe how evidence evolves through the VAP execution lifecycle and to identify the major preservation layers that contribute to downstream interpretation.

The lineage model described here is derived from:

* Stage-specific pipeline implementation review
* Empirical forensic analysis across 13 production VAP runs

  * 12 epilepsy WES runs
  * 1 HG002 WGS benchmark run
* Column lineage analysis
* Stage07 preservation-boundary analysis

This document serves as the architectural bridge between preservation doctrine and eventual VAP-TEP contract implementation.

---

# 1. Preservation Philosophy

VAP is not a candidate-generation system.

VAP is an evidence-preservation system that progressively enriches biological observations through deterministic annotation, interpretation, prioritization, and validation preparation.

Accordingly, preservation must not focus solely on final candidate states.

Preservation must maintain lineage between:

```text
Observation
    ↓
Normalization
    ↓
Interpretation
    ↓
Prioritization
    ↓
Validation Preparation
```

Each layer contributes information that may be biologically relevant to future downstream consumers.

---

# 2. Evidence Lifecycle Overview

The empirically observed lineage model is:

```text
Stage07
    Observation Entity
        ↓

Stage08
    Normalization Entity
        ↓

Stage09
    Coding Interpretation Overlay
        ↓

Stage10
    Noncoding Interpretation Overlay
        ↓

Stage11
    Prioritization Overlay
        ↓

Stage12
    Validation Overlay
```

Stage13 exists outside the evidence-preservation stream and provides execution metadata, run summaries, and audit context.

Stage13 is therefore considered a contextual sidecar rather than an evidence substrate.

---

# 3. Observation Layer (Stage07)

## Role

Stage07 represents the first biologically interpretable observation boundary.

At this stage:

* Variant calling has completed
* Annotation has been performed
* Variant identity is established
* Gene and transcript relationships are established

Stage07 therefore represents the earliest preservation-compliant scientific observation surface.

## Preservation Role

```text
Observation Entity
```

## Characteristics

Stage07 preserves:

* Variant identity
* Sample identity
* Genotype context
* Gene mappings
* Transcript mappings
* Consequence annotations
* Clinical annotations
* Population-frequency annotations

Stage07 does not yet perform:

* Prioritization
* Candidate ranking
* Validation preparation

Accordingly, Stage07 serves as the preservation anchor for VAP-TEP construction.

---

# 4. Normalization Layer (Stage08)

## Role

Stage08 is the first semantic normalization boundary.

Forensic analysis demonstrates that Stage08 is not merely a partitioning stage.

Instead, Stage08 transforms Stage07 observations into a normalized interoperability substrate.

## Preservation Role

```text
Normalization Entity
```

## Key Additions

Stage08 introduces normalized semantic context including:

* variant_context
* variant_effect_severity
* qc_status
* interpretability_status
* frequency_status
* clinical_status
* annotation_source
* annotation_version
* gene_mapping_status

Stage08 additionally creates routing substrates used by downstream systems:

* coding_candidates.tsv
* splice_region_candidates.tsv
* noncoding_candidates.tsv
* stage_08_vdb_ready_variants.tsv
* stage_08_rdgp_gene_evidence_seed.tsv

## Interpretation Boundary

Stage08 performs no interpretation.

Stage08 performs no prioritization.

Stage08 performs no validation preparation.

Its role is semantic normalization and interoperability preparation.

---

# 5. Coding Interpretation Layer (Stage09)

## Role

Stage09 performs coding-specific interpretation.

It consumes:

```text
coding_candidates.tsv
splice_region_candidates.tsv
```

and appends coding interpretation context.

## Preservation Role

```text
Coding Interpretation Overlay
```

## Key Additions

Examples include:

* functional_impact
* coding_interpretation_label
* rarity_flag
* clinical_evidence
* qc_reliability

Stage09 does not alter the underlying observation entity.

Instead, it overlays coding-specific reasoning.

---

# 6. Noncoding Interpretation Layer (Stage10)

## Role

Stage10 performs noncoding-specific interpretation.

It consumes:

```text
noncoding_candidates.tsv
```

and appends noncoding interpretation context.

## Preservation Role

```text
Noncoding Interpretation Overlay
```

## Key Additions

Examples include:

* noncoding_functional_context
* noncoding_interpretation_label
* rarity_flag
* clinical_evidence
* qc_reliability

Stage10 similarly preserves the underlying observation entity while contributing noncoding reasoning context.

---

# 7. Prioritization Layer (Stage11)

## Role

Stage11 recombines interpreted coding and noncoding evidence into a unified prioritization substrate.

Forensic analysis demonstrates that Stage11 is not a subset-generation stage.

Instead, Stage11 performs deterministic prioritization over the interpreted evidence universe.

## Preservation Role

```text
Prioritization Overlay
```

## Key Additions

Examples include:

* priority_tier
* priority_rank
* priority_reason
* source_interpretation_label
* variant_origin

Stage11 therefore represents prioritization context rather than new biological observation.

---

# 8. Validation Layer (Stage12)

## Role

Stage12 prepares variants for downstream review and validation workflows.

Forensic analysis demonstrates that Stage12 is:

* Row preserving
* Variant preserving
* Additive

Stage12 performs no filtering and no reinterpretation.

## Preservation Role

```text
Validation Overlay
```

## Key Additions

Examples include:

* validation_required
* validation_priority
* suggested_validation_method
* validation_reason

Stage12 therefore represents operational validation context rather than biological interpretation.

---

# 9. Preservation Hierarchy

The observed preservation hierarchy is:

```text
Observation Entity
    Stage07

Normalization Entity
    Stage08

Interpretation Overlays
    Stage09
    Stage10

Prioritization Overlay
    Stage11

Validation Overlay
    Stage12
```

This hierarchy reflects the scientific role of each stage rather than implementation details.

---

# 10. Implications for VAP-TEP

The lineage model implies that a preservation-compliant VAP-TEP cannot be constructed solely from candidate-oriented outputs.

Observation context must remain traceable.

Normalization context must remain traceable.

Interpretation context must remain traceable.

Prioritization and validation context must remain traceable.

Accordingly, future VAP-TEP contract design should preserve lineage across all evidence layers while maintaining explicit provenance between them.

The exact payload structure is defined separately by the VAP-TEP contract specification.

This document establishes the preservation model that justifies that future contract.
