# Roadmap

This roadmap reflects planned development priorities and may evolve as repositories mature and framework standards improve.

## Overview

This repository is part of a broader effort to build a **modular, reproducible, and clinically-relevant bioinformatics ecosystem** for variant analysis, gene prioritization, and disease-focused interpretation.

Development proceeds in stages, with emphasis on:

* reproducibility
* clarity of pipeline design
* alignment with real-world clinical genomics workflows

---

## Immediate Next Step

### Stabilization and Framework Consolidation

Following the release of `variant_annotation_pipeline` v1.0:

* Pause major feature development
* Consolidate and refine the underlying framework:

  * `reproducible_pipeline_framework`
  * `AI_Workspace` (governance, documentation, agent coordination)
* Standardize:

  * pipeline conventions
  * documentation structure
  * reproducibility practices

This phase ensures that future repositories build on a stable foundation.

---

## Near-Term Development

### 1. Gene Set Consensus Layer

**Repository:** `gene_set_consensus`

* Aggregate and harmonize gene sets from:

  * curated databases
  * literature sources
  * disease-specific resources
* Provide reusable overlays for downstream analysis
* Enable integration into variant interpretation pipelines

---

### 2. Variant Annotation Pipeline Enhancements

**Repository:** `variant_annotation_pipeline`

Planned improvements include:

* integration of gene set overlays
* expanded annotation layers
* improved prioritization strategies

---

### 3. Variant Database Layer

**Repository:** `variant_database`

* Develop a structured storage layer using:

  * SQL
  * SQLAlchemy
* Support:

  * persistent variant storage
  * queryable annotation results
  * integration with upstream pipelines

---

## Mid-Term Development

### RNA-seq Pipeline

**Repository:** `rnaseq_pipeline`

* Extend the framework to transcriptomic workflows
* Enable differential expression and downstream analysis
* Maintain consistency with existing pipeline conventions

---

### Rare Disease Gene Prioritization

**Repository:** `rare_disease_gene_prioritization`

* Combine:

  * variant annotation outputs
  * gene set overlays
  * disease-specific knowledge
* Develop prioritization strategies for candidate gene identification

---

### PICU Data Harmonization

**Repository:** `picu_harmonization`

* Develop tools for integrating clinical and biological datasets
* Focus on:

  * schema standardization
  * data cleaning and normalization
  * downstream compatibility with analysis pipelines

---

## Longer-Term Directions

* Integration of AI-assisted prediction tools
* Incorporation of external resources (e.g., GTR)
* Cross-repository interoperability via shared framework standards
* Expansion toward clinically-oriented decision support workflows

---

## Philosophy

This roadmap is intentionally ambitious.

The focus is not on rapid feature accumulation, but on building a **coherent, extensible system** where:

* each repository serves a clear role
* components integrate cleanly
* workflows remain reproducible and interpretable

Priorities may evolve as the framework matures and new insights are gained.
