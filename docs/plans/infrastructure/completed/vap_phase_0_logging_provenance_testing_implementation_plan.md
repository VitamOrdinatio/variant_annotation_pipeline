# VAP Phase 0 Implementation Plan
## Logging, Provenance, and Testing Foundation

## Purpose

Implement the Phase 0 foundation required before MARK runtime optimization.

Phase 0 will make VAP:
- observable
- provenance-aware
- testable
- deterministic
- safer to run repeatedly on MARK1 / MARK2 / MARK3

This phase does not optimize runtime yet.  
It prepares VAP so runtime optimization can be measured and validated.

During Phase 0, legacy `metadata.json` and `config_used.yaml` may still be emitted, but `metadata/run_metadata.json` and `metadata/config_snapshot.yaml` become the preferred forward-facing artifacts.

---

## Current Diagnosis

VAP already has a good execution skeleton:

- timestamped `run_id`
- isolated `results/<run_id>/` directories
- centralized runtime `state`
- config snapshotting
- final `metadata.json`
- stage-based execution order

However, the logging system is incomplete.

Current issue:

```text
results/bootstrap_logs/pipeline.log
```

is used as the primary logger before `run_id` creation and continues being used after the run starts.

A run-specific log path already exists:

```text
results/<run_id>/logs/pipeline.log
```

---

## Phase 0 Goals

1. Separate bootstrap logging from canonical run logging.
2. Make `results/<run_id>/logs/pipeline.log` the authoritative run log.
3. Preserve bootstrap logs only for pre-run failures and setup diagnostics.
4. Add structured run metadata artifacts.
5. Add stage timing instrumentation.
6. Add `pytest` coverage for logging, provenance, schema, and determinism contracts.
7. Keep implementation local-first on `sys76` before `MARK` validation.

---

## Non-Goals

Phase 0 will NOT:

- optimize thread counts
- tune MARK performance
- rerun HG002 end-to-end
- alter Stage 08 VDB/RDGP output contracts
- create a new pipeline stage
- rewrite VAP into Nextflow/Snakemake
- introduce heavy dependencies unless clearly justified

---

## Target Runtime Structure

```text
results/<run_id>/
├── logs/
│   └── pipeline.log
├── metadata/
│   ├── run_metadata.json
│   ├── run_fingerprint.json
│   ├── runtime_profile.tsv
│   ├── config_snapshot.yaml
│   └── stage_summaries/
│       ├── stage_01_summary.json
│       ├── stage_02_summary.json
│       └── ...
├── interim/
├── processed/
├── reports/
├── final/
└── validation/
```

Existing `config_used.yaml` and `metadata.json` may be preserved temporarily for backward compatibility, but new structured artifacts should move toward `metadata/`.

---

## Implementation Tasks

### Task 1 — Add metadata directory to run paths

Update `initialize_run_paths()` so each run creates:

- `results/<run_id>/metadata/`
- `results/<run_id>/metadata/stage_summaries/`

Add paths:

```py
metadata_dir
stage_summaries_dir
run_metadata_path
run_fingerprint_path
runtime_profile_path
config_snapshot_path
```

---

### Task 2 — Refactor logger lifecycle

Phase 0 does not require separate `stage_XX.log` files; per-stage observability is captured through pipeline.log, runtime_profile.tsv, and stage summary JSONs.

Phase 0 will implement **two** logger phases:

```text
bootstrap_logger → run_logger
```

**Bootstrap logger** writes only to:

```text
results/bootstrap_logs/pipeline.log
```

**Run logger** writes to:

```text
results/<run_id>/logs/pipeline.log
```

Once `run_id` exists, the pipeline must switch to the run logger.

Acceptance criteria:

- bootstrap log records config-load and pre-run failures
- run log records all stage execution
- canonical run provenance lives under `results/<run_id>/`
- bootstrap log no longer accumulates full run histories

---

### Task 3 — Add stage timing instrumentation

Wrap each stage execution with timing logic:

```text
stage_start_time
stage_end_time
elapsed_seconds
status
```

Update `state["stage_outputs"][stage_name]` with timing fields.

---

### Task 4 — Emit runtime_profile.tsv

Write:

```text
results/<run_id>/metadata/runtime_profile.tsv
```

Required columns:

```text
stage
status
start_time
end_time
elapsed_seconds
```

Optional future columns:

```text
threads
max_memory_gb
cpu_percent
temp_dir
```

---

### Task 5 — Emit per-stage summary JSONs

For each stage, write:

```text
results/<run_id>/metadata/stage_summaries/stage_XX_summary.json
```

Minimum fields:

```json
{
  "stage": "stage_07_annotate_variants",
  "status": "success",
  "start_time": "...",
  "end_time": "...",
  "elapsed_seconds": 123.45,
  "input_artifacts": [],
  "output_artifacts": [],
  "warning_count": 0,
  "error_count": 0
}
```

---

### Task 6 — Emit run_fingerprint.json

Write:

```text
results/<run_id>/metadata/run_fingerprint.json
```

Include:

```text
run_id
pipeline_name
pipeline_version
git_commit
config_hash
config_path
reference_genome
reference_fasta_path
reference_fasta_hash_or_size
hostname
execution_mode
execution_profile
python_version
tool_versions
created_at
```

This supports MARK1/MARK2/MARK3 replication checks.

---

### Task 7 — Preserve deterministic serialization

All JSON outputs must use:

```py
json.dump(..., indent=2, sort_keys=True)
```

All TSV outputs should preserve stable column order.

---

### Task 8 — Add pytest scaffold

Create real tests under:

```text
tests/
```

Initial tests:

```text
tests/test_logging_contract.py
tests/test_run_fingerprint.py
tests/test_stage_summary_json.py
tests/test_runtime_profile_schema.py
tests/test_config_snapshot.py
tests/test_variant_id_determinism.py
tests/test_missing_value_semantics.py
tests/test_stable_json_serialization.py
tests/test_run_paths.py
```

---

## First Test Targets

### Logging contract

Verify:

- bootstrap log path resolves under `results/bootstrap_logs/`
- run log path resolves under `results/<run_id>/logs/`
- run logger does not write canonical stage events to bootstrap log


### Runtime profile schema

Verify required columns:

```text
stage
status
start_time
end_time
elapsed_seconds
```

### Run fingerprint

Verify required fields exist.

### Stable JSON

Verify repeated serialization of the same object produces identical output.

### Run Path Check

Verify creation of: 

```text
logs/
metadata/
metadata/stage_summaries/
interim/
processed/
reports/
final/
validation/
```

---

## Dependency Policy

Use standard library first for:

- logging
- JSON
- hashing
- pathlib
- subprocess
- timestamps
- platform metadata
- CSV/TSV writing

Allow `pytest`.

Use `pandas`, `pyarrow`, or `polars` only after benchmarking shows a clear reliability or runtime advantage.

---

## Local-First Workflow

Develop on sys76 first.

Run:

`pytest -q`

Then run a lightweight VAP smoke test if available.

Only after local tests pass:

1. commit to GitHub
2. pull on MARK1
3. run pytest -q on MARK1
4. run a minimal smoke test
5. only later rerun HG002

---

## Acceptance Criteria

Phase 0 is complete when:

- `results/<run_id>/logs/pipeline.log` is authoritative
- bootstrap logs no longer contain full run execution
- run metadata artifacts are emitted
- runtime profile is emitted
- per-stage summary JSONs are emitted
- run fingerprint is emitted
- pytest suite passes locally on sys76
- pytest suite passes on MARK1
- no VDB/RDGP-facing output schemas are changed

---

## Bottom Line

Phase 0 completes the observability foundation original VAP already started.

The goal is not to rewrite VAP.

The goal is to make VAP self-describing, testable, auditable, and ready for MARK-scale runtime optimization.

---