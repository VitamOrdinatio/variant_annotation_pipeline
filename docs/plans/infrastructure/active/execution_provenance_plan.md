# Execution Provenance Implementation Plan

**Document Location**

`docs/plans/infrastructure/active/execution_provenance_plan.md`

---

# 1. Purpose

This plan implements the Execution Provenance Contract.

Its purpose is to elevate execution provenance into a first-class infrastructure capability of VAP so that every scientific execution transparently declares, validates, preserves, and transports the computational substrate that produced its biological evidence.

Execution provenance strengthens deterministic reproducibility without altering biological interpretation.

---

# 2. Relationship to Existing Infrastructure

Execution provenance complements—not replaces—existing runtime metadata.

Current infrastructure already preserves:

- configuration snapshot
- runtime profile
- stage summaries
- run fingerprint
- run metadata
- TEP context metadata

Execution provenance introduces a normalized, validated representation of:

- toolchain identity
- annotation environment
- scientific resources

---

# 3. Guiding Principles

Implementation shall satisfy the following principles.

## Single Source of Truth

Execution provenance shall be resolved once.

Downstream stages consume execution provenance rather than rediscovering it.

---

## Scientific Reproducibility

Scientific tools and resources shall be identified by observed runtime identity rather than assumed configuration.

---

## Producer Responsibility

VAP is responsible for declaring the execution substrate that produced its evidence.

VDB shall preserve execution provenance rather than reconstruct it.

---

## Incremental Adoption

Historical execution modes remain supported.

Legacy executions explicitly indicate reduced provenance completeness.

---

# 4. Planned Runtime Architecture

```
Configuration

↓

Pipeline Initialization

↓

Execution Provenance Resolution

↓

Execution Provenance Validation

↓

Execution Provenance Receipt

↓

Pipeline Execution

↓

Run Metadata

↓

TEP Context Transport
```

---

# 5. Execution Provenance Model

Execution provenance consists of:

```
execution_provenance
├── toolchain_environment
├── annotation_environment
└── resource_environment
```

Each component resolves independently.

Each contributes to overall contract status.

---

# 6. Implementation Waves

---

## Wave 1 — Configuration Contract

Objectives

- extend production configuration
- declare expected execution substrate
- validate declared fields

Deliverables

- annotation provenance configuration
- toolchain declarations
- resource declarations

Acceptance

Configuration validation recognizes execution provenance declarations.

---

## Wave 2 — Provenance Resolver

Objectives

Introduce

```
src/execution_provenance.py
```

Responsibilities

- resolve toolchain
- resolve annotation environment
- resolve resource environment
- normalize observations
- emit canonical execution provenance object

Acceptance

Execution provenance can be resolved independently of Stage 07.

---

## Wave 3 — Toolchain Resolution

Resolve

- BWA
- samtools
- GATK
- Java
- Perl
- Python

Capture

- executable
- observed version
- declared version
- contract status

Acceptance

Toolchain contract passes before pipeline execution.

---

## Wave 4 — Annotation Environment

Resolve

- VEP software version
- cache release
- assembly
- species
- cache directory
- executable

Replace banner-only version recording.

Acceptance

Annotation provenance accurately distinguishes software version from cache release.

---

## Wave 5 — Resource Identity

Resolve

- reference FASTA
- FASTA index
- sequence dictionary
- BWA index
- MitoCarta
- Genes4Epilepsy

Capture

- SHA-256
- size
- resolved path
- contract status

Acceptance

Scientific resources possess immutable identities.

---

## Wave 6 — Pipeline Integration

Pipeline initialization resolves execution provenance before Stage 01.

Stage 07 consumes execution provenance.

Stage-local version discovery is removed.

Acceptance

Pipeline contains a single provenance authority.

---

## Wave 7 — Receipt Emission

Emit

```
metadata/execution_provenance.json
```

Update

- run_metadata.json
- metadata.json

Acceptance

Execution provenance becomes permanent run output.

---

## Wave 8 — TEP Transport

Transport

```
execution_provenance.json
```

into

```
entities/context/
```

Update

- entity inventory
- lineage manifest
- validation report

Acceptance

Execution provenance becomes first-class transported context.

---

## Wave 9 — Validation

Expand automated testing.

Validation includes

- version agreement
- resource identity
- failure semantics
- fixture compatibility
- transport integrity

Acceptance

All regression tests pass.

---

## Wave 10 — SYS76 Production Validation

Install production toolchain.

Validate

- execution provenance
- annotation environment
- scientific resources

Execute

ERR10619300

Compare against certified MARK execution.

Acceptance

Execution provenance demonstrates transparent scientific reproducibility across hardware.

---

# 7. Test Strategy

Testing proceeds in three layers.

---

## Unit Tests

Execution provenance resolver

Toolchain parsing

Resource hashing

Annotation environment

---

## Integration Tests

Pipeline initialization

Run metadata

Receipt emission

Fixture execution

---

## End-to-End Validation

ERR10619300

SYS76

Deterministic comparison against certified MARK execution.

---

# 8. Expected Artifacts

New runtime artifact

```
metadata/execution_provenance.json
```

Updated runtime artifacts

```
run_metadata.json

metadata.json

config_snapshot.yaml
```

Updated TEP

```
entities/context/execution_provenance.json
```

---

# 9. Risks

Primary risks

- incorrect version parsing
- legacy fixture compatibility
- platform-specific executable behavior

Mitigations

- centralized resolver
- compatibility modes
- comprehensive regression testing

---

# 10. Success Criteria

Execution provenance implementation is considered complete when:

✓ execution provenance resolves before Stage 01

✓ scientific toolchain is version validated

✓ annotation environment is explicitly preserved

✓ scientific resources possess immutable identities

✓ execution provenance receipt is emitted

✓ run metadata references execution provenance

✓ TEP transports execution provenance

✓ Stage-specific version discovery has been eliminated

✓ historical fixture workflows remain functional

✓ SYS76 execution reproduces the certified MARK scientific outputs with transparent execution provenance.