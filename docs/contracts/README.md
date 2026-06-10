# VAP Contract Ecosystem

The `docs/contracts/` namespace defines the formal governance surfaces of the Variant Annotation Pipeline (VAP). These contracts establish deterministic expectations for architectural behavior, stage-level semantics, interoperability substrates, benchmarking components, and operational workflows.

Within VAP, contracts function as stability boundaries that reduce architecture drift and preserve semantic continuity across:

* pipeline execution,
* downstream interoperability,
* substrate generation,
* benchmarking,
* observability,
* and release governance.

Rather than serving as implementation tutorials, these documents define the expected operational and semantic behavior of major VAP components.

---

# Contract Topology

```text
docs/contracts/
├── script/
│   ├── operations/
│   └── substrates/
├── stage/
└── system/
    ├── benchmarking/
    ├── core/
    └── substrates/
```

The contract ecosystem is organized into three primary governance layers:

| Contract Layer | Purpose                                                                            |
| -------------- | ---------------------------------------------------------------------------------- |
| `system/`      | Defines architecture-wide operational and semantic guarantees                      |
| `stage/`       | Defines behavior and outputs for individual pipeline stages                        |
| `script/`      | Defines operational utility workflows and analytical substrate generation behavior |

---

# System Contracts

System contracts govern the architecture-level behavior of VAP and define reproducibility, interoperability, benchmarking, and substrate continuity expectations.

## Core Architecture

| Contract                             | Purpose                                               |
| ------------------------------------ | ----------------------------------------------------- |
| `system/core/vap_system_contract.md` | Canonical architecture contract for the VAP ecosystem |

The system contract defines:

* pipeline scope,
* execution boundaries,
* interoperability guarantees,
* provenance expectations,
* telemetry continuity,
* and downstream substrate generation behavior.

---

## Benchmarking Contracts

| Contract                                                       | Purpose                                                   |
| -------------------------------------------------------------- | --------------------------------------------------------- |
| `system/benchmarking/hg002_benchmarking_component_contract.md` | HG002 benchmarking architecture and validation governance |

These contracts define benchmarking expectations and controlled evaluation semantics for reference-aligned validation workflows.

---

## Substrate Contracts

| Contract                                                        | Purpose                                          |
| --------------------------------------------------------------- | ------------------------------------------------ |
| `system/substrates/cross_assay_figure_substrate_contract.md`    | Figure-generation substrate governance           |
| `system/substrates/stage_12_duckdb_exemplar_export_contract.md` | DuckDB export substrate architecture             |
| `system/substrates/substrate_dimension_summary_contract.md`     | Cohort-scale substrate dimensionality governance |

These contracts govern deterministic generation of analytical evidence substrates used throughout:

* cross-run analysis,
* interoperability validation,
* reviewability assessment,
* and downstream semantic composition workflows.

---

# Stage Contracts

Stage contracts define deterministic operational behavior for major VAP execution stages.

| Contract                     | Scope                                                       |
| ---------------------------- | ----------------------------------------------------------- |
| `stage/stage_08_contract.md` | Semantic interoperability boundary and partition governance |
| `stage/stage_09_contract.md` | Coding interpretability refinement                          |
| `stage/stage_10_contract.md` | Noncoding interpretability refinement                       |
| `stage/stage_11_contract.md` | Prioritization substrate generation                         |
| `stage/stage_12_contract.md` | Validation and reviewability governance                     |
| `stage/stage_13_contract.md` | Final summary artifact emission                             |

These documents define:

* expected inputs and outputs,
* semantic routing behavior,
* interoperability surfaces,
* substrate continuity,
* and downstream readiness guarantees.

## Architectural Importance of Stage 08

`stage_08_contract.md` represents a foundational architectural boundary within VAP.

Stage 08 formalizes the semantic interoperability boundary where annotated variant evidence is deterministically partitioned into interoperable downstream substrates. This stage enables:

* VDB-ready variant substrates,
* RDGP-ready evidence surfaces,
* provenance-linked semantic routing,
* and bounded interpretability escalation workflows.

---

# Script Contracts

Script contracts govern operational utilities and analytical substrate generation workflows external to the core stage execution pipeline.

---

## Operational Script Contracts

| Contract                                                                 | Purpose                                    |
| ------------------------------------------------------------------------ | ------------------------------------------ |
| `script/operations/lightweight_batched_vap_export_contract.md`           | Lightweight cohort export governance       |
| `script/operations/srr_preprocessing_contract.md`                        | SRA preprocessing workflow behavior        |
| `script/operations/vap_bioproject_fastq_acquisition_trilogy_contract.md` | FASTQ acquisition orchestration governance |

These contracts govern deterministic operational workflows supporting:

* cohort acquisition,
* preprocessing,
* infrastructure portability,
* and export continuity.

---

## Analytical Substrate Script Contracts

| Contract                                                               | Purpose                                      |
| ---------------------------------------------------------------------- | -------------------------------------------- |
| `script/substrates/stage12_analytical_batch_export_runner_contract.md` | Batch analytical export substrate generation |

These workflows support deterministic construction of analytical surfaces used for:

* cross-run comparison,
* reviewability assessment,
* interoperability validation,
* and semantic governance analysis.

---

# Recommended Reading Order

For reviewers exploring the VAP governance ecosystem for the first time, the following order is recommended:

1. `system/core/vap_system_contract.md`
2. `stage/stage_08_contract.md`
3. `system/benchmarking/hg002_benchmarking_component_contract.md`
4. `system/substrates/`
5. `stage/`
6. `script/`

This progression moves from high-level architectural governance toward operational and substrate-specific execution behavior.

---

# Contract Governance Philosophy

VAP contracts are designed to preserve:

* deterministic execution behavior,
* semantic continuity,
* provenance integrity,
* interoperability stability,
* and bounded interpretability escalation.

The goal of this governance architecture is not simply reproducibility of execution, but reproducibility of semantic structure and downstream evidence interpretation surfaces.

Contracts therefore function as architectural stabilization mechanisms across:

* execution infrastructure,
* substrate generation,
* benchmarking workflows,
* and downstream interoperability ecosystems.

---

# Relationship to Release Readiness

The VAP contract ecosystem serves as a core release-governance surface for VAP v1.

Contracts are used to:

* reduce architecture drift,
* formalize semantic routing behavior,
* stabilize interoperability guarantees,
* and preserve reviewer-visible operational coherence across repository evolution.

During release preparation, contracts should remain synchronized with:

* implementation behavior,
* pipeline outputs,
* substrate schemas,
* and repository topology.

Stale or orphaned contracts are considered release-surface inconsistencies and should be resolved before formal release tagging.
