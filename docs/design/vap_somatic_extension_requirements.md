# VAP Somatic Extension Requirements

## Document Status

- **Purpose:** Define the architectural, analytical, and preservation requirements for a future somatic-mutation-enabled VAP
- **Scope:** Tumor–normal and tumor-only sequencing branches integrated with the existing germline VAP architecture
- **Status:** Design requirements
- **Target location:** `docs/design/vap_somatic_extension_requirements.md`

## Purpose

The Variant Annotation Pipeline (VAP) currently implements a germline-oriented workflow. A future somatic extension must add tumor-aware mutation calling and annotation without destabilizing the existing germline branch.

The governing model is a dual-branch patient architecture:

```text
patient
├── germline specimen(s)
│   └── germline VAP branch
└── tumor specimen(s) + matched normal specimen
    └── somatic VAP branch
```

This architecture must support patients who have both:

- a rare or inherited constitutional disorder; and
- an acquired cancer state.

The two branches must remain analytically distinct while preserving a shared patient identity and enabling downstream integration in VDB and RDGP-like reasoning systems.

---

# Core Architectural Principle

A somatic branch is not a germline branch with different filters.

Somatic evidence is inherently comparative and specimen-relative.

The fundamental somatic observation is not:

```text
variant in tumor
```

It is:

```text
variant observed in tumor
relative to matched normal
under a defined purity, depth, copy-number,
contamination, caller, and filtering context
```

Therefore, the tumor–normal relationship must be preserved as first-class evidence.

---

# Branching Model

## Germline branch

The germline branch should continue to preserve:

- constitutional genotype observations;
- Mendelian inheritance context;
- zygosity;
- germline population frequency;
- transcript and consequence annotation;
- clinical significance;
- phenotype-gene interpretation;
- germline provenance and uncertainty.

## Somatic branch

The somatic branch must preserve:

- tumor-specific SNV and indel evidence;
- matched-normal comparison;
- tumor and normal allele depths;
- variant allele fraction;
- purity and contamination context;
- copy-number and LOH state;
- clonality or subclonality;
- somatic filtering and confidence;
- cancer-specific annotation;
- caller and model provenance;
- benchmark truth status when available.

## Patient-level linkage

Both branches must reconnect through a stable patient identity:

```text
patient_id
├── germline_analysis_id
└── somatic_analysis_id
```

A matched normal may participate in both branches:

```text
matched normal
├── germline interpretation substrate
└── somatic comparator substrate
```

Its dual role must be explicit rather than inferred.

---

# Required Identity Model

A future VAP somatic extension should preserve at least:

```text
patient_id
specimen_id
specimen_role
tumor_normal_pair_id
collection_timepoint
anatomic_site
tumor_type
normal_tissue_source
library_id
run_accession
analysis_id
branch_type
```

Recommended `specimen_role` values include:

```text
germline_reference
tumor_primary
tumor_metastatic
tumor_recurrence
matched_normal_blood
matched_normal_tissue
tumor_only
technical_control
reference_material
```

Recommended `branch_type` values:

```text
germline
somatic_tumor_normal
somatic_tumor_only
```

---

# Somatic Calling Requirements

## Tumor–normal mode

Tumor–normal mode should be the preferred analytical path.

The caller must evaluate evidence jointly across:

- tumor reads;
- matched-normal reads;
- base quality;
- mapping quality;
- strand orientation;
- local sequence context;
- contamination;
- tumor purity;
- copy-number state.

The architecture should support caller-specific adapters while preserving a caller-independent internal evidence model.

## Tumor-only mode

Tumor-only mode may be supported, but it must carry an explicit uncertainty state.

Tumor-only analysis should preserve:

- population frequency filters;
- panel-of-normals evidence;
- germline-likelihood estimates;
- contamination estimates;
- classification uncertainty;
- inability to definitively distinguish somatic from rare germline variation.

Tumor-only calls must never be represented as equivalent in confidence to matched tumor–normal calls.

## Multi-caller support

A future VAP should permit multiple somatic callers without forcing a single implementation into the core architecture.

The caller interface should preserve:

```text
caller_name
caller_version
calling_mode
caller_parameters
reference_bundle
panel_of_normals
germline_resource
filter_status
filter_reason
raw_call_identity
```

Consensus calling may be added later, but individual caller evidence must remain reconstructable.

---

# Required Somatic Observation Model

A canonical somatic observation should preserve at least:

```text
somatic_observation_id
patient_id
tumor_specimen_id
normal_specimen_id
tumor_normal_pair_id
chromosome
position
reference_allele
alternate_allele
variant_type
reference_assembly
tumor_depth
normal_depth
tumor_ref_count
tumor_alt_count
normal_ref_count
normal_alt_count
tumor_vaf
normal_vaf
tumor_genotype
normal_genotype
caller_name
caller_version
filter_status
filter_reason
quality_metrics
purity_estimate
contamination_estimate
copy_number_state
loss_of_heterozygosity_status
clonality_status
benchmark_truth_status
annotation_status
provenance
epistemic_status
```

Somatic observations should remain immutable evidence records.

Downstream candidate tiers, driver labels, and treatment relevance should be projections.

---

# Annotation Requirements

The somatic branch must support cancer-aware annotation beyond standard germline consequence annotation.

Required annotation domains include:

- coding consequence;
- splice consequence;
- regulatory and noncoding context;
- cancer census membership;
- known oncogene or tumor-suppressor role;
- hotspot status;
- recurrence in cancer cohorts;
- therapeutic evidence;
- resistance associations;
- diagnostic or prognostic relevance;
- tissue-specific cancer context;
- somatic clinical significance;
- germline predisposition overlap;
- transcript selection policy;
- structural and copy-number context.

Annotation sources must remain versioned and provenance-preserved.

No annotation source should overwrite the original call evidence.

---

# Germline–Somatic Interaction Requirements

The architecture must support cases in which the same gene or locus participates in both branches.

Examples include:

- germline cancer-predisposition variants;
- somatic second hits;
- loss of heterozygosity;
- biallelic inactivation;
- constitutional mosaicism;
- therapy-related secondary malignancy;
- rare-disease genes with acquired tumor relevance.

The system should support relationships such as:

```text
germline_variant
    predisposes_to
tumor_state
```

```text
germline_variant
    paired_with
somatic_second_hit
```

```text
matched_normal_genotype
    compared_against
tumor_genotype
```

These relationships should be projected downstream and should not be embedded as irreversible biological conclusions inside the raw observation record.

---

# Copy-Number and Structural Context

A somatic extension limited to SNVs and small indels would be incomplete.

The architecture should eventually support:

- copy-number gains and losses;
- focal amplifications;
- homozygous deletions;
- loss of heterozygosity;
- structural variants;
- gene fusions;
- chromothripsis-like events;
- complex rearrangements.

These event classes may be implemented incrementally, but the identity and preservation model should anticipate them from the beginning.

A copy-number state should be linkable to small-variant evidence because VAF interpretation depends on local ploidy.

---

# Purity, Contamination, and Clonality

Somatic evidence quality depends on specimen composition.

The branch should preserve:

```text
tumor_purity_estimate
normal_contamination_estimate
tumor_contamination_estimate
ploidy_estimate
local_copy_number
cellular_prevalence
clonality_status
```

Recommended `clonality_status` values:

```text
clonal
subclonal
indeterminate
not_assessed
```

These values must retain method provenance.

---

# Filtering and Rejected Evidence

Rejected calls are scientifically informative and should not disappear.

The branch should preserve:

- raw candidate calls;
- caller filter status;
- filter reasons;
- orientation-bias evidence;
- panel-of-normals support;
- germline-likelihood evidence;
- low-depth or low-VAF status;
- contamination-related rejection;
- mapping or sequence-context artifacts.

A future VAP should distinguish:

```text
not_detected
detected_and_filtered
detected_and_retained
retained_with_uncertainty
```

These states are not interchangeable.

---

# Benchmarking Requirements

Before patient-derived demonstration, the somatic branch should be evaluated against a recognized tumor–normal reference system.

Preferred initial benchmark:

```text
HCC1395 tumor
HCC1395BL matched normal
PRJNA489865 / SRP162370
```

Benchmarking should measure:

- precision;
- recall;
- F1 score;
- false-positive rate;
- false-negative rate;
- SNV performance;
- indel performance;
- VAF-stratified performance;
- depth-stratified performance;
- purity-stratified performance;
- reproducibility across runs and platforms.

Truth-set membership must be represented as evidence, not as an overwrite of the observed call.

---

# Validation Requirements

The somatic branch should use the same layered validation philosophy as VAP:

## Layer 1 — Synthetic unit validation

Test:

- tumor–normal identity;
- VAF calculations;
- filtering states;
- purity and contamination fields;
- copy-number linkage;
- caller adapter behavior;
- serialization and round-trip integrity.

## Layer 2 — Repository-local benchmark validation

Use small local fixtures and reduced benchmark slices.

## Layer 3 — Full benchmark execution

Run public reference datasets on MARK or sys76.

Validation must confirm:

- deterministic execution;
- no unexplained evidence loss;
- stable caller provenance;
- reconstructable tumor–normal relationships;
- faithful TEP-VAP emission;
- benchmark metric reproducibility.

---

# TEP-VAP Requirements

Somatic TEP-VAP emission should preserve:

```text
patient identity
tumor and normal specimen identities
pairing relationship
raw and filtered somatic observations
caller provenance
annotation provenance
copy-number and purity context
validation outputs
benchmark metadata
lineage manifest
entity inventory
```

Somatic TEP-VAPs should not flatten tumor and normal observations into a single undifferentiated table.

The transport object should preserve the comparison structure explicitly.

---

# VDB Integration Requirements

VDB should ingest germline and somatic evidence as distinct assertion families.

Suggested distinction:

```text
germline_variant_observation
somatic_variant_observation
tumor_normal_comparison
copy_number_observation
loss_of_heterozygosity_observation
structural_variant_observation
```

Patient-level convergence may later be projected across branches, but the producer-side evidence must remain distinct and traceable.

---

# Scientific Boundaries

A future VAP somatic branch may support:

- analytical benchmarking;
- research-grade somatic calling;
- evidence preservation;
- candidate prioritization;
- oncology case-study demonstration.

It should not be represented as:

- a validated clinical diagnostic assay;
- a treatment recommendation engine;
- a substitute for pathology review;
- a replacement for orthogonal validation;
- a clinical tumor board.

Clinical claims require assay validation, regulatory governance, laboratory procedures, and expert interpretation beyond the scope of this design.

---

# Recommended Implementation Sequence

```text
Phase 1
Identity, specimen-role, and tumor–normal pairing model

Phase 2
Somatic caller interface and immutable observation record

Phase 3
SNV and small-indel benchmark support

Phase 4
Cancer-aware annotation and uncertainty model

Phase 5
Copy-number and LOH integration

Phase 6
Structural variation and fusion support

Phase 7
Germline–somatic patient-level convergence

Phase 8
Somatic TEP-VAP and VDB ingestion
```

---

# Final Requirement

The somatic extension should preserve this invariant:

> Germline and somatic analyses may share a patient, a specimen, a gene, or a locus, but they must never lose their distinct biological meaning, analytical provenance, or epistemic status.

The correct architecture is therefore:

```text
shared patient identity
        ↓
branch-specific evidence generation
        ↓
branch-specific preservation
        ↓
downstream convergence by explicit projection
```
