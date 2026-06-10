## `substrate_dimension_summary.tsv`

The `substrate_dimension_summary.tsv` file provides a single-row-per-run interoperability census describing how much reusable downstream semantic infrastructure a completed VAP run produced.

Unlike `stage_metrics_long.tsv`, which acts as VAP’s telemetry bus, `substrate_dimension_summary.tsv` summarizes relationships among:

* VDB-ready variant substrate
* RDGP-ready gene substrate
* candidate reviewability surface
* overlay contextualization surface
* semantic breadth and interpretability density

The table is intended for cross-run comparative analysis and downstream narrative construction.

---

# Column Groups

## Identity

| Column           | Description                                                           | Units       |
| ---------------- | --------------------------------------------------------------------- | ----------- |
| `SRA`            | Sample/SRA accession identifier                                       | string      |
| `run_id`         | VAP execution run identifier                                          | string      |
| `depth_category` | Sequencing depth stratification label (`q1`, `median`, `q3`, `hg002`) | categorical |

---

## Core Variant Substrate

| Column                          | Description                                                          | Units           |
| ------------------------------- | -------------------------------------------------------------------- | --------------- |
| `vdb_ready_variant_rows`        | Total rows in `stage_08_vdb_ready_variants.tsv`                      | rows            |
| `unique_variant_ids`            | Distinct `variant_id` values in VDB-ready substrate                  | unique variants |
| `unique_genes_in_vdb_substrate` | Distinct normalized `gene_id` values observed in VDB-ready substrate | unique genes    |
| `coding_variant_rows`           | Coding-routed variant rows from VAP telemetry                        | rows            |
| `noncoding_variant_rows`        | Noncoding-routed variant rows from VAP telemetry                     | rows            |
| `coding_to_noncoding_ratio`     | `coding_variant_rows / noncoding_variant_rows`                       | ratio           |

Distinct counts are computed using normalized identifiers with whitespace trimming.

---

## RDGP Gene Substrate

| Column                          | Description                                                  | Units         |
| ------------------------------- | ------------------------------------------------------------ | ------------- |
| `rdgp_ready_gene_rows`          | Total rows in `stage_08_rdgp_gene_evidence_seed.tsv`         | rows          |
| `unique_rdgp_genes`             | Distinct normalized `gene_id` values in RDGP-ready substrate | unique genes  |
| `variants_per_rdgp_gene_mean`   | Mean distinct variant burden per gene in VDB substrate       | variants/gene |
| `variants_per_rdgp_gene_median` | Median distinct variant burden per gene in VDB substrate     | variants/gene |
| `rdgp_to_vdb_row_ratio`         | `rdgp_ready_gene_rows / vdb_ready_variant_rows`              | ratio         |

Variant burden calculations are derived from distinct `variant_id` counts grouped by normalized `gene_id`.

---

## Reviewability Surface

| Column                                 | Description                                                          | Units |
| -------------------------------------- | -------------------------------------------------------------------- | ----- |
| `candidate_reviewability_rows`         | Cardinality of the canonical candidate reviewability summary surface | rows  |
| `reviewable_candidate_rows`            | Validation-routed candidate rows requiring downstream review         | rows  |
| `validation_required_rows`             | Rows where `validation_required == true`                             | rows  |
| `high_priority_validation_rows`        | Rows with high-equivalent validation priority                        | rows  |
| `reviewable_candidate_density_vs_vdb`  | `reviewable_candidate_rows / vdb_ready_variant_rows`                 | ratio |
| `reviewable_candidate_density_vs_rdgp` | `reviewable_candidate_rows / rdgp_ready_gene_rows`                   | ratio |

`candidate_reviewability_rows` describes the shape of the reviewability substrate, whereas validation-related counts describe run-specific candidate burden.

---

## Tiered Gene Surface

| Column                      | Description                                | Units        |
| --------------------------- | ------------------------------------------ | ------------ |
| `tier1_unique_genes`        | Distinct genes assigned to tier 1          | unique genes |
| `tier2_unique_genes`        | Distinct genes assigned to tier 2          | unique genes |
| `tier3_unique_genes`        | Distinct genes assigned to tier 3          | unique genes |
| `tier1_to_tier2_gene_ratio` | `tier1_unique_genes / tier2_unique_genes`  | ratio        |
| `tier2_to_tier3_gene_ratio` | `tier2_unique_genes / tier3_unique_genes`  | ratio        |
| `occupied_priority_tiers`   | Number of non-empty priority tiers present | tiers        |

Tiered gene counts are computed from distinct normalized `gene_id` values in `stage_12_validation_candidates.tsv`.

---

## Overlay Surface

| Column                                 | Description                                              | Units        |
| -------------------------------------- | -------------------------------------------------------- | ------------ |
| `gene_list_overlay_intersection_rows`  | Overlay matrix cardinality                               | rows         |
| `unique_overlay_genes`                 | Distinct overlay genes across EPI25 + MitoCarta          | unique genes |
| `epilepsy_overlay_genes`               | Distinct EPI25 overlay genes                             | unique genes |
| `mito_overlay_genes`                   | Distinct MitoCarta overlay genes                         | unique genes |
| `dual_epi_mito_overlay_genes`          | Overlay genes shared between EPI25 and MitoCarta         | unique genes |
| `overlay_gene_density_vs_rdgp`         | `unique_overlay_genes / unique_rdgp_genes`               | ratio        |
| `overlay_gene_density_vs_tiered_genes` | `unique_overlay_genes / unique(tier1+tier2+tier3 genes)` | ratio        |

Overlay membership is determined using normalized Ensembl gene identifiers.

---

## Overlay Evidence Richness

| Column                                | Description                                         | Units         |
| ------------------------------------- | --------------------------------------------------- | ------------- |
| `overlay_clinical_evidence_rows`      | Distinct overlay clinical evidence aggregation rows | rows          |
| `overlay_frequency_profile_rows`      | Distinct overlay frequency profile aggregation rows | rows          |
| `overlay_functional_impact_rows`      | Distinct overlay functional impact aggregation rows | rows          |
| `unique_clinical_status_values`       | Distinct normalized `clinical_status` values        | unique labels |
| `unique_frequency_status_values`      | Distinct normalized `frequency_status` values       | unique labels |
| `unique_functional_impact_values`     | Distinct normalized `functional_impact` values      | unique labels |
| `overlay_evidence_modalities_present` | Number of populated overlay evidence modalities     | modalities    |

Overlay evidence summaries are generated from coding variants intersecting overlay gene lists.

---

## Semantic Breadth

| Column                               | Description                                        | Units         |
| ------------------------------------ | -------------------------------------------------- | ------------- |
| `unique_consequence_classes`         | Distinct normalized consequence classes            | unique labels |
| `unique_clinvar_significance_values` | Distinct ClinVar significance labels               | unique labels |
| `unique_frequency_bins`              | Distinct frequency-status bins                     | unique labels |
| `unique_functional_impact_classes`   | Distinct functional impact classes                 | unique labels |
| `unique_interpretation_labels`       | Distinct interpretation labels                     | unique labels |
| `semantic_breadth_score`             | Transparent additive semantic dimensionality score | score         |

The `semantic_breadth_score` is computed as:

```text
unique_consequence_classes
+ unique_clinvar_significance_values
+ unique_frequency_bins
+ unique_functional_impact_classes
+ unique_interpretation_labels
+ occupied_priority_tiers
+ overlay_evidence_modalities_present
```

This is not a biological burden score. It is an interoperability dimensionality score intended to summarize semantic diversity within a run.

---

## Audit Fields

| Column                     | Description                                                | Units       |
| -------------------------- | ---------------------------------------------------------- | ----------- |
| `source_files_present`     | Pipe-delimited list of detected source files               | string      |
| `missing_expected_files`   | Pipe-delimited list of missing required files              | string      |
| `substrate_summary_status` | Overall execution status (`complete`, `partial`, `failed`) | categorical |

---

# Implementation Notes

* Large TSV scans are performed using DuckDB.
* Telemetry-native values are preferentially harvested from `stage_metrics_long.tsv`.
* Distinct entity counts are computed directly from source-truth TSV artifacts.
* Gene identifiers are normalized using whitespace trimming and Ensembl version stripping when applicable.
* Ratios use safe division semantics; zero denominators produce `NA`.
