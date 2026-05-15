# docs/status/phase1_operational_findings.md

# Phase 1 Operational Findings

## MARK1 Infrastructure and Execution Observations

**Repository:** variant_annotation_pipeline  
**Branch:** `phase0-logging-foundation`  

**Phase:** Phase 1A  
**Status:** ACTIVE OPERATIONAL CHARACTERIZATION

---

## Related Documents

- `docs/status/phase1_runtime_baseline_status.md`
- `docs/status/phase1_reproducibility_assessment.md`
- `docs/status/phase1_operational_findings.md`

---

# Purpose

This document tracks operational lessons, infrastructure observations, execution workflows, and systems-engineering findings that emerged during Phase 1A production execution on MARK1.

The goal is to preserve operational knowledge separately from:

- runtime telemetry interpretation
- reproducibility assessment
- scientific execution outcomes

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

---

### `tmux` Operational Adoption

This workflow introduces persistent detached execution management for long-running VAP production workloads.

Phase 1A represents the first formal adoption of:

`tmux`

for long-running VAP production execution.

This marks an important operational maturity milestone for the repository.

---

## Operational Maturity Milestones

Phase 1A introduced several operational maturity improvements:

- detached execution management via tmux
- MARK-class production execution
- telemetry harvesting
- runtime profiling
- assay-aware provenance correction
- same-sample rerun reproducibility assessment
- production-grade run fingerprinting
- structured metadata artifact generation

---

## Current Known Limitations

Current known limitations identified during Phase 1A include:

- residual HG002 assumptions remain in portions of the codebase
- assay type reporting currently defaults to WGS
- manifest-driven cohort execution has not yet been implemented
- multi-node orchestration is not yet implemented
- telemetry-driven optimization has not yet been performed
- runtime economics remain influenced by virtualized MARK infrastructure
- byte-identical artifact reproducibility has not yet been formally evaluated

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
- reran ERR10619281 after metadata refinements to assess metadata-transition reproducibility behavior

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

## Current Unknowns

The following questions remain under active investigation:

- cross-node reproducibility (MARK1 vs MARK2/3)
- WGS reproducibility stability
- long-term cache effects
- filesystem I/O scaling behavior
- interval-sharded GATK behavior
- high-fork VEP scaling
- manifest-driven parallel orchestration behavior

---

## Operational Outlook

Phase 1A demonstrates that VAP has progressed beyond:

- single-run execution
- HG002-only operational assumptions
- minimally instrumented pipeline behavior

and is now transitioning toward:

- cohort-aware execution
- reproducibility-oriented telemetry collection
- operational observability
- infrastructure-aware scaling strategy
- reusable runtime comparison tooling
- production-style execution workflows

---