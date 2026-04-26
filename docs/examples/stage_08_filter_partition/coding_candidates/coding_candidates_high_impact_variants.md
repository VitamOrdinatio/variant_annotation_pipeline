# coding_candidates_high_impact_variants.md

An excerpt of high-impact coding variant candidates from stage 08 output on HG002 run

## folder path

`steelsparrow@pop-os:/mnt/storage/delme/stage_08_out_HG002_run$`

## bash cmd:

```bash
awk -F'\t' 'NR==1 || $0 ~ /HIGH/' coding_candidates.tsv | head > docs/examples/coding_candidates_high_impact_variants.md
```

## output

```text
sample_id	run_id	source_pipeline	variant_id	chromosome	position	reference_allele	alternate_allele	variant_type	variant_class	quality_flag	gene_id	gene_symbol	transcript_id	consequence	impact_class	clinical_significance	clinvar_significance	population_frequency	gnomad_af	exac_af	thousand_genomes_af	mito_flag	epilepsy_flag	annotation_source	annotation_version	gene_mapping_status	variant_context	variant_effect_severity	qc_status	interpretability_status	frequency_status	clinical_status
HG002	run_2026_04_17_082417	variant_annotation_pipeline	1:9718724:A:AT	1	9718724	A	AT	insertion	coding	PASS	NA	PIK3CD	ENST00000377346.9	frameshift_variant	HIGH	NA	NA	0	0	NA	NA	False	False	VEP	115	mapped	coding	HIGH	pass	interpretable_now	rare	missing
HG002	run_2026_04_17_082417	variant_annotation_pipeline	1:11846011:A:G	1	11846011	A	G	snv	coding	PASS	NA	NPPA	ENST00000376480.7	stop_lost	HIGH	benign	benign	0.4183	0.1791	NA	0.4183	False	False	VEP	115	mapped	coding	HIGH	pass	interpretable_now	common	benign
HG002	run_2026_04_17_082417	variant_annotation_pipeline	1:26345031:GAAATGAGGCATCA:G	1	26345031	GAAATGAGGCATCA	G	deletion	coding	PASS	NA	CRYBG2	ENST00000308182.10	frameshift_variant	HIGH	NA	NA	0.7034	0.7034	NA	NA	False	False	VEP	115	mapped	coding	HIGH	pass	interpretable_now	common	missing
HG002	run_2026_04_17_082417	variant_annotation_pipeline	1:26345047:AGCAC:A	1	26345047	AGCAC	A	deletion	coding	PASS	NA	CRYBG2	ENST00000308182.10	frameshift_variant	HIGH	NA	NA	0.7101	0.7101	NA	NA	False	False	VEP	115	mapped	coding	HIGH	pass	interpretable_now	common	missing
HG002	run_2026_04_17_082417	variant_annotation_pipeline	1:26345053:GGGGCCCTTCACGACCTCTTTCCAGGTGGGGAACA:G	1	26345053	GGGGCCCTTCACGACCTCTTTCCAGGTGGGGAACA	G	deletion	coding	PASS	NA	CRYBG2	ENST00000308182.10	frameshift_variant	HIGH	NA	NA	0.7374	0.7374	NA	NA	False	False	VEP	115	mapped	coding	HIGH	pass	interpretable_now	common	missing
HG002	run_2026_04_17_082417	variant_annotation_pipeline	1:47219920:CACCAG:C	1	47219920	CACCAG	C	deletion	coding	PASS	NA	TAL1	ENST00000691006.1	frameshift_variant	HIGH	NA	NA	0.009975	0.009975	NA	NA	False	False	VEP	115	mapped	coding	HIGH	pass	interpretable_now	rare	missing
HG002	run_2026_04_17_082417	variant_annotation_pipeline	1:48242556:G:T	1	48242556	G	T	snv	coding	PASS	NA	SLC5A9	ENST00000438567.7	stop_gained	HIGH	benign	benign	0.1142	0.1138	NA	0.1142	False	False	VEP	115	mapped	coding	HIGH	pass	interpretable_now	common	benign
HG002	run_2026_04_17_082417	variant_annotation_pipeline	1:120005329:CTG:C	1	120005329	CTG	C	deletion	coding	PASS	NA	NOTCH2	ENST00000256646.7	frameshift_variant&splice_region_variant	HIGH	NA	NA	NULL	NA	NA	NA	False	False	VEP	115	mapped	splice_region	HIGH	pass	interpretable_now	missing	missing
HG002	run_2026_04_17_082417	variant_annotation_pipeline	1:120436638:AAG:A	1	120436638	AAG	A	deletion	coding	PASS	NA	NBPF8	ENST00000698216.1	frameshift_variant	HIGH	NA	NA	0.7036	0.7036	NA	NA	False	False	VEP	115	mapped	coding	HIGH	pass	interpretable_now	common	missing
```

Notes:

- `gene_id` may be NA for certain records due to mapping limitations or annotation source constraints.
- `low_quality` indicates presence of QC flags in contributing variants (e.g., caution flags from Stage 08).