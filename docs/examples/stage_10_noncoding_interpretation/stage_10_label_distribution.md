# stage_10_label_distribution

## Source

- Source file: `/root/dev/portfolio_projects/variant_annotation_pipeline/results/run_2026_04_17_082417/processed/stage_10_noncoding_interpreted.tsv`
- Run ID: `run_2026_04_17_082417`
- Sample/Dataset: `HG002`

## Method

Artifacts are generated using a config-driven extraction system ("Artificer") and curated for clarity.

## Output

### Noncoding Interpretation

| Label | Count |
| --- | --- |
| noncoding_common_or_low_support | 3344586 |
| noncoding_uninterpretable | 1152270 |
| regulatory_or_transcript_rare | 112242 |

---

### Functional Context

| Label | Count |
| --- | --- |
| intronic | 1615376 |
| transcript_associated | 1253498 |
| intergenic | 1107793 |
| proximal | 587954 |
| unknown | 44477 |

---

### Rarity Flag

| Label | Count |
| --- | --- |
| common | 4206244 |
| low_frequency | 156992 |
| rare | 128469 |
| missing | 117393 |

---

### Clinical Evidence

| Label | Count |
| --- | --- |
| missing | 4576020 |
| benign | 31605 |
| likely_benign | 1071 |
| vus | 356 |
| pathogenic | 28 |
| conflicting | 13 |
| likely_pathogenic | 5 |

## Interpretation

- Majority of noncoding variants (~3.3M) are classified as common or low-support  
- A large subset (~1.15M) remains uninterpretable  
- A smaller subset (~112k) represents rare variants in regulatory or transcript-associated regions  

### Key Insight

> Most noncoding variants cannot be interpreted using current annotation frameworks.

This reflects:

- limitations in regulatory annotation  
- incomplete understanding of noncoding function  
- reliance on additional data (e.g., transcriptomics, epigenomics)

### Important Distinction

Unlike coding variants:

- noncoding interpretation is context-dependent  
- deterministic labeling identifies candidates, not conclusions  

## Notes

- No additional notes.

## Limitations

- Excerpt or summary only.
- Not the full dataset unless explicitly stated.
- No new inference performed.
