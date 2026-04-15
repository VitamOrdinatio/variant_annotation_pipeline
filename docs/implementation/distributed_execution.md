# Distributed Execution Contract  
## variant_annotation_pipeline v1.0  
## docs/implementation/distributed_execution.md

---

## 1. Purpose

This document defines the **future distributed execution model** for  
`variant_annotation_pipeline`.

Distributed execution is **not implemented in v1.0**, but the system must be designed so that future versions can support:

- batch processing of multiple samples
- execution across multiple machines or nodes
- resumable and fault-tolerant workflows
- manifest-driven orchestration

This document defines the **contract boundary** that enables those features.

---

## 2. Governing Principle

```text
Each sample run must be fully self-contained and independently executable.
```

This ensures:

- no shared mutable state between runs
- no cross-run dependencies
- easy parallelization
- safe distributed scheduling

---

## 3. Execution Model (Future)

Future distributed execution will follow this model:

```text
manifest → job dispatcher → per-sample runs → aggregation
```

### Components

1. **Manifest**
   - list of samples
   - input paths
   - metadata
   - execution parameters

2. **Dispatcher**
   - submits jobs to:
     - local threads
     - HPC schedulers (SLURM, PBS)
     - cloud runners
   - assigns one job per sample

3. **Worker (per-sample pipeline)**
   - executes full pipeline using existing v1 logic
   - produces self-contained run directory

4. **Aggregator**
   - merges completed runs
   - produces cohort-level outputs

---

## 4. Manifest Schema (Future)

A manifest file defines multiple samples.

Example (TSV or CSV):

```text
sample_id,fastq_1,fastq_2,reference_genome
HG002,/path/to/R1.fastq.gz,/path/to/R2.fastq.gz,GRCh38
HG003,/path/to/R1.fastq.gz,/path/to/R2.fastq.gz,GRCh38
```

### Required fields

- `sample_id`
- `fastq_1`
- `fastq_2`

### Optional fields

- `reference_genome`
- `bioproject_accession`
- `sra_accession`
- `sample_alias`

---

## 5. Job Isolation Requirements

Each job must:

- operate in its own run directory:
  ```text
  results/<run_id>/
  ```
- write its own:
  - logs
  - artifacts
  - metadata
- not modify shared global state

### Forbidden behavior

- writing to shared global files
- overwriting other runs
- relying on in-memory cross-sample communication

---

## 6. Deterministic Run Structure

Each distributed job must produce:

```text
results/<run_id>/
├── logs/
├── interim/
├── processed/
├── reports/
├── metadata.json
```

This structure must match v1 single-sample execution.

---

## 7. Idempotency Requirement

Each run must be:

```text
idempotent
```

Meaning:

- re-running the same sample with the same config produces equivalent outputs
- partial runs can be safely restarted
- stage-level overwrites are controlled

---

## 8. Failure Model

Distributed execution must classify job outcomes:

- `completed`
- `failed`
- `partial`
- `skipped`

Failures must not corrupt:

- other runs
- aggregation inputs

### Required behavior

- failed runs remain isolated
- metadata captures failure reason
- successful runs remain usable

---

## 9. Logging Requirements

Each run must produce:

```text
results/<run_id>/logs/pipeline.log
```

Log content must include:

- stage start/stop events
- tool invocations
- warnings
- errors
- runtime durations

---

## 10. Resource Constraints (Future)

Distributed execution must allow per-job specification of:

- CPU cores
- memory
- disk usage
- runtime limits

These may be defined in:

- manifest
- config
- scheduler directives

---

## 11. Scheduler Integration (Future)

The system should be compatible with:

- local multiprocessing
- SLURM
- PBS
- cloud batch systems

### Example abstraction

```text
dispatch(sample) → run_pipeline(config_for_sample)
```

Scheduler-specific logic must remain outside core pipeline code.

---

## 12. Data Locality Considerations

Future execution may involve:

- local disks
- shared filesystems
- cloud storage

Pipeline design must assume:

- input files are accessible via paths
- outputs are written locally per run
- aggregation reads from finalized outputs

---

## 13. Interaction with State Schema

Distributed execution relies on:

```text
docs/implementation/state_schema.md
```

Key dependencies:

- `state["run"]`
- `state["sample"]`
- `state["artifacts"]`
- `state["stage_outputs"]`

These must remain stable across versions.

---

## 14. Interaction with Aggregation Schema

Distributed execution produces inputs for:

```text
docs/implementation/aggregation_schema.md
```

Each completed run must be:

- discoverable
- self-describing
- mergeable

---

## 15. Configuration Strategy (Future)

Distributed mode may introduce:

```yaml
execution:
  mode: distributed
  manifest_path: path/to/manifest.tsv
  scheduler: slurm
```

This is not required for v1.

---

## 16. Non-Goals for v1.0

The following are explicitly **not implemented**:

- manifest parsing
- job dispatching
- parallel execution
- scheduler integration
- distributed retries
- inter-process communication

v1 remains strictly:

```text
single-sample, single-run execution
```

---

## 17. Forward-Compatible Design Rules

To enable distributed execution later, v1 must ensure:

1. all runs are independent
2. all outputs are namespaced by `run_id`
3. no global mutable state exists
4. all metadata is stored per run
5. all stages are deterministic

---

## 18. Summary Rule

```text
v1 builds a correct single-sample pipeline.
future versions replicate that pipeline across samples without changing its core logic.
```

---

# End of Distributed Execution Contract