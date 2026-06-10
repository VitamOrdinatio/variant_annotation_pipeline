# build_provenance_summary_plan.md

# Purpose

This document defines the implementation plan for generating:

```text
provenance_summary.new.tsv
```

for the post–May 22 VAP cohort expansion runs.

The goal is to extend the cross-run provenance telemetry substrate while preserving:

* append-only governance,
* deterministic metadata aggregation,
* provenance continuity,
* and historical telemetry integrity.

This implementation functions as:

```text
horizontal provenance observability infrastructure
```

within the broader VAP cross-run synthesis ecosystem.

---

# Scope

This implementation updates the cross-run telemetry layer for:

```text
docs/case_studies/cross_runs/cross_run_tables/provenance_summary.tsv
```

The implementation applies ONLY to:

* the 13 newer VAP executions completed after the original May 22 deterministic reproducibility cohort,
* and generation of append-ready provenance telemetry rows.

This implementation does NOT:

* overwrite the original May 22 provenance substrate,
* mutate historical telemetry,
* or regenerate the original deterministic reproducibility study.

---

# Historical Context

The original May 22 provenance telemetry artifact summarized:

* reproducibility-oriented VAP executions,
* infrastructure telemetry,
* execution metadata,
* and environment provenance.

Following the original reproducibility study, 13 additional executions were completed:

* 12 epilepsy WES runs
* 1 HG002 WGS benchmark run

This implementation therefore performs:

```text
incremental provenance extension
```

rather than:

```text
historical provenance replacement.
```

---

# Canonical Cohort Composition

The implementation will iterate over a manifest-driven cohort consisting of:

| Cohort Type         | Count |
| ------------------- | ----- |
| q1 WES              | 4     |
| median WES          | 4     |
| q3 WES              | 4     |
| HG002 WGS benchmark | 1     |

Total:

```text
13 run_<id> executions
```

---

# Canonical Manifest Rows

The implementation will use the following explicit manifest rows:

| source_accession | sample_id | run_id | assay_type | run_classification |
| --- | --- | --- | --- | --- |
| ERR10619203 | ERR10619203 | run_2026_05_30_071639 | WES | q3 |
| ERR10619207 | ERR10619207 | run_2026_06_01_124134 | WES | q3 |
| ERR10619208 | ERR10619208 | run_2026_05_30_151355 | WES | median |
| ERR10619212 | ERR10619212 | run_2026_05_30_214724 | WES | q1 |
| ERR10619225 | ERR10619225 | run_2026_05_31_091242 | WES | q3 |
| ERR10619230 | ERR10619230 | run_2026_06_01_004903 | WES | q3 |
| ERR10619241 | ERR10619241 | run_2026_06_02_052302 | WES | q1 |
| ERR10619281 | ERR10619281 | run_2026_05_27_233524 | WES | median |
| ERR10619285 | ERR10619285 | run_2026_06_02_124300 | WES | median |
| ERR10619300 | ERR10619300 | run_2026_05_27_172531 | WES | median |
| ERR10619309 | ERR10619309 | run_2026_06_02_181024 | WES | q1 |
| ERR10619330 | ERR10619330 | run_2026_06_01_203130 | WES | q1 |
| SRR12898354 | HG002 | run_2026_06_03_010030 | WGS | benchmark_wgs |

The `source_accession` field is retained for operator clarity, but the emitted `sample_id` must use the governed synthesis label.

---

# HG002 Naming Governance

The WGS benchmark execution:

```text
SRR12898354
```

should be represented within:

```text
sample_id
```

as:

```text
HG002
```

This preserves:

* benchmark cognition,
* assay-aware synthesis readability,
* and ecosystem-level semantic clarity.

HG002 is considered:

```text
a benchmark substrate identity
```

rather than merely:

```text
an accession identifier.
```

---

# Canonical Input Artifacts

The implementation will aggregate telemetry from:

## 1. run_metadata.json

Canonical path:

```text
results/<run_id>/metadata/run_metadata.json
```

Primary purpose:

* operational execution metadata,
* machine telemetry,
* runtime status,
* pipeline metadata.

---

## 2. run_fingerprint.json

Canonical path:

```text
results/<run_id>/metadata/run_fingerprint.json
```

Primary purpose:

* git provenance,
* configuration fingerprinting,
* reference genome provenance,
* execution-profile telemetry.

---

## 3. config_snapshot.yaml (optional contextual support)

Canonical path:

```text
results/<run_id>/metadata/config_snapshot.yaml
```

This file is not expected to serve as a primary aggregation substrate, but may assist future schema expansion or provenance debugging.

---

# Canonical Output Artifact

The implementation will generate:

```text
provenance_summary.new.tsv
```

The file will contain ONLY the 13 newer runs.

The implementation must NOT:

* merge historical rows,
* overwrite May 22 artifacts,
* or emit duplicate provenance rows.

---

# Canonical Output Schema

The implementation must preserve the historical column ordering exactly:

```text
sample_id
run_id
assay_type
run_classification
assay_metadata_status
run_notes
pipeline_version
status
machine_id
config_path
git_commit
config_hash
reference_genome
reference_fasta_hash_or_size
execution_profile
```

Schema drift is prohibited.

Column ordering is considered governance-significant.

---

# Provenance Mapping Strategy

## sample_id

Source:

* manifest-driven cohort mapping

Special case:

```text
SRR12898354 → HG002
```

---

## run_id

Source:

```text
run_metadata.json
```

---

## assay_type

Recommended mapping:

| Cohort      | assay_type |
| ----------- | ---------- |
| WES cohorts | WES        |
| HG002       | WGS        |

---

## run_classification

Recommended mapping:

| Cohort        | run_classification |
| ------------- | ------------------ |
| q1 cohort     | q1                 |
| median cohort | median             |
| q3 cohort     | q3                 |
| HG002         | benchmark_wgs      |

This preserves:

* assay semantics,
* cohort semantics,
* and benchmark semantics independently.

---

## assay_metadata_status

Recommended deterministic value:

```text
available
```

---

## run_notes

Recommended descriptive values:

Examples:

```text
epilepsy_wes_cross_run_cohort
hg002_wgs_benchmark
```

The implementation should remain deterministic and concise.

---

## pipeline_version

Preferred source priority:

1. run_metadata.json
2. run_fingerprint.json

---

## status

Source:

```text
run_metadata.json
```

Expected canonical value:

```text
completed
```

---

## machine_id

Source:

```text
run_metadata.json
```

---

## config_path

Source:

```text
run_metadata.json
```

---

## git_commit

Source:

```text
run_fingerprint.json
```

---

## config_hash

Source:

```text
run_fingerprint.json
```

---

## reference_genome

Source:

```text
run_fingerprint.json
```

Expected canonical value:

```text
GRCh38
```

---

## reference_fasta_hash_or_size

Source:

```text
run_fingerprint.json
```

---

## execution_profile

Source:

```text
run_fingerprint.json
```

---

# Validation Requirements

The implementation should validate:

## 1. Row cardinality

Expected:

```text
13 rows
```

---

## 2. Unique run_id constraint

Each:

```text
run_id
```

must appear exactly once.

---

## 3. Schema stability

Output columns must exactly match the historical May 22 artifact.

---

## 4. Missing provenance detection

The implementation should fail loudly if required provenance fields are absent.

Silent provenance degradation is prohibited.

---

# Filesystem Governance

The implementation must act as:

```text
read-only provenance aggregation infrastructure
```

The implementation must NOT:

* mutate run metadata,
* modify original telemetry,
* or overwrite historical provenance artifacts.

---

# Recommended Script Location

Recommended implementation path:

```text
scripts/analysis/build_provenance_summary.py
```

---

# Recommended Output Path

Recommended output location:

```text
docs/case_studies/cross_runs/cross_run_tables/provenance_summary.new.tsv
```

---

# Recommended CLI Defaults

The script should support the following defaults when executed from the VAP repository root:

```text
--results-dir results
--out docs/case_studies/cross_runs/cross_run_tables/provenance_summary.new.tsv
```

Expected invocation:

```text
python scripts/analysis/build_provenance_summary.py
```

The script should permit alternate results directories to support:

* MARK-side execution
* sys76 lightweight artifact execution
* future archived run rehydration workflows

---

# Future Extensibility

This implementation should establish a reusable aggregation pattern for remaining stale telemetry updates including:

* run_reproducibility_summary.tsv
* clinical_status_summary.tsv
* variant_consequence_summary.tsv
* coding_noncoding_consequence_summary.tsv

Implementation architecture should therefore favor:

* manifest-driven iteration,
* reusable schema validation,
* deterministic provenance extraction,
* and governance-aware aggregation behavior.

---

# Governance Alignment

This implementation aligns with broader VAP cross-run governance principles emphasizing:

* provenance preservation,
* append-only telemetry,
* deterministic infrastructure observability,
* artifact isomorphism,
* and reconstructable synthesis substrate generation.

The provenance layer therefore functions as:

```text
cross-run execution identity infrastructure
```

within the broader horizontal synthesis ecosystem.
