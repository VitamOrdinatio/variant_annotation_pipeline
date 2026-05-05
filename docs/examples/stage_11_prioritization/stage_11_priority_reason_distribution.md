# stage_11_priority_reason_distribution

## Source

- Source file: `/root/dev/portfolio_projects/variant_annotation_pipeline/results/run_2026_04_17_082417/processed/stage_11_prioritized_variants.tsv`
- Run ID: `run_2026_04_17_082417`
- Sample/Dataset: `HG002`

## Output

| value | count |
| --- | --- |
| noncoding label noncoding_common_or_low_support | 3344586 |
| noncoding label noncoding_uninterpretable | 1152270 |
| noncoding label regulatory_or_transcript_rare | 112242 |
| coding label coding_common_or_low_support | 25169 |
| coding label coding_uninterpretable | 1196 |
| coding label lof_or_missense_rare | 1121 |

## Interpretation

- Noncoding variants dominate prioritization (~4.6M total)  
- Coding variants represent a small subset (~27k)  
- Rare coding variants (~1.1k) form a key candidate group  

### Key Insight

> Prioritization reflects underlying genome structure:
>
> - noncoding space dominates  
> - coding variants provide interpretable signals  

### Additional Insight

> Coding variants provide interpretable signal, while noncoding variants dominate volume.

## Notes

- No additional notes.

## Limitations

- Excerpt or summary only.
- Not the full dataset unless explicitly stated.
- No new inference performed.
