# Phase 1A MARK Runtime Baseline Summary
## HG002 Instrumented Production Rerun

**Repository:** variant_annotation_pipeline  
**Branch:** `phase0-logging-foundation`  
**Execution Profile:** `mark_baseline_phase1a`  
**Machine:** `VandPyMolGPUResearch`  
**Run ID:** `run_2026_05_13_060859`  
**Execution Mode:** `full_pipeline`  
**Status:** COMPLETED SUCCESSFULLY  

---

# Executive Summary

Phase 1A successfully completed the first fully instrumented HG002 production rerun on MARK1.

This run established the first comprehensive runtime baseline for VAP under production-scale execution conditions with:

- runtime telemetry
- stage-level timing
- provenance fingerprints
- stage summaries
- resource snapshots
- deterministic metadata emission
- operational tmux-managed execution

The run completed all 13 stages successfully.

Observed total runtime:

```text
~22 hours 44 minutes 34 seconds
```

This represents a substantial improvement over the earlier approximate:

```text
~36 hour
```

historical runtime estimate.

---

# Strategic Significance

Phase 1A provided the first evidence-driven view into VAP runtime economics.

The run demonstrated that:

- VAP is operationally stable at HG002 scale
- observability infrastructure is functioning correctly
- deterministic metadata systems are functioning correctly
- major bottlenecks are now empirically identifiable
- future optimization efforts can now proceed rationally

Most importantly:

```text
VEP annotation is NOT the dominant runtime bottleneck.
```

Instead, runtime is overwhelmingly dominated by:

- Stage 05 — Variant Calling
- Stage 02 — Alignment

This materially changes future optimization priorities.

---

# Runtime Breakdown

| Stage | Description | Runtime (seconds) | Runtime (hours) |
|---|---|---:|---:|
| Stage 01 | Load Data | 0 | 0.00 |
| Stage 02 | Align Reads | 31,601 | 8.78 |
| Stage 03 | Process BAM | 1,062 | 0.30 |
| Stage 04 | QC Aligned Reads | 174 | 0.05 |
| Stage 05 | Call Variants | 41,883 | 11.63 |
| Stage 06 | Normalize VCF | 60 | 0.02 |
| Stage 07 | Annotate Variants (VEP) | 6,091 | 1.69 |
| Stage 08 | Filter & Partition | 547 | 0.15 |
| Stage 09 | Interpret Coding | 2 | <0.01 |
| Stage 10 | Interpret Noncoding | 168 | 0.05 |
| Stage 11 | Prioritize Variants | 142 | 0.04 |
| Stage 12 | Validate Variants | 144 | 0.04 |
| Stage 13 | Write Summary | 0 | 0.00 |

---

# Primary Runtime Bottlenecks

## Stage 05 — Variant Calling

Observed runtime:

```text
11.63 hours
```

This was the single largest runtime contributor.

Likely contributing factors:

- Java/GATK execution behavior
- BAM traversal cost
- variant calling computational complexity
- storage I/O
- virtualization overhead
- thread utilization efficiency

This stage now represents the highest-value optimization target.

---

## Stage 02 — Read Alignment

Observed runtime:

```text
8.78 hours
```

Observed during execution:

```text
bwa mem
~1440% CPU utilization
```

Approximate interpretation:

```text
~14–15 logical cores worth of active compute utilization
```

This demonstrates meaningful parallel execution behavior.

However, Stage 02 remains a major runtime contributor and likely interacts strongly with:

- storage throughput
- SAM/BAM serialization
- network-backed block storage behavior
- compression/decompression overhead

---

## Stage 07 — VEP Annotation

Observed runtime:

```text
1.69 hours
```

This was substantially lower than initially feared.

This finding is strategically important because earlier assumptions suggested VEP might dominate runtime.

Phase 1A demonstrated that:

```text
VEP is important, but NOT the primary bottleneck.
```

---

# Infrastructure Observations

MARK1 appears to be:

- virtualized
- KVM/QEMU-backed
- network-storage-backed
- likely operating on Ceph/RBD infrastructure

Observed characteristics included:

- virtualized Xeon Gold 6230 CPUs
- RBD-backed storage devices
- large available RAM (~256 GiB)
- fluctuating CPU availability
- offline virtual CPUs

This suggests that:

```text
infrastructure limitations may contribute significantly to runtime behavior
```

particularly:

- storage I/O latency
- virtualization overhead
- shared-resource contention

---

# Operational Successes

Phase 1A successfully validated:

- tmux-managed long-running execution
- detached execution persistence
- runtime telemetry capture
- stage-level observability
- provenance fingerprinting
- deterministic metadata generation
- canonical logging behavior
- MARK operational harnesses
- full production HG002 execution stability

This marks a substantial operational maturity milestone for VAP.

---

# Determinism Observations

The rerun produced structurally coherent outputs across all stages.

Observed outputs included:

- annotated VCFs
- interpreted coding/noncoding TSVs
- prioritization tables
- validation candidate tables
- stage summaries
- artifact manifests
- provenance metadata
- runtime telemetry

No catastrophic structural divergence was observed relative to earlier successful HG002 runs.

This supports continued confidence in VAP reproducibility behavior.

---

# Strategic Implications

Phase 1A materially changes future optimization strategy.

Initial assumptions emphasized:

```text
VEP optimization
```

However, Phase 1A demonstrates that:

```text
alignment + variant calling dominate runtime economics
```

Future optimization efforts should therefore prioritize:

1. Stage 05 variant calling optimization
2. Stage 02 alignment optimization
3. storage/I/O considerations
4. thread utilization analysis
5. infrastructure-aware execution strategy

---

# Horizontal Scaling Implications

Even with the improved runtime:

```text
~22.7 hours per HG002-scale SRA
```

large-scale cohort execution remains computationally expensive.

Projected execution burden:

```text
144 SRAs × ~22.7 hours
≈ 3269 node-hours
```

Approximate wall-clock estimates:

| Nodes | Estimated Runtime |
|---|---:|
| 1 node | ~136 days |
| 3 nodes | ~45 days |
| 5 nodes | ~27 days |
| 10 nodes | ~14 days |

Therefore:

```text
horizontal scaling remains strategically important
```

particularly for:

- epilepsy cohort execution
- GEO contrast analysis
- RSP network convergence workflows

---

# Emerging Strategic Direction

Phase 1A suggests the following likely trajectory:

- continue bounded optimization efforts
- prioritize evidence-driven tuning
- avoid premature over-optimization
- transition toward manifest-driven execution
- scale horizontally across MARK-class nodes
- freeze VAP v1 once operational maturity is sufficient

This reflects a shift from:

```text
infinite vertical optimization
```

toward:

```text
distributed cohort-scale execution strategy
```

---

# Key Deliverables Generated

## Metadata

```text
metadata/runtime_profile.tsv
metadata/stage_resource_snapshots.tsv
metadata/run_metadata.json
metadata/run_fingerprint.json
metadata/stage_summaries/
```

## Core Pipeline Outputs

```text
annotated_variants.vcf
annotated_variants.tsv
stage_08_vdb_ready_variants.tsv
stage_11_prioritized_variants.tsv
stage_12_validation_candidates.tsv
stage_13_run_report.md
```

---

# Final Assessment

Phase 1A was highly successful.

The run established:

- the first trustworthy VAP runtime baseline
- the first full production observability baseline
- the first empirical bottleneck profile
- the first infrastructure-aware execution characterization

Most importantly:

```text
future optimization and scaling decisions can now proceed from evidence rather than speculation.
```