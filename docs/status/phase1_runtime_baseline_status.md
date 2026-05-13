# Phase 1 Runtime Baseline Status
## MARK1 HG002 Instrumented Baseline Rerun

**Repository:** variant_annotation_pipeline  
**Branch:** `phase0-logging-foundation`  
**Phase:** Phase 1A  
**Status:** IN PROGRESS  
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

If runtime remains near:

`~36 hours/SRA`

then horizontal scaling infrastructure becomes strategically important.

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

### Phase 1A

`RUNNING`

Current observed stage during drafting:

`Stage 02 — Alignment`

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

## Preliminary Assessment

Phase 1A has already validated several important operational advances:

- MARK operational harness functionality
- tmux-managed execution
- telemetry emission
- provenance infrastructure
- deterministic fixture preflight execution
- real-time runtime observation workflows

The final runtime analysis will determine whether future effort should prioritize:

`vertical optimization`

or:

`horizontal execution scaling`

for large-scale epilepsy cohort processing.