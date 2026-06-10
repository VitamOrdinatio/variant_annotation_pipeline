# F3B_SEMANTIC_BRANCHING_SCHEMA.md

# Purpose

This document defines the canonical telemetry substrate schema for:

```text
metrics/figure_f3b_semantic_branching.tsv
```

F3B exists to communicate:

```text
semantic evidence preservation topology.
```

Specifically:

```text
VAP preserves multiple biologically meaningful evidence classes
and does not naïvely discard noncoding evidence.
```

Unlike F3A:

F3B is NOT:

- a coarse lineage funnel
- a deterministic reduction cascade
- a simple survivorship Sankey

F3B instead models:

- semantic evidence branching
- interpretation topology
- evidence preservation structure
- coding/noncoding semantic continuity
- refinement observability

---

# Canonical Output Path

`metrics/figure_f3b_semantic_branching.tsv`

This substrate is emitted by:

```python
build_f3b_semantic_branching_table()
```

inside:

`src/metrics/metric_aggregation.py`

---

# Schema Columns

| Column             | Description                          |
| ------------------ | ------------------------------------ |
| figure_id          | Figure namespace identifier (`F3B`)  |
| run_id             | Canonical VAP run identifier         |
| sample_id          | Sample accession or identifier       |
| assay_type         | WES, WGS, etc.                       |
| run_classification | Pipeline execution class             |
| branch_order       | Deterministic renderer ordering      |
| branch_id          | Stable semantic branch identifier    |
| branch_label       | Human-readable semantic branch label |
| semantic_group     | Higher-level ontology grouping       |
| branch_class       | Rendering/domain classification      |
| stage_id           | Originating telemetry stage          |
| metric_name        | Source metric identifier             |
| metric_value       | Canonical semantic branch magnitude  |
| semantic_role      | Semantic role classification         |
| semantic_caveat    | Caveat or interpretive restraint     |
| source_artifact    | Upstream telemetry source            |
| generated_at       | UTC timestamp                        |

---

# Semantic Groups

Allowed canonical semantic groups:

| semantic_group     | Meaning                                           |
| ------------------ | ------------------------------------------------- |
| rare_interpretable | Biologically meaningful rare evidence             |
| common_low_support | Common or lower-confidence evidence               |
| uninterpretable    | Evidence retained with interpretation limitations |

Additional groups may be introduced later if:

- provenance-preserving
- ontology-stable
- assay-agnostic

---

# Branch Classes

Allowed canonical branch classes:

| branch_class | Meaning                    |
| ------------ | -------------------------- |
| coding       | Coding-derived evidence    |
| noncoding    | Noncoding-derived evidence |
| mixed        | Mixed semantic lineage     |

Future classes may include:

- structural
- transcriptomic
- mitochondrial_specific

provided ontology integrity is preserved.

---

# Current Canonical Branches

| branch_id                    | semantic_group     | branch_class |
| ---------------------------- | ------------------ | ------------ |
| coding_rare_interpretable    | rare_interpretable | coding       |
| regulatory_transcript_rare   | rare_interpretable | noncoding    |
| common_low_support           | common_low_support | coding       |
| noncoding_common_low_support | common_low_support | noncoding    |
| coding_uninterpretable       | uninterpretable    | coding       |
| noncoding_uninterpretable    | uninterpretable    | noncoding    |

---

# Ontology Rules

F3B semantic branches are:

- observational
- provenance-preserving
- non-diagnostic
- non-exclusive unless explicitly stated

F3B must NEVER imply:

- pathogenicity certainty
- validation completion
- semantic exclusivity
- causal certainty

---

# Forbidden Semantic Transformations

Forbidden:

- silent ontology merging
- unsupported survivorship claims
- fabricated exclusivity
- semantic inflation
- destructive compression
- unsupported causal interpretation

---

# Validation Rules

Validation requirements:

- deterministic branch ordering
- telemetry parity preservation
- ontology conservation
- no silent row duplication
- no unsupported semantic collapse

Required checks:

| Validation Target | Expected Behavior              |
| ----------------- | ------------------------------ |
| metric_value      | reconciles to source telemetry |
| semantic_group    | ontology-valid                 |
| branch_class      | renderer-valid                 |
| branch ordering   | deterministic                  |
| semantic caveats  | preserved                      |

---

# Architectural Position

F3B substrate generation is:

```text
semantic telemetry infrastructure
```

NOT:

```text
plot-specific formatting logic
```

Renderer implementations must remain downstream consumers of this schema.

---