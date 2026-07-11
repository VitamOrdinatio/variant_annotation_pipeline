# Genotype Observation Architecture

## Purpose

This document defines the architecture for surfacing caller-emitted genotype evidence as a first-class VAP evidence domain.

VAP already produces VCF artifacts containing sample-specific genotype evidence in FORMAT and sample columns. The genotype observation architecture promotes that latent evidence into an explicit, governed, and transportable observation surface without altering the established variant-centric pipeline.

This document defines:

- why genotype observation belongs within VAP;
- where genotype evidence enters the VAP evidence lifecycle;
- how genotype observation relates to variant observation;
- which authority boundaries govern genotype handling;
- which invariants must remain true across processed outputs, TEP-VAP emission, VDB registration, and RDGP reasoning;
- what existing VAP behavior must remain unchanged.

This document does not define the final TSV schema, hash serialization, parser implementation, CLI behavior, SQLite schema, or validation thresholds. Those concerns belong to subsequent design, specification, schema, contract, implementation-planning, and validation documents.

---

## Architectural Thesis

VAP already produces VCF artifacts containing caller-emitted, sample-specific genotype evidence.

The genotype observation architecture surfaces this latent evidence as a first-class VAP evidence domain and transports it through TEP-VAP without altering the established variant-centric pipeline.

The governing model is:

```text
Annotated VCF
    ├── Variant Observation Projection
    │       └── annotated_variants.tsv
    │               └── Stages 8–13
    │
    └── Genotype Observation Projection
            └── genotype_observations.tsv
                    └── TEP-VAP genotype entity
```

The two outputs are sibling projections from the same annotated VCF record universe.

The genotype observation surface is not derived from `annotated_variants.tsv`.

The genotype observation surface is not an interpretation overlay.

The genotype observation surface is not a new variant-centric stage.

---

## Biological and Computational Meaning

### Biological genotype

A genotype is the sample-specific allelic state represented by the alleles called at a genomic locus.

For a diploid locus:

```text
allele 1
+
allele 2
=
genotype
```

The same genomic locus may have different genotype states across samples.

Examples include:

```text
heterozygous

homozygous reference

homozygous alternate

phased heterozygous

no-call

haploid or hemizygous state
```

### Genotype observation

A genotype observation is the caller-emitted representation of that sample-specific allelic state together with its supporting evidence.

Examples include:

```text
GT

AD

DP

GQ

PL

phase notation

sample FORMAT values
```

VAP does not create or infer this evidence downstream.

VAP surfaces and preserves the genotype evidence already emitted by the variant caller.

---

## Current VAP Evidence Boundary

The genotype evidence lifecycle currently behaves as follows:

```text
Stage 05 raw VCF
    caller-emitted genotype evidence present

Stage 06 normalized VCF
    genotype evidence remains within the VCF artifact

Stage 07 annotated VCF
    genotype evidence remains within the VCF artifact

Stage 07 annotated_variants.tsv
    variant-centric annotation projection only

Stages 08–13
    variant-centric transformation, interpretation,
    prioritization, validation, and reporting
```

The current Stage 07 TSV projection reads the variant and INFO-level fields required for the canonical variant-centric pathway.

It does not surface FORMAT or sample-column genotype evidence into the TSV pathway.

The genotype observation architecture therefore introduces an additional projection from the annotated VCF rather than modifying the established variant-centric projection.

---

## Sibling Projection Model

The canonical architecture is:

```text
annotated_variants.vcf
    ├── variant observation projection
    └── genotype observation projection
```

These two projections remain distinct because they answer different scientific questions.

### Variant observation asks

```text
What genomic alternate allele was observed?

Where is it located?

How was it annotated?

What biological context applies?
```

### Genotype observation asks

```text
What sample-specific allelic state did the caller emit?

What caller evidence supports that state?

Was the call phased, unphased, missing, filtered, or no-call?
```

The relationship is therefore:

```text
variant observation
    ≠
genotype observation
    ≠
interpretation
```

They are related evidence objects, not interchangeable representations.

---

## Genotype Observation Scope and Absence Semantics

A genotype observation surface is a preservation surface for caller-emitted genotype evidence present in VCF records.

The absence of a row from `genotype_observations.tsv` does not mean:

```text
homozygous reference
variant absent
locus callable
locus not assayed
no variant evidence exists
```

It means only that no genotype observation was emitted into this surface for that row, locus, sample, or source-record context.

For VAP v1, `genotype_observations.tsv` is expected to represent genotype evidence for VCF records, not a genome-wide genotype matrix. It is therefore a positive or record-scoped genotype observation surface, not a complete reference-genotype absence surface.

Downstream systems must not infer reference genotype, biological absence, callability, assay scope, or opportunity from missing genotype rows. Those concepts require separate opportunity, callability, coverage, assay-scope, or reference-confidence evidence.

---

## Relationship to the 13-Stage Variant-Centric Pipeline

The existing 13 VAP stages are variant-centric.

They perform:

```text
data loading

alignment

BAM processing

alignment QC

variant calling

VCF normalization

variant annotation

variant filtering and partitioning

coding interpretation

noncoding interpretation

prioritization

validation preparation

run summarization
```

Genotype observation surfacing is attached to the VCF lifecycle but does not belong inside the semantic numbering of Stages 8–13.

The genotype projection should be implemented as an observation-domain projection invoked by pipeline orchestration after the annotated VCF exists.

The architectural relationship is:

```text
Stage 07 annotated VCF
        ├── canonical variant projection
        │       └── annotated_variants.tsv
        │               └── Stages 8–13
        │
        └── genotype projection
                └── genotype_observations.tsv
```

The genotype projection must not alter the existing variant-centric execution path.

---

## Genotype Observation Authority

### Variant caller authority

The variant caller is authoritative for caller-emitted genotype evidence, including:

```text
GT

AD

DP

GQ

PL

FORMAT structure

sample field values

phase notation

no-call representation

caller-specific genotype filters
```

### Source VCF context

FORMAT values are not fully interpretable without their source VCF context.

The genotype observation surface should preserve or reference the source VCF context needed to interpret FORMAT fields, including:

```text
FORMAT definitions

sample column names

contig and reference declarations

source VCF path

source VCF checksum

caller or workflow metadata, where available

header context required to interpret caller-specific FORMAT fields
```

VAP may emit normalized descriptive labels, but raw FORMAT keys, raw sample values, and source VCF context remain the authoritative preserved evidence.

### VAP authority

VAP is authoritative for:

```text
preserving raw caller-emitted genotype fields

surfacing genotype observations into a governed tabular artifact

normalizing descriptive labels without replacing raw values

preserving source VCF provenance

preserving source VCF header/context references

preserving VCF sample-column identity

mapping VCF sample-column identity to VAP sample/run identity

maintaining sample and run identity

linking genotype observations to variant observations

transporting genotype evidence through TEP-VAP
```

The VCF sample column name must be preserved and mapped explicitly to VAP sample and run identity. VAP must not assume that the VCF sample column label, SRA accession, run identifier, and biological specimen identifier are always the same identifier.

VAP must not infer inheritance, disease causality, or compound heterozygosity.

### VDB authority

VDB is authoritative for:

```text
genotype entity registration

persistent storage

cross-entity topology

variant/genotype relationship persistence

consumer-facing genotype projections
```

### RDGP authority

RDGP is authoritative for:

```text
inheritance reasoning

zygosity-aware prioritization

compound heterozygous reasoning

family-model reasoning

genotype-aware burden interpretation
```

---

## First-Class Evidence Requirements

Genotype observation becomes first-class only when it receives all of the following:

```text
a named evidence domain

an explicit entity role

a governed schema

source provenance

lineage representation

validation criteria

processed-output emission

TEP-VAP transport

consumer expectations

future versioning
```

A standalone TSV is not sufficient.

The first-class surface requires:

```text
processed/genotype_observations.tsv

run-state registration

TEP genotype entity

entity inventory record

lineage manifest record

transport checksum

validation coverage

consumer contract
```

---

## Relational and Lineage Invariants

A genotype observation must never become detached from:

```text
its source VCF record

its sample

its run

its reference-build context

its coordinate and allele identity

its corresponding variant observation
```

The minimum relational invariant is:

```text
Every genotype observation must remain provably linked
to one source VCF record and to the corresponding
variant observation when that observation exists.
```

The architecture requires preservation of:

```text
VCF sample-column identity

VAP sample identity

run identity

specimen or participant identity, if known

reference build

chromosome

position

reference allele

alternate allele

normalization state or policy

allele index, where applicable

source VCF identity

source VCF header/context identity

source-record identity
```

Subsequent design and schema documents must provide both:

```text
a compact join handle

and

decomposed source-preserved identity fields
```

The architecture does not yet prescribe the final durable-handle or hashing algorithm.

Any future hash-based identity must define:

```text
canonical serialization order

normalization policy identifier

contig normalization rules

missing-value encoding

multiallelic allele indexing

hash algorithm

identity-version semantics
```

---

## Non-Interference Doctrine

Genotype observation surfacing must not alter existing variant-centric VAP behavior.

For identical run inputs and configuration, genotype surfacing must not change:

```text
variant calls

normalized VCF content

annotated VCF content

annotated_variants.tsv content

Stage 8–13 row counts

Stage 8–13 column sets

coding interpretation labels

noncoding interpretation labels

priority assignments

validation assignments

existing scientific evidence semantics
```

Only additive outputs may be introduced.

Expected additive changes include:

```text
processed/genotype_observations.tsv

TEP genotype entity

entity inventory updates

lineage manifest updates

validation report updates

artifact manifest or run-summary registration where appropriate
```

This non-interference invariant must be validated explicitly.

---

## Existing-Run Backfill and Future Automatic Emission

The architecture supports two execution contexts that must share the same genotype projection implementation.

### Existing canonical-run backfill

```text
retained annotated VCF
    ↓
canonical genotype projection logic
    ↓
processed/genotype_observations.tsv
    ↓
additive TEP-VAP hardening
```

### Future VAP execution

```text
annotated VCF created
    ↓
canonical genotype projection logic
    ↓
processed/genotype_observations.tsv
    ↓
automatic TEP-VAP genotype entity emission
```

The backfill path and future-execution path must not implement genotype parsing independently.

A single canonical projection implementation must govern both.

---

## TEP-VAP Integration

The canonical processed artifact should be:

```text
processed/genotype_observations.tsv
```

The canonical TEP-VAP destination should be:

```text
entities/genotype/genotype_observations.tsv
```

The genotype TEP entity should be first-class and explicitly identified as caller-emitted sample genotype evidence.

The lineage model should record:

```text
annotated_variants.vcf
    → genotype_observations.tsv
```

and separately:

```text
annotated_variants.vcf
    → annotated_variants.tsv
```

VDB may then register the relationship:

```text
variant_observation
    ↔
genotype_observation
```

without implying that genotype was derived from the Stage 07 TSV.

---

## Future Cardinality and Extensibility

The architecture must remain compatible with:

```text
multi-allelic VCF records

phased genotype calls

haploid contexts

hemizygous contexts

mitochondrial ploidy

multisample VCFs

split-normalized variant projections

missing genotype fields

no-call states

caller-specific FORMAT extensions
```

The architecture must not encode the following as universal biological truth:

```text
one sample
×
one variant row
×
one genotype row
```

The initial implementation may target the current canonical single-sample VAP corpus.

However, the evidence model must remain compatible with broader cardinalities.

---

## Ploidy and Allelic-State Non-Overinterpretation

Initial genotype observation surfacing should preserve GT arity, allele structure, phase notation, and raw caller evidence without inferring biological ploidy, sex, inheritance mode, or mitochondrial heteroplasmy unless those values are explicitly emitted by the caller or declared by an upstream governed artifact.

For example, VAP should not infer:

```text
hemizygosity from chromosome label alone

sex-specific genotype meaning from sample naming alone

mitochondrial heteroplasmy from allele depth alone

inheritance compatibility from GT alone

compound heterozygosity from the presence of multiple heterozygous calls
```

Those are downstream reasoning tasks requiring additional metadata, projection policy, family context, ploidy context, or RDGP-owned reasoning models.

VAP may preserve caller-emitted evidence that later supports those analyses, but it must not convert preserved genotype observations into inheritance conclusions.

---

## RDGP-Ready Does Not Mean RDGP-Sufficient

Genotype observation surfacing makes caller-emitted genotype evidence available to VDB and RDGP, but it does not by itself create a complete inheritance-reasoning surface.

RDGP-ready genotype reasoning may also require:

```text
variant consequence context

gene and transcript projection

phase evidence

family relationships

sample sex or ploidy metadata

opportunity and callability context

coverage or assay-scope evidence

quality threshold policies

population-frequency context

phenotype and prior evidence
```

The genotype observation surface therefore provides an essential observation substrate, not a complete RDGP reasoning product.

VAP preserves genotype evidence.

VDB registers, relates, and projects genotype evidence.

RDGP reasons over genotype evidence in combination with other governed evidence surfaces.

---

## Non-Goals

Genotype observation surfacing does not:

```text
infer inheritance mode

infer disease causality

infer compound heterozygosity

reclassify variants

change interpretation labels

change priority tiers

change validation assignments

replace raw GT with normalized labels

treat no-call as homozygous reference

treat absence from a VCF as homozygous reference

infer homozygous reference state from missing genotype rows

create a genome-wide reference genotype matrix

define opportunity, callability, or assay-scope denominators

force genotype columns into Stage 8–13 artifacts

require immediate VDB schema redesign

require rerunning canonical SRAs when retained VCFs are available
```

---

## Architectural Success Criteria

The architecture is successful when:

```text
caller-emitted genotype evidence is surfaced
as a first-class VAP observation domain

processed/genotype_observations.tsv is emitted
for eligible VAP runs

TEP-VAP transports genotype observations
as a dedicated genotype entity

every genotype observation remains linked
to source VCF, sample, run, assembly context,
and the corresponding variant observation relationship
when such a relationship exists

complex cases such as multiallelic records,
split-normalized projections, or future multisample VCFs
preserve enough source identity for VDB to construct
variant/genotype relationships without inference

existing Stage 1–13 behavior remains unchanged

VDB can register the variant/genotype relationship
without inference

missing genotype rows are not interpreted
as homozygous reference, variant absence,
callability, or assay opportunity

source VCF header/context and sample-column identity
remain available for downstream interpretation of FORMAT fields

RDGP receives genotype-aware evidence only as an observation substrate,
not as a completed inheritance-reasoning result

RDGP can later consume genotype-aware VDB projections
for inheritance and zygosity reasoning
```

---

## Final Doctrine

VAP does not create genotype meaning downstream.

VAP surfaces caller-emitted genotype evidence already present in the VCF record universe.

Missing genotype-observation rows are not absence calls.

Variant observation and genotype observation remain distinct but explicitly linked evidence domains.

Genotype surfacing is additive.

The established variant-centric pipeline remains unchanged.

TEP-VAP transports both observation domains so that VDB can preserve their relationship and RDGP can reason over it.
