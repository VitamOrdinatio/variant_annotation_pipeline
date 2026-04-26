# Noncoding Candidate Verification (Stage 08)

This directory contains verification artifacts for **noncoding variant candidates** produced by Stage 08 of the Variant Annotation Pipeline (VAP).

Noncoding candidates represent the majority of detected variants and require additional context for interpretation.

---

## What These Files Demonstrate

- correct partitioning of noncoding variant space  
- expected dominance of intronic and intergenic variants  
- distribution of regulatory and transcript-associated contexts  
- separation of interpretability states  
- preservation of annotation fields for downstream analysis  

---

## Key Artifacts

- [Consequence Distribution](noncoding_candidates_consequence_distribution.md)  
  Major noncoding consequence categories (intron, intergenic, UTR, etc.)

- [Variant Context Distribution](noncoding_candidates_variant_context_distribution.md)  
  Intronic, intergenic, regulatory, splice-region breakdown

- [Variant Type Distribution](noncoding_candidates_variant_type_distro.md)  
  SNVs dominate, with insertions/deletions present

- [Interpretability Distribution](noncoding_candidates_interpretability.md)  
  Most variants require external annotation (expected)

- [Example Records (TSV)](noncoding_candidates_excerpt.tsv)  
- [Example Records (Readable)](noncoding_candidates_excerpt.md)

- [High-Impact / Splice-Region Examples](noncoding_candidates_high_impact_variants.md)

---

## Important Notes

- HG002 is a benchmark genome (GIAB), not a disease case  
- Most noncoding variants are expected to be:
  - common  
  - low interpretability without additional annotation  
- Stage 08 intentionally **does not perform regulatory interpretation**

---

## Partitioning Clarification

Variants are routed based on **variant_context**, not strictly `variant_class`.

This allows:
- splice-region variants to be preserved for specialized interpretation  
- consistent handling of ambiguous or mixed annotations  

---

## Role in the System

Noncoding candidates are preserved for:

- future regulatory annotation layers  
- integration with RNA-seq evidence (RSP)  
- downstream RDGP prioritization when context is available  

---

## Bottom Line

This directory demonstrates correct handling of the **large, complex noncoding variant space**, preserving information without premature interpretation.