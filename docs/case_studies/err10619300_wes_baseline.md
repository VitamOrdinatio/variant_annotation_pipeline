# ERR10619300 WES Baseline Case Study
## Phase 1A Saudi Epilepsy WES Operational Reproducibility Assessment on MARK1

**Repository:** `variant_annotation_pipeline`  
**Branch:** `phase0-logging-foundation`  
**Hardware:** `MARK1 (VandPyMolGPUResearch)`  
**Pipeline Version:** `v1-pre-release`  
**Dataset:** `ERR10619300`  
**Assay Type:** `WES`  

---

# Overview

This case study documents repeated fully instrumented production execution of the Saudi epilepsy WES sample `ERR10619300` on MARK1 infrastructure during VAP Phase 1A telemetry characterization.

Unlike the `ERR10619281` metadata-transition reproducibility assessment, this execution campaign focused specifically on:

- same-patch operational reproducibility
- runtime telemetry stability
- repeated fully instrumented WES execution behavior
- downstream biological-result stability
- cohort-scale execution feasibility

This case study therefore functions as the first formal same-patch WES rerun reproducibility assessment within the VAP ecosystem.

---

# Dataset Background

`ERR10619300` originates from the same Saudi epilepsy WES cohort used for early Phase 1A operational characterization.

The sample was selected because it provided:

- clinically relevant epilepsy WES scale
- manageable runtime economics
- compatibility with repeated MARK1 execution
- an opportunity to evaluate operational reproducibility after provenance-model stabilization

Importantly, both executions occurred after implementation of assay-aware provenance corrections.

This allows the resulting runs to function as a clean same-patch reproducibility pair.

---

# Execution Context

The following executions were performed:

| Run Category | Run ID | Description |
|---|---|---|
| Initial post-patch execution | `run_2026_05_14_164444` | First fully instrumented WES execution |
| Same-patch rerun | `run_2026_05_15_063040` | Repeated fully instrumented execution under stable provenance semantics |

Both runs incorporated:

- assay-aware provenance propagation
- config-driven WES typing
- canonical runtime telemetry
- structured metadata emission
- stage runtime profiling
- lightweight reproducibility infrastructure

No deliberate runtime optimization was introduced between runs.

This preserved trustworthy baseline telemetry conditions.

---

# Reproducibility Objectives

This execution campaign evaluated:

1. Same-patch operational reproducibility
2. Runtime telemetry stability
3. Structural-output reproducibility
4. Biological-result reproducibility
5. Fully instrumented repeated execution behavior

Importantly, this campaign intentionally avoided:

- aggressive runtime optimization
- orchestration changes
- thread-model experimentation
- infrastructure migration

in order to preserve clean repeated execution conditions.

---

# Runtime Telemetry

Observed runtime telemetry for `ERR10619300`:

| Execution | Runtime | Status |
|---|---|---|
| Initial post-patch execution | 4 h 55 m 57 s | Success |
| Same-patch rerun | 4 h 59 m 27 s | Success |

Observed runtime variation was modest and operationally expected.

Observed runtime behavior remained broadly similar across both executions.

Importantly:

- runtime telemetry varied slightly
- timestamps varied
- provenance hashes varied
- run IDs varied

while downstream biological-result structure remained stable.

---

# Reproducibility Findings

## FASTQ Stability

Observed FASTQ pair counts remained identical across both executions:

| Metric | Value |
|---|---:|
| FASTQ R1 reads | 83,673,287 |
| FASTQ R2 reads | 83,673,287 |

---

## Stage 11/12 Stability

Observed downstream prioritization structure remained stable:

| Metric | Value |
|---|---:|
| Stage 11 prioritized rows | 736,468 |
| Stage 12 validation rows | 736,468 |

No evidence of downstream biological-result instability was observed across repeated execution.

---

## Structural Reproducibility

Observed stable structural behavior included:

- Stage 11 row counts
- Stage 12 row counts
- output schemas
- artifact organization
- prioritized candidate structure
- validation-candidate structure

Large-output artifact structure remained stable across repeated fully instrumented execution.

---

## Biological Reproducibility

Observed stable biological-result behavior included:

- stable prioritized variant distributions
- stable validation-candidate distributions
- stable downstream interpretation structure

Current evidence therefore supports strong observational biological-result reproducibility across repeated same-patch WES execution on MARK1.

---

# Runtime Variability vs Biological Stability

One of the most important findings from this execution campaign was the operational distinction between:

- telemetry variability
- biological-result stability

Observed operational variability included:

- runtime differences
- timestamps
- run IDs
- provenance hashes
- lightweight artifact hashes

However:

- Stage 11 output structure remained stable
- Stage 12 output structure remained stable
- prioritized biological interpretation remained stable

This distinction is operationally important because it demonstrates that repeated production execution can exhibit normal telemetry variability without implying downstream biological instability.

This distinction becomes increasingly important during future cohort-scale execution where operational telemetry naturally fluctuates across runs.

---

# Operational Findings

This execution campaign further validated several operational maturity improvements within VAP:

- repeated fully instrumented WES execution
- reusable telemetry infrastructure
- detached `tmux` execution workflows
- structured runtime profiling
- assay-aware provenance propagation
- lightweight reproducibility comparison tooling
- reusable MARK operational harnesses

Additionally, this campaign reinforced the observation that Saudi epilepsy WES runtime economics were substantially more favorable than earlier HG002 WGS assumptions.

Observed WES runtime remained approximately:

```text
~5 hours/sample
```

This materially improves projected feasibility for future epilepsy cohort-scale execution on MARK-class infrastructure.

---

# Biological / Interpretive Observations

Exploratory post-run probing identified variants intersecting several loci with established epilepsy or mitochondrial relevance, including:

- `SYNGAP1`
- `NPRL3`
- `POLG`
- `TWNK`
- `MFN2`
- `DNA2`

Importantly, this case study does **not** claim enrichment or disease association.

However, the observed outputs demonstrate that VAP-generated prioritized candidate streams may provide useful substrate for future:

- RDGP evaluation
- GSC overlay integration
- VDB persistence
- cohort-level recurrence analysis

This observation represents an important ecosystem milestone because it demonstrates that provenance-controlled epilepsy WES ingestion streams are now operationally achievable within VAP.

---

# Generated Artifacts

This execution campaign generated:

```text
metadata/runtime_profile.tsv
metadata/run_metadata.json
metadata/run_fingerprint.json
metadata/stage_summaries/
processed/stage_11_prioritized_variants.tsv
processed/stage_12_validation_candidates.tsv
processed/stage_13_run_report.md
```

Additional comparison infrastructure developed during this campaign included:

```text
scripts/analysis/compare_vap_runs.py
scripts/mark/mark_compare_err10619300_runs.sh
```

These tools support lightweight reproducibility assessment without requiring transfer of large BAM/VCF artifacts from MARK infrastructure.

---

# Limitations

Current limitations include:

- conclusions remain observational rather than statistically modeled
- cross-node reproducibility remains untested
- byte-identical reproducibility has not yet been formally evaluated
- long-term cache effects remain unknown
- filesystem I/O variability remains incompletely characterized

Additionally, biological relevance of observed candidate loci has not yet been evaluated using formal cohort-level enrichment frameworks.

---

# Ecosystem Implications

This case study further strengthens the operational foundation of the broader VitamOrdinatio ecosystem.

VAP is now capable of generating:

- provenance-controlled variant evidence
- telemetry-characterized execution outputs
- reproducibility-aware candidate streams
- structured downstream interpretation artifacts

under repeated same-patch production execution conditions.

These outputs are expected to become foundational upstream inputs for:

- VDB
- RDGP
- GSC overlay integration
- future cohort-level convergence analysis

Importantly, this campaign demonstrates that VAP-generated outputs are beginning to transition from static execution artifacts toward reusable persistent evidence streams within the broader ecosystem architecture.

---

# Preliminary Conclusions

The `ERR10619300` execution campaign demonstrated:

- stable same-patch WES execution behavior
- stable downstream biological-result structure
- stable fully instrumented telemetry behavior
- reproducibility-oriented operational infrastructure
- operationally tractable WES runtime economics
- feasibility of repeated provenance-controlled epilepsy WES execution on MARK-class infrastructure

Most importantly, this campaign established the first clean same-patch operational reproducibility baseline within the VAP ecosystem.

This now complements the:

- metadata-transition reproducibility observations from `ERR10619281`
- historical HG002 operational baseline comparisons

and further strengthens the foundation for future:

- VDB persistence
- RDGP ingestion
- GSC overlay integration
- and cohort-scale epilepsy WES execution.