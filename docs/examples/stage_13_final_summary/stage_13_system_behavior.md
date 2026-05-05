# Stage 13 — System Behavior Summary

## Overview

This artifact summarizes how VAP behaves as a system when applied to a healthy reference genome (HG002).

---

## Expected vs Observed Behavior

| Expectation | Observed |
|------------|----------|
| No pathogenic signal | No high-priority variants |
| Most variants noncoding | Confirmed |
| Rare coding variants present | Confirmed |
| Validation workload limited | ~2.4% |
| No false positives | No high-priority variants |

---

## Key System Properties

### Selectivity

> Only a small fraction of variants are selected for validation.

---

### Determinism

> All validation candidates originate from Tier 2 prioritization.

---

### Biological Realism

> Variant distributions match known genome-wide patterns.

---

### Restraint

> The system avoids overcalling disease-relevant variants.

---

### Calibration

> Observed behavior matches expected output for a healthy reference genome, confirming appropriate system calibration.

---

## Bottom Line

> VAP behaves as a calibrated, biologically informed variant prioritization system.