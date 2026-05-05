# Variant Annotation Pipeline (VAP)

End-to-end whole-genome sequencing (WGS) pipeline that transforms raw FASTQ data into **structured, interpretable, and validated variant evidence**, demonstrating correct system behavior on a benchmark human genome (HG002).

---

## Pipeline Architecture

![VAP Pipeline Architecture](assets/vap_pipeline_architecture.png)

--

## 🧠 What This Project Proves

Most pipelines stop at variant annotation.

**VAP goes further.**

It demonstrates how genomic data can be transformed into a **decision-ready system** that:

- identifies candidate variants  
- prioritizes biologically meaningful signal  
- assigns validation requirements  
- avoids false-positive conclusions  

> **Key result:**  
> A healthy reference genome (HG002) produces **no high-priority variants**, confirming correct system calibration.

---

## 🔬 Key Metrics (HG002 Run)

- ~4.6 million variants processed  
- >99% QC pass rate  
- ~2.4% variants selected for validation  
- 0 high-priority (pathogenic) variants identified  
- deterministic mapping from prioritization → validation  

---

## 🔁 System Flow

```text
FASTQ
→ alignment (BWA)
→ BAM processing
→ variant calling (GATK)
→ VCF normalization
→ VEP annotation
→ structured variant datasets
→ interpretation (coding + noncoding)
→ prioritization
→ validation triage
→ system-level summary
```

---

## 🧬 Pipeline Stages
### Data Generation
  - FASTQ → BAM → VCF 
  - alignment, QC, variant calling 
### Annotation
  - VEP annotation (gene, transcript, consequence, population frequency) 
### Data Engineering (Stage 08)
  - schema-aligned, structured variant datasets 
  - VDB-ready outputs 
  - RDGP gene evidence seeds 
### Interpretation (Stage 09–10)
  - coding vs noncoding signal characterization 
  - identification of interpretable vs ambiguous variants 
### Prioritization (Stage 11)
  - tiered classification of variants 
  - identification of candidate variants 
### Validation (Stage 12)
  - assignment of validation requirements 
  - selective triage (~2.4% of variants) 
### System Summary (Stage 13)
  - confirmation of pipeline behavior 
  - validation of biological realism 
  - proof of correct system calibration 


---

## 🧠 System Behavior (HG002)
  - no pathogenic signal detected 
  - rare coding variants present but not overcalled 
  - noncoding variation dominates candidate space 
  - validation workload constrained and explainable 

**Conclusion:**
VAP behaves as a calibrated, biologically informed variant prioritization system.


---

## Start Here: Evidence of System Behavior

These artifacts provide the fastest review path for understanding VAP as an end-to-end genomic decision system.

1. [Stage 13 — System Behavior Summary](docs/examples/stage_13_final_summary/stage_13_system_behavior.md)  
   Final proof that VAP behaves correctly on HG002.

2. [Stage 13 — Final Run Report](docs/examples/stage_13_final_summary/stage_13_run_report.md)  
   Run-level summary, QC checks, assumptions, and non-goals.

3. [Stage 12 — Validation Summary](docs/examples/stage_12_validation/stage_12_validation_summary.md)  
   Validation triage logic and selective review behavior.

4. [Stage 11 — Prioritization Summary](docs/examples/stage_11_prioritization/stage_11_summary.md)  
   Priority tier behavior and absence of high-priority calls in HG002.

5. [Stage 08 — Filter & Partition Overview](docs/examples/stage_08_filter_partition/README.md)  
   Transition from annotation output to structured data products.

6. [Stage 01–06 — Foundation Validation](docs/examples/stage_01_06_foundation/stage_01_06_validation_summary.md)  
   Alignment, QC, variant calling, and normalization evidence.


---

## 🧠 Design Philosophy
VAP is designed as a modular, contract-driven system with clear separation of concerns:
  - data generation (VAP) 
  - data storage (VDB — planned) 
  - data interpretation (RDGP — planned) 

This ensures:
  - reproducibility 
  - auditability 
  - extensibility 


---

## 🧬 Why This Matters
Genomic pipelines are used in:
  - rare disease analysis 
  - clinical genomics 
  - translational research 

In these contexts, false positives are costly.

VAP demonstrates:
  - how to avoid overcalling 
  - how to preserve biological realism 
  - how to build interpretable pipelines 


---

## 🔧 Development Approach
This project was developed using a hybrid workflow:
  - manual system design and biological reasoning 
  - AI-assisted implementation 
  - continuous validation against expected genomic patterns 

AI accelerates development; system behavior and interpretation are manually verified.


---

## 📊 Dataset
  - GIAB HG002 (NA24385) 
  - SRA: SRR12898354 
  - benchmark-grade human WGS dataset 


---

## 🔁 Reproducibility
Each run includes:
  - run identifiers 
  - configuration snapshots 
  - structured outputs 
  - deterministic artifact generation 


---

## 🧭 Roadmap

```text
v1.0 → single-sample validated pipeline (current)
v1.1 → expanded annotation + tools
v2.0 → distributed multi-sample execution
v3.0 → cross-sample analysis + integration
```


---

## 🧠 Bottom Line
VAP demonstrates that raw genomic data can be transformed into:
> structured, interpretable, and validation-ready evidence — without overcalling biological signal

This is not just a pipeline.

It is a **coherent system for genomic decision-making.**

---
