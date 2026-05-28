# vap_depth_stratified_epilepsy_panel_design.md

# VAP Depth-Stratified Epilepsy Panel Design (Draft v0.1)

## Repository

`variant_annotation_pipeline (VAP)`

---

# Purpose

This document defines the scientific rationale, cohort selection philosophy, stratification strategy, and translational interpretation goals governing the construction of a depth-stratified epilepsy sequencing panel for VAP ecosystem demonstrations.

The panel is intended to support:

* VAP reproducibility demonstrations
* biological candidate recovery demonstrations
* GSC overlay contextualization
* future VDB substrate generation
* future RDGP exemplar construction
* sequencing-depth robustness assessment
* translational systems-biology storytelling

using real-world epilepsy sequencing data.

---

# Core Principle

The purpose of this panel is NOT:

* clinical diagnosis
* powered association testing
* pathogenicity determination
* cohort-scale inference

Instead, the purpose is:

```text
controlled translational substrate demonstration
```

using biologically contextualized epilepsy sequencing data.

---

# Scientific Motivation

Initial VAP validation runs on Saudi epilepsy sequencing datasets demonstrated:

* deterministic rerun reproducibility
* stable pipeline execution
* biologically plausible candidate recovery
* overlap with epilepsy-prioritized loci
* overlap with mitochondrial-associated loci

Specifically:

* EPI25 overlap signals were observed
* MitoCarta overlap signals were observed
* epilepsy-relevant candidate loci emerged from annotated outputs

This created an opportunity to construct a:

```text
depth-stratified translational recovery panel
```

for downstream ecosystem demonstrations.

---

# Panel Design Philosophy

The panel was intentionally designed to avoid:

* ultra-low-depth sequencing extremes
* ultra-high-depth sequencing extremes
* pathological technical outliers
* arbitrary sample selection

Instead, the panel aims to capture:

```text
controlled sequencing-depth diversity
```

while preserving:

* technical plausibility
* biological interpretability
* translational realism

---

# Stratification Strategy

SRAs are sorted in:

```text
descending order by read count
```

where:

* Rank 1 corresponds to the highest read-count sample.

The cohort is stratified into:

| Category | Meaning                      |
| -------- | ---------------------------- |
| Q1       | higher-depth quartile        |
| Median   | middle-depth reference group |
| Q3       | lower-depth quartile         |

Extreme tails are intentionally avoided.

---

# Selected Panel Structure

## Planned Panel

| Category | Sample Count |
| -------- | ------------ |
| Q1       | n=3          |
| Median   | n=3          |
| Q3       | n=3          |

Total:

```text
9 epilepsy SRAs
```

---

# Current Planned SRAs

## Q1 — Higher-Depth Quartile

| SRA         |  Read Count |     Rank |
| ----------- | ----------: | -------: |
| ERR10619330 | 210,460,026 | 35 / 144 |
| ERR10619309 | 205,213,734 | 36 / 144 |
| ERR10619212 | 203,719,472 | 37 / 144 |

---

## Median Group

| SRA         |  Read Count |     Rank |
| ----------- | ----------: | -------: |
| ERR10619285 | 167,725,712 | 72 / 144 |
| ERR10619281 | 167,393,032 | 73 / 144 |
| ERR10619300 | 167,346,574 | 74 / 144 |

---

## Q3 — Lower-Depth Quartile

| SRA         |  Read Count |      Rank |
| ----------- | ----------: | --------: |
| ERR10619225 | 141,637,092 | 107 / 144 |
| ERR10619230 | 141,194,746 | 108 / 144 |
| ERR10619203 | 140,909,888 | 109 / 144 |

---

# Why This Design Is Scientifically Useful

This design enables exploration of:

* reproducibility under moderate depth variation
* candidate recovery stability
* overlay recovery robustness
* translational interpretability
* semantic contextualization consistency

without requiring:

* large powered cohorts
* inferential clinical statistics
* formal disease association claims

---

# Important Scientific Constraint

This panel is NOT intended to support:

* statistically powered disease association claims
* clinical pathogenicity assertions
* diagnostic interpretation
* formal penetrance estimation
* epidemiological inference

The panel should instead be viewed as:

```text
a reproducible translational systems-biology demonstration panel
```

---

# Statistical Philosophy

The planned design uses:

```text
n=3 per depth stratum
```

This is considered sufficient for:

* descriptive summaries
* exploratory comparisons
* variability assessment
* reproducibility assessment
* trend visualization
* ecosystem demonstrations

This is NOT considered sufficient for:

* strong inferential statistics
* high-powered hypothesis testing
* definitive biological conclusions

---

# Recommended Statistical Framing

Analyses should be framed as:

* exploratory
* descriptive
* comparative
* systems-oriented
* translational

rather than:

* inferential
* diagnostic
* causality-focused

---

# Planned Biological Harvest Metrics

The panel is intended to support harvesting of:

## Variant-Level Metrics

* total variant counts
* coding variant counts
* missense counts
* synonymous counts
* splice-region counts
* frameshift counts
* nonsense counts
* HIGH/MODERATE/LOW impact distributions

---

## Gene-Level Metrics

* gene burden summaries
* high-impact burden summaries
* candidate recurrence
* mitochondrial candidate burden
* epilepsy-prioritized burden

---

## Overlay Metrics

Candidate intersections against:

* EPI25
* MitoCarta
* Genes4Epilepsy
* future GSC overlays

---

# Ecosystem Integration Goals

This panel is intended to demonstrate interoperability between:

| Repo | Planned Role                           |
| ---- | -------------------------------------- |
| VAP  | variant recovery and annotation        |
| GSC  | semantic overlay contextualization     |
| VDB  | future normalized evidence persistence |
| RDGP | future semantic prioritization         |

---

# Translational Questions Of Interest

The panel may support exploratory questions such as:

## 1. Overlay Robustness

```text
Do biologically prioritized candidate overlaps remain stable across moderate sequencing-depth strata?
```

---

## 2. Candidate Recovery Stability

```text
Does candidate recovery remain biologically interpretable under moderate sequencing-depth variation?
```

---

## 3. Mitochondrial Sensitivity

```text
Are mitochondrial-associated candidate recoveries disproportionately sensitive to sequencing depth?
```

---

## 4. Candidate Recurrence

```text
Do epilepsy-prioritized loci recur across independent Saudi epilepsy sequencing samples?
```

---

# Future Ecosystem Potential

This panel may later support:

* VDB ingestion
* RDGP exemplar generation
* overlay-aware prioritization
* transcriptomic contextualization
* semantic prioritization demonstrations
* explainability demonstrations
* inheritance-aware reasoning demonstrations

---

# Metadata Caveat

The ENA metadata for the associated BioProject lists:

```text
library_strategy = AMPLICON
```

However:

* the BioProject title
* associated study description
* sequencing scale
* sequencing structure

strongly indicate a whole-exome sequencing (WES)-style cohort.

This metadata inconsistency should be documented transparently in future case-study methods sections.

---

# Key Design Philosophy

The purpose of this panel is not merely to showcase:

```text
pipeline execution
```

but rather to demonstrate:

```text
biologically contextualized translational substrate recovery
```

from real-world epilepsy sequencing data.

---

# Final Design Principle

The panel should prioritize:

* reproducibility
* interpretability
* semantic contextualization
* translational realism
* ecosystem interoperability

over:

* scale
* throughput
* benchmark-style optimization
* opaque performance metrics

# End of vap_depth_stratified_epilepsy_panel_design.md
