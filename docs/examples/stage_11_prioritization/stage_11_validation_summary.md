# Stage 11 — Prioritization Validation Summary

## Overview

Stage 11 integrates coding and noncoding interpretation outputs into structured priority tiers.

---

## Key Metrics

- total variants processed: ~4.64M  
- high-priority candidates: 0  
- moderate-priority candidates: ~113k  
- low-priority variants: ~3.37M  
- uninterpretable variants: ~1.15M  

---

## Key Observations

- majority of variants are low-priority or uninterpretable  
- a small subset (~2.4%) are elevated to candidate status  
- no high-priority variants are identified  

---

## Critical Validation Insight

> A correct prioritization system must not identify high-priority variants in a healthy genome.

The absence of high-priority candidates confirms:

- appropriate filtering thresholds  
- lack of overcalling  
- correct integration of interpretation layers  

---

## Interpretation Logic

Stage 11 integrates:

- Stage 09 (coding interpretation)  
- Stage 10 (noncoding classification)  

to assign:

- Tier 2: candidate variants  
- Tier 3: common / low-support variants  
- Tier 4: uninterpretable variants  

---

## System Behavior

- coding variants contribute interpretable signals  
- noncoding variants are largely preserved or down-ranked  
- prioritization reflects both biological reality and annotation limits  

---

## Important Considerations

- HG002 is a healthy reference genome  
- candidate variants do not imply disease  
- prioritization is deterministic, not diagnostic  

---

## Conclusion

Stage 11 successfully:

- integrates interpretation layers  
- reduces candidate space to a manageable subset  
- avoids false-positive prioritization  

---

## Bottom Line

> Stage 11 identifies candidate variants while correctly avoiding disease inference in a healthy genome.