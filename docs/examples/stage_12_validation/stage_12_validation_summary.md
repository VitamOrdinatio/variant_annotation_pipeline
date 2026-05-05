# Stage 12 — Validation Summary

## Overview

Stage 12 converts prioritized variants into validation-ready candidates by assigning validation requirements, priorities, and methods.

---

## Key Metrics

- total variants: ~4.64M  
- validation required: ~113k (~2.4%)  
- high-confidence variants: ~99%  
- artifact-flagged variants: 0  

---

## Validation Efficiency

> Only ~2.4% of variants require validation, demonstrating strong upstream filtering and prioritization discipline.

---

## Validation Allocation

- All Tier 2 variants are assigned IGV validation  
- Tier 3 and Tier 4 variants are not prioritized for validation  

---

## Key Insight

> Validation effort is concentrated exclusively on prioritized candidates, ensuring efficient use of downstream resources.

### Validation Composition

> The majority of validation candidates are noncoding variants, reflecting genome-wide variation patterns.

### Gene-Level Burden

> Validation burden is concentrated in large, mutation-dense genes such as CSMD1 and RBFOX1.

---

## System Behavior

Stage 12 demonstrates:

- deterministic mapping from prioritization → validation  
- no over-assignment of validation tasks  
- preservation of biological realism in HG002  

---

## Biological Context

HG002 is a healthy genome:

- absence of high-priority variants is expected  
- validation triage reflects candidate uncertainty, not disease  

---

## Important Considerations

- validation is computationally assigned, not experimentally performed  
- IGV is recommended for visual confirmation  
- candidates require phenotype context for interpretation  

---

## Bottom Line

> Stage 12 ensures that only biologically plausible candidate variants are advanced for validation, maintaining system precision and interpretability.