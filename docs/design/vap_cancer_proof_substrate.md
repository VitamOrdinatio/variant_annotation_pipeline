# VAP Cancer Proof Substrate Strategy

## Document Status

- **Purpose:** Design guidance for a future somatic-mutation-enabled VAP
- **Scope:** Publicly accessible human cancer WES and WGS substrates
- **Status:** Candidate survey and execution-readiness framework
- **Last reviewed:** 2026-07-23

## Purpose

This document identifies publicly accessible cancer sequencing datasets that could support future development, benchmarking, and demonstration of a somatic-mutation-enabled Variant Annotation Pipeline (VAP).

The present VAP architecture is germline-oriented. The datasets below are therefore not proposed for immediate interpretation with the current pipeline. They are intended to establish a defensible future substrate strategy for:

- paired tumor–normal somatic SNV and small-indel calling;
- tumor-only versus matched-normal comparison;
- tumor purity and variant-allele-fraction sensitivity;
- copy-number and loss-of-heterozygosity analysis;
- structural-variant-aware WGS analysis;
- preservation of somatic evidence, provenance, and uncertainty;
- oncology-focused portfolio and case-study development.

In this document, **publicly accessible** means that raw sequence data are openly retrievable without controlled-access authorization. It does not imply that the data are free of all reuse conditions or are legally in the public domain.

---

# Selection Requirements

A preferred VAP cancer proof substrate should satisfy as many of the following as possible:

1. Human tumor-derived DNA.
2. Publicly retrievable raw reads.
3. Illumina paired-end WES or WGS.
4. Clearly identified tumor and matched-normal specimens.
5. Stable patient or specimen linkage across runs.
6. Peer-reviewed publication tied directly to the sequencing deposit.
7. Published somatic findings or a community truth set.
8. Sufficient metadata to preserve tissue state, tumor status, preparation, platform, and provenance.
9. Practical run size for MARK or sys76.
10. No requirement for dbGaP, EGA, or other controlled-access approval.

A BioProject registration alone is not sufficient. Execution readiness requires verification at the **run level**.

---

# Recommended Substrate Ladder

## Tier 1 — Primary Technical Benchmark

### PRJNA489865 / SRP162370  
### HCC1395 and HCC1395BL matched tumor–normal reference system

**Cancer type:** Breast ductal carcinoma / triple-negative breast cancer reference model  
**Data types:** WGS and WES across multiple platforms, centers, replicates, coverages, and mixture conditions  
**Tumor sample:** HCC1395  
**Matched normal:** HCC1395BL, a B-lymphocyte-derived line from the same donor  
**Public raw data:** Yes  
**Publication support:** Strong  
**Truth resource:** High-confidence somatic SNV and indel call set

This is the strongest available starting substrate for a future somatic-capable VAP.

The SEQC2 Somatic Mutation Working Group established HCC1395 and HCC1395BL as community reference materials for benchmarking cancer mutation detection. The consortium generated public WGS and WES data under `PRJNA489865` and developed a reference somatic call set supported by multiple sequencing centers, aligners, callers, and orthogonal evidence.

Published descriptions report a reference set containing approximately:

- 39,536 somatic SNVs;
- 2,020 somatic small indels.

The corpus also includes technically valuable perturbations such as:

- variable tumor purity;
- variable normal contamination;
- multiple sequencing depths;
- fresh and FFPE-like inputs;
- independent sequencing centers;
- multiple library and sequencing conditions.

### Why this should be first

This substrate provides something most patient studies cannot:

> A matched tumor–normal cancer genome with public raw reads and a community-derived somatic benchmark.

It would allow a future VAP implementation to measure:

- precision and recall against a recognized call set;
- sensitivity across variant allele fractions;
- reproducibility across centers and replicates;
- robustness to depth and purity;
- SNV versus indel performance;
- preservation of benchmark truth through downstream annotation and TEP emission.

### Limitations

HCC1395 is a reference cell-line system, not a fresh primary tumor cohort. It should be described as a **technical oncology benchmark**, not as a patient-cohort discovery study.

The normal line is EBV-transformed, and the tumor line has undergone cell-culture evolution. These properties must remain visible in provenance and should not be conflated with primary tissue biology.

### Recommended role

```text
Primary somatic caller validation substrate
```

### Execution-readiness status

```text
HIGH — recommended first cancer substrate after somatic architecture exists
```

---

## Tier 2 — Preferred Patient-Derived WES Demonstration

### PRJNA713359  
### Inflammatory breast cancer whole-exome sequencing

**Cancer type:** Inflammatory breast cancer  
**Data type:** WES  
**Publication:** Luo et al. (2021), *Whole-exome sequencing identifies somatic mutations and intratumor heterogeneity in inflammatory breast cancer*  
**Public raw-data statement:** Yes; the publication directs readers to `PRJNA713359`  
**Scientific strengths:** Patient tumors, somatic mutation analysis, intratumor heterogeneity, aggressive oncology phenotype

This is the most promising patient-derived WES candidate identified in the present review.

The associated peer-reviewed study used whole-exome sequencing to characterize somatic mutations and intratumor heterogeneity in inflammatory breast cancer. The article states that the generated sequencing data were deposited in SRA under `PRJNA713359`.

### Why it is attractive

- clinically important and aggressive cancer state;
- direct publication-to-BioProject linkage;
- WES is operationally lighter than WGS;
- study questions align with future somatic architecture;
- suitable for demonstrating tumor-specific evidence interpretation beyond a reference cell line.

### Required pre-execution audit

Before selection of any run, VAP must verify:

- whether matched normals are present for each selected tumor;
- whether raw FASTQ files are openly downloadable;
- exact tumor, normal, biopsy, and patient identifiers;
- whether multiple tumor regions or serial specimens exist;
- library layout and capture kit;
- sequencing depth and read length;
- reference assembly used in the publication;
- whether any files are RNA-seq rather than WES.

### Recommended role

```text
First patient-derived somatic WES case study
```

### Execution-readiness status

```text
MEDIUM-HIGH — publication-linked and promising, but run-level pairing must be audited
```

---

## Tier 2 — Compact Patient/Model WES Study

### PRJNA606980  
### Breast tumor and patient-derived cell-line sequencing

**Cancer type:** Breast cancer  
**Data type:** Publication-linked sequencing deposited in SRA  
**Publication:** Rashid et al. (2021), *Discovery of a novel potentially transforming somatic mutation in CSF2RB in a breast cancer patient*  
**Public raw-data statement:** Yes; the publication identifies `PRJNA606980`

This project is tied to a focused study of a breast cancer patient and a cell line established from the patient’s tumor. The study reported a potentially transforming somatic `CSF2RB` alteration.

### Scientific value

This is potentially useful as a compact, mechanistically interpretable proof substrate because it offers a publication-defined candidate alteration and a relationship between patient tumor material and a derived model.

### Limitations and audit requirements

It must not be assumed that the project contains a conventional matched blood-normal pair. Before use, the run metadata must establish:

- which sample represents primary tumor;
- which sample represents the derived cell line;
- whether a germline normal is available;
- whether all runs are WES;
- whether the study design permits tumor–normal somatic calling or only tumor/model comparison.

### Recommended role

```text
Focused candidate-recovery and tumor-to-model preservation study
```

### Execution-readiness status

```text
MEDIUM — public and publication-linked, but biological pairing requires careful audit
```

---

## Tier 3 — Multimodal Melanoma Candidate

### PRJNA777362  
### Acral melanoma WES and RNA-seq

**Cancer type:** Acral melanoma  
**Data types:** WES and RNA-seq  
**Public raw data:** Yes  
**NCBI project size:** 12 SRA experiments, 4 BioSamples, approximately 113 Gbases  
**Publication linkage:** Study-associated publication reports deposition under `PRJNA777362`

NCBI currently identifies this project as containing raw sequence reads for whole-exome and RNA sequencing of acral melanoma.

### Scientific value

Acral melanoma is a biologically distinctive melanoma subtype. A combined WES/RNA-seq project could eventually support:

- somatic coding-variant analysis;
- expression-aware interpretation;
- candidate driver contextualization;
- future VAP-to-RSP or VDB multimodal integration.

### Limitations

The project contains only four BioSamples and mixes WES with RNA-seq. The current metadata available from the BioProject summary do not establish a complete matched tumor–normal design.

### Required audit

- identify the WES-only experiments;
- determine whether any sample is matched normal;
- map all experiments to the four BioSamples;
- verify paired-end layout;
- confirm tumor tissue versus cell-line or nevus context;
- identify the exact publication corresponding to each sequence subset.

### Recommended role

```text
Exploratory multimodal melanoma substrate
```

### Execution-readiness status

```text
MEDIUM-LOW — public, but not yet established as a clean tumor–normal pair
```

---

## Tier 3 — Intrahepatic Cholangiocarcinoma Exome Series

### GSE63420  
### Paired tumor and adjacent non-tumor intrahepatic cholangiocarcinoma

**Cancer type:** Intrahepatic cholangiocarcinoma  
**Data types:** Whole-exome sequencing and RNA-seq  
**Study design:** Eight tumor/adjacent-normal pairs were reported; seven RNA pairs passed downstream quality review  
**Publication focus:** `FGFR2-PPHLN1` fusion and damaging `ARAF` mutations

This GEO series is scientifically attractive because it combines paired tumor and adjacent non-tumor tissues with exome and transcriptome analysis.

### Potential value

- matched primary human tissues;
- actionable fusion and driver-gene context;
- paired DNA/RNA design;
- direct relevance to precision oncology.

### Limitation

GEO series metadata and publication statements do not by themselves establish that all raw exome FASTQs remain openly and straightforwardly retrievable from SRA. The exome and RNA components must be disentangled at the accession level.

### Required audit

- enumerate linked SRA accessions;
- confirm which runs are WES;
- confirm paired-end layout;
- map tumor and adjacent-normal pairs;
- verify unrestricted FASTQ availability;
- inspect capture chemistry and reference build.

### Recommended role

```text
Future paired-tissue precision-oncology case study
```

### Execution-readiness status

```text
MEDIUM-LOW — strong scientific design, but raw-read access and run mapping require confirmation
```

---

# Rejected or Non-Actionable Candidates

## PRJNA278883 — Microdissected pancreatic cancer WES

The associated publication is scientifically compelling, but the current NCBI BioProject page states:

> No public data is linked to this project.

Accordingly, `PRJNA278883` is not an executable VAP substrate at present.

It should remain documented as a negative search result because the BioProject title and publication can misleadingly suggest open availability.

### Status

```text
REJECT — no linked public sequence dataset
```

---

## Controlled-access cancer cohorts

Many of the strongest patient tumor–normal studies are available only through:

- dbGaP;
- EGA;
- institutional data-access committees;
- TCGA/GDC controlled-access BAM or raw-read tiers.

These resources are scientifically valuable but do not meet the present requirement for an openly downloadable portfolio substrate. They should not be represented as public FASTQ datasets.

---

# Recommended Development Order

## Stage 1 — Architecture before execution

A future somatic-capable VAP should first define:

- tumor and matched-normal identities;
- somatic calling interface;
- caller provenance;
- reference and panel-of-normals policy;
- contamination and tumor-purity metadata;
- variant allele fraction;
- strand and orientation-bias evidence;
- copy-number state;
- loss of heterozygosity;
- clonality or subclonality representation;
- filtering status and reason codes;
- confidence and uncertainty;
- benchmark truth-set membership;
- preservation of rejected as well as accepted calls.

## Stage 2 — HCC1395/HCC1395BL benchmark

Use `PRJNA489865` to validate:

1. matched tumor–normal ingestion;
2. somatic SNV and indel calling;
3. benchmark precision and recall;
4. depth and purity sensitivity;
5. cross-run reproducibility;
6. somatic annotation;
7. TEP-VAP preservation.

## Stage 3 — Patient-derived WES

After benchmark certification, select one carefully audited pair from `PRJNA713359`.

This would answer a different question:

> Can the architecture that performs correctly on a reference system preserve and interpret evidence from a real patient tumor study?

## Stage 4 — Multimodal expansion

Consider `PRJNA777362` or `GSE63420` only after VAP has stable interfaces for:

- DNA and RNA evidence linkage;
- gene fusion observations;
- expression context;
- specimen-role provenance.

---

# Proposed Somatic Evidence Model

A future VAP somatic record should preserve at least:

```text
patient_id
specimen_id
specimen_role
tumor_normal_pair_id
tumor_site
normal_tissue_source
collection_timepoint
library_id
run_accession
reference_assembly
somatic_caller
somatic_caller_version
filter_status
filter_reason
chromosome
position
reference_allele
alternate_allele
tumor_depth
normal_depth
tumor_alt_count
normal_alt_count
tumor_vaf
normal_vaf
tumor_genotype
normal_genotype
copy_number_state
loss_of_heterozygosity_status
purity_estimate
contamination_estimate
clonality_status
clinical_annotation
benchmark_truth_status
provenance
epistemic_status
```

Somatic evidence should not be compressed into a germline-style genotype row. The tumor–normal relationship is part of the observation itself.

---

# Scientific Boundaries

A future cancer demonstration should distinguish among:

```text
technical benchmark
patient-derived case study
cohort analysis
clinical validation
```

These are not interchangeable.

HCC1395 can validate technical performance but cannot substitute for a patient cohort.

A single patient tumor–normal pair can demonstrate evidence preservation and candidate recovery but cannot establish population-level recurrence or clinical utility.

A publication-linked candidate is a concordance target, not an independent truth set.

---

# Final Recommendation

The substrate strategy should be locked as:

```text
Primary benchmark:
    PRJNA489865 / SRP162370
    HCC1395 tumor + HCC1395BL matched normal
    WGS/WES
    community somatic truth set

Primary patient WES candidate:
    PRJNA713359
    inflammatory breast cancer
    publication-linked
    run-level tumor–normal audit required

Secondary focused candidate:
    PRJNA606980
    breast tumor / patient-derived model
    publication-linked
    pairing audit required

Exploratory multimodal candidates:
    PRJNA777362
    GSE63420

Rejected:
    PRJNA278883
    no currently linked public data
```

For portfolio and job-search purposes, this is a stronger design than presenting an unverified list of cancer BioProjects. It shows that future oncology support will proceed through a disciplined sequence:

```text
community benchmark
        ↓
patient-derived matched WES
        ↓
multimodal oncology evidence
        ↓
VDB-preserved somatic reasoning surfaces
```

---

# References

1. Fang LT, et al. *Establishing community reference samples, data and call sets for benchmarking cancer mutation detection using whole-genome sequencing.* Nature Biotechnology. 2021.
2. Xiao W, et al. *Toward best practice in cancer mutation detection with whole-genome and whole-exome sequencing.* Nature Biotechnology. 2021.
3. Sahraeian SME, et al. *Achieving robust somatic mutation detection with deep learning models derived from reference data sets.* Genome Biology. 2022.
4. Xiao C, et al. *Personalized genome assembly for accurate cancer somatic mutation discovery using tumor-normal paired reference samples.* Genome Biology. 2022.
5. Luo R, et al. *Whole-exome sequencing identifies somatic mutations and intratumor heterogeneity in inflammatory breast cancer.* npj Breast Cancer. 2021.
6. Rashid M, et al. *Discovery of a novel potentially transforming somatic mutation in CSF2RB in a breast cancer patient.* Cancer Medicine. 2021.
7. NCBI BioProject `PRJNA489865`.
8. NCBI BioProject `PRJNA713359`.
9. NCBI BioProject `PRJNA606980`.
10. NCBI BioProject `PRJNA777362`.
11. NCBI GEO Series `GSE63420`.
