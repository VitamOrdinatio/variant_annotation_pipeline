# Coding Candidate Verification (Stage 08)

This directory contains verification artifacts for **coding variant candidates** produced by Stage 08 of the Variant Annotation Pipeline (VAP).

Coding candidates represent variants mapped to protein-coding regions and are the primary input for downstream interpretation of functional impact.

---

## Why This Matters

This stage reduces ~4.6M variants to a manageable set of ~24k coding variants,
enabling focused downstream interpretation of functional impact.

---

## Key Metrics (HG002)

- total coding variants: ~24,000  
- SNVs dominate coding variation (~23.5k)  
- high-impact variants (frameshift, stop_gained): rare (~100–300 scale)

---

## What These Files Demonstrate

- correct partitioning of coding vs noncoding variants  
- expected distribution of coding consequences (e.g., synonymous, missense, frameshift, stop_gained)  
- preservation of variant-level annotation fields  
- identification of high-impact coding variants  
- variant-type distribution within coding space  

---

## Key Artifacts

- [Validation Summary](stage_08_coding_validation_summary.md)

- [Consequence Distribution](coding_candidates_consequence_distribution.md)  
  Summary of coding variant consequences (missense, synonymous, frameshift, etc.)

- [Variant Type Distribution](coding_candidates_variant_type_distribution.md)  
  Distribution of SNVs, insertions, deletions, and complex variants

- [Example Records (Readable)](coding_candidates_excerpt.md)
  Representative rows from coding_candidates.tsv

- [High-Impact Coding Variants (Readable)](coding_candidates_high_impact_variants.md)
  Subset of HIGH-impact variants (e.g., frameshift, stop_gained)

---

## Interpretation Notes

- HIGH-impact variants represent the most likely candidates for functional disruption  
- Many variants in HG002 are benign/common; this dataset is not a disease cohort  
- These artifacts demonstrate correct **classification and filtering**, not clinical prioritization  

---

## Role in the System

Coding candidate outputs feed into:

- **VDB (variant_database)** → structured storage  
- **RDGP (rare_disease_gene_prioritization)** → gene-level aggregation and prioritization  

---

## Bottom Line

This directory demonstrates that Stage 08 correctly extracts and structures **coding variant candidates** suitable for downstream biological interpretation.