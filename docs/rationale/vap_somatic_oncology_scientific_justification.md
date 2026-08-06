# VAP Somatic Oncology Architecture Justification

Somatic Oncology Sequencing Concepts for Future VAP Development

## Purpose

This rationale document explains core somatic oncology sequencing concepts in the context of a future cancer-aware Variant Annotation Pipeline (VAP). It is intended for oncology sequencing integration within future VAP design.

The central architecture is:

```text
patient
├── germline branch
└── somatic branch
```

A patient may have both a constitutional genetic disorder and an acquired cancer state. The two branches share patient identity, but they answer different biological questions and must preserve distinct evidence.

---

# 1. Germline Versus Somatic Analysis

## Germline analysis

Germline analysis asks:

> Which variants are present in the patient’s constitutional genome?

These variants are usually present in most cells and may be inherited, de novo, benign, pathogenic, or associated with disease predisposition.

```text
patient specimen
      ↓
FASTQ
      ↓
alignment
      ↓
germline variant calling
      ↓
annotation
      ↓
interpretation
```

## Somatic analysis

Somatic oncology analysis asks:

> Which mutations are present in the tumor that are absent, or meaningfully different, in the patient’s constitutional genome?

```text
tumor specimen
      +
matched normal specimen
      ↓
joint comparison
      ↓
somatic mutation evidence
```

A somatic observation is not simply “variant detected in tumor.” It is:

```text
variant detected in tumor
relative to matched normal
under defined depth, purity, ploidy,
copy-number, contamination, and filtering conditions
```

---

# 2. Tumor–Normal Pairing

Tumor–normal pairing is the foundation of matched somatic analysis.

The tumor specimen may come from a primary tumor, metastasis, recurrence, biopsy, resection, bone marrow, circulating tumor DNA, or a tumor-derived cell line.

The matched normal ideally comes from the same patient and serves as the operational approximation of constitutional DNA. Common sources include blood, buccal cells, adjacent non-tumor tissue, or fibroblasts.

Suppose a tumor contains a `BRCA2` variant. Without matched normal data, it may be unclear whether it is inherited, de novo germline, acquired somatic, an artifact, or contamination.

A future VAP should preserve:

```text
patient_id
tumor_specimen_id
normal_specimen_id
tumor_normal_pair_id
specimen_role
collection_timepoint
tumor_site
normal_tissue_source
```

The matched normal may participate in both branches:

```text
matched normal
├── germline interpretation
└── somatic comparison
```

---

# 3. Variant Allele Fraction

Variant allele fraction, or VAF, is the proportion of reads supporting an alternate allele.

If a position has 100 reads and 25 support the alternate allele:

```text
VAF = 25 / 100 = 0.25 = 25%
```

In germline analysis, a heterozygous diploid variant often appears near 50% VAF. In cancer, a real mutation may appear at 5%, 10%, 20%, 35%, 50%, or higher depending on:

- tumor purity;
- clonality;
- copy number;
- local ploidy;
- contamination;
- sequencing depth;
- mapping quality.

A low VAF may reflect a genuine subclone, low purity, an emerging resistant clone, or artifact. A high VAF may reflect clonality, amplification of the mutant allele, or loss of the reference allele.

A future VAP should preserve:

```text
tumor_depth
normal_depth
tumor_ref_count
tumor_alt_count
normal_ref_count
normal_alt_count
tumor_vaf
normal_vaf
```

---

# 4. Tumor Purity

Tumor purity is the estimated fraction of a specimen derived from tumor cells.

A biopsy may contain:

```text
60% tumor cells
40% normal stromal, immune, and vascular cells
```

Normal-cell admixture dilutes somatic mutations. A heterozygous mutation present in every tumor cell might appear near 50% VAF at 100% purity, but near 20% VAF at 40% purity. Assuming a diploid locus, no copy-number alteration, and a heterozygous clonal mutation, the expected VAF may decline from approximately 50% at complete tumor purity to approximately 20% at 40% purity.

Purity affects:

- mutation-calling sensitivity;
- VAF interpretation;
- copy-number estimation;
- clonality inference;
- LOH analysis;
- false-negative risk.

Preserve:

```text
tumor_purity_estimate
purity_method
purity_software
purity_software_version
purity_uncertainty
```

---

# 5. Ploidy

Ploidy is the number of chromosome copies in a cell. Normal human somatic cells are usually diploid, but cancers frequently show whole-genome duplication, chromosome gains, chromosome losses, amplifications, and aneuploidy.

If a region has four copies and only one carries a mutation, expected VAF may be closer to 25% than 50%, even in a pure tumor.

Therefore:

```text
VAF without ploidy context can be misleading
```

Preserve:

```text
ploidy_estimate
local_copy_number
major_allele_copy_number
minor_allele_copy_number
ploidy_method
```

---

# 6. Copy-Number Alterations

Copy-number alterations are gains or losses of genomic material.

Examples include:

```text
MYC amplification
ERBB2 amplification
CDKN2A deletion
PTEN deletion
```

Cancer may be driven by focal amplifications, broad gains, heterozygous deletions, homozygous deletions, chromosome-arm changes, or whole-chromosome aneuploidy.

Copy-number state also changes expected VAF, so SNVs and indels should be interpreted in local copy-number context.

A copy-number observation should preserve:

```text
chromosomal_interval
total_copy_number
major_copy_number
minor_copy_number
gain_or_loss_status
focal_or_broad_status
caller
confidence
tumor_purity_context
```

---

# 7. Loss of Heterozygosity

Loss of heterozygosity, or LOH, occurs when one parental allele is lost or functionally eliminated in the tumor.

Example:

```text
matched normal:
BRCA2 = A/G

tumor:
BRCA2 = G/G
```

The tumor has lost the chromosome copy carrying `A`. The observed allelic pattern may arise through deletion or copy-neutral mechanisms and must be interpreted with local copy-number and purity context.

LOH is important in tumor-suppressor inactivation, hereditary cancer syndromes, second-hit models, and biallelic loss.

This creates a natural bridge between germline and somatic VAP:

```text
germline pathogenic variant
        +
somatic second hit or LOH
        ↓
biallelic tumor-suppressor inactivation
```

Preserve:

```text
locus
germline_heterozygosity_state
tumor_allelic_state
copy_number_context
loh_status
loh_method
confidence
```

---

# 8. Structural Variants

Structural variants are large genomic rearrangements, including:

- deletions;
- duplications;
- inversions;
- translocations;
- insertions;
- complex rearrangements.

They can disrupt tumor suppressors, activate oncogenes, alter enhancers, create gene fusions, or generate amplifications.

WGS is generally more informative than WES for structural-variant discovery because it captures intronic and intergenic breakpoints.

Preserve:

```text
breakpoint_1
breakpoint_2
orientation
event_type
supporting_read_pairs
split_read_support
copy_number_context
affected_genes
caller
confidence
```

---

# 9. Gene Fusions

A gene fusion occurs when parts of two genes are joined by a structural rearrangement.

Examples include:

```text
BCR::ABL1
EML4::ALK
NTRK fusions
FGFR2 fusions
```

Some fusions act as drivers, define tumor subtypes, support diagnosis, or predict therapy response.

DNA sequencing may detect the rearrangement, while RNA sequencing may confirm expression of the fusion transcript.

A future VAP–RSP ecosystem could link:

```text
DNA structural evidence
        +
RNA fusion expression evidence
```

Fusion observations should preserve:

```text
gene_5_prime
gene_3_prime
genomic_breakpoints
transcript_breakpoints
reading_frame
supporting_reads
DNA_or_RNA_evidence
fusion_caller
confidence
clinical_annotation
```

---

# 10. Somatic Filtering States

Somatic callers generate candidate mutations and then filter them.

Common reasons include:

- low depth;
- low alternate-read count;
- strand bias;
- orientation bias;
- mapping artifact;
- panel-of-normals support;
- contamination;
- sequence-context artifact;
- germline likelihood;
- poor base quality;
- read-position bias.

A filtered call is not the same as an absent call.

Important states are:

```text
not detected
detected and retained
detected and filtered
retained with uncertainty
```

A future VAP should preserve:

```text
raw_call_status
filter_status
filter_reason
caller_quality_metrics
artifact_evidence
panel_of_normals_status
germline_likelihood
```

---

# 11. Benchmark Truth

Cancer genomics needs reference materials analogous to HG002 germline benchmarking.

```text
HG002
    ↓
germline truth set
```

A somatic example is:

```text
HCC1395 tumor
+
HCC1395BL matched normal
    ↓
community somatic truth set
```

Benchmark truth sets support measurement of:

- precision;
- recall;
- F1 score;
- false-positive rate;
- false-negative rate;
- VAF-stratified performance;
- depth-stratified performance;
- SNV performance;
- indel performance.

A publication-reported mutation is not automatically a formal truth-set variant. Truth sets are generally built through multiple callers, multiple centers, orthogonal validation, consensus procedures, and confidence-region definitions.

Preserve:

```text
truth_set_name
truth_set_version
truth_region_status
truth_variant_status
comparison_method
precision
recall
false_positive
false_negative
```

---

# 12. Cancer-Aware Annotation

Standard germline annotation remains useful in oncology, but it is insufficient alone.

Cancer-specific annotation may include:

- hotspot status;
- oncogene or tumor-suppressor role;
- recurrence across cancer cohorts;
- somatic clinical significance;
- therapy sensitivity;
- therapy resistance;
- diagnostic relevance;
- prognostic relevance;
- cancer census membership;
- tumor-specific evidence level;
- biomarker eligibility;
- mutational-signature context.

Potential resources include:

```text
COSMIC
Cancer Gene Census
CIViC
OncoKB
ClinGen somatic resources
Cancer Genome Interpreter
```

Licensing and redistribution requirements must be reviewed before integration.

A driver alteration contributes to tumor growth or survival. A passenger alteration is present but does not materially drive tumor biology. This distinction is probabilistic and tumor-context dependent.

Cancer annotation should preserve:

```text
annotation_source
source_version
cancer_type
evidence_level
biomarker_type
therapy_context
driver_status
hotspot_status
clinical_significance
provenance
```

Annotations should never overwrite the original sequence observation.

---

# 13. Germline–Somatic Convergence

The future capability is to connect constitutional and acquired variation without collapsing them.

```text
                       patient
                          │
          ┌───────────────┴───────────────┐
          │                               │
          ▼                               ▼
   germline VAP branch              somatic VAP branch
          │                               │
constitutional variants         tumor–normal comparison
          │                               │
rare-disease meaning             acquired cancer mutations
          │                               │
          └───────────────┬───────────────┘
                          ▼
                    TEP-VAP outputs
                          │
                          ▼
                         VDB
```

The evidence objects should remain separate. Relationships such as germline predisposition, somatic second hit, or LOH should be created by explicit downstream projection.

---

# 14. Transferable VAP Capabilities

Many existing VAP capabilities already transfer to oncology:

- deterministic execution;
- staged architecture;
- stable run identities;
- reference provenance;
- tool-version capture;
- checksums;
- telemetry;
- immutable observation preservation;
- annotation provenance;
- validation reports;
- entity inventories;
- lineage manifests;
- TEP-VAP emission;
- VDB ingestion.

The oncology branch adds new biological primitives while reusing these execution and governance foundations.

---

# 15 Relationship to Somatic Extension Requirements

This rationale establishes the biological and architectural justification for
`docs/design/vap_somatic_extension_requirements.md`.

The rationale explains why somatic observations require branch-specific,
relational evidence. The requirements document translates those principles into
identity, calling, annotation, validation, TEP-VAP, and VDB integration
requirements.

---

# 16. Justification Summary: Somatic-Oncology VAP Expansion

A concise explanation:

> My current VAP implementation is germline-oriented, but I have designed a future somatic extension around a dual-branch patient model. The germline branch preserves constitutional variation, while the somatic branch treats tumor–normal comparison as a first-class observation. The extension would add tumor and normal specimen identities, VAF, purity and ploidy context, copy-number and LOH evidence, structural variants and fusions, somatic caller filtering states, cancer-aware annotation, and benchmarking against a reference tumor–normal truth set. The existing VAP execution, provenance, validation, and evidence-preservation architecture is transferable, while the somatic branch adds oncology-specific analytical semantics.

A more technical explanation:

> The key design decision is not to model somatic analysis as germline calling with different filters. Somatic evidence is relational. A call is meaningful only in the context of tumor depth, normal depth, VAF, purity, local copy number, contamination, caller state, and matched-normal comparison. My design keeps germline and somatic evidence distinct at the producer layer and reconnects them downstream through shared patient identity and explicit relationships such as second hits or LOH.

---

# 17. Key Terms

```text
Tumor–normal pairing
Comparison of tumor DNA with constitutional DNA from the same patient.

VAF
Fraction of reads supporting the alternate allele.

Tumor purity
Fraction of the specimen derived from tumor cells.

Ploidy
Number of chromosome copies in the tumor genome.

Copy-number alteration
Gain or loss of genomic material.

LOH
Loss of one parental allele in the tumor.

Structural variant
Large genomic rearrangement.

Gene fusion
Rearrangement joining portions of two genes.

Somatic filtering state
Caller decision and reason for retaining or rejecting a candidate.

Benchmark truth
Reference call set used to measure analytical performance.

Cancer-aware annotation
Interpretation using tumor-specific biological and clinical evidence.
```

---

# 18. Final Concept

The future VAP architecture can be summarized as:

```text
shared patient identity
        ↓
separate germline and somatic evidence generation
        ↓
branch-specific provenance and interpretation
        ↓
explicit downstream convergence
```

The governing principle is:

> Germline and somatic observations may involve the same patient, gene, or locus, but they must retain their distinct biological meaning, analytical provenance, and uncertainty.
