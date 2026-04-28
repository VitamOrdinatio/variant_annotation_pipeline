# Stage 09 — Coding Variant Interpretation

## Overview

Stage 09 performs **rule-based interpretation of coding variants**, transforming annotated variant records into structured, classification-ready data products.

This stage integrates:

- functional consequence annotations (VEP)
- population frequency data (gnomAD, 1000 Genomes, ExAC)
- clinical evidence (ClinVar)
- QC and interpretability filters

The result is a **deterministic classification of coding variants** into biologically meaningful categories suitable for downstream prioritization.

---

## Biological Sanity Check

Observed variant distributions are consistent with published human genome studies:

- ~10–12k missense variants per individual
- hundreds of predicted loss-of-function variants
- presence of ClinVar “pathogenic” annotations in healthy individuals

These patterns are expected and reflect natural human genetic variation rather than disease.

---

## Inputs and Outputs

**Input:**
- Stage 08 partitioned coding variants  
- Annotated VCF-derived records with gene, transcript, and consequence data  

**Output:**
- `stage_09_coding_interpreted.tsv`

Each output row represents a **sample-scoped gene-variant record** enriched with:

- functional interpretation
- rarity classification
- clinical evidence flags
- prioritization-ready labels

---

## Key Metrics (HG002 Run)

- Total coding variants processed: **~27,486**
- Rare variants identified: **1,335**
- Loss-of-function variants: **789**
- Missense variants: **11,573**
- Synonymous variants: **11,601**

### Clinical Evidence

- Pathogenic: **20**
- Likely pathogenic: **13**
- VUS: **184**
- Conflicting: **61**
- Benign / likely benign: **7,450+**
- Missing clinical annotation: **19,758**

---

## Interpretation Labels

Stage 09 assigns each variant to a structured interpretation class:

| Label | Count | Description |
|------|------|-------------|
| lof_or_missense_rare | 1,121 | High-priority candidates (rare + impactful) |
| coding_common_or_low_support | 25,169 | Common or low-impact variants |
| coding_uninterpretable | 1,196 | Insufficient data or ambiguous classification |

---

## Functional Impact Breakdown

| Functional Class | Count |
|----------------|------|
| missense | 11,573 |
| synonymous | 11,601 |
| splice_relevant | 3,154 |
| loss_of_function | 789 |
| other_coding | 369 |

---

## Example: High-Value Variant

`gene:` PIK3CD
`consequence:` frameshift_variant
`impact_class:` HIGH
`population_frequency:` 0
`rarity_flag:` rare
`coding_interpretation_label:` lof_or_missense_rare
`qc_status:` pass
`qc_reliability:` high_confidence


This example demonstrates a **rare loss-of-function variant**, a key signal for downstream prioritization.

---

## Interpretation Logic

Stage 09 applies **deterministic rule-based classification** using:

### 1. Functional Impact
- HIGH → loss_of_function  
- MODERATE → missense  
- LOW → synonymous  

### 2. Frequency Thresholds
- rare  
- low_frequency  
- common  

### 3. Clinical Evidence
- pathogenic / likely pathogenic  
- VUS  
- benign / conflicting / missing  

---

## Derived Fields

The following fields are introduced in Stage 09:

- `functional_impact`
- `rarity_flag`
- `clinical_evidence`
- `coding_interpretation_label`

Supporting flags:

- `is_lof_candidate`
- `is_rare_candidate`
- `is_clinically_supported`
- `is_high_quality`
- `is_potential_artifact`

These fields transform raw annotations into **structured reasoning inputs**.

---

## Data Quality and QC

- All variants pass upstream QC filters (`qc_status = pass`)
- Interpretation is limited to:
  - `interpretability_status = interpretable_now`
- Reliability is tracked via:
  - `qc_reliability = high_confidence`

---

## Output Characteristics

The Stage 09 output is:

- schema-aligned  
- fully annotated and classified  
- QC-validated  
- deterministic and reproducible  

This dataset is **ready for integration with noncoding interpretation (Stage 10)** and subsequent prioritization (Stage 11).

---

## System Context

Stage 09 represents the **first interpretation layer** in the VAP pipeline:

* Stage 08 → Data engineering (partitioning)
* Stage 09 → Coding interpretation ← current stage
* Stage 10 → Noncoding interpretation
* Stage 11 → Integrated prioritization


This stage converts **variant-level data into structured biological evidence**.

---

## Execution Evidence

See supporting artifacts:

- `stage_09_run_excerpt_log.md`
- `stage_09_label_distribution.md`
- `stage_09_high_value_examples.md`

---

## Biological Sanity Check

Observed variant distributions from this Stage 09 run (HG002) are consistent with established human genome studies.

Typical per-individual expectations from large-scale population datasets include:

- ~20,000–25,000 coding variants  
- ~10,000–12,000 missense variants  
- hundreds of predicted loss-of-function (LoF) variants  

Published studies supporting these ranges include:

- Hanchard NA, Choudhury A. 1000 Genomes Project phase 4: The gift that keeps on giving. Cell. 2022;185(18):3286-3289. doi:10.1016/j.cell.2022.08.001

- Gustafson JA, Gibson SB, Damaraju N, et al. High-coverage nanopore sequencing of samples from the 1000 Genomes Project to build a comprehensive catalog of human genetic variation. Genome Res. 2024;34(11):2061-2073. Published 2024 Nov 20. doi:10.1101/gr.279273.124

- Chen S, Francioli LC, Goodrich JK, et al. A genomic mutational constraint map using variation in 76,156 human genomes. Nature. 2024;625(7993):92-100. doi:10.1038/s41586-023-06045-0

- Karczewski KJ, Francioli LC, Tiao G, et al. The mutational constraint spectrum quantified from variation in 141,456 humans. Nature. 2020;581(7809):434-443. doi:10.1038/s41586-020-2308-7

- MacArthur DG, Balasubramanian S, Frankish A, et al. A systematic survey of loss-of-function variants in human protein-coding genes. Science. 2012;335(6070):823-828. doi:10.1126/science.1215040

- 1000 Genomes Project Consortium, Auton A, Brooks LD, et al. A global reference for human genetic variation. Nature. 2015;526(7571):68-74. doi:10.1038/nature15393


### Interpretation Context

HG002 represents a healthy reference individual and is not expected to exhibit disease phenotypes.

The presence of:

- missense variants  
- predicted loss-of-function variants  
- ClinVar-annotated “pathogenic” variants  

reflects:

- natural human genetic variation  
- context-dependent pathogenicity  
- limitations and inconsistencies in clinical annotation databases  

Stage 09 identifies candidate variants based on structural and statistical criteria and does **not perform clinical diagnosis**.

---

## Summary

Stage 09 demonstrates that VAP is not only capable of:

- processing genomic data  
- annotating variants  

but also:

> **performing structured, reproducible biological interpretation at scale**

This establishes the foundation for downstream reasoning and candidate prioritization.

---