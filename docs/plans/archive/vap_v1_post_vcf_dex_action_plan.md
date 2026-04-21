# Variant Annotation Pipeline — Action Plan (Post-VCF Generation)

## Purpose
This document defines the next-phase implementation plan for extending the current pipeline from **variant generation → variant interpretation**.

Current pipeline status:
- FASTQ → BAM → VCF ✔
- Variant normalization ✔
- Annotation ❌
- Filtering ❌
- Interpretation ❌
- Reporting ❌

Goal:
Transform pipeline into a **clinically relevant, end-to-end variant interpretation system** aligned with real-world bioinformatics analyst workflows.

---

# 0. Current State Assessment

## Completed Outputs
- aligned BAM (~23 GB)
- BAM index (.bai)
- raw VCF (~889 MB)
- normalized VCF (~889 MB)
- VCF index

## Confirmed Success Criteria
- No active processes
- All expected intermediate artifacts present
- File sizes consistent with full HG002 run

## Known Gaps
- No annotation layer
- No filtering/prioritization
- No QC metrics surfaced
- No final outputs (tables, reports)

---

# 1. Pipeline Expansion Overview

## New Stages to Implement

| Stage | Name                     | Priority | Description |
|------|--------------------------|----------|------------|
| 07   | Annotation               | CRITICAL | Functional + population annotation |
| 08   | Filtering                | CRITICAL | Reduce to biologically meaningful variants |
| 09   | QC Metrics               | HIGH     | Generate pipeline-level statistics |
| 10   | Gene Prioritization      | HIGH     | Focus on disease-relevant genes |
| 11   | Reporting               | HIGH     | Produce interpretable outputs |

---

# 2. Stage 07 — Variant Annotation (CRITICAL)

## Tool Options
- ANNOVAR (recommended first implementation)
- VEP (future extension)

## Selected Tool
- ANNOVAR (initial implementation simplicity)

## Annotation Targets

### Functional Annotation
- Gene name
- Exonic function (synonymous, nonsynonymous, stopgain, etc.)
- Amino acid change

### Population Frequency
- gnomAD / ExAC allele frequency
- 1000 Genomes frequency

### Clinical Databases (future extension)
- ClinVar
- HGMD (if available)

## Inputs
- normalized_variants.vcf

## Outputs
- annotated_variants.txt (ANNOVAR format)
- multianno.txt (final merged annotation table)

## Implementation Tasks

- [ ] Install ANNOVAR locally
- [ ] Download annotation databases
- [ ] Convert VCF → ANNOVAR input format
- [ ] Run table_annovar.pl
- [ ] Store outputs in:
results/<run_id>/processed/annotation/


---

# 3. Stage 08 — Variant Filtering (CRITICAL)

## Objective
Reduce millions of variants → manageable candidate set

## Filtering Strategy (Initial)

### Quality Filters
- QUAL > 30
- DP > 10

### Population Filters
- Remove variants with AF > 0.01

### Functional Filters
- Keep:
- nonsynonymous
- stopgain
- frameshift

## Output
- filtered_variants.tsv

## Implementation Tasks

- [ ] Parse ANNOVAR output
- [ ] Apply filters using Python (pandas)
- [ ] Save filtered dataset

---

# 4. Stage 09 — QC Metrics (HIGH PRIORITY)

## Objective
Provide pipeline validation and sanity checks

## Metrics to Generate

- Total variants
- SNP count
- Indel count
- Ti/Tv ratio
- Mean depth (if extractable)
- Chromosome distribution

## Output
- qc_metrics.json
- qc_summary.txt

## Implementation Tasks

- [ ] Parse VCF
- [ ] Compute metrics
- [ ] Store results in:
results/<run_id>/processed/qc/

---

# 5. Stage 10 — Gene Prioritization (HIGH PRIORITY)

## Objective
Focus analysis on biologically relevant targets

## Strategy (Phase 1)

### Gene Lists
- MitoCarta genes
- POLG-related pathways
- Custom disease gene panels

### Filtering Logic
- Keep variants in genes of interest

## Output
- prioritized_variants.tsv

## Implementation Tasks

- [ ] Import gene list
- [ ] Cross-reference with annotated variants
- [ ] Filter dataset

---

# 6. Stage 11 — Reporting (HIGH PRIORITY)

## Objective
Generate human-readable outputs

## Output Types

### Tables
- top_variants.tsv
- prioritized_variants.tsv

### Summaries
- variant_summary.txt
- gene_summary.txt

### (Future)
- PDF report
- visualization plots

## Implementation Tasks

- [ ] Format output tables
- [ ] Generate summary statistics
- [ ] Write human-readable report

---

# 7. Performance Optimization (Parallel Track)

## Goals
Reduce runtime and improve scalability

## Improvements

- [ ] Split HaplotypeCaller by chromosome
- [ ] Parallel execution (GNU parallel or Python multiprocessing)
- [ ] Merge VCF outputs

---

# 8. Storage Optimization (Immediate Fix)

## Problem
Redundant BAM files consuming space

## Actions

- [ ] Remove unsorted BAM after validation:
rm aligned.bam

- [ ] Add cleanup step in pipeline

---

# 9. Pipeline Integration Plan

## Directory Structure (New Additions)
results/<run_id>/
│
├── interim/
├── processed/
│   ├── annotation/
│   ├── filtered/
│   ├── qc/
│   ├── prioritized/
│
├── reports/
│
└── logs/

---

# 10. SOP Alignment (IMPORTANT)

Each new stage must include:

- Input definition
- Output definition
- Command used
- Expected runtime
- Failure modes
- Validation checks

Create:
- SOP_annotation.md
- SOP_filtering.md
- SOP_qc.md

---

# 11. Immediate Next Steps (Execution Order)

## Phase 1 (Do First)
- [ ] Confirm logs are clean
- [ ] Count total variants
- [ ] Remove redundant BAM

## Phase 2 (Core Build)
- [ ] Install ANNOVAR
- [ ] Implement annotation stage
- [ ] Validate annotation output

## Phase 3 (Interpretation)
- [ ] Implement filtering
- [ ] Generate QC metrics

## Phase 4 (Value Layer)
- [ ] Add gene prioritization
- [ ] Generate reports

---

# 12. Definition of “Pipeline Complete”

Pipeline is considered complete when:

- [ ] Annotated variants generated
- [ ] Filtered variant set produced
- [ ] QC metrics available
- [ ] Gene-prioritized results generated
- [ ] Human-readable report produced

---

# 13. Strategic Outcome

Upon completion, this pipeline will demonstrate:

- End-to-end NGS analysis capability
- Variant interpretation proficiency
- Clinical bioinformatics readiness
- Reproducible pipeline engineering

This directly aligns with:
- Genome Bioinformatics Analyst roles
- Clinical genomics pipelines
- Rare disease variant analysis workflows

---

# 14. Notes for Future Extensions

- CNV integration
- mtDNA / heteroplasmy analysis
- Machine learning prioritization
- Database integration (PostgreSQL)
- Web-based visualization layer

---
