# Stage 04 — Alignment QC (VAP)

Stage 04 performs **quality control on aligned sequencing reads** following BAM generation.

This stage verifies that upstream alignment is successful before variant calling.

---

## What Stage 04 Does

- evaluates mapping quality and alignment completeness  
- validates paired-end read structure  
- provides confidence that downstream variant calling is meaningful  

---

## Key Artifact

- [Aligned-Read QC Report](stage_04_qc_report.md)

---

## Metrics Demonstrated

- total reads  
- mapped reads  
- mapping rate (~99% for HG002)  
- properly paired reads  
- pairing rate (~97–98%)  

---

## Interpretation Notes

- High mapping and pairing rates indicate:
  - correct reference genome usage  
  - successful alignment (BWA)  
  - readiness for variant calling  

- Poor QC here would invalidate downstream results  

---

## Role in the System

Stage 04 acts as a **validation checkpoint** between:

- alignment (Stage 02–03)  
→ and  
- variant calling (Stage 05)  

---

## Bottom Line

This stage demonstrates that the pipeline produces **high-quality aligned reads**, enabling reliable variant detection downstream.