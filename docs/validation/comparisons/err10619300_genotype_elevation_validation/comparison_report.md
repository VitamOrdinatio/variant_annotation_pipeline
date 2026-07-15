# Historical Run Reproducibility Comparison Report

- Comparison ID: `run_2026_07_14_114546_vs_run_2026_05_27_172531`
- Generated UTC: `2026-07-15T15:30:42+00:00`
- Script version: `0.9.0`
- Overall bounded result: `SCIENTIFIC_DIFFERENCE_UNDER_REVIEW`

## Evidence Sources

- Current execution: `/home/steelsparrow/dev/portfolio_projects/variant_annotation_pipeline/results/run_2026_07_14_114546`
- Current run ID: `run_2026_07_14_114546`
- Historical lightweight reference: `/home/steelsparrow/dev/portfolio_projects/variant_annotation_pipeline/results/run_2026_05_27_172531`
- Historical run ID: `run_2026_05_27_172531`
- Certified case-study reference: `/home/steelsparrow/dev/portfolio_projects/variant_annotation_pipeline/docs/case_studies/err10619300`

## Executive Interpretation

The comparison is asymmetric by design. Missing historical artifacts are not mismatches, current-only architecture is validated independently, and unresolved scientific differences are not attributed to hardware without equivalent software, configuration, annotation, reference, and resource evidence.

## Stage-Summary Classification Counts

```text
EXPECTED_ARCHITECTURE_EVOLUTION: 1
MATCH: 180
RUN_IDENTITY_DIFFERENCE: 36
UNDER_REVIEW: 161
```

## Historical Availability Classification Counts

```text
HISTORICAL_ARTIFACT_UNAVAILABLE: 5
MATCH: 13
UNDER_REVIEW: 1
```

## Current-Only Capability Validation

| Capability | Classification | Details |
|---|---|---|
| execution_provenance | CURRENT_ONLY_VALIDATION_PASS | contract_status=pass |
| genotype_observations | CURRENT_ONLY_VALIDATION_PASS | size_bytes=705943953 |
| genotype_projection_summary | CURRENT_ONLY_VALIDATION_PASS | status=pass_with_advisory; status_source=projection.projection_status |
| native_tep_vap | CURRENT_ONLY_VALIDATION_PASS | validation=True; inventory=True; lineage=True |
| tep_execution_provenance_transport | CURRENT_ONLY_VALIDATION_PASS | canonical context transport path |
| tep_metadata_entity | CURRENT_ONLY_VALIDATION_PASS | config snapshot transport |

## Scientific Differences Under Review

| Stage | Field | Historical | Current | Delta | Classification |
|---|---|---:|---:|---:|---|
| stage_08_summary | `clinical_status.benign` | 31199 | 31200 | 1.0 | UNDER_REVIEW |
| stage_08_summary | `clinical_status.likely_benign` | 1958 | 1959 | 1.0 | UNDER_REVIEW |
| stage_08_summary | `clinical_status.missing` | 702717 | 702754 | 37.0 | UNDER_REVIEW |
| stage_08_summary | `clinical_status.vus` | 459 | 460 | 1.0 | UNDER_REVIEW |
| stage_08_summary | `frequency_status.common` | 636061 | 636071 | 10.0 | UNDER_REVIEW |
| stage_08_summary | `frequency_status.low_frequency` | 30205 | 30198 | -7.0 | UNDER_REVIEW |
| stage_08_summary | `frequency_status.missing` | 27397 | 27434 | 37.0 | UNDER_REVIEW |
| stage_08_summary | `interpretability_counts.interpretable_now` | 26439 | 26451 | 12.0 | UNDER_REVIEW |
| stage_08_summary | `interpretability_counts.needs_external_annotation` | 697955 | 697983 | 28.0 | UNDER_REVIEW |
| stage_08_summary | `partition_counts.coding_candidates` | 24041 | 24053 | 12.0 | UNDER_REVIEW |
| stage_08_summary | `partition_counts.noncoding_candidates` | 710029 | 710057 | 28.0 | UNDER_REVIEW |
| stage_08_summary | `partition_qc_counts.coding_candidates_context::coding` | 23548 | 23560 | 12.0 | UNDER_REVIEW |
| stage_08_summary | `partition_qc_counts.noncoding_candidates_context::intergenic` | 115823 | 115865 | 42.0 | UNDER_REVIEW |
| stage_08_summary | `partition_qc_counts.noncoding_candidates_context::intronic` | 459180 | 459181 | 1.0 | UNDER_REVIEW |
| stage_08_summary | `partition_qc_counts.noncoding_candidates_context::noncoding_transcript` | 16107 | 16099 | -8.0 | UNDER_REVIEW |
| stage_08_summary | `partition_qc_counts.noncoding_candidates_context::regulatory` | 106845 | 106838 | -7.0 | UNDER_REVIEW |
| stage_08_summary | `partition_qc_counts.selected_context::coding` | 23548 | 23560 | 12.0 | UNDER_REVIEW |
| stage_08_summary | `partition_qc_counts.selected_context::intergenic` | 115823 | 115865 | 42.0 | UNDER_REVIEW |
| stage_08_summary | `partition_qc_counts.selected_context::intronic` | 459180 | 459181 | 1.0 | UNDER_REVIEW |
| stage_08_summary | `partition_qc_counts.selected_context::noncoding_transcript` | 16107 | 16099 | -8.0 | UNDER_REVIEW |
| stage_08_summary | `partition_qc_counts.selected_context::regulatory` | 106845 | 106838 | -7.0 | UNDER_REVIEW |
| stage_08_summary | `qc_status_counts.pass` | 724394 | 724434 | 40.0 | UNDER_REVIEW |
| stage_08_summary | `total_variants` | 736468 | 736508 | 40.0 | UNDER_REVIEW |
| stage_08_summary | `variant_summary_rows` | 736468 | 736508 | 40.0 | UNDER_REVIEW |
| stage_08_summary | `variants_by_context.coding` | 23548 | 23560 | 12.0 | UNDER_REVIEW |
| stage_08_summary | `variants_by_context.intergenic` | 115823 | 115865 | 42.0 | UNDER_REVIEW |
| stage_08_summary | `variants_by_context.intronic` | 459180 | 459181 | 1.0 | UNDER_REVIEW |
| stage_08_summary | `variants_by_context.noncoding_transcript` | 16107 | 16099 | -8.0 | UNDER_REVIEW |
| stage_08_summary | `variants_by_context.regulatory` | 106845 | 106838 | -7.0 | UNDER_REVIEW |
| stage_08_summary | `variants_by_severity.LOW` | 17329 | 17334 | 5.0 | UNDER_REVIEW |
| stage_08_summary | `variants_by_severity.MODERATE` | 11750 | 11757 | 7.0 | UNDER_REVIEW |
| stage_08_summary | `variants_by_severity.MODIFIER` | 706922 | 706950 | 28.0 | UNDER_REVIEW |
| stage_08_summary | `variants_by_variant_class.coding` | 26439 | 26451 | 12.0 | UNDER_REVIEW |
| stage_08_summary | `variants_by_variant_class.noncoding` | 697955 | 697983 | 28.0 | UNDER_REVIEW |
| stage_08_summary | `variants_by_variant_type.complex` | 3717 | 3719 | 2.0 | UNDER_REVIEW |
| stage_08_summary | `variants_by_variant_type.deletion` | 80153 | 80165 | 12.0 | UNDER_REVIEW |
| stage_08_summary | `variants_by_variant_type.indel` | 207 | 208 | 1.0 | UNDER_REVIEW |
| stage_08_summary | `variants_by_variant_type.insertion` | 53675 | 53676 | 1.0 | UNDER_REVIEW |
| stage_08_summary | `variants_by_variant_type.snv` | 598716 | 598740 | 24.0 | UNDER_REVIEW |
| stage_09_summary | `benign_or_likely_benign_count` | 7536 | 7538 | 2.0 | UNDER_REVIEW |
| stage_09_summary | `clinical_evidence_distribution.benign` | 6794 | 6795 | 1.0 | UNDER_REVIEW |
| stage_09_summary | `clinical_evidence_distribution.likely_benign` | 742 | 743 | 1.0 | UNDER_REVIEW |
| stage_09_summary | `clinical_evidence_distribution.missing` | 18558 | 18567 | 9.0 | UNDER_REVIEW |
| stage_09_summary | `clinical_evidence_distribution.vus` | 254 | 255 | 1.0 | UNDER_REVIEW |
| stage_09_summary | `coding_interpretation_label_distribution.coding_common_or_low_support` | 24855 | 24867 | 12.0 | UNDER_REVIEW |
| stage_09_summary | `coding_interpretation_label_distribution.coding_uninterpretable` | 432 | 431 | -1.0 | UNDER_REVIEW |
| stage_09_summary | `coding_interpretation_label_distribution.lof_or_missense_rare` | 1148 | 1149 | 1.0 | UNDER_REVIEW |
| stage_09_summary | `common_variant_count` | 23460 | 23470 | 10.0 | UNDER_REVIEW |
| stage_09_summary | `input_rows` | 26439 | 26451 | 12.0 | UNDER_REVIEW |
| stage_09_summary | `interpreted_rows` | 26439 | 26451 | 12.0 | UNDER_REVIEW |
| stage_09_summary | `missense_variant_count` | 11375 | 11382 | 7.0 | UNDER_REVIEW |
| stage_09_summary | `rare_variant_count` | 1404 | 1405 | 1.0 | UNDER_REVIEW |
| stage_09_summary | `rarity_flag_distribution.common` | 23460 | 23470 | 10.0 | UNDER_REVIEW |
| stage_09_summary | `rarity_flag_distribution.rare` | 1404 | 1405 | 1.0 | UNDER_REVIEW |
| stage_09_summary | `total_coding_variants` | 26439 | 26451 | 12.0 | UNDER_REVIEW |
| stage_09_summary | `uninterpretable_count` | 432 | 431 | -1.0 | UNDER_REVIEW |
| stage_10_summary | `clinical_evidence_distribution.missing` | 684159 | 684187 | 28.0 | UNDER_REVIEW |
| stage_10_summary | `input_rows` | 710029 | 710057 | 28.0 | UNDER_REVIEW |
| stage_10_summary | `intergenic_variant_count` | 115823 | 115865 | 42.0 | UNDER_REVIEW |
| stage_10_summary | `interpreted_rows` | 710029 | 710057 | 28.0 | UNDER_REVIEW |
| stage_10_summary | `intronic_variant_count` | 317908 | 317900 | -8.0 | UNDER_REVIEW |
| stage_10_summary | `low_frequency_variant_count` | 28854 | 28847 | -7.0 | UNDER_REVIEW |
| stage_10_summary | `noncoding_functional_context_distribution.intergenic` | 115823 | 115865 | 42.0 | UNDER_REVIEW |
| stage_10_summary | `noncoding_functional_context_distribution.intronic` | 317908 | 317900 | -8.0 | UNDER_REVIEW |
| stage_10_summary | `noncoding_functional_context_distribution.proximal` | 106839 | 106832 | -7.0 | UNDER_REVIEW |
| stage_10_summary | `noncoding_functional_context_distribution.transcript_associated` | 157379 | 157380 | 1.0 | UNDER_REVIEW |
| stage_10_summary | `noncoding_interpretation_label_distribution.noncoding_common_or_low_support` | 556082 | 556076 | -6.0 | UNDER_REVIEW |
| stage_10_summary | `noncoding_interpretation_label_distribution.noncoding_uninterpretable` | 127903 | 127945 | 42.0 | UNDER_REVIEW |
| stage_10_summary | `noncoding_interpretation_label_distribution.regulatory_or_transcript_rare` | 26044 | 26036 | -8.0 | UNDER_REVIEW |
| stage_10_summary | `proximal_variant_count` | 106839 | 106832 | -7.0 | UNDER_REVIEW |
| stage_10_summary | `rare_variant_count` | 41401 | 41400 | -1.0 | UNDER_REVIEW |
| stage_10_summary | `rarity_flag_distribution.low_frequency` | 28854 | 28847 | -7.0 | UNDER_REVIEW |
| stage_10_summary | `rarity_flag_distribution.rare` | 41401 | 41400 | -1.0 | UNDER_REVIEW |
| stage_10_summary | `total_noncoding_variants` | 710029 | 710057 | 28.0 | UNDER_REVIEW |
| stage_10_summary | `transcript_associated_variant_count` | 157379 | 157380 | 1.0 | UNDER_REVIEW |
| stage_10_summary | `uninterpretable_count` | 127903 | 127945 | 42.0 | UNDER_REVIEW |
| stage_11_summary | `counts_by_gene_id_top_50.ENSG00000055609` | 284 | 285 | 1.0 | UNDER_REVIEW |
| stage_11_summary | `counts_by_gene_id_top_50.ENSG00000141837` | 249 | 248 | -1.0 | UNDER_REVIEW |
| stage_11_summary | `counts_by_gene_id_top_50.ENSG00000155093` | 461 | 466 | 5.0 | UNDER_REVIEW |
| stage_11_summary | `counts_by_gene_id_top_50.ENSG00000169894` | 522 | 517 | -5.0 | UNDER_REVIEW |
| stage_11_summary | `counts_by_gene_id_top_50.ENSG00000172264` | 299 | 298 | -1.0 | UNDER_REVIEW |
| stage_11_summary | `counts_by_gene_id_top_50.ENSG00000172969` | 271 | 268 | -3.0 | UNDER_REVIEW |
| stage_11_summary | `counts_by_gene_id_top_50.ENSG00000198010` | 365 | 364 | -1.0 | UNDER_REVIEW |
| stage_11_summary | `counts_by_gene_id_top_50.ENSG00000259154` | 262 | 272 | 10.0 | UNDER_REVIEW |
| stage_11_summary | `counts_by_gene_id_top_50.ENSG00000293035` | 321 | 327 | 6.0 | UNDER_REVIEW |
| stage_11_summary | `counts_by_gene_id_top_50.NA` | 115823 | 115865 | 42.0 | UNDER_REVIEW |
| stage_11_summary | `counts_by_priority_rank.2` | 27192 | 27185 | -7.0 | UNDER_REVIEW |
| stage_11_summary | `counts_by_priority_rank.3` | 580937 | 580943 | 6.0 | UNDER_REVIEW |
| stage_11_summary | `counts_by_priority_rank.4` | 128335 | 128376 | 41.0 | UNDER_REVIEW |
| stage_11_summary | `counts_by_priority_tier.tier_2_moderate_candidate` | 27192 | 27185 | -7.0 | UNDER_REVIEW |
| stage_11_summary | `counts_by_priority_tier.tier_3_low_support_or_common` | 580937 | 580943 | 6.0 | UNDER_REVIEW |
| stage_11_summary | `counts_by_priority_tier.tier_4_uninterpretable_or_qc_limited` | 128335 | 128376 | 41.0 | UNDER_REVIEW |
| stage_11_summary | `counts_by_source_interpretation_label.coding_common_or_low_support` | 24855 | 24867 | 12.0 | UNDER_REVIEW |
| stage_11_summary | `counts_by_source_interpretation_label.coding_uninterpretable` | 432 | 431 | -1.0 | UNDER_REVIEW |
| stage_11_summary | `counts_by_source_interpretation_label.lof_or_missense_rare` | 1148 | 1149 | 1.0 | UNDER_REVIEW |
| stage_11_summary | `counts_by_source_interpretation_label.noncoding_common_or_low_support` | 556082 | 556076 | -6.0 | UNDER_REVIEW |
| stage_11_summary | `counts_by_source_interpretation_label.noncoding_uninterpretable` | 127903 | 127945 | 42.0 | UNDER_REVIEW |
| stage_11_summary | `counts_by_source_interpretation_label.regulatory_or_transcript_rare` | 26044 | 26036 | -8.0 | UNDER_REVIEW |
| stage_11_summary | `counts_by_variant_origin.coding` | 26439 | 26451 | 12.0 | UNDER_REVIEW |
| stage_11_summary | `counts_by_variant_origin.noncoding` | 710029 | 710057 | 28.0 | UNDER_REVIEW |
| stage_11_summary | `input_rows` | 736468 | 736508 | 40.0 | UNDER_REVIEW |
| stage_11_summary | `low_priority_candidate_count` | 580937 | 580943 | 6.0 | UNDER_REVIEW |
| stage_11_summary | `moderate_priority_candidate_count` | 27192 | 27185 | -7.0 | UNDER_REVIEW |
| stage_11_summary | `output_rows` | 736468 | 736508 | 40.0 | UNDER_REVIEW |
| stage_11_summary | `uninterpretable_count` | 128335 | 128376 | 41.0 | UNDER_REVIEW |
| stage_12_summary | `counts_by_priority_tier.tier_2_moderate_candidate` | 27192 | 27185 | -7.0 | UNDER_REVIEW |
| stage_12_summary | `counts_by_priority_tier.tier_3_low_support_or_common` | 580937 | 580943 | 6.0 | UNDER_REVIEW |
| stage_12_summary | `counts_by_priority_tier.tier_4_uninterpretable_or_qc_limited` | 128335 | 128376 | 41.0 | UNDER_REVIEW |
| stage_12_summary | `counts_by_suggested_validation_method.IGV` | 27196 | 27189 | -7.0 | UNDER_REVIEW |
| stage_12_summary | `counts_by_suggested_validation_method.none` | 709272 | 709319 | 47.0 | UNDER_REVIEW |
| stage_12_summary | `counts_by_validation_priority.low` | 709272 | 709319 | 47.0 | UNDER_REVIEW |
| stage_12_summary | `counts_by_validation_priority.medium` | 27192 | 27185 | -7.0 | UNDER_REVIEW |
| stage_12_summary | `counts_by_validation_required.False` | 709272 | 709319 | 47.0 | UNDER_REVIEW |
| stage_12_summary | `counts_by_validation_required.True` | 27196 | 27189 | -7.0 | UNDER_REVIEW |
| stage_12_summary | `input_rows` | 736468 | 736508 | 40.0 | UNDER_REVIEW |
| stage_12_summary | `output_rows` | 736468 | 736508 | 40.0 | UNDER_REVIEW |
| stage_13_final_summary | `counts_by_priority_rank.2` | 27192 | 27185 | -7.0 | UNDER_REVIEW |
| stage_13_final_summary | `counts_by_priority_rank.3` | 580937 | 580943 | 6.0 | UNDER_REVIEW |
| stage_13_final_summary | `counts_by_priority_rank.4` | 128335 | 128376 | 41.0 | UNDER_REVIEW |
| stage_13_final_summary | `counts_by_priority_tier.tier_2_moderate_candidate` | 27192 | 27185 | -7.0 | UNDER_REVIEW |
| stage_13_final_summary | `counts_by_priority_tier.tier_3_low_support_or_common` | 580937 | 580943 | 6.0 | UNDER_REVIEW |
| stage_13_final_summary | `counts_by_priority_tier.tier_4_uninterpretable_or_qc_limited` | 128335 | 128376 | 41.0 | UNDER_REVIEW |
| stage_13_final_summary | `counts_by_source_interpretation_label.coding_common_or_low_support` | 24855 | 24867 | 12.0 | UNDER_REVIEW |
| stage_13_final_summary | `counts_by_source_interpretation_label.coding_uninterpretable` | 432 | 431 | -1.0 | UNDER_REVIEW |
| stage_13_final_summary | `counts_by_source_interpretation_label.lof_or_missense_rare` | 1148 | 1149 | 1.0 | UNDER_REVIEW |
| stage_13_final_summary | `counts_by_source_interpretation_label.noncoding_common_or_low_support` | 556082 | 556076 | -6.0 | UNDER_REVIEW |
| stage_13_final_summary | `counts_by_source_interpretation_label.noncoding_uninterpretable` | 127903 | 127945 | 42.0 | UNDER_REVIEW |
| stage_13_final_summary | `counts_by_source_interpretation_label.regulatory_or_transcript_rare` | 26044 | 26036 | -8.0 | UNDER_REVIEW |
| stage_13_final_summary | `counts_by_suggested_validation_method.IGV` | 27196 | 27189 | -7.0 | UNDER_REVIEW |
| stage_13_final_summary | `counts_by_suggested_validation_method.none` | 709272 | 709319 | 47.0 | UNDER_REVIEW |
| stage_13_final_summary | `counts_by_validation_priority.low` | 709272 | 709319 | 47.0 | UNDER_REVIEW |
| stage_13_final_summary | `counts_by_validation_priority.medium` | 27192 | 27185 | -7.0 | UNDER_REVIEW |
| stage_13_final_summary | `counts_by_validation_required.False` | 709272 | 709319 | 47.0 | UNDER_REVIEW |
| stage_13_final_summary | `counts_by_validation_required.True` | 27196 | 27189 | -7.0 | UNDER_REVIEW |
| stage_13_final_summary | `counts_by_variant_origin.coding` | 26439 | 26451 | 12.0 | UNDER_REVIEW |
| stage_13_final_summary | `counts_by_variant_origin.noncoding` | 710029 | 710057 | 28.0 | UNDER_REVIEW |
| stage_13_final_summary | `low_priority_candidate_count` | 580937 | 580943 | 6.0 | UNDER_REVIEW |
| stage_13_final_summary | `moderate_priority_candidate_count` | 27192 | 27185 | -7.0 | UNDER_REVIEW |
| stage_13_final_summary | `prioritized_variant_count` | 736468 | 736508 | 40.0 | UNDER_REVIEW |
| stage_13_final_summary | `qc_status_by_stage.stage_11.input_rows` | 736468 | 736508 | 40.0 | UNDER_REVIEW |
| stage_13_final_summary | `qc_status_by_stage.stage_11.output_rows` | 736468 | 736508 | 40.0 | UNDER_REVIEW |
| stage_13_final_summary | `qc_status_by_stage.stage_12.input_rows` | 736468 | 736508 | 40.0 | UNDER_REVIEW |
| stage_13_final_summary | `qc_status_by_stage.stage_12.output_rows` | 736468 | 736508 | 40.0 | UNDER_REVIEW |
| stage_13_final_summary | `top_gene_variant_counts` | [{"gene_id": "NA", "variant_count": "115823"}, {"gene_id": "ENSG00000078328", "variant_count": "751"}, {"gene_id": "ENSG00000183117", "variant_count": "668"}, {"gene_id": "ENSG00000169894", "variant_count": "522"}, {"gene_id": "ENSG00000155093", "variant_count": "461"}, {"gene_id": "ENSG00000181143", "variant_count": "416"}, {"gene_id": "ENSG00000186153", "variant_count": "401"}, {"gene_id": "ENSG00000290523", "variant_count": "386"}, {"gene_id": "ENSG00000185345", "variant_count": "366"}, {"gene_id": "ENSG00000198010", "variant_count": "365"}] | [{"gene_id": "NA", "variant_count": "115865"}, {"gene_id": "ENSG00000078328", "variant_count": "751"}, {"gene_id": "ENSG00000183117", "variant_count": "668"}, {"gene_id": "ENSG00000169894", "variant_count": "517"}, {"gene_id": "ENSG00000155093", "variant_count": "466"}, {"gene_id": "ENSG00000181143", "variant_count": "416"}, {"gene_id": "ENSG00000186153", "variant_count": "401"}, {"gene_id": "ENSG00000290523", "variant_count": "386"}, {"gene_id": "ENSG00000185345", "variant_count": "366"}, {"gene_id": "ENSG00000198010", "variant_count": "364"}] |  | UNDER_REVIEW |
| stage_13_final_summary | `total_variants_processed` | 736468 | 736508 | 40.0 | UNDER_REVIEW |
| stage_13_final_summary | `uninterpretable_count` | 128335 | 128376 | 41.0 | UNDER_REVIEW |
| stage_13_final_summary | `validation_candidate_count` | 736468 | 736508 | 40.0 | UNDER_REVIEW |
| stage_13_final_summary | `validation_required_count` | 27196 | 27189 | -7.0 | UNDER_REVIEW |

## Shared Tabular Surfaces

| Table | Historical Rows | Current Rows | Delta | Shared Columns | Classification |
|---|---:|---:|---:|---:|---|
| `stage_09_coding_interpreted.tsv` | 26439 | 26451 | 12 | 43 | UNDER_REVIEW |

## Certified Case-Study Surfaces

Recognized certified surfaces inventoried: 84017.

Version 0.8 compares supported certified surfaces independently for each historical run and retains unsupported multidimensional surfaces as explicitly not comparable.

## Historical Evidence Limitations

- The historical local run is a lightweight extraction, not a complete MARK execution snapshot.
- The current run includes execution provenance, elevated genotype, metadata transport, and fresh native TEP-VAP emission introduced after the historical run.
- Missing historical artifacts are classified as unavailable rather than mismatched.
- Case-study tables are curated surfaces and do not substitute for absent historical full-row artifacts.
- Hardware causality cannot be inferred unless software, configuration, annotation, reference, and resource identities are equivalent.
- Version 0.9 preserves ecosystem missingness semantics by distinguishing lexical nonemptiness, explicit missing sentinels, explicit not-applicable states, and true semantic value presence while retaining the v0.8 certification gates; historical noncoding identity evidence and complete upstream historical attribution remain unavailable.

## Bounded Conclusion

The comparison result is `SCIENTIFIC_DIFFERENCE_UNDER_REVIEW`.

Operational validity, TEP validity, historical coverage, stage-summary reproducibility, semantic reproducibility, row-level reproducibility, and current-only capability validation remain distinct conclusions.

## Output Artifacts

- `comparison_manifest.json`
- `comparison_receipt.json`
- `current_artifact_inventory.tsv`
- `historical_artifact_inventory.tsv`
- `shared_artifact_inventory.tsv`
- `historical_availability_report.tsv`
- `stage_summary_comparison.tsv`
- `tabular_schema_comparison.tsv`
- `keyed_table_comparison_summary.tsv`
- `unmatched_variant_keys.tsv`
- `keyed_shared_row_differences.tsv`
- `scientific_variant_differences.tsv`
- `column_distribution_comparison.tsv`
- `numeric_column_summary_comparison.tsv`
- `semantic_surface_comparison.tsv`
- `case_study_surface_derivation.tsv`
- `case_study_comparison_summary.json`
- `tep_comparison_input_integrity.tsv`
- `tep_comparison_input_integrity_summary.json`
- `genotype_schema_inventory.tsv`
- `genotype_schema_resolution.tsv`
- `genotype_schema_summary.json`
- `sage_review_manifest.json`
- `sage_review_manifest.md`
- `current_only_capability_validation.tsv`
- `comparison_report.md`
