# Variant Summary (Stage 08)

This directory contains **global summary statistics** for Stage 08 outputs.

These artifacts provide a high-level view of the entire variant dataset after filtering and partitioning.

---

## Why This Matters

These summaries provide a global validation layer,
confirming that Stage 08 outputs match expected genome-wide patterns
in variant distribution, frequency, and functional impact.

---

## Key Metrics (HG002)

- total variants: ~4.64M  
- noncoding variants: ~4.61M (>99%)  
- coding variants: ~24k (~0.5%)  

- common variants: ~4.23M  
- rare variants: ~129k  
- missing frequency: ~117k  

- MODIFIER impact: ~4.60M  
- HIGH impact: ~791  

---

## What These Files Demonstrate

- overall distribution of coding vs noncoding variants  
- population frequency distribution across all variants  
- severity distribution (impact_class) across dataset  

---

## Key Artifacts

- [Variant Summary](stage_08_variant_summary_validation_summary.md)

- [Coding vs Noncoding Distribution](variant_summary_coding_vs_noncoding_flags.md)  
  Shows overwhelming dominance of noncoding variants

- [Frequency Distribution](variant_summary_frequency_distribution.md)  
  Breakdown into common, low-frequency, rare, and missing categories

- [Severity Distribution](variant_summary_severity_distribution.md)  
  Distribution of MODIFIER, LOW, MODERATE, and HIGH impact variants

---

## Interpretation Notes

- Most variants are:
  - noncoding  
  - common  
  - low or modifier impact  

This is expected for whole-genome sequencing data.

- High-impact variants are rare but critical for downstream analysis  

---

## Role in the System

These summaries act as:

- QC validation of Stage 08 outputs  
- sanity checks for partitioning logic  
- reference metrics for downstream analysis  

---

## Bottom Line

This directory demonstrates that Stage 08 outputs are **globally consistent, biologically plausible, and correctly partitioned**.