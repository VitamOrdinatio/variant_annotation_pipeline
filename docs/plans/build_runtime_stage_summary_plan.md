# build_runtime_stage_summary_plan.md

# Purpose

This document defines the implementation plan for generating:

```text
runtime_stage_summary.new.tsv
```

for the post–May 22 VAP cohort expansion runs.

This artifact functions as an:

```text
append-ready runtime telemetry substrate
```

rather than a replacement for the original deterministic baseline artifact.

The goal is to preserve:

* historical reproducibility telemetry,
* append-only governance,
* provenance continuity,
* and deterministic cohort-scale runtime observability structure.

---

# Scope

This implementation specifically updates the cross-run comparative telemetry layer for:

```text
runtime_stage_summary.tsv
```

located at:

```text
docs/case_studies/cross_runs/cross_run_tables/
```

This plan applies ONLY to:

* the 13 newer VAP executions completed after the original May 22 deterministic reproducibility study,
* and generation of append-ready runtime telemetry rows.

This implementation does NOT:

* overwrite historical telemetry,
* mutate original May 22 outputs,
* or regenerate the original deterministic comparison cohort.

---

# Historical Context

The original May 22 runtime telemetry artifact summarized:

* repeated deterministic VAP executions,
* across a smaller cohort,
* intended to evaluate reproducibility stability.

Those runs demonstrated:

```text
biological-output agreement across repeated executions
```

despite non-identical filesystem byte structure.

Following that study, 13 additional VAP executions were completed:

* 12 epilepsy WES runs
* 1 HG002 WGS run

The goal of this implementation is therefore:

```text
incremental telemetry extension
```

rather than:

```text
historical telemetry replacement.
```

---

# Canonical Input Manifest

The implementation will iterate over an explicit cohort manifest containing:

| SRA | run_id | depth_category |
| --- | ------ | -------------- |

Canonical cohort composition:

* 4 q1 WES runs
* 4 median WES runs
* 4 q3 WES runs
* 1 HG002 WGS run

Total:

```text
13 run_<id> executions
```

## Explicit Cohort Manifest

| SRA           | run_<id>                | Depth Category | 
| --------------| ----------------------- | -------------- |
| `ERR10619203` | `run_2026_05_30_071639` | q3             |
| `ERR10619207` | `run_2026_06_01_124134` | q3             | 
| `ERR10619208` | `run_2026_05_30_151355` | median         |
| `ERR10619212` | `run_2026_05_30_214724` | q1             |
| `ERR10619225` | `run_2026_05_31_091242` | q3             | 
| `ERR10619230` | `run_2026_06_01_004903` | q3             | 
| `ERR10619241` | `run_2026_06_02_052302` | q1             | 
| `ERR10619281` | `run_2026_05_27_233524` | median         |
| `ERR10619285` | `run_2026_06_02_124300` | median         | 
| `ERR10619300` | `run_2026_05_27_172531` | median         |
| `ERR10619309` | `run_2026_06_02_181024` | q1             | 
| `ERR10619330` | `run_2026_06_01_203130` | q1             | 
| `SRR12898354` | `run_2026_06_03_010030` | hg002          | 

Note that for SRA `SRR12898354`, `hg002` is interchangeable.

---

# Canonical Input Artifact

For each run:

```text
results/<run_id>/metadata/stage_resource_snapshots.tsv
```

will be used as the canonical telemetry substrate.

This file contains:

* stage identifiers,
* start/end timestamps,
* and resource snapshot telemetry.

---

# Canonical Output Artifact

The implementation will generate:

```text
runtime_stage_summary.new.tsv
```

The file will contain ONLY the 13 newer runs.

It will NOT contain:

* historical May 22 runs,
* duplicate rows,
* or merged telemetry.

Future concatenation/appending may occur downstream.

---

# Canonical Output Schema

The output schema must exactly preserve the historical schema ordering:

```text
sample_id
run_id
stage
elapsed_seconds
status
start_time
end_time
```

Schema drift is not permitted.

Column ordering is considered governance-significant.

---

# Stage Aggregation Logic

Each stage within:

```text
stage_resource_snapshots.tsv
```

contains two canonical telemetry events:

| phase | meaning         |
| ----- | --------------- |
| start | stage entered   |
| end   | stage completed |

The implementation will:

1. identify matching start/end rows per stage,
2. extract timestamps,
3. compute elapsed runtime,
4. generate a single summary row per stage.

Expected output cardinality:

```text
13 stages × 13 runs = 169 rows
```

assuming complete telemetry coverage.

---

# Timestamp Handling

Timestamp parsing should use:

```python
pd.to_datetime(..., utc=True)
```

to ensure:

* timezone stability,
* deterministic runtime calculation,
* and cross-run consistency.

Elapsed runtime should be emitted as:

```text
elapsed_seconds
```

using numeric second-resolution duration.

---

# Status Rules

Recommended deterministic status behavior:

| Condition              | status     |
| ---------------------- | ---------- |
| both start/end present | success    |
| missing end            | incomplete |
| missing start          | incomplete |
| duplicated transitions | ambiguous  |

The implementation should fail loudly on ambiguous stage topology.

Silent corruption is prohibited.

---

# Missing Data Policy

The implementation should preserve observability transparency.

If a run:

* lacks telemetry,
* contains malformed stage transitions,
* or contains missing stages,

the script should:

1. emit explicit console warnings,
2. record the affected run/stage,
3. continue processing remaining runs where possible.

Operational transparency is preferred over silent omission.

---

# Recommended Validation

Validation should confirm:

## 1. Expected stage count

Expected:

```text
13 stages per run
```

## 2. Unique stage cardinality

Each:

```text
(run_id, stage)
```

pair should appear exactly once.

## 3. Schema validation

Output columns must exactly match the historical May 22 artifact.

## 4. Runtime sanity checks

Elapsed runtime should:

* be non-negative,
* and remain operationally plausible.

---

# Filesystem Governance

The implementation must NOT:

* modify historical May 22 TSVs,
* alter original run directories,
* or mutate telemetry substrate files.

The implementation acts strictly as:

```text
read-only telemetry aggregation infrastructure.
```

---

# Recommended Script Location

Recommended implementation location:

```text
scripts/cross_run/build_runtime_stage_summary.py
```

---

# Recommended Output Location

Recommended output path:

```text
docs/case_studies/cross_runs/cross_run_tables/runtime_stage_summary.new.tsv
```

---

# Future Extensibility

This implementation should establish a reusable pattern for remaining stale telemetry updates, including:

* provenance_summary.tsv
* run_reproducibility_summary.tsv
* clinical_status_summary.tsv
* variant_consequence_summary.tsv
* coding_noncoding_consequence_summary.tsv

Accordingly, implementation architecture should favor:

* deterministic aggregation,
* manifest-driven execution,
* reusable validation helpers,
* and explicit schema governance.

---

# Governance Alignment

This implementation aligns with broader VAP cross-run governance principles emphasizing:

* append-only comparative telemetry,
* provenance preservation,
* deterministic observability,
* artifact isomorphism,
* and reconstructable semantic infrastructure.

The implementation therefore functions as:

```text
horizontal runtime observability infrastructure
```

within the broader cross-run synthesis ecosystem.
