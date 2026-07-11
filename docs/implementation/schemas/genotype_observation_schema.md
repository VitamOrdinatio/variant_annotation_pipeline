# Genotype Observation Schema

## Purpose

This document defines the canonical physical and semantic schema for VAP genotype observation artifacts.

It translates the certified genotype observation architecture, design, and specification into concrete artifact shapes that remain coherent across:

```text
VAP
    ↓
TEP-VAP
    ↓
VDB
    ↓
RDGP
```

This schema freezes:

```text
canonical artifact set

TSV field set and field order

JSON artifact structure

null and Boolean semantics

logical data types

controlled vocabularies

identity fields

provenance fields

relationship fields

cross-artifact invariants

schema versioning
```

This schema does not define:

```text
Python function signatures

CLI syntax

backfill orchestration

SQLite DDL

VDB physical persistence

RDGP inheritance logic

validation thresholds
```

Those concerns belong to the genotype observation contract, implementation plan, and validation documents.

---

## Relationship to Certified Sister Documents

The certified architecture defines:

```text
why genotype observation exists

where it belongs

which authority boundaries apply

which cross-repository invariants must remain true
```

The certified design defines:

```text
the parallel projection model

component responsibilities

artifact movement

TEP-VAP integration

backfill and future-execution reuse
```

The certified specification defines:

```text
mandatory projection behavior

record inclusion

sample resolution

raw evidence preservation

normalization limits

failure semantics

downstream interpretation restrictions
```

This schema defines the required artifact shape that implements those decisions.

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

---

## Schema Scope

This schema governs three canonical artifacts:

```text
processed/genotype_observations.tsv

processed/genotype_projection_summary.json

processed/genotype_source_header_context.json
```

The corresponding TEP-VAP paths are:

```text
entities/genotype/genotype_observations.tsv

entities/genotype/genotype_projection_summary.json

entities/genotype/genotype_source_header_context.json
```

The genotype observation surface is record-scoped.

It represents genotype evidence for source VCF records present in the annotated VCF.

It is not:

```text
a genome-wide genotype matrix

a reference-confidence matrix

a callability surface

an assay-opportunity surface

a negative-evidence surface
```

---

# Canonical Artifact Set

## Record-Level Artifact

```text
genotype_observations.tsv
```

Purpose:

```text
one source-faithful genotype observation
per selected sample
per readable source VCF record
```

## Projection Summary Artifact

```text
genotype_projection_summary.json
```

Purpose:

```text
deterministic audit summary

projection metrics

sample-resolution status

source identity

output identity

cross-artifact count invariants
```

## Source Header Context Artifact

```text
genotype_source_header_context.json
```

Purpose:

```text
portable VCF header context

FORMAT definitions

sample-column declarations

reference declarations

contig declarations

caller/workflow metadata

source header identity
```

The header-context artifact exists because source VCF paths alone are not portable audit references.

---

# Serialization Conventions

## Encoding

All artifacts shall use:

```text
UTF-8
```

No byte-order mark shall be emitted.

## TSV Delimiter

`genotype_observations.tsv` shall use:

```text
tab
```

as the field delimiter.

## Newlines

All text artifacts shall use:

```text
LF
```

line endings.

## TSV Header

The first line of `genotype_observations.tsv` shall contain the canonical field names in the exact order defined by this schema.

## Null Semantics

The canonical VAP-level null token shall be:

```text
NA
```

`NA` means:

```text
not available

not applicable

not emitted by policy

not derivable under the governed schema
```

Literal VCF missing-value syntax shall remain preserved in raw fields.

Examples:

```text
gt_raw = .

gt_raw = ./.

sample_format_raw = .

ad_raw = .
```

The projection shall not rewrite literal source `.` values to `NA` in raw fields.

Derived or contextual fields may use `NA`.

## Boolean Semantics

Canonical TSV Boolean values shall be:

```text
True

False
```

Boolean fields shall not use:

```text
1

0

yes

no

TRUE

FALSE
```

## List-Field Semantics

TSV list-like fields shall use deterministic delimiters.

Comma-delimited fields preserve source or structural order:

```text
called_allele_indices
alt_depths_raw
alternate_alleles_raw
```

Semicolon-delimited fields preserve deterministic lexical order unless otherwise specified:

```text
projection_warning_codes
unknown_format_fields
```

List fields shall not contain spaces after delimiters.

If no values are available, the field shall be `NA`.

If a list value can contain a reserved delimiter, the value shall be percent-encoded according to the field-specific encoding policy.


## Numeric Semantics

Parsed numeric convenience fields shall use base-10 canonical rendering without thousands separators.

Integer-valued fields shall not contain decimal points.

Invalid or unavailable parsed numeric values shall be:

```text
NA
```

while the corresponding raw source field remains preserved.

## Deterministic Ordering

`genotype_observations.tsv` row order shall match source VCF data-record order.

JSON object keys shall be emitted in deterministic lexical order.

Controlled-list values shall use the ordering rules defined in this schema.

Volatile timestamps shall not appear in deterministic scientific artifacts.

Execution timestamps may appear only in separate non-deterministic operational logs.

---

# genotype_observations.tsv

## Row Cardinality

Version 1 shall emit:

```text
one row

per selected sample

per readable source VCF data record
```

Multiallelic source records shall remain unsplit.

The row represents the source genotype record, not one alternate-allele projection.

## Canonical Column Order

The exact v1 column order shall be:

```text
schema_version
genotype_observation_id
genotype_observation_id_version
entity_type
evidence_class

sample_id
sample_alias
sra_accession
run_id
vcf_sample_column_name
sample_selection_policy
sample_identity_mapping_status
source_pipeline
assay_type

source_vcf_path
source_vcf_sha256
source_vcf_header_hash
source_record_ordinal
source_line_number
source_record_hash

reference_build
chromosome
position
reference_allele
alternate_alleles_raw
alternate_allele_count
alternate_allele
is_multiallelic
normalization_policy_id
normalization_state

variant_relationship_status
variant_id
variant_observation_id
relationship_reason

format_raw
sample_format_raw
format_key_count
sample_value_count
format_alignment_status
unknown_format_fields

gt_raw
ad_raw
dp_raw
gq_raw
pl_raw
ft_raw

gt_status
gt_arity
gt_separator
phase_state
called_allele_indices
missing_allele_count
genotype_call_state
is_no_call
is_partial_no_call

ref_depth
alt_depth
alt_depths_raw
dp_value
gq_value
pl_value_count

site_filter_raw
sample_filter_raw

record_parse_status
record_preservation_status
projection_warning_codes
```

---

## Schema and Entity Identity Fields

### schema_version

Required value:

```text
genotype_observation_v1
```

### genotype_observation_id

Logical type:

```text
lowercase hexadecimal SHA-256 string
```

Construction:

```text
SHA-256 over the UTF-8 bytes of:

genotype_observation_id_version
|
run_id
|
vcf_sample_column_name
|
source_vcf_sha256
|
source_record_ordinal
|
source_record_hash
```

`source_record_ordinal` is included to prevent identity collision if two source VCF data lines are byte-identical within the same source artifact.

The identity is sample-scoped, run-scoped, source-record-occurrence-scoped, and producer-scoped.

It is not a universal biological genotype identity.

### genotype_observation_id_version

Required value:

```text
genotype_observation_id_v1
```

### entity_type

Required value:

```text
genotype_observation
```

### evidence_class

Required value:

```text
caller_emitted_sample_genotype
```

---

## Sample and Run Identity Fields

Required:

```text
sample_id
run_id
vcf_sample_column_name
sample_selection_policy
sample_identity_mapping_status
source_pipeline
```

Nullable enrichment:

```text
sample_alias
sra_accession
assay_type
```

Allowed `sample_selection_policy` values:

```text
single_sample_column
explicit_sample_name
explicit_sample_index
explicit_mapping
```

Allowed successful `sample_identity_mapping_status` values:

```text
exact_match
single_column_context_match
explicit_alias_match
explicit_mapping
```

`unresolved` and `conflicting` are projection failures and shall not appear in successful rows.

---

## Source VCF Identity Fields

Required:

```text
source_vcf_path
source_vcf_sha256
source_vcf_header_hash
source_record_ordinal
source_record_hash
```

`source_record_ordinal` is a 1-based ordinal among non-header source records.

`source_line_number` is optional physical provenance.

`source_record_hash` shall be:

```text
SHA-256 of the exact decompressed logical VCF data line
excluding the terminal line ending
```

---

### source_vcf_header_hash

`source_vcf_header_hash` shall be:

```text
SHA-256 of the exact decompressed logical VCF header block
including all header lines before the first data record
excluding terminal file-level line-ending ambiguity
```

Implementations should canonicalize line endings to LF before hashing the header block unless a later contract explicitly chooses a different policy.

The header hash identifies the source header context used to interpret FORMAT fields. It is not a full source VCF checksum and is not a coordinate or genotype identity.

---

## Coordinate and Allele Fields

Required:

```text
reference_build
chromosome
position
reference_allele
alternate_alleles_raw
alternate_allele_count
is_multiallelic
```

`alternate_allele` is populated only when exactly one ALT exists.

For multiallelic records:

```text
alternate_allele = NA
```

`normalization_policy_id` and `normalization_state` may be `NA` when unavailable.

---

## Variant-Relationship Fields

Required:

```text
variant_relationship_status
```

Allowed values:

```text
direct
complex
deferred
unresolved
```

For `direct` relationships:

```text
variant_id
alternate_allele
```

shall be non-null.

For non-direct relationships:

```text
variant_id = NA
```

Recommended `relationship_reason` values:

```text
biallelic_direct_match
multiallelic_source_record
split_normalization_relationship_deferred
variant_observation_id_unavailable
identity_context_incomplete
```

`variant_id` is the producer-side coordinate/allele convenience identifier used for direct run-scoped joins when unambiguous.

`variant_observation_id` is the stable identifier of the corresponding VAP variant-observation entity when such an identifier is available in the TEP-VAP package.

For `variant_relationship_status = direct`:

```text
variant_id != NA
alternate_allele != NA
alternate_allele_count = 1
```

`variant_observation_id` should be populated when available. It may be `NA` when the corresponding variant-observation entity does not yet expose a stable identifier, provided the decomposed coordinate and allele fields remain sufficient for VDB to reconstruct the relationship without inference.

---

## Raw FORMAT and Sample Fields

Required:

```text
format_raw
sample_format_raw
format_key_count
sample_value_count
format_alignment_status
```

Allowed `format_alignment_status` values:

```text
aligned
sample_values_shorter
sample_values_longer
format_missing
sample_field_missing
malformed
```

`unknown_format_fields` shall preserve unknown FORMAT key/value pairs in source order as deterministic semicolon-delimited `key=value` pairs.

Reserved characters shall be percent-encoded.

### unknown_format_fields Encoding Policy

`unknown_format_fields` shall preserve unknown FORMAT key/value pairs in
source FORMAT order.

Pairs shall be serialized as:

```text
key=value;key=value
```

The following bytes are reserved and shall be percent-encoded:

```text
%       → %25
;       → %3B
=       → %3D
TAB     → %09
CR      → %0D
LF      → %0A
```

Encoding shall operate over the UTF-8 byte representation of the key or
value.

Percent-encoded hexadecimal digits shall use uppercase ASCII characters.

The percent byte shall be encoded before other reserved bytes are
serialized.

No spaces shall be inserted around `=` or `;`.

Example:

```text
source key:
    X;TAG

source value:
    a=b%2

serialized pair:
    X%3BTAG=a%3Db%252
```

If no unknown FORMAT fields exist:

```text
unknown_format_fields = NA
```

The corresponding pytest should assert this exact serialization.

Also clarify the gzip test:

```text
plain and gzipped logical records
    must have equal source_record_hash
```

but

```text
source_vcf_sha256 may differ
because it hashes the physical source artifact
```

Since source_vcf_sha256 participates in genotype_observation_id, the genotype observation IDs of a plain and gzip source are not required to match. The test name already correctly targets logical-record hashes rather than observation IDs.

---

## Recognized Raw FORMAT Fields

Raw string fields:

```text
gt_raw
ad_raw
dp_raw
gq_raw
pl_raw
ft_raw
```

If a key is absent from FORMAT:

```text
field = NA
```

If the key is present with literal source value `.`:

```text
field = .
```

---

## GT Structural Fields

Allowed `gt_status` values:

```text
present_parseable
absent_from_format
missing_value
complete_no_call
partial_no_call
malformed
```

`gt_arity` describes GT structure only.

Allowed `gt_separator` values:

```text
/
|
none
mixed
NA
```

Allowed `phase_state` values:

```text
phased
unphased
not_applicable
malformed_or_complex
unknown
```

Allowed `genotype_call_state` values:

```text
homozygous_reference_call
heterozygous_call
homozygous_alternate_call
alternate_alleles_differ
single_allele_reference_call
single_allele_alternate_call
partial_no_call
complete_no_call
other_parseable_call
unparseable
NA
```

No GT structural field establishes biological ploidy, hemizygosity, sample sex, inheritance, or carrier state.

---

## Depth and Likelihood Convenience Fields

Parsed convenience fields:

```text
ref_depth
alt_depth
alt_depths_raw
dp_value
gq_value
pl_value_count
```

`alt_depth` is populated only for structurally compatible biallelic records.

`dp_value` derives only from FORMAT/DP.

The schema shall not substitute INFO/DP.

The schema shall not interpret PL ordering or collapse the PL vector.

---

## Filter Fields

`site_filter_raw` preserves VCF FILTER.

`sample_filter_raw` preserves FORMAT/FT when present.

These fields remain semantically distinct.

When FORMAT/FT is present:

```text
ft_raw = exact raw FORMAT/FT value
sample_filter_raw = exact raw FORMAT/FT value
```

`ft_raw` preserves the recognized FORMAT field.

`sample_filter_raw` provides the semantic sample-level filter surface for downstream consumers.

When FORMAT/FT is absent:

```text
ft_raw = NA
sample_filter_raw = NA
```

unless a later caller-specific policy defines an alternate sample-level filter source.

---

## Parsing and Preservation Fields

Allowed `record_parse_status` values:

```text
parsed
parsed_with_warnings
malformed_gt_preserved
format_alignment_warning
missing_format_preserved
missing_sample_field_preserved
```

Required `record_preservation_status` value:

```text
preserved_from_source_vcf
```

`projection_warning_codes` shall be a deterministic semicolon-delimited list in lexical order.

Allowed v1 codes include:

```text
missing_gt
missing_ad
missing_dp
missing_gq
missing_pl
missing_ft
missing_format
missing_sample_field
sample_values_shorter_than_format
sample_values_longer_than_format
malformed_gt
unknown_format_fields_present
multiallelic_direct_link_deferred
variant_relationship_unresolved
normalization_policy_unavailable
```

---

# genotype_projection_summary.json

Top-level shape:

```json
{
  "schema_version": "genotype_projection_summary_v1",
  "projection": {},
  "source_vcf": {},
  "sample_resolution": {},
  "counts": {},
  "status_counts": {},
  "warnings": [],
  "outputs": {}
}
```

Required `projection` keys:

```text
projection_version
projection_status
source_pipeline
reference_build
```

Allowed projection statuses:

```text
success
success_with_warnings
failed
```

Required `source_vcf` keys:

```text
path
sha256
header_hash
source_record_count
irreparably_malformed_record_count
```

Required `sample_resolution` keys:

```text
sample_id
run_id
vcf_sample_column_name
sample_selection_policy
sample_identity_mapping_status
```

Required count keys:

```text
genotype_observation_row_count
gt_present_count
gt_absent_count
complete_no_call_count
partial_no_call_count
ad_present_count
dp_present_count
gq_present_count
pl_present_count
multiallelic_record_count
phased_gt_count
unphased_gt_count
malformed_gt_count
format_sample_mismatch_count
projection_warning_count
```

Required invariant:

```text
source_record_count
=
genotype_observation_row_count
+
irreparably_malformed_record_count
```

Required outputs:

```text
genotype_observations_path
genotype_observations_sha256
header_context_path
header_context_sha256
```

The summary shall not contain its own SHA-256 or volatile timestamps.

---

# genotype_source_header_context.json

Top-level shape:

```json
{
  "schema_version": "genotype_source_header_context_v1",
  "source_vcf": {},
  "reference_context": {},
  "sample_columns": [],
  "format_definitions": [],
  "contig_declarations": [],
  "caller_metadata": {}
}
```

Required `source_vcf` keys:

```text
path
sha256
header_hash
```

Required `reference_context` key:

```text
reference_build
```

Optional reference keys:

```text
reference_declaration
reference_fasta_path
reference_fasta_sha256
sequence_dictionary_path
sequence_dictionary_sha256
fasta_index_path
fasta_index_sha256
```

`sample_columns` preserves source #CHROM order.

Each FORMAT definition shall include:

```text
id
number
type
description
raw_header_line
```

Each contig declaration shall include:

```text
id
length
assembly
raw_header_line
```

Caller metadata may include:

```text
source
source_version
command_line
workflow_name
workflow_version
annotation_engine
annotation_assembly
```

Unavailable JSON values shall be `null`.

Array ordering shall be deterministic:

```text
sample_columns
    preserves source #CHROM sample-column order

format_definitions
    preserves source VCF header order for FORMAT declarations

contig_declarations
    preserves source VCF header order for contig declarations

caller_metadata
    uses deterministic lexical key ordering
```

The header-context artifact should preserve source header order where that order reflects the original VCF context.

---

# Cross-Artifact Invariants

The following semantic values shall agree across all three artifacts, even when represented under different physical JSON paths:

```text
TSV source_vcf_sha256
    =
summary.source_vcf.sha256
    =
header_context.source_vcf.sha256

TSV source_vcf_header_hash
    =
summary.source_vcf.header_hash
    =
header_context.source_vcf.header_hash

TSV sample_id
    =
summary.sample_resolution.sample_id

TSV run_id
    =
summary.sample_resolution.run_id

TSV reference_build
    =
summary.projection.reference_build
    =
header_context.reference_context.reference_build

TSV vcf_sample_column_name
    =
summary.sample_resolution.vcf_sample_column_name
```

The TSV row count shall equal:

```text
summary.counts.genotype_observation_row_count
```

Within one TSV:

```text
genotype_observation_id
source_record_ordinal
```

shall each be unique.

When `variant_relationship_status = direct`:

```text
variant_id != NA
alternate_allele != NA
alternate_allele_count = 1
```

Every populated derived field shall remain auditable against raw evidence and header context.

---

# TEP-VAP Paths and Entity Roles

Canonical TEP paths:

```text
entities/genotype/genotype_observations.tsv
entities/genotype/genotype_projection_summary.json
entities/genotype/genotype_source_header_context.json
```

Recommended entity semantics:

```text
entity_domain = genotype
entity_role = genotype_observation
source_stage = genotype_projection
source_artifact_role = caller_emitted_genotype_observations
```

Required lineage:

```text
annotated_variants.vcf
    → genotype_observations.tsv

annotated_variants.vcf header context
    → genotype_source_header_context.json

genotype_observations.tsv
    → genotype_projection_summary.json
```

The lineage shall not imply that genotype observations derive from `annotated_variants.tsv`.

---

# VDB Ingestion Expectations

VDB may rely on this schema to:

```text
register VAP genotype producer identities

preserve source VCF and header identities

resolve sample/run context

preserve raw caller evidence

construct direct variant relationships where declared

defer complex relationships where declared

build genotype-aware consumer projections
```

VDB shall preserve:

```text
genotype_observation_id
source_record_hash
source_vcf_sha256
```

when assigning consumer-side identities.

---

# RDGP Interpretation Guardrails

This schema alone does not establish:

```text
inheritance mode
carrier status
compound heterozygosity
de novo status
hemizygosity
biological ploidy
mitochondrial heteroplasmy
genome-wide homozygous-reference state
negative evidence
```

Genotype fields remain observation substrate.

---

# Schema Evolution and Versioning

Initial versions:

```text
genotype_observation_v1
genotype_projection_summary_v1
genotype_source_header_context_v1
genotype_observation_id_v1
```

A schema-version change is required when:

```text
column order changes

field meaning changes

controlled vocabularies change incompatibly

identity construction changes

null semantics change

Boolean semantics change

hash construction changes

JSON top-level shapes change
```

---

# Examples

## Biallelic Heterozygous Record

Source:

```text
CHROM=1
POS=895427
REF=G
ALT=C
FORMAT=GT:AD:DP:GQ:PL
SAMPLE=0/1:1,3:4:15:72,0,15
```

Expected core fields:

```text
alternate_allele_count = 1
alternate_allele = C
is_multiallelic = False
variant_relationship_status = direct
gt_raw = 0/1
gt_status = present_parseable
gt_arity = 2
gt_separator = /
phase_state = unphased
called_allele_indices = 0,1
missing_allele_count = 0
genotype_call_state = heterozygous_call
is_no_call = False
is_partial_no_call = False
ad_raw = 1,3
ref_depth = 1
alt_depth = 3
alt_depths_raw = 3
dp_raw = 4
dp_value = 4
gq_raw = 15
gq_value = 15
pl_raw = 72,0,15
pl_value_count = 3
```

## Complete No-Call

```text
GT=./.
gt_status = complete_no_call
gt_arity = 2
called_allele_indices = NA
missing_allele_count = 2
genotype_call_state = complete_no_call
is_no_call = True
```

## Partial No-Call

```text
GT=0/.
gt_status = partial_no_call
called_allele_indices = 0
missing_allele_count = 1
genotype_call_state = partial_no_call
is_partial_no_call = True
```

## Single-Allele Alternate Call

```text
GT=1
gt_arity = 1
gt_separator = none
phase_state = not_applicable
called_allele_indices = 1
genotype_call_state = single_allele_alternate_call
```

This does not establish biological haploidy or hemizygosity.

## Multiallelic GT 1/2

```text
REF=A
ALT=C,G
GT=1/2
AD=2,4,7

alternate_alleles_raw = C,G
alternate_allele_count = 2
alternate_allele = NA
is_multiallelic = True
variant_relationship_status = complex
variant_id = NA
called_allele_indices = 1,2
genotype_call_state = alternate_alleles_differ
ref_depth = 2
alt_depth = NA
alt_depths_raw = 4,7
```

## Missing Optional FORMAT Fields

```text
FORMAT=GT:DP
SAMPLE=0/1:14

ad_raw = NA
gq_raw = NA
pl_raw = NA
projection_warning_codes = missing_ad;missing_gq;missing_pl
```

## FORMAT/Sample Length Mismatch

```text
FORMAT=GT:AD:DP:GQ
SAMPLE=0/1:10,4:14

format_key_count = 4
sample_value_count = 3
format_alignment_status = sample_values_shorter
gq_raw = NA
record_parse_status = format_alignment_warning
```

---

# Schema Acceptance Criteria

The schema is satisfied when implementation and validation demonstrate:

```text
exact canonical column order

valid controlled vocabularies

deterministic identity construction

source-record traceability

portable source-header context

raw FORMAT preservation

unknown FORMAT preservation

correct null semantics

correct GT-arity semantics

source-faithful multiallelic representation

conditional direct variant linkage

TSV/summary/header-context parity

unique genotype observation identities

deterministic JSON structure

TEP-VAP path compliance

VDB registration readiness

RDGP guardrail preservation
```

---

# Final Schema Doctrine

Every genotype observation row represents one selected sample on one exact source VCF record.

Every convenience field remains auditable against preserved raw caller evidence.

Every relationship field exposes its certainty.

Every missing value preserves its correct semantic layer.

Every source VCF header context required to interpret FORMAT evidence remains portable through TEP-VAP.

VAP preserves genotype evidence.

VDB registers and relates genotype evidence.

RDGP reasons over genotype evidence only in combination with additional governed context.
