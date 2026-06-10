# Stage 10 — Noncoding Interpretation (VAP)

## Overview

Stage 10 applies rule-based classification to noncoding variants, assigning structured labels while preserving interpretability constraints.

Unlike coding variants, noncoding variants cannot generally be interpreted using sequence-level information alone. This stage therefore focuses on:

- categorizing variants into interpretable vs uninterpretable groups  
- identifying rare variants in regulatory or transcript-associated contexts  
- preserving uncertainty where biological meaning cannot be confidently assigned  

---

## Key Metrics (HG002)

- total noncoding variants processed: ~4.61M  
- common variants: ~4.2M  
- rare variants: ~128k  
- regulatory/transcript-associated rare variants: ~112k  
- uninterpretable variants: ~1.15M  

---

## Why This Stage Matters

Stage 10 acknowledges a fundamental limitation in genomics:

> Most noncoding variants cannot be interpreted without additional biological context.

Rather than overinterpreting, this stage:

- classifies variants using deterministic rules  
- preserves the full noncoding space  
- identifies candidates for downstream analysis  

---

## Hallmark Artifacts

**Recommended reading order:** Validation Summary → Summary → Label Distribution → High-Value Examples

- [Stage 10 Validation Summary](./stage_10_validation_summary.md)  
  Interpretation of noncoding variant distributions, system behavior, and biological constraints.

- [Stage 10 Summary](./stage_10_summary.md)  
  Deterministic counts and structured outputs from noncoding interpretation.

- [Label Distribution](./stage_10_label_distribution.md)  
  Quantitative breakdown of interpretation labels, functional context, rarity, and clinical evidence.

- [High-Value Examples](./stage_10_high_value_examples.md)  
  Curated examples illustrating rare candidates, regulatory contexts, and interpretability limitations.

---

## Interpretation Framework

Stage 10 assigns variants into three broad categories:

### 1. Common / Low-Support Variants
- high population frequency  
- unlikely to be functionally relevant  

### 2. Regulatory or Transcript-Associated Rare Variants
- low-frequency variants in gene-associated or regulatory contexts  
- candidates for downstream prioritization  

### 3. Uninterpretable Variants
- insufficient annotation or context  
- preserved for future analysis  

---

## Key Insights

### Noncoding Dominance

> The vast majority of genomic variation occurs outside coding regions.

---

### Limited Interpretability

> Many noncoding variants cannot be meaningfully interpreted with current knowledge.

---

### Candidate Identification

> A small subset of variants may warrant further investigation, particularly when rare and located in regulatory contexts.

### Interpretation Scope

Noncoding variants require additional context (regulatory, transcriptomic, or functional data) and therefore represent a less directly interpretable signal compared to coding variants.

This stage highlights both the abundance and the interpretive limitations of noncoding variation.

---

## Important Considerations

- HG002 is a healthy benchmark genome (GIAB)  
- presence of rare or annotated variants does not imply disease  
- noncoding interpretation requires integration with:
  - transcriptomics (RSP)  
  - regulatory annotation  
  - functional genomics  

---

## Role in the Pipeline

Stage 10 connects:

```text
Stage 08 (noncoding candidates)
↓
Stage 10 (noncoding interpretation)
↓
Stage 11 (prioritization)
```


It also provides input to:

- RDGP (gene-level prioritization)  
- RSP (transcriptomic integration)  

---

## System Design Principle

> Do not overinterpret noncoding variation.

Stage 10 is intentionally conservative:

- assigns structure without forcing meaning  
- preserves uncertainty as a first-class outcome  

---

## Bottom Line

> Stage 10 identifies noncoding candidates while explicitly preserving the limits of biological interpretation.

See also: [Interpretation Layer Overview](../../interpretation_framework.md)
See also: [HG002 Benchmarking Case Study](../../case_studies/hg002/README.md)