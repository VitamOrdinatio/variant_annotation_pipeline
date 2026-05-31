# System Contract — Stage 12 DuckDB Exploration and Exemplar Export Harness

## Purpose

This contract defines a lightweight, reproducible Stage 12 exploration workflow for VAP run outputs.

The system converts a large `stage_12_validation_candidates.tsv` file into a local DuckDB database, then executes standardized SQL-derived analyses to generate small, case-study-ready TSV artifacts.

This workflow supports exploratory and narrative downstream analysis. It is not part of the core VAP variant-calling pipeline and does not make diagnostic claims.

---

# Scope

## In Scope

This system supports:

1. Loading a Stage 12 TSV into DuckDB.
2. Creating a canonical table named:

```sql
main.stage12
```

3. Running reproducible SQL queries against `main.stage12`.

4. Exporting small bucket-specific TSVs for:

   * Stage 12 executive summaries,
   * LANE case-study candidate review,
   * representative variant/gene exemplars,
   * semantic triage documentation.

5. Reusing the same logic across multiple WES SRAs.

## Out of Scope

This system does not:

1. Modify the original Stage 12 TSV.
2. Replace the core VAP pipeline.
3. Perform clinical interpretation.
4. Persist generated TSVs in Git.
5. Require a production database server.
6. Implement VDB-scale warehouse logic.

---

# Canonical Inputs

Each analyzed run must provide:

```text
<run_dir>/processed/stage_12_validation_candidates.tsv
```

The Stage 12 TSV is treated as the immutable source artifact.

Expected key columns include:

```text
sample_id
run_id
variant_id
chromosome
position
reference_allele
alternate_allele
gene_symbol
gene_id
variant_class
consequence
functional_impact
clinical_significance
clinical_status
is_clinically_supported
frequency_status
gnomad_af
epilepsy_flag
mito_flag
priority_tier
priority_rank
priority_reason
validation_required
validation_priority
suggested_validation_method
interpretability_status
coding_interpretation_label
qc_status
```

---

# Canonical DuckDB Table Contract

Every run-specific DuckDB database must contain:

```sql
main.stage12
```

All reusable SQL must reference:

```sql
FROM main.stage12
```

Reusable SQL must not hardcode run-specific catalog names such as:

```sql
FROM stage12_exploration.main.stage12
```

This ensures the same SQL logic can run against any active DuckDB connection.

---

# Per-Run DuckDB Database Contract

Each SRA/run should have its own DuckDB file.

Recommended naming:

```text
<sample_id>_stage12_exploration.duckdb
```

Example:

```text
err10619281_stage12_exploration.duckdb
err10619300_stage12_exploration.duckdb
```

Recommended location:

```text
<run_dir>/logs/stage12_exploration/
```

DuckDB files are generated analysis artifacts and should not be committed to Git.

---

# Canonical Output Contract

Small exported TSVs should be written to:

```text
<run_dir>/logs/stage12_exploration/lane_candidate_slices/
```

Generated TSVs are run artifacts and should not be committed to Git.

Tracked files should include only:

```text
scripts/analysis/sql/*.sql
docs/case_studies/<sample_id>/*.md
docs/templates/*.md
```

---

# Git Tracking Policy

## Tracked

The repository should track:

```text
scripts/analysis/sql/stage12_load_prioritized_variant_candidates.sql
scripts/analysis/sql/stage12_exploration.sql
scripts/analysis/sql/stage12_exemplar_bucket_exports.sql
docs/case_studies/<sample_id>/*.md
docs/templates/stage12_exploration_executive_summary_template.md
```

## Not Tracked

The repository should not track:

```text
*.duckdb
*.duckdb.wal
results/
logs/stage12_exploration/*.tsv
logs/stage12_exploration/lane_candidate_slices/*.tsv
```

---

# SQL File Roles

## 1. Load SQL

Purpose:

Load a run-specific Stage 12 TSV into DuckDB as `main.stage12`.

Required behavior:

```sql
DROP TABLE IF EXISTS stage12;

CREATE TABLE stage12 AS
SELECT *
FROM read_csv_auto(
    '<RUN_DIR>/processed/stage_12_validation_candidates.tsv',
    delim='\t',
    header=true,
    all_varchar=true,
    sample_size=-1
);
```

All columns should initially be loaded as text to avoid type inference errors involving chromosomes, missing values, or ontology labels.

---

## 2. Exploration SQL

Purpose:

Support interactive inspection and executive-summary generation.

This file may contain:

* row counts,
* column value counts,
* distinct ontology checks,
* single-axis filters,
* exploratory multi-axis filters.

This file is allowed to be exploratory, but should use:

```sql
FROM main.stage12
```

rather than run-specific catalog names.

---

## 3. Exemplar Bucket Export SQL

Purpose:

Generate standardized case-study seed artifacts for LANE and VAP documentation.

This file should contain only stable, intentionally selected exports.

Each bucket export should use:

```sql
COPY (
    SELECT ...
    FROM main.stage12
    WHERE ...
) TO '<RUN_DIR>/logs/stage12_exploration/lane_candidate_slices/<sample_id>_<bucket_name>.tsv'
WITH (HEADER, DELIMITER '\t');
```

---

# Execution Model

The manual DBeaver workflow is acceptable for the current phase.

Canonical execution sequence:

1. Create or open the run-specific DuckDB database.
2. Load the Stage 12 TSV into `main.stage12`.
3. Run preflight checks.
4. Run exploration SQL as needed.
5. Run exemplar bucket export SQL.
6. Inspect generated TSV files.
7. Summarize findings in Markdown.

Future automation may wrap this workflow in Python using DuckDB, but the SQL logic remains the authoritative analytical layer.

---

# Preflight Requirements

Before running bucket exports, confirm:

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

The observed `sample_id` and `run_id` must match the intended SRA/run.

---

# Safety Guarantees

The original TSV must never be modified.

DuckDB databases are disposable exploration layers derived from the immutable Stage 12 TSV.

Generated TSVs may be deleted and regenerated.

Only SQL logic and documentation should be tracked in Git.

---

# Reuse Across Multiple SRAs

For the 10 WES SRAs, the invariant contract is:

```sql
FROM main.stage12
```

The variable components are:

```text
sample_id
run_dir
duckdb_path
output_dir
output filename prefix
```

The system should avoid manually editing analytical logic between SRAs.

Only paths and sample-specific output prefixes should vary.

---

# Future Automation Direction

If this workflow remains useful across multiple SRAs, promote it to a Python-controlled DuckDB harness.

The Python wrapper should control:

* run manifest,
* TSV input paths,
* DuckDB database paths,
* output directories,
* sample-specific filename prefixes,
* SQL execution order,
* preflight validation,
* export verification.

DuckDB should remain the analytical engine.

Python should provide orchestration and reduce manual path-editing risk.

---

# Design Principle

This workflow separates:

```text
canonical evidence substrate  →  DuckDB exploration layer  →  exported narrative slices
```

The core design goal is to preserve biological interpretability while making Stage 12 exploration reproducible, reviewable, and safe across multiple VAP runs.
