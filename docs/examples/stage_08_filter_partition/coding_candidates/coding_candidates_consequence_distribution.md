# coding_consequence_distribution

## Source

- Source file: `/mnt/storage/vap_runs/HG002/run_2026_04_17_082417/raw_mark_outputs/processed/coding_candidates.tsv`
- Run ID: `run_2026_04_17_082417`
- Sample/Dataset: `HG002`

## Method

Artifacts are generated using a config-driven extraction system ("Artificer") and curated for clarity.

## Output

| value | count |
| --- | --- |
| synonymous_variant | 11600 |
| missense_variant | 11321 |
| frameshift_variant | 310 |
| splice_region_variant&synonymous_variant | 259 |
| missense_variant&splice_region_variant | 249 |
| inframe_deletion | 202 |
| inframe_insertion | 158 |
| stop_gained | 99 |
| stop_lost | 24 |
| start_lost | 10 |
| inframe_insertion&stop_retained_variant | 7 |
| frameshift_variant&splice_region_variant | 6 |
| frameshift_variant&splice_donor_region_variant | 3 |
| missense_variant&NMD_transcript_variant | 3 |
| stop_gained&frameshift_variant | 3 |
| frameshift_variant&start_lost&start_retained_variant | 2 |
| frameshift_variant&stop_lost | 2 |
| inframe_deletion&splice_region_variant | 2 |
| inframe_insertion&splice_region_variant | 2 |
| protein_altering_variant | 2 |

## Interpretation

## Interpretation

- Coding variation is dominated by:
  - synonymous variants (~11.6k)  
  - missense variants (~11.3k)

- High-impact variants are rare:
  - frameshift variants (~310)  
  - stop_gained variants (~99)

### Key Insight

> Most coding variants are **benign or tolerated**, while functionally disruptive variants are rare.

This is consistent with expected patterns in human whole-genome sequencing data.

## Notes

- No additional notes.

## Limitations

- Excerpt or summary only.
- Not the full dataset unless explicitly stated.
- No new inference performed.
