# VAP-TEP Lineage Manifest Schema

## Purpose

This document defines the schema for the VAP Transitional Evidence Product (VAP-TEP) lineage manifest.

The lineage manifest is the authoritative machine-readable index for a VAP-TEP package.

It records:

* TEP identity
* source run identity
* preserved entity inventory
* source artifact provenance
* integrity metadata
* parent/child lineage relationships
* transport-discovery metadata

The lineage manifest enables downstream consumers to understand what evidence was transported, where it came from, and how preserved entities relate to one another.

---

# 1. Schema Status

```text
schema_name: vap_tep_lineage_manifest
schema_version: 0.1.0
status: draft
```

This schema is intended for VAP-TEP v1 implementation.

---

# 2. Canonical Filename

A VAP-TEP package MUST contain the lineage manifest at package root:

```text
lineage_manifest.json
```

The file MUST be valid UTF-8 encoded JSON.

---

# 3. Top-Level Object

The lineage manifest MUST be a JSON object with the following top-level keys:

```text
manifest_type
manifest_schema_version
tep_id
tep_schema_version
producer
source_run
package
entities
lineage_edges
validation_summary
```

---

# 4. Top-Level Fields

## 4.1 manifest_type

Required.

```json
"manifest_type": "vap_tep_lineage_manifest"
```

MUST equal:

```text
vap_tep_lineage_manifest
```

---

## 4.2 manifest_schema_version

Required.

```json
"manifest_schema_version": "0.1.0"
```

MUST identify the lineage manifest schema version.

---

## 4.3 tep_id

Required.

```json
"tep_id": "vap_tep_SRR12898354_run_2026_06_03_010030_v1"
```

MUST uniquely identify the transported VAP-TEP.

The `tep_id` MUST be stable within a given package.

---

## 4.4 tep_schema_version

Required.

```json
"tep_schema_version": "vap_tep_v1"
```

MUST identify the VAP-TEP payload schema family.

---

## 4.5 producer

Required.

Object describing the producing repository and implementation.

Required fields:

```text
repository
pipeline
producer_version
created_utc
```

Example:

```json
"producer": {
  "repository": "variant_annotation_pipeline",
  "pipeline": "VAP",
  "producer_version": "v1",
  "created_utc": "2026-06-18T00:00:00Z"
}
```

---

## 4.6 source_run

Required.

Object describing the source VAP run.

Required fields:

```text
sample_id
run_id
run_directory
```

Recommended fields:

```text
technical_mode
case_study_label
```

Example:

```json
"source_run": {
  "sample_id": "SRR12898354",
  "run_id": "run_2026_06_03_010030",
  "run_directory": "results/run_2026_06_03_010030",
  "technical_mode": "WGS",
  "case_study_label": "HG002"
}
```

---

## 4.7 package

Required.

Object describing the TEP package itself.

Required fields:

```text
package_root
package_format
self_describing
```

Recommended fields:

```text
package_sha256
```

Example:

```json
"package": {
  "package_root": "vap_tep_SRR12898354_run_2026_06_03_010030_v1",
  "package_format": "directory",
  "self_describing": true
}
```

---

# 5. Entities

## 5.1 entities

Required.

Array of entity objects.

Each entity object MUST describe one preserved logical entity.

Required entity roles:

```text
observation_entity
normalization_entity
routing_entity
coding_interpretation_overlay
noncoding_interpretation_overlay
prioritization_overlay
validation_overlay
context_sidecar
```

The lineage manifest itself MUST also be discoverable, either as:

```text
lineage_manifest
```

or through the top-level manifest object.

VAP-TEP v1 SHOULD represent `lineage_manifest` as an entity for validation simplicity.

---

## 5.2 Entity Object Required Fields

Each entity object MUST contain:

```text
entity_id
entity_role
source_stage
source_artifacts
transport_path
row_count
column_count
variant_id_count
sha256
required
```

---

## 5.3 entity_id

Required.

Stable identifier for the transported entity.

Example:

```json
"entity_id": "observation_entity"
```

Recommended v1 entity IDs:

```text
observation_entity
normalization_entity
routing_entity
coding_interpretation_overlay
noncoding_interpretation_overlay
prioritization_overlay
validation_overlay
context_sidecar
lineage_manifest
```

---

## 5.4 entity_role

Required.

MUST be one of:

```text
observation_entity
normalization_entity
routing_entity
coding_interpretation_overlay
noncoding_interpretation_overlay
prioritization_overlay
validation_overlay
context_sidecar
lineage_manifest
```

---

## 5.5 source_stage

Required.

MUST identify the producing VAP stage.

Allowed values:

```text
stage07
stage08
stage09
stage10
stage11
stage12
stage13
tep_construction
```

---

## 5.6 source_artifacts

Required.

Array of source artifact records.

Each record MUST include:

```text
source_artifact
source_artifact_role
source_artifact_sha256
source_artifact_exists
```

Recommended fields:

```text
source_artifact_rows
source_artifact_columns
source_artifact_variant_id_count
```

Example:

```json
"source_artifacts": [
  {
    "source_artifact": "results/run_2026_06_03_010030/processed/stage_08_vdb_ready_variants.tsv",
    "source_artifact_role": "stage08_vdb_ready_variants",
    "source_artifact_sha256": "abc123...",
    "source_artifact_exists": true,
    "source_artifact_rows": 4636584,
    "source_artifact_columns": 34,
    "source_artifact_variant_id_count": 4636584
  }
]
```

---

## 5.7 transport_path

Required.

Relative path within the VAP-TEP package where the transported entity can be found.

Example:

```json
"transport_path": "normalization/stage_08_vdb_ready_variants.tsv"
```

---

## 5.8 row_count

Required.

Number of data rows in the transported entity.

For non-tabular metadata entities, this MAY be:

```json
null
```

provided the entity has a valid `sha256`.

---

## 5.9 column_count

Required.

Number of columns in the transported entity.

For non-tabular metadata entities, this MAY be:

```json
null
```

provided the entity has a valid `sha256`.

---

## 5.10 variant_id_count

Required.

Number of distinct `variant_id` values in the transported entity.

For non-variant-level entities, this MAY be:

```json
null
```

---

## 5.11 sha256

Required.

SHA256 checksum of the transported entity content.

---

## 5.12 required

Required.

Boolean indicating whether the entity is required for VAP-TEP compliance.

All core v1 entities MUST set:

```json
"required": true
```

---

# 6. Lineage Edges

## 6.1 lineage_edges

Required.

Array of directed parent/child relationships between entities.

Each lineage edge MUST contain:

```text
parent_entity_id
child_entity_id
relationship
```

Recommended fields:

```text
validation_basis
```

---

## 6.2 Required v1 Lineage Edges

A VAP-TEP v1 lineage manifest MUST include at least:

```text
observation_entity
    →
normalization_entity

normalization_entity
    →
routing_entity

routing_entity
    →
coding_interpretation_overlay

routing_entity
    →
noncoding_interpretation_overlay

coding_interpretation_overlay
    →
prioritization_overlay

noncoding_interpretation_overlay
    →
prioritization_overlay

prioritization_overlay
    →
validation_overlay

validation_overlay
    →
context_sidecar
```

The final edge to `context_sidecar` represents contextual association, not evidence derivation.

---

## 6.3 relationship

Required.

Allowed values:

```text
normalizes
routes
interprets_coding
interprets_noncoding
prioritizes
prepares_validation
contextualizes
indexes
```

---

# 7. Validation Summary

## 7.1 validation_summary

Required.

Object summarizing VAP-TEP acceptance validation.

Required fields:

```text
validation_status
criteria_version
criteria_passed
criteria_failed
validated_utc
```

Example:

```json
"validation_summary": {
  "validation_status": "not_validated",
  "criteria_version": "vap_tep_acceptance_criteria_v1",
  "criteria_passed": [],
  "criteria_failed": [],
  "validated_utc": null
}
```

Before validation, `validation_status` SHOULD be:

```text
not_validated
```

After validation, `validation_status` MUST be either:

```text
pass
fail
```

---

# 8. Required v1 Entity Inventory

A complete VAP-TEP v1 lineage manifest MUST enumerate the following entities:

| Entity ID                          | Entity Role                        | Source Stage       | Required |
| ---------------------------------- | ---------------------------------- | ------------------ | -------- |
| `observation_entity`               | `observation_entity`               | `stage07`          | true     |
| `normalization_entity`             | `normalization_entity`             | `stage08`          | true     |
| `routing_entity`                   | `routing_entity`                   | `stage08`          | true     |
| `coding_interpretation_overlay`    | `coding_interpretation_overlay`    | `stage09`          | true     |
| `noncoding_interpretation_overlay` | `noncoding_interpretation_overlay` | `stage10`          | true     |
| `prioritization_overlay`           | `prioritization_overlay`           | `stage11`          | true     |
| `validation_overlay`               | `validation_overlay`               | `stage12`          | true     |
| `context_sidecar`                  | `context_sidecar`                  | `stage13`          | true     |
| `lineage_manifest`                 | `lineage_manifest`                 | `tep_construction` | true     |

---

# 9. Required Artifact Mapping

VAP-TEP v1 SHOULD use the following default source artifact mapping.

| Entity Role                        | Source Artifact(s)                                                                  |
| ---------------------------------- | ----------------------------------------------------------------------------------- |
| `observation_entity`               | Stage07 `*.annotated_variants.tsv`                                                  |
| `normalization_entity`             | `stage_08_selected_transcript_consequences.tsv`; `stage_08_vdb_ready_variants.tsv`  |
| `routing_entity`                   | `coding_candidates.tsv`; `splice_region_candidates.tsv`; `noncoding_candidates.tsv` |
| `coding_interpretation_overlay`    | `stage_09_coding_interpreted.tsv`                                                   |
| `noncoding_interpretation_overlay` | `stage_10_noncoding_interpreted.tsv`                                                |
| `prioritization_overlay`           | `stage_11_prioritized_variants.tsv`                                                 |
| `validation_overlay`               | `stage_12_validation_candidates.tsv`                                                |
| `context_sidecar`                  | Stage13 outputs and run metadata                                                    |
| `lineage_manifest`                 | `lineage_manifest.json`                                                             |

---

# 10. Null Semantics

Fields that are not applicable MUST use JSON null.

Fields that are missing unexpectedly MUST cause validation failure unless explicitly declared optional.

Empty strings MUST NOT be used to represent null values in the lineage manifest.

---

# 11. Example Minimal Manifest Skeleton

```json
{
  "manifest_type": "vap_tep_lineage_manifest",
  "manifest_schema_version": "0.1.0",
  "tep_id": "vap_tep_SRR12898354_run_2026_06_03_010030_v1",
  "tep_schema_version": "vap_tep_v1",
  "producer": {
    "repository": "variant_annotation_pipeline",
    "pipeline": "VAP",
    "producer_version": "v1",
    "created_utc": "2026-06-18T00:00:00Z"
  },
  "source_run": {
    "sample_id": "SRR12898354",
    "run_id": "run_2026_06_03_010030",
    "run_directory": "results/run_2026_06_03_010030",
    "technical_mode": "WGS",
    "case_study_label": "HG002"
  },
  "package": {
    "package_root": "vap_tep_SRR12898354_run_2026_06_03_010030_v1",
    "package_format": "directory",
    "self_describing": true
  },
  "entities": [],
  "lineage_edges": [],
  "validation_summary": {
    "validation_status": "not_validated",
    "criteria_version": "vap_tep_acceptance_criteria_v1",
    "criteria_passed": [],
    "criteria_failed": [],
    "validated_utc": null
  }
}
```

---

# 12. Validation Notes

The lineage manifest schema supports future automated validation of:

```text
AC-001 through AC-033
```

as defined in:

```text
docs/contracts/system/validation/vap_tep_acceptance_criteria.md
```

A VAP-TEP package cannot be considered compliant unless its lineage manifest passes schema validation and acceptance validation.
