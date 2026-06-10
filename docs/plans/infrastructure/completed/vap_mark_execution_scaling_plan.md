# VAP MARK Optimization and Replication Strategy
## variant_annotation_pipeline (VAP)
## MARK Execution Scaling Plan
## Version: Draft v1.0

---

## Purpose

This document formalizes the phased execution strategy for:

1. Optimizing VAP runtime performance on MARK-class systems
2. Preserving deterministic and reproducible pipeline behavior
3. Preparing VAP for large-scale cohort execution
4. Supporting future distributed execution across MARK1, MARK2, and MARK3
5. Enabling efficient processing of epilepsy-focused SRA cohorts

This is a systems-engineering and execution-planning document.

It is NOT:
- a system contract
- a scientific manuscript
- an implementation spec
- a scheduler design
- a distributed orchestration framework

---

## Strategic Context

Current state:

- VAP v1 successfully completed HG002 on MARK1
- End-to-end runtime:
  - ~36 hours total
- Approximate runtime through Stage 08:
  - ~28 hours
- MARK hardware:
  - 40 CPU cores available
- Current VAP execution profile:
  - approximately 8 cores utilized

Future planned execution scope:

- 144 epilepsy-manifestation-linked SRAs
- Additional downstream:
  - GSC overlays
  - VDB ingestion
  - RDGP-compatible aggregation

This execution scale makes runtime optimization a strategic necessity.

---

## Governing Principles

### 1. Correctness before speed

Performance optimization must NEVER:
- break determinism
- alter schema contracts
- silently modify outputs
- weaken provenance tracking
- bypass validation logic

---

### 2. HG002 remains the calibration benchmark

HG002 is the canonical:
- runtime benchmark
- determinism benchmark
- schema validation benchmark
- QC calibration benchmark

All optimization passes must first validate against HG002.

---

### 3. Stage-aware optimization

Optimization must occur:
- per stage
- per bottleneck
- per resource type

NOT through indiscriminate thread inflation.

---

### 4. Deterministic reproducibility is mandatory

Optimized runs must preserve:
- output schemas
- row counts
- prioritization distributions
- validation candidate distributions
- summary statistics
- artifact manifests
- contract-level invariants
- stable sorting policy
- stable TSV row ordering
- stable JSON serialization

---

## High-Level Execution Plan

The optimization and scaling strategy consists of six phases (P0 to P5).

---

### Phase 0 — Logging, Provenance, and Test Foundation

Before benchmarking, define a clean logging model:

```text
results/<run_id>/
├── logs/
│   ├── pipeline.log
│   ├── stage_01.log
│   ├── stage_02.log
│   ├── ...
│   └── runtime_profile.tsv
├── metadata/
│   ├── run_metadata.json
│   ├── tool_versions.json
│   ├── config_snapshot.yaml
|   ├── run_fingerprint.json
│   └── input_manifest.json
```

Each stage should log:

```text
stage_name
stage_number
start_time
end_time
elapsed_seconds
input_artifacts
output_artifacts
tool_commands
tool_versions
thread_count
memory/temp settings
status
warnings
errors
```

The logging system should support three levels:

```text
1. pipeline-level log        = end-to-end story
2. stage-level logs          = debugging and timing
3. structured metadata files = reproducibility/provenance
```

MARK probe logs are useful operational wrappers, but the authoritative provenance should live inside the run directory. 

MARK probe logs are retrieval/debug artifacts, not the permanent system of record.

The first VAP test suite should not try to test full HG002 execution. It should test the contracts and utilities:

```text
tests/
├── test_logging_contract.py
├── test_run_fingerprint.py
├── test_stage_summary_json.py
├── test_config_snapshot.py
├── test_runtime_profile_schema.py
├── test_stage08_schema_contract.py
├── test_variant_id_determinism.py
├── test_missing_value_semantics.py
├── test_stable_json_serialization.py
└── test_output_manifest_contract.py
```

#### Phase 0 Deliverables

1. VAP-native logging scaffold
2. structured metadata artifacts
3. run_fingerprint.json
4. per-stage summary JSONs
5. runtime_profile.tsv
6. pytest suite for logging/provenance/schema contracts
7. small fixture dataset for fast tests
8. CI-ready local test command, e.g. pytest -q

---

### Phase 1 — Benchmarking and Runtime Instrumentation

#### Objective

Establish a precise understanding of:
- stage-level wall times
- CPU utilization
- memory utilization
- I/O bottlenecks
- tool-specific scaling limitations

before modifying execution behavior.

---

#### Rationale

Blind optimization risks:
- unstable performance
- nondeterministic behavior
- inefficient CPU oversubscription
- I/O thrashing
- debugging complexity

Profiling must precede tuning.

---

### Phase 1 Deliverables

#### 1. Run Provenance Fingerprint

Example:

`results/<run_id>/metadata/run_fingerprint.json`

Containing:

- pipeline git commit hash
- config hash
- reference genome checksum
- tool versions
- environment snapshot
- hostname
- execution profile name

This becomes critical once MARK2 and MARK3 exist for provenance and deterministic output validation.

---

#### 2. Stage-level timing instrumentation

All stages should emit:
- start timestamp
- stop timestamp
- elapsed wall time

Example:

```text
[STAGE START] Stage 07
[STAGE END] Stage 07
[ELAPSED] 07:13:22
```

---

#### 3. Resource utilization capture

Capture:

- CPU usage
- memory usage
- thread counts
- disk utilization
- temp directory growth

where feasible.

---

#### 4. Timing summary artifact

**Potential summary artifact:**

`results/<run_id>/reports/runtime_profile.tsv`

Example columns:

| stage    | wall_time | cpu_percent | max_memory_gb |
| -------- | --------- | ----------- | ------------- |
| stage_05 | 08:12:11  | 730%        | 42            |
| stage_07 | 11:02:54  | 620%        | 28            |

**Potential JSON artifact:**

Emit: 

`results/<run_id>/metadata/stage_07_summary.json`

for every stage.

Example: 

```JSON
{
  "stage": "stage_07",
  "status": "completed",
  "start_time": "...",
  "end_time": "...",
  "elapsed_seconds": 41222,
  "threads": 16,
  "input_artifacts": [...],
  "output_artifacts": [...],
  "warning_count": 14,
  "error_count": 0
}
```

Reason:

- future dashboards
- easier aggregation
- easier automated validation
- easier restart logic
- easier distributed orchestration later

This becomes very important for future manifest-driven execution.

---

#### 5. Identify dominant bottlenecks

Likely heavy stages:

- alignment
- BAM sorting
- variant calling
- VEP annotation
- large TSV processing

---

#### Success Criteria

- Explicit run fingerprint exists
- Stage-level runtime map exists
- Dominant bottlenecks identified
- Resource saturation patterns understood
- Optimization targets prioritized

---

### Phase 2 — MARK Execution Profile Design

#### Objective

Create a MARK-optimized execution profile that safely leverages high-core hardware.

---

#### Rationale

Current VAP execution underutilizes MARK resources.

However:

- some tools scale poorly
- excessive threading can increase I/O contention
- some pipeline stages remain serial
- over-parallelization can reduce stability

A dedicated MARK execution profile is required.

---

#### Proposed Profile

Example conceptual profile:

```yaml
execution_profile:
  name: mark_highcore
  max_threads: 32
  reserve_threads: 8
```

---

#### Potential Configuration Areas

**Alignment**
- BWA thread scaling
- minimap2 scaling
- temp directory placement

**BAM Sorting**
- memory-per-thread tuning
- sort chunk optimization

**Variant Calling**
- thread tuning
- interval sharding evaluation

**VEP Annotation**
- `--fork` optimization
- cache locality optimization
- temp handling

**Python Stages**
- streaming vs full DataFrame loads
- chunked TSV processing

---

#### Phase 2 Deliverables

- MARK high-core profile
- stage-specific thread configuration
- temp directory policy
- resource safety guidelines

---

#### Success Criteria

- MARK profile implemented
- resource usage scales safely
- no contract violations introduced
- no instability introduced

---

### Phase 3 — Stage-by-Stage Optimization

#### Objective

Optimize the highest-cost stages individually.

---

#### Optimization Targets

**3.1 Alignment**

Potential improvements:

- increased thread count
- optimized temp storage
- memory tuning

---

**3.2 BAM Processing**

Potential improvements:

- sort parallelization
- compression tuning
- indexing efficiency

---

**3.3 Variant Calling**

Potential improvements:

- interval parallelization
- caller-specific thread optimization

---

**3.4 VEP Annotation**

Potential improvements:

- optimized `--fork`
- cache optimization
- reduced annotation overhead

Caution:

- VEP may become I/O-bound
- excessive forks may reduce performance

---

**3.5 Python TSV Processing**

Potential improvements:

- streaming parsers
- chunked processing
- reduced memory duplication
- selective pandas usage

---

**3.6 Checkpoint / Resume Hardening**

Heavy stages must:

- support resumability
- avoid recomputation
- validate upstream artifacts before rerun

### Success Criteria

- runtime reduction achieved
- no output divergence
- reproducibility preserved
- checkpoint behavior hardened

---

### Phase 4 — HG002 Revalidation Run on MARK1

#### Objective

Re-run HG002 after optimization and compare against the original benchmark run.

---

#### Rationale

HG002 is the calibration genome and must remain the canonical reproducibility reference.

---

#### Comparison Requirements

Compare:

- output schemas
- row counts
- summary JSONs
- artifact manifests
- validation distributions
- prioritization distributions
- warning profiles
- Stage 13 outputs
- runtime metrics

---

#### Validation Targets

**Deterministic equivalence**

Expected:

- identical or contract-equivalent outputs

---

**Performance improvement**

Target:

- significant reduction from ~36 hours

Exact target TBD after profiling.

---

### Logging Retention Policy

A policy will need to be formalized for how to handle logs for 144 SRAs

Because eventually:

```text
144 SRAs × verbose logs × many stages
```

can become very large and bulky.

A logging retion policy thus should define:

- required retained logs
- optional ephemeral debug logs
- compressed archival behavior

---

#### Success Criteria

- runtime reduced
- schemas preserved
- deterministic behavior preserved
- no biological plausibility drift
- no contract violations

---

### Phase 5 — Cohort Execution Scaling

#### Objective

Transition from benchmark execution to cohort-scale epilepsy SRA processing.

---

#### Immediate Planned Runs

**HG002**
- [x] MARK1 baseline
- [ ] MARK2 replication
- [ ] MARK3 replication

**ERR10619281**
- [ ] MARK1
- [ ] MARK2
- [ ] MARK3

**ERR10619300**
- [ ] MARK1
- [ ] MARK2
- [ ] MARK3

---

### Long-Term Scaling Goal

Execute approximately:

- 144 epilepsy-linked SRAs

using:

- reproducible per-sample runs
- isolated run directories
- future aggregation compatibility

---

### Scaling Philosophy

Future cohort execution should follow:

```text
single-sample deterministic runs
→ aggregation later
→ GSC overlays
→ VDB ingestion
→ RDGP-compatible downstream analysis
```

NOT:

- monolithic multi-sample execution
- shared mutable execution state
- direct cross-sample coupling

---

### Libary Import Policy

- Use standard library for logging, JSON, hashing, paths, subprocess, timestamps.
- Use `pandas` only where it clearly reduces runtime or code fragility for tabular transforms.
- Prefer streaming/chunked processing for multi-GB TSV stages.
- Allow libraries if they produce hours-level savings or major reliability gains.

For performance, `pandas` may help in some mid-sized table operations, but for 1–2.5 GB TSVs it can also become memory-heavy. We will benchmark three modes where relevant:

- `stdlib` csv streaming
- `pandas` chunked read_csv
- possibly `pyarrow`/`polars` later if there is a clear hours-level gain


#### Future-Compatible Directions

Potential future extensions:

- manifest-driven orchestration
- distributed scheduling
- MARK1/MARK2/MARK3 dispatch
- cohort aggregation layers
- interval-sharded execution
- VDB-native ingestion
- GSC-assisted prioritization overlays

These are future directions and are NOT required for current VAP v1 optimization work.

---

### Risks and Failure Modes

#### Technical Risks

- CPU oversubscription
- I/O saturation
- memory exhaustion
- temp storage overflow
- nondeterministic ordering
- scheduler instability
- inconsistent tool behavior under scaling

#### Pipeline Risks

- schema drift
- output divergence
- altered prioritization distributions
- altered validation burden
- silent truncation
- corrupted checkpoints

---

### Non-Goals

This plan does NOT currently include:

- cloud orchestration
- Kubernetes
- distributed databases
- workflow engine migration
- Nextflow/Snakemake rewrite
- GPU acceleration
- AI prioritization redesign
- full cohort aggregation implementation

---

### Bottom Line


> VAP has demonstrated successful end-to-end execution on MARK1.

> VAP needs runtime optimization for faster end-to-end execution.

> VAP needs to be able to replicate SRA / ENA inputs in deterministic fashion.

```text
The next strategic priority is transforming VAP from a proof-of-execution system
into an efficient, scalable, deterministic cohort-processing platform suitable
for large epilepsy-focused SRA analyses.
```

---