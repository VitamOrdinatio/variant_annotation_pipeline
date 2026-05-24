# F3B_IMPLEMENTATION_PLAN.md

# Purpose

F3B communicates:

```text
semantic refinement observability.
```

Unlike F3A:

F3B is NOT:
- a lineage diagram
- a simple flow chart
- or a deterministic reduction cascade.

F3B exists to expose:

- semantic decomposition
- interpretation topology
- prioritization structure
- validation topology
- refinement observability

The reviewer should conclude:

```text
The semantic refinement structure is observable,
inspectable,
and explainable.
```

NOT:

```text
The pipeline performs opaque ranking magic.
```

---

# Telemetry Inputs

Primary telemetry substrate:

`metrics/figure_f3b_semantic_branching.tsv`

This TSV is generated deterministically from:

`metrics/stage_metrics_long.tsv`

via:

```python
build_f3b_semantic_branching_table()
```

Supporting telemetry JSONs:

```text
metrics/stage_08_partition_metrics.json
metrics/stage_09_coding_interpretation_metrics.json
metrics/stage_10_noncoding_interpretation_metrics.json
metrics/stage_11_prioritization_metrics.json
metrics/stage_12_validation_metrics.json
```

Optional supporting processed artifacts:

```text
processed/stage_09_coding_interpreted.tsv
processed/stage_10_noncoding_interpreted.tsv
processed/stage_11_prioritized_variants.tsv
processed/stage_12_validation_candidates.tsv
```

---

# Canonical Metrics

Canonical F3B domains:

## Stage 08

- coding_candidates
- splice_region_candidates
- qc_flagged

## Stage 09

- consequence_distribution__*
- clinical_significance_distribution__*
- rarity_flag_distribution__*
- functional_impact_distribution__*

## Stage 10

- noncoding_functional_context_distribution__*
- noncoding_interpretation_label_distribution__*
- rarity_flag_distribution__*

## Stage 11

- counts_by_priority_tier__*
- counts_by_priority_rank__*
- counts_by_variant_origin__*
- counts_by_source_interpretation_label__*

## Stage 12

- counts_by_validation_priority__*
- counts_by_suggested_validation_method__*
- counts_by_validation_required__*

---

# Allowed Transformations

Allowed:

- grouped semantic aggregation
- panel decomposition
- ontology compression
- category collapsing
- semantic ordering
- deterministic sorting
- restrained normalization
- provenance-preserving semantic grouping

Allowed semantic grouping examples:

```text
HIGH + MODERATE
```

for readability.

Allowed ordering:

- severity-descending
- rarity-descending
- validation-priority-descending

Allowed panelization:

- interpretation panels
- prioritization panels
- validation panels
- coding/noncoding decomposition panels

---

# Forbidden Transformations

Forbidden:

- forced exclusivity
- fabricated semantic survivorship
- unsupported lineage inference
- hidden overlap elimination
- silent ontology merging
- unsupported causal claims
- semantic inflation

Specifically forbidden:

- implying coding + splice are mutually exclusive
- implying prioritization equals pathogenicity
- implying validation routing equals validation completion

Forbidden visual framing:

```text
semantic funnel collapse theater
```

where:
- large evidence classes visually “die”
- uncertainty is visually punished
- interpretability gaps are hidden

---

# Proposed Visualization Architecture

Recommended architecture:

```text
hybrid semantic topology system
```

NOT:

```text
mega-Sankey topology graph
```

Recommended semantic domains:

| Domain | Purpose |
|---|---|
| Rare interpretable evidence | biologically meaningful retained substrate |
| Regulatory/transcript rare evidence | preserved noncoding semantic continuity |
| Common or low-support evidence | deprioritized but preserved substrate |
| Uninterpretable evidence | retained evidence with interpretive limitations |
| Validation-ready evidence | downstream routing topology |

Recommended visualization structures:

- stacked distributions
- semantic decomposition matrices
- restrained heatmaps
- topology summaries
- categorical observability panels

Avoid:

- dense crossing flows
- artificial lineage weaving
- network dramatization
- fabricated semantic exclusivity
- destructive evidence collapse
- fake survivorship topology

---

# Reviewer Risk Analysis

## Risk 1

Reviewer conclusion:

```text
All semantic classes are exclusive.
```

Mitigation:

- explicit overlap honesty
- restrained decomposition language

---

## Risk 2

Reviewer conclusion:

```text
Interpretation labels imply diagnosis.
```

Mitigation:

- preserve observational framing
- avoid pathogenicity claims

---

## Risk 3

Reviewer conclusion:

```text
Prioritization tiers represent certainty.
```

Mitigation:

- emphasize routing semantics
- avoid certainty framing

---

## Risk 4

Reviewer conclusion:

```text
Noncoding interpretation is fully mature.
```

Mitigation:

- preserve scientific restraint
- preserve AlphaGenome-not-yet-run honesty

---

# Provenance Outputs

Expected outputs:

```text
PNG
PDF
source TSV
provenance TSV
optional audit TSV
```

Recommended naming:

```text
err10619300_f3b_semantic_refinement_observability.png
err10619300_f3b_semantic_refinement_observability.pdf
err10619300_f3b_semantic_refinement_observability_source.tsv
err10619300_f3b_semantic_refinement_observability_provenance.tsv
```

Provenance outputs should include:

- telemetry source files
- semantic grouping rules
- normalization rules
- ordering rules
- panel mappings
- ontology compression notes

---

# Canonical F3B Schema

Canonical substrate:

`metrics/figure_f3b_semantic_branching.tsv`

Canonical schema reference:

`F3B_SEMANTIC_BRANCHING_SCHEMA.md`

Renderer implementations must consume the canonical schema rather than reconstructing semantic topology directly from raw telemetry metrics.

---

# Validation Strategy

Validation must include:

- metric parity validation
- ontology reconciliation
- overlap honesty checks
- semantic grouping verification
- panel-to-source parity checks
- no fabricated exclusivity

Specific checks:

| Validation Target | Expected Behavior |
|---|---|
| Semantic totals | reconcile to source telemetry |
| Grouped classes | preserve provenance |
| Panel decompositions | preserve row conservation |
| Priority topology | deterministic |
| Validation topology | deterministic |

Additional checks:

- no silent ontology loss
- no semantic duplication
- no unsupported compression

---

# Final Architectural Position

F3B is NOT:

```text
ranking theater.
```

F3B is:

```text
semantic refinement observability infrastructure.
```

The figure system should communicate:

```text
semantic transparency,
interpretability,
and refinement inspectability.
```
