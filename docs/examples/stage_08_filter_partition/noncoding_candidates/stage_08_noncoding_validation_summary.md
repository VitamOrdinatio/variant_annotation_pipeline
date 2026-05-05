# Stage 08 — Noncoding Candidate Validation Summary

## Overview

Stage 08 partitions annotated variants into coding and noncoding sets.

The noncoding set represents the majority of genomic variation and is preserved for downstream interpretation.

---

## Key Metrics

- total input variants: ~4.6M  
- noncoding variants retained: ~4.63M  
- proportion of total: >99%  

---

## Consequence Profile

Dominant categories:

- intronic variants (~2.8M combined)  
- intergenic variants (~1.1M)  
- upstream/downstream gene variants (~0.5M combined)  

---

## Variant Types

- SNVs dominate (~3.9M variants)  
- insertions/deletions present but less frequent  

---

## Functional Interpretation

- most variants classified as MODIFIER  
- limited interpretability without additional annotation  
- high-impact annotations in noncoding space require caution  

---

## Key Insight

> The majority of genomic variation occurs in noncoding regions and cannot be interpreted using coding-centric frameworks.

---

## System Role

Noncoding candidates are preserved for:

- regulatory annotation  
- transcriptomic integration (RSP)  
- downstream prioritization (RDGP)  

---

## Conclusion

Stage 08 successfully:

- partitions noncoding variants correctly  
- preserves full noncoding space  
- avoids premature interpretation  

This enables flexible, context-aware downstream analysis.

---

## Bottom Line

> Noncoding variation is preserved—not interpreted—until sufficient biological context is available.