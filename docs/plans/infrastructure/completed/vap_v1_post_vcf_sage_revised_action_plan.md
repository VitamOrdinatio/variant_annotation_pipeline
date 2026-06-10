# VAP Scientific Requirements — Post-VCF Implementation

## Document Purpose

This document defines the **scientific and analytical requirements** for extending the Variant Annotation Pipeline (VAP) from:

```text
VCF generation → biologically and clinically meaningful interpretation
```

This document supersedes informal chat-based guidance and is intended to guide **DEX implementation decisions**.

---

# 1. Core Design Principle

## Rule 1 — Preserve the Master Callset

```text
Do NOT biologically narrow the variant set early.
```

### Required Architecture

```text
normalized VCF (master callset)
    ↓
annotation layer
    ↓
derived analysis views (non-destructive)
```

### Rationale

* Enables future noncoding interpretation
* Supports AlphaGenome / regulatory scoring
* Prevents re-running pipeline for new hypotheses
* Maintains reproducibility and auditability

---

# 2. Pipeline Structure (Post-VCF)

## Required Stages

| Stage | Name              | Type     |
| ----- | ----------------- | -------- |
| 01A   | FASTQ QC (FastQC) | REQUIRED |
| 01B   | Trimming          | OPTIONAL |
| 07    | Annotation        | REQUIRED |
| 08    | View Generation   | REQUIRED |
| 09    | QC Metrics        | REQUIRED |
| 10    | Prioritization    | REQUIRED |
| 11    | Reporting         | REQUIRED |

---

# 3. Stage 01A — FASTQ QC (FastQC)

## Objective

Assess raw read quality prior to alignment.

## Requirements

* Run FastQC on both paired FASTQ files
* Generate:

  * HTML reports
  * compressed QC outputs
* Store under:

  ```text
  results/<run_id>/qc/fastqc/
  ```

## Assumptions

* Input FASTQs are Illumina short-read data

## Limitations

* FastQC does not improve data quality
* Does not reduce runtime

## Edge Cases

* Adapter contamination
* Low-quality tails
* Overrepresented sequences

## Validation Strategy

* Confirm report generation
* Summarize:

  * per-base quality
  * adapter content
  * duplication levels

## Implementation Notes

* Must not modify input FASTQ files
* Outputs are diagnostic only

---

# 4. Stage 01B — Trimming (OPTIONAL)

## Rule

```text
Trimming must NOT be enabled by default.
```

## Objective

Remove adapters or low-quality sequence **only if justified by QC**

## Requirements

* Config-controlled execution:

  ```yaml
  preprocessing:
    run_trimming: false
  ```

## Assumptions

* Modern Illumina data is often already clean

## Limitations

* Adds runtime
* May not improve downstream results

## Edge Cases

* Adapter contamination
* Read pair desynchronization
* Altered read length distributions

## Validation Strategy

Must compare:

```text
trimmed vs untrimmed pipelines
```

Evaluate:

* mapping rate
* variant count
* Ti/Tv
* HG002 concordance (if applicable)

## Implementation Notes

* Preserve original FASTQ paths
* Track provenance in metadata

---

# 5. Stage 07 — Annotation Layer

## Objective

Create a **rich, master annotated variant table**.

## Requirements

### Minimum Fields

#### Core

* chromosome
* position
* REF / ALT

#### Functional

* gene symbol
* transcript ID
* exon/intron/intergenic
* consequence class
* amino acid change

#### Population

* gnomAD AF
* 1000 Genomes AF

#### Clinical (if available)

* ClinVar annotation

#### Noncoding Support

* genomic region classification
* nearest gene
* UTR / promoter / intronic flags

---

## Assumptions

* Transcript selection affects interpretation

## Limitations

* Annotation ≠ interpretation
* Noncoding annotation initially shallow

## Edge Cases

* multi-allelic sites
* transcript discordance
* missing annotation fields

## Validation Strategy

* annotation completeness rate
* AF fill-rate
* consequence distribution sanity check
* coding vs noncoding ratio

## Implementation Notes

* ANNOVAR acceptable for v1
* MUST normalize output into pipeline-defined schema
* preserve original coordinates

---

# 6. Stage 08 — View Generation (NOT destructive filtering)

## Rule

```text
Filtering must produce views, NOT destroy the master callset.
```

## Required Views

* qc_view.tsv
* coding_view.tsv
* noncoding_view.tsv
* rare_variant_view.tsv
* panel_overlap_view.tsv
* manual_review_view.tsv

---

## Assumptions

* Different biological questions require different subsets

## Limitations

* Views are convenience layers, not ground truth

## Edge Cases

* clinically relevant variants may be excluded in some views
* noncoding variants must remain available

## Validation Strategy

* track variant counts per view
* confirm master callset remains unchanged

## Implementation Notes

* filters must be YAML-configurable
* log all filter effects

---

# 7. Stage 09 — QC Metrics

## Objective

Ensure pipeline output is biologically and technically valid

## Required Metrics

* total variants
* SNP count
* indel count
* Ti/Tv ratio
* chromosome distribution
* annotation completeness
* per-view counts

---

## Assumptions

* HG002 is a benchmark, not a disease case

## Limitations

* QC strongest in benchmark regions only

## Edge Cases

* repetitive regions
* low coverage regions

## Validation Strategy

* compare to expected WGS ranges
* benchmark against known HG002 characteristics

## Implementation Notes

* output JSON + text summary

---

# 8. Stage 10 — Prioritization Layer

## Objective

Generate biologically meaningful candidate subsets

## Required Outputs

* coding_prioritized.tsv
* noncoding_prioritized.tsv
* gene_panel_prioritized.tsv

---

## Assumptions

* prioritization is context-dependent

## Limitations

* HG002 is not a disease sample

## Edge Cases

* panel hits ≠ pathogenic variants
* regulatory variants outside gene boundaries

## Validation Strategy

* count overlaps with gene sets
* verify retention of key annotation fields

## Implementation Notes

* DO NOT remove upstream evidence columns
* prioritize via ranking/scoring when possible

---

# 9. Stage 11 — Reporting

## Objective

Produce human-readable outputs without loss of provenance

## Required Outputs

* variant_summary.txt
* gene_summary.txt
* top_variants.tsv

---

## Assumptions

* users require readable summaries

## Limitations

* reports are summaries, not full data

## Edge Cases

* absence of evidence ≠ absence of variant

## Validation Strategy

* ensure report numbers match upstream tables

## Implementation Notes

* reports must reference source files

---

# 10. Storage Optimization Policy

## May Remove

* unsorted BAM
* temporary split files
* transient intermediates

## Must Keep

* sorted BAM + BAI
* normalized VCF + index
* annotation master table
* logs
* metadata

---

# 11. Definition of Pipeline Completion

Pipeline is complete when:

* master annotated callset exists
* multiple analysis views generated
* QC metrics validated
* prioritization outputs available
* reporting layer implemented

---

# 12. Strategic Outcome

This pipeline must demonstrate:

* end-to-end NGS capability
* reproducible analysis
* clinically relevant interpretation logic
* extensibility to noncoding / regulatory analysis

---

# End of Document

