# Coding Candidate Verification (Stage 08)

This directory contains verification artifacts for **coding variant candidates** produced by Stage 08 of the Variant Annotation Pipeline (VAP).

Coding candidates represent variants mapped to protein-coding regions and are the primary input for downstream interpretation of functional impact.

---

## What These Files Demonstrate

- correct partitioning of coding vs noncoding variants  
- expected distribution of coding consequences (e.g., synonymous, missense, frameshift, stop_gained)  
- preservation of variant-level annotation fields  
- identification of high-impact coding variants  
- variant-type distribution within coding space  

---

## Key Artifacts

- [Consequence Distribution](coding_candidates_consequence_distribution.md)  
  Summary of coding variant consequences (missense, synonymous, frameshift, etc.)

- [Variant Type Distribution](coding_candidates_variant_type_distro.md)  
  Distribution of SNVs, insertions, deletions, and complex variants

- [Example Records (TSV)](coding_candidates_excerpt.tsv)  
  Representative rows from coding_candidates.tsv

- [Example Records (Readable)](coding_candidates_excerpt.md)

- [High-Impact Coding Variants (TSV)](coding_candidates_high_impact_variants.tsv)  
  Subset of HIGH-impact variants (e.g., frameshift, stop_gained)

- [High-Impact Coding Variants (Readable)](coding_candidates_high_impact_variants.md)

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