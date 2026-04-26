# Variant Summary (Stage 08)

This directory contains **global summary statistics** for Stage 08 outputs.

These artifacts provide a high-level view of the entire variant dataset after filtering and partitioning.

---

## What These Files Demonstrate

- overall distribution of coding vs noncoding variants  
- population frequency distribution across all variants  
- severity distribution (impact_class) across dataset  

---

## Key Artifacts

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