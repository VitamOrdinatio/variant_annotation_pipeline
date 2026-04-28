# 📄 Stage 12 Contract (Validation — Light v1)

Save as:

```text
docs/contracts/stage_12_contract.md
```

# Stage 12 — Validate Variants

## Purpose

Prepare prioritized variants for manual or visual validation (e.g., IGV review).

---

## Inputs

- `stage_11_prioritized_variants.tsv`

---

## Outputs

- `stage_12_validation_candidates.tsv`

---

## Added Fields

- `validation_required` (True/False)
- `validation_priority` (high | medium | low)
- `suggested_validation_method` (IGV | manual_review | none)

---

## Rules

```text
Tier 1 → validation_required = True, high
Tier 2 → validation_required = True, medium
Tier 3 → validation_required = False
Tier 4 → validation_required = False
```


---

## Non-Goals

- No actual IGV execution
- No BAM parsing

---