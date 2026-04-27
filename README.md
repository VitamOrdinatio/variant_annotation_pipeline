# Variant Annotation Pipeline (VAP)

End-to-end whole-genome sequencing (WGS) pipeline executed on real data (HG002, GIAB), transforming raw FASTQ files into annotated variant datasets and structured, downstream-ready outputs.

---

## 🚀 Current Status

### Key Metrics

- Variants processed: `~4.6 million`  
- Irreparably malformed rows: `0`  
- QC pass rate: `>99%`

VAP successfully executes end-to-end through **Stage 08 (filtering and partitioning annotated variants)** on HG002 (GIAB benchmark dataset), with successful checkpoint execution on full dataset (~4.6M variants processed).

**Completed pipeline stages:**
- FASTQ ingestion
- BWA alignment
- BAM sorting and indexing
- aligned-read QC
- GATK HaplotypeCaller
- VCF normalization
- VEP annotation (offline mode)
- annotated VCF and TSV generation
- filtering and partitioning annotated variants

Large genomic outputs (FASTQ, BAM, VCF, full TSV) are intentionally excluded from version control.  
Representative outputs and run summaries are provided below.

---

## 🔬 Execution Evidence (Proven Pipeline Run)

These artifacts provide direct evidence of successful end-to-end execution on real WGS data (HG002).

### Output Manifest
- [Stage 08 Output Manifest](docs/examples/stage_08_filter_partition/stage_08_output_manifest.md)

### Quality Control
- [Aligned-Read QC Report](docs/examples/stage_04_qc/stage_04_qc_report.md)

### Representative Outputs
- [Annotated Variant Columns](docs/examples/stage_07_vep_annotation/stage_07_columns.tsv)
- [Example Annotated Variants](docs/examples/stage_07_vep_annotation/stage_07_example_rows.tsv)
- [Missense Variant Examples](docs/examples/stage_07_vep_annotation/stage_07_missense_examples.tsv)
- [Stop-Gained Variant Examples](docs/examples/stage_07_vep_annotation/stage_07_stop_gained_examples.tsv)

### Annotation Evidence
- [VEP Summary Report](docs/examples/stage_07_vep_annotation/stage_07_vep_summary.html)
- [VEP Warnings Log](docs/examples/stage_07_vep_annotation/stage_07_vep_variants_vcf_example_warnings.txt)


📁 All artifacts are organized by pipeline stage under `docs/examples/`.

---

## 🔬 End-to-End Pipeline Narrative

**Summary:**
- **Input → Output:** FASTQ → BAM → VCF → annotated variants → structured data products  
- **System transition:** bioinformatics pipeline → data engineering system  
- **Downstream readiness:** VDB (storage), RDGP (prioritization)

---

The Variant Annotation Pipeline (VAP) is designed to demonstrate how raw sequencing data can be transformed into structured, interpretable genomic evidence through a reproducible, contract-driven workflow.

### From Raw Data to Biological Context

The pipeline begins with raw whole-genome sequencing (WGS) data (FASTQ) and progresses through alignment, quality control, variant calling, and normalization.

- **Stage 04 (QC)** validates that sequencing reads are accurately aligned to the reference genome, ensuring downstream analyses are reliable.
- **Stage 07 (VEP Annotation)** enriches detected variants with gene, transcript, consequence, and population frequency information, producing structured variant-level records.

At this point, the pipeline has converted raw sequencing data into biologically meaningful annotations.

---

### From Annotation to Structured Data Products

Stage 08 represents a key architectural transition:

> the pipeline shifts from tool-driven processing to data engineering.

In this stage:

- ~4.6 million annotated variants are processed  
- 0 irreparably malformed records are observed  
- outputs are transformed into **schema-aligned, downstream-ready datasets**

Stage 08 produces:

- **VDB-ready variant records**  
  → normalized, lossless representations suitable for structured storage  

- **RDGP gene evidence seeds**  
  → aggregated gene-level summaries for prioritization workflows  

This stage demonstrates deterministic transformation of large-scale genomic data into structured outputs aligned with system contracts.

---

### Separation of Concerns (Design Philosophy)

VAP is intentionally designed to separate:

- **data generation (VAP)**  
- **data storage (VDB — planned)**  
- **data interpretation (RDGP — planned)**  

Stage 08 enforces this boundary by:

- preserving all annotation fields  
- avoiding irreversible filtering  
- deferring prioritization decisions  

This ensures that downstream systems operate on complete, unbiased data.

---

### Why This Matters

Most bioinformatics pipelines stop at annotation.

VAP goes further by demonstrating:

- how to structure variant data for database ingestion  
- how to aggregate variant signals into gene-level evidence  
- how to maintain reproducibility and traceability at scale  

This approach mirrors real-world clinical and research workflows, where:

- raw sequencing data must be transformed into reliable evidence  
- data must remain auditable and reproducible  
- interpretation must be layered on top of well-defined data contracts  

---

### Bottom Line

VAP demonstrates an end-to-end transformation:

`FASTQ → BAM → VCF → Annotated Variants → Structured Data Products → Gene-Level Evidence`


This pipeline is not just a collection of tools—it is a **coherent system for generating, structuring, and preparing genomic data for downstream analysis and clinical reasoning**.

It demonstrates how genomic data pipelines can be designed as **modular, contract-driven systems** rather than linear toolchains.

---

## 🔁 Pipeline Architecture

![VAP Pipeline](assets/vap_pipeline_architecture.png)

This architecture highlights the separation between variant generation, data engineering, and interpretation layers, with explicit bifurcation for coding and noncoding analysis.

---

## Stage 08 Evidence (Filtering & Partitioning)

Key results:

- ~4.6 million variants processed  
- 0 irreparably malformed rows  
- >99% QC pass rate  

### Representative Outputs

- [Stage 08 Summary](docs/examples/stage_08_filter_partition/stage_08_summary.json)
- [Coding Candidate Examples](docs/examples/stage_08_filter_partition/coding_candidates/coding_candidates_excerpt.md)
- [Noncoding Candidate Examples](docs/examples/stage_08_filter_partition/noncoding_candidates/noncoding_candidates_excerpt.md)
- [RDGP Gene Evidence (Seed)](docs/examples/stage_08_filter_partition/rdgp_gene_evidence/rdgp_seed_overview.md)
- [RDGP Summary Counts](docs/examples/stage_08_filter_partition/rdgp_gene_evidence/rdgp_summary_counts_only.md)

🔗 [Explore all Stage 08 outputs](docs/examples/stage_08_filter_partition/)

---

## 🧠 Overview

The **variant_annotation_pipeline** is a reproducible workflow that transforms **raw WGS FASTQ data** into **annotated and structured variant datasets** suitable for downstream analysis.

It emphasizes:

- reproducibility  
- modular pipeline design  
- biological interpretability  
- scalable architecture  

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

## Version Status

**Current milestone:** `v0.5.0`

VAP is operational through Stage 08, including:
- FASTQ → BAM → VCF → VEP annotation
- filtering and partitioning of annotated variants
- corrected gene ID mapping
- VDB-ready variant outputs
- RDGP gene evidence seed outputs

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
