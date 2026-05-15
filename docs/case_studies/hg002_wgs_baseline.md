# HG002 Operational Baseline Case Study
## Phase 0 → Phase 1A Observability and Metadata Maturation on MARK1

**Repository:** `variant_annotation_pipeline`  
**Branch:** `phase0-logging-foundation`  
**Hardware:** `MARK1 (VandPyMolGPUResearch)`  
**Pipeline Version:** `v1-pre-release`  
**Dataset:** `HG002`  
**Assay Type:** `WGS`  

---

# Overview

This case study documents the operational evolution of VAP from an initially minimally instrumented production pipeline into a telemetry-aware, provenance-aware, and reproducibility-oriented execution framework.

Unlike the Saudi epilepsy WES reproducibility campaigns, this case study focuses primarily on:

- observability maturation
- metadata-awareness maturation
- operational instrumentation evolution
- runtime telemetry emergence
- provenance infrastructure development
- production execution introspection

The HG002 execution history therefore represents the foundational operational maturation layer of the VAP ecosystem.

---

# Background

HG002 served as the original large-scale production validation dataset for VAP on MARK1 infrastructure.

An early production HG002 execution completed successfully prior to implementation of:

- canonical runtime telemetry
- structured metadata emission
- stage runtime profiling
- stage resource telemetry
- reproducibility-aware infrastructure
- run fingerprinting
- canonical logging architecture

Although biologically successful, the original execution exposed an important systems-engineering limitation:

```text
successful execution alone was insufficient for operational interpretation
```

Specifically, the original production run lacked:

- populated canonical logs
- runtime stage breakdowns
- structured provenance artifacts
- telemetry-driven bottleneck visibility
- reproducibility-oriented metadata structure

This operational limitation directly motivated development of the broader:

`phase0-logging-foundation`

branch.

---

# Historical HG002 Production Execution

The original HG002 production execution completed successfully with an observed approximate runtime near:

```text
~36 hours
```

This execution demonstrated that VAP could successfully process large-scale WGS data on MARK1 infrastructure.

However, operational introspection remained limited.

As a result:

- runtime bottlenecks could not be rigorously evaluated
- scaling behavior could not be characterized
- optimization priorities remained uncertain
- reproducibility interpretation remained difficult

Important execution artifacts were therefore harvested manually and partially reconstructed using:

- direct filesystem inspection
- ad hoc telemetry recovery
- Artificer-assisted artifact extraction

This experience became operationally important because it exposed the need for:

- canonical metadata emission
- structured telemetry persistence
- reproducibility-oriented artifact generation
- operationally queryable execution outputs

---

# Phase 0 Instrumentation Response

In response to the limitations observed during the original HG002 execution, Phase 0 introduced substantial operational instrumentation improvements.

These included:

- canonical run logging
- runtime profiling
- stage summaries
- stage resource telemetry
- run fingerprints
- structured metadata emission
- lightweight regression testing
- operational execution harnesses
- reusable comparison tooling foundations

Importantly, these changes were implemented prior to broad optimization efforts in order to preserve trustworthy baseline telemetry conditions.

This represented a deliberate strategic decision:

```text
improve observability before optimization
```

rather than attempting premature runtime tuning without sufficient telemetry visibility.

---

# Phase 1A HG002 Instrumented Rerun

Following Phase 0 observability maturation, HG002 was rerun on MARK1 using the newly instrumented telemetry infrastructure.

The Phase 1A rerun completed successfully with an observed runtime near:

```text
~22 h 44 m
```

This materially revised the earlier historical estimate near:

```text
~36 hours
```

and demonstrated that prior runtime assumptions had likely been influenced by incomplete operational visibility.

---

# Runtime Telemetry Findings

The instrumented HG002 rerun revealed several important operational findings.

Primary runtime bottlenecks were identified as:

- Stage 05 — Variant Calling
- Stage 02 — Alignment

Importantly, early telemetry suggested that:

- VEP annotation was not the dominant runtime bottleneck
- runtime behavior differed from initial intuition
- alignment and variant calling dominated execution economics

This finding materially influenced future optimization strategy discussions.

---

# Operational Observability Maturation

The HG002 execution history ultimately demonstrated the operational importance of:

- telemetry-aware execution
- structured runtime visibility
- provenance persistence
- stage-level introspection
- operational metadata generation

The transition from the original minimally instrumented execution toward the fully instrumented rerun therefore represents a major operational maturation milestone within VAP.

This maturation included emergence of:

- `runtime_profile.tsv`
- `run_metadata.json`
- `run_fingerprint.json`
- stage runtime summaries
- canonical pipeline logs
- structured execution telemetry

These artifacts fundamentally changed the operational interpretability of VAP execution behavior.

---

# Metadata and Provenance Evolution

One of the most important lessons from the HG002 execution history was that:

```text
biological success alone is insufficient for sustainable pipeline engineering
```

Without:

- provenance visibility
- telemetry persistence
- structured metadata emission
- operational reproducibility infrastructure

large-scale execution behavior becomes difficult to interpret retrospectively.

The HG002 rerun therefore became an early proof-of-concept demonstrating that:

- execution observability
- provenance infrastructure
- and runtime telemetry

must be treated as first-class pipeline outputs rather than auxiliary debugging artifacts.

---

# Operational Lessons Learned

Several important operational lessons emerged during this campaign.

---

## Observability Before Optimization

The HG002 experience demonstrated the importance of:

```text
instrument first
optimize second
```

Without sufficient telemetry infrastructure:

- optimization priorities remain speculative
- bottlenecks remain ambiguous
- runtime interpretation remains incomplete

---

## Metadata Persistence as Core Infrastructure

The original execution demonstrated that metadata persistence should not be treated as optional.

Instead:

- provenance artifacts
- runtime telemetry
- stage summaries
- reproducibility-oriented outputs

must be treated as core operational infrastructure.

---

## Manual Artifact Recovery Does Not Scale

The original HG002 execution required substantial manual artifact reconstruction effort.

This operational burden motivated development of:

- canonical telemetry emission
- reusable metadata artifacts
- structured execution summaries
- comparison-oriented infrastructure

Future cohort-scale execution would not be sustainable without these improvements.

---

# Ecosystem Implications

The HG002 operational maturation campaign established foundational infrastructure that later enabled:

- Saudi epilepsy WES telemetry campaigns
- metadata-transition reproducibility assessment
- same-patch operational reproducibility assessment
- lightweight reproducibility tooling
- reusable MARK operational harnesses
- future VDB persistence planning
- future RDGP ingestion planning
- future GSC overlay integration

In this sense, HG002 represents the operational origin point of the modern telemetry-aware VAP ecosystem.

---

# Limitations

Current limitations include:

- historical HG002 telemetry remains partially reconstructed
- the original execution lacked complete structured metadata
- byte-identical reproducibility was not evaluated
- cross-node reproducibility remains untested
- runtime economics remain partially influenced by virtualized MARK infrastructure

Additionally, some historical runtime interpretations remain approximate because the earliest execution predated canonical telemetry infrastructure.

---

# Preliminary Conclusions

The HG002 operational maturation campaign demonstrated:

- successful large-scale WGS execution on MARK1
- the necessity of telemetry-aware pipeline engineering
- the importance of structured metadata persistence
- the importance of provenance-oriented infrastructure
- the operational value of stage-level runtime visibility
- the strategic importance of observability-first systems engineering

Most importantly, the HG002 experience directly motivated the telemetry and reproducibility infrastructure that later enabled:

- metadata-transition reproducibility assessment (`ERR10619281`)
- same-patch operational reproducibility assessment (`ERR10619300`)
- and future ecosystem-scale evidence persistence planning.

In this sense, HG002 serves as the foundational operational maturation case study of the VAP ecosystem.