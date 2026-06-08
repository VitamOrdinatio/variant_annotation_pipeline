# How to Audit Cross-Run Artifacts in VAP

## Purpose

This document explains how to traverse and audit the VAP cross-run case-study architecture using `ERR10619281` as the canonical example.

The goal is not to inspect every generated artifact individually. Instead, this guide teaches readers how to:

* navigate the 7-contrast architecture,
* understand how semantic evidence is distributed across contrasts,
* validate reproducibility surfaces,
* cross-reference independently generated exemplar case-study artifacts,
* and verify deterministic biological evidence organization across distinct `run_<id>` executions.

This document acts as a bridge between:

1. the distributed cross-run audit architecture under:

```text
docs/case_studies/cross_runs/
```

and

2. the independently generated official exemplar `ERR10619281` case study under:

[ERR10619281 case study validation](../err10619281/)

---

## Recommended Reading Strategy

This document is intentionally hyperlink-dense.

Reviewers are encouraged to:

1. read conceptually,
2. selectively descend into linked artifacts,
3. compare cross-run outputs against the independently generated exemplar `ERR10619281` case study,
4. and verify deterministic semantic stability across independent execution contexts.

The document therefore functions both as:

* an audit traversal guide,
* and a reproducibility validation bridge between independently generated artifact ecosystems.

---

# Core Concept

Independent VAP executions may differ operationally through:

* runtime,
* telemetry,
* execution identity,
* timestamps,
* and provenance lineage,

while still preserving stable downstream semantic evidence organization.

For identical SRA input, semantic topology, evidence routing, interoperability substrates, and bounded reviewability structures should remain highly stable across independent executions.

The cross-run architecture exists to demonstrate this property explicitly.

---

# Recommended Audit Entry Point

Start here:

[`docs/case_studies/cross_runs/contrasts/`](contrasts/)

This directory contains the primary distributed audit substrate for the 12-SRA cross-run architecture.

Within this directory, each contrast isolates a distinct systems-level property of VAP.

For `ERR10619281`, each contrast contains a dedicated sample-specific subtree:

```text
contrast_<XX>_<theme>/ERR10619281/
```

The seven contrasts are:

| Contrast | Theme                                 |
| -------- | ------------------------------------- |
| 01       | [Semantic governance](contrasts/contrast_01_semantic_governance/) |
| 02       | [Interoperability architecture](contrasts/contrast_02_interoperability_architecture/) |
| 03       | [Observability infrastructure](contrasts/contrast_03_observability_infrastructure/) |
| 04       | [Individualized semantic topology](contrasts/contrast_04_individualized_semantic_topology/) |
| 05       | [Semantic compression architecture](contrasts/contrast_05_semantic_compression_architecture/) |
| 06       | [Bounded reviewability governance](contrasts/contrast_06_bounded_reviewability_governance/) |
| 07       | [Deterministic provenance architecture](contrasts/contrast_07_deterministic_provenance_architecture/) |

Each of the 12 WES epilepsy SRAs exist as its own subfolder within each of the 7 contrasts.

---

# Critical Audit Principle

The cross-run contrasts are independently harvested audit surfaces derived from VAP execution artifacts.

Readers should repeatedly cross-reference these artifacts against the official exemplar `ERR10619281` case study, which functions as an "answer key" for validating:

- semantic consistency,
- substrate stability,
- figure continuity,
- and evidence-routing determinism.

---

# Official Exemplar Answer Key

Primary location: 

[`docs/case_studies/err10619281/`](../err10619281/) 

Important narrative documents: 

- [`err10619281_wes_case_study.md`](../err10619281/err10619281_wes_case_study.md)
- [`err10619281_wes_reproducibility.md`](../err10619281/err10619281_wes_reproducibility.md)

Important directories: 

- [`figures/`](../err10619281/figures/)
- [`tables/`](../err10619281/tables/)
- [`manifests/`](../err10619281/manifests/)
 
These artifacts were generated independently from the cross-run contrast architecture.

The near-identical semantic outputs across distinct executions demonstrate that VAP is:

* `run_<id>` agnostic,
* provenance-aware,
* and biologically deterministic for identical SRA input.

---

# Contrast 01 — Semantic Governance

Primary location:

[`contrast_01_semantic_governance/ERR10619281/`](contrasts/contrast_01_semantic_governance/ERR10619281/)

Key subdirectories:

- [`figures/`](contrasts/contrast_01_semantic_governance/ERR10619281/figures/)
- [`tables/`](contrasts/contrast_01_semantic_governance/ERR10619281/tables/)
- [`sql_outputs/lane_candidate_slices/`](contrasts/contrast_01_semantic_governance/ERR10619281/sql_outputs/lane_candidate_slices/)
- [`sql_outputs/value_counts/`](contrasts/contrast_01_semantic_governance/ERR10619281/sql_outputs/value_counts/)

Important figures:

- [`ERR10619281_f3a_deterministic_evidence_lineage.png`](contrasts/contrast_01_semantic_governance/ERR10619281/figures/ERR10619281_f3a_deterministic_evidence_lineage.png)
- [`ERR10619281_f3b_semantic_branching.png`](contrasts/contrast_01_semantic_governance/ERR10619281/figures/ERR10619281_f3b_semantic_branching.png)

These figures demonstrate:

- deterministic evidence routing,
- semantic partitioning,
- interpretability-aware branching,
- and downstream evidence refinement pressure.

## Answer-Key Checkpoint

Cross-reference the independently generated official exemplar artifacts:

- [`ERR10619281_f3a_deterministic_evidence_lineage.png`](../err10619281/figures/ERR10619281_f3a_deterministic_evidence_lineage.png)
- [`ERR10619281_f3b_semantic_branching.png`](../err10619281/figures/ERR10619281_f3b_semantic_branching.png)

Also inspect the independently harvested provenance/source tables:

- [`ERR10619281_f3a_deterministic_evidence_lineage_source.tsv`](../err10619281/figures/ERR10619281_f3a_deterministic_evidence_lineage_source.tsv)
- [`ERR10619281_f3a_deterministic_evidence_lineage_provenance.tsv`](../err10619281/figures/ERR10619281_f3a_deterministic_evidence_lineage_provenance.tsv)
- [`ERR10619281_f3b_semantic_branching_source.tsv`](../err10619281/figures/ERR10619281_f3b_semantic_branching_source.tsv)
- [`ERR10619281_f3b_semantic_branching_provenance.tsv`](../err10619281/figures/ERR10619281_f3b_semantic_branching_provenance.tsv)

These independently generated artifacts should exhibit stable semantic topology despite differing provenance identities and execution timestamps.

---

# Contrast 02 — Interoperability Architecture

Primary location:

[`contrast_02_interoperability_architecture/ERR10619281/`](contrasts/contrast_02_interoperability_architecture/ERR10619281/)

Key subdirectories:

* [`figures/`](contrasts/contrast_02_interoperability_architecture/ERR10619281/figures/)
* [`tables/`](contrasts/contrast_02_interoperability_architecture/ERR10619281/tables/)
* [`sql_outputs/targeted_semantic_buckets/`](contrasts/contrast_02_interoperability_architecture/ERR10619281/sql_outputs/targeted_semantic_buckets/)
* [`sql_outputs/tiered_gene_outputs/`](contrasts/contrast_02_interoperability_architecture/ERR10619281/sql_outputs/tiered_gene_outputs/)

Key figure:

* [`ERR10619281_f5_interoperability_substrates.png`](contrasts/contrast_02_interoperability_architecture/ERR10619281/figures/ERR10619281_f5_interoperability_substrates.png)

Important tables:

* [`candidate_reviewability_readiness.tsv`](contrasts/contrast_02_interoperability_architecture/ERR10619281/tables/candidate_reviewability_readiness.tsv)
* [`substrate_dimension_summary.tsv`](contrasts/contrast_02_interoperability_architecture/ERR10619281/tables/substrate_dimension_summary.tsv)
* [`gene_list_overlay_intersections.tsv`](contrasts/contrast_02_interoperability_architecture/ERR10619281/tables/gene_list_overlay_intersections.tsv)
* [`overlay_gene_coding_clinical_evidence.tsv`](contrasts/contrast_02_interoperability_architecture/ERR10619281/tables/overlay_gene_coding_clinical_evidence.tsv)
* [`overlay_gene_coding_frequency_profiles.tsv`](contrasts/contrast_02_interoperability_architecture/ERR10619281/tables/overlay_gene_coding_frequency_profiles.tsv)
* [`overlay_gene_coding_functional_impact.tsv`](contrasts/contrast_02_interoperability_architecture/ERR10619281/tables/overlay_gene_coding_functional_impact.tsv)

Important tiered gene outputs:

* [`tier1_unique_genes.tsv`](contrasts/contrast_02_interoperability_architecture/ERR10619281/sql_outputs/tiered_gene_outputs/tier1_unique_genes.tsv)
* [`tier2_unique_genes.tsv`](contrasts/contrast_02_interoperability_architecture/ERR10619281/sql_outputs/tiered_gene_outputs/tier2_unique_genes.tsv)
* [`tier3_unique_genes.tsv`](contrasts/contrast_02_interoperability_architecture/ERR10619281/sql_outputs/tiered_gene_outputs/tier3_unique_genes.tsv)

This contrast demonstrates that VAP emits deterministic downstream interoperability substrates suitable for future RDGP-, VDB-, overlay-, and cohort-scale reuse.

## Answer-Key Checkpoint

Cross-reference the independently generated official exemplar interoperability artifacts:

* [`ERR10619281_f5_interoperability_substrates.png`](../err10619281/figures/ERR10619281_f5_interoperability_substrates.png)
* [`ERR10619281_f5_interoperability_substrates.svg`](../err10619281/figures/ERR10619281_f5_interoperability_substrates.svg)

Also compare against the official exemplar support tables:

* [`candidate_reviewability_readiness.tsv`](../err10619281/tables/candidate_reviewability_readiness.tsv)
* [`gene_list_overlay_intersections.tsv`](../err10619281/tables/gene_list_overlay_intersections.tsv)
* [`overlay_gene_coding_clinical_evidence.tsv`](../err10619281/tables/overlay_gene_coding_clinical_evidence.tsv)
* [`overlay_gene_coding_frequency_profiles.tsv`](../err10619281/tables/overlay_gene_coding_frequency_profiles.tsv)
* [`overlay_gene_coding_functional_impact.tsv`](../err10619281/tables/overlay_gene_coding_functional_impact.tsv)

The interoperability architecture should remain structurally stable across independent executions even when `run_<id>` identities differ.

---

# Contrast 03 — Observability Infrastructure

Primary location:

[`contrast_03_observability_infrastructure/ERR10619281/`](contrasts/contrast_03_observability_infrastructure/ERR10619281/)

Key subdirectories:

* [`continuity_probes/`](contrasts/contrast_03_observability_infrastructure/ERR10619281/continuity_probes/)
* [`metadata/`](contrasts/contrast_03_observability_infrastructure/ERR10619281/metadata/)
* [`tables/`](contrasts/contrast_03_observability_infrastructure/ERR10619281/tables/)

Key metadata artifacts:

* [`config_snapshot.yaml`](contrasts/contrast_03_observability_infrastructure/ERR10619281/metadata/config_snapshot.yaml)
* [`run_fingerprint.json`](contrasts/contrast_03_observability_infrastructure/ERR10619281/metadata/run_fingerprint.json)
* [`run_metadata.json`](contrasts/contrast_03_observability_infrastructure/ERR10619281/metadata/run_metadata.json)
* [`runtime_profile.tsv`](contrasts/contrast_03_observability_infrastructure/ERR10619281/metadata/runtime_profile.tsv)
* [`sra_run_depth_metadata.tsv`](contrasts/contrast_03_observability_infrastructure/ERR10619281/metadata/sra_run_depth_metadata.tsv)

Key observability tables:

* [`provenance_summary.tsv`](contrasts/contrast_03_observability_infrastructure/ERR10619281/tables/provenance_summary.tsv)
* [`runtime_stage_summary.tsv`](contrasts/contrast_03_observability_infrastructure/ERR10619281/tables/runtime_stage_summary.tsv)

Continuity probe outputs:

* [`ERR10619281_tier1_unique_genes.tsv`](contrasts/contrast_03_observability_infrastructure/ERR10619281/continuity_probes/ERR10619281_tier1_unique_genes.tsv)
* [`ERR10619281_tier2_unique_genes.tsv`](contrasts/contrast_03_observability_infrastructure/ERR10619281/continuity_probes/ERR10619281_tier2_unique_genes.tsv)
* [`ERR10619281_tier3_unique_genes.tsv`](contrasts/contrast_03_observability_infrastructure/ERR10619281/continuity_probes/ERR10619281_tier3_unique_genes.tsv)

This contrast demonstrates that operational variability is observable, measurable, and separable from downstream semantic stability.

## Answer-Key Checkpoint

Cross-reference the official exemplar observability and reproducibility artifacts:

* [`err10619281_wes_reproducibility.md`](../err10619281/err10619281_wes_reproducibility.md)
* [`err10619281_f1_provenance_transition_summary.png`](../err10619281/figures/err10619281_f1_provenance_transition_summary.png)
* [`err10619281_f1_provenance_transition_summary_source.tsv`](../err10619281/figures/err10619281_f1_provenance_transition_summary_source.tsv)
* [`err10619281_f2_runtime_observability_profile.png`](../err10619281/figures/err10619281_f2_runtime_observability_profile.png)
* [`err10619281_f2_runtime_observability_profile_source.tsv`](../err10619281/figures/err10619281_f2_runtime_observability_profile_source.tsv)

Also compare against the official exemplar tables:

* [`runtime_stage_summary.tsv`](../err10619281/tables/runtime_stage_summary.tsv)
* [`provenance_summary.tsv`](../err10619281/tables/provenance_summary.tsv)
* [`run_reproducibility_summary.tsv`](../err10619281/tables/run_reproducibility_summary.tsv)

Runtime and provenance details may vary across executions. Semantic governance topology should remain stable.

---

# Contrast 04 — Individualized Semantic Topology

Primary location:

[`contrast_04_individualized_semantic_topology/ERR10619281/`](contrasts/contrast_04_individualized_semantic_topology/ERR10619281/)

Key subdirectories:

* [`figures/`](contrasts/contrast_04_individualized_semantic_topology/ERR10619281/figures/)
* [`tables/`](contrasts/contrast_04_individualized_semantic_topology/ERR10619281/tables/)
* [`sql_outputs/overlay_tiered_gene_outputs/`](contrasts/contrast_04_individualized_semantic_topology/ERR10619281/sql_outputs/overlay_tiered_gene_outputs/)

Key figure:

* [`ERR10619281_f5_interoperability_substrates.png`](contrasts/contrast_04_individualized_semantic_topology/ERR10619281/figures/ERR10619281_f5_interoperability_substrates.png)

Important overlay-tiered outputs:

* [`ERR10619281_tier1_unique_genes_mito_epi_overlay.tsv`](contrasts/contrast_04_individualized_semantic_topology/ERR10619281/sql_outputs/overlay_tiered_gene_outputs/ERR10619281_tier1_unique_genes_mito_epi_overlay.tsv)
* [`ERR10619281_tier2_unique_genes_mito_epi_overlay.tsv`](contrasts/contrast_04_individualized_semantic_topology/ERR10619281/sql_outputs/overlay_tiered_gene_outputs/ERR10619281_tier2_unique_genes_mito_epi_overlay.tsv)
* [`ERR10619281_tier3_unique_genes_mito_epi_overlay.tsv`](contrasts/contrast_04_individualized_semantic_topology/ERR10619281/sql_outputs/overlay_tiered_gene_outputs/ERR10619281_tier3_unique_genes_mito_epi_overlay.tsv)

Important tables:

* [`gene_list_overlay_intersections.tsv`](contrasts/contrast_04_individualized_semantic_topology/ERR10619281/tables/gene_list_overlay_intersections.tsv)
* [`overlay_gene_coding_clinical_evidence.tsv`](contrasts/contrast_04_individualized_semantic_topology/ERR10619281/tables/overlay_gene_coding_clinical_evidence.tsv)

This contrast demonstrates that semantic governance can remain stable while individualized biological evidence topology is preserved.

## Answer-Key Checkpoint

Compare against the official exemplar case-study narrative and overlay tables:

* [`err10619281_wes_case_study.md`](../err10619281/err10619281_wes_case_study.md)
* [`gene_list_overlay_intersections.tsv`](../err10619281/tables/gene_list_overlay_intersections.tsv)
* [`overlay_gene_coding_clinical_evidence.tsv`](../err10619281/tables/overlay_gene_coding_clinical_evidence.tsv)
* [`overlay_gene_coding_frequency_profiles.tsv`](../err10619281/tables/overlay_gene_coding_frequency_profiles.tsv)
* [`overlay_gene_coding_functional_impact.tsv`](../err10619281/tables/overlay_gene_coding_functional_impact.tsv)

The cross-run contrast should preserve individualized contextual topology while remaining compatible with the official exemplar interpretation surface.

---

# Contrast 05 — Semantic Compression Architecture

Primary location:

[`contrast_05_semantic_compression_architecture/ERR10619281/`](contrasts/contrast_05_semantic_compression_architecture/ERR10619281/)

Key subdirectories:

* [`figures/`](contrasts/contrast_05_semantic_compression_architecture/ERR10619281/figures/)
* [`tables/`](contrasts/contrast_05_semantic_compression_architecture/ERR10619281/tables/)
* [`sql_outputs/targeted_semantic_buckets/`](contrasts/contrast_05_semantic_compression_architecture/ERR10619281/sql_outputs/targeted_semantic_buckets/)
* [`sql_outputs/value_counts/`](contrasts/contrast_05_semantic_compression_architecture/ERR10619281/sql_outputs/value_counts/)

Coding figure family:

* [`ERR10619281_f4a_clinvar_significance.png`](contrasts/contrast_05_semantic_compression_architecture/ERR10619281/figures/ERR10619281_f4a_clinvar_significance.png)
* [`ERR10619281_f4a_consequence.png`](contrasts/contrast_05_semantic_compression_architecture/ERR10619281/figures/ERR10619281_f4a_consequence.png)
* [`ERR10619281_f4a_pop_freq_bins.png`](contrasts/contrast_05_semantic_compression_architecture/ERR10619281/figures/ERR10619281_f4a_pop_freq_bins.png)

Noncoding figure family:

* [`ERR10619281_f4b_clinvar_significance.png`](contrasts/contrast_05_semantic_compression_architecture/ERR10619281/figures/ERR10619281_f4b_clinvar_significance.png)
* [`ERR10619281_f4b_consequence.png`](contrasts/contrast_05_semantic_compression_architecture/ERR10619281/figures/ERR10619281_f4b_consequence.png)
* [`ERR10619281_f4b_pop_freq_bins.png`](contrasts/contrast_05_semantic_compression_architecture/ERR10619281/figures/ERR10619281_f4b_pop_freq_bins.png)

Important tables:

* [`clinical_status_summary.tsv`](contrasts/contrast_05_semantic_compression_architecture/ERR10619281/tables/clinical_status_summary.tsv)
* [`coding_noncoding_consequence_summary.tsv`](contrasts/contrast_05_semantic_compression_architecture/ERR10619281/tables/coding_noncoding_consequence_summary.tsv)
* [`variant_consequence_summary.tsv`](contrasts/contrast_05_semantic_compression_architecture/ERR10619281/tables/variant_consequence_summary.tsv)

Representative value-count outputs:

* [`value_counts__clinvar_significance.tsv`](contrasts/contrast_05_semantic_compression_architecture/ERR10619281/sql_outputs/value_counts/value_counts__clinvar_significance.tsv)
* [`value_counts__clinical_significance.tsv`](contrasts/contrast_05_semantic_compression_architecture/ERR10619281/sql_outputs/value_counts/value_counts__clinical_significance.tsv)
* [`value_counts__consequence.tsv`](contrasts/contrast_05_semantic_compression_architecture/ERR10619281/sql_outputs/value_counts/value_counts__consequence.tsv)
* [`value_counts__priority_tier.tsv`](contrasts/contrast_05_semantic_compression_architecture/ERR10619281/sql_outputs/value_counts/value_counts__priority_tier.tsv)

This contrast demonstrates semantic compression of high-dimensional evidence into interpretable governance surfaces while preserving coding and noncoding evidence structure.

## Answer-Key Checkpoint

Cross-reference the official exemplar semantic composition figures:

* [`ERR10619281_f4a_clinvar_significance.png`](../err10619281/figures/ERR10619281_f4a_clinvar_significance.png)
* [`ERR10619281_f4a_consequence.png`](../err10619281/figures/ERR10619281_f4a_consequence.png)
* [`ERR10619281_f4a_pop_freq_bins.png`](../err10619281/figures/ERR10619281_f4a_pop_freq_bins.png)
* [`ERR10619281_f4b_clinvar_significance.png`](../err10619281/figures/ERR10619281_f4b_clinvar_significance.png)
* [`ERR10619281_f4b_consequence.png`](../err10619281/figures/ERR10619281_f4b_consequence.png)
* [`ERR10619281_f4b_pop_freq_bins.png`](../err10619281/figures/ERR10619281_f4b_pop_freq_bins.png)

Also compare against the official exemplar tables:

* [`clinical_status_summary.tsv`](../err10619281/tables/clinical_status_summary.tsv)
* [`coding_noncoding_consequence_summary.tsv`](../err10619281/tables/coding_noncoding_consequence_summary.tsv)
* [`variant_consequence_summary.tsv`](../err10619281/tables/variant_consequence_summary.tsv)

Readers should observe highly stable semantic distributions, such as coding ClinVar significance structure and coding/noncoding consequence organization, despite distinct provenance identities.

---

# Contrast 06 — Bounded Reviewability Governance

Primary location:

[`contrast_06_bounded_reviewability_governance/ERR10619281/`](contrasts/contrast_06_bounded_reviewability_governance/ERR10619281/)

Key subdirectories:

* [`tables/`](contrasts/contrast_06_bounded_reviewability_governance/ERR10619281/tables/)
* [`sql_outputs/targeted_semantic_buckets/`](contrasts/contrast_06_bounded_reviewability_governance/ERR10619281/sql_outputs/targeted_semantic_buckets/)
* [`sql_outputs/unique_genes/`](contrasts/contrast_06_bounded_reviewability_governance/ERR10619281/sql_outputs/unique_genes/)

Important tables:

* [`candidate_reviewability_readiness.tsv`](contrasts/contrast_06_bounded_reviewability_governance/ERR10619281/tables/candidate_reviewability_readiness.tsv)
* [`priority_tier_summary.tsv`](contrasts/contrast_06_bounded_reviewability_governance/ERR10619281/tables/priority_tier_summary.tsv)
* [`substrate_dimension_summary.tsv`](contrasts/contrast_06_bounded_reviewability_governance/ERR10619281/tables/substrate_dimension_summary.tsv)

Representative targeted semantic buckets:

* [`ERR10619281_bucket_1a_validation_routed_epilepsy_mito.tsv`](contrasts/contrast_06_bounded_reviewability_governance/ERR10619281/sql_outputs/targeted_semantic_buckets/ERR10619281_bucket_1a_validation_routed_epilepsy_mito.tsv)
* [`ERR10619281_bucket_1b_clinically_contextualized_epilepsy_mito.tsv`](contrasts/contrast_06_bounded_reviewability_governance/ERR10619281/sql_outputs/targeted_semantic_buckets/ERR10619281_bucket_1b_clinically_contextualized_epilepsy_mito.tsv)
* [`ERR10619281_bucket_2a_rare_impact_coding_triage_summary.tsv`](contrasts/contrast_06_bounded_reviewability_governance/ERR10619281/sql_outputs/targeted_semantic_buckets/ERR10619281_bucket_2a_rare_impact_coding_triage_summary.tsv)
* [`ERR10619281_bucket_2b_rare_impact_tier2.tsv`](contrasts/contrast_06_bounded_reviewability_governance/ERR10619281/sql_outputs/targeted_semantic_buckets/ERR10619281_bucket_2b_rare_impact_tier2.tsv)
* [`ERR10619281_bucket_2c_rare_impact_deprioritized.tsv`](contrasts/contrast_06_bounded_reviewability_governance/ERR10619281/sql_outputs/targeted_semantic_buckets/ERR10619281_bucket_2c_rare_impact_deprioritized.tsv)

Unique-gene continuity outputs:

* [`ERR10619281_tier1_unique_genes.tsv`](contrasts/contrast_06_bounded_reviewability_governance/ERR10619281/sql_outputs/unique_genes/ERR10619281_tier1_unique_genes.tsv)
* [`ERR10619281_tier2_unique_genes.tsv`](contrasts/contrast_06_bounded_reviewability_governance/ERR10619281/sql_outputs/unique_genes/ERR10619281_tier2_unique_genes.tsv)
* [`ERR10619281_tier3_unique_genes.tsv`](contrasts/contrast_06_bounded_reviewability_governance/ERR10619281/sql_outputs/unique_genes/ERR10619281_tier3_unique_genes.tsv)
* [`ERR10619281_tier1_unique_genes_mito_epi_overlay.tsv`](contrasts/contrast_06_bounded_reviewability_governance/ERR10619281/sql_outputs/unique_genes/ERR10619281_tier1_unique_genes_mito_epi_overlay.tsv)
* [`ERR10619281_tier2_unique_genes_mito_epi_overlay.tsv`](contrasts/contrast_06_bounded_reviewability_governance/ERR10619281/sql_outputs/unique_genes/ERR10619281_tier2_unique_genes_mito_epi_overlay.tsv)
* [`ERR10619281_tier3_unique_genes_mito_epi_overlay.tsv`](contrasts/contrast_06_bounded_reviewability_governance/ERR10619281/sql_outputs/unique_genes/ERR10619281_tier3_unique_genes_mito_epi_overlay.tsv)

This contrast demonstrates that VAP constrains escalation pressure while preserving semantic evidence richness.

## Answer-Key Checkpoint

Compare against the official exemplar tables:

* [`candidate_reviewability_readiness.tsv`](../err10619281/tables/candidate_reviewability_readiness.tsv)
* [`priority_tier_summary.tsv`](../err10619281/tables/priority_tier_summary.tsv)
* [`gene_list_overlay_intersections.tsv`](../err10619281/tables/gene_list_overlay_intersections.tsv)

Also inspect the exemplar manifests that describe official artifact governance:

* [`table_manifest.tsv`](../err10619281/manifests/table_manifest.tsv)
* [`stage12_bucket_manifest.tsv`](../err10619281/manifests/stage12_bucket_manifest.tsv)
* [`stage12_sql_manifest.tsv`](../err10619281/manifests/stage12_sql_manifest.tsv)

The prioritization and reviewability architecture should remain stable across independent executions.

---

# Contrast 07 — Deterministic Provenance Architecture

Primary location:

[`contrast_07_deterministic_provenance_architecture/ERR10619281/`](contrasts/contrast_07_deterministic_provenance_architecture/ERR10619281/)

Key subdirectories:

* [`metrics/`](contrasts/contrast_07_deterministic_provenance_architecture/ERR10619281/metrics/)
* [`tables/`](contrasts/contrast_07_deterministic_provenance_architecture/ERR10619281/tables/)

Important stage metrics:

* [`stage_05_variant_calling_metrics.json`](contrasts/contrast_07_deterministic_provenance_architecture/ERR10619281/metrics/stage_05_variant_calling_metrics.json)
* [`stage_06_normalization_metrics.json`](contrasts/contrast_07_deterministic_provenance_architecture/ERR10619281/metrics/stage_06_normalization_metrics.json)
* [`stage_07_annotation_metrics.json`](contrasts/contrast_07_deterministic_provenance_architecture/ERR10619281/metrics/stage_07_annotation_metrics.json)
* [`stage_08_partition_metrics.json`](contrasts/contrast_07_deterministic_provenance_architecture/ERR10619281/metrics/stage_08_partition_metrics.json)
* [`stage_09_coding_interpretation_metrics.json`](contrasts/contrast_07_deterministic_provenance_architecture/ERR10619281/metrics/stage_09_coding_interpretation_metrics.json)
* [`stage_10_noncoding_interpretation_metrics.json`](contrasts/contrast_07_deterministic_provenance_architecture/ERR10619281/metrics/stage_10_noncoding_interpretation_metrics.json)
* [`stage_11_prioritization_metrics.json`](contrasts/contrast_07_deterministic_provenance_architecture/ERR10619281/metrics/stage_11_prioritization_metrics.json)
* [`stage_12_validation_metrics.json`](contrasts/contrast_07_deterministic_provenance_architecture/ERR10619281/metrics/stage_12_validation_metrics.json)

Important tables:

* [`runtime_stage_summary.tsv`](contrasts/contrast_07_deterministic_provenance_architecture/ERR10619281/tables/runtime_stage_summary.tsv)
* [`stage_funnel_summary.tsv`](contrasts/contrast_07_deterministic_provenance_architecture/ERR10619281/tables/stage_funnel_summary.tsv)
* [`provenance_summary.tsv`](contrasts/contrast_07_deterministic_provenance_architecture/ERR10619281/tables/provenance_summary.tsv)
* [`sra_run_depth_metadata.tsv`](contrasts/contrast_07_deterministic_provenance_architecture/ERR10619281/tables/sra_run_depth_metadata.tsv)

This contrast exposes stage-level metrics and provenance telemetry while preserving downstream semantic stability.

## Answer-Key Checkpoint

Compare against the official exemplar runtime and provenance tables:

* [`runtime_stage_summary.tsv`](../err10619281/tables/runtime_stage_summary.tsv)
* [`stage_funnel_summary.tsv`](../err10619281/tables/stage_funnel_summary.tsv)
* [`provenance_summary.tsv`](../err10619281/tables/provenance_summary.tsv)
* [`run_reproducibility_summary.tsv`](../err10619281/tables/run_reproducibility_summary.tsv)

Also inspect official exemplar manifest governance:

* [`run_identity_manifest.tsv`](../err10619281/manifests/run_identity_manifest.tsv)
* [`case_study_artifact_manifest.tsv`](../err10619281/manifests/case_study_artifact_manifest.tsv)

Minor operational variability may exist across executions, including runtime and provenance identity differences. The key audit question is whether semantic topology, evidence routing, and downstream substrate organization remain stable.

---

# Final Interpretation

The cross-run architecture is intentionally redundant with the official exemplar case study.

This allows readers to validate that independently harvested artifacts and distinct provenance surfaces still converge on stable downstream semantic evidence organization.

VAP is not deterministic because artifacts are duplicated. VAP is deterministic because independently generated executions preserve stable semantic governance architecture for identical biological input.

That property is the central purpose of the cross-run audit framework.
