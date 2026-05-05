# stage_10_high_value_examples

## Source

- Source file: `/root/dev/portfolio_projects/variant_annotation_pipeline/results/run_2026_04_17_082417/processed/stage_10_noncoding_interpreted.tsv`
- Run ID: `run_2026_04_17_082417`
- Sample/Dataset: `HG002`

## Method

Artifacts are generated using a config-driven extraction system ("Artificer") and curated for clarity.

## Output

## Biological Sanity Check

Observed noncoding variant distributions are expected for a healthy reference individual and should not be interpreted as diagnosis.

## Rare Noncoding Candidate Examples

Rare noncoding variants selected from Stage 10 interpreted variants.

```text
sample_id	run_id	source_pipeline	variant_id	chromosome	position	reference_allele	alternate_allele	variant_type	variant_class	quality_flag	gene_id	gene_symbol	transcript_id	consequence	impact_class	clinical_significance	clinvar_significance	population_frequency	gnomad_af	exac_af	thousand_genomes_af	mito_flag	epilepsy_flag	annotation_source	annotation_version	gene_mapping_status	variant_context	variant_effect_severity	qc_status	interpretability_status	frequency_status	clinical_status	noncoding_functional_context	rarity_flag	clinical_evidence	qc_reliability	noncoding_interpretation_label	is_regulatory_candidate	is_rare_candidate	is_clinically_supported	is_high_quality	is_potential_artifact
```

## Regulatory / Functional Context Examples

```text
sample_id  run_id                 source_pipeline              variant_id   chromosome  position  reference_allele  alternate_allele  variant_type  variant_class  quality_flag  gene_id          gene_symbol  transcript_id      consequence                         impact_class  clinical_significance  clinvar_significance  population_frequency  gnomad_af  exac_af  thousand_genomes_af  mito_flag  epilepsy_flag  annotation_source  annotation_version  gene_mapping_status  variant_context       variant_effect_severity  qc_status  interpretability_status    frequency_status  clinical_status  noncoding_functional_context  rarity_flag  clinical_evidence  qc_reliability   noncoding_interpretation_label   is_regulatory_candidate  is_rare_candidate  is_clinically_supported  is_high_quality  is_potential_artifact
HG002      run_2026_04_17_082417  variant_annotation_pipeline  1:14522:G:A  1           14522     G                 A                 snv           noncoding      PASS          ENSG00000310526  WASH7P       ENST00000831140.1  non_coding_transcript_exon_variant  MODIFIER      NA                     NA                    0.1893                0.1893     NA       NA                   False      False          VEP                115                 mapped               noncoding_transcript  MODIFIER                 pass       needs_external_annotation  common            missing          transcript_associated         common       missing            high_confidence  noncoding_common_or_low_support  False                    False              False                    True             False                
HG002      run_2026_04_17_082417  variant_annotation_pipeline  1:14542:A:G  1           14542     A                 G                 snv           noncoding      PASS          ENSG00000310526  WASH7P       ENST00000831140.1  non_coding_transcript_exon_variant  MODIFIER      NA                     NA                    0.3406                0.3406     NA       NA                   False      False          VEP                115                 mapped               noncoding_transcript  MODIFIER                 pass       needs_external_annotation  common            missing          transcript_associated         common       missing            high_confidence  noncoding_common_or_low_support  False                    False              False                    True             False                
HG002      run_2026_04_17_082417  variant_annotation_pipeline  1:14574:A:G  1           14574     A                 G                 snv           noncoding      PASS          ENSG00000310526  WASH7P       ENST00000831140.1  non_coding_transcript_exon_variant  MODIFIER      NA                     NA                    0.4207                0.4207     NA       NA                   False      False          VEP                115                 mapped               noncoding_transcript  MODIFIER                 pass       needs_external_annotation  common            missing          transcript_associated         common       missing            high_confidence  noncoding_common_or_low_support  False                    False              False                    True             False                
HG002      run_2026_04_17_082417  variant_annotation_pipeline  1:14590:G:A  1           14590     G                 A                 snv           noncoding      PASS          ENSG00000310526  WASH7P       ENST00000831140.1  non_coding_transcript_exon_variant  MODIFIER      NA                     NA                    0.2387                0.2387     NA       NA                   False      False          VEP                115                 mapped               noncoding_transcript  MODIFIER                 pass       needs_external_annotation  common            missing          transcript_associated         common       missing            high_confidence  noncoding_common_or_low_support  False                    False              False                    True             False                
HG002      run_2026_04_17_082417  variant_annotation_pipeline  1:14599:T:A  1           14599     T                 A                 snv           noncoding      PASS          ENSG00000310526  WASH7P       ENST00000831140.1  non_coding_transcript_exon_variant  MODIFIER      NA                     NA                    0.1476                0.1476     NA       0.121                False      False          VEP                115                 mapped               noncoding_transcript  MODIFIER                 pass       needs_external_annotation  common            missing          transcript_associated         common       missing            high_confidence  noncoding_common_or_low_support  False                    False              False                    True             False                
```

## Clinically Supported Examples

```text
sample_id  run_id                 source_pipeline              variant_id      chromosome  position  reference_allele  alternate_allele  variant_type  variant_class  quality_flag  gene_id          gene_symbol  transcript_id      consequence              impact_class  clinical_significance  clinvar_significance  population_frequency  gnomad_af  exac_af  thousand_genomes_af  mito_flag  epilepsy_flag  annotation_source  annotation_version  gene_mapping_status  variant_context  variant_effect_severity  qc_status  interpretability_status    frequency_status  clinical_status  noncoding_functional_context  rarity_flag    clinical_evidence  qc_reliability   noncoding_interpretation_label   is_regulatory_candidate  is_rare_candidate  is_clinically_supported  is_high_quality  is_potential_artifact
HG002      run_2026_04_17_082417  variant_annotation_pipeline  1:942451:T:C    1           942451    T                 C                 snv           noncoding      PASS          ENSG00000188976  NOC2L        ENST00000327044.7  downstream_gene_variant  MODIFIER      benign                 benign                1                     1.0000     NA       1                    False      False          VEP                115                 mapped               regulatory       MODIFIER                 pass       needs_external_annotation  common            benign           proximal                      common         benign             high_confidence  noncoding_common_or_low_support  False                    False              False                    True             False                
HG002      run_2026_04_17_082417  variant_annotation_pipeline  1:942934:G:C    1           942934    G                 C                 snv           noncoding      PASS          ENSG00000188976  NOC2L        ENST00000327044.7  downstream_gene_variant  MODIFIER      benign                 benign                0.0431                0.0431     NA       0.0083               False      False          VEP                115                 mapped               regulatory       MODIFIER                 pass       needs_external_annotation  low_frequency     benign           proximal                      low_frequency  benign             high_confidence  noncoding_common_or_low_support  False                    False              False                    True             False                
HG002      run_2026_04_17_082417  variant_annotation_pipeline  1:976215:A:G    1           976215    A                 G                 snv           noncoding      PASS          ENSG00000187583  PLEKHN1      ENST00000379410.8  downstream_gene_variant  MODIFIER      pathogenic             pathogenic            0.7103                0.7103     NA       0.4092               False      False          VEP                115                 mapped               regulatory       MODIFIER                 pass       needs_external_annotation  common            pathogenic       proximal                      common         pathogenic         high_confidence  noncoding_common_or_low_support  False                    False              True                     True             False                
HG002      run_2026_04_17_082417  variant_annotation_pipeline  1:1013466:T:TA  1           1013466   T                 TA                insertion     noncoding      PASS          ENSG00000187608  ISG15        ENST00000649529.1  upstream_gene_variant    MODIFIER      benign                 benign                0.8544                0.8544     NA       0.5575               False      False          VEP                115                 mapped               regulatory       MODIFIER                 pass       needs_external_annotation  common            benign           proximal                      common         benign             high_confidence  noncoding_common_or_low_support  False                    False              False                    True             False                
HG002      run_2026_04_17_082417  variant_annotation_pipeline  1:1013490:C:G   1           1013490   C                 G                 snv           noncoding      PASS          ENSG00000187608  ISG15        ENST00000649529.1  upstream_gene_variant    MODIFIER      benign                 benign                0.903                 0.9030     NA       0.7194               False      False          VEP                115                 mapped               regulatory       MODIFIER                 pass       needs_external_annotation  common            benign           proximal                      common         benign             high_confidence  noncoding_common_or_low_support  False                    False              False                    True             False                
```

## Interpretation

These examples illustrate three important classes of noncoding variants:

### 1. Rare Noncoding Candidates
- low-frequency variants with potential regulatory or transcript association  
- candidates for downstream analysis  

### 2. Regulatory / Transcript-Associated Variants
- variants located near or within gene-associated regions  
- may influence gene expression or transcript structure  

### 3. Clinically Annotated Variants
- variants with ClinVar annotations (benign, pathogenic, etc.)  
- often occur at high population frequency  

---

### Key Insight

> Noncoding variants may appear biologically relevant, but interpretation is limited without additional context.

This demonstrates:

- limitations of sequence-based annotation  
- need for integration with functional data (RSP)  

### Interpretation Boundary

Stage 10 intentionally avoids assigning biological meaning beyond available annotation.

---

## Notes

- No additional notes.

## Limitations

- Excerpt or summary only.
- Not the full dataset unless explicitly stated.
- No new inference performed.
