# Workflow Specification  
## variant_annotation_pipeline v1.0  
## docs/implementation/workflow.md

---

## 1. Purpose

This document defines the **end-to-end execution workflow** of  
`variant_annotation_pipeline` v1.0.

It describes:

- stage ordering
- data flow between stages
- state transitions
- artifact generation
- execution control behavior

This document is implementation-facing and governs how:

```text
run_pipeline.py + pipeline_runner.py + stage modules
```

work together.

---

## 2. Governing Principle

```text
Pipeline execution is a deterministic, stage-ordered transformation of state.
```

Each stage:

- reads from `state`
- performs a transformation
- writes back to `state`
- records outputs and QC
- does not mutate unrelated sections

---

## 3. High-Level Pipeline Flow

```text
FASTQ → BAM → VCF → annotation → prioritization → validation → summary
```

Expanded:

```text
Stage 01: Load Data
Stage 02: Align Reads
Stage 03: Process BAM
Stage 04: QC Aligned Reads
Stage 05: Call Variants
Stage 06: Normalize VCF
Stage 07: Annotate Variants
Stage 08: Filter and Partition
Stage 09: Interpret Coding Variants
Stage 10: Interpret Non-Coding Variants
Stage 11: Prioritize Variants
Stage 12: Validate Variants
Stage 13: Write Summary
```

---

## 4. Stage Execution Order

Stages must execute strictly in the following order:

```python
STAGE_ORDER = [
    "stage_01_load_data",
    "stage_02_align_data",
    "stage_03_process_bam",
    "stage_04_qc_aligned_reads",
    "stage_05_call_variants",
    "stage_06_normalize_vcf",
    "stage_07_annotate_variants",
    "stage_08_filter_and_partition",
    "stage_09_interpret_coding",
    "stage_10_interpret_noncoding",
    "stage_11_prioritize_variants",
    "stage_12_validate_variants",
    "stage_13_write_summary",
]
```

No dynamic reordering is allowed in v1.

---

## 5. Stage Interface Contract

Each stage must implement:

```python
def run_stage(config: dict, paths: dict, logger, state: dict) -> dict:
    return state
```

### Inputs

- `config` → parsed YAML config
- `paths` → resolved run directory paths
- `logger` → structured logger
- `state` → current pipeline state

### Output

- updated `state`

---

## 6. Pipeline Runner Responsibilities

`pipeline_runner.py` is responsible for:

1. loading config
2. initializing `state`
3. generating `run_id`
4. creating output directories
5. initializing logging
6. executing stages in order
7. handling failures
8. writing metadata
9. finalizing run status

---

## 7. Run Lifecycle

### 7.1 Initialization

```text
- load config
- generate run_id
- create results/<run_id>/
- initialize logger
- initialize state["run"]
```

---

### 7.2 Execution

For each stage:

```text
- log stage start
- execute stage.run_stage()
- update state
- record stage_outputs
- log completion
```

---

### 7.3 Failure Handling

If a stage raises an exception:

```text
- log error
- record in state["errors"]
- mark run status as "failed"
- write metadata.json
- stop execution
```

---

### 7.4 Completion

If all stages succeed:

```text
- set run status = "completed"
- write metadata.json
- finalize logs
```

---

## 8. State Flow Model

```text
state (Stage N) → transform → state (Stage N+1)
```

Each stage:

- must not delete prior state sections
- may append or update relevant fields
- must record its outputs in:
  - `state["artifacts"]`
  - `state["qc"]`
  - `state["stage_outputs"]`

---

## 9. Artifact Flow

Artifacts are written progressively:

| Stage | Artifact |
|------|--------|
| 02 | aligned BAM |
| 03 | sorted BAM + index |
| 04 | QC report |
| 05 | raw VCF |
| 06 | normalized VCF |
| 07 | annotated VCF + TSV |
| 08 | filtered + partitioned tables |
| 09 | interpreted coding table |
| 10 | interpreted noncoding table |
| 11 | prioritized table + gene summary |
| 12 | validation notes + IGV candidates |
| 13 | run summary report |

---

## 10. Directory Structure

Each run produces:

```text
results/<run_id>/
├── logs/
│   └── pipeline.log
├── interim/
├── processed/
├── reports/
├── metadata.json
```

### Directory usage

- `interim/` → intermediate files (BAM, raw VCF)
- `processed/` → final tables (annotated, prioritized)
- `reports/` → human-readable outputs
- `logs/` → execution logs

---

## 11. Logging Workflow

Each stage must:

```text
- log start
- log key metrics
- log output paths
- log completion
```

The pipeline runner must:

```text
- initialize logger
- write log file to results/<run_id>/logs/pipeline.log
```

---

## 12. Metadata Output

At the end of the run:

```text
results/<run_id>/metadata.json
```

This must include:

- run metadata (`state["run"]`)
- sample metadata (`state["sample"]`)
- artifact paths
- stage outputs
- QC summaries
- warnings and errors

---

## 13. Determinism Requirements

Pipeline execution must be:

```text
deterministic
```

Meaning:

- same inputs + same config → same outputs
- stage order is fixed
- all parameters come from config
- all outputs are recorded in state

---

## 14. Execution Modes

### v1 Supported Mode

```text
full_pipeline
```

### Future Mode (not required)

```text
annotation_only
```

Pipeline runner should:

- read mode from config
- allow stage logic to branch internally if needed
- not skip stages globally in v1

---

## 15. Extension Points

The workflow must support future additions without breaking v1:

- additional annotation stages
- AI-based scoring (future)
- cohort aggregation (future)
- distributed execution (future)

### Design rule

```text
new stages must append, not rewrite existing flow
```

---

## 16. Failure Isolation

Failures must:

- stop execution immediately
- preserve prior outputs
- not corrupt state
- be recorded in:
  - `state["errors"]`
  - logs

---

## 17. Summary Rule

```text
Pipeline execution is a linear, state-driven sequence of transformations that produces a fully reproducible, self-contained run directory.
```

---

# End of Workflow Specification