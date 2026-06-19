# VAP-TEP Risk Assessment

## Purpose

This document identifies scientific preservation risks associated with construction of the Variant Annotation Pipeline Transitional Evidence Product (VAP-TEP).

The purpose of this document is not to evaluate implementation risk.

The purpose is not to evaluate software architecture risk.

The purpose is to identify preservation failure modes that could compromise future scientific reinterpretation, discovery, reproducibility, or evidence continuity.

This document serves as the scientific preservation risk authority for future VAP-TEP implementation efforts.

---

# Scope

This document evaluates risks associated with:

* observation preservation
* contextual evidence preservation
* provenance preservation
* uncertainty preservation
* future reinterpretability
* discovery enablement

This document does not address:

* implementation architecture
* transport mechanisms
* database structures
* storage technologies
* schema design

---

# Risk Assessment Thesis

The primary risk in VAP-TEP construction is not merely data loss.

The primary risk is loss of future scientific interpretability.

A preservation system can remain technically functional while simultaneously eliminating future discovery opportunities.

Accordingly:

> The most significant preservation failures are those that prevent future systems from reconstructing what VAP observed, how VAP interpreted those observations, and how future science might reinterpret them.

---

# Risk Severity Principles

Preservation risks should be evaluated according to their impact on the following questions:

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
Why was evidence prioritized?
```

```text
Why was evidence not prioritized?
```

```text
How might future science reinterpret it?
```

Failure modes that prevent these questions from being answered should be considered high severity.

---

# Risk Register

## Risk 01: Candidate-Only Preservation

### Failure Mode

Only Stage 12 validation-ready candidates or Stage 13 summaries are preserved.

Observed variants that fail to reach candidate status are discarded.

### Scientific Consequence

Future systems lose access to observed biological substrate that was not selected for review.

Historical interpretation becomes biased toward evidence considered important at the time of execution.

Future discovery opportunities become constrained by historical prioritization decisions.

### Impact on VDB Discovery

VDB becomes a candidate repository rather than an evidence repository.

Discovery opportunities become limited to previously selected evidence.

### Impact on Future RDGP Reasoning

Future gene prioritization systems cannot evaluate evidence that was observed but not escalated.

Potential modifier, burden, or regulatory signals become unavailable.

### Recommended Mitigation

Preserve observations independently from candidate status.

Treat candidate designation as contextual information rather than preservation eligibility.

---

## Risk 02: Loss of Noncoding Observations

### Failure Mode

Noncoding evidence is discarded due to weak current interpretability.

### Scientific Consequence

Future regulatory interpretation becomes impossible for discarded observations.

Emerging biological models may be unable to evaluate previously observed evidence.

### Impact on VDB Discovery

Regulatory discovery surfaces become incomplete.

Future noncoding evidence exploration becomes artificially constrained.

### Impact on Future RDGP Reasoning

Future regulatory burden models, enhancer models, and noncoding prioritization frameworks lose access to potentially relevant substrate.

### Recommended Mitigation

Preserve noncoding observations regardless of current interpretive confidence.

Preserve associated uncertainty.

---

## Risk 03: Loss of Common Variants

### Failure Mode

Common variants are excluded from preservation due to population prevalence.

### Scientific Consequence

Future modifier models, burden analyses, protective variant studies, and population-aware interpretation systems become impaired.

### Impact on VDB Discovery

Discovery systems lose access to potentially important background context.

### Impact on Future RDGP Reasoning

Future polygenic and oligogenic reasoning frameworks become less informative.

### Recommended Mitigation

Treat population frequency as contextual information rather than automatic exclusion criteria.

---

## Risk 04: Loss of Genotype Context

### Failure Mode

Variant identity is preserved while genotype state is lost.

### Scientific Consequence

Biological interpretation becomes incomplete.

Future inheritance reasoning and burden analyses become impaired.

### Impact on VDB Discovery

Variant-level exploration remains possible but sample-level biological interpretation becomes weakened.

### Impact on Future RDGP Reasoning

Inheritance-aware prioritization and genotype-dependent reasoning become unreliable.

### Recommended Mitigation

Preserve genotype context alongside variant observations.

---

## Risk 05: Loss of Annotation Context

### Failure Mode

Only final classifications are preserved while annotation context is discarded.

### Scientific Consequence

Future systems cannot reconstruct what VAP knew at the time of execution.

Historical interpretation becomes difficult to audit.

### Impact on VDB Discovery

Evidence becomes detached from its original biological context.

### Impact on Future RDGP Reasoning

Future systems cannot compare contemporary interpretation against historical interpretation.

### Recommended Mitigation

Preserve annotation context independently from downstream interpretation outcomes.

---

## Risk 06: Loss of Population Context

### Failure Mode

Population evidence is removed after prioritization.

### Scientific Consequence

Historical rarity assessments become irreproducible.

Future population-aware reinterpretation becomes constrained.

### Impact on VDB Discovery

Population-based exploration becomes incomplete.

### Impact on Future RDGP Reasoning

Frequency-aware reasoning becomes less reliable.

### Recommended Mitigation

Preserve population context as an independent evidence layer.

---

## Risk 07: Loss of Clinical Context

### Failure Mode

Clinical interpretation state available during execution is discarded.

### Scientific Consequence

Historical interpretation environments become unrecoverable.

Future systems cannot determine how clinical evidence evolved over time.

### Impact on VDB Discovery

Temporal interpretation comparisons become difficult.

### Impact on Future RDGP Reasoning

Historical clinical evidence cannot be incorporated into reinterpretation workflows.

### Recommended Mitigation

Preserve available clinical interpretation context as historical evidence.

---

## Risk 08: Loss of Stage Lineage

### Failure Mode

Evidence is preserved without workflow progression history.

### Scientific Consequence

Future systems cannot determine how evidence reached its final state.

### Impact on VDB Discovery

Evidence trajectories become opaque.

Discovery systems lose visibility into refinement history.

### Impact on Future RDGP Reasoning

Prioritization decisions become difficult to audit.

### Recommended Mitigation

Preserve stage-derived context and evidence progression history.

---

## Risk 09: Loss of Uncertainty and Null Semantics

### Failure Mode

Unknown, ambiguous, unmapped, unsupported, and unavailable states collapse into a generic null representation.

### Scientific Consequence

Future interpretation becomes vulnerable to historical distortion.

Important limitations become invisible.

### Impact on VDB Discovery

Discovery systems may misinterpret absence of evidence as evidence of absence.

### Impact on Future RDGP Reasoning

Reasoning systems become susceptible to overconfidence and invalid assumptions.

### Recommended Mitigation

Preserve uncertainty states explicitly.

Maintain semantic distinctions between different forms of incompleteness.

---

## Risk 10: Loss of Provenance

### Failure Mode

Evidence becomes detached from its source, execution context, or lineage.

### Scientific Consequence

Scientific reproducibility becomes impaired.

Auditability becomes difficult.

### Impact on VDB Discovery

Trust in preserved evidence decreases.

### Impact on Future RDGP Reasoning

Evidence reliability becomes harder to assess.

### Recommended Mitigation

Preserve provenance as a first-class preservation requirement.

---

## Risk 11: Summary-Over-Substrate Collapse

### Failure Mode

Summary outputs are preserved while underlying observations are discarded.

### Scientific Consequence

Future reinterpretation becomes impossible.

Summary statistics cannot replace underlying biological observations.

### Impact on VDB Discovery

Discovery systems become limited to aggregate representations.

### Impact on Future RDGP Reasoning

Variant-level reasoning becomes impossible.

### Recommended Mitigation

Treat summaries as supplementary context rather than preservation substitutes.

---

## Risk 12: Loss of Deprioritized Evidence

### Failure Mode

Only escalated evidence survives preservation.

### Scientific Consequence

Historical false negatives become invisible.

Future reinterpretation opportunities become restricted.

### Impact on VDB Discovery

Discovery systems inherit historical selection bias.

### Impact on Future RDGP Reasoning

Future frameworks cannot reevaluate historical deprioritization decisions.

### Recommended Mitigation

Preserve evidence independently from prioritization outcomes.

---

## Risk 13: Loss of Healthy-Control Context

### Failure Mode

Evidence originating from healthy-control samples is considered scientifically unimportant and discarded.

### Scientific Consequence

Baseline biological context becomes less informative.

False-positive characterization becomes more difficult.

### Impact on VDB Discovery

Control-aware exploration becomes impaired.

### Impact on Future RDGP Reasoning

Future disease-versus-background comparisons become weaker.

### Recommended Mitigation

Preserve healthy-control observations and associated context.

---

## Risk 14: Overbinding to Current Scientific Models

### Failure Mode

Preservation eligibility becomes tightly coupled to current biological understanding.

### Scientific Consequence

Future discoveries become constrained by contemporary assumptions.

Historical blind spots become embedded into preservation policy.

### Impact on VDB Discovery

Discovery systems inherit present-day limitations.

### Impact on Future RDGP Reasoning

Future reasoning frameworks lose access to evidence classes that were previously undervalued.

### Recommended Mitigation

Separate preservation eligibility from current interpretive confidence.

Preserve observations even when scientific understanding remains incomplete.

---

# Cross-Cutting Mitigation Principles

The following principles reduce multiple preservation risks simultaneously.

## Preserve Observations Independently from Interpretation

Observation existence should not depend upon interpretation success.

---

## Preserve Context Independently from Prioritization

Context remains valuable even when evidence is not escalated.

---

## Preserve Uncertainty Explicitly

Unknown states should remain distinguishable from negative states.

---

## Preserve Lineage Explicitly

Evidence history should remain reconstructable.

---

## Preserve Future Discovery Opportunities

When preservation decisions are uncertain, preference should generally be given to preserving evidence rather than discarding evidence.

---

# Assumptions

* VAP remains authoritative for observation generation.
* VDB remains authoritative for persistence and brokerage.
* Future scientific understanding will differ from current understanding.
* Future interpretation frameworks may use evidence differently than contemporary systems.

---

# Limitations

* This document does not define implementation requirements.
* This document does not define storage architecture.
* This document does not define retention policies.
* Future scientific discoveries cannot be predicted.

---

# Edge Cases

Particular attention should be given to:

* noncoding observations
* common variants
* weakly supported variants
* clinically unexplained variants
* conflicting annotations
* ambiguous mappings
* deprioritized evidence
* healthy-control observations
* negative findings

These evidence classes are disproportionately vulnerable to preservation failure.

---

# Validation Strategy

A preservation strategy should be considered successful if future systems can:

1. reconstruct observed biological substrate
2. reconstruct contextual evidence available to VAP
3. reconstruct interpretation state
4. reconstruct prioritization decisions
5. reconstruct uncertainty state
6. reconstruct provenance lineage
7. reevaluate historical evidence using future scientific frameworks

without requiring access to the original VAP execution environment.

---

# Implementation Relevance

This document defines preservation risks that implementation authorities should mitigate.

Implementation approaches may vary.

The preservation objectives described here should remain stable regardless of implementation strategy.

---

# Conclusion

The dominant preservation risk facing VAP-TEP is evidence collapse.

The greatest scientific failure is not preserving too much weak evidence.

The greater failure is discarding observations whose future significance cannot yet be recognized.

A successful VAP-TEP should preserve enough biological substrate and contextual evidence to ensure that future systems can continue reasoning, discovery, reinterpretation, and validation long after the original execution environment no longer exists.
