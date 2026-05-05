# stage_07_missense_examples

## Source

- Source file: `/mnt/storage/vap_runs/HG002/run_2026_04_17_082417/raw_mark_outputs/processed/HG002_run_2026_04_17_082417.annotated_variants.tsv`
- Run ID: `run_2026_04_17_082417`
- Sample/Dataset: `HG002`

## Method

Artifacts are generated using a config-driven extraction system ("Artificer") and curated for clarity.

## Output

| sample_id | run_id | source_pipeline | variant_id | chromosome | position | reference_allele | alternate_allele | quality_flag | gene_id | gene_symbol | transcript_id | consequence | impact_class | impact | variant_class | variant_type | clinical_significance | clinvar_significance | population_frequency | gnomad_af | exac_af | thousand_genomes_af | mito_flag | epilepsy_flag |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| HG002 | run_2026_04_17_082417 | variant_annotation_pipeline | 1:953279:T:C | 1 | 953279 | T | C | PASS | ENSG00000188976 | NOC2L | ENST00000327044.7 | missense_variant | MODERATE | MODERATE | SNV | coding | NA | NA | 0.9227 | 0.9227 | NA | 0.907 | False | False |
| HG002 | run_2026_04_17_082417 | variant_annotation_pipeline | 1:973858:G:C | 1 | 973858 | G | C | PASS | ENSG00000187583 | PLEKHN1 | ENST00000379410.8 | missense_variant | MODERATE | MODERATE | SNV | coding | NA | NA | 0.7766 | 0.7766 | NA | 0.8169 | False | False |
| HG002 | run_2026_04_17_082417 | variant_annotation_pipeline | 1:1072052:G:A | 1 | 1072052 | G | A | PASS | ENSG00000237330 | RNF223 | ENST00000453464.3 | missense_variant | MODERATE | MODERATE | SNV | coding | NA | NA | 0.5321 | 0.5321 | NA | 0.2307 | False | False |
| HG002 | run_2026_04_17_082417 | variant_annotation_pipeline | 1:1072326:G:A | 1 | 1072326 | G | A | PASS | ENSG00000237330 | RNF223 | ENST00000453464.3 | missense_variant | MODERATE | MODERATE | SNV | coding | NA | NA | 0.0002 | 0.0002 | NA | 0 | False | False |
| HG002 | run_2026_04_17_082417 | variant_annotation_pipeline | 1:1334174:T:C | 1 | 1334174 | T | C | PASS | ENSG00000169962 | TAS1R3 | ENST00000339381.6 | missense_variant | MODERATE | MODERATE | SNV | coding | NA | NA | 0.9519 | 0.9519 | NA | 0.9803 | False | False |
| HG002 | run_2026_04_17_082417 | variant_annotation_pipeline | 1:1640423:C:T | 1 | 1640423 | C | T | PASS | ENSG00000248333 | CDK11B | ENST00000341832.11 | missense_variant | MODERATE | MODERATE | SNV | coding | NA | NA | 0.2589 | 0.2589 | NA | NA | False | False |
| HG002 | run_2026_04_17_082417 | variant_annotation_pipeline | 1:1668373:C:T | 1 | 1668373 | C | T | PASS | ENSG00000189339 | SLC35E2B | ENST00000617444.5 | missense_variant | MODERATE | MODERATE | SNV | coding | NA | NA | 0.6271 | 0.6271 | NA | NA | False | False |
| HG002 | run_2026_04_17_082417 | variant_annotation_pipeline | 1:1707555:C:T | 1 | 1707555 | C | T | PASS | ENSG00000008128 | CDK11A | ENST00000404249.8 | missense_variant | MODERATE | MODERATE | SNV | coding | NA | NA | 0.3437 | 0.3437 | NA | 0.8797 | False | False |
| HG002 | run_2026_04_17_082417 | variant_annotation_pipeline | 1:1719406:G:A | 1 | 1719406 | G | A | PASS | ENSG00000008128 | CDK11A | ENST00000404249.8 | missense_variant | MODERATE | MODERATE | SNV | coding | NA | NA | 0.7474 | 0.7474 | NA | 0.4992 | False | False |
| HG002 | run_2026_04_17_082417 | variant_annotation_pipeline | 1:1754601:G:T | 1 | 1754601 | G | T | PASS | ENSG00000008130 | NADK | ENST00000341426.9 | missense_variant | MODERATE | MODERATE | SNV | coding | NA | NA | 0.2494 | 0.2494 | NA | 0.0499 | False | False |

## Interpretation

These examples illustrate MODERATE-impact coding variants (missense).

Notably:

- many have high population frequency  
- these are unlikely to be pathogenic  
- HG002 is a benchmark, non-diseased state

This highlights the importance of integrating allele frequency in downstream filtering (Stage 08–10).

## Notes

- No additional notes.

## Limitations

- Excerpt or summary only.
- Not the full dataset unless explicitly stated.
- No new inference performed.
