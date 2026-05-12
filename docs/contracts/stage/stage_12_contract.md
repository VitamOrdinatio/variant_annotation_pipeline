# 📄 Stage 12 Contract (Validation — Light v1)

## Purpose

Stage 12 — Validate Variants:

Prepare prioritized variants for manual or visual validation (e.g., IGV review).

---

## Inputs

- `stage_11_prioritized_variants.tsv`

---

## Required Input Fields

- `priority_tier`
- `priority_rank`
- `variant_id`
- `gene_id`
- `gene_symbol`
- `chromosome`
- `position`

---

## Outputs

- `stage_12_validation_candidates.tsv`

---

## Added Fields

- `validation_required` (True/False)
- `validation_priority` (high | medium | low)
- `suggested_validation_method` (IGV | manual_review | none)
- `validation_reason` (string)
    - Examples
      - "tier_1_high_confidence_candidate"
      - "tier_2_moderate_candidate"

---

## Suggested Validation Method Rules

Tier 1:
  suggested_validation_method = IGV

Tier 2:
  suggested_validation_method = IGV

Tier 3:
  suggested_validation_method = none

Tier 4:
  suggested_validation_method = none


manual_review reserved for edge-case workflows (not used in v1)

---

## Rules

```text
Tier 1 → validation_required = True, high
Tier 2 → validation_required = True, medium
Tier 3 → validation_required = False, validation_priority = low
Tier 4 → validation_required = False, validation_priority = low
```

---

## QC Requirements

- All input rows preserved
- All rows assigned validation_required
- No null validation_priority
- Row count invariant maintained

---

## Summary Output

stage_12_summary.json

Must include:
- counts by validation_required
- counts by validation_priority
- counts by priority_tier


## Non-Goals

- No actual IGV execution
- No BAM parsing
- No variant filtering or removal
- No reinterpretation of evidence

---