# VAP-TEP Example Walkthrough

## Purpose

This document provides conceptual examples illustrating how biological observations move through the Variant Annotation Pipeline (VAP) and how those observations should be preserved within a Variant Annotation Pipeline Transitional Evidence Product (VAP-TEP).

This document is not a schema.

This document is not an implementation specification.

This document is not a transport design.

Instead, this document demonstrates how the preservation principles defined in the VAP Preservation Mission, VAP-TEP Preservation Brief, VAP-TEP Payload Model, and VAP-TEP Risk Assessment apply to representative observations.

The purpose of these examples is to illustrate:

```text
What was observed?

What did VAP know?

What did VAP not know?

What context accumulated?

What should survive transport?

How might future science reinterpret the observation?
```

---

# Scope

The examples presented here are conceptual.

The observations are representative examples designed to exercise preservation requirements.

The examples intentionally include observations with differing levels of current interpretability.

The objective is to demonstrate preservation behavior rather than clinical significance.

---

# Walkthrough Philosophy

The purpose of VAP-TEP is not to preserve only highly ranked candidates.

The purpose is to preserve observed biological substrate together with the contextual evidence necessary for future reinterpretation.

Accordingly, this walkthrough includes:

```text
Coding Candidate

Noncoding Observation

Common Variant

Unannotated Observation
```

These examples represent distinct preservation challenges.

Together they illustrate why preservation eligibility should not be determined solely by present-day interpretive value.

---

# Walkthrough A: Coding Candidate

## Scenario

A coding variant is observed in a biologically relevant gene.

The variant receives strong annotation support, clinical support, and reviewability support.

The observation ultimately becomes validation-ready.

---

## VAP Progression

```text
Observed Variant
        ↓
Stage 07 Annotation
        ↓
Stage 08 Coding Partition
        ↓
Stage 09 Coding Interpretation
        ↓
Stage 11 Prioritization
        ↓
Stage 12 Validation Ready
        ↓
VAP-TEP
```

---

## What Was Observed?

```text
Variant

Genotype

Sample Association

Coverage Context

Quality Context
```

---

## What Did VAP Know?

```text
Coding Consequence

Gene Association

Clinical Support

Population Context

Reviewability Context
```

---

## What Did VAP Not Know?

```text
Future Clinical Interpretations

Future Disease Models

Future Mechanistic Understanding
```

---

## What Must Survive Transport?

```text
Observation Entity

Variant Entity

Genotype Entity

Annotation Entity

Clinical Context Entity

Coding Interpretation Entity

Prioritization Entity

Validation Entity

Provenance Entity

Uncertainty Entity
```

---

## Future Reinterpretation Potential

Future systems may:

* update clinical significance
* revise consequence interpretation
* alter prioritization frameworks
* incorporate additional evidence sources

Preserving only the final candidate label would be insufficient.

The underlying observation and contextual evidence must remain available.

---

# Walkthrough B: Noncoding Observation

## Scenario

A noncoding variant is observed.

The variant receives limited regulatory support and does not become validation-ready.

Current interpretation confidence is low.

The observation is not escalated.

---

## VAP Progression

```text
Observed Variant
        ↓
Stage 07 Annotation
        ↓
Stage 08 Noncoding Partition
        ↓
Stage 10 Noncoding Interpretation
        ↓
Not Prioritized
        ↓
Not Validation Ready
        ↓
VAP-TEP
```

---

## What Was Observed?

```text
Variant

Genotype

Sample Association

Regulatory-Proximal Observation
```

---

## What Did VAP Know?

```text
Noncoding Status

Available Regulatory Context

Available Population Context

Available Annotation Context
```

---

## What Did VAP Not Know?

```text
Whether the Variant Is Functional

Whether a Relevant Regulatory Mechanism Exists

Whether Future Evidence Will Emerge
```

---

## What Must Survive Transport?

```text
Observation Entity

Variant Entity

Genotype Entity

Annotation Entity

Noncoding Interpretation Entity

Provenance Entity

Uncertainty Entity
```

Importantly:

```text
Not Prioritized
```

must also survive.

The absence of prioritization is itself contextual information.

---

## Future Reinterpretation Potential

Future systems may discover:

* novel enhancer functions
* novel promoter relationships
* chromatin interactions
* disease-associated regulatory mechanisms

A discarded observation cannot benefit from future discoveries.

A preserved observation can.

---

## Preservation Lesson

```text
Not Prioritized
≠
Not Preservation-Worthy
```

---

# Walkthrough C: Common Variant

## Scenario

A variant is observed with relatively common population frequency.

Current interpretation frameworks do not consider the observation particularly important.

The variant is not escalated.

---

## VAP Progression

```text
Observed Variant
        ↓
Stage 07 Annotation
        ↓
Stage 08 Population Context
        ↓
Common Frequency Classification
        ↓
Not Prioritized
        ↓
VAP-TEP
```

---

## What Was Observed?

```text
Variant

Genotype

Population Frequency Context
```

---

## What Did VAP Know?

```text
Common Population Frequency

Available Annotation Context

Available Clinical Context
```

---

## What Did VAP Not Know?

```text
Modifier Effects

Polygenic Contributions

Protective Effects

Future Burden Relationships
```

---

## What Must Survive Transport?

```text
Observation Entity

Variant Entity

Genotype Entity

Population Context Entity

Annotation Entity

Provenance Entity

Uncertainty Entity
```

---

## Future Reinterpretation Potential

Future systems may determine that the variant contributes to:

* disease susceptibility
* disease resilience
* modifier effects
* polygenic burden
* oligogenic interactions

Current frequency alone cannot determine future scientific importance.

---

## Preservation Lesson

```text
Common
≠
Disposable
```

---

# Walkthrough D: Unannotated Observation

## Scenario

A variant is observed.

Current annotation systems provide little or no useful interpretation.

No clinical support exists.

No meaningful review pathway exists.

The observation remains largely unexplained.

---

## VAP Progression

```text
Observed Variant
        ↓
Stage 07 Annotation Attempt
        ↓
Minimal Annotation
        ↓
No Clinical Support
        ↓
No Prioritization
        ↓
VAP-TEP
```

---

## What Was Observed?

```text
Variant

Genotype

Sample Association
```

---

## What Did VAP Know?

```text
Observation Exists

Current Interpretation Is Limited
```

---

## What Did VAP Not Know?

```text
Biological Function

Clinical Significance

Future Disease Associations

Future Regulatory Context
```

---

## What Must Survive Transport?

```text
Observation Entity

Variant Entity

Genotype Entity

Provenance Entity

Uncertainty Entity
```

Annotation absence should also remain reconstructable.

---

## Future Reinterpretation Potential

Future systems may gain access to:

* improved annotation resources
* new disease associations
* new functional evidence
* new biological models

The observation may eventually become highly informative.

---

## Preservation Lesson

```text
Absence of Annotation
≠
Absence of Relevance
```

---

# Comparative Analysis

The four observations differ substantially in current interpretive value.

```text
Coding Candidate
    High Current Support

Noncoding Observation
    Limited Current Support

Common Variant
    Low Current Priority

Unannotated Observation
    Minimal Current Interpretation
```

Despite these differences:

```text
All Four Observations
Remain Preservation-Eligible
```

This outcome follows directly from the preservation mission.

Preservation eligibility is determined by future reinterpretability requirements rather than current interpretive confidence.

---

# Why VAP-TEP Preserves More Than Candidates

A candidate-only preservation strategy would preserve Walkthrough A while potentially discarding Walkthroughs B, C, and D.

Such a strategy would introduce substantial scientific risk.

Future discovery frequently emerges from observations that initially appear weakly informative.

VAP-TEP therefore preserves observations together with contextual evidence rather than preserving only reviewer-selected findings.

The objective is not merely to remember what VAP considered important.

The objective is to preserve enough evidence so that future systems can determine what is important.

---

# Preservation Validation Questions

For every preserved observation, future systems should be able to answer:

```text
What was observed?
```

```text
What context accompanied the observation?
```

```text
What did VAP know at the time?
```

```text
What did VAP not know at the time?
```

```text
Why was the observation prioritized?
```

```text
Why was the observation not prioritized?
```

```text
How might future science reinterpret it?
```

A VAP-TEP should not be considered scientifically complete unless these questions remain answerable.

---

# Assumptions

* Future scientific understanding will differ from current understanding.
* VAP remains authoritative for observed biological evidence.
* VDB remains authoritative for persistence and brokerage.
* Preservation and interpretation remain separate responsibilities.

---

# Limitations

* The examples presented here are conceptual.
* The examples are not intended as clinical guidance.
* The examples do not define implementation requirements.
* Future reinterpretation pathways cannot be predicted with certainty.

---

# Edge Cases

The walkthroughs intentionally highlight evidence classes that are frequently vulnerable to preservation failure:

```text
Noncoding Observations

Common Variants

Unannotated Variants

Non-Prioritized Evidence

Uncertain Evidence
```

These classes should receive particular preservation attention.

---

# Conclusion

The purpose of VAP-TEP is not merely to transport candidate variants.

The purpose of VAP-TEP is to preserve observed biological substrate together with the contextual evidence necessary for future reinterpretation.

A coding candidate, a noncoding observation, a common variant, and an unannotated observation may differ dramatically in present-day utility.

All remain scientifically valuable preservation targets because future systems may derive meaning that is not currently visible.

The same preservation principles apply to healthy-control observations. Control evidence may provide future calibration, background, reproducibility, and burden-modeling value despite lacking disease significance.

The central preservation objective is therefore not to preserve today's conclusions.

The objective is to preserve tomorrow's opportunity to reach better conclusions.

