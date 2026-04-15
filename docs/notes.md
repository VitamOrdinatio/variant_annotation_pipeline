# Notes

## `variant_annotation_pipeline`

---

# 1. Purpose

This repository implements a **reproducible, end-to-end variant annotation pipeline** that begins with **raw WGS FASTQ data** and produces **biologically interpretable variant outputs**.

The pipeline is designed to demonstrate:

* NGS data processing from **FASTQ → BAM → VCF**
* integration of standard tools used in clinical genomics workflows
* coding and non-coding variant annotation
* biologically motivated variant prioritization
* reproducible pipeline design using the `reproducible_pipeline_framework`

---

# 2. Scientific Objective

## Primary Objective

```text
Demonstrate that a reproducible pipeline can transform raw WGS sequencing data
into annotated and prioritized variants suitable for biological interpretation.
```

## Secondary Objective

```text
Identify and annotate variants occurring in mitochondrial-associated genes
(MitoCarta) and/or epilepsy-related genes (enes4Epilepsy), permitting comparisons of variant sets for downstream analysis.
```

---

# 3. Scope (Version 1)

## Included

* single-sample analysis
* WGS FASTQ input
* full 13-stage pipeline execution
* coding + non-coding variant annotation
* mitochondrial gene prioritization
* reproducible outputs and logging

## Excluded

* multi-sample cohort comparison
* statistical enrichment analysis
* clinical diagnosis claims
* mtDNA heteroplasmy or deletion analysis
* deep-learning model dependency (AlphaGenome, etc.)

---

# 4. Version Roadmap (High-Level)

```text
v1.0 → single-sample end-to-end pipeline (FASTQ → BAM → VCF → interpretation)
v1.1 → enhanced analytical toolkit
v1.2 → extended annotation and reference resources
v1.3 → AI predictive interpretation layer
v2.0 → distributed manifest-driven batch execution across multiple machines
- multiple machines can process different samples independently
- sample-level outputs are generated in a consistent format
v3.0 → centralized aggregation and cross-sample comparative analysis




```

## Tool and Dataset Usage Across Roadmap Trajectory 

These are required tools or datasets for this repository. Alternatives can be suggested by SWE agent, but their usage must receive final approval by the user.

**v1.0 single-sample end-to-end pipeline**

**v1.0 datasets**
- dataset: BioProject PRJNA200694 (GIAB); we select a single SRA (WGS) in which a VCF has already been generated outside of the variant_annotation_pipeline.
1. Success of our variation_annotation_pipeline analysis will be benchmarked against the independently-verified VCF.
2. Benchmark against independently-generated high-confidence VCF
(e.g., GIAB truth set where applicable)

**v1.0 gene lists**
- gene-set overlay layer (used for post-annotation variant prioritization): 
1. MitoCarta (gene list of nuclear-encoded mitochondrial genes)
2. Genes4Epilepsy (gene list of epilepsy genes) 

**v1.0 tools**
- tool: BWA (mapping, alignment)
- tool: samtools (BAM processing, sorting, indexing, QC metrics)
- tool: GATK (variant calling, pre-processing best practices)
- tool: VEP (core annotation, ClinVar)
- tool: pandas (dataframes)
- tool: IGV (validation)

**v1.1 enhanced analytical toolkit**
- tool: bcftools (VCF manipulation)
- tool: BEDTools (interval logic, genome arithmetic, intersect gene-lists like MitoCarta and Genes4Epilepsy)
- tool: VCFtools (summary statistics, filtering, richer VCF-analysis toolkit)
- tool: SnpEff (alternative / comparison annotation engine)

**v1.2 extended annotation and reference resources**
- tool: CMAT (a ClinVar mapping and annotation toolkit for ontology associations and related mappings)
- tool: gnomAD (population-based filtering)
- tool: ExAC (population-based filtering)
- tool: ANNOVAR (alternative / comparison annotation engine)

**v1.3 AI predictive interpretation layer**
- tool: AlphaMissense (AI prediction, optional: not required for core execution)
- tool: SpliceAI (AI prediction, optional: not required for core execution)
- tool: AlphaGenome (non-coding regulatory modeling; conceptual integration only)

**v2.0 distributed manifest-driven batch execution across multiple machines**
- manifest-driven, batch operator demo over a small manifest, not full BioProject ingestion

**v2.0 core batch-ready datasets**
- dataset: BioProject PRJNA200694 (GIAB), multiple sequencing runs of same reference individual → used for reproducibility, not cohort diversity
- dataset: BioProject PRJEB6930 (1KG) is a future batch-ready public WGS reference set for comparison

**v2.0 disease-extension datasets**
- dataset: BioProject PRJEB57558 (Saudi epilepsy cohort); 144 SRAs that are WES
- dataset: BioProject PRJNA574037 (unverified; candidate dataset) contains reads for targeted amplicons derived from a single mitochondrial disease patient; the 17 nuclear-encoded amplicon targets are POLG, DNA2, RRM2B, TK2, DGUOK, MPV17, MNF2, SUCLA2, OPA1, SLC25A4, FBXL4, SPG7, POLG2, MGME1, RNASEH1, SUCLG1 and TWNK. Useful for disease extension of our repo pipeline.
- dataset: BioProject PRJNA1434109 (unverified; candidate dataset) contains a family cohort (patient, mother and father) of WGS data. Patient exhibits the CACNA1A c.5610del and presents with epilepsy with ataxia / migraine. Useful for disease extension of our repo pipeline.

**v3.0 centralized aggregation and cross-sample comparative analysis**
- tool: DeepVariant (alternate variant caller to GATK, useful for variant call comparisons)
- tool: dv-trio (a trio-aware version incorporating DeepVariant, GATK co-calling and FamSeq to improve Mendelian consistency)
- tool: RecallME (benchmarking / optimization tool for variant calling pipelines, designed for VCF comparison and caller evaluation)
          
---

# 5. Input Data

## Primary Dataset

PRJNA200694 (GIAB)

* human whole-genome sequencing (WGS)
* FASTQ available via SRA/ENA
* gold-standard benchmark dataset

## Input Type

* paired-end FASTQ

## Reference Genome

* GRCh38

---

# 6. Pipeline Overview

```text
FASTQ
→ alignment (BWA-MEM)
→ BAM processing (samtools)
→ variant calling (GATK)
→ VCF normalization
→ variant annotation (VEP)
→ filtering and prioritization
→ mitochondrial gene overlay (MitoCarta)
→ epilepsy gene set overlay (Genes4Epilepsy)
→ reporting
```

---

# 7. Core Tools (v1 Implementation)

* BWA-MEM
* samtools
* GATK
* Ensembl VEP
* ClinVar
* Python (pandas)

---

# 8. Annotation Sources

* gnomAD (via VEP)
* ClinVar (via VEP)
* Sequence Ontology consequence terms
* dbSNP (reference variant database)

---

# 9. Outputs

## Core Outputs

* `aligned.bam`
* `aligned.bam.bai`
* `variants.vcf` or `variants.vcf.gz`

---

## Annotation Outputs

* `annotated_variants.tsv`
* `prioritized_variants.tsv`

---

## Summary Outputs

* `gene_summary.tsv`
* `mitochondrial_variants.tsv`
* `epilepsy_variants.tsv`
* `run_summary.md`

---

# 10. Variant Prioritization Strategy

## Annotation Layer

Each variant includes:

* gene assignment
* consequence type (coding / non-coding)
* population allele frequency (gnomAD / ExAC legacy context / 1KG)
* clinical annotation (ClinVar, if available)

---

## Filtering Strategy

* retain all variants for annotation
* apply prioritization filters downstream

---

## Prioritization Criteria

* rare variants (low population frequency)
* coding consequences (missense, nonsense, splice-region)
* non-coding variants retained for future interpretation
* coding variants in mitochondrial-associated genes flagged (MitoCarta)
* coding variants in epilepsy-associated genes flagged (Genes4Epilepsy)

---

## Output Philosophy

```text
The pipeline produces candidate variants for biological interpretation,
not definitive clinical diagnoses.
```

---

# 11. Reproducibility Requirements

* each run includes:
  * run_id
  * configuration snapshot
  * logs
* deterministic outputs given identical inputs
* CLI-based execution
* alignment with `reproducible_pipeline_framework`

---

# 12. Storage Retention Policy

## v1 (Development Mode)

Retain all files:

* FASTQ
* BAM
* VCF
* annotations
* logs

---

## v2+ (Batch Mode)

After successful completion:

### Retain

* BAM + index
* VCF (preferably compressed)
* annotated outputs
* summary outputs
* logs and config

---

### Optional Deletion

```text
FASTQ files may be deleted after:
- BAM is verified
- VCF is generated
- annotation is complete
- run is marked successful
```

---

## Reproducibility Safeguard

* store SRA accession
* store download commands
* store reference genome version
* store pipeline version

---

# 13. Standard Operating Procedures (SOPs)

This repository follows an SOP-driven design:

* `SOP_template.md` → general pipeline structure
* `SOP_pipeline.md` → variant annotation workflow

Each stage defines:

* inputs
* outputs
* QC checks
* reproducibility requirements

This structure mirrors best practices in regulated and clinical genomics environments.

---

# 14. Supported Tools and Resources (Portfolio Alignment)

This pipeline is designed to align with common clinical genomics workflows and demonstrate familiarity with widely used tools and datasets.

---

## Core Data Types

* FASTQ (raw reads)
* BAM (aligned reads)
* VCF (variant calls)

---

## Visualization and Validation

* IGV

  * recommended for manual inspection of variant evidence

---

## Population and Reference Datasets

* PRJEB6930 (1KG)
* ExAC
* gnomAD (primary population dataset via VEP)

---

## Clinical Databases

* ClinVar (integrated via VEP)
* HGMD (not included in v1; potential future integration)

---

## Alternative Annotation Tools

* ANNOVAR (alternative annotation framework; not used in v1)

---

## AI/ML-Based Variant Interpretation (Future Integration)

* AlphaMissense (coding variant pathogenicity prediction)
* SpliceAI (splice impact prediction)
* AlphaGenome (non-coding regulatory variant modeling)

These tools are not required for v1 execution but are supported conceptually in pipeline design.

---

## Benchmark Dataset

* PRJNA200694

---

# 15. Limitations

* single-sample analysis (v1)
* no cohort-level inference
* limited non-coding interpretation (annotation only)
* no mtDNA deletion or heteroplasmy modeling
* dependent on sequencing quality

---

# 16. Design Principles

```text
- reproducibility over speed
- clarity over complexity
- single-sample correctness before scaling
- extensibility toward modern genomics tools
```

---

# 17. Implementation Notes for SWE Agent

* must follow `reproducible_pipeline_framework` architecture
* stage-based execution (13-stage pipeline)
* maintain a state object across stages
* support CLI execution for single-sample mode (v1)
* batch mode reserved for v2

---

# End of Notes
