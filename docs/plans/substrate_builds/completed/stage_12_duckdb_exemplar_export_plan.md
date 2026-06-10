# Implementation Plan — Stage 12 DuckDB Exploration and Exemplar Export Harness

This plan (`stage_12_duckdb_exemplar_export_plan.md`) is specific for CLI-only harvesting of `stage_12_validation_candidates.tsv`, using python and `DuckDB`, thus bypassing `DBeaver GUI` access. Because this plan covers CLI-usage only, this approach can scale to deterministically generate `stage_12_validation_candidates.tsv` exemplar exports across numerous VAP-processed SRAs.

Note: 

For the implementation plan that is GUI-based and thus utilizes `DBeaver GUI`, see:

`err10619281_exemplar_bucket_extraction_plan.md`

---

## Purpose

Implement a lightweight Python + DuckDB wrapper that reproducibly exports Stage 12 exploration artifacts from VAP run outputs.

The wrapper will convert a run-specific `stage_12_validation_candidates.tsv` into a local DuckDB database, generate value-count summaries, export tiered unique-gene summaries, and write LANE-oriented candidate bucket TSVs.

---

# Target Script

```text
scripts/analysis/export_stage12_duckdb_exploration.py
```

---

# Canonical Invocation

The script must accept relative paths from the VAP root repo.

From VAP repo root, with the VAP virtual environment activated:

```bash
python scripts/analysis/export_stage12_duckdb_exploration.py \
  results/run_<id>/processed/stage_12_validation_candidates.tsv
```

The same script must also accept absolute paths, for example:

```bash
python scripts/analysis/export_stage12_duckdb_exploration.py \
  /mnt/storage/vap_runs/results/run_<id>/processed/stage_12_validation_candidates.tsv
```

The `run_<id>` folder is dynamically-generated as a timestamp at time of VAP operation on SRA data.

---

## Example Invocation

For example, the SRA ERR10619281 was processed by VAP resulting in the `run_<id>` of `run_2026_05_27_233524`.

The script must accept relative paths from the VAP root repo with the VAP virtual environment activated:

```bash
python scripts/analysis/export_stage12_duckdb_exploration.py \
  results/run_2026_05_27_233524/processed/stage_12_validation_candidates.tsv
```

The same script must also accept absolute paths, for example:

```bash
python scripts/analysis/export_stage12_duckdb_exploration.py \
  /mnt/storage/vap_runs/results/run_2026_05_27_233524/processed/stage_12_validation_candidates.tsv
```

---

# Dependency Updates

Add to `requirements.txt` if not already present:

```text
duckdb
PyYAML
```

`duckdb` and `PyYAML` are Python packages installed into the project virtual environment via pip.

If `PyYAML` is already present, add only:

```text
duckdb
```

---

# Input Contract

The script is executed after a complete VAP run.  

- A complete VAP run on MARK has telemetry, metric emissions, and auto-rendered figures and tables.
- Each complete VAP run is timestamped with a unique `run_<id>` and VAP outputs are written to `<VAP repo root>/results/run_<id>/`.
- A typical complete VAP run generates 12 directories with 96 files.
- For our purposes, 2 of those 96 files are critical for this script.

A simplified directory tree of a complete run on MARK will look something like this:

```text
run_<id>/
├── figures/
├── final/
├── interim/
├── logs/
├── metadata/
│   └── config_snapshot.yaml
├── metrics/
├── processed/
│   └── stage_12_validation_candidates.tsv
├── reports/
└── validation/
```

For simplicity, only files relevant for the `export_stage12_duckdb_exploration.py` are shown above.

- `config_snapshot.yaml` is used to harvest SRA accession information
- `stage_12_validation_candidates.tsv` is a large TSV (~500 MB) that contains semantic-rich data for variants (rows).

---

## Script Argument

The script (`export_stage12_duckdb_exploration.py`) accepts one required positional argument:

```text
path/to/run_<id>/processed/stage_12_validation_candidates.tsv
```

The provided TSV must:

1. Exist.
2. Be named:

```text
stage_12_validation_candidates.tsv
```

3. Live under:

```text
run_<id>/processed/
```

## Script Inference

The script infers:

```text
processed_dir = tsv_path.parent
run_dir = processed_dir.parent
run_id = run_dir.name
config_path = run_dir / "metadata" / "config_snapshot.yaml"
```

The script reads:

```text
run_<id>/metadata/config_snapshot.yaml
```

to extract:

```yaml
input:
  sample_id
  sra_accession
  sample_alias
  assay_type
  bioproject_accession
```

At minimum, the script requires:

```text
input.sample_id
```

Recommended metadata fields, when available:

```text
input.sra_accession
input.sample_alias
input.assay_type
input.bioproject_accession
```

---

# Output Directory Contract

The script creates:

```text
run_<id>/logs/stage12_exploration/
```

with subfolders:

```text
run_<id>/logs/stage12_exploration/value_counts/
run_<id>/logs/stage12_exploration/unique_genes/
run_<id>/logs/stage12_exploration/lane_candidate_slices/
```

The script is executed after a complete VAP run, and adds the following to that specific run:

```text
run_<id>/
├── figures/
├── final/
├── interim/
├── logs/
│   ├── stage12_exploration/
│   │   ├── lane_candidate_slices/
│   │   │   ├── <sample_id>_bucket_1a_validation_routed_epilepsy_mito.tsv
│   │   │   ├── <sample_id>_bucket_1b_clinically_contextualized_epilepsy_mito.tsv
│   │   │   ├── <sample_id>_bucket_2a_rare_impact_coding_triage_summary.tsv
│   │   │   ├── <sample_id>_bucket_2b_rare_impact_tier2.tsv
│   │   │   ├── <sample_id>_bucket_2c_rare_impact_deprioritized.tsv
│   │   │   ├── <sample_id>_bucket_3a_clinvar_supported_deprioritized.tsv
│   │   │   ├── <sample_id>_bucket_3b_tier3_background_summary.tsv
│   │   │   └── <sample_id>_bucket_4a_representative_noncoding_semantic_exemplars.tsv
│   │   ├── unique_genes/
│   │   │   ├── <sample_id>_tier1_unique_genes.tsv
│   │   │   ├── <sample_id>_tier1_unique_genes_mito_epi_overlay.tsv
│   │   │   ├── <sample_id>_tier2_unique_genes.tsv
│   │   │   ├── <sample_id>_tier2_unique_genes_mito_epi_overlay.tsv
│   │   │   ├── <sample_id>_tier3_unique_genes.tsv
│   │   │   └── <sample_id>_tier3_unique_genes_mito_epi_overlay.tsv
│   │   ├── value_counts/
│   │   │   ├── value_counts__clinical_evidence.tsv
│   │   │   ├── value_counts__clinical_significance.tsv
│   │   │   ├── value_counts__clinical_status.tsv
│   │   │   ├── value_counts__clinvar_significance.tsv
│   │   │   ├── value_counts__coding_interpretation_label.tsv
│   │   │   ├── value_counts__consequence.tsv
│   │   │   ├── value_counts__epilepsy_flag.tsv
│   │   │   ├── value_counts__frequency_status.tsv
│   │   │   ├── value_counts__functional_impact.tsv
│   │   │   ├── value_counts__gene_mapping_status.tsv
│   │   │   ├── value_counts__impact_class.tsv
│   │   │   ├── value_counts__interpretability_status.tsv
│   │   │   ├── value_counts__is_clinically_supported.tsv
│   │   │   ├── value_counts__is_high_quality.tsv
│   │   │   ├── value_counts__is_lof_candidate.tsv
│   │   │   ├── value_counts__is_potential_artifact.tsv
│   │   │   ├── value_counts__is_rare_candidate.tsv
│   │   │   ├── value_counts__mito_flag.tsv
│   │   │   ├── value_counts__priority_tier.tsv
│   │   │   ├── value_counts__qc_reliability.tsv
│   │   │   ├── value_counts__qc_status.tsv
│   │   │   ├── value_counts__quality_flag.tsv
│   │   │   ├── value_counts__rarity_flag.tsv
│   │   │   ├── value_counts__source_interpretation_label.tsv
│   │   │   ├── value_counts__suggested_validation_method.tsv
│   │   │   ├── value_counts__validation_priority.tsv
│   │   │   ├── value_counts__validation_required.tsv
│   │   │   ├── value_counts__variant_class.tsv
│   │   │   ├── value_counts__variant_effect_severity.tsv
│   │   │   ├── value_counts__variant_origin.tsv
│   │   │   └── value_counts__variant_type.tsv
│   │   ├── <sample_id>_stage12_exploration.duckdb
│   │   ├── stage12_exploration_duckdb.log
│   │   └── stage12_exploration_manifest.tsv
├── metadata/
├── metrics/
├── processed/
├── reports/
└── validation/
```

---

## DuckDB Output File

The script writes the DuckDB file to:

```text
run_<id>/logs/stage12_exploration/<sample_id>_stage12_exploration.duckdb
```

Example:

```text
results/run_2026_05_27_233524/logs/stage12_exploration/ERR10619281_stage12_exploration.duckdb
```

---

## Logging Contract

The script must write a run-local log file to:

```text
run_<id>/logs/stage12_exploration/stage12_exploration_duckdb.log
```

The log must record:

1. Script start timestamp.
2. Input TSV path.
3. Inferred run_dir.
4. Inferred run_id.
5. Config snapshot path.
6. Parsed sample_id, sra_accession, assay_type, and bioproject_accession when available.
7. DuckDB database path.
8. Output directories created.
9. Row count loaded into main.stage12.
10. Each value-count file attempted.
11. Each unique-gene file attempted.
12. Each LANE bucket file attempted.
13. Files successfully written.
14. Files not written.
15. SQL/query errors, if any.
16. Final completion status.

The log file is a generated run artifact and should not be committed to Git.

---

# Query Failure Policy

The script must not abort the entire run if a non-critical export query fails.

For each export operation:

1. Attempt the query/export.
2. If successful:
   - write the TSV,
   - log success,
   - include the output path in the manifest.
3. If unsuccessful:
   - catch the exception,
   - log the failure,
   - record the intended output path as not written,
   - continue to the next export operation.

Critical failures should still stop execution. Critical failures include:

1. Missing input TSV.
2. Missing `config_snapshot.yaml`.
3. Missing required `input.sample_id`.
4. Failure to create output directories.
5. Failure to create/open DuckDB database.
6. Failure to load `main.stage12`.
7. Missing core required Stage 12 columns needed for most exports.

Non-critical failures include:

1. A value-count export for an optional column that is absent.
2. A specific bucket query failing.
3. A specific unique-gene export failing.
4. A file write failure for one export target.

The script should complete with a status such as:

```text
completed_with_warnings
```

if one or more non-critical exports fail.

---

# Canonical DuckDB Contract

The wrapper must create or replace a table named:

```sql
main.stage12
```

All internal SQL must reference:

```sql
main.stage12
```

The script must not hardcode DuckDB catalog names derived from database filenames.

---

# Execution Flow

## Step 1 — Resolve Input Paths

The script will:

1. Resolve the provided TSV path.
2. Confirm file existence.
3. Confirm filename equals `stage_12_validation_candidates.tsv`.
4. Infer `run_dir`.
5. Confirm `metadata/config_snapshot.yaml` exists.
6. Parse `sample_id` from config.

If any required input is missing, fail clearly.

---

## Step 2 — Create Output Folders

Create:

```text
logs/stage12_exploration/
logs/stage12_exploration/value_counts/
logs/stage12_exploration/unique_genes/
logs/stage12_exploration/lane_candidate_slices/
```

relative to the inferred `run_dir`.

---

## Step 3 — Create DuckDB Database

Open or create:

```text
<run_dir>/logs/stage12_exploration/<sample_id>_stage12_exploration.duckdb
```

Behavior:

1. Connect using Python `duckdb`.
2. Drop stale `main.stage12` if it exists.
3. Load TSV into `main.stage12` using DuckDB CSV reader.

Canonical load SQL:

```sql
DROP TABLE IF EXISTS stage12;

CREATE TABLE stage12 AS
SELECT *
FROM read_csv_auto(
    '<stage_12_validation_candidates.tsv>',
    delim='\t',
    header=true,
    all_varchar=true,
    sample_size=-1
);
```

Rationale:

`all_varchar=true` avoids type inference failures for fields such as `chromosome`, where values may include both numeric chromosomes and `MT`.

---

## Step 4 — Preflight Validation

After load, run:

```sql
SELECT COUNT(*) AS n_rows
FROM main.stage12;
```

and:

```sql
SELECT sample_id, run_id, COUNT(*) AS n_rows
FROM main.stage12
GROUP BY sample_id, run_id
ORDER BY n_rows DESC;
```

The script should print this to stdout.

Recommended optional validation:

1. Confirm required columns exist.
2. Confirm all observed `sample_id` values are consistent with config metadata.
3. Confirm all observed `run_id` values are consistent with inferred `run_dir.name`.
4. Print `log_path`

Do not silently continue if required columns are missing.

---

# Required Columns

The script must validate presence of these columns before export:

```text
alternate_allele
chromosome
clinical_evidence
clinical_significance
clinical_status
clinvar_significance
coding_interpretation_label
consequence
epilepsy_flag
frequency_status
functional_impact
gene_id
gene_mapping_status
gene_symbol
gnomad_af
impact_class
interpretability_status
is_clinically_supported
is_high_quality
is_lof_candidate
is_potential_artifact
is_rare_candidate
mito_flag
position
priority_rank
priority_reason
priority_tier
qc_reliability
qc_status
quality_flag
rarity_flag
reference_allele
run_id
sample_id
source_interpretation_label
suggested_validation_method
validation_priority
validation_required
variant_class
variant_effect_severity
variant_id
variant_origin
variant_type
```

Additional columns may exist and should be preserved in the database.

---

# Step 5 — Export Value Counts

Export value-count TSVs for key semantic columns to:

```text
<run_dir>/logs/stage12_exploration/value_counts/
```

Recommended key columns:

```text
clinical_evidence
clinical_significance
clinical_status
clinvar_significance
coding_interpretation_label
consequence
epilepsy_flag
frequency_status
functional_impact
gene_mapping_status
impact_class
interpretability_status
is_clinically_supported
is_high_quality
is_lof_candidate
is_potential_artifact
is_rare_candidate
mito_flag
priority_tier
qc_reliability
qc_status
quality_flag
rarity_flag
source_interpretation_label
suggested_validation_method
validation_priority
validation_required
variant_class
variant_effect_severity
variant_origin
variant_type
```

For each available column, export:

```text
value_counts__<column>.tsv
```

using:

```sql
SELECT
    <column>,
    COUNT(*) AS count
FROM main.stage12
GROUP BY <column>
ORDER BY count DESC, <column> ASC;
```

If a recommended column is missing, report it and skip that value-count export.

---

# Step 6 — Export Tiered Unique Genes

Export unique-gene summary files to:

```text
<run_dir>/logs/stage12_exploration/unique_genes/
```

Output files come in two forms across 3 tiers of priority:

- unique genes
- unique genes with mitochondria + epilepsy overlays

Required output files:

```text
<sample_id>_tier1_unique_genes.tsv
<sample_id>_tier1_unique_genes_mito_epi_overlay.tsv
<sample_id>_tier2_unique_genes.tsv
<sample_id>_tier2_unique_genes_mito_epi_overlay.tsv
<sample_id>_tier3_unique_genes.tsv
<sample_id>_tier3_unique_genes_mito_epi_overlay.tsv
```

Each file should contain:

```text
gene_symbol
n_variants
```

Tier filters:

```sql
priority_tier LIKE 'tier_1%'
priority_tier LIKE 'tier_2%'
priority_tier LIKE 'tier_3%'
```

## Explicit SQL Code Usage for Tiered Unique Genes

SQL blocks below are query bodies. The Python wrapper must embed each query body inside DuckDB COPY (...) TO '<output>' WITH (HEADER, DELIMITER '\t').

### Tiered Unique Genes WITHOUT Mitochondria + Epilepsy Overlay

1. For writing the `<sample_id>_tier1_unique_genes.tsv` file, use this precise sql code pattern:

```sql
SELECT
    gene_symbol,
    COUNT(*) AS n_variants
FROM main.stage12
WHERE priority_tier LIKE 'tier_1%'
AND gene_symbol IS NOT NULL
AND gene_symbol != ''    
GROUP BY gene_symbol
ORDER BY n_variants DESC, gene_symbol ASC
```

2. For writing the `<sample_id>_tier2_unique_genes.tsv` file, use this precise sql code pattern:

```sql
SELECT
    gene_symbol,
    COUNT(*) AS n_variants
FROM main.stage12
WHERE priority_tier LIKE 'tier_2%'
AND gene_symbol IS NOT NULL
AND gene_symbol != ''
GROUP BY gene_symbol
ORDER BY n_variants DESC, gene_symbol ASC
```

3. For writing the `<sample_id>_tier3_unique_genes.tsv` file, use this precise sql code pattern:

```sql
SELECT
    gene_symbol,
    COUNT(*) AS n_variants
FROM main.stage12
WHERE priority_tier LIKE 'tier_3%'
AND gene_symbol IS NOT NULL
AND gene_symbol != ''    
GROUP BY gene_symbol
ORDER BY n_variants DESC, gene_symbol ASC
```

---

### Tiered Unique Genes WITH Mitochondria + Epilepsy Overlay

4. For writing the `<sample_id>_tier1_unique_genes_mito_epi_overlay.tsv` file, use this precise sql code pattern:

```sql
SELECT
    gene_symbol,
    COUNT(*) AS n_variants
FROM main.stage12
WHERE priority_tier LIKE 'tier_1%'
AND gene_symbol IS NOT NULL
AND gene_symbol != ''
AND variant_class='coding'
AND (epilepsy_flag='True' OR mito_flag='True')   
GROUP BY gene_symbol
ORDER BY n_variants DESC, gene_symbol ASC
```

5. For writing the `<sample_id>_tier2_unique_genes_mito_epi_overlay.tsv` file, use this precise sql code pattern:

```sql
SELECT
    gene_symbol,
    COUNT(*) AS n_variants
FROM main.stage12
WHERE priority_tier LIKE 'tier_2%'
AND gene_symbol IS NOT NULL
AND gene_symbol != ''
AND variant_class='coding'
AND (epilepsy_flag='True' OR mito_flag='True')   
GROUP BY gene_symbol
ORDER BY n_variants DESC, gene_symbol ASC
```

6. For writing the `<sample_id>_tier3_unique_genes_mito_epi_overlay.tsv` file, use this precise sql code pattern:

```sql
SELECT
    gene_symbol,
    COUNT(*) AS n_variants
FROM main.stage12
WHERE priority_tier LIKE 'tier_3%'
AND gene_symbol IS NOT NULL
AND gene_symbol != ''
AND variant_class='coding'
AND (epilepsy_flag='True' OR mito_flag='True')   
GROUP BY gene_symbol
ORDER BY n_variants DESC, gene_symbol ASC
```

---

# Step 7 — Export LANE Candidate Bucket Slices

Export LANE-oriented candidate TSVs to:

```text
logs/stage12_exploration/lane_candidate_slices/
```

Required exports:

```text
<sample_id>_bucket_1a_validation_routed_epilepsy_mito.tsv
<sample_id>_bucket_1b_clinically_contextualized_epilepsy_mito.tsv
<sample_id>_bucket_2a_rare_impact_coding_triage_summary.tsv
<sample_id>_bucket_2b_rare_impact_tier2.tsv
<sample_id>_bucket_2c_rare_impact_deprioritized.tsv
<sample_id>_bucket_3a_clinvar_supported_deprioritized.tsv
<sample_id>_bucket_3b_tier3_background_summary.tsv
<sample_id>_bucket_4a_representative_noncoding_semantic_exemplars.tsv
```

## Explicit SQL Code Usage for Buckets

SQL blocks below are query bodies. The Python wrapper must embed each query body inside DuckDB COPY (...) TO '<output>' WITH (HEADER, DELIMITER '\t').

Use the following sql code precisely for provenance and reproducibility purposes.

### Bucket 1A: Validation-Routed Epilepsy- and Mitochondrial-Enriched Candidate Coding Variants

For writing `<sample_id>_bucket_1a_validation_routed_epilepsy_mito.tsv`, use this precise SQL code pattern:

```sql
SELECT sample_id, run_id, chromosome, position, reference_allele, alternate_allele, variant_id, gene_symbol, gene_id, variant_class, consequence, functional_impact, clinical_significance, clinical_status, is_clinically_supported, frequency_status, gnomad_af, epilepsy_flag, mito_flag, priority_tier, priority_rank, priority_reason, validation_required, validation_priority, suggested_validation_method, interpretability_status, coding_interpretation_label, qc_status
FROM main.stage12
WHERE variant_class='coding'
AND is_clinically_supported='True'
AND (epilepsy_flag='True' OR mito_flag='True')
AND validation_required='True'
ORDER BY priority_rank ASC, validation_priority ASC, gene_symbol ASC
```

---

### Bucket 1B: Clinically-Contextualized Epilepsy- and Mitochondrial-Enriched Candidate Coding Variants

For writing `<sample_id>_bucket_1b_clinically_contextualized_epilepsy_mito.tsv`, use this precise SQL code pattern:

```sql
SELECT sample_id, run_id, chromosome, position, reference_allele, alternate_allele, variant_id, gene_symbol, gene_id, variant_class, consequence, functional_impact, clinical_significance, clinical_status, is_clinically_supported, frequency_status, gnomad_af, epilepsy_flag, mito_flag, priority_tier, priority_rank, priority_reason, validation_required, validation_priority, suggested_validation_method, interpretability_status, coding_interpretation_label, qc_status
FROM main.stage12
WHERE variant_class='coding'
AND is_clinically_supported='True'
AND (epilepsy_flag='True' OR mito_flag='True')
ORDER BY validation_required DESC, priority_rank ASC, gene_symbol ASC
```

---

### Bucket 2A: Triage Summary of Rare Frequency, Functional Impacts in Candidate Coding Variants

For writing `<sample_id>_bucket_2a_rare_impact_coding_triage_summary.tsv`, use this precise SQL code pattern:

```sql
SELECT functional_impact, priority_tier, validation_required, COUNT(*) AS n
FROM main.stage12
WHERE variant_class='coding'
AND frequency_status='rare'
AND functional_impact IN ('missense', 'loss_of_function', 'splice_relevant')
GROUP BY functional_impact, priority_tier, validation_required
ORDER BY n DESC, functional_impact ASC, priority_tier ASC, validation_required DESC
```

---

### Bucket 2B: Tier 2 Prioritized Candidate Coding Variants with Rare Frequency, Functional Impacts

For writing `<sample_id>_bucket_2b_rare_impact_tier2.tsv`, use this precise SQL code pattern:

```sql
SELECT sample_id, run_id, chromosome, position, reference_allele, alternate_allele, variant_id, gene_symbol, gene_id, variant_class, consequence, functional_impact, clinical_significance, clinical_status, is_clinically_supported, frequency_status, gnomad_af, epilepsy_flag, mito_flag, priority_tier, priority_rank, priority_reason, validation_required, validation_priority, suggested_validation_method, interpretability_status, coding_interpretation_label, qc_status
FROM main.stage12
WHERE variant_class='coding'
AND frequency_status='rare'
AND functional_impact IN ('missense', 'loss_of_function', 'splice_relevant')
AND priority_tier LIKE 'tier_2%'
ORDER BY is_clinically_supported DESC, epilepsy_flag DESC, mito_flag DESC, functional_impact ASC, gene_symbol ASC
LIMIT 15
```

---

### Bucket 2C: Deprioritized Candidate Coding Variants with Rare Frequency, Functional Impacts

For writing `<sample_id>_bucket_2c_rare_impact_deprioritized.tsv`, use this precise SQL code pattern:

```sql
SELECT sample_id, run_id, chromosome, position, reference_allele, alternate_allele, variant_id, gene_symbol, gene_id, variant_class, consequence, functional_impact, clinical_significance, clinical_status, is_clinically_supported, frequency_status, gnomad_af, epilepsy_flag, mito_flag, priority_tier, priority_rank, priority_reason, validation_required, validation_priority, suggested_validation_method, interpretability_status, coding_interpretation_label, qc_status
FROM main.stage12
WHERE variant_class = 'coding'
AND frequency_status = 'rare'
AND functional_impact IN ('missense', 'loss_of_function', 'splice_relevant')
AND validation_required = 'False'
AND (priority_tier LIKE 'tier_3%' OR priority_tier LIKE 'tier_4%')
ORDER BY is_clinically_supported DESC, epilepsy_flag DESC, mito_flag DESC, functional_impact ASC, gene_symbol ASC
LIMIT 15
```

---

### Bucket 3A: Deprioritized Candidate Coding Variants with Clinical Support and Mitochondrial or Epilepsy Gene Evidence

For writing `<sample_id>_bucket_3a_clinvar_supported_deprioritized.tsv`, use this precise SQL code pattern:

```sql
SELECT sample_id, run_id, chromosome, position, reference_allele, alternate_allele, variant_id, gene_symbol, gene_id, variant_class, consequence, functional_impact, clinical_significance, clinical_status, is_clinically_supported, frequency_status, gnomad_af, epilepsy_flag, mito_flag, priority_tier, priority_rank, priority_reason, validation_required, validation_priority, suggested_validation_method, interpretability_status, coding_interpretation_label, qc_status
FROM main.stage12
WHERE variant_class='coding'
AND validation_required='False'
AND priority_tier LIKE 'tier_3%'
AND is_clinically_supported='True'
ORDER BY epilepsy_flag DESC, mito_flag DESC, frequency_status ASC, gene_symbol ASC
LIMIT 15
```

---

### Bucket 3B: Deprioritized Candidate Coding Variant Summary with Clinical Support

For writing `<sample_id>_bucket_3b_tier3_background_summary.tsv`, use this precise SQL code pattern:

```sql
SELECT functional_impact, frequency_status, is_clinically_supported, COUNT(*) AS n
FROM main.stage12
WHERE variant_class='coding'
AND validation_required='False'
AND priority_tier LIKE 'tier_3%'
GROUP BY functional_impact, frequency_status, is_clinically_supported
ORDER BY n DESC, functional_impact ASC, frequency_status ASC, is_clinically_supported DESC
```

---

### Bucket 4A: Representative Noncoding Candidate Variants of Rare Frequency and Clinical Support or Association to Mitochondrial Function or Epilepsy Manifestation

For writing `<sample_id>_bucket_4a_representative_noncoding_semantic_exemplars.tsv`, use this precise SQL code pattern:

```sql
SELECT sample_id, run_id, chromosome, position, reference_allele, alternate_allele, variant_id, gene_symbol, gene_id, variant_class, consequence, functional_impact, clinical_significance, clinical_status, is_clinically_supported, frequency_status, gnomad_af, epilepsy_flag, mito_flag, priority_tier, priority_rank, priority_reason, validation_required, validation_priority, suggested_validation_method, interpretability_status, qc_status
FROM main.stage12
WHERE variant_class='noncoding'
AND frequency_status='rare'
AND (epilepsy_flag='True' OR mito_flag='True' OR is_clinically_supported='True')
ORDER BY is_clinically_supported DESC, epilepsy_flag DESC, mito_flag DESC, priority_rank ASC, gene_symbol ASC
LIMIT 15
```

---

# Step 8 — Export Run Manifest Summary

Write a small metadata summary file to:

```text
logs/stage12_exploration/stage12_exploration_manifest.tsv
```

Recommended columns:

```text
sample_id
sra_accession
sample_alias
assay_type
bioproject_accession
run_id
run_dir
input_tsv
duckdb_path
n_stage12_rows
value_counts_dir
unique_genes_dir
lane_candidate_slices_dir
status
n_files_attempted
n_files_written
n_files_failed
log_path
failed_outputs
```

This makes downstream harvesting easier on MARK and sys76.

---

# Step 9 — Print Final Summary

At completion, print:

```text
Stage12 DuckDB exploration complete.
Sample ID: <sample_id>
Run ID: <run_id>
Rows loaded: <n>
DuckDB: <path>
Value counts: <path>
Unique genes: <path>
LANE candidate slices: <path>
Manifest: <path>
```

---

# File Placement in VAP Repo

Tracked code:

```text
scripts/analysis/export_stage12_duckdb_exploration.py
```

Tracked documentation:

```text
docs/contracts/system/stage12_duckdb_exploration_contract.md
docs/plans/stage12_duckdb_exploration_implementation_plan.md
docs/templates/stage12_exploration_executive_summary_template.md
docs/case_studies/err10619281/err10619281_exemplar_bucket_extraction_plan.md
docs/case_studies/err10619281/executive_summary_err10619281_explore_stage12.md
```

Optional tracked SQL references:

```text
scripts/analysis/sql/stage12_load_prioritized_variant_candidates.sql
scripts/analysis/sql/stage12_exploration.sql
scripts/analysis/sql/stage12_exemplar_bucket_exports.sql
```

Generated artifacts must remain untracked.

---

# Git Ignore Requirements

Ensure `.gitignore` excludes:

```text
*.duckdb
*.duckdb.wal
results/
```

If run artifacts outside `results/` are possible, also exclude generated Stage 12 exploration outputs by pattern.

---

# MARK Compatibility

The script must work from VAP repo root on MARK with repo-relative paths, for example:

```bash
python scripts/analysis/export_stage12_duckdb_exploration.py \
  results/run_2026_05_27_233524/processed/stage_12_validation_candidates.tsv
```

This allows bulky TSVs and generated DuckDB files to remain on MARK.

The user can harvest only small generated TSV outputs from:

```text
results/run_<id>/logs/stage12_exploration/
```

---

# sys76 Compatibility

The same script must work on sys76 with absolute storage paths, for example:

```bash
python scripts/analysis/export_stage12_duckdb_exploration.py \
  /mnt/storage/vap_runs/results/run_2026_05_27_233524/processed/stage_12_validation_candidates.tsv
```

---

# Future Multi-Run Extension

For near-term use, the script processes one run at a time.

Future extension may add:

```bash
python scripts/analysis/export_stage12_duckdb_exploration.py \
  --manifest stage12_runs.tsv
```

where `stage12_runs.tsv` contains one Stage 12 TSV path per row.

This would support systematic execution across numerous VAP-completed WES SRA runs.

Do not implement manifest mode in the first version unless needed.

---

# Acceptance Criteria

The implementation is complete when:

1. The script runs from VAP repo root.
2. The script accepts a single Stage 12 TSV path.
3. The script derives `run_dir`, `run_id`, and `sample_id`.
4. The script creates a run-local DuckDB database.
5. The script loads TSV into `main.stage12` with all columns as strings.
6. The script exports value counts.
7. The script exports Tier 1, Tier 2, and Tier 3 unique-gene files.
8. The script exports all required LANE candidate bucket TSVs.
9. The script writes a manifest summary.
10. The script prints a clear completion report.
11. The original TSV is never modified.
12. Generated artifacts remain outside Git tracking.
13. The script writes `run_<id>/logs/stage12_exploration/stage12_exploration_duckdb.log`.
14. The log records input path, inferred metadata, DuckDB path, attempted outputs, successful outputs, failed outputs, and query errors.
15. A failed individual export does not abort the full script.
16. The final manifest records files written and files not written.
17. The script exits cleanly with warning status if non-critical exports fail.

---