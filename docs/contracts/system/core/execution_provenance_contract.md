# Execution Provenance Contract

**Document Location**

`docs/contracts/system/core/execution_provenance_contract.md`

---

# 1. Purpose

This contract defines the canonical execution provenance model for the Variant Annotation Pipeline (VAP).

Execution provenance describes the computational substrate under which a VAP run was produced, including:

- software toolchain
- annotation environment
- reference resources
- execution platform
- reproducibility receipts

The purpose of execution provenance is to make every VAP execution scientifically reproducible, operationally auditable, and transportable through downstream consumers including TEP-VAP and VDB.

This contract governs only execution provenance.

It does not redefine biological provenance, semantic provenance, evidence provenance, or variant lineage.

---

# 2. Scope

This contract applies to:

- full_pipeline execution
- annotation_only execution
- post_vep_fixture execution (with defined exceptions)

It governs:

- runtime environment resolution
- version discovery
- resource identity
- contract validation
- provenance receipt emission
- transport into TEP-VAP

---

# 3. Governing Invariant

A VAP execution SHALL NOT begin scientific processing until the required execution provenance has been resolved and validated.

Execution provenance is therefore considered part of pipeline initialization rather than downstream annotation.

---

# 4. Architectural Role

Execution provenance is infrastructure metadata.

It exists independently of:

- sample identity
- genomic observations
- variant interpretation
- biological evidence

Execution provenance describes the environment that produced evidence rather than the evidence itself.

---

# 5. Canonical Execution Provenance Model

Execution provenance SHALL consist of three logical surfaces.

```
execution_provenance
├── toolchain_environment
├── annotation_environment
└── resource_environment
```

Each surface is independently validated.

Each surface contributes to the overall execution provenance contract status.

---

# 6. Toolchain Environment

The toolchain environment describes executable software responsible for pipeline execution.

Required production tools include:

- BWA
- samtools
- GATK
- Java
- Perl
- Ensembl VEP
- Python

Each tool SHALL preserve:

- configured executable
- resolved executable
- observed version
- version parsing status
- contract status

When applicable, declared versions SHALL be compared against observed versions.

---

# 7. Annotation Environment

The annotation environment describes the semantic annotation substrate.

For VEP this SHALL include:

- annotation engine
- observed VEP software version
- declared VEP software version
- observed cache release
- declared cache release
- species
- assembly
- cache location
- offline mode
- resolved executable
- resolved cache directory
- Perl version
- contract status

The software version and cache release SHALL be treated as independent provenance fields.

Example:

```
software_version = 115.2

cache_release = 115
```

These SHALL NOT be conflated.

---

# 8. Resource Environment

The resource environment describes immutable scientific inputs.

Required resources include:

- reference FASTA
- FASTA index
- sequence dictionary
- BWA index
- MitoCarta
- Genes4Epilepsy

Each resource SHALL preserve:

- configured path
- resolved path
- existence
- size
- SHA-256 checksum
- resource role
- contract status

Resource identity SHALL be determined by checksum rather than filename.

---

# 9. Runtime Resolution Contract

Execution provenance SHALL be resolved immediately following pipeline initialization.

The required order is:

```
configuration validation

↓

run directory initialization

↓

state initialization

↓

execution provenance resolution

↓

execution provenance validation

↓

receipt emission

↓

Stage 01
```

Scientific processing SHALL NOT begin until execution provenance has passed validation.

---

# 10. Version Validation

Where declared versions exist, observed versions SHALL be compared against declared versions.

Validation SHALL distinguish:

- exact match
- compatible match
- incompatible version
- unavailable version
- unparsable version

Failures SHALL prevent execution unless explicitly permitted by execution mode.

---

# 11. Resource Validation

Every required scientific resource SHALL satisfy:

- exists
- readable
- checksum successfully computed

Missing required resources SHALL terminate execution.

---

# 12. Execution Modes

## Full Pipeline

Full runtime resolution SHALL be performed.

All contracts SHALL be validated.

---

## Annotation Only

Annotation environment SHALL be validated.

Toolchain validation SHALL include only tools required by the execution mode.

---

## Post-VEP Fixture

Historical producer provenance SHALL be preserved.

Live execution tool probing SHALL NOT be required.

Execution provenance SHALL explicitly indicate:

```
resolution_mode = retained_source_provenance
```

Legacy executions MAY produce partial provenance.

Incomplete historical provenance SHALL be represented explicitly rather than inferred.

---

# 13. Failure Semantics

Execution provenance SHALL distinguish:

- missing
- unavailable
- legacy
- incompatible
- unresolved
- failed validation

Unknown values SHALL NOT be silently replaced with inferred values.

---

# 14. Runtime State Contract

Execution provenance SHALL exist as a first-class runtime object.

```
state

└── execution_provenance
```

Stage-specific code SHALL consume this canonical structure rather than independently discovering software versions.

---

# 15. Receipt Contract

Every successful execution SHALL emit:

```
metadata/execution_provenance.json
```

This receipt SHALL contain:

- toolchain environment
- annotation environment
- resource environment
- validation outcomes
- generation timestamp

This receipt constitutes the authoritative execution provenance artifact.

---

# 16. Run Metadata Contract

`run_metadata.json` SHALL include a summarized execution provenance section.

The complete execution provenance SHALL remain in:

```
metadata/execution_provenance.json
```

to avoid unnecessary duplication.

---

# 17. TEP-VAP Transport Contract

Execution provenance SHALL be transported into TEP-VAP.

The canonical location SHALL be:

```
entities/context/execution_provenance.json
```

Execution provenance SHALL therefore become a first-class transported context artifact.

Entity inventory and lineage manifests SHALL preserve:

- artifact identity
- checksum
- source path
- artifact role

for the transported execution provenance receipt.

---

# 18. Responsibilities

Pipeline initialization SHALL:

- resolve execution provenance
- validate execution provenance
- emit execution provenance receipt

Stage-specific implementations SHALL:

- consume execution provenance
- SHALL NOT independently rediscover execution versions

---

# 19. Backward Compatibility

Historical VAP executions remain valid.

Older runs lacking execution provenance SHALL continue to be consumable.

Legacy executions SHALL explicitly indicate reduced provenance completeness rather than fabricating unavailable information.

---

# 20. Non-Goals

This contract does not:

- containerize VAP
- replace configuration snapshots
- redefine biological provenance
- redefine evidence provenance
- redefine semantic provenance
- guarantee identical wall-clock execution
- guarantee identical timestamps
- replace TEP lineage
- require VDB to infer execution provenance

---

# 21. Acceptance Criteria

Execution provenance implementation is complete when:

- execution provenance is resolved before Stage 01
- required tools are version validated
- required scientific resources are checksum validated
- execution provenance receipt is emitted
- run metadata references the receipt
- TEP-VAP transports execution provenance
- Stage-specific version discovery has been eliminated
- historical execution modes remain functional
- deterministic execution behavior is preserved