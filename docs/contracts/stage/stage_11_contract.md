# Stage 11 — Prioritize Variants

## Purpose

Stage 11 integrates coding (Stage 09) and noncoding (Stage 10) interpreted variants into a unified candidate set and assigns deterministic priority tiers.

This stage performs **prioritization only**, not new annotation or biological inference.

---

## Inputs

### Required Artifacts

- `stage_09_coding_interpreted.tsv`
- `stage_10_noncoding_interpreted.tsv`

---

## Core Principles

- No new annotation sources introduced
- No probabilistic ranking or scoring
- Deterministic tier assignment based on existing fields
- Preserve all upstream fields
- Do not drop rows except irreparably malformed

---

## Integration Model

All variants are combined into a unified table:

```text
stage_11_prioritized_variants.tsv
```

Each row retains origin:
`variant_origin = coding | noncoding`

---

### Required Output Fields (additive)

### Core prioritization fields

- `priority_tier`
- `priority_reason`
- `is_high_priority_candidate` (True/False)
- `is_moderate_priority_candidate` - (True/False)
- `is_low_priority_candidate` (True/False)
- `is_uninterpretable` (True/False)

---

## Priority Tier Definitions

### Tier 1 — High Confidence Candidate

Criteria:

```text
coding:
  interpretation_label == "lof_or_missense_rare"
  AND qc_reliability == high_confidence

noncoding:
  interpretation_label == "regulatory_rare_supported"
```


### Tier 2 — Moderate Candidate

Criteria:

```text
coding:
  interpretation_label == "lof_or_missense_rare"
  AND qc_reliability == caution

noncoding:
  interpretation_label == "regulatory_or_transcript_rare"
```


### Tier 3 — Low Support / Common

Criteria:

```text
coding:
  interpretation_label == "coding_common_or_low_support"

noncoding:
  interpretation_label == "noncoding_common_or_low_support"
```

### Tier 4 — Uninterpretable / QC Limited

Criteria:

```text
coding:
  interpretation_label == "coding_uninterpretable"

noncoding:
  interpretation_label == "noncoding_uninterpretable"
```

---

## Priority Assignment Rules

Each variant must receive exactly one priority_tier

Tier precedence:
`Tier 1 > Tier 2 > Tier 3 > Tier 4`

---

## QC Requirements

### Required checks

- All rows assigned a priority tier
- No overlap between tiers
- Input row count == output row count

---

## Summary Output

`stage_11_summary.json`

Must include:

- counts by priority_tier
- counts by variant_origin
- counts by gene_id
- counts of high-priority candidates

---

## Assumptions

- Stage 09 and Stage 10 outputs are contract-compliant
- Interpretation labels are biologically meaningful and stable

---

## Non-Goals

- No ranking within tiers
- No phenotype matching
- No gene scoring
- No machine learning


---