# Stage 12 — Validation Composition

## Overview

This artifact summarizes the functional composition of variants assigned for validation in Stage 12.

---

## Consequence Distribution

| Consequence | Count |
|-------------|--------|
| intron_variant | 1,612,915 |
| intron_variant&non_coding_transcript_variant | 1,194,565 |
| intergenic_variant | 1,107,793 |
| upstream_gene_variant | 305,835 |
| downstream_gene_variant | 282,119 |
| non_coding_transcript_exon_variant | 48,919 |
| 3_prime_UTR_variant | 39,307 |
| synonymous_variant | 11,600 |
| missense_variant | 11,321 |

---

## Interpretation

- The validation set is dominated by **noncoding variants**  
- Coding variants (missense, synonymous) represent a small fraction  
- Intronic and intergenic variants account for the majority of validation candidates  

---

## Key Insight

> Validation workload reflects genome structure: noncoding variation dominates candidate space, while coding variants provide interpretable signal.

---

## System Implications

- Noncoding validation requires:
  - regulatory context  
  - transcriptomic integration (RSP)  
- Coding validation remains more interpretable but less frequent  

---

## Bottom Line

> Stage 12 validation composition reflects biological reality: most candidate variants lie outside coding regions and require context-aware interpretation.