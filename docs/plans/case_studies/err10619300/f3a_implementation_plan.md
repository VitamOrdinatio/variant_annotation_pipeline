# F3A_IMPLEMENTATION_PLAN.md

# Purpose

F3A communicates:

```text
deterministic evidence lineage.
```

The figure exists to establish:

- operational trust
- refinement traceability
- deterministic evidence preservation
- reviewer comprehension of stagewise refinement

The reviewer should conclude:

```text
Evidence refinement remains deterministic, inspectable, and provenance-aware.
```

NOT:

```text
The pipeline aggressively destroys evidence through opaque filtering.
```

F3A is now considered:

```text
the refinement backbone
and trust backbone
of the ERR10619300 case study.
```

---

# Telemetry Inputs

Primary canonical telemetry substrate:

```text
metrics/figure_f3a_flow.tsv
```

Secondary telemetry reconciliation substrate:

```text
metrics/stage_metrics_long.tsv
```

Optional validation references:

```text
metrics/stage_08_partition_metrics.json
metrics/stage_11_prioritization_metrics.json
metrics/stage_12_validation_metrics.json
```

No legacy harvested tables should be used as primary source-of-truth.

---

# Canonical Metrics

The following metrics are considered canonical F3A substrate:

| Flow Segment | Metric |
|---|---|
| Raw variants | raw_called_variants |
| Normalized variants | normalized_variants |
| Annotated variants | annotated_variants_tsv |
| Partitioned evidence | partitioned_variants_total |
| Prioritized evidence | prioritized_variants_rows |
| Validation-ready evidence | validation_candidates_rows |

Supporting reconciliation metrics:

| Metric |
|---|
| coding_candidates |
| splice_region_candidates |
| qc_flagged |
| coding_interpreted_rows |
| noncoding_interpreted_rows |

---

# Called Variants To Validation-Ready Candidate Variants

| Node                                 | Canonical metric                                                  |
| ------------------------------------ | ----------------------------------------------------------------- |
| Called variants                      | raw_called_variants                                               |
| Annotated evidence                   | annotated_variants_tsv                                            |
| Coding/splice interpretable evidence | coding_interpreted_rows + splice_region_candidates                |
| Prioritized candidates               | high_priority_candidate_count + moderate_priority_candidate_count |
| Validation-ready candidates          | counts_by_validation_required__True                               |

---

# Allowed Transformations

Allowed:

- deterministic aggregation
- direct telemetry rendering
- monotonic lineage ordering
- restrained node collapsing
- visual width scaling
- optional log scaling for readability
- provenance-preserving relabeling
- stage ordering normalization

Allowed ordering:

```text
05 → 06 → 07 → 08 → 11 → 12
```

Allowed visual compression:

```text
partitioned semantic evidence
```

may represent Stage 08 collectively.

Allowed width normalization:

- linear scaling
- restrained log scaling

provided:
- ordering remains preserved
- relative evidence magnitude remains visually honest

---

# Forbidden Transformations

Forbidden:

- fabricated branch exclusivity
- implied evidence destruction
- unsupported survivorship claims
- semantic overlap concealment
- hidden deduplication
- inferred biological causality
- topology dramatization
- unsupported Sankey splitting

Specifically forbidden:

```text
coding_candidates
+
splice_region_candidates
```

MUST NOT be visualized as:
- mutually exclusive branches
- additive lineage totals

Reason:

Stage 08 overlap semantics are non-exclusive.

Additionally:

```text
qc_flagged
```

MUST NOT be represented as:
- evidence removal
- evidence destruction
- terminal evidence discard

because it behaves as:
- orthogonal review overlay
- not deterministic branch elimination

---

# Proposed Visualization Architecture

Recommended architecture:

```text
restrained deterministic lineage Sankey
```

OR:

```text
deterministic refinement cascade
```

Key characteristics:

- low branching complexity
- visually restrained geometry
- monotonic left-to-right refinement
- provenance-aware labeling
- explicit evidence counts
- minimal semantic theatrics

Recommended node ordering:

```text
Raw
→ Normalized
→ Annotated
→ Partitioned
→ Prioritized
→ Validation-ready
```

Recommended style:

- muted palette
- infrastructure-oriented aesthetics
- readability-first geometry
- reviewer cognition prioritization

Avoid:

- aggressive color saturation
- excessive branching
- circular topology
- network-hairball aesthetics

---

# Reviewer Risk Analysis

## Risk 1

Reviewer conclusion:

```text
The pipeline aggressively destroys variants.
```

Mitigation:

- monotonic refinement framing
- preservation-oriented language
- restrained reduction geometry

---

## Risk 2

Reviewer conclusion:

```text
All semantic branches are exclusive.
```

Mitigation:

- avoid overlap-heavy branch rendering
- avoid additive branch claims
- preserve Stage 08 ambiguity honestly

---

## Risk 3

Reviewer conclusion:

```text
QC flagging represents evidence deletion.
```

Mitigation:

- present QC as orthogonal overlay
- avoid terminal discard geometry

---

## Risk 4

Reviewer conclusion:

```text
Validation-ready means clinically validated.
```

Mitigation:

- explicit “validation-ready” terminology
- avoid diagnostic language

---

# Provenance Outputs

Expected deterministic outputs:

```text
PNG
PDF
source TSV
provenance TSV
optional audit TSV
```

Recommended filenames:

```text
err10619300_f3a_deterministic_evidence_lineage.png
err10619300_f3a_deterministic_evidence_lineage.pdf
err10619300_f3a_deterministic_evidence_lineage_source.tsv
err10619300_f3a_deterministic_evidence_lineage_provenance.tsv
```

Provenance TSV should include:

- source telemetry files
- metric extraction timestamps
- run_id
- plotting parameters
- scaling mode
- metric reconciliation notes

---

# Validation Strategy

Validation must include:

- telemetry reconciliation
- row conservation checks
- monotonic lineage verification
- Stage 08 overlap honesty checks
- figure-to-telemetry parity validation
- source TSV reconciliation

Validation checks:

| Validation Target | Expected Behavior |
|---|---|
| Raw → normalized | monotonic |
| Normalized → annotated | monotonic |
| Annotated → partitioned | semantically coherent |
| Partitioned → prioritized | deterministic refinement |
| Prioritized → validation-ready | deterministic routing |

Additional validation:

- no branch totals may exceed upstream totals
- no fabricated exclusivity
- no hidden branch merging
- no semantic drift from telemetry substrate

---

# Final Architectural Position

F3A is NOT:

```text
semantic theater.
```

F3A is:

```text
deterministic evidence lineage infrastructure.
```

The figure should communicate:

```text
trust,
traceability,
and refinement observability.
```
