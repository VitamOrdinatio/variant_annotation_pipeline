# ERR10619281 Reproducibility Case Study
## Phase 1A Saudi Epilepsy WES Reproducibility Assessment on MARK1

**Repository:** `variant_annotation_pipeline`  
**Branch:** `phase0-logging-foundation`  
**Hardware:** `MARK1 (VandPyMolGPUResearch)`  
**Pipeline Version:** `v1-pre-release`  
**Dataset:** `ERR10619281`  
**Assay Type:** `WES`  

---

# Overview

This case study documents repeated production execution of the Saudi epilepsy WES sample `ERR10619281` using VAP Phase 1A telemetry instrumentation on MARK1 infrastructure.

The primary goals of this execution campaign were:

- evaluate operational reproducibility
- evaluate metadata/provenance stability
- validate assay-aware provenance corrections
- characterize runtime telemetry behavior
- assess downstream biological-result stability
- establish reusable reproducibility comparison infrastructure

This case study represents one of the first operationally instrumented metadata-transition reproducibility assessments within the VAP ecosystem.

---

# Dataset Background

`ERR10619281` originates from a Saudi epilepsy whole-exome sequencing (WES) cohort selected for early Phase 1A production telemetry characterization.

The sample was intentionally selected because it provided:

- real-world epilepsy WES scale
- clinically relevant biological context
- manageable runtime economics
- compatibility with controlled repeated execution on MARK infrastructure

This dataset ultimately became the first formal same-sample reproducibility assessment target within VAP.

---

# Execution Context

The following executions were performed:

| Run Category | Run ID | Description |
|---|---|---|
| Initial baseline | `run_2026_05_14_083044` | Pre-assay-provenance patch execution |
| Post-patch rerun | `run_2026_05_14_231247` | Assay-aware provenance-corrected rerun |

The first run completed prior to introduction of explicit assay-aware provenance handling.

The post-patch rerun incorporated:

- config-driven assay typing
- explicit `WES` propagation
- improved provenance emission behavior
- stabilized telemetry instrumentation

Importantly, the reruns were intentionally performed without aggressive optimization changes in order to preserve trustworthy baseline telemetry conditions.

---

# Reproducibility Objectives

This case study evaluated multiple reproducibility dimensions simultaneously:

1. Biological-result reproducibility
2. Structural-output reproducibility
3. Runtime telemetry variability
4. Provenance-model stability
5. Same-sample rerun behavior
6. Metadata-transition tolerance

Importantly, the goal was not strict byte-identical artifact reproduction.

Instead, Phase 1A focused primarily on:

- stable biological interpretation behavior
- stable Stage 11/12 output structure
- stable prioritized candidate generation
- stable validation-candidate generation

under repeated production execution.

---

# Runtime Telemetry

Observed runtime telemetry for `ERR10619281`:

| Execution | Runtime | Status |
|---|---|---|
| Pre-provenance patch baseline | 5 h 04 m 24 s | Success |
| Post-provenance patch rerun | 4 h 56 m 30 s | Success |

Stage-specific telemetry comparison:

| Stage | Run A | Run B |
|---|---:|---:|
| `stage_02_align_data` | 6290s | 6084s |
| `stage_05_call_variants` | 10189s | 9947s |
| `stage_07_annotate_variants` | 1232s | 1215s |

Observed runtime variation was modest and operationally expected.

Importantly:

- runtime telemetry varied slightly
- timestamps varied
- provenance hashes varied

while downstream biological-result structure remained stable.

---

# Reproducibility Findings

## FASTQ Stability

Observed FASTQ pair counts remained identical across repeated executions:

| Metric | Value |
|---|---:|
| FASTQ R1 reads | 83,696,516 |
| FASTQ R2 reads | 83,696,516 |

---

## Stage 11/12 Stability

Observed downstream prioritization structure remained stable:

| Metric | Value |
|---|---:|
| Stage 11 prioritized rows | 811,554 |
| Stage 12 validation rows | 811,554 |

No evidence of downstream biological-result instability was observed across repeated execution.

---

## Reproducibility Layers

Phase 1A reproducibility assessment distinguished between multiple operational reproducibility layers:

### 1. Byte-level reproducibility

Sensitive to:

- timestamps
- runtime telemetry
- provenance hashes
- ordering behavior
- metadata emission

Strict byte-identical reproducibility was not expected during this phase.

---

### 2. Structural reproducibility

Observed stable behavior included:

- Stage 11 row counts
- Stage 12 row counts
- output schemas
- artifact organization
- prioritized candidate structure

---

### 3. Biological reproducibility

Observed stable biological-result behavior included:

- stable prioritized variant distributions
- stable validation-candidate distributions
- stable downstream interpretation structure

Current evidence therefore supports strong observational biological-result reproducibility across repeated WES execution on MARK1.

---

# Runtime Variability vs Biological Stability

One of the most important findings from this case study was the distinction between:

- operational variability
- biological-result stability

Observed operational variability included:

- runtime differences
- run IDs
- timestamps
- config hashes
- provenance metadata
- lightweight artifact hashes

However:

- Stage 11 output structure remained stable
- Stage 12 output structure remained stable
- prioritized biological interpretation remained stable

This distinction is operationally important because it demonstrates that minor telemetry/provenance variability does not necessarily imply biological-result instability.

---

# Operational Findings

This execution campaign also validated several operational maturity improvements within VAP:

- detached `tmux` execution workflows
- production telemetry harvesting
- runtime profiling
- stage-resource instrumentation
- assay-aware provenance correction
- lightweight reproducibility comparison tooling
- reusable MARK execution harnesses

Additionally, this campaign demonstrated that Saudi epilepsy WES runtime economics were substantially more favorable than earlier WGS assumptions.

Observed WES runtime:

```text
~5 hours/sample
```

This materially improved projected feasibility for future epilepsy cohort-scale execution.

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
```

Additional comparison infrastructure developed during this campaign included:

```text
scripts/analysis/compare_vap_runs.py
scripts/mark/mark_compare_err10619281_runs.sh
```

These tools support lightweight reproducibility assessment without requiring large artifact transfer from MARK infrastructure.

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

This case study represents an important transition point within the broader VitamOrdinatio ecosystem.

VAP is now capable of generating:

- provenance-controlled variant evidence
- telemetry-characterized execution outputs
- reproducibility-aware candidate streams
- structured downstream interpretation artifacts

These outputs are expected to become foundational upstream inputs for:

- VDB
- RDGP
- GSC overlay integration
- future cohort-level convergence analysis

Importantly, this campaign demonstrated that VAP-generated outputs no longer terminate solely as static artifacts, but instead are beginning to function as reusable ecosystem evidence streams.

---

# Preliminary Conclusions

The `ERR10619281` reproducibility campaign demonstrated:

- stable same-sample WES execution behavior
- stable downstream biological-result structure
- successful assay-aware provenance correction
- reproducibility-oriented telemetry instrumentation
- operationally tractable WES runtime economics
- feasibility of provenance-controlled epilepsy WES cohort processing on MARK-class infrastructure

Most importantly, this campaign established the first operationally validated bridge between:

- VAP-generated candidate evidence
- downstream RDGP/GSC ecosystem integration
- and future persistent query-oriented genomic infrastructure.