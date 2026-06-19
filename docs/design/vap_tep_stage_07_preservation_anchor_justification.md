# VAP-TEP Stage 07 Preservation Anchor Justification

## Purpose

This document provides the scientific justification for selecting Stage 07 as the preservation anchor for VAP-TEP construction.

The purpose of this document is not to define implementation architecture.

The purpose is not to define payload structures.

The purpose is to establish the earliest scientifically defensible preservation boundary within the Variant Annotation Pipeline (VAP).

This document should be interpreted as a preservation-boundary justification.

---

# The Core Question

The VAP-TEP implementation effort requires identification of the earliest preservation-critical boundary within VAP.

The central question is:

```text
What is the earliest stage-derived substrate
that satisfies VAP preservation doctrine?
```

This question influences:

* VAP-TEP construction
* source artifact manifest design
* provenance preservation
* future reinterpretability
* VDB persistence strategy
* future RDGP reasoning

Accordingly, the preservation boundary must be selected from a scientific perspective rather than an implementation perspective.

---

# Candidate Preservation Boundaries

Several candidate boundaries exist.

## Candidate A

```text
Stage 11
+
Stage 12
```

Candidate-oriented preservation.

---

## Candidate B

```text
Stage 08
+
Stage 11
+
Stage 12
```

Interoperability-oriented preservation.

---

## Candidate C

```text
Stage 07
+
Stage 08
+
Stage 09
+
Stage 10
+
Stage 11
+
Stage 12
```

Observation-first preservation.

---

# Preservation Doctrine Requirements

The VAP Preservation Mission establishes the following principles:

```text
Preserve observations.

Preserve context.

Preserve uncertainty.

Preserve topology.

Preserve future reinterpretability.
```

The VAP-TEP Preservation Brief further establishes:

```text
Candidate status
is an interpretation state,
not an observation boundary.
```

Therefore, any preservation boundary must preserve observed biological substrate before prioritization and validation occur.

---

# Why Stage 11 Is Insufficient

Stage 11 represents prioritization outcomes.

Stage 11 answers:

```text
What did VAP consider important?
```

It does not fully answer:

```text
What did VAP observe?
```

Stage 11 already reflects interpretation and selection.

Consequently:

```text
Stage 11
≠
Observation Boundary
```

Using Stage 11 as the preservation anchor would introduce candidate-collapse risk.

Future systems would lose access to large portions of observed biological substrate.

---

# Why Stage 12 Is Insufficient

Stage 12 represents validation-ready evidence.

Stage 12 is valuable.

However, Stage 12 is the most selective interpretation surface within the workflow.

Using Stage 12 as the preservation anchor would effectively reduce VAP-TEP to a candidate export mechanism.

Such an approach would violate:

* preservation doctrine
* future reinterpretability goals
* noncoding preservation goals
* negative evidence preservation goals

Stage 12 therefore cannot serve as the preservation anchor.

---

# Why Stage 08 Is Attractive

Stage 08 represents the first major interoperability-oriented substrate within VAP.

Stage 08 provides:

```text
Coding Partition

Noncoding Partition

Gene Evidence Surfaces

Population Context

Frequency Context

Impact Context
```

Stage 08 also serves as the natural bridge toward:

```text
VDB
```

and

```text
RDGP
```

integration.

From an implementation perspective, Stage 08 is extremely attractive.

---

# Why Stage 08 Is Not the Earliest Preservation Boundary

Despite its strengths, Stage 08 already represents a semantic organization layer.

Stage 08 answers:

```text
How did VAP organize observations?
```

rather than:

```text
What observations existed?
```

Stage 08 partitions and organizes evidence after annotation has already occurred.

Therefore:

```text
Stage 08
=
Interoperability Boundary
```

but not necessarily:

```text
Stage 08
=
Earliest Observation Boundary
```

A preservation strategy anchored solely on Stage 08 assumes that Stage 08 remains non-destructive relative to Stage 07.

That assumption may be valid.

However, it must be demonstrated rather than assumed.

---

# Why Stage 07 Is the Earliest Preservation-Critical Boundary

Stage 07 represents the point at which observed variant substrate becomes biologically contextualized.

At Stage 07, VAP has already established:

```text
Variant Identity

Genotype Context

Transcript Context

Gene Context

Consequence Context

Impact Context

Population Context

Clinical Context
```

while remaining upstream of:

```text
Partitioning

Prioritization

Validation Selection
```

Stage 07 therefore represents the earliest stage where observations become scientifically interpretable.

Most importantly:

```text
Stage 07 preserves observations
before semantic reduction occurs.
```

This makes Stage 07 the earliest preservation-critical boundary within the interpretation workflow.

---

# Observation Boundary Versus Interoperability Boundary

An important distinction emerges from this analysis.

## Observation Boundary

```text
Stage 07
```

Answers:

```text
What was observed?
```

---

## Interoperability Boundary

```text
Stage 08
```

Answers:

```text
How was the observation organized?
```

---

These boundaries serve different purposes.

They should not be treated as equivalent.

---

# Preferred Conceptual Model

The most scientifically coherent model is:

```text
Observation Entity
        ↓
Interpretation Entities
```

Within VAP this maps naturally to:

```text
Stage 07
    Observation Entity
```

```text
Stage 08
    Organization Entity
```

```text
Stage 09
    Coding Interpretation Entity
```

```text
Stage 10
    Noncoding Interpretation Entity
```

```text
Stage 11
    Prioritization Entity
```

```text
Stage 12
    Validation Entity
```

This model aligns with:

* VAP Preservation Mission
* VAP-TEP Preservation Brief
* VAP-TEP Payload Model
* VAP-TEP Risk Assessment
* Truth Layer transport doctrine

---

# Minimum Scientifically Defensible VAP-TEP

The smallest preservation-compliant VAP-TEP should preserve:

```text
Stage 07 Observation Context
```

together with sufficient downstream context to preserve:

```text
Stage 08 Organization Context

Stage 09 Interpretation Context

Stage 10 Interpretation Context

Stage 11 Prioritization Context

Stage 12 Validation Context
```

The goal is not maximal preservation.

The goal is preservation sufficient to support future reinterpretation.

---

# Implications for VDB

This analysis does not imply that VDB must persist Stage 07 artifacts directly.

Rather, it establishes that:

```text
Stage 07
=
scientific preservation anchor
```

and

```text
Stage 08
=
natural interoperability substrate
```

A valid VAP-TEP may ultimately choose to expose Stage 08-oriented semantic surfaces.

However, preservation doctrine should remain anchored to Stage 07.

---

# Final Determination

The preferred preservation anchor for VAP-TEP is:

```text
Stage 07
```

because it is the earliest stage at which observed biological substrate becomes scientifically interpretable while remaining upstream of semantic partitioning, prioritization, and validation selection.

Stage 08 remains the strongest interoperability boundary within the pipeline.

However:

```text
Observation Boundary
≠
Interoperability Boundary
```

The distinction between those concepts is critical.

A preservation-compliant VAP-TEP should therefore treat Stage 07 as the scientific preservation anchor while leveraging later stages as contextual interpretation layers.

This approach best satisfies VAP preservation doctrine, Truth Layer governance, future VDB persistence goals, and future RDGP reinterpretation requirements.


## Appendix A: Empirical Forensics Supporting Stage 07 Preservation Anchoring

### Purpose

The Stage 07 preservation-anchor recommendation was originally derived from preservation doctrine, payload modeling, and scientific reinterpretability requirements.

Subsequent forensic analysis of completed VAP production runs was performed to evaluate whether the implementation behavior of Stage 07 and Stage 08 supports this architectural conclusion.

The goal was not to replace preservation doctrine with implementation details. Rather, the goal was to determine whether real-world VAP execution behavior is consistent with the preservation model.

---

### Forensic Dataset

Analysis was performed across thirteen completed VAP runs:

* twelve epilepsy WES runs
* one HG002 WGS benchmark run

The audit therefore spans:

* heterogeneous biological samples
* heterogeneous sequencing depths
* both WES and WGS execution modes
* production-validated VAP outputs

---

### Finding 01: Stage 08 Is Row-Preserving Relative to Stage 07

For all audited runs:

```text
Stage07 row count
=
Stage08 row count
```

No evidence of large-scale variant elimination was observed at the Stage 07 → Stage 08 boundary.

This finding is important because it demonstrates that Stage 08 is not functioning as a candidate-selection layer.

Instead, Stage 08 behaves as a semantic organization and interoperability layer operating on the complete Stage 07 variant substrate.

Implication:

```text
Stage08
=
projection of Stage07

not

subset of Stage07
```

---

### Finding 02: Stage 08 Preserves the Observation Substrate

Stage 07 contains the canonical annotated variant records produced by VAP.

Forensic inspection demonstrated that Stage 08 consumes the complete Stage 07 substrate and preserves the underlying variant population while adding interoperability-oriented metadata.

Observed Stage 08 enrichments include:

* annotation source tracking
* annotation version tracking
* gene mapping status
* variant context classification
* variant effect severity
* quality-control status
* interpretability status
* frequency status
* clinical status

These additions increase downstream utility without materially reducing the observed variant substrate.

---

### Finding 03: Stage 08 Represents Semantic Enrichment Rather Than Semantic Reduction

Stage 07 contains the earliest scientifically interpretable variant representation produced by VAP.

Stage 08 introduces normalization and organizational context while preserving row cardinality.

Examples observed during forensic review include normalization of:

* variant classification terminology
* effect severity terminology
* interoperability-facing metadata

This behavior is consistent with Stage 08 functioning as an interoperability substrate rather than a preservation boundary.

---

### Finding 04: Stage 08 Contains Distinct Semantic Roles

Forensic analysis identified two Stage 08 artifacts:

```text
stage_08_selected_transcript_consequences.tsv

stage_08_vdb_ready_variants.tsv
```

Across all audited runs these artifacts were observed to be:

* byte-identical
* row-identical
* checksum-identical

However, architectural review determined that these artifacts represent distinct semantic roles.

Current VAP v1 behavior utilizes a selected-transcript representation, resulting in identical payloads.

Future VAP releases may diverge these artifacts as transcript modeling evolves.

Therefore:

```text
physical equivalence
≠
semantic equivalence
```

VAP-TEP construction should preserve both artifact identities within source-artifact manifests even when checksums are identical.

---

### Preservation Interpretation

The forensic evidence supports the following architectural model:

```text
Stage07
    Scientific Observation Anchor

Stage08
    Row-Preserving Interoperability Projection

Stage09
    Coding Interpretation Overlay

Stage10
    Noncoding Interpretation Overlay

Stage11
    Prioritization Overlay

Stage12
    Validation Overlay

Stage13
    Summary / Audit Context
```

Under this model:

* Stage 07 remains the earliest preservation-critical boundary.
* Stage 08 functions as the primary interoperability substrate.
* Later stages provide interpretation context rather than replacing the observation layer.

---

### Conclusion

Production forensics performed across thirteen completed VAP runs support the preservation-oriented conclusion that Stage 07 represents the scientifically authoritative preservation anchor for VAP-TEP construction.

The evidence further demonstrates that Stage 08 behaves as a row-preserving, observation-preserving interoperability projection of Stage 07 rather than a candidate-selection boundary.

This distinction provides empirical support for the VAP-TEP architecture:

```text
Stage07
    Preservation Anchor

Stage08
    Transport Substrate

Stage09–12
    Interpretation Overlays

Stage13
    Summary Context
```
