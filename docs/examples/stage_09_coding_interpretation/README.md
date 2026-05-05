## Stage 09 — Coding Interpretation Artifacts

This directory contains evidence demonstrating successful execution of Stage 09.

Stage 09 performs rule-based classification of coding variants and produces structured, prioritization-ready outputs.

Artifacts include:
- summary (overview and logic)
- label distributions (quantitative evidence)
- high-value examples (biological signal)
- execution logs (runtime validation)

---

## Key Metrics (HG002)

- total coding variants processed: ~27,486  
- rare variants: ~1,335  
- loss-of-function variants: ~789  
- missense variants: ~11,573  

---

## Why This Stage Matters

Stage 09 applies deterministic rules to identify:

- rare coding variants  
- loss-of-function candidates  
- clinically supported variants  

This is the first stage where variants are elevated from:
- annotated data  
→ to  
- prioritization-ready candidates

---

## Hallmark Artifacts

**Recommended reading order:** Validation Summary → Summary → Label Distribution → High-Value Examples → Run Log

- [Stage 09 Validation Summary](./stage_09_validation_summary.md)  
  Curated interpretation of Stage 09 outputs, key metrics, and biological sanity checks.

- [Stage 09 Summary](./stage_09_summary.md)  
  Deterministic summary of coding interpretation counts and logic.

- [Label Distribution](./stage_09_label_distribution.md)  
  Quantitative breakdown of interpretation labels, functional impact, rarity, and clinical evidence.

- [High-Value Examples](./stage_09_high_value_examples.md)  
  Representative coding variants including loss-of-function, rare missense, and clinically annotated examples.


## Interpretation Context (HG002)

HG002 represents a healthy reference individual and is not expected to exhibit disease phenotypes.

The presence of missense, loss-of-function, and ClinVar-annotated “pathogenic” variants reflects:

- natural human genetic variation
- context-dependent pathogenicity
- limitations and inconsistencies in clinical annotation databases

Stage 09 identifies candidate variants based on structural and statistical criteria, not clinical diagnosis.

See also: [Interpretation Layer Overview](../../interpretation_layer.md)