# stage_12_failed_qc_examples

## Source

- Source file: `/root/dev/portfolio_projects/variant_annotation_pipeline/results/run_2026_04_17_082417/processed/stage_12_validation_candidates.tsv`
- Run ID: `run_2026_04_17_082417`
- Sample/Dataset: `HG002`


## Why These Examples Matter

These examples demonstrate:

- common variants  
- noncoding variants with low interpretability  
- variants lacking supporting evidence  

They highlight the system’s ability to deprioritize low-quality or non-informative signals.

## Stage 12 QC / Artifact Examples

These examples document variants that may require caution because of artifact flags or lower reliability.

### Lower-Reliability Examples

```text
sample_id  run_id                 source_pipeline              variant_id        chromosome  position  reference_allele  alternate_allele  variant_type  variant_class  quality_flag  gene_id          gene_symbol  transcript_id      consequence          impact_class  clinical_significance  clinvar_significance  population_frequency  gnomad_af  exac_af  thousand_genomes_af  mito_flag  epilepsy_flag  annotation_source  annotation_version  gene_mapping_status  variant_context  variant_effect_severity  qc_status  interpretability_status  frequency_status  clinical_status  functional_impact  rarity_flag  clinical_evidence  qc_reliability  coding_interpretation_label  is_lof_candidate  is_rare_candidate  is_clinically_supported  is_high_quality  is_potential_artifact  variant_origin  source_interpretation_label  priority_tier                         priority_rank  priority_reason                            is_high_priority_candidate  is_moderate_priority_candidate  is_low_priority_candidate  is_uninterpretable  validation_required  validation_priority  suggested_validation_method  validation_reason                   
HG002      run_2026_04_17_082417  variant_annotation_pipeline  1:924024:C:G      1           924024    C                 G                 snv           unknown        PASS          ENSG00000187634  SAMD11       ENST00000616016.5  5_prime_UTR_variant  MODIFIER      NA                     NA                    0.6813                0.6813     NA       0.3268               False      False          VEP                115                 mapped               unknown          MODIFIER                 caution    unsupported_currently    common            missing          NA                 common       missing            caution         NA                           NA                False              False                    False            False                  noncoding       noncoding_uninterpretable    tier_4_uninterpretable_or_qc_limited  4              noncoding label noncoding_uninterpretable  False                       False                           False                      True                False                low                  none                         tier_4_uninterpretable_or_qc_limited
HG002      run_2026_04_17_082417  variant_annotation_pipeline  1:924310:C:G      1           924310    C                 G                 snv           unknown        PASS          ENSG00000187634  SAMD11       ENST00000616016.5  5_prime_UTR_variant  MODIFIER      NA                     NA                    0.6923                0.6923     NA       0.3737               False      False          VEP                115                 mapped               unknown          MODIFIER                 caution    unsupported_currently    common            missing          NA                 common       missing            caution         NA                           NA                False              False                    False            False                  noncoding       noncoding_uninterpretable    tier_4_uninterpretable_or_qc_limited  4              noncoding label noncoding_uninterpretable  False                       False                           False                      True                False                low                  none                         tier_4_uninterpretable_or_qc_limited
HG002      run_2026_04_17_082417  variant_annotation_pipeline  1:924321:C:G      1           924321    C                 G                 snv           unknown        PASS          ENSG00000187634  SAMD11       ENST00000616016.5  5_prime_UTR_variant  MODIFIER      NA                     NA                    0.6923                0.6923     NA       0.3737               False      False          VEP                115                 mapped               unknown          MODIFIER                 caution    unsupported_currently    common            missing          NA                 common       missing            caution         NA                           NA                False              False                    False            False                  noncoding       noncoding_uninterpretable    tier_4_uninterpretable_or_qc_limited  4              noncoding label noncoding_uninterpretable  False                       False                           False                      True                False                low                  none                         tier_4_uninterpretable_or_qc_limited
HG002      run_2026_04_17_082417  variant_annotation_pipeline  1:944296:G:A      1           944296    G                 A                 snv           unknown        PASS          ENSG00000188976  NOC2L        ENST00000327044.7  3_prime_UTR_variant  MODIFIER      NA                     NA                    0.886                 0.8860     NA       0.7867               False      False          VEP                115                 mapped               unknown          MODIFIER                 caution    unsupported_currently    common            missing          NA                 common       missing            caution         NA                           NA                False              False                    False            False                  noncoding       noncoding_uninterpretable    tier_4_uninterpretable_or_qc_limited  4              noncoding label noncoding_uninterpretable  False                       False                           False                      True                False                low                  none                         tier_4_uninterpretable_or_qc_limited
HG002      run_2026_04_17_082417  variant_annotation_pipeline  1:944307:T:C      1           944307    T                 C                 snv           unknown        PASS          ENSG00000188976  NOC2L        ENST00000327044.7  3_prime_UTR_variant  MODIFIER      NA                     NA                    0.9211                0.9211     NA       0.9062               False      False          VEP                115                 mapped               unknown          MODIFIER                 caution    unsupported_currently    common            missing          NA                 common       missing            caution         NA                           NA                False              False                    False            False                  noncoding       noncoding_uninterpretable    tier_4_uninterpretable_or_qc_limited  4              noncoding label noncoding_uninterpretable  False                       False                           False                      True                False                low                  none                         tier_4_uninterpretable_or_qc_limited
HG002      run_2026_04_17_082417  variant_annotation_pipeline  1:965337:CTTAT:C  1           965337    CTTAT             C                 deletion      unknown        PASS          ENSG00000187961  KLHL17       ENST00000338591.8  3_prime_UTR_variant  MODIFIER      NA                     NA                    0.3706                0.3706     NA       0.034                False      False          VEP                115                 mapped               unknown          MODIFIER                 caution    unsupported_currently    common            missing          NA                 common       missing            caution         NA                           NA                False              False                    False            False                  noncoding       noncoding_uninterpretable    tier_4_uninterpretable_or_qc_limited  4              noncoding label noncoding_uninterpretable  False                       False                           False                      True                False                low                  none                         tier_4_uninterpretable_or_qc_limited
HG002      run_2026_04_17_082417  variant_annotation_pipeline  1:965350:G:A      1           965350    G                 A                 snv           unknown        PASS          ENSG00000187961  KLHL17       ENST00000338591.8  3_prime_UTR_variant  MODIFIER      NA                     NA                    0.6474                0.6474     NA       0.2005               False      False          VEP                115                 mapped               unknown          MODIFIER                 caution    unsupported_currently    common            missing          NA                 common       missing            caution         NA                           NA                False              False                    False            False                  noncoding       noncoding_uninterpretable    tier_4_uninterpretable_or_qc_limited  4              noncoding label noncoding_uninterpretable  False                       False                           False                      True                False                low                  none                         tier_4_uninterpretable_or_qc_limited
HG002      run_2026_04_17_082417  variant_annotation_pipeline  1:965592:T:G      1           965592    T                 G                 snv           unknown        PASS          ENSG00000187961  KLHL17       ENST00000338591.8  3_prime_UTR_variant  MODIFIER      NA                     NA                    0.9334                0.9301     NA       0.9334               False      False          VEP                115                 mapped               unknown          MODIFIER                 caution    unsupported_currently    common            missing          NA                 common       missing            caution         NA                           NA                False              False                    False            False                  noncoding       noncoding_uninterpretable    tier_4_uninterpretable_or_qc_limited  4              noncoding label noncoding_uninterpretable  False                       False                           False                      True                False                low                  none                         tier_4_uninterpretable_or_qc_limited
HG002      run_2026_04_17_082417  variant_annotation_pipeline  1:965643:T:C      1           965643    T                 C                 snv           unknown        PASS          ENSG00000187961  KLHL17       ENST00000338591.8  3_prime_UTR_variant  MODIFIER      NA                     NA                    0.8866                0.8866     NA       0.7867               False      False          VEP                115                 mapped               unknown          MODIFIER                 caution    unsupported_currently    common            missing          NA                 common       missing            caution         NA                           NA                False              False                    False            False                  noncoding       noncoding_uninterpretable    tier_4_uninterpretable_or_qc_limited  4              noncoding label noncoding_uninterpretable  False                       False                           False                      True                False                low                  none                         tier_4_uninterpretable_or_qc_limited
HG002      run_2026_04_17_082417  variant_annotation_pipeline  1:975058:A:G      1           975058    A                 G                 snv           unknown        PASS          ENSG00000187583  PLEKHN1      ENST00000379410.8  3_prime_UTR_variant  MODIFIER      NA                     NA                    0.9305                0.9305     NA       0.789                False      False          VEP                115                 mapped               unknown          MODIFIER                 caution    unsupported_currently    common            missing          NA                 common       missing            caution         NA                           NA                False              False                    False            False                  noncoding       noncoding_uninterpretable    tier_4_uninterpretable_or_qc_limited  4              noncoding label noncoding_uninterpretable  False                       False                           False                      True                False                low                  none                         tier_4_uninterpretable_or_qc_limited
```

## Interpretation

These examples represent variants that are correctly excluded from validation due to a combination of:

- high population frequency (common variants)
- noncoding location (UTR and regulatory regions)
- lack of supporting clinical or functional evidence

All examples are assigned to:

- Tier 4 (uninterpretable or QC-limited)
- validation_required = False

### Key Observations

- Population frequencies are high (≥0.3–0.9), indicating these are common polymorphisms
- Functional impact is classified as MODIFIER, reflecting low predicted biological consequence
- Variants are consistently labeled as noncoding_uninterpretable

### System Insight

> Stage 12 correctly prevents validation of variants that are common, noncoding, and biologically uninformative.

This demonstrates that the pipeline avoids over-prioritizing background genomic variation.

### Bottom Line

> These examples confirm that low-value signals are systematically filtered out and do not consume validation resources.

## Notes

- No additional notes.

## Limitations

- Excerpt or summary only.
- Not the full dataset unless explicitly stated.
- No new inference performed.
