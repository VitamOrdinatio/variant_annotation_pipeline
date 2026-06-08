# build_coding_noncoding_consequence_summary_plan.md

# Purpose

This document defines the implementation plan for generating:

```text
coding_noncoding_consequence_summary.new.tsv
```

for the post–May 22 VAP cohort expansion runs.

The goal is to append 13 newer VAP executions to the existing public cross-run artifact while preserving:

* May 22 schema compatibility,
* apples-to-apples case-study narrative consistency,
* deterministic flattening of modern telemetry,
* and append-only governance.

This artifact is intended for public case-study review and Markdown-driven narrative synthesis.

It is not intended to serve as a durable downstream repo interface for VDB, RDGP, or other future ecosystem consumers.

---

# Scope

This implementation updates the cross-run table:

```text
docs/case_studies/cross_runs/cross_run_tables/coding_noncoding_consequence_summary.tsv
```

by generating:

```text
coding_noncoding_consequence_summary.new.tsv
```

containing only the 13 newer VAP executions.

This implementation does NOT:

* overwrite the May 22 baseline artifact,
* regenerate historical rows,
* alter the public schema,
* or introduce new telemetry axes that were not present in the May 22 artifact.

---

# Historical Baseline Schema

The May 22 artifact uses the following schema:

```text
sample_id
run_id
assay_type
run_classification
interpretation_domain
summary_axis
consequence_label
count
```

This schema ordering must be preserved exactly.

Schema drift is prohibited.

---

# Public Artifact Compatibility Principle

The modern VAP telemetry substrate is more granular than the May 22 public artifact.

For this table, the implementation intentionally flattens modern telemetry into the older public schema because the goal is:

```text
case-study narrative comparability
```

rather than:

```text
new ontology expansion
```

This flattening is acceptable because:

* the artifact is public-facing documentation substrate,
* the output is used for Markdown/case-study synthesis,
* the table is not carried forward as a downstream ecosystem interface,
* and apples-to-apples public interpretability is more important here than exposing every modern metric namespace.

The flattening rules must be explicit, deterministic, and documented.

---

# Canonical Input Artifact

For each run, the implementation will read:

```text
results/<run_id>/metrics/stage_metrics_long.tsv
```

This modern telemetry file contains richer metric families that must be flattened into the May 22 schema.

---

# Canonical Output Artifact

The implementation will write:

```text
docs/case_studies/cross_runs/cross_run_tables/coding_noncoding_consequence_summary.new.tsv
```

The output will contain only the 13 newer runs.

The output must be append-ready.

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

# Historical Summary Axes

The May 22 artifact contains the following `summary_axis` values:

```text
clinical_status
frequency_class
interpretation_label
variant_function
context
```

The implementation must emit only these axes.

No additional axes may be introduced.

---

# Interpretation Domains

The implementation must preserve:

```text
coding
noncoding
```

The domain is derived from modern stage identity and metric family.

Canonical stage mapping:

| stage_id | interpretation_domain |
| -------- | --------------------- |
| stage_09 | coding                |
| stage_10 | noncoding             |

Some summary axes derive from stage-specific metrics. Others derive from later aggregate interpretation metrics and must be split back into coding/noncoding by label prefix.

---

# Flattening Rules

## 1. frequency_class

Modern source:

```text
stage_09 / population_frequency_bin__*
stage_10 / population_frequency_bin__*
```

Output mapping:

| source stage | output interpretation_domain |
| ------------ | ---------------------------- |
| stage_09     | coding                       |
| stage_10     | noncoding                    |

Output `summary_axis`:

```text
frequency_class
```

Output `consequence_label`:

```text
common
rare
unknown
```

Rules:

* `common` and `rare` are emitted directly from modern `population_frequency_bin__common` and `population_frequency_bin__rare`.
* `unknown` must be emitted as `0` if not present.
* No additional population-frequency bins may be emitted.

---

## 2. interpretation_label

Modern source:

```text
counts_by_source_interpretation_label__*
```

Output `summary_axis`:

```text
interpretation_label
```

Domain splitting rules:

| Modern label prefix | output interpretation_domain |
| ------------------- | ---------------------------- |
| coding_             | coding                       |
| lof_                | coding                       |
| noncoding_          | noncoding                    |
| regulatory_         | noncoding                    |

The label suffix is preserved as the output `consequence_label`.

Rules:

* Labels absent from modern telemetry but present in the May 22 topology should be emitted as `0` where needed for compatibility.
* No labels outside the historical May 22 topology should be emitted unless explicitly approved later.

---

## 3. context

Modern source:

```text
stage_10 / noncoding_functional_context_distribution__*
```

Output `summary_axis`:

```text
context
```

Output domain:

```text
noncoding
```

Output `consequence_label` values:

```text
intergenic
intronic
proximal
regulatory
transcript_associated
unknown
```

Rules:

* Modern labels are emitted directly where names match.
* `regulatory` must be emitted as `0` if not present.
* Context is emitted for the noncoding domain only, matching May 22 public artifact topology.

---

## 4. variant_function

Modern source:

```text
stage_09 / consequence_distribution__*
stage_10 / consequence_distribution__*
```

Output `summary_axis`:

```text
variant_function
```

Output domains:

```text
coding
noncoding
```

Output `consequence_label` values:

```text
loss_of_function
missense
other_coding
splice_relevant
synonymous
unknown
```

Flattening priority:

1. `loss_of_function`
2. `missense`
3. `splice_relevant`
4. `synonymous`
5. `other_coding`

`unknown` must be emitted as `0` if not present.

Loss-of-function terms include:

```text
frameshift_variant
stop_gained
stop_lost
start_lost
splice_acceptor_variant
splice_donor_variant
```

Missense terms include:

```text
missense_variant
```

Splice-relevant terms include:

```text
splice_region_variant
splice_donor_region_variant
splice_donor_5th_base_variant
splice_polypyrimidine_tract_variant
```

Synonymous terms include:

```text
synonymous_variant
stop_retained_variant
```

All other recognized consequence strings collapse to:

```text
other_coding
```

The priority order matters because compound VEP consequence strings may contain multiple terms.

For example:

```text
splice_region_variant&synonymous_variant
```

must classify as:

```text
splice_relevant
```

not:

```text
synonymous
```

---

## 5. clinical_status

Modern source:

```text
stage_09 / clinical_significance_distribution__*
stage_10 / clinical_significance_distribution__*
```

Output `summary_axis`:

```text
clinical_status
```

Output domains:

```text
coding
noncoding
```

Canonical output labels:

```text
benign
conflicting
likely_benign
likely_pathogenic
missing
pathogenic
vus
```

Flattening rules:

* Missing or empty clinical-significance labels collapse to `missing`.
* Terms containing `pathogenic` and `likely_pathogenic` are counted in their corresponding categories.
* Terms containing `benign` and `likely_benign` are counted in their corresponding categories.
* Terms containing `conflicting` collapse to `conflicting`.
* Terms containing `uncertain_significance` or `vus` collapse to `vus`.
* Compound clinical-significance strings must be deterministically assigned by priority.

Recommended priority:

1. `pathogenic`
2. `likely_pathogenic`
3. `conflicting`
4. `vus`
5. `likely_benign`
6. `benign`
7. `missing`

This priority is chosen for stable case-study flattening, not clinical adjudication.

---

# Expected Output Cardinality

The May 22 artifact does not emit a perfectly rectangular grid across all summary axes.

Therefore, row cardinality should be validated against the explicitly defined historical topology rather than assuming:

```text
runs × domains × axes × labels
```

Expected append cardinality should be computed from the implemented historical topology template.

The implementation should report:

* total rows,
* rows per run,
* axes per run,
* and labels per run/domain/axis.

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
summary_axis
consequence_label
count
```

---

## 2. Unique semantic row identity

Each:

```text
run_id
interpretation_domain
summary_axis
consequence_label
```

combination must appear exactly once.

---

## 3. HG002 governance

HG002 rows must use:

```text
sample_id = HG002
assay_type = WGS
run_classification = benchmark_wgs
```

---

## 4. Count validity

`count` must be:

* non-null,
* integer-compatible,
* and non-negative.

---

## 5. Historical topology compatibility

Each run must emit the same deterministic historical topology template.

Any missing expected label should be emitted as `0`.

Any unexpected label should be excluded unless explicitly added to the historical topology template.

---

# Missing Data Policy

The implementation should fail loudly if a required modern metric family is absent.

For absent labels within an otherwise present metric family, the implementation should emit `0` if the label belongs to the historical topology template.

This preserves case-study comparability while preventing silent loss of major telemetry surfaces.

---

# Filesystem Governance

The implementation must function as:

```text
read-only semantic composition aggregation infrastructure
```

The implementation must NOT:

* modify upstream telemetry,
* overwrite the May 22 baseline artifact,
* mutate VAP run outputs,
* or introduce new public-schema columns.

---

# Recommended Script Location

```text
scripts/analysis/build_coding_noncoding_consequence_summary.py
```

---

# Recommended Output Path

```text
docs/case_studies/cross_runs/cross_run_tables/coding_noncoding_consequence_summary.new.tsv
```

---

# Recommended CLI Defaults

When executed from the VAP repository root:

```text
--results-dir results
--out docs/case_studies/cross_runs/cross_run_tables/coding_noncoding_consequence_summary.new.tsv
```

Expected invocation:

```bash
python scripts/analysis/build_coding_noncoding_consequence_summary.py
```

The script should also allow path overrides.

---

# Governance Qualification

This implementation intentionally performs legacy-compatible flattening.

The output should be interpreted as:

```text
a public case-study compatibility artifact
```

not:

```text
a complete representation of the modern VAP telemetry ontology.
```

This qualification should be preserved in README or methods notes accompanying the cross-run tables.

---

# Governance Alignment

This implementation aligns with broader VAP cross-run governance principles emphasizing:

* append-only telemetry extension,
* public artifact continuity,
* bounded semantic compression,
* deterministic flattening,
* and narrative comparability.

This table supports:

```text
Contrast 05:
Coding vs Noncoding Semantic Compression
```

by preserving a stable public-facing semantic composition matrix across historical and newer VAP executions.
