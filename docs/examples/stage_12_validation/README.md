# Stage 12 — Variant Validation (VAP)

## Overview

Stage 12 converts prioritized variants into validation-ready candidates by assigning validation requirements, priorities, and methods.

---

## Role in Pipeline

Stage 12 follows prioritization:

Stage 11 → identify candidates  
Stage 12 → determine which candidates require validation  
Stage 13 → summarize findings  

---

## Key Metrics (HG002)

- total variants: ~4.64M  
- validation required: ~113k (~2.4%)  
- validation method: IGV for all candidates  

---

## Why This Stage Matters

> A correct system must validate selectively, not exhaustively.

Stage 12 ensures:

- only prioritized variants are validated  
- validation effort is controlled  
- false positives are minimized  

> Stage 12 enforces validation discipline by ensuring that only biologically plausible candidates are advanced for review.

---

## Key Insights

### Controlled Validation

> Only ~2.4% of variants require validation.

---

### Biological Consistency

> HG002 produces no high-priority variants and limited validation targets.

---

### System Integrity

> Validation is strictly tied to prioritization logic.

---

## Hallmark Artifacts

The following artifacts represent the core outputs of Stage 12. These are sufficient to understand validation logic, system behavior, and biological context.

- [Stage 12 Validation Summary](./stage_12_validation_summary.md)  
  System-level interpretation of validation logic, efficiency, and biological correctness.

- [Stage 12 Summary](./stage_12_summary.md)  
  Core metrics and distributions for validation assignment.

- [Validation Pass Distribution](./stage_12_validation_pass_distribution.md)  
  Breakdown of which variants are selected for validation.

- [Validation Rationale](./stage_12_validation_rationale.md)  
  Explanation of how prioritization tiers drive validation decisions.

- [Validation Composition](./stage_12_validation_composition.md)  
  Functional breakdown of validation candidates (coding vs noncoding consequences).

- [Gene-Level Validation Burden](./stage_12_gene_validation_burden.md)  
  Distribution of validation candidates across genes.

- [Validation-Pass Examples](./stage_12_validation_pass_examples.md)  
  Representative variants that pass prioritization and require validation.

---

## Suggested Read Order

To understand Stage 12 as a validation system, review artifacts in the following order:

1. **Validation Summary**  
   Start here for a high-level understanding of system behavior and validation philosophy.

2. **Stage 12 Summary**  
   Review core metrics and confirm alignment with Stage 11 outputs.

3. **Validation Pass Distribution**  
   Understand how many variants are selected for validation and how selective the system is.

4. **Validation Rationale**  
   See how prioritization tiers map directly to validation decisions.

5. **Validation Composition**  
   Examine what types of variants dominate the validation set.

6. **Gene-Level Validation Burden**  
   Understand where validation effort is concentrated across the genome.

7. **Validation-Pass Examples**  
   Inspect representative variants to see how prioritization and validation intersect in practice.

---

## Supporting Artifacts

These artifacts provide additional context for QC behavior and filtering:

- stage_12_qc_reliability_distribution.md  
- stage_12_artifact_flag_distribution.md  
- stage_12_high_confidence_examples.md  
- stage_12_failed_qc_examples.md  
- stage_12_summary.json

---

## Bottom Line

> Stage 12 enforces disciplined validation by ensuring that only biologically plausible and prioritized candidates are advanced for review.

See also: [HG002 Benchmarking Case Study](../../case_studies/hg002/README.md)