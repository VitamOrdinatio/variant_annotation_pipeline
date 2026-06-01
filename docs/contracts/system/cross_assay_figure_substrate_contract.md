# cross_assay_figure_substrate_contract.md

## Purpose

This document defines the canonical behavioral contract governing metric emission, figure substrate assembly, and auto-render semantics across heterogeneous assay contexts within the Variant Annotation Pipeline (VAP).

The purpose of this contract is to ensure that:

* Whole exome sequencing (WES) runs,
* Whole genome sequencing (WGS) runs,
* healthy control datasets,
* disease-oriented datasets,
* and future assay contexts

all produce deterministic, semantically coherent, and reproducibly renderable figure substrates without flattening or silently corrupting biological meaning.

This contract formalizes the boundary between:

1. biological pipeline completion,
2. metric emission,
3. figure substrate assembly,
4. and downstream figure rendering.

---

# Scope

This contract governs:

* sidecar metric emission,
* figure substrate generation,
* auto-render orchestration,
* figure substrate validation,
* renderer gating behavior,
* and assay-aware semantic compatibility.

This contract does NOT govern:

* upstream variant calling,
* annotation semantics,
* transcript arbitration,
* or downstream VDB persistence contracts.

---

# Background

The motivating validation case for this contract was an HG002 WGS validation run which:

* successfully completed all 13 VAP stages,
* produced canonical processed artifacts,
* emitted most stage metrics successfully,
* but failed during figure substrate assembly due to assay-specific metric category absence.

The failure occurred because:

* figure substrate builders assumed the existence of biologically contingent semantic categories,
* and auto-render orchestration halted after figure substrate assembly incompleteness.

This revealed that:

* biological pipeline completion,
* figure substrate completeness,
* and figure rendering readiness

must be treated as distinct but formally connected operational states.

---

# Core Architectural Principle

VAP SHALL distinguish between:

1. Biological pipeline completion
2. Metric emission completeness
3. Figure substrate completeness
4. Renderer eligibility

These SHALL NOT be conflated.

---

# Canonical Definitions

## Biological Pipeline Completion

A run is considered biologically complete when:

* all required VAP stages execute successfully,
* canonical processed artifacts are produced,
* and stage summaries complete without fatal pipeline exceptions.

Biological completion does NOT imply:

* figure substrate completeness,
* figure renderer eligibility,
* or semantic category completeness.

---

## Metric Emission Completeness

Metric emission completeness refers to successful emission of:

* stage metric JSON files,
* long-format metric TSVs,
* and expected metric namespaces and aggregation groups.

Metric completeness does NOT imply:

* all biological semantic categories are populated,
* or all downstream figures are renderable.

---

## Figure Substrate Completeness

Figure substrate completeness refers to successful assembly of all expected figure-specific substrate files required by the configured figure set.

Figure substrate completeness SHALL be determinable from canonical artifact manifests and resolved figure configuration state.

Examples include:

* figure_f3a_flow_v2.tsv
* figure_f3b_semantic_branching.tsv
* figure_f4a_coding_semantic_composition_collapsed.tsv
* figure_f4b_noncoding_semantic_composition_collapsed.tsv

Figure substrate completeness SHALL be evaluated independently from biological completion.

---

## Renderer Eligibility

A figure SHALL only be eligible for rendering when:

* all required substrate files exist,
* substrate schemas validate,
* required columns validate,
* and semantic aggregation has completed successfully.

Renderer eligibility SHALL NOT be inferred merely from biological pipeline completion.

---

# Cross-Assay Compatibility Requirements

## WES and WGS Compatibility

Figure substrate builders SHALL operate correctly across:

* WES runs,
* WGS runs,
* healthy control datasets,
* disease-oriented datasets,
* and future cohort contexts.

The absence of a biological category in one assay context SHALL NOT be interpreted as pipeline failure.

---

## Assay-Aware Semantic Variability

Certain semantic categories are biologically contingent and may legitimately be absent in:

* healthy controls,
* non-disease cohorts,
* low-burden samples,
* or assay-specific contexts.

Examples include:

* clinically supported LOF categories,
* rare pathogenic enrichment categories,
* disease-associated semantic partitions.

The absence of such categories SHALL be treated as a valid biological state unless otherwise specified.

---

# Semantic Absence and Zero-Fill Policy

## Semantic Absence vs Null Semantics

The following states SHALL remain distinct:

* biologically absent categories,
* unknown or unavailable values,
* malformed or unresolved structures.

Biologically absent count-like semantic aggregation categories MAY be zero-filled when their absence represents a valid biological state.

Examples include:
* interpretation bucket counts,
* semantic partition counts,
* source interpretation category counts,
* and other count-oriented aggregation outputs.

Unknown, unresolved, malformed, or structurally invalid semantic states SHALL NOT be silently converted to zero.

---

## Non-Zero-Fill Structural Failures

The following SHALL remain fatal:

* missing required artifact files,
* missing required structural columns,
* malformed TSV schemas,
* corrupted JSON structures,
* failed substrate parsing,
* unresolved figure dependencies.

These SHALL produce explicit substrate assembly failure states.

---

# Renderer Gating Semantics

## Strict Renderer Behavior

When:

```yaml
figures:
  strict: true
```

then:

* any substrate assembly failure SHALL halt rendering,
* figure orchestration SHALL terminate non-successfully.

---

## Non-Strict Renderer Behavior

When:

```yaml
figures:
  strict: false
```

then:

* figure substrate failures SHALL be logged explicitly,
* unaffected figures MAY proceed if their own substrate contracts validate,
* failed figures SHALL be omitted from final rendering outputs.

However:

* malformed substrates SHALL NEVER silently render.

---

# Figure Substrate Validation Obligations

Figure substrate builders SHALL:

* validate required metric keys,
* validate required columns,
* validate schema integrity,
* and emit explicit failure diagnostics.

Missing biological semantic categories SHALL NOT raise structural exceptions when zero-fill semantics apply.

---

# Probe and Diagnostic Requirements

All figure substrate failures SHALL:

* emit human-readable diagnostics,
* identify missing categories or artifacts,
* identify affected figures,
* and support MARK probe workflows.

Probe outputs SHOULD:

* be timestamped,
* be text-readable,
* and be retrievable independently from the main run.

---

# Pytest Coverage Obligations

The VAP test suite SHALL include:

* WES semantic aggregation cases,
* WGS semantic aggregation cases,
* healthy-control semantic cases,
* missing-category zero-fill tests,
* malformed substrate tests,
* renderer strict/non-strict behavior tests,
* and figure substrate schema validation tests.

---

# Future Compatibility Expectations

This contract SHALL remain compatible with:

* future assay types,
* future figure sets,
* future semantic partitioning logic,
* future VDB persistence expectations,
* and future ontology-aware semantic aggregation.

The contract SHALL prioritize:

* semantic preservation,
* deterministic reproducibility,
* assay-aware biological interpretation,
* and explicit operational transparency.

---

# Non-Goals

This contract SHALL NOT:

* flatten biological uncertainty,
* silently infer unsupported semantics,
* auto-repair malformed structural artifacts,
* or permit rendering from incomplete structural substrate states.

---

# Operational Philosophy

VAP SHALL behave as:

* a deterministic semantic infrastructure system,
* not merely a plotting utility.

Biological absence is not equivalent to pipeline failure.

Structural ambiguity is not equivalent to biological ambiguity.

Renderer safety SHALL prioritize semantic integrity over maximal render completion.
