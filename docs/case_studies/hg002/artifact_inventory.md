# HG002 Artifact Inventory

This document inventories the major artifacts associated with the HG002 benchmarking case study within the Variant Annotation Pipeline (VAP) repository.

The HG002 case study demonstrates:

* benchmark-aware substrate validation,
* representation-aware benchmarking,
* provenance-aware execution,
* deterministic artifact emission,
* and operational observability across the VAP ecosystem.

HG002 benchmarking evaluates upstream small-variant substrate concordance against GIAB HG002 v4.2.1 truth resources using `hap.py` inside GIAB high-confidence benchmark regions.

---

# 1. Benchmarking Artifacts

Location:

[docs/case_studies/hg002/benchmarking/](benchmarking/)

These artifacts contain the primary benchmarking outputs generated from `hap.py` evaluation.

## Core benchmarking outputs

| Artifact                       | Purpose                                 |
| ------------------------------ | --------------------------------------- |
| [`hg002_benchmark_summary.tsv`](./benchmarking/hg002_benchmark_summary.tsv) | High-level benchmarking summary |
| [`hg002_benchmark_summary.json`](./benchmarking/hg002_benchmark_summary.json) | Machine-readable benchmarking summary |
| [`hg002_snp_indel_metrics.tsv`](./benchmarking/hg002_snp_indel_metrics.tsv) | Stratified SNP vs INDEL metrics |
| [`hg002_false_positives.tsv`](./benchmarking/hg002_false_positives.tsv) | Representative false-positive substrate |
| [`hg002_false_negatives.tsv`](./benchmarking/hg002_false_negatives.tsv) | Representative false-negative substrate |
| [`benchmarking.log`](./benchmarking/benchmarking.log) | Benchmark execution telemetry |

## hap.py outputs

Location:

[docs/case_studies/hg002/benchmarking/happy/](benchmarking/happy/)

These files contain raw and extended `hap.py` outputs, including ROC curves, metrics, and concordance summaries.

| Artifact | Purpose |
|---|---|
| [`hg002_happy.summary.csv`](./benchmarking/happy/hg002_happy.summary.csv) | Primary hap.py concordance summary |
| [`hg002_happy.extended.csv`](./benchmarking/happy/hg002_happy.extended.csv) | Extended benchmarking metrics |
| [`hg002_happy.metrics.json.gz`](./benchmarking/happy/hg002_happy.metrics.json.gz) | Structured metrics export |
| [`hg002_happy.runinfo.json`](./benchmarking/happy/hg002_happy.runinfo.json) | Runtime metadata |                |

## Interoperability / namespace mediation

Location:

[docs/case_studies/hg002/benchmarking/interoperability/](benchmarking/interoperability/)

These artifacts document benchmark-local namespace mediation and harmonization.

| Artifact | Purpose |
|---|---|
| [`namespace_harmonization_manifest.json`](./benchmarking/interoperability/namespace_harmonization_manifest.json) | Run-scoped namespace mediation manifest |
| [`HG002_GRCh38_1_22_v4.2.1_benchmark.nochr.bed`](./benchmarking/interoperability/HG002_GRCh38_1_22_v4.2.1_benchmark.nochr.bed) | Harmonized GIAB BED resource |
| [`HG002_GRCh38_1_22_v4.2.1_benchmark.nochr.vcf.gz.md`](./benchmarking/interoperability/HG002_GRCh38_1_22_v4.2.1_benchmark.nochr.vcf.gz.md) | Provenance checksum metadata |

---

# 2. Figure Artifacts

## Primary Hero Figure

| Artifact | Purpose |
|---|---|
| [`hg002_happy_benchmarking.png`](./figures/hg002_happy_benchmarking.png) | Benchmark-aware substrate validation and representation-aware benchmarking synthesis figure |

Demonstrates:

* benchmark-aware substrate validation,
* representation-aware concordance,
* namespace mediation,
* provenance-aware benchmarking,
* engineering trust boundaries,
* operational observability.

Location:

[docs/case_studies/hg002/figures/](./figures/)

The HG002 figure suite communicates operational reproducibility, semantic evidence organization, benchmarking concordance, and interoperability-oriented downstream substrate generation.

---

## F1 — Benchmark operational stability

| Artifact                                     | Purpose                                          |
| -------------------------------------------- | ------------------------------------------------ |
| [`hg002_f1_benchmark_operational_stability.png`](./figures/hg002_f1_benchmark_operational_stability.png) | Runtime reproducibility and structural stability |

Demonstrates:

* deterministic structural outputs,
* reproducible evidence organization,
* stable downstream semantic routing.

---

## F2 — Runtime observability profile

| Artifact                                   | Purpose                          |
| ------------------------------------------ | -------------------------------- |
| [`hg002_f2_runtime_observability_profile.png`](./figures/hg002_f2_runtime_observability_profile.png) | Stage-resolved runtime telemetry |

Demonstrates:

* execution observability,
* runtime decomposition,
* stage-level operational telemetry.

---

## F3A — Deterministic evidence lineage

| Artifact                                     | Purpose                      |
| -------------------------------------------- | ---------------------------- |
| [`HG002_f3a_deterministic_evidence_lineage.png`](./figures/HG002_f3a_deterministic_evidence_lineage.png) | Evidence refinement topology |

Demonstrates:

* evidence refinement pressure,
* deterministic prioritization routing,
* validation-ready substrate emergence.

---

## F3B — Semantic evidence branching

| Artifact                         | Purpose                                |
| -------------------------------- | -------------------------------------- |
| [`HG002_f3b_semantic_branching.png`](./figures/HG002_f3b_semantic_branching.png) | Coding vs noncoding semantic branching |

Demonstrates:

* preservation of semantic evidence classes,
* noncoding expansion in WGS contexts,
* interpretability-aware evidence partitioning.

---

## F4A — Coding variant semantic distributions

| Artifact | Purpose |
|---|---|
| [`HG002_f4a_clinvar_significance.png`](./figures/HG002_f4a_clinvar_significance.png) | Coding ClinVar significance distribution |
| [`HG002_f4a_consequence.png`](./figures/HG002_f4a_consequence.png) | Coding consequence distribution |
| [`HG002_f4a_pop_freq_bins.png`](./figures/HG002_f4a_pop_freq_bins.png) | Coding population frequency structure |

---

## F4B — Noncoding variant semantic distributions

| Artifact | Purpose |
|---|---|
| [`HG002_f4b_clinvar_significance.png`](./figures/HG002_f4b_clinvar_significance.png) | Noncoding ClinVar significance distribution |
| [`HG002_f4b_consequence.png`](./figures/HG002_f4b_consequence.png) | Noncoding consequence distribution |
| [`HG002_f4b_pop_freq_bins.png`](./figures/HG002_f4b_pop_freq_bins.png) | Noncoding population frequency structure |

Demonstrates:

* WGS noncoding evidence expansion,
* interpretability asymmetry,
* evidence topology preservation.

---

## F5 — Interoperability substrates

| Artifact                                 | Purpose                                  |
| ---------------------------------------- | ---------------------------------------- |
| [`HG002_f5_interoperability_substrates.png`](./figures/HG002_f5_interoperability_substrates.png) | Stage 08 substrate emission architecture |

Demonstrates:

* deterministic downstream substrate generation,
* RDGP-ready aggregation surfaces,
* VDB-ready normalized variant exports.

---

# 3. Summary Table Artifacts

Location:

[docs/case_studies/hg002/tables/summary/](./tables/summary/)

These TSV artifacts summarize semantic topology, prioritization behavior, operational observability, and evidence organization.

Key artifacts include:

| Artifact                                   | Purpose                                   |
| ------------------------------------------ | ----------------------------------------- |
| [`priority_tier_summary.tsv`](./tables/summary/priority_tier_summary.tsv) | Tier distribution overview |
| [`candidate_reviewability_readiness.tsv`](./tables/summary/candidate_reviewability_readiness.tsv) | Validation-readiness routing |
| [`clinical_status_summary.tsv`](./tables/summary/clinical_status_summary.tsv) | Clinical evidence classification |
| [`runtime_stage_summary.tsv`](./tables/summary/runtime_stage_summary.tsv) | Runtime telemetry decomposition |
| [`stage_funnel_summary.tsv`](./tables/summary/stage_funnel_summary.tsv) | Stage-level evidence reduction |
| [`provenance_summary.tsv`](./tables/summary/provenance_summary.tsv) | Deterministic provenance accounting |
| [`variant_consequence_summary.tsv`](./tables/summary/variant_consequence_summary.tsv) | Consequence topology |
| [`coding_noncoding_consequence_summary.tsv`](./tables/summary/coding_noncoding_consequence_summary.tsv) | Coding vs noncoding semantic organization |

---

# 4. Overlay / Gene-Level Evidence Artifacts

Location:

[docs/case_studies/hg002/tables/summary/](./tables/summary/)

These artifacts support semantic overlay analysis, contextual prioritization, and downstream evidence organization.

| Artifact | Purpose |
|---|---|
| [`overlay_gene_coding_clinical_evidence.tsv`](./tables/summary/overlay_gene_coding_clinical_evidence.tsv) | Clinical overlay evidence |
| [`overlay_gene_coding_frequency_profiles.tsv`](./tables/summary/overlay_gene_coding_frequency_profiles.tsv) | Population frequency context |
| [`overlay_gene_coding_functional_impact.tsv`](./tables/summary/overlay_gene_coding_functional_impact.tsv) | Functional consequence aggregation |
| [`gene_list_overlay_intersections.tsv`](./tables/summary/gene_list_overlay_intersections.tsv) | Overlay intersection topology |

---

# 5. Unique Gene Artifacts

Location:


[docs/case_studies/hg002/tables/unique_genes/](./tables/unique_genes/)

These artifacts summarize unique genes stratified by semantic prioritization tiers.

| Artifact | Purpose |
|---|---|
| [`HG002_tier1_unique_genes.tsv`](./tables/unique_genes/HG002_tier1_unique_genes.tsv) | Tier 1 genes |
| [`HG002_tier2_unique_genes.tsv`](./tables/unique_genes/HG002_tier2_unique_genes.tsv) | Tier 2 genes |
| [`HG002_tier3_unique_genes.tsv`](./tables/unique_genes/HG002_tier3_unique_genes.tsv) | Tier 3 genes |

Overlay-aware variants additionally preserve epilepsy / mitochondrial contextualization.

---

# 6. Value-Count Semantic Telemetry

Location:

[docs/case_studies/hg002/tables/value_counts/](./tables/value_counts/)

These artifacts provide normalized semantic frequency distributions across multiple evidence dimensions.

Examples include:

* [`value_counts__clinvar_significance.tsv`](./tables/value_counts/value_counts__clinvar_significance.tsv)
* [`value_counts__consequence.tsv`](./tables/value_counts/value_counts__consequence.tsv)
* [`value_counts__priority_tier.tsv`](./tables/value_counts/value_counts__priority_tier.tsv)
* [`value_counts__interpretability_status.tsv`](./tables/value_counts/value_counts__interpretability_status.tsv)
* [`value_counts__variant_effect_severity.tsv`](./tables/value_counts/value_counts__variant_effect_severity.tsv)

These artifacts support:

* semantic observability,
* downstream visualization,
* deterministic telemetry generation,
* and governance validation.

---

# 7. Candidate Slice Artifacts

Location:

[docs/case_studies/hg002/tables/lane_candidate_slices/](./tables/lane_candidate_slices/)

These TSV artifacts provide representative candidate subsets used for interpretability demonstrations, prioritization inspection, and semantic topology analysis.

Examples include:

| Artifact | Purpose |
|---|---|
| [`HG002_bucket_1a_validation_routed_epilepsy_mito.tsv`](./tables/lane_candidate_slices/HG002_bucket_1a_validation_routed_epilepsy_mito.tsv) | Validation-routed contextual evidence |
| [`HG002_bucket_2a_rare_impact_coding_triage_summary.tsv`](./tables/lane_candidate_slices/HG002_bucket_2a_rare_impact_coding_triage_summary.tsv) | Rare coding prioritization substrate |
| [`HG002_bucket_4a_representative_noncoding_semantic_exemplars.tsv`](./tables/lane_candidate_slices/HG002_bucket_4a_representative_noncoding_semantic_exemplars.tsv) | Noncoding semantic exemplars |

These artifacts are demonstrative operational substrates and are not clinical interpretations.

---

# 8. Governance / Design Documents

| Artifact | Purpose |
|---|---|
| [`hg002_benchmarking_design_philosophy.md`](./hg002_benchmarking_design_philosophy.md) | Benchmarking doctrine and scope |
| [`hg002_wgs_baseline.md`](./hg002_wgs_baseline.md) | WGS baseline operational characterization |

Additional implementation and benchmarking governance documents exist elsewhere in the repository under:

* [`docs/contracts/`](../../contracts/)
* [`docs/plans/`](../../plans/)
* [`tests/benchmarking/`](../../../tests/benchmarking/)
* [`scripts/benchmarking/`](../../../scripts/benchmarking/)

---

# 9. Scientific Positioning

The HG002 case study demonstrates that:

* VAP achieves strong small-variant concordance against GIAB HG002 v4.2.1,
* benchmarking can be representation-aware and provenance-aware,
* deterministic semantic evidence organization is preserved,
* and VAP emits reusable downstream interoperability substrates.

Importantly:

Benchmarking validates upstream substrate integrity and concordance within constrained GIAB benchmark regions. Benchmarking does not validate downstream biological interpretation, diagnosis, or clinical decision-making.

The HG002 benchmarking case study should therefore be interpreted as:

* engineering validation,
* operational validation,
* substrate validation,
* and concordance evaluation.

Not clinical validation.

---

# Related HG002 Documents

* [`README.md`](./README.md)
* [`hg002_artifact_navigation_guide.md`](./hg002_artifact_navigation_guide.md)
* [`artifact_inventory.md`](./artifact_inventory.md)
* [`hg002_semantic_evidence_landscape.md`](./hg002_semantic_evidence_landscape.md)
* [`hg002_benchmarking_design_philosophy.md`](./hg002_benchmarking_design_philosophy.md)
* [`hg002_wgs_baseline.md`](./hg002_wgs_baseline.md)