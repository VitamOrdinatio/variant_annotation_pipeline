# Genotype Observation Design

## Purpose

This document defines the system design for surfacing caller-emitted genotype evidence as a first-class VAP observation domain.

The genotype observation architecture establishes why genotype belongs within VAP, where it enters the evidence lifecycle, and which invariants must remain true.

This design translates that architecture into a concrete system shape.

It defines:

```text
participating components

data movement

projection timing

artifact registration

TEP-VAP integration

canonical-run backfill behavior

future automatic emission

non-interference controls
```

This document does not freeze:

```text
the final genotype TSV schema

column ordering

allowed-value enumerations

hash serialization rules

CLI syntax

SQLite tables

VDB persistence implementation

validation thresholds
```

Those concerns belong to subsequent specification, schema, contract, implementation-planning, and validation documents.

---

## Design Goals

The genotype observation design must satisfy the following goals.

### Surface latent caller evidence

VAP must surface the sample-specific genotype evidence already present in annotated VCF FORMAT and sample columns.

### Preserve source authority

Raw caller-emitted values must remain authoritative.

Any normalized labels emitted by VAP are deterministic convenience projections and must not replace raw source values.

### Remain additive

Genotype observation surfacing must add new artifacts and metadata without changing existing variant-centric outputs.

### Reuse one implementation

The 13-run backfill and future VAP execution must use the same canonical genotype projection implementation.

### Preserve explicit relationships

Every genotype observation must remain provably linked to:

```text
its source VCF record

its sample

its run

its assembly context

its coordinate and allele identity

its corresponding variant-observation relationship,
when such a relationship exists
```

For straightforward normalized biallelic records, this may resolve to a direct variant-observation join. For multiallelic records, split-normalized projections, or future multisample VCFs, the genotype observation must preserve enough source identity for VDB to construct the appropriate relationship without inference.

### Support future complexity

The design must remain compatible with:

```text
multi-allelic records

phased calls

non-diploid contexts

multisample VCFs

split-normalized projections

caller-specific FORMAT extensions
```

---

## System Context

The established variant-centric path remains:

```text
annotated_variants.vcf
    ↓
annotated_variants.tsv
    ↓
Stage 08 filtering and partitioning
    ↓
Stage 09 coding interpretation
    ↓
Stage 10 noncoding interpretation
    ↓
Stage 11 prioritization
    ↓
Stage 12 validation preparation
    ↓
Stage 13 run summarization
```

The genotype observation path is introduced in parallel:

```text
annotated_variants.vcf
    ↓
genotype projection component
    ↓
processed/genotype_observations.tsv
    ↓
run-state registration
    ↓
TEP-VAP genotype entity transport
    ↓
entities/genotype/genotype_observations.tsv
```

The two paths share the annotated VCF as a common source artifact.

They do not depend on one another semantically.

---

## Parallel Projection Design

The canonical design is:

```text
Annotated VCF
    ├── Variant Observation Projection
    │       └── annotated_variants.tsv
    │               └── Stages 08–13
    │
    └── Genotype Observation Projection
            └── genotype_observations.tsv
                    └── TEP-VAP genotype entity
```

The genotype projection is not derived from `annotated_variants.tsv`.

The genotype projection does not feed Stage 08.

The genotype projection does not alter coding or noncoding interpretation.

The genotype projection does not alter prioritization or validation preparation.

The two projections remain explicitly linked because they arise from the same annotated VCF record universe.

---

## Component Responsibilities

### Genotype Projection Module

The genotype projection module owns deterministic genotype extraction and surfacing.

Probable implementation location:

```text
pipeline/genotype_projection.py
```

Its responsibilities are:

```text
inspect annotated VCF headers

resolve the intended sample column

validate FORMAT/sample structure

parse FORMAT keys and sample values

preserve raw caller-emitted genotype evidence

extract recognized genotype fields when present

derive normalized descriptive states

preserve source-record provenance

emit genotype_observations.tsv

return structured projection metrics
```

It must not:

```text
modify the source VCF

modify annotated_variants.tsv

modify Stage 08–13 artifacts

register VDB entities

perform inheritance reasoning

perform disease interpretation

implement SQLite persistence
```

---

### Pipeline Orchestration

Pipeline orchestration determines when genotype projection runs and which execution context is supplied.

Likely integration points include:

```text
run_pipeline.py

src/pipeline_runner.py
```

The orchestrator is responsible for:

```text
waiting until the annotated VCF exists and is validated

passing the authoritative annotated VCF path

passing sample identity

passing run identity

passing reference-build context

passing source-pipeline context

selecting the processed output path

recording projection success or failure

registering the emitted artifact in pipeline state
```

The projection should be invoked after Stage 07 completes and before normal run finalization.

Its execution order may precede Stage 08, but Stage 08 must not consume its output.

Therefore:

```text
execution ordering
≠
semantic dependency
```

---

### Run-State Registration

The emitted artifact should be registered additively within VAP run state.

Recommended artifact registration:

```text
state["artifacts"]["genotype_observations"]
```

Recommended QC registration:

```text
state["qc"]["genotype_projection_qc"]
```

Recommended execution registration:

```text
state["stage_outputs"]["genotype_observation_projection"]
```

The implementation may later introduce a dedicated projection-output state domain if repository-wide state architecture supports it.

The design preference is to minimize state-model disruption while keeping genotype projection explicitly identifiable and non-numbered.

---

### TEP Entity Builder

The TEP builder consumes:

```text
processed/genotype_observations.tsv
```

and transports it to:

```text
entities/genotype/genotype_observations.tsv
```

The genotype artifact must be registered as a first-class TEP entity.

Recommended semantic role:

```text
entity_domain = genotype

entity_role = genotype_observation

source_stage = genotype_projection

source_artifact_role = caller_emitted_genotype_observations
```

The TEP builder is responsible for:

```text
artifact transport

checksum calculation

inventory registration

lineage registration support

required-artifact validation

transport-path declaration
```

The TEP builder must not reinterpret genotype evidence.

---

### Canonical-Run Backfill Wrapper

A separate MARK-oriented backfill wrapper should iterate the 13 canonical VAP runs.

The wrapper may own:

```text
run-manifest iteration

source VCF discovery

preflight validation

existing-output detection

TEP path resolution

per-run logging

failure isolation

summary reporting

TGZ receipt generation
```

It must not implement a second genotype parser.

The required design is:

```text
backfill wrapper
    ↓
canonical genotype projection module
    ↓
processed/genotype_observations.tsv
    ↓
TEP-VAP hardening
```

The same projection logic must serve both backfill and future pipeline execution.

---

## Invocation Timing and Dependency Boundaries

The genotype projection should run after the annotated VCF is complete and validated.

Recommended execution order:

```text
Stage 07 completes
    ├── annotated VCF available
    ├── annotated TSV available
    └── genotype projection invoked

then

Stage 08 begins on annotated TSV
```

The genotype projection belongs to the observation domain.

Stage 08 belongs to the variant-routing domain.

Stage 08 must not depend on genotype output.

The projection may be treated as mandatory for completed future VAP executions if genotype emission is part of the VAP output contract.

That operational requirement does not make genotype a semantic input to Stage 08.

---

## Source Context and Authority

The projection consumes two categories of information.

### Caller-emitted VCF content

The VCF is authoritative for:

```text
CHROM

POS

REF

ALT

QUAL

FILTER

FORMAT

sample field

GT

AD

DP

GQ

PL

FT where present

phase notation

no-call representation

caller-specific FORMAT values
```

### Source VCF header context

The projection should preserve or reference source VCF header context needed to interpret FORMAT fields.

This includes, where available:

```text
FORMAT header definitions

contig declarations

reference declarations

sample column names

caller or workflow metadata

source VCF header checksum or header-context hash
```

The design does not require copying the full VCF header into every genotype row.

However, TEP-VAP must preserve enough header context or header identity for VDB and downstream consumers to audit how FORMAT fields were defined in the source artifact.


### VAP-supplied run context

VAP runtime state or configuration supplies:

```text
sample_id

run_id

reference_build

source_pipeline

annotated_vcf_path
```

The projection must also preserve the resolved VCF sample-column identity:

```text
vcf_sample_column_name

sample_selection_policy

sample_identity_mapping_status
```

VAP must not assume that the VCF sample column label, SRA accession, run identifier, and biological specimen identifier are identical.

Additional context may include:

```text
SRA accession

assay type

annotation engine

normalization policy identifier
```

The design must preserve the authority distinction.

Caller-emitted evidence must not be rewritten as though it originated from VAP.

VAP-supplied context must not be inferred from FORMAT values.

---

## Genotype Surface Scope

The genotype observation artifact is a record-scoped preservation surface.

It represents genotype evidence emitted for records present in the source VCF. It is not a genome-wide genotype matrix and does not represent every locus where the sample may be homozygous reference, unassayed, not callable, or absent from the called variant set.

Therefore, missing rows from `genotype_observations.tsv` must not be interpreted as:

```text
homozygous reference

variant absent

locus callable

locus not assayed

reference-confidence evidence

negative evidence for RDGP
```

Those concepts require separate opportunity, callability, coverage, assay-scope, or reference-confidence surfaces.

The genotype projection may summarize source-record counts and projection coverage in QC metrics, but it must not emit synthetic genotype observations for loci absent from the source VCF.

---

## Record Projection Workflow

For each source VCF record, the genotype projection should perform the following sequence.

```text
1. Read coordinate and allele fields.

2. Read FORMAT keys.

3. Resolve the selected sample column.

4. Preserve the raw FORMAT string.

5. Preserve the raw sample field.

6. Map FORMAT keys to sample values.

7. Extract recognized genotype fields when present.

8. Derive descriptive genotype states without replacing raw values.

9. Preserve source-record identity and provenance.

10. Emit the genotype observation according to the locked cardinality policy.

11. Record projection metrics and missingness states.
```

The parser must tolerate optional genotype fields being absent.

The parser must not infer values that the caller did not emit.

---

## Record Cardinality Model

The genotype projection must preserve source VCF semantics before optimizing joins.

Two broad row models are possible.

### One row per sample per source VCF record

Example source record:

```text
REF=A
ALT=C,G
GT=1/2
```

A single genotype observation preserves:

```text
source_record_ref = A

source_record_alt = C,G

gt_raw = 1/2

called_allele_indices = 1,2
```

Advantages:

```text
faithful to source VCF structure

simple source-record traceability

no synthetic genotype splitting

record-level AD and PL arrays remain intact
```

### One row per alternate-allele projection

The same record may be represented as separate allele rows.

Advantages:

```text
direct joins to allele-specific variant observations
```

Risks:

```text
GT 1/2 becomes distributed across multiple rows

record-level likelihood arrays become difficult to represent

source genotype meaning may be flattened

synthetic projection logic becomes part of the producer contract
```

### Design preference

The preferred design is:

```text
one source-faithful genotype observation
per selected sample per source VCF record
```

This preserves caller-emitted record semantics.

A future explicit link surface may associate one genotype observation with multiple allele-specific variant observations when necessary.

The initial canonical corpus may be predominantly biallelic after normalization.

That operational reality must not be encoded as universal biological truth.

---

## Variant/Genotype Relationship Design

The design uses two complementary linkage layers.

### Direct convenience linkage

For straightforward normalized biallelic records, preserve:

```text
sample_id

run_id

reference_build

chromosome

position

reference_allele

alternate_allele

variant_id
```

These fields support direct run-scoped joins.

For multiallelic or otherwise complex records, direct `variant_id` linkage must not fabricate a single allele-specific relationship when the source record supports multiple alternate alleles or multiple called allele indices.

In those cases, the genotype observation should preserve source-faithful record identity and mark direct allele-specific linkage as complex, deferred, or requiring a future link surface.

### Source-faithful linkage

Always preserve sufficient provenance for complex relationships:

```text
source_vcf_path

source_vcf_sha256

source_record_hash

source_record_ref

source_record_alt

called_allele_indices

allele_index where applicable
```

A separate `variant_genotype_links.tsv` is not required by this design for the initial implementation.

However, the genotype artifact must contain enough information to generate such a link surface deterministically later.

A dedicated link artifact becomes appropriate when the system must represent:

```text
one source record to multiple variant observations

multiallelic source records

split-normalized records

multiple samples

nonstandard ploidy

many-to-many projection relationships
```

---

## Raw and Normalized Evidence Layers

The genotype observation contains two conceptual layers.

### Raw source layer

Preserve exactly when present:

```text
FORMAT

sample FORMAT value

GT

AD

DP

GQ

PL

FT

caller-specific fields retained by policy
```

### Normalized descriptive layer

VAP may derive:

```text
genotype_label

zygosity_state

phase_state

is_no_call

is_missing

gt_arity

called_allele_indices

multiallelic status
```

`gt_arity` means the number of allele positions represented in the raw `GT` string after parsing genotype separators such as `/` or `|`.

Examples:

```text
GT=0/1      gt_arity=2
GT=1/1      gt_arity=2
GT=0|1      gt_arity=2
GT=1        gt_arity=1
GT=./.      gt_arity=2
GT=1/2      gt_arity=2
GT=0/1/2    gt_arity=3
```

This field describes the structure of the emitted `GT` value. It is not a biological ploidy assertion.

VAP should preserve caller-emitted or upstream-declared ploidy context when available, but it must not infer biological ploidy, sex, hemizygosity, inheritance mode, or mitochondrial heteroplasmy from GT structure, chromosome label, sample name, or allele depth alone.

The governing rule is:

```text
Raw caller evidence is authoritative.

Normalized labels are deterministic convenience projections.
```

Normalized labels must never replace raw values.

The raw layer must remain sufficient to audit every normalized classification.

---

## Missingness and No-Call Design

The genotype projection must distinguish at least the following states:

```text
FORMAT column absent

sample column absent

GT absent from FORMAT

GT key present with missing value

GT = .

GT = ./.

GT = .|.

malformed GT

record-level filter present

sample-level filter present

absence from source VCF record universe
    # represented in projection scope/QC only,
    # not as a per-row genotype observation
```

Because `genotype_observations.tsv` is record-scoped, absence from the source VCF record universe is not emitted as a genotype observation row. It may be summarized in projection metrics or scope documentation, but it must not be converted into homozygous reference, no-call, or negative evidence.

These states are not equivalent.

The design prohibits:

```text
coercing missing GT to homozygous reference

coercing no-call to absence

coercing malformed GT to unknown without preserving the raw value

treating absence from the VCF as a genotype observation
```

The later schema and specification documents must define explicit status values for these conditions.

---

## Error Handling

The design adopts strictness at file and header boundaries while preserving incomplete record-level evidence when possible.

### Projection-level failure conditions

The projection should fail when:

```text
the VCF header is missing

the source VCF is globally malformed

the expected sample cannot be resolved

a multisample VCF is encountered without an explicit sample-selection policy

required source context is unavailable

the output artifact cannot be written deterministically
```

Whether absence of FORMAT is a hard failure depends on the later contract.

For genotype-required execution, FORMAT absence should fail.

For surveillance or explicitly optional execution, it may be reported as unavailable.

### Record-level preservation conditions

Individual records should be preserved and classified when:

```text
GT is absent

AD is absent

DP is absent

GQ is absent

PL is absent

FORMAT/sample lengths differ

caller-specific fields are unsupported

sample values contain missing trailing entries
```

Optional field absence must not cause silent record deletion.

---

## Canonical Artifact-Set Resolution

The certified genotype observation schema resolves the physical artifact
set that this design previously left partially open.

The canonical genotype projection output is the indivisible three-artifact
set:

```text
processed/genotype_observations.tsv

processed/genotype_projection_summary.json

processed/genotype_source_header_context.json
```

The canonical TEP-VAP destinations are:

```text
entities/genotype/genotype_observations.tsv

entities/genotype/genotype_projection_summary.json

entities/genotype/genotype_source_header_context.json
```

Where this design refers generically to:

```text
the genotype artifact

a projection summary

header context or equivalent metadata
```

those references shall be interpreted according to the certified
three-artifact schema above.

The projection, backfill, future automatic-emission path, and TEP-VAP
packaging path shall treat the three artifacts as one complete output set.

## Processed Artifact Design

The canonical run-level artifact is:

```text
processed/genotype_observations.tsv
```

The artifact must be:

```text
deterministic

tabular

source-traceable

sample-aware

run-aware

assembly-aware

checksum-addressable

suitable for TEP transport

suitable for VDB registration
```

The processed artifact is additive.

It does not replace:

```text
annotated_variants.vcf

annotated_variants.tsv

stage_08_vdb_ready_variants.tsv
```

---

## Projection Summary Design

In addition to `processed/genotype_observations.tsv`, the projection should emit or register a compact projection summary.

Recommended artifact or run-state role:

```text
processed/genotype_projection_summary.json
```

or equivalent structured run-state metadata.

The summary should capture:

```text
source_vcf_path

source_vcf_sha256

source_header_context_hash, where available

resolved_sample_column

sample_id

run_id

reference_build

source_record_count

genotype_observation_row_count

GT_present_count

GT_missing_count

no_call_count

AD_present_count

DP_present_count

GQ_present_count

PL_present_count

multiallelic_record_count

phased_gt_count

unphased_gt_count

malformed_record_count

projection_status

projection_warnings
```

The summary is not a replacement for genotype observations. It is a compact audit surface for TEP packaging, VDB registration, backfill certification, and future RDGP-readiness checks.


---

## TEP-VAP Packaging Design

The canonical TEP-VAP location is:

```text
entities/genotype/genotype_observations.tsv
```

Recommended companion location:

```text
entities/genotype/genotype_projection_summary.json
```

or equivalent manifest metadata.

The TEP should also preserve or reference the source VCF header context used to interpret FORMAT fields, either as a header-context artifact, a header checksum, or a declared source VCF artifact reference.

TEP integration must update:

```text
entity_inventory.json

lineage_manifest.json

validation_report.md

artifact checksums

package manifests where applicable
```

Required lineage:

```text
annotated_variants.vcf
    → genotype_observations.tsv
```

Parallel lineage:

```text
annotated_variants.vcf
    → annotated_variants.tsv
```

The TEP must not imply:

```text
annotated_variants.tsv
    → genotype_observations.tsv
```

because the genotype projection reads FORMAT and sample data directly from the VCF.

---

## Backfill Design for the 13 Canonical Runs

The existing canonical corpus includes:

```text
12 epilepsy WES runs

1 HG002 WGS run
```

The backfill workflow should be divided into four phases.

### Preflight

For each run:

```text
confirm run directory exists

locate retained annotated VCF

confirm VCF is readable

inspect VCF header

resolve sample column

confirm reference metadata exists

confirm TEP path exists

detect pre-existing genotype output
```

### Projection

Invoke the canonical genotype projection implementation to emit:

```text
processed/genotype_observations.tsv
```

### TEP hardening

Transport the processed artifact into:

```text
entities/genotype/genotype_observations.tsv
```

Then refresh:

```text
entity inventory

lineage manifest

validation report
```

### Receipts

Write run-external audit outputs under:

```text
/root/Desktop/
```

Recommended receipts include:

```text
per-run status

source VCF path

source VCF checksum

source record count

genotype output row count

output checksum

GT availability count

AD availability count

DP availability count

GQ availability count

PL availability count

missingness distributions

TEP registration status

lineage status

validation status
```

A TGZ bundle should package the full receipt set.

The backfill must not modify existing variant-centric artifacts.

---

## Future Automatic Emission

Future VAP executions should automatically produce:

```text
processed/genotype_observations.tsv
```

after the annotated VCF becomes available.

Future TEP-VAP builds should automatically transport:

```text
entities/genotype/genotype_observations.tsv
```

The future execution path should conceptually call a single projection interface such as:

```text
project genotype observations from:
    annotated VCF
    sample identity
    run identity
    reference build
    source-pipeline context

emit:
    genotype observation artifact
    structured projection summary
```

The exact Python function name and signature are deferred.

The callable must guarantee:

```text
deterministic output

no source VCF mutation

no variant-centric TSV mutation

structured result metadata

explicit failures

reusable invocation from backfill and normal execution
```

---

## Non-Interference Controls

The implementation must explicitly verify that genotype surfacing does not change:

```text
raw VCF

normalized VCF

annotated VCF

annotated_variants.tsv

Stage 08 outputs

Stage 09 outputs

Stage 10 outputs

Stage 11 outputs

Stage 12 outputs

Stage 13 scientific summaries

existing TEP-VAP variant entities and their scientific contents
```

For existing canonical runs, pre-patch and post-patch checksums should be compared for all preserved scientific evidence artifacts.

Expected changes are limited to:

```text
processed/genotype_observations.tsv

TEP genotype artifact

entity inventory

lineage manifest

validation report

package or artifact manifests

run-state metadata in future executions
```

If existing TEP-VAP manifests are updated to register genotype artifacts, those manifest changes must be additive. Existing variant entities must not be rewritten except for additive cross-reference metadata explicitly permitted by the later contract.

---

## Extensibility

The design must remain compatible with:

```text
single-sample VCFs

multisample VCFs

biallelic records

multiallelic records

phased genotypes

unphased genotypes

haploid calls

diploid calls

hemizygous contexts

mitochondrial contexts

polyploid or copy-number-aware callers

caller-specific FORMAT fields

split-normalized variant projections
```

The initial implementation may explicitly support only the current canonical single-sample VAP corpus.

Unsupported complexity must be detected and reported rather than silently flattened.

---

## Design Decisions Deferred to Later Documents

The following are intentionally deferred.

### Specification

```text
required behaviors

parsing rules

normalization semantics

status semantics

multisample policy

multiallelic policy

determinism requirements
```

### Schema

```text
exact columns

column order

data types

null representation

allowed values

identity fields

hash fields
```

### Contract

```text
producer guarantees

consumer expectations

required artifact status

error conditions

version compatibility
```

### Implementation Plan

```text
module names

function names

orchestration patch points

backfill script design

TEP-builder patch sequence

test implementation order
```

### Validation

```text
acceptance criteria

row-count parity checks

source-record traceability checks

non-interference checks

multiallelic tests

missingness tests

backfill certification
```

---

## Design Success Criteria

The design is successful when it provides a clear path for:

```text
one canonical genotype projection implementation

automatic future processed-output emission

additive 13-run backfill

first-class TEP-VAP genotype transport

explicit variant/genotype linkage

raw caller evidence preservation

normalized convenience labels

strict non-interference with Stages 01–13

future VDB registration

record-scoped genotype evidence is not treated
as genome-wide reference genotype evidence

missing genotype rows are not treated
as homozygous reference, variant absence,
callability, or negative RDGP evidence

VDB can preserve genotype observations
without re-reading raw VAP internals

RDGP receives genotype as an observation substrate,
not as a completed inheritance interpretation

future RDGP genotype-aware reasoning
```

---

## Final Design Summary

The genotype observation system uses one source-faithful projection from the annotated VCF.

That projection is invoked automatically by VAP orchestration, emits `processed/genotype_observations.tsv`, registers the artifact in run state, and enables TEP-VAP transport to `entities/genotype/genotype_observations.tsv`.

The 13-run backfill and future pipeline execution use the same canonical projection logic.

Raw caller evidence remains authoritative.

Normalized labels remain additive.

Stages 08–13 remain unchanged.

Variant observation and genotype observation remain separate but explicitly linked evidence domains.

VDB preserves their relationship and exposes genotype-aware projection surfaces under explicit policy.

RDGP reasons over genotype-aware VDB projections downstream, without treating VAP genotype observations alone as complete inheritance interpretations.