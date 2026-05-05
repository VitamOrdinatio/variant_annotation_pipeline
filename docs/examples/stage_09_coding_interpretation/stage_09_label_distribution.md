# stage_09_label_distribution

## Source

- Source file: `/root/dev/portfolio_projects/variant_annotation_pipeline/results/run_2026_04_17_082417/processed/stage_09_coding_interpreted.tsv`
- Run ID: `run_2026_04_17_082417`
- Sample/Dataset: `HG002`

## Method

Artifacts are generated using a config-driven extraction system ("Artificer") and curated for clarity.

## Output

### Coding Interpretation

| Label | Count |
| --- | --- |
| coding_common_or_low_support | 25169 |
| coding_uninterpretable | 1196 |
| lof_or_missense_rare | 1121 |

---

### Functional Impact

| Label | Count |
| --- | --- |
| synonymous | 11601 |
| missense | 11573 |
| splice_relevant | 3154 |
| loss_of_function | 789 |
| other_coding | 369 |

---

### Rarity Flag

| Label | Count |
| --- | --- |
| common | 24674 |
| rare | 1335 |
| low_frequency | 1215 |
| missing | 262 |

---

### Clinical Evidence

| Label | Count |
| --- | --- |
| missing | 19758 |
| benign | 6712 |
| likely_benign | 738 |
| vus | 184 |
| conflicting | 61 |
| pathogenic | 20 |
| likely_pathogenic | 13 |

## Interpretation

- Majority of coding variants are classified as common or low-support (~25k)  
- A small subset (~1.1k) are rare or loss-of-function candidates  
- ~1.2k variants remain uninterpretable  

### Key Insight

> Only a small fraction of variants meet criteria for further investigation.

This reflects realistic genome-wide variation patterns and validates interpretation logic.

## Notes

- No additional notes.

## Limitations

- Excerpt or summary only.
- Not the full dataset unless explicitly stated.
- No new inference performed.
