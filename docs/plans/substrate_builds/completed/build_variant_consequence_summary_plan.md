# build_variant_consequence_summary_plan.md

# Purpose

This document defines the implementation plan for generating:

```text
variant_consequence_summary.new.tsv
```

for the post–May 22 VAP cohort expansion runs.

The goal is to extend the existing cross-run semantic consequence telemetry substrate while preserving:

* append-only governance,
* deterministic semantic compression,
* historical schema compatibility,
* and stable coding/noncoding comparative topology.

This implementation functions as:

```text
cross-run molecular consequence composition telemetry
```

within the broader VAP horizontal synthesis ecosystem.

---

# Scope

This implementation updates the cross-run table:

```text
docs/case_studies/cross_runs/cross_run_tables/variant_consequence_summary.tsv
```

by generating:

```text
variant_consequence_summary.new.tsv
```

containing only the 13 newer VAP executions.

This implementation does NOT:

* overwrite the May 22 baseline artifact,
* regenerate historical rows,
* expand the schema,
* or introduce additional semantic compression categories beyond the historical topology.

---

# Historical Baseline Schema

The May 22 artifact uses the following schema:

```text
sample_id
run_id
assay_type
run_classification
interpretation_domain
molecular_consequence
count
```

This schema ordering must be preserved exactly.

Schema drift is prohibited.

---

# Historical Telemetry Topology

The May 22 artifact encodes:

```text
2 interpretation domains × 6 molecular consequence classes
```

per run.

Observed interpretation domains:

```text
coding
noncoding
```

Observed molecular consequence classes:

```text
loss_of_function
missense
other_coding
splice_relevant
synonymous
utr_regulatory
```

Expected append-only topology:

```text
13 runs × 2 domains × 6 consequence classes
= 156 rows
```

---

# Canonical Input Artifact

For each run, the implementation will read:

```text
results/<run_id>/metrics/stage_metrics_long.tsv
```

The implementation will extract metrics from two canonical metric families:

## Coding metrics

```text
coding_consequence__
```

## Noncoding metrics

```text
noncoding_consequence__
```

Example metric names:

```text
coding_consequence__loss_of_function
coding_consequence__missense
coding_consequence__other_coding
coding_consequence__splice_relevant
coding_consequence__synonymous
coding_consequence__utr_regulatory
```

and:

```text
noncoding_consequence__loss_of_function
noncoding_consequence__missense
noncoding_consequence__other_coding
noncoding_consequence__splice_relevant
noncoding_consequence__synonymous
noncoding_consequence__utr_regulatory
```

---

# Extraction Logic

For each manifest run:

1. read `stage_metrics_long.tsv`
2. extract rows beginning with:

   * `coding_consequence__`
   * `noncoding_consequence__`
3. parse:

   * interpretation domain
   * molecular consequence class
4. emit one row per:

   * interpretation_domain
   * molecular_consequence

The implementation should preserve the exact historical topology.

No additional semantic categories may be emitted.

---

# Canonical Manifest Rows

The implementation will use explicit manifest rows:

| source_accession | sample_id   | run_id                | assay_type | run_classification |
| ---------------- | ----------- | --------------------- | ---------- | ------------------ |
| ERR10619203      | ERR10619203 | run_2026_05_30_071639 | WES        | q3                 |
| ERR10619207      | ERR10619207 | run_2026_06_01_124134 | WES        | q3                 |
| ERR10619208      | ERR10619208 | run_2026_05_30_151355 | WES        | median             |
| ERR10619212      | ERR10619212 | run_2026_05_30_214724 | WES        | q1                 |
| ERR10619225      | ERR10619225 | run_2026_05_31_091242 | WES        | q3                 |
| ERR10619230      | ERR10619230 | run_2026_06_01_004903 | WES        | q3                 |
| ERR10619241      | ERR10619241 | run_2026_06_02_052302 | WES        | q1                 |
| ERR10619281      | ERR10619281 | run_2026_05_27_233524 | WES        | median             |
| ERR10619285      | ERR10619285 | run_2026_06_02_124300 | WES        | median             |
| ERR10619300      | ERR10619300 | run_2026_05_27_172531 | WES        | median             |
| ERR10619309      | ERR10619309 | run_2026_06_02_181024 | WES        | q1                 |
| ERR10619330      | ERR10619330 | run_2026_06_01_203130 | WES        | q1                 |
| SRR12898354      | HG002       | run_2026_06_03_010030 | WGS        | benchmark_wgs      |

The emitted `sample_id` must use the governed synthesis label.

---

# Field Mapping

## sample_id

Source:

```text
manifest.sample_id
```

Special case:

```text
SRR12898354 → HG002
```

---

## run_id

Source:

```text
manifest.run_id
```

---

## assay_type

Source:

```text
manifest.assay_type
```

---

## run_classification

Source:

```text
manifest.run_classification
```

---

## interpretation_domain

Derived from metric prefix:

| Metric Prefix           | interpretation_domain |
| ----------------------- | --------------------- |
| coding_consequence__    | coding                |
| noncoding_consequence__ | noncoding             |

---

## molecular_consequence

Derived from metric suffix after:

```text
coding_consequence__
noncoding_consequence__
```

Canonical emitted classes:

```text
loss_of_function
missense
other_coding
splice_relevant
synonymous
utr_regulatory
```

---

## count

Source:

```text
metric_value
```

from `stage_metrics_long.tsv`.

The emitted value should be integer-compatible and non-negative.

---

# Validation Requirements

The implementation should validate:

## 1. Schema stability

Output columns must exactly match:

```text
sample_id
run_id
assay_type
run_classification
interpretation_domain
molecular_consequence
count
```

---

## 2. Row cardinality

Expected:

```text
156 rows
```

---

## 3. Domain completeness

Each run must contain exactly:

```text
coding
noncoding
```

---

## 4. Consequence completeness

Each interpretation domain must contain exactly:

```text
loss_of_function
missense
other_coding
splice_relevant
synonymous
utr_regulatory
```

---

## 5. Unique row identity

Each:

```text
run_id
interpretation_domain
molecular_consequence
```

triple must appear exactly once.

---

## 6. HG002 governance

HG002 rows must use:

```text
sample_id = HG002
assay_type = WGS
run_classification = benchmark_wgs
```

---

## 7. Count validity

`count` must be:

* non-null,
* integer-compatible,
* and non-negative.

---

# Missing Data Policy

The implementation should fail loudly if:

* a canonical interpretation domain is missing,
* a molecular consequence category is absent,
* or duplicate semantic rows are detected.

Silent semantic topology drift is prohibited.

---

# Filesystem Governance

The implementation must function as:

```text
read-only semantic consequence aggregation infrastructure
```

The implementation must NOT:

* modify upstream telemetry,
* overwrite the May 22 baseline artifact,
* or mutate VAP run outputs.

---

# Recommended Script Location

```text
scripts/analysis/build_variant_consequence_summary.py
```

---

# Recommended Output Path

```text
docs/case_studies/cross_runs/cross_run_tables/variant_consequence_summary.new.tsv
```

---

# Recommended CLI Defaults

When executed from the VAP repository root:

```text
--results-dir results
--out docs/case_studies/cross_runs/cross_run_tables/variant_consequence_summary.new.tsv
```

Expected invocation:

```bash
python scripts/analysis/build_variant_consequence_summary.py
```

The script should also allow path overrides for alternate execution environments.

---

# Governance Alignment

This implementation aligns with broader VAP cross-run governance principles emphasizing:

* bounded semantic compression,
* stable topology preservation,
* deterministic comparative telemetry,
* append-only governance,
* and reconstructable cross-run semantic infrastructure.

This table specifically supports:

```text
Contrast 05:
coding vs noncoding semantic compression analysis
```

by preserving a compact and topology-stable representation of molecular consequence burden across heterogeneous VAP executions.
