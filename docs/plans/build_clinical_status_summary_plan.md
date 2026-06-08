# build_clinical_status_summary_plan.md

# Purpose

This document defines the implementation plan for generating:

```text
clinical_status_summary.new.tsv
```

for the post–May 22 VAP cohort expansion runs.

The goal is to extend the existing cross-run clinical-status telemetry substrate while preserving:

* append-only governance,
* historical schema compatibility,
* deterministic ClinVar-status aggregation,
* and strict backward compatibility with the May 22 artifact.

This implementation functions as:

```text
cross-run clinical evidence composition telemetry
```

within the broader VAP horizontal synthesis ecosystem.

---

# Scope

This implementation updates the cross-run table:

```text
docs/case_studies/cross_runs/cross_run_tables/clinical_status_summary.tsv
```

by generating an append-ready file:

```text
clinical_status_summary.new.tsv
```

for the 13 newer VAP executions only.

This implementation does NOT:

* overwrite the May 22 baseline file,
* regenerate historical rows,
* expand the schema,
* or include additional clinical-significance metrics beyond the original seven status buckets.

---

# Historical Baseline Schema

The May 22 artifact uses the following schema:

```text
sample_id
run_id
assay_type
run_classification
clinical_evidence
clinical_status
variant_count
```

This column order must be preserved exactly.

Schema drift is prohibited.

---

# Canonical Clinical Status Buckets

The implementation will emit only the seven clinical-status categories present in the May 22 artifact:

```text
benign
conflicting
likely_benign
likely_pathogenic
missing
pathogenic
vus
```

The implementation must not add newer or richer upstream metrics such as:

```text
clinical_significance_distribution__
```

Those richer metrics may be useful later, but they are out of scope for this append-only compatibility update.

---

# Canonical Input Artifact

For each run, the implementation will read:

```text
results/<run_id>/metadata/stage_metrics_long.tsv
```

The relevant rows are those where:

```text
metric_name
```

starts with:

```text
clinical_status__
```

Example metric names:

```text
clinical_status__benign
clinical_status__conflicting
clinical_status__likely_benign
clinical_status__likely_pathogenic
clinical_status__missing
clinical_status__pathogenic
clinical_status__vus
```

---

# Extraction Logic

For each manifest row:

1. read `stage_metrics_long.tsv`
2. filter rows where `metric_name` begins with `clinical_status__`
3. retain only the canonical seven May 22 buckets
4. parse `clinical_status` from the suffix after `clinical_status__`
5. emit one row per clinical-status bucket

Expected cardinality:

```text
13 runs × 7 clinical-status buckets = 91 rows
```

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

## clinical_evidence

Recommended deterministic value:

```text
clinvar
```

---

## clinical_status

Source:

```text
metric_name suffix after clinical_status__
```

---

## variant_count

Source:

```text
metric_value
```

from `stage_metrics_long.tsv`.

The value should be emitted as an integer count.

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
clinical_evidence
clinical_status
variant_count
```

---

## 2. Row cardinality

Expected:

```text
91 rows
```

---

## 3. Per-run bucket completeness

Each run must emit exactly the seven canonical clinical-status buckets.

---

## 4. Unique row identity

Each:

```text
run_id + clinical_status
```

pair must appear exactly once.

---

## 5. HG002 governance

The HG002 benchmark row group must use:

```text
sample_id = HG002
assay_type = WGS
run_classification = benchmark_wgs
```

---

## 6. Count validity

`variant_count` must be:

* non-null,
* integer-compatible,
* and non-negative.

---

# Missing Data Policy

The implementation should fail loudly if any canonical clinical-status bucket is missing for a run.

Silent omission would break compatibility with the historical May 22 substrate.

---

# Filesystem Governance

The implementation must act as:

```text
read-only clinical-status aggregation infrastructure
```

It must NOT:

* mutate run outputs,
* overwrite the May 22 table,
* or modify upstream `stage_metrics_long.tsv` files.

---

# Recommended Script Location

```text
scripts/analysis/build_clinical_status_summary.py
```

---

# Recommended Output Path

```text
docs/case_studies/cross_runs/cross_run_tables/clinical_status_summary.new.tsv
```

---

# Recommended CLI Defaults

When executed from the VAP repository root, the script should default to:

```text
--results-dir results
--out docs/case_studies/cross_runs/cross_run_tables/clinical_status_summary.new.tsv
```

Expected invocation:

```bash
python scripts/analysis/build_clinical_status_summary.py
```

The script should also allow both paths to be overridden.

---

# Governance Alignment

This implementation aligns with VAP cross-run governance principles emphasizing:

* append-only telemetry extension,
* stable schema preservation,
* bounded semantic compression,
* clinical-interpretation restraint,
* and deterministic comparative substrate generation.

This table supports future Contrast 05 analysis by preserving a compact cross-run view of clinical-status burden without expanding into unsupported biological interpretation.
