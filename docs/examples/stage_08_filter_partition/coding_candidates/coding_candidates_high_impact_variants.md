# coding_high_impact_examples

## Source

- Source file: `/mnt/storage/vap_runs/HG002/run_2026_04_17_082417/raw_mark_outputs/processed/coding_candidates.tsv`
- Run ID: `run_2026_04_17_082417`
- Sample/Dataset: `HG002`

## Method

Artifacts are generated using a config-driven extraction system ("Artificer") and curated for clarity.

## Output

| sample_id | run_id | source_pipeline | variant_id | chromosome | position | reference_allele | alternate_allele | variant_type | variant_class | quality_flag | gene_id | gene_symbol | transcript_id | consequence | impact_class | clinical_significance | clinvar_significance | population_frequency | gnomad_af | exac_af | thousand_genomes_af | mito_flag | epilepsy_flag | annotation_source | annotation_version | gene_mapping_status | variant_context | variant_effect_severity | qc_status | interpretability_status | frequency_status | clinical_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| HG002 | run_2026_04_17_082417 | variant_annotation_pipeline | 1:9718724:A:AT | 1 | 9718724 | A | AT | insertion | coding | PASS | ENSG00000171608 | PIK3CD | ENST00000377346.9 | frameshift_variant | HIGH | NA | NA | 0 | 0 | NA | NA | False | False | VEP | 115 | mapped | coding | HIGH | pass | interpretable_now | rare | missing |
| HG002 | run_2026_04_17_082417 | variant_annotation_pipeline | 1:11846011:A:G | 1 | 11846011 | A | G | snv | coding | PASS | ENSG00000175206 | NPPA | ENST00000376480.7 | stop_lost | HIGH | benign | benign | 0.4183 | 0.1791 | NA | 0.4183 | False | False | VEP | 115 | mapped | coding | HIGH | pass | interpretable_now | common | benign |
| HG002 | run_2026_04_17_082417 | variant_annotation_pipeline | 1:26345031:GAAATGAGGCATCA:G | 1 | 26345031 | GAAATGAGGCATCA | G | deletion | coding | PASS | ENSG00000176092 | CRYBG2 | ENST00000308182.10 | frameshift_variant | HIGH | NA | NA | 0.7034 | 0.7034 | NA | NA | False | False | VEP | 115 | mapped | coding | HIGH | pass | interpretable_now | common | missing |
| HG002 | run_2026_04_17_082417 | variant_annotation_pipeline | 1:26345047:AGCAC:A | 1 | 26345047 | AGCAC | A | deletion | coding | PASS | ENSG00000176092 | CRYBG2 | ENST00000308182.10 | frameshift_variant | HIGH | NA | NA | 0.7101 | 0.7101 | NA | NA | False | False | VEP | 115 | mapped | coding | HIGH | pass | interpretable_now | common | missing |
| HG002 | run_2026_04_17_082417 | variant_annotation_pipeline | 1:26345053:GGGGCCCTTCACGACCTCTTTCCAGGTGGGGAACA:G | 1 | 26345053 | GGGGCCCTTCACGACCTCTTTCCAGGTGGGGAACA | G | deletion | coding | PASS | ENSG00000176092 | CRYBG2 | ENST00000308182.10 | frameshift_variant | HIGH | NA | NA | 0.7374 | 0.7374 | NA | NA | False | False | VEP | 115 | mapped | coding | HIGH | pass | interpretable_now | common | missing |
| HG002 | run_2026_04_17_082417 | variant_annotation_pipeline | 1:47219920:CACCAG:C | 1 | 47219920 | CACCAG | C | deletion | coding | PASS | ENSG00000162367 | TAL1 | ENST00000691006.1 | frameshift_variant | HIGH | NA | NA | 0.009975 | 0.009975 | NA | NA | False | False | VEP | 115 | mapped | coding | HIGH | pass | interpretable_now | rare | missing |
| HG002 | run_2026_04_17_082417 | variant_annotation_pipeline | 1:48242556:G:T | 1 | 48242556 | G | T | snv | coding | PASS | ENSG00000117834 | SLC5A9 | ENST00000438567.7 | stop_gained | HIGH | benign | benign | 0.1142 | 0.1138 | NA | 0.1142 | False | False | VEP | 115 | mapped | coding | HIGH | pass | interpretable_now | common | benign |
| HG002 | run_2026_04_17_082417 | variant_annotation_pipeline | 1:120005329:CTG:C | 1 | 120005329 | CTG | C | deletion | coding | PASS | ENSG00000134250 | NOTCH2 | ENST00000256646.7 | frameshift_variant&splice_region_variant | HIGH | NA | NA | NULL | NA | NA | NA | False | False | VEP | 115 | mapped | splice_region | HIGH | pass | interpretable_now | missing | missing |
| HG002 | run_2026_04_17_082417 | variant_annotation_pipeline | 1:120436638:AAG:A | 1 | 120436638 | AAG | A | deletion | coding | PASS | ENSG00000270231 | NBPF8 | ENST00000698216.1 | frameshift_variant | HIGH | NA | NA | 0.7036 | 0.7036 | NA | NA | False | False | VEP | 115 | mapped | coding | HIGH | pass | interpretable_now | common | missing |
| HG002 | run_2026_04_17_082417 | variant_annotation_pipeline | 1:120466107:C:G | 1 | 120466107 | C | G | snv | coding | PASS | ENSG00000270231 | NBPF8 | ENST00000698216.1 | stop_gained | HIGH | NA | NA | 0.4942 | 0.4942 | NA | NA | False | False | VEP | 115 | mapped | coding | HIGH | pass | interpretable_now | common | missing |

## Interpretation

These examples highlight HIGH-impact coding variants, including:

- frameshift variants  
- stop_gained variants  
- stop_lost variants  

### Key Observations

- Some HIGH-impact variants occur at high population frequency  
- Several are annotated as benign in ClinVar  

### Key Insight

> Functional impact ≠ clinical pathogenicity

This demonstrates the necessity of integrating:

- population frequency  
- clinical databases  
- gene-level context  

in downstream prioritization (Stage 09–11).

## Notes

- No additional notes.

## Limitations

- Excerpt or summary only.
- Not the full dataset unless explicitly stated.
- No new inference performed.
