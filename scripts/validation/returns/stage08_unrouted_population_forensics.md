# Stage08 Unrouted Population Forensics

Generated: 2026-06-17T18:53:56Z

Definition:

```text
unrouted_population = Stage08 variant_ids - union(Stage09 variant_ids, Stage10 variant_ids)
```

## run_2026_05_30_071639

### Files

Stage08: `results/run_2026_05_30_071639/processed/stage_08_vdb_ready_variants.tsv`
Stage09: `results/run_2026_05_30_071639/processed/coding_candidates.tsv`
Stage10: `results/run_2026_05_30_071639/processed/noncoding_candidates.tsv`

### Counts

| Metric | Count |
|---|---:|
| Stage08 rows | 674593 |
| Stage09 rows | 23907 |
| Stage10 rows | 648322 |
| Stage08 distinct variant_ids | 674593 |
| Routed distinct variant_ids | 672229 |
| Unrouted distinct variant_ids | 2364 |
| Unrouted Stage08 rows | 2364 |

### Unrouted Population: variant_context

```text
2364	splice_region
```

### Unrouted Population: variant_class

```text
2364	coding
```

### Unrouted Population: gene_mapping_status

```text
2364	mapped
```

### Unrouted Population: qc_status

```text
2364	pass
```

### Unrouted Population: interpretability_status

```text
2364	interpretable_now
```

### Unrouted Population: frequency_status

```text
2109	common
116	low_frequency
102	rare
37	missing
```

### Unrouted Population: clinical_status

```text
```

### First 10 Unrouted Rows

```text
sample_id	run_id	source_pipeline	variant_id	chromosome	position	reference_allele	alternate_allele	variant_type	variant_class	quality_flag	gene_id	gene_symbol	transcript_id	consequence	impact_class	clinical_significance	clinvar_significance	population_frequency	gnomad_af	exac_af	thousand_genomes_af	mito_flag	epilepsy_flag	annotation_source	annotation_version	gene_mapping_status	variant_context	variant_effect_severity	qc_status	interpretability_status	frequency_status	clinical_status
ERR10619203	run_2026_05_30_071639	variant_annotation_pipeline	1:17375:A:G	1	17375	A	G	snv	coding	PASS	ENSG00000227232	WASH7P	ENST00000488147.2	splice_region_variant&splice_polypyrimidine_tract_variant&intron_variant&non_coding_transcript_variant	LOW	NA	NA	0.009963	0.009963	NA	NA	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	rare	missing
ERR10619203	run_2026_05_30_071639	variant_annotation_pipeline	1:17746:A:G	1	17746	A	G	snv	coding	PASS	ENSG00000310526	WASH7P	ENST00000831140.1	splice_region_variant&splice_polypyrimidine_tract_variant&intron_variant&non_coding_transcript_variant	LOW	NA	NA	0.1499	0.1499	NA	NA	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	missing
ERR10619203	run_2026_05_30_071639	variant_annotation_pipeline	1:1041950:T:C	1	1041950	T	C	snv	coding	PASS	ENSG00000188157	AGRN	ENST00000379370.7	splice_region_variant&splice_polypyrimidine_tract_variant&intron_variant	LOW	benign	benign	0.8852	0.8852	NA	0.6899	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	benign
ERR10619203	run_2026_05_30_071639	variant_annotation_pipeline	1:1721589:C:T	1	1721589	C	T	snv	coding	PASS	ENSG00000008128	CDK11A	ENST00000404249.8	splice_region_variant&intron_variant	LOW	NA	NA	0.7474	0.7474	NA	0.4985	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	missing
ERR10619203	run_2026_05_30_071639	variant_annotation_pipeline	1:1735814:T:C	1	1735814	T	C	snv	coding	PASS	ENSG00000293188	NA	ENST00000577672.2	splice_region_variant&splice_polypyrimidine_tract_variant&intron_variant&non_coding_transcript_variant	LOW	NA	NA	0.7001	0.7001	NA	0.4349	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	missing
ERR10619203	run_2026_05_30_071639	variant_annotation_pipeline	1:1765220:A:G	1	1765220	A	G	snv	coding	PASS	ENSG00000008130	NADK	ENST00000341426.9	splice_region_variant&intron_variant	LOW	NA	NA	0.7412	0.7412	NA	0.4955	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	missing
ERR10619203	run_2026_05_30_071639	variant_annotation_pipeline	1:2596694:T:C	1	2596694	T	C	snv	coding	PASS	ENSG00000142606	MMEL1	ENST00000378412.8	splice_region_variant&splice_polypyrimidine_tract_variant&intron_variant	LOW	NA	NA	0.5016	0.5016	NA	0.3835	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	missing
ERR10619203	run_2026_05_30_071639	variant_annotation_pipeline	1:3831039:T:C	1	3831039	T	C	snv	coding	PASS	ENSG00000116198	CEP104	ENST00000378230.8	splice_region_variant&intron_variant	LOW	benign	benign	0.9198	0.7895	NA	0.9198	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	benign
ERR10619203	run_2026_05_30_071639	variant_annotation_pipeline	1:3890079:T:A	1	3890079	T	A	snv	coding	PASS	ENSG00000198912	C1ORF174	ENST00000361605.4	splice_region_variant&splice_polypyrimidine_tract_variant&intron_variant	LOW	NA	NA	0.5696	0.4215	NA	0.5696	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	missing
ERR10619203	run_2026_05_30_071639	variant_annotation_pipeline	1:5088375:TA:T	1	5088375	TA	T	deletion	coding	PASS	ENSG00000231510	LINC02782	ENST00000443270.1	splice_region_variant&splice_polypyrimidine_tract_variant&intron_variant&non_coding_transcript_variant	LOW	NA	NA	0.1579	0.1579	NA	NA	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	missing
```

---

## run_2026_06_01_124134

### Files

Stage08: `results/run_2026_06_01_124134/processed/stage_08_vdb_ready_variants.tsv`
Stage09: `results/run_2026_06_01_124134/processed/coding_candidates.tsv`
Stage10: `results/run_2026_06_01_124134/processed/noncoding_candidates.tsv`

### Counts

| Metric | Count |
|---|---:|
| Stage08 rows | 678379 |
| Stage09 rows | 24149 |
| Stage10 rows | 651824 |
| Stage08 distinct variant_ids | 678379 |
| Routed distinct variant_ids | 675973 |
| Unrouted distinct variant_ids | 2406 |
| Unrouted Stage08 rows | 2406 |

### Unrouted Population: variant_context

```text
2406	splice_region
```

### Unrouted Population: variant_class

```text
2406	coding
```

### Unrouted Population: gene_mapping_status

```text
2406	mapped
```

### Unrouted Population: qc_status

```text
2406	pass
```

### Unrouted Population: interpretability_status

```text
2406	interpretable_now
```

### Unrouted Population: frequency_status

```text
2139	common
132	low_frequency
98	rare
37	missing
```

### Unrouted Population: clinical_status

```text
```

### First 10 Unrouted Rows

```text
sample_id	run_id	source_pipeline	variant_id	chromosome	position	reference_allele	alternate_allele	variant_type	variant_class	quality_flag	gene_id	gene_symbol	transcript_id	consequence	impact_class	clinical_significance	clinvar_significance	population_frequency	gnomad_af	exac_af	thousand_genomes_af	mito_flag	epilepsy_flag	annotation_source	annotation_version	gene_mapping_status	variant_context	variant_effect_severity	qc_status	interpretability_status	frequency_status	clinical_status
ERR10619207	run_2026_06_01_124134	variant_annotation_pipeline	1:16856:A:G	1	16856	A	G	snv	coding	PASS	ENSG00000310526	WASH7P	ENST00000831140.1	splice_donor_variant&non_coding_transcript_variant	HIGH	NA	NA	0.02175	0.02175	NA	NA	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	HIGH	pass	interpretable_now	low_frequency	missing
ERR10619207	run_2026_06_01_124134	variant_annotation_pipeline	1:847806:G:C	1	847806	G	C	snv	coding	PASS	ENSG00000228794	LINC01128	ENST00000666741.3	splice_region_variant&non_coding_transcript_exon_variant	LOW	NA	NA	0.0144	0.0040	NA	0.0144	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	low_frequency	missing
ERR10619207	run_2026_06_01_124134	variant_annotation_pipeline	1:1041950:T:C	1	1041950	T	C	snv	coding	PASS	ENSG00000188157	AGRN	ENST00000379370.7	splice_region_variant&splice_polypyrimidine_tract_variant&intron_variant	LOW	benign	benign	0.8852	0.8852	NA	0.6899	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	benign
ERR10619207	run_2026_06_01_124134	variant_annotation_pipeline	1:1721589:C:T	1	1721589	C	T	snv	coding	PASS	ENSG00000008128	CDK11A	ENST00000404249.8	splice_region_variant&intron_variant	LOW	NA	NA	0.7474	0.7474	NA	0.4985	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	missing
ERR10619207	run_2026_06_01_124134	variant_annotation_pipeline	1:1735814:T:C	1	1735814	T	C	snv	coding	PASS	ENSG00000293188	NA	ENST00000577672.2	splice_region_variant&splice_polypyrimidine_tract_variant&intron_variant&non_coding_transcript_variant	LOW	NA	NA	0.7001	0.7001	NA	0.4349	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	missing
ERR10619207	run_2026_06_01_124134	variant_annotation_pipeline	1:1765220:A:G	1	1765220	A	G	snv	coding	PASS	ENSG00000008130	NADK	ENST00000341426.9	splice_region_variant&intron_variant	LOW	NA	NA	0.7412	0.7412	NA	0.4955	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	missing
ERR10619207	run_2026_06_01_124134	variant_annotation_pipeline	1:2596694:T:C	1	2596694	T	C	snv	coding	PASS	ENSG00000142606	MMEL1	ENST00000378412.8	splice_region_variant&splice_polypyrimidine_tract_variant&intron_variant	LOW	NA	NA	0.5016	0.5016	NA	0.3835	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	missing
ERR10619207	run_2026_06_01_124134	variant_annotation_pipeline	1:2855629:G:A	1	2855629	G	A	snv	coding	PASS	ENSG00000295089	NA	ENST00000727914.1	splice_donor_variant&non_coding_transcript_variant	HIGH	NA	NA	0.2678	0.2678	NA	0.0371	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	HIGH	pass	interpretable_now	common	missing
ERR10619207	run_2026_06_01_124134	variant_annotation_pipeline	1:3683186:TG:T	1	3683186	TG	T	deletion	coding	PASS	ENSG00000078900	TP73	ENST00000378295.9	splice_region_variant&intron_variant	LOW	NA	NA	0.3419	0.1675	NA	0.3419	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	missing
ERR10619207	run_2026_06_01_124134	variant_annotation_pipeline	1:3831039:T:C	1	3831039	T	C	snv	coding	PASS	ENSG00000116198	CEP104	ENST00000378230.8	splice_region_variant&intron_variant	LOW	benign	benign	0.9198	0.7895	NA	0.9198	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	benign
```

---

## run_2026_05_30_151355

### Files

Stage08: `results/run_2026_05_30_151355/processed/stage_08_vdb_ready_variants.tsv`
Stage09: `results/run_2026_05_30_151355/processed/coding_candidates.tsv`
Stage10: `results/run_2026_05_30_151355/processed/noncoding_candidates.tsv`

### Counts

| Metric | Count |
|---|---:|
| Stage08 rows | 849399 |
| Stage09 rows | 25497 |
| Stage10 rows | 821358 |
| Stage08 distinct variant_ids | 849399 |
| Routed distinct variant_ids | 846855 |
| Unrouted distinct variant_ids | 2544 |
| Unrouted Stage08 rows | 2544 |

### Unrouted Population: variant_context

```text
2544	splice_region
```

### Unrouted Population: variant_class

```text
2544	coding
```

### Unrouted Population: gene_mapping_status

```text
2544	mapped
```

### Unrouted Population: qc_status

```text
2544	pass
```

### Unrouted Population: interpretability_status

```text
2544	interpretable_now
```

### Unrouted Population: frequency_status

```text
2240	common
131	low_frequency
124	rare
49	missing
```

### Unrouted Population: clinical_status

```text
```

### First 10 Unrouted Rows

```text
sample_id	run_id	source_pipeline	variant_id	chromosome	position	reference_allele	alternate_allele	variant_type	variant_class	quality_flag	gene_id	gene_symbol	transcript_id	consequence	impact_class	clinical_significance	clinvar_significance	population_frequency	gnomad_af	exac_af	thousand_genomes_af	mito_flag	epilepsy_flag	annotation_source	annotation_version	gene_mapping_status	variant_context	variant_effect_severity	qc_status	interpretability_status	frequency_status	clinical_status
ERR10619208	run_2026_05_30_151355	variant_annotation_pipeline	1:962350:C:T	1	962350	C	T	snv	coding	PASS	ENSG00000187961	KLHL17	ENST00000338591.8	splice_region_variant&splice_polypyrimidine_tract_variant&intron_variant	LOW	NA	NA	0.1747	0.0775	NA	0.1747	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	missing
ERR10619208	run_2026_05_30_151355	variant_annotation_pipeline	1:1721589:C:T	1	1721589	C	T	snv	coding	PASS	ENSG00000008128	CDK11A	ENST00000404249.8	splice_region_variant&intron_variant	LOW	NA	NA	0.7474	0.7474	NA	0.4985	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	missing
ERR10619208	run_2026_05_30_151355	variant_annotation_pipeline	1:1735814:T:C	1	1735814	T	C	snv	coding	PASS	ENSG00000293188	NA	ENST00000577672.2	splice_region_variant&splice_polypyrimidine_tract_variant&intron_variant&non_coding_transcript_variant	LOW	NA	NA	0.7001	0.7001	NA	0.4349	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	missing
ERR10619208	run_2026_05_30_151355	variant_annotation_pipeline	1:1765220:A:G	1	1765220	A	G	snv	coding	PASS	ENSG00000008130	NADK	ENST00000341426.9	splice_region_variant&intron_variant	LOW	NA	NA	0.7412	0.7412	NA	0.4955	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	missing
ERR10619208	run_2026_05_30_151355	variant_annotation_pipeline	1:2596694:T:C	1	2596694	T	C	snv	coding	PASS	ENSG00000142606	MMEL1	ENST00000378412.8	splice_region_variant&splice_polypyrimidine_tract_variant&intron_variant	LOW	NA	NA	0.5016	0.5016	NA	0.3835	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	missing
ERR10619208	run_2026_05_30_151355	variant_annotation_pipeline	1:3831039:T:C	1	3831039	T	C	snv	coding	PASS	ENSG00000116198	CEP104	ENST00000378230.8	splice_region_variant&intron_variant	LOW	benign	benign	0.9198	0.7895	NA	0.9198	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	benign
ERR10619208	run_2026_05_30_151355	variant_annotation_pipeline	1:3836494:C:A	1	3836494	C	A	snv	coding	PASS	ENSG00000116198	CEP104	ENST00000378230.8	splice_donor_variant	HIGH	NA	NA	0.004988	0.004988	NA	NA	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	HIGH	pass	interpretable_now	rare	missing
ERR10619208	run_2026_05_30_151355	variant_annotation_pipeline	1:3890079:T:A	1	3890079	T	A	snv	coding	PASS	ENSG00000198912	C1ORF174	ENST00000361605.4	splice_region_variant&splice_polypyrimidine_tract_variant&intron_variant	LOW	NA	NA	0.5696	0.4215	NA	0.5696	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	missing
ERR10619208	run_2026_05_30_151355	variant_annotation_pipeline	1:5875102:T:A	1	5875102	T	A	snv	coding	PASS	ENSG00000131697	NPHP4	ENST00000378156.9	splice_acceptor_variant	HIGH	benign	benign	0.1567	0.1567	NA	0.09	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	HIGH	pass	interpretable_now	common	benign
ERR10619208	run_2026_05_30_151355	variant_annotation_pipeline	1:6526010:C:T	1	6526010	C	T	snv	coding	PASS	ENSG00000162408	NOL9	ENST00000377705.6	splice_region_variant&splice_polypyrimidine_tract_variant&intron_variant	LOW	NA	NA	0.9794	0.9794	NA	0.9266	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	missing
```

---

## run_2026_05_30_214724

### Files

Stage08: `results/run_2026_05_30_214724/processed/stage_08_vdb_ready_variants.tsv`
Stage09: `results/run_2026_05_30_214724/processed/coding_candidates.tsv`
Stage10: `results/run_2026_05_30_214724/processed/noncoding_candidates.tsv`

### Counts

| Metric | Count |
|---|---:|
| Stage08 rows | 905517 |
| Stage09 rows | 24592 |
| Stage10 rows | 878368 |
| Stage08 distinct variant_ids | 905517 |
| Routed distinct variant_ids | 902960 |
| Unrouted distinct variant_ids | 2557 |
| Unrouted Stage08 rows | 2557 |

### Unrouted Population: variant_context

```text
2557	splice_region
```

### Unrouted Population: variant_class

```text
2557	coding
```

### Unrouted Population: gene_mapping_status

```text
2557	mapped
```

### Unrouted Population: qc_status

```text
2557	pass
```

### Unrouted Population: interpretability_status

```text
2557	interpretable_now
```

### Unrouted Population: frequency_status

```text
2239	common
137	low_frequency
134	rare
47	missing
```

### Unrouted Population: clinical_status

```text
```

### First 10 Unrouted Rows

```text
sample_id	run_id	source_pipeline	variant_id	chromosome	position	reference_allele	alternate_allele	variant_type	variant_class	quality_flag	gene_id	gene_symbol	transcript_id	consequence	impact_class	clinical_significance	clinvar_significance	population_frequency	gnomad_af	exac_af	thousand_genomes_af	mito_flag	epilepsy_flag	annotation_source	annotation_version	gene_mapping_status	variant_context	variant_effect_severity	qc_status	interpretability_status	frequency_status	clinical_status
ERR10619212	run_2026_05_30_214724	variant_annotation_pipeline	1:17746:A:G	1	17746	A	G	snv	coding	PASS	ENSG00000310526	WASH7P	ENST00000831140.1	splice_region_variant&splice_polypyrimidine_tract_variant&intron_variant&non_coding_transcript_variant	LOW	NA	NA	0.1499	0.1499	NA	NA	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	missing
ERR10619212	run_2026_05_30_214724	variant_annotation_pipeline	1:183733:C:T	1	183733	C	T	snv	coding	PASS	ENSG00000279928	DDX11L17	ENST00000624431.2	splice_region_variant&splice_polypyrimidine_tract_variant&intron_variant&non_coding_transcript_variant	LOW	NA	NA	0.01079	0.01079	NA	NA	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	low_frequency	missing
ERR10619212	run_2026_05_30_214724	variant_annotation_pipeline	1:1041950:T:C	1	1041950	T	C	snv	coding	PASS	ENSG00000188157	AGRN	ENST00000379370.7	splice_region_variant&splice_polypyrimidine_tract_variant&intron_variant	LOW	benign	benign	0.8852	0.8852	NA	0.6899	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	benign
ERR10619212	run_2026_05_30_214724	variant_annotation_pipeline	1:1721589:C:T	1	1721589	C	T	snv	coding	PASS	ENSG00000008128	CDK11A	ENST00000404249.8	splice_region_variant&intron_variant	LOW	NA	NA	0.7474	0.7474	NA	0.4985	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	missing
ERR10619212	run_2026_05_30_214724	variant_annotation_pipeline	1:1735814:T:C	1	1735814	T	C	snv	coding	PASS	ENSG00000293188	NA	ENST00000577672.2	splice_region_variant&splice_polypyrimidine_tract_variant&intron_variant&non_coding_transcript_variant	LOW	NA	NA	0.7001	0.7001	NA	0.4349	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	missing
ERR10619212	run_2026_05_30_214724	variant_annotation_pipeline	1:1765220:A:G	1	1765220	A	G	snv	coding	PASS	ENSG00000008130	NADK	ENST00000341426.9	splice_region_variant&intron_variant	LOW	NA	NA	0.7412	0.7412	NA	0.4955	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	missing
ERR10619212	run_2026_05_30_214724	variant_annotation_pipeline	1:2596694:T:C	1	2596694	T	C	snv	coding	PASS	ENSG00000142606	MMEL1	ENST00000378412.8	splice_region_variant&splice_polypyrimidine_tract_variant&intron_variant	LOW	NA	NA	0.5016	0.5016	NA	0.3835	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	missing
ERR10619212	run_2026_05_30_214724	variant_annotation_pipeline	1:3683186:TG:T	1	3683186	TG	T	deletion	coding	PASS	ENSG00000078900	TP73	ENST00000378295.9	splice_region_variant&intron_variant	LOW	NA	NA	0.3419	0.1675	NA	0.3419	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	missing
ERR10619212	run_2026_05_30_214724	variant_annotation_pipeline	1:3831039:T:C	1	3831039	T	C	snv	coding	PASS	ENSG00000116198	CEP104	ENST00000378230.8	splice_region_variant&intron_variant	LOW	benign	benign	0.9198	0.7895	NA	0.9198	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	benign
ERR10619212	run_2026_05_30_214724	variant_annotation_pipeline	1:3890079:T:A	1	3890079	T	A	snv	coding	PASS	ENSG00000198912	C1ORF174	ENST00000361605.4	splice_region_variant&splice_polypyrimidine_tract_variant&intron_variant	LOW	NA	NA	0.5696	0.4215	NA	0.5696	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	missing
```

---

## run_2026_05_31_091242

### Files

Stage08: `results/run_2026_05_31_091242/processed/stage_08_vdb_ready_variants.tsv`
Stage09: `results/run_2026_05_31_091242/processed/coding_candidates.tsv`
Stage10: `results/run_2026_05_31_091242/processed/noncoding_candidates.tsv`

### Counts

| Metric | Count |
|---|---:|
| Stage08 rows | 757635 |
| Stage09 rows | 25332 |
| Stage10 rows | 729815 |
| Stage08 distinct variant_ids | 757635 |
| Routed distinct variant_ids | 755147 |
| Unrouted distinct variant_ids | 2488 |
| Unrouted Stage08 rows | 2488 |

### Unrouted Population: variant_context

```text
2488	splice_region
```

### Unrouted Population: variant_class

```text
2488	coding
```

### Unrouted Population: gene_mapping_status

```text
2488	mapped
```

### Unrouted Population: qc_status

```text
2488	pass
```

### Unrouted Population: interpretability_status

```text
2488	interpretable_now
```

### Unrouted Population: frequency_status

```text
2206	common
129	low_frequency
115	rare
38	missing
```

### Unrouted Population: clinical_status

```text
```

### First 10 Unrouted Rows

```text
sample_id	run_id	source_pipeline	variant_id	chromosome	position	reference_allele	alternate_allele	variant_type	variant_class	quality_flag	gene_id	gene_symbol	transcript_id	consequence	impact_class	clinical_significance	clinvar_significance	population_frequency	gnomad_af	exac_af	thousand_genomes_af	mito_flag	epilepsy_flag	annotation_source	annotation_version	gene_mapping_status	variant_context	variant_effect_severity	qc_status	interpretability_status	frequency_status	clinical_status
ERR10619225	run_2026_05_31_091242	variant_annotation_pipeline	1:15045:C:T	1	15045	C	T	snv	coding	PASS	ENSG00000310526	WASH7P	ENST00000831140.1	splice_region_variant&splice_polypyrimidine_tract_variant&intron_variant&non_coding_transcript_variant	LOW	NA	NA	0.4369	0.4369	NA	NA	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	missing
ERR10619225	run_2026_05_31_091242	variant_annotation_pipeline	1:962350:C:T	1	962350	C	T	snv	coding	PASS	ENSG00000187961	KLHL17	ENST00000338591.8	splice_region_variant&splice_polypyrimidine_tract_variant&intron_variant	LOW	NA	NA	0.1747	0.0775	NA	0.1747	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	missing
ERR10619225	run_2026_05_31_091242	variant_annotation_pipeline	1:1041950:T:C	1	1041950	T	C	snv	coding	PASS	ENSG00000188157	AGRN	ENST00000379370.7	splice_region_variant&splice_polypyrimidine_tract_variant&intron_variant	LOW	benign	benign	0.8852	0.8852	NA	0.6899	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	benign
ERR10619225	run_2026_05_31_091242	variant_annotation_pipeline	1:1063202:G:C	1	1063202	G	C	snv	coding	PASS	ENSG00000217801	PTPN11BP	ENST00000412397.2	splice_donor_variant&non_coding_transcript_variant	HIGH	NA	NA	0.4846	0.4846	NA	0.0673	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	HIGH	pass	interpretable_now	common	missing
ERR10619225	run_2026_05_31_091242	variant_annotation_pipeline	1:1455924:T:C	1	1455924	T	C	snv	coding	PASS	ENSG00000215915	ATAD3C	ENST00000378785.7	splice_region_variant&intron_variant	LOW	NA	NA	0.5333	0.4275	NA	0.5333	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	missing
ERR10619225	run_2026_05_31_091242	variant_annotation_pipeline	1:1486536:T:C	1	1486536	T	C	snv	coding	PASS	ENSG00000160072	ATAD3B	ENST00000673477.1	splice_region_variant&splice_polypyrimidine_tract_variant&intron_variant	LOW	NA	NA	0.2716	0.2716	NA	NA	True	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	missing
ERR10619225	run_2026_05_31_091242	variant_annotation_pipeline	1:1721589:C:T	1	1721589	C	T	snv	coding	PASS	ENSG00000008128	CDK11A	ENST00000404249.8	splice_region_variant&intron_variant	LOW	NA	NA	0.7474	0.7474	NA	0.4985	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	missing
ERR10619225	run_2026_05_31_091242	variant_annotation_pipeline	1:1735814:T:C	1	1735814	T	C	snv	coding	PASS	ENSG00000293188	NA	ENST00000577672.2	splice_region_variant&splice_polypyrimidine_tract_variant&intron_variant&non_coding_transcript_variant	LOW	NA	NA	0.7001	0.7001	NA	0.4349	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	missing
ERR10619225	run_2026_05_31_091242	variant_annotation_pipeline	1:1765220:A:G	1	1765220	A	G	snv	coding	PASS	ENSG00000008130	NADK	ENST00000341426.9	splice_region_variant&intron_variant	LOW	NA	NA	0.7412	0.7412	NA	0.4955	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	missing
ERR10619225	run_2026_05_31_091242	variant_annotation_pipeline	1:2596694:T:C	1	2596694	T	C	snv	coding	PASS	ENSG00000142606	MMEL1	ENST00000378412.8	splice_region_variant&splice_polypyrimidine_tract_variant&intron_variant	LOW	NA	NA	0.5016	0.5016	NA	0.3835	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	missing
```

---

## run_2026_06_01_004903

### Files

Stage08: `results/run_2026_06_01_004903/processed/stage_08_vdb_ready_variants.tsv`
Stage09: `results/run_2026_06_01_004903/processed/coding_candidates.tsv`
Stage10: `results/run_2026_06_01_004903/processed/noncoding_candidates.tsv`

### Counts

| Metric | Count |
|---|---:|
| Stage08 rows | 681054 |
| Stage09 rows | 24556 |
| Stage10 rows | 654106 |
| Stage08 distinct variant_ids | 681054 |
| Routed distinct variant_ids | 678662 |
| Unrouted distinct variant_ids | 2392 |
| Unrouted Stage08 rows | 2392 |

### Unrouted Population: variant_context

```text
2392	splice_region
```

### Unrouted Population: variant_class

```text
2392	coding
```

### Unrouted Population: gene_mapping_status

```text
2392	mapped
```

### Unrouted Population: qc_status

```text
2392	pass
```

### Unrouted Population: interpretability_status

```text
2392	interpretable_now
```

### Unrouted Population: frequency_status

```text
2104	common
123	low_frequency
119	rare
46	missing
```

### Unrouted Population: clinical_status

```text
```

### First 10 Unrouted Rows

```text
sample_id	run_id	source_pipeline	variant_id	chromosome	position	reference_allele	alternate_allele	variant_type	variant_class	quality_flag	gene_id	gene_symbol	transcript_id	consequence	impact_class	clinical_significance	clinvar_significance	population_frequency	gnomad_af	exac_af	thousand_genomes_af	mito_flag	epilepsy_flag	annotation_source	annotation_version	gene_mapping_status	variant_context	variant_effect_severity	qc_status	interpretability_status	frequency_status	clinical_status
ERR10619230	run_2026_06_01_004903	variant_annotation_pipeline	1:1041950:T:C	1	1041950	T	C	snv	coding	PASS	ENSG00000188157	AGRN	ENST00000379370.7	splice_region_variant&splice_polypyrimidine_tract_variant&intron_variant	LOW	benign	benign	0.8852	0.8852	NA	0.6899	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	benign
ERR10619230	run_2026_06_01_004903	variant_annotation_pipeline	1:1721589:C:T	1	1721589	C	T	snv	coding	PASS	ENSG00000008128	CDK11A	ENST00000404249.8	splice_region_variant&intron_variant	LOW	NA	NA	0.7474	0.7474	NA	0.4985	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	missing
ERR10619230	run_2026_06_01_004903	variant_annotation_pipeline	1:1735814:T:C	1	1735814	T	C	snv	coding	PASS	ENSG00000293188	NA	ENST00000577672.2	splice_region_variant&splice_polypyrimidine_tract_variant&intron_variant&non_coding_transcript_variant	LOW	NA	NA	0.7001	0.7001	NA	0.4349	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	missing
ERR10619230	run_2026_06_01_004903	variant_annotation_pipeline	1:1765220:A:G	1	1765220	A	G	snv	coding	PASS	ENSG00000008130	NADK	ENST00000341426.9	splice_region_variant&intron_variant	LOW	NA	NA	0.7412	0.7412	NA	0.4955	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	missing
ERR10619230	run_2026_06_01_004903	variant_annotation_pipeline	1:3831039:T:C	1	3831039	T	C	snv	coding	PASS	ENSG00000116198	CEP104	ENST00000378230.8	splice_region_variant&intron_variant	LOW	benign	benign	0.9198	0.7895	NA	0.9198	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	benign
ERR10619230	run_2026_06_01_004903	variant_annotation_pipeline	1:3890079:T:A	1	3890079	T	A	snv	coding	PASS	ENSG00000198912	C1ORF174	ENST00000361605.4	splice_region_variant&splice_polypyrimidine_tract_variant&intron_variant	LOW	NA	NA	0.5696	0.4215	NA	0.5696	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	missing
ERR10619230	run_2026_06_01_004903	variant_annotation_pipeline	1:6526010:C:T	1	6526010	C	T	snv	coding	PASS	ENSG00000162408	NOL9	ENST00000377705.6	splice_region_variant&splice_polypyrimidine_tract_variant&intron_variant	LOW	NA	NA	0.9794	0.9794	NA	0.9266	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	missing
ERR10619230	run_2026_06_01_004903	variant_annotation_pipeline	1:9014873:G:A	1	9014873	G	A	snv	coding	PASS	ENSG00000197241	SLC2A7	ENST00000400906.2	splice_region_variant&splice_polypyrimidine_tract_variant&intron_variant	LOW	NA	NA	0.4826	0.4465	NA	0.4826	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	missing
ERR10619230	run_2026_06_01_004903	variant_annotation_pipeline	1:9039668:A:G	1	9039668	A	G	snv	coding	PASS	ENSG00000142583	SLC2A5	ENST00000377424.9	splice_region_variant&splice_polypyrimidine_tract_variant&intron_variant	LOW	benign	benign	0.053	0.0517	NA	0.053	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	benign
ERR10619230	run_2026_06_01_004903	variant_annotation_pipeline	1:11654311:T:G	1	11654311	T	G	snv	coding	PASS	ENSG00000116661	FBXO2	ENST00000354287.5	splice_region_variant&intron_variant	LOW	benign	benign	0.8207	0.7991	NA	0.8207	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	benign
```

---

## run_2026_06_02_052302

### Files

Stage08: `results/run_2026_06_02_052302/processed/stage_08_vdb_ready_variants.tsv`
Stage09: `results/run_2026_06_02_052302/processed/coding_candidates.tsv`
Stage10: `results/run_2026_06_02_052302/processed/noncoding_candidates.tsv`

### Counts

| Metric | Count |
|---|---:|
| Stage08 rows | 909698 |
| Stage09 rows | 23648 |
| Stage10 rows | 883594 |
| Stage08 distinct variant_ids | 909698 |
| Routed distinct variant_ids | 907242 |
| Unrouted distinct variant_ids | 2456 |
| Unrouted Stage08 rows | 2456 |

### Unrouted Population: variant_context

```text
2456	splice_region
```

### Unrouted Population: variant_class

```text
2456	coding
```

### Unrouted Population: gene_mapping_status

```text
2456	mapped
```

### Unrouted Population: qc_status

```text
2456	pass
```

### Unrouted Population: interpretability_status

```text
2456	interpretable_now
```

### Unrouted Population: frequency_status

```text
2174	common
120	rare
120	low_frequency
42	missing
```

### Unrouted Population: clinical_status

```text
```

### First 10 Unrouted Rows

```text
sample_id	run_id	source_pipeline	variant_id	chromosome	position	reference_allele	alternate_allele	variant_type	variant_class	quality_flag	gene_id	gene_symbol	transcript_id	consequence	impact_class	clinical_significance	clinvar_significance	population_frequency	gnomad_af	exac_af	thousand_genomes_af	mito_flag	epilepsy_flag	annotation_source	annotation_version	gene_mapping_status	variant_context	variant_effect_severity	qc_status	interpretability_status	frequency_status	clinical_status
ERR10619241	run_2026_06_02_052302	variant_annotation_pipeline	1:847806:G:C	1	847806	G	C	snv	coding	PASS	ENSG00000228794	LINC01128	ENST00000666741.3	splice_region_variant&non_coding_transcript_exon_variant	LOW	NA	NA	0.0144	0.0040	NA	0.0144	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	low_frequency	missing
ERR10619241	run_2026_06_02_052302	variant_annotation_pipeline	1:1041950:T:C	1	1041950	T	C	snv	coding	PASS	ENSG00000188157	AGRN	ENST00000379370.7	splice_region_variant&splice_polypyrimidine_tract_variant&intron_variant	LOW	benign	benign	0.8852	0.8852	NA	0.6899	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	benign
ERR10619241	run_2026_06_02_052302	variant_annotation_pipeline	1:1721589:C:T	1	1721589	C	T	snv	coding	PASS	ENSG00000008128	CDK11A	ENST00000404249.8	splice_region_variant&intron_variant	LOW	NA	NA	0.7474	0.7474	NA	0.4985	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	missing
ERR10619241	run_2026_06_02_052302	variant_annotation_pipeline	1:1735814:T:C	1	1735814	T	C	snv	coding	PASS	ENSG00000293188	NA	ENST00000577672.2	splice_region_variant&splice_polypyrimidine_tract_variant&intron_variant&non_coding_transcript_variant	LOW	NA	NA	0.7001	0.7001	NA	0.4349	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	missing
ERR10619241	run_2026_06_02_052302	variant_annotation_pipeline	1:1765220:A:G	1	1765220	A	G	snv	coding	PASS	ENSG00000008130	NADK	ENST00000341426.9	splice_region_variant&intron_variant	LOW	NA	NA	0.7412	0.7412	NA	0.4955	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	missing
ERR10619241	run_2026_06_02_052302	variant_annotation_pipeline	1:2596694:T:C	1	2596694	T	C	snv	coding	PASS	ENSG00000142606	MMEL1	ENST00000378412.8	splice_region_variant&splice_polypyrimidine_tract_variant&intron_variant	LOW	NA	NA	0.5016	0.5016	NA	0.3835	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	missing
ERR10619241	run_2026_06_02_052302	variant_annotation_pipeline	1:3831039:T:C	1	3831039	T	C	snv	coding	PASS	ENSG00000116198	CEP104	ENST00000378230.8	splice_region_variant&intron_variant	LOW	benign	benign	0.9198	0.7895	NA	0.9198	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	benign
ERR10619241	run_2026_06_02_052302	variant_annotation_pipeline	1:3890079:T:A	1	3890079	T	A	snv	coding	PASS	ENSG00000198912	C1ORF174	ENST00000361605.4	splice_region_variant&splice_polypyrimidine_tract_variant&intron_variant	LOW	NA	NA	0.5696	0.4215	NA	0.5696	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	missing
ERR10619241	run_2026_06_02_052302	variant_annotation_pipeline	1:4423343:T:C	1	4423343	T	C	snv	coding	PASS	ENSG00000235054	LINC01777	ENST00000635002.1	splice_region_variant&splice_polypyrimidine_tract_variant&intron_variant&non_coding_transcript_variant	LOW	NA	NA	0.0669	0.0669	NA	0.0129	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	missing
ERR10619241	run_2026_06_02_052302	variant_annotation_pipeline	1:5875102:T:A	1	5875102	T	A	snv	coding	PASS	ENSG00000131697	NPHP4	ENST00000378156.9	splice_acceptor_variant	HIGH	benign	benign	0.1567	0.1567	NA	0.09	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	HIGH	pass	interpretable_now	common	benign
```

---

## run_2026_05_27_233524

### Files

Stage08: `results/run_2026_05_27_233524/processed/stage_08_vdb_ready_variants.tsv`
Stage09: `results/run_2026_05_27_233524/processed/coding_candidates.tsv`
Stage10: `results/run_2026_05_27_233524/processed/noncoding_candidates.tsv`

### Counts

| Metric | Count |
|---|---:|
| Stage08 rows | 811554 |
| Stage09 rows | 25288 |
| Stage10 rows | 783685 |
| Stage08 distinct variant_ids | 811554 |
| Routed distinct variant_ids | 808973 |
| Unrouted distinct variant_ids | 2581 |
| Unrouted Stage08 rows | 2581 |

### Unrouted Population: variant_context

```text
2581	splice_region
```

### Unrouted Population: variant_class

```text
2581	coding
```

### Unrouted Population: gene_mapping_status

```text
2581	mapped
```

### Unrouted Population: qc_status

```text
2581	pass
```

### Unrouted Population: interpretability_status

```text
2581	interpretable_now
```

### Unrouted Population: frequency_status

```text
2268	common
153	low_frequency
122	rare
38	missing
```

### Unrouted Population: clinical_status

```text
```

### First 10 Unrouted Rows

```text
sample_id	run_id	source_pipeline	variant_id	chromosome	position	reference_allele	alternate_allele	variant_type	variant_class	quality_flag	gene_id	gene_symbol	transcript_id	consequence	impact_class	clinical_significance	clinvar_significance	population_frequency	gnomad_af	exac_af	thousand_genomes_af	mito_flag	epilepsy_flag	annotation_source	annotation_version	gene_mapping_status	variant_context	variant_effect_severity	qc_status	interpretability_status	frequency_status	clinical_status
ERR10619281	run_2026_05_27_233524	variant_annotation_pipeline	1:1041950:T:C	1	1041950	T	C	snv	coding	PASS	ENSG00000188157	AGRN	ENST00000379370.7	splice_region_variant&splice_polypyrimidine_tract_variant&intron_variant	LOW	benign	benign	0.8852	0.8852	NA	0.6899	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	benign
ERR10619281	run_2026_05_27_233524	variant_annotation_pipeline	1:1284097:T:TG	1	1284097	T	TG	insertion	coding	PASS	ENSG00000162572	SCNN1D	ENST00000379116.10	splice_region_variant&intron_variant	LOW	NA	NA	0.06771	0.06771	NA	NA	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	missing
ERR10619281	run_2026_05_27_233524	variant_annotation_pipeline	1:1331945:G:GC	1	1331945	G	GC	insertion	coding	PASS	ENSG00000169962	TAS1R3	ENST00000339381.6	splice_region_variant&intron_variant	LOW	NA	NA	0.4962	0.1895	NA	0.4962	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	missing
ERR10619281	run_2026_05_27_233524	variant_annotation_pipeline	1:1455924:T:C	1	1455924	T	C	snv	coding	PASS	ENSG00000215915	ATAD3C	ENST00000378785.7	splice_region_variant&intron_variant	LOW	NA	NA	0.5333	0.4275	NA	0.5333	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	missing
ERR10619281	run_2026_05_27_233524	variant_annotation_pipeline	1:1456217:T:C	1	1456217	T	C	snv	coding	PASS	ENSG00000215915	ATAD3C	ENST00000378785.7	splice_region_variant&splice_polypyrimidine_tract_variant&intron_variant	LOW	NA	NA	0.9944	0.9944	NA	NA	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	missing
ERR10619281	run_2026_05_27_233524	variant_annotation_pipeline	1:1486536:T:C	1	1486536	T	C	snv	coding	PASS	ENSG00000160072	ATAD3B	ENST00000673477.1	splice_region_variant&splice_polypyrimidine_tract_variant&intron_variant	LOW	NA	NA	0.2716	0.2716	NA	NA	True	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	missing
ERR10619281	run_2026_05_27_233524	variant_annotation_pipeline	1:1708173:T:C	1	1708173	T	C	snv	coding	PASS	ENSG00000008128	CDK11A	ENST00000404249.8	splice_region_variant&intron_variant	LOW	NA	NA	0.2587	0.0757	NA	0.2587	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	missing
ERR10619281	run_2026_05_27_233524	variant_annotation_pipeline	1:1721589:C:T	1	1721589	C	T	snv	coding	PASS	ENSG00000008128	CDK11A	ENST00000404249.8	splice_region_variant&intron_variant	LOW	NA	NA	0.7474	0.7474	NA	0.4985	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	missing
ERR10619281	run_2026_05_27_233524	variant_annotation_pipeline	1:1735814:T:C	1	1735814	T	C	snv	coding	PASS	ENSG00000293188	NA	ENST00000577672.2	splice_region_variant&splice_polypyrimidine_tract_variant&intron_variant&non_coding_transcript_variant	LOW	NA	NA	0.7001	0.7001	NA	0.4349	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	missing
ERR10619281	run_2026_05_27_233524	variant_annotation_pipeline	1:1765220:A:G	1	1765220	A	G	snv	coding	PASS	ENSG00000008130	NADK	ENST00000341426.9	splice_region_variant&intron_variant	LOW	NA	NA	0.7412	0.7412	NA	0.4955	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	missing
```

---

## run_2026_06_02_124300

### Files

Stage08: `results/run_2026_06_02_124300/processed/stage_08_vdb_ready_variants.tsv`
Stage09: `results/run_2026_06_02_124300/processed/coding_candidates.tsv`
Stage10: `results/run_2026_06_02_124300/processed/noncoding_candidates.tsv`

### Counts

| Metric | Count |
|---|---:|
| Stage08 rows | 795059 |
| Stage09 rows | 24437 |
| Stage10 rows | 768137 |
| Stage08 distinct variant_ids | 795059 |
| Routed distinct variant_ids | 792574 |
| Unrouted distinct variant_ids | 2485 |
| Unrouted Stage08 rows | 2485 |

### Unrouted Population: variant_context

```text
2485	splice_region
```

### Unrouted Population: variant_class

```text
2485	coding
```

### Unrouted Population: gene_mapping_status

```text
2485	mapped
```

### Unrouted Population: qc_status

```text
2485	pass
```

### Unrouted Population: interpretability_status

```text
2485	interpretable_now
```

### Unrouted Population: frequency_status

```text
2215	common
126	low_frequency
107	rare
37	missing
```

### Unrouted Population: clinical_status

```text
```

### First 10 Unrouted Rows

```text
sample_id	run_id	source_pipeline	variant_id	chromosome	position	reference_allele	alternate_allele	variant_type	variant_class	quality_flag	gene_id	gene_symbol	transcript_id	consequence	impact_class	clinical_significance	clinvar_significance	population_frequency	gnomad_af	exac_af	thousand_genomes_af	mito_flag	epilepsy_flag	annotation_source	annotation_version	gene_mapping_status	variant_context	variant_effect_severity	qc_status	interpretability_status	frequency_status	clinical_status
ERR10619285	run_2026_06_02_124300	variant_annotation_pipeline	1:17746:A:G	1	17746	A	G	snv	coding	PASS	ENSG00000310526	WASH7P	ENST00000831140.1	splice_region_variant&splice_polypyrimidine_tract_variant&intron_variant&non_coding_transcript_variant	LOW	NA	NA	0.1499	0.1499	NA	NA	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	missing
ERR10619285	run_2026_06_02_124300	variant_annotation_pipeline	1:962350:C:T	1	962350	C	T	snv	coding	PASS	ENSG00000187961	KLHL17	ENST00000338591.8	splice_region_variant&splice_polypyrimidine_tract_variant&intron_variant	LOW	NA	NA	0.1747	0.0775	NA	0.1747	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	missing
ERR10619285	run_2026_06_02_124300	variant_annotation_pipeline	1:1041950:T:C	1	1041950	T	C	snv	coding	PASS	ENSG00000188157	AGRN	ENST00000379370.7	splice_region_variant&splice_polypyrimidine_tract_variant&intron_variant	LOW	benign	benign	0.8852	0.8852	NA	0.6899	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	benign
ERR10619285	run_2026_06_02_124300	variant_annotation_pipeline	1:1197430:C:T	1	1197430	C	T	snv	coding	PASS	ENSG00000162571	TTLL10	ENST00000379289.6	splice_region_variant&splice_polypyrimidine_tract_variant&intron_variant	LOW	NA	NA	0.003	0.0008	NA	0.003	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	rare	missing
ERR10619285	run_2026_06_02_124300	variant_annotation_pipeline	1:1331945:G:GC	1	1331945	G	GC	insertion	coding	PASS	ENSG00000169962	TAS1R3	ENST00000339381.6	splice_region_variant&intron_variant	LOW	NA	NA	0.4962	0.1895	NA	0.4962	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	missing
ERR10619285	run_2026_06_02_124300	variant_annotation_pipeline	1:1398672:CTAGAG:C	1	1398672	CTAGAG	C	deletion	coding	PASS	ENSG00000221978	CCNL2	ENST00000400809.8	splice_acceptor_variant&splice_polypyrimidine_tract_variant&intron_variant	HIGH	NA	NA	0.1021	0.0741	NA	0.1021	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	HIGH	pass	interpretable_now	common	missing
ERR10619285	run_2026_06_02_124300	variant_annotation_pipeline	1:1455924:T:C	1	1455924	T	C	snv	coding	PASS	ENSG00000215915	ATAD3C	ENST00000378785.7	splice_region_variant&intron_variant	LOW	NA	NA	0.5333	0.4275	NA	0.5333	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	missing
ERR10619285	run_2026_06_02_124300	variant_annotation_pipeline	1:1486536:T:C	1	1486536	T	C	snv	coding	PASS	ENSG00000160072	ATAD3B	ENST00000673477.1	splice_region_variant&splice_polypyrimidine_tract_variant&intron_variant	LOW	NA	NA	0.2716	0.2716	NA	NA	True	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	missing
ERR10619285	run_2026_06_02_124300	variant_annotation_pipeline	1:1708173:T:C	1	1708173	T	C	snv	coding	PASS	ENSG00000008128	CDK11A	ENST00000404249.8	splice_region_variant&intron_variant	LOW	NA	NA	0.2587	0.0757	NA	0.2587	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	missing
ERR10619285	run_2026_06_02_124300	variant_annotation_pipeline	1:1721589:C:T	1	1721589	C	T	snv	coding	PASS	ENSG00000008128	CDK11A	ENST00000404249.8	splice_region_variant&intron_variant	LOW	NA	NA	0.7474	0.7474	NA	0.4985	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	missing
```

---

## run_2026_05_27_172531

### Files

Stage08: `results/run_2026_05_27_172531/processed/stage_08_vdb_ready_variants.tsv`
Stage09: `results/run_2026_05_27_172531/processed/coding_candidates.tsv`
Stage10: `results/run_2026_05_27_172531/processed/noncoding_candidates.tsv`

### Counts

| Metric | Count |
|---|---:|
| Stage08 rows | 736468 |
| Stage09 rows | 24041 |
| Stage10 rows | 710029 |
| Stage08 distinct variant_ids | 736468 |
| Routed distinct variant_ids | 734070 |
| Unrouted distinct variant_ids | 2398 |
| Unrouted Stage08 rows | 2398 |

### Unrouted Population: variant_context

```text
2398	splice_region
```

### Unrouted Population: variant_class

```text
2398	coding
```

### Unrouted Population: gene_mapping_status

```text
2398	mapped
```

### Unrouted Population: qc_status

```text
2398	pass
```

### Unrouted Population: interpretability_status

```text
2398	interpretable_now
```

### Unrouted Population: frequency_status

```text
2103	common
141	low_frequency
113	rare
41	missing
```

### Unrouted Population: clinical_status

```text
```

### First 10 Unrouted Rows

```text
sample_id	run_id	source_pipeline	variant_id	chromosome	position	reference_allele	alternate_allele	variant_type	variant_class	quality_flag	gene_id	gene_symbol	transcript_id	consequence	impact_class	clinical_significance	clinvar_significance	population_frequency	gnomad_af	exac_af	thousand_genomes_af	mito_flag	epilepsy_flag	annotation_source	annotation_version	gene_mapping_status	variant_context	variant_effect_severity	qc_status	interpretability_status	frequency_status	clinical_status
ERR10619300	run_2026_05_27_172531	variant_annotation_pipeline	1:17746:A:G	1	17746	A	G	snv	coding	PASS	ENSG00000310526	WASH7P	ENST00000831140.1	splice_region_variant&splice_polypyrimidine_tract_variant&intron_variant&non_coding_transcript_variant	LOW	NA	NA	0.1499	0.1499	NA	NA	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	missing
ERR10619300	run_2026_05_27_172531	variant_annotation_pipeline	1:182597:G:A	1	182597	G	A	snv	coding	PASS	ENSG00000310527	WASH9P	ENST00000831131.1	splice_region_variant&splice_polypyrimidine_tract_variant&intron_variant&non_coding_transcript_variant	LOW	NA	NA	0.03696	0.03696	NA	NA	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	low_frequency	missing
ERR10619300	run_2026_05_27_172531	variant_annotation_pipeline	1:1041950:T:C	1	1041950	T	C	snv	coding	PASS	ENSG00000188157	AGRN	ENST00000379370.7	splice_region_variant&splice_polypyrimidine_tract_variant&intron_variant	LOW	benign	benign	0.8852	0.8852	NA	0.6899	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	benign
ERR10619300	run_2026_05_27_172531	variant_annotation_pipeline	1:1398672:CTAGAG:C	1	1398672	CTAGAG	C	deletion	coding	PASS	ENSG00000221978	CCNL2	ENST00000400809.8	splice_acceptor_variant&splice_polypyrimidine_tract_variant&intron_variant	HIGH	NA	NA	0.1021	0.0741	NA	0.1021	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	HIGH	pass	interpretable_now	common	missing
ERR10619300	run_2026_05_27_172531	variant_annotation_pipeline	1:1455924:T:C	1	1455924	T	C	snv	coding	PASS	ENSG00000215915	ATAD3C	ENST00000378785.7	splice_region_variant&intron_variant	LOW	NA	NA	0.5333	0.4275	NA	0.5333	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	missing
ERR10619300	run_2026_05_27_172531	variant_annotation_pipeline	1:1456217:T:C	1	1456217	T	C	snv	coding	PASS	ENSG00000215915	ATAD3C	ENST00000378785.7	splice_region_variant&splice_polypyrimidine_tract_variant&intron_variant	LOW	NA	NA	0.9944	0.9944	NA	NA	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	missing
ERR10619300	run_2026_05_27_172531	variant_annotation_pipeline	1:1486536:T:C	1	1486536	T	C	snv	coding	PASS	ENSG00000160072	ATAD3B	ENST00000673477.1	splice_region_variant&splice_polypyrimidine_tract_variant&intron_variant	LOW	NA	NA	0.2716	0.2716	NA	NA	True	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	missing
ERR10619300	run_2026_05_27_172531	variant_annotation_pipeline	1:1721589:C:T	1	1721589	C	T	snv	coding	PASS	ENSG00000008128	CDK11A	ENST00000404249.8	splice_region_variant&intron_variant	LOW	NA	NA	0.7474	0.7474	NA	0.4985	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	missing
ERR10619300	run_2026_05_27_172531	variant_annotation_pipeline	1:1735814:T:C	1	1735814	T	C	snv	coding	PASS	ENSG00000293188	NA	ENST00000577672.2	splice_region_variant&splice_polypyrimidine_tract_variant&intron_variant&non_coding_transcript_variant	LOW	NA	NA	0.7001	0.7001	NA	0.4349	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	missing
ERR10619300	run_2026_05_27_172531	variant_annotation_pipeline	1:1765220:A:G	1	1765220	A	G	snv	coding	PASS	ENSG00000008130	NADK	ENST00000341426.9	splice_region_variant&intron_variant	LOW	NA	NA	0.7412	0.7412	NA	0.4955	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	missing
```

---

## run_2026_06_02_181024

### Files

Stage08: `results/run_2026_06_02_181024/processed/stage_08_vdb_ready_variants.tsv`
Stage09: `results/run_2026_06_02_181024/processed/coding_candidates.tsv`
Stage10: `results/run_2026_06_02_181024/processed/noncoding_candidates.tsv`

### Counts

| Metric | Count |
|---|---:|
| Stage08 rows | 879401 |
| Stage09 rows | 23953 |
| Stage10 rows | 852953 |
| Stage08 distinct variant_ids | 879401 |
| Routed distinct variant_ids | 876906 |
| Unrouted distinct variant_ids | 2495 |
| Unrouted Stage08 rows | 2495 |

### Unrouted Population: variant_context

```text
2495	splice_region
```

### Unrouted Population: variant_class

```text
2495	coding
```

### Unrouted Population: gene_mapping_status

```text
2495	mapped
```

### Unrouted Population: qc_status

```text
2495	pass
```

### Unrouted Population: interpretability_status

```text
2495	interpretable_now
```

### Unrouted Population: frequency_status

```text
2221	common
126	low_frequency
118	rare
30	missing
```

### Unrouted Population: clinical_status

```text
```

### First 10 Unrouted Rows

```text
sample_id	run_id	source_pipeline	variant_id	chromosome	position	reference_allele	alternate_allele	variant_type	variant_class	quality_flag	gene_id	gene_symbol	transcript_id	consequence	impact_class	clinical_significance	clinvar_significance	population_frequency	gnomad_af	exac_af	thousand_genomes_af	mito_flag	epilepsy_flag	annotation_source	annotation_version	gene_mapping_status	variant_context	variant_effect_severity	qc_status	interpretability_status	frequency_status	clinical_status
ERR10619309	run_2026_06_02_181024	variant_annotation_pipeline	1:1041950:T:C	1	1041950	T	C	snv	coding	PASS	ENSG00000188157	AGRN	ENST00000379370.7	splice_region_variant&splice_polypyrimidine_tract_variant&intron_variant	LOW	benign	benign	0.8852	0.8852	NA	0.6899	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	benign
ERR10619309	run_2026_06_02_181024	variant_annotation_pipeline	1:1455924:T:C	1	1455924	T	C	snv	coding	PASS	ENSG00000215915	ATAD3C	ENST00000378785.7	splice_region_variant&intron_variant	LOW	NA	NA	0.5333	0.4275	NA	0.5333	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	missing
ERR10619309	run_2026_06_02_181024	variant_annotation_pipeline	1:1486536:T:C	1	1486536	T	C	snv	coding	PASS	ENSG00000160072	ATAD3B	ENST00000673477.1	splice_region_variant&splice_polypyrimidine_tract_variant&intron_variant	LOW	NA	NA	0.2716	0.2716	NA	NA	True	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	missing
ERR10619309	run_2026_06_02_181024	variant_annotation_pipeline	1:1721589:C:T	1	1721589	C	T	snv	coding	PASS	ENSG00000008128	CDK11A	ENST00000404249.8	splice_region_variant&intron_variant	LOW	NA	NA	0.7474	0.7474	NA	0.4985	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	missing
ERR10619309	run_2026_06_02_181024	variant_annotation_pipeline	1:1735814:T:C	1	1735814	T	C	snv	coding	PASS	ENSG00000293188	NA	ENST00000577672.2	splice_region_variant&splice_polypyrimidine_tract_variant&intron_variant&non_coding_transcript_variant	LOW	NA	NA	0.7001	0.7001	NA	0.4349	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	missing
ERR10619309	run_2026_06_02_181024	variant_annotation_pipeline	1:1765220:A:G	1	1765220	A	G	snv	coding	PASS	ENSG00000008130	NADK	ENST00000341426.9	splice_region_variant&intron_variant	LOW	NA	NA	0.7412	0.7412	NA	0.4955	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	missing
ERR10619309	run_2026_06_02_181024	variant_annotation_pipeline	1:2487169:G:A	1	2487169	G	A	snv	coding	PASS	ENSG00000149527	PLCH2	ENST00000378486.8	splice_region_variant&splice_polypyrimidine_tract_variant&intron_variant	LOW	NA	NA	0.003	0.0008	NA	0.003	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	rare	missing
ERR10619309	run_2026_06_02_181024	variant_annotation_pipeline	1:3831039:T:C	1	3831039	T	C	snv	coding	PASS	ENSG00000116198	CEP104	ENST00000378230.8	splice_region_variant&intron_variant	LOW	benign	benign	0.9198	0.7895	NA	0.9198	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	benign
ERR10619309	run_2026_06_02_181024	variant_annotation_pipeline	1:3890079:T:A	1	3890079	T	A	snv	coding	PASS	ENSG00000198912	C1ORF174	ENST00000361605.4	splice_region_variant&splice_polypyrimidine_tract_variant&intron_variant	LOW	NA	NA	0.5696	0.4215	NA	0.5696	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	missing
ERR10619309	run_2026_06_02_181024	variant_annotation_pipeline	1:6206733:G:C	1	6206733	G	C	snv	coding	PASS	ENSG00000158286	RNF207	ENST00000377939.5	splice_region_variant&intron_variant	LOW	NA	NA	0.3759	0.1542	NA	0.3759	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	missing
```

---

## run_2026_06_01_203130

### Files

Stage08: `results/run_2026_06_01_203130/processed/stage_08_vdb_ready_variants.tsv`
Stage09: `results/run_2026_06_01_203130/processed/coding_candidates.tsv`
Stage10: `results/run_2026_06_01_203130/processed/noncoding_candidates.tsv`

### Counts

| Metric | Count |
|---|---:|
| Stage08 rows | 963426 |
| Stage09 rows | 24563 |
| Stage10 rows | 936295 |
| Stage08 distinct variant_ids | 963426 |
| Routed distinct variant_ids | 960858 |
| Unrouted distinct variant_ids | 2568 |
| Unrouted Stage08 rows | 2568 |

### Unrouted Population: variant_context

```text
2568	splice_region
```

### Unrouted Population: variant_class

```text
2568	coding
```

### Unrouted Population: gene_mapping_status

```text
2568	mapped
```

### Unrouted Population: qc_status

```text
2568	pass
```

### Unrouted Population: interpretability_status

```text
2568	interpretable_now
```

### Unrouted Population: frequency_status

```text
2271	common
141	low_frequency
108	rare
48	missing
```

### Unrouted Population: clinical_status

```text
```

### First 10 Unrouted Rows

```text
sample_id	run_id	source_pipeline	variant_id	chromosome	position	reference_allele	alternate_allele	variant_type	variant_class	quality_flag	gene_id	gene_symbol	transcript_id	consequence	impact_class	clinical_significance	clinvar_significance	population_frequency	gnomad_af	exac_af	thousand_genomes_af	mito_flag	epilepsy_flag	annotation_source	annotation_version	gene_mapping_status	variant_context	variant_effect_severity	qc_status	interpretability_status	frequency_status	clinical_status
ERR10619330	run_2026_06_01_203130	variant_annotation_pipeline	1:182597:G:A	1	182597	G	A	snv	coding	PASS	ENSG00000310527	WASH9P	ENST00000831131.1	splice_region_variant&splice_polypyrimidine_tract_variant&intron_variant&non_coding_transcript_variant	LOW	NA	NA	0.03696	0.03696	NA	NA	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	low_frequency	missing
ERR10619330	run_2026_06_01_203130	variant_annotation_pipeline	1:183238:G:C	1	183238	G	C	snv	coding	PASS	ENSG00000308415	DDX11L2	ENST00000833856.1	splice_region_variant&non_coding_transcript_exon_variant	LOW	NA	NA	0.05707	0.05707	NA	NA	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	missing
ERR10619330	run_2026_06_01_203130	variant_annotation_pipeline	1:971318:A:C	1	971318	A	C	snv	coding	PASS	ENSG00000187583	PLEKHN1	ENST00000379410.8	splice_region_variant&splice_polypyrimidine_tract_variant&intron_variant	LOW	NA	NA	0.008956	0.008956	NA	NA	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	rare	missing
ERR10619330	run_2026_06_01_203130	variant_annotation_pipeline	1:1041950:T:C	1	1041950	T	C	snv	coding	PASS	ENSG00000188157	AGRN	ENST00000379370.7	splice_region_variant&splice_polypyrimidine_tract_variant&intron_variant	LOW	benign	benign	0.8852	0.8852	NA	0.6899	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	benign
ERR10619330	run_2026_06_01_203130	variant_annotation_pipeline	1:1257135:A:G	1	1257135	A	G	snv	coding	PASS	ENSG00000160087	UBE2J2	ENST00000349431.11	splice_region_variant&splice_polypyrimidine_tract_variant&intron_variant	LOW	NA	NA	0.236	0.0835	NA	0.236	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	missing
ERR10619330	run_2026_06_01_203130	variant_annotation_pipeline	1:1285922:A:G	1	1285922	A	G	snv	coding	PASS	ENSG00000162572	SCNN1D	ENST00000379116.10	splice_region_variant&splice_polypyrimidine_tract_variant&intron_variant	LOW	NA	NA	0.1241	0.0349	NA	0.1241	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	missing
ERR10619330	run_2026_06_01_203130	variant_annotation_pipeline	1:1455924:T:C	1	1455924	T	C	snv	coding	PASS	ENSG00000215915	ATAD3C	ENST00000378785.7	splice_region_variant&intron_variant	LOW	NA	NA	0.5333	0.4275	NA	0.5333	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	missing
ERR10619330	run_2026_06_01_203130	variant_annotation_pipeline	1:1486536:T:C	1	1486536	T	C	snv	coding	PASS	ENSG00000160072	ATAD3B	ENST00000673477.1	splice_region_variant&splice_polypyrimidine_tract_variant&intron_variant	LOW	NA	NA	0.2716	0.2716	NA	NA	True	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	missing
ERR10619330	run_2026_06_01_203130	variant_annotation_pipeline	1:1526453:C:G	1	1526453	C	G	snv	coding	PASS	ENSG00000197785	ATAD3A	ENST00000378756.8	splice_region_variant&splice_polypyrimidine_tract_variant&intron_variant	LOW	benign&likely_benign	benign&likely_benign	0.0749	0.0216	NA	0.0749	True	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	likely_benign
ERR10619330	run_2026_06_01_203130	variant_annotation_pipeline	1:1721589:C:T	1	1721589	C	T	snv	coding	PASS	ENSG00000008128	CDK11A	ENST00000404249.8	splice_region_variant&intron_variant	LOW	NA	NA	0.7474	0.7474	NA	0.4985	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	missing
```

---

## run_2026_06_03_010030

### Files

Stage08: `results/run_2026_06_03_010030/processed/stage_08_vdb_ready_variants.tsv`
Stage09: `results/run_2026_06_03_010030/processed/coding_candidates.tsv`
Stage10: `results/run_2026_06_03_010030/processed/noncoding_candidates.tsv`

### Counts

| Metric | Count |
|---|---:|
| Stage08 rows | 4636584 |
| Stage09 rows | 24278 |
| Stage10 rows | 4609098 |
| Stage08 distinct variant_ids | 4636584 |
| Routed distinct variant_ids | 4633376 |
| Unrouted distinct variant_ids | 3208 |
| Unrouted Stage08 rows | 3208 |

### Unrouted Population: variant_context

```text
3208	splice_region
```

### Unrouted Population: variant_class

```text
3208	coding
```

### Unrouted Population: gene_mapping_status

```text
3208	mapped
```

### Unrouted Population: qc_status

```text
3208	pass
```

### Unrouted Population: interpretability_status

```text
3208	interpretable_now
```

### Unrouted Population: frequency_status

```text
2932	common
118	low_frequency
102	rare
56	missing
```

### Unrouted Population: clinical_status

```text
```

### First 10 Unrouted Rows

```text
sample_id	run_id	source_pipeline	variant_id	chromosome	position	reference_allele	alternate_allele	variant_type	variant_class	quality_flag	gene_id	gene_symbol	transcript_id	consequence	impact_class	clinical_significance	clinvar_significance	population_frequency	gnomad_af	exac_af	thousand_genomes_af	mito_flag	epilepsy_flag	annotation_source	annotation_version	gene_mapping_status	variant_context	variant_effect_severity	qc_status	interpretability_status	frequency_status	clinical_status
HG002	run_2026_06_03_010030	variant_annotation_pipeline	1:1041950:T:C	1	1041950	T	C	snv	coding	PASS	ENSG00000188157	AGRN	ENST00000379370.7	splice_region_variant&splice_polypyrimidine_tract_variant&intron_variant	LOW	benign	benign	0.8852	0.8852	NA	0.6899	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	benign
HG002	run_2026_06_03_010030	variant_annotation_pipeline	1:1063202:G:C	1	1063202	G	C	snv	coding	PASS	ENSG00000217801	PTPN11BP	ENST00000412397.2	splice_donor_variant&non_coding_transcript_variant	HIGH	NA	NA	0.4846	0.4846	NA	0.0673	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	HIGH	pass	interpretable_now	common	missing
HG002	run_2026_06_03_010030	variant_annotation_pipeline	1:1137118:G:C	1	1137118	G	C	snv	coding	PASS	ENSG00000223823	LINC01342	ENST00000416774.1	splice_region_variant&intron_variant&non_coding_transcript_variant	LOW	NA	NA	0.497	0.4970	NA	0.2625	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	missing
HG002	run_2026_06_03_010030	variant_annotation_pipeline	1:1180477:T:C	1	1180477	T	C	snv	coding	PASS	ENSG00000162571	TTLL10	ENST00000379289.6	splice_region_variant&splice_polypyrimidine_tract_variant&intron_variant	LOW	NA	NA	0.01711	0.01711	NA	NA	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	low_frequency	missing
HG002	run_2026_06_03_010030	variant_annotation_pipeline	1:1721589:C:T	1	1721589	C	T	snv	coding	PASS	ENSG00000008128	CDK11A	ENST00000404249.8	splice_region_variant&intron_variant	LOW	NA	NA	0.7474	0.7474	NA	0.4985	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	missing
HG002	run_2026_06_03_010030	variant_annotation_pipeline	1:1735814:T:C	1	1735814	T	C	snv	coding	PASS	ENSG00000293188	NA	ENST00000577672.2	splice_region_variant&splice_polypyrimidine_tract_variant&intron_variant&non_coding_transcript_variant	LOW	NA	NA	0.7001	0.7001	NA	0.4349	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	missing
HG002	run_2026_06_03_010030	variant_annotation_pipeline	1:1765220:A:G	1	1765220	A	G	snv	coding	PASS	ENSG00000008130	NADK	ENST00000341426.9	splice_region_variant&intron_variant	LOW	NA	NA	0.7412	0.7412	NA	0.4955	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	missing
HG002	run_2026_06_03_010030	variant_annotation_pipeline	1:2426036:T:C	1	2426036	T	C	snv	coding	PASS	ENSG00000149527	PLCH2	ENST00000609981.5	splice_region_variant&5_prime_UTR_variant	LOW	NA	NA	1	0.9992	NA	1	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	missing
HG002	run_2026_06_03_010030	variant_annotation_pipeline	1:2596694:T:C	1	2596694	T	C	snv	coding	PASS	ENSG00000142606	MMEL1	ENST00000378412.8	splice_region_variant&splice_polypyrimidine_tract_variant&intron_variant	LOW	NA	NA	0.5016	0.5016	NA	0.3835	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	missing
HG002	run_2026_06_03_010030	variant_annotation_pipeline	1:2855629:G:A	1	2855629	G	A	snv	coding	PASS	ENSG00000295089	NA	ENST00000727914.1	splice_donor_variant&non_coding_transcript_variant	HIGH	NA	NA	0.2678	0.2678	NA	0.0371	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	HIGH	pass	interpretable_now	common	missing
```

---

