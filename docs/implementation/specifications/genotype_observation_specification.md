# Genotype Observation Specification

## Purpose

This specification defines the normative producer behavior required to surface caller-emitted genotype evidence as a first-class VAP observation domain.

It translates the certified genotype observation architecture and design into implementation requirements that remain coherent across:

```text
VAP
    ↓
TEP-VAP
    ↓
VDB
    ↓
RDGP
```

This document specifies:

```text
required projection behavior

required inputs

required outputs

sample resolution

VCF record handling

FORMAT and sample-field preservation

genotype-state normalization boundaries

source provenance

variant/genotype relationship semantics

determinism

TEP-VAP registration

backfill behavior

future automatic emission

non-interference

downstream interpretation restrictions
```

This document does not freeze:

```text
final TSV column order

final data types

final allowed-value enumerations

final hash-field names

CLI syntax

SQLite schema

VDB persistence implementation

RDGP reasoning implementation

validation thresholds
```

Those concerns belong to the genotype observation schema, contract, implementation plan, and validation documents.

---

## Relationship to Certified Architecture and Design

The certified architecture defines:

```text
why genotype observation belongs within VAP

where genotype evidence enters the VAP evidence lifecycle

which authority boundaries govern genotype handling

which invariants must remain true across repositories
```

The certified design defines:

```text
component responsibilities

parallel projection behavior

execution timing

artifact movement

backfill and future-execution reuse

TEP-VAP integration

non-interference controls
```

This specification defines the mandatory behavior that implements those decisions.

The governing precedence is:

```text
Architecture
    >
Design
    >
Specification
    >
Schema
    >
Implementation
```

The specification shall not contradict the architecture or design.

---

## Normative Language

The following terms are normative:

```text
shall
    mandatory

shall not
    prohibited

should
    strongly recommended

may
    optional
```

---

## Scope

The genotype observation projection shall deterministically surface caller-emitted, record-scoped genotype evidence from an annotated VCF.

The projection surface is:

```text
record-scoped
```

It is not:

```text
a genome-wide genotype matrix

a reference-confidence surface

a callability surface

an assay-opportunity surface

a coverage-denominator surface

a negative-evidence surface
```

The projection shall emit genotype observations only for records present in the source VCF.

The projection shall not synthesize genotype observations for loci absent from the source VCF.

Absence of a row from `genotype_observations.tsv` shall not be interpreted as:

```text
homozygous reference

variant absence

locus callable

locus not callable

locus not assayed

negative evidence for RDGP

lack of disease relevance
```

---

## Cross-Repository Responsibility Boundary

### VAP responsibility

VAP shall:

```text
surface caller-emitted genotype evidence

preserve raw FORMAT and sample values

preserve source VCF context

preserve sample and run identity

emit deterministic normalized descriptive fields

preserve source-record identity

preserve enough linkage context for VDB

transport genotype observations through TEP-VAP
```

VAP shall not:

```text
infer inheritance

infer carrier state

infer compound heterozygosity

infer de novo status

infer disease causality

infer biological ploidy

infer hemizygosity

infer mitochondrial heteroplasmy
```

### VDB responsibility

VDB shall remain responsible for:

```text
genotype entity registration

persistent genotype storage

variant/genotype topology

cross-entity joins

consumer-facing genotype projections

relationship construction for complex records
```

### RDGP responsibility

RDGP shall remain responsible for:

```text
inheritance reasoning

zygosity-aware prioritization

compound heterozygous reasoning

family-model reasoning

genotype-aware burden interpretation
```

A VAP genotype observation is an observation substrate.

It is not a completed inheritance-reasoning result.

---

## Functional Projection Requirements

The genotype observation projection shall:

```text
consume one annotated VCF

resolve one selected sample

read every readable non-header source record

preserve raw FORMAT and sample fields

extract recognized genotype fields into convenience columns where supported

preserve all raw FORMAT/sample content, including unknown caller-specific FORMAT fields

derive only syntactically supported descriptive fields

emit one record-scoped genotype observation per selected sample per readable source record

emit a structured projection summary

register the output artifact in VAP state

support TEP-VAP transport
```

The projection shall not:

```text
modify the source VCF

modify annotated_variants.tsv

modify Stage 08–13 artifacts

feed genotype evidence into Stage 08–13

split source genotype meaning into synthetic interpretation rows

perform downstream biological inference
```

---

## Required Source Artifact

The authoritative source artifact shall be:

```text
annotated_variants.vcf
```

The source VCF shall:

```text
exist

be a regular readable file

be non-empty

contain a valid VCF header

contain the standard fixed VCF columns

contain a #CHROM header line

contain at least one sample column for genotype-required execution
```

For genotype-required execution, the source VCF shall contain a `FORMAT` column.

If `FORMAT` is absent, the projection shall fail unless operating under a separately governed surveillance-only mode.

The genotype projection shall not use `annotated_variants.tsv` as its source.

---

## Required VAP Runtime Context

The projection shall require:

```text
sample_id

run_id

reference_build

source_pipeline

annotated_vcf_path

output_directory
```

From `output_directory`, the projection shall deterministically resolve:

```text
genotype_observations.tsv

genotype_projection_summary.json

genotype_source_header_context.json
```

An implementation may accept explicit paths for all three artifacts instead
of `output_directory`, but it shall not accept only the genotype TSV path
without also governing the summary and header-context destinations.

The projection should also receive, where available:

```text
SRA accession

sample alias

assay type

normalization policy identifier

annotation engine

config snapshot identity
```

The projection shall preserve the distinction between:

```text
VCF sample-column identity

VAP sample identity

SRA accession

run identity

biological specimen identity
```

These identifiers shall not be assumed to be interchangeable.

---

## Source VCF Header-Context Requirements

FORMAT values shall not be treated as fully interpretable without their source VCF header context.

The projection shall preserve or reference enough source header context to audit:

```text
FORMAT definitions

sample column names

contig declarations

reference declarations

caller or workflow metadata, where available

header context required for caller-specific FORMAT interpretation
```

At minimum, the projection system shall preserve:

```text
source_vcf_path

source_vcf_sha256

source_vcf_header_hash

resolved sample column name

observed FORMAT keys

FORMAT definitions for observed keys, where available
```

The complete VCF header need not be duplicated into every genotype observation row.

A companion header-context artifact or equivalent manifest representation may be used.

---

## VCF Sample Resolution and Identity Mapping

Exactly one VCF sample column shall be selected for one projection execution.

### Single-sample VCF

If exactly one sample column exists:

```text
that sample column may be selected
```

The projection shall record:

```text
vcf_sample_column_name

sample_selection_policy = single_sample_column
```

The selected VCF sample label shall be compared with supplied VAP sample context.

Textual inequality shall not automatically invalidate the mapping if a governed alias or mapping relationship exists.

### Multisample VCF

If multiple sample columns exist:

```text
an explicit sample-selection input or governed mapping shall be required
```

The projection shall not:

```text
select the first sample column automatically

select the last sample column automatically

select the closest textual match

infer the intended sample from position alone
```

### Mapping status

The projection shall emit or register a sample identity mapping status.

Conceptual statuses include:

```text
exact_match

single_column_context_match

explicit_alias_match

explicit_mapping

unresolved

conflicting
```

The final allowed values belong to the schema.

Unresolved or conflicting sample identity shall fail genotype-required execution.

---

## Record-Scoped Surface Semantics

`genotype_observations.tsv` shall represent genotype evidence for source VCF records.

It shall not represent every genomic locus.

It shall not represent loci absent from the VCF.

It shall not create synthetic homozygous-reference rows.

It shall not create synthetic no-call rows for absent records.

It shall not create synthetic negative evidence.

The record-scoped meaning shall remain visible in:

```text
artifact documentation

projection summary

TEP-VAP metadata

consumer contract
```

---

## Source Record Inclusion and Exclusion

For each non-header source VCF record with readable fixed coordinate fields, the projection shall emit one genotype observation row for the selected sample.

The source record shall be preserved even when:

```text
GT is absent

GT is missing

AD is absent

DP is absent

GQ is absent

PL is absent

FT is absent

FORMAT/sample lengths differ

caller-specific fields are unsupported
```

A record may be excluded only when its fixed VCF structure is irreparably malformed such that source coordinate and allele identity cannot be established.

Every excluded record shall be counted and described in the projection summary.

The following invariant shall hold:

```text
source_record_count
=
genotype_observation_row_count
+
irreparably_malformed_record_count
```

For this invariant, `source_record_count` means the number of non-header VCF data lines encountered after global header validation, including records later classified as irreparably malformed. Header lines are not included.

`genotype_observation_row_count` counts emitted genotype-observation rows.

`irreparably_malformed_record_count` counts non-header data lines excluded because coordinate and allele identity could not be established.

---

## Projection Cardinality

For genotype observation specification version 1, the projection shall emit:

```text
one genotype observation row

per selected sample

per readable source VCF record
```

The projection shall preserve source-record cardinality.

The projection shall not split a multiallelic source record into multiple genotype observation rows.

Example:

```text
REF=A
ALT=C,G
GT=1/2
```

shall remain one genotype observation preserving:

```text
source_record_ref = A

source_record_alt = C,G

gt_raw = 1/2

called_allele_indices = 1,2
```

A future relationship layer may associate this genotype observation with multiple allele-specific variant observations.

---

## FORMAT and Sample-Field Parsing

The projection shall preserve:

```text
FORMAT exactly as emitted

selected sample field exactly as emitted
```

The projection shall parse FORMAT/sample values positionally.

Conceptual algorithm:

```text
format_keys = FORMAT split by ":"

sample_values = sample field split by ":"

map each format key to the sample value at the same index
```

### Equal-length vectors

When key and value counts are equal:

```text
the mapping shall be treated as structurally aligned
```

### Sample values shorter than FORMAT keys

The projection shall:

```text
preserve available values

represent trailing values as explicitly missing

mark the record as incomplete sample-value alignment
```

### Sample values longer than FORMAT keys

The projection shall:

```text
preserve the raw sample string

preserve unmatched trailing values where possible

mark the record as malformed FORMAT/sample alignment
```

The projection shall not silently discard unmatched values.

### FORMAT absent or missing

If FORMAT is absent at the file level during genotype-required execution:

```text
the projection shall fail
```

If FORMAT is present as a column but missing for one record:

```text
the record shall be preserved

the record shall receive an explicit missing-FORMAT status
```

---

## Raw Evidence Preservation

The projection shall preserve the following fields exactly when present:

```text
FORMAT

sample field

GT

AD

DP

GQ

PL

FT
```

The projection shall also preserve caller-specific FORMAT content.

Unknown FORMAT keys shall not be discarded.

Raw caller evidence shall remain authoritative.

Normalized descriptive fields shall remain additive.

The raw evidence shall remain sufficient to audit every normalized field.

---

## GT Structural Parsing

The projection shall preserve:

```text
gt_raw

allele tokens

separator structure

called allele indices

missing allele positions

phase notation
```

The projection may derive only syntactically supported structural descriptions.

The projection shall not infer biological meaning requiring external context.

---

## GT-Arity Semantics

The projection may emit:

```text
gt_arity
```

`gt_arity` shall mean:

```text
the number of allele positions represented in the raw GT structure
```

Examples:

```text
GT=0/1
gt_arity=2

GT=1/1
gt_arity=2

GT=0|1
gt_arity=2

GT=1
gt_arity=1

GT=./.
gt_arity=2

GT=1/2
gt_arity=2

GT=0/1/2
gt_arity=3
```

`gt_arity` shall not be represented as biological ploidy.

The projection shall not infer:

```text
sample sex

chromosome-specific ploidy

hemizygosity

copy-number state

mitochondrial ploidy

inheritance mode
```

from GT arity alone.

---

## Phase-State Semantics

The projection may derive phase state from GT separators.

Conceptual behavior:

```text
GT contains only "|"
    phased

GT contains only "/"
    unphased

GT contains no separator and one allele token
    not_applicable

GT contains mixed separators
    malformed_or_complex

GT absent or unparseable
    unknown
```

The raw GT shall always remain authoritative.

A phased separator shall not imply inherited phase, parental phase, or compound-heterozygous phase.

---

## Genotype Call-State Normalization

The projection may emit a deterministic call-state label.

Safe conceptual categories include:

```text
homozygous_reference_call

heterozygous_call

homozygous_alternate_call

alternate_alleles_differ

single_allele_reference_call

single_allele_alternate_call

partial_no_call

complete_no_call

unparseable
```

`single_allele_reference_call` and `single_allele_alternate_call` describe GT structure with one allele position. They do not establish biological haploidy, hemizygosity, chromosome-specific ploidy, sample sex, inheritance mode, or copy-number state.


The final enum belongs to the schema.

The projection shall not emit biologically interpretive labels such as:

```text
carrier

hemizygous

compound_heterozygous

de_novo

inherited

heteroplasmic
```

A call-state label describes caller-emitted GT structure for a source record.

It does not establish genome-wide state.

---

## AD Handling

The projection shall preserve `AD` exactly when present.

The projection may parse AD as an ordered depth vector.

For a biallelic record:

```text
AD[0]
    reference depth

AD[1]
    alternate depth
```

For a multiallelic record:

```text
AD[0]
    reference depth

AD[1:]
    alternate-allele depth vector
```

The projection shall not collapse a multiallelic AD vector into one alternate-depth scalar.

A scalar alternate depth may be emitted only when exactly one alternate allele exists and the AD vector is structurally compatible.

Allele depth alone shall not be interpreted as:

```text
heteroplasmy

mosaicism

allelic imbalance

copy-number state
```

---

## DP Handling

The projection shall preserve sample-level `FORMAT/DP` exactly when present.

The projection may parse it as an integer when syntactically valid.

The projection shall not silently substitute:

```text
INFO/DP
```

for:

```text
FORMAT/DP
```

These evidence fields shall remain distinct.

---

## GQ Handling

The projection shall preserve `GQ` exactly when present.

The projection may parse it numerically when syntactically valid.

The projection shall not classify GQ into high, medium, or low confidence unless a later governed policy explicitly defines such thresholds.

---

## PL Handling

The projection shall preserve the complete `PL` vector exactly when present.

The projection shall not collapse PL into a single scalar.

The projection shall not interpret PL ordering without accounting for:

```text
allele cardinality

GT arity

VCF conventions

caller behavior
```

The raw vector shall remain authoritative.

---

## Site and Sample Filter Semantics

The projection shall preserve site-level VCF `FILTER`.

The projection shall preserve sample-level `FORMAT/FT` when present.

These fields shall remain distinct.

The projection shall not treat:

```text
site FILTER = PASS
```

as equivalent to:

```text
sample FT = PASS
```

The projection shall not reinterpret filter values beyond deterministic source preservation unless governed later.

---

## Missingness and No-Call Semantics

The projection shall distinguish three missingness layers.

### Artifact-level missingness

Examples:

```text
source VCF absent

header absent

FORMAT column absent

sample column absent
```

These conditions may cause projection failure.

### Record-level structural missingness

Examples:

```text
FORMAT = .

sample field = .

GT absent from FORMAT

GT value empty

FORMAT/sample length mismatch
```

These conditions shall usually preserve the source record with explicit status.

### GT call missingness

Examples:

```text
GT = .

GT = ./.

GT = .|.

GT = 0/.

GT = .|1
```

These forms shall preserve raw GT and receive distinct deterministic classification where possible.

The projection shall not collapse all missingness into one generic state.

The projection shall not rewrite missing or no-call GT as homozygous reference.

---

## Multiallelic Record Semantics

Multiallelic source records shall remain source-faithful.

The projection shall preserve:

```text
source_record_ref

source_record_alt

alternate allele count

called allele indices

raw GT

raw AD

raw PL
```

The projection shall not fabricate a single allele-specific variant relationship when the genotype observation refers to multiple alternate alleles.

Complex linkage shall be marked explicitly and deferred to VDB relationship construction.

---

## Source VCF and Source-Record Identity

The projection shall preserve:

```text
source_vcf_path

source_vcf_sha256

source_vcf_header_hash

source record ordinal or line number

source_record_hash
```

`source_record_hash` shall be defined as:

```text
SHA-256 of the exact decompressed logical VCF data-line bytes
excluding the terminal line ending
```

Equivalent logical VCF records in `.vcf` and `.vcf.gz` representations should therefore produce the same source-record hash.

`source_record_hash` identifies the source record.

It is not a coordinate-normalized variant identity.

A future coordinate handle may be defined separately.

---

## Variant-Observation Relationship Status

The projection shall preserve enough identity for VDB to construct variant/genotype relationships without inference from opaque fields.

For straightforward normalized biallelic records, the projection may emit a direct relationship using:

```text
reference_build

chromosome

position

reference_allele

alternate_allele

variant_id
```

Direct `variant_id` linkage shall be emitted only when unambiguous under the declared VAP variant identity policy.

For multiallelic, split-normalized, multisample, or otherwise complex records:

```text
direct linkage shall not be fabricated
```

The projection shall preserve source-record identity and emit a relationship status indicating that direct linkage is:

```text
complex

deferred

unresolved
```

The final enum belongs to the schema.

---

## Output Artifact Requirements

The canonical record-level artifact shall be:

```text
processed/genotype_observations.tsv
```

The artifact shall be:

```text
deterministic

UTF-8 encoded

tab-delimited

source-order preserving

sample-aware

run-aware

assembly-aware

source-traceable

checksum-addressable

suitable for TEP-VAP transport

suitable for VDB registration
```

The artifact shall not replace:

```text
annotated_variants.vcf

annotated_variants.tsv

stage_08_vdb_ready_variants.tsv
```

---

## Projection Summary Requirements

The projection shall emit:

```text
processed/genotype_projection_summary.json
```

The summary shall include at least:

```text
projection status

source VCF path

source VCF SHA256

source VCF header hash

resolved VCF sample column

sample selection policy

sample identity mapping status

sample_id

run_id

reference_build

source record count

genotype observation row count

irreparably malformed record count

GT present count

GT absent count

complete no-call count

partial no-call count

AD present count

DP present count

GQ present count

PL present count

multiallelic record count

phased GT count

unphased GT count

malformed GT count

FORMAT/sample mismatch count

projection warning count
```

The summary is an audit artifact.

It is not a substitute for record-level genotype observations.

---

## Determinism Requirements

Equivalent source inputs and equivalent runtime context shall produce byte-identical output artifacts.

Determinism shall include:

```text
source-order row emission

stable column order

UTF-8 encoding

tab delimiters

newline convention

null representation

Boolean representation

numeric rendering

source-record hash behavior

header-context hash behavior

summary key semantics
```

Determinism supports:

```text
VDB idempotent registration

stable lineage

repeatable TEP-VAP emission

reproducible RDGP projections
```

---

## Idempotency and Overwrite Rules

If the output does not exist:

```text
the projection shall create it
```

If the output exists and deterministic regeneration is byte-identical:

```text
the projection may report idempotent success
```

If the output exists and differs:

```text
the projection shall fail unless explicit overwrite is authorized
```

The projection shall not silently replace an existing genotype artifact.

Backfill and future pipeline execution shall use the same overwrite semantics.

---

## Projection-Level Failure Conditions

The projection shall fail genotype-required execution when:

```text
source VCF is absent

source VCF is unreadable

VCF header is missing

required fixed columns are missing

FORMAT column is absent

no sample column exists

expected sample cannot be resolved

multiple samples exist without explicit selection policy

sample identity mapping is conflicting or unresolved

required VAP runtime context is absent

source checksum cannot be calculated

output cannot be written deterministically

fatal global parsing inconsistency occurs
```

---

## Record-Level Warning and Preservation Conditions

A source record should still be emitted with explicit status when:

```text
GT is absent

GT is missing

AD is absent

DP is absent

GQ is absent

PL is absent

FT is absent

FORMAT/sample lengths differ

caller-specific fields are unsupported

GT is malformed

sample values contain trailing missing entries
```

Optional field absence shall not cause silent record deletion.

---

## Run-State Registration Requirements

Future VAP execution shall register the complete genotype artifact set:

```text
state["artifacts"]["genotype_observations"]

state["artifacts"]["genotype_projection_summary"]

state["artifacts"]["genotype_source_header_context"]
```

The projection shall also register:

```text
state["qc"]["genotype_projection_qc"]

state["stage_outputs"]["genotype_observation_projection"]
```

Equivalent state locations may be used only if they:

```text
preserve all three artifact identities

preserve the non-numbered projection identity

remain compatible with current VAP state handling

permit Stage 13 and TEP-VAP construction to discover
the complete genotype artifact set
```

The projection shall not be represented as a replacement for Stage 07 or
Stage 08.

---

## TEP-VAP Registration and Lineage

A genotype-enabled TEP-VAP shall include the complete canonical genotype
artifact set:

```text
entities/genotype/genotype_observations.tsv

entities/genotype/genotype_projection_summary.json

entities/genotype/genotype_source_header_context.json
```

The three artifacts form one contract-governed genotype observation package.

A partial artifact set is not a conformant genotype-enabled TEP-VAP.

The TEP-VAP shall preserve or reference source VCF header context sufficient to interpret retained FORMAT fields.

TEP integration shall update:

```text
entity_inventory.json

lineage_manifest.json

validation_report.md

artifact checksums

package manifests where applicable
```

The genotype entity shall be represented as:

```text
entity_domain = genotype

entity_role = genotype_observation

source_stage = genotype_projection

source_artifact_role = caller_emitted_genotype_observations
```

Required lineage shall record:

```text
annotated_variants.vcf
    → genotype_observations.tsv
```

Parallel lineage shall record:

```text
annotated_variants.vcf
    → annotated_variants.tsv
```

The TEP-VAP shall not imply:

```text
annotated_variants.tsv
    → genotype_observations.tsv
```

because genotype observations are projected directly from the annotated VCF.

The full source VCF need not be transported inside the TEP-VAP if the package preserves:

```text
source VCF path

source VCF checksum

source VCF header hash

sample-column identity

FORMAT definitions used

source-record hashes
```

A source VCF path alone is not a portable audit reference. If the full source VCF is not transported inside TEP-VAP, the package shall preserve enough portable source context for VDB to audit genotype observations without relying on an operator-local filesystem path.

At minimum, this should include:

```text
source_vcf_sha256

source_vcf_header_hash

observed FORMAT definitions or a header-context artifact

resolved sample-column identity

source-record hashes

source artifact location or cold-storage/recovery reference, where available
```

The source path may be preserved as provenance, but it shall not be the only retained evidence needed to interpret FORMAT/sample genotype fields.

---

## Canonical-Run Backfill Requirements

The 13-run canonical backfill shall:

```text
use retained annotated VCFs

invoke the canonical genotype projection implementation

emit processed/genotype_observations.tsv

emit processed/genotype_projection_summary.json

emit processed/genotype_source_header_context.json

transport all three artifacts into TEP-VAP

update inventory

update lineage

rerun validation

write run-external receipts
```

The backfill shall not:

```text
rerun variant calling

rerun normalization

rerun annotation

modify Stage 08–13 outputs

use an independent parser

silently overwrite conflicting genotype outputs
```

The backfill receipts shall be written outside immutable run results, such as:

```text
/root/Desktop/
```

The receipt bundle should include:

```text
per-run status

source VCF checksum

source header hash

source record count

output row count

output checksum

GT/AD/DP/GQ/PL availability counts

missingness distributions

sample mapping status

TEP registration status

lineage status

validation status

non-interference checksum results
```

---

## Future Automatic-Emission Requirements

Future eligible VAP executions shall automatically emit:

```text
processed/genotype_observations.tsv

processed/genotype_projection_summary.json

processed/genotype_source_header_context.json
```

Future TEP-VAP generation shall automatically transport:

```text
entities/genotype/genotype_observations.tsv

entities/genotype/genotype_projection_summary.json

entities/genotype/genotype_source_header_context.json
```

The future execution path and canonical-run backfill shall invoke the same canonical genotype projection implementation.

Independent parsing behavior shall not be introduced.

---

## Non-Interference Requirements

Genotype observation surfacing shall not change:

```text
raw VCF content

normalized VCF content

annotated VCF content

annotated_variants.tsv content

Stage 08 row counts

Stage 08 column sets

Stage 09 outputs

Stage 10 outputs

Stage 11 outputs

Stage 12 outputs

Stage 13 scientific summaries

existing TEP-VAP variant entities and their scientific contents
```

For canonical-run backfill, pre-patch and post-patch checksums shall be compared for pre-existing scientific evidence artifacts.

Expected additive changes are limited to:

```text
processed/genotype_observations.tsv

processed/genotype_projection_summary.json

TEP genotype artifacts

entity inventory

lineage manifest

validation report

package or artifact manifests

future run-state metadata
```

Manifest changes shall be additive.

Existing variant entities shall not be rewritten except for additive cross-reference metadata explicitly permitted by a later contract.

---

## Downstream Interpretation Restrictions

A genotype observation shall not, by itself, establish:

```text
inheritance mode

carrier status

compound heterozygosity

de novo status

hemizygosity

biological ploidy

mitochondrial heteroplasmy

disease causality

genome-wide homozygous-reference state

negative evidence
```

A heterozygous call shall not establish carrier status.

Two heterozygous calls in one gene shall not establish compound heterozygosity.

A single-allele GT structure shall not establish haploidy, hemizygosity, sample sex, chromosome-specific ploidy, or copy-number state.

Allele depth shall not establish heteroplasmy or mosaicism.

Absence of a genotype-observation row shall not establish homozygous reference, variant absence, callability, assay opportunity, or negative RDGP evidence.

These conclusions require additional governed evidence and belong downstream.

---

## Unsupported and Deferred Cases

The initial implementation may explicitly support:

```text
single-sample annotated VCFs

current canonical VAP caller output

record-faithful biallelic and multiallelic preservation

standard GT/AD/DP/GQ/PL/FT parsing
```

The initial implementation may defer full support for:

```text
multisample projection

polyploid-specific interpretation

copy-number-aware genotype semantics

gVCF reference-confidence blocks

family-aware projection

opportunity and callability surfaces

coverage-denominator surfaces

complete variant/genotype link artifacts

caller-specific biological interpretation
```

Unsupported complexity shall be detected and reported.

It shall not be silently flattened.

---

## Acceptance Conditions

An implementation satisfies this specification when it demonstrates:

```text
deterministic projection

one output row per selected sample per readable source record

raw FORMAT and sample-field preservation

recognized FORMAT extraction without unknown-field loss

source VCF and header-context preservation

explicit VCF sample-column identity

explicit VAP sample/run mapping

GT arity without biological ploidy inference

record-scoped absence semantics

multiallelic source-faithful preservation

conditional direct variant linkage

required projection summary emission

additive processed-output emission

additive TEP-VAP transport

inventory and lineage registration

canonical-run backfill reuse

future automatic-emission readiness

unchanged variant-centric outputs

VDB registration without producer-identity inference

RDGP-ready observation substrate without inheritance overreach
```

---

## Final Specification

VAP shall preserve caller-emitted genotype evidence.

VAP shall surface that evidence as a first-class, record-scoped genotype observation domain.

VAP shall preserve raw evidence, source context, sample identity, run identity, and source-record identity.

VAP shall describe only what is syntactically determinable.

VAP shall not infer biological ploidy, inheritance, carrier state, compound heterozygosity, hemizygosity, heteroplasmy, or disease causality.

VAP shall preserve enough identity and provenance for VDB to register genotype observations and their relationships without fabricating source meaning.

VDB shall preserve and relate genotype evidence.

RDGP shall remain responsible for downstream genotype-aware reasoning.
