# Stage07–Stage12 Lineage Forensics

Generated: 2026-06-18T04:37:40Z

Purpose:

```text
Audit row, variant_id, and column lineage from Stage07 through Stage12
across 12 epilepsy WES runs and 1 HG002 WGS run.
```

## ERR10619203 / run_2026_05_30_071639 / q3

# Artifact Inventory

### Stage07 annotated_variants.tsv

- path: `results/run_2026_05_30_071639/processed/ERR10619203_run_2026_05_30_071639.annotated_variants.tsv`
- size_bytes: 158283260
- rows: 
- columns: 25
- header_sha256: `617480c310358e0f764d2996153e3428ee6270702ce98194140c6e7ba6074d9f`
- has_variant_id: yes
- distinct_variant_ids: 674593

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	quality_flag
    10	gene_id
    11	gene_symbol
    12	transcript_id
    13	consequence
    14	impact_class
    15	impact
    16	variant_class
    17	variant_type
    18	clinical_significance
    19	clinvar_significance
    20	population_frequency
    21	gnomad_af
    22	exac_af
    23	thousand_genomes_af
    24	mito_flag
    25	epilepsy_flag
```

First data row preview:
```text
ERR10619203	run_2026_05_30_071639	variant_annotation_pipeline	1:14542:A:G	1	14542	A	G	PASS	ENSG00000310526	WASH7P	ENST00000831140.1	non_coding_transcript_exon_variant	MODIFIER	MODIFIER	SNV	non-coding	NA	NA	0.3406	0.3406	NA	NA	False	False

```

### Stage08 selected_transcript_consequences.tsv

- path: `results/run_2026_05_30_071639/processed/stage_08_selected_transcript_consequences.tsv`
- size_bytes: 227580171
- rows: 
- columns: 33
- header_sha256: `cd5a915c5bc9d15f76cda12616b5dae1e039ecb5f00164e46acc177e2d42a402`
- has_variant_id: yes
- distinct_variant_ids: 674593

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
```

First data row preview:
```text
ERR10619203	run_2026_05_30_071639	variant_annotation_pipeline	1:14542:A:G	1	14542	A	G	snv	noncoding	PASS	ENSG00000310526	WASH7P	ENST00000831140.1	non_coding_transcript_exon_variant	MODIFIER	NA	NA	0.3406	0.3406	NA	NA	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	noncoding_transcript	MODIFIER	pass	needs_external_annotation	common	missing

```

### Stage08 vdb_ready_variants.tsv

- path: `results/run_2026_05_30_071639/processed/stage_08_vdb_ready_variants.tsv`
- size_bytes: 227580171
- rows: 
- columns: 33
- header_sha256: `cd5a915c5bc9d15f76cda12616b5dae1e039ecb5f00164e46acc177e2d42a402`
- has_variant_id: yes
- distinct_variant_ids: 674593

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
```

First data row preview:
```text
ERR10619203	run_2026_05_30_071639	variant_annotation_pipeline	1:14542:A:G	1	14542	A	G	snv	noncoding	PASS	ENSG00000310526	WASH7P	ENST00000831140.1	non_coding_transcript_exon_variant	MODIFIER	NA	NA	0.3406	0.3406	NA	NA	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	noncoding_transcript	MODIFIER	pass	needs_external_annotation	common	missing

```

### Stage08 coding_candidates.tsv

- path: `results/run_2026_05_30_071639/processed/coding_candidates.tsv`
- size_bytes: 7683762
- rows: 
- columns: 33
- header_sha256: `cd5a915c5bc9d15f76cda12616b5dae1e039ecb5f00164e46acc177e2d42a402`
- has_variant_id: yes
- distinct_variant_ids: 23907

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
```

First data row preview:
```text
ERR10619203	run_2026_05_30_071639	variant_annotation_pipeline	1:69270:A:G	1	69270	A	G	snv	coding	PASS	ENSG00000186092	OR4F5	ENST00000641515.2	synonymous_variant	LOW	NA	NA	0.9961	0.9961	NA	NA	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	coding	LOW	pass	interpretable_now	common	missing

```

### Stage08 splice_region_candidates.tsv

- path: `results/run_2026_05_30_071639/processed/splice_region_candidates.tsv`
- size_bytes: 1045224
- rows: 
- columns: 33
- header_sha256: `cd5a915c5bc9d15f76cda12616b5dae1e039ecb5f00164e46acc177e2d42a402`
- has_variant_id: yes
- distinct_variant_ids: 2829

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
```

First data row preview:
```text
ERR10619203	run_2026_05_30_071639	variant_annotation_pipeline	1:17375:A:G	1	17375	A	G	snv	coding	PASS	ENSG00000227232	WASH7P	ENST00000488147.2	splice_region_variant&splice_polypyrimidine_tract_variant&intron_variant&non_coding_transcript_variant	LOW	NA	NA	0.009963	0.009963	NA	NA	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	rare	missing

```

### Stage08 noncoding_candidates.tsv

- path: `results/run_2026_05_30_071639/processed/noncoding_candidates.tsv`
- size_bytes: 219015356
- rows: 
- columns: 33
- header_sha256: `cd5a915c5bc9d15f76cda12616b5dae1e039ecb5f00164e46acc177e2d42a402`
- has_variant_id: yes
- distinct_variant_ids: 648322

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
```

First data row preview:
```text
ERR10619203	run_2026_05_30_071639	variant_annotation_pipeline	1:14542:A:G	1	14542	A	G	snv	noncoding	PASS	ENSG00000310526	WASH7P	ENST00000831140.1	non_coding_transcript_exon_variant	MODIFIER	NA	NA	0.3406	0.3406	NA	NA	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	noncoding_transcript	MODIFIER	pass	needs_external_annotation	common	missing

```

### Stage08 variant_summary.tsv

- path: `results/run_2026_05_30_071639/processed/stage_08_variant_summary.tsv`
- size_bytes: 171210080
- rows: 
- columns: 26
- header_sha256: `a0088e61e1ce409de45d1365b177ff47234ecb57dacab3ef0cb50fe3f613b55a`
- has_variant_id: yes
- distinct_variant_ids: 674593

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	gene_symbols
    10	gene_mapping_status
    11	worst_consequence
    12	highest_impact
    13	canonical_present
    14	coding_flag
    15	splice_flag
    16	noncoding_flag
    17	transcript_count
    18	variant_type
    19	variant_class
    20	quality_flag
    21	qc_status
    22	population_frequency
    23	frequency_status
    24	clinical_status
    25	annotation_source
    26	annotation_version
```

First data row preview:
```text
ERR10619203	run_2026_05_30_071639	variant_annotation_pipeline	10:100024218:CA:C	10	100024218	CA	C	NA	mapped	upstream_gene_variant	MODIFIER	False	False	False	True	1	deletion	noncoding	PASS	pass	0.4902	common	missing	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #

```

### Stage08 rdgp_gene_evidence_seed.tsv

- path: `results/run_2026_05_30_071639/processed/stage_08_rdgp_gene_evidence_seed.tsv`
- size_bytes: 11729809
- rows: 
- columns: 10
- header_sha256: `18d500222bcf3f2b99e044e14b9a1f0647d3f9bf1593555fa16359bb3996d3a3`
- has_variant_id: no
- distinct_variant_ids: NA

Header:
```text
     1	sample_id
     2	gene_id
     3	gene_symbol
     4	variant_count
     5	high_impact_variant_count
     6	rare_variant_count
     7	pathogenic_variant_count
     8	max_variant_severity
     9	has_low_quality_evidence
    10	contributing_variant_ids
```

First data row preview:
```text
ERR10619203	ENSG00000000003	TSPAN6	3	0	0	0	MODERATE	False	X:100631032:G:GCTGTC,X:100632405:C:CA,X:100635207:C:T

```

### Stage09 coding_interpreted.tsv

- path: `results/run_2026_05_30_071639/processed/stage_09_coding_interpreted.tsv`
- size_bytes: 11176316
- rows: 
- columns: 43
- header_sha256: `8132a0aab15233fd27576c5624b2e8393fe622aa2bd651c8bdfc94c6215d5d3b`
- has_variant_id: yes
- distinct_variant_ids: 26271

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
    34	functional_impact
    35	rarity_flag
    36	clinical_evidence
    37	qc_reliability
    38	coding_interpretation_label
    39	is_lof_candidate
    40	is_rare_candidate
    41	is_clinically_supported
    42	is_high_quality
    43	is_potential_artifact
```

First data row preview:
```text
ERR10619203	run_2026_05_30_071639	variant_annotation_pipeline	1:69270:A:G	1	69270	A	G	snv	coding	PASS	ENSG00000186092	OR4F5	ENST00000641515.2	synonymous_variant	LOW	NA	NA	0.9961	0.9961	NA	NA	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	coding	LOW	pass	interpretable_now	common	missing	synonymous	common	missing	high_confidence	coding_common_or_low_support	False	False	False	True	False

```

### Stage10 noncoding_interpreted.tsv

- path: `results/run_2026_05_30_071639/processed/stage_10_noncoding_interpreted.tsv`
- size_bytes: 285812594
- rows: 
- columns: 43
- header_sha256: `52d4bd70320ef627d745025507d0b4bd3197d1fef0d1436811b20a6c4486c87e`
- has_variant_id: yes
- distinct_variant_ids: 648322

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
    34	noncoding_functional_context
    35	rarity_flag
    36	clinical_evidence
    37	qc_reliability
    38	noncoding_interpretation_label
    39	is_regulatory_candidate
    40	is_rare_candidate
    41	is_clinically_supported
    42	is_high_quality
    43	is_potential_artifact
```

First data row preview:
```text
ERR10619203	run_2026_05_30_071639	variant_annotation_pipeline	1:14542:A:G	1	14542	A	G	snv	noncoding	PASS	ENSG00000310526	WASH7P	ENST00000831140.1	non_coding_transcript_exon_variant	MODIFIER	NA	NA	0.3406	0.3406	NA	NA	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	noncoding_transcript	MODIFIER	pass	needs_external_annotation	common	missing	transcript_associated	common	missing	high_confidence	noncoding_common_or_low_support	False	False	False	True	False

```

### Stage11 prioritized_variants.tsv

- path: `results/run_2026_05_30_071639/processed/stage_11_prioritized_variants.tsv`
- size_bytes: 367221142
- rows: 
- columns: 52
- header_sha256: `446c7603e23bb60bb4da68196782174abe5aea562307628ddf55513a5e4bae54`
- has_variant_id: yes
- distinct_variant_ids: 674593

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
    34	functional_impact
    35	rarity_flag
    36	clinical_evidence
    37	qc_reliability
    38	coding_interpretation_label
    39	is_lof_candidate
    40	is_rare_candidate
    41	is_clinically_supported
    42	is_high_quality
    43	is_potential_artifact
    44	variant_origin
    45	source_interpretation_label
    46	priority_tier
    47	priority_rank
    48	priority_reason
    49	is_high_priority_candidate
    50	is_moderate_priority_candidate
    51	is_low_priority_candidate
    52	is_uninterpretable
```

First data row preview:
```text
ERR10619203	run_2026_05_30_071639	variant_annotation_pipeline	1:69270:A:G	1	69270	A	G	snv	coding	PASS	ENSG00000186092	OR4F5	ENST00000641515.2	synonymous_variant	LOW	NA	NA	0.9961	0.9961	NA	NA	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	coding	LOW	pass	interpretable_now	common	missing	synonymous	common	missing	high_confidence	coding_common_or_low_support	False	False	False	True	False	coding	coding_common_or_low_support	tier_3_low_support_or_common	3	coding label coding_common_or_low

```

### Stage11 gene_variant_counts.tsv

- path: `results/run_2026_05_30_071639/processed/stage_11_gene_variant_counts.tsv`
- size_bytes: 798796
- rows: 
- columns: 2
- header_sha256: `a728a2468d9a3e433005a28bf32c7a8a5cce42466215a1338be8933e0d5ade04`
- has_variant_id: no
- distinct_variant_ids: NA

Header:
```text
     1	gene_id
     2	variant_count
```

First data row preview:
```text
NA	100675

```

### Stage12 validation_candidates.tsv

- path: `results/run_2026_05_30_071639/processed/stage_12_validation_candidates.tsv`
- size_bytes: 397759340
- rows: 
- columns: 56
- header_sha256: `d43ee98c7824c468f1e6523d1886bf0d1164aa6e1003677f73093d557ac2d385`
- has_variant_id: yes
- distinct_variant_ids: 674593

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
    34	functional_impact
    35	rarity_flag
    36	clinical_evidence
    37	qc_reliability
    38	coding_interpretation_label
    39	is_lof_candidate
    40	is_rare_candidate
    41	is_clinically_supported
    42	is_high_quality
    43	is_potential_artifact
    44	variant_origin
    45	source_interpretation_label
    46	priority_tier
    47	priority_rank
    48	priority_reason
    49	is_high_priority_candidate
    50	is_moderate_priority_candidate
    51	is_low_priority_candidate
    52	is_uninterpretable
    53	validation_required
    54	validation_priority
    55	suggested_validation_method
    56	validation_reason
```

First data row preview:
```text
ERR10619203	run_2026_05_30_071639	variant_annotation_pipeline	1:69270:A:G	1	69270	A	G	snv	coding	PASS	ENSG00000186092	OR4F5	ENST00000641515.2	synonymous_variant	LOW	NA	NA	0.9961	0.9961	NA	NA	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	coding	LOW	pass	interpretable_now	common	missing	synonymous	common	missing	high_confidence	coding_common_or_low_support	False	False	False	True	False	coding	coding_common_or_low_support	tier_3_low_support_or_common	3	coding label coding_common_or_low

```

# Transition Lineage

### Stage07 annotated → Stage08 selected

| Metric | Stage07 annotated | Stage08 selected |
|---|---:|---:|
| rows |  |  |
| columns | 25 | 33 |
| distinct_variant_ids | 674593 | 674593 |

Removed columns:
```text
epilepsy_flag,impact
```

Added columns:
```text
annotation_source,annotation_version,clinical_status,epilepsy_flag,frequency_status,gene_mapping_status,interpretability_status,qc_status,variant_context,variant_effect_severity
```

Shared columns:
```text
alternate_allele,chromosome,clinical_significance,clinvar_significance,consequence,exac_af,gene_id,gene_symbol,gnomad_af,impact_class,mito_flag,population_frequency,position,quality_flag,reference_allele,run_id,sample_id,source_pipeline,thousand_genomes_af,transcript_id,variant_class,variant_id,variant_type
```

### Stage08 selected → Stage08 VDB-ready

| Metric | Stage08 selected | Stage08 VDB-ready |
|---|---:|---:|
| rows |  |  |
| columns | 33 | 33 |
| distinct_variant_ids | 674593 | 674593 |

Removed columns:
```text
NONE
```

Added columns:
```text
NONE
```

Shared columns:
```text
alternate_allele,annotation_source,annotation_version,chromosome,clinical_significance,clinical_status,clinvar_significance,consequence,epilepsy_flag,exac_af,frequency_status,gene_id,gene_mapping_status,gene_symbol,gnomad_af,impact_class,interpretability_status,mito_flag,population_frequency,position,qc_status,quality_flag,reference_allele,run_id,sample_id,source_pipeline,thousand_genomes_af,transcript_id,variant_class,variant_context,variant_effect_severity,variant_id,variant_type
```

### Stage08 VDB-ready → Stage09 coding interpreted

| Metric | Stage08 VDB-ready | Stage09 coding interpreted |
|---|---:|---:|
| rows |  |  |
| columns | 33 | 43 |
| distinct_variant_ids | 674593 | 26271 |

Removed columns:
```text
clinical_status
```

Added columns:
```text
clinical_evidence,clinical_status,coding_interpretation_label,functional_impact,is_clinically_supported,is_high_quality,is_lof_candidate,is_potential_artifact,is_rare_candidate,qc_reliability,rarity_flag
```

Shared columns:
```text
alternate_allele,annotation_source,annotation_version,chromosome,clinical_significance,clinvar_significance,consequence,epilepsy_flag,exac_af,frequency_status,gene_id,gene_mapping_status,gene_symbol,gnomad_af,impact_class,interpretability_status,mito_flag,population_frequency,position,qc_status,quality_flag,reference_allele,run_id,sample_id,source_pipeline,thousand_genomes_af,transcript_id,variant_class,variant_context,variant_effect_severity,variant_id,variant_type
```

### Stage08 VDB-ready → Stage10 noncoding interpreted

| Metric | Stage08 VDB-ready | Stage10 noncoding interpreted |
|---|---:|---:|
| rows |  |  |
| columns | 33 | 43 |
| distinct_variant_ids | 674593 | 648322 |

Removed columns:
```text
clinical_status
```

Added columns:
```text
clinical_evidence,clinical_status,is_clinically_supported,is_high_quality,is_potential_artifact,is_rare_candidate,is_regulatory_candidate,noncoding_functional_context,noncoding_interpretation_label,qc_reliability,rarity_flag
```

Shared columns:
```text
alternate_allele,annotation_source,annotation_version,chromosome,clinical_significance,clinvar_significance,consequence,epilepsy_flag,exac_af,frequency_status,gene_id,gene_mapping_status,gene_symbol,gnomad_af,impact_class,interpretability_status,mito_flag,population_frequency,position,qc_status,quality_flag,reference_allele,run_id,sample_id,source_pipeline,thousand_genomes_af,transcript_id,variant_class,variant_context,variant_effect_severity,variant_id,variant_type
```

### Stage09 coding interpreted → Stage11 prioritized

| Metric | Stage09 coding interpreted | Stage11 prioritized |
|---|---:|---:|
| rows |  |  |
| columns | 43 | 52 |
| distinct_variant_ids | 26271 | 674593 |

Removed columns:
```text
is_potential_artifact
```

Added columns:
```text
is_high_priority_candidate,is_low_priority_candidate,is_moderate_priority_candidate,is_potential_artifact,is_uninterpretable,priority_rank,priority_reason,priority_tier,source_interpretation_label,variant_origin
```

Shared columns:
```text
alternate_allele,annotation_source,annotation_version,chromosome,clinical_evidence,clinical_significance,clinical_status,clinvar_significance,coding_interpretation_label,consequence,epilepsy_flag,exac_af,frequency_status,functional_impact,gene_id,gene_mapping_status,gene_symbol,gnomad_af,impact_class,interpretability_status,is_clinically_supported,is_high_quality,is_lof_candidate,is_rare_candidate,mito_flag,population_frequency,position,qc_reliability,qc_status,quality_flag,rarity_flag,reference_allele,run_id,sample_id,source_pipeline,thousand_genomes_af,transcript_id,variant_class,variant_context,variant_effect_severity,variant_id,variant_type
```

### Stage10 noncoding interpreted → Stage11 prioritized

| Metric | Stage10 noncoding interpreted | Stage11 prioritized |
|---|---:|---:|
| rows |  |  |
| columns | 43 | 52 |
| distinct_variant_ids | 648322 | 674593 |

Removed columns:
```text
is_potential_artifact,is_regulatory_candidate,noncoding_functional_context,noncoding_interpretation_label
```

Added columns:
```text
coding_interpretation_label,functional_impact,is_high_priority_candidate,is_lof_candidate,is_low_priority_candidate,is_moderate_priority_candidate,is_potential_artifact,is_uninterpretable,priority_rank,priority_reason,priority_tier,source_interpretation_label,variant_origin
```

Shared columns:
```text
alternate_allele,annotation_source,annotation_version,chromosome,clinical_evidence,clinical_significance,clinical_status,clinvar_significance,consequence,epilepsy_flag,exac_af,frequency_status,gene_id,gene_mapping_status,gene_symbol,gnomad_af,impact_class,interpretability_status,is_clinically_supported,is_high_quality,is_rare_candidate,mito_flag,population_frequency,position,qc_reliability,qc_status,quality_flag,rarity_flag,reference_allele,run_id,sample_id,source_pipeline,thousand_genomes_af,transcript_id,variant_class,variant_context,variant_effect_severity,variant_id,variant_type
```

### Stage11 prioritized → Stage12 validation candidates

| Metric | Stage11 prioritized | Stage12 validation candidates |
|---|---:|---:|
| rows |  |  |
| columns | 52 | 56 |
| distinct_variant_ids | 674593 | 674593 |

Removed columns:
```text
is_uninterpretable
```

Added columns:
```text
is_uninterpretable,suggested_validation_method,validation_priority,validation_reason,validation_required
```

Shared columns:
```text
alternate_allele,annotation_source,annotation_version,chromosome,clinical_evidence,clinical_significance,clinical_status,clinvar_significance,coding_interpretation_label,consequence,epilepsy_flag,exac_af,frequency_status,functional_impact,gene_id,gene_mapping_status,gene_symbol,gnomad_af,impact_class,interpretability_status,is_clinically_supported,is_high_priority_candidate,is_high_quality,is_lof_candidate,is_low_priority_candidate,is_moderate_priority_candidate,is_potential_artifact,is_rare_candidate,mito_flag,population_frequency,position,priority_rank,priority_reason,priority_tier,qc_reliability,qc_status,quality_flag,rarity_flag,reference_allele,run_id,sample_id,source_interpretation_label,source_pipeline,thousand_genomes_af,transcript_id,variant_class,variant_context,variant_effect_severity,variant_id,variant_origin,variant_type
```

---

## ERR10619207 / run_2026_06_01_124134 / q3

# Artifact Inventory

### Stage07 annotated_variants.tsv

- path: `results/run_2026_06_01_124134/processed/ERR10619207_run_2026_06_01_124134.annotated_variants.tsv`
- size_bytes: 159051766
- rows: 
- columns: 25
- header_sha256: `617480c310358e0f764d2996153e3428ee6270702ce98194140c6e7ba6074d9f`
- has_variant_id: yes
- distinct_variant_ids: 678379

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	quality_flag
    10	gene_id
    11	gene_symbol
    12	transcript_id
    13	consequence
    14	impact_class
    15	impact
    16	variant_class
    17	variant_type
    18	clinical_significance
    19	clinvar_significance
    20	population_frequency
    21	gnomad_af
    22	exac_af
    23	thousand_genomes_af
    24	mito_flag
    25	epilepsy_flag
```

First data row preview:
```text
ERR10619207	run_2026_06_01_124134	variant_annotation_pipeline	1:13649:G:C	1	13649	G	C	PASS	ENSG00000223972	DDX11L1	ENST00000450305.2	non_coding_transcript_exon_variant	MODIFIER	MODIFIER	SNV	non-coding	NA	NA	0.2367	0.2367	NA	NA	False	False

```

### Stage08 selected_transcript_consequences.tsv

- path: `results/run_2026_06_01_124134/processed/stage_08_selected_transcript_consequences.tsv`
- size_bytes: 228741540
- rows: 
- columns: 33
- header_sha256: `cd5a915c5bc9d15f76cda12616b5dae1e039ecb5f00164e46acc177e2d42a402`
- has_variant_id: yes
- distinct_variant_ids: 678379

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
```

First data row preview:
```text
ERR10619207	run_2026_06_01_124134	variant_annotation_pipeline	1:13649:G:C	1	13649	G	C	snv	noncoding	PASS	ENSG00000223972	DDX11L1	ENST00000450305.2	non_coding_transcript_exon_variant	MODIFIER	NA	NA	0.2367	0.2367	NA	NA	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	noncoding_transcript	MODIFIER	pass	needs_external_annotation	common	missing

```

### Stage08 vdb_ready_variants.tsv

- path: `results/run_2026_06_01_124134/processed/stage_08_vdb_ready_variants.tsv`
- size_bytes: 228741540
- rows: 
- columns: 33
- header_sha256: `cd5a915c5bc9d15f76cda12616b5dae1e039ecb5f00164e46acc177e2d42a402`
- has_variant_id: yes
- distinct_variant_ids: 678379

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
```

First data row preview:
```text
ERR10619207	run_2026_06_01_124134	variant_annotation_pipeline	1:13649:G:C	1	13649	G	C	snv	noncoding	PASS	ENSG00000223972	DDX11L1	ENST00000450305.2	non_coding_transcript_exon_variant	MODIFIER	NA	NA	0.2367	0.2367	NA	NA	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	noncoding_transcript	MODIFIER	pass	needs_external_annotation	common	missing

```

### Stage08 coding_candidates.tsv

- path: `results/run_2026_06_01_124134/processed/coding_candidates.tsv`
- size_bytes: 7763821
- rows: 
- columns: 33
- header_sha256: `cd5a915c5bc9d15f76cda12616b5dae1e039ecb5f00164e46acc177e2d42a402`
- has_variant_id: yes
- distinct_variant_ids: 24149

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
```

First data row preview:
```text
ERR10619207	run_2026_06_01_124134	variant_annotation_pipeline	1:946247:G:A	1	946247	G	A	snv	coding	PASS	ENSG00000188976	NOC2L	ENST00000327044.7	synonymous_variant	LOW	NA	NA	0.4419	0.4419	NA	0.0643	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	coding	LOW	pass	interpretable_now	common	missing

```

### Stage08 splice_region_candidates.tsv

- path: `results/run_2026_06_01_124134/processed/splice_region_candidates.tsv`
- size_bytes: 1073036
- rows: 
- columns: 33
- header_sha256: `cd5a915c5bc9d15f76cda12616b5dae1e039ecb5f00164e46acc177e2d42a402`
- has_variant_id: yes
- distinct_variant_ids: 2899

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
```

First data row preview:
```text
ERR10619207	run_2026_06_01_124134	variant_annotation_pipeline	1:16856:A:G	1	16856	A	G	snv	coding	PASS	ENSG00000310526	WASH7P	ENST00000831140.1	splice_donor_variant&non_coding_transcript_variant	HIGH	NA	NA	0.02175	0.02175	NA	NA	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	HIGH	pass	interpretable_now	low_frequency	missing

```

### Stage08 noncoding_candidates.tsv

- path: `results/run_2026_06_01_124134/processed/noncoding_candidates.tsv`
- size_bytes: 220078631
- rows: 
- columns: 33
- header_sha256: `cd5a915c5bc9d15f76cda12616b5dae1e039ecb5f00164e46acc177e2d42a402`
- has_variant_id: yes
- distinct_variant_ids: 651824

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
```

First data row preview:
```text
ERR10619207	run_2026_06_01_124134	variant_annotation_pipeline	1:13649:G:C	1	13649	G	C	snv	noncoding	PASS	ENSG00000223972	DDX11L1	ENST00000450305.2	non_coding_transcript_exon_variant	MODIFIER	NA	NA	0.2367	0.2367	NA	NA	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	noncoding_transcript	MODIFIER	pass	needs_external_annotation	common	missing

```

### Stage08 variant_summary.tsv

- path: `results/run_2026_06_01_124134/processed/stage_08_variant_summary.tsv`
- size_bytes: 172101761
- rows: 
- columns: 26
- header_sha256: `a0088e61e1ce409de45d1365b177ff47234ecb57dacab3ef0cb50fe3f613b55a`
- has_variant_id: yes
- distinct_variant_ids: 678379

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	gene_symbols
    10	gene_mapping_status
    11	worst_consequence
    12	highest_impact
    13	canonical_present
    14	coding_flag
    15	splice_flag
    16	noncoding_flag
    17	transcript_count
    18	variant_type
    19	variant_class
    20	quality_flag
    21	qc_status
    22	population_frequency
    23	frequency_status
    24	clinical_status
    25	annotation_source
    26	annotation_version
```

First data row preview:
```text
ERR10619207	run_2026_06_01_124134	variant_annotation_pipeline	10:100006744:C:G	10	100006744	C	G	DNMBP	mapped	intron_variant	MODIFIER	False	False	False	True	1	snv	noncoding	PASS	pass	0.2496	common	missing	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #

```

### Stage08 rdgp_gene_evidence_seed.tsv

- path: `results/run_2026_06_01_124134/processed/stage_08_rdgp_gene_evidence_seed.tsv`
- size_bytes: 11748002
- rows: 
- columns: 10
- header_sha256: `18d500222bcf3f2b99e044e14b9a1f0647d3f9bf1593555fa16359bb3996d3a3`
- has_variant_id: no
- distinct_variant_ids: NA

Header:
```text
     1	sample_id
     2	gene_id
     3	gene_symbol
     4	variant_count
     5	high_impact_variant_count
     6	rare_variant_count
     7	pathogenic_variant_count
     8	max_variant_severity
     9	has_low_quality_evidence
    10	contributing_variant_ids
```

First data row preview:
```text
ERR10619207	ENSG00000000003	TSPAN6	2	0	0	0	MODIFIER	False	X:100624191:G:C,X:100624362:T:C

```

### Stage09 coding_interpreted.tsv

- path: `results/run_2026_06_01_124134/processed/stage_09_coding_interpreted.tsv`
- size_bytes: 11302159
- rows: 
- columns: 43
- header_sha256: `8132a0aab15233fd27576c5624b2e8393fe622aa2bd651c8bdfc94c6215d5d3b`
- has_variant_id: yes
- distinct_variant_ids: 26555

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
    34	functional_impact
    35	rarity_flag
    36	clinical_evidence
    37	qc_reliability
    38	coding_interpretation_label
    39	is_lof_candidate
    40	is_rare_candidate
    41	is_clinically_supported
    42	is_high_quality
    43	is_potential_artifact
```

First data row preview:
```text
ERR10619207	run_2026_06_01_124134	variant_annotation_pipeline	1:946247:G:A	1	946247	G	A	snv	coding	PASS	ENSG00000188976	NOC2L	ENST00000327044.7	synonymous_variant	LOW	NA	NA	0.4419	0.4419	NA	0.0643	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	coding	LOW	pass	interpretable_now	common	missing	synonymous	common	missing	high_confidence	coding_common_or_low_support	False	False	False	True	False

```

### Stage10 noncoding_interpreted.tsv

- path: `results/run_2026_06_01_124134/processed/stage_10_noncoding_interpreted.tsv`
- size_bytes: 287209270
- rows: 
- columns: 43
- header_sha256: `52d4bd70320ef627d745025507d0b4bd3197d1fef0d1436811b20a6c4486c87e`
- has_variant_id: yes
- distinct_variant_ids: 651824

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
    34	noncoding_functional_context
    35	rarity_flag
    36	clinical_evidence
    37	qc_reliability
    38	noncoding_interpretation_label
    39	is_regulatory_candidate
    40	is_rare_candidate
    41	is_clinically_supported
    42	is_high_quality
    43	is_potential_artifact
```

First data row preview:
```text
ERR10619207	run_2026_06_01_124134	variant_annotation_pipeline	1:13649:G:C	1	13649	G	C	snv	noncoding	PASS	ENSG00000223972	DDX11L1	ENST00000450305.2	non_coding_transcript_exon_variant	MODIFIER	NA	NA	0.2367	0.2367	NA	NA	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	noncoding_transcript	MODIFIER	pass	needs_external_annotation	common	missing	transcript_associated	common	missing	high_confidence	noncoding_common_or_low_support	False	False	False	True	False

```

### Stage11 prioritized_variants.tsv

- path: `results/run_2026_06_01_124134/processed/stage_11_prioritized_variants.tsv`
- size_bytes: 369165975
- rows: 
- columns: 52
- header_sha256: `446c7603e23bb60bb4da68196782174abe5aea562307628ddf55513a5e4bae54`
- has_variant_id: yes
- distinct_variant_ids: 678379

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
    34	functional_impact
    35	rarity_flag
    36	clinical_evidence
    37	qc_reliability
    38	coding_interpretation_label
    39	is_lof_candidate
    40	is_rare_candidate
    41	is_clinically_supported
    42	is_high_quality
    43	is_potential_artifact
    44	variant_origin
    45	source_interpretation_label
    46	priority_tier
    47	priority_rank
    48	priority_reason
    49	is_high_priority_candidate
    50	is_moderate_priority_candidate
    51	is_low_priority_candidate
    52	is_uninterpretable
```

First data row preview:
```text
ERR10619207	run_2026_06_01_124134	variant_annotation_pipeline	1:946247:G:A	1	946247	G	A	snv	coding	PASS	ENSG00000188976	NOC2L	ENST00000327044.7	synonymous_variant	LOW	NA	NA	0.4419	0.4419	NA	0.0643	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	coding	LOW	pass	interpretable_now	common	missing	synonymous	common	missing	high_confidence	coding_common_or_low_support	False	False	False	True	False	coding	coding_common_or_low_support	tier_3_low_support_or_common	3	coding label coding_common_

```

### Stage11 gene_variant_counts.tsv

- path: `results/run_2026_06_01_124134/processed/stage_11_gene_variant_counts.tsv`
- size_bytes: 799573
- rows: 
- columns: 2
- header_sha256: `a728a2468d9a3e433005a28bf32c7a8a5cce42466215a1338be8933e0d5ade04`
- has_variant_id: no
- distinct_variant_ids: NA

Header:
```text
     1	gene_id
     2	variant_count
```

First data row preview:
```text
NA	103302

```

### Stage12 validation_candidates.tsv

- path: `results/run_2026_06_01_124134/processed/stage_12_validation_candidates.tsv`
- size_bytes: 399893774
- rows: 
- columns: 56
- header_sha256: `d43ee98c7824c468f1e6523d1886bf0d1164aa6e1003677f73093d557ac2d385`
- has_variant_id: yes
- distinct_variant_ids: 678379

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
    34	functional_impact
    35	rarity_flag
    36	clinical_evidence
    37	qc_reliability
    38	coding_interpretation_label
    39	is_lof_candidate
    40	is_rare_candidate
    41	is_clinically_supported
    42	is_high_quality
    43	is_potential_artifact
    44	variant_origin
    45	source_interpretation_label
    46	priority_tier
    47	priority_rank
    48	priority_reason
    49	is_high_priority_candidate
    50	is_moderate_priority_candidate
    51	is_low_priority_candidate
    52	is_uninterpretable
    53	validation_required
    54	validation_priority
    55	suggested_validation_method
    56	validation_reason
```

First data row preview:
```text
ERR10619207	run_2026_06_01_124134	variant_annotation_pipeline	1:946247:G:A	1	946247	G	A	snv	coding	PASS	ENSG00000188976	NOC2L	ENST00000327044.7	synonymous_variant	LOW	NA	NA	0.4419	0.4419	NA	0.0643	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	coding	LOW	pass	interpretable_now	common	missing	synonymous	common	missing	high_confidence	coding_common_or_low_support	False	False	False	True	False	coding	coding_common_or_low_support	tier_3_low_support_or_common	3	coding label coding_common_

```

# Transition Lineage

### Stage07 annotated → Stage08 selected

| Metric | Stage07 annotated | Stage08 selected |
|---|---:|---:|
| rows |  |  |
| columns | 25 | 33 |
| distinct_variant_ids | 678379 | 678379 |

Removed columns:
```text
epilepsy_flag,impact
```

Added columns:
```text
annotation_source,annotation_version,clinical_status,epilepsy_flag,frequency_status,gene_mapping_status,interpretability_status,qc_status,variant_context,variant_effect_severity
```

Shared columns:
```text
alternate_allele,chromosome,clinical_significance,clinvar_significance,consequence,exac_af,gene_id,gene_symbol,gnomad_af,impact_class,mito_flag,population_frequency,position,quality_flag,reference_allele,run_id,sample_id,source_pipeline,thousand_genomes_af,transcript_id,variant_class,variant_id,variant_type
```

### Stage08 selected → Stage08 VDB-ready

| Metric | Stage08 selected | Stage08 VDB-ready |
|---|---:|---:|
| rows |  |  |
| columns | 33 | 33 |
| distinct_variant_ids | 678379 | 678379 |

Removed columns:
```text
NONE
```

Added columns:
```text
NONE
```

Shared columns:
```text
alternate_allele,annotation_source,annotation_version,chromosome,clinical_significance,clinical_status,clinvar_significance,consequence,epilepsy_flag,exac_af,frequency_status,gene_id,gene_mapping_status,gene_symbol,gnomad_af,impact_class,interpretability_status,mito_flag,population_frequency,position,qc_status,quality_flag,reference_allele,run_id,sample_id,source_pipeline,thousand_genomes_af,transcript_id,variant_class,variant_context,variant_effect_severity,variant_id,variant_type
```

### Stage08 VDB-ready → Stage09 coding interpreted

| Metric | Stage08 VDB-ready | Stage09 coding interpreted |
|---|---:|---:|
| rows |  |  |
| columns | 33 | 43 |
| distinct_variant_ids | 678379 | 26555 |

Removed columns:
```text
clinical_status
```

Added columns:
```text
clinical_evidence,clinical_status,coding_interpretation_label,functional_impact,is_clinically_supported,is_high_quality,is_lof_candidate,is_potential_artifact,is_rare_candidate,qc_reliability,rarity_flag
```

Shared columns:
```text
alternate_allele,annotation_source,annotation_version,chromosome,clinical_significance,clinvar_significance,consequence,epilepsy_flag,exac_af,frequency_status,gene_id,gene_mapping_status,gene_symbol,gnomad_af,impact_class,interpretability_status,mito_flag,population_frequency,position,qc_status,quality_flag,reference_allele,run_id,sample_id,source_pipeline,thousand_genomes_af,transcript_id,variant_class,variant_context,variant_effect_severity,variant_id,variant_type
```

### Stage08 VDB-ready → Stage10 noncoding interpreted

| Metric | Stage08 VDB-ready | Stage10 noncoding interpreted |
|---|---:|---:|
| rows |  |  |
| columns | 33 | 43 |
| distinct_variant_ids | 678379 | 651824 |

Removed columns:
```text
clinical_status
```

Added columns:
```text
clinical_evidence,clinical_status,is_clinically_supported,is_high_quality,is_potential_artifact,is_rare_candidate,is_regulatory_candidate,noncoding_functional_context,noncoding_interpretation_label,qc_reliability,rarity_flag
```

Shared columns:
```text
alternate_allele,annotation_source,annotation_version,chromosome,clinical_significance,clinvar_significance,consequence,epilepsy_flag,exac_af,frequency_status,gene_id,gene_mapping_status,gene_symbol,gnomad_af,impact_class,interpretability_status,mito_flag,population_frequency,position,qc_status,quality_flag,reference_allele,run_id,sample_id,source_pipeline,thousand_genomes_af,transcript_id,variant_class,variant_context,variant_effect_severity,variant_id,variant_type
```

### Stage09 coding interpreted → Stage11 prioritized

| Metric | Stage09 coding interpreted | Stage11 prioritized |
|---|---:|---:|
| rows |  |  |
| columns | 43 | 52 |
| distinct_variant_ids | 26555 | 678379 |

Removed columns:
```text
is_potential_artifact
```

Added columns:
```text
is_high_priority_candidate,is_low_priority_candidate,is_moderate_priority_candidate,is_potential_artifact,is_uninterpretable,priority_rank,priority_reason,priority_tier,source_interpretation_label,variant_origin
```

Shared columns:
```text
alternate_allele,annotation_source,annotation_version,chromosome,clinical_evidence,clinical_significance,clinical_status,clinvar_significance,coding_interpretation_label,consequence,epilepsy_flag,exac_af,frequency_status,functional_impact,gene_id,gene_mapping_status,gene_symbol,gnomad_af,impact_class,interpretability_status,is_clinically_supported,is_high_quality,is_lof_candidate,is_rare_candidate,mito_flag,population_frequency,position,qc_reliability,qc_status,quality_flag,rarity_flag,reference_allele,run_id,sample_id,source_pipeline,thousand_genomes_af,transcript_id,variant_class,variant_context,variant_effect_severity,variant_id,variant_type
```

### Stage10 noncoding interpreted → Stage11 prioritized

| Metric | Stage10 noncoding interpreted | Stage11 prioritized |
|---|---:|---:|
| rows |  |  |
| columns | 43 | 52 |
| distinct_variant_ids | 651824 | 678379 |

Removed columns:
```text
is_potential_artifact,is_regulatory_candidate,noncoding_functional_context,noncoding_interpretation_label
```

Added columns:
```text
coding_interpretation_label,functional_impact,is_high_priority_candidate,is_lof_candidate,is_low_priority_candidate,is_moderate_priority_candidate,is_potential_artifact,is_uninterpretable,priority_rank,priority_reason,priority_tier,source_interpretation_label,variant_origin
```

Shared columns:
```text
alternate_allele,annotation_source,annotation_version,chromosome,clinical_evidence,clinical_significance,clinical_status,clinvar_significance,consequence,epilepsy_flag,exac_af,frequency_status,gene_id,gene_mapping_status,gene_symbol,gnomad_af,impact_class,interpretability_status,is_clinically_supported,is_high_quality,is_rare_candidate,mito_flag,population_frequency,position,qc_reliability,qc_status,quality_flag,rarity_flag,reference_allele,run_id,sample_id,source_pipeline,thousand_genomes_af,transcript_id,variant_class,variant_context,variant_effect_severity,variant_id,variant_type
```

### Stage11 prioritized → Stage12 validation candidates

| Metric | Stage11 prioritized | Stage12 validation candidates |
|---|---:|---:|
| rows |  |  |
| columns | 52 | 56 |
| distinct_variant_ids | 678379 | 678379 |

Removed columns:
```text
is_uninterpretable
```

Added columns:
```text
is_uninterpretable,suggested_validation_method,validation_priority,validation_reason,validation_required
```

Shared columns:
```text
alternate_allele,annotation_source,annotation_version,chromosome,clinical_evidence,clinical_significance,clinical_status,clinvar_significance,coding_interpretation_label,consequence,epilepsy_flag,exac_af,frequency_status,functional_impact,gene_id,gene_mapping_status,gene_symbol,gnomad_af,impact_class,interpretability_status,is_clinically_supported,is_high_priority_candidate,is_high_quality,is_lof_candidate,is_low_priority_candidate,is_moderate_priority_candidate,is_potential_artifact,is_rare_candidate,mito_flag,population_frequency,position,priority_rank,priority_reason,priority_tier,qc_reliability,qc_status,quality_flag,rarity_flag,reference_allele,run_id,sample_id,source_interpretation_label,source_pipeline,thousand_genomes_af,transcript_id,variant_class,variant_context,variant_effect_severity,variant_id,variant_origin,variant_type
```

---

## ERR10619208 / run_2026_05_30_151355 / median

# Artifact Inventory

### Stage07 annotated_variants.tsv

- path: `results/run_2026_05_30_151355/processed/ERR10619208_run_2026_05_30_151355.annotated_variants.tsv`
- size_bytes: 199088085
- rows: 
- columns: 25
- header_sha256: `617480c310358e0f764d2996153e3428ee6270702ce98194140c6e7ba6074d9f`
- has_variant_id: yes
- distinct_variant_ids: 849399

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	quality_flag
    10	gene_id
    11	gene_symbol
    12	transcript_id
    13	consequence
    14	impact_class
    15	impact
    16	variant_class
    17	variant_type
    18	clinical_significance
    19	clinvar_significance
    20	population_frequency
    21	gnomad_af
    22	exac_af
    23	thousand_genomes_af
    24	mito_flag
    25	epilepsy_flag
```

First data row preview:
```text
ERR10619208	run_2026_05_30_151355	variant_annotation_pipeline	1:13813:T:G	1	13813	T	G	PASS	ENSG00000290825	DDX11L16	ENST00000832823.1	upstream_gene_variant	MODIFIER	MODIFIER	SNV	non-coding	NA	NA	0.4861	0.4861	NA	NA	False	False

```

### Stage08 selected_transcript_consequences.tsv

- path: `results/run_2026_05_30_151355/processed/stage_08_selected_transcript_consequences.tsv`
- size_bytes: 286434617
- rows: 
- columns: 33
- header_sha256: `cd5a915c5bc9d15f76cda12616b5dae1e039ecb5f00164e46acc177e2d42a402`
- has_variant_id: yes
- distinct_variant_ids: 849399

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
```

First data row preview:
```text
ERR10619208	run_2026_05_30_151355	variant_annotation_pipeline	1:13813:T:G	1	13813	T	G	snv	noncoding	PASS	ENSG00000290825	DDX11L16	ENST00000832823.1	upstream_gene_variant	MODIFIER	NA	NA	0.4861	0.4861	NA	NA	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	regulatory	MODIFIER	pass	needs_external_annotation	common	missing

```

### Stage08 vdb_ready_variants.tsv

- path: `results/run_2026_05_30_151355/processed/stage_08_vdb_ready_variants.tsv`
- size_bytes: 286434617
- rows: 
- columns: 33
- header_sha256: `cd5a915c5bc9d15f76cda12616b5dae1e039ecb5f00164e46acc177e2d42a402`
- has_variant_id: yes
- distinct_variant_ids: 849399

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
```

First data row preview:
```text
ERR10619208	run_2026_05_30_151355	variant_annotation_pipeline	1:13813:T:G	1	13813	T	G	snv	noncoding	PASS	ENSG00000290825	DDX11L16	ENST00000832823.1	upstream_gene_variant	MODIFIER	NA	NA	0.4861	0.4861	NA	NA	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	regulatory	MODIFIER	pass	needs_external_annotation	common	missing

```

### Stage08 coding_candidates.tsv

- path: `results/run_2026_05_30_151355/processed/coding_candidates.tsv`
- size_bytes: 8198261
- rows: 
- columns: 33
- header_sha256: `cd5a915c5bc9d15f76cda12616b5dae1e039ecb5f00164e46acc177e2d42a402`
- has_variant_id: yes
- distinct_variant_ids: 25497

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
```

First data row preview:
```text
ERR10619208	run_2026_05_30_151355	variant_annotation_pipeline	1:924533:A:G	1	924533	A	G	snv	coding	PASS	ENSG00000187634	SAMD11	ENST00000616016.5	synonymous_variant	LOW	NA	NA	0.7498	0.7498	NA	0.4039	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	coding	LOW	pass	interpretable_now	common	missing

```

### Stage08 splice_region_candidates.tsv

- path: `results/run_2026_05_30_151355/processed/splice_region_candidates.tsv`
- size_bytes: 1140291
- rows: 
- columns: 33
- header_sha256: `cd5a915c5bc9d15f76cda12616b5dae1e039ecb5f00164e46acc177e2d42a402`
- has_variant_id: yes
- distinct_variant_ids: 3084

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
```

First data row preview:
```text
ERR10619208	run_2026_05_30_151355	variant_annotation_pipeline	1:962350:C:T	1	962350	C	T	snv	coding	PASS	ENSG00000187961	KLHL17	ENST00000338591.8	splice_region_variant&splice_polypyrimidine_tract_variant&intron_variant	LOW	NA	NA	0.1747	0.0775	NA	0.1747	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	missing

```

### Stage08 noncoding_candidates.tsv

- path: `results/run_2026_05_30_151355/processed/noncoding_candidates.tsv`
- size_bytes: 277286443
- rows: 
- columns: 33
- header_sha256: `cd5a915c5bc9d15f76cda12616b5dae1e039ecb5f00164e46acc177e2d42a402`
- has_variant_id: yes
- distinct_variant_ids: 821358

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
```

First data row preview:
```text
ERR10619208	run_2026_05_30_151355	variant_annotation_pipeline	1:13813:T:G	1	13813	T	G	snv	noncoding	PASS	ENSG00000290825	DDX11L16	ENST00000832823.1	upstream_gene_variant	MODIFIER	NA	NA	0.4861	0.4861	NA	NA	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	regulatory	MODIFIER	pass	needs_external_annotation	common	missing

```

### Stage08 variant_summary.tsv

- path: `results/run_2026_05_30_151355/processed/stage_08_variant_summary.tsv`
- size_bytes: 215651941
- rows: 
- columns: 26
- header_sha256: `a0088e61e1ce409de45d1365b177ff47234ecb57dacab3ef0cb50fe3f613b55a`
- has_variant_id: yes
- distinct_variant_ids: 849399

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	gene_symbols
    10	gene_mapping_status
    11	worst_consequence
    12	highest_impact
    13	canonical_present
    14	coding_flag
    15	splice_flag
    16	noncoding_flag
    17	transcript_count
    18	variant_type
    19	variant_class
    20	quality_flag
    21	qc_status
    22	population_frequency
    23	frequency_status
    24	clinical_status
    25	annotation_source
    26	annotation_version
```

First data row preview:
```text
ERR10619208	run_2026_05_30_151355	variant_annotation_pipeline	10:100007383:A:C	10	100007383	A	C	DNMBP	mapped	intron_variant	MODIFIER	False	False	False	True	1	snv	noncoding	PASS	pass	0.4062	common	missing	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #

```

### Stage08 rdgp_gene_evidence_seed.tsv

- path: `results/run_2026_05_30_151355/processed/stage_08_rdgp_gene_evidence_seed.tsv`
- size_bytes: 14131609
- rows: 
- columns: 10
- header_sha256: `18d500222bcf3f2b99e044e14b9a1f0647d3f9bf1593555fa16359bb3996d3a3`
- has_variant_id: no
- distinct_variant_ids: NA

Header:
```text
     1	sample_id
     2	gene_id
     3	gene_symbol
     4	variant_count
     5	high_impact_variant_count
     6	rare_variant_count
     7	pathogenic_variant_count
     8	max_variant_severity
     9	has_low_quality_evidence
    10	contributing_variant_ids
```

First data row preview:
```text
ERR10619208	ENSG00000000003	TSPAN6	3	0	1	0	MODIFIER	False	X:100624693:A:T,X:100624733:C:T,X:100634498:CT:C

```

### Stage09 coding_interpreted.tsv

- path: `results/run_2026_05_30_151355/processed/stage_09_coding_interpreted.tsv`
- size_bytes: 11935354
- rows: 
- columns: 43
- header_sha256: `8132a0aab15233fd27576c5624b2e8393fe622aa2bd651c8bdfc94c6215d5d3b`
- has_variant_id: yes
- distinct_variant_ids: 28041

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
    34	functional_impact
    35	rarity_flag
    36	clinical_evidence
    37	qc_reliability
    38	coding_interpretation_label
    39	is_lof_candidate
    40	is_rare_candidate
    41	is_clinically_supported
    42	is_high_quality
    43	is_potential_artifact
```

First data row preview:
```text
ERR10619208	run_2026_05_30_151355	variant_annotation_pipeline	1:924533:A:G	1	924533	A	G	snv	coding	PASS	ENSG00000187634	SAMD11	ENST00000616016.5	synonymous_variant	LOW	NA	NA	0.7498	0.7498	NA	0.4039	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	coding	LOW	pass	interpretable_now	common	missing	synonymous	common	missing	high_confidence	coding_common_or_low_support	False	False	False	True	False

```

### Stage10 noncoding_interpreted.tsv

- path: `results/run_2026_05_30_151355/processed/stage_10_noncoding_interpreted.tsv`
- size_bytes: 361941536
- rows: 
- columns: 43
- header_sha256: `52d4bd70320ef627d745025507d0b4bd3197d1fef0d1436811b20a6c4486c87e`
- has_variant_id: yes
- distinct_variant_ids: 821358

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
    34	noncoding_functional_context
    35	rarity_flag
    36	clinical_evidence
    37	qc_reliability
    38	noncoding_interpretation_label
    39	is_regulatory_candidate
    40	is_rare_candidate
    41	is_clinically_supported
    42	is_high_quality
    43	is_potential_artifact
```

First data row preview:
```text
ERR10619208	run_2026_05_30_151355	variant_annotation_pipeline	1:13813:T:G	1	13813	T	G	snv	noncoding	PASS	ENSG00000290825	DDX11L16	ENST00000832823.1	upstream_gene_variant	MODIFIER	NA	NA	0.4861	0.4861	NA	NA	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	regulatory	MODIFIER	pass	needs_external_annotation	common	missing	proximal	common	missing	high_confidence	noncoding_common_or_low_support	False	False	False	True	False

```

### Stage11 prioritized_variants.tsv

- path: `results/run_2026_05_30_151355/processed/stage_11_prioritized_variants.tsv`
- size_bytes: 462134655
- rows: 
- columns: 52
- header_sha256: `446c7603e23bb60bb4da68196782174abe5aea562307628ddf55513a5e4bae54`
- has_variant_id: yes
- distinct_variant_ids: 849399

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
    34	functional_impact
    35	rarity_flag
    36	clinical_evidence
    37	qc_reliability
    38	coding_interpretation_label
    39	is_lof_candidate
    40	is_rare_candidate
    41	is_clinically_supported
    42	is_high_quality
    43	is_potential_artifact
    44	variant_origin
    45	source_interpretation_label
    46	priority_tier
    47	priority_rank
    48	priority_reason
    49	is_high_priority_candidate
    50	is_moderate_priority_candidate
    51	is_low_priority_candidate
    52	is_uninterpretable
```

First data row preview:
```text
ERR10619208	run_2026_05_30_151355	variant_annotation_pipeline	1:924533:A:G	1	924533	A	G	snv	coding	PASS	ENSG00000187634	SAMD11	ENST00000616016.5	synonymous_variant	LOW	NA	NA	0.7498	0.7498	NA	0.4039	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	coding	LOW	pass	interpretable_now	common	missing	synonymous	common	missing	high_confidence	coding_common_or_low_support	False	False	False	True	False	coding	coding_common_or_low_support	tier_3_low_support_or_common	3	coding label coding_common

```

### Stage11 gene_variant_counts.tsv

- path: `results/run_2026_05_30_151355/processed/stage_11_gene_variant_counts.tsv`
- size_bytes: 839826
- rows: 
- columns: 2
- header_sha256: `a728a2468d9a3e433005a28bf32c7a8a5cce42466215a1338be8933e0d5ade04`
- has_variant_id: no
- distinct_variant_ids: NA

Header:
```text
     1	gene_id
     2	variant_count
```

First data row preview:
```text
NA	135092

```

### Stage12 validation_candidates.tsv

- path: `results/run_2026_05_30_151355/processed/stage_12_validation_candidates.tsv`
- size_bytes: 500642774
- rows: 
- columns: 56
- header_sha256: `d43ee98c7824c468f1e6523d1886bf0d1164aa6e1003677f73093d557ac2d385`
- has_variant_id: yes
- distinct_variant_ids: 849399

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
    34	functional_impact
    35	rarity_flag
    36	clinical_evidence
    37	qc_reliability
    38	coding_interpretation_label
    39	is_lof_candidate
    40	is_rare_candidate
    41	is_clinically_supported
    42	is_high_quality
    43	is_potential_artifact
    44	variant_origin
    45	source_interpretation_label
    46	priority_tier
    47	priority_rank
    48	priority_reason
    49	is_high_priority_candidate
    50	is_moderate_priority_candidate
    51	is_low_priority_candidate
    52	is_uninterpretable
    53	validation_required
    54	validation_priority
    55	suggested_validation_method
    56	validation_reason
```

First data row preview:
```text
ERR10619208	run_2026_05_30_151355	variant_annotation_pipeline	1:924533:A:G	1	924533	A	G	snv	coding	PASS	ENSG00000187634	SAMD11	ENST00000616016.5	synonymous_variant	LOW	NA	NA	0.7498	0.7498	NA	0.4039	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	coding	LOW	pass	interpretable_now	common	missing	synonymous	common	missing	high_confidence	coding_common_or_low_support	False	False	False	True	False	coding	coding_common_or_low_support	tier_3_low_support_or_common	3	coding label coding_common

```

# Transition Lineage

### Stage07 annotated → Stage08 selected

| Metric | Stage07 annotated | Stage08 selected |
|---|---:|---:|
| rows |  |  |
| columns | 25 | 33 |
| distinct_variant_ids | 849399 | 849399 |

Removed columns:
```text
epilepsy_flag,impact
```

Added columns:
```text
annotation_source,annotation_version,clinical_status,epilepsy_flag,frequency_status,gene_mapping_status,interpretability_status,qc_status,variant_context,variant_effect_severity
```

Shared columns:
```text
alternate_allele,chromosome,clinical_significance,clinvar_significance,consequence,exac_af,gene_id,gene_symbol,gnomad_af,impact_class,mito_flag,population_frequency,position,quality_flag,reference_allele,run_id,sample_id,source_pipeline,thousand_genomes_af,transcript_id,variant_class,variant_id,variant_type
```

### Stage08 selected → Stage08 VDB-ready

| Metric | Stage08 selected | Stage08 VDB-ready |
|---|---:|---:|
| rows |  |  |
| columns | 33 | 33 |
| distinct_variant_ids | 849399 | 849399 |

Removed columns:
```text
NONE
```

Added columns:
```text
NONE
```

Shared columns:
```text
alternate_allele,annotation_source,annotation_version,chromosome,clinical_significance,clinical_status,clinvar_significance,consequence,epilepsy_flag,exac_af,frequency_status,gene_id,gene_mapping_status,gene_symbol,gnomad_af,impact_class,interpretability_status,mito_flag,population_frequency,position,qc_status,quality_flag,reference_allele,run_id,sample_id,source_pipeline,thousand_genomes_af,transcript_id,variant_class,variant_context,variant_effect_severity,variant_id,variant_type
```

### Stage08 VDB-ready → Stage09 coding interpreted

| Metric | Stage08 VDB-ready | Stage09 coding interpreted |
|---|---:|---:|
| rows |  |  |
| columns | 33 | 43 |
| distinct_variant_ids | 849399 | 28041 |

Removed columns:
```text
clinical_status
```

Added columns:
```text
clinical_evidence,clinical_status,coding_interpretation_label,functional_impact,is_clinically_supported,is_high_quality,is_lof_candidate,is_potential_artifact,is_rare_candidate,qc_reliability,rarity_flag
```

Shared columns:
```text
alternate_allele,annotation_source,annotation_version,chromosome,clinical_significance,clinvar_significance,consequence,epilepsy_flag,exac_af,frequency_status,gene_id,gene_mapping_status,gene_symbol,gnomad_af,impact_class,interpretability_status,mito_flag,population_frequency,position,qc_status,quality_flag,reference_allele,run_id,sample_id,source_pipeline,thousand_genomes_af,transcript_id,variant_class,variant_context,variant_effect_severity,variant_id,variant_type
```

### Stage08 VDB-ready → Stage10 noncoding interpreted

| Metric | Stage08 VDB-ready | Stage10 noncoding interpreted |
|---|---:|---:|
| rows |  |  |
| columns | 33 | 43 |
| distinct_variant_ids | 849399 | 821358 |

Removed columns:
```text
clinical_status
```

Added columns:
```text
clinical_evidence,clinical_status,is_clinically_supported,is_high_quality,is_potential_artifact,is_rare_candidate,is_regulatory_candidate,noncoding_functional_context,noncoding_interpretation_label,qc_reliability,rarity_flag
```

Shared columns:
```text
alternate_allele,annotation_source,annotation_version,chromosome,clinical_significance,clinvar_significance,consequence,epilepsy_flag,exac_af,frequency_status,gene_id,gene_mapping_status,gene_symbol,gnomad_af,impact_class,interpretability_status,mito_flag,population_frequency,position,qc_status,quality_flag,reference_allele,run_id,sample_id,source_pipeline,thousand_genomes_af,transcript_id,variant_class,variant_context,variant_effect_severity,variant_id,variant_type
```

### Stage09 coding interpreted → Stage11 prioritized

| Metric | Stage09 coding interpreted | Stage11 prioritized |
|---|---:|---:|
| rows |  |  |
| columns | 43 | 52 |
| distinct_variant_ids | 28041 | 849399 |

Removed columns:
```text
is_potential_artifact
```

Added columns:
```text
is_high_priority_candidate,is_low_priority_candidate,is_moderate_priority_candidate,is_potential_artifact,is_uninterpretable,priority_rank,priority_reason,priority_tier,source_interpretation_label,variant_origin
```

Shared columns:
```text
alternate_allele,annotation_source,annotation_version,chromosome,clinical_evidence,clinical_significance,clinical_status,clinvar_significance,coding_interpretation_label,consequence,epilepsy_flag,exac_af,frequency_status,functional_impact,gene_id,gene_mapping_status,gene_symbol,gnomad_af,impact_class,interpretability_status,is_clinically_supported,is_high_quality,is_lof_candidate,is_rare_candidate,mito_flag,population_frequency,position,qc_reliability,qc_status,quality_flag,rarity_flag,reference_allele,run_id,sample_id,source_pipeline,thousand_genomes_af,transcript_id,variant_class,variant_context,variant_effect_severity,variant_id,variant_type
```

### Stage10 noncoding interpreted → Stage11 prioritized

| Metric | Stage10 noncoding interpreted | Stage11 prioritized |
|---|---:|---:|
| rows |  |  |
| columns | 43 | 52 |
| distinct_variant_ids | 821358 | 849399 |

Removed columns:
```text
is_potential_artifact,is_regulatory_candidate,noncoding_functional_context,noncoding_interpretation_label
```

Added columns:
```text
coding_interpretation_label,functional_impact,is_high_priority_candidate,is_lof_candidate,is_low_priority_candidate,is_moderate_priority_candidate,is_potential_artifact,is_uninterpretable,priority_rank,priority_reason,priority_tier,source_interpretation_label,variant_origin
```

Shared columns:
```text
alternate_allele,annotation_source,annotation_version,chromosome,clinical_evidence,clinical_significance,clinical_status,clinvar_significance,consequence,epilepsy_flag,exac_af,frequency_status,gene_id,gene_mapping_status,gene_symbol,gnomad_af,impact_class,interpretability_status,is_clinically_supported,is_high_quality,is_rare_candidate,mito_flag,population_frequency,position,qc_reliability,qc_status,quality_flag,rarity_flag,reference_allele,run_id,sample_id,source_pipeline,thousand_genomes_af,transcript_id,variant_class,variant_context,variant_effect_severity,variant_id,variant_type
```

### Stage11 prioritized → Stage12 validation candidates

| Metric | Stage11 prioritized | Stage12 validation candidates |
|---|---:|---:|
| rows |  |  |
| columns | 52 | 56 |
| distinct_variant_ids | 849399 | 849399 |

Removed columns:
```text
is_uninterpretable
```

Added columns:
```text
is_uninterpretable,suggested_validation_method,validation_priority,validation_reason,validation_required
```

Shared columns:
```text
alternate_allele,annotation_source,annotation_version,chromosome,clinical_evidence,clinical_significance,clinical_status,clinvar_significance,coding_interpretation_label,consequence,epilepsy_flag,exac_af,frequency_status,functional_impact,gene_id,gene_mapping_status,gene_symbol,gnomad_af,impact_class,interpretability_status,is_clinically_supported,is_high_priority_candidate,is_high_quality,is_lof_candidate,is_low_priority_candidate,is_moderate_priority_candidate,is_potential_artifact,is_rare_candidate,mito_flag,population_frequency,position,priority_rank,priority_reason,priority_tier,qc_reliability,qc_status,quality_flag,rarity_flag,reference_allele,run_id,sample_id,source_interpretation_label,source_pipeline,thousand_genomes_af,transcript_id,variant_class,variant_context,variant_effect_severity,variant_id,variant_origin,variant_type
```

---

## ERR10619212 / run_2026_05_30_214724 / q1

# Artifact Inventory

### Stage07 annotated_variants.tsv

- path: `results/run_2026_05_30_214724/processed/ERR10619212_run_2026_05_30_214724.annotated_variants.tsv`
- size_bytes: 212353031
- rows: 
- columns: 25
- header_sha256: `617480c310358e0f764d2996153e3428ee6270702ce98194140c6e7ba6074d9f`
- has_variant_id: yes
- distinct_variant_ids: 905517

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	quality_flag
    10	gene_id
    11	gene_symbol
    12	transcript_id
    13	consequence
    14	impact_class
    15	impact
    16	variant_class
    17	variant_type
    18	clinical_significance
    19	clinvar_significance
    20	population_frequency
    21	gnomad_af
    22	exac_af
    23	thousand_genomes_af
    24	mito_flag
    25	epilepsy_flag
```

First data row preview:
```text
ERR10619212	run_2026_05_30_214724	variant_annotation_pipeline	1:13649:G:C	1	13649	G	C	PASS	ENSG00000223972	DDX11L1	ENST00000450305.2	non_coding_transcript_exon_variant	MODIFIER	MODIFIER	SNV	non-coding	NA	NA	0.2367	0.2367	NA	NA	False	False

```

### Stage08 selected_transcript_consequences.tsv

- path: `results/run_2026_05_30_214724/processed/stage_08_selected_transcript_consequences.tsv`
- size_bytes: 305461910
- rows: 
- columns: 33
- header_sha256: `cd5a915c5bc9d15f76cda12616b5dae1e039ecb5f00164e46acc177e2d42a402`
- has_variant_id: yes
- distinct_variant_ids: 905517

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
```

First data row preview:
```text
ERR10619212	run_2026_05_30_214724	variant_annotation_pipeline	1:13649:G:C	1	13649	G	C	snv	noncoding	PASS	ENSG00000223972	DDX11L1	ENST00000450305.2	non_coding_transcript_exon_variant	MODIFIER	NA	NA	0.2367	0.2367	NA	NA	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	noncoding_transcript	MODIFIER	pass	needs_external_annotation	common	missing

```

### Stage08 vdb_ready_variants.tsv

- path: `results/run_2026_05_30_214724/processed/stage_08_vdb_ready_variants.tsv`
- size_bytes: 305461910
- rows: 
- columns: 33
- header_sha256: `cd5a915c5bc9d15f76cda12616b5dae1e039ecb5f00164e46acc177e2d42a402`
- has_variant_id: yes
- distinct_variant_ids: 905517

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
```

First data row preview:
```text
ERR10619212	run_2026_05_30_214724	variant_annotation_pipeline	1:13649:G:C	1	13649	G	C	snv	noncoding	PASS	ENSG00000223972	DDX11L1	ENST00000450305.2	non_coding_transcript_exon_variant	MODIFIER	NA	NA	0.2367	0.2367	NA	NA	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	noncoding_transcript	MODIFIER	pass	needs_external_annotation	common	missing

```

### Stage08 coding_candidates.tsv

- path: `results/run_2026_05_30_214724/processed/coding_candidates.tsv`
- size_bytes: 7903722
- rows: 
- columns: 33
- header_sha256: `cd5a915c5bc9d15f76cda12616b5dae1e039ecb5f00164e46acc177e2d42a402`
- has_variant_id: yes
- distinct_variant_ids: 24592

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
```

First data row preview:
```text
ERR10619212	run_2026_05_30_214724	variant_annotation_pipeline	1:924533:A:G	1	924533	A	G	snv	coding	PASS	ENSG00000187634	SAMD11	ENST00000616016.5	synonymous_variant	LOW	NA	NA	0.7498	0.7498	NA	0.4039	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	coding	LOW	pass	interpretable_now	common	missing

```

### Stage08 splice_region_candidates.tsv

- path: `results/run_2026_05_30_214724/processed/splice_region_candidates.tsv`
- size_bytes: 1145969
- rows: 
- columns: 33
- header_sha256: `cd5a915c5bc9d15f76cda12616b5dae1e039ecb5f00164e46acc177e2d42a402`
- has_variant_id: yes
- distinct_variant_ids: 3098

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
```

First data row preview:
```text
ERR10619212	run_2026_05_30_214724	variant_annotation_pipeline	1:17746:A:G	1	17746	A	G	snv	coding	PASS	ENSG00000310526	WASH7P	ENST00000831140.1	splice_region_variant&splice_polypyrimidine_tract_variant&intron_variant&non_coding_transcript_variant	LOW	NA	NA	0.1499	0.1499	NA	NA	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	missing

```

### Stage08 noncoding_candidates.tsv

- path: `results/run_2026_05_30_214724/processed/noncoding_candidates.tsv`
- size_bytes: 296602907
- rows: 
- columns: 33
- header_sha256: `cd5a915c5bc9d15f76cda12616b5dae1e039ecb5f00164e46acc177e2d42a402`
- has_variant_id: yes
- distinct_variant_ids: 878368

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
```

First data row preview:
```text
ERR10619212	run_2026_05_30_214724	variant_annotation_pipeline	1:13649:G:C	1	13649	G	C	snv	noncoding	PASS	ENSG00000223972	DDX11L1	ENST00000450305.2	non_coding_transcript_exon_variant	MODIFIER	NA	NA	0.2367	0.2367	NA	NA	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	noncoding_transcript	MODIFIER	pass	needs_external_annotation	common	missing

```

### Stage08 variant_summary.tsv

- path: `results/run_2026_05_30_214724/processed/stage_08_variant_summary.tsv`
- size_bytes: 229970519
- rows: 
- columns: 26
- header_sha256: `a0088e61e1ce409de45d1365b177ff47234ecb57dacab3ef0cb50fe3f613b55a`
- has_variant_id: yes
- distinct_variant_ids: 905517

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	gene_symbols
    10	gene_mapping_status
    11	worst_consequence
    12	highest_impact
    13	canonical_present
    14	coding_flag
    15	splice_flag
    16	noncoding_flag
    17	transcript_count
    18	variant_type
    19	variant_class
    20	quality_flag
    21	qc_status
    22	population_frequency
    23	frequency_status
    24	clinical_status
    25	annotation_source
    26	annotation_version
```

First data row preview:
```text
ERR10619212	run_2026_05_30_214724	variant_annotation_pipeline	10:10000862:T:C	10	10000862	T	C	NA	mapped	intron_variant&non_coding_transcript_variant	MODIFIER	False	False	False	True	1	snv	noncoding	PASS	pass	0.8313	common	missing	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #

```

### Stage08 rdgp_gene_evidence_seed.tsv

- path: `results/run_2026_05_30_214724/processed/stage_08_rdgp_gene_evidence_seed.tsv`
- size_bytes: 14956384
- rows: 
- columns: 10
- header_sha256: `18d500222bcf3f2b99e044e14b9a1f0647d3f9bf1593555fa16359bb3996d3a3`
- has_variant_id: no
- distinct_variant_ids: NA

Header:
```text
     1	sample_id
     2	gene_id
     3	gene_symbol
     4	variant_count
     5	high_impact_variant_count
     6	rare_variant_count
     7	pathogenic_variant_count
     8	max_variant_severity
     9	has_low_quality_evidence
    10	contributing_variant_ids
```

First data row preview:
```text
ERR10619212	ENSG00000000003	TSPAN6	4	0	0	0	MODIFIER	False	X:100624362:T:C,X:100632405:CA:C,X:100634498:CTT:C,X:100638147:T:C

```

### Stage09 coding_interpreted.tsv

- path: `results/run_2026_05_30_214724/processed/stage_09_coding_interpreted.tsv`
- size_bytes: 11558524
- rows: 
- columns: 43
- header_sha256: `8132a0aab15233fd27576c5624b2e8393fe622aa2bd651c8bdfc94c6215d5d3b`
- has_variant_id: yes
- distinct_variant_ids: 27149

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
    34	functional_impact
    35	rarity_flag
    36	clinical_evidence
    37	qc_reliability
    38	coding_interpretation_label
    39	is_lof_candidate
    40	is_rare_candidate
    41	is_clinically_supported
    42	is_high_quality
    43	is_potential_artifact
```

First data row preview:
```text
ERR10619212	run_2026_05_30_214724	variant_annotation_pipeline	1:924533:A:G	1	924533	A	G	snv	coding	PASS	ENSG00000187634	SAMD11	ENST00000616016.5	synonymous_variant	LOW	NA	NA	0.7498	0.7498	NA	0.4039	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	coding	LOW	pass	interpretable_now	common	missing	synonymous	common	missing	high_confidence	coding_common_or_low_support	False	False	False	True	False

```

### Stage10 noncoding_interpreted.tsv

- path: `results/run_2026_05_30_214724/processed/stage_10_noncoding_interpreted.tsv`
- size_bytes: 387136438
- rows: 
- columns: 43
- header_sha256: `52d4bd70320ef627d745025507d0b4bd3197d1fef0d1436811b20a6c4486c87e`
- has_variant_id: yes
- distinct_variant_ids: 878368

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
    34	noncoding_functional_context
    35	rarity_flag
    36	clinical_evidence
    37	qc_reliability
    38	noncoding_interpretation_label
    39	is_regulatory_candidate
    40	is_rare_candidate
    41	is_clinically_supported
    42	is_high_quality
    43	is_potential_artifact
```

First data row preview:
```text
ERR10619212	run_2026_05_30_214724	variant_annotation_pipeline	1:13649:G:C	1	13649	G	C	snv	noncoding	PASS	ENSG00000223972	DDX11L1	ENST00000450305.2	non_coding_transcript_exon_variant	MODIFIER	NA	NA	0.2367	0.2367	NA	NA	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	noncoding_transcript	MODIFIER	pass	needs_external_annotation	common	missing	transcript_associated	common	missing	high_confidence	noncoding_common_or_low_support	False	False	False	True	False

```

### Stage11 prioritized_variants.tsv

- path: `results/run_2026_05_30_214724/processed/stage_11_prioritized_variants.tsv`
- size_bytes: 492710834
- rows: 
- columns: 52
- header_sha256: `446c7603e23bb60bb4da68196782174abe5aea562307628ddf55513a5e4bae54`
- has_variant_id: yes
- distinct_variant_ids: 905517

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
    34	functional_impact
    35	rarity_flag
    36	clinical_evidence
    37	qc_reliability
    38	coding_interpretation_label
    39	is_lof_candidate
    40	is_rare_candidate
    41	is_clinically_supported
    42	is_high_quality
    43	is_potential_artifact
    44	variant_origin
    45	source_interpretation_label
    46	priority_tier
    47	priority_rank
    48	priority_reason
    49	is_high_priority_candidate
    50	is_moderate_priority_candidate
    51	is_low_priority_candidate
    52	is_uninterpretable
```

First data row preview:
```text
ERR10619212	run_2026_05_30_214724	variant_annotation_pipeline	1:924533:A:G	1	924533	A	G	snv	coding	PASS	ENSG00000187634	SAMD11	ENST00000616016.5	synonymous_variant	LOW	NA	NA	0.7498	0.7498	NA	0.4039	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	coding	LOW	pass	interpretable_now	common	missing	synonymous	common	missing	high_confidence	coding_common_or_low_support	False	False	False	True	False	coding	coding_common_or_low_support	tier_3_low_support_or_common	3	coding label coding_common

```

### Stage11 gene_variant_counts.tsv

- path: `results/run_2026_05_30_214724/processed/stage_11_gene_variant_counts.tsv`
- size_bytes: 843414
- rows: 
- columns: 2
- header_sha256: `a728a2468d9a3e433005a28bf32c7a8a5cce42466215a1338be8933e0d5ade04`
- has_variant_id: no
- distinct_variant_ids: NA

Header:
```text
     1	gene_id
     2	variant_count
```

First data row preview:
```text
NA	141962

```

### Stage12 validation_candidates.tsv

- path: `results/run_2026_05_30_214724/processed/stage_12_validation_candidates.tsv`
- size_bytes: 533746545
- rows: 
- columns: 56
- header_sha256: `d43ee98c7824c468f1e6523d1886bf0d1164aa6e1003677f73093d557ac2d385`
- has_variant_id: yes
- distinct_variant_ids: 905517

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
    34	functional_impact
    35	rarity_flag
    36	clinical_evidence
    37	qc_reliability
    38	coding_interpretation_label
    39	is_lof_candidate
    40	is_rare_candidate
    41	is_clinically_supported
    42	is_high_quality
    43	is_potential_artifact
    44	variant_origin
    45	source_interpretation_label
    46	priority_tier
    47	priority_rank
    48	priority_reason
    49	is_high_priority_candidate
    50	is_moderate_priority_candidate
    51	is_low_priority_candidate
    52	is_uninterpretable
    53	validation_required
    54	validation_priority
    55	suggested_validation_method
    56	validation_reason
```

First data row preview:
```text
ERR10619212	run_2026_05_30_214724	variant_annotation_pipeline	1:924533:A:G	1	924533	A	G	snv	coding	PASS	ENSG00000187634	SAMD11	ENST00000616016.5	synonymous_variant	LOW	NA	NA	0.7498	0.7498	NA	0.4039	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	coding	LOW	pass	interpretable_now	common	missing	synonymous	common	missing	high_confidence	coding_common_or_low_support	False	False	False	True	False	coding	coding_common_or_low_support	tier_3_low_support_or_common	3	coding label coding_common

```

# Transition Lineage

### Stage07 annotated → Stage08 selected

| Metric | Stage07 annotated | Stage08 selected |
|---|---:|---:|
| rows |  |  |
| columns | 25 | 33 |
| distinct_variant_ids | 905517 | 905517 |

Removed columns:
```text
epilepsy_flag,impact
```

Added columns:
```text
annotation_source,annotation_version,clinical_status,epilepsy_flag,frequency_status,gene_mapping_status,interpretability_status,qc_status,variant_context,variant_effect_severity
```

Shared columns:
```text
alternate_allele,chromosome,clinical_significance,clinvar_significance,consequence,exac_af,gene_id,gene_symbol,gnomad_af,impact_class,mito_flag,population_frequency,position,quality_flag,reference_allele,run_id,sample_id,source_pipeline,thousand_genomes_af,transcript_id,variant_class,variant_id,variant_type
```

### Stage08 selected → Stage08 VDB-ready

| Metric | Stage08 selected | Stage08 VDB-ready |
|---|---:|---:|
| rows |  |  |
| columns | 33 | 33 |
| distinct_variant_ids | 905517 | 905517 |

Removed columns:
```text
NONE
```

Added columns:
```text
NONE
```

Shared columns:
```text
alternate_allele,annotation_source,annotation_version,chromosome,clinical_significance,clinical_status,clinvar_significance,consequence,epilepsy_flag,exac_af,frequency_status,gene_id,gene_mapping_status,gene_symbol,gnomad_af,impact_class,interpretability_status,mito_flag,population_frequency,position,qc_status,quality_flag,reference_allele,run_id,sample_id,source_pipeline,thousand_genomes_af,transcript_id,variant_class,variant_context,variant_effect_severity,variant_id,variant_type
```

### Stage08 VDB-ready → Stage09 coding interpreted

| Metric | Stage08 VDB-ready | Stage09 coding interpreted |
|---|---:|---:|
| rows |  |  |
| columns | 33 | 43 |
| distinct_variant_ids | 905517 | 27149 |

Removed columns:
```text
clinical_status
```

Added columns:
```text
clinical_evidence,clinical_status,coding_interpretation_label,functional_impact,is_clinically_supported,is_high_quality,is_lof_candidate,is_potential_artifact,is_rare_candidate,qc_reliability,rarity_flag
```

Shared columns:
```text
alternate_allele,annotation_source,annotation_version,chromosome,clinical_significance,clinvar_significance,consequence,epilepsy_flag,exac_af,frequency_status,gene_id,gene_mapping_status,gene_symbol,gnomad_af,impact_class,interpretability_status,mito_flag,population_frequency,position,qc_status,quality_flag,reference_allele,run_id,sample_id,source_pipeline,thousand_genomes_af,transcript_id,variant_class,variant_context,variant_effect_severity,variant_id,variant_type
```

### Stage08 VDB-ready → Stage10 noncoding interpreted

| Metric | Stage08 VDB-ready | Stage10 noncoding interpreted |
|---|---:|---:|
| rows |  |  |
| columns | 33 | 43 |
| distinct_variant_ids | 905517 | 878368 |

Removed columns:
```text
clinical_status
```

Added columns:
```text
clinical_evidence,clinical_status,is_clinically_supported,is_high_quality,is_potential_artifact,is_rare_candidate,is_regulatory_candidate,noncoding_functional_context,noncoding_interpretation_label,qc_reliability,rarity_flag
```

Shared columns:
```text
alternate_allele,annotation_source,annotation_version,chromosome,clinical_significance,clinvar_significance,consequence,epilepsy_flag,exac_af,frequency_status,gene_id,gene_mapping_status,gene_symbol,gnomad_af,impact_class,interpretability_status,mito_flag,population_frequency,position,qc_status,quality_flag,reference_allele,run_id,sample_id,source_pipeline,thousand_genomes_af,transcript_id,variant_class,variant_context,variant_effect_severity,variant_id,variant_type
```

### Stage09 coding interpreted → Stage11 prioritized

| Metric | Stage09 coding interpreted | Stage11 prioritized |
|---|---:|---:|
| rows |  |  |
| columns | 43 | 52 |
| distinct_variant_ids | 27149 | 905517 |

Removed columns:
```text
is_potential_artifact
```

Added columns:
```text
is_high_priority_candidate,is_low_priority_candidate,is_moderate_priority_candidate,is_potential_artifact,is_uninterpretable,priority_rank,priority_reason,priority_tier,source_interpretation_label,variant_origin
```

Shared columns:
```text
alternate_allele,annotation_source,annotation_version,chromosome,clinical_evidence,clinical_significance,clinical_status,clinvar_significance,coding_interpretation_label,consequence,epilepsy_flag,exac_af,frequency_status,functional_impact,gene_id,gene_mapping_status,gene_symbol,gnomad_af,impact_class,interpretability_status,is_clinically_supported,is_high_quality,is_lof_candidate,is_rare_candidate,mito_flag,population_frequency,position,qc_reliability,qc_status,quality_flag,rarity_flag,reference_allele,run_id,sample_id,source_pipeline,thousand_genomes_af,transcript_id,variant_class,variant_context,variant_effect_severity,variant_id,variant_type
```

### Stage10 noncoding interpreted → Stage11 prioritized

| Metric | Stage10 noncoding interpreted | Stage11 prioritized |
|---|---:|---:|
| rows |  |  |
| columns | 43 | 52 |
| distinct_variant_ids | 878368 | 905517 |

Removed columns:
```text
is_potential_artifact,is_regulatory_candidate,noncoding_functional_context,noncoding_interpretation_label
```

Added columns:
```text
coding_interpretation_label,functional_impact,is_high_priority_candidate,is_lof_candidate,is_low_priority_candidate,is_moderate_priority_candidate,is_potential_artifact,is_uninterpretable,priority_rank,priority_reason,priority_tier,source_interpretation_label,variant_origin
```

Shared columns:
```text
alternate_allele,annotation_source,annotation_version,chromosome,clinical_evidence,clinical_significance,clinical_status,clinvar_significance,consequence,epilepsy_flag,exac_af,frequency_status,gene_id,gene_mapping_status,gene_symbol,gnomad_af,impact_class,interpretability_status,is_clinically_supported,is_high_quality,is_rare_candidate,mito_flag,population_frequency,position,qc_reliability,qc_status,quality_flag,rarity_flag,reference_allele,run_id,sample_id,source_pipeline,thousand_genomes_af,transcript_id,variant_class,variant_context,variant_effect_severity,variant_id,variant_type
```

### Stage11 prioritized → Stage12 validation candidates

| Metric | Stage11 prioritized | Stage12 validation candidates |
|---|---:|---:|
| rows |  |  |
| columns | 52 | 56 |
| distinct_variant_ids | 905517 | 905517 |

Removed columns:
```text
is_uninterpretable
```

Added columns:
```text
is_uninterpretable,suggested_validation_method,validation_priority,validation_reason,validation_required
```

Shared columns:
```text
alternate_allele,annotation_source,annotation_version,chromosome,clinical_evidence,clinical_significance,clinical_status,clinvar_significance,coding_interpretation_label,consequence,epilepsy_flag,exac_af,frequency_status,functional_impact,gene_id,gene_mapping_status,gene_symbol,gnomad_af,impact_class,interpretability_status,is_clinically_supported,is_high_priority_candidate,is_high_quality,is_lof_candidate,is_low_priority_candidate,is_moderate_priority_candidate,is_potential_artifact,is_rare_candidate,mito_flag,population_frequency,position,priority_rank,priority_reason,priority_tier,qc_reliability,qc_status,quality_flag,rarity_flag,reference_allele,run_id,sample_id,source_interpretation_label,source_pipeline,thousand_genomes_af,transcript_id,variant_class,variant_context,variant_effect_severity,variant_id,variant_origin,variant_type
```

---

## ERR10619225 / run_2026_05_31_091242 / q3

# Artifact Inventory

### Stage07 annotated_variants.tsv

- path: `results/run_2026_05_31_091242/processed/ERR10619225_run_2026_05_31_091242.annotated_variants.tsv`
- size_bytes: 177765811
- rows: 
- columns: 25
- header_sha256: `617480c310358e0f764d2996153e3428ee6270702ce98194140c6e7ba6074d9f`
- has_variant_id: yes
- distinct_variant_ids: 757635

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	quality_flag
    10	gene_id
    11	gene_symbol
    12	transcript_id
    13	consequence
    14	impact_class
    15	impact
    16	variant_class
    17	variant_type
    18	clinical_significance
    19	clinvar_significance
    20	population_frequency
    21	gnomad_af
    22	exac_af
    23	thousand_genomes_af
    24	mito_flag
    25	epilepsy_flag
```

First data row preview:
```text
ERR10619225	run_2026_05_31_091242	variant_annotation_pipeline	1:10439:AC:A	1	10439	AC	A	PASS	ENSG00000223972	DDX11L1	ENST00000450305.2	upstream_gene_variant	MODIFIER	MODIFIER	deletion	non-coding	NA	NA	0.4031	0.4031	NA	NA	False	False

```

### Stage08 selected_transcript_consequences.tsv

- path: `results/run_2026_05_31_091242/processed/stage_08_selected_transcript_consequences.tsv`
- size_bytes: 255624040
- rows: 
- columns: 33
- header_sha256: `cd5a915c5bc9d15f76cda12616b5dae1e039ecb5f00164e46acc177e2d42a402`
- has_variant_id: yes
- distinct_variant_ids: 757635

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
```

First data row preview:
```text
ERR10619225	run_2026_05_31_091242	variant_annotation_pipeline	1:10439:AC:A	1	10439	AC	A	deletion	noncoding	PASS	ENSG00000223972	DDX11L1	ENST00000450305.2	upstream_gene_variant	MODIFIER	NA	NA	0.4031	0.4031	NA	NA	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	regulatory	MODIFIER	pass	needs_external_annotation	common	missing

```

### Stage08 vdb_ready_variants.tsv

- path: `results/run_2026_05_31_091242/processed/stage_08_vdb_ready_variants.tsv`
- size_bytes: 255624040
- rows: 
- columns: 33
- header_sha256: `cd5a915c5bc9d15f76cda12616b5dae1e039ecb5f00164e46acc177e2d42a402`
- has_variant_id: yes
- distinct_variant_ids: 757635

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
```

First data row preview:
```text
ERR10619225	run_2026_05_31_091242	variant_annotation_pipeline	1:10439:AC:A	1	10439	AC	A	deletion	noncoding	PASS	ENSG00000223972	DDX11L1	ENST00000450305.2	upstream_gene_variant	MODIFIER	NA	NA	0.4031	0.4031	NA	NA	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	regulatory	MODIFIER	pass	needs_external_annotation	common	missing

```

### Stage08 coding_candidates.tsv

- path: `results/run_2026_05_31_091242/processed/coding_candidates.tsv`
- size_bytes: 8141452
- rows: 
- columns: 33
- header_sha256: `cd5a915c5bc9d15f76cda12616b5dae1e039ecb5f00164e46acc177e2d42a402`
- has_variant_id: yes
- distinct_variant_ids: 25332

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
```

First data row preview:
```text
ERR10619225	run_2026_05_31_091242	variant_annotation_pipeline	1:924533:A:G	1	924533	A	G	snv	coding	PASS	ENSG00000187634	SAMD11	ENST00000616016.5	synonymous_variant	LOW	NA	NA	0.7498	0.7498	NA	0.4039	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	coding	LOW	pass	interpretable_now	common	missing

```

### Stage08 splice_region_candidates.tsv

- path: `results/run_2026_05_31_091242/processed/splice_region_candidates.tsv`
- size_bytes: 1117805
- rows: 
- columns: 33
- header_sha256: `cd5a915c5bc9d15f76cda12616b5dae1e039ecb5f00164e46acc177e2d42a402`
- has_variant_id: yes
- distinct_variant_ids: 3029

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
```

First data row preview:
```text
ERR10619225	run_2026_05_31_091242	variant_annotation_pipeline	1:15045:C:T	1	15045	C	T	snv	coding	PASS	ENSG00000310526	WASH7P	ENST00000831140.1	splice_region_variant&splice_polypyrimidine_tract_variant&intron_variant&non_coding_transcript_variant	LOW	NA	NA	0.4369	0.4369	NA	NA	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	missing

```

### Stage08 noncoding_candidates.tsv

- path: `results/run_2026_05_31_091242/processed/noncoding_candidates.tsv`
- size_bytes: 246554978
- rows: 
- columns: 33
- header_sha256: `cd5a915c5bc9d15f76cda12616b5dae1e039ecb5f00164e46acc177e2d42a402`
- has_variant_id: yes
- distinct_variant_ids: 729815

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
```

First data row preview:
```text
ERR10619225	run_2026_05_31_091242	variant_annotation_pipeline	1:10439:AC:A	1	10439	AC	A	deletion	noncoding	PASS	ENSG00000223972	DDX11L1	ENST00000450305.2	upstream_gene_variant	MODIFIER	NA	NA	0.4031	0.4031	NA	NA	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	regulatory	MODIFIER	pass	needs_external_annotation	common	missing

```

### Stage08 variant_summary.tsv

- path: `results/run_2026_05_31_091242/processed/stage_08_variant_summary.tsv`
- size_bytes: 192342581
- rows: 
- columns: 26
- header_sha256: `a0088e61e1ce409de45d1365b177ff47234ecb57dacab3ef0cb50fe3f613b55a`
- has_variant_id: yes
- distinct_variant_ids: 757635

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	gene_symbols
    10	gene_mapping_status
    11	worst_consequence
    12	highest_impact
    13	canonical_present
    14	coding_flag
    15	splice_flag
    16	noncoding_flag
    17	transcript_count
    18	variant_type
    19	variant_class
    20	quality_flag
    21	qc_status
    22	population_frequency
    23	frequency_status
    24	clinical_status
    25	annotation_source
    26	annotation_version
```

First data row preview:
```text
ERR10619225	run_2026_05_31_091242	variant_annotation_pipeline	10:100007115:CA:C	10	100007115	CA	C	DNMBP	mapped	intron_variant	MODIFIER	False	False	False	True	1	deletion	noncoding	PASS	pass	0.003219	rare	missing	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #

```

### Stage08 rdgp_gene_evidence_seed.tsv

- path: `results/run_2026_05_31_091242/processed/stage_08_rdgp_gene_evidence_seed.tsv`
- size_bytes: 12932893
- rows: 
- columns: 10
- header_sha256: `18d500222bcf3f2b99e044e14b9a1f0647d3f9bf1593555fa16359bb3996d3a3`
- has_variant_id: no
- distinct_variant_ids: NA

Header:
```text
     1	sample_id
     2	gene_id
     3	gene_symbol
     4	variant_count
     5	high_impact_variant_count
     6	rare_variant_count
     7	pathogenic_variant_count
     8	max_variant_severity
     9	has_low_quality_evidence
    10	contributing_variant_ids
```

First data row preview:
```text
ERR10619225	ENSG00000000003	TSPAN6	1	0	0	0	MODIFIER	False	X:100632405:CA:C

```

### Stage09 coding_interpreted.tsv

- path: `results/run_2026_05_31_091242/processed/stage_09_coding_interpreted.tsv`
- size_bytes: 11835473
- rows: 
- columns: 43
- header_sha256: `8132a0aab15233fd27576c5624b2e8393fe622aa2bd651c8bdfc94c6215d5d3b`
- has_variant_id: yes
- distinct_variant_ids: 27820

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
    34	functional_impact
    35	rarity_flag
    36	clinical_evidence
    37	qc_reliability
    38	coding_interpretation_label
    39	is_lof_candidate
    40	is_rare_candidate
    41	is_clinically_supported
    42	is_high_quality
    43	is_potential_artifact
```

First data row preview:
```text
ERR10619225	run_2026_05_31_091242	variant_annotation_pipeline	1:924533:A:G	1	924533	A	G	snv	coding	PASS	ENSG00000187634	SAMD11	ENST00000616016.5	synonymous_variant	LOW	NA	NA	0.7498	0.7498	NA	0.4039	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	coding	LOW	pass	interpretable_now	common	missing	synonymous	common	missing	high_confidence	coding_common_or_low_support	False	False	False	True	False

```

### Stage10 noncoding_interpreted.tsv

- path: `results/run_2026_05_31_091242/processed/stage_10_noncoding_interpreted.tsv`
- size_bytes: 321763832
- rows: 
- columns: 43
- header_sha256: `52d4bd70320ef627d745025507d0b4bd3197d1fef0d1436811b20a6c4486c87e`
- has_variant_id: yes
- distinct_variant_ids: 729815

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
    34	noncoding_functional_context
    35	rarity_flag
    36	clinical_evidence
    37	qc_reliability
    38	noncoding_interpretation_label
    39	is_regulatory_candidate
    40	is_rare_candidate
    41	is_clinically_supported
    42	is_high_quality
    43	is_potential_artifact
```

First data row preview:
```text
ERR10619225	run_2026_05_31_091242	variant_annotation_pipeline	1:10439:AC:A	1	10439	AC	A	deletion	noncoding	PASS	ENSG00000223972	DDX11L1	ENST00000450305.2	upstream_gene_variant	MODIFIER	NA	NA	0.4031	0.4031	NA	NA	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	regulatory	MODIFIER	pass	needs_external_annotation	common	missing	proximal	common	missing	high_confidence	noncoding_common_or_low_support	False	False	False	True	False

```

### Stage11 prioritized_variants.tsv

- path: `results/run_2026_05_31_091242/processed/stage_11_prioritized_variants.tsv`
- size_bytes: 412438718
- rows: 
- columns: 52
- header_sha256: `446c7603e23bb60bb4da68196782174abe5aea562307628ddf55513a5e4bae54`
- has_variant_id: yes
- distinct_variant_ids: 757635

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
    34	functional_impact
    35	rarity_flag
    36	clinical_evidence
    37	qc_reliability
    38	coding_interpretation_label
    39	is_lof_candidate
    40	is_rare_candidate
    41	is_clinically_supported
    42	is_high_quality
    43	is_potential_artifact
    44	variant_origin
    45	source_interpretation_label
    46	priority_tier
    47	priority_rank
    48	priority_reason
    49	is_high_priority_candidate
    50	is_moderate_priority_candidate
    51	is_low_priority_candidate
    52	is_uninterpretable
```

First data row preview:
```text
ERR10619225	run_2026_05_31_091242	variant_annotation_pipeline	1:924533:A:G	1	924533	A	G	snv	coding	PASS	ENSG00000187634	SAMD11	ENST00000616016.5	synonymous_variant	LOW	NA	NA	0.7498	0.7498	NA	0.4039	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	coding	LOW	pass	interpretable_now	common	missing	synonymous	common	missing	high_confidence	coding_common_or_low_support	False	False	False	True	False	coding	coding_common_or_low_support	tier_3_low_support_or_common	3	coding label coding_common

```

### Stage11 gene_variant_counts.tsv

- path: `results/run_2026_05_31_091242/processed/stage_11_gene_variant_counts.tsv`
- size_bytes: 819833
- rows: 
- columns: 2
- header_sha256: `a728a2468d9a3e433005a28bf32c7a8a5cce42466215a1338be8933e0d5ade04`
- has_variant_id: no
- distinct_variant_ids: NA

Header:
```text
     1	gene_id
     2	variant_count
```

First data row preview:
```text
NA	114529

```

### Stage12 validation_candidates.tsv

- path: `results/run_2026_05_31_091242/processed/stage_12_validation_candidates.tsv`
- size_bytes: 446742832
- rows: 
- columns: 56
- header_sha256: `d43ee98c7824c468f1e6523d1886bf0d1164aa6e1003677f73093d557ac2d385`
- has_variant_id: yes
- distinct_variant_ids: 757635

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
    34	functional_impact
    35	rarity_flag
    36	clinical_evidence
    37	qc_reliability
    38	coding_interpretation_label
    39	is_lof_candidate
    40	is_rare_candidate
    41	is_clinically_supported
    42	is_high_quality
    43	is_potential_artifact
    44	variant_origin
    45	source_interpretation_label
    46	priority_tier
    47	priority_rank
    48	priority_reason
    49	is_high_priority_candidate
    50	is_moderate_priority_candidate
    51	is_low_priority_candidate
    52	is_uninterpretable
    53	validation_required
    54	validation_priority
    55	suggested_validation_method
    56	validation_reason
```

First data row preview:
```text
ERR10619225	run_2026_05_31_091242	variant_annotation_pipeline	1:924533:A:G	1	924533	A	G	snv	coding	PASS	ENSG00000187634	SAMD11	ENST00000616016.5	synonymous_variant	LOW	NA	NA	0.7498	0.7498	NA	0.4039	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	coding	LOW	pass	interpretable_now	common	missing	synonymous	common	missing	high_confidence	coding_common_or_low_support	False	False	False	True	False	coding	coding_common_or_low_support	tier_3_low_support_or_common	3	coding label coding_common

```

# Transition Lineage

### Stage07 annotated → Stage08 selected

| Metric | Stage07 annotated | Stage08 selected |
|---|---:|---:|
| rows |  |  |
| columns | 25 | 33 |
| distinct_variant_ids | 757635 | 757635 |

Removed columns:
```text
epilepsy_flag,impact
```

Added columns:
```text
annotation_source,annotation_version,clinical_status,epilepsy_flag,frequency_status,gene_mapping_status,interpretability_status,qc_status,variant_context,variant_effect_severity
```

Shared columns:
```text
alternate_allele,chromosome,clinical_significance,clinvar_significance,consequence,exac_af,gene_id,gene_symbol,gnomad_af,impact_class,mito_flag,population_frequency,position,quality_flag,reference_allele,run_id,sample_id,source_pipeline,thousand_genomes_af,transcript_id,variant_class,variant_id,variant_type
```

### Stage08 selected → Stage08 VDB-ready

| Metric | Stage08 selected | Stage08 VDB-ready |
|---|---:|---:|
| rows |  |  |
| columns | 33 | 33 |
| distinct_variant_ids | 757635 | 757635 |

Removed columns:
```text
NONE
```

Added columns:
```text
NONE
```

Shared columns:
```text
alternate_allele,annotation_source,annotation_version,chromosome,clinical_significance,clinical_status,clinvar_significance,consequence,epilepsy_flag,exac_af,frequency_status,gene_id,gene_mapping_status,gene_symbol,gnomad_af,impact_class,interpretability_status,mito_flag,population_frequency,position,qc_status,quality_flag,reference_allele,run_id,sample_id,source_pipeline,thousand_genomes_af,transcript_id,variant_class,variant_context,variant_effect_severity,variant_id,variant_type
```

### Stage08 VDB-ready → Stage09 coding interpreted

| Metric | Stage08 VDB-ready | Stage09 coding interpreted |
|---|---:|---:|
| rows |  |  |
| columns | 33 | 43 |
| distinct_variant_ids | 757635 | 27820 |

Removed columns:
```text
clinical_status
```

Added columns:
```text
clinical_evidence,clinical_status,coding_interpretation_label,functional_impact,is_clinically_supported,is_high_quality,is_lof_candidate,is_potential_artifact,is_rare_candidate,qc_reliability,rarity_flag
```

Shared columns:
```text
alternate_allele,annotation_source,annotation_version,chromosome,clinical_significance,clinvar_significance,consequence,epilepsy_flag,exac_af,frequency_status,gene_id,gene_mapping_status,gene_symbol,gnomad_af,impact_class,interpretability_status,mito_flag,population_frequency,position,qc_status,quality_flag,reference_allele,run_id,sample_id,source_pipeline,thousand_genomes_af,transcript_id,variant_class,variant_context,variant_effect_severity,variant_id,variant_type
```

### Stage08 VDB-ready → Stage10 noncoding interpreted

| Metric | Stage08 VDB-ready | Stage10 noncoding interpreted |
|---|---:|---:|
| rows |  |  |
| columns | 33 | 43 |
| distinct_variant_ids | 757635 | 729815 |

Removed columns:
```text
clinical_status
```

Added columns:
```text
clinical_evidence,clinical_status,is_clinically_supported,is_high_quality,is_potential_artifact,is_rare_candidate,is_regulatory_candidate,noncoding_functional_context,noncoding_interpretation_label,qc_reliability,rarity_flag
```

Shared columns:
```text
alternate_allele,annotation_source,annotation_version,chromosome,clinical_significance,clinvar_significance,consequence,epilepsy_flag,exac_af,frequency_status,gene_id,gene_mapping_status,gene_symbol,gnomad_af,impact_class,interpretability_status,mito_flag,population_frequency,position,qc_status,quality_flag,reference_allele,run_id,sample_id,source_pipeline,thousand_genomes_af,transcript_id,variant_class,variant_context,variant_effect_severity,variant_id,variant_type
```

### Stage09 coding interpreted → Stage11 prioritized

| Metric | Stage09 coding interpreted | Stage11 prioritized |
|---|---:|---:|
| rows |  |  |
| columns | 43 | 52 |
| distinct_variant_ids | 27820 | 757635 |

Removed columns:
```text
is_potential_artifact
```

Added columns:
```text
is_high_priority_candidate,is_low_priority_candidate,is_moderate_priority_candidate,is_potential_artifact,is_uninterpretable,priority_rank,priority_reason,priority_tier,source_interpretation_label,variant_origin
```

Shared columns:
```text
alternate_allele,annotation_source,annotation_version,chromosome,clinical_evidence,clinical_significance,clinical_status,clinvar_significance,coding_interpretation_label,consequence,epilepsy_flag,exac_af,frequency_status,functional_impact,gene_id,gene_mapping_status,gene_symbol,gnomad_af,impact_class,interpretability_status,is_clinically_supported,is_high_quality,is_lof_candidate,is_rare_candidate,mito_flag,population_frequency,position,qc_reliability,qc_status,quality_flag,rarity_flag,reference_allele,run_id,sample_id,source_pipeline,thousand_genomes_af,transcript_id,variant_class,variant_context,variant_effect_severity,variant_id,variant_type
```

### Stage10 noncoding interpreted → Stage11 prioritized

| Metric | Stage10 noncoding interpreted | Stage11 prioritized |
|---|---:|---:|
| rows |  |  |
| columns | 43 | 52 |
| distinct_variant_ids | 729815 | 757635 |

Removed columns:
```text
is_potential_artifact,is_regulatory_candidate,noncoding_functional_context,noncoding_interpretation_label
```

Added columns:
```text
coding_interpretation_label,functional_impact,is_high_priority_candidate,is_lof_candidate,is_low_priority_candidate,is_moderate_priority_candidate,is_potential_artifact,is_uninterpretable,priority_rank,priority_reason,priority_tier,source_interpretation_label,variant_origin
```

Shared columns:
```text
alternate_allele,annotation_source,annotation_version,chromosome,clinical_evidence,clinical_significance,clinical_status,clinvar_significance,consequence,epilepsy_flag,exac_af,frequency_status,gene_id,gene_mapping_status,gene_symbol,gnomad_af,impact_class,interpretability_status,is_clinically_supported,is_high_quality,is_rare_candidate,mito_flag,population_frequency,position,qc_reliability,qc_status,quality_flag,rarity_flag,reference_allele,run_id,sample_id,source_pipeline,thousand_genomes_af,transcript_id,variant_class,variant_context,variant_effect_severity,variant_id,variant_type
```

### Stage11 prioritized → Stage12 validation candidates

| Metric | Stage11 prioritized | Stage12 validation candidates |
|---|---:|---:|
| rows |  |  |
| columns | 52 | 56 |
| distinct_variant_ids | 757635 | 757635 |

Removed columns:
```text
is_uninterpretable
```

Added columns:
```text
is_uninterpretable,suggested_validation_method,validation_priority,validation_reason,validation_required
```

Shared columns:
```text
alternate_allele,annotation_source,annotation_version,chromosome,clinical_evidence,clinical_significance,clinical_status,clinvar_significance,coding_interpretation_label,consequence,epilepsy_flag,exac_af,frequency_status,functional_impact,gene_id,gene_mapping_status,gene_symbol,gnomad_af,impact_class,interpretability_status,is_clinically_supported,is_high_priority_candidate,is_high_quality,is_lof_candidate,is_low_priority_candidate,is_moderate_priority_candidate,is_potential_artifact,is_rare_candidate,mito_flag,population_frequency,position,priority_rank,priority_reason,priority_tier,qc_reliability,qc_status,quality_flag,rarity_flag,reference_allele,run_id,sample_id,source_interpretation_label,source_pipeline,thousand_genomes_af,transcript_id,variant_class,variant_context,variant_effect_severity,variant_id,variant_origin,variant_type
```

---

## ERR10619230 / run_2026_06_01_004903 / q3

# Artifact Inventory

### Stage07 annotated_variants.tsv

- path: `results/run_2026_06_01_004903/processed/ERR10619230_run_2026_06_01_004903.annotated_variants.tsv`
- size_bytes: 159669102
- rows: 
- columns: 25
- header_sha256: `617480c310358e0f764d2996153e3428ee6270702ce98194140c6e7ba6074d9f`
- has_variant_id: yes
- distinct_variant_ids: 681054

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	quality_flag
    10	gene_id
    11	gene_symbol
    12	transcript_id
    13	consequence
    14	impact_class
    15	impact
    16	variant_class
    17	variant_type
    18	clinical_significance
    19	clinvar_significance
    20	population_frequency
    21	gnomad_af
    22	exac_af
    23	thousand_genomes_af
    24	mito_flag
    25	epilepsy_flag
```

First data row preview:
```text
ERR10619230	run_2026_06_01_004903	variant_annotation_pipeline	1:13273:G:C	1	13273	G	C	PASS	ENSG00000223972	DDX11L1	ENST00000450305.2	non_coding_transcript_exon_variant	MODIFIER	MODIFIER	SNV	non-coding	NA	NA	0.0950	0.0950	NA	0.0204	False	False

```

### Stage08 selected_transcript_consequences.tsv

- path: `results/run_2026_06_01_004903/processed/stage_08_selected_transcript_consequences.tsv`
- size_bytes: 229644521
- rows: 
- columns: 33
- header_sha256: `cd5a915c5bc9d15f76cda12616b5dae1e039ecb5f00164e46acc177e2d42a402`
- has_variant_id: yes
- distinct_variant_ids: 681054

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
```

First data row preview:
```text
ERR10619230	run_2026_06_01_004903	variant_annotation_pipeline	1:13273:G:C	1	13273	G	C	snv	noncoding	PASS	ENSG00000223972	DDX11L1	ENST00000450305.2	non_coding_transcript_exon_variant	MODIFIER	NA	NA	0.095	0.0950	NA	0.0204	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	noncoding_transcript	MODIFIER	pass	needs_external_annotation	common	missing

```

### Stage08 vdb_ready_variants.tsv

- path: `results/run_2026_06_01_004903/processed/stage_08_vdb_ready_variants.tsv`
- size_bytes: 229644521
- rows: 
- columns: 33
- header_sha256: `cd5a915c5bc9d15f76cda12616b5dae1e039ecb5f00164e46acc177e2d42a402`
- has_variant_id: yes
- distinct_variant_ids: 681054

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
```

First data row preview:
```text
ERR10619230	run_2026_06_01_004903	variant_annotation_pipeline	1:13273:G:C	1	13273	G	C	snv	noncoding	PASS	ENSG00000223972	DDX11L1	ENST00000450305.2	non_coding_transcript_exon_variant	MODIFIER	NA	NA	0.095	0.0950	NA	0.0204	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	noncoding_transcript	MODIFIER	pass	needs_external_annotation	common	missing

```

### Stage08 coding_candidates.tsv

- path: `results/run_2026_06_01_004903/processed/coding_candidates.tsv`
- size_bytes: 7891142
- rows: 
- columns: 33
- header_sha256: `cd5a915c5bc9d15f76cda12616b5dae1e039ecb5f00164e46acc177e2d42a402`
- has_variant_id: yes
- distinct_variant_ids: 24556

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
```

First data row preview:
```text
ERR10619230	run_2026_06_01_004903	variant_annotation_pipeline	1:924533:A:G	1	924533	A	G	snv	coding	PASS	ENSG00000187634	SAMD11	ENST00000616016.5	synonymous_variant	LOW	NA	NA	0.7498	0.7498	NA	0.4039	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	coding	LOW	pass	interpretable_now	common	missing

```

### Stage08 splice_region_candidates.tsv

- path: `results/run_2026_06_01_004903/processed/splice_region_candidates.tsv`
- size_bytes: 1065272
- rows: 
- columns: 33
- header_sha256: `cd5a915c5bc9d15f76cda12616b5dae1e039ecb5f00164e46acc177e2d42a402`
- has_variant_id: yes
- distinct_variant_ids: 2889

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
```

First data row preview:
```text
ERR10619230	run_2026_06_01_004903	variant_annotation_pipeline	1:1041950:T:C	1	1041950	T	C	snv	coding	PASS	ENSG00000188157	AGRN	ENST00000379370.7	splice_region_variant&splice_polypyrimidine_tract_variant&intron_variant	LOW	benign	benign	0.8852	0.8852	NA	0.6899	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	benign

```

### Stage08 noncoding_candidates.tsv

- path: `results/run_2026_06_01_004903/processed/noncoding_candidates.tsv`
- size_bytes: 220862579
- rows: 
- columns: 33
- header_sha256: `cd5a915c5bc9d15f76cda12616b5dae1e039ecb5f00164e46acc177e2d42a402`
- has_variant_id: yes
- distinct_variant_ids: 654106

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
```

First data row preview:
```text
ERR10619230	run_2026_06_01_004903	variant_annotation_pipeline	1:13273:G:C	1	13273	G	C	snv	noncoding	PASS	ENSG00000223972	DDX11L1	ENST00000450305.2	non_coding_transcript_exon_variant	MODIFIER	NA	NA	0.095	0.0950	NA	0.0204	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	noncoding_transcript	MODIFIER	pass	needs_external_annotation	common	missing

```

### Stage08 variant_summary.tsv

- path: `results/run_2026_06_01_004903/processed/stage_08_variant_summary.tsv`
- size_bytes: 172841864
- rows: 
- columns: 26
- header_sha256: `a0088e61e1ce409de45d1365b177ff47234ecb57dacab3ef0cb50fe3f613b55a`
- has_variant_id: yes
- distinct_variant_ids: 681054

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	gene_symbols
    10	gene_mapping_status
    11	worst_consequence
    12	highest_impact
    13	canonical_present
    14	coding_flag
    15	splice_flag
    16	noncoding_flag
    17	transcript_count
    18	variant_type
    19	variant_class
    20	quality_flag
    21	qc_status
    22	population_frequency
    23	frequency_status
    24	clinical_status
    25	annotation_source
    26	annotation_version
```

First data row preview:
```text
ERR10619230	run_2026_06_01_004903	variant_annotation_pipeline	10:100006981:A:ACTG	10	100006981	A	ACTG	DNMBP	mapped	intron_variant	MODIFIER	False	False	False	True	1	insertion	noncoding	PASS	pass	NULL	missing	missing	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #

```

### Stage08 rdgp_gene_evidence_seed.tsv

- path: `results/run_2026_06_01_004903/processed/stage_08_rdgp_gene_evidence_seed.tsv`
- size_bytes: 11780591
- rows: 
- columns: 10
- header_sha256: `18d500222bcf3f2b99e044e14b9a1f0647d3f9bf1593555fa16359bb3996d3a3`
- has_variant_id: no
- distinct_variant_ids: NA

Header:
```text
     1	sample_id
     2	gene_id
     3	gene_symbol
     4	variant_count
     5	high_impact_variant_count
     6	rare_variant_count
     7	pathogenic_variant_count
     8	max_variant_severity
     9	has_low_quality_evidence
    10	contributing_variant_ids
```

First data row preview:
```text
ERR10619230	ENSG00000000003	TSPAN6	1	0	0	0	MODIFIER	False	X:100632405:CA:C

```

### Stage09 coding_interpreted.tsv

- path: `results/run_2026_06_01_004903/processed/stage_09_coding_interpreted.tsv`
- size_bytes: 11460041
- rows: 
- columns: 43
- header_sha256: `8132a0aab15233fd27576c5624b2e8393fe622aa2bd651c8bdfc94c6215d5d3b`
- has_variant_id: yes
- distinct_variant_ids: 26948

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
    34	functional_impact
    35	rarity_flag
    36	clinical_evidence
    37	qc_reliability
    38	coding_interpretation_label
    39	is_lof_candidate
    40	is_rare_candidate
    41	is_clinically_supported
    42	is_high_quality
    43	is_potential_artifact
```

First data row preview:
```text
ERR10619230	run_2026_06_01_004903	variant_annotation_pipeline	1:924533:A:G	1	924533	A	G	snv	coding	PASS	ENSG00000187634	SAMD11	ENST00000616016.5	synonymous_variant	LOW	NA	NA	0.7498	0.7498	NA	0.4039	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	coding	LOW	pass	interpretable_now	common	missing	synonymous	common	missing	high_confidence	coding_common_or_low_support	False	False	False	True	False

```

### Stage10 noncoding_interpreted.tsv

- path: `results/run_2026_06_01_004903/processed/stage_10_noncoding_interpreted.tsv`
- size_bytes: 288240801
- rows: 
- columns: 43
- header_sha256: `52d4bd70320ef627d745025507d0b4bd3197d1fef0d1436811b20a6c4486c87e`
- has_variant_id: yes
- distinct_variant_ids: 654106

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
    34	noncoding_functional_context
    35	rarity_flag
    36	clinical_evidence
    37	qc_reliability
    38	noncoding_interpretation_label
    39	is_regulatory_candidate
    40	is_rare_candidate
    41	is_clinically_supported
    42	is_high_quality
    43	is_potential_artifact
```

First data row preview:
```text
ERR10619230	run_2026_06_01_004903	variant_annotation_pipeline	1:13273:G:C	1	13273	G	C	snv	noncoding	PASS	ENSG00000223972	DDX11L1	ENST00000450305.2	non_coding_transcript_exon_variant	MODIFIER	NA	NA	0.095	0.0950	NA	0.0204	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	noncoding_transcript	MODIFIER	pass	needs_external_annotation	common	missing	transcript_associated	common	missing	high_confidence	noncoding_common_or_low_support	False	False	False	True	False

```

### Stage11 prioritized_variants.tsv

- path: `results/run_2026_06_01_004903/processed/stage_11_prioritized_variants.tsv`
- size_bytes: 370613536
- rows: 
- columns: 52
- header_sha256: `446c7603e23bb60bb4da68196782174abe5aea562307628ddf55513a5e4bae54`
- has_variant_id: yes
- distinct_variant_ids: 681054

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
    34	functional_impact
    35	rarity_flag
    36	clinical_evidence
    37	qc_reliability
    38	coding_interpretation_label
    39	is_lof_candidate
    40	is_rare_candidate
    41	is_clinically_supported
    42	is_high_quality
    43	is_potential_artifact
    44	variant_origin
    45	source_interpretation_label
    46	priority_tier
    47	priority_rank
    48	priority_reason
    49	is_high_priority_candidate
    50	is_moderate_priority_candidate
    51	is_low_priority_candidate
    52	is_uninterpretable
```

First data row preview:
```text
ERR10619230	run_2026_06_01_004903	variant_annotation_pipeline	1:924533:A:G	1	924533	A	G	snv	coding	PASS	ENSG00000187634	SAMD11	ENST00000616016.5	synonymous_variant	LOW	NA	NA	0.7498	0.7498	NA	0.4039	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	coding	LOW	pass	interpretable_now	common	missing	synonymous	common	missing	high_confidence	coding_common_or_low_support	False	False	False	True	False	coding	coding_common_or_low_support	tier_3_low_support_or_common	3	coding label coding_common

```

### Stage11 gene_variant_counts.tsv

- path: `results/run_2026_06_01_004903/processed/stage_11_gene_variant_counts.tsv`
- size_bytes: 803793
- rows: 
- columns: 2
- header_sha256: `a728a2468d9a3e433005a28bf32c7a8a5cce42466215a1338be8933e0d5ade04`
- has_variant_id: no
- distinct_variant_ids: NA

Header:
```text
     1	gene_id
     2	variant_count
```

First data row preview:
```text
NA	105028

```

### Stage12 validation_candidates.tsv

- path: `results/run_2026_06_01_004903/processed/stage_12_validation_candidates.tsv`
- size_bytes: 401466535
- rows: 
- columns: 56
- header_sha256: `d43ee98c7824c468f1e6523d1886bf0d1164aa6e1003677f73093d557ac2d385`
- has_variant_id: yes
- distinct_variant_ids: 681054

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
    34	functional_impact
    35	rarity_flag
    36	clinical_evidence
    37	qc_reliability
    38	coding_interpretation_label
    39	is_lof_candidate
    40	is_rare_candidate
    41	is_clinically_supported
    42	is_high_quality
    43	is_potential_artifact
    44	variant_origin
    45	source_interpretation_label
    46	priority_tier
    47	priority_rank
    48	priority_reason
    49	is_high_priority_candidate
    50	is_moderate_priority_candidate
    51	is_low_priority_candidate
    52	is_uninterpretable
    53	validation_required
    54	validation_priority
    55	suggested_validation_method
    56	validation_reason
```

First data row preview:
```text
ERR10619230	run_2026_06_01_004903	variant_annotation_pipeline	1:924533:A:G	1	924533	A	G	snv	coding	PASS	ENSG00000187634	SAMD11	ENST00000616016.5	synonymous_variant	LOW	NA	NA	0.7498	0.7498	NA	0.4039	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	coding	LOW	pass	interpretable_now	common	missing	synonymous	common	missing	high_confidence	coding_common_or_low_support	False	False	False	True	False	coding	coding_common_or_low_support	tier_3_low_support_or_common	3	coding label coding_common

```

# Transition Lineage

### Stage07 annotated → Stage08 selected

| Metric | Stage07 annotated | Stage08 selected |
|---|---:|---:|
| rows |  |  |
| columns | 25 | 33 |
| distinct_variant_ids | 681054 | 681054 |

Removed columns:
```text
epilepsy_flag,impact
```

Added columns:
```text
annotation_source,annotation_version,clinical_status,epilepsy_flag,frequency_status,gene_mapping_status,interpretability_status,qc_status,variant_context,variant_effect_severity
```

Shared columns:
```text
alternate_allele,chromosome,clinical_significance,clinvar_significance,consequence,exac_af,gene_id,gene_symbol,gnomad_af,impact_class,mito_flag,population_frequency,position,quality_flag,reference_allele,run_id,sample_id,source_pipeline,thousand_genomes_af,transcript_id,variant_class,variant_id,variant_type
```

### Stage08 selected → Stage08 VDB-ready

| Metric | Stage08 selected | Stage08 VDB-ready |
|---|---:|---:|
| rows |  |  |
| columns | 33 | 33 |
| distinct_variant_ids | 681054 | 681054 |

Removed columns:
```text
NONE
```

Added columns:
```text
NONE
```

Shared columns:
```text
alternate_allele,annotation_source,annotation_version,chromosome,clinical_significance,clinical_status,clinvar_significance,consequence,epilepsy_flag,exac_af,frequency_status,gene_id,gene_mapping_status,gene_symbol,gnomad_af,impact_class,interpretability_status,mito_flag,population_frequency,position,qc_status,quality_flag,reference_allele,run_id,sample_id,source_pipeline,thousand_genomes_af,transcript_id,variant_class,variant_context,variant_effect_severity,variant_id,variant_type
```

### Stage08 VDB-ready → Stage09 coding interpreted

| Metric | Stage08 VDB-ready | Stage09 coding interpreted |
|---|---:|---:|
| rows |  |  |
| columns | 33 | 43 |
| distinct_variant_ids | 681054 | 26948 |

Removed columns:
```text
clinical_status
```

Added columns:
```text
clinical_evidence,clinical_status,coding_interpretation_label,functional_impact,is_clinically_supported,is_high_quality,is_lof_candidate,is_potential_artifact,is_rare_candidate,qc_reliability,rarity_flag
```

Shared columns:
```text
alternate_allele,annotation_source,annotation_version,chromosome,clinical_significance,clinvar_significance,consequence,epilepsy_flag,exac_af,frequency_status,gene_id,gene_mapping_status,gene_symbol,gnomad_af,impact_class,interpretability_status,mito_flag,population_frequency,position,qc_status,quality_flag,reference_allele,run_id,sample_id,source_pipeline,thousand_genomes_af,transcript_id,variant_class,variant_context,variant_effect_severity,variant_id,variant_type
```

### Stage08 VDB-ready → Stage10 noncoding interpreted

| Metric | Stage08 VDB-ready | Stage10 noncoding interpreted |
|---|---:|---:|
| rows |  |  |
| columns | 33 | 43 |
| distinct_variant_ids | 681054 | 654106 |

Removed columns:
```text
clinical_status
```

Added columns:
```text
clinical_evidence,clinical_status,is_clinically_supported,is_high_quality,is_potential_artifact,is_rare_candidate,is_regulatory_candidate,noncoding_functional_context,noncoding_interpretation_label,qc_reliability,rarity_flag
```

Shared columns:
```text
alternate_allele,annotation_source,annotation_version,chromosome,clinical_significance,clinvar_significance,consequence,epilepsy_flag,exac_af,frequency_status,gene_id,gene_mapping_status,gene_symbol,gnomad_af,impact_class,interpretability_status,mito_flag,population_frequency,position,qc_status,quality_flag,reference_allele,run_id,sample_id,source_pipeline,thousand_genomes_af,transcript_id,variant_class,variant_context,variant_effect_severity,variant_id,variant_type
```

### Stage09 coding interpreted → Stage11 prioritized

| Metric | Stage09 coding interpreted | Stage11 prioritized |
|---|---:|---:|
| rows |  |  |
| columns | 43 | 52 |
| distinct_variant_ids | 26948 | 681054 |

Removed columns:
```text
is_potential_artifact
```

Added columns:
```text
is_high_priority_candidate,is_low_priority_candidate,is_moderate_priority_candidate,is_potential_artifact,is_uninterpretable,priority_rank,priority_reason,priority_tier,source_interpretation_label,variant_origin
```

Shared columns:
```text
alternate_allele,annotation_source,annotation_version,chromosome,clinical_evidence,clinical_significance,clinical_status,clinvar_significance,coding_interpretation_label,consequence,epilepsy_flag,exac_af,frequency_status,functional_impact,gene_id,gene_mapping_status,gene_symbol,gnomad_af,impact_class,interpretability_status,is_clinically_supported,is_high_quality,is_lof_candidate,is_rare_candidate,mito_flag,population_frequency,position,qc_reliability,qc_status,quality_flag,rarity_flag,reference_allele,run_id,sample_id,source_pipeline,thousand_genomes_af,transcript_id,variant_class,variant_context,variant_effect_severity,variant_id,variant_type
```

### Stage10 noncoding interpreted → Stage11 prioritized

| Metric | Stage10 noncoding interpreted | Stage11 prioritized |
|---|---:|---:|
| rows |  |  |
| columns | 43 | 52 |
| distinct_variant_ids | 654106 | 681054 |

Removed columns:
```text
is_potential_artifact,is_regulatory_candidate,noncoding_functional_context,noncoding_interpretation_label
```

Added columns:
```text
coding_interpretation_label,functional_impact,is_high_priority_candidate,is_lof_candidate,is_low_priority_candidate,is_moderate_priority_candidate,is_potential_artifact,is_uninterpretable,priority_rank,priority_reason,priority_tier,source_interpretation_label,variant_origin
```

Shared columns:
```text
alternate_allele,annotation_source,annotation_version,chromosome,clinical_evidence,clinical_significance,clinical_status,clinvar_significance,consequence,epilepsy_flag,exac_af,frequency_status,gene_id,gene_mapping_status,gene_symbol,gnomad_af,impact_class,interpretability_status,is_clinically_supported,is_high_quality,is_rare_candidate,mito_flag,population_frequency,position,qc_reliability,qc_status,quality_flag,rarity_flag,reference_allele,run_id,sample_id,source_pipeline,thousand_genomes_af,transcript_id,variant_class,variant_context,variant_effect_severity,variant_id,variant_type
```

### Stage11 prioritized → Stage12 validation candidates

| Metric | Stage11 prioritized | Stage12 validation candidates |
|---|---:|---:|
| rows |  |  |
| columns | 52 | 56 |
| distinct_variant_ids | 681054 | 681054 |

Removed columns:
```text
is_uninterpretable
```

Added columns:
```text
is_uninterpretable,suggested_validation_method,validation_priority,validation_reason,validation_required
```

Shared columns:
```text
alternate_allele,annotation_source,annotation_version,chromosome,clinical_evidence,clinical_significance,clinical_status,clinvar_significance,coding_interpretation_label,consequence,epilepsy_flag,exac_af,frequency_status,functional_impact,gene_id,gene_mapping_status,gene_symbol,gnomad_af,impact_class,interpretability_status,is_clinically_supported,is_high_priority_candidate,is_high_quality,is_lof_candidate,is_low_priority_candidate,is_moderate_priority_candidate,is_potential_artifact,is_rare_candidate,mito_flag,population_frequency,position,priority_rank,priority_reason,priority_tier,qc_reliability,qc_status,quality_flag,rarity_flag,reference_allele,run_id,sample_id,source_interpretation_label,source_pipeline,thousand_genomes_af,transcript_id,variant_class,variant_context,variant_effect_severity,variant_id,variant_origin,variant_type
```

---

## ERR10619241 / run_2026_06_02_052302 / q1

# Artifact Inventory

### Stage07 annotated_variants.tsv

- path: `results/run_2026_06_02_052302/processed/ERR10619241_run_2026_06_02_052302.annotated_variants.tsv`
- size_bytes: 213192791
- rows: 
- columns: 25
- header_sha256: `617480c310358e0f764d2996153e3428ee6270702ce98194140c6e7ba6074d9f`
- has_variant_id: yes
- distinct_variant_ids: 909698

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	quality_flag
    10	gene_id
    11	gene_symbol
    12	transcript_id
    13	consequence
    14	impact_class
    15	impact
    16	variant_class
    17	variant_type
    18	clinical_significance
    19	clinvar_significance
    20	population_frequency
    21	gnomad_af
    22	exac_af
    23	thousand_genomes_af
    24	mito_flag
    25	epilepsy_flag
```

First data row preview:
```text
ERR10619241	run_2026_06_02_052302	variant_annotation_pipeline	1:13012:G:C	1	13012	G	C	PASS	ENSG00000223972	DDX11L1	ENST00000450305.2	non_coding_transcript_exon_variant	MODIFIER	MODIFIER	SNV	non-coding	NA	NA	0.008552	0.008552	NA	NA	False	False

```

### Stage08 selected_transcript_consequences.tsv

- path: `results/run_2026_06_02_052302/processed/stage_08_selected_transcript_consequences.tsv`
- size_bytes: 306748326
- rows: 
- columns: 33
- header_sha256: `cd5a915c5bc9d15f76cda12616b5dae1e039ecb5f00164e46acc177e2d42a402`
- has_variant_id: yes
- distinct_variant_ids: 909698

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
```

First data row preview:
```text
ERR10619241	run_2026_06_02_052302	variant_annotation_pipeline	1:13012:G:C	1	13012	G	C	snv	noncoding	PASS	ENSG00000223972	DDX11L1	ENST00000450305.2	non_coding_transcript_exon_variant	MODIFIER	NA	NA	0.008552	0.008552	NA	NA	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	noncoding_transcript	MODIFIER	pass	needs_external_annotation	rare	missing

```

### Stage08 vdb_ready_variants.tsv

- path: `results/run_2026_06_02_052302/processed/stage_08_vdb_ready_variants.tsv`
- size_bytes: 306748326
- rows: 
- columns: 33
- header_sha256: `cd5a915c5bc9d15f76cda12616b5dae1e039ecb5f00164e46acc177e2d42a402`
- has_variant_id: yes
- distinct_variant_ids: 909698

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
```

First data row preview:
```text
ERR10619241	run_2026_06_02_052302	variant_annotation_pipeline	1:13012:G:C	1	13012	G	C	snv	noncoding	PASS	ENSG00000223972	DDX11L1	ENST00000450305.2	non_coding_transcript_exon_variant	MODIFIER	NA	NA	0.008552	0.008552	NA	NA	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	noncoding_transcript	MODIFIER	pass	needs_external_annotation	rare	missing

```

### Stage08 coding_candidates.tsv

- path: `results/run_2026_06_02_052302/processed/coding_candidates.tsv`
- size_bytes: 7606237
- rows: 
- columns: 33
- header_sha256: `cd5a915c5bc9d15f76cda12616b5dae1e039ecb5f00164e46acc177e2d42a402`
- has_variant_id: yes
- distinct_variant_ids: 23648

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
```

First data row preview:
```text
ERR10619241	run_2026_06_02_052302	variant_annotation_pipeline	1:69270:A:G	1	69270	A	G	snv	coding	PASS	ENSG00000186092	OR4F5	ENST00000641515.2	synonymous_variant	LOW	NA	NA	0.9961	0.9961	NA	NA	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	coding	LOW	pass	interpretable_now	common	missing

```

### Stage08 splice_region_candidates.tsv

- path: `results/run_2026_06_02_052302/processed/splice_region_candidates.tsv`
- size_bytes: 1093743
- rows: 
- columns: 33
- header_sha256: `cd5a915c5bc9d15f76cda12616b5dae1e039ecb5f00164e46acc177e2d42a402`
- has_variant_id: yes
- distinct_variant_ids: 2951

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
```

First data row preview:
```text
ERR10619241	run_2026_06_02_052302	variant_annotation_pipeline	1:847806:G:C	1	847806	G	C	snv	coding	PASS	ENSG00000228794	LINC01128	ENST00000666741.3	splice_region_variant&non_coding_transcript_exon_variant	LOW	NA	NA	0.0144	0.0040	NA	0.0144	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	low_frequency	missing

```

### Stage08 noncoding_candidates.tsv

- path: `results/run_2026_06_02_052302/processed/noncoding_candidates.tsv`
- size_bytes: 298222743
- rows: 
- columns: 33
- header_sha256: `cd5a915c5bc9d15f76cda12616b5dae1e039ecb5f00164e46acc177e2d42a402`
- has_variant_id: yes
- distinct_variant_ids: 883594

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
```

First data row preview:
```text
ERR10619241	run_2026_06_02_052302	variant_annotation_pipeline	1:13012:G:C	1	13012	G	C	snv	noncoding	PASS	ENSG00000223972	DDX11L1	ENST00000450305.2	non_coding_transcript_exon_variant	MODIFIER	NA	NA	0.008552	0.008552	NA	NA	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	noncoding_transcript	MODIFIER	pass	needs_external_annotation	rare	missing

```

### Stage08 variant_summary.tsv

- path: `results/run_2026_06_02_052302/processed/stage_08_variant_summary.tsv`
- size_bytes: 231077248
- rows: 
- columns: 26
- header_sha256: `a0088e61e1ce409de45d1365b177ff47234ecb57dacab3ef0cb50fe3f613b55a`
- has_variant_id: yes
- distinct_variant_ids: 909698

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	gene_symbols
    10	gene_mapping_status
    11	worst_consequence
    12	highest_impact
    13	canonical_present
    14	coding_flag
    15	splice_flag
    16	noncoding_flag
    17	transcript_count
    18	variant_type
    19	variant_class
    20	quality_flag
    21	qc_status
    22	population_frequency
    23	frequency_status
    24	clinical_status
    25	annotation_source
    26	annotation_version
```

First data row preview:
```text
ERR10619241	run_2026_06_02_052302	variant_annotation_pipeline	10:100024168:G:A	10	100024168	G	A	NA	mapped	upstream_gene_variant	MODIFIER	False	False	False	True	1	snv	noncoding	PASS	pass	0.277	common	missing	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #

```

### Stage08 rdgp_gene_evidence_seed.tsv

- path: `results/run_2026_06_02_052302/processed/stage_08_rdgp_gene_evidence_seed.tsv`
- size_bytes: 14936680
- rows: 
- columns: 10
- header_sha256: `18d500222bcf3f2b99e044e14b9a1f0647d3f9bf1593555fa16359bb3996d3a3`
- has_variant_id: no
- distinct_variant_ids: NA

Header:
```text
     1	sample_id
     2	gene_id
     3	gene_symbol
     4	variant_count
     5	high_impact_variant_count
     6	rare_variant_count
     7	pathogenic_variant_count
     8	max_variant_severity
     9	has_low_quality_evidence
    10	contributing_variant_ids
```

First data row preview:
```text
ERR10619241	ENSG00000000003	TSPAN6	3	0	0	0	MODIFIER	False	X:100624832:C:CT,X:100632405:C:CA,X:100632926:T:TA

```

### Stage09 coding_interpreted.tsv

- path: `results/run_2026_06_02_052302/processed/stage_09_coding_interpreted.tsv`
- size_bytes: 11121024
- rows: 
- columns: 43
- header_sha256: `8132a0aab15233fd27576c5624b2e8393fe622aa2bd651c8bdfc94c6215d5d3b`
- has_variant_id: yes
- distinct_variant_ids: 26104

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
    34	functional_impact
    35	rarity_flag
    36	clinical_evidence
    37	qc_reliability
    38	coding_interpretation_label
    39	is_lof_candidate
    40	is_rare_candidate
    41	is_clinically_supported
    42	is_high_quality
    43	is_potential_artifact
```

First data row preview:
```text
ERR10619241	run_2026_06_02_052302	variant_annotation_pipeline	1:69270:A:G	1	69270	A	G	snv	coding	PASS	ENSG00000186092	OR4F5	ENST00000641515.2	synonymous_variant	LOW	NA	NA	0.9961	0.9961	NA	NA	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	coding	LOW	pass	interpretable_now	common	missing	synonymous	common	missing	high_confidence	coding_common_or_low_support	False	False	False	True	False

```

### Stage10 noncoding_interpreted.tsv

- path: `results/run_2026_06_02_052302/processed/stage_10_noncoding_interpreted.tsv`
- size_bytes: 389265185
- rows: 
- columns: 43
- header_sha256: `52d4bd70320ef627d745025507d0b4bd3197d1fef0d1436811b20a6c4486c87e`
- has_variant_id: yes
- distinct_variant_ids: 883594

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
    34	noncoding_functional_context
    35	rarity_flag
    36	clinical_evidence
    37	qc_reliability
    38	noncoding_interpretation_label
    39	is_regulatory_candidate
    40	is_rare_candidate
    41	is_clinically_supported
    42	is_high_quality
    43	is_potential_artifact
```

First data row preview:
```text
ERR10619241	run_2026_06_02_052302	variant_annotation_pipeline	1:13012:G:C	1	13012	G	C	snv	noncoding	PASS	ENSG00000223972	DDX11L1	ENST00000450305.2	non_coding_transcript_exon_variant	MODIFIER	NA	NA	0.008552	0.008552	NA	NA	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	noncoding_transcript	MODIFIER	pass	needs_external_annotation	rare	missing	transcript_associated	rare	missing	high_confidence	regulatory_or_transcript_rare	False	True	False	True	False

```

### Stage11 prioritized_variants.tsv

- path: `results/run_2026_06_02_052302/processed/stage_11_prioritized_variants.tsv`
- size_bytes: 494796094
- rows: 
- columns: 52
- header_sha256: `446c7603e23bb60bb4da68196782174abe5aea562307628ddf55513a5e4bae54`
- has_variant_id: yes
- distinct_variant_ids: 909698

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
    34	functional_impact
    35	rarity_flag
    36	clinical_evidence
    37	qc_reliability
    38	coding_interpretation_label
    39	is_lof_candidate
    40	is_rare_candidate
    41	is_clinically_supported
    42	is_high_quality
    43	is_potential_artifact
    44	variant_origin
    45	source_interpretation_label
    46	priority_tier
    47	priority_rank
    48	priority_reason
    49	is_high_priority_candidate
    50	is_moderate_priority_candidate
    51	is_low_priority_candidate
    52	is_uninterpretable
```

First data row preview:
```text
ERR10619241	run_2026_06_02_052302	variant_annotation_pipeline	1:69270:A:G	1	69270	A	G	snv	coding	PASS	ENSG00000186092	OR4F5	ENST00000641515.2	synonymous_variant	LOW	NA	NA	0.9961	0.9961	NA	NA	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	coding	LOW	pass	interpretable_now	common	missing	synonymous	common	missing	high_confidence	coding_common_or_low_support	False	False	False	True	False	coding	coding_common_or_low_support	tier_3_low_support_or_common	3	coding label coding_common_or_low

```

### Stage11 gene_variant_counts.tsv

- path: `results/run_2026_06_02_052302/processed/stage_11_gene_variant_counts.tsv`
- size_bytes: 844661
- rows: 
- columns: 2
- header_sha256: `a728a2468d9a3e433005a28bf32c7a8a5cce42466215a1338be8933e0d5ade04`
- has_variant_id: no
- distinct_variant_ids: NA

Header:
```text
     1	gene_id
     2	variant_count
```

First data row preview:
```text
NA	147659

```

### Stage12 validation_candidates.tsv

- path: `results/run_2026_06_02_052302/processed/stage_12_validation_candidates.tsv`
- size_bytes: 536052400
- rows: 
- columns: 56
- header_sha256: `d43ee98c7824c468f1e6523d1886bf0d1164aa6e1003677f73093d557ac2d385`
- has_variant_id: yes
- distinct_variant_ids: 909698

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
    34	functional_impact
    35	rarity_flag
    36	clinical_evidence
    37	qc_reliability
    38	coding_interpretation_label
    39	is_lof_candidate
    40	is_rare_candidate
    41	is_clinically_supported
    42	is_high_quality
    43	is_potential_artifact
    44	variant_origin
    45	source_interpretation_label
    46	priority_tier
    47	priority_rank
    48	priority_reason
    49	is_high_priority_candidate
    50	is_moderate_priority_candidate
    51	is_low_priority_candidate
    52	is_uninterpretable
    53	validation_required
    54	validation_priority
    55	suggested_validation_method
    56	validation_reason
```

First data row preview:
```text
ERR10619241	run_2026_06_02_052302	variant_annotation_pipeline	1:69270:A:G	1	69270	A	G	snv	coding	PASS	ENSG00000186092	OR4F5	ENST00000641515.2	synonymous_variant	LOW	NA	NA	0.9961	0.9961	NA	NA	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	coding	LOW	pass	interpretable_now	common	missing	synonymous	common	missing	high_confidence	coding_common_or_low_support	False	False	False	True	False	coding	coding_common_or_low_support	tier_3_low_support_or_common	3	coding label coding_common_or_low

```

# Transition Lineage

### Stage07 annotated → Stage08 selected

| Metric | Stage07 annotated | Stage08 selected |
|---|---:|---:|
| rows |  |  |
| columns | 25 | 33 |
| distinct_variant_ids | 909698 | 909698 |

Removed columns:
```text
epilepsy_flag,impact
```

Added columns:
```text
annotation_source,annotation_version,clinical_status,epilepsy_flag,frequency_status,gene_mapping_status,interpretability_status,qc_status,variant_context,variant_effect_severity
```

Shared columns:
```text
alternate_allele,chromosome,clinical_significance,clinvar_significance,consequence,exac_af,gene_id,gene_symbol,gnomad_af,impact_class,mito_flag,population_frequency,position,quality_flag,reference_allele,run_id,sample_id,source_pipeline,thousand_genomes_af,transcript_id,variant_class,variant_id,variant_type
```

### Stage08 selected → Stage08 VDB-ready

| Metric | Stage08 selected | Stage08 VDB-ready |
|---|---:|---:|
| rows |  |  |
| columns | 33 | 33 |
| distinct_variant_ids | 909698 | 909698 |

Removed columns:
```text
NONE
```

Added columns:
```text
NONE
```

Shared columns:
```text
alternate_allele,annotation_source,annotation_version,chromosome,clinical_significance,clinical_status,clinvar_significance,consequence,epilepsy_flag,exac_af,frequency_status,gene_id,gene_mapping_status,gene_symbol,gnomad_af,impact_class,interpretability_status,mito_flag,population_frequency,position,qc_status,quality_flag,reference_allele,run_id,sample_id,source_pipeline,thousand_genomes_af,transcript_id,variant_class,variant_context,variant_effect_severity,variant_id,variant_type
```

### Stage08 VDB-ready → Stage09 coding interpreted

| Metric | Stage08 VDB-ready | Stage09 coding interpreted |
|---|---:|---:|
| rows |  |  |
| columns | 33 | 43 |
| distinct_variant_ids | 909698 | 26104 |

Removed columns:
```text
clinical_status
```

Added columns:
```text
clinical_evidence,clinical_status,coding_interpretation_label,functional_impact,is_clinically_supported,is_high_quality,is_lof_candidate,is_potential_artifact,is_rare_candidate,qc_reliability,rarity_flag
```

Shared columns:
```text
alternate_allele,annotation_source,annotation_version,chromosome,clinical_significance,clinvar_significance,consequence,epilepsy_flag,exac_af,frequency_status,gene_id,gene_mapping_status,gene_symbol,gnomad_af,impact_class,interpretability_status,mito_flag,population_frequency,position,qc_status,quality_flag,reference_allele,run_id,sample_id,source_pipeline,thousand_genomes_af,transcript_id,variant_class,variant_context,variant_effect_severity,variant_id,variant_type
```

### Stage08 VDB-ready → Stage10 noncoding interpreted

| Metric | Stage08 VDB-ready | Stage10 noncoding interpreted |
|---|---:|---:|
| rows |  |  |
| columns | 33 | 43 |
| distinct_variant_ids | 909698 | 883594 |

Removed columns:
```text
clinical_status
```

Added columns:
```text
clinical_evidence,clinical_status,is_clinically_supported,is_high_quality,is_potential_artifact,is_rare_candidate,is_regulatory_candidate,noncoding_functional_context,noncoding_interpretation_label,qc_reliability,rarity_flag
```

Shared columns:
```text
alternate_allele,annotation_source,annotation_version,chromosome,clinical_significance,clinvar_significance,consequence,epilepsy_flag,exac_af,frequency_status,gene_id,gene_mapping_status,gene_symbol,gnomad_af,impact_class,interpretability_status,mito_flag,population_frequency,position,qc_status,quality_flag,reference_allele,run_id,sample_id,source_pipeline,thousand_genomes_af,transcript_id,variant_class,variant_context,variant_effect_severity,variant_id,variant_type
```

### Stage09 coding interpreted → Stage11 prioritized

| Metric | Stage09 coding interpreted | Stage11 prioritized |
|---|---:|---:|
| rows |  |  |
| columns | 43 | 52 |
| distinct_variant_ids | 26104 | 909698 |

Removed columns:
```text
is_potential_artifact
```

Added columns:
```text
is_high_priority_candidate,is_low_priority_candidate,is_moderate_priority_candidate,is_potential_artifact,is_uninterpretable,priority_rank,priority_reason,priority_tier,source_interpretation_label,variant_origin
```

Shared columns:
```text
alternate_allele,annotation_source,annotation_version,chromosome,clinical_evidence,clinical_significance,clinical_status,clinvar_significance,coding_interpretation_label,consequence,epilepsy_flag,exac_af,frequency_status,functional_impact,gene_id,gene_mapping_status,gene_symbol,gnomad_af,impact_class,interpretability_status,is_clinically_supported,is_high_quality,is_lof_candidate,is_rare_candidate,mito_flag,population_frequency,position,qc_reliability,qc_status,quality_flag,rarity_flag,reference_allele,run_id,sample_id,source_pipeline,thousand_genomes_af,transcript_id,variant_class,variant_context,variant_effect_severity,variant_id,variant_type
```

### Stage10 noncoding interpreted → Stage11 prioritized

| Metric | Stage10 noncoding interpreted | Stage11 prioritized |
|---|---:|---:|
| rows |  |  |
| columns | 43 | 52 |
| distinct_variant_ids | 883594 | 909698 |

Removed columns:
```text
is_potential_artifact,is_regulatory_candidate,noncoding_functional_context,noncoding_interpretation_label
```

Added columns:
```text
coding_interpretation_label,functional_impact,is_high_priority_candidate,is_lof_candidate,is_low_priority_candidate,is_moderate_priority_candidate,is_potential_artifact,is_uninterpretable,priority_rank,priority_reason,priority_tier,source_interpretation_label,variant_origin
```

Shared columns:
```text
alternate_allele,annotation_source,annotation_version,chromosome,clinical_evidence,clinical_significance,clinical_status,clinvar_significance,consequence,epilepsy_flag,exac_af,frequency_status,gene_id,gene_mapping_status,gene_symbol,gnomad_af,impact_class,interpretability_status,is_clinically_supported,is_high_quality,is_rare_candidate,mito_flag,population_frequency,position,qc_reliability,qc_status,quality_flag,rarity_flag,reference_allele,run_id,sample_id,source_pipeline,thousand_genomes_af,transcript_id,variant_class,variant_context,variant_effect_severity,variant_id,variant_type
```

### Stage11 prioritized → Stage12 validation candidates

| Metric | Stage11 prioritized | Stage12 validation candidates |
|---|---:|---:|
| rows |  |  |
| columns | 52 | 56 |
| distinct_variant_ids | 909698 | 909698 |

Removed columns:
```text
is_uninterpretable
```

Added columns:
```text
is_uninterpretable,suggested_validation_method,validation_priority,validation_reason,validation_required
```

Shared columns:
```text
alternate_allele,annotation_source,annotation_version,chromosome,clinical_evidence,clinical_significance,clinical_status,clinvar_significance,coding_interpretation_label,consequence,epilepsy_flag,exac_af,frequency_status,functional_impact,gene_id,gene_mapping_status,gene_symbol,gnomad_af,impact_class,interpretability_status,is_clinically_supported,is_high_priority_candidate,is_high_quality,is_lof_candidate,is_low_priority_candidate,is_moderate_priority_candidate,is_potential_artifact,is_rare_candidate,mito_flag,population_frequency,position,priority_rank,priority_reason,priority_tier,qc_reliability,qc_status,quality_flag,rarity_flag,reference_allele,run_id,sample_id,source_interpretation_label,source_pipeline,thousand_genomes_af,transcript_id,variant_class,variant_context,variant_effect_severity,variant_id,variant_origin,variant_type
```

---

## ERR10619281 / run_2026_05_27_233524 / median

# Artifact Inventory

### Stage07 annotated_variants.tsv

- path: `results/run_2026_05_27_233524/processed/ERR10619281_run_2026_05_27_233524.annotated_variants.tsv`
- size_bytes: 190317266
- rows: 
- columns: 25
- header_sha256: `617480c310358e0f764d2996153e3428ee6270702ce98194140c6e7ba6074d9f`
- has_variant_id: yes
- distinct_variant_ids: 811554

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	quality_flag
    10	gene_id
    11	gene_symbol
    12	transcript_id
    13	consequence
    14	impact_class
    15	impact
    16	variant_class
    17	variant_type
    18	clinical_significance
    19	clinvar_significance
    20	population_frequency
    21	gnomad_af
    22	exac_af
    23	thousand_genomes_af
    24	mito_flag
    25	epilepsy_flag
```

First data row preview:
```text
ERR10619281	run_2026_05_27_233524	variant_annotation_pipeline	1:13813:T:G	1	13813	T	G	PASS	ENSG00000290825	DDX11L16	ENST00000832823.1	upstream_gene_variant	MODIFIER	MODIFIER	SNV	non-coding	NA	NA	0.4861	0.4861	NA	NA	False	False

```

### Stage08 selected_transcript_consequences.tsv

- path: `results/run_2026_05_27_233524/processed/stage_08_selected_transcript_consequences.tsv`
- size_bytes: 273767292
- rows: 
- columns: 33
- header_sha256: `cd5a915c5bc9d15f76cda12616b5dae1e039ecb5f00164e46acc177e2d42a402`
- has_variant_id: yes
- distinct_variant_ids: 811554

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
```

First data row preview:
```text
ERR10619281	run_2026_05_27_233524	variant_annotation_pipeline	1:13813:T:G	1	13813	T	G	snv	noncoding	PASS	ENSG00000290825	DDX11L16	ENST00000832823.1	upstream_gene_variant	MODIFIER	NA	NA	0.4861	0.4861	NA	NA	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	regulatory	MODIFIER	pass	needs_external_annotation	common	missing

```

### Stage08 vdb_ready_variants.tsv

- path: `results/run_2026_05_27_233524/processed/stage_08_vdb_ready_variants.tsv`
- size_bytes: 273767292
- rows: 
- columns: 33
- header_sha256: `cd5a915c5bc9d15f76cda12616b5dae1e039ecb5f00164e46acc177e2d42a402`
- has_variant_id: yes
- distinct_variant_ids: 811554

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
```

First data row preview:
```text
ERR10619281	run_2026_05_27_233524	variant_annotation_pipeline	1:13813:T:G	1	13813	T	G	snv	noncoding	PASS	ENSG00000290825	DDX11L16	ENST00000832823.1	upstream_gene_variant	MODIFIER	NA	NA	0.4861	0.4861	NA	NA	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	regulatory	MODIFIER	pass	needs_external_annotation	common	missing

```

### Stage08 coding_candidates.tsv

- path: `results/run_2026_05_27_233524/processed/coding_candidates.tsv`
- size_bytes: 8136434
- rows: 
- columns: 33
- header_sha256: `cd5a915c5bc9d15f76cda12616b5dae1e039ecb5f00164e46acc177e2d42a402`
- has_variant_id: yes
- distinct_variant_ids: 25288

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
```

First data row preview:
```text
ERR10619281	run_2026_05_27_233524	variant_annotation_pipeline	1:69270:A:G	1	69270	A	G	snv	coding	PASS	ENSG00000186092	OR4F5	ENST00000641515.2	synonymous_variant	LOW	NA	NA	0.9961	0.9961	NA	NA	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	coding	LOW	pass	interpretable_now	common	missing

```

### Stage08 splice_region_candidates.tsv

- path: `results/run_2026_05_27_233524/processed/splice_region_candidates.tsv`
- size_bytes: 1155621
- rows: 
- columns: 33
- header_sha256: `cd5a915c5bc9d15f76cda12616b5dae1e039ecb5f00164e46acc177e2d42a402`
- has_variant_id: yes
- distinct_variant_ids: 3128

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
```

First data row preview:
```text
ERR10619281	run_2026_05_27_233524	variant_annotation_pipeline	1:1041950:T:C	1	1041950	T	C	snv	coding	PASS	ENSG00000188157	AGRN	ENST00000379370.7	splice_region_variant&splice_polypyrimidine_tract_variant&intron_variant	LOW	benign	benign	0.8852	0.8852	NA	0.6899	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	benign

```

### Stage08 noncoding_candidates.tsv

- path: `results/run_2026_05_27_233524/processed/noncoding_candidates.tsv`
- size_bytes: 264668428
- rows: 
- columns: 33
- header_sha256: `cd5a915c5bc9d15f76cda12616b5dae1e039ecb5f00164e46acc177e2d42a402`
- has_variant_id: yes
- distinct_variant_ids: 783685

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
```

First data row preview:
```text
ERR10619281	run_2026_05_27_233524	variant_annotation_pipeline	1:13813:T:G	1	13813	T	G	snv	noncoding	PASS	ENSG00000290825	DDX11L16	ENST00000832823.1	upstream_gene_variant	MODIFIER	NA	NA	0.4861	0.4861	NA	NA	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	regulatory	MODIFIER	pass	needs_external_annotation	common	missing

```

### Stage08 variant_summary.tsv

- path: `results/run_2026_05_27_233524/processed/stage_08_variant_summary.tsv`
- size_bytes: 206170223
- rows: 
- columns: 26
- header_sha256: `a0088e61e1ce409de45d1365b177ff47234ecb57dacab3ef0cb50fe3f613b55a`
- has_variant_id: yes
- distinct_variant_ids: 811554

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	gene_symbols
    10	gene_mapping_status
    11	worst_consequence
    12	highest_impact
    13	canonical_present
    14	coding_flag
    15	splice_flag
    16	noncoding_flag
    17	transcript_count
    18	variant_type
    19	variant_class
    20	quality_flag
    21	qc_status
    22	population_frequency
    23	frequency_status
    24	clinical_status
    25	annotation_source
    26	annotation_version
```

First data row preview:
```text
ERR10619281	run_2026_05_27_233524	variant_annotation_pipeline	10:100007115:C:CA	10	100007115	C	CA	DNMBP	mapped	intron_variant	MODIFIER	False	False	False	True	1	insertion	noncoding	PASS	pass	0.00365	rare	missing	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #

```

### Stage08 rdgp_gene_evidence_seed.tsv

- path: `results/run_2026_05_27_233524/processed/stage_08_rdgp_gene_evidence_seed.tsv`
- size_bytes: 13628889
- rows: 
- columns: 10
- header_sha256: `18d500222bcf3f2b99e044e14b9a1f0647d3f9bf1593555fa16359bb3996d3a3`
- has_variant_id: no
- distinct_variant_ids: NA

Header:
```text
     1	sample_id
     2	gene_id
     3	gene_symbol
     4	variant_count
     5	high_impact_variant_count
     6	rare_variant_count
     7	pathogenic_variant_count
     8	max_variant_severity
     9	has_low_quality_evidence
    10	contributing_variant_ids
```

First data row preview:
```text
ERR10619281	ENSG00000000005	TNMD	3	0	0	0	LOW	False	X:100594020:G:A,X:100594054:T:C,X:100602389:A:G

```

### Stage09 coding_interpreted.tsv

- path: `results/run_2026_05_27_233524/processed/stage_09_coding_interpreted.tsv`
- size_bytes: 11870252
- rows: 
- columns: 43
- header_sha256: `8132a0aab15233fd27576c5624b2e8393fe622aa2bd651c8bdfc94c6215d5d3b`
- has_variant_id: yes
- distinct_variant_ids: 27869

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
    34	functional_impact
    35	rarity_flag
    36	clinical_evidence
    37	qc_reliability
    38	coding_interpretation_label
    39	is_lof_candidate
    40	is_rare_candidate
    41	is_clinically_supported
    42	is_high_quality
    43	is_potential_artifact
```

First data row preview:
```text
ERR10619281	run_2026_05_27_233524	variant_annotation_pipeline	1:69270:A:G	1	69270	A	G	snv	coding	PASS	ENSG00000186092	OR4F5	ENST00000641515.2	synonymous_variant	LOW	NA	NA	0.9961	0.9961	NA	NA	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	coding	LOW	pass	interpretable_now	common	missing	synonymous	common	missing	high_confidence	coding_common_or_low_support	False	False	False	True	False

```

### Stage10 noncoding_interpreted.tsv

- path: `results/run_2026_05_27_233524/processed/stage_10_noncoding_interpreted.tsv`
- size_bytes: 345440819
- rows: 
- columns: 43
- header_sha256: `52d4bd70320ef627d745025507d0b4bd3197d1fef0d1436811b20a6c4486c87e`
- has_variant_id: yes
- distinct_variant_ids: 783685

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
    34	noncoding_functional_context
    35	rarity_flag
    36	clinical_evidence
    37	qc_reliability
    38	noncoding_interpretation_label
    39	is_regulatory_candidate
    40	is_rare_candidate
    41	is_clinically_supported
    42	is_high_quality
    43	is_potential_artifact
```

First data row preview:
```text
ERR10619281	run_2026_05_27_233524	variant_annotation_pipeline	1:13813:T:G	1	13813	T	G	snv	noncoding	PASS	ENSG00000290825	DDX11L16	ENST00000832823.1	upstream_gene_variant	MODIFIER	NA	NA	0.4861	0.4861	NA	NA	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	regulatory	MODIFIER	pass	needs_external_annotation	common	missing	proximal	common	missing	high_confidence	noncoding_common_or_low_support	False	False	False	True	False

```

### Stage11 prioritized_variants.tsv

- path: `results/run_2026_05_27_233524/processed/stage_11_prioritized_variants.tsv`
- size_bytes: 441652271
- rows: 
- columns: 52
- header_sha256: `446c7603e23bb60bb4da68196782174abe5aea562307628ddf55513a5e4bae54`
- has_variant_id: yes
- distinct_variant_ids: 811554

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
    34	functional_impact
    35	rarity_flag
    36	clinical_evidence
    37	qc_reliability
    38	coding_interpretation_label
    39	is_lof_candidate
    40	is_rare_candidate
    41	is_clinically_supported
    42	is_high_quality
    43	is_potential_artifact
    44	variant_origin
    45	source_interpretation_label
    46	priority_tier
    47	priority_rank
    48	priority_reason
    49	is_high_priority_candidate
    50	is_moderate_priority_candidate
    51	is_low_priority_candidate
    52	is_uninterpretable
```

First data row preview:
```text
ERR10619281	run_2026_05_27_233524	variant_annotation_pipeline	1:69270:A:G	1	69270	A	G	snv	coding	PASS	ENSG00000186092	OR4F5	ENST00000641515.2	synonymous_variant	LOW	NA	NA	0.9961	0.9961	NA	NA	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	coding	LOW	pass	interpretable_now	common	missing	synonymous	common	missing	high_confidence	coding_common_or_low_support	False	False	False	True	False	coding	coding_common_or_low_support	tier_3_low_support_or_common	3	coding label coding_common_or_low

```

### Stage11 gene_variant_counts.tsv

- path: `results/run_2026_05_27_233524/processed/stage_11_gene_variant_counts.tsv`
- size_bytes: 836049
- rows: 
- columns: 2
- header_sha256: `a728a2468d9a3e433005a28bf32c7a8a5cce42466215a1338be8933e0d5ade04`
- has_variant_id: no
- distinct_variant_ids: NA

Header:
```text
     1	gene_id
     2	variant_count
```

First data row preview:
```text
NA	128568

```

### Stage12 validation_candidates.tsv

- path: `results/run_2026_05_27_233524/processed/stage_12_validation_candidates.tsv`
- size_bytes: 478429000
- rows: 
- columns: 56
- header_sha256: `d43ee98c7824c468f1e6523d1886bf0d1164aa6e1003677f73093d557ac2d385`
- has_variant_id: yes
- distinct_variant_ids: 811554

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
    34	functional_impact
    35	rarity_flag
    36	clinical_evidence
    37	qc_reliability
    38	coding_interpretation_label
    39	is_lof_candidate
    40	is_rare_candidate
    41	is_clinically_supported
    42	is_high_quality
    43	is_potential_artifact
    44	variant_origin
    45	source_interpretation_label
    46	priority_tier
    47	priority_rank
    48	priority_reason
    49	is_high_priority_candidate
    50	is_moderate_priority_candidate
    51	is_low_priority_candidate
    52	is_uninterpretable
    53	validation_required
    54	validation_priority
    55	suggested_validation_method
    56	validation_reason
```

First data row preview:
```text
ERR10619281	run_2026_05_27_233524	variant_annotation_pipeline	1:69270:A:G	1	69270	A	G	snv	coding	PASS	ENSG00000186092	OR4F5	ENST00000641515.2	synonymous_variant	LOW	NA	NA	0.9961	0.9961	NA	NA	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	coding	LOW	pass	interpretable_now	common	missing	synonymous	common	missing	high_confidence	coding_common_or_low_support	False	False	False	True	False	coding	coding_common_or_low_support	tier_3_low_support_or_common	3	coding label coding_common_or_low

```

# Transition Lineage

### Stage07 annotated → Stage08 selected

| Metric | Stage07 annotated | Stage08 selected |
|---|---:|---:|
| rows |  |  |
| columns | 25 | 33 |
| distinct_variant_ids | 811554 | 811554 |

Removed columns:
```text
epilepsy_flag,impact
```

Added columns:
```text
annotation_source,annotation_version,clinical_status,epilepsy_flag,frequency_status,gene_mapping_status,interpretability_status,qc_status,variant_context,variant_effect_severity
```

Shared columns:
```text
alternate_allele,chromosome,clinical_significance,clinvar_significance,consequence,exac_af,gene_id,gene_symbol,gnomad_af,impact_class,mito_flag,population_frequency,position,quality_flag,reference_allele,run_id,sample_id,source_pipeline,thousand_genomes_af,transcript_id,variant_class,variant_id,variant_type
```

### Stage08 selected → Stage08 VDB-ready

| Metric | Stage08 selected | Stage08 VDB-ready |
|---|---:|---:|
| rows |  |  |
| columns | 33 | 33 |
| distinct_variant_ids | 811554 | 811554 |

Removed columns:
```text
NONE
```

Added columns:
```text
NONE
```

Shared columns:
```text
alternate_allele,annotation_source,annotation_version,chromosome,clinical_significance,clinical_status,clinvar_significance,consequence,epilepsy_flag,exac_af,frequency_status,gene_id,gene_mapping_status,gene_symbol,gnomad_af,impact_class,interpretability_status,mito_flag,population_frequency,position,qc_status,quality_flag,reference_allele,run_id,sample_id,source_pipeline,thousand_genomes_af,transcript_id,variant_class,variant_context,variant_effect_severity,variant_id,variant_type
```

### Stage08 VDB-ready → Stage09 coding interpreted

| Metric | Stage08 VDB-ready | Stage09 coding interpreted |
|---|---:|---:|
| rows |  |  |
| columns | 33 | 43 |
| distinct_variant_ids | 811554 | 27869 |

Removed columns:
```text
clinical_status
```

Added columns:
```text
clinical_evidence,clinical_status,coding_interpretation_label,functional_impact,is_clinically_supported,is_high_quality,is_lof_candidate,is_potential_artifact,is_rare_candidate,qc_reliability,rarity_flag
```

Shared columns:
```text
alternate_allele,annotation_source,annotation_version,chromosome,clinical_significance,clinvar_significance,consequence,epilepsy_flag,exac_af,frequency_status,gene_id,gene_mapping_status,gene_symbol,gnomad_af,impact_class,interpretability_status,mito_flag,population_frequency,position,qc_status,quality_flag,reference_allele,run_id,sample_id,source_pipeline,thousand_genomes_af,transcript_id,variant_class,variant_context,variant_effect_severity,variant_id,variant_type
```

### Stage08 VDB-ready → Stage10 noncoding interpreted

| Metric | Stage08 VDB-ready | Stage10 noncoding interpreted |
|---|---:|---:|
| rows |  |  |
| columns | 33 | 43 |
| distinct_variant_ids | 811554 | 783685 |

Removed columns:
```text
clinical_status
```

Added columns:
```text
clinical_evidence,clinical_status,is_clinically_supported,is_high_quality,is_potential_artifact,is_rare_candidate,is_regulatory_candidate,noncoding_functional_context,noncoding_interpretation_label,qc_reliability,rarity_flag
```

Shared columns:
```text
alternate_allele,annotation_source,annotation_version,chromosome,clinical_significance,clinvar_significance,consequence,epilepsy_flag,exac_af,frequency_status,gene_id,gene_mapping_status,gene_symbol,gnomad_af,impact_class,interpretability_status,mito_flag,population_frequency,position,qc_status,quality_flag,reference_allele,run_id,sample_id,source_pipeline,thousand_genomes_af,transcript_id,variant_class,variant_context,variant_effect_severity,variant_id,variant_type
```

### Stage09 coding interpreted → Stage11 prioritized

| Metric | Stage09 coding interpreted | Stage11 prioritized |
|---|---:|---:|
| rows |  |  |
| columns | 43 | 52 |
| distinct_variant_ids | 27869 | 811554 |

Removed columns:
```text
is_potential_artifact
```

Added columns:
```text
is_high_priority_candidate,is_low_priority_candidate,is_moderate_priority_candidate,is_potential_artifact,is_uninterpretable,priority_rank,priority_reason,priority_tier,source_interpretation_label,variant_origin
```

Shared columns:
```text
alternate_allele,annotation_source,annotation_version,chromosome,clinical_evidence,clinical_significance,clinical_status,clinvar_significance,coding_interpretation_label,consequence,epilepsy_flag,exac_af,frequency_status,functional_impact,gene_id,gene_mapping_status,gene_symbol,gnomad_af,impact_class,interpretability_status,is_clinically_supported,is_high_quality,is_lof_candidate,is_rare_candidate,mito_flag,population_frequency,position,qc_reliability,qc_status,quality_flag,rarity_flag,reference_allele,run_id,sample_id,source_pipeline,thousand_genomes_af,transcript_id,variant_class,variant_context,variant_effect_severity,variant_id,variant_type
```

### Stage10 noncoding interpreted → Stage11 prioritized

| Metric | Stage10 noncoding interpreted | Stage11 prioritized |
|---|---:|---:|
| rows |  |  |
| columns | 43 | 52 |
| distinct_variant_ids | 783685 | 811554 |

Removed columns:
```text
is_potential_artifact,is_regulatory_candidate,noncoding_functional_context,noncoding_interpretation_label
```

Added columns:
```text
coding_interpretation_label,functional_impact,is_high_priority_candidate,is_lof_candidate,is_low_priority_candidate,is_moderate_priority_candidate,is_potential_artifact,is_uninterpretable,priority_rank,priority_reason,priority_tier,source_interpretation_label,variant_origin
```

Shared columns:
```text
alternate_allele,annotation_source,annotation_version,chromosome,clinical_evidence,clinical_significance,clinical_status,clinvar_significance,consequence,epilepsy_flag,exac_af,frequency_status,gene_id,gene_mapping_status,gene_symbol,gnomad_af,impact_class,interpretability_status,is_clinically_supported,is_high_quality,is_rare_candidate,mito_flag,population_frequency,position,qc_reliability,qc_status,quality_flag,rarity_flag,reference_allele,run_id,sample_id,source_pipeline,thousand_genomes_af,transcript_id,variant_class,variant_context,variant_effect_severity,variant_id,variant_type
```

### Stage11 prioritized → Stage12 validation candidates

| Metric | Stage11 prioritized | Stage12 validation candidates |
|---|---:|---:|
| rows |  |  |
| columns | 52 | 56 |
| distinct_variant_ids | 811554 | 811554 |

Removed columns:
```text
is_uninterpretable
```

Added columns:
```text
is_uninterpretable,suggested_validation_method,validation_priority,validation_reason,validation_required
```

Shared columns:
```text
alternate_allele,annotation_source,annotation_version,chromosome,clinical_evidence,clinical_significance,clinical_status,clinvar_significance,coding_interpretation_label,consequence,epilepsy_flag,exac_af,frequency_status,functional_impact,gene_id,gene_mapping_status,gene_symbol,gnomad_af,impact_class,interpretability_status,is_clinically_supported,is_high_priority_candidate,is_high_quality,is_lof_candidate,is_low_priority_candidate,is_moderate_priority_candidate,is_potential_artifact,is_rare_candidate,mito_flag,population_frequency,position,priority_rank,priority_reason,priority_tier,qc_reliability,qc_status,quality_flag,rarity_flag,reference_allele,run_id,sample_id,source_interpretation_label,source_pipeline,thousand_genomes_af,transcript_id,variant_class,variant_context,variant_effect_severity,variant_id,variant_origin,variant_type
```

---

## ERR10619285 / run_2026_06_02_124300 / median

# Artifact Inventory

### Stage07 annotated_variants.tsv

- path: `results/run_2026_06_02_124300/processed/ERR10619285_run_2026_06_02_124300.annotated_variants.tsv`
- size_bytes: 186489504
- rows: 
- columns: 25
- header_sha256: `617480c310358e0f764d2996153e3428ee6270702ce98194140c6e7ba6074d9f`
- has_variant_id: yes
- distinct_variant_ids: 795059

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	quality_flag
    10	gene_id
    11	gene_symbol
    12	transcript_id
    13	consequence
    14	impact_class
    15	impact
    16	variant_class
    17	variant_type
    18	clinical_significance
    19	clinvar_significance
    20	population_frequency
    21	gnomad_af
    22	exac_af
    23	thousand_genomes_af
    24	mito_flag
    25	epilepsy_flag
```

First data row preview:
```text
ERR10619285	run_2026_06_02_124300	variant_annotation_pipeline	1:13289:CCT:C	1	13289	CCT	C	PASS	ENSG00000223972	DDX11L1	ENST00000450305.2	non_coding_transcript_exon_variant	MODIFIER	MODIFIER	deletion	non-coding	NA	NA	0.0040	0.0040	NA	0	False	False

```

### Stage08 selected_transcript_consequences.tsv

- path: `results/run_2026_06_02_124300/processed/stage_08_selected_transcript_consequences.tsv`
- size_bytes: 268217339
- rows: 
- columns: 33
- header_sha256: `cd5a915c5bc9d15f76cda12616b5dae1e039ecb5f00164e46acc177e2d42a402`
- has_variant_id: yes
- distinct_variant_ids: 795059

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
```

First data row preview:
```text
ERR10619285	run_2026_06_02_124300	variant_annotation_pipeline	1:13289:CCT:C	1	13289	CCT	C	deletion	noncoding	PASS	ENSG00000223972	DDX11L1	ENST00000450305.2	non_coding_transcript_exon_variant	MODIFIER	NA	NA	0.004	0.0040	NA	0	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	noncoding_transcript	MODIFIER	pass	needs_external_annotation	rare	missing

```

### Stage08 vdb_ready_variants.tsv

- path: `results/run_2026_06_02_124300/processed/stage_08_vdb_ready_variants.tsv`
- size_bytes: 268217339
- rows: 
- columns: 33
- header_sha256: `cd5a915c5bc9d15f76cda12616b5dae1e039ecb5f00164e46acc177e2d42a402`
- has_variant_id: yes
- distinct_variant_ids: 795059

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
```

First data row preview:
```text
ERR10619285	run_2026_06_02_124300	variant_annotation_pipeline	1:13289:CCT:C	1	13289	CCT	C	deletion	noncoding	PASS	ENSG00000223972	DDX11L1	ENST00000450305.2	non_coding_transcript_exon_variant	MODIFIER	NA	NA	0.004	0.0040	NA	0	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	noncoding_transcript	MODIFIER	pass	needs_external_annotation	rare	missing

```

### Stage08 coding_candidates.tsv

- path: `results/run_2026_06_02_124300/processed/coding_candidates.tsv`
- size_bytes: 7850514
- rows: 
- columns: 33
- header_sha256: `cd5a915c5bc9d15f76cda12616b5dae1e039ecb5f00164e46acc177e2d42a402`
- has_variant_id: yes
- distinct_variant_ids: 24437

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
```

First data row preview:
```text
ERR10619285	run_2026_06_02_124300	variant_annotation_pipeline	1:69270:A:G	1	69270	A	G	snv	coding	PASS	ENSG00000186092	OR4F5	ENST00000641515.2	synonymous_variant	LOW	NA	NA	0.9961	0.9961	NA	NA	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	coding	LOW	pass	interpretable_now	common	missing

```

### Stage08 splice_region_candidates.tsv

- path: `results/run_2026_06_02_124300/processed/splice_region_candidates.tsv`
- size_bytes: 1108220
- rows: 
- columns: 33
- header_sha256: `cd5a915c5bc9d15f76cda12616b5dae1e039ecb5f00164e46acc177e2d42a402`
- has_variant_id: yes
- distinct_variant_ids: 3003

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
```

First data row preview:
```text
ERR10619285	run_2026_06_02_124300	variant_annotation_pipeline	1:17746:A:G	1	17746	A	G	snv	coding	PASS	ENSG00000310526	WASH7P	ENST00000831140.1	splice_region_variant&splice_polypyrimidine_tract_variant&intron_variant&non_coding_transcript_variant	LOW	NA	NA	0.1499	0.1499	NA	NA	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	missing

```

### Stage08 noncoding_candidates.tsv

- path: `results/run_2026_06_02_124300/processed/noncoding_candidates.tsv`
- size_bytes: 259440578
- rows: 
- columns: 33
- header_sha256: `cd5a915c5bc9d15f76cda12616b5dae1e039ecb5f00164e46acc177e2d42a402`
- has_variant_id: yes
- distinct_variant_ids: 768137

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
```

First data row preview:
```text
ERR10619285	run_2026_06_02_124300	variant_annotation_pipeline	1:13289:CCT:C	1	13289	CCT	C	deletion	noncoding	PASS	ENSG00000223972	DDX11L1	ENST00000450305.2	non_coding_transcript_exon_variant	MODIFIER	NA	NA	0.004	0.0040	NA	0	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	noncoding_transcript	MODIFIER	pass	needs_external_annotation	rare	missing

```

### Stage08 variant_summary.tsv

- path: `results/run_2026_06_02_124300/processed/stage_08_variant_summary.tsv`
- size_bytes: 201939875
- rows: 
- columns: 26
- header_sha256: `a0088e61e1ce409de45d1365b177ff47234ecb57dacab3ef0cb50fe3f613b55a`
- has_variant_id: yes
- distinct_variant_ids: 795059

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	gene_symbols
    10	gene_mapping_status
    11	worst_consequence
    12	highest_impact
    13	canonical_present
    14	coding_flag
    15	splice_flag
    16	noncoding_flag
    17	transcript_count
    18	variant_type
    19	variant_class
    20	quality_flag
    21	qc_status
    22	population_frequency
    23	frequency_status
    24	clinical_status
    25	annotation_source
    26	annotation_version
```

First data row preview:
```text
ERR10619285	run_2026_06_02_124300	variant_annotation_pipeline	10:100005711:G:A	10	100005711	G	A	DNMBP	mapped	intron_variant	MODIFIER	False	False	False	True	1	snv	noncoding	PASS	pass	0.2222	common	missing	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #

```

### Stage08 rdgp_gene_evidence_seed.tsv

- path: `results/run_2026_06_02_124300/processed/stage_08_rdgp_gene_evidence_seed.tsv`
- size_bytes: 13395437
- rows: 
- columns: 10
- header_sha256: `18d500222bcf3f2b99e044e14b9a1f0647d3f9bf1593555fa16359bb3996d3a3`
- has_variant_id: no
- distinct_variant_ids: NA

Header:
```text
     1	sample_id
     2	gene_id
     3	gene_symbol
     4	variant_count
     5	high_impact_variant_count
     6	rare_variant_count
     7	pathogenic_variant_count
     8	max_variant_severity
     9	has_low_quality_evidence
    10	contributing_variant_ids
```

First data row preview:
```text
ERR10619285	ENSG00000000003	TSPAN6	1	0	1	0	MODIFIER	True	X:100627813:CTT:C

```

### Stage09 coding_interpreted.tsv

- path: `results/run_2026_06_02_124300/processed/stage_09_coding_interpreted.tsv`
- size_bytes: 11453017
- rows: 
- columns: 43
- header_sha256: `8132a0aab15233fd27576c5624b2e8393fe622aa2bd651c8bdfc94c6215d5d3b`
- has_variant_id: yes
- distinct_variant_ids: 26922

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
    34	functional_impact
    35	rarity_flag
    36	clinical_evidence
    37	qc_reliability
    38	coding_interpretation_label
    39	is_lof_candidate
    40	is_rare_candidate
    41	is_clinically_supported
    42	is_high_quality
    43	is_potential_artifact
```

First data row preview:
```text
ERR10619285	run_2026_06_02_124300	variant_annotation_pipeline	1:69270:A:G	1	69270	A	G	snv	coding	PASS	ENSG00000186092	OR4F5	ENST00000641515.2	synonymous_variant	LOW	NA	NA	0.9961	0.9961	NA	NA	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	coding	LOW	pass	interpretable_now	common	missing	synonymous	common	missing	high_confidence	coding_common_or_low_support	False	False	False	True	False

```

### Stage10 noncoding_interpreted.tsv

- path: `results/run_2026_06_02_124300/processed/stage_10_noncoding_interpreted.tsv`
- size_bytes: 338619318
- rows: 
- columns: 43
- header_sha256: `52d4bd70320ef627d745025507d0b4bd3197d1fef0d1436811b20a6c4486c87e`
- has_variant_id: yes
- distinct_variant_ids: 768137

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
    34	noncoding_functional_context
    35	rarity_flag
    36	clinical_evidence
    37	qc_reliability
    38	noncoding_interpretation_label
    39	is_regulatory_candidate
    40	is_rare_candidate
    41	is_clinically_supported
    42	is_high_quality
    43	is_potential_artifact
```

First data row preview:
```text
ERR10619285	run_2026_06_02_124300	variant_annotation_pipeline	1:13289:CCT:C	1	13289	CCT	C	deletion	noncoding	PASS	ENSG00000223972	DDX11L1	ENST00000450305.2	non_coding_transcript_exon_variant	MODIFIER	NA	NA	0.004	0.0040	NA	0	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	noncoding_transcript	MODIFIER	pass	needs_external_annotation	rare	missing	transcript_associated	rare	missing	high_confidence	regulatory_or_transcript_rare	False	True	False	True	False

```

### Stage11 prioritized_variants.tsv

- path: `results/run_2026_06_02_124300/processed/stage_11_prioritized_variants.tsv`
- size_bytes: 432692518
- rows: 
- columns: 52
- header_sha256: `446c7603e23bb60bb4da68196782174abe5aea562307628ddf55513a5e4bae54`
- has_variant_id: yes
- distinct_variant_ids: 795059

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
    34	functional_impact
    35	rarity_flag
    36	clinical_evidence
    37	qc_reliability
    38	coding_interpretation_label
    39	is_lof_candidate
    40	is_rare_candidate
    41	is_clinically_supported
    42	is_high_quality
    43	is_potential_artifact
    44	variant_origin
    45	source_interpretation_label
    46	priority_tier
    47	priority_rank
    48	priority_reason
    49	is_high_priority_candidate
    50	is_moderate_priority_candidate
    51	is_low_priority_candidate
    52	is_uninterpretable
```

First data row preview:
```text
ERR10619285	run_2026_06_02_124300	variant_annotation_pipeline	1:69270:A:G	1	69270	A	G	snv	coding	PASS	ENSG00000186092	OR4F5	ENST00000641515.2	synonymous_variant	LOW	NA	NA	0.9961	0.9961	NA	NA	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	coding	LOW	pass	interpretable_now	common	missing	synonymous	common	missing	high_confidence	coding_common_or_low_support	False	False	False	True	False	coding	coding_common_or_low_support	tier_3_low_support_or_common	3	coding label coding_common_or_low

```

### Stage11 gene_variant_counts.tsv

- path: `results/run_2026_06_02_124300/processed/stage_11_gene_variant_counts.tsv`
- size_bytes: 830421
- rows: 
- columns: 2
- header_sha256: `a728a2468d9a3e433005a28bf32c7a8a5cce42466215a1338be8933e0d5ade04`
- has_variant_id: no
- distinct_variant_ids: NA

Header:
```text
     1	gene_id
     2	variant_count
```

First data row preview:
```text
NA	124926

```

### Stage12 validation_candidates.tsv

- path: `results/run_2026_06_02_124300/processed/stage_12_validation_candidates.tsv`
- size_bytes: 468720979
- rows: 
- columns: 56
- header_sha256: `d43ee98c7824c468f1e6523d1886bf0d1164aa6e1003677f73093d557ac2d385`
- has_variant_id: yes
- distinct_variant_ids: 795059

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
    34	functional_impact
    35	rarity_flag
    36	clinical_evidence
    37	qc_reliability
    38	coding_interpretation_label
    39	is_lof_candidate
    40	is_rare_candidate
    41	is_clinically_supported
    42	is_high_quality
    43	is_potential_artifact
    44	variant_origin
    45	source_interpretation_label
    46	priority_tier
    47	priority_rank
    48	priority_reason
    49	is_high_priority_candidate
    50	is_moderate_priority_candidate
    51	is_low_priority_candidate
    52	is_uninterpretable
    53	validation_required
    54	validation_priority
    55	suggested_validation_method
    56	validation_reason
```

First data row preview:
```text
ERR10619285	run_2026_06_02_124300	variant_annotation_pipeline	1:69270:A:G	1	69270	A	G	snv	coding	PASS	ENSG00000186092	OR4F5	ENST00000641515.2	synonymous_variant	LOW	NA	NA	0.9961	0.9961	NA	NA	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	coding	LOW	pass	interpretable_now	common	missing	synonymous	common	missing	high_confidence	coding_common_or_low_support	False	False	False	True	False	coding	coding_common_or_low_support	tier_3_low_support_or_common	3	coding label coding_common_or_low

```

# Transition Lineage

### Stage07 annotated → Stage08 selected

| Metric | Stage07 annotated | Stage08 selected |
|---|---:|---:|
| rows |  |  |
| columns | 25 | 33 |
| distinct_variant_ids | 795059 | 795059 |

Removed columns:
```text
epilepsy_flag,impact
```

Added columns:
```text
annotation_source,annotation_version,clinical_status,epilepsy_flag,frequency_status,gene_mapping_status,interpretability_status,qc_status,variant_context,variant_effect_severity
```

Shared columns:
```text
alternate_allele,chromosome,clinical_significance,clinvar_significance,consequence,exac_af,gene_id,gene_symbol,gnomad_af,impact_class,mito_flag,population_frequency,position,quality_flag,reference_allele,run_id,sample_id,source_pipeline,thousand_genomes_af,transcript_id,variant_class,variant_id,variant_type
```

### Stage08 selected → Stage08 VDB-ready

| Metric | Stage08 selected | Stage08 VDB-ready |
|---|---:|---:|
| rows |  |  |
| columns | 33 | 33 |
| distinct_variant_ids | 795059 | 795059 |

Removed columns:
```text
NONE
```

Added columns:
```text
NONE
```

Shared columns:
```text
alternate_allele,annotation_source,annotation_version,chromosome,clinical_significance,clinical_status,clinvar_significance,consequence,epilepsy_flag,exac_af,frequency_status,gene_id,gene_mapping_status,gene_symbol,gnomad_af,impact_class,interpretability_status,mito_flag,population_frequency,position,qc_status,quality_flag,reference_allele,run_id,sample_id,source_pipeline,thousand_genomes_af,transcript_id,variant_class,variant_context,variant_effect_severity,variant_id,variant_type
```

### Stage08 VDB-ready → Stage09 coding interpreted

| Metric | Stage08 VDB-ready | Stage09 coding interpreted |
|---|---:|---:|
| rows |  |  |
| columns | 33 | 43 |
| distinct_variant_ids | 795059 | 26922 |

Removed columns:
```text
clinical_status
```

Added columns:
```text
clinical_evidence,clinical_status,coding_interpretation_label,functional_impact,is_clinically_supported,is_high_quality,is_lof_candidate,is_potential_artifact,is_rare_candidate,qc_reliability,rarity_flag
```

Shared columns:
```text
alternate_allele,annotation_source,annotation_version,chromosome,clinical_significance,clinvar_significance,consequence,epilepsy_flag,exac_af,frequency_status,gene_id,gene_mapping_status,gene_symbol,gnomad_af,impact_class,interpretability_status,mito_flag,population_frequency,position,qc_status,quality_flag,reference_allele,run_id,sample_id,source_pipeline,thousand_genomes_af,transcript_id,variant_class,variant_context,variant_effect_severity,variant_id,variant_type
```

### Stage08 VDB-ready → Stage10 noncoding interpreted

| Metric | Stage08 VDB-ready | Stage10 noncoding interpreted |
|---|---:|---:|
| rows |  |  |
| columns | 33 | 43 |
| distinct_variant_ids | 795059 | 768137 |

Removed columns:
```text
clinical_status
```

Added columns:
```text
clinical_evidence,clinical_status,is_clinically_supported,is_high_quality,is_potential_artifact,is_rare_candidate,is_regulatory_candidate,noncoding_functional_context,noncoding_interpretation_label,qc_reliability,rarity_flag
```

Shared columns:
```text
alternate_allele,annotation_source,annotation_version,chromosome,clinical_significance,clinvar_significance,consequence,epilepsy_flag,exac_af,frequency_status,gene_id,gene_mapping_status,gene_symbol,gnomad_af,impact_class,interpretability_status,mito_flag,population_frequency,position,qc_status,quality_flag,reference_allele,run_id,sample_id,source_pipeline,thousand_genomes_af,transcript_id,variant_class,variant_context,variant_effect_severity,variant_id,variant_type
```

### Stage09 coding interpreted → Stage11 prioritized

| Metric | Stage09 coding interpreted | Stage11 prioritized |
|---|---:|---:|
| rows |  |  |
| columns | 43 | 52 |
| distinct_variant_ids | 26922 | 795059 |

Removed columns:
```text
is_potential_artifact
```

Added columns:
```text
is_high_priority_candidate,is_low_priority_candidate,is_moderate_priority_candidate,is_potential_artifact,is_uninterpretable,priority_rank,priority_reason,priority_tier,source_interpretation_label,variant_origin
```

Shared columns:
```text
alternate_allele,annotation_source,annotation_version,chromosome,clinical_evidence,clinical_significance,clinical_status,clinvar_significance,coding_interpretation_label,consequence,epilepsy_flag,exac_af,frequency_status,functional_impact,gene_id,gene_mapping_status,gene_symbol,gnomad_af,impact_class,interpretability_status,is_clinically_supported,is_high_quality,is_lof_candidate,is_rare_candidate,mito_flag,population_frequency,position,qc_reliability,qc_status,quality_flag,rarity_flag,reference_allele,run_id,sample_id,source_pipeline,thousand_genomes_af,transcript_id,variant_class,variant_context,variant_effect_severity,variant_id,variant_type
```

### Stage10 noncoding interpreted → Stage11 prioritized

| Metric | Stage10 noncoding interpreted | Stage11 prioritized |
|---|---:|---:|
| rows |  |  |
| columns | 43 | 52 |
| distinct_variant_ids | 768137 | 795059 |

Removed columns:
```text
is_potential_artifact,is_regulatory_candidate,noncoding_functional_context,noncoding_interpretation_label
```

Added columns:
```text
coding_interpretation_label,functional_impact,is_high_priority_candidate,is_lof_candidate,is_low_priority_candidate,is_moderate_priority_candidate,is_potential_artifact,is_uninterpretable,priority_rank,priority_reason,priority_tier,source_interpretation_label,variant_origin
```

Shared columns:
```text
alternate_allele,annotation_source,annotation_version,chromosome,clinical_evidence,clinical_significance,clinical_status,clinvar_significance,consequence,epilepsy_flag,exac_af,frequency_status,gene_id,gene_mapping_status,gene_symbol,gnomad_af,impact_class,interpretability_status,is_clinically_supported,is_high_quality,is_rare_candidate,mito_flag,population_frequency,position,qc_reliability,qc_status,quality_flag,rarity_flag,reference_allele,run_id,sample_id,source_pipeline,thousand_genomes_af,transcript_id,variant_class,variant_context,variant_effect_severity,variant_id,variant_type
```

### Stage11 prioritized → Stage12 validation candidates

| Metric | Stage11 prioritized | Stage12 validation candidates |
|---|---:|---:|
| rows |  |  |
| columns | 52 | 56 |
| distinct_variant_ids | 795059 | 795059 |

Removed columns:
```text
is_uninterpretable
```

Added columns:
```text
is_uninterpretable,suggested_validation_method,validation_priority,validation_reason,validation_required
```

Shared columns:
```text
alternate_allele,annotation_source,annotation_version,chromosome,clinical_evidence,clinical_significance,clinical_status,clinvar_significance,coding_interpretation_label,consequence,epilepsy_flag,exac_af,frequency_status,functional_impact,gene_id,gene_mapping_status,gene_symbol,gnomad_af,impact_class,interpretability_status,is_clinically_supported,is_high_priority_candidate,is_high_quality,is_lof_candidate,is_low_priority_candidate,is_moderate_priority_candidate,is_potential_artifact,is_rare_candidate,mito_flag,population_frequency,position,priority_rank,priority_reason,priority_tier,qc_reliability,qc_status,quality_flag,rarity_flag,reference_allele,run_id,sample_id,source_interpretation_label,source_pipeline,thousand_genomes_af,transcript_id,variant_class,variant_context,variant_effect_severity,variant_id,variant_origin,variant_type
```

---

## ERR10619300 / run_2026_05_27_172531 / median

# Artifact Inventory

### Stage07 annotated_variants.tsv

- path: `results/run_2026_05_27_172531/processed/ERR10619300_run_2026_05_27_172531.annotated_variants.tsv`
- size_bytes: 172658910
- rows: 
- columns: 25
- header_sha256: `617480c310358e0f764d2996153e3428ee6270702ce98194140c6e7ba6074d9f`
- has_variant_id: yes
- distinct_variant_ids: 736468

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	quality_flag
    10	gene_id
    11	gene_symbol
    12	transcript_id
    13	consequence
    14	impact_class
    15	impact
    16	variant_class
    17	variant_type
    18	clinical_significance
    19	clinvar_significance
    20	population_frequency
    21	gnomad_af
    22	exac_af
    23	thousand_genomes_af
    24	mito_flag
    25	epilepsy_flag
```

First data row preview:
```text
ERR10619300	run_2026_05_27_172531	variant_annotation_pipeline	1:13813:T:G	1	13813	T	G	PASS	ENSG00000290825	DDX11L16	ENST00000832823.1	upstream_gene_variant	MODIFIER	MODIFIER	SNV	non-coding	NA	NA	0.4861	0.4861	NA	NA	False	False

```

### Stage08 selected_transcript_consequences.tsv

- path: `results/run_2026_05_27_172531/processed/stage_08_selected_transcript_consequences.tsv`
- size_bytes: 248357863
- rows: 
- columns: 33
- header_sha256: `cd5a915c5bc9d15f76cda12616b5dae1e039ecb5f00164e46acc177e2d42a402`
- has_variant_id: yes
- distinct_variant_ids: 736468

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
```

First data row preview:
```text
ERR10619300	run_2026_05_27_172531	variant_annotation_pipeline	1:13813:T:G	1	13813	T	G	snv	noncoding	PASS	ENSG00000290825	DDX11L16	ENST00000832823.1	upstream_gene_variant	MODIFIER	NA	NA	0.4861	0.4861	NA	NA	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	regulatory	MODIFIER	pass	needs_external_annotation	common	missing

```

### Stage08 vdb_ready_variants.tsv

- path: `results/run_2026_05_27_172531/processed/stage_08_vdb_ready_variants.tsv`
- size_bytes: 248357863
- rows: 
- columns: 33
- header_sha256: `cd5a915c5bc9d15f76cda12616b5dae1e039ecb5f00164e46acc177e2d42a402`
- has_variant_id: yes
- distinct_variant_ids: 736468

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
```

First data row preview:
```text
ERR10619300	run_2026_05_27_172531	variant_annotation_pipeline	1:13813:T:G	1	13813	T	G	snv	noncoding	PASS	ENSG00000290825	DDX11L16	ENST00000832823.1	upstream_gene_variant	MODIFIER	NA	NA	0.4861	0.4861	NA	NA	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	regulatory	MODIFIER	pass	needs_external_annotation	common	missing

```

### Stage08 coding_candidates.tsv

- path: `results/run_2026_05_27_172531/processed/coding_candidates.tsv`
- size_bytes: 7726925
- rows: 
- columns: 33
- header_sha256: `cd5a915c5bc9d15f76cda12616b5dae1e039ecb5f00164e46acc177e2d42a402`
- has_variant_id: yes
- distinct_variant_ids: 24041

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
```

First data row preview:
```text
ERR10619300	run_2026_05_27_172531	variant_annotation_pipeline	1:69270:A:G	1	69270	A	G	snv	coding	PASS	ENSG00000186092	OR4F5	ENST00000641515.2	synonymous_variant	LOW	NA	NA	0.9961	0.9961	NA	NA	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	coding	LOW	pass	interpretable_now	common	missing

```

### Stage08 splice_region_candidates.tsv

- path: `results/run_2026_05_27_172531/processed/splice_region_candidates.tsv`
- size_bytes: 1067690
- rows: 
- columns: 33
- header_sha256: `cd5a915c5bc9d15f76cda12616b5dae1e039ecb5f00164e46acc177e2d42a402`
- has_variant_id: yes
- distinct_variant_ids: 2891

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
```

First data row preview:
```text
ERR10619300	run_2026_05_27_172531	variant_annotation_pipeline	1:17746:A:G	1	17746	A	G	snv	coding	PASS	ENSG00000310526	WASH7P	ENST00000831140.1	splice_region_variant&splice_polypyrimidine_tract_variant&intron_variant&non_coding_transcript_variant	LOW	NA	NA	0.1499	0.1499	NA	NA	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	missing

```

### Stage08 noncoding_candidates.tsv

- path: `results/run_2026_05_27_172531/processed/noncoding_candidates.tsv`
- size_bytes: 239736675
- rows: 
- columns: 33
- header_sha256: `cd5a915c5bc9d15f76cda12616b5dae1e039ecb5f00164e46acc177e2d42a402`
- has_variant_id: yes
- distinct_variant_ids: 710029

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
```

First data row preview:
```text
ERR10619300	run_2026_05_27_172531	variant_annotation_pipeline	1:13813:T:G	1	13813	T	G	snv	noncoding	PASS	ENSG00000290825	DDX11L16	ENST00000832823.1	upstream_gene_variant	MODIFIER	NA	NA	0.4861	0.4861	NA	NA	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	regulatory	MODIFIER	pass	needs_external_annotation	common	missing

```

### Stage08 variant_summary.tsv

- path: `results/run_2026_05_27_172531/processed/stage_08_variant_summary.tsv`
- size_bytes: 186969157
- rows: 
- columns: 26
- header_sha256: `a0088e61e1ce409de45d1365b177ff47234ecb57dacab3ef0cb50fe3f613b55a`
- has_variant_id: yes
- distinct_variant_ids: 736468

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	gene_symbols
    10	gene_mapping_status
    11	worst_consequence
    12	highest_impact
    13	canonical_present
    14	coding_flag
    15	splice_flag
    16	noncoding_flag
    17	transcript_count
    18	variant_type
    19	variant_class
    20	quality_flag
    21	qc_status
    22	population_frequency
    23	frequency_status
    24	clinical_status
    25	annotation_source
    26	annotation_version
```

First data row preview:
```text
ERR10619300	run_2026_05_27_172531	variant_annotation_pipeline	10:100001413:G:GT	10	100001413	G	GT	DNMBP	mapped	intron_variant	MODIFIER	False	False	False	True	1	insertion	noncoding	PASS	pass	0.4633	common	missing	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #

```

### Stage08 rdgp_gene_evidence_seed.tsv

- path: `results/run_2026_05_27_172531/processed/stage_08_rdgp_gene_evidence_seed.tsv`
- size_bytes: 12535650
- rows: 
- columns: 10
- header_sha256: `18d500222bcf3f2b99e044e14b9a1f0647d3f9bf1593555fa16359bb3996d3a3`
- has_variant_id: no
- distinct_variant_ids: NA

Header:
```text
     1	sample_id
     2	gene_id
     3	gene_symbol
     4	variant_count
     5	high_impact_variant_count
     6	rare_variant_count
     7	pathogenic_variant_count
     8	max_variant_severity
     9	has_low_quality_evidence
    10	contributing_variant_ids
```

First data row preview:
```text
ERR10619300	ENSG00000000003	TSPAN6	1	0	1	0	MODIFIER	False	X:100633857:T:C

```

### Stage09 coding_interpreted.tsv

- path: `results/run_2026_05_27_172531/processed/stage_09_coding_interpreted.tsv`
- size_bytes: 11249450
- rows: 
- columns: 43
- header_sha256: `8132a0aab15233fd27576c5624b2e8393fe622aa2bd651c8bdfc94c6215d5d3b`
- has_variant_id: yes
- distinct_variant_ids: 26439

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
    34	functional_impact
    35	rarity_flag
    36	clinical_evidence
    37	qc_reliability
    38	coding_interpretation_label
    39	is_lof_candidate
    40	is_rare_candidate
    41	is_clinically_supported
    42	is_high_quality
    43	is_potential_artifact
```

First data row preview:
```text
ERR10619300	run_2026_05_27_172531	variant_annotation_pipeline	1:69270:A:G	1	69270	A	G	snv	coding	PASS	ENSG00000186092	OR4F5	ENST00000641515.2	synonymous_variant	LOW	NA	NA	0.9961	0.9961	NA	NA	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	coding	LOW	pass	interpretable_now	common	missing	synonymous	common	missing	high_confidence	coding_common_or_low_support	False	False	False	True	False

```

### Stage10 noncoding_interpreted.tsv

- path: `results/run_2026_05_27_172531/processed/stage_10_noncoding_interpreted.tsv`
- size_bytes: 312898466
- rows: 
- columns: 43
- header_sha256: `52d4bd70320ef627d745025507d0b4bd3197d1fef0d1436811b20a6c4486c87e`
- has_variant_id: yes
- distinct_variant_ids: 710029

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
    34	noncoding_functional_context
    35	rarity_flag
    36	clinical_evidence
    37	qc_reliability
    38	noncoding_interpretation_label
    39	is_regulatory_candidate
    40	is_rare_candidate
    41	is_clinically_supported
    42	is_high_quality
    43	is_potential_artifact
```

First data row preview:
```text
ERR10619300	run_2026_05_27_172531	variant_annotation_pipeline	1:13813:T:G	1	13813	T	G	snv	noncoding	PASS	ENSG00000290825	DDX11L16	ENST00000832823.1	upstream_gene_variant	MODIFIER	NA	NA	0.4861	0.4861	NA	NA	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	regulatory	MODIFIER	pass	needs_external_annotation	common	missing	proximal	common	missing	high_confidence	noncoding_common_or_low_support	False	False	False	True	False

```

### Stage11 prioritized_variants.tsv

- path: `results/run_2026_05_27_172531/processed/stage_11_prioritized_variants.tsv`
- size_bytes: 400737008
- rows: 
- columns: 52
- header_sha256: `446c7603e23bb60bb4da68196782174abe5aea562307628ddf55513a5e4bae54`
- has_variant_id: yes
- distinct_variant_ids: 736468

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
    34	functional_impact
    35	rarity_flag
    36	clinical_evidence
    37	qc_reliability
    38	coding_interpretation_label
    39	is_lof_candidate
    40	is_rare_candidate
    41	is_clinically_supported
    42	is_high_quality
    43	is_potential_artifact
    44	variant_origin
    45	source_interpretation_label
    46	priority_tier
    47	priority_rank
    48	priority_reason
    49	is_high_priority_candidate
    50	is_moderate_priority_candidate
    51	is_low_priority_candidate
    52	is_uninterpretable
```

First data row preview:
```text
ERR10619300	run_2026_05_27_172531	variant_annotation_pipeline	1:69270:A:G	1	69270	A	G	snv	coding	PASS	ENSG00000186092	OR4F5	ENST00000641515.2	synonymous_variant	LOW	NA	NA	0.9961	0.9961	NA	NA	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	coding	LOW	pass	interpretable_now	common	missing	synonymous	common	missing	high_confidence	coding_common_or_low_support	False	False	False	True	False	coding	coding_common_or_low_support	tier_3_low_support_or_common	3	coding label coding_common_or_low

```

### Stage11 gene_variant_counts.tsv

- path: `results/run_2026_05_27_172531/processed/stage_11_gene_variant_counts.tsv`
- size_bytes: 814478
- rows: 
- columns: 2
- header_sha256: `a728a2468d9a3e433005a28bf32c7a8a5cce42466215a1338be8933e0d5ade04`
- has_variant_id: no
- distinct_variant_ids: NA

Header:
```text
     1	gene_id
     2	variant_count
```

First data row preview:
```text
NA	115823

```

### Stage12 validation_candidates.tsv

- path: `results/run_2026_05_27_172531/processed/stage_12_validation_candidates.tsv`
- size_bytes: 434113994
- rows: 
- columns: 56
- header_sha256: `d43ee98c7824c468f1e6523d1886bf0d1164aa6e1003677f73093d557ac2d385`
- has_variant_id: yes
- distinct_variant_ids: 736468

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
    34	functional_impact
    35	rarity_flag
    36	clinical_evidence
    37	qc_reliability
    38	coding_interpretation_label
    39	is_lof_candidate
    40	is_rare_candidate
    41	is_clinically_supported
    42	is_high_quality
    43	is_potential_artifact
    44	variant_origin
    45	source_interpretation_label
    46	priority_tier
    47	priority_rank
    48	priority_reason
    49	is_high_priority_candidate
    50	is_moderate_priority_candidate
    51	is_low_priority_candidate
    52	is_uninterpretable
    53	validation_required
    54	validation_priority
    55	suggested_validation_method
    56	validation_reason
```

First data row preview:
```text
ERR10619300	run_2026_05_27_172531	variant_annotation_pipeline	1:69270:A:G	1	69270	A	G	snv	coding	PASS	ENSG00000186092	OR4F5	ENST00000641515.2	synonymous_variant	LOW	NA	NA	0.9961	0.9961	NA	NA	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	coding	LOW	pass	interpretable_now	common	missing	synonymous	common	missing	high_confidence	coding_common_or_low_support	False	False	False	True	False	coding	coding_common_or_low_support	tier_3_low_support_or_common	3	coding label coding_common_or_low

```

# Transition Lineage

### Stage07 annotated → Stage08 selected

| Metric | Stage07 annotated | Stage08 selected |
|---|---:|---:|
| rows |  |  |
| columns | 25 | 33 |
| distinct_variant_ids | 736468 | 736468 |

Removed columns:
```text
epilepsy_flag,impact
```

Added columns:
```text
annotation_source,annotation_version,clinical_status,epilepsy_flag,frequency_status,gene_mapping_status,interpretability_status,qc_status,variant_context,variant_effect_severity
```

Shared columns:
```text
alternate_allele,chromosome,clinical_significance,clinvar_significance,consequence,exac_af,gene_id,gene_symbol,gnomad_af,impact_class,mito_flag,population_frequency,position,quality_flag,reference_allele,run_id,sample_id,source_pipeline,thousand_genomes_af,transcript_id,variant_class,variant_id,variant_type
```

### Stage08 selected → Stage08 VDB-ready

| Metric | Stage08 selected | Stage08 VDB-ready |
|---|---:|---:|
| rows |  |  |
| columns | 33 | 33 |
| distinct_variant_ids | 736468 | 736468 |

Removed columns:
```text
NONE
```

Added columns:
```text
NONE
```

Shared columns:
```text
alternate_allele,annotation_source,annotation_version,chromosome,clinical_significance,clinical_status,clinvar_significance,consequence,epilepsy_flag,exac_af,frequency_status,gene_id,gene_mapping_status,gene_symbol,gnomad_af,impact_class,interpretability_status,mito_flag,population_frequency,position,qc_status,quality_flag,reference_allele,run_id,sample_id,source_pipeline,thousand_genomes_af,transcript_id,variant_class,variant_context,variant_effect_severity,variant_id,variant_type
```

### Stage08 VDB-ready → Stage09 coding interpreted

| Metric | Stage08 VDB-ready | Stage09 coding interpreted |
|---|---:|---:|
| rows |  |  |
| columns | 33 | 43 |
| distinct_variant_ids | 736468 | 26439 |

Removed columns:
```text
clinical_status
```

Added columns:
```text
clinical_evidence,clinical_status,coding_interpretation_label,functional_impact,is_clinically_supported,is_high_quality,is_lof_candidate,is_potential_artifact,is_rare_candidate,qc_reliability,rarity_flag
```

Shared columns:
```text
alternate_allele,annotation_source,annotation_version,chromosome,clinical_significance,clinvar_significance,consequence,epilepsy_flag,exac_af,frequency_status,gene_id,gene_mapping_status,gene_symbol,gnomad_af,impact_class,interpretability_status,mito_flag,population_frequency,position,qc_status,quality_flag,reference_allele,run_id,sample_id,source_pipeline,thousand_genomes_af,transcript_id,variant_class,variant_context,variant_effect_severity,variant_id,variant_type
```

### Stage08 VDB-ready → Stage10 noncoding interpreted

| Metric | Stage08 VDB-ready | Stage10 noncoding interpreted |
|---|---:|---:|
| rows |  |  |
| columns | 33 | 43 |
| distinct_variant_ids | 736468 | 710029 |

Removed columns:
```text
clinical_status
```

Added columns:
```text
clinical_evidence,clinical_status,is_clinically_supported,is_high_quality,is_potential_artifact,is_rare_candidate,is_regulatory_candidate,noncoding_functional_context,noncoding_interpretation_label,qc_reliability,rarity_flag
```

Shared columns:
```text
alternate_allele,annotation_source,annotation_version,chromosome,clinical_significance,clinvar_significance,consequence,epilepsy_flag,exac_af,frequency_status,gene_id,gene_mapping_status,gene_symbol,gnomad_af,impact_class,interpretability_status,mito_flag,population_frequency,position,qc_status,quality_flag,reference_allele,run_id,sample_id,source_pipeline,thousand_genomes_af,transcript_id,variant_class,variant_context,variant_effect_severity,variant_id,variant_type
```

### Stage09 coding interpreted → Stage11 prioritized

| Metric | Stage09 coding interpreted | Stage11 prioritized |
|---|---:|---:|
| rows |  |  |
| columns | 43 | 52 |
| distinct_variant_ids | 26439 | 736468 |

Removed columns:
```text
is_potential_artifact
```

Added columns:
```text
is_high_priority_candidate,is_low_priority_candidate,is_moderate_priority_candidate,is_potential_artifact,is_uninterpretable,priority_rank,priority_reason,priority_tier,source_interpretation_label,variant_origin
```

Shared columns:
```text
alternate_allele,annotation_source,annotation_version,chromosome,clinical_evidence,clinical_significance,clinical_status,clinvar_significance,coding_interpretation_label,consequence,epilepsy_flag,exac_af,frequency_status,functional_impact,gene_id,gene_mapping_status,gene_symbol,gnomad_af,impact_class,interpretability_status,is_clinically_supported,is_high_quality,is_lof_candidate,is_rare_candidate,mito_flag,population_frequency,position,qc_reliability,qc_status,quality_flag,rarity_flag,reference_allele,run_id,sample_id,source_pipeline,thousand_genomes_af,transcript_id,variant_class,variant_context,variant_effect_severity,variant_id,variant_type
```

### Stage10 noncoding interpreted → Stage11 prioritized

| Metric | Stage10 noncoding interpreted | Stage11 prioritized |
|---|---:|---:|
| rows |  |  |
| columns | 43 | 52 |
| distinct_variant_ids | 710029 | 736468 |

Removed columns:
```text
is_potential_artifact,is_regulatory_candidate,noncoding_functional_context,noncoding_interpretation_label
```

Added columns:
```text
coding_interpretation_label,functional_impact,is_high_priority_candidate,is_lof_candidate,is_low_priority_candidate,is_moderate_priority_candidate,is_potential_artifact,is_uninterpretable,priority_rank,priority_reason,priority_tier,source_interpretation_label,variant_origin
```

Shared columns:
```text
alternate_allele,annotation_source,annotation_version,chromosome,clinical_evidence,clinical_significance,clinical_status,clinvar_significance,consequence,epilepsy_flag,exac_af,frequency_status,gene_id,gene_mapping_status,gene_symbol,gnomad_af,impact_class,interpretability_status,is_clinically_supported,is_high_quality,is_rare_candidate,mito_flag,population_frequency,position,qc_reliability,qc_status,quality_flag,rarity_flag,reference_allele,run_id,sample_id,source_pipeline,thousand_genomes_af,transcript_id,variant_class,variant_context,variant_effect_severity,variant_id,variant_type
```

### Stage11 prioritized → Stage12 validation candidates

| Metric | Stage11 prioritized | Stage12 validation candidates |
|---|---:|---:|
| rows |  |  |
| columns | 52 | 56 |
| distinct_variant_ids | 736468 | 736468 |

Removed columns:
```text
is_uninterpretable
```

Added columns:
```text
is_uninterpretable,suggested_validation_method,validation_priority,validation_reason,validation_required
```

Shared columns:
```text
alternate_allele,annotation_source,annotation_version,chromosome,clinical_evidence,clinical_significance,clinical_status,clinvar_significance,coding_interpretation_label,consequence,epilepsy_flag,exac_af,frequency_status,functional_impact,gene_id,gene_mapping_status,gene_symbol,gnomad_af,impact_class,interpretability_status,is_clinically_supported,is_high_priority_candidate,is_high_quality,is_lof_candidate,is_low_priority_candidate,is_moderate_priority_candidate,is_potential_artifact,is_rare_candidate,mito_flag,population_frequency,position,priority_rank,priority_reason,priority_tier,qc_reliability,qc_status,quality_flag,rarity_flag,reference_allele,run_id,sample_id,source_interpretation_label,source_pipeline,thousand_genomes_af,transcript_id,variant_class,variant_context,variant_effect_severity,variant_id,variant_origin,variant_type
```

---

## ERR10619309 / run_2026_06_02_181024 / q1

# Artifact Inventory

### Stage07 annotated_variants.tsv

- path: `results/run_2026_06_02_181024/processed/ERR10619309_run_2026_06_02_181024.annotated_variants.tsv`
- size_bytes: 206089676
- rows: 
- columns: 25
- header_sha256: `617480c310358e0f764d2996153e3428ee6270702ce98194140c6e7ba6074d9f`
- has_variant_id: yes
- distinct_variant_ids: 879401

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	quality_flag
    10	gene_id
    11	gene_symbol
    12	transcript_id
    13	consequence
    14	impact_class
    15	impact
    16	variant_class
    17	variant_type
    18	clinical_significance
    19	clinvar_significance
    20	population_frequency
    21	gnomad_af
    22	exac_af
    23	thousand_genomes_af
    24	mito_flag
    25	epilepsy_flag
```

First data row preview:
```text
ERR10619309	run_2026_06_02_181024	variant_annotation_pipeline	1:13550:G:A	1	13550	G	A	PASS	ENSG00000223972	DDX11L1	ENST00000450305.2	non_coding_transcript_exon_variant	MODIFIER	MODIFIER	SNV	non-coding	NA	NA	0.0034	0.0034	NA	0.0008	False	False

```

### Stage08 selected_transcript_consequences.tsv

- path: `results/run_2026_06_02_181024/processed/stage_08_selected_transcript_consequences.tsv`
- size_bytes: 296549215
- rows: 
- columns: 33
- header_sha256: `cd5a915c5bc9d15f76cda12616b5dae1e039ecb5f00164e46acc177e2d42a402`
- has_variant_id: yes
- distinct_variant_ids: 879401

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
```

First data row preview:
```text
ERR10619309	run_2026_06_02_181024	variant_annotation_pipeline	1:13550:G:A	1	13550	G	A	snv	noncoding	PASS	ENSG00000223972	DDX11L1	ENST00000450305.2	non_coding_transcript_exon_variant	MODIFIER	NA	NA	0.0034	0.0034	NA	0.0008	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	noncoding_transcript	MODIFIER	pass	needs_external_annotation	rare	missing

```

### Stage08 vdb_ready_variants.tsv

- path: `results/run_2026_06_02_181024/processed/stage_08_vdb_ready_variants.tsv`
- size_bytes: 296549215
- rows: 
- columns: 33
- header_sha256: `cd5a915c5bc9d15f76cda12616b5dae1e039ecb5f00164e46acc177e2d42a402`
- has_variant_id: yes
- distinct_variant_ids: 879401

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
```

First data row preview:
```text
ERR10619309	run_2026_06_02_181024	variant_annotation_pipeline	1:13550:G:A	1	13550	G	A	snv	noncoding	PASS	ENSG00000223972	DDX11L1	ENST00000450305.2	non_coding_transcript_exon_variant	MODIFIER	NA	NA	0.0034	0.0034	NA	0.0008	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	noncoding_transcript	MODIFIER	pass	needs_external_annotation	rare	missing

```

### Stage08 coding_candidates.tsv

- path: `results/run_2026_06_02_181024/processed/coding_candidates.tsv`
- size_bytes: 7698238
- rows: 
- columns: 33
- header_sha256: `cd5a915c5bc9d15f76cda12616b5dae1e039ecb5f00164e46acc177e2d42a402`
- has_variant_id: yes
- distinct_variant_ids: 23953

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
```

First data row preview:
```text
ERR10619309	run_2026_06_02_181024	variant_annotation_pipeline	1:924533:A:G	1	924533	A	G	snv	coding	PASS	ENSG00000187634	SAMD11	ENST00000616016.5	synonymous_variant	LOW	NA	NA	0.7498	0.7498	NA	0.4039	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	coding	LOW	pass	interpretable_now	common	missing

```

### Stage08 splice_region_candidates.tsv

- path: `results/run_2026_06_02_181024/processed/splice_region_candidates.tsv`
- size_bytes: 1102341
- rows: 
- columns: 33
- header_sha256: `cd5a915c5bc9d15f76cda12616b5dae1e039ecb5f00164e46acc177e2d42a402`
- has_variant_id: yes
- distinct_variant_ids: 2981

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
```

First data row preview:
```text
ERR10619309	run_2026_06_02_181024	variant_annotation_pipeline	1:1041950:T:C	1	1041950	T	C	snv	coding	PASS	ENSG00000188157	AGRN	ENST00000379370.7	splice_region_variant&splice_polypyrimidine_tract_variant&intron_variant	LOW	benign	benign	0.8852	0.8852	NA	0.6899	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	benign

```

### Stage08 noncoding_candidates.tsv

- path: `results/run_2026_06_02_181024/processed/noncoding_candidates.tsv`
- size_bytes: 287919555
- rows: 
- columns: 33
- header_sha256: `cd5a915c5bc9d15f76cda12616b5dae1e039ecb5f00164e46acc177e2d42a402`
- has_variant_id: yes
- distinct_variant_ids: 852953

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
```

First data row preview:
```text
ERR10619309	run_2026_06_02_181024	variant_annotation_pipeline	1:13550:G:A	1	13550	G	A	snv	noncoding	PASS	ENSG00000223972	DDX11L1	ENST00000450305.2	non_coding_transcript_exon_variant	MODIFIER	NA	NA	0.0034	0.0034	NA	0.0008	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	noncoding_transcript	MODIFIER	pass	needs_external_annotation	rare	missing

```

### Stage08 variant_summary.tsv

- path: `results/run_2026_06_02_181024/processed/stage_08_variant_summary.tsv`
- size_bytes: 223440678
- rows: 
- columns: 26
- header_sha256: `a0088e61e1ce409de45d1365b177ff47234ecb57dacab3ef0cb50fe3f613b55a`
- has_variant_id: yes
- distinct_variant_ids: 879401

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	gene_symbols
    10	gene_mapping_status
    11	worst_consequence
    12	highest_impact
    13	canonical_present
    14	coding_flag
    15	splice_flag
    16	noncoding_flag
    17	transcript_count
    18	variant_type
    19	variant_class
    20	quality_flag
    21	qc_status
    22	population_frequency
    23	frequency_status
    24	clinical_status
    25	annotation_source
    26	annotation_version
```

First data row preview:
```text
ERR10619309	run_2026_06_02_181024	variant_annotation_pipeline	10:100006504:T:C	10	100006504	T	C	DNMBP	mapped	intron_variant	MODIFIER	False	False	False	True	1	snv	noncoding	PASS	pass	0.2731	common	missing	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #

```

### Stage08 rdgp_gene_evidence_seed.tsv

- path: `results/run_2026_06_02_181024/processed/stage_08_rdgp_gene_evidence_seed.tsv`
- size_bytes: 14489354
- rows: 
- columns: 10
- header_sha256: `18d500222bcf3f2b99e044e14b9a1f0647d3f9bf1593555fa16359bb3996d3a3`
- has_variant_id: no
- distinct_variant_ids: NA

Header:
```text
     1	sample_id
     2	gene_id
     3	gene_symbol
     4	variant_count
     5	high_impact_variant_count
     6	rare_variant_count
     7	pathogenic_variant_count
     8	max_variant_severity
     9	has_low_quality_evidence
    10	contributing_variant_ids
```

First data row preview:
```text
ERR10619309	ENSG00000000003	TSPAN6	3	0	0	0	MODERATE	False	X:100624362:T:C,X:100632405:CA:C,X:100635207:C:T

```

### Stage09 coding_interpreted.tsv

- path: `results/run_2026_06_02_181024/processed/stage_09_coding_interpreted.tsv`
- size_bytes: 11259451
- rows: 
- columns: 43
- header_sha256: `8132a0aab15233fd27576c5624b2e8393fe622aa2bd651c8bdfc94c6215d5d3b`
- has_variant_id: yes
- distinct_variant_ids: 26448

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
    34	functional_impact
    35	rarity_flag
    36	clinical_evidence
    37	qc_reliability
    38	coding_interpretation_label
    39	is_lof_candidate
    40	is_rare_candidate
    41	is_clinically_supported
    42	is_high_quality
    43	is_potential_artifact
```

First data row preview:
```text
ERR10619309	run_2026_06_02_181024	variant_annotation_pipeline	1:924533:A:G	1	924533	A	G	snv	coding	PASS	ENSG00000187634	SAMD11	ENST00000616016.5	synonymous_variant	LOW	NA	NA	0.7498	0.7498	NA	0.4039	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	coding	LOW	pass	interpretable_now	common	missing	synonymous	common	missing	high_confidence	coding_common_or_low_support	False	False	False	True	False

```

### Stage10 noncoding_interpreted.tsv

- path: `results/run_2026_06_02_181024/processed/stage_10_noncoding_interpreted.tsv`
- size_bytes: 375842200
- rows: 
- columns: 43
- header_sha256: `52d4bd70320ef627d745025507d0b4bd3197d1fef0d1436811b20a6c4486c87e`
- has_variant_id: yes
- distinct_variant_ids: 852953

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
    34	noncoding_functional_context
    35	rarity_flag
    36	clinical_evidence
    37	qc_reliability
    38	noncoding_interpretation_label
    39	is_regulatory_candidate
    40	is_rare_candidate
    41	is_clinically_supported
    42	is_high_quality
    43	is_potential_artifact
```

First data row preview:
```text
ERR10619309	run_2026_06_02_181024	variant_annotation_pipeline	1:13550:G:A	1	13550	G	A	snv	noncoding	PASS	ENSG00000223972	DDX11L1	ENST00000450305.2	non_coding_transcript_exon_variant	MODIFIER	NA	NA	0.0034	0.0034	NA	0.0008	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	noncoding_transcript	MODIFIER	pass	needs_external_annotation	rare	missing	transcript_associated	rare	missing	high_confidence	regulatory_or_transcript_rare	False	True	False	True	False

```

### Stage11 prioritized_variants.tsv

- path: `results/run_2026_06_02_181024/processed/stage_11_prioritized_variants.tsv`
- size_bytes: 478371332
- rows: 
- columns: 52
- header_sha256: `446c7603e23bb60bb4da68196782174abe5aea562307628ddf55513a5e4bae54`
- has_variant_id: yes
- distinct_variant_ids: 879401

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
    34	functional_impact
    35	rarity_flag
    36	clinical_evidence
    37	qc_reliability
    38	coding_interpretation_label
    39	is_lof_candidate
    40	is_rare_candidate
    41	is_clinically_supported
    42	is_high_quality
    43	is_potential_artifact
    44	variant_origin
    45	source_interpretation_label
    46	priority_tier
    47	priority_rank
    48	priority_reason
    49	is_high_priority_candidate
    50	is_moderate_priority_candidate
    51	is_low_priority_candidate
    52	is_uninterpretable
```

First data row preview:
```text
ERR10619309	run_2026_06_02_181024	variant_annotation_pipeline	1:924533:A:G	1	924533	A	G	snv	coding	PASS	ENSG00000187634	SAMD11	ENST00000616016.5	synonymous_variant	LOW	NA	NA	0.7498	0.7498	NA	0.4039	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	coding	LOW	pass	interpretable_now	common	missing	synonymous	common	missing	high_confidence	coding_common_or_low_support	False	False	False	True	False	coding	coding_common_or_low_support	tier_3_low_support_or_common	3	coding label coding_common

```

### Stage11 gene_variant_counts.tsv

- path: `results/run_2026_06_02_181024/processed/stage_11_gene_variant_counts.tsv`
- size_bytes: 844803
- rows: 
- columns: 2
- header_sha256: `a728a2468d9a3e433005a28bf32c7a8a5cce42466215a1338be8933e0d5ade04`
- has_variant_id: no
- distinct_variant_ids: NA

Header:
```text
     1	gene_id
     2	variant_count
```

First data row preview:
```text
NA	145244

```

### Stage12 validation_candidates.tsv

- path: `results/run_2026_06_02_181024/processed/stage_12_validation_candidates.tsv`
- size_bytes: 518275544
- rows: 
- columns: 56
- header_sha256: `d43ee98c7824c468f1e6523d1886bf0d1164aa6e1003677f73093d557ac2d385`
- has_variant_id: yes
- distinct_variant_ids: 879401

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
    34	functional_impact
    35	rarity_flag
    36	clinical_evidence
    37	qc_reliability
    38	coding_interpretation_label
    39	is_lof_candidate
    40	is_rare_candidate
    41	is_clinically_supported
    42	is_high_quality
    43	is_potential_artifact
    44	variant_origin
    45	source_interpretation_label
    46	priority_tier
    47	priority_rank
    48	priority_reason
    49	is_high_priority_candidate
    50	is_moderate_priority_candidate
    51	is_low_priority_candidate
    52	is_uninterpretable
    53	validation_required
    54	validation_priority
    55	suggested_validation_method
    56	validation_reason
```

First data row preview:
```text
ERR10619309	run_2026_06_02_181024	variant_annotation_pipeline	1:924533:A:G	1	924533	A	G	snv	coding	PASS	ENSG00000187634	SAMD11	ENST00000616016.5	synonymous_variant	LOW	NA	NA	0.7498	0.7498	NA	0.4039	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	coding	LOW	pass	interpretable_now	common	missing	synonymous	common	missing	high_confidence	coding_common_or_low_support	False	False	False	True	False	coding	coding_common_or_low_support	tier_3_low_support_or_common	3	coding label coding_common

```

# Transition Lineage

### Stage07 annotated → Stage08 selected

| Metric | Stage07 annotated | Stage08 selected |
|---|---:|---:|
| rows |  |  |
| columns | 25 | 33 |
| distinct_variant_ids | 879401 | 879401 |

Removed columns:
```text
epilepsy_flag,impact
```

Added columns:
```text
annotation_source,annotation_version,clinical_status,epilepsy_flag,frequency_status,gene_mapping_status,interpretability_status,qc_status,variant_context,variant_effect_severity
```

Shared columns:
```text
alternate_allele,chromosome,clinical_significance,clinvar_significance,consequence,exac_af,gene_id,gene_symbol,gnomad_af,impact_class,mito_flag,population_frequency,position,quality_flag,reference_allele,run_id,sample_id,source_pipeline,thousand_genomes_af,transcript_id,variant_class,variant_id,variant_type
```

### Stage08 selected → Stage08 VDB-ready

| Metric | Stage08 selected | Stage08 VDB-ready |
|---|---:|---:|
| rows |  |  |
| columns | 33 | 33 |
| distinct_variant_ids | 879401 | 879401 |

Removed columns:
```text
NONE
```

Added columns:
```text
NONE
```

Shared columns:
```text
alternate_allele,annotation_source,annotation_version,chromosome,clinical_significance,clinical_status,clinvar_significance,consequence,epilepsy_flag,exac_af,frequency_status,gene_id,gene_mapping_status,gene_symbol,gnomad_af,impact_class,interpretability_status,mito_flag,population_frequency,position,qc_status,quality_flag,reference_allele,run_id,sample_id,source_pipeline,thousand_genomes_af,transcript_id,variant_class,variant_context,variant_effect_severity,variant_id,variant_type
```

### Stage08 VDB-ready → Stage09 coding interpreted

| Metric | Stage08 VDB-ready | Stage09 coding interpreted |
|---|---:|---:|
| rows |  |  |
| columns | 33 | 43 |
| distinct_variant_ids | 879401 | 26448 |

Removed columns:
```text
clinical_status
```

Added columns:
```text
clinical_evidence,clinical_status,coding_interpretation_label,functional_impact,is_clinically_supported,is_high_quality,is_lof_candidate,is_potential_artifact,is_rare_candidate,qc_reliability,rarity_flag
```

Shared columns:
```text
alternate_allele,annotation_source,annotation_version,chromosome,clinical_significance,clinvar_significance,consequence,epilepsy_flag,exac_af,frequency_status,gene_id,gene_mapping_status,gene_symbol,gnomad_af,impact_class,interpretability_status,mito_flag,population_frequency,position,qc_status,quality_flag,reference_allele,run_id,sample_id,source_pipeline,thousand_genomes_af,transcript_id,variant_class,variant_context,variant_effect_severity,variant_id,variant_type
```

### Stage08 VDB-ready → Stage10 noncoding interpreted

| Metric | Stage08 VDB-ready | Stage10 noncoding interpreted |
|---|---:|---:|
| rows |  |  |
| columns | 33 | 43 |
| distinct_variant_ids | 879401 | 852953 |

Removed columns:
```text
clinical_status
```

Added columns:
```text
clinical_evidence,clinical_status,is_clinically_supported,is_high_quality,is_potential_artifact,is_rare_candidate,is_regulatory_candidate,noncoding_functional_context,noncoding_interpretation_label,qc_reliability,rarity_flag
```

Shared columns:
```text
alternate_allele,annotation_source,annotation_version,chromosome,clinical_significance,clinvar_significance,consequence,epilepsy_flag,exac_af,frequency_status,gene_id,gene_mapping_status,gene_symbol,gnomad_af,impact_class,interpretability_status,mito_flag,population_frequency,position,qc_status,quality_flag,reference_allele,run_id,sample_id,source_pipeline,thousand_genomes_af,transcript_id,variant_class,variant_context,variant_effect_severity,variant_id,variant_type
```

### Stage09 coding interpreted → Stage11 prioritized

| Metric | Stage09 coding interpreted | Stage11 prioritized |
|---|---:|---:|
| rows |  |  |
| columns | 43 | 52 |
| distinct_variant_ids | 26448 | 879401 |

Removed columns:
```text
is_potential_artifact
```

Added columns:
```text
is_high_priority_candidate,is_low_priority_candidate,is_moderate_priority_candidate,is_potential_artifact,is_uninterpretable,priority_rank,priority_reason,priority_tier,source_interpretation_label,variant_origin
```

Shared columns:
```text
alternate_allele,annotation_source,annotation_version,chromosome,clinical_evidence,clinical_significance,clinical_status,clinvar_significance,coding_interpretation_label,consequence,epilepsy_flag,exac_af,frequency_status,functional_impact,gene_id,gene_mapping_status,gene_symbol,gnomad_af,impact_class,interpretability_status,is_clinically_supported,is_high_quality,is_lof_candidate,is_rare_candidate,mito_flag,population_frequency,position,qc_reliability,qc_status,quality_flag,rarity_flag,reference_allele,run_id,sample_id,source_pipeline,thousand_genomes_af,transcript_id,variant_class,variant_context,variant_effect_severity,variant_id,variant_type
```

### Stage10 noncoding interpreted → Stage11 prioritized

| Metric | Stage10 noncoding interpreted | Stage11 prioritized |
|---|---:|---:|
| rows |  |  |
| columns | 43 | 52 |
| distinct_variant_ids | 852953 | 879401 |

Removed columns:
```text
is_potential_artifact,is_regulatory_candidate,noncoding_functional_context,noncoding_interpretation_label
```

Added columns:
```text
coding_interpretation_label,functional_impact,is_high_priority_candidate,is_lof_candidate,is_low_priority_candidate,is_moderate_priority_candidate,is_potential_artifact,is_uninterpretable,priority_rank,priority_reason,priority_tier,source_interpretation_label,variant_origin
```

Shared columns:
```text
alternate_allele,annotation_source,annotation_version,chromosome,clinical_evidence,clinical_significance,clinical_status,clinvar_significance,consequence,epilepsy_flag,exac_af,frequency_status,gene_id,gene_mapping_status,gene_symbol,gnomad_af,impact_class,interpretability_status,is_clinically_supported,is_high_quality,is_rare_candidate,mito_flag,population_frequency,position,qc_reliability,qc_status,quality_flag,rarity_flag,reference_allele,run_id,sample_id,source_pipeline,thousand_genomes_af,transcript_id,variant_class,variant_context,variant_effect_severity,variant_id,variant_type
```

### Stage11 prioritized → Stage12 validation candidates

| Metric | Stage11 prioritized | Stage12 validation candidates |
|---|---:|---:|
| rows |  |  |
| columns | 52 | 56 |
| distinct_variant_ids | 879401 | 879401 |

Removed columns:
```text
is_uninterpretable
```

Added columns:
```text
is_uninterpretable,suggested_validation_method,validation_priority,validation_reason,validation_required
```

Shared columns:
```text
alternate_allele,annotation_source,annotation_version,chromosome,clinical_evidence,clinical_significance,clinical_status,clinvar_significance,coding_interpretation_label,consequence,epilepsy_flag,exac_af,frequency_status,functional_impact,gene_id,gene_mapping_status,gene_symbol,gnomad_af,impact_class,interpretability_status,is_clinically_supported,is_high_priority_candidate,is_high_quality,is_lof_candidate,is_low_priority_candidate,is_moderate_priority_candidate,is_potential_artifact,is_rare_candidate,mito_flag,population_frequency,position,priority_rank,priority_reason,priority_tier,qc_reliability,qc_status,quality_flag,rarity_flag,reference_allele,run_id,sample_id,source_interpretation_label,source_pipeline,thousand_genomes_af,transcript_id,variant_class,variant_context,variant_effect_severity,variant_id,variant_origin,variant_type
```

---

## ERR10619330 / run_2026_06_01_203130 / q1

# Artifact Inventory

### Stage07 annotated_variants.tsv

- path: `results/run_2026_06_01_203130/processed/ERR10619330_run_2026_06_01_203130.annotated_variants.tsv`
- size_bytes: 225644886
- rows: 
- columns: 25
- header_sha256: `617480c310358e0f764d2996153e3428ee6270702ce98194140c6e7ba6074d9f`
- has_variant_id: yes
- distinct_variant_ids: 963426

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	quality_flag
    10	gene_id
    11	gene_symbol
    12	transcript_id
    13	consequence
    14	impact_class
    15	impact
    16	variant_class
    17	variant_type
    18	clinical_significance
    19	clinvar_significance
    20	population_frequency
    21	gnomad_af
    22	exac_af
    23	thousand_genomes_af
    24	mito_flag
    25	epilepsy_flag
```

First data row preview:
```text
ERR10619330	run_2026_06_01_203130	variant_annotation_pipeline	1:13418:G:A	1	13418	G	A	PASS	ENSG00000223972	DDX11L1	ENST00000450305.2	intron_variant&non_coding_transcript_variant	MODIFIER	MODIFIER	SNV	non-coding	NA	NA	0.2087	0.2087	NA	NA	False	False

```

### Stage08 selected_transcript_consequences.tsv

- path: `results/run_2026_06_01_203130/processed/stage_08_selected_transcript_consequences.tsv`
- size_bytes: 324783912
- rows: 
- columns: 33
- header_sha256: `cd5a915c5bc9d15f76cda12616b5dae1e039ecb5f00164e46acc177e2d42a402`
- has_variant_id: yes
- distinct_variant_ids: 963426

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
```

First data row preview:
```text
ERR10619330	run_2026_06_01_203130	variant_annotation_pipeline	1:13418:G:A	1	13418	G	A	snv	noncoding	PASS	ENSG00000223972	DDX11L1	ENST00000450305.2	intron_variant&non_coding_transcript_variant	MODIFIER	NA	NA	0.2087	0.2087	NA	NA	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	intronic	MODIFIER	pass	needs_external_annotation	common	missing

```

### Stage08 vdb_ready_variants.tsv

- path: `results/run_2026_06_01_203130/processed/stage_08_vdb_ready_variants.tsv`
- size_bytes: 324783912
- rows: 
- columns: 33
- header_sha256: `cd5a915c5bc9d15f76cda12616b5dae1e039ecb5f00164e46acc177e2d42a402`
- has_variant_id: yes
- distinct_variant_ids: 963426

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
```

First data row preview:
```text
ERR10619330	run_2026_06_01_203130	variant_annotation_pipeline	1:13418:G:A	1	13418	G	A	snv	noncoding	PASS	ENSG00000223972	DDX11L1	ENST00000450305.2	intron_variant&non_coding_transcript_variant	MODIFIER	NA	NA	0.2087	0.2087	NA	NA	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	intronic	MODIFIER	pass	needs_external_annotation	common	missing

```

### Stage08 coding_candidates.tsv

- path: `results/run_2026_06_01_203130/processed/coding_candidates.tsv`
- size_bytes: 7893405
- rows: 
- columns: 33
- header_sha256: `cd5a915c5bc9d15f76cda12616b5dae1e039ecb5f00164e46acc177e2d42a402`
- has_variant_id: yes
- distinct_variant_ids: 24563

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
```

First data row preview:
```text
ERR10619330	run_2026_06_01_203130	variant_annotation_pipeline	1:924533:A:G	1	924533	A	G	snv	coding	PASS	ENSG00000187634	SAMD11	ENST00000616016.5	synonymous_variant	LOW	NA	NA	0.7498	0.7498	NA	0.4039	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	coding	LOW	pass	interpretable_now	common	missing

```

### Stage08 splice_region_candidates.tsv

- path: `results/run_2026_06_01_203130/processed/splice_region_candidates.tsv`
- size_bytes: 1132468
- rows: 
- columns: 33
- header_sha256: `cd5a915c5bc9d15f76cda12616b5dae1e039ecb5f00164e46acc177e2d42a402`
- has_variant_id: yes
- distinct_variant_ids: 3058

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
```

First data row preview:
```text
ERR10619330	run_2026_06_01_203130	variant_annotation_pipeline	1:182597:G:A	1	182597	G	A	snv	coding	PASS	ENSG00000310527	WASH9P	ENST00000831131.1	splice_region_variant&splice_polypyrimidine_tract_variant&intron_variant&non_coding_transcript_variant	LOW	NA	NA	0.03696	0.03696	NA	NA	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	low_frequency	missing

```

### Stage08 noncoding_candidates.tsv

- path: `results/run_2026_06_01_203130/processed/noncoding_candidates.tsv`
- size_bytes: 315930699
- rows: 
- columns: 33
- header_sha256: `cd5a915c5bc9d15f76cda12616b5dae1e039ecb5f00164e46acc177e2d42a402`
- has_variant_id: yes
- distinct_variant_ids: 936295

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
```

First data row preview:
```text
ERR10619330	run_2026_06_01_203130	variant_annotation_pipeline	1:13418:G:A	1	13418	G	A	snv	noncoding	PASS	ENSG00000223972	DDX11L1	ENST00000450305.2	intron_variant&non_coding_transcript_variant	MODIFIER	NA	NA	0.2087	0.2087	NA	NA	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	intronic	MODIFIER	pass	needs_external_annotation	common	missing

```

### Stage08 variant_summary.tsv

- path: `results/run_2026_06_01_203130/processed/stage_08_variant_summary.tsv`
- size_bytes: 244796875
- rows: 
- columns: 26
- header_sha256: `a0088e61e1ce409de45d1365b177ff47234ecb57dacab3ef0cb50fe3f613b55a`
- has_variant_id: yes
- distinct_variant_ids: 963426

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	gene_symbols
    10	gene_mapping_status
    11	worst_consequence
    12	highest_impact
    13	canonical_present
    14	coding_flag
    15	splice_flag
    16	noncoding_flag
    17	transcript_count
    18	variant_type
    19	variant_class
    20	quality_flag
    21	qc_status
    22	population_frequency
    23	frequency_status
    24	clinical_status
    25	annotation_source
    26	annotation_version
```

First data row preview:
```text
ERR10619330	run_2026_06_01_203130	variant_annotation_pipeline	10:100005358:G:C	10	100005358	G	C	DNMBP	mapped	intron_variant	MODIFIER	False	False	False	True	1	snv	noncoding	PASS	pass	0.2234	common	missing	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #

```

### Stage08 rdgp_gene_evidence_seed.tsv

- path: `results/run_2026_06_01_203130/processed/stage_08_rdgp_gene_evidence_seed.tsv`
- size_bytes: 15579881
- rows: 
- columns: 10
- header_sha256: `18d500222bcf3f2b99e044e14b9a1f0647d3f9bf1593555fa16359bb3996d3a3`
- has_variant_id: no
- distinct_variant_ids: NA

Header:
```text
     1	sample_id
     2	gene_id
     3	gene_symbol
     4	variant_count
     5	high_impact_variant_count
     6	rare_variant_count
     7	pathogenic_variant_count
     8	max_variant_severity
     9	has_low_quality_evidence
    10	contributing_variant_ids
```

First data row preview:
```text
ERR10619330	ENSG00000000003	TSPAN6	2	0	0	0	MODIFIER	False	X:100624362:T:C,X:100631833:T:C

```

### Stage09 coding_interpreted.tsv

- path: `results/run_2026_06_01_203130/processed/stage_09_coding_interpreted.tsv`
- size_bytes: 11551273
- rows: 
- columns: 43
- header_sha256: `8132a0aab15233fd27576c5624b2e8393fe622aa2bd651c8bdfc94c6215d5d3b`
- has_variant_id: yes
- distinct_variant_ids: 27131

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
    34	functional_impact
    35	rarity_flag
    36	clinical_evidence
    37	qc_reliability
    38	coding_interpretation_label
    39	is_lof_candidate
    40	is_rare_candidate
    41	is_clinically_supported
    42	is_high_quality
    43	is_potential_artifact
```

First data row preview:
```text
ERR10619330	run_2026_06_01_203130	variant_annotation_pipeline	1:924533:A:G	1	924533	A	G	snv	coding	PASS	ENSG00000187634	SAMD11	ENST00000616016.5	synonymous_variant	LOW	NA	NA	0.7498	0.7498	NA	0.4039	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	coding	LOW	pass	interpretable_now	common	missing	synonymous	common	missing	high_confidence	coding_common_or_low_support	False	False	False	True	False

```

### Stage10 noncoding_interpreted.tsv

- path: `results/run_2026_06_01_203130/processed/stage_10_noncoding_interpreted.tsv`
- size_bytes: 412498128
- rows: 
- columns: 43
- header_sha256: `52d4bd70320ef627d745025507d0b4bd3197d1fef0d1436811b20a6c4486c87e`
- has_variant_id: yes
- distinct_variant_ids: 936295

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
    34	noncoding_functional_context
    35	rarity_flag
    36	clinical_evidence
    37	qc_reliability
    38	noncoding_interpretation_label
    39	is_regulatory_candidate
    40	is_rare_candidate
    41	is_clinically_supported
    42	is_high_quality
    43	is_potential_artifact
```

First data row preview:
```text
ERR10619330	run_2026_06_01_203130	variant_annotation_pipeline	1:13418:G:A	1	13418	G	A	snv	noncoding	PASS	ENSG00000223972	DDX11L1	ENST00000450305.2	intron_variant&non_coding_transcript_variant	MODIFIER	NA	NA	0.2087	0.2087	NA	NA	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	intronic	MODIFIER	pass	needs_external_annotation	common	missing	transcript_associated	common	missing	high_confidence	noncoding_common_or_low_support	False	False	False	True	False

```

### Stage11 prioritized_variants.tsv

- path: `results/run_2026_06_01_203130/processed/stage_11_prioritized_variants.tsv`
- size_bytes: 523935173
- rows: 
- columns: 52
- header_sha256: `446c7603e23bb60bb4da68196782174abe5aea562307628ddf55513a5e4bae54`
- has_variant_id: yes
- distinct_variant_ids: 963426

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
    34	functional_impact
    35	rarity_flag
    36	clinical_evidence
    37	qc_reliability
    38	coding_interpretation_label
    39	is_lof_candidate
    40	is_rare_candidate
    41	is_clinically_supported
    42	is_high_quality
    43	is_potential_artifact
    44	variant_origin
    45	source_interpretation_label
    46	priority_tier
    47	priority_rank
    48	priority_reason
    49	is_high_priority_candidate
    50	is_moderate_priority_candidate
    51	is_low_priority_candidate
    52	is_uninterpretable
```

First data row preview:
```text
ERR10619330	run_2026_06_01_203130	variant_annotation_pipeline	1:924533:A:G	1	924533	A	G	snv	coding	PASS	ENSG00000187634	SAMD11	ENST00000616016.5	synonymous_variant	LOW	NA	NA	0.7498	0.7498	NA	0.4039	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	coding	LOW	pass	interpretable_now	common	missing	synonymous	common	missing	high_confidence	coding_common_or_low_support	False	False	False	True	False	coding	coding_common_or_low_support	tier_3_low_support_or_common	3	coding label coding_common

```

### Stage11 gene_variant_counts.tsv

- path: `results/run_2026_06_01_203130/processed/stage_11_gene_variant_counts.tsv`
- size_bytes: 857193
- rows: 
- columns: 2
- header_sha256: `a728a2468d9a3e433005a28bf32c7a8a5cce42466215a1338be8933e0d5ade04`
- has_variant_id: no
- distinct_variant_ids: NA

Header:
```text
     1	gene_id
     2	variant_count
```

First data row preview:
```text
NA	162498

```

### Stage12 validation_candidates.tsv

- path: `results/run_2026_06_01_203130/processed/stage_12_validation_candidates.tsv`
- size_bytes: 567676081
- rows: 
- columns: 56
- header_sha256: `d43ee98c7824c468f1e6523d1886bf0d1164aa6e1003677f73093d557ac2d385`
- has_variant_id: yes
- distinct_variant_ids: 963426

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
    34	functional_impact
    35	rarity_flag
    36	clinical_evidence
    37	qc_reliability
    38	coding_interpretation_label
    39	is_lof_candidate
    40	is_rare_candidate
    41	is_clinically_supported
    42	is_high_quality
    43	is_potential_artifact
    44	variant_origin
    45	source_interpretation_label
    46	priority_tier
    47	priority_rank
    48	priority_reason
    49	is_high_priority_candidate
    50	is_moderate_priority_candidate
    51	is_low_priority_candidate
    52	is_uninterpretable
    53	validation_required
    54	validation_priority
    55	suggested_validation_method
    56	validation_reason
```

First data row preview:
```text
ERR10619330	run_2026_06_01_203130	variant_annotation_pipeline	1:924533:A:G	1	924533	A	G	snv	coding	PASS	ENSG00000187634	SAMD11	ENST00000616016.5	synonymous_variant	LOW	NA	NA	0.7498	0.7498	NA	0.4039	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	coding	LOW	pass	interpretable_now	common	missing	synonymous	common	missing	high_confidence	coding_common_or_low_support	False	False	False	True	False	coding	coding_common_or_low_support	tier_3_low_support_or_common	3	coding label coding_common

```

# Transition Lineage

### Stage07 annotated → Stage08 selected

| Metric | Stage07 annotated | Stage08 selected |
|---|---:|---:|
| rows |  |  |
| columns | 25 | 33 |
| distinct_variant_ids | 963426 | 963426 |

Removed columns:
```text
epilepsy_flag,impact
```

Added columns:
```text
annotation_source,annotation_version,clinical_status,epilepsy_flag,frequency_status,gene_mapping_status,interpretability_status,qc_status,variant_context,variant_effect_severity
```

Shared columns:
```text
alternate_allele,chromosome,clinical_significance,clinvar_significance,consequence,exac_af,gene_id,gene_symbol,gnomad_af,impact_class,mito_flag,population_frequency,position,quality_flag,reference_allele,run_id,sample_id,source_pipeline,thousand_genomes_af,transcript_id,variant_class,variant_id,variant_type
```

### Stage08 selected → Stage08 VDB-ready

| Metric | Stage08 selected | Stage08 VDB-ready |
|---|---:|---:|
| rows |  |  |
| columns | 33 | 33 |
| distinct_variant_ids | 963426 | 963426 |

Removed columns:
```text
NONE
```

Added columns:
```text
NONE
```

Shared columns:
```text
alternate_allele,annotation_source,annotation_version,chromosome,clinical_significance,clinical_status,clinvar_significance,consequence,epilepsy_flag,exac_af,frequency_status,gene_id,gene_mapping_status,gene_symbol,gnomad_af,impact_class,interpretability_status,mito_flag,population_frequency,position,qc_status,quality_flag,reference_allele,run_id,sample_id,source_pipeline,thousand_genomes_af,transcript_id,variant_class,variant_context,variant_effect_severity,variant_id,variant_type
```

### Stage08 VDB-ready → Stage09 coding interpreted

| Metric | Stage08 VDB-ready | Stage09 coding interpreted |
|---|---:|---:|
| rows |  |  |
| columns | 33 | 43 |
| distinct_variant_ids | 963426 | 27131 |

Removed columns:
```text
clinical_status
```

Added columns:
```text
clinical_evidence,clinical_status,coding_interpretation_label,functional_impact,is_clinically_supported,is_high_quality,is_lof_candidate,is_potential_artifact,is_rare_candidate,qc_reliability,rarity_flag
```

Shared columns:
```text
alternate_allele,annotation_source,annotation_version,chromosome,clinical_significance,clinvar_significance,consequence,epilepsy_flag,exac_af,frequency_status,gene_id,gene_mapping_status,gene_symbol,gnomad_af,impact_class,interpretability_status,mito_flag,population_frequency,position,qc_status,quality_flag,reference_allele,run_id,sample_id,source_pipeline,thousand_genomes_af,transcript_id,variant_class,variant_context,variant_effect_severity,variant_id,variant_type
```

### Stage08 VDB-ready → Stage10 noncoding interpreted

| Metric | Stage08 VDB-ready | Stage10 noncoding interpreted |
|---|---:|---:|
| rows |  |  |
| columns | 33 | 43 |
| distinct_variant_ids | 963426 | 936295 |

Removed columns:
```text
clinical_status
```

Added columns:
```text
clinical_evidence,clinical_status,is_clinically_supported,is_high_quality,is_potential_artifact,is_rare_candidate,is_regulatory_candidate,noncoding_functional_context,noncoding_interpretation_label,qc_reliability,rarity_flag
```

Shared columns:
```text
alternate_allele,annotation_source,annotation_version,chromosome,clinical_significance,clinvar_significance,consequence,epilepsy_flag,exac_af,frequency_status,gene_id,gene_mapping_status,gene_symbol,gnomad_af,impact_class,interpretability_status,mito_flag,population_frequency,position,qc_status,quality_flag,reference_allele,run_id,sample_id,source_pipeline,thousand_genomes_af,transcript_id,variant_class,variant_context,variant_effect_severity,variant_id,variant_type
```

### Stage09 coding interpreted → Stage11 prioritized

| Metric | Stage09 coding interpreted | Stage11 prioritized |
|---|---:|---:|
| rows |  |  |
| columns | 43 | 52 |
| distinct_variant_ids | 27131 | 963426 |

Removed columns:
```text
is_potential_artifact
```

Added columns:
```text
is_high_priority_candidate,is_low_priority_candidate,is_moderate_priority_candidate,is_potential_artifact,is_uninterpretable,priority_rank,priority_reason,priority_tier,source_interpretation_label,variant_origin
```

Shared columns:
```text
alternate_allele,annotation_source,annotation_version,chromosome,clinical_evidence,clinical_significance,clinical_status,clinvar_significance,coding_interpretation_label,consequence,epilepsy_flag,exac_af,frequency_status,functional_impact,gene_id,gene_mapping_status,gene_symbol,gnomad_af,impact_class,interpretability_status,is_clinically_supported,is_high_quality,is_lof_candidate,is_rare_candidate,mito_flag,population_frequency,position,qc_reliability,qc_status,quality_flag,rarity_flag,reference_allele,run_id,sample_id,source_pipeline,thousand_genomes_af,transcript_id,variant_class,variant_context,variant_effect_severity,variant_id,variant_type
```

### Stage10 noncoding interpreted → Stage11 prioritized

| Metric | Stage10 noncoding interpreted | Stage11 prioritized |
|---|---:|---:|
| rows |  |  |
| columns | 43 | 52 |
| distinct_variant_ids | 936295 | 963426 |

Removed columns:
```text
is_potential_artifact,is_regulatory_candidate,noncoding_functional_context,noncoding_interpretation_label
```

Added columns:
```text
coding_interpretation_label,functional_impact,is_high_priority_candidate,is_lof_candidate,is_low_priority_candidate,is_moderate_priority_candidate,is_potential_artifact,is_uninterpretable,priority_rank,priority_reason,priority_tier,source_interpretation_label,variant_origin
```

Shared columns:
```text
alternate_allele,annotation_source,annotation_version,chromosome,clinical_evidence,clinical_significance,clinical_status,clinvar_significance,consequence,epilepsy_flag,exac_af,frequency_status,gene_id,gene_mapping_status,gene_symbol,gnomad_af,impact_class,interpretability_status,is_clinically_supported,is_high_quality,is_rare_candidate,mito_flag,population_frequency,position,qc_reliability,qc_status,quality_flag,rarity_flag,reference_allele,run_id,sample_id,source_pipeline,thousand_genomes_af,transcript_id,variant_class,variant_context,variant_effect_severity,variant_id,variant_type
```

### Stage11 prioritized → Stage12 validation candidates

| Metric | Stage11 prioritized | Stage12 validation candidates |
|---|---:|---:|
| rows |  |  |
| columns | 52 | 56 |
| distinct_variant_ids | 963426 | 963426 |

Removed columns:
```text
is_uninterpretable
```

Added columns:
```text
is_uninterpretable,suggested_validation_method,validation_priority,validation_reason,validation_required
```

Shared columns:
```text
alternate_allele,annotation_source,annotation_version,chromosome,clinical_evidence,clinical_significance,clinical_status,clinvar_significance,coding_interpretation_label,consequence,epilepsy_flag,exac_af,frequency_status,functional_impact,gene_id,gene_mapping_status,gene_symbol,gnomad_af,impact_class,interpretability_status,is_clinically_supported,is_high_priority_candidate,is_high_quality,is_lof_candidate,is_low_priority_candidate,is_moderate_priority_candidate,is_potential_artifact,is_rare_candidate,mito_flag,population_frequency,position,priority_rank,priority_reason,priority_tier,qc_reliability,qc_status,quality_flag,rarity_flag,reference_allele,run_id,sample_id,source_interpretation_label,source_pipeline,thousand_genomes_af,transcript_id,variant_class,variant_context,variant_effect_severity,variant_id,variant_origin,variant_type
```

---

## hg002 / run_2026_06_03_010030 / hg002

# Artifact Inventory

### Stage07 annotated_variants.tsv

- path: `results/run_2026_06_03_010030/processed/HG002_run_2026_06_03_010030.annotated_variants.tsv`
- size_bytes: 1053663787
- rows: 
- columns: 25
- header_sha256: `617480c310358e0f764d2996153e3428ee6270702ce98194140c6e7ba6074d9f`
- has_variant_id: yes
- distinct_variant_ids: 4636584

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	quality_flag
    10	gene_id
    11	gene_symbol
    12	transcript_id
    13	consequence
    14	impact_class
    15	impact
    16	variant_class
    17	variant_type
    18	clinical_significance
    19	clinvar_significance
    20	population_frequency
    21	gnomad_af
    22	exac_af
    23	thousand_genomes_af
    24	mito_flag
    25	epilepsy_flag
```

First data row preview:
```text
HG002	run_2026_06_03_010030	variant_annotation_pipeline	1:14522:G:A	1	14522	G	A	PASS	ENSG00000310526	WASH7P	ENST00000831140.1	non_coding_transcript_exon_variant	MODIFIER	MODIFIER	SNV	non-coding	NA	NA	0.1893	0.1893	NA	NA	False	False

```

### Stage08 selected_transcript_consequences.tsv

- path: `results/run_2026_06_03_010030/processed/stage_08_selected_transcript_consequences.tsv`
- size_bytes: 1532561623
- rows: 
- columns: 33
- header_sha256: `cd5a915c5bc9d15f76cda12616b5dae1e039ecb5f00164e46acc177e2d42a402`
- has_variant_id: yes
- distinct_variant_ids: 4636584

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
```

First data row preview:
```text
HG002	run_2026_06_03_010030	variant_annotation_pipeline	1:14522:G:A	1	14522	G	A	snv	noncoding	PASS	ENSG00000310526	WASH7P	ENST00000831140.1	non_coding_transcript_exon_variant	MODIFIER	NA	NA	0.1893	0.1893	NA	NA	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	noncoding_transcript	MODIFIER	pass	needs_external_annotation	common	missing

```

### Stage08 vdb_ready_variants.tsv

- path: `results/run_2026_06_03_010030/processed/stage_08_vdb_ready_variants.tsv`
- size_bytes: 1532561623
- rows: 
- columns: 33
- header_sha256: `cd5a915c5bc9d15f76cda12616b5dae1e039ecb5f00164e46acc177e2d42a402`
- has_variant_id: yes
- distinct_variant_ids: 4636584

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
```

First data row preview:
```text
HG002	run_2026_06_03_010030	variant_annotation_pipeline	1:14522:G:A	1	14522	G	A	snv	noncoding	PASS	ENSG00000310526	WASH7P	ENST00000831140.1	non_coding_transcript_exon_variant	MODIFIER	NA	NA	0.1893	0.1893	NA	NA	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	noncoding_transcript	MODIFIER	pass	needs_external_annotation	common	missing

```

### Stage08 coding_candidates.tsv

- path: `results/run_2026_06_03_010030/processed/coding_candidates.tsv`
- size_bytes: 7654401
- rows: 
- columns: 33
- header_sha256: `cd5a915c5bc9d15f76cda12616b5dae1e039ecb5f00164e46acc177e2d42a402`
- has_variant_id: yes
- distinct_variant_ids: 24278

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
```

First data row preview:
```text
HG002	run_2026_06_03_010030	variant_annotation_pipeline	1:924533:A:G	1	924533	A	G	snv	coding	PASS	ENSG00000187634	SAMD11	ENST00000616016.5	synonymous_variant	LOW	NA	NA	0.7498	0.7498	NA	0.4039	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	coding	LOW	pass	interpretable_now	common	missing

```

### Stage08 splice_region_candidates.tsv

- path: `results/run_2026_06_03_010030/processed/splice_region_candidates.tsv`
- size_bytes: 1357199
- rows: 
- columns: 33
- header_sha256: `cd5a915c5bc9d15f76cda12616b5dae1e039ecb5f00164e46acc177e2d42a402`
- has_variant_id: yes
- distinct_variant_ids: 3733

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
```

First data row preview:
```text
HG002	run_2026_06_03_010030	variant_annotation_pipeline	1:1041950:T:C	1	1041950	T	C	snv	coding	PASS	ENSG00000188157	AGRN	ENST00000379370.7	splice_region_variant&splice_polypyrimidine_tract_variant&intron_variant	LOW	benign	benign	0.8852	0.8852	NA	0.6899	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	benign

```

### Stage08 noncoding_candidates.tsv

- path: `results/run_2026_06_03_010030/processed/noncoding_candidates.tsv`
- size_bytes: 1523731924
- rows: 
- columns: 33
- header_sha256: `cd5a915c5bc9d15f76cda12616b5dae1e039ecb5f00164e46acc177e2d42a402`
- has_variant_id: yes
- distinct_variant_ids: 4609098

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
```

First data row preview:
```text
HG002	run_2026_06_03_010030	variant_annotation_pipeline	1:14522:G:A	1	14522	G	A	snv	noncoding	PASS	ENSG00000310526	WASH7P	ENST00000831140.1	non_coding_transcript_exon_variant	MODIFIER	NA	NA	0.1893	0.1893	NA	NA	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	noncoding_transcript	MODIFIER	pass	needs_external_annotation	common	missing

```

### Stage08 variant_summary.tsv

- path: `results/run_2026_06_03_010030/processed/stage_08_variant_summary.tsv`
- size_bytes: 1155807098
- rows: 
- columns: 26
- header_sha256: `a0088e61e1ce409de45d1365b177ff47234ecb57dacab3ef0cb50fe3f613b55a`
- has_variant_id: yes
- distinct_variant_ids: 4636584

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	gene_symbols
    10	gene_mapping_status
    11	worst_consequence
    12	highest_impact
    13	canonical_present
    14	coding_flag
    15	splice_flag
    16	noncoding_flag
    17	transcript_count
    18	variant_type
    19	variant_class
    20	quality_flag
    21	qc_status
    22	population_frequency
    23	frequency_status
    24	clinical_status
    25	annotation_source
    26	annotation_version
```

First data row preview:
```text
HG002	run_2026_06_03_010030	variant_annotation_pipeline	10:100000235:C:T	10	100000235	C	T	DNMBP	mapped	intron_variant	MODIFIER	False	False	False	True	1	snv	noncoding	PASS	pass	0.3094	common	missing	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #

```

### Stage08 rdgp_gene_evidence_seed.tsv

- path: `results/run_2026_06_03_010030/processed/stage_08_rdgp_gene_evidence_seed.tsv`
- size_bytes: 60237527
- rows: 
- columns: 10
- header_sha256: `18d500222bcf3f2b99e044e14b9a1f0647d3f9bf1593555fa16359bb3996d3a3`
- has_variant_id: no
- distinct_variant_ids: NA

Header:
```text
     1	sample_id
     2	gene_id
     3	gene_symbol
     4	variant_count
     5	high_impact_variant_count
     6	rare_variant_count
     7	pathogenic_variant_count
     8	max_variant_severity
     9	has_low_quality_evidence
    10	contributing_variant_ids
```

First data row preview:
```text
HG002	ENSG00000000003	TSPAN6	4	0	1	0	MODIFIER	True	X:100626986:T:C,X:100626987:G:T,X:100629536:GC:G,X:100636869:G:A

```

### Stage09 coding_interpreted.tsv

- path: `results/run_2026_06_03_010030/processed/stage_09_coding_interpreted.tsv`
- size_bytes: 11562281
- rows: 
- columns: 43
- header_sha256: `8132a0aab15233fd27576c5624b2e8393fe622aa2bd651c8bdfc94c6215d5d3b`
- has_variant_id: yes
- distinct_variant_ids: 27486

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
    34	functional_impact
    35	rarity_flag
    36	clinical_evidence
    37	qc_reliability
    38	coding_interpretation_label
    39	is_lof_candidate
    40	is_rare_candidate
    41	is_clinically_supported
    42	is_high_quality
    43	is_potential_artifact
```

First data row preview:
```text
HG002	run_2026_06_03_010030	variant_annotation_pipeline	1:924533:A:G	1	924533	A	G	snv	coding	PASS	ENSG00000187634	SAMD11	ENST00000616016.5	synonymous_variant	LOW	NA	NA	0.7498	0.7498	NA	0.4039	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	coding	LOW	pass	interpretable_now	common	missing	synonymous	common	missing	high_confidence	coding_common_or_low_support	False	False	False	True	False

```

### Stage10 noncoding_interpreted.tsv

- path: `results/run_2026_06_03_010030/processed/stage_10_noncoding_interpreted.tsv`
- size_bytes: 2001072770
- rows: 
- columns: 43
- header_sha256: `52d4bd70320ef627d745025507d0b4bd3197d1fef0d1436811b20a6c4486c87e`
- has_variant_id: yes
- distinct_variant_ids: 4609098

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
    34	noncoding_functional_context
    35	rarity_flag
    36	clinical_evidence
    37	qc_reliability
    38	noncoding_interpretation_label
    39	is_regulatory_candidate
    40	is_rare_candidate
    41	is_clinically_supported
    42	is_high_quality
    43	is_potential_artifact
```

First data row preview:
```text
HG002	run_2026_06_03_010030	variant_annotation_pipeline	1:14522:G:A	1	14522	G	A	snv	noncoding	PASS	ENSG00000310526	WASH7P	ENST00000831140.1	non_coding_transcript_exon_variant	MODIFIER	NA	NA	0.1893	0.1893	NA	NA	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	noncoding_transcript	MODIFIER	pass	needs_external_annotation	common	missing	transcript_associated	common	missing	high_confidence	noncoding_common_or_low_support	False	False	False	True	False

```

### Stage11 prioritized_variants.tsv

- path: `results/run_2026_06_03_010030/processed/stage_11_prioritized_variants.tsv`
- size_bytes: 2488077748
- rows: 
- columns: 52
- header_sha256: `446c7603e23bb60bb4da68196782174abe5aea562307628ddf55513a5e4bae54`
- has_variant_id: yes
- distinct_variant_ids: 4636584

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
    34	functional_impact
    35	rarity_flag
    36	clinical_evidence
    37	qc_reliability
    38	coding_interpretation_label
    39	is_lof_candidate
    40	is_rare_candidate
    41	is_clinically_supported
    42	is_high_quality
    43	is_potential_artifact
    44	variant_origin
    45	source_interpretation_label
    46	priority_tier
    47	priority_rank
    48	priority_reason
    49	is_high_priority_candidate
    50	is_moderate_priority_candidate
    51	is_low_priority_candidate
    52	is_uninterpretable
```

First data row preview:
```text
HG002	run_2026_06_03_010030	variant_annotation_pipeline	1:924533:A:G	1	924533	A	G	snv	coding	PASS	ENSG00000187634	SAMD11	ENST00000616016.5	synonymous_variant	LOW	NA	NA	0.7498	0.7498	NA	0.4039	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	coding	LOW	pass	interpretable_now	common	missing	synonymous	common	missing	high_confidence	coding_common_or_low_support	False	False	False	True	False	coding	coding_common_or_low_support	tier_3_low_support_or_common	3	coding label coding_common_or_lo

```

### Stage11 gene_variant_counts.tsv

- path: `results/run_2026_06_03_010030/processed/stage_11_gene_variant_counts.tsv`
- size_bytes: 998494
- rows: 
- columns: 2
- header_sha256: `a728a2468d9a3e433005a28bf32c7a8a5cce42466215a1338be8933e0d5ade04`
- has_variant_id: no
- distinct_variant_ids: NA

Header:
```text
     1	gene_id
     2	variant_count
```

First data row preview:
```text
NA	1107793

```

### Stage12 validation_candidates.tsv

- path: `results/run_2026_06_03_010030/processed/stage_12_validation_candidates.tsv`
- size_bytes: 2701088532
- rows: 
- columns: 56
- header_sha256: `d43ee98c7824c468f1e6523d1886bf0d1164aa6e1003677f73093d557ac2d385`
- has_variant_id: yes
- distinct_variant_ids: 4636584

Header:
```text
     1	sample_id
     2	run_id
     3	source_pipeline
     4	variant_id
     5	chromosome
     6	position
     7	reference_allele
     8	alternate_allele
     9	variant_type
    10	variant_class
    11	quality_flag
    12	gene_id
    13	gene_symbol
    14	transcript_id
    15	consequence
    16	impact_class
    17	clinical_significance
    18	clinvar_significance
    19	population_frequency
    20	gnomad_af
    21	exac_af
    22	thousand_genomes_af
    23	mito_flag
    24	epilepsy_flag
    25	annotation_source
    26	annotation_version
    27	gene_mapping_status
    28	variant_context
    29	variant_effect_severity
    30	qc_status
    31	interpretability_status
    32	frequency_status
    33	clinical_status
    34	functional_impact
    35	rarity_flag
    36	clinical_evidence
    37	qc_reliability
    38	coding_interpretation_label
    39	is_lof_candidate
    40	is_rare_candidate
    41	is_clinically_supported
    42	is_high_quality
    43	is_potential_artifact
    44	variant_origin
    45	source_interpretation_label
    46	priority_tier
    47	priority_rank
    48	priority_reason
    49	is_high_priority_candidate
    50	is_moderate_priority_candidate
    51	is_low_priority_candidate
    52	is_uninterpretable
    53	validation_required
    54	validation_priority
    55	suggested_validation_method
    56	validation_reason
```

First data row preview:
```text
HG002	run_2026_06_03_010030	variant_annotation_pipeline	1:924533:A:G	1	924533	A	G	snv	coding	PASS	ENSG00000187634	SAMD11	ENST00000616016.5	synonymous_variant	LOW	NA	NA	0.7498	0.7498	NA	0.4039	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	coding	LOW	pass	interpretable_now	common	missing	synonymous	common	missing	high_confidence	coding_common_or_low_support	False	False	False	True	False	coding	coding_common_or_low_support	tier_3_low_support_or_common	3	coding label coding_common_or_lo

```

# Transition Lineage

### Stage07 annotated → Stage08 selected

| Metric | Stage07 annotated | Stage08 selected |
|---|---:|---:|
| rows |  |  |
| columns | 25 | 33 |
| distinct_variant_ids | 4636584 | 4636584 |

Removed columns:
```text
epilepsy_flag,impact
```

Added columns:
```text
annotation_source,annotation_version,clinical_status,epilepsy_flag,frequency_status,gene_mapping_status,interpretability_status,qc_status,variant_context,variant_effect_severity
```

Shared columns:
```text
alternate_allele,chromosome,clinical_significance,clinvar_significance,consequence,exac_af,gene_id,gene_symbol,gnomad_af,impact_class,mito_flag,population_frequency,position,quality_flag,reference_allele,run_id,sample_id,source_pipeline,thousand_genomes_af,transcript_id,variant_class,variant_id,variant_type
```

### Stage08 selected → Stage08 VDB-ready

| Metric | Stage08 selected | Stage08 VDB-ready |
|---|---:|---:|
| rows |  |  |
| columns | 33 | 33 |
| distinct_variant_ids | 4636584 | 4636584 |

Removed columns:
```text
NONE
```

Added columns:
```text
NONE
```

Shared columns:
```text
alternate_allele,annotation_source,annotation_version,chromosome,clinical_significance,clinical_status,clinvar_significance,consequence,epilepsy_flag,exac_af,frequency_status,gene_id,gene_mapping_status,gene_symbol,gnomad_af,impact_class,interpretability_status,mito_flag,population_frequency,position,qc_status,quality_flag,reference_allele,run_id,sample_id,source_pipeline,thousand_genomes_af,transcript_id,variant_class,variant_context,variant_effect_severity,variant_id,variant_type
```

### Stage08 VDB-ready → Stage09 coding interpreted

| Metric | Stage08 VDB-ready | Stage09 coding interpreted |
|---|---:|---:|
| rows |  |  |
| columns | 33 | 43 |
| distinct_variant_ids | 4636584 | 27486 |

Removed columns:
```text
clinical_status
```

Added columns:
```text
clinical_evidence,clinical_status,coding_interpretation_label,functional_impact,is_clinically_supported,is_high_quality,is_lof_candidate,is_potential_artifact,is_rare_candidate,qc_reliability,rarity_flag
```

Shared columns:
```text
alternate_allele,annotation_source,annotation_version,chromosome,clinical_significance,clinvar_significance,consequence,epilepsy_flag,exac_af,frequency_status,gene_id,gene_mapping_status,gene_symbol,gnomad_af,impact_class,interpretability_status,mito_flag,population_frequency,position,qc_status,quality_flag,reference_allele,run_id,sample_id,source_pipeline,thousand_genomes_af,transcript_id,variant_class,variant_context,variant_effect_severity,variant_id,variant_type
```

### Stage08 VDB-ready → Stage10 noncoding interpreted

| Metric | Stage08 VDB-ready | Stage10 noncoding interpreted |
|---|---:|---:|
| rows |  |  |
| columns | 33 | 43 |
| distinct_variant_ids | 4636584 | 4609098 |

Removed columns:
```text
clinical_status
```

Added columns:
```text
clinical_evidence,clinical_status,is_clinically_supported,is_high_quality,is_potential_artifact,is_rare_candidate,is_regulatory_candidate,noncoding_functional_context,noncoding_interpretation_label,qc_reliability,rarity_flag
```

Shared columns:
```text
alternate_allele,annotation_source,annotation_version,chromosome,clinical_significance,clinvar_significance,consequence,epilepsy_flag,exac_af,frequency_status,gene_id,gene_mapping_status,gene_symbol,gnomad_af,impact_class,interpretability_status,mito_flag,population_frequency,position,qc_status,quality_flag,reference_allele,run_id,sample_id,source_pipeline,thousand_genomes_af,transcript_id,variant_class,variant_context,variant_effect_severity,variant_id,variant_type
```

### Stage09 coding interpreted → Stage11 prioritized

| Metric | Stage09 coding interpreted | Stage11 prioritized |
|---|---:|---:|
| rows |  |  |
| columns | 43 | 52 |
| distinct_variant_ids | 27486 | 4636584 |

Removed columns:
```text
is_potential_artifact
```

Added columns:
```text
is_high_priority_candidate,is_low_priority_candidate,is_moderate_priority_candidate,is_potential_artifact,is_uninterpretable,priority_rank,priority_reason,priority_tier,source_interpretation_label,variant_origin
```

Shared columns:
```text
alternate_allele,annotation_source,annotation_version,chromosome,clinical_evidence,clinical_significance,clinical_status,clinvar_significance,coding_interpretation_label,consequence,epilepsy_flag,exac_af,frequency_status,functional_impact,gene_id,gene_mapping_status,gene_symbol,gnomad_af,impact_class,interpretability_status,is_clinically_supported,is_high_quality,is_lof_candidate,is_rare_candidate,mito_flag,population_frequency,position,qc_reliability,qc_status,quality_flag,rarity_flag,reference_allele,run_id,sample_id,source_pipeline,thousand_genomes_af,transcript_id,variant_class,variant_context,variant_effect_severity,variant_id,variant_type
```

### Stage10 noncoding interpreted → Stage11 prioritized

| Metric | Stage10 noncoding interpreted | Stage11 prioritized |
|---|---:|---:|
| rows |  |  |
| columns | 43 | 52 |
| distinct_variant_ids | 4609098 | 4636584 |

Removed columns:
```text
is_potential_artifact,is_regulatory_candidate,noncoding_functional_context,noncoding_interpretation_label
```

Added columns:
```text
coding_interpretation_label,functional_impact,is_high_priority_candidate,is_lof_candidate,is_low_priority_candidate,is_moderate_priority_candidate,is_potential_artifact,is_uninterpretable,priority_rank,priority_reason,priority_tier,source_interpretation_label,variant_origin
```

Shared columns:
```text
alternate_allele,annotation_source,annotation_version,chromosome,clinical_evidence,clinical_significance,clinical_status,clinvar_significance,consequence,epilepsy_flag,exac_af,frequency_status,gene_id,gene_mapping_status,gene_symbol,gnomad_af,impact_class,interpretability_status,is_clinically_supported,is_high_quality,is_rare_candidate,mito_flag,population_frequency,position,qc_reliability,qc_status,quality_flag,rarity_flag,reference_allele,run_id,sample_id,source_pipeline,thousand_genomes_af,transcript_id,variant_class,variant_context,variant_effect_severity,variant_id,variant_type
```

### Stage11 prioritized → Stage12 validation candidates

| Metric | Stage11 prioritized | Stage12 validation candidates |
|---|---:|---:|
| rows |  |  |
| columns | 52 | 56 |
| distinct_variant_ids | 4636584 | 4636584 |

Removed columns:
```text
is_uninterpretable
```

Added columns:
```text
is_uninterpretable,suggested_validation_method,validation_priority,validation_reason,validation_required
```

Shared columns:
```text
alternate_allele,annotation_source,annotation_version,chromosome,clinical_evidence,clinical_significance,clinical_status,clinvar_significance,coding_interpretation_label,consequence,epilepsy_flag,exac_af,frequency_status,functional_impact,gene_id,gene_mapping_status,gene_symbol,gnomad_af,impact_class,interpretability_status,is_clinically_supported,is_high_priority_candidate,is_high_quality,is_lof_candidate,is_low_priority_candidate,is_moderate_priority_candidate,is_potential_artifact,is_rare_candidate,mito_flag,population_frequency,position,priority_rank,priority_reason,priority_tier,qc_reliability,qc_status,quality_flag,rarity_flag,reference_allele,run_id,sample_id,source_interpretation_label,source_pipeline,thousand_genomes_af,transcript_id,variant_class,variant_context,variant_effect_severity,variant_id,variant_origin,variant_type
```

---

# Cross-Run Column First Appearance Map

Generated from all available audited artifacts.

| column | observed_surfaces |
|---|---|
| alternate_allele | stage07,stage08_coding,stage08_noncoding,stage08_selected,stage08_splice,stage08_variant_summary,stage08_vdb,stage09,stage10,stage11,stage12 |
| annotation_source | stage08_coding,stage08_noncoding,stage08_selected,stage08_splice,stage08_variant_summary,stage08_vdb,stage09,stage10,stage11,stage12 |
| annotation_version | stage08_coding,stage08_noncoding,stage08_selected,stage08_splice,stage08_vdb,stage09,stage10,stage11,stage12 |
| annotation_version | stage08_variant_summary |
| canonical_present | stage08_variant_summary |
| chromosome | stage07,stage08_coding,stage08_noncoding,stage08_selected,stage08_splice,stage08_variant_summary,stage08_vdb,stage09,stage10,stage11,stage12 |
| clinical_evidence | stage09,stage10,stage11,stage12 |
| clinical_significance | stage07,stage08_coding,stage08_noncoding,stage08_selected,stage08_splice,stage08_vdb,stage09,stage10,stage11,stage12 |
| clinical_status | stage08_variant_summary,stage09,stage10,stage11,stage12 |
| clinical_status | stage08_coding,stage08_noncoding,stage08_selected,stage08_splice,stage08_vdb |
| clinvar_significance | stage07,stage08_coding,stage08_noncoding,stage08_selected,stage08_splice,stage08_vdb,stage09,stage10,stage11,stage12 |
| coding_flag | stage08_variant_summary |
| coding_interpretation_label | stage09,stage11,stage12 |
| consequence | stage07,stage08_coding,stage08_noncoding,stage08_selected,stage08_splice,stage08_vdb,stage09,stage10,stage11,stage12 |
| contributing_variant_ids | stage08_rdgp_seed |
| epilepsy_flag | stage08_coding,stage08_noncoding,stage08_selected,stage08_splice,stage08_vdb,stage09,stage10,stage11,stage12 |
| epilepsy_flag | stage07 |
| exac_af | stage07,stage08_coding,stage08_noncoding,stage08_selected,stage08_splice,stage08_vdb,stage09,stage10,stage11,stage12 |
| frequency_status | stage08_coding,stage08_noncoding,stage08_selected,stage08_splice,stage08_variant_summary,stage08_vdb,stage09,stage10,stage11,stage12 |
| functional_impact | stage09,stage11,stage12 |
| gene_id | stage07,stage08_coding,stage08_noncoding,stage08_rdgp_seed,stage08_selected,stage08_splice,stage08_vdb,stage09,stage10,stage11,stage11_gene_counts,stage12 |
| gene_mapping_status | stage08_coding,stage08_noncoding,stage08_selected,stage08_splice,stage08_variant_summary,stage08_vdb,stage09,stage10,stage11,stage12 |
| gene_symbol | stage07,stage08_coding,stage08_noncoding,stage08_rdgp_seed,stage08_selected,stage08_splice,stage08_vdb,stage09,stage10,stage11,stage12 |
| gene_symbols | stage08_variant_summary |
| gnomad_af | stage07,stage08_coding,stage08_noncoding,stage08_selected,stage08_splice,stage08_vdb,stage09,stage10,stage11,stage12 |
| has_low_quality_evidence | stage08_rdgp_seed |
| highest_impact | stage08_variant_summary |
| high_impact_variant_count | stage08_rdgp_seed |
| impact | stage07 |
| impact_class | stage07,stage08_coding,stage08_noncoding,stage08_selected,stage08_splice,stage08_vdb,stage09,stage10,stage11,stage12 |
| interpretability_status | stage08_coding,stage08_noncoding,stage08_selected,stage08_splice,stage08_vdb,stage09,stage10,stage11,stage12 |
| is_clinically_supported | stage09,stage10,stage11,stage12 |
| is_high_priority_candidate | stage11,stage12 |
| is_high_quality | stage09,stage10,stage11,stage12 |
| is_lof_candidate | stage09,stage11,stage12 |
| is_low_priority_candidate | stage11,stage12 |
| is_moderate_priority_candidate | stage11,stage12 |
| is_potential_artifact | stage11,stage12 |
| is_potential_artifact | stage09,stage10 |
| is_rare_candidate | stage09,stage10,stage11,stage12 |
| is_regulatory_candidate | stage10 |
| is_uninterpretable | stage12 |
| is_uninterpretable | stage11 |
| max_variant_severity | stage08_rdgp_seed |
| mito_flag | stage07,stage08_coding,stage08_noncoding,stage08_selected,stage08_splice,stage08_vdb,stage09,stage10,stage11,stage12 |
| noncoding_flag | stage08_variant_summary |
| noncoding_functional_context | stage10 |
| noncoding_interpretation_label | stage10 |
| pathogenic_variant_count | stage08_rdgp_seed |
| population_frequency | stage07,stage08_coding,stage08_noncoding,stage08_selected,stage08_splice,stage08_variant_summary,stage08_vdb,stage09,stage10,stage11,stage12 |
| position | stage07,stage08_coding,stage08_noncoding,stage08_selected,stage08_splice,stage08_variant_summary,stage08_vdb,stage09,stage10,stage11,stage12 |
| priority_rank | stage11,stage12 |
| priority_reason | stage11,stage12 |
| priority_tier | stage11,stage12 |
| qc_reliability | stage09,stage10,stage11,stage12 |
| qc_status | stage08_coding,stage08_noncoding,stage08_selected,stage08_splice,stage08_variant_summary,stage08_vdb,stage09,stage10,stage11,stage12 |
| quality_flag | stage07,stage08_coding,stage08_noncoding,stage08_selected,stage08_splice,stage08_variant_summary,stage08_vdb,stage09,stage10,stage11,stage12 |
| rare_variant_count | stage08_rdgp_seed |
| rarity_flag | stage09,stage10,stage11,stage12 |
| reference_allele | stage07,stage08_coding,stage08_noncoding,stage08_selected,stage08_splice,stage08_variant_summary,stage08_vdb,stage09,stage10,stage11,stage12 |
| run_id | stage07,stage08_coding,stage08_noncoding,stage08_selected,stage08_splice,stage08_variant_summary,stage08_vdb,stage09,stage10,stage11,stage12 |
| sample_id | stage07,stage08_coding,stage08_noncoding,stage08_rdgp_seed,stage08_selected,stage08_splice,stage08_variant_summary,stage08_vdb,stage09,stage10,stage11,stage12 |
| source_interpretation_label | stage11,stage12 |
| source_pipeline | stage07,stage08_coding,stage08_noncoding,stage08_selected,stage08_splice,stage08_variant_summary,stage08_vdb,stage09,stage10,stage11,stage12 |
| splice_flag | stage08_variant_summary |
| suggested_validation_method | stage12 |
| thousand_genomes_af | stage07,stage08_coding,stage08_noncoding,stage08_selected,stage08_splice,stage08_vdb,stage09,stage10,stage11,stage12 |
| transcript_count | stage08_variant_summary |
| transcript_id | stage07,stage08_coding,stage08_noncoding,stage08_selected,stage08_splice,stage08_vdb,stage09,stage10,stage11,stage12 |
| validation_priority | stage12 |
| validation_reason | stage12 |
| validation_required | stage12 |
| variant_class | stage07,stage08_coding,stage08_noncoding,stage08_selected,stage08_splice,stage08_variant_summary,stage08_vdb,stage09,stage10,stage11,stage12 |
| variant_context | stage08_coding,stage08_noncoding,stage08_selected,stage08_splice,stage08_vdb,stage09,stage10,stage11,stage12 |
| variant_count | stage08_rdgp_seed |
| variant_count | stage11_gene_counts |
| variant_effect_severity | stage08_coding,stage08_noncoding,stage08_selected,stage08_splice,stage08_vdb,stage09,stage10,stage11,stage12 |
| variant_id | stage07,stage08_coding,stage08_noncoding,stage08_selected,stage08_splice,stage08_variant_summary,stage08_vdb,stage09,stage10,stage11,stage12 |
| variant_origin | stage11,stage12 |
| variant_type | stage07,stage08_coding,stage08_noncoding,stage08_selected,stage08_splice,stage08_variant_summary,stage08_vdb,stage09,stage10,stage11,stage12 |
| worst_consequence | stage08_variant_summary |
