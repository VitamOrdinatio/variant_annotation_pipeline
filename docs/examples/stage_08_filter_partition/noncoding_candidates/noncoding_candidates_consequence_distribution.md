# noncoding_consequence_distribution

## Source

- Source file: `/mnt/storage/vap_runs/HG002/run_2026_04_17_082417/raw_mark_outputs/processed/noncoding_candidates.tsv`
- Run ID: `run_2026_04_17_082417`
- Sample/Dataset: `HG002`

## Method

Artifacts are generated using a config-driven extraction system ("Artificer") and curated for clarity.

## Output

| value | count |
| --- | --- |
| intron_variant | 1612915 |
| intron_variant&non_coding_transcript_variant | 1194565 |
| intergenic_variant | 1107793 |
| upstream_gene_variant | 305835 |
| downstream_gene_variant | 282119 |
| non_coding_transcript_exon_variant | 48919 |
| 3_prime_UTR_variant | 39307 |
| intron_variant&NMD_transcript_variant | 8531 |
| 5_prime_UTR_variant | 5129 |
| splice_polypyrimidine_tract_variant&intron_variant | 2028 |
| splice_polypyrimidine_tract_variant&intron_variant&non_coding_transcript_variant | 922 |
| splice_donor_region_variant&intron_variant | 345 |
| splice_donor_region_variant&intron_variant&non_coding_transcript_variant | 270 |
| 3_prime_UTR_variant&NMD_transcript_variant | 186 |
| splice_donor_5th_base_variant&intron_variant&non_coding_transcript_variant | 100 |
| splice_donor_5th_base_variant&intron_variant | 88 |
| mature_miRNA_variant | 17 |
| stop_retained_variant | 14 |
| 5_prime_UTR_variant&NMD_transcript_variant | 3 |
| coding_sequence_variant | 3 |

## Interpretation

- Noncoding variation is dominated by:
  - intronic variants (~1.6M+)  
  - intergenic variants (~1.1M)

- Additional regulatory contexts include:
  - upstream/downstream gene variants  
  - UTR variants  
  - splice-region variants  

### Key Insight

> The vast majority of genomic variation occurs outside coding regions.

These variants:

- are difficult to interpret without additional context  
- require integration with regulatory and transcriptomic data  

This distribution is consistent with expected patterns in human WGS data.

## Notes

- No additional notes.

## Limitations

- Excerpt or summary only.
- Not the full dataset unless explicitly stated.
- No new inference performed.
