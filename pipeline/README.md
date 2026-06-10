# VAP Pipeline Execution Ecosystem (`pipeline/`)

The `pipeline/` namespace contains the reusable stage-oriented biological processing architecture of the Variant Annotation Pipeline (VAP).

This namespace implements the core execution stages responsible for transforming:

```text
raw sequencing evidence
```

into:

```text
interoperable semantic evidence substrates.
```

Unlike:

* `src/` — orchestration and telemetry infrastructure
* `scripts/` — operational utilities and analytical helpers

the `pipeline/` namespace contains the reusable biological and semantic processing stages forming the operational core of VAP execution.

---

# Pipeline Philosophy

The VAP pipeline ecosystem emphasizes:

* deterministic stage transitions,
* provenance continuity,
* semantic interoperability,
* bounded interpretability refinement,
* and reproducible substrate generation.

Importantly, the pipeline architecture intentionally avoids treating variant annotation as a terminal endpoint.

Instead, the stage ecosystem progressively transforms evidence through:

* normalization,
* annotation,
* semantic partitioning,
* interpretability refinement,
* prioritization,
* validation,
* and summary abstraction.

This philosophy increasingly positions VAP as:

```text
semantic evidence infrastructure
```

rather than simply:

```text
variant annotation tooling.
```

---

# Pipeline Topology

```text
pipeline/
├── stage_01_load_data.py
├── stage_02_align_data.py
├── stage_03_process_bam.py
├── stage_04_qc_aligned_reads.py
├── stage_05_call_variants.py
├── stage_06_normalize_vcf.py
├── stage_07_annotate_variants.py
├── stage_08_filter_and_partition.py
├── stage_09_interpret_coding.py
├── stage_10_interpret_noncoding.py
├── stage_11_prioritize_variants.py
├── stage_12_validate_variants.py
└── stage_13_write_summary.py
```

The stage architecture is intentionally decomposed into:

| Layer                              | Stages | Purpose                                                              |
| ---------------------------------- | ------ | -------------------------------------------------------------------- |
| Upstream substrate generation      | 01–07  | sequencing, alignment, variant generation, normalization, annotation |
| Semantic interoperability boundary | 08     | semantic partitioning and downstream substrate emission              |
| Interpretability refinement        | 09–13  | coding/noncoding refinement, prioritization, validation, reporting   |

---

# Upstream Variant Substrate Generation

Stages 01–07 establish the normalized upstream evidence substrate used throughout downstream semantic refinement workflows.

---

## Stage 01 — Data Loading

| Stage                   | Purpose                                 |
| ----------------------- | --------------------------------------- |
| `stage_01_load_data.py` | sequencing ingestion and initialization |

This stage governs:

* FASTQ ingestion,
* input validation,
* execution initialization,
* and upstream provenance establishment.

---

## Stage 02 — Alignment

| Stage                    | Purpose                 |
| ------------------------ | ----------------------- |
| `stage_02_align_data.py` | alignment orchestration |

This stage governs:

* reference alignment,
* alignment execution,
* and BAM generation workflows.

---

## Stage 03 — BAM Processing

| Stage                     | Purpose                        |
| ------------------------- | ------------------------------ |
| `stage_03_process_bam.py` | BAM processing and preparation |

This stage governs:

* BAM refinement,
* sorting,
* indexing,
* and downstream-ready alignment preparation.

---

## Stage 04 — Alignment QC

| Stage                          | Purpose                      |
| ------------------------------ | ---------------------------- |
| `stage_04_qc_aligned_reads.py` | aligned-read quality control |

This stage performs:

* alignment QC,
* coverage assessment,
* and execution-quality evaluation.

---

## Stage 05 — Variant Calling

| Stage                       | Purpose                   |
| --------------------------- | ------------------------- |
| `stage_05_call_variants.py` | variant calling workflows |

This stage transforms processed alignment substrates into raw variant evidence.

---

## Stage 06 — VCF Normalization

| Stage                       | Purpose                            |
| --------------------------- | ---------------------------------- |
| `stage_06_normalize_vcf.py` | representation-aware normalization |

This stage governs:

* normalization,
* decomposition,
* left-alignment,
* and reproducibility-aware variant representation stabilization.

This normalization layer later became especially important for:

* HG002 benchmarking,
* representation-aware comparison,
* and interoperability continuity.

---

## Stage 07 — Variant Annotation

| Stage                           | Purpose                             |
| ------------------------------- | ----------------------------------- |
| `stage_07_annotate_variants.py` | annotation and enrichment workflows |

This stage governs:

* annotation integration,
* functional consequence enrichment,
* population-frequency integration,
* and preliminary interpretability layering.

---

# Stage 08 — Semantic Interoperability Boundary

| Stage                              | Purpose                                                         |
| ---------------------------------- | --------------------------------------------------------------- |
| `stage_08_filter_and_partition.py` | semantic partitioning and interoperability substrate generation |

Stage 08 represents the major architectural boundary within VAP.

This stage performs:

* semantic partitioning,
* coding/noncoding decomposition,
* interoperability preparation,
* reviewability-aware routing,
* and downstream substrate generation.

Outputs generated here become foundational infrastructure for:

* RDGP,
* VDB,
* downstream semantic governance workflows,
* and future cross-modal interoperability systems.

Importantly:

```text
Stage 08 governs evidence organization rather than simplistic evidence elimination.
```

This distinction is one of the defining architectural properties of VAP.

---

# Semantic Interpretability Refinement

Stages 09–13 perform downstream evidence refinement and reporting abstraction.

---

## Stage 09 — Coding Interpretation

| Stage                          | Purpose                    |
| ------------------------------ | -------------------------- |
| `stage_09_interpret_coding.py` | coding evidence refinement |

This stage performs:

* coding interpretation,
* evidence prioritization,
* and coding consequence contextualization.

---

## Stage 10 — Noncoding Interpretation

| Stage                             | Purpose                       |
| --------------------------------- | ----------------------------- |
| `stage_10_interpret_noncoding.py` | noncoding evidence refinement |

This stage governs:

* noncoding contextualization,
* regulatory interpretation,
* and downstream semantic refinement.

---

## Stage 11 — Prioritization

| Stage                             | Purpose                             |
| --------------------------------- | ----------------------------------- |
| `stage_11_prioritize_variants.py` | prioritization substrate generation |

This stage constructs:

* prioritization surfaces,
* reviewability-oriented evidence layers,
* and downstream-ready semantic prioritization substrates.

---

## Stage 12 — Validation

| Stage                           | Purpose                                 |
| ------------------------------- | --------------------------------------- |
| `stage_12_validate_variants.py` | validation and reviewability governance |

This stage governs:

* validation-oriented refinement,
* reviewability escalation,
* and semantic governance hardening.

This layer became especially important throughout:

* cross-run governance studies,
* semantic reproducibility analyses,
* and interoperability-oriented validation workflows.

---

## Stage 13 — Summary Emission

| Stage                       | Purpose                                         |
| --------------------------- | ----------------------------------------------- |
| `stage_13_write_summary.py` | summary abstraction and final artifact emission |

This stage generates:

* summary abstractions,
* provenance-linked reporting layers,
* and downstream evidence products.

---

# Relationship to `src/`

The `pipeline/` namespace contains reusable stage-oriented biological processing logic.

The `src/` namespace instead governs:

* orchestration,
* telemetry,
* runtime coordination,
* and execution governance.

This separation preserves:

| Concern                 | Namespace   |
| ----------------------- | ----------- |
| biological processing   | `pipeline/` |
| execution orchestration | `src/`      |

This architectural decomposition became increasingly important during:

* observability expansion,
* reproducibility hardening,
* and telemetry maturation.

---

# Relationship to Contracts

The stage ecosystem is formally governed by:

* `docs/contracts/stage/`

These contracts define:

* stage expectations,
* interoperability guarantees,
* semantic routing behavior,
* and downstream substrate continuity.

The implementation within `pipeline/` operationally realizes those governance surfaces.

---

# Relationship to Case Studies

The reusable pipeline ecosystem directly enabled:

| Case Study       | Contribution                                       |
| ---------------- | -------------------------------------------------- |
| HG002            | benchmark-aware normalization and validation       |
| ERR10619281      | deterministic rerun reproducibility                |
| ERR10619300      | semantic governance and partitioning analyses      |
| 12-SRA cross-run | cross-run interoperability and topology continuity |

In particular:

* Stage 06 normalization,
* Stage 08 semantic partitioning,
* and Stages 09–12 interpretability refinement

became foundational infrastructure for later governance and interoperability analyses.

---

# Operational Maturity Themes

The `pipeline/` ecosystem consistently emphasizes:

* deterministic stage transitions,
* provenance continuity,
* semantic governance,
* interoperability-oriented evidence generation,
* bounded interpretability refinement,
* and reproducibility-aware execution.

Collectively, these stages demonstrate that VAP evolved beyond:

```text
annotation-centric workflows
```

into:

```text
governed semantic evidence refinement infrastructure.
```

---

# Recommended Reading Order

Most reviewers should begin with:

1. `stage_06_normalize_vcf.py`
2. `stage_07_annotate_variants.py`
3. `stage_08_filter_and_partition.py`
4. `stage_11_prioritize_variants.py`
5. `stage_12_validate_variants.py`

This sequence progressively exposes:

* representation-aware normalization,
* evidence enrichment,
* semantic partitioning,
* prioritization,
* and validation-oriented governance.

---

# Final Positioning

The `pipeline/` namespace demonstrates that VAP matured through:

* layered stage decomposition,
* interoperability-oriented evidence partitioning,
* deterministic semantic refinement,
* and reproducibility-aware biological processing.

These stages therefore function as:

```text
the reusable biological execution substrate
```

underlying the broader semantic evidence ecosystem of VAP.
