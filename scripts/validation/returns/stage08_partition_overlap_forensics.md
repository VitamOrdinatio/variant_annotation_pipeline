# Stage08 Partition Overlap Forensics

Generated: 2026-06-17T23:28:55Z

Run audited: `run_2026_06_03_010030`

Purpose:

```text
Determine whether Stage08 partition overlap is primarily coding ∩ splice,
or whether overlap also involves noncoding partition membership.
```

## Files

- Coding: `results/run_2026_06_03_010030/processed/coding_candidates.tsv`
- Splice: `results/run_2026_06_03_010030/processed/splice_region_candidates.tsv`
- Noncoding: `results/run_2026_06_03_010030/processed/noncoding_candidates.tsv`

## Overlap Counts

| Intersection | Distinct variant_ids |
|---|---:|
| coding ∩ splice | 525 |
| coding ∩ noncoding | 0 |
| splice ∩ noncoding | 0 |
| any overlap | 525 |

## Coding ∩ Splice Characterization

### variant_context
```text
525	splice_region
```

### variant_class
```text
525	coding
```

### consequence
```text
259	splice_region_variant&synonymous_variant
249	missense_variant&splice_region_variant
6	frameshift_variant&splice_region_variant
2	stop_gained&splice_region_variant
2	inframe_insertion&splice_region_variant
2	inframe_deletion&splice_region_variant
1	start_lost&splice_region_variant
1	splice_region_variant&synonymous_variant&NMD_transcript_variant
1	splice_donor_variant&stop_gained&frameshift_variant
1	splice_acceptor_variant&frameshift_variant
1	frameshift_variant&splice_region_variant&intron_variant
```

### impact_class
```text
260	LOW
253	MODERATE
12	HIGH
```

## Coding ∩ Noncoding Characterization

### First 20 rows
```text
```

## Splice ∩ Noncoding Characterization

### First 20 rows
```text
```

## Coding ∩ Splice First 20 Rows

```text
sample_id	run_id	source_pipeline	variant_id	chromosome	position	reference_allele	alternate_allele	variant_type	variant_class	quality_flag	gene_id	gene_symbol	transcript_id	consequence	impact_class	clinical_significance	clinvar_significance	population_frequency	gnomad_af	exac_af	thousand_genomes_af	mito_flag	epilepsy_flag	annotation_source	annotation_version	gene_mapping_status	variant_context	variant_effect_severity	qc_status	interpretability_status	frequency_status	clinical_status
HG002	run_2026_06_03_010030	variant_annotation_pipeline	1:1708951:C:T	1	1708951	C	T	snv	coding	PASS	ENSG00000008128	CDK11A	ENST00000404249.8	splice_region_variant&synonymous_variant	LOW	NA	NA	0.3154	0.0883	NA	0.3154	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	missing
HG002	run_2026_06_03_010030	variant_annotation_pipeline	1:2609830:A:G	1	2609830	A	G	snv	coding	PASS	ENSG00000142606	MMEL1	ENST00000378412.8	splice_region_variant&synonymous_variant	LOW	NA	NA	0.7027	0.5315	NA	0.7027	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	missing
HG002	run_2026_06_03_010030	variant_annotation_pipeline	1:12893472:T:C	1	12893472	T	C	snv	coding	PASS	ENSG00000187545	PRAMEF10	ENST00000235347.4	missense_variant&splice_region_variant	MODERATE	NA	NA	0.412	0.412	NA	NA	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	MODERATE	pass	interpretable_now	common	missing
HG002	run_2026_06_03_010030	variant_annotation_pipeline	1:13308331:A:G	1	13308331	A	G	snv	coding	PASS	ENSG00000237700	PRAMEF33	ENST00000437300.2	missense_variant&splice_region_variant	MODERATE	NA	NA	0.2529	0.2529	NA	NA	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	MODERATE	pass	interpretable_now	common	missing
HG002	run_2026_06_03_010030	variant_annotation_pipeline	1:16577417:T:A	1	16577417	T	A	snv	coding	PASS	ENSG00000219481	NBPF1	ENST00000430580.6	missense_variant&splice_region_variant	MODERATE	NA	NA	0.8562	0.8562	NA	NA	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	MODERATE	pass	interpretable_now	common	missing
HG002	run_2026_06_03_010030	variant_annotation_pipeline	1:21468895:A:G	1	21468895	A	G	snv	coding	PASS	ENSG00000142794	NBPF3	ENST00000318249.10	missense_variant&splice_region_variant	MODERATE	NA	NA	0.4239	0.4239	NA	0.1445	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	MODERATE	pass	interpretable_now	common	missing
HG002	run_2026_06_03_010030	variant_annotation_pipeline	1:21984331:T:C	1	21984331	T	C	snv	coding	PASS	ENSG00000219073	CELA3B	ENST00000337107.11	splice_region_variant&synonymous_variant	LOW	NA	NA	0.8932	0.8932	NA	0.8434	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	missing
HG002	run_2026_06_03_010030	variant_annotation_pipeline	1:31698605:T:G	1	31698605	T	G	snv	coding	PASS	ENSG00000084636	COL16A1	ENST00000373672.8	splice_region_variant&synonymous_variant	LOW	NA	NA	0.82	0.6258	NA	0.82	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	missing
HG002	run_2026_06_03_010030	variant_annotation_pipeline	1:42665982:G:A	1	42665982	G	A	snv	coding	PASS	ENSG00000171960	PPIH	ENST00000304979.8	splice_region_variant&synonymous_variant	LOW	NA	NA	0.1504	0.1504	NA	0.0363	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	missing
HG002	run_2026_06_03_010030	variant_annotation_pipeline	1:54548340:C:T	1	54548340	C	T	snv	coding	PASS	ENSG00000162390	ACOT11	ENST00000343744.7	missense_variant&splice_region_variant	MODERATE	NA	NA	0.0291	0.0291	NA	0.0038	True	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	MODERATE	pass	interpretable_now	low_frequency	missing
HG002	run_2026_06_03_010030	variant_annotation_pipeline	1:54594689:G:A	1	54594689	G	A	snv	coding	PASS	ENSG00000162390	ACOT11	ENST00000343744.7	missense_variant&splice_region_variant	MODERATE	NA	NA	0.5371	0.2554	NA	0.5371	True	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	MODERATE	pass	interpretable_now	common	missing
HG002	run_2026_06_03_010030	variant_annotation_pipeline	1:66822362:C:T	1	66822362	C	T	snv	coding	PASS	ENSG00000152763	DNAI4	ENST00000371026.8	missense_variant&splice_region_variant	MODERATE	NA	NA	0.5537	0.5148	NA	0.5537	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	MODERATE	pass	interpretable_now	common	missing
HG002	run_2026_06_03_010030	variant_annotation_pipeline	1:75236989:G:A	1	75236989	G	A	snv	coding	PASS	ENSG00000137968	SLC44A5	ENST00000370859.8	splice_region_variant&synonymous_variant	LOW	NA	NA	0.1172	0.1162	NA	0.1172	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	missing
HG002	run_2026_06_03_010030	variant_annotation_pipeline	1:85128709:T:C	1	85128709	T	C	snv	coding	PASS	ENSG00000162643	DNAI3	ENST00000294664.11	splice_region_variant&synonymous_variant	LOW	NA	NA	0.0525	0.0525	NA	0.0023	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	missing
HG002	run_2026_06_03_010030	variant_annotation_pipeline	1:88805891:T:C	1	88805891	T	C	snv	coding	PASS	ENSG00000065243	PKN2	ENST00000370521.8	splice_region_variant&synonymous_variant	LOW	NA	NA	0.5116	0.5116	NA	0.3563	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	missing
HG002	run_2026_06_03_010030	variant_annotation_pipeline	1:91316474:T:C	1	91316474	T	C	snv	coding	PASS	ENSG00000162669	HFM1	ENST00000370425.8	missense_variant&splice_region_variant	MODERATE	NA	NA	0.125	0.1250	NA	0.1233	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	MODERATE	pass	interpretable_now	common	missing
HG002	run_2026_06_03_010030	variant_annotation_pipeline	1:94001103:A:G	1	94001103	A	G	snv	coding	PASS	ENSG00000198691	ABCA4	ENST00000370225.4	splice_region_variant&synonymous_variant	LOW	benign	benign	0.733	0.3011	NA	0.733	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	benign
HG002	run_2026_06_03_010030	variant_annotation_pipeline	1:107770636:C:T	1	107770636	C	T	snv	coding	PASS	ENSG00000134215	VAV3	ENST00000370056.9	splice_region_variant&synonymous_variant	LOW	NA	NA	0.6876	0.6709	NA	0.6876	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	missing
HG002	run_2026_06_03_010030	variant_annotation_pipeline	1:110456232:G:A	1	110456232	G	A	snv	coding	PASS	ENSG00000143125	PROK1	ENST00000271331.4	missense_variant&splice_region_variant	MODERATE	NA	NA	0.4411	0.4411	NA	0.3654	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	MODERATE	pass	interpretable_now	common	missing
HG002	run_2026_06_03_010030	variant_annotation_pipeline	1:120005329:CTG:C	1	120005329	CTG	C	deletion	coding	PASS	ENSG00000134250	NOTCH2	ENST00000256646.7	frameshift_variant&splice_region_variant	HIGH	NA	NA	NULL	NA	NA	NA	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	HIGH	pass	interpretable_now	missing	missing
```

