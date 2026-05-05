# Stage 11 — Gene Burden Overview

## Overview

This artifact summarizes the distribution of prioritized-variant records across gene symbols.

Counts reflect the number of Stage 11 records associated with each gene.

---

## Top Genes by Record Count (Excluding NA)

| Rank | Gene Symbol | Record Count |
|------|------------|--------------|
| 1 | CSMD1 | 8,781 |
| 2 | RBFOX1 | 7,094 |
| 3 | PTPRD | 4,738 |
| 4 | CNTNAP2 | 4,577 |
| 5 | LRP1B | 3,963 |
| 6 | SGCZ | 3,473 |
| 7 | EYS | 3,452 |
| 8 | PCDH15 | 3,371 |
| 9 | WWOX | 3,249 |
| 10 | CDH13 | 3,237 |
| 11 | CNTN5 | 3,236 |
| 12 | CTNNA3 | 3,024 |
| 13 | FHIT | 2,981 |
| 14 | MACROD2 | 2,857 |
| 15 | MAGI2 | 2,850 |
| 16 | ROBO2 | 2,848 |
| 17 | PRKN | 2,754 |
| 18 | DLG2 | 2,590 |
| 19 | PWRN1 | 2,523 |

---

## Unassigned Records

| Category | Record Count |
|----------|--------------|
| NA (no gene_symbol) | 2,086,508 |

---

## Interpretation

- A substantial number of records (~2.08M) lack a gene symbol, reflecting:
  - intergenic variants  
  - incomplete annotation  
  - noncoding regions without gene assignment  

- Genes with high record counts tend to be:
  - large in genomic span  
  - rich in intronic or regulatory sequence  
  - highly polymorphic  


> These patterns are consistent with known large, mutation-dense genes in the human genome.

---

## Key Insight

> High record count per gene does NOT imply biological importance or disease relevance.

Instead, these counts reflect:

- genomic architecture  
- mutation density  
- annotation coverage  

---

## Important Considerations

- HG002 is a healthy benchmark genome  
- prioritized records do not imply pathogenicity  
- gene-level counts are descriptive, not diagnostic  

---

## Role in the Pipeline

This artifact provides:

- a sanity check on gene-level aggregation  
- insight into distribution of variant records  
- context for downstream prioritization  

---

## Bottom Line

> Gene-level record counts reflect genome structure—not disease signal—and must be interpreted with caution.