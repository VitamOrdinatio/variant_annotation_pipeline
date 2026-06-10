# VAP Orchestration Core (`src/`)

The `src/` namespace contains the reusable orchestration and execution-governance substrate of the Variant Annotation Pipeline (VAP).

This namespace is intentionally distinct from:

* `pipeline/` — stage-specific reusable execution logic
* `scripts/` — operational utilities and one-off analytical workflows

Instead, `src/` contains the reusable infrastructure responsible for:

* execution orchestration,
* configuration handling,
* telemetry aggregation,
* provenance-linked metric emission,
* and runtime coordination.

This namespace increasingly functions as:

```text
the operational control layer of the VAP ecosystem.
```

---

# Architectural Separation

The repository intentionally separates reusable infrastructure into two major namespaces:

| Namespace   | Responsibility                                                           |
| ----------- | ------------------------------------------------------------------------ |
| `pipeline/` | stage-specific reusable biological processing logic                      |
| `src/`      | orchestration, telemetry, runtime coordination, and execution governance |

This separation prevents:

* orchestration collapse into stage logic,
* telemetry fragmentation,
* execution-state ambiguity,
* and infrastructure coupling.

The distinction became increasingly important during:

* observability expansion,
* reproducibility hardening,
* telemetry maturation,
* and cross-run governance analysis.

---

# Namespace Topology

```text
src/
├── config_loader.py
├── metrics/
└── pipeline_runner.py
```

| Component            | Purpose                                                          |
| -------------------- | ---------------------------------------------------------------- |
| `config_loader.py`   | deterministic configuration loading and validation               |
| `pipeline_runner.py` | orchestration and execution coordination                         |
| `metrics/`           | telemetry aggregation and provenance-aware metric infrastructure |

---

# Pipeline Runner

| Component            | Purpose                                           |
| -------------------- | ------------------------------------------------- |
| `pipeline_runner.py` | central orchestration and execution control layer |

The pipeline runner coordinates:

* stage sequencing,
* execution lifecycle management,
* runtime coordination,
* output organization,
* telemetry integration,
* provenance-aware execution handling,
* and deterministic stage progression.

This orchestration layer became increasingly important as VAP evolved from:

```text
single-run execution
```

into:

```text
multi-run semantic evidence infrastructure.
```

---

# Configuration Infrastructure

| Component          | Purpose                                              |
| ------------------ | ---------------------------------------------------- |
| `config_loader.py` | deterministic configuration ingestion and validation |

The configuration subsystem governs:

* execution configuration,
* stage parameterization,
* runtime setup,
* interoperability consistency,
* and reproducibility-aware initialization.

This infrastructure helps stabilize:

* deterministic execution behavior,
* operational portability,
* and provenance continuity.

---

# Metrics Ecosystem

The `metrics/` namespace governs telemetry-aware execution instrumentation and reproducibility-linked metric infrastructure.

---

# Metrics Topology

```text
metrics/
├── metric_aggregation.py
├── metric_collectors.py
├── metric_io.py
├── metric_record.py
├── metric_validation.py
└── stage_metric_emitters.py
```

| Component                  | Purpose                                      |
| -------------------------- | -------------------------------------------- |
| `metric_aggregation.py`    | runtime metric aggregation and harmonization |
| `metric_collectors.py`     | telemetry collection infrastructure          |
| `metric_io.py`             | metric persistence and serialization         |
| `metric_record.py`         | metric-record structure definitions          |
| `metric_validation.py`     | metric integrity validation                  |
| `stage_metric_emitters.py` | stage-level telemetry emission               |

---

# Telemetry Philosophy

The metrics ecosystem intentionally treats telemetry as:

```text
architectural infrastructure
```

rather than optional debugging output.

The observability subsystem supports:

* provenance-linked telemetry,
* runtime characterization,
* reproducibility analysis,
* stage-level operational introspection,
* and cross-run governance evaluation.

This telemetry architecture later became foundational infrastructure for:

* HG002 runtime characterization,
* semantic reproducibility studies,
* observability-aware cross-run analysis,
* and interoperability governance workflows.

---

# Provenance-Aware Execution

The orchestration ecosystem emphasizes:

* deterministic stage sequencing,
* stable execution identities,
* provenance continuity,
* telemetry-linked execution surfaces,
* and reproducible runtime coordination.

This philosophy enables VAP to preserve:

* operational traceability,
* runtime observability,
* and semantic continuity

across:

* reruns,
* heterogeneous cohorts,
* benchmarking workflows,
* and analytical substrate generation.

---

# Relationship to `pipeline/`

The `pipeline/` namespace contains reusable biological and stage-specific execution logic.

The `src/` namespace instead governs:

* orchestration,
* telemetry,
* execution coordination,
* and runtime infrastructure.

This separation preserves:

| Concern                | Namespace   |
| ---------------------- | ----------- |
| biological stage logic | `pipeline/` |
| execution governance   | `src/`      |

This architectural distinction became increasingly important during:

* observability expansion,
* deterministic rerun validation,
* telemetry maturation,
* and semantic governance scaling.

---

# Relationship to `scripts/`

The `scripts/` ecosystem intentionally contains:

* bounded operational utilities,
* analytical helpers,
* and one-off substrate-generation workflows.

The `src/` namespace instead contains:

```text
reusable orchestration infrastructure.
```

This separation prevents operational analysis tooling from destabilizing the reusable execution substrate.

---

# Relationship to Case Studies

The orchestration and telemetry infrastructure contained within `src/` directly enabled:

| Case Study       | Contribution                                        |
| ---------------- | --------------------------------------------------- |
| HG002            | runtime characterization and benchmarking telemetry |
| ERR10619281      | deterministic rerun validation                      |
| ERR10619300      | semantic-governance execution continuity            |
| 12-SRA cross-run | cohort-scale telemetry and reproducibility analysis |

In particular:

* stage metric emitters,
* aggregation infrastructure,
* and runtime coordination layers

became foundational infrastructure for later observability-aware analyses.

---

# Operational Maturity Themes

The `src/` ecosystem consistently emphasizes:

* deterministic orchestration,
* telemetry-aware execution,
* provenance continuity,
* reproducibility infrastructure,
* runtime observability,
* and execution-governance separation.

Collectively, these components demonstrate that VAP evolved beyond:

```text
pipeline scripting
```

into:

```text
governed execution infrastructure.
```

---

# Recommended Reading Order

Most reviewers should begin with:

1. `pipeline_runner.py`
2. `config_loader.py`
3. `metrics/stage_metric_emitters.py`
4. `metrics/metric_aggregation.py`
5. `metrics/metric_validation.py`

This sequence progressively exposes:

* orchestration,
* configuration governance,
* telemetry emission,
* aggregation architecture,
* and reproducibility validation.

---

# Final Positioning

The `src/` namespace demonstrates that VAP matured through:

* orchestration hardening,
* telemetry-aware execution engineering,
* provenance-linked runtime coordination,
* and reproducibility-oriented infrastructure design.

These components therefore function as:

```text
the reusable orchestration substrate
```

underlying the broader semantic evidence ecosystem of VAP.
