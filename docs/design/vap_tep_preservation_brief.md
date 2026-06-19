# VAP-TEP Preservation Brief

## Purpose

This document defines the scientific preservation requirements for the Variant Annotation Pipeline Transitional Evidence Product (VAP-TEP).

The purpose of VAP-TEP is not to preserve only the final outputs of VAP.

The purpose of VAP-TEP is to preserve sufficient biological observations and contextual evidence so that future systems can accurately reconstruct:

* what VAP observed
* what VAP inferred
* what VAP prioritized
* what VAP did not prioritize
* what VAP knew at the time of execution
* what VAP did not know at the time of execution

without requiring access to the original VAP execution environment.

This document serves as the scientific preservation authority for future VAP-TEP implementation.

---

# Scope

This document addresses:

* observation preservation
* evidence continuity
* future reinterpretability
* scientific reproducibility
* uncertainty preservation
* discovery enablement

This document does not define:

* implementation architecture
* schemas
* databases
* transport mechanisms
* storage formats

Those responsibilities belong to implementation authorities.

---

# Preservation Thesis

VAP is an observation refinery.

Its scientific value is not limited to the variants ultimately selected for validation or review.

VAP progressively transforms observed biological substrate through annotation, partitioning, interpretation, prioritization, validation readiness assessment, and reporting.

Therefore:

> Candidate status is an interpretation state, not an observation boundary.

The preservation objective of VAP-TEP is to ensure that future systems can reconstruct both the observed biological substrate and the interpretive context accumulated throughout the VAP workflow.

---

# Scientific Premises

## Premise 1: Scientific knowledge is incomplete

Current biological understanding is necessarily incomplete.

Many disease mechanisms remain undiscovered.

Many regulatory systems remain poorly characterized.

Many variant classes remain difficult to interpret.

Preservation decisions must therefore account for future scientific advancement.

---

## Premise 2: Current importance is not equivalent to preservation importance

Evidence that appears low-value today may become highly informative tomorrow.

Historically, multiple classes of biological evidence transitioned from low-interest observations to clinically significant evidence classes as scientific understanding matured.

Preservation eligibility must therefore be evaluated independently from current clinical utility.

---

## Premise 3: Lost observations cannot be reinterpreted

Future systems can reinterpret preserved observations.

Future systems cannot reinterpret observations that were discarded.

When preservation decisions are uncertain, preserving evidence generally carries lower scientific risk than removing evidence.

---

# VAP as an Observation Refinery

VAP does not create biological observations.

VAP receives observed variant substrate and progressively enriches it with contextual information.

The VAP workflow can therefore be viewed as a refinement process:

```text
Observed Variant Substrate
        ↓
Annotation
        ↓
Partitioning
        ↓
Coding Interpretation
        ↓
Noncoding Interpretation
        ↓
Prioritization
        ↓
Validation Readiness
        ↓
Reporting
```

Each stage contributes scientific context.

No downstream stage fully replaces upstream information.

Accordingly, preservation must include both observations and accumulated context.

---

# Preservation Boundary by Stage

## Stage 07 — Annotation

Stage 07 establishes biological context around observed variants.

Preservation-critical information includes:

* variant identity
* genomic coordinates
* reference allele
* alternate allele
* genotype state
* transcript associations
* consequence assignments
* gene associations
* annotation source context
* annotation version context
* unmapped states
* ambiguous states

Stage 07 represents the earliest preservation-critical boundary within the interpretation workflow.

---

## Stage 08 — Partitioning and Weak Filtering

Stage 08 organizes observed substrate into biologically meaningful evidence classes.

Preservation-critical information includes:

* coding designation
* noncoding designation
* gene-level summaries
* population frequency context
* impact distributions
* partition membership
* weak-filter outcomes

Stage 08 remains preservation-critical because it captures how observations were categorized before downstream interpretation.

---

## Stage 09 — Coding Interpretation

Preservation-critical information includes:

* coding evidence assessments
* coding consequence interpretation
* impact classifications
* clinical support surfaces
* coding uncertainty

---

## Stage 10 — Noncoding Interpretation

Preservation-critical information includes:

* regulatory evidence
* noncoding classifications
* regulatory annotations
* proximity relationships
* noncoding uncertainty
* weakly supported noncoding evidence

Particular care should be taken to preserve noncoding evidence due to ongoing limitations in biological understanding.

---

## Stage 11 — Prioritization

Preservation-critical information includes:

* prioritization outcomes
* prioritization rationale
* prioritization category assignments
* escalation decisions
* deprioritization decisions

Future systems must be able to determine not only why evidence was selected but also why evidence was not selected.

---

## Stage 12 — Validation-Ready Candidates

Preservation-critical information includes:

* validation eligibility
* validation rationale
* candidate reviewability context
* supporting evidence structures

Stage 12 represents an important interpretation state but not the entirety of VAP knowledge.

---

## Stage 13 — Summary Outputs

Preservation-critical information includes:

* aggregate evidence summaries
* run-level summaries
* execution-level reporting context

Stage 13 provides auditability and historical reconstruction context.

---

# Evidence Classes That Must Survive

The following evidence classes should be considered preservation-eligible.

## Negative Evidence

Negative evidence preserves historical non-selection decisions and supports future reevaluation.

---

## Known Variants

Known variants preserve historical interpretation continuity.

---

## Rare Variants

Rare variants remain important for current and future disease discovery.

---

## Common Variants

Common variants should not be excluded solely because of population prevalence.

Future polygenic, oligogenic, modifier, burden, or regulatory models may require them.

---

## Coding Variants

Coding variants remain important due to established disease relevance.

---

## Noncoding Variants

Noncoding variants require particularly strong preservation protection.

Future interpretation systems may derive substantial meaning from currently unexplained regulatory evidence.

---

## Annotated Variants

Annotated variants preserve contemporary biological interpretation state.

---

## Unannotated Variants

Unannotated variants preserve future discovery opportunity.

Absence of interpretation is not evidence of absence.

---

## Currently Unexplained Variants

Variants lacking current explanatory models should remain preservation-eligible.

Future systems may identify relationships unavailable to current science.

---

# Context That Must Accompany Observations

Observations alone are insufficient.

> Future systems must be able to reconstruct stage lineage and evidence progression history.

The following contextual layers are preservation-critical.

## Variant Identity Context

Future systems must be able to determine precisely what was observed.

---

## Genotype Context

Future systems must understand the observed state of the variant within the sample.

---

## Annotation Context

Future systems must understand how VAP interpreted the observation at the time of execution.

---

## Population Context

Future systems must understand frequency-related evidence available during interpretation.

---

## Clinical Context

Future systems must understand historical clinical interpretation state.

---

## Coding Interpretation Context

Future systems must understand coding-related reasoning applied by VAP.

---

## Noncoding Interpretation Context

Future systems must understand regulatory and noncoding reasoning applied by VAP.

---

## Prioritization Context

Future systems must understand escalation and deprioritization decisions.

---

## Validation Context

Future systems must understand why evidence was considered review-ready or not review-ready.

---

## Provenance Context

Future systems must be able to determine:

* where evidence originated
* how evidence was generated
* when evidence was generated
* which execution produced the evidence

---

## Uncertainty Context

Future systems must be able to distinguish between:

* known
* unknown
* ambiguous
* unmapped
* unsupported
* unavailable

states.

Preserving uncertainty is necessary for scientifically defensible reinterpretation.

---

# What Must Not Be Collapsed

The following distinctions should remain reconstructable:

* coding versus noncoding
* prioritized versus deprioritized
* interpreted versus uninterpreted
* annotated versus unannotated
* known versus uncertain
* candidate versus noncandidate
* observation versus summary

Preservation systems should avoid collapsing these distinctions into a single final-state representation.

---

# Current Support Versus Preservation Eligibility

The proposition:

> Current scientific support should not determine preservation eligibility.

is broadly supported.

Current scientific understanding is incomplete.

Many future discoveries will emerge from evidence classes that currently appear weakly informative.

Preservation decisions should therefore prioritize future reinterpretability rather than current popularity or current clinical significance.

Practical constraints may influence implementation strategies, but scientific preservation requirements should remain independent from transient interpretation confidence.

---

# Future Reinterpretability Requirements

A compliant preservation strategy should allow future systems to answer:

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
Why was this evidence prioritized?
```

```text
Why was this evidence not prioritized?
```

```text
How might future science reinterpret it?
```

without requiring access to the original VAP execution environment.

---

# Assumptions

* VAP remains authoritative for biological observations generated during execution.
* VDB remains authoritative for persistence and brokerage.
* Future scientific understanding will differ from current understanding.
* Future interpretation systems may use evidence differently than current systems.
* Preservation and interpretation are distinct responsibilities.

---

# Limitations

* This document does not define implementation requirements.
* This document does not define storage architecture.
* This document does not define retention policies.
* This document cannot predict future biological discoveries.

---

# Edge Cases

Particular care should be taken when handling:

* common variants
* noncoding variants
* weakly supported variants
* variants lacking annotation
* variants lacking clinical support
* ambiguous mappings
* conflicting annotations
* negative findings
* healthy-control observations

These evidence classes may become scientifically valuable despite limited present-day utility.

---

# Validation Strategy

A preservation strategy should be considered successful if future systems can reconstruct:

1. the original observed biological substrate
2. the contextual evidence available to VAP
3. the interpretation state generated by VAP
4. the uncertainty state generated by VAP
5. the prioritization decisions generated by VAP

without requiring re-execution of the original workflow.

---

# Implementation Relevance

This document establishes the scientific preservation requirements that future implementation authorities must satisfy.

Implementation approaches may vary.

Scientific preservation objectives should remain stable regardless of implementation choice.

---

# Conclusion

VAP-TEP should preserve more than final candidates and final reports.

It should preserve the observed biological substrate, annotation context, interpretation lineage, prioritization state, validation state, provenance context, and uncertainty state necessary for future scientific reinterpretation.

The central objective of VAP-TEP is evidence continuity.

Future systems should be able to determine what VAP observed, what VAP concluded, what VAP did not conclude, and how future science might reinterpret those observations long after the original execution environment no longer exists.
