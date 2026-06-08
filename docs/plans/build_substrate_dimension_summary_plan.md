# Implementation Plan — `scripts/mark/build_substrate_dimension_summary.py`

## Objective

Build a MARK-native script that generates a global append-ready:

```text
substrate_dimension_summary.new.tsv
```

for the 13 completed VAP runs.

The output summarizes, one row per SRA/run, how much reusable downstream semantic infrastructure VAP manufactured for:

* VDB-ready variant substrate
* RDGP-ready gene substrate
* candidate reviewability
* priority-tiered interpretation surface
* overlay gene-list contextualization
* semantic breadth
* interoperability readiness

The script will be executed from MARK VAP repo root and will not modify any existing VAP run artifacts.

---

## Script Location

```text
scripts/mark/build_substrate_dimension_summary.py
```

---

## Output Location

The script writes only to:

```text
/root/Desktop/substrate_dimension_summary/
├── substrate_dimension_summary.new.tsv
└── substrate_dimension_summary_build_audit.tsv
```

---

## Source Immutability Rule

All VAP run artifacts on MARK are read-only source truth.

The script may read from:

```text
results/<run_id>/
```

but must never write to, overwrite, move, delete, patch, or modify anything inside:

```text
results/
processed/
metrics/
metadata/
logs/
docs/
```

All generated outputs must be written outside the VAP repo to:

```text
/root/Desktop/substrate_dimension_summary/
```

---

## Manifest

The script will use a hardcoded 13-run manifest and will not auto-discover runs.

```python
MANIFEST = [
    ("ERR10619203", "run_2026_05_30_071639", "q3"),
    ("ERR10619207", "run_2026_06_01_124134", "q3"),
    ("ERR10619208", "run_2026_05_30_151355", "median"),
    ("ERR10619212", "run_2026_05_30_214724", "q1"),
    ("ERR10619225", "run_2026_05_31_091242", "q3"),
    ("ERR10619230", "run_2026_06_01_004903", "q3"),
    ("ERR10619241", "run_2026_06_02_052302", "q1"),
    ("ERR10619281", "run_2026_05_27_233524", "median"),
    ("ERR10619285", "run_2026_06_02_124300", "median"),
    ("ERR10619300", "run_2026_05_27_172531", "median"),
    ("ERR10619309", "run_2026_06_02_181024", "q1"),
    ("ERR10619330", "run_2026_06_01_203130", "q1"),
    ("SRR12898354", "run_2026_06_03_010030", "hg002"),
]
```

---

## Inputs Per Run

For each manifest run, the script reads:

```text
results/<run_id>/metrics/stage_metrics_long.tsv
results/<run_id>/processed/stage_08_vdb_ready_variants.tsv
results/<run_id>/processed/stage_08_rdgp_gene_evidence_seed.tsv
results/<run_id>/processed/stage_12_validation_candidates.tsv
```

Reference gene lists:

```text
data/reference/gene_lists/epi25_vap_overlay_seed.tsv
data/reference/gene_lists/mitocarta_vap_overlay_seed.tsv
```

---

## Architecture

The builder uses three layers.

### Layer A — Telemetry Harvest

Primary source:

```text
results/<run_id>/metrics/stage_metrics_long.tsv
```

Use `metric_name → metric_value` lookups wherever the metric is already telemetry-native.

Examples:

```text
vdb_ready_variants_rows
rdgp_gene_evidence_seed_rows
counts_by_variant_origin__coding
counts_by_variant_origin__noncoding
validation_candidates_rows
counts_by_validation_required__True
counts_by_validation_priority__high
counts_by_priority_tier__tier_1_high_confidence_candidate
counts_by_priority_tier__tier_2_moderate_candidate
counts_by_priority_tier__tier_3_low_support_or_common
```

Telemetry-derived values should be preferred over recomputation unless the contract explicitly requires distinct entity counts or medians.

### Layer B — Source-Truth DISTINCT Scans

Use DuckDB for compact DISTINCT operations against large TSVs.

Sources:

```text
stage_08_vdb_ready_variants.tsv
stage_08_rdgp_gene_evidence_seed.tsv
stage_12_validation_candidates.tsv
```

Required source-truth scans include:

```text
unique_variant_ids
unique_genes_in_vdb_substrate
unique_rdgp_genes
variants_per_rdgp_gene_mean
variants_per_rdgp_gene_median
semantic breadth distinct counts
```

### Layer C — Overlay Gene-List Reconciliation

Use:

```text
epi25_vap_overlay_seed.tsv
mitocarta_vap_overlay_seed.tsv
stage_12_validation_candidates.tsv
```

to compute overlay surface metrics.

The EPI25 and MitoCarta lists are expected to have zero Ensembl gene overlap. If overlap is detected, the script should record it in audit and continue only if logic explicitly supports dual-hit counting.

---

## Normalization Policy

Before joins, comparisons, and distinct counts:

* Trim all string fields.
* Lowercase case-insensitive categorical fields.
* Preserve canonical casing for `gene_symbol` in outputs, but uppercase normalized gene symbols when performing distinct gene-symbol counts.
* Treat the following as missing/null-like:

```text
NA
empty string
.
none
null
nan
```

Boolean normalization:

```text
true-like: true, yes, y, 1, required
false-like: false, no, n, 0, not_required
```

Ratios should use safe division. If denominator is zero, output `NA`, not zero.

---

## Output Columns

The output file must contain one row per manifest run with these columns in this order:

```text
SRA
run_id
depth_category
vdb_ready_variant_rows
unique_variant_ids
unique_genes_in_vdb_substrate
coding_variant_rows
noncoding_variant_rows
coding_to_noncoding_ratio
rdgp_ready_gene_rows
unique_rdgp_genes
variants_per_rdgp_gene_mean
variants_per_rdgp_gene_median
rdgp_to_vdb_row_ratio
candidate_reviewability_rows
reviewable_candidate_rows
validation_required_rows
high_priority_validation_rows
reviewable_candidate_density_vs_vdb
reviewable_candidate_density_vs_rdgp
tier1_unique_genes
tier2_unique_genes
tier3_unique_genes
tier1_to_tier2_gene_ratio
tier2_to_tier3_gene_ratio
occupied_priority_tiers
gene_list_overlay_intersection_rows
unique_overlay_genes
epilepsy_overlay_genes
mito_overlay_genes
dual_epi_mito_overlay_genes
overlay_gene_density_vs_rdgp
overlay_gene_density_vs_tiered_genes
overlay_clinical_evidence_rows
overlay_frequency_profile_rows
overlay_functional_impact_rows
unique_clinical_status_values
unique_frequency_status_values
unique_functional_impact_values
overlay_evidence_modalities_present
unique_consequence_classes
unique_clinvar_significance_values
unique_frequency_bins
unique_functional_impact_classes
unique_interpretation_labels
semantic_breadth_score
source_files_present
missing_expected_files
substrate_summary_status
```

---

## Field Derivation Rules

### Identity

```text
SRA = manifest sample_id
run_id = manifest run_id
depth_category = manifest depth_category
```

---

## Core Variant Substrate

### `vdb_ready_variant_rows`

Telemetry-native:

```text
metric_name == vdb_ready_variants_rows
```

Fallback:

```text
nrows(stage_08_vdb_ready_variants.tsv)
```

### `unique_variant_ids`

Source-truth DISTINCT scan:

```sql
COUNT(DISTINCT variant_id)
FROM stage_08_vdb_ready_variants.tsv
```

### `unique_genes_in_vdb_substrate`

Source-truth DISTINCT scan:

```sql
COUNT(DISTINCT gene_id)
FROM stage_08_vdb_ready_variants.tsv
WHERE gene_id IS NOT NULL
```

### `coding_variant_rows`

Telemetry-native:

```text
metric_name == counts_by_variant_origin__coding
```

Fallback:

```text
metric_name == coding_interpreted_rows
```

### `noncoding_variant_rows`

Telemetry-native:

```text
metric_name == counts_by_variant_origin__noncoding
```

Fallback:

```text
metric_name == noncoding_interpreted_rows
```

### `coding_to_noncoding_ratio`

```text
coding_variant_rows / noncoding_variant_rows
```

Use safe division.

---

## RDGP Gene Substrate

### `rdgp_ready_gene_rows`

Telemetry-native:

```text
metric_name == rdgp_gene_evidence_seed_rows
```

Fallback:

```text
metric_name == rdgp_gene_evidence_seed_tsv_rows
```

### `unique_rdgp_genes`

Source-truth DISTINCT scan:

```sql
COUNT(DISTINCT gene_id)
FROM stage_08_rdgp_gene_evidence_seed.tsv
WHERE gene_id IS NOT NULL
```

### `variants_per_rdgp_gene_mean`

Source-truth calculation from VDB-ready variants:

```sql
WITH gene_counts AS (
    SELECT gene_id, COUNT(DISTINCT variant_id) AS variant_count
    FROM stage_08_vdb_ready_variants.tsv
    WHERE gene_id IS NOT NULL
    GROUP BY gene_id
)
SELECT AVG(variant_count)
FROM gene_counts
```

### `variants_per_rdgp_gene_median`

Same `gene_counts` CTE:

```sql
SELECT MEDIAN(variant_count)
FROM gene_counts
```

### `rdgp_to_vdb_row_ratio`

```text
rdgp_ready_gene_rows / vdb_ready_variant_rows
```

Use safe division.

---

## Reviewability Surface

### `candidate_reviewability_rows`

Telemetry-native if present in `stage_metrics_long.tsv`; otherwise compute from the candidate reviewability aggregation logic used for `candidate_reviewability_readiness.tsv`.

Do not substitute `validation_candidates_rows`, because that counts the full `stage_12_validation_candidates.tsv` substrate, not the reviewability summary surface.

Initial implementation:

`candidate_reviewability_rows = len(CANDIDATE_REVIEWABILITY_METRICS)`

This represents the cardinality of the candidate reviewability summary surface, not the number of stage12 validation candidates.

### `reviewable_candidate_rows`

Initial implementation definition:

```text
reviewable_candidate_rows = validation_required_rows
```

This is an explicit v1 proxy because VAP’s validation routing is the current canonical machine-readable reviewability signal. If a future dedicated reviewability_status field exists, this definition should be revised.

### `validation_required_rows`

Telemetry-native:

```text
metric_name == counts_by_validation_required__True
```

### `high_priority_validation_rows`

Telemetry-native:

```text
metric_name == counts_by_validation_priority__high
```

### `reviewable_candidate_density_vs_vdb`

```text
reviewable_candidate_rows / vdb_ready_variant_rows
```

### `reviewable_candidate_density_vs_rdgp`

```text
reviewable_candidate_rows / rdgp_ready_gene_rows
```

---

## Tiered Gene Surface

The contract names these as genes, but available telemetry counts priority-tiered candidate rows. To preserve semantic accuracy, the implementation should compute unique genes directly from `stage_12_validation_candidates.tsv`.

### `tier1_unique_genes`

```sql
COUNT(DISTINCT gene_id)
FROM stage_12_validation_candidates.tsv
WHERE priority_tier = 'tier_1_high_confidence_candidate'
```

### `tier2_unique_genes`

```sql
COUNT(DISTINCT gene_id)
FROM stage_12_validation_candidates.tsv
WHERE priority_tier = 'tier_2_moderate_candidate'
```

### `tier3_unique_genes`

```sql
COUNT(DISTINCT gene_id)
FROM stage_12_validation_candidates.tsv
WHERE priority_tier = 'tier_3_low_support_or_common'
```

### `occupied_priority_tiers`

Count distinct non-empty `priority_tier` values in `stage_12_validation_candidates.tsv`.

### `tier1_to_tier2_gene_ratio`

```text
tier1_unique_genes / tier2_unique_genes
```

### `tier2_to_tier3_gene_ratio`

```text
tier2_unique_genes / tier3_unique_genes
```

Use safe division.

---

## Overlay Surface

Overlay membership is defined by explicit Ensembl gene ID membership in:

```text
epi25_vap_overlay_seed.tsv
mitocarta_vap_overlay_seed.tsv
```

### `gene_list_overlay_intersection_rows`

Expected full matrix size:

```text
1140
```

per run.

This represents the number of overlay genes considered, including zero-count genes.

### `unique_overlay_genes`

Compute from overlay seed lists after normalizing Ensembl `gene_id` for matching.

Also validate that normalized `gene_symbol` count agrees with normalized Ensembl `gene_id` count. If they disagree, use Ensembl `gene_id` for operational matching but record the discrepancy in audit.


```text
count unique Ensembl gene IDs across EPI25 + MitoCarta seed lists
```

Expected:

```text
1140
```

### `epilepsy_overlay_genes`

```text
count unique genes in epi25_vap_overlay_seed.tsv
```

Expected:

```text
7
```

### `mito_overlay_genes`

```text
count unique genes in mitocarta_vap_overlay_seed.tsv
```

Expected:

```text
1133
```

### `dual_epi_mito_overlay_genes`

```text
count overlap between EPI25 and MitoCarta Ensembl gene IDs
```

Expected:

```text
0
```

### `overlay_gene_density_vs_rdgp`

```text
unique_overlay_genes / unique_rdgp_genes
```

### `overlay_gene_density_vs_tiered_genes`

```text
unique_overlay_genes / unique(tier1 + tier2 + tier3 genes)
```

For the denominator, compute distinct `gene_id` from `stage_12_validation_candidates.tsv` where `priority_tier` is one of tier 1, tier 2, or tier 3.

---

## Overlay Evidence Richness

These are derived from the overlay builders’ intended aggregation dimensions but should be recomputed from source truth where feasible.

### `overlay_clinical_evidence_rows`

Count aggregated rows from source-truth overlay substrate grouped by:

```text
gene_id
gene_symbol
overlay_source
clinical_evidence
clinical_status
```

using coding rows in `stage_12_validation_candidates.tsv` whose `gene_id` occurs in either overlay seed list.

### `overlay_frequency_profile_rows`

Count aggregated rows from source-truth overlay substrate grouped by:

```text
gene_id
gene_symbol
overlay_source
frequency_status
rarity_flag
```

### `overlay_functional_impact_rows`

Count aggregated rows from source-truth overlay substrate grouped by:

```text
gene_id
gene_symbol
overlay_source
functional_impact
```

### `unique_clinical_status_values`

Distinct normalized `clinical_status` values among overlay coding rows.

### `unique_frequency_status_values`

Distinct normalized `frequency_status` values among overlay coding rows.

### `unique_functional_impact_values`

Distinct normalized `functional_impact` values among overlay coding rows.

### `overlay_evidence_modalities_present`

Additive count of overlay evidence modalities with nonzero row counts:

```text
clinical evidence view present
+ frequency profile view present
+ functional impact view present
```

Expected range:

```text
0..3
```

---

## Semantic Breadth

Compute from source-truth stage12 values, not from telemetry row-count distributions, to avoid counting duplicated metric namespaces.

### `unique_consequence_classes`

```sql
COUNT(DISTINCT consequence)
FROM stage_12_validation_candidates.tsv
WHERE consequence IS NOT NULL
```

### `unique_clinvar_significance_values`

```sql
COUNT(DISTINCT clinvar_significance)
FROM stage_12_validation_candidates.tsv
WHERE clinvar_significance IS NOT NULL
```

### `unique_frequency_bins`

```sql
COUNT(DISTINCT frequency_status)
FROM stage_12_validation_candidates.tsv
WHERE frequency_status IS NOT NULL
```

### `unique_functional_impact_classes`

```sql
COUNT(DISTINCT functional_impact)
FROM stage_12_validation_candidates.tsv
WHERE functional_impact IS NOT NULL
```

### `unique_interpretation_labels`

Recommended definition:

```text
distinct source_interpretation_label
```

from `stage_12_validation_candidates.tsv`.

If `source_interpretation_label` is missing, fallback to `coding_interpretation_label`.

### `semantic_breadth_score`

Transparent additive dimensionality:

```text
unique_consequence_classes
+ unique_clinvar_significance_values
+ unique_frequency_bins
+ unique_functional_impact_classes
+ unique_interpretation_labels
+ occupied_priority_tiers
+ overlay_evidence_modalities_present
```

This is not a biological score and must not be interpreted as biological burden.

---

## Audit Fields

Audit output should contain one row per run with:

```text
SRA
run_id
depth_category
stage_metrics_long_present
vdb_ready_variants_present
rdgp_gene_seed_present
stage12_validation_candidates_present
epi25_seed_present
mitocarta_seed_present
source_files_present
missing_expected_files
metrics_loaded
duckdb_scans_completed
substrate_summary_status
error_message
```

---

## Status Rules

### `source_files_present`

Pipe-delimited list of expected source files that exist.

### `missing_expected_files`

Pipe-delimited list of expected source files that are absent.

### `substrate_summary_status`

Allowed values:

```text
complete
complete_with_optional_missing
partial
failed
```

Initial implementation should treat all listed source files as required.

If all required files exist and all calculations complete:

```text
complete
```

If any required file is missing:

```text
partial
```

If an exception prevents row construction:

```text
failed
```

---

## Engine

Use:

```text
DuckDB
```

for large TSV scans.

Use:

```text
pandas
```

for:

* `stage_metrics_long.tsv` telemetry lookup
* reference gene-list loading
* final table assembly
* audit writing

---

## Validation Expectations

After running on MARK:

```bash
ls -lh /root/Desktop/substrate_dimension_summary/
```

Expected files:

```text
substrate_dimension_summary.new.tsv
substrate_dimension_summary_build_audit.tsv
```

Row-count check:

```bash
wc -l /root/Desktop/substrate_dimension_summary/substrate_dimension_summary.new.tsv
```

Expected:

```text
14
```

because there are 13 data rows plus header.

Audit check:

```bash
column -t -s $'\t' /root/Desktop/substrate_dimension_summary/substrate_dimension_summary_build_audit.tsv | less -S
```

Spot-check output:

```bash
column -t -s $'\t' /root/Desktop/substrate_dimension_summary/substrate_dimension_summary.new.tsv | less -S
```

Expected sanity checks:

```text
unique_overlay_genes = 1140
epilepsy_overlay_genes = 7
mito_overlay_genes = 1133
dual_epi_mito_overlay_genes = 0
overlay_evidence_modalities_present = 3
```

For `ERR10619300`, prior probes observed:

```text
unique_variant_ids = 736468
unique_genes_in_vdb_substrate = 41954
unique_rdgp_genes = 41953
variants_per_rdgp_gene_mean ≈ 17.5542
variants_per_rdgp_gene_median = 7.0
```

These values should reproduce for:

```text
ERR10619300 / run_2026_05_27_172531
```

---

## Implementation Notes

The implementation should favor correctness and explicitness over clever abstraction.

Recommended internal helpers:

```text
safe_divide(numerator, denominator)
metric_lookup(metrics_df, metric_name, default=None)
load_overlay_seed(path)
compute_distinct_vdb_metrics(path)
compute_rdgp_metrics(path)
compute_stage12_metrics(path, epi25_ids, mitocarta_ids)
build_run_row(...)
build_audit_row(...)
```

The first implementation should be verbose and auditable. Refactoring can happen later after output validation.
