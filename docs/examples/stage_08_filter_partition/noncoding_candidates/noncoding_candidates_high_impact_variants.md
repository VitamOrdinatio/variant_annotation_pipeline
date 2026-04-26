# noncoding_candidates_high_impact_variants.md

An excerpt of high-impact noncoding variant candidates from stage 08 output on HG002 run

**Note:**
These records appear in the noncoding/splice-region candidate space because Stage 08 partitions by `variant_context`, not solely by `variant_class`. Some splice-region records may retain `variant_class=coding` while being routed for noncoding/splice-aware interpretation.


## folder path

`steelsparrow@pop-os:/mnt/storage/delme/stage_08_out_HG002_run$`


## bash cmd:

```bash
awk -F'\t' 'NR==1 || $0 ~ /HIGH/' noncoding_candidates.tsv | head > docs/examples/noncoding_candidates_high_impact_variants.md
```


## output

```text
sample_id	run_id	source_pipeline	variant_id	chromosome	position	reference_allele	alternate_allele	variant_type	variant_class	quality_flag	gene_id	gene_symbol	transcript_id	consequence	impact_class	clinical_significance	clinvar_significance	population_frequency	gnomad_af	exac_af	thousand_genomes_af	mito_flag	epilepsy_flag	annotation_source	annotation_version	gene_mapping_status	variant_context	variant_effect_severity	qc_status	interpretability_status	frequency_status	clinical_status
HG002	run_2026_04_17_082417	variant_annotation_pipeline	1:1063202:G:C	1	1063202	G	C	snv	coding	PASS	NA	PTPN11BP	ENST00000412397.2	splice_donor_variant&non_coding_transcript_variant	HIGH	NA	NA	0.4846	0.4846	NA	0.0673	False	False	VEP	115	mapped	splice_region	HIGH	pass	interpretable_now	common	missing
HG002	run_2026_04_17_082417	variant_annotation_pipeline	1:2855629:G:A	1	2855629	G	A	snv	coding	PASS	NA	ENSG00000295089	ENST00000727914.1	splice_donor_variant&non_coding_transcript_variant	HIGH	NA	NA	0.2678	0.2678	NA	0.0371	False	False	VEP	115	mapped	splice_region	HIGH	pass	interpretable_now	common	missing
HG002	run_2026_04_17_082417	variant_annotation_pipeline	1:9244919:CCCCAGGCA:C	1	9244919	CCCCAGGCA	C	deletion	coding	PASS	NA	H6PD	ENST00000377403.7	splice_acceptor_variant&5_prime_UTR_variant&intron_variant	HIGH	NA	NA	NULL	NA	NA	NA	False	False	VEP	115	mapped	splice_region	HIGH	pass	interpretable_now	missing	missing
HG002	run_2026_04_17_082417	variant_annotation_pipeline	1:16681711:C:G	1	16681711	C	G	snv	coding	PASS	NA	ENSG00000280114	ENST00000624828.1	splice_donor_variant&non_coding_transcript_variant	HIGH	NA	NA	0.2926	0.2926	NA	NA	False	False	VEP	115	mapped	splice_region	HIGH	pass	interpretable_now	common	missing
HG002	run_2026_04_17_082417	variant_annotation_pipeline	1:23670909:A:T	1	23670909	A	T	snv	coding	PASS	NA	EEF1A1P48	ENST00000451300.2	splice_acceptor_variant&non_coding_transcript_variant	HIGH	NA	NA	0.292	0.2139	NA	0.292	False	False	VEP	115	mapped	splice_region	HIGH	pass	interpretable_now	common	missing
HG002	run_2026_04_17_082417	variant_annotation_pipeline	1:44206707:CTAAAA:C,CTAAAATAAAATAAAA	1	44206707	CTAAAA	C,CTAAAATAAAATAAAA	complex	coding	PASS	NA	ENSG00000302536	ENST00000787675.1	splice_acceptor_variant&splice_polypyrimidine_tract_variant&intron_variant&non_coding_transcript_variant	HIGH	NA	NA	0.481	0.481	NA	NA	False	False	VEP	115	mapped	splice_region	HIGH	pass	interpretable_now	common	missing
HG002	run_2026_04_17_082417	variant_annotation_pipeline	1:53342986:C:T	1	53342986	C	T	snv	coding	PASS	NA	ENSG00000226938	ENST00000792492.1	splice_acceptor_variant&non_coding_transcript_variant	HIGH	NA	NA	0.4516	0.3604	NA	0.4516	False	False	VEP	115	mapped	splice_region	HIGH	pass	interpretable_now	common	missing
HG002	run_2026_04_17_082417	variant_annotation_pipeline	1:83096978:A:G	1	83096978	A	G	snv	coding	PASS	NA	LINC01362	ENST00000452901.5	splice_donor_variant&non_coding_transcript_variant	HIGH	NA	NA	1	0.9940	NA	1	False	False	VEP	115	mapped	splice_region	HIGH	pass	interpretable_now	common	missing
HG002	run_2026_04_17_082417	variant_annotation_pipeline	1:86636910:T:C	1	86636910	T	C	snv	coding	PASS	NA	CLCA3P	ENST00000466454.1	splice_donor_variant&non_coding_transcript_variant	HIGH	NA	NA	0.0405	0.0405	NA	0.0068	False	False	VEP	115	mapped	splice_region	HIGH	pass	interpretable_now	low_frequency	missing
```

Notes:

- `gene_id` may be NA for certain records due to mapping limitations or annotation source constraints.
- `low_quality` indicates presence of QC flags in contributing variants (e.g., caution flags from Stage 08).