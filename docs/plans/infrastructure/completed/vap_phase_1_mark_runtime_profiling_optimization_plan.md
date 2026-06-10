# VAP Phase 1 Implementation Plan
## MARK Runtime Profiling and Optimization

**Repository:** variant_annotation_pipeline  
**Branch:** `phase0-logging-foundation`  
**Status:** Draft  
**Purpose:** Evidence-driven performance engineering for MARK-class execution

---

# Purpose

Phase 1 will transform VAP optimization from estimate-driven tuning into evidence-driven performance engineering.

The goal is to reduce MARK runtime for HG002 and future epilepsy SRA runs while preserving:

- deterministic behavior
- schema stability
- provenance integrity
- Stage 08+ downstream compatibility
- VDB/RDGP-facing contract safety

---

# Strategic Context

VAP has already completed a full HG002 run on MARK1.

Observed baseline:

```text
HG002 full pipeline on MARK1: ~36 hours
Stages 01–08 estimate: ~28 hours
Current thread usage: ~8 cores
MARK available cores: ~40
```

The original successful HG002 run is biologically useful but operationally under-instrumented:

- no populated run logs were preserved
- no runtime profile existed
- no per-stage timing existed
- no resource telemetry existed

Phase 0 corrected this by adding:

- canonical run logs
- runtime profiles
- stage summaries
- run metadata
- run fingerprints
- deterministic fixture execution
- `pytest` regression protection

Phase 1 now uses that foundation to profile and optimize real MARK execution.

---

## Core Principle

Do not optimize blindly.

Phase 1 follows:

```text
instrument → profile → analyze → tune → validate → re-run HG002 → compare
```

NOT:

```text
increase all thread counts and hope
```

---

## Primary Goals

1. Establish a measured MARK1 HG002 runtime profile.
2. Identify true bottleneck stages.
3. Tune thread/fork/resource settings safely.
4. Preserve deterministic output contracts.
5. Reduce HG002 wallclock runtime by hours, not seconds.
6. Prepare VAP for future ERR10619281 / ERR10619300 / 144-SRA execution.

---

## Non-Goals

Phase 1 will NOT:

- rewrite VAP into Nextflow/Snakemake
- introduce distributed scheduling yet
- redesign Stage 08 contracts
- alter biological prioritization logic
- change output schemas without contract review
- optimize for tiny local fixture runtime
- pursue micro-optimizations that save only seconds

---

## Phase 1A — Instrumented Baseline Rerun

### Objective

Run HG002 on MARK1 using the Phase 0 observability system without major performance changes.

This establishes a trustworthy runtime baseline.

---

### Why This Matters

The historical 36-hour HG002 run lacks sufficient runtime observability.

A new baseline must capture:

- per-stage wall time
- stage success/failure status
- run fingerprint
- config snapshot
- runtime profile
- stage summary JSONs
- canonical pipeline log

---

### Deliverables

```text
results/<run_id>/
├── logs/pipeline.log
├── metadata/runtime_profile.tsv
├── metadata/run_metadata.json
├── metadata/run_fingerprint.json
├── metadata/stage_summaries/
└── processed/
```

---

### Acceptance Criteria

- HG002 completes successfully on MARK1.
- Runtime profile contains all 13 stages.
- No stage has missing start/end timing.
- Stage 08+ outputs remain schema-compatible.
- Stage 13 completes.
- Run fingerprint records config/git/environment identity.

---

## Phase 1B — Runtime Analysis

### Objective

Analyze instrumented HG002 runtime profile.

---

### Required Analysis

For each stage:

- wallclock time
- percentage of total runtime
- skipped/success/failure status
- tool invoked
- configured threads/forks
- likely resource class:
  - CPU-bound
  - I/O-bound
  - memory-bound
  - external-tool-bound
  - Python/TSV-bound

---

### Expected Bottleneck Candidates

Likely high-cost stages:

```text
Stage 02 — BWA alignment
Stage 03 — BAM sorting/indexing
Stage 05 — GATK HaplotypeCaller
Stage 06 — VCF normalization
Stage 07 — VEP annotation
Stage 08 — large TSV partitioning
```

Stage 07 is a strong suspected bottleneck, but Phase 1 must verify this.

---

## Phase 1C — MARK High-Core Profile Design

### Objective

Create a dedicated MARK execution profile.

Candidate config:

`config/config.mark.highcore.yaml`

or equivalent profile overlay.

---

### Initial Safe Tuning Hypotheses

Current settings:

```yaml
bwa threads: 8
samtools threads: 8
gatk java_options: "-Xmx16g"
vep fork: 4
```

Initial MARK-aware candidate ranges:

```yaml
bwa threads: 24–32
samtools threads: 16–24
gatk java_options: "-Xmx32g" or "-Xmx48g"
vep fork: 8–16
```

These are hypotheses, not final values.

High VEP fork counts may produce diminishing returns or runtime regressions due to:

- cache contention
- filesystem pressure
- process scheduling overhead
- memory amplification
- compressed VCF I/O saturation

---

### Resource Reservation Policy

Do not allocate all 40 cores.

Reserve capacity for:

- OS
- filesystem
- compression
- Java overhead
- VEP cache I/O
- monitoring

Initial policy:

```text
max active compute threads: 32
reserve threads: ~8
```

---

## Phase 1D — Targeted Optimization Experiments

### Determinism Preservation Requirement

Performance optimizations must not introduce nondeterministic output ordering, unstable row counts, or schema drift.

Any optimization that alters deterministic behavior must be rejected or formally reviewed.

### Objective

Tune one bottleneck class at a time.

Captured in:

`docs/profiling/stage_runtime_matrix.tsv`

which tracks:

- stage runtime
- config knobs
- git commits
- elapsed time
- warnings
- outcomes

systematically.

Rationale:

```text
Optimization history becomes hard to reason about across many experiments without data collection and subsequent analysis.
```

---

### Experiment Rules

Each experiment must record:

- config used
- git commit
- run ID
- stage runtime profile
- output schema comparison
- key row counts
- warning/error counts
- failure modes

---

### Candidate Experiments

#### Alignment

Tune:

```yaml
tools.bwa.threads
```

Compare:

- Stage 02 runtime
- BAM output presence
- downstream row counts

---

### BAM Processing

Tune:

```yaml
tools.samtools.threads
```

Potential future addition:

```text
samtools sort memory-per-thread
```

Compare:

- Stage 03 runtime
- BAM/index creation
- downstream compatibility

---

### GATK Variant Calling

Tune:

```yaml
tools.gatk.java_options
```

Potential future investigation:

```text
interval sharding
```

Compare:

- Stage 05 runtime
- raw VCF variant count
- downstream normalized count

---

### VEP Annotation

Tune:

```yaml
tools.vep.fork
```

Candidate values:

```text
4, 8, 12, 16
```

Compare:

- Stage 07 runtime
- warning count
- annotated VCF/TSV row counts
- Stage 08 compatibility

Caution:

```text
VEP may become I/O/cache-bound if fork count is too high.
```

---

### Large TSV Processing

Stages 08–13 currently appear fast on fixture, but HG002-scale TSVs are multi-GB.

Evaluate:

- Python streaming performance
- memory pressure
- output row counts
- need for chunked or optimized parsing

Do not introduce pandas/polars/pyarrow unless benchmarks show clear benefit.

---

## Phase 1E — HG002 Optimized Revalidation

### Objective

Rerun full HG002 on MARK1 with optimized settings.

---

### Compare Against

- original MARK1 HG002 successful run
- Phase 1A instrumented baseline
- Phase 1D experimental runs

---

### Required Comparisons

Compare:

- total runtime
- per-stage runtime
- output schemas
- row counts
- Stage 08 summary
- Stage 09 summary
- Stage 10 summary
- Stage 11 summary
- Stage 12 summary
- Stage 13 final summary
- artifact manifest
- warning profiles
- run fingerprints

---

### Success Criteria

Phase 1 succeeds if:

- HG002 runtime decreases meaningfully
- no schema drift occurs
- no deterministic contract is violated
- Stage 13 completes
- output counts are explainable and stable
- optimized settings are documented

Runtime improvement target:

```text
hours-level improvement
```

not seconds-level improvement.

---

## Phase 1F — Prepare Epilepsy SRA Execution

Once HG002 is optimized and validated, proceed to:

```text
ERR10619281 on MARK1
ERR10619300 on MARK1
```

Then later:

```text
MARK2 replication
MARK3 replication
144-SRA manifest-driven execution
```

---

## Safety Gates


Do not advance from one phase to the next unless:

- `pytest` passes
- post-VEP fixture execution passes
- MARK run fingerprint is recorded
- runtime profile is complete
- Stage 08+ schemas remain stable
- Stage 13 completes
- lightweight fixture execution remains functional

---

## Recommended Commands Before MARK Runs

Local preflight on sys76:

```bash
pytest -q
python run_pipeline.py --config config/config.example.post_vep.yaml
```

MARK preflight:

```bash
pytest -q
python run_pipeline.py --config config/config.example.post_vep.yaml
```

Then full MARK execution.

---

## Documentation Deliverables

Phase 1 should produce:

```text
docs/status/phase1_mark_baseline_runtime_report.md
docs/status/phase1_mark_optimization_experiment_log.md
docs/status/phase1_hg002_optimized_revalidation_report.md
```

Optional:

`docs/profiling/`

for detailed runtime tables.

---

## Final Outcome

Phase 1 should leave VAP with:

- a measured MARK runtime baseline
- an optimized MARK execution profile
- documented runtime improvements
- reproducible performance evidence
- HG002 optimized validation
- readiness for epilepsy SRA scaling

This phase converts VAP from a correct pipeline into a measurable, tunable, scalable execution system.

---