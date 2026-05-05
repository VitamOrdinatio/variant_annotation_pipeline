# VAP Interpretation Layer — Coding vs Noncoding Reasoning

## Overview

Stages 09 and 10 implement the interpretation layer of the Variant Annotation Pipeline (VAP).

These stages transform annotated variants into structured evidence for prioritization, while explicitly accounting for the fundamental differences between coding and noncoding regions.

---

## Core Principle

> Not all variants are equally interpretable.

The pipeline distinguishes between:

- **Coding variants** → interpretable with established biological rules  
- **Noncoding variants** → context-dependent and often uninterpretable  

---

## Stage 09 — Coding Interpretation

Coding variants are evaluated using deterministic criteria:

- functional impact (e.g., missense, loss-of-function)  
- population frequency  
- clinical annotation (ClinVar)  

### Outcome

- identification of rare and high-impact variants  
- structured labels for prioritization  

### Key Insight

> Coding variants can often be interpreted directly from sequence and annotation data.

---

## Stage 10 — Noncoding Interpretation

Noncoding variants are classified rather than fully interpreted.

The pipeline assigns:

- common / low-support labels  
- regulatory or transcript-associated candidate labels  
- uninterpretable status  

### Outcome

- preservation of noncoding variant space  
- identification of candidates for downstream analysis  

### Key Insight

> Noncoding variants require external context (e.g., transcriptomics, regulatory data) for meaningful interpretation.

---

## Comparative Summary

| Feature | Coding (Stage 09) | Noncoding (Stage 10) |
|--------|------------------|----------------------|
| Interpretability | High | Limited |
| Primary signals | Functional impact, rarity | Context, regulatory proximity |
| Deterministic conclusions | Often possible | Rarely possible |
| Role in pipeline | Candidate identification | Candidate preservation |

---

## System Design Philosophy

The pipeline intentionally:

- applies **interpretation where justified (coding)**  
- preserves **uncertainty where necessary (noncoding)**  

---

## Integration with Downstream Stages

Outputs from Stages 09 and 10 feed into:

- **Stage 11 — Prioritization**
- **RDGP — Gene-level reasoning**
- **RSP — Transcriptomic integration (noncoding)**  

---

## Why This Matters

> A robust variant interpretation system must distinguish between:
>
> - what is known  
> - what is uncertain  
> - what requires additional data  

This distinction is critical for:

- clinical genomics  
- rare disease analysis  
- translational bioinformatics  

---

## Bottom Line

> The VAP interpretation layer applies biological reasoning where possible and preserves uncertainty where necessary.