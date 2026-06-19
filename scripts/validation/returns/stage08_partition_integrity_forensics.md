# Stage08 Partition Integrity Forensics

Generated: 2026-06-17T22:11:42Z

Question:

```text
Does coding_candidates + splice_region_candidates + noncoding_candidates exactly reconstruct Stage08?
```

## run_2026_05_30_071639

### Files

Stage08: `results/run_2026_05_30_071639/processed/stage_08_vdb_ready_variants.tsv`
Coding partition: `results/run_2026_05_30_071639/processed/coding_candidates.tsv`
Splice partition: `results/run_2026_05_30_071639/processed/splice_region_candidates.tsv`
Noncoding partition: `results/run_2026_05_30_071639/processed/noncoding_candidates.tsv`

### Partition Row Accounting

| Metric | Count | Percent of Stage08 |
|---|---:|---:|
| Stage08 rows |  | 100.000000 |
| Coding rows |  | NA |
| Splice-region rows |  | NA |
| Noncoding rows |  | NA |
| Coding + splice + noncoding | 0 | NA |
| Delta: Stage08 - partitions | 0 | NA |

**Row accounting result:** Perfect row reconstruction.

### Variant-ID Set Accounting

| Metric | Count |
|---|---:|
| Stage08 distinct variant_ids | 674593 |
| Union partition distinct variant_ids | 674593 |
| Variant_ids appearing in more than one partition | 465 |
| Stage08 ids absent from partitions | 0 |
| Partition ids absent from Stage08 | 0 |

**Set accounting result:** Partition union exactly reconstructs Stage08 variant_id set.

### Stage09 / Stage10 Downstream Check

- stage_09_coding_interpreted rows: 
- expected coding + splice rows: 0
- expected - observed delta: 0
- stage_10_noncoding_interpreted rows: 
- expected noncoding rows: 
- expected - observed delta: 0

### First Row Previews

Coding:
ERR10619203	run_2026_05_30_071639	variant_annotation_pipeline	1:69270:A:G	1	69270	A	G	snv	coding	PASS	ENSG00000186092	OR4F5	ENST00000641515.2	synonymous_variant	LOW	NA	NA	0.9961	0.9961	NA	NA	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	coding	LOW	pass	interpretable_now	common	missing

Splice-region:
ERR10619203	run_2026_05_30_071639	variant_annotation_pipeline	1:17375:A:G	1	17375	A	G	snv	coding	PASS	ENSG00000227232	WASH7P	ENST00000488147.2	splice_region_variant&splice_polypyrimidine_tract_variant&intron_variant&non_coding_transcript_variant	LOW	NA	NA	0.009963	0.009963	NA	NA	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	rare	missing

Noncoding:
ERR10619203	run_2026_05_30_071639	variant_annotation_pipeline	1:14542:A:G	1	14542	A	G	snv	noncoding	PASS	ENSG00000310526	WASH7P	ENST00000831140.1	non_coding_transcript_exon_variant	MODIFIER	NA	NA	0.3406	0.3406	NA	NA	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	noncoding_transcript	MODIFIER	pass	needs_external_annotation	common	missing

---

## run_2026_06_01_124134

### Files

Stage08: `results/run_2026_06_01_124134/processed/stage_08_vdb_ready_variants.tsv`
Coding partition: `results/run_2026_06_01_124134/processed/coding_candidates.tsv`
Splice partition: `results/run_2026_06_01_124134/processed/splice_region_candidates.tsv`
Noncoding partition: `results/run_2026_06_01_124134/processed/noncoding_candidates.tsv`

### Partition Row Accounting

| Metric | Count | Percent of Stage08 |
|---|---:|---:|
| Stage08 rows |  | 100.000000 |
| Coding rows |  | NA |
| Splice-region rows |  | NA |
| Noncoding rows |  | NA |
| Coding + splice + noncoding | 0 | NA |
| Delta: Stage08 - partitions | 0 | NA |

**Row accounting result:** Perfect row reconstruction.

### Variant-ID Set Accounting

| Metric | Count |
|---|---:|
| Stage08 distinct variant_ids | 678379 |
| Union partition distinct variant_ids | 678379 |
| Variant_ids appearing in more than one partition | 493 |
| Stage08 ids absent from partitions | 0 |
| Partition ids absent from Stage08 | 0 |

**Set accounting result:** Partition union exactly reconstructs Stage08 variant_id set.

### Stage09 / Stage10 Downstream Check

- stage_09_coding_interpreted rows: 
- expected coding + splice rows: 0
- expected - observed delta: 0
- stage_10_noncoding_interpreted rows: 
- expected noncoding rows: 
- expected - observed delta: 0

### First Row Previews

Coding:
ERR10619207	run_2026_06_01_124134	variant_annotation_pipeline	1:946247:G:A	1	946247	G	A	snv	coding	PASS	ENSG00000188976	NOC2L	ENST00000327044.7	synonymous_variant	LOW	NA	NA	0.4419	0.4419	NA	0.0643	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	coding	LOW	pass	interpretable_now	common	missing

Splice-region:
ERR10619207	run_2026_06_01_124134	variant_annotation_pipeline	1:16856:A:G	1	16856	A	G	snv	coding	PASS	ENSG00000310526	WASH7P	ENST00000831140.1	splice_donor_variant&non_coding_transcript_variant	HIGH	NA	NA	0.02175	0.02175	NA	NA	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	HIGH	pass	interpretable_now	low_frequency	missing

Noncoding:
ERR10619207	run_2026_06_01_124134	variant_annotation_pipeline	1:13649:G:C	1	13649	G	C	snv	noncoding	PASS	ENSG00000223972	DDX11L1	ENST00000450305.2	non_coding_transcript_exon_variant	MODIFIER	NA	NA	0.2367	0.2367	NA	NA	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	noncoding_transcript	MODIFIER	pass	needs_external_annotation	common	missing

---

## run_2026_05_30_151355

### Files

Stage08: `results/run_2026_05_30_151355/processed/stage_08_vdb_ready_variants.tsv`
Coding partition: `results/run_2026_05_30_151355/processed/coding_candidates.tsv`
Splice partition: `results/run_2026_05_30_151355/processed/splice_region_candidates.tsv`
Noncoding partition: `results/run_2026_05_30_151355/processed/noncoding_candidates.tsv`

### Partition Row Accounting

| Metric | Count | Percent of Stage08 |
|---|---:|---:|
| Stage08 rows |  | 100.000000 |
| Coding rows |  | NA |
| Splice-region rows |  | NA |
| Noncoding rows |  | NA |
| Coding + splice + noncoding | 0 | NA |
| Delta: Stage08 - partitions | 0 | NA |

**Row accounting result:** Perfect row reconstruction.

### Variant-ID Set Accounting

| Metric | Count |
|---|---:|
| Stage08 distinct variant_ids | 849399 |
| Union partition distinct variant_ids | 849399 |
| Variant_ids appearing in more than one partition | 540 |
| Stage08 ids absent from partitions | 0 |
| Partition ids absent from Stage08 | 0 |

**Set accounting result:** Partition union exactly reconstructs Stage08 variant_id set.

### Stage09 / Stage10 Downstream Check

- stage_09_coding_interpreted rows: 
- expected coding + splice rows: 0
- expected - observed delta: 0
- stage_10_noncoding_interpreted rows: 
- expected noncoding rows: 
- expected - observed delta: 0

### First Row Previews

Coding:
ERR10619208	run_2026_05_30_151355	variant_annotation_pipeline	1:924533:A:G	1	924533	A	G	snv	coding	PASS	ENSG00000187634	SAMD11	ENST00000616016.5	synonymous_variant	LOW	NA	NA	0.7498	0.7498	NA	0.4039	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	coding	LOW	pass	interpretable_now	common	missing

Splice-region:
ERR10619208	run_2026_05_30_151355	variant_annotation_pipeline	1:962350:C:T	1	962350	C	T	snv	coding	PASS	ENSG00000187961	KLHL17	ENST00000338591.8	splice_region_variant&splice_polypyrimidine_tract_variant&intron_variant	LOW	NA	NA	0.1747	0.0775	NA	0.1747	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	missing

Noncoding:
ERR10619208	run_2026_05_30_151355	variant_annotation_pipeline	1:13813:T:G	1	13813	T	G	snv	noncoding	PASS	ENSG00000290825	DDX11L16	ENST00000832823.1	upstream_gene_variant	MODIFIER	NA	NA	0.4861	0.4861	NA	NA	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	regulatory	MODIFIER	pass	needs_external_annotation	common	missing

---

## run_2026_05_30_214724

### Files

Stage08: `results/run_2026_05_30_214724/processed/stage_08_vdb_ready_variants.tsv`
Coding partition: `results/run_2026_05_30_214724/processed/coding_candidates.tsv`
Splice partition: `results/run_2026_05_30_214724/processed/splice_region_candidates.tsv`
Noncoding partition: `results/run_2026_05_30_214724/processed/noncoding_candidates.tsv`

### Partition Row Accounting

| Metric | Count | Percent of Stage08 |
|---|---:|---:|
| Stage08 rows |  | 100.000000 |
| Coding rows |  | NA |
| Splice-region rows |  | NA |
| Noncoding rows |  | NA |
| Coding + splice + noncoding | 0 | NA |
| Delta: Stage08 - partitions | 0 | NA |

**Row accounting result:** Perfect row reconstruction.

### Variant-ID Set Accounting

| Metric | Count |
|---|---:|
| Stage08 distinct variant_ids | 905517 |
| Union partition distinct variant_ids | 905517 |
| Variant_ids appearing in more than one partition | 541 |
| Stage08 ids absent from partitions | 0 |
| Partition ids absent from Stage08 | 0 |

**Set accounting result:** Partition union exactly reconstructs Stage08 variant_id set.

### Stage09 / Stage10 Downstream Check

- stage_09_coding_interpreted rows: 
- expected coding + splice rows: 0
- expected - observed delta: 0
- stage_10_noncoding_interpreted rows: 
- expected noncoding rows: 
- expected - observed delta: 0

### First Row Previews

Coding:
ERR10619212	run_2026_05_30_214724	variant_annotation_pipeline	1:924533:A:G	1	924533	A	G	snv	coding	PASS	ENSG00000187634	SAMD11	ENST00000616016.5	synonymous_variant	LOW	NA	NA	0.7498	0.7498	NA	0.4039	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	coding	LOW	pass	interpretable_now	common	missing

Splice-region:
ERR10619212	run_2026_05_30_214724	variant_annotation_pipeline	1:17746:A:G	1	17746	A	G	snv	coding	PASS	ENSG00000310526	WASH7P	ENST00000831140.1	splice_region_variant&splice_polypyrimidine_tract_variant&intron_variant&non_coding_transcript_variant	LOW	NA	NA	0.1499	0.1499	NA	NA	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	missing

Noncoding:
ERR10619212	run_2026_05_30_214724	variant_annotation_pipeline	1:13649:G:C	1	13649	G	C	snv	noncoding	PASS	ENSG00000223972	DDX11L1	ENST00000450305.2	non_coding_transcript_exon_variant	MODIFIER	NA	NA	0.2367	0.2367	NA	NA	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	noncoding_transcript	MODIFIER	pass	needs_external_annotation	common	missing

---

## run_2026_05_31_091242

### Files

Stage08: `results/run_2026_05_31_091242/processed/stage_08_vdb_ready_variants.tsv`
Coding partition: `results/run_2026_05_31_091242/processed/coding_candidates.tsv`
Splice partition: `results/run_2026_05_31_091242/processed/splice_region_candidates.tsv`
Noncoding partition: `results/run_2026_05_31_091242/processed/noncoding_candidates.tsv`

### Partition Row Accounting

| Metric | Count | Percent of Stage08 |
|---|---:|---:|
| Stage08 rows |  | 100.000000 |
| Coding rows |  | NA |
| Splice-region rows |  | NA |
| Noncoding rows |  | NA |
| Coding + splice + noncoding | 0 | NA |
| Delta: Stage08 - partitions | 0 | NA |

**Row accounting result:** Perfect row reconstruction.

### Variant-ID Set Accounting

| Metric | Count |
|---|---:|
| Stage08 distinct variant_ids | 757635 |
| Union partition distinct variant_ids | 757635 |
| Variant_ids appearing in more than one partition | 541 |
| Stage08 ids absent from partitions | 0 |
| Partition ids absent from Stage08 | 0 |

**Set accounting result:** Partition union exactly reconstructs Stage08 variant_id set.

### Stage09 / Stage10 Downstream Check

- stage_09_coding_interpreted rows: 
- expected coding + splice rows: 0
- expected - observed delta: 0
- stage_10_noncoding_interpreted rows: 
- expected noncoding rows: 
- expected - observed delta: 0

### First Row Previews

Coding:
ERR10619225	run_2026_05_31_091242	variant_annotation_pipeline	1:924533:A:G	1	924533	A	G	snv	coding	PASS	ENSG00000187634	SAMD11	ENST00000616016.5	synonymous_variant	LOW	NA	NA	0.7498	0.7498	NA	0.4039	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	coding	LOW	pass	interpretable_now	common	missing

Splice-region:
ERR10619225	run_2026_05_31_091242	variant_annotation_pipeline	1:15045:C:T	1	15045	C	T	snv	coding	PASS	ENSG00000310526	WASH7P	ENST00000831140.1	splice_region_variant&splice_polypyrimidine_tract_variant&intron_variant&non_coding_transcript_variant	LOW	NA	NA	0.4369	0.4369	NA	NA	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	missing

Noncoding:
ERR10619225	run_2026_05_31_091242	variant_annotation_pipeline	1:10439:AC:A	1	10439	AC	A	deletion	noncoding	PASS	ENSG00000223972	DDX11L1	ENST00000450305.2	upstream_gene_variant	MODIFIER	NA	NA	0.4031	0.4031	NA	NA	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	regulatory	MODIFIER	pass	needs_external_annotation	common	missing

---

## run_2026_06_01_004903

### Files

Stage08: `results/run_2026_06_01_004903/processed/stage_08_vdb_ready_variants.tsv`
Coding partition: `results/run_2026_06_01_004903/processed/coding_candidates.tsv`
Splice partition: `results/run_2026_06_01_004903/processed/splice_region_candidates.tsv`
Noncoding partition: `results/run_2026_06_01_004903/processed/noncoding_candidates.tsv`

### Partition Row Accounting

| Metric | Count | Percent of Stage08 |
|---|---:|---:|
| Stage08 rows |  | 100.000000 |
| Coding rows |  | NA |
| Splice-region rows |  | NA |
| Noncoding rows |  | NA |
| Coding + splice + noncoding | 0 | NA |
| Delta: Stage08 - partitions | 0 | NA |

**Row accounting result:** Perfect row reconstruction.

### Variant-ID Set Accounting

| Metric | Count |
|---|---:|
| Stage08 distinct variant_ids | 681054 |
| Union partition distinct variant_ids | 681054 |
| Variant_ids appearing in more than one partition | 497 |
| Stage08 ids absent from partitions | 0 |
| Partition ids absent from Stage08 | 0 |

**Set accounting result:** Partition union exactly reconstructs Stage08 variant_id set.

### Stage09 / Stage10 Downstream Check

- stage_09_coding_interpreted rows: 
- expected coding + splice rows: 0
- expected - observed delta: 0
- stage_10_noncoding_interpreted rows: 
- expected noncoding rows: 
- expected - observed delta: 0

### First Row Previews

Coding:
ERR10619230	run_2026_06_01_004903	variant_annotation_pipeline	1:924533:A:G	1	924533	A	G	snv	coding	PASS	ENSG00000187634	SAMD11	ENST00000616016.5	synonymous_variant	LOW	NA	NA	0.7498	0.7498	NA	0.4039	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	coding	LOW	pass	interpretable_now	common	missing

Splice-region:
ERR10619230	run_2026_06_01_004903	variant_annotation_pipeline	1:1041950:T:C	1	1041950	T	C	snv	coding	PASS	ENSG00000188157	AGRN	ENST00000379370.7	splice_region_variant&splice_polypyrimidine_tract_variant&intron_variant	LOW	benign	benign	0.8852	0.8852	NA	0.6899	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	benign

Noncoding:
ERR10619230	run_2026_06_01_004903	variant_annotation_pipeline	1:13273:G:C	1	13273	G	C	snv	noncoding	PASS	ENSG00000223972	DDX11L1	ENST00000450305.2	non_coding_transcript_exon_variant	MODIFIER	NA	NA	0.095	0.0950	NA	0.0204	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	noncoding_transcript	MODIFIER	pass	needs_external_annotation	common	missing

---

## run_2026_06_02_052302

### Files

Stage08: `results/run_2026_06_02_052302/processed/stage_08_vdb_ready_variants.tsv`
Coding partition: `results/run_2026_06_02_052302/processed/coding_candidates.tsv`
Splice partition: `results/run_2026_06_02_052302/processed/splice_region_candidates.tsv`
Noncoding partition: `results/run_2026_06_02_052302/processed/noncoding_candidates.tsv`

### Partition Row Accounting

| Metric | Count | Percent of Stage08 |
|---|---:|---:|
| Stage08 rows |  | 100.000000 |
| Coding rows |  | NA |
| Splice-region rows |  | NA |
| Noncoding rows |  | NA |
| Coding + splice + noncoding | 0 | NA |
| Delta: Stage08 - partitions | 0 | NA |

**Row accounting result:** Perfect row reconstruction.

### Variant-ID Set Accounting

| Metric | Count |
|---|---:|
| Stage08 distinct variant_ids | 909698 |
| Union partition distinct variant_ids | 909698 |
| Variant_ids appearing in more than one partition | 495 |
| Stage08 ids absent from partitions | 0 |
| Partition ids absent from Stage08 | 0 |

**Set accounting result:** Partition union exactly reconstructs Stage08 variant_id set.

### Stage09 / Stage10 Downstream Check

- stage_09_coding_interpreted rows: 
- expected coding + splice rows: 0
- expected - observed delta: 0
- stage_10_noncoding_interpreted rows: 
- expected noncoding rows: 
- expected - observed delta: 0

### First Row Previews

Coding:
ERR10619241	run_2026_06_02_052302	variant_annotation_pipeline	1:69270:A:G	1	69270	A	G	snv	coding	PASS	ENSG00000186092	OR4F5	ENST00000641515.2	synonymous_variant	LOW	NA	NA	0.9961	0.9961	NA	NA	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	coding	LOW	pass	interpretable_now	common	missing

Splice-region:
ERR10619241	run_2026_06_02_052302	variant_annotation_pipeline	1:847806:G:C	1	847806	G	C	snv	coding	PASS	ENSG00000228794	LINC01128	ENST00000666741.3	splice_region_variant&non_coding_transcript_exon_variant	LOW	NA	NA	0.0144	0.0040	NA	0.0144	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	low_frequency	missing

Noncoding:
ERR10619241	run_2026_06_02_052302	variant_annotation_pipeline	1:13012:G:C	1	13012	G	C	snv	noncoding	PASS	ENSG00000223972	DDX11L1	ENST00000450305.2	non_coding_transcript_exon_variant	MODIFIER	NA	NA	0.008552	0.008552	NA	NA	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	noncoding_transcript	MODIFIER	pass	needs_external_annotation	rare	missing

---

## run_2026_05_27_233524

### Files

Stage08: `results/run_2026_05_27_233524/processed/stage_08_vdb_ready_variants.tsv`
Coding partition: `results/run_2026_05_27_233524/processed/coding_candidates.tsv`
Splice partition: `results/run_2026_05_27_233524/processed/splice_region_candidates.tsv`
Noncoding partition: `results/run_2026_05_27_233524/processed/noncoding_candidates.tsv`

### Partition Row Accounting

| Metric | Count | Percent of Stage08 |
|---|---:|---:|
| Stage08 rows |  | 100.000000 |
| Coding rows |  | NA |
| Splice-region rows |  | NA |
| Noncoding rows |  | NA |
| Coding + splice + noncoding | 0 | NA |
| Delta: Stage08 - partitions | 0 | NA |

**Row accounting result:** Perfect row reconstruction.

### Variant-ID Set Accounting

| Metric | Count |
|---|---:|
| Stage08 distinct variant_ids | 811554 |
| Union partition distinct variant_ids | 811554 |
| Variant_ids appearing in more than one partition | 547 |
| Stage08 ids absent from partitions | 0 |
| Partition ids absent from Stage08 | 0 |

**Set accounting result:** Partition union exactly reconstructs Stage08 variant_id set.

### Stage09 / Stage10 Downstream Check

- stage_09_coding_interpreted rows: 
- expected coding + splice rows: 0
- expected - observed delta: 0
- stage_10_noncoding_interpreted rows: 
- expected noncoding rows: 
- expected - observed delta: 0

### First Row Previews

Coding:
ERR10619281	run_2026_05_27_233524	variant_annotation_pipeline	1:69270:A:G	1	69270	A	G	snv	coding	PASS	ENSG00000186092	OR4F5	ENST00000641515.2	synonymous_variant	LOW	NA	NA	0.9961	0.9961	NA	NA	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	coding	LOW	pass	interpretable_now	common	missing

Splice-region:
ERR10619281	run_2026_05_27_233524	variant_annotation_pipeline	1:1041950:T:C	1	1041950	T	C	snv	coding	PASS	ENSG00000188157	AGRN	ENST00000379370.7	splice_region_variant&splice_polypyrimidine_tract_variant&intron_variant	LOW	benign	benign	0.8852	0.8852	NA	0.6899	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	benign

Noncoding:
ERR10619281	run_2026_05_27_233524	variant_annotation_pipeline	1:13813:T:G	1	13813	T	G	snv	noncoding	PASS	ENSG00000290825	DDX11L16	ENST00000832823.1	upstream_gene_variant	MODIFIER	NA	NA	0.4861	0.4861	NA	NA	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	regulatory	MODIFIER	pass	needs_external_annotation	common	missing

---

## run_2026_06_02_124300

### Files

Stage08: `results/run_2026_06_02_124300/processed/stage_08_vdb_ready_variants.tsv`
Coding partition: `results/run_2026_06_02_124300/processed/coding_candidates.tsv`
Splice partition: `results/run_2026_06_02_124300/processed/splice_region_candidates.tsv`
Noncoding partition: `results/run_2026_06_02_124300/processed/noncoding_candidates.tsv`

### Partition Row Accounting

| Metric | Count | Percent of Stage08 |
|---|---:|---:|
| Stage08 rows |  | 100.000000 |
| Coding rows |  | NA |
| Splice-region rows |  | NA |
| Noncoding rows |  | NA |
| Coding + splice + noncoding | 0 | NA |
| Delta: Stage08 - partitions | 0 | NA |

**Row accounting result:** Perfect row reconstruction.

### Variant-ID Set Accounting

| Metric | Count |
|---|---:|
| Stage08 distinct variant_ids | 795059 |
| Union partition distinct variant_ids | 795059 |
| Variant_ids appearing in more than one partition | 518 |
| Stage08 ids absent from partitions | 0 |
| Partition ids absent from Stage08 | 0 |

**Set accounting result:** Partition union exactly reconstructs Stage08 variant_id set.

### Stage09 / Stage10 Downstream Check

- stage_09_coding_interpreted rows: 
- expected coding + splice rows: 0
- expected - observed delta: 0
- stage_10_noncoding_interpreted rows: 
- expected noncoding rows: 
- expected - observed delta: 0

### First Row Previews

Coding:
ERR10619285	run_2026_06_02_124300	variant_annotation_pipeline	1:69270:A:G	1	69270	A	G	snv	coding	PASS	ENSG00000186092	OR4F5	ENST00000641515.2	synonymous_variant	LOW	NA	NA	0.9961	0.9961	NA	NA	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	coding	LOW	pass	interpretable_now	common	missing

Splice-region:
ERR10619285	run_2026_06_02_124300	variant_annotation_pipeline	1:17746:A:G	1	17746	A	G	snv	coding	PASS	ENSG00000310526	WASH7P	ENST00000831140.1	splice_region_variant&splice_polypyrimidine_tract_variant&intron_variant&non_coding_transcript_variant	LOW	NA	NA	0.1499	0.1499	NA	NA	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	missing

Noncoding:
ERR10619285	run_2026_06_02_124300	variant_annotation_pipeline	1:13289:CCT:C	1	13289	CCT	C	deletion	noncoding	PASS	ENSG00000223972	DDX11L1	ENST00000450305.2	non_coding_transcript_exon_variant	MODIFIER	NA	NA	0.004	0.0040	NA	0	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	noncoding_transcript	MODIFIER	pass	needs_external_annotation	rare	missing

---

## run_2026_05_27_172531

### Files

Stage08: `results/run_2026_05_27_172531/processed/stage_08_vdb_ready_variants.tsv`
Coding partition: `results/run_2026_05_27_172531/processed/coding_candidates.tsv`
Splice partition: `results/run_2026_05_27_172531/processed/splice_region_candidates.tsv`
Noncoding partition: `results/run_2026_05_27_172531/processed/noncoding_candidates.tsv`

### Partition Row Accounting

| Metric | Count | Percent of Stage08 |
|---|---:|---:|
| Stage08 rows |  | 100.000000 |
| Coding rows |  | NA |
| Splice-region rows |  | NA |
| Noncoding rows |  | NA |
| Coding + splice + noncoding | 0 | NA |
| Delta: Stage08 - partitions | 0 | NA |

**Row accounting result:** Perfect row reconstruction.

### Variant-ID Set Accounting

| Metric | Count |
|---|---:|
| Stage08 distinct variant_ids | 736468 |
| Union partition distinct variant_ids | 736468 |
| Variant_ids appearing in more than one partition | 493 |
| Stage08 ids absent from partitions | 0 |
| Partition ids absent from Stage08 | 0 |

**Set accounting result:** Partition union exactly reconstructs Stage08 variant_id set.

### Stage09 / Stage10 Downstream Check

- stage_09_coding_interpreted rows: 
- expected coding + splice rows: 0
- expected - observed delta: 0
- stage_10_noncoding_interpreted rows: 
- expected noncoding rows: 
- expected - observed delta: 0

### First Row Previews

Coding:
ERR10619300	run_2026_05_27_172531	variant_annotation_pipeline	1:69270:A:G	1	69270	A	G	snv	coding	PASS	ENSG00000186092	OR4F5	ENST00000641515.2	synonymous_variant	LOW	NA	NA	0.9961	0.9961	NA	NA	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	coding	LOW	pass	interpretable_now	common	missing

Splice-region:
ERR10619300	run_2026_05_27_172531	variant_annotation_pipeline	1:17746:A:G	1	17746	A	G	snv	coding	PASS	ENSG00000310526	WASH7P	ENST00000831140.1	splice_region_variant&splice_polypyrimidine_tract_variant&intron_variant&non_coding_transcript_variant	LOW	NA	NA	0.1499	0.1499	NA	NA	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	missing

Noncoding:
ERR10619300	run_2026_05_27_172531	variant_annotation_pipeline	1:13813:T:G	1	13813	T	G	snv	noncoding	PASS	ENSG00000290825	DDX11L16	ENST00000832823.1	upstream_gene_variant	MODIFIER	NA	NA	0.4861	0.4861	NA	NA	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	regulatory	MODIFIER	pass	needs_external_annotation	common	missing

---

## run_2026_06_02_181024

### Files

Stage08: `results/run_2026_06_02_181024/processed/stage_08_vdb_ready_variants.tsv`
Coding partition: `results/run_2026_06_02_181024/processed/coding_candidates.tsv`
Splice partition: `results/run_2026_06_02_181024/processed/splice_region_candidates.tsv`
Noncoding partition: `results/run_2026_06_02_181024/processed/noncoding_candidates.tsv`

### Partition Row Accounting

| Metric | Count | Percent of Stage08 |
|---|---:|---:|
| Stage08 rows |  | 100.000000 |
| Coding rows |  | NA |
| Splice-region rows |  | NA |
| Noncoding rows |  | NA |
| Coding + splice + noncoding | 0 | NA |
| Delta: Stage08 - partitions | 0 | NA |

**Row accounting result:** Perfect row reconstruction.

### Variant-ID Set Accounting

| Metric | Count |
|---|---:|
| Stage08 distinct variant_ids | 879401 |
| Union partition distinct variant_ids | 879401 |
| Variant_ids appearing in more than one partition | 486 |
| Stage08 ids absent from partitions | 0 |
| Partition ids absent from Stage08 | 0 |

**Set accounting result:** Partition union exactly reconstructs Stage08 variant_id set.

### Stage09 / Stage10 Downstream Check

- stage_09_coding_interpreted rows: 
- expected coding + splice rows: 0
- expected - observed delta: 0
- stage_10_noncoding_interpreted rows: 
- expected noncoding rows: 
- expected - observed delta: 0

### First Row Previews

Coding:
ERR10619309	run_2026_06_02_181024	variant_annotation_pipeline	1:924533:A:G	1	924533	A	G	snv	coding	PASS	ENSG00000187634	SAMD11	ENST00000616016.5	synonymous_variant	LOW	NA	NA	0.7498	0.7498	NA	0.4039	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	coding	LOW	pass	interpretable_now	common	missing

Splice-region:
ERR10619309	run_2026_06_02_181024	variant_annotation_pipeline	1:1041950:T:C	1	1041950	T	C	snv	coding	PASS	ENSG00000188157	AGRN	ENST00000379370.7	splice_region_variant&splice_polypyrimidine_tract_variant&intron_variant	LOW	benign	benign	0.8852	0.8852	NA	0.6899	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	common	benign

Noncoding:
ERR10619309	run_2026_06_02_181024	variant_annotation_pipeline	1:13550:G:A	1	13550	G	A	snv	noncoding	PASS	ENSG00000223972	DDX11L1	ENST00000450305.2	non_coding_transcript_exon_variant	MODIFIER	NA	NA	0.0034	0.0034	NA	0.0008	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	noncoding_transcript	MODIFIER	pass	needs_external_annotation	rare	missing

---

## run_2026_06_01_203130

### Files

Stage08: `results/run_2026_06_01_203130/processed/stage_08_vdb_ready_variants.tsv`
Coding partition: `results/run_2026_06_01_203130/processed/coding_candidates.tsv`
Splice partition: `results/run_2026_06_01_203130/processed/splice_region_candidates.tsv`
Noncoding partition: `results/run_2026_06_01_203130/processed/noncoding_candidates.tsv`

### Partition Row Accounting

| Metric | Count | Percent of Stage08 |
|---|---:|---:|
| Stage08 rows |  | 100.000000 |
| Coding rows |  | NA |
| Splice-region rows |  | NA |
| Noncoding rows |  | NA |
| Coding + splice + noncoding | 0 | NA |
| Delta: Stage08 - partitions | 0 | NA |

**Row accounting result:** Perfect row reconstruction.

### Variant-ID Set Accounting

| Metric | Count |
|---|---:|
| Stage08 distinct variant_ids | 963426 |
| Union partition distinct variant_ids | 963426 |
| Variant_ids appearing in more than one partition | 490 |
| Stage08 ids absent from partitions | 0 |
| Partition ids absent from Stage08 | 0 |

**Set accounting result:** Partition union exactly reconstructs Stage08 variant_id set.

### Stage09 / Stage10 Downstream Check

- stage_09_coding_interpreted rows: 
- expected coding + splice rows: 0
- expected - observed delta: 0
- stage_10_noncoding_interpreted rows: 
- expected noncoding rows: 
- expected - observed delta: 0

### First Row Previews

Coding:
ERR10619330	run_2026_06_01_203130	variant_annotation_pipeline	1:924533:A:G	1	924533	A	G	snv	coding	PASS	ENSG00000187634	SAMD11	ENST00000616016.5	synonymous_variant	LOW	NA	NA	0.7498	0.7498	NA	0.4039	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	coding	LOW	pass	interpretable_now	common	missing

Splice-region:
ERR10619330	run_2026_06_01_203130	variant_annotation_pipeline	1:182597:G:A	1	182597	G	A	snv	coding	PASS	ENSG00000310527	WASH9P	ENST00000831131.1	splice_region_variant&splice_polypyrimidine_tract_variant&intron_variant&non_coding_transcript_variant	LOW	NA	NA	0.03696	0.03696	NA	NA	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	splice_region	LOW	pass	interpretable_now	low_frequency	missing

Noncoding:
ERR10619330	run_2026_06_01_203130	variant_annotation_pipeline	1:13418:G:A	1	13418	G	A	snv	noncoding	PASS	ENSG00000223972	DDX11L1	ENST00000450305.2	intron_variant&non_coding_transcript_variant	MODIFIER	NA	NA	0.2087	0.2087	NA	NA	False	False	VEP	# ENSEMBL VARIANT EFFECT PREDICTOR #	mapped	intronic	MODIFIER	pass	needs_external_annotation	common	missing

---

## run_2026_06_03_010030

