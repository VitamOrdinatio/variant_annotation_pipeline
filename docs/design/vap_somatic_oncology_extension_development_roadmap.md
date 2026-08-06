

# VAP Somatic Oncology Extension Development Roadmap

> The following documents collectively define the scientific rationale, public benchmark substrates, architectural requirements, and long-term capability roadmap for extending VAP from germline rare-disease analysis into somatic oncology while preserving the pipeline's core evidence-preservation doctrine.

## Related Somatic Oncology Design Documents

1. [Public Somatic WES / WGS dataset selection strategy](./public_somatic_wes_wgs_dataset_selection_strategy.md)
2. [VAP Cancer Proof Substrate *(candidate public benchmark datasets and proof-of-capability substrates)*](./vap_cancer_proof_substrate.md)
3. [VAP Somatic Extension requirements](./vap_somatic_extension_requirements.md)
4. [VAP Somatic Oncology Extension Development Roadmap](./vap_somatic_oncology_extension_development_roadmap.md)

## Related Germline Experimental Design Documents

1. [WES Epilepsy Experimental Design](./wes_epilepsy_experimental_design.md)
2. [WGS Epilepsy Experimental Design](./wgs_epilepsy_experimental_design.md)
3. [WES / WGS Comparative Experimental Design](./wes_wgs_comparative_experimental_design.md)


## Document Status

- **Purpose:** Phased roadmap for extending VAP from germline analysis into somatic oncology
- **Target location:** `docs/plans/vap_somatic_oncology_extension_development_plan.md`
- **Status:** Forward-looking development plan

## Executive Summary

VAP already provides most of the general infrastructure needed for a somatic branch:

- deterministic staged execution;
- FASTQ ingestion;
- alignment and BAM processing;
- normalized small-variant substrates;
- annotation infrastructure;
- stable run identities;
- provenance capture;
- telemetry;
- validation reports;
- semantic preservation;
- entity inventories;
- lineage manifests;
- TEP-VAP emission;
- VDB interoperability.

The extension should therefore be treated as:

```text
existing VAP infrastructure
        +
tumor–normal comparative evidence model
        +
somatic calling and annotation semantics
```

Recommended first major target:

> A benchmark-aware matched tumor–normal somatic SNV/indel branch with VAF, filtering-state preservation, caller provenance, and somatic TEP-VAP emission.

Estimated effort:

```text
Prototype:
    1–2 weeks

Credible somatic SNV/indel MVP:
    4–8 weeks

Purity/ploidy/CNV/LOH-aware branch:
    2–3 months

Broad oncology platform with SV, fusion,
tumor-only, and longitudinal support:
    4–6+ months
```

## Scientific Architecture

```text
patient
├── germline branch
└── somatic branch
```

The germline branch preserves constitutional variation.

The somatic branch preserves tumor-specific evidence relative to matched normal.

Both branches may share patient identity, specimens, genes, and loci, but must retain distinct biological meaning, analytical provenance, uncertainty, and epistemic status.

A somatic observation is not simply:

```text
variant detected in tumor
```

It is:

```text
variant detected in tumor
relative to matched normal
under defined depth, VAF, purity, ploidy,
copy-number, contamination, caller,
and filtering context
```

The tumor–normal relationship is part of the observation itself.

## Initial Scope

The first somatic-capable release should support:

- paired tumor–normal intake;
- stable patient and specimen identity;
- somatic SNV and small-indel calling;
- raw and filtered call preservation;
- tumor and normal depth;
- tumor and normal allele counts;
- tumor and normal VAF;
- caller-specific filter reasons;
- normalized variant identity;
- basic consequence annotation;
- cancer-aware annotation foundations;
- deterministic validation;
- benchmark truth comparison;
- somatic TEP-VAP emission;
- future VDB ingestion.

Deferred capabilities:

- structural variants;
- gene fusions;
- tumor-only calling;
- mature clonality analysis;
- mutational signatures;
- microsatellite instability;
- tumor mutational burden;
- homologous recombination deficiency;
- circulating tumor DNA;
- minimal residual disease;
- longitudinal tumor evolution;
- primary–metastatic comparison;
- neoantigen analysis;
- clinical report generation.

## Recommended Benchmark Substrate

Primary technical benchmark:

```text
PRJNA489865 / SRP162370
HCC1395 tumor
HCC1395BL matched normal
```

This substrate provides public matched tumor–normal WGS/WES, community benchmark truth, replicate conditions, and opportunities for depth- and purity-stratified validation.

After benchmark validation, a run-level-audited patient WES pair from `PRJNA713359` is the preferred patient-derived demonstration.

## Phase S0 — Scientific and Architectural Design

**Estimated effort:** 3–7 focused days

Lock:

- tumor–normal identity model;
- specimen-role model;
- caller-independent observation model;
- branch-routing model;
- benchmark strategy;
- filtering-state model;
- provenance model;
- somatic TEP-VAP concept;
- preliminary VDB assertion-family mapping.

Completion condition:

> A somatic observation can be described independently of any one caller’s VCF vocabulary.

## Phase S1 — Matched Tumor–Normal Prototype

**Estimated cumulative effort:** 1–2 weeks

Scope:

- one somatic caller;
- one matched pair;
- SNVs and small indels;
- reduced region or limited benchmark slice;
- basic annotation;
- VAF;
- raw and filtered state preservation.

Required identity:

```text
patient_id
tumor_specimen_id
normal_specimen_id
tumor_normal_pair_id
specimen_role
run_accession
library_id
```

Required caller provenance:

```text
caller_name
caller_version
caller_parameters
calling_mode
panel_of_normals
germline_resource
filter_status
filter_reason
```

Required observation fields:

```text
chromosome
position
reference_allele
alternate_allele
tumor_depth
normal_depth
tumor_ref_count
tumor_alt_count
normal_ref_count
normal_alt_count
tumor_vaf
normal_vaf
```

Validation:

- synthetic tumor–normal fixtures;
- tumor/normal reversal tests;
- sample-name mismatch tests;
- VAF tests;
- filter-state tests;
- deterministic reruns.

## Phase S2 — Benchmark-Aware Somatic MVP

**Estimated cumulative effort:** 4–8 weeks

Scope:

- full HCC1395/HCC1395BL execution;
- truth-set comparison;
- deterministic reruns;
- complete provenance;
- caller-independent schema;
- preliminary somatic TEP-VAP;
- local and MARK validation.

Measure:

- precision;
- recall;
- F1;
- false positives;
- false negatives;
- SNV performance;
- indel performance;
- VAF-stratified performance;
- depth-stratified performance;
- confidence-region performance.

Preserve filtering states:

```text
not_detected
detected_and_retained
detected_and_filtered
retained_with_uncertainty
```

Completion condition:

> VAP can reproducibly process a complete benchmark tumor–normal pair and report interpretable somatic SNV/indel performance.

## Phase S3 — Cancer-Aware Annotation

**Estimated cumulative effort:** 6–10 weeks

Add structured support for:

- cancer hotspot status;
- oncogene role;
- tumor-suppressor role;
- recurrence in cancer cohorts;
- diagnostic relevance;
- prognostic relevance;
- therapy sensitivity;
- therapy resistance;
- cancer-type specificity;
- biomarker evidence;
- somatic clinical significance;
- germline predisposition overlap.

Candidate resources include COSMIC, Cancer Gene Census, CIViC, OncoKB, ClinGen somatic resources, and Cancer Genome Interpreter.

Licensing, redistribution, versioning, and provenance must be reviewed before integration.

Cancer-aware annotation must remain additive and must never overwrite original call evidence.

## Phase S4 — Purity, Ploidy, CNV, and LOH

**Estimated cumulative effort:** 2–3 months

Preserve:

```text
tumor_purity_estimate
contamination_estimate
ploidy_estimate
local_total_copy_number
major_allele_copy_number
minor_allele_copy_number
loh_status
copy_number_caller
purity_method
confidence
```

Support:

- gain;
- amplification;
- heterozygous deletion;
- homozygous deletion;
- arm-level alteration;
- whole-chromosome alteration;
- copy-neutral LOH;
- deletion-associated LOH.

Enable explicit germline–somatic relationships without collapsing the source observations.

## Phase S5 — Somatic TEP-VAP and VDB Integration

**Estimated cumulative effort:** 2–3 months

Proposed TEP entity families:

```text
patient_context
specimen_context
tumor_normal_pair
somatic_small_variant_observation
somatic_filtering_context
somatic_annotation
copy_number_observation
loh_observation
benchmark_context
execution_context
```

Potential VDB assertion families:

```text
somatic_variant_observation
tumor_normal_comparison
copy_number_observation
loss_of_heterozygosity_observation
benchmark_concordance_assertion
```

VDB should preserve and relate the evidence, not reinterpret it.

## Phase S6 — Structural Variation and Fusion Support

**Estimated cumulative effort:** 3–5 months

Support structural events such as deletions, duplications, inversions, translocations, insertions, and complex rearrangements.

Preserve breakpoints, orientation, event type, split-read support, paired-read support, copy-number context, caller, and confidence.

Fusion support should preserve:

```text
gene_5_prime
gene_3_prime
genomic_breakpoint
transcript_breakpoint
reading_frame
DNA_evidence
RNA_evidence
fusion_caller
confidence
clinical_context
```

Potential future convergence:

```text
VAP DNA evidence
        +
RSP RNA evidence
        ↓
VDB convergence surface
```

## Phase S7 — Extended Oncology Capabilities

**Estimated cumulative effort:** 4–6+ months

Possible later modules:

- tumor-only calling;
- longitudinal tumor analysis;
- primary versus metastasis comparison;
- clonality and subclonality;
- mutational signatures;
- microsatellite instability;
- tumor mutational burden;
- homologous recombination deficiency;
- circulating tumor DNA;
- minimal residual disease;
- therapy-response evolution;
- FFPE artifact handling;
- clinical evidence classification.

Each should be treated as a distinct scientific module rather than a generic oncology mode.

## Validation Strategy

### Layer 1 — Synthetic unit validation

Test identity, pairing, VAF, filter states, provenance serialization, caller adapters, and round-trip preservation.

### Layer 2 — Repository-local integration validation

Use reduced benchmark slices, truth-set fixtures, local examples, deterministic reruns, and TEP round-trip checks.

### Layer 3 — Full production validation

Use MARK or sys76 for complete HCC1395/HCC1395BL execution, benchmark metrics, cross-node reproducibility, storage characterization, telemetry, and TEP-VAP certification.

## Timeline

| Milestone | Estimated Effort |
|---|---:|
| Scientific and architectural design | 3–7 days |
| Matched tumor–normal prototype | 1–2 weeks |
| Benchmark-aware SNV/indel MVP | 4–8 weeks |
| Cancer-aware annotation | 6–10 weeks cumulative |
| Purity/ploidy/CNV/LOH branch | 2–3 months cumulative |
| SV and fusion support | 3–5 months cumulative |
| Broad oncology platform | 4–6+ months cumulative |

These estimates assume focused development by one experienced contributor using the existing VAP infrastructure.

## Principal Schedule Risks

### Caller resource complexity

Somatic callers may require a panel of normals, germline resources, contamination estimation, orientation-bias models, interval resources, and strict sample-name matching.

### Benchmark compatibility

Truth sets, confidence regions, normalized representations, and caller outputs must be aligned correctly.

### Purity and CNV coupling

VAF, purity, ploidy, copy number, and LOH are interdependent and should not be implemented as unrelated columns.

### Schema pressure

A somatic observation is a comparative evidence object. Poor early schema decisions would create expensive downstream rework.

### Compute and storage

Tumor–normal processing doubles primary input and alignment storage before caller intermediates, CNV outputs, benchmarks, and repeated validation runs are considered.

## Recommended Initial Release Claim

> VAP supports research-grade matched tumor–normal somatic SNV and small-indel analysis with deterministic execution, VAF and filtering-state preservation, benchmark-aware validation, provenance-complete evidence emission, and future-compatible interfaces for purity, copy number, LOH, structural variation, and VDB integration.

The initial release should not claim:

- comprehensive oncology support;
- clinical diagnostic validation;
- treatment recommendation;
- complete structural-variant support;
- tumor-only equivalence;
- production clinical reporting.

## Final Recommendation

The best near-term target is:

```text
benchmarked matched tumor–normal
somatic SNV/indel branch
```

with stable pairing identity, caller-independent schema, VAF, raw and filtered evidence preservation, truth-set comparison, complete provenance, and somatic TEP-VAP design.

A credible somatic MVP should be budgeted at:

```text
4–8 focused weeks
```

A mature branch incorporating purity, ploidy, copy number, LOH, cancer-aware annotation, and VDB integration is more realistically:

```text
2–3 months
```

The governing development principle is:

> Build the comparative evidence model first. Add oncology breadth only after the tumor–normal substrate, provenance, and preservation semantics are stable.
