# SAGE-VAP Comparison Review Manifest

- Comparison ID: `run_2026_07_14_114546_vs_run_2026_05_27_172531`
- Script version: `0.9.0`
- Review status: `READY_FOR_SAGE_REVIEW`
- Overall comparison result: `SCIENTIFIC_DIFFERENCE_UNDER_REVIEW`
- Genotype elevation closure: `PASS_WITH_BOUNDED_LIMITATIONS`
- TEP input integrity: `pass`
- Genotype schema status: `pass`

## Review Questions

- Does the evidence support certification that genotype elevation is transport-valid and scientifically coherent?
- Is source-record context recovery with explicit complex-relationship deferral acceptable for multiallelic records?
- Are the bounded historical noncoding and earliest-divergence limitations acceptable?
- Are any additional scientific controls required before VDB ingestion?

## Declared Limitations

- The historical local run is a lightweight extraction, not a complete MARK execution snapshot.
- The current run includes execution provenance, elevated genotype, metadata transport, and fresh native TEP-VAP emission introduced after the historical run.
- Missing historical artifacts are classified as unavailable rather than mismatched.
- Case-study tables are curated surfaces and do not substitute for absent historical full-row artifacts.
- Hardware causality cannot be inferred unless software, configuration, annotation, reference, and resource identities are equivalent.
- Version 0.9 preserves ecosystem missingness semantics by distinguishing lexical nonemptiness, explicit missing sentinels, explicit not-applicable states, and true semantic value presence while retaining the v0.8 certification gates; historical noncoding identity evidence and complete upstream historical attribution remain unavailable.

## Included Evidence

- `case_study_comparison_summary.json`
- `case_study_surface_derivation.tsv`
- `column_distribution_comparison.tsv`
- `comparison_manifest.json`
- `comparison_receipt.json`
- `comparison_report.md`
- `current_artifact_inventory.tsv`
- `current_only_capability_validation.tsv`
- `genotype_column_resolution.tsv`
- `genotype_elevation_closure_summary.json`
- `genotype_elevation_closure_summary.md`
- `genotype_schema_inventory.tsv`
- `genotype_schema_resolution.tsv`
- `genotype_schema_summary.json`
- `historical_artifact_inventory.tsv`
- `historical_availability_report.tsv`
- `keyed_shared_row_differences.tsv`
- `keyed_table_comparison_summary.tsv`
- `numeric_column_summary_comparison.tsv`
- `representative_genotype_exemplars.tsv`
- `sage_review_manifest.json`
- `sage_review_manifest.md`
- `scientific_variant_differences.tsv`
- `semantic_surface_comparison.tsv`
- `shared_artifact_inventory.tsv`
- `stage_summary_comparison.tsv`
- `tabular_schema_comparison.tsv`
- `tep_comparison_input_integrity.tsv`
- `tep_comparison_input_integrity_summary.json`
- `unmatched_variant_keys.tsv`
- `variant_delta_dossier.md`
- `variant_delta_dossier.tsv`
- `variant_delta_dossier_summary.tsv`
- `variant_delta_field_availability.tsv`
- `variant_delta_lineage_matrix.tsv`
- `variant_delta_locus_pairing.tsv`
