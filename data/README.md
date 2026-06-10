# `data/`

Persistent operational substrates, lightweight orchestration surfaces, and semantic coordination artifacts for VAP.

---

# Overview

The `data/` directory contains lightweight operational artifacts that support deterministic execution, semantic coordination, interoperability workflows, and reproducible development within the Variant Annotation Pipeline (VAP).

Unlike large genomic payloads (FASTQ/BAM/VCF/WGS-scale TSVs), the artifacts contained here are intentionally lightweight, versionable, and repository-resident.

These files primarily function as:

* orchestration manifests,
* semantic overlay seeds,
* fixture datasets,
* coordination surfaces,
* lightweight transfer definitions,
* and deterministic execution substrates.

---

# Semantic Infrastructure Concepts

VAP distinguishes between several operational artifact classes.

| Concept                 | Meaning                                                                                           |
| ----------------------- | ------------------------------------------------------------------------------------------------- |
| Payloads                | Large biological evidence artifacts such as FASTQ, BAM, VCF, and cohort-scale annotation tables   |
| Substrates              | Structured semantic evidence surfaces derived from payloads                                       |
| Coordination Surfaces   | Lightweight artifacts used to coordinate deterministic execution and interoperability             |
| Orchestration Manifests | TSV/YAML control-plane artifacts governing execution, extraction, routing, or transfer operations |
| Payload-plane           | High-volume biological evidence movement and transformation                                       |
| Control-plane           | Lightweight deterministic governance and orchestration infrastructure                             |

VAP intentionally versions control-plane infrastructure while excluding large payload-plane artifacts from repository storage.

This distinction enables:

* reproducible orchestration,
* deterministic extraction workflows,
* lightweight portability,
* semantic continuity,
* and scalable interoperability development.

---

# Data Topology

```text
data/
├── example/
├── interim/
├── processed/
├── raw/
└── reference/
```

| Directory    | Purpose                                                                |
| ------------ | ---------------------------------------------------------------------- |
| `example/`   | Lightweight fixture datasets for rapid smoketesting and development    |
| `interim/`   | Runtime-generated transient execution artifacts (gitignored)           |
| `processed/` | Runtime-generated processed outputs (gitignored)                       |
| `raw/`       | Runtime-generated raw payload ingestion surfaces (gitignored)          |
| `reference/` | Persistent operational reference substrates and orchestration surfaces |

---

# Why Large Payloads Are Excluded

VAP intentionally excludes large genomic payloads from repository version control.

Examples include:

* FASTQ files,
* BAM files,
* CRAM files,
* cohort-scale VCFs,
* annotated whole-genome TSVs.

These artifacts are:

* extremely large,
* execution-specific,
* compute-environment dependent,
* and unsuitable for repository-scale version governance.

Instead, VAP versions:

* orchestration logic,
* semantic governance surfaces,
* manifests,
* telemetry,
* schemas,
* fixtures,
* and interoperability substrates.

This permits deterministic reproducibility without repository-scale payload inflation.

---

# `data/example/`

The `example/` directory contains lightweight fixture datasets used for:

* smoketesting,
* telemetry validation,
* regression testing,
* rapid iteration,
* and deterministic development workflows.

This layer was critical during VAP development because whole-genome execution on MARK HPC infrastructure can require many hours of runtime.

Example fixtures permit rapid validation of:

* stage execution,
* metadata emission,
* runtime telemetry,
* schema continuity,
* and post-VEP orchestration behavior.

Representative artifacts include:

| Artifact                         | Purpose                                              |
| -------------------------------- | ---------------------------------------------------- |
| `example_annotated_variants.tsv` | Lightweight annotated substrate for post-VEP testing |
| `example_annotated_variants.vcf` | Minimal VCF fixture                                  |
| `example_gene_set_epilepsy.tsv`  | Overlay seed example                                 |
| `example_gene_set_mito.tsv`      | Overlay seed example                                 |

---

# `data/reference/`

The `reference/` directory contains persistent operational substrates used by VAP orchestration and downstream interoperability workflows.

These artifacts function primarily as lightweight control-plane infrastructure.

---

# Transitional Overlay Architecture

VAP currently supports lightweight semantic overlay integration through repository-resident gene overlay substrates.

This architecture is intentionally transitional.

At present:

```text
VAP → lightweight overlay bridge → future interoperability ecosystem
```

rather than:

```text
VAP → final semantic destination
```

The current overlay model enables:

* deterministic semantic enrichment,
* targeted SQL slicing,
* lightweight consensus overlays,
* and interoperability experimentation

prior to full VDB-mediated ecosystem routing.

Future repository interoperability will increasingly transition toward:

```text
VAP → VDB → GSC / RDGP / RSP
```

governed semantic routing infrastructure.

---

## Current Transitional Semantic Layering

![VAP to GSC Consensus Layering Workflow](../docs/architecture/conceptual/vap_to_gsc_consensus_layering_workflow.png)

The current lightweight overlay architecture permits VAP outputs to participate in downstream biological contextualization workflows before the full repository ecosystem is simultaneously operational.

Examples include:

* EPI25 overlays,
* MitoCarta overlays,
* targeted consensus enrichment,
* post-VAP SQL substrate slicing.

These overlays are currently mediated through lightweight repository-resident substrates located in:

```text
data/reference/gene_lists/
```

Once VDB becomes operational, these static overlay bridges are expected to transition toward governed interoperability routing across repository interfaces.

---

# `data/reference/gene_lists/`

Contains lightweight semantic overlay substrates used for post-VAP contextualization workflows.

Current examples include:

| Artifact                         | Purpose                                 |
| -------------------------------- | --------------------------------------- |
| `epi25_vap_overlay_seed.tsv`     | Epilepsy-focused overlay substrate      |
| `mitocarta_vap_overlay_seed.tsv` | Mitochondrial-focused overlay substrate |

These substrates currently support:

* overlay intersection workflows,
* downstream prioritization,
* targeted semantic enrichment,
* and cross-run interpretability analyses.

---

# Manifest-Oriented Orchestration

A major architectural characteristic of VAP is deterministic manifest-oriented orchestration.

Rather than hardcoding execution topology, many workflows are governed through lightweight TSV manifests.

This enables:

* reproducible extraction,
* deterministic routing,
* scalable orchestration,
* lightweight transfer coordination,
* and reproducible cohort processing.

---

# `data/reference/lightweight_transfer/`

Supports lightweight transfer extraction workflows.

Used primarily by:

```text
scripts/mark/export_lightweight_vap_runs.py
```

This system permits extraction of lightweight operational artifacts from completed MARK executions for downstream review and analysis on external systems such as `sys76`.

Manifest-driven coordination permits deterministic transfer selection without requiring full payload migration.

---

# `data/reference/sra_support/`

Contains orchestration surfaces supporting controlled SRA acquisition workflows.

This infrastructure supports:

* BioProject harvesting,
* run topology analysis,
* depth-aware cohort selection,
* reproducible download coordination,
* and polite external resource usage.

Primary scripts include:

```text
scripts/resources/download_selected_fastqs_polite.sh
scripts/resources/harvest_bioproject_run_manifest.sh
scripts/resources/select_bioproject_runs_by_depth.sh
```

The associated manifests and logs preserve provenance continuity for cohort construction workflows.

---

# `data/reference/stage12_analytical_batch_exports/`

Supports deterministic SQL-oriented extraction workflows from large Stage 12 validation substrates.

Used primarily by:

```text
scripts/analysis/run_stage12_duckdb_exports_from_manifest.py
```

This architecture enables lightweight analytical harvesting from large validation surfaces without requiring direct manual interaction with full cohort-scale TSV payloads.

Manifest-driven exports preserve:

* reproducibility,
* deterministic extraction,
* and scalable analytical coordination.

---

# Runtime Execution Surfaces

The following directories are runtime-oriented payload surfaces and are intentionally gitignored:

| Directory    | Purpose                           |
| ------------ | --------------------------------- |
| `raw/`       | Raw payload ingestion surfaces    |
| `interim/`   | Intermediate execution substrates |
| `processed/` | Processed execution outputs       |

These directories exist primarily to support local execution topology and reproducible runtime organization.

They are not intended to function as repository-scale payload storage.

---

# Architectural Summary

The `data/` directory functions as lightweight semantic infrastructure supporting:

* deterministic orchestration,
* manifest-oriented execution governance,
* interoperability experimentation,
* substrate continuity,
* semantic overlay coordination,
* and scalable evidence routing.

Rather than serving merely as static storage, this layer increasingly operates as a lightweight control-plane enabling reproducible semantic infrastructure workflows across the broader VAP ecosystem.
