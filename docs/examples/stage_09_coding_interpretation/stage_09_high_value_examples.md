# stage_09_high_value_examples

## Source

- Source file: `/root/dev/portfolio_projects/variant_annotation_pipeline/results/run_2026_04_17_082417/processed/stage_09_coding_interpreted.tsv`
- Run ID: `run_2026_04_17_082417`
- Sample/Dataset: `HG002`

## Method

Artifacts are generated using a config-driven extraction system ("Artificer") and curated for clarity.

## Output

## Biological Sanity Check

Observed coding variant distributions are expected for a healthy reference individual and should not be interpreted as diagnosis.

## Loss-of-Function Examples

High-impact coding disruptions selected from Stage 09 interpreted variants.

```text
sample_id  run_id                 source_pipeline              variant_id                                        chromosome  position  reference_allele                     alternate_allele  variant_type  variant_class  quality_flag  gene_id          gene_symbol  transcript_id       consequence         impact_class  clinical_significance  clinvar_significance  population_frequency  gnomad_af  exac_af  thousand_genomes_af  mito_flag  epilepsy_flag  annotation_source  annotation_version  gene_mapping_status  variant_context  variant_effect_severity  qc_status  interpretability_status  frequency_status  clinical_status  functional_impact  rarity_flag  clinical_evidence  qc_reliability   coding_interpretation_label   is_lof_candidate  is_rare_candidate  is_clinically_supported  is_high_quality  is_potential_artifact
HG002      run_2026_04_17_082417  variant_annotation_pipeline  1:9718724:A:AT                                    1           9718724   A                                    AT                insertion     coding         PASS          ENSG00000171608  PIK3CD       ENST00000377346.9   frameshift_variant  HIGH          NA                     NA                    0                     0          NA       NA                   False      False          VEP                115                 mapped               coding           HIGH                     pass       interpretable_now        rare              missing          loss_of_function   rare         missing            high_confidence  lof_or_missense_rare          True              True               False                    True             False                
HG002      run_2026_04_17_082417  variant_annotation_pipeline  1:11846011:A:G                                    1           11846011  A                                    G                 snv           coding         PASS          ENSG00000175206  NPPA         ENST00000376480.7   stop_lost           HIGH          benign                 benign                0.4183                0.1791     NA       0.4183               False      False          VEP                115                 mapped               coding           HIGH                     pass       interpretable_now        common            benign           loss_of_function   common       benign             high_confidence  coding_common_or_low_support  True              False              False                    True             False                
HG002      run_2026_04_17_082417  variant_annotation_pipeline  1:26345031:GAAATGAGGCATCA:G                       1           26345031  GAAATGAGGCATCA                       G                 deletion      coding         PASS          ENSG00000176092  CRYBG2       ENST00000308182.10  frameshift_variant  HIGH          NA                     NA                    0.7034                0.7034     NA       NA                   False      False          VEP                115                 mapped               coding           HIGH                     pass       interpretable_now        common            missing          loss_of_function   common       missing            high_confidence  coding_common_or_low_support  True              False              False                    True             False                
HG002      run_2026_04_17_082417  variant_annotation_pipeline  1:26345047:AGCAC:A                                1           26345047  AGCAC                                A                 deletion      coding         PASS          ENSG00000176092  CRYBG2       ENST00000308182.10  frameshift_variant  HIGH          NA                     NA                    0.7101                0.7101     NA       NA                   False      False          VEP                115                 mapped               coding           HIGH                     pass       interpretable_now        common            missing          loss_of_function   common       missing            high_confidence  coding_common_or_low_support  True              False              False                    True             False                
HG002      run_2026_04_17_082417  variant_annotation_pipeline  1:26345053:GGGGCCCTTCACGACCTCTTTCCAGGTGGGGAACA:G  1           26345053  GGGGCCCTTCACGACCTCTTTCCAGGTGGGGAACA  G                 deletion      coding         PASS          ENSG00000176092  CRYBG2       ENST00000308182.10  frameshift_variant  HIGH          NA                     NA                    0.7374                0.7374     NA       NA                   False      False          VEP                115                 mapped               coding           HIGH                     pass       interpretable_now        common            missing          loss_of_function   common       missing            high_confidence  coding_common_or_low_support  True              False              False                    True             False                
```

## Missense / Rare Examples

```text
sample_id  run_id                 source_pipeline              variant_id     chromosome  position  reference_allele  alternate_allele  variant_type  variant_class  quality_flag  gene_id          gene_symbol  transcript_id       consequence       impact_class  clinical_significance   clinvar_significance    population_frequency  gnomad_af  exac_af  thousand_genomes_af  mito_flag  epilepsy_flag  annotation_source  annotation_version  gene_mapping_status  variant_context  variant_effect_severity  qc_status  interpretability_status  frequency_status  clinical_status  functional_impact  rarity_flag    clinical_evidence  qc_reliability   coding_interpretation_label  is_lof_candidate  is_rare_candidate  is_clinically_supported  is_high_quality  is_potential_artifact
HG002      run_2026_04_17_082417  variant_annotation_pipeline  1:1072326:G:A  1           1072326   G                 A                 snv           coding         PASS          ENSG00000237330  RNF223       ENST00000453464.3   missense_variant  MODERATE      NA                      NA                      0.0002                0.0002     NA       0                    False      False          VEP                115                 mapped               coding           MODERATE                 pass       interpretable_now        rare              missing          missense           rare           missing            high_confidence  lof_or_missense_rare         False             True               False                    True             False                
HG002      run_2026_04_17_082417  variant_annotation_pipeline  1:3781099:C:T  1           3781099   C                 T                 snv           coding         PASS          ENSG00000130764  LRRC47       ENST00000378251.3   missense_variant  MODERATE      NA                      NA                      0.0194                0.0194     NA       0.0015               False      False          VEP                115                 mapped               coding           MODERATE                 pass       interpretable_now        low_frequency     missing          missense           low_frequency  missing            high_confidence  lof_or_missense_rare         False             False              False                    True             False                
HG002      run_2026_04_17_082417  variant_annotation_pipeline  1:5864452:C:A  1           5864452   C                 A                 snv           coding         PASS          ENSG00000131697  NPHP4        ENST00000378156.9   missense_variant  MODERATE      uncertain_significance  uncertain_significance  0.001152              0.001152   NA       NA                   False      False          VEP                115                 mapped               coding           MODERATE                 pass       interpretable_now        rare              vus              missense           rare           vus                high_confidence  lof_or_missense_rare         False             True               False                    True             False                
HG002      run_2026_04_17_082417  variant_annotation_pipeline  1:6249964:C:T  1           6249964   C                 T                 snv           coding         PASS          ENSG00000158292  GPR153       ENST00000377893.3   missense_variant  MODERATE      NA                      NA                      0.0357                0.0357     NA       0                    False      False          VEP                115                 mapped               coding           MODERATE                 pass       interpretable_now        low_frequency     missing          missense           low_frequency  missing            high_confidence  lof_or_missense_rare         False             False              False                    True             False                
HG002      run_2026_04_17_082417  variant_annotation_pipeline  1:6645884:C:T  1           6645884   C                 T                 snv           coding         PASS          ENSG00000007923  DNAJC11      ENST00000377577.10  missense_variant  MODERATE      NA                      NA                      0.0441                0.0441     NA       0.0038               True       False          VEP                115                 mapped               coding           MODERATE                 pass       interpretable_now        low_frequency     missing          missense           low_frequency  missing            high_confidence  lof_or_missense_rare         False             False              False                    True             False                
```

## Clinically Supported Examples

```text
sample_id  run_id                 source_pipeline              variant_id     chromosome  position  reference_allele  alternate_allele  variant_type  variant_class  quality_flag  gene_id          gene_symbol  transcript_id      consequence         impact_class  clinical_significance  clinvar_significance  population_frequency  gnomad_af  exac_af  thousand_genomes_af  mito_flag  epilepsy_flag  annotation_source  annotation_version  gene_mapping_status  variant_context  variant_effect_severity  qc_status  interpretability_status  frequency_status  clinical_status  functional_impact  rarity_flag  clinical_evidence  qc_reliability   coding_interpretation_label   is_lof_candidate  is_rare_candidate  is_clinically_supported  is_high_quality  is_potential_artifact
HG002      run_2026_04_17_082417  variant_annotation_pipeline  1:1014274:A:G  1           1014274   A                 G                 snv           coding         PASS          ENSG00000187608  ISG15        ENST00000649529.1  synonymous_variant  LOW           benign                 benign                0.8257                0.8257     NA       0.5083               False      False          VEP                115                 mapped               coding           LOW                      pass       interpretable_now        common            benign           synonymous         common       benign             high_confidence  coding_common_or_low_support  False             False              False                    True             False                
HG002      run_2026_04_17_082417  variant_annotation_pipeline  1:1046551:A:G  1           1046551   A                 G                 snv           coding         PASS          ENSG00000188157  AGRN         ENST00000379370.7  synonymous_variant  LOW           benign                 benign                0.7977                0.7977     NA       0.4554               False      False          VEP                115                 mapped               coding           LOW                      pass       interpretable_now        common            benign           synonymous         common       benign             high_confidence  coding_common_or_low_support  False             False              False                    True             False                
HG002      run_2026_04_17_082417  variant_annotation_pipeline  1:1047614:T:C  1           1047614   T                 C                 snv           coding         PASS          ENSG00000188157  AGRN         ENST00000379370.7  synonymous_variant  LOW           benign                 benign                0.8359                0.8359     NA       0.5151               False      False          VEP                115                 mapped               coding           LOW                      pass       interpretable_now        common            benign           synonymous         common       benign             high_confidence  coding_common_or_low_support  False             False              False                    True             False                
HG002      run_2026_04_17_082417  variant_annotation_pipeline  1:1048922:T:C  1           1048922   T                 C                 snv           coding         PASS          ENSG00000188157  AGRN         ENST00000379370.7  synonymous_variant  LOW           benign                 benign                0.5457                0.5457     NA       0.2405               False      False          VEP                115                 mapped               coding           LOW                      pass       interpretable_now        common            benign           synonymous         common       benign             high_confidence  coding_common_or_low_support  False             False              False                    True             False                
HG002      run_2026_04_17_082417  variant_annotation_pipeline  1:1054900:C:T  1           1054900   C                 T                 snv           coding         PASS          ENSG00000188157  AGRN         ENST00000379370.7  synonymous_variant  LOW           benign                 benign                0.5853                0.5853     NA       0.2617               False      False          VEP                115                 mapped               coding           LOW                      pass       interpretable_now        common            benign           synonymous         common       benign             high_confidence  coding_common_or_low_support  False             False              False                    True             False                
```

## Interpretation

These examples illustrate three classes of coding variants:

### Loss-of-Function Variants

- include frameshift and stop-altering variants  
- may disrupt protein function  

### Rare Missense Variants

- occur at low population frequency  
- may represent candidates for further analysis  

### Clinically Annotated Variants

- include variants labeled as benign, VUS, or pathogenic in ClinVar  

---

### Key Insight

> The presence of rare, loss-of-function, or ClinVar-annotated variants in HG002 does NOT indicate disease.

This reflects:

- natural human genetic variation  
- incomplete penetrance  
- limitations in clinical annotation databases  

Stage 09 identifies candidates—not diagnoses.

## Notes

- No additional notes.

## Limitations

- Excerpt or summary only.
- Not the full dataset unless explicitly stated.
- No new inference performed.
