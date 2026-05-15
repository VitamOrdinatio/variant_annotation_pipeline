# Phase 1 Runtime Baseline Status
## MARK1 HG002 Instrumented Baseline Rerun

**Repository:** variant_annotation_pipeline  
**Branch:** `phase0-logging-foundation`  

**Phase:** Phase 1A  
**Status:** PHASE 1A HG002 COMPLETE — WES EXTENSION ACTIVE

**Date Started:** 2026-05-13  
**Hardware:** MARK1 (`VandPyMolGPUResearch`)  

---

# Purpose

This document tracks the live operational status and strategic interpretation of the Phase 1A instrumented HG002 rerun on MARK1.

The primary goal of this rerun is NOT merely to rerun HG002, but rather to establish the first fully instrumented runtime baseline for VAP under production-scale execution conditions.

This run serves as:

- a runtime profiling baseline
- a telemetry validation run
- an observability validation run
- a reproducibility checkpoint
- a scaling economics assessment
- a future optimization reference point

---

# Background

A prior HG002 VAP run on MARK1 completed successfully in approximately:

```text
~36 hours
```

However, the original run lacked sufficient operational observability:

- no populated canonical logs
- no runtime profile
- no stage timing breakdown
- no stage resource telemetry
- incomplete provenance instrumentation

As a result, optimization opportunities could not be evaluated rigorously.

Phase 0 addressed this limitation by introducing:

- canonical run logging
- runtime profiling
- stage summaries
- run fingerprints
- deterministic metadata emission
- regression testing
- lightweight fixture execution
- stage resource telemetry
- operational execution harnesses

Phase 1A now applies those systems to a real HG002 production rerun.

The Phase 1A HG002 rerun completed successfully with an observed runtime of approximately:

```text
~22 h 44 m
```

This materially revised the earlier approximate:

```text
~36 h
```

historical runtime estimate.

Primary observed runtime bottlenecks were:

- Stage 05 — Variant Calling
- Stage 02 — Alignment

Critically:

```text
VEP annotation was NOT the dominant runtime bottleneck.
```

---

## Current Execution Context

### Active Execution Harness

`scripts/mark/mark_run_phase1a_hg002_baseline.sh`

### Active Configuration

`config/config.mark.baseline.yaml`

This rerun intentionally preserves near-original runtime settings in order to establish a trustworthy pre-optimization baseline.

### Execution Mode

`full_pipeline`

### Current Operational Workflow

Execution is being managed via:

`tmux`

Session:

`vap_phase1a`

This provides:

- detached long-running execution safety
- session persistence
- reconnection capability
- operational resilience against browser disconnects

---

## Early Runtime Observations

### Stage 02 Alignment

Observed:

`bwa mem`

actively aligning reads into:

`results/run_<run_id>/interim/*.aligned.sam`

This confirms:

- Stage 02 is functioning correctly
- write paths are healthy
- interim artifact emission is active
- large-scale alignment execution is progressing


### CPU Utilization Observation

Observed CPU utilization:

`~1440% CPU`

on a 40-core MARK node.

Approximate interpretation:

`~14–15 logical cores worth of compute activity observed during alignment.`

This observation is operationally important because it suggests:

- the pipeline is capable of meaningful parallelism
- BWA alignment is not purely single-threaded
- actual runtime behavior may differ from simplistic thread-count assumptions

However, this does NOT yet imply the overall pipeline is near-optimal.

---

# Runtime Telemetry Tracking

Telemetry observations are currently being collected prior to deliberate optimization efforts in order to preserve trustworthy pre-optimization runtime baselines.

| Input Dataset | Assay Type | MARK Node | VAP Version | Runtime | Status | Notes |
|---|---|---|---|---|---|---|
| HG002 | WGS | MARK1 | v1 | ~22 h 44 m | Success | Instrumented production rerun |
| ERR10619281 (pre-provenance patch) | WES* | MARK1 | v1 | ~5 h 04 m | Success | First Saudi epilepsy cohort baseline; completed before assay-type provenance patch; runtime valid, metadata partially superseded |
| ERR10619300 (post-provenance patch) | WES | MARK1 | v1 | ~4 h 56 m | Success | Saudi epilepsy cohort baseline; run_id `run_2026_05_14_164444`; 736,468 prioritized rows |
| ERR10619281 (post-provenance patch) | WES        | MARK1     | v1          | ~4 h 56 m 30 s | Success | Provenance-corrected rerun completed successfully; run_id `run_2026_05_14_231247`; FASTQ pair counts stable at 83,696,516 reads each; Stage 11/12 rows stable at 811,554; reproducibility comparison candidate established |

**Notes:**
- ERR10619300 completed successfully after the assay-type provenance patch. This run therefore represents the first Saudi WES baseline with corrected WES-aware metadata/provenance behavior.

- ERR10619281 also completed successfully before the assay-type provenance patch. That first run remains valid as a runtime baseline, but its metadata should be treated as partially superseded for assay-type provenance. A provenance-corrected ERR10619281 rerun is now in progress to support same-sample reproducibility comparison.

---

## Initial Replication Insights

| Dataset     | Run Context                 | FASTQ Pair Counts       | Stage 11/12 Stable Rows |
| ----------- | --------------------------- | ----------------------- | ----------------------- |
| ERR10619281 | pre-provenance patch        | 83,696,516 / 83,696,516 | 811,554                 |
| ERR10619281 | post-provenance patch rerun | 83,696,516 / 83,696,516 | 811,554                 |
| ERR10619300 | post-provenance patch       | 83,673,287 / 83,673,287 | 736,468                 |

> Deterministic output established for both ERR10619281 VAP runs.

---

## Emerging Strategic Consideration

An important realization during Phase 1A is that the prior:

`~36 hour HG002 runtime`

may already represent partially optimized real-world execution behavior.

This possibility must be evaluated carefully.

At present, there are two possible outcomes:

### Scenario A — Significant Optimization Headroom Exists

Possible if telemetry reveals:

- underutilized cores
- VEP bottlenecks
- I/O inefficiencies
- suboptimal thread/fork settings
- memory constraints
- serialization bottlenecks

In this scenario:

- Phase 1 optimization proceeds aggressively
- runtime reduction efforts continue
- high-core MARK profiles are developed further

### Scenario B — Runtime Is Already Near Practical Limits

Possible if telemetry reveals:

- sustained high resource utilization
- strong parallel efficiency
- limited remaining bottleneck opportunities
- acceptable scaling behavior

In this scenario, strategic emphasis may shift toward:

- freezing VAP v1 earlier
- transitioning to manifest-driven execution
- scaling horizontally via MARK2/MARK3
- prioritizing cohort execution over further optimization

---

## Scaling Implications

Future execution goals include approximately:

`~144 epilepsy-related SRAs`

including:

`ERR10619281`
`ERR10619300`

If WGS-scale runtime remains near:

`~22–23 hours/SRA`

then horizontal scaling infrastructure becomes strategically important for large WGS cohort execution.

However, early Saudi epilepsy WES telemetry suggests substantially improved runtime economics:

`~5 hours/SRA`

This materially improves the feasibility of large-scale epilepsy cohort processing on MARK-class infrastructure.

This includes:

- MARK2 allocation
- MARK3 allocation
- parallel manifest-driven orchestration
- execution scheduling strategy

Phase 1A therefore informs not only optimization strategy, but also infrastructure allocation strategy.

---

## Determinism Consideration

Phase 1A also functions as a reproducibility checkpoint.

Because this rerun uses:

- same machine
- same dataset
- same general configuration class

the resulting outputs should remain biologically and structurally stable.

Expected stable outputs include:

- variant counts
- Stage 08–13 row counts
- prioritized variant structure
- validation candidate structure
- stage summary metrics
- artifact manifests

Expected variable outputs include:

- run IDs
- timestamps
- runtime profiles
- telemetry snapshots
- absolute paths

This rerun therefore also evaluates VAP determinism under repeated production execution.

---

## Operational Lessons Already Observed

### Multi-Repo VENV Ambiguity

An important operational issue was identified during execution setup:

Multiple repositories using:

`.venv/`

can create ambiguous shell prompts.

Observed issue:

`(.venv)`

alone was insufficient to determine which repository environment was active.

Correct validation methods include:

```bash
which python
echo $VIRTUAL_ENV
```

This operational lesson is important for future multi-repo workflow management.

### `tmux` Operational Adoption

This workflow introduces persistent detached execution management for long-running VAP production workloads.

Phase 1A represents the first formal adoption of:

`tmux`

for long-running VAP production execution.

This marks an important operational maturity milestone for the repository.

---

## Current Status

### Phase 1A HG002 Baseline

`COMPLETE`

### Phase 1A WES Extension

`ACTIVE`

Current active execution focus:

- Saudi epilepsy cohort baseline characterization
- WES runtime telemetry collection
- cohort reproducibility assessment
- metadata model refinement
- assay-type-aware provenance correction and same-sample WES rerun validation

---

## Next Expected Deliverables

Upon run completion:

```text
metadata/runtime_profile.tsv
metadata/stage_resource_snapshots.tsv
metadata/run_metadata.json
metadata/run_fingerprint.json
metadata/stage_summaries/
```

These artifacts will drive:

- bottleneck analysis
- optimization planning
- scaling strategy decisions
- future MARK2/MARK3 allocation rationale

---

## Current Known Limitations

Current known limitations identified during Phase 1A include:

- residual HG002 assumptions remain in portions of the codebase
- assay type reporting currently defaults to WGS
- manifest-driven cohort execution has not yet been implemented
- multi-node orchestration is not yet implemented
- telemetry-driven optimization has not yet been performed
- runtime economics remain influenced by virtualized MARK infrastructure

These limitations are now being addressed incrementally as VAP transitions from HG002-centric validation toward generalized cohort-scale execution.

---

## Phase 1A Follow-Up Decisions

Successful execution of the first Saudi epilepsy WES sample revealed that VAP has now progressed beyond HG002-only operational assumptions.

As a result, the following strategic decisions were made:

- retain HG002 locking behavior as the default v1 safety model
- formalize controlled non-HG002 execution using:
  - `execution_profile.allow_non_hg002=true`
- transition assay type reporting toward config-driven provenance
- execute additional WES telemetry baselines before optimization efforts
- rerun ERR10619281 after metadata refinements to assess reproducibility behavior

This strategy preserves:

- reproducibility safeguards
- provenance clarity
- operational stability

while enabling:

- cohort-scale execution
- generalized sample processing
- future manifest-driven orchestration
- downstream RDGP/GSC/VDB integration

---

## Immediate Implementation Boundary

Before additional Saudi WES baseline runs, VAP will receive only minimal provenance-correctness updates.

Allowed near-term changes:

- make `input.assay_type` config-driven
- propagate assay type into Stage 01 sample state
- ensure WES configs report `assay_type: WES`
- preserve `execution_profile.allow_non_hg002=true` as the explicit controlled bypass for non-HG002 execution
- add only narrowly scoped tests needed to protect assay-type provenance behavior

Deferred until after telemetry collection:

- runtime optimization
- thread/fork tuning
- Java/GATK tuning
- manifest-driven cohort execution
- multi-node orchestration
- broad refactoring
- downstream interpretation redesign
- AlphaGenome integration

Rationale:

The immediate priority is to collect trustworthy baseline telemetry for Saudi WES samples while preventing metadata/provenance violations. Broader VAP optimization should wait until HG002 and Saudi WES telemetry have been collected and compared.

---

## Preliminary Assessment

Phase 1A has already validated several important operational advances:

- MARK operational harness functionality
- tmux-managed execution
- telemetry emission
- provenance infrastructure
- deterministic fixture preflight execution
- real-time runtime observation workflows

Ongoing telemetry analysis will help determine whether future effort should prioritize:

`vertical optimization`

or:

`horizontal execution scaling`

for large-scale epilepsy cohort processing.