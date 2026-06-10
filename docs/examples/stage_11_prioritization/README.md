# Stage 11 — Variant Prioritization (VAP)

## Overview

Stage 11 integrates coding and noncoding interpretation outputs into deterministic priority tiers for downstream review.

This stage represents the transition from:

- interpreted variant evidence  
→ to  
- prioritized candidate sets  

---

## Key Metrics (HG002)

- total variants processed: ~4.64M  
- high-priority candidates: 0  
- moderate-priority candidates: ~113k  
- low-priority variants: ~3.37M  
- uninterpretable variants: ~1.15M  

### Signal Compression

> Stage 11 reduces ~4.6 million variants to ~113k candidates, and ultimately 0 high-priority calls in a healthy genome.

---

## Why This Stage Matters

> A correct prioritization system must avoid false positives.

HG002 is a healthy benchmark genome.  
The absence of high-priority variants demonstrates:

- appropriate filtering thresholds  
- correct integration of interpretation layers  
- lack of overcalling  

---

## Hallmark Artifacts

**Recommended reading order:** Validation Summary → Summary → Candidate Composition  → Tier Distribution → Candidate Examples → Gene Burden → Coding Candidate Breakdown

- [Stage 11 Validation Summary](./stage_11_validation_summary.md)  
  System-level validation of prioritization logic and biological correctness.

- [Stage 11 Summary](./stage_11_summary.md)  
  Core metrics, distributions, and system behavior.

- [Candidate Composition](./stage_11_candidate_composition.md)  
  Distribution of Tier 2 candidates by coding vs noncoding origin.

- [Priority Tier Distribution](./stage_11_priority_tier_distribution.md)  
  Breakdown of variants into Tier 2–4 categories.

- [Priority Reason Distribution](./stage_11_priority_reason_distribution.md)  
  Contribution of coding vs noncoding interpretation to prioritization.

- [Candidate Variant Examples](./stage_11_candidate_variant_examples.md)  
  Representative moderate-priority variants for review.

- [Gene Burden Overview](./stage_11_gene_burden_overview.md)  
  Distribution of prioritized records across genes.

- [Coding Candidate Breakdown](./stage_11_coding_candidate_breakdown.md)  
  Functional, rarity, and clinical composition of Tier 2 coding candidates.

### Coding Candidate Composition

- ~92% missense variants  
- ~8% loss-of-function variants  
- ~88% lack clinical annotation  

> Most coding candidates represent uncertain biological signal requiring further context.

---

## Interpretation Framework

Stage 11 assigns variants into:

### Tier 2 — Moderate Candidates
- rare coding variants  
- regulatory or transcript-associated variants  

### Tier 3 — Low Support / Common
- high-frequency variants  
- low-impact variants  

### Tier 4 — Uninterpretable
- insufficient annotation  
- QC-limited records  

---

## Key Insights

### Controlled Prioritization

> Only ~2.4% of variants are elevated to candidate status.

---

### Biological Consistency

> Most variants are correctly deprioritized in a healthy genome.

---

### System Integrity

> No high-priority variants confirms correct behavior.

---

## Important Considerations

- HG002 is a healthy benchmark genome  
- candidate variants do not imply disease  
- prioritization is deterministic, not diagnostic  

---

## Role in Pipeline

```text
Stage 09 + Stage 10
↓
Stage 11 (prioritization)
↓
Stage 12 (validation)
↓
Stage 13 (reporting)
```

---

## Bottom Line

> Stage 11 identifies candidate variants while correctly avoiding disease inference in a healthy genome.

See also: [HG002 Benchmarking Case Study](../../case_studies/hg002/README.md)