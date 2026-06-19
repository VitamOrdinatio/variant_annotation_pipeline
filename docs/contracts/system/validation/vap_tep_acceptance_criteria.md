# VAP Transitional Evidence Product (VAP-TEP) Acceptance Criteria

The `vap_tep_acceptance_criteria.md` defines successful VAP-TEP validation, and is supported by:

```text
vap_tep_contract.md
        ↓
vap_tep_transport_requirements.md
        ↓
vap_tep_acceptance_criteria.md (this document)
        ↓
implementation
```

See also:

- [VAP TEP Core Contract](../core/vap_tep_contract.md)
- [VAP TEP Transport Requirements](../interfaces/vap_tep_transport_requirements.md)


This document (`vap_tep_acceptance_criteria.md`) answers:

```text
How do we determine that a constructed VAP-TEP is valid?
```

Examples:

```text
✓ Stage07 entity present
✓ Stage08 entity present
✓ Routing entity present
✓ Lineage manifest present
✓ Observation lineage continuity preserved
✓ Required identifiers present
✓ SHA256 lineage records present
✓ Required overlays preserved
```

## Purpose

This document defines the acceptance criteria required for a VAP Transitional Evidence Product (VAP-TEP) to be considered compliant.

This document validates compliance against:

```text
docs/contracts/system/core/vap_tep_contract.md
```

and

```text
docs/contracts/system/interfaces/vap_tep_transport_requirements.md
```

A VAP-TEP is accepted only if all required acceptance criteria pass.

---

# 1. Acceptance Philosophy

A VAP-TEP is accepted only if:

* required preservation entities exist
* required lineage exists
* required provenance exists
* required identifiers exist
* required transport metadata exists
* required integrity metadata exists

Partial compliance is not sufficient.

Acceptance is binary:

```text
PASS
```

or

```text
FAIL
```

---

# 2. Required Entity Validation

## AC-001 Observation Entity Present

### Requirement

Observation Entity exists.

### Verification

Confirm presence of:

```text
Stage07 Observation Entity
```

### Result

PASS / FAIL

---

## AC-002 Normalization Entity Present

### Requirement

Normalization Entity exists.

### Verification

Confirm presence of:

```text
Stage08 Normalization Entity
```

### Result

PASS / FAIL

---

## AC-003 Routing Entity Present

### Requirement

Routing Entity exists.

### Verification

Confirm presence of:

```text
Stage08 Routing Entity
```

including:

```text
coding routing surface
splice routing surface
noncoding routing surface
```

### Result

PASS / FAIL

---

## AC-004 Coding Interpretation Overlay Present

### Requirement

Coding Interpretation Overlay exists.

### Verification

Confirm presence of:

```text
Stage09 Coding Interpretation Overlay
```

### Result

PASS / FAIL

---

## AC-005 Noncoding Interpretation Overlay Present

### Requirement

Noncoding Interpretation Overlay exists.

### Verification

Confirm presence of:

```text
Stage10 Noncoding Interpretation Overlay
```

### Result

PASS / FAIL

---

## AC-006 Prioritization Overlay Present

### Requirement

Prioritization Overlay exists.

### Verification

Confirm presence of:

```text
Stage11 Prioritization Overlay
```

### Result

PASS / FAIL

---

## AC-007 Validation Overlay Present

### Requirement

Validation Overlay exists.

### Verification

Confirm presence of:

```text
Stage12 Validation Overlay
```

### Result

PASS / FAIL

---

## AC-008 Lineage Manifest Present

### Requirement

Lineage Manifest exists.

### Verification

Confirm presence of:

```text
lineage_manifest
```

### Result

PASS / FAIL

---

## AC-009 Context Sidecar Present

### Requirement

Context Sidecar exists.

### Verification

Confirm presence of:

```text
Stage13-derived Context Sidecar
```

### Result

PASS / FAIL

---

# 3. Identifier Validation

## AC-010 TEP Identifier Present

### Requirement

```text
tep_id
```

exists.

### Result

PASS / FAIL

---

## AC-011 Sample Identifier Present

### Requirement

```text
sample_id
```

exists.

### Result

PASS / FAIL

---

## AC-012 Run Identifier Present

### Requirement

```text
run_id
```

exists.

### Result

PASS / FAIL

---

## AC-013 Variant Identity Preserved

### Requirement

```text
variant_id
```

exists wherever variant-level entities are present.

### Result

PASS / FAIL

---

## AC-013A TEP Schema Version Present

### Requirement

```text
tep_schema_version
```

exists for explicit versioning of lineage manifests.

### Results

PASS / FAIL

---

# 4. Lineage Validation

## AC-014 Source Artifact Provenance Present

### Requirement

Every entity preserves:

```text
source_artifact
source_stage
```

### Result

PASS / FAIL

---

## AC-015 Parent Entity Lineage Present

### Requirement

Lineage manifest preserves:

```text
parent_entities
```

### Result

PASS / FAIL

---

## AC-016 Child Entity Lineage Present

### Requirement

Lineage manifest preserves:

```text
child_entities
```

### Result

PASS / FAIL

---

## AC-017 Entity Role Present

### Requirement

Every entity declares:

```text
entity_role
```

### Result

PASS / FAIL

---

## AC-017A Entity Role Cardinality

### Requirement

Exactly one instance of each required entity role exists.

### Verification

Confirm exactly one:

```text
observation_entity
normalization_entity
routing_entity
coding_interpretation_overlay
noncoding_interpretation_overlay
prioritization_overlay
validation_overlay
lineage_manifest
```

### Result

PASS / FAIL

---

# 5. Stage07–Stage08 Preservation Validation

## AC-018 Observation Linkage Preserved

### Requirement

Observation and normalization entities remain linked.

### Verification

Confirm preservation of:

```text
sample_id
run_id
variant_id
```

linkage.

### Result

PASS / FAIL

---

## AC-019 Stage07 Artifact Traceability Present

### Requirement

Observation entity retains source artifact provenance.

### Result

PASS / FAIL

---

## AC-020 Stage08 Artifact Traceability Present

### Requirement

Normalization entity retains source artifact provenance.

### Result

PASS / FAIL

---

# 6. Normalization Validation

## AC-021 Required Stage08 Fields Present

### Requirement

Normalization entity preserves required semantic normalization fields.

At minimum:

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

### Result

PASS / FAIL

---

# 7. Interpretation Overlay Validation

## AC-022 Coding Interpretation Fields Preserved

### Requirement

Coding interpretation fields remain present.

Examples include:

```text
functional_impact
coding_interpretation_label
clinical_evidence
```

### Result

PASS / FAIL

---

## AC-023 Noncoding Interpretation Fields Preserved

### Requirement

Noncoding interpretation fields remain present.

Examples include:

```text
noncoding_functional_context
noncoding_interpretation_label
is_regulatory_candidate
```

### Result

PASS / FAIL

---

# 8. Integrity Validation

## AC-024 Artifact Checksums Present

### Requirement

All transported entities preserve integrity metadata.

At minimum:

```text
sha256
```

must be present.

### Result

PASS / FAIL

---

## AC-025 Lineage Manifest Checksums Present

### Requirement

Lineage manifest preserves integrity metadata.

### Result

PASS / FAIL

---

# 9. Transport Validation

## AC-026 Package Is Self-Describing

### Requirement

Consumer can determine:

```text
tep identity
entity inventory
lineage relationships
source provenance
```

without external metadata.

### Result

PASS / FAIL

---

## AC-027 Consumer Discoverability

### Requirement

Consumer can enumerate all entities from lineage manifest.

### Result

PASS / FAIL

---

# 10. Preservation Validation

## AC-028 Candidate-Only Preservation Prohibited

### Requirement

VAP-TEP does not consist solely of:

```text
Stage11
Stage12
```

candidate-oriented outputs.

### Result

PASS / FAIL

---

## AC-029 Observation Context Preserved

### Requirement

Observation Entity remains present.

### Result

PASS / FAIL

---

## AC-030 Normalization Context Preserved

### Requirement

Normalization Entity remains present.

### Result

PASS / FAIL

---

## AC-031 Interpretation Context Preserved

### Requirement

Coding and noncoding interpretation overlays remain present.

### Result

PASS / FAIL

---

## AC-032 Prioritization Context Preserved

### Requirement

Prioritization Overlay remains present.

### Result

PASS / FAIL

---

## AC-033 Validation Context Preserved

### Requirement

Validation Overlay remains present.

### Result

PASS / FAIL

---

# 11. Compliance Determination

A VAP-TEP is compliant only if:

```text
AC-001 through AC-033
```

all pass.

Any failed acceptance criterion results in:

```text
VAP-TEP NON-COMPLIANT
```

A compliant VAP-TEP must preserve:

```text
Observation
Normalization
Routing
Interpretation
Prioritization
Validation
```

with complete lineage, provenance, transport metadata, and integrity metadata.
