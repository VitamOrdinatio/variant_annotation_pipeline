# VAP Test Ecosystem

The `tests/` namespace contains the validation and regression-testing layer of the Variant Annotation Pipeline (VAP).

These tests protect the repository’s core engineering guarantees across:

* execution lifecycle behavior,
* metadata and provenance contracts,
* runtime telemetry schemas,
* stable JSON serialization,
* stage summary emission,
* benchmarking workflows,
* and observability metric infrastructure.

The test ecosystem supports the broader VAP release goal:

```text
reproducible semantic evidence infrastructure
```

rather than simply checking isolated script behavior.

---

# Test Topology

```text
tests/
├── benchmarking/
├── metrics/
├── test_logging_contract.py
├── test_metadata_schema_contract.py
├── test_pipeline_lifecycle_smoke.py
├── test_post_vep_fixture_mode.py
├── test_post_vep_fixture_outputs.py
├── test_run_fingerprint.py
├── test_run_metadata.py
├── test_run_paths.py
├── test_runtime_profile_schema.py
├── test_stable_json_serialization.py
├── test_stage_resource_snapshots.py
└── test_stage_summary_json.py
```

| Test Layer      | Purpose                                                            |
| --------------- | ------------------------------------------------------------------ |
| `benchmarking/` | HG002 benchmarking workflow validation                             |
| `metrics/`      | telemetry and metric aggregation validation                        |
| root tests      | pipeline lifecycle, metadata, runtime, and observability contracts |

---

# Running Tests

From the repository root:

```bash
pytest tests/
```

For a quieter test run:

```bash
pytest -q tests/
```

For targeted validation:

```bash
pytest tests/metrics/
pytest tests/benchmarking/
```

---

# Core Runtime Contract Tests

The root-level test suite validates execution and observability expectations that apply across the VAP ecosystem.

| Test                                | Purpose                                             |
| ----------------------------------- | --------------------------------------------------- |
| `test_pipeline_lifecycle_smoke.py`  | confirms core pipeline lifecycle behavior           |
| `test_run_paths.py`                 | validates deterministic run-directory structure     |
| `test_run_metadata.py`              | validates run metadata emission                     |
| `test_run_fingerprint.py`           | validates reproducible run identity surfaces        |
| `test_logging_contract.py`          | validates logging behavior                          |
| `test_metadata_schema_contract.py`  | validates metadata schema expectations              |
| `test_runtime_profile_schema.py`    | validates runtime profile structure                 |
| `test_stage_resource_snapshots.py`  | validates stage resource snapshot behavior          |
| `test_stage_summary_json.py`        | validates stage summary JSON emission               |
| `test_stable_json_serialization.py` | validates deterministic JSON serialization behavior |

These tests collectively protect:

* run identity,
* metadata continuity,
* output structure,
* telemetry emission,
* logging contracts,
* and stage-level observability.

---

# Post-VEP Fixture Tests

| Test                               | Purpose                                    |
| ---------------------------------- | ------------------------------------------ |
| `test_post_vep_fixture_mode.py`    | validates post-VEP fixture execution mode  |
| `test_post_vep_fixture_outputs.py` | validates expected fixture output behavior |

These tests support lightweight validation of downstream VAP behavior without requiring full upstream WGS/WES execution.

This fixture layer is important because it allows development and regression validation to proceed without repeatedly invoking large external genomics workflows.

---

# Metrics Test Ecosystem

The `metrics/` namespace validates the telemetry and metric infrastructure used throughout modern VAP execution.

| Test                                    | Purpose                               |
| --------------------------------------- | ------------------------------------- |
| `metrics/test_metric_aggregation.py`    | validates metric aggregation behavior |
| `metrics/test_stage_metric_emitters.py` | validates stage-level metric emission |

These tests protect the observability infrastructure used for:

* runtime characterization,
* stage-level telemetry,
* reproducibility evaluation,
* cross-run governance analysis,
* and operational reporting.

---

# Benchmarking Test Ecosystem

The `benchmarking/` namespace validates HG002 benchmarking support.

| Test                                             | Purpose                                                      |
| ------------------------------------------------ | ------------------------------------------------------------ |
| `benchmarking/test_run_hg002_happy_benchmark.py` | validates HG002 `hap.py` benchmarking orchestration behavior |

This test layer supports benchmark-aware validation of the HG002 workflow while preserving controlled execution assumptions around reference resources and benchmarking substrates.

---

# Relationship to Observability

The VAP test ecosystem is tightly coupled to observability infrastructure.

Tests validate that VAP emits:

* run metadata,
* runtime profiles,
* stage summaries,
* resource snapshots,
* metric records,
* stable JSON artifacts,
* and logging outputs.

This reflects a central VAP design principle:

```text
observability is infrastructure, not incidental logging.
```

---

# Relationship to Release Readiness

The test ecosystem is one of the primary release gates for VAP v1.

A release-ready state should demonstrate:

* passing root tests,
* passing metrics tests,
* passing benchmarking tests,
* stable schema behavior,
* and reproducible observability outputs.

The minimum release validation command is:

```bash
pytest tests/
```

A green test suite supports claims of:

* deterministic execution structure,
* metadata continuity,
* telemetry integrity,
* benchmarking workflow stability,
* and reproducibility-aware engineering.

---

# Relationship to Case Studies

The test infrastructure helped support the later development of:

| Case Study       | Test-Relevant Infrastructure                           |
| ---------------- | ------------------------------------------------------ |
| HG002            | benchmarking, runtime profile, metadata, observability |
| ERR10619281      | deterministic rerun and metadata continuity            |
| ERR10619300      | fixture validation and downstream evidence surfaces    |
| 12-SRA cross-run | telemetry and metric aggregation infrastructure        |

These tests therefore function as engineering guardrails beneath the public-facing case-study ecosystem.

---

# Test Philosophy

The VAP test suite is designed to validate more than isolated function correctness.

It protects:

* lifecycle behavior,
* reproducibility surfaces,
* metadata contracts,
* observability outputs,
* benchmark orchestration,
* and telemetry aggregation.

This aligns with the broader repository philosophy that VAP is:

```text
traceable genomic evidence infrastructure
```

rather than a collection of ungoverned execution scripts.

---

# Recommended Reviewer Path

Reviewers interested in engineering maturity should inspect:

1. `test_pipeline_lifecycle_smoke.py`
2. `test_run_metadata.py`
3. `test_stage_summary_json.py`
4. `metrics/test_stage_metric_emitters.py`
5. `benchmarking/test_run_hg002_happy_benchmark.py`

This sequence progressively exposes:

* pipeline lifecycle testing,
* provenance metadata validation,
* stage summary validation,
* telemetry emission validation,
* and benchmark workflow validation.

---

# Final Positioning

The `tests/` namespace demonstrates that VAP release readiness is evaluated through:

* execution-contract validation,
* observability-contract validation,
* metric infrastructure testing,
* and benchmark workflow testing.

These tests are therefore a core component of the repository’s reproducibility and release-governance posture.
