# noncoding_high_impact_examples

## Source

- Source file: `/mnt/storage/vap_runs/HG002/run_2026_04_17_082417/raw_mark_outputs/processed/noncoding_candidates.tsv`
- Run ID: `run_2026_04_17_082417`
- Sample/Dataset: `HG002`

## Method

Artifacts are generated using a config-driven extraction system ("Artificer") and curated for clarity.

## Output

| sample_id | run_id | source_pipeline | variant_id | chromosome | position | reference_allele | alternate_allele | variant_type | variant_class | quality_flag | gene_id | gene_symbol | transcript_id | consequence | impact_class | clinical_significance | clinvar_significance | population_frequency | gnomad_af | exac_af | thousand_genomes_af | mito_flag | epilepsy_flag | annotation_source | annotation_version | gene_mapping_status | variant_context | variant_effect_severity | qc_status | interpretability_status | frequency_status | clinical_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| HG002 | run_2026_04_17_082417 | variant_annotation_pipeline | 12:45554579:AACTGGAAACATTGCGCAGGGGCCATGCTAATCTTCTCTGTATCGTTCCAATTTTAGTATATGTGCTGCCGAAGCGAGCACAT:A | 12 | 45554579 | AACTGGAAACATTGCGCAGGGGCCATGCTAATCTTCTCTGTATCGTTCCAATTTTAGTATATGTGCTGCCGAAGCGAGCACAT | A | deletion | unknown | PASS | ENSG00000283545 | U6 | ENST00000384129.2 | transcript_ablation | HIGH | NA | NA | 1 | 1 | NA | NA | False | False | VEP | 115 | mapped | unknown | HIGH | caution | unsupported_currently | common | missing |
| HG002 | run_2026_04_17_082417 | variant_annotation_pipeline | 2:153208061:ATTTTTTTTTTTTTTTTTTTAAAAGGACATGAGGATGATTTATTTGGCAGTCAGATCTTAAGAGGGCAGCAGAACTAGCAAATGGCCAACCCTGAGCCCAAATG:A | 2 | 153208061 | ATTTTTTTTTTTTTTTTTTTAAAAGGACATGAGGATGATTTATTTGGCAGTCAGATCTTAAGAGGGCAGCAGAACTAGCAAATGGCCAACCCTGAGCCCAAATG | A | deletion | unknown | PASS | ENSG00000226338 | NA | ENST00000443733.1 | transcript_ablation | HIGH | NA | NA | 0.9273 | 0.9273 | NA | NA | False | False | VEP | 115 | mapped | unknown | HIGH | caution | unsupported_currently | common | missing |

## Interpretation

These examples illustrate HIGH-impact annotations in noncoding contexts, including:

- transcript_ablation events  
- structural disruptions in noncoding transcripts  

### Key Observations

- some variants occur at very high population frequency  
- interpretability is marked as "unsupported_currently"  

### Key Insight

> HIGH annotation impact does not imply biological or clinical significance in noncoding regions.

This reflects:

- limitations of current annotation frameworks  
- lack of regulatory interpretation for many noncoding elements  

These variants require:

- specialized regulatory annotation  
- experimental validation  
- integration with functional data  

before biological conclusions can be drawn.

## Notes

- No additional notes.

## Limitations

- Excerpt or summary only.
- Not the full dataset unless explicitly stated.
- No new inference performed.
