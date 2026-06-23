# VAP → VDB TEP Ingestion Interface

## Purpose

This document defines the system interface governing ingestion of VAP Transitional Evidence Products into VDB.

The purpose of this interface is to ensure that VAP-produced evidence enters VDB without loss of:

```text
source identity
sample identity
run identity
variant identity
artifact provenance
evidence lineage
semantic surface structure
validation state
future reinterpretability
```

This interface is not a database schema.

This interface is not a VDB implementation plan.

This interface is the boundary contract between:

```text
VAP
    →
VAP-TEP
    →
VDB
```

---

# 1. Interface Status

```text
Status: Draft v0.1
Owner: DEX-VAP
Producer Authority: VAP
Consumer Authority: VDB
Transport Authority: TEP
```

This document should be treated as a VAP-side system contract for downstream VDB ingestion.

---

# 2. Governing Doctrine

The governing preservation doctrine is:

```text
Stage07 is the preservation anchor.
```

Stage07 represents the last complete biologically interpretable observation surface before VAP applies downstream semantic transformation, routing, interpretation, prioritization, and validation overlays.

Therefore, VDB ingestion MUST NOT treat downstream candidate files as sufficient substitutes for Stage07-derived observation evidence.

Stages08–12 MUST be treated as additive semantic overlays:

```text
Stage07 Observation Entity
    ↓
Stage08 Normalization Entity
    ↓
Stage08 Routing Entity
    ↓
Stage09 Coding Interpretation Overlay
Stage10 Noncoding Interpretation Overlay
    ↓
Stage11 Prioritization Overlay
    ↓
Stage12 Validation Overlay
```

VDB ingestion MUST preserve this topology.

---

# 3. Interface Boundary

## 3.1 VAP Responsibility

VAP owns:

```text
execution
annotation
evidence generation
run-scoped provenance
source artifact creation
source package identity
VAP-TEP construction
```

VAP remains authoritative for VAP-produced evidence.

## 3.2 TEP Responsibility

The VAP-TEP owns transport structure.

The VAP-TEP preserves:

```text
transport identity
source package identity
entity inventory
artifact lineage
provenance topology
semantic topology
validation status
```

The VAP-TEP MUST NOT reinterpret evidence.

## 3.3 VDB Responsibility

VDB owns:

```text
ingestion
durable persistence
namespace brokerage
discovery surfaces
query surfaces
downstream interoperability views
```

VDB MAY normalize, index, broker, and materialize queryable representations.

VDB MUST NOT erase source identities or collapse evidence topology.

---

# 4. Authoritative Transport Input

The authoritative input to this interface is:

```text
VAP-TEP package
```

Raw VAP stage outputs are not the direct ingestion contract unless they are transported as VAP-TEP entities.

A compliant VDB ingestion process MUST use the VAP-TEP lineage manifest as the authoritative inventory of transported entities.

At minimum, VDB ingestion MUST discover:

```text
tep_id
tep_schema_version
source_repository
source_package_id
sample_id
run_id
entity_id
entity_role
source_stage
source_artifact
source_artifact_sha256
row_count
column_count
parent_entities
child_entities
validation_status
```

---

# 5. Required Ingestion Entities

A VDB-compatible VAP-TEP MUST expose the following logical entities.

## 5.1 Observation Entity

```text
Source: Stage07
Role: earliest complete biologically interpretable observation surface
```

VDB MUST preserve this entity as the observation anchor.

Required preservation concepts include:

```text
sample_id
run_id
variant_id
genomic coordinates
reference allele
alternate allele
genotype context
gene mappings
transcript mappings
consequence annotations
population-frequency annotations
clinical annotations
annotation source metadata
```

## 5.2 Normalization Entity

```text
Source: Stage08
Role: semantic normalization surface
```

VDB MUST preserve normalized fields such as:

```text
annotation_source
annotation_version
gene_mapping_status
variant_context
variant_effect_severity
qc_status
interpretability_status
frequency_status
clinical_status
```

## 5.3 Routing Entity

```text
Source: Stage08
Role: deterministic evidence routing surface
```

VDB MUST preserve routing surfaces including, when present:

```text
coding candidates
splice candidates
noncoding candidates
RDGP gene-evidence seed surfaces
VDB-ready variant surfaces
```

Routing surfaces MUST NOT be assumed to be mutually exclusive.

## 5.4 Coding Interpretation Overlay

```text
Source: Stage09
Role: coding-specific interpretation overlay
```

Representative fields include:

```text
functional_impact
coding_interpretation_label
rarity_flag
clinical_evidence
qc_reliability
is_lof_candidate
is_rare_candidate
is_clinically_supported
```

## 5.5 Noncoding Interpretation Overlay

```text
Source: Stage10
Role: noncoding-specific interpretation overlay
```

Representative fields include:

```text
noncoding_functional_context
noncoding_interpretation_label
rarity_flag
clinical_evidence
qc_reliability
is_regulatory_candidate
is_rare_candidate
is_clinically_supported
```

Noncoding evidence MUST be treated as first-class evidence.

## 5.6 Prioritization Overlay

```text
Source: Stage11
Role: prioritization context
```

Representative fields include:

```text
priority_tier
priority_rank
priority_reason
variant_origin
source_interpretation_label
```

Prioritization fields are overlays, not replacements for observation evidence.

## 5.7 Validation Overlay

```text
Source: Stage12
Role: validation-preparation context
```

Representative fields include:

```text
validation_required
validation_priority
suggested_validation_method
validation_reason
```

Validation fields are overlays, not replacements for observation evidence.

## 5.8 Context Sidecar

```text
Source: Stage13 and run metadata
Role: audit and execution context
```

The context sidecar MAY include:

```text
run_metadata.json
runtime_profile.tsv
stage summaries
pipeline summaries
validation summaries
reporting summaries
```

The context sidecar MUST NOT replace primary evidence entities.

---

# 6. Identity Preservation Requirements

VDB ingestion MUST preserve the following source identities:

```text
tep_id
source_repository
source_package_id
sample_id
run_id
variant_id
entity_id
entity_role
source_stage
source_artifact
```

For VAP-derived evidence:

```text
source_repository = VAP
```

The VAP-emitted field:

```text
run_id
```

MAY be persisted by VDB as:

```text
vap_run_id
```

provided the original emitted identity remains recoverable through artifact metadata or provenance records.

VDB MUST NOT regenerate VAP `variant_id` values.

VDB MAY create internal canonical identifiers, but those identifiers are additive and MUST NOT replace source identifiers.

---

# 7. Provenance Preservation Requirements

VDB ingestion MUST preserve provenance sufficient to reconstruct:

```text
source repository
source package
source run
source sample
source artifact
source stage
transport entity
transport package
ingestion event
```

Every ingested entity MUST remain attributable to:

```text
source_artifact
source_artifact_sha256
source_stage
entity_role
tep_id
```

VDB MUST preserve artifact-level checksums.

VDB SHOULD preserve ingestion-time checksums or equivalent integrity records for persisted representations.

---

# 8. Lineage Preservation Requirements

VDB ingestion MUST preserve the VAP-TEP lineage graph.

At minimum, VDB MUST preserve the relationship:

```text
Stage07 Observation Entity
    →
Stage08 Normalization Entity
```

VDB MUST also preserve downstream overlay relationships:

```text
Stage08 Normalization Entity
    →
Stage08 Routing Entity
    →
Stage09 Coding Interpretation Overlay
    →
Stage11 Prioritization Overlay
    →
Stage12 Validation Overlay
```

and:

```text
Stage08 Routing Entity
    →
Stage10 Noncoding Interpretation Overlay
    →
Stage11 Prioritization Overlay
    →
Stage12 Validation Overlay
```

VDB MUST NOT flatten this graph into a single candidate table as the only persisted representation.

---

# 9. Semantic Persistence Expectations

VDB MAY persist VAP-TEP evidence into normalized relational structures.

Expected persistence domains include:

```text
tep_package
source_package
sample
run
variant_entity
variant_observation
annotation
transcript_consequence
gene_mapping
semantic_partition
interpretation_overlay
prioritization_overlay
validation_overlay
provenance_record
lineage_edge
ingestion_event
```

This list is conceptual and does not prescribe exact table names.

The required behavior is preservation of semantic domains, not a specific schema.

---

# 10. Multiplicity Preservation Requirements

VDB ingestion MUST preserve evidence multiplicity.

VDB MUST NOT assume:

```text
one variant = one transcript
one variant = one gene
one variant = one consequence
one variant = one interpretation
one sample = one run forever
```

Current VAP v1 outputs may contain simplified transcript surfaces.

Future VAP releases may expand transcript complexity.

VDB ingestion MUST remain compatible with:

```text
multi-transcript interpretation
multi-gene mapping
ambiguous gene mapping
expanded noncoding annotation
additional semantic overlays
```

---

# 11. Required Validation Gate

VDB MUST NOT ingest a VAP-TEP as a trusted persistence package unless the VAP-TEP validation state is discoverable.

At minimum, VDB ingestion MUST record:

```text
validation_status
validation_schema_version
validation_check_count
validation_failed_count
validator_version
validated_at
```

Recommended ingestion policy:

```text
validation_status = PASS
    → eligible for trusted ingestion

validation_status = FAIL
    → reject or quarantine

validation_status missing
    → reject or quarantine
```

VDB MAY support quarantine ingestion for debugging, but quarantined packages MUST NOT enter normal query surfaces.

---

# 12. Required Integrity Gate

Before persistence, VDB ingestion SHOULD verify:

```text
lineage_manifest present
required entities present
required identifiers present
source_artifact_sha256 present
transport entity checksums present
tep_id present
sample_id present
run_id present
variant_id recoverable for variant entities
```

Failure of any required integrity gate SHOULD prevent trusted ingestion.

---

# 13. Non-Substitution Rules

The following substitutions are explicitly prohibited.

## 13.1 Stage12 Candidate Substitution

VDB MUST NOT treat Stage12 validation candidates as a complete representation of VAP evidence.

Stage12 is a selective validation-preparation overlay.

## 13.2 Stage11 Priority Substitution

VDB MUST NOT treat Stage11 prioritized variants as a complete representation of VAP evidence.

Prioritization is an overlay.

## 13.3 Stage08 Substitution for Stage07

VDB MUST NOT treat Stage08 normalized surfaces as the earliest preserved observation boundary.

Stage08 is semantically organized and must remain linked back to Stage07.

## 13.4 Context Sidecar Substitution

VDB MUST NOT treat Stage13 summaries, reports, or metadata as substitutes for primary evidence entities.

---

# 14. Discovery and Namespace Brokerage

After ingestion, VDB MAY perform discovery operations such as:

```text
artifact profiling
entity classification
identity detection
routing classification
semantic domain assignment
```

VDB MAY also perform namespace brokerage such as:

```text
source gene identifier → canonical gene identifier
source transcript identifier → canonical transcript identifier
source variant representation → canonical variant entity
```

Namespace brokerage MUST be additive.

Source identifiers MUST remain recoverable.

---

# 15. Downstream View Compatibility

VDB MAY materialize downstream views for:

```text
RDGP sample-gene prioritization
GSC phenotype-gene overlay compatibility
cohort recurrence analysis
noncoding burden analysis
clinical reviewability inspection
variant reinterpretation
```

Such views are derived surfaces.

Derived views MUST NOT replace canonical ingested evidence.

For RDGP-facing views, the derived identity may be:

```text
(sample_id, gene_id)
```

For VAP-ingested source evidence, the primary preserved identity remains:

```text
(sample_id, run_id, variant_id)
```

or VDB-normalized equivalents that retain all three source identities.

---

# 16. Minimum Acceptance Criteria for VDB Ingestion

A VAP-TEP is eligible for VDB trusted ingestion only if VDB can confirm:

```text
AC-VDB-001 tep_id present
AC-VDB-002 source_package_id present
AC-VDB-003 sample_id present
AC-VDB-004 run_id present
AC-VDB-005 lineage_manifest present
AC-VDB-006 Observation Entity present
AC-VDB-007 Normalization Entity present
AC-VDB-008 Routing Entity present
AC-VDB-009 Coding Interpretation Overlay present
AC-VDB-010 Noncoding Interpretation Overlay present
AC-VDB-011 Prioritization Overlay present
AC-VDB-012 Validation Overlay present
AC-VDB-013 Context Sidecar present
AC-VDB-014 source_artifact_sha256 present for transported entities
AC-VDB-015 Stage07 → Stage08 lineage recoverable
AC-VDB-016 variant_id recoverable for variant-level entities
AC-VDB-017 validation_status discoverable
AC-VDB-018 failed validation checks absent for trusted ingestion
```

---

# 17. Explicit Non-Goals

This interface does not define:

```text
VDB table schemas
SQL DDL
indexing strategy
query API design
clinical interpretation logic
RDGP ranking behavior
GSC overlay scoring behavior
cohort analysis algorithms
```

Those concerns belong to downstream repository-specific contracts.

---

# 18. Interface Guarantee

A compliant VAP → VDB TEP ingestion interface guarantees:

```text
VAP remains source authority.
TEP remains transport authority.
VDB becomes persistence and discovery authority.
Stage07 remains the preservation anchor.
Stages08–12 remain additive semantic overlays.
Source identities remain recoverable.
Lineage remains reconstructable.
Validation status remains auditable.
Future reinterpretability remains protected.
```

---

# 19. Recommended Next Implementation Step

The next implementation step is to create a VDB-side ingestion readiness checklist that maps each VAP-TEP entity role to a planned VDB persistence domain.

Recommended target document:

```text
docs/contracts/system/validation/vap_to_vdb_tep_ingestion_readiness_checklist.md
```
