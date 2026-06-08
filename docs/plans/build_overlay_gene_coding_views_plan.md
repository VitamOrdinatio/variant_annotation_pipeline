# Implementation Plan — scripts/mark/build_overlay_gene_coding_views.py

Used in cross-run case study contrast 2

# Objective

Build three append-ready global overlay gene coding update files from the 13 completed VAP runs on MARK:

```text
overlay_gene_coding_clinical_evidence.new.tsv
overlay_gene_coding_frequency_profiles.new.tsv
overlay_gene_coding_functional_impact.new.tsv
```

The validated clinical-evidence output must remain backward-compatible and must not be semantically altered while adding the two new views.

The script is executed from MARK's VAP repo root.

The script will parse each run’s canonical:

`results/<run_id>/processed/stage_12_validation_candidates.tsv`

and obtain specific metadata fields from:

`results/<run_id>/metrics/stage_metrics_long.tsv`

and write outputs to:

`/root/Desktop/overlay_gene_coding/`

---

# Inputs

## Manifest Inputs

The script will use an internal 13-row manifest:

```text

| SRA           | run_<id>                | Depth Category | 
| --------------| ----------------------- | -------------- |
| `ERR10619203` | `run_2026_05_30_071639` | q3             |
| `ERR10619207` | `run_2026_06_01_124134` | q3             | 
| `ERR10619208` | `run_2026_05_30_151355` | median         |
| `ERR10619212` | `run_2026_05_30_214724` | q1             |
| `ERR10619225` | `run_2026_05_31_091242` | q3             | 
| `ERR10619230` | `run_2026_06_01_004903` | q3             | 
| `ERR10619241` | `run_2026_06_02_052302` | q1             | 
| `ERR10619281` | `run_2026_05_27_233524` | median         |
| `ERR10619285` | `run_2026_06_02_124300` | median         | 
| `ERR10619300` | `run_2026_05_27_172531` | median         |
| `ERR10619309` | `run_2026_06_02_181024` | q1             | 
| `ERR10619330` | `run_2026_06_01_203130` | q1             | 
| `SRR12898354` | `run_2026_06_03_010030` | hg002          | 
```

It will not auto-discover runs.

---

# Gene List Inputs

The script will read two explicit overlay seed files from MARK's VAP repo:

```text
data/reference/gene_lists/epi25_vap_overlay_seed.tsv
data/reference/gene_lists/mitocarta_vap_overlay_seed.tsv
```

These files define overlay membership.

The script should normalize/strip whitespace from gene-list column names before use.

Overlay matching is performed by:

```text
stage_12_validation_candidates.gene_id
    matched to
overlay_seed.ensembl_gene_id
```

Only records with non-empty `gene_id` and `non-empty` gene_symbol are eligible for output.

---

# Metadata Inputs

For each manifest run, the script will also read:

```text
results/<run_id>/metrics/stage_metrics_long.tsv
```

The script will use the row where:

```text
metric_name == validation_candidates_rows
```

to obtain:

```text
assay_type
run_classification
```

These metadata fields are then propagated into `overlay_gene_coding_clinical_evidence.new.tsv`.

---

# Outputs

Outputs are written to MARK's extraction point (`/root/Desktop/overlay_gene_coding/`):

```text
/root/Desktop/overlay_gene_coding/
├── overlay_gene_coding_clinical_evidence.new.tsv
├── overlay_gene_coding_frequency_profiles.new.tsv
├── overlay_gene_coding_functional_impact.new.tsv
└── overlay_gene_coding_views_build_audit.tsv
```

---

# Clinical Evidence Filtering Logic

For each `stage_12_validation_candidates.tsv`, include rows where:

```text
variant_origin == coding
AND gene_id is not empty
AND gene_symbol is not empty
AND gene_id is present in either:
    data/reference/gene_lists/epi25_vap_overlay_seed.tsv
    OR
    data/reference/gene_lists/mitocarta_vap_overlay_seed.tsv
```

The script should not rely on `mito_flag` or `epilepsy_flag` as the primary inclusion rule.

Those fields may be useful for audit/debugging, but the authoritative overlay membership for this output comes from the explicit gene-list seed files.

No gene-size normalization will be attempted here.

---

# Boolean Flag Handling

This first clinical-evidence implementation does not use `mito_flag` or `epilepsy_flag` as the authoritative overlay inclusion rule.

Overlay membership is determined by explicit Ensembl gene ID membership in:

```text
data/reference/gene_lists/epi25_vap_overlay_seed.tsv
data/reference/gene_lists/mitocarta_vap_overlay_seed.tsv
```

The `mito_flag` and `epilepsy_flag` columns may be inspected later for debugging or concordance checks, but they are not required for primary filtering.

---

# Clinical Evidence Overlay Logic

For each included coding candidate row:

```text
if gene_id is present in mitocarta_vap_overlay_seed.tsv:
    mitocarta_hit = True

if gene_id is present in epi25_vap_overlay_seed.tsv:
    epi25_hit = True
```

Each included row may generate one or two overlay records:

```text
mitocarta_hit == True  → overlay_source = mitocarta
epi25_hit == True      → overlay_source = epi25_all_epilepsy
```

If both are true, the variant contributes once to each `overlay_source`.

For each emitted record:

```text
match_key = ensembl_gene_id
```

Overlay source summary fields are:

```text
overlay_source_count = number of overlay lists containing the gene_id
overlay_source_list  = pipe-delimited list of all matched overlay sources
```

Recommended ordering for `overlay_source_list`:

```text
epi25_all_epilepsy|mitocarta
```

when both are present.

---

# Output — Clinical Evidence View

The script will generate:

`overlay_gene_coding_clinical_evidence.new.tsv`

with columns in this exact order:

```text
sample_id
run_id
assay_type
run_classification
gene_id
gene_symbol
overlay_source
overlay_source_count
overlay_source_list
mitocarta_hit
epi25_hit
match_key
clinical_evidence
clinical_status
variant_count
```

Group by all columns except `variant_count`.

Count rows as:

`variant_count`

The output is gene-level/semantic-category aggregation, not variant-level export.

---

# Output — Frequency Profile View

The script will generate:

`overlay_gene_coding_frequency_profiles.new.tsv`

with columns in this exact order:

```text
sample_id
run_id
assay_type
run_classification
gene_id
gene_symbol
overlay_source
overlay_source_count
overlay_source_list
mitocarta_hit
epi25_hit
match_key
frequency_status
rarity_flag
variant_count
```

Group by all columns except variant_count.

# Output — Functional Impact View

The script will generate:

`overlay_gene_coding_functional_impact.new.tsv`

with columns in this exact order:

```text
sample_id
run_id
assay_type
run_classification
gene_id
gene_symbol
overlay_source
overlay_source_count
overlay_source_list
mitocarta_hit
epi25_hit
match_key
functional_impact
variant_count
```

Group by all columns except `variant_count`.

---

# Backward Compatibility Requirement

The existing validated clinical-evidence view must not change except for removal of temporary debug console output.

Known validated row counts that must continue to reproduce:

```text
ERR10619281  → 510 rows
ERR10619300  → 465 rows
SRR12898354  → 474 rows
```

---

# Audit Behavior

The audit file should record, per run:

```text
sample_id
run_id
depth_category
input_path
input_exists
rows_scanned
coding_rows_scanned
eligible_gene_id_rows
overlay_matched_rows
clinical_evidence_rows_written
frequency_profile_rows_written
functional_impact_rows_written
mitocarta_gene_matches
epi25_gene_matches
both_overlay_gene_matches
status
```

The audit should also record whether both seed files were found and how many unique Ensembl gene IDs were loaded from each.

---

# Engine

Use DuckDB for TSV scanning and aggregation because HG002’s `stage_12_validation_candidates.tsv` is multi-GB.

The script should use explicit column names from `stage_12_validation_candidates.tsv`.

The script should normalize gene-list seed column names using `.strip()` before selecting `ensembl_gene_id`, because seed headers may contain trailing whitespace.

The script does not need boolean normalization for primary overlay membership in this first clinical-evidence implementation because overlay membership is defined by explicit seed-list joins.

---

# Safety Rules

The script:

- WILL read from results/<run_id>/processed/
- WILL write only to /root/Desktop/overlay_gene_coding/
- WILL NOT modify or delete source files
- WILL NOT append directly to existing global files
- WILL NOT auto-discover run directories

---

# Backward Compatibility Validation Targets

Before attempting full cohort generation and append workflows, the first operational validation goal is to determine whether the script can approximately replicate known row counts already observed in existing overlay outputs.

Known reference counts:

```text
ERR10619281  → 510 rows
ERR10619300  → 465 rows
SRR12898354  → 474 rows
```

Note that SRR12898354 = HG002.


These counts represent the current observed output sizes for:

```text
overlay_gene_coding_clinical_evidence.tsv
```

The validation count is the number of aggregated output rows per `(sample_id, run_id)`, not the sum of `variant_count`.

The first-pass implementation should therefore be validated against these approximate retrieval counts.

Large row counts are expected because:

- the overlay outputs are variant-derived semantic aggregation tables,
- genes may contribute multiple variants,
- multiple semantic categories may exist per gene,
- no gene-size normalization is being performed,
- and genes overlapping both overlay lists may contribute to multiple overlay records.

Exact row-count equivalence is preferred, but small discrepancies may reveal:

- overlay membership differences,
- duplicate handling differences,
- grouping-key differences,
- or prior-generation logic drift.

The audit file should therefore include:

```text
rows_written
```

per run for rapid comparison against historical outputs.

---

# Validation Expectations

After running, inspect:

```bash
ls -lh /root/Desktop/overlay_gene_coding/
head /root/Desktop/overlay_gene_coding/*.new.tsv
column -t -s $'\t' /root/Desktop/overlay_gene_coding/overlay_gene_coding_views_build_audit.tsv | less -S
```

Additional quick validation:

```bash
for f in /root/Desktop/overlay_gene_coding/*.new.tsv; do
  echo "$f"
  awk -F'\t' '
  NR>1 {count[$1 FS $2]++}
  END {for (k in count) print k, count[k]}
  ' "$f" | sort
  echo
done
```

If both validation blocks pass, then manually transfer the .new.tsv outputs back to sys76 for review and append.


# Appendix: Mapping


## `stage_12_validation_candidates.tsv` Column Names

- sample_id
- run_id
- source_pipeline
- variant_id
- chromosome
- position
- reference_allele
- alternate_allele
- variant_type
- variant_class
- quality_flag
- gene_id
- gene_symbol
- transcript_id
- consequence
- impact_class
- clinical_significance
- clinvar_significance
- population_frequency
- gnomad_af
- exac_af
- thousand_genomes_af
- mito_flag
- epilepsy_flag
- annotation_source
- annotation_version
- gene_mapping_status
- variant_context
- variant_effect_severity
- qc_status
- interpretability_status
- frequency_status
- clinical_status
- functional_impact
- rarity_flag
- clinical_evidence
- qc_reliability
- coding_interpretation_label
- is_lof_candidate
- is_rare_candidate
- is_clinically_supported
- is_high_quality
- is_potential_artifact
- variant_origin
- source_interpretation_label
- priority_tier
- priority_rank
- priority_reason
- is_high_priority_candidate
- is_moderate_priority_candidate
- is_low_priority_candidate
- is_uninterpretable
- validation_required
- validation_priority
- suggested_validation_method
- validation_reason

## `overlay_gene_coding_clinical_evidence.tsv` Column Mapping

| overlay TSV column | source / rule |
|---|---|
| sample_id | `stage_12_validation_candidates.tsv.sample_id` |
| run_id | `stage_12_validation_candidates.tsv.run_id` |
| assay_type | `stage_metrics_long.tsv` where `metric_name == validation_candidates_rows` |
| run_classification | `stage_metrics_long.tsv` where `metric_name == validation_candidates_rows` |
| gene_id | `stage_12_validation_candidates.tsv.gene_id` |
| gene_symbol | `stage_12_validation_candidates.tsv.gene_symbol` |
| overlay_source | script-derived: `mitocarta` or `epi25_all_epilepsy` |
| overlay_source_count | number of overlay seed lists containing `gene_id` |
| overlay_source_list | pipe-delimited list of all matched overlay sources |
| mitocarta_hit | script-derived from MitoCarta seed membership |
| epi25_hit | script-derived from EPI25 seed membership |
| match_key | constant string: `ensembl_gene_id` |
| clinical_evidence | `stage_12_validation_candidates.tsv.clinical_evidence` |
| clinical_status | `stage_12_validation_candidates.tsv.clinical_status` |
| variant_count | grouped row count calculated by script |

---

## `overlay_gene_coding_frequency_profiles.tsv` Column Mapping

| overlay TSV column | source / rule |
|---|---|
| sample_id | `stage_12_validation_candidates.tsv.sample_id` |
| run_id | `stage_12_validation_candidates.tsv.run_id` |
| assay_type | `stage_metrics_long.tsv` where `metric_name == validation_candidates_rows` |
| run_classification | `stage_metrics_long.tsv` where `metric_name == validation_candidates_rows` |
| gene_id | `stage_12_validation_candidates.tsv.gene_id` |
| gene_symbol | `stage_12_validation_candidates.tsv.gene_symbol` |
| overlay_source | script-derived: `mitocarta` or `epi25_all_epilepsy` |
| overlay_source_count | number of overlay seed lists containing `gene_id` |
| overlay_source_list | pipe-delimited list of all matched overlay sources |
| mitocarta_hit | script-derived from MitoCarta seed membership |
| epi25_hit | script-derived from EPI25 seed membership |
| match_key | constant string: `ensembl_gene_id` |
| frequency_status | `stage_12_validation_candidates.tsv.frequency_status` |
| rarity_flag | `stage_12_validation_candidates.tsv.rarity_flag` |
| variant_count | grouped row count calculated by script |

---

## `overlay_gene_coding_functional_impact.tsv` Column Mapping

| overlay TSV column | source / rule |
|---|---|
| sample_id | `stage_12_validation_candidates.tsv.sample_id` |
| run_id | `stage_12_validation_candidates.tsv.run_id` |
| assay_type | `stage_metrics_long.tsv` where `metric_name == validation_candidates_rows` |
| run_classification | `stage_metrics_long.tsv` where `metric_name == validation_candidates_rows` |
| gene_id | `stage_12_validation_candidates.tsv.gene_id` |
| gene_symbol | `stage_12_validation_candidates.tsv.gene_symbol` |
| overlay_source | script-derived: `mitocarta` or `epi25_all_epilepsy` |
| overlay_source_count | number of overlay seed lists containing `gene_id` |
| overlay_source_list | pipe-delimited list of all matched overlay sources |
| mitocarta_hit | script-derived from MitoCarta seed membership |
| epi25_hit | script-derived from EPI25 seed membership |
| match_key | constant string: `ensembl_gene_id` |
| functional_impact | `stage_12_validation_candidates.tsv.functional_impact` |
| variant_count | grouped row count calculated by script |

---

## Gene List References

7 unique genes on Epi25 all epilepsy list:
- `data/reference/gene_lists/epi25_vap_overlay_seed.tsv`

1,133 unique genes on MitoCarta list:
- `data/reference/gene_lists/mitocarta_vap_overlay_seed.tsv`
