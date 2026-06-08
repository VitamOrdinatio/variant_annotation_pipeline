# Contract for `substrate_dimension_summary.tsv`

## Purpose

The `substrate_dimension_summary.tsv` file is useful to examine VAP outputs that are RDGP-ready and VDB-ready. The `substrate_dimension_summary.tsv` is also useful in that `stage_metrics_long.tsv` acts any given VAP-executed SRA's telemetry bus while the `substrate_dimension_summary.tsv` offers single-row-per-SRA interoperability census.

The `substrate_dimension_summary.tsv` answers:

```text
For this run, how much reusable downstream semantic infrastructure did VAP manufacture?
```

---

# Recommended Role

`stage_metrics_long.tsv` is the telemetry bus.

`substrate_dimension_summary.tsv` is the cross-repository interoperability product census.

That means `substrate_dimension_summary.tsv` should summarize not just counts, but relationships among:

- VDB-ready variant substrate
- RDGP-ready gene substrate
- candidate reviewability surface
- overlay contextualization surface
- tiered gene substrate
- semantic density / compression / breadth

---

# Recommended Output Columns for `substrate_dimension_summary.tsv`

```text
substrate_dimension_summary.tsv
├── identity
│   ├── SRA
│   ├── run_id
│   └── depth_category
│
├── core_variant_substrate
│   ├── vdb_ready_variant_rows
│   ├── unique_variant_ids
│   ├── unique_genes_in_vdb_substrate
│   ├── coding_variant_rows
│   ├── noncoding_variant_rows
│   └── coding_to_noncoding_ratio
│
├── rdgp_gene_substrate
│   ├── rdgp_ready_gene_rows
│   ├── unique_rdgp_genes
│   ├── variants_per_rdgp_gene_mean
│   ├── variants_per_rdgp_gene_median
│   └── rdgp_to_vdb_row_ratio
│
├── reviewability_surface
│   ├── candidate_reviewability_rows
│   ├── reviewable_candidate_rows
│   ├── validation_required_rows
│   ├── high_priority_validation_rows
│   ├── reviewable_candidate_density_vs_vdb
│   └── reviewable_candidate_density_vs_rdgp
│
├── tiered_gene_surface
│   ├── tier1_unique_genes
│   ├── tier2_unique_genes
│   ├── tier3_unique_genes
│   ├── tier1_to_tier2_gene_ratio
│   ├── tier2_to_tier3_gene_ratio
│   └── occupied_priority_tiers
│
├── overlay_surface
│   ├── gene_list_overlay_intersection_rows
│   ├── unique_overlay_genes
│   ├── epilepsy_overlay_genes
│   ├── mito_overlay_genes
│   ├── dual_epi_mito_overlay_genes
│   ├── overlay_gene_density_vs_rdgp
│   └── overlay_gene_density_vs_tiered_genes
│
├── overlay_evidence_richness
│   ├── overlay_clinical_evidence_rows
│   ├── overlay_frequency_profile_rows
│   ├── overlay_functional_impact_rows
│   ├── unique_clinical_status_values
│   ├── unique_frequency_status_values
│   ├── unique_functional_impact_values
│   └── overlay_evidence_modalities_present
│
├── semantic_breadth
│   ├── unique_consequence_classes
│   ├── unique_clinvar_significance_values
│   ├── unique_frequency_bins
│   ├── unique_functional_impact_classes
│   ├── unique_interpretation_labels
│   └── semantic_breadth_score
│
└── audit
    ├── source_files_present
    ├── missing_expected_files
    └── substrate_summary_status
```

# Rules

## Coding and Noncoding Rules

1. `coding_variant_rows`:

```text
coding = records with coding interpretation/consequence class routed to coding substrate
```

2. `noncoding_variant_rows`:

```text
noncoding = records routed to noncoding substrate
```

Avoid relying on free-text consequence names as VAP already has a canonical coding/noncoding field.

## Ratio Rules

1. `coding_to_noncoding_ratio`:

```text
coding_to_noncoding_ratio = coding_variant_rows / noncoding_variant_rows
```

2. `overlay_gene_density_vs_tiered_genes`:

```text
overlay_gene_density_vs_tiered_genes = unique_overlay_genes / unique(tier1 + tier2 + tier3 genes)
```

## Reviewable / High-Priority Logic Rules

1. `reviewable_candidate_rows`

   - `reviewable_candidate_rows`: rows in `candidate_reviewability_readiness.tsv` meeting canonical reviewable status

2. `validation_required_rows`

   - `validation_required_rows`: rows where `validation_required == true/yes/1`

3. `high_priority_validation_rows`
   
   - `high_priority_validation_rows`: rows where `validation_priority` is high-equivalent

## Semantic Breadth Score

- Keep `semantic_breadth_score` exactly as transparent additive dimensionality
- Label `semantic_breadth_score` explicitly as not weighted and not comparable as biological burden.

## `substrate_summary_status`

Possible field values:

```text
complete
complete_with_optional_missing
partial
failed
```

---

# Calculation rules

Use direct row counts where possible:

```text
vdb_ready_variant_rows = nrows(stage_08_vdb_ready_variants.tsv)
rdgp_ready_gene_rows = nrows(stage_08_rdgp_gene_evidence_seed.tsv)
candidate_reviewability_rows = nrows(candidate_reviewability_readiness.tsv)
gene_list_overlay_intersection_rows = nrows(gene_list_overlay_intersections.tsv)
```

Use distinct counts:

```text
unique_variant_ids = count distinct variant_id
unique_rdgp_genes = count distinct gene_id when available; otherwise gene_symbol
unique_overlay_genes = count distinct normalized gene_symbol
```

Use trim() and uppercase gene symbols before distinct counts.


Use ratios with safe division:

```text
rdgp_to_vdb_row_ratio = rdgp_ready_gene_rows / vdb_ready_variant_rows

reviewable_candidate_density_vs_vdb =
reviewable_candidate_rows / vdb_ready_variant_rows

reviewable_candidate_density_vs_rdgp =
reviewable_candidate_rows / rdgp_ready_gene_rows

overlay_gene_density_vs_rdgp =
unique_overlay_genes / unique_rdgp_genes

tier1_to_tier2_gene_ratio =
tier1_unique_genes / tier2_unique_genes

tier2_to_tier3_gene_ratio =
tier2_unique_genes / tier3_unique_genes
```

If denominator is zero, use NA, not zero.

---

# Normalization Policy

Boolean normalization:

```text
true-like = true, yes, y, 1, required
false-like = false, no, n, 0, not_required
```

Missing / null:

```text
NA, empty, ., none, null are treated as missing.
```

Gene symbol normalization:

```text
trim whitespace and uppercase before distinct counts.
```

Ratio precision:

```text
store ratios as decimal numeric values, preferably 6 significant digits.
```

---

# Semantic Breadth Score

Keep this simple and transparent:

```text
semantic_breadth_score =
unique_consequence_classes
+ unique_clinvar_significance_values
+ unique_frequency_bins
+ unique_functional_impact_classes
+ unique_interpretation_labels
+ occupied_priority_tiers
+ overlay_evidence_modalities_present
```

This is not a biological score. It is an interoperability dimensionality score.

---