# Genotype Observation Contract

## Purpose

This contract defines the producer and consumer obligations governing
the genotype observation evidence domain introduced into the Variant
Annotation Pipeline (VAP).

It establishes the binding interface between:

```text
VAP
    ↓
TEP-VAP
    ↓
VDB
    ↓
RDGP
```

The architecture defines **why** genotype observations exist, the design
defines **how** they are produced, the specification defines **required
behavior**, the schema defines **artifact shape**, the validation
document defines **how correctness is demonstrated**, and this contract
defines **what each participating system may rely upon and what each
system must preserve**.

## Contract Scope

This contract governs producer guarantees, producer limitations,
transport guarantees, consumer expectations, version compatibility,
identity preservation, provenance preservation, additive integration,
and failure semantics. It does not redefine parsing algorithms, TSV
columns, implementation details, or validation procedures.

## Governing Precedence

```text
Architecture
    ↓
Design
    ↓
Specification
    ↓
Schema
       ├── Validation
       └── Contract
              ↓
       Implementation Plan
              ↓
             Code
```

Validation and contract are complementary authorities.

```text
Validation
    defines how conformance is demonstrated.

Contract
    defines producer and consumer obligations.
```

Neither validation nor contract may weaken the architecture, design,
specification, or schema.

## Contract Parties

### VAP Producer

VAP shall:

- deterministically project genotype observations;
- preserve raw caller evidence;
- preserve source provenance;
- emit schema-conformant artifacts;
- package genotype entities into TEP-VAP;
- validate emitted artifacts.

### TEP-VAP

TEP-VAP shall transport genotype artifacts without reinterpretation.

### VDB

VDB shall preserve producer identities, construct persistent
relationships, and expose consumer query surfaces without altering
producer meaning.

### RDGP

RDGP shall perform downstream biological reasoning using genotype
observations together with additional governed evidence.

## Producer Truth Principle

The genotype artifacts emitted by VAP constitute the authoritative
producer representation of caller-emitted genotype evidence.

Consumers may add:

```text
canonical database identities

indexes

relationship topology

query projections

reasoning annotations
```

Consumers shall not:

```text
overwrite raw producer values

replace producer identity

silently alter producer-declared relationship status

promote derived consumer interpretations into producer truth
```

Producer evidence is immutable.

Consumer interpretation is additive.

## Producer Guarantees

VAP guarantees:

-   deterministic artifact generation
-   one genotype observation per selected sample per readable source VCF
    record
-   preservation of raw FORMAT/sample evidence
-   preservation of source-record identity
-   preservation of source VCF identity and header context
-   explicit sample mapping
-   additive TEP-VAP packaging

Processed artifacts and packaged TEP artifacts shall be byte-identical.

## Producer Non-Guarantees

VAP does not establish:

-   genome-wide genotype completeness
-   homozygous-reference state
-   inheritance mode
-   carrier status
-   compound heterozygosity
-   de novo status
-   biological ploidy
-   hemizygosity
-   heteroplasmy
-   disease causality
-   callability
-   assay opportunity
-   coverage opportunity
-   reference-confidence evidence
-   negative evidence inferred from missing rows

## Canonical Artifact Contract

Required processed artifacts:

```text
processed/genotype_observations.tsv
processed/genotype_projection_summary.json
processed/genotype_source_header_context.json
```

Required packaged artifacts:

```text
entities/genotype/genotype_observations.tsv
entities/genotype/genotype_projection_summary.json
entities/genotype/genotype_source_header_context.json
```

## Artifact-Set Completeness and Atomicity

The three canonical genotype artifacts form one indivisible producer
artifact set.

```text
genotype_observations.tsv

genotype_projection_summary.json

genotype_source_header_context.json
```

A run shall not be represented as genotype-enabled when only a partial
artifact set exists.

The projection implementation shall construct artifacts through temporary
paths and shall publish the canonical filenames only after:

```text
all three artifacts have been created successfully

cross-artifact invariants pass

required checksums have been calculated

the projection summary is complete
```

If publication fails, temporary or partial artifacts shall not be treated
as canonical outputs.

## Identity and Provenance Contract

The following producer identities shall be preserved:

-   genotype_observation_id
-   source_vcf_sha256
-   source_vcf_header_hash
-   source_record_hash
-   source_record_ordinal
-   run_id
-   sample_id
-   reference_build

### Source VCF Header Hash Policy

For genotype observation contract version 1:

```text
source_vcf_header_hash
```

shall be calculated as SHA-256 over the exact decompressed logical VCF
header block after line endings have been canonicalized to LF.

The header block shall include:

```text
all ## metadata lines

the #CHROM header line

one LF terminator after each header line,
including the #CHROM line
```

No data record shall be included.

This policy is mandatory for:

```text
genotype_observation_v1

genotype_projection_summary_v1

genotype_source_header_context_v1
```

## Variant Relationship Contract

When `variant_relationship_status = direct`, VDB may construct direct
relationships.

When the status is `complex`, `deferred`, or `unresolved`, VDB shall
preserve uncertainty and shall not fabricate allele-specific
relationships.

## Consumer Reliance

VDB may rely upon validated schema compliance, deterministic producer
identities, preserved raw evidence, provenance, and explicit
relationship status.

## Consumer Obligations

Consumers shall preserve producer identity, raw genotype evidence,
provenance, schema version, and declared uncertainty.

## Version Compatibility

Initial supported versions:

```text
genotype_observation_v1
genotype_projection_summary_v1
genotype_source_header_context_v1
genotype_observation_id_v1
```

Unsupported versions shall not be silently coerced.

A consumer may preserve an unsupported artifact set for audit, but shall
not register its genotype observations into an active supported schema
without an explicit governed migration.

Version migration shall preserve the original producer artifacts,
producer identities, and source provenance.

## Validation and Certification Dependency

Validation operates at two distinct levels.

### Subsystem Implementation Conformance

The genotype observation implementation may be considered conformant when:

```text
the lightweight genotype pytest suite passes

the existing VAP unit-test suite continues to pass

schema-conformant fixture artifacts are emitted

fixture-based TEP packaging tests pass

fixture inputs and variant-centric artifacts remain unchanged
```

This establishes implementation correctness for the genotype observation
subsystem.

### Production Package Conformance

A production VAP run or TEP-VAP package may be represented as
genotype-enabled only after the applicable integration or backfill
validation confirms:

```text
all three canonical processed artifacts exist

all three canonical TEP-VAP artifacts exist

processed and packaged checksums match

entity inventory registration is complete

lineage registration is complete

TEP validation passes

pre-existing scientific artifacts remain unchanged
```

Lightweight unit validation does not by itself certify a production TEP-VAP.

Producer guarantees apply at the level proven by the corresponding
validation layer.

## Idempotency and Duplicate Handling

Repeated delivery of a genotype artifact set with identical:

```text
schema versions

producer identities

source VCF identity

source-record identities

artifact checksums
```

shall be treated as idempotent.

If the same `genotype_observation_id` is encountered with different
producer content, the conflict shall be treated as a contract violation.

Consumers shall not silently update or replace the existing producer
observation.

## Failure Conditions

Contract violations include:

-   missing required artifacts
-   checksum mismatch
-   schema incompatibility
-   unresolved sample identity
-   conflicting producer identities
-   processed/TEP byte inequality

## Non-Interference Guarantee

Genotype enablement is additive and shall not modify existing Stage
08–13 behavior or variant-centric scientific outputs.

## Deferred Capabilities

Outside the scope of this contract:

-   multisample projection
-   family-aware reasoning
-   copy-number-aware interpretation
-   genome-wide genotype matrices
-   opportunity and callability surfaces

## Final Contract Doctrine

VAP preserves genotype evidence.

TEP-VAP transports genotype evidence.

VDB registers and relates genotype evidence.

RDGP reasons over genotype evidence only in combination with additional
governed evidence.
