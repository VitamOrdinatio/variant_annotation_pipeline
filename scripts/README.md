# VAP Script Ecosystem

The `scripts/` namespace contains the operational utility layer of the Variant Annotation Pipeline (VAP).

Unlike the core pipeline implementation located within:

* `src/`
* `pipeline/`
* and governed stage infrastructure,

the `scripts/` ecosystem intentionally contains:

```text
bounded operational utilities,
analytical helpers,
execution wrappers,
resource setup workflows,
and one-off infrastructure tooling.
```

These scripts support:

* benchmarking,
* substrate generation,
* telemetry harvesting,
* figure rendering,
* cohort preparation,
* cross-run analysis,
* and operational reproducibility workflows.

---

# Script Philosophy

The VAP script ecosystem intentionally prioritizes:

* operational pragmatism,
* deterministic outputs,
* reproducible substrate generation,
* infrastructure portability,
* and analytical decomposability.

Importantly:

```text
scripts are intentionally allowed to be task-specific and operationally bounded.
```

Not every script is intended to evolve into reusable generalized infrastructure.

Instead, many scripts represent:

* controlled operational probes,
* substrate builders,
* analysis orchestrators,
* or reproducible one-off evidence-generation utilities.

This design philosophy preserves:

* repository agility,
* analytical transparency,
* and operational traceability

without forcing premature abstraction.

---

# Script Topology

```text
scripts/
├── analysis/
├── benchmarking/
├── configs/
├── data_prep/
├── environment/
├── figures/
├── mark/
├── orchestration/
├── resources/
└── tools/
```

| Namespace        | Purpose                                                          |
| ---------------- | ---------------------------------------------------------------- |
| `analysis/`      | analytical substrate generation and cross-run evidence workflows |
| `benchmarking/`  | HG002 benchmarking orchestration                                 |
| `configs/`       | figure and analysis configuration substrates                     |
| `data_prep/`     | sequencing and dataset preparation                               |
| `environment/`   | environment validation and setup                                 |
| `figures/`       | case-study figure rendering                                      |
| `mark/`          | MARK HPC execution workflows                                     |
| `orchestration/` | top-level orchestration setup                                    |
| `resources/`     | external reference and annotation acquisition                    |
| `tools/`         | pipeline dependency installation and validation                  |

---

# Analysis Ecosystem

The `analysis/` namespace contains one of the largest operational substrate-generation layers within VAP.

These scripts support deterministic generation of:

* semantic governance surfaces,
* telemetry summaries,
* interoperability analyses,
* reviewability metrics,
* and cross-run evidence abstractions.

Representative workflows include:

| Script Class                                  | Purpose                                               |
| --------------------------------------------- | ----------------------------------------------------- |
| `build_*`                                     | deterministic substrate aggregation and summarization |
| `append_*`                                    | semantic enrichment and annotation augmentation       |
| `compare_vap_runs.py`                         | cross-run semantic reproducibility analysis           |
| `harvest_vap_case_metrics.py`                 | cohort-scale evidence harvesting                      |
| `export_stage12_duckdb_exploration.py`        | analytical substrate export                           |
| `run_stage12_duckdb_exports_from_manifest.py` | batch export orchestration                            |

This namespace directly enabled the later:

* HG002 benchmarking ecosystem,
* ERR10619281 semantic stability analysis,
* ERR10619300 semantic-governance studies,
* and 12-SRA cross-run governance workflows.

---

# Benchmarking Ecosystem

The `benchmarking/` namespace governs benchmark-aware validation workflows.

| Script                         | Purpose                                               |
| ------------------------------ | ----------------------------------------------------- |
| `run_hg002_happy_benchmark.py` | representation-aware HG002 benchmarking orchestration |

This infrastructure supports:

* `hap.py` benchmarking,
* representation-aware normalization,
* namespace mediation,
* and benchmark-governed validation workflows.

These scripts contributed directly to the HG002 case-study ecosystem.

---

# Configuration Ecosystem

The `configs/` namespace contains deterministic configuration substrates used throughout:

* figure generation,
* semantic governance analyses,
* interoperability rendering,
* and case-study workflows.

This namespace intentionally preserves:

* reproducible figure inputs,
* parameter continuity,
* and configuration traceability.

---

# Figure Generation Ecosystem

The `figures/` namespace governs deterministic rendering of case-study visual infrastructure.

Representative figure workflows include:

| Script                                                          | Purpose                                 |
| --------------------------------------------------------------- | --------------------------------------- |
| `generate_case_study_f1_reproducibility_summary.py`             | deterministic rerun visualization       |
| `generate_case_study_f2_runtime_observability_profile.py`       | runtime telemetry visualization         |
| `generate_case_study_f3a_deterministic_evidence_lineage.py`     | semantic lineage visualization          |
| `generate_case_study_f3b_semantic_branching.py`                 | semantic branching topology             |
| `generate_case_study_f4_semantic_categories.py`                 | semantic compression visualization      |
| `generate_case_study_f5_stage08_interoperability_substrates.py` | Stage 08 interoperability visualization |

Importantly:

```text
many VAP figures are generated deterministically from analytical substrates rather than manually assembled.
```

This reinforces:

* reproducibility,
* provenance continuity,
* and governance transparency.

---

# MARK Execution Ecosystem

The `mark/` namespace contains HPC-oriented execution workflows associated with the MARK execution environment.

These scripts support:

* staged checkpoint execution,
* HG002 benchmarking,
* WES/WGS baseline execution,
* lightweight export workflows,
* substrate generation,
* and execution reproducibility.

Representative workflows include:

| Script Class | Purpose                                |
| ------------ | -------------------------------------- |
| `mark_run_*` | deterministic stage execution wrappers |
| `build_*`    | cohort-scale substrate generation      |
| `export_*`   | lightweight evidence export workflows  |

This namespace reflects the operational reality that VAP matured through:

```text
real HPC execution infrastructure
```

rather than exclusively local lightweight experimentation.

---

# Resource & Environment Ecosystem

The `resources/`, `environment/`, and `tools/` namespaces govern operational infrastructure setup.

These workflows support:

* annotation-resource acquisition,
* reference setup,
* GIAB benchmarking resources,
* dependency installation,
* and environment validation.

Representative infrastructure includes:

| Namespace      | Purpose                                      |
| -------------- | -------------------------------------------- |
| `resources/`   | external biological resource acquisition     |
| `environment/` | Python environment validation                |
| `tools/`       | dependency installation and pipeline tooling |

These scripts emphasize:

* infrastructure reproducibility,
* operational portability,
* and controlled environment initialization.

---

# Relationship to Contracts

Many operationally important scripts are governed by contracts located within:

* `docs/contracts/script/`

These contracts formalize:

* execution expectations,
* substrate guarantees,
* interoperability continuity,
* and analytical export behavior.

The script ecosystem therefore balances:

```text
operational flexibility
```

with:

```text
governed reproducibility.
```

---

# Relationship to Case Studies

The script ecosystem directly generated many substrates later surfaced throughout:

* HG002 benchmarking,
* semantic reproducibility studies,
* interoperability analyses,
* and cross-run governance case studies.

Importantly, many later public-facing artifacts originated from:

* deterministic analytical builders,
* substrate aggregators,
* telemetry harvesters,
* and figure-generation workflows contained here.

---

# Operational Maturity Themes

The script ecosystem consistently emphasizes:

* reproducible evidence generation,
* analytical decomposition,
* telemetry-aware execution,
* provenance continuity,
* interoperability-oriented substrate generation,
* and deterministic figure rendering.

Collectively, these scripts reveal how VAP evolved operationally through:

* iterative execution,
* governed analysis generation,
* and reproducible semantic evidence construction.

---

# Recommended Reading Order

Most reviewers should begin with:

1. `benchmarking/run_hg002_happy_benchmark.py`
2. `analysis/compare_vap_runs.py`
3. `analysis/harvest_vap_case_metrics.py`
4. `figures/README.md`
5. `mark/README.md`

This sequence progressively exposes:

* benchmarking infrastructure,
* reproducibility analysis,
* evidence harvesting,
* deterministic figure generation,
* and HPC execution orchestration.

---

# Final Positioning

The `scripts/` ecosystem demonstrates that VAP matured through:

* operational execution,
* deterministic analytical generation,
* substrate-oriented engineering,
* telemetry-aware workflows,
* and reproducible evidence construction.

These scripts therefore function as:

```text
operational infrastructure utilities
```

supporting the broader semantic evidence ecosystem of VAP without forcing unnecessary abstraction of every analytical workflow.
