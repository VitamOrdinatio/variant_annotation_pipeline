# WES Epilepsy Experimental Design

## Purpose

This experiment documents the design and rationale for the Variant Annotation Pipeline (VAP) evaluation on a representative subset of epilepsy whole-exome sequencing (WES) specimens drawn from **BioProject `PRJEB57558`**.

Rather than processing all 144 individuals in the BioProject during VAP v1.0 development, a scientifically representative subset of **12 epilepsy WES samples** was selected to evaluate pipeline correctness, reproducibility, semantic stability, and preservation behavior across heterogeneous sequencing depths.

---

## Experimental Objectives

Primary objectives were to evaluate whether VAP could:

- execute reproducibly across independent epilepsy WES specimens;
- preserve deterministic evidence throughout all pipeline stages;
- produce stable review-ready semantic surfaces;
- remain robust across heterogeneous sequencing depths;
- emit lossless TEP-VAP artifacts suitable for downstream consumers.

A secondary objective was to establish a reusable epilepsy corpus for downstream VDB and RDGP development.

---

## Study Design

### Source cohort

- **BioProject:** `PRJEB57558`
- **Sequencing strategy:** Human paired-end Whole Exome Sequencing (WES)
- **Total BioProject size:** 144 epilepsy patients

### Experimental subset

Twelve specimens were intentionally selected across the sequencing-depth distribution.

Depth categories:

- **q1** — highest read counts
- **median** — intermediate read counts
- **q3** — lowest read counts

This stratification allowed pipeline behavior to be evaluated under varying substrate complexity rather than only high-quality datasets.

---

## Selected Specimens

| SRA | Depth |
|---|---|
| ERR10619203 | q3 |
| ERR10619207 | q3 |
| ERR10619208 | median |
| ERR10619212 | q1 |
| ERR10619225 | q3 |
| ERR10619230 | q3 |
| ERR10619241 | q1 |
| ERR10619281 | median |
| ERR10619285 | median |
| ERR10619300 | median |
| ERR10619309 | q1 |
| ERR10619330 | q1 |

Each specimen was processed independently through the complete VAP workflow.

---

## Cross-System Reproducibility

The same twelve specimens were processed on two independent compute environments.

### MARK

Initial production execution and architecture validation.

### sys76

Independent replication of the complete execution corpus using the modernized VAP implementation.

This enabled comparison of:

- stage completion;
- deterministic routing;
- semantic preservation;
- emitted artifacts;
- TEP-VAP transport fidelity;
- cross-platform reproducibility.

---

## Principal Scientific Questions

The study was designed to answer:

1. Are reviewable candidate densities stable across heterogeneous sequencing depths?
2. Does sequencing depth materially influence candidate escalation?
3. Are review-ready semantic surfaces reproducible?
4. Are Tier 1 and Tier 2 candidate structures preserved consistently?
5. Are clinically supported coding candidates retained across runs?
6. Does semantic governance constrain reviewability appropriately?
7. Are execution lineage and provenance deterministic across repeated executions?
8. Can VAP generate identical preservation surfaces on independent compute infrastructure?

---

## Expected Deliverables

The experiment produces:

- deterministic stage outputs;
- genotype-aware observations;
- review-ready candidate surfaces;
- cross-run comparison tables;
- semantic governance metrics;
- telemetry summaries;
- TEP-VAP preservation artifacts.

These artifacts collectively form the producer corpus used for VDB ingestion and later RDGP development.

---

## Success Criteria

The experiment is considered successful when:

- all twelve WES specimens complete successfully;
- deterministic behavior is maintained across depth categories;
- preservation boundaries exhibit no unexplained evidence loss;
- semantic routing remains stable;
- provenance and lineage artifacts validate successfully;
- identical scientific conclusions are reproducible across MARK and sys76 implementations;
- emitted TEP-VAP artifacts preserve producer identity and evidence fidelity.

---

## Scientific Scope

This study is an engineering validation and evidence-preservation experiment.

It is **not** intended to perform population-level epilepsy association testing, estimate disease prevalence, or infer causal mechanisms.

Instead, the objective is to demonstrate that VAP provides a deterministic, reproducible, provenance-preserving computational substrate for epilepsy whole-exome sequencing that can be reliably consumed by downstream systems such as VDB and RDGP.

## Intended Scientific Description

> A depth-stratified epilepsy whole-exome sequencing execution and reproducibility study demonstrating deterministic evidence preservation, semantic governance, and transport-ready TEP-VAP generation across independent computational environments.
