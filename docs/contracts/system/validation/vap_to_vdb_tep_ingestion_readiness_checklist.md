# VAP → VDB TEP Ingestion Readiness Checklist

## Purpose

This document provides the validation checklist used to determine whether a VDB ingestion implementation is capable of safely ingesting VAP Transitional Evidence Products (VAP-TEPs).

This checklist operationalizes the requirements defined in:

```text
docs/contracts/system/interfaces/vap_to_vdb_tep_ingestion_interface.md
```

Successful completion of this checklist indicates ingestion readiness.

Failure of any required item indicates that trusted VAP-TEP ingestion is not yet certified.

---

# 1. Certification Scope

This checklist evaluates:

```text
identity preservation
artifact preservation
lineage preservation
semantic preservation
validation preservation
future reinterpretability preservation
```

This checklist does not evaluate:

```text
query performance
database indexing
API responsiveness
cohort analytics
clinical interpretation quality
```

---

# 2. Identity Preservation Certification

## ID-001

Verify `tep_id` is persisted.

Status:

```text
[ ] PASS
[ ] FAIL
```

Notes:

```text
```

---

## ID-002

Verify `source_repository` is persisted.

Status:

```text
[ ] PASS
[ ] FAIL
```

---

## ID-003

Verify `source_package_id` is persisted.

Status:

```text
[ ] PASS
[ ] FAIL
```

---

## ID-004

Verify `sample_id` is persisted.

Status:

```text
[ ] PASS
[ ] FAIL
```

---

## ID-005

Verify `run_id` is persisted.

Status:

```text
[ ] PASS
[ ] FAIL
```

---

## ID-006

Verify `variant_id` remains recoverable.

Status:

```text
[ ] PASS
[ ] FAIL
```

---

## ID-007

Verify VDB canonical identifiers do not replace source identifiers.

Status:

```text
[ ] PASS
[ ] FAIL
```

---

# 3. Artifact Preservation Certification

## ART-001

Verify lineage manifest is ingested.

Status:

```text
[ ] PASS
[ ] FAIL
```

---

## ART-002

Verify all transported entities are discoverable.

Status:

```text
[ ] PASS
[ ] FAIL
```

---

## ART-003

Verify source artifact paths remain recoverable.

Status:

```text
[ ] PASS
[ ] FAIL
```

---

## ART-004

Verify source artifact checksums are preserved.

Status:

```text
[ ] PASS
[ ] FAIL
```

---

## ART-005

Verify entity role assignments remain recoverable.

Status:

```text
[ ] PASS
[ ] FAIL
```

---

# 4. Stage07 Preservation Certification

## S07-001

Verify Observation Entity exists.

Status:

```text
[ ] PASS
[ ] FAIL
```

---

## S07-002

Verify Observation Entity originates from Stage07.

Status:

```text
[ ] PASS
[ ] FAIL
```

---

## S07-003

Verify Stage07 evidence is queryable independently of downstream overlays.

Status:

```text
[ ] PASS
[ ] FAIL
```

---

## S07-004

Verify Stage07 evidence is not replaced by Stage11 or Stage12 outputs.

Status:

```text
[ ] PASS
[ ] FAIL
```

---

# 5. Semantic Overlay Preservation Certification

## SEM-001

Verify Stage08 Normalization Entity exists.

Status:

```text
[ ] PASS
[ ] FAIL
```

---

## SEM-002

Verify Stage08 Routing Entity exists.

Status:

```text
[ ] PASS
[ ] FAIL
```

---

## SEM-003

Verify Stage09 Coding Overlay exists.

Status:

```text
[ ] PASS
[ ] FAIL
```

---

## SEM-004

Verify Stage10 Noncoding Overlay exists.

Status:

```text
[ ] PASS
[ ] FAIL
```

---

## SEM-005

Verify Stage11 Prioritization Overlay exists.

Status:

```text
[ ] PASS
[ ] FAIL
```

---

## SEM-006

Verify Stage12 Validation Overlay exists.

Status:

```text
[ ] PASS
[ ] FAIL
```

---

## SEM-007

Verify overlays remain linked to their parent entities.

Status:

```text
[ ] PASS
[ ] FAIL
```

---

# 6. Lineage Preservation Certification

## LIN-001

Verify Stage07 → Stage08 lineage is recoverable.

Status:

```text
[ ] PASS
[ ] FAIL
```

---

## LIN-002

Verify Stage08 → Stage09 lineage is recoverable.

Status:

```text
[ ] PASS
[ ] FAIL
```

---

## LIN-003

Verify Stage08 → Stage10 lineage is recoverable.

Status:

```text
[ ] PASS
[ ] FAIL
```

---

## LIN-004

Verify Stage09 → Stage11 lineage is recoverable.

Status:

```text
[ ] PASS
[ ] FAIL
```

---

## LIN-005

Verify Stage10 → Stage11 lineage is recoverable.

Status:

```text
[ ] PASS
[ ] FAIL
```

---

## LIN-006

Verify Stage11 → Stage12 lineage is recoverable.

Status:

```text
[ ] PASS
[ ] FAIL
```

---

## LIN-007

Verify lineage graph reconstruction is possible from persisted records.

Status:

```text
[ ] PASS
[ ] FAIL
```

---

# 7. Multiplicity Preservation Certification

## MUL-001

Verify multi-transcript relationships remain supported.

Status:

```text
[ ] PASS
[ ] FAIL
```

---

## MUL-002

Verify multi-gene mappings remain supported.

Status:

```text
[ ] PASS
[ ] FAIL
```

---

## MUL-003

Verify multiple interpretation overlays can coexist for a single variant.

Status:

```text
[ ] PASS
[ ] FAIL
```

---

## MUL-004

Verify future semantic expansion does not require identifier replacement.

Status:

```text
[ ] PASS
[ ] FAIL
```

---

# 8. Validation Preservation Certification

## VAL-001

Verify validation status is persisted.

Status:

```text
[ ] PASS
[ ] FAIL
```

---

## VAL-002

Verify validator version is persisted.

Status:

```text
[ ] PASS
[ ] FAIL
```

---

## VAL-003

Verify validation check count is persisted.

Status:

```text
[ ] PASS
[ ] FAIL
```

---

## VAL-004

Verify validation failure count is persisted.

Status:

```text
[ ] PASS
[ ] FAIL
```

---

## VAL-005

Verify validation timestamp is persisted.

Status:

```text
[ ] PASS
[ ] FAIL
```

---

# 9. Non-Substitution Certification

## NS-001

Verify Stage12 candidates are not the sole persisted representation.

Status:

```text
[ ] PASS
[ ] FAIL
```

---

## NS-002

Verify Stage11 prioritized variants are not the sole persisted representation.

Status:

```text
[ ] PASS
[ ] FAIL
```

---

## NS-003

Verify Stage08 normalized entities do not replace Stage07 observations.

Status:

```text
[ ] PASS
[ ] FAIL
```

---

## NS-004

Verify metadata sidecars do not replace primary evidence entities.

Status:

```text
[ ] PASS
[ ] FAIL
```

---

# 10. Trusted Ingestion Certification

Trusted ingestion may be granted only if:

```text
All ID checks PASS
All ART checks PASS
All S07 checks PASS
All SEM checks PASS
All LIN checks PASS
All VAL checks PASS
All NS checks PASS
```

Certification Result:

```text
[ ] TRUSTED INGESTION APPROVED

[ ] TRUSTED INGESTION DENIED
```

Reviewer:

```text
```

Date:

```text
```

Version:

```text
```
