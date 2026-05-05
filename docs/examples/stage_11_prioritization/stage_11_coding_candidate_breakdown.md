# Stage 11 — Coding Candidate Breakdown

## Overview

This artifact characterizes the subset of **Tier 2 coding candidates** identified during Stage 11 prioritization.

Total coding candidates: **1,121**

---

## Functional Impact Distribution

| Category | Count |
|----------|--------|
| missense | 1,029 |
| loss_of_function | 92 |

---

## Rarity Distribution

| Category | Count |
|----------|--------|
| rare | 636 |
| low_frequency | 485 |

---

## Clinical Annotation

| Category | Count |
|----------|--------|
| missing | 988 |
| VUS | 102 |
| conflicting | 27 |
| pathogenic | 3 |
| likely_pathogenic | 1 |

---

## Combined Impact × Rarity

| Category | Count |
|----------|--------|
| missense_rare | 579 |
| missense_low_frequency | 450 |
| loss_of_function_rare | 57 |
| loss_of_function_low_frequency | 35 |

---

## Interpretation

- Coding candidates are dominated by **missense variants (~92%)**  
- **Loss-of-function variants are rare (~8%)**, but represent higher-impact events  
- Most candidates are **rare or low-frequency**, consistent with prioritization logic  

### Clinical Signal

- The vast majority (~88%) lack clinical annotation  
- A small subset (~9%) are classified as VUS  
- Only **4 variants** carry pathogenic or likely pathogenic labels  

---

## Key Insight

> Prioritized coding candidates are enriched for rare, potentially impactful variants, but most lack strong clinical evidence.

---

## Biological Context

- Missense variants dominate due to their prevalence in coding regions  
- Loss-of-function variants are rarer but more disruptive  
- Clinical databases (e.g., ClinVar) provide incomplete coverage  

---

## System Implications

- Coding candidates provide **interpretable signal**, but:
  - require phenotype context  
  - require gene-level prioritization (RDGP)  
  - require validation (Stage 12)  

---

## Important Considerations

- HG002 is a healthy benchmark genome  
- presence of rare or pathogenic-labeled variants does not imply disease  
- interpretation remains probabilistic  

---

## Bottom Line

> Coding candidate variants provide interpretable signal, but most represent uncertain or weakly supported biological evidence requiring further context.