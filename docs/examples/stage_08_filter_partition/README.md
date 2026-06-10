# Stage 08 — Filter & Partition (VAP)

> Stage 08 reduces ~4.6 million variants into structured datasets for interpretation and prioritization, while preserving the full biological complexity of the genome.

## Overview

Stage 08 transforms annotated variants (Stage 07) into structured subsets for downstream analysis.

This stage performs:

- partitioning into **coding vs noncoding variants**
- generation of **gene-level evidence (RDGP seed)**
- creation of **global summary statistics**

### System Role

Stage 08 represents the transition from tool-driven processing to data engineering.

It ensures that all downstream stages operate on:

- schema-aligned variant records
- complete annotation data
- reproducible and auditable outputs

This stage enables subsequent interpretation, prioritization, and validation layers.

---

## Key Outcomes (HG002)

- total variants: ~4.64M  
- noncoding variants: ~4.61M (>99%)  
- coding variants: ~24k (~0.5%)  

- rare variants: ~129k  
- high-impact variants: ~791  

---

## Stage 08 Components

### 1️⃣ Coding Candidates

→ [`coding_candidates/`](./coding_candidates/)

Focused set of variants affecting coding regions:

- ~24k variants retained  
- dominated by missense and synonymous variants  
- high-impact variants are rare  

**Purpose:** enable direct functional interpretation (Stage 09)


### 2️⃣ Noncoding Candidates

→ [`noncoding_candidates/`](./noncoding_candidates/)

Full preservation of noncoding variant space:

- >99% of total variants  
- dominated by intronic and intergenic variants  
- limited interpretability without additional context  

**Purpose:** enable regulatory and transcriptomic integration (RSP)


### 3️⃣ RDGP Gene Evidence

→ [`rdgp_gene_evidence/`](./rdgp_gene_evidence/)

Aggregation of variants into gene-level summaries:

- ~50k genes represented  
- multi-dimensional evidence:
  - total variant burden  
  - rare variant burden  
  - high-impact burden  
  - pathogenic evidence  

**Purpose:** foundation for gene prioritization (RDGP)


### 4️⃣ Global Variant Summary

→ [`variant_summary/`](./variant_summary/)

Dataset-wide validation metrics:

- coding vs noncoding distribution  
- frequency distribution (common → rare)  
- impact distribution (MODIFIER → HIGH)  

**Purpose:** global QC and biological sanity check

---

## Key Insights

### Variant Distribution

> The vast majority of genomic variation is noncoding (>99%)


### Frequency Structure

> Most variants are common; rare variants represent a small but critical subset


### Functional Impact

> High-impact variants are extremely rare relative to total variation


### System Insight

> Stage 08 reduces complexity while preserving information:

- compresses variant space for interpretation (coding)
- preserves noncoding space for future analysis
- enables gene-level reasoning (RDGP)

---

## Role in the Pipeline

Stage 08 connects:

```text
Stage 07 (annotation)
    ↓
Stage 08 (partition + aggregation)
    ↓
Stage 09–10 (interpretation)
    ↓
Stage 11 (prioritization)
```

---

## Validation Summary

Stage 08 outputs are:

- structurally consistent
- biologically plausible
- quantitatively aligned with expected WGS patterns

---

## Important Notes

- HG002 is a benchmark genome (GIAB), not a disease case
- presence of pathogenic annotations does not imply disease
- noncoding variants require additional context for interpretation

---

### Bottom Line

```text
Stage 08 converts raw variant annotation into structured,
interpretable, and prioritization-ready data layers.
```

---

See also: [HG002 Benchmarking Case Study](../../case_studies/hg002/README.md)