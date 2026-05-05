# Noncoding Candidate Verification (Stage 08)

This directory contains verification artifacts for **noncoding variant candidates** produced by Stage 08 of the Variant Annotation Pipeline (VAP).

Noncoding candidates represent the majority of detected variants and require additional context for interpretation.

---

## Why This Matters

Stage 08 preserves the full noncoding variant space (~4.6M variants),
which cannot be interpreted using coding-centric rules.

These variants require integration with:
- regulatory annotation  
- transcriptomics (RSP)  
- functional genomics  

to become interpretable.

---

## Key Metrics (HG002)

- total noncoding variants: ~4.63 million  
- intronic variants: ~2.8M  
- intergenic variants: ~1.1M  
- SNVs dominate (~3.9M)

---

## What These Files Demonstrate

- correct partitioning of noncoding variant space  
- expected dominance of intronic and intergenic variants  
- distribution of regulatory and transcript-associated contexts  
- separation of interpretability states  
- preservation of annotation fields for downstream analysis  

---

## Key Artifacts

- [Validation Summary](stage_08_noncoding_validation_summary.md)

- [Consequence Distribution](noncoding_candidates_consequence_distribution.md)  
  Major noncoding consequence categories (intron, intergenic, UTR, etc.)

- [Variant Type Distribution](noncoding_candidates_variant_type_distribution.md)  
  SNVs dominate, with insertions/deletions present

- [Example Records (Readable)](noncoding_candidates_excerpt.md)
  Representative rows from noncoding_candidates.tsv  

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