# F4_IMPLEMENTATION_PLAN.md

# Purpose

F4 communicates:

```text
biological evidence observability.
```

F4 is NOT:

```text
a collection of generic variant charts.
```

F4 exists to expose:

- biological evidence structure
- semantic evidence preservation
- interpretation distributions
- coding/noncoding evidence topology
- rarity structure
- clinical evidence landscape
- validation-readiness landscape

The reviewer should conclude:

```text
The repository preserves biologically meaningful substrate
for future reinterpretation and translational analysis.
```

NOT:

```text
The repository claims diagnostic certainty.
```

F4 now functions as:

```text
a semantic biological observability suite.
```

---

# Telemetry Inputs

Primary telemetry substrate:

```text
metrics/stage_metrics_long.tsv
```

Supporting telemetry JSONs:

```text
metrics/stage_09_coding_interpretation_metrics.json
metrics/stage_10_noncoding_interpretation_metrics.json
metrics/stage_11_prioritization_metrics.json
metrics/stage_12_validation_metrics.json
```

Optional validation references:

```text
processed/stage_09_coding_interpreted.tsv
processed/stage_10_noncoding_interpreted.tsv
processed/stage_11_prioritized_variants.tsv
```

Legacy harvested tables MAY be used only as:
- secondary reconciliation aids
- optional comparative summaries

but NOT as canonical source-of-truth.

---

# Canonical Metrics

## F4A — Coding vs Noncoding Landscape

Canonical metrics:

- variants_by_variant_class__coding
- variants_by_variant_class__noncoding
- variants_by_context__*

---

## F4B — Functional Consequence Landscape

Canonical metrics:

- consequence_distribution__*
- variants_by_severity__*
- functional_impact_distribution__*

---

## F4C — Clinical Significance Landscape

Canonical metrics:

- clinical_significance_distribution__*
- clinvar_significance_distribution__*

---

## F4D — Interpretation Label Topology

Canonical metrics:

- noncoding_interpretation_label_distribution__*
- counts_by_source_interpretation_label__*

---

## F4E — Rarity / Frequency Structure

Canonical metrics:

- rarity_flag_distribution__*
- frequency_status__*

---

## F4F — Validation Readiness Structure

Canonical metrics:

- counts_by_validation_required__*
- counts_by_validation_priority__*
- counts_by_suggested_validation_method__*

---

# Allowed Transformations

Allowed:

- category grouping
- ontology compression
- deterministic sorting
- severity ordering
- rarity ordering
- category collapsing
- restrained normalization
- panel decomposition
- provenance-preserving relabeling

Allowed grouping examples:

```text
Benign + Likely benign
```

ONLY IF:
- grouping is explicitly documented
- provenance remains recoverable

Allowed normalization:

- raw counts
- percent-of-total
- restrained log scaling

Allowed ordering:

- severity-descending
- rarity-descending
- interpretability-descending

Allowed panelization:

- independent panel scales
- panel-local normalization
- semantic-domain separation

---

# Forbidden Transformations

Forbidden:

- pathogenicity inflation
- mechanistic speculation
- unsupported disease claims
- enrichment theatrics
- hidden semantic compression
- unsupported ontology collapse
- diagnostic framing
- causality implication

Specifically forbidden:

- implying clinical diagnosis
- implying causal pathogenicity
- implying mechanistic certainty
- implying noncoding interpretation maturity beyond current telemetry support

Forbidden visual rhetoric:

```text
catastrophic-risk theater
```

including:
- extreme color dramatization
- exaggerated rarity collapse
- alarmist pathogenicity framing

Forbidden semantic behavior:

- silent ontology merging
- hidden denominator changes
- undocumented filtering
- unsupported cross-panel comparisons

---

# Proposed Visualization Architecture

Recommended architecture:

```text
multi-panel biological observability suite
```

Recommended panel organization:

| Panel | Domain |
|---|---|
| F4A | coding vs noncoding topology |
| F4B | functional consequence landscape |
| F4C | clinical evidence distributions |
| F4D | interpretation label topology |
| F4E | rarity and frequency structure |
| F4F | validation-readiness topology |

Recommended visualization types:

- stacked distributions
- restrained bar systems
- semantic topology summaries
- categorical heatmaps
- ontology distribution matrices

Avoid:

- network hairballs
- pathway dramatization
- systems-biology overclaim graphics
- unsupported mechanistic diagrams
- AI-orchestration aesthetics

Recommended visual tone:

```text
translational infrastructure observability
```

NOT:

```text
consumer analytics dashboard
```

---

# Reviewer Risk Analysis

## Risk 1

Reviewer conclusion:

```text
The pipeline claims pathogenicity.
```

Mitigation:

- observational framing
- preserve uncertainty classes
- avoid causal terminology

---

## Risk 2

Reviewer conclusion:

```text
Clinical significance equals diagnosis.
```

Mitigation:

- preserve ClinVar provenance language
- avoid diagnostic wording

---

## Risk 3

Reviewer conclusion:

```text
Noncoding interpretation is comprehensive.
```

Mitigation:

- preserve scientific restraint
- preserve “AlphaGenome not yet run” reality

---

## Risk 4

Reviewer conclusion:

```text
Rarity equals disease relevance.
```

Mitigation:

- separate rarity from pathogenicity
- preserve observational semantics

---

## Risk 5

Reviewer conclusion:

```text
Validation routing implies validation completion.
```

Mitigation:

- preserve “validation-ready” framing
- avoid confirmed-language

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

Recommended filenames:

```text
err10619300_f4_biological_observability_suite.png
err10619300_f4_biological_observability_suite.pdf
err10619300_f4_biological_observability_suite_source.tsv
err10619300_f4_biological_observability_suite_provenance.tsv
```

Recommended optional outputs:

```text
panel_manifest.tsv
ontology_groupings.tsv
normalization_rules.tsv
```

Provenance TSV must include:

- source telemetry files
- panel mappings
- semantic grouping rules
- ordering rules
- normalization modes
- telemetry extraction timestamps
- run_id

---

# Validation Strategy

Validation must include:

- metric parity validation
- panel-to-source reconciliation
- ontology conservation checks
- rarity-distribution reconciliation
- severity-distribution reconciliation
- no hidden semantic compression
- no unsupported grouping

Specific validation checks:

| Validation Target | Expected Behavior |
|---|---|
| Clinical distributions | reconcile to telemetry |
| Severity totals | reconcile to source counts |
| Rarity totals | preserve row conservation |
| Interpretation labels | preserve ontology provenance |
| Validation readiness | preserve deterministic routing |

Additional checks:

- no silent denominator shifts
- no unsupported normalization
- no cross-panel semantic contradiction

---

# Final Architectural Position

F4 is NOT:

```text
variant-chart theater.
```

F4 is:

```text
biological evidence observability infrastructure.
```

The figure suite should communicate:

```text
scientific restraint,
semantic transparency,
evidence preservation,
and translational maturity.
```