# f3_cross_assay_semantic_hardening_plan.md

## Purpose

This implementation plan defines the hardening strategy required to bring F3 semantic aggregation and figure substrate generation into compliance with the cross-assay figure substrate contract.

The primary operational directive is:

1. Preserve existing WES figure substrate and autorender behavior.
2. Permit successful WGS autorender execution for biologically valid healthy-control datasets such as HG002.

This plan SHALL prioritize semantic preservation and deterministic reproducibility over maximal render permissiveness.

---

# Background

The HG002 WGS validation run:

```text
run_2026_05_28_063354
```

successfully completed the canonical VAP pipeline but failed during figure substrate assembly for F3 semantic aggregation.

The failure occurred because:

* F3 semantic aggregation logic assumed the existence of biologically contingent semantic count categories,
* and missing category lookups raised structural exceptions.

The corresponding WES validation run:

```text
run_2026_05_27_233524
```

successfully completed both:

* canonical pipeline execution,
* and figure autorender orchestration.

Structural comparison demonstrated that:

* core pipeline execution remained healthy,
* canonical processed artifacts emitted correctly,
* stage metrics emitted correctly,
* but F3 semantic aggregation did not tolerate biologically absent count categories in healthy-control WGS context.

---

# Architectural Objective

F3 semantic aggregation SHALL distinguish between:

1. biologically absent semantic count categories,
2. and structurally invalid aggregation states.

The following SHALL remain distinct:

* absent biological category,
* unknown semantic state,
* malformed structural state,
* unresolved aggregation dependency.

---

# Prime Directive

## Required Preservation Constraint

Hardening SHALL preserve existing WES figure outputs.

Specifically:

* pre-hardening WES F3/F4/F5 outputs SHALL remain value-equivalent,
* semantic aggregation values SHALL remain unchanged for existing WES validation datasets,
* and figure rendering behavior SHALL remain unchanged for existing WES cohorts.

This SHALL be treated as a regression protection requirement.

---

## Required WGS Compatibility Constraint

Hardening SHALL permit successful F3 semantic aggregation and autorender execution for:

* HG002 WGS,
* future healthy-control WGS datasets,
* and future assay-compatible WGS cohorts.

Biologically absent semantic categories explicitly designated as zero-fillable SHALL NOT trigger structural aggregation failure.

---

# Current Failure Mechanism

Current F3 aggregation logic performs direct lookup access:

```python
lookup[(stage_name,metric_name)]
```

This causes:

```text
missing semantic category -> KeyError
```

during aggregation for biologically contingent count buckets.

This behavior violates the cross-assay figure substrate contract.

---

# Hardening Strategy

## Strategy Overview

Hardening SHALL:

* preserve strict structural validation,
* preserve strict artifact validation,
* preserve strict required metric validation,
* while permitting explicit zero-fill semantics for designated biological count categories.

---

# Semantic Classification Model

## Required Structural Metrics

The following metric classes SHALL remain structurally required:

* backbone lineage metrics,
* artifact dependency metrics,
* required stage completion metrics,
* required validation metrics,
* required aggregation metrics.

Missing required structural metrics SHALL remain fatal.

---

## Optional Biological Count Categories

The following classes MAY be treated as zero-fillable:

* interpretation label count buckets,
* semantic partition count buckets,
* biologically contingent evidence category counts,
* disease-associated count categories absent in healthy-control datasets.

Examples include:

* counts_by_source_interpretation_label__lof_rare_clinically_supported
* counts_by_source_interpretation_label__regulatory_or_transcript_rare

Absence of these categories MAY validly represent:

```text
observed biological count = 0
```

rather than:

```text
aggregation failure
```

---

# Localization Strategy

Zero-fill semantics SHALL NOT be implemented globally.

Specifically:

* low-level metric lookup SHALL remain strict,
* generic metric access SHALL remain structurally validating,
* global metric retrieval SHALL NOT silently substitute zero.

Instead:

* zero-fill semantics SHALL be localized to assay-aware F3 semantic aggregation logic.

This preserves:

* structural safety,
* semantic transparency,
* and failure interpretability.

---

# F3 Hardening Objectives

## F3A Objectives

F3A hardening SHALL:

* preserve current WES edge values,
* preserve current scaling behavior,
* preserve current lineage semantics,
* while permitting absent biological categories to contribute zero to aggregate counts.

---

## F3B Objectives

F3B hardening SHALL:

* preserve current WES semantic branch values,
* preserve current branch structure,
* preserve current semantic grouping logic,
* while permitting biologically absent branches to emit zero-valued branch counts.

Absent biological branches SHALL remain explicitly represented rather than silently omitted.

---

# Non-Goals

Hardening SHALL NOT:

* weaken structural validation globally,
* permit malformed artifacts,
* silently ignore unresolved dependencies,
* flatten semantic ambiguity into zero,
* or silently alter WES aggregation behavior.

---

# Pytest Requirements

Hardening SHALL include pytest coverage for:

## WES Preservation Tests

Tests SHALL verify:

* WES F3 outputs remain value-equivalent,
* existing WES figure substrates remain unchanged,
* existing WES render outputs remain structurally consistent.

---

## WGS Healthy-Control Tests

Tests SHALL verify:

* biologically absent categories zero-fill correctly,
* F3 substrate generation completes successfully,
* renderer eligibility and autorender execution,
* and figure orchestration proceeds successfully.

---

## Structural Failure Tests

Tests SHALL verify:

* malformed metric files remain fatal,
* missing required backbone metrics remain fatal,
* unresolved dependencies remain fatal,
* and invalid schemas remain fatal.

---

# MARK Validation Strategy

Validation SHALL proceed using completed HG002 and WES runs already present on MARK.

The hardening workflow SHALL follow:

1. Implement localized F3 semantic hardening on sys76.
2. Add pytest coverage on sys76.
3. Push hardened implementation to Git.
4. Pull hardened implementation on MARK.
5. Re-run figure substrate generation against completed HG002 run only.
6. Verify successful substrate emission.
7. Verify successful autorender execution.
8. Compare WES outputs pre/post hardening for equivalence.

No full 20-hour WGS rerun SHALL be required unless canonical biological pipeline behavior changes.

---

# Acceptance Criteria

Hardening SHALL be considered successful when:

## WES Preservation

The following remain unchanged for WES validation cohorts:

* F3 semantic substrate values,
* F4 semantic substrate values,
* figure manifests,
* rendered figures,
* and semantic aggregation outputs.

---

## WGS Compatibility

HG002 SHALL:

* emit complete F3 substrate outputs,
* complete autorender orchestration successfully,
* produce renderer-eligible figure substrates,
* and avoid structural aggregation failure from biologically absent categories.

---

# Operational Philosophy

The objective of this hardening effort is NOT to maximize rendering permissiveness.

The objective is to:

* preserve deterministic semantic infrastructure behavior,
* preserve structural rigor,
* preserve biological interpretability,
* and distinguish valid biological absence from structural corruption.

Healthy-control WGS absence states SHALL remain biologically meaningful rather than structurally fatal.
