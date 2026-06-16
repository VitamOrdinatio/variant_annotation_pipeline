# VAP Preservation Mission

## Purpose

This document defines the scientific preservation mission for the Variant Annotation Pipeline (VAP).

Its purpose is to guide future VAP-TEP construction by identifying the evidence, provenance, topology, context, and scientific meaning that must survive transport into downstream systems such as VDB.

This document is intended primarily for SAGE-VAP.

---

## Repository

```text
Repository Name:
    Variant Annotation Pipeline (VAP)

Repository Version:
    v1.x

Preservation Authority:
    SAGE-VAP

Associated TEP:
    VAP-TEP
```

---

## Mission Statement

VAP exists to transform raw sequencing data into interpretable variant evidence while preserving sufficient context to enable future biological, clinical, and computational reinterpretation.

The preservation mission of VAP is:

```text
Preserve observed evidence.

Preserve provenance.

Preserve topology.

Preserve scientific meaning.

Preserve future interpretability.
```

---

## Repository Stewardship Role

### Primary Evidence Class

```text
Observed Variant Evidence
```

VAP is the ecosystem authority for transforming sequencing observations into annotated variant evidence while preserving biological substrate.

---

### Repository Responsibility

```text
Observation

Annotation

Evidence Refinement

Evidence Packaging

Interpretation Support
```

VAP is not primarily a reasoning repository.

VAP generates evidence that downstream repositories may later aggregate, prioritize, interpret, or reason over.

---

## Preservation Principle 1: Evidence Is Primary

VAP is authoritative for observed variant evidence.

Observed evidence should remain preservable even when:

* no ClinVar annotation exists
* no VEP annotation exists
* no disease association exists
* no current interpretation exists
* no current review pathway exists

The absence of prior knowledge does not reduce the value of observed evidence.

---

### Evidence Classes Requiring Preservation

```text
Variant Calls

Annotated Variant Records

Clinical Annotation Fields

Functional Annotation Fields

Population Frequency Fields

Reviewability Signals

Candidate Evidence

Stage-Level Evidence Products

Cross-Run Evidence Products
```

---

### Questions

```text
What evidence would be impossible to reconstruct later?

What evidence is uniquely produced by VAP?

What evidence remains valuable even if current interpretation changes?
```

---

## Preservation Principle 2: Scientific Meaning Must Survive

VAP should avoid preservation strategies that retain only currently interesting variants.

Future discoveries may alter interpretation.

Evidence preservation should prioritize retention of biological substrate rather than reviewer-selected findings.

---

### Scientific Context Requiring Preservation

```text
Observed Variant Context

Annotation Context

Clinical Context

Functional Context

Reviewability Context

Candidate Escalation Context

Pipeline Processing Context
```

---

### Questions

```text
What biological meaning must remain visible?

What scientific assumptions should remain traceable?

What future reinterpretations should remain possible?
```

---

## Preservation Principle 3: Provenance Must Remain Reconstructable

Future consumers should be able to determine:

* where evidence originated
* how evidence was generated
* what software produced the evidence
* what reference resources were used
* what execution context existed
* what run produced the evidence

Transport should never sever provenance from evidence.

---

### Provenance Requirements

```text
Sample Identity

Run Identity

Pipeline Version

Configuration Snapshot

Reference Resources

Annotation Resources

Execution Metadata

Stage-Level Provenance

Artifact Lineage
```

---

### Questions

```text
Where did the evidence originate?

How was the evidence generated?

What resources were used?

What software produced the evidence?

What execution context existed?
```

---

## Preservation Principle 4: Topology Must Remain Visible

VAP is a staged pipeline.

Important stage-level transitions should remain reconstructable.

Future consumers should be able to understand how evidence progressed through the pipeline lifecycle.

---

### Topology Requiring Preservation

```text
Pipeline Stage Relationships

Evidence Escalation Relationships

Candidate Promotion Relationships

Artifact Lineage Relationships

Run-Level Relationships

Sample-Level Relationships
```

---

### Questions

```text
What relationships give the evidence meaning?

What structural context would be lost if flattened?

What topology is required for future interpretation?
```

---

## Preservation Principle 5: Observation and Interpretation Must Remain Distinct

Observed evidence and interpretation are not equivalent.

VAP may attach interpretation-supporting annotations, but these should remain distinguishable from the underlying observed evidence.

Future consumers should always be able to separate:

```text
Observation

Annotation

Interpretation
```

---

### Observed Elements

```text
Variant Calls

Genomic Coordinates

Genotypes

Coverage Metrics

Quality Metrics

Sample-Level Evidence
```

---

### Derived Elements

```text
VEP Annotations

ClinVar Annotations

Functional Predictions

Reviewability Labels

Candidate Prioritization Labels

Clinical Support Labels
```

---

### Questions

```text
What was directly observed?

What was inferred?

What was annotated?

What was derived?
```

---

## Preservation Principle 6: Future Reinterpretation Is a First-Class Requirement

Evidence should be preserved in a manner that supports:

* future clinical reinterpretation
* future semantic aggregation
* future statistical analysis
* future gene prioritization
* future reasoning systems
* future disease discovery

Preservation decisions should favor future utility over present convenience.

---

### Future Reuse Scenarios

```text
Clinical Reinterpretation

Gene Prior Aggregation

Gene Prioritization

Cross-Run Comparison

Cross-Study Comparison

Rare Disease Investigation

Statistical Reanalysis

Future Reasoning Systems
```

---

### Questions

```text
How might this evidence be used in ten years?

What future discoveries could alter interpretation?

What information would future systems regret losing?
```

---

## Repository-Specific Preservation Risks

### Risks

```text
Loss of Biological Substrate

Loss of Provenance

Loss of Pipeline Topology

Loss of Stage-Level Context

Loss of Candidate Escalation Context

Over-Filtering of Variants

Over-Normalization of Evidence

Conflation of Observation and Interpretation
```

---

## TEP Preservation Requirements

This section defines the minimum scientific expectations for VAP-TEP.

---

### Required Evidence Preservation

```text
Observed Variant Evidence

Annotated Variant Evidence

Candidate Evidence

Reviewability Evidence

Clinical Annotation Evidence

Cross-Run Evidence Products
```

---

### Required Provenance Preservation

```text
Sample Provenance

Run Provenance

Execution Provenance

Pipeline Provenance

Resource Provenance

Artifact Lineage
```

---

### Required Topology Preservation

```text
Pipeline Stage Relationships

Evidence Progression Relationships

Artifact Lineage Relationships

Candidate Escalation Relationships
```

---

### Required Context Preservation

```text
Biological Context

Annotation Context

Reviewability Context

Clinical Context

Execution Context
```

---

## Questions for VAP-TEP Design Review

The VAP-TEP should be evaluated against the following questions:

```text
Does observed evidence survive?

Does provenance survive?

Does topology survive?

Does scientific meaning survive?

Does uncertainty survive?

Does future reinterpretation remain possible?

Can VDB understand the transported evidence?

Can future repositories build upon the transported evidence?
```

A VAP-TEP implementation should not be considered complete unless these questions can be answered affirmatively.

---

## Deliverables

This preservation mission should directly support:

```text
SAGE-VAP
    Preservation Brief

DEX-VAP
    TEP Implementation Plan

DEX-VAP-Validate
    TEP Compliance Review

VDB
    Discovery

VDB
    Validation

VDB
    Namespace Brokerage

VDB
    Semantic Persistence
```

---

## Summary

VAP is the ecosystem authority for observed variant evidence.

Its preservation mission is to ensure that observed biological substrate, provenance, topology, annotation context, and future interpretability survive transport into downstream systems.

The purpose of VAP-TEP is not merely to move files.

The purpose of VAP-TEP is to preserve observed biological evidence in a form that remains scientifically meaningful, provenance-rich, topology-aware, and reusable by future repositories and future investigators.
