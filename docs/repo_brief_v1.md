# repo_brief.md

## Variant Annotation Pipeline — v1.0 Implementation Contract

---

# 1. Purpose

This repository implements a **reproducible, single-sample variant annotation pipeline** that processes **raw WGS FASTQ data** into **annotated and prioritized variant outputs**.

The pipeline demonstrates:

* FASTQ → BAM → VCF processing
* variant annotation using standard clinical genomics tools
* biologically informed prioritization using gene-set overlays
* reproducible pipeline execution aligned with `reproducible_pipeline_framework`

---

# 2. Scope (v1.0)

## Included

* single-sample analysis
* WGS FASTQ input
* full pipeline execution (FASTQ → BAM → VCF → annotation → prioritization)
* gene-set overlay prioritization
* reproducible outputs and logging

## Excluded

* multi-sample processing
* batch execution
* cohort-level analysis
* AI-based prediction tools
* alternative variant callers (DeepVariant, etc.)

---

# 3. Primary Dataset

- BioProject: PRJNA200694 (GIAB)
  - sample: HG002 (NA24385)
  - SRA run: SRR12898354
  - input: paired-end WGS FASTQ
  - human WGS
  - public FASTQ
  - reference genome: GRCh38
  - benchmark-grade reference

## Dataset Notes

This implementation uses a single publicly available WGS sequencing run from the GIAB project:

- SRR12898354 corresponds to HG002, a benchmark human genome sample widely used for validation.

- This run serves as the FASTQ input for the pipeline.

- Validation is performed against **independently generated, sample-matched GIAB high-confidence variant callsets**, not a VCF derived solely from this single sequencing run.

HG002 is selected as the initial v1 sample due to its extensive benchmark resources and widespread use in variant calling validation.

---

# 4. Validation Strategy

The pipeline must support validation by:

```text
Compare generated VCF against independently generated, sample-matched GIAB high-confidence small-variant callsets
(HG002, GRCh38).
```

This is used to confirm correctness of the variant calling workflow.

---

# 5. Pipeline Overview

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

# 6. Required Tools (v1)

## Core Tools

* BWA-MEM → alignment
* samtools → BAM processing (sorting, indexing, QC)
* GATK → variant calling (best practices workflow)
* Ensembl VEP → variant annotation (ClinVar, consequence terms)
* Python (pandas) → data processing

---

## Visualization

* IGV → manual validation of variant evidence

---

# 7. Gene-Set Overlay Layer

Gene sets must be integrated as **post-annotation overlays**.

## Required Gene Sets

* MitoCarta → mitochondrial-associated genes
* SAGAS → epilepsy-associated genes
* Genes4Epilepsy → epilepsy-associated genes

---

## Implementation Requirement

Each annotated variant must include flags:

```text
mito_flag
epilepsy_flag
```

---

# 8. Output Requirements

Each run must generate a structured output directory:

```text
results/<run_id>/
```

---

## Core Outputs

* aligned.bam
* aligned.bam.bai
* variants.vcf or variants.vcf.gz

---

## Annotation Outputs

* annotated_variants.tsv
* prioritized_variants.tsv

(optional intermediate outputs such as track-specific tables may be produced)

---

## Summary Outputs

* gene_summary.tsv
* run_summary.md

---

# 9. Output Semantics

## annotated_variants.tsv

Must include:

* genomic coordinates
* gene assignment
* consequence type
* population frequency (if available via VEP)
* clinical annotation (ClinVar if available)
* gene-set flags

---

## prioritized_variants.tsv

Filtered subset based on:

* rarity
* functional consequence
* gene-set membership

---

# 10. Execution Requirements

## CLI Interface

Pipeline must be executable as:

```bash
python run_pipeline.py --input <FASTQ> --output <dir>
```

---

## Determinism

* identical inputs must produce identical outputs
* all parameters must be recorded

---

## Logging

Each run must generate:

* execution logs
* tool versions
* configuration snapshot

---

# 11. Reproducibility Requirements

Each run must include:

* run_id
* reference genome version (GRCh38)
* tool versions
* pipeline version

---

# 12. Storage Policy (v1)

Retain all intermediate and final files:

* FASTQ
* BAM
* VCF
* annotations

No deletion occurs in v1.

---

# 13. Alignment with Framework

Pipeline must:

* follow `reproducible_pipeline_framework` structure
* implement stage-based execution
* maintain a state object across stages

---

# 14. Non-Goals (Explicit)

The following are **not required in v1**:

* batch processing
* distributed execution
* DeepVariant
* SpliceAI / AlphaMissense / AlphaGenome
* ANNOVAR / SnpEff
* cohort analysis

---

# 15. Success Criteria

The implementation is successful if:

```text
1. Pipeline executes end-to-end from FASTQ input
2. Produces valid BAM and VCF outputs
3. Generates annotated variant tables
4. Applies gene-set overlays correctly
5. Outputs are reproducible
6. Variant calls are broadly consistent with sample-matched GIAB high-confidence callsets for HG002 on GRCh38
```

---

# End of Repo Brief (v1.0)
