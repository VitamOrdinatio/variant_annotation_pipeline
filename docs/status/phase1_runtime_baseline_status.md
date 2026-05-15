# docs/status/phase1_runtime_baseline_status.md

# Phase 1 Runtime Baseline Status
## MARK1 HG002 Instrumented Baseline Rerun

**Repository:** variant_annotation_pipeline  
**Branch:** `phase0-logging-foundation`  

**Phase:** Phase 1A  
**Status:** PHASE 1A HG002 COMPLETE — WES EXTENSION ACTIVE

**Date Started:** 2026-05-13  
**Hardware:** MARK1 (`VandPyMolGPUResearch`)  

---

## Related Documents

- `docs/status/phase1_runtime_baseline_status.md`
- `docs/status/phase1_reproducibility_assessment.md`
- `docs/status/phase1_operational_findings.md`

---

# Purpose

This document tracks runtime telemetry, execution economics, scaling interpretation, and optimization-oriented observations for Phase 1A VAP production execution on MARK1 infrastructure.

The primary goal is to establish trustworthy pre-optimization runtime baselines prior to deliberate tuning or orchestration expansion.

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
- structured metadata emission
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

---

## Early Bottleneck Findings

Contrary to initial expectations, early telemetry suggests that:

- Stage 05 (variant calling)
- Stage 02 (alignment)

 dominate runtime behavior.

VEP annotation was not observed to be the primary runtime bottleneck during current WES telemetry collection.

This finding may substantially influence future optimization priorities.

---

# Runtime Telemetry Tracking

Telemetry observations are currently being collected prior to deliberate optimization efforts in order to preserve trustworthy pre-optimization runtime baselines.

| Input Dataset | Assay Type | MARK Node | VAP Version | Runtime | Status | Notes |
|---|---|---|---|---|---|---|
| HG002 | WGS | MARK1 | v1 | ~22 h 44 m | Success | Instrumented production rerun |
| ERR10619281 (pre-provenance patch) | WES* | MARK1 | v1 | ~5 h 04 m | Success | First Saudi epilepsy cohort baseline; completed before assay-type provenance patch; runtime valid, metadata partially superseded |
| ERR10619281 (post-provenance patch) | WES | MARK1 | v1 | ~4 h 56 m 30 s | Success | Provenance-corrected rerun completed successfully; run_id `run_2026_05_14_231247`; FASTQ pair counts stable at 83,696,516 reads each; Stage 11/12 rows stable at 811,554; reproducibility comparison candidate established |
| ERR10619300 (post-provenance patch) | WES | MARK1 | v1 | ~4 h 56 m | Success | Saudi epilepsy cohort baseline; run_id `run_2026_05_14_164444`; 736,468 prioritized rows |
| ERR10619300 (same-patch rerun) | WES | MARK1 | v1 | ~4 h 59 m 27 s | Success | Same-patch reproducibility rerun; run_id `run_2026_05_15_063040`; FASTQ and Stage 11/12 metrics stable |


**Notes:**
- ERR10619300 completed successfully after the assay-type provenance patch. This run therefore represents the first Saudi WES baseline with corrected WES-aware metadata/provenance behavior.

- ERR10619281 also completed successfully before the assay-type provenance patch. That first run remains valid as a runtime baseline, but its metadata should be treated as partially superseded for assay-type provenance.

The provenance-corrected ERR10619281 rerun completed successfully and now serves as the metadata-transition reproducibility comparison pair within the Saudi epilepsy WES telemetry campaign.

---

## Stage-specific telemetry for ERR10619281

| Stage                      |  Run A | Run B |
| -------------------------- | -----: | ----: |
| stage_02_align_data        |  6290s | 6084s |
| stage_05_call_variants     | 10189s | 9947s |
| stage_07_annotate_variants |  1232s | 1215s |

> Both runs on ERR10619281 exhibit similar telemetry metrics

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

## Infrastructure Strategy Revision

Early WES telemetry materially revised the expected runtime economics for epilepsy-cohort processing.

Historical assumptions based on HG002-scale WGS runtime (~36h) initially implied that large cohort execution would require aggressive horizontal scaling infrastructure.

However, observed Saudi epilepsy WES runtime (~5h/sample) substantially improved projected cohort feasibility on MARK-class infrastructure.

This revised:
- execution scheduling expectations
- cohort throughput assumptions
- hardware allocation strategy
- manifest orchestration feasibility

---

## Scaling Implications

Future execution goals include approximately:

`~144 epilepsy-related SRAs`

including:

`ERR10619281`
`ERR10619300`

If production-scale WGS runtime remains near:

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

## Preliminary Assessment

Phase 1A has already validated several important operational advances:

- MARK operational harness functionality
- telemetry emission
- provenance infrastructure
- real-time runtime observation workflows
- early biological-result-layer reproducibility stability

Ongoing telemetry analysis will help determine whether future effort should prioritize:

`vertical optimization`

or:

`horizontal execution scaling`

for large-scale epilepsy cohort processing.

---

## Next Steps

```text
The repeated telemetry campaigns on ERR10619281 and ERR10619300 now justify dedicated reproducibility assessment documentation and lightweight comparison tooling.
```

---