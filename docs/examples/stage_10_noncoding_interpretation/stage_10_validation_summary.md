# Stage 10 — Noncoding Interpretation Validation Summary

## Overview

Stage 10 applies rule-based classification to noncoding variants, assigning structured labels while preserving interpretability constraints.

---

## Key Metrics

- total noncoding variants: ~4.61M  
- common variants: ~4.2M  
- rare variants: ~128k  
- regulatory/transcript-associated rare variants: ~112k  
- uninterpretable variants: ~1.15M  

---

## Interpretation Label Distribution

- common / low-support: ~3.34M  
- uninterpretable: ~1.15M  
- regulatory or transcript-associated rare: ~112k  

---

## Functional Context

- intronic variants dominate (~1.6M)  
- transcript-associated variants (~1.25M)  
- intergenic variants (~1.1M)  

---

## Key Observations

- most noncoding variants are common and low-impact  
- a large fraction cannot be interpreted  
- a small subset may have regulatory or transcript-level relevance  

---

## Key Insight

> Noncoding variant interpretation is fundamentally limited by current biological knowledge.

---

## Important Considerations

- HG002 is a healthy reference genome  
- presence of rare or annotated variants does not imply disease  
- interpretation requires external data integration  

---

## System Role

Stage 10 produces:

- structured noncoding interpretation labels  
- candidate variants for downstream prioritization (Stage 11)  
- inputs for transcriptomic integration (RSP)  

---

## Conclusion

Stage 10 successfully:

- partitions noncoding variants into interpretable categories  
- preserves uncertainty where interpretation is not possible  
- identifies candidates for downstream analysis  


### Interpretation Boundary

Stage 10 intentionally avoids assigning biological meaning beyond available annotation.

---

## Bottom Line

> Stage 10 identifies noncoding candidates without overinterpreting biological significance.