# Stage 01–06 — Foundation (Alignment → Variant Calling → Normalization)

## Overview

Stages 01–06 of VAP establish the structural and quantitative foundation of the pipeline:

- Stage 01–02: FASTQ ingestion and alignment
- Stage 03–04: BAM processing and QC
- Stage 05: Variant calling (GATK HaplotypeCaller)
- Stage 06: Variant normalization

These stages transform raw sequencing reads into a high-quality, normalized variant set suitable for downstream interpretation.

---

## Why This Matters

This stage demonstrates that:

- raw sequencing data was successfully transformed into a biologically plausible variant set  
- intermediate outputs meet expected statistical properties of human WGS data  
- downstream interpretation is grounded in validated inputs  

---

## Key Outputs

- Sorted, indexed BAM (alignment)
- Raw VCF (variant calls)
- Normalized VCF (post-processing)

---

## 🔗 Hallmark Artifacts

**Recommended reading order:** Validation Summary → QC Report → Variant Counts → Example Rows

- **Validation Summary (key metrics & conclusions)**  
  → [stage_01_06_validation_summary.md](./stage_01_06_validation_summary.md)

- **Alignment QC Report (mapping, pairing, mtDNA)**  
  → [stage_04_qc_report.md](./stage_04_qc_report.md)

- **Variant Count Sanity (raw vs normalized)**  
  → [stage_05_raw_vcf_variant_count.md](./stage_05_raw_vcf_variant_count.md)  
  → [stage_06_normalized_vcf_variant_count.md](./stage_06_normalized_vcf_variant_count.md)

- **Representative Variant Records (normalized VCF excerpt)**  
  → [stage_06_normalized_vcf_example_rows.md](./stage_06_normalized_vcf_example_rows.md)

- *(Optional)* **Per-contig Coverage (idxstats)**  
  → [stage_04_bam_idxstats_summary.md](./stage_04_bam_idxstats_summary.md)

---

## Summary

Stage 01–06 execution produced:

- ~4.66 million variants (expected for WGS)
- structurally valid BAM and VCF outputs
- no loss of variants during normalization

These results are consistent with expected properties of the HG002 benchmark genome.

---

## Artifact Notes

Artifacts are generated deterministically using Artificer and curated for clarity and interpretability.

See also: [HG002 Benchmarking Case Study](../../case_studies/hg002/README.md)