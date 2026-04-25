# Variant Annotation Pipeline (VAP)

Built from raw WGS data (HG002, GIAB) with full pipeline execution through variant annotation.

A reproducible, end-to-end whole-genome sequencing (WGS) pipeline that transforms raw FASTQ data into annotated and biologically interpretable variant sets.

---

## 🚀 Current Status

VAP successfully executes end-to-end through **Stage 07 (VEP annotation)** on HG002 (GIAB benchmark dataset).

**Completed pipeline stages:**
- FASTQ ingestion
- BWA alignment
- BAM sorting and indexing
- aligned-read QC
- GATK HaplotypeCaller
- VCF normalization
- VEP annotation (offline mode)
- annotated VCF and TSV generation

Large genomic outputs (FASTQ, BAM, VCF, full TSV) are intentionally excluded from version control.  
Representative outputs and run summaries are provided below.

---

## 🔬 Execution Evidence (Stage 01–07)

These artifacts demonstrate successful pipeline execution on real WGS data:

### Output Manifest
- [Stage 07 Output Manifest](docs/examples/stage_07_output_manifest.md)

### Quality Control
- [Aligned-Read QC Report](docs/examples/stage_04_qc_report.md)

### Representative Outputs
- [Annotated Variant Columns](docs/examples/stage_07_columns.tsv)
- [Example Annotated Variants](docs/examples/stage_07_example_rows.tsv)
- [Missense Variant Examples](docs/examples/stage_07_missense_examples.tsv)
- [Stop-Gained Variant Examples](docs/examples/stage_07_stop_gained_examples.tsv)

### Annotation Evidence
- [VEP Summary Report](docs/examples/stage_07_vep_summary.html)
- [VEP Warnings Log](docs/examples/stage_07_vep_variants_vcf_warnings.txt)

---

## 🧠 Overview

The **variant_annotation_pipeline** is a reproducible workflow that transforms **raw WGS FASTQ data** into **annotated and biologically interpretable variant sets**.

It is designed to demonstrate how modern genomics pipelines can be built from first principles with emphasis on:

- reproducibility  
- biological interpretability  
- modular pipeline design  
- scalability from single-sample to cohort-level analysis  

---

## Purpose

This repository addresses a fundamental question in computational genomics:

```text
Can raw WGS FASTQ data be systematically transformed into
annotated and prioritized variant sets suitable for biological interpretation?
```

To answer this, the pipeline implements a complete workflow from **FASTQ → BAM → VCF → annotation → prioritization**, using widely adopted tools in clinical and research genomics.

---

## What This Project Demonstrates

* End-to-end NGS data processing from raw sequencing reads
* Integration of standard genomics tools (alignment, variant calling, annotation)
* Use of gene-set overlays for biologically informed variant prioritization
* Reproducible pipeline design aligned with modern software engineering practices
* A scalable architecture that supports distributed execution across multiple machines

---

## High-Level Pipeline

```text
FASTQ
→ alignment (BWA-MEM)
→ BAM processing (samtools)
→ variant calling (GATK)
→ VCF generation
→ variant annotation (VEP)
→ gene-set overlay annotation
→ prioritization
→ reporting
```

---

## Dataset (v1)

The initial implementation (v1.0) uses:

* **PRJNA200694 (GIAB)**
  * sample: HG002 (NA24385)
  * SRA run: SRR12898354
  * human whole-genome sequencing (WGS)
  * publicly available FASTQ data
  * benchmark-grade reference dataset

A single sample is processed end-to-end and validated against independently generated, sample-matched GIAB high-confidence small-variant callsets.

---

## Gene-Set Driven Prioritization

Beyond standard annotation, this pipeline introduces a **gene-set overlay layer** to support biologically meaningful prioritization.

Included gene sets:

* **MitoCarta** → nuclear-encoded mitochondrial genes
* **Genes4Epilepsy** → epilepsy-associated genes

Each variant is annotated with gene-set membership flags, enabling downstream filtering and interpretation.

---

## Reproducibility

Each pipeline run is fully reproducible and includes:

* run identifiers
* configuration snapshots
* tool version tracking
* structured outputs
* complete logging

The pipeline is designed to integrate with a broader **reproducible_pipeline_framework**.

---

## Project Structure

```text
variant_annotation_pipeline/
  data/
    interim/
    processed/
    raw/
  docs/
      implementation/
        aggregation_schema.md
        architecture_schema.md
        data_schema.md
        distributed_execution.md
        state_schema.md
        workflow.md  
      SOP/
        SOP_pipeline.md
        SOP_template.md
      design.md
      notes.md
      repo_brief_v1.md
  environment/
    README.md
  pipeline/
  results/
    figures/
    tables/
  scripts/
    README.md
  src/
  tests/
    README.md
  README.md
```

All detailed design specifications and implementation contracts are located in the docs/ directory.

---

## Roadmap

```text
v1.0 → single-sample end-to-end pipeline (FASTQ → BAM → VCF → interpretation)
v1.1 → analytical toolkit expansion (bcftools, BEDTools, VCFtools)
v1.2 → annotation resource expansion (gnomAD, ANNOVAR, etc.)
v1.3 → AI-based annotation (AlphaMissense, SpliceAI; AlphaGenome conceptual)
v2.0 → distributed batch execution across multiple machines
v3.0 → centralized aggregation and cross-sample comparative analysis
```

---

## Why This Matters

Variant annotation pipelines are foundational to:

* human genetics research
* rare disease analysis
* clinical genomics workflows

This project demonstrates not only how such a pipeline is built, but how it can be:

* rigorously designed
* reproducibly executed
* extended toward real-world biological questions

---

## Notes

* This pipeline produces **candidate variants for interpretation**, not clinical diagnoses.
* Advanced AI tools (e.g., AlphaGenome) are included as **conceptual extensions**, not required dependencies.
* Dataset expansions (e.g., epilepsy cohorts, trio analyses) are planned for future versions.

---

## Ecosystem Context (Planned Integration)

VAP is designed as part of a broader computational genomics system.

Planned downstream components include:

- **variant_database (VDB)**  
  Centralized storage and structured access layer for annotated variant data.

- **rnaseq_pipeline (RSP)**  
  Functional genomics pipeline for transcriptomic evidence integration.

- **rare_disease_gene_prioritization (RDGP)**  
  Gene-level prioritization using aggregated variant and functional evidence.

These components are currently under active design and will integrate with VAP outputs through defined system contracts.

---

## Sequence Data and Git

Large genomic outputs (FASTQ, BAM, VCF, full TSV) are intentionally excluded from version control due to size constraints.  
This repository instead tracks reproducible code, configuration, and representative outputs.

---

## Author

Designed as part of a portfolio project in computational genomics, integrating principles from molecular biology, bioinformatics, and software engineering.

---
