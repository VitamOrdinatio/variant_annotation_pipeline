# Stage 12 — Validation Rationale Distribution

## Overview

This artifact summarizes the rationale used to assign validation status.

---

## Validation Reason Distribution

| Reason | Count |
|--------|--------|
| tier_2_moderate_candidate | 113,363 |
| tier_3_low_support_or_common | 3,369,755 |
| tier_4_uninterpretable_or_qc_limited | 1,153,466 |

---

## Interpretation

- Only Tier 2 variants are selected for validation  
- Tier 3 and Tier 4 variants are excluded from validation  

---

## Key Insight

> Validation is driven exclusively by prioritization logic.

---

## System Behavior

- deterministic mapping from Stage 11 → Stage 12  
- no leakage between tiers  
- no over-assignment of validation  

---

## Bottom Line

> Validation triage is strictly controlled and fully explainable.