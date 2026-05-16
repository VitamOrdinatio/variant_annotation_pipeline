# VAP v1 Evidence Harvest Attack Vector

## Goal
Generate small, deterministic, figure-ready case-study tables from VAP run metadata and stage summaries.

## Primary v1 Claims
1. VAP funnels raw NGS calls into structured candidate evidence.
2. VAP reproduces biological outputs across repeated runs.
3. VAP preserves provenance at run, stage, artifact, and configuration levels.
4. VAP generates GSC-overlay-ready gene-level evidence.
5. VAP exposes runtime and stage bottlenecks.
6. VAP summarizes coding/noncoding biological consequence structure.

## Tier 1 Inputs: Metadata-first
Use small files first:
- metadata/run_metadata.json
- metadata/run_fingerprint.json
- metadata/runtime_profile.tsv
- processed/stage_08_summary.json
- processed/stage_09_summary.json
- processed/stage_10_summary.json
- processed/stage_11_summary.json
- processed/stage_12_summary.json
- processed/stage_13_final_summary.json
- processed/stage_13_run_report.md
- processed/stage_13_artifact_manifest.json

## Tier 1 Outputs
Create:
- docs/case_studies/tables/stage_funnel_summary.tsv
- docs/case_studies/tables/runtime_stage_summary.tsv
- docs/case_studies/tables/coding_noncoding_consequence_summary.tsv
- docs/case_studies/tables/clinical_status_summary.tsv
- docs/case_studies/tables/priority_tier_summary.tsv
- docs/case_studies/tables/validation_readiness_summary.tsv
- docs/case_studies/tables/provenance_summary.tsv

## Tier 2 Inputs: Large TSVs only when needed
Use stage_11_prioritized_variants.tsv only for:
- GSC overlay intersections
- candidate spotlight variants
- gene-symbol-aware burden tables
- exact locus-level inspection

## Key Figure Substrates
1. Variant funnel:
   raw called → normalized → annotated → coding/noncoding → tiered priority → IGV validation candidates

2. Runtime telemetry:
   stage runtime barplot, highlighting Stage 02 alignment and Stage 05 variant calling.

3. Biological refinement:
   HIGH/MODERATE/LOW/MODIFIER impact counts and coding/noncoding consequence profiles.

4. Determinism:
   replicate run row-count stability, tier stability, validation-count stability, and summary-hash stability where appropriate.

5. GSC bridge:
   VAP gene-level evidence + phenotype-scoped GSC overlays → candidate substrate, not clinical diagnosis.

## Implementation Rule
Build metadata-first. Parse large variant tables only after summary-table harvest is stable.