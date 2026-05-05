# stage_12_validation_pass_examples

## Source

- Source file: `/root/dev/portfolio_projects/variant_annotation_pipeline/results/run_2026_04_17_082417/processed/stage_12_validation_candidates.tsv`
- Run ID: `run_2026_04_17_082417`
- Sample/Dataset: `HG002`


## Why These Examples Matter

These examples represent the subset of variants that:

- survive prioritization (Stage 11)
- pass QC filters
- require independent validation (Stage 12)

They illustrate the precise handoff between prioritization and validation layers.

## Stage 12 Validation-Pass Examples

These examples represent variants that Stage 12 marks as requiring validation or higher-priority review. They are triage candidates, not clinically confirmed findings.

### Validation-Required Examples

```text
sample_id  run_id                 source_pipeline              variant_id      chromosome  position  reference_allele  alternate_allele  variant_type  variant_class  quality_flag  gene_id          gene_symbol  transcript_id       consequence         impact_class  clinical_significance   clinvar_significance    population_frequency  gnomad_af  exac_af  thousand_genomes_af  mito_flag  epilepsy_flag  annotation_source  annotation_version  gene_mapping_status  variant_context  variant_effect_severity  qc_status  interpretability_status  frequency_status  clinical_status  functional_impact  rarity_flag    clinical_evidence  qc_reliability   coding_interpretation_label  is_lof_candidate  is_rare_candidate  is_clinically_supported  is_high_quality  is_potential_artifact  variant_origin  source_interpretation_label  priority_tier              priority_rank  priority_reason                    is_high_priority_candidate  is_moderate_priority_candidate  is_low_priority_candidate  is_uninterpretable  validation_required  validation_priority  suggested_validation_method  validation_reason        
HG002      run_2026_04_17_082417  variant_annotation_pipeline  1:1072326:G:A   1           1072326   G                 A                 snv           coding         PASS          ENSG00000237330  RNF223       ENST00000453464.3   missense_variant    MODERATE      NA                      NA                      0.0002                0.0002     NA       0                    False      False          VEP                115                 mapped               coding           MODERATE                 pass       interpretable_now        rare              missing          missense           rare           missing            high_confidence  lof_or_missense_rare         False             True               False                    True             False                  coding          lof_or_missense_rare         tier_2_moderate_candidate  2              coding label lof_or_missense_rare  False                       True                            False                      False               True                 medium               IGV                          tier_2_moderate_candidate
HG002      run_2026_04_17_082417  variant_annotation_pipeline  1:3781099:C:T   1           3781099   C                 T                 snv           coding         PASS          ENSG00000130764  LRRC47       ENST00000378251.3   missense_variant    MODERATE      NA                      NA                      0.0194                0.0194     NA       0.0015               False      False          VEP                115                 mapped               coding           MODERATE                 pass       interpretable_now        low_frequency     missing          missense           low_frequency  missing            high_confidence  lof_or_missense_rare         False             False              False                    True             False                  coding          lof_or_missense_rare         tier_2_moderate_candidate  2              coding label lof_or_missense_rare  False                       True                            False                      False               True                 medium               IGV                          tier_2_moderate_candidate
HG002      run_2026_04_17_082417  variant_annotation_pipeline  1:5864452:C:A   1           5864452   C                 A                 snv           coding         PASS          ENSG00000131697  NPHP4        ENST00000378156.9   missense_variant    MODERATE      uncertain_significance  uncertain_significance  0.001152              0.001152   NA       NA                   False      False          VEP                115                 mapped               coding           MODERATE                 pass       interpretable_now        rare              vus              missense           rare           vus                high_confidence  lof_or_missense_rare         False             True               False                    True             False                  coding          lof_or_missense_rare         tier_2_moderate_candidate  2              coding label lof_or_missense_rare  False                       True                            False                      False               True                 medium               IGV                          tier_2_moderate_candidate
HG002      run_2026_04_17_082417  variant_annotation_pipeline  1:6249964:C:T   1           6249964   C                 T                 snv           coding         PASS          ENSG00000158292  GPR153       ENST00000377893.3   missense_variant    MODERATE      NA                      NA                      0.0357                0.0357     NA       0                    False      False          VEP                115                 mapped               coding           MODERATE                 pass       interpretable_now        low_frequency     missing          missense           low_frequency  missing            high_confidence  lof_or_missense_rare         False             False              False                    True             False                  coding          lof_or_missense_rare         tier_2_moderate_candidate  2              coding label lof_or_missense_rare  False                       True                            False                      False               True                 medium               IGV                          tier_2_moderate_candidate
HG002      run_2026_04_17_082417  variant_annotation_pipeline  1:6645884:C:T   1           6645884   C                 T                 snv           coding         PASS          ENSG00000007923  DNAJC11      ENST00000377577.10  missense_variant    MODERATE      NA                      NA                      0.0441                0.0441     NA       0.0038               True       False          VEP                115                 mapped               coding           MODERATE                 pass       interpretable_now        low_frequency     missing          missense           low_frequency  missing            high_confidence  lof_or_missense_rare         False             False              False                    True             False                  coding          lof_or_missense_rare         tier_2_moderate_candidate  2              coding label lof_or_missense_rare  False                       True                            False                      False               True                 medium               IGV                          tier_2_moderate_candidate
HG002      run_2026_04_17_082417  variant_annotation_pipeline  1:9718724:A:AT  1           9718724   A                 AT                insertion     coding         PASS          ENSG00000171608  PIK3CD       ENST00000377346.9   frameshift_variant  HIGH          NA                      NA                      0                     0          NA       NA                   False      False          VEP                115                 mapped               coding           HIGH                     pass       interpretable_now        rare              missing          loss_of_function   rare           missing            high_confidence  lof_or_missense_rare         True              True               False                    True             False                  coding          lof_or_missense_rare         tier_2_moderate_candidate  2              coding label lof_or_missense_rare  False                       True                            False                      False               True                 medium               IGV                          tier_2_moderate_candidate
HG002      run_2026_04_17_082417  variant_annotation_pipeline  1:11656010:G:A  1           11656010  G                 A                 snv           coding         PASS          ENSG00000132879  FBXO44       ENST00000251547.10  missense_variant    MODERATE      NA                      NA                      0.0088                0.0088     NA       0.0008               False      False          VEP                115                 mapped               coding           MODERATE                 pass       interpretable_now        rare              missing          missense           rare           missing            high_confidence  lof_or_missense_rare         False             True               False                    True             False                  coding          lof_or_missense_rare         tier_2_moderate_candidate  2              coding label lof_or_missense_rare  False                       True                            False                      False               True                 medium               IGV                          tier_2_moderate_candidate
HG002      run_2026_04_17_082417  variant_annotation_pipeline  1:11858462:C:T  1           11858462  C                 T                 snv           coding         PASS          ENSG00000120937  NPPB         ENST00000376468.4   missense_variant    MODERATE      NA                      NA                      0.0038                0.0038     NA       0                    False      False          VEP                115                 mapped               coding           MODERATE                 pass       interpretable_now        rare              missing          missense           rare           missing            high_confidence  lof_or_missense_rare         False             True               False                    True             False                  coding          lof_or_missense_rare         tier_2_moderate_candidate  2              coding label lof_or_missense_rare  False                       True                            False                      False               True                 medium               IGV                          tier_2_moderate_candidate
HG002      run_2026_04_17_082417  variant_annotation_pipeline  1:12115601:G:A  1           12115601  G                 A                 snv           coding         PASS          ENSG00000120949  TNFRSF8      ENST00000263932.7   missense_variant    MODERATE      NA                      NA                      0.0026                0.0026     NA       0.0008               False      False          VEP                115                 mapped               coding           MODERATE                 pass       interpretable_now        rare              missing          missense           rare           missing            high_confidence  lof_or_missense_rare         False             True               False                    True             False                  coding          lof_or_missense_rare         tier_2_moderate_candidate  2              coding label lof_or_missense_rare  False                       True                            False                      False               True                 medium               IGV                          tier_2_moderate_candidate
HG002      run_2026_04_17_082417  variant_annotation_pipeline  1:12847604:A:G  1           12847604  A                 G                 snv           coding         PASS          ENSG00000179172  HNRNPCL1     ENST00000317869.7   missense_variant    MODERATE      NA                      NA                      0.0014                0.0014     NA       0.0008               False      False          VEP                115                 mapped               coding           MODERATE                 pass       interpretable_now        rare              missing          missense           rare           missing            high_confidence  lof_or_missense_rare         False             True               False                    True             False                  coding          lof_or_missense_rare         tier_2_moderate_candidate  2              coding label lof_or_missense_rare  False                       True                            False                      False               True                 medium               IGV                          tier_2_moderate_candidate
```

## Interpretation

These examples represent the subset of variants that Stage 12 explicitly selects for validation.

### Key Observations

- All variants:
  - originate from Tier 2 prioritization
  - have validation_required = True
  - are assigned validation_priority = medium
  - are assigned IGV as the validation method

- Variants are predominantly:
  - coding
  - rare or low-frequency
  - functionally interpretable (missense or loss_of_function)

### Relationship to Stage 11

These variants demonstrate the direct mapping:

- Stage 11 → identifies candidate variants
- Stage 12 → assigns validation requirements without altering candidate identity

### System Insight

> Validation assignment is deterministic and strictly derived from prioritization logic.

No additional filtering or reinterpretation occurs at this stage.

### Bottom Line

> These examples confirm that validation decisions are consistent, explainable, and fully traceable to upstream prioritization.

## Notes

- No additional notes.

## Limitations

- Excerpt or summary only.
- Not the full dataset unless explicitly stated.
- No new inference performed.
