# RDGP Gene Evidence (Stage 08)

This directory contains **gene-level aggregation artifacts** derived from Stage 08 outputs.

These files represent the transition from variant-level data to **gene-level evidence**, forming the foundation for rare disease gene prioritization.

---

## Why This Matters

This stage transforms millions of variants into gene-level summaries,
enabling prioritization strategies used in rare disease analysis.

It represents the transition from:
- variant-centric analysis  
→ to  
- gene-centric reasoning

---

## Key Metrics (HG002)

- genes represented: ~50,230  
- total aggregated variants: ~3.5M  
- high-impact variants: ~791  
- rare variants: ~99k  

---

## What These Files Demonstrate

- aggregation of variant-level data into gene-level summaries  
- preservation of severity, rarity, and quality information  
- multiple prioritization strategies based on:
  - total variant burden  
  - high-impact variant burden  
  - rare variant burden  
  - pathogenic evidence  

---

## Key Artifacts

- [RDGP Validation Summary](stage_08_rdgp_validation_summary.md)

- [Seed Overview](rdgp_seed_overview.md)  
  Example rows showing gene-level aggregation structure

- [Summary Counts](rdgp_summary_counts_only.md)  
  Global statistics across ~50k genes

### Prioritization Views

- [Top Genes by Total Variant Burden](rdgp_top_genes_by_disease_burden.md)  
- [Top Genes by High-Impact Burden](rdgp_top_genes_by_high_impact_burden.md)  
- [Top Genes by Rare Variant Burden](rdgp_top_genes_by_rare_variant_burden.md)  
- [Top Genes by Pathogenic + High-Impact Evidence](rdgp_top_genes_by_pathogenic_evidence_or_high_impact_variants.md)

---

## Important Notes

- HG002 is a benchmark genome (GIAB), not a disease cohort  
- These rankings reflect **variant distributions**, not clinical diagnoses  
- gene_id may be `NA` in some cases due to annotation mapping limitations  
- `low_quality` indicates presence of QC flags from contributing variants  

---

## Role in the System

These outputs serve as:

- input to **RDGP (rare_disease_gene_prioritization)**  
- intermediate representation between:
  - VAP (variant-level)
  - RDGP (reasoning layer)

---

## Bottom Line

This directory demonstrates successful transformation of variant-level data into **structured gene-level evidence**, enabling downstream prioritization workflows.