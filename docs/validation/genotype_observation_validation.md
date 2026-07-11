# Genotype Observation Validation

## Purpose

This document defines the validation strategy for the genotype observation
projection introduced into the Variant Annotation Pipeline (VAP).

Its purpose is to demonstrate that genotype information originating from
the annotated VCF is:

- surfaced without loss,
- preserved faithfully,
- emitted deterministically,
- transported into TEP-VAP,
- and introduced without altering existing variant-centric pipeline behavior.

Validation proves implementation correctness.

It does not redefine architecture, design, specification, or schema.

---

# Relationship to Certified Sister Documents

This validation document follows the certified:

```text
Architecture
    ↓
Design
    ↓
Specification
    ↓
Schema
```

Validation exists to demonstrate that implementation satisfies those
governing documents.

If implementation and documentation disagree, the certified documentation
is authoritative.

---

# Validation Scope

This document defines a lightweight v1 validation strategy centered on automated unit tests.

Validation covers four immediate objectives.

## 1. Genotype Projection Logic

Confirm genotype information is correctly projected from representative annotated VCF fixtures.

## 2. Schema-Conformant Artifact Construction

Confirm genotype observation, projection summary, and source header-context artifacts conform to the certified schema.

## 3. TEP-VAP Packaging Readiness

Confirm genotype artifacts can be transported into the expected TEP-VAP genotype entity paths by unit-tested packaging logic.

## 4. Local Non-Interference Guardrails

Confirm genotype projection does not mutate source VCF fixtures, existing variant-centric TSV fixtures, or unrelated fixture artifacts.

Full pipeline execution, canonical 13-run backfill certification, and Stages 08–13 checksum certification are deferred validation layers.

---

# Validation Strategy

Validation shall use automated pytest unit tests as the primary v1 mechanism.

Manual inspection is reserved for exploratory development and debugging.

The v1 validation target is not full clinical, biological, or corpus-level certification. It is implementation correctness for the genotype observation subsystem against representative fixtures and certified schema expectations.

Repository acceptance for this phase shall be based on repeatable automated unit tests.

---

# Lightweight Validation Boundary

For this validation phase, tests should not require:

```text
full FASTQ-to-TEP pipeline execution

canonical 13-run corpus execution

MARK filesystem access

VDB ingestion

RDGP execution

manual review of complete output packages
```

Tests may use temporary directories and small representative VCF fixtures to exercise:

```text
genotype projection

schema column ordering

summary generation

header-context generation

TEP path packaging logic

checksum-preserving artifact copies

local non-interference against fixture files
```

This keeps validation fast, deterministic, and appropriate for routine pytest execution.

---

# Unit Test Requirements

Unit tests shall validate genotype projection logic independently from
pipeline execution.

Minimum coverage includes:

```text
GT preservation

AD preservation

DP preservation

GQ preservation

PL preservation

FT preservation

FORMAT preservation

unknown FORMAT preservation

GT arity

phase determination

no-call handling

partial no-call handling

multiallelic preservation

deterministic genotype_observation_id generation

schema-compliant column ordering

projection summary generation

header-context generation

record-scoped absence semantics

literal VCF missing-value preservation

NA null-token semantics

single-allele call-state handling without haploid inference

FORMAT/sample length mismatch handling

source-record ordinal and hash behavior

source-header hash behavior

variant relationship status for direct and complex records

portable header-context artifact generation

TEP path packaging without evidence reinterpretation
```

Representative fixtures shall be used.

The validation framework is not required to exhaustively enumerate every
possible VCF genotype state.

---

# Deferred Integration Validation

Full integration validation is deferred from the lightweight v1 validation phase.

A later validation layer should verify that normal VAP execution creates:

```text
processed/genotype_observations.tsv

processed/genotype_projection_summary.json

processed/genotype_source_header_context.json
```

and registers those artifacts correctly within pipeline state.

A later validation layer should also verify that genotype projection is invoked automatically during normal pipeline execution.

These integration checks are not required for the initial lightweight unit-test validation phase.

---

# TEP-VAP Packaging Unit Validation

Lightweight validation shall verify TEP-VAP packaging behavior using temporary test directories and representative genotype artifacts.

Unit tests shall verify that genotype artifacts are copied or staged into:

```text
entities/genotype/
```

The following artifacts are required:

```text
genotype_observations.tsv

genotype_projection_summary.json

genotype_source_header_context.json
```

Unit tests shall verify:

- artifact presence,
- checksum preservation,
- expected TEP path construction,
- byte-identical processed and packaged artifacts.

Full entity inventory registration, lineage manifest registration, and validation report registration may be tested with isolated helper-unit tests if the corresponding builder functions are available.

Complete TEP package certification is deferred to a later integration/backfill validation layer.

---

# Non-Interference Validation

Genotype projection shall not alter existing variant-centric behavior.

For lightweight v1 validation, non-interference shall be tested against representative fixtures.

Unit tests should verify that genotype projection does not mutate:

```text
source annotated VCF fixtures

annotated_variants.tsv fixtures

representative Stages 08–13 fixture artifacts, when provided
```

Expected new or modified artifacts in unit tests are limited to:

```text
processed/genotype_observations.tsv

processed/genotype_projection_summary.json

processed/genotype_source_header_context.json

packaged genotype artifacts under entities/genotype/
```

Full Stages 08–13 checksum comparison for canonical production runs is deferred to later integration or backfill certification.

Unexpected mutation of existing fixture inputs or existing variant-centric fixture outputs constitutes validation failure.

---

# Recommended Pytest Layout

```text
tests/

    test_genotype_projection.py

    test_genotype_projection_schema.py

    test_genotype_projection_summary.py

    test_genotype_projection_header_context.py

    test_genotype_tep_packaging.py

    test_genotype_non_interference.py
```

A later integration phase may add:

```text
tests/

    test_genotype_pipeline_integration.py

    test_genotype_canonical_backfill.py
```

---

# Minimum Test Cases

Recommended minimum automated tests include:

```text
test_biallelic_projection

test_homozygous_reference_projection

test_homozygous_alternate_projection

test_complete_no_call_projection

test_partial_no_call_projection

test_single_allele_call_does_not_emit_haploid_label

test_multiallelic_projection_remains_unsplit

test_unknown_format_preservation

test_literal_vcf_missing_values_preserved_in_raw_fields

test_na_null_semantics_for_derived_fields

test_format_sample_length_mismatch_preserved

test_schema_column_order

test_genotype_observation_id_determinism

test_source_record_ordinal_prevents_duplicate_record_id_collision

test_projection_summary_counts

test_header_context_generation

test_direct_variant_relationship_for_biallelic_record

test_complex_variant_relationship_for_multiallelic_record

test_tep_packaging_paths

test_processed_and_tep_checksums_match

test_projection_does_not_mutate_source_vcf_fixture

test_projection_does_not_mutate_variant_tsv_fixture
```

The validation framework is not required to exhaustively enumerate every possible VCF genotype state.

---

# Deferred Canonical Backfill Certification

Canonical 13-run backfill validation is deferred from the lightweight unit-test phase.

A later validation phase should execute genotype projection against the canonical producer corpus:

```text
12 epilepsy WES runs

1 HG002 WGS run
```

That later phase should certify:

```text
processed genotype artifact generation

TEP genotype artifact transport

projection summaries

header-context artifacts

lineage and inventory registration

non-interference checksums

run-external receipt generation
```

The lightweight v1 validation phase should use representative fixtures rather than the full canonical corpus.

---

# Acceptance Criteria

The lightweight v1 genotype validation phase is considered complete when:

```text
all genotype unit-test suites pass

existing VAP unit tests continue to pass

representative genotype_observations.tsv artifacts are schema-compliant

representative genotype_projection_summary.json artifacts are schema-compliant

representative genotype_source_header_context.json artifacts are schema-compliant

TEP packaging unit tests place genotype artifacts under entities/genotype/

processed and packaged genotype artifacts are byte-identical in unit tests

source VCF and variant-centric fixture artifacts remain unchanged
```

Full pipeline integration, canonical 13-run backfill, and production Stages 08–13 checksum certification remain deferred validation layers.

---

# Final Validation Doctrine

Validation demonstrates that genotype information has been surfaced as a
first-class observation without modifying the existing variant-centric
pipeline.

Successful lightweight validation proves:

- genotype evidence is preserved correctly in representative fixtures;
- genotype artifacts are deterministic and schema-conformant;
- genotype artifacts can be transported byte-for-byte into the expected
  TEP-VAP paths;
- genotype artifacts are structurally ready for later VDB ingestion;
- source and variant-centric fixture artifacts remain unchanged.

It does not by itself certify:

```text
full pipeline integration

a canonical production run

the 13-run backfill corpus

production Stage 08–13 checksum parity

VDB ingestion behavior
```