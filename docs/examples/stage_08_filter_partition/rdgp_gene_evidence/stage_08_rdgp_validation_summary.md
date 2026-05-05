# Stage 08 — RDGP Gene Evidence Validation Summary

## Overview

Stage 08 aggregates variant-level data into gene-level evidence summaries,
forming the foundation for rare disease gene prioritization.

---

## Key Metrics

- genes represented: ~50,230  
- total aggregated variants: ~3.5M  
- rare variants: ~99k  
- high-impact variants: ~791  

---

## Aggregation Structure

Each gene is summarized by:

- total variant count  
- rare variant count  
- high-impact variant count  
- pathogenic variant count  
- maximum severity  

---

## Key Observations

- most genes contain multiple variants  
- rare and high-impact variants are uncommon  
- variant burden varies widely across genes  

---

## Interpretation

> Gene-level evidence is multi-dimensional and cannot be reduced to a single metric.

Different prioritization strategies emphasize:

- total burden  
- rare variation  
- functional impact  
- clinical annotation  

---

## Important Considerations

- HG002 is a healthy benchmark genome  
- presence of pathogenic annotations does not imply disease  
- high-variant genes often reflect genomic size or complexity  

---

## System Role

This stage provides input to:

- RDGP (gene prioritization)  
- downstream interpretation workflows  

---

## Conclusion

Stage 08 successfully:

- aggregates variant-level data into gene-level summaries  
- preserves multiple evidence dimensions  
- enables flexible prioritization strategies  

---

## Bottom Line

> Gene-level evidence is constructed—not inferred—and must be interpreted in context.