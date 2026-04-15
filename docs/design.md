# design.md

## Variant Annotation Pipeline — System Design & Experimental Framework

---

# 1. Project Philosophy

This repository is designed as a **reproducible, extensible variant annotation pipeline** built from first principles.

The design prioritizes:

* reproducibility over speed
* biological interpretability over raw output
* single-sample correctness before scaling
* explicit experimental design before implementation

This reflects a traditional experimental biology approach applied to modern computational genomics.

---

# 2. Experimental Design

## Core Question

```text
Can a reproducible pipeline transform raw WGS FASTQ data
into biologically interpretable and prioritized variant sets?
```

---

## Dataset

Primary dataset:

* PRJNA200694 (GIAB)
  * sample: HG002 (NA24385)
  * SRA run: SRR12898354
  * human WGS
  * public FASTQ
  * benchmark-grade reference

---

## Method

```text
FASTQ → alignment → BAM → variant calling → VCF → annotation → prioritization → reporting
```

---

## Outputs

* annotated variant tables
* prioritized variant tables
* gene-set overlays
* summary reports

---

## Validation

```text
Compare generated VCF against independently generated, sample-matched GIAB high-confidence small-variant callsets (HG002, GRCh38).
```

---

## Limitations

* single-sample design (v1)
* no cohort-level inference
* no mtDNA structural variant modeling
* limited non-coding interpretation (annotation only)

---

# 3. Dataset Strategy

## Tier 1 — Core Pipeline Datasets

* GIAB → validation and correctness
* 1000 Genomes → generalization (v2+)

---

## Tier 2 — Disease Extension

* PRJEB57558 → epilepsy cohort (WES)
* PRJNA1434109 → trio WGS *(unverified)*

---

## Tier 3 — Specialized Datasets

* PRJNA574037 → targeted amplicon *(unverified)*

---

## Assay Considerations

```text
WGS → full coding + non-coding space  
WES → coding-focused  
Amplicon → highly targeted  
```

These datasets are not directly comparable.

---

# 4. Pipeline Architecture

## Layer 1 — Single-Sample Pipeline

```text
FASTQ → BAM → VCF → annotation → prioritization
```

---

## Layer 2 — Batch Execution

```text
manifest → multiple independent sample runs
```

---

## Layer 3 — Aggregation

```text
sample outputs → unified dataset → comparative analysis
```

---

# 5. Distributed Compute Strategy

This pipeline is designed to operate across multiple independent machines.

## Model

```text
Machine 1 → sample A  
Machine 2 → sample B  
Machine 3 → sample C  
...
```

Each run is independent.

---

## Key Principle

```text
One sample = one self-contained analysis unit
```

---

## Reunification

All outputs are later consolidated on a central system (Sys76 laptop):

```text
results/ → merged → comparative analysis
```

---

# 6. Gene Set Strategy

Gene sets are used as **annotation overlays**, not primary datasets.

## Included Gene Sets

* MitoCarta → mitochondrial genes
* SAGAS → epilepsy genes
* Genes4Epilepsy → epilepsy genes

---

## Integration

Each variant is annotated with:

```text
mito_flag  
epilepsy_flag  
```

---

## Purpose

```text
Enable biologically informed prioritization
```

---

# 7. Version Roadmap

```text
v1.0 → single-sample pipeline (FASTQ → BAM → VCF → interpretation)
v1.1 → analytical toolkit expansion
v1.2 → annotation/resource expansion
v1.3 → AI predictive annotation layer
v2.0 → distributed manifest-driven batch execution
v3.0 → centralized aggregation and comparative analysis
```

---

# 8. Tooling Strategy

## v1 Core Tools

* BWA
* samtools
* GATK
* VEP
* pandas
* IGV

---

## v1.1 Analytical Tools

* bcftools
* BEDTools
* VCFtools
* SnpEff

---

## v1.2 Annotation Expansion

* gnomAD
* ExAC
* ANNOVAR
* CMAT

---

## v1.3 AI Layer

* AlphaMissense
* SpliceAI
* AlphaGenome *(conceptual only)*

---

# 9. Feasibility & Hardware Constraints

## Hardware Model

* primary system: Sys76 laptop
* auxiliary systems: multiple laptops/desktops

---

## Execution Strategy

```text
v1 → single machine  
v2 → distributed execution across machines  
```

---

## Expected Runtime

* alignment → hours
* variant calling → overnight to multi-day
* annotation → hours

---

## Bottleneck

```text
GATK variant calling
```

---

# 10. Output Design

Per-sample outputs:

* BAM / index
* VCF
* annotated_variants.tsv
* prioritized_variants.tsv
* gene_summary.tsv
* run_summary.md

---

# 11. Reproducibility Model

Each run includes:

* run_id
* config snapshot
* logs
* tool versions
* reference genome version

---

# 12. Storage Strategy

## v1

Retain all files.

---

## v2+

Retain:

* BAM
* VCF
* annotations

Optionally delete:

* FASTQ (after verification)

---

# 13. SOP Integration

This project uses:

* SOP_template.md
* SOP_pipeline.md

Each stage defines:

* inputs
* outputs
* QC checks
* reproducibility constraints

---

# 14. Future Directions

* DeepVariant integration
* dv-trio for family-based analysis
* RecallME benchmarking
* cohort-level normalization
* publication-ready datasets

---

# 15. Design Principles

```text
- reproducibility over speed  
- clarity over complexity  
- correctness before scaling  
- modular, extensible architecture  
```

---

# 16. State Requirements and Distributed Execution Design

## 16.1 Purpose

This pipeline must support both:

* single-sample execution on one machine
* distributed multi-machine execution in which different machines process different samples independently

The state model must therefore support:

```text
per-sample reproducibility
distributed execution
later reunification on a central machine
```

---

## 16.2 Core State Principles

### Principle 1 — One Sample = One Independent Run

Each sample must be processed as a fully self-contained analysis unit.

This means:

* no shared mutable state across machines
* no assumption that multiple samples are processed on the same machine
* no dependence on another sample’s completion for single-sample execution

---

### Principle 2 — Every Run Must Be Reconstructible

Each completed run must emit enough metadata to reconstruct:

* what sample was processed
* where it came from
* what software version was used
* what reference genome was used
* what outputs were generated
* whether the run succeeded or failed

---

### Principle 3 — Aggregation Must Not Depend on FASTQ Retention

Later comparative analysis on the central Sys76 machine must not require raw FASTQ files to still be present locally.

Reunification must instead depend on:

* machine-readable metadata
* stable sample identifiers
* preserved output files
* preserved provenance information

---

### Principle 4 — Successful and Failed Runs Must Be Programmatically Distinguishable

A run must always end in a machine-readable status such as:

```text
completed
failed
partial
```

This is required for:

* batch execution
* resume behavior
* aggregation
* debugging

---

## 16.3 Minimum Per-Sample State Requirements

Every per-sample run must record, at minimum:

* `sample_id`
* `run_id`
* `bioproject_accession`
* `sra_accession`
* `reference_genome`
* `pipeline_version`
* `config_version` or config snapshot path
* `machine_id` or hostname
* `start_time`
* `end_time`
* `status`
* stage completion status
* key output file paths
* validation status
* warnings / errors

---

## 16.4 Distributed Execution Requirements

For distributed multi-machine execution:

* each machine receives a subset manifest or one sample at a time
* each machine executes the same pipeline version
* each machine must produce outputs in the same directory structure and metadata format
* each machine must emit a machine-readable run record suitable for later aggregation
* sample identifiers must remain stable across all machines

---

## 16.5 Aggregation Requirements

The central aggregation system (Sys76) must be able to reunify per-sample outputs without ambiguity.

To support this, each completed sample run must expose:

* stable sample identifier
* source dataset identifiers
* machine-readable metadata
* prioritized variant outputs
* summary outputs
* success / failure status

Aggregation must be able to:

* ignore failed runs safely
* merge successful runs consistently
* preserve provenance
* support later comparative analysis

---

## 16.6 State Design Philosophy

The pipeline state should be understood in two layers:

### Layer A — Per-Sample Pipeline State

Tracks one sample through:

```text
FASTQ → BAM → VCF → annotation → prioritization
```

### Layer B — Aggregation State

Tracks multiple completed sample runs during reunification and comparative analysis.

These two layers must remain conceptually distinct.

---

## 16.7 Division of Responsibility

### Research Agent responsibilities

Research Agent defines:

* what state must guarantee
* which identifiers and provenance fields are scientifically required
* what information must survive distributed execution
* what aggregation must be able to recover later

### SWE Agent responsibilities

SWE Agent defines:

* exact state schema
* required vs optional fields
* serialization format
* file naming conventions
* machine-readable metadata structure
* resume / retry / skip-if-complete behavior
* aggregation implementation details

---

## 16.8 Required Future Implementation Documents

The following implementation-facing documents should be created by SWE Agent:

* `docs/state_schema.md`
* `docs/aggregation_schema.md`
* `docs/distributed_execution.md`

These documents should formalize the requirements described here.

---

## 16.9 Guiding Rule

```text
Research Agent defines the invariants.
SWE Agent defines the implementation.
```

---

# 17. Stage Intent Map (v1 of variant_annotation_pipeline)

stage_01: FASTQ ingestion
    - input: raw FASTQ
    - goal: validate and prepare reads
    - notes: ensure integrity, correct pairing

stage_02: alignment
    - input: FASTQ
    - goal: generate aligned BAM (BWA-MEM)

stage_03: BAM processing
    - input: aligned BAM
    - goal: sorting, indexing (samtools)

stage_04: QC aligned reads
    - input: sorted BAM + BAI
    - goal: aligned-reads QC report (samtools)

stage_05: variant calling
    - input: sorted BAM, BAI
    - goal: generate VCF (GATK)

stage_06: VCF normalization and cleaning
    - input: raw VCF
    - goal: normalize VCF (GATK)

stage_07: Annotation (No Filtering)
    - input: normalized VCF
    - goal: annotate variants (ANNOVAR or equivalent)

stage_8: Global Filtering and Partitioning into Dual Tracks
    - input: annotated variant table
    - goal: generate filtered variant table
    - goal: generate coding-track table
    - goal: generate non-coding-track table

stage_09: Intepretation (Track A: Coding)
    - input: coding-track table
    - goal: make interpreted coding table

stage_10: Intepretation (Track A: Non-Coding)
    - input: non-coding-track table
    - goal: make interpreted non-coding table

stage_11: Variant Prioritization
    - input: interpreted coding table
    - input: interpreted non-coding table
    - goal: flag MitoCarta / epilepsy genes
    - goal: generate prioritized variant table

stage_12: Validation Preparation for Manual IGV Review
    - input: prioritized variant table
    - input: upstream BAM/VCF-derived context from earlier stages
    - goal: generate validation notes
    - goal: generate IGV review candidate list

stage_13: Generate Summary Reports
    - input: all outputs

---

# End of Design Document
