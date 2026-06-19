# VAP-TEP Payload Decision Rationale

## Purpose

This document captures the reasoning behind major VAP-TEP payload design decisions.

These decisions are derived from:

* Stage07 preservation-boundary analysis
* Stage08–12 implementation review
* Empirical lineage forensics across 13 production VAP runs
* Column lineage auditing
* VAP-TEP preservation lineage modeling

This document serves as the rationale layer between preservation doctrine and future implementation.

---

# Decision 1

## What is the smallest preservation-compliant VAP-TEP?

### Decision

The smallest preservation-compliant VAP-TEP consists of:

```text
Stage07 Observation Entity
+
Stage08 Normalization Entity
+
Stage09 Coding Interpretation Overlay
+
Stage10 Noncoding Interpretation Overlay
+
Stage11 Prioritization Overlay
+
Stage12 Validation Overlay
+
Lineage Manifest
```

### Rationale

Stage07 alone is insufficient because it lacks normalization and downstream interpretation context.

Stage12 alone is insufficient because not all interpretation-layer fields survive literally to the validation boundary.

Forensic analysis demonstrates that biologically meaningful information is introduced at multiple stages of the pipeline.

Accordingly, preservation must encompass the complete evidence lifecycle rather than a single terminal artifact.

### Consequence

Candidate-only preservation is not preservation-compliant.

---

# Decision 2

## Which Stage08 normalization fields are mandatory?

### Decision

The following normalization fields are considered mandatory preservation fields:

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
variant_type
population_frequency
```

### Rationale

Stage08 is the first semantic normalization boundary.

These fields explain how Stage07 observations were transformed into an interoperability substrate suitable for downstream reasoning.

Removal of these fields would sever interpretive context between observation and interpretation layers.

### Consequence

Stage08 normalization context must remain traceable within VAP-TEP.

---

# Decision 3

## Which interpretation overlays must survive literally?

### Decision

Stage09 coding interpretation fields and Stage10 noncoding interpretation fields must survive literally.

Examples include:

### Stage09

```text
functional_impact
coding_interpretation_label
clinical_evidence
rarity_flag
qc_reliability
is_lof_candidate
```

### Stage10

```text
noncoding_functional_context
noncoding_interpretation_label
is_regulatory_candidate
clinical_evidence
rarity_flag
qc_reliability
```

### Rationale

Interpretation overlays are the primary scientific products of Stages09 and 10.

Forensic analysis demonstrates that some noncoding interpretation fields do not survive literally into downstream artifacts.

Accordingly, preservation cannot rely solely upon Stage11 or Stage12 outputs.

### Consequence

Interpretation overlays must be explicitly preserved.

---

# Decision 4

## Should VAP-TEP preserve entities separately?

### Decision

Yes.

VAP-TEP should preserve evidence entities separately.

### Canonical Structure

```text
Observation Entity
Normalization Entity
Coding Interpretation Overlay
Noncoding Interpretation Overlay
Prioritization Overlay
Validation Overlay
```

### Rationale

Each layer represents a distinct evidence role.

Collapsing all layers into a single merged representation obscures:

* provenance
* evidence timing
* interpretation boundaries
* future reinterpretation opportunities

### Consequence

Merged views may be materialized downstream but should not be the canonical preservation structure.

---

# Decision 5

## How should lineage be represented?

### Decision

Lineage must be explicit and machine-readable.

### Required Artifact-Level Lineage

```text
tep_id
run_id
sample_id

source_artifact
source_artifact_sha256

row_count
column_count
variant_id_count

parent_artifacts
child_artifacts

entity_role
```

### Required Row-Level Lineage

```text
variant_id
```

serves as the primary evidence join key.

### Rationale

Preservation without lineage is merely storage.

Explicit lineage enables:

* reproducibility
* reinterpretation
* auditability
* downstream evidence federation

### Consequence

Lineage is a first-class preservation concern.

---

# Decision 6

## How should Stage07 and Stage08 be linked?

### Decision

Stage07 and Stage08 must remain explicitly linked.

### Required Keys

```text
sample_id
run_id
variant_id
```

### Required Validation

```text
Stage07 row count
=
Stage08 selected row count

Stage07 distinct variant_ids
=
Stage08 selected distinct variant_ids
```

### Required Artifact Traceability

```text
stage07_artifact
stage08_selected_artifact
stage08_vdb_ready_artifact
```

### Rationale

Stage07 represents the observation boundary.

Stage08 represents the normalization boundary.

Preservation requires proof that normalization did not sever observational identity.

### Consequence

Stage07 and Stage08 form the foundational preservation linkage within VAP-TEP.

---

# Summary

The VAP-TEP preservation model is founded upon six evidence layers:

```text
Observation
    Stage07

Normalization
    Stage08

Coding Interpretation
    Stage09

Noncoding Interpretation
    Stage10

Prioritization
    Stage11

Validation
    Stage12
```

VAP-TEP therefore preserves not merely candidate variants, but the complete evidence lineage that produced those candidates.
