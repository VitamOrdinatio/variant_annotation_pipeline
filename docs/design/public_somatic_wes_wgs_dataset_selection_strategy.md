# Public Somatic WES/WGS Dataset Selection Strategy

## Document Status

- **Purpose:** Define a reproducible method for identifying public cancer sequencing substrates suitable for future VAP development
- **Scope:** Human somatic WES and WGS datasets
- **Status:** Dataset-selection governance
- **Target location:** `docs/design/public_somatic_wes_wgs_dataset_selection_strategy.md`

## Purpose

This document codifies the strategy used to identify, verify, rank, and reject public cancer WES and WGS datasets for future use by a somatic-mutation-enabled Variant Annotation Pipeline (VAP).

The goal is not merely to find cancer BioProjects.

The goal is to identify datasets that are:

- scientifically relevant;
- publicly retrievable;
- technically interpretable;
- correctly paired;
- publication-linked;
- execution-ready;
- suitable for reproducible portfolio and benchmark work.

---

# Governing Principle

Dataset selection must proceed through four distinct gates:

```text
scientific attractiveness
        ↓
public accessibility
        ↓
run-level interpretability
        ↓
execution readiness
```

A project may pass one gate and fail the next.

For example:

- a strong publication may have no public raw data;
- a public BioProject may contain mixed WES and RNA-seq runs;
- paired samples may exist but lack clear patient linkage;
- raw reads may be controlled access;
- tumor and normal labels may be ambiguous;
- files may be technically public but impractical to execute.

No project should be called executable until all four gates are passed.

---

# Scope and Terminology

## Publicly accessible

In this strategy, publicly accessible means:

- raw sequence reads can be retrieved without controlled-access authorization;
- no dbGaP, EGA, or institutional application is required;
- accession-level metadata are visible;
- the files can be downloaded through SRA, ENA, or an equivalent public archive.

This does not imply unrestricted legal public-domain status.

## Preferred data types

Priority order:

```text
1. Paired-end WES tumor–normal
2. Paired-end WGS tumor–normal
3. Tumor-only WES or WGS with strong metadata
4. Cell-line tumor–normal benchmark systems
5. Multimodal WES/WGS plus RNA-seq projects
```

The exact order may change by experimental aim.

---

# Hard Inclusion Criteria

A preferred substrate should meet all of the following:

1. `Homo sapiens`.
2. Cancer or tumor state is explicit.
3. WES or WGS is explicit.
4. Raw reads are public.
5. Paired-end layout is verified.
6. Specimen roles are identifiable.
7. Publication or benchmark documentation is available.
8. Run accessions can be mapped to BioSamples.
9. Reference assembly and sequencing design can be determined.
10. Data volume is feasible for the intended compute node.

For tumor–normal studies, also require:

11. Stable tumor–normal pair mapping.
12. Shared patient identity.
13. Normal tissue source is known or recoverable.
14. Collection timepoint and tumor site are preserved when available.

---

# Preferred Scientific Features

These are not always mandatory, but they increase value:

- matched blood normal;
- primary tumor rather than cell line;
- multiple tumor regions;
- serial or recurrent specimens;
- orthogonal validation;
- published driver or hotspot findings;
- known benchmark truth set;
- tumor purity estimates;
- copy-number data;
- pathology metadata;
- clinical subtype;
- treatment or outcome context;
- multiple sequencing depths;
- cross-center replicates.

---

# Search Procedure

## Step 1 — Define the experimental aim

Before searching, decide whether the intended substrate is:

```text
technical benchmark
patient-derived case study
cohort demonstration
multimodal integration study
```

The search criteria differ by aim.

A benchmark may prioritize truth sets and replicates.

A patient case study may prioritize primary tissue and publication linkage.

A cohort study may prioritize sample count and consistent metadata.

---

## Step 2 — Search primary archives

Search:

- NCBI BioProject;
- NCBI SRA;
- ENA Browser;
- GEO when sequencing studies are deposited through GEO;
- publication supplementary material;
- benchmark consortium pages.

Use combinations of:

```text
cancer
tumor
whole exome
whole genome
paired
matched normal
somatic
Homo sapiens
```

Do not rely on BioProject title alone.

---

## Step 3 — Verify publication linkage

Require direct evidence that the publication and sequence deposit correspond.

Acceptable evidence includes:

- publication Data Availability section;
- BioProject accession in Methods;
- SRA study accession in supplementary material;
- archive page linking the publication;
- consortium documentation tying truth sets to runs.

A citation to an unrelated umbrella project is insufficient.

---

## Step 4 — Verify public raw-read access

Confirm:

- SRA or ENA run accessions exist;
- FASTQ retrieval is possible;
- files are not controlled access;
- data are not BAM-only unless BAM ingestion is explicitly supported;
- data have not been withdrawn;
- the BioProject is not merely registered without linked datasets.

A BioProject stating:

```text
No public data is linked to this project
```

must be rejected unless another verified public accession is found.

---

## Step 5 — Perform run-level audit

For every candidate run, record:

```text
BioProject
SRA Study
Experiment
Run
BioSample
patient_id
specimen_id
specimen_role
tumor_normal_pair_id
sequencing_strategy
library_layout
platform
read_length
read_count
base_count
file_size
reference_build
capture_kit
publication
```

Run-level audit is mandatory because project-level descriptions often hide mixed assays and ambiguous sample roles.

---

## Step 6 — Confirm tumor–normal mapping

Do not infer pairing from accession proximity.

Pairing must be supported by:

- patient identifier;
- explicit matched-normal field;
- sample title;
- BioSample attributes;
- publication sample table;
- supplementary metadata.

Required relationship:

```text
tumor specimen
    belongs to patient X

normal specimen
    belongs to patient X

pair identifier
    links both explicitly
```

If pairing cannot be proven, the dataset cannot be used for matched somatic calling.

---

## Step 7 — Check assay purity

Many cancer projects mix:

- WES;
- WGS;
- RNA-seq;
- targeted panels;
- ChIP-seq;
- single-cell sequencing;
- methylation data.

Each run must be classified individually.

A project containing WES does not mean every run is WES.

---

## Step 8 — Assess technical compatibility

Verify:

- paired-end layout;
- sequencing platform;
- read length;
- genome build;
- capture kit for WES;
- expected coverage;
- lane structure;
- duplicate or replicate status;
- FFPE status;
- UMI usage;
- tumor purity;
- contamination;
- practical storage requirement.

Compatibility review should precede download.

---

## Step 9 — Estimate compute and storage cost

For each candidate, estimate:

- compressed archive size;
- decompressed FASTQ size;
- alignment footprint;
- temporary-sort space;
- final BAM/CRAM size;
- VCF and annotation size;
- telemetry and TEP-VAP size.

WGS tumor–normal pairs may require several hundred gigabytes to over a terabyte of working space depending on implementation.

---

## Step 10 — Identify a benchmark surface

A preferred dataset should provide at least one external comparison target:

- community truth set;
- validated somatic variants;
- known driver alteration;
- orthogonal validation;
- publication-defined candidate;
- reported mutation spectrum;
- expected tumor subtype markers.

Publication concordance is not equivalent to a truth set.

The distinction must remain explicit.

---

# Candidate Classification

## Class A — Benchmark-ready

Criteria:

- public raw reads;
- clear tumor–normal identity;
- verified pairing;
- publication or consortium documentation;
- truth set or benchmark target;
- execution metadata complete.

Example:

```text
PRJNA489865 / SRP162370
HCC1395 / HCC1395BL
```

## Class B — Patient-ready

Criteria:

- public raw reads;
- primary patient tumor;
- matched normal;
- clear pairing;
- publication linkage;
- no truth set required.

## Class C — Audit-required

Criteria:

- scientifically attractive;
- likely public;
- publication-linked;
- one or more run-level uncertainties remain.

Typical unresolved issues:

- tumor/normal mapping;
- mixed assay types;
- missing normal;
- unclear patient identifiers;
- uncertain FASTQ access.

## Class D — Non-actionable

Criteria:

- no linked public data;
- controlled access only;
- withdrawn accessions;
- inaccessible raw reads;
- pairing impossible to establish;
- metadata insufficient for responsible interpretation.

---

# Ranking Framework

Each candidate may be scored across:

```text
public_access
tumor_normal_clarity
publication_linkage
benchmark_strength
metadata_quality
assay_purity
clinical_relevance
compute_feasibility
portfolio_value
future_vdb_value
```

Suggested ordinal scale:

```text
0 = absent
1 = weak
2 = partial
3 = strong
```

A high total score does not override a hard failure in public access or pairing.

Hard-fail conditions should be applied first.

---

# Negative-Finding Preservation

Rejected projects should remain documented.

For each rejected candidate, record:

```text
accession
reason_rejected
date_checked
source_checked
whether_recheck_is_warranted
```

This prevents repeated investigation of the same dead end.

Example:

```text
PRJNA278883
reason: no public data linked
status: reject
```

Negative findings are part of the search provenance.

---

# Search Provenance

Each dataset review should preserve:

```text
search_date
search_queries
archives_checked
publication_checked
BioProject_checked
SRA_checked
ENA_checked
run_metadata_snapshot
reviewer
decision
decision_reason
```

Because archive metadata can change, decisions must be time-stamped.

---

# Recommended Search Order

## WES-first

WES should generally be searched first because it offers:

- lower storage cost;
- faster iteration;
- easier caller development;
- coding-focused benchmark surfaces;
- more practical tumor–normal experimentation.

Preferred WES progression:

```text
reference benchmark
        ↓
single patient tumor–normal pair
        ↓
small patient cohort
```

## WGS second

WGS should follow after SNV/indel somatic architecture is stable.

WGS adds:

- noncoding somatic mutations;
- structural variants;
- copy-number resolution;
- breakpoint analysis;
- more complete mutational signatures;
- substantially greater compute cost.

---

# Recommended Substrate Ladder

```text
Tier 1
PRJNA489865 / SRP162370
HCC1395 / HCC1395BL
technical benchmark

Tier 2
PRJNA713359
patient-derived inflammatory breast cancer WES
run-level pairing audit required

Tier 2
PRJNA606980
focused breast tumor / patient-derived model study
biological pairing audit required

Tier 3
PRJNA777362
acral melanoma WES + RNA-seq
multimodal audit required

Tier 3
GSE63420
cholangiocarcinoma paired tissue study
raw-read mapping audit required

Reject
PRJNA278883
no public linked data
```

This ladder should be revised only when new run-level evidence is obtained.

---

# Final Decision Rule

A dataset is execution-ready only when all of the following are true:

```text
public raw reads verified
+
assay type verified
+
paired-end layout verified
+
tumor/normal roles verified
+
patient pairing verified
+
publication linkage verified
+
compute feasibility verified
+
benchmark or comparison surface defined
```

The governing principle is:

> Select datasets by verified execution truth, not by attractive titles, publication prestige, or assumed BioProject completeness.

# Appendix A: Biological Substrate Readiness Checklist

| Check                           | Status |
| ------------------------------- | ------ |
| BioProject reachable            | ✓ or x |
| SRA runs present                | ✓ or x |
| FASTQs downloadable             | ✓ or x |
| Paired-end confirmed            | ✓ or x |
| Tumor/normal mapping verified   | ✓ or x |
| Patient pairing verified        | ✓ or x |
| WES only (no RNA contamination) | ✓ or x |
| Practical storage estimate      | ✓ or x |
| MARK execution feasible         | ✓ or x |
