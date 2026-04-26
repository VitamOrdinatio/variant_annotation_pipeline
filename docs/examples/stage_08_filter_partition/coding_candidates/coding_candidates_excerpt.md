# coding_candidates_excerpt.md

## folder path:

`steelsparrow@pop-os:/mnt/storage/delme/stage_08_out_HG002_run$`


## bash cmd:

```bash
alias tsvhead='head -n 5'
tsvhead < coding_candidates.tsv > docs/examples/coding_candidates_excerpt.md
```


## output

```text
sample_id	run_id	source_pipeline	variant_id	chromosome	position	reference_allele	alternate_allele	variant_type	variant_class	quality_flag	gene_id	gene_symbol	transcript_id	consequence	impact_class	clinical_significance	clinvar_significance	population_frequency	gnomad_af	exac_af	thousand_genomes_af	mito_flag	epilepsy_flag	annotation_source	annotation_version	gene_mapping_status	variant_context	variant_effect_severity	qc_status	interpretability_status	frequency_status	clinical_status
HG002	run_2026_04_17_082417	variant_annotation_pipeline	1:924533:A:G	1	924533	A	G	snv	coding	PASS	NA	SAMD11	ENST00000616016.5	synonymous_variant	LOW	NA	NA	0.7498	0.7498	NA	0.4039	False	False	VEP	115	mapped	coding	LOW	pass	interpretable_now	common	missing
HG002	run_2026_04_17_082417	variant_annotation_pipeline	1:946247:G:A	1	946247	G	A	snv	coding	PASS	NA	NOC2L	ENST00000327044.7	synonymous_variant	LOW	NA	NA	0.4419	0.4419	NA	0.0643	False	False	VEP	115	mapped	coding	LOW	pass	interpretable_now	common	missing
HG002	run_2026_04_17_082417	variant_annotation_pipeline	1:952421:A:G	1	952421	A	G	snv	coding	PASS	NA	NOC2L	ENST00000327044.7	synonymous_variant	LOW	NA	NA	0.9223	0.9223	NA	0.9062	False	False	VEP	115	mapped	coding	LOW	pass	interpretable_now	common	missing
HG002	run_2026_04_17_082417	variant_annotation_pipeline	1:953259:T:C	1	953259	T	C	snv	coding	PASS	NA	NOC2L	ENST00000327044.7	synonymous_variant	LOW	NA	NA	0.9227	0.9227	NA	0.907	False	False	VEP	115	mapped	coding	LOW	pass	interpretable_now	common	missing
```

Notes:

- `gene_id` may be NA for certain records due to mapping limitations or annotation source constraints.
- `low_quality` indicates presence of QC flags in contributing variants (e.g., caution flags from Stage 08).