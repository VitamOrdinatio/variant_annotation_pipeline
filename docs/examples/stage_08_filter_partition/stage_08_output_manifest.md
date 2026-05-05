# Stage 08 — Output Manifest

## Overview

Stage 08 generates structured outputs across four conceptual layers:

- coding candidates  
- noncoding candidates  
- gene-level aggregation (RDGP seed)  
- global summary statistics  

---

## Output Structure

### Coding Candidates

- coding_candidates.tsv  
- consequence distribution  
- variant type distribution  
- example records  
- high-impact variant subset  

---

### Noncoding Candidates

- noncoding_candidates.tsv  
- consequence distribution  
- variant type distribution  
- example records  
- high-impact / splice-region subset  

---

### RDGP Gene Evidence

- gene-level aggregation table (~50k genes)  
- summary counts  
- prioritization views:
  - variant burden  
  - high-impact burden  
  - rare variant burden  
  - pathogenic evidence  

---

### Variant Summary

- coding vs noncoding distribution  
- frequency distribution  
- severity distribution  

---

## Key Characteristics

- outputs are **partitioned, not filtered destructively**  
- full variant space is preserved  
- multiple analytical views are generated  

---

## Interpretation

> Stage 08 produces a multi-layer representation of genomic variation,
enabling downstream interpretation and prioritization without loss of information.

---

## Notes

- Raw files are large and excluded from Git  
- Artifacts represent curated, human-readable summaries  