# ERR10619281 Representative Exemplar Bucket Extraction Plan Using DBeaver

This plan (`err10619281_exemplar_bucket_extraction_plan.md`) is specific for operator exploration of stage12_prioritized variants of ERR10619281 using `DBeaver GUI` access with a `DuckDB database` underneath.

Note:

For the implementation plan that is CLI-driven and thus bypasses `DBeaver GUI`, see:

`stage_12_duckdb_exemplar_export_plan.md`

---

## Purpose

This document defines the locked SQL extraction strategy for generating representative Stage 12 exemplar buckets from:

```sql
stage12_exploration.main.stage12
```

These buckets are intended to support the ERR10619281 WES case study narrative.

They are not diagnostic claims. They are representative semantic evidence-routing exemplars.

---

# DuckDB Export Execution Notes

The SQL examples in this document are intended to be executed against:

```sql
stage12_exploration.main.stage12
```

within a DuckDB database environment accessed through DBeaver.

Representative exemplar exports are generated using:

```sql
COPY (
    SELECT ...
) TO '/path/output.tsv'
WITH (HEADER, DELIMITER '\t');
```

The canonical Stage 12 substrate columns reflect the exported VAP schema and therefore use:

```text
chromosome
position
reference_allele
alternate_allele
```

rather than abbreviated aliases such as:

```text
chrom
pos
ref
alt
```

All SQL examples in this document should preserve compatibility with the actual exported Stage 12 substrate schema.

---

# Locked Bucket Taxonomy

| Bucket ID | Purpose                                                                   | Output Type           | Strategic Role                                 |
| --------- | ------------------------------------------------------------------------- | --------------------- | ---------------------------------------------- |
| Bucket_1A | Validation-routed clinically contextualized epilepsy/mito coding evidence | Row-level TSV         | Flagship exemplars                             |
| Bucket_1B | Clinically contextualized epilepsy/mito coding evidence                   | Row-level TSV         | Supporting clinically relevant exemplars       |
| Bucket_2A | Rare biologically impactful coding evidence triage                        | Aggregate summary TSV | Semantic refinement pressure demonstration     |
| Bucket_2B | Rare-impact variants escalated to Tier 2                                  | Row-level TSV         | Interpretability-aware escalation exemplars    |
| Bucket_2C | Rare-impact variants deprioritized to Tier 3/4                            | Row-level TSV         | Disciplined triage exemplars                   |
| Bucket_3A | ClinVar-supported but deprioritized coding evidence                       | Row-level TSV         | Demonstrates semantic restraint                |
| Bucket_3B | Validation-not-required Tier 3 background evidence                        | Aggregate summary TSV | Background burden context                      |
| Bucket_4A | Representative noncoding semantic exemplars                               | Row-level TSV         | Future-facing noncoding preservation narrative |
| Bucket_5A | Cross-run overlap exemplars                                               | Future                | Not used yet                                   |

---

# Recommended Export Columns

Use these columns for row-level exemplar TSVs when available:

```sql
sample_id,
run_id,
chromosome,
position,
reference_allele,
alternate_allele,
variant_id,
gene_symbol,
gene_id,
variant_class,
consequence,
functional_impact,
clinical_significance,
clinical_status,
is_clinically_supported,
frequency_status,
gnomad_af,
epilepsy_flag,
mito_flag,
priority_tier,
priority_rank,
priority_reason,
validation_required,
validation_priority,
suggested_validation_method,
interpretability_status,
coding_interpretation_label,
qc_status
```

If one or more columns do not exist, omit only the missing column rather than changing the bucket logic.

---

# Bucket_1A — Validation-Routed Clinically Contextualized Epilepsy/Mito Coding Evidence

## Purpose

Flagship Stage 12 exemplars.

These rows show coding variants that are:

* clinically supported,
* epilepsy- or mitochondrial-flagged,
* and routed for validation.

## SQL

```sql
SELECT
    sample_id,
    run_id,
    chromosome,
    position,
    reference_allele,
    alternate_allele,
    variant_id,
    gene_symbol,
    gene_id,
    variant_class,
    consequence,
    functional_impact,
    clinical_significance,
    clinical_status,
    is_clinically_supported,
    frequency_status,
    gnomad_af,
    epilepsy_flag,
    mito_flag,
    priority_tier,
    priority_rank,
    priority_reason,
    validation_required,
    validation_priority,
    suggested_validation_method,
    interpretability_status,
    coding_interpretation_label,
    qc_status
FROM stage12_exploration.main.stage12
WHERE variant_class = 'coding'
AND is_clinically_supported = 'True'
AND (epilepsy_flag = 'True' OR mito_flag = 'True')
AND validation_required = 'True'
ORDER BY
    priority_rank ASC,
    validation_priority ASC,
    gene_symbol ASC;
```

## Expected Count

Previously observed:

```text
N = 2
```

## Export Filename

```text
err10619281_bucket_1a_validation_routed_epilepsy_mito.tsv
```

---

# Bucket_1B — Clinically Contextualized Epilepsy/Mito Coding Evidence

## Purpose

Supporting clinically contextualized coding evidence.

This includes all clinically supported coding variants intersecting epilepsy or mitochondrial flags, regardless of validation-routing status.

## SQL

```sql
SELECT
    sample_id,
    run_id,
    chromosome,
    position,
    reference_allele,
    alternate_allele,
    variant_id,
    gene_symbol,
    gene_id,
    variant_class,
    consequence,
    functional_impact,
    clinical_significance,
    clinical_status,
    is_clinically_supported,
    frequency_status,
    gnomad_af,
    epilepsy_flag,
    mito_flag,
    priority_tier,
    priority_rank,
    priority_reason,
    validation_required,
    validation_priority,
    suggested_validation_method,
    interpretability_status,
    coding_interpretation_label,
    qc_status
FROM stage12_exploration.main.stage12
WHERE variant_class = 'coding'
AND is_clinically_supported = 'True'
AND (epilepsy_flag = 'True' OR mito_flag = 'True')
ORDER BY
    validation_required DESC,
    priority_rank ASC,
    gene_symbol ASC;
```

## Expected Count

Previously observed:

```text
N = 7
```

## Export Filename

```text
err10619281_bucket_1b_clinically_contextualized_epilepsy_mito.tsv
```

---

# Bucket_2A — Rare Biologically Impactful Coding Evidence Triage

## Purpose

Aggregate summary table.

This bucket characterizes how rare biologically impactful coding evidence is distributed across:

* functional impact class,
* priority tier,
* and validation-routing state.

This is not a row-level exemplar bucket.

## SQL

```sql
SELECT
    functional_impact,
    priority_tier,
    validation_required,
    COUNT(*) AS n
FROM stage12_exploration.main.stage12
WHERE variant_class = 'coding'
AND frequency_status = 'rare'
AND functional_impact IN ('missense', 'loss_of_function', 'splice_relevant')
GROUP BY
    functional_impact,
    priority_tier,
    validation_required
ORDER BY
    n DESC,
    functional_impact ASC,
    priority_tier ASC,
    validation_required DESC;
```

## Expected Count

Previously observed:

```text
987 total rare-impact coding variants
8 grouped rows
```

## Export Filename

```text
err10619281_bucket_2a_rare_impact_coding_triage_summary.tsv
```

---

# Bucket_2B — Rare-Impact Variants Escalated to Tier 2

## Purpose

Representative examples of rare biologically impactful coding evidence that VAP escalated into moderate-priority review substrate.

## SQL

```sql
SELECT
    sample_id,
    run_id,
    chromosome,
    position,
    reference_allele,
    alternate_allele,
    variant_id,
    gene_symbol,
    gene_id,
    variant_class,
    consequence,
    functional_impact,
    clinical_significance,
    clinical_status,
    is_clinically_supported,
    frequency_status,
    gnomad_af,
    epilepsy_flag,
    mito_flag,
    priority_tier,
    priority_rank,
    priority_reason,
    validation_required,
    validation_priority,
    suggested_validation_method,
    interpretability_status,
    coding_interpretation_label,
    qc_status
FROM stage12_exploration.main.stage12
WHERE variant_class = 'coding'
AND frequency_status = 'rare'
AND functional_impact IN ('missense', 'loss_of_function', 'splice_relevant')
AND priority_tier LIKE 'tier_2%'
ORDER BY
    is_clinically_supported DESC,
    epilepsy_flag DESC,
    mito_flag DESC,
    functional_impact ASC,
    gene_symbol ASC
LIMIT 15;
```

## Export Filename

```text
err10619281_bucket_2b_rare_impact_tier2.tsv
```

---

# Bucket_2C — Rare-Impact Variants Deprioritized

## Purpose

Representative examples of rare biologically impactful coding evidence that was not escalated, demonstrating disciplined semantic triage.

## SQL

```sql
SELECT
    sample_id,
    run_id,
    chromosome,
    position,
    reference_allele,
    alternate_allele,
    variant_id,
    gene_symbol,
    gene_id,
    variant_class,
    consequence,
    functional_impact,
    clinical_significance,
    clinical_status,
    is_clinically_supported,
    frequency_status,
    gnomad_af,
    epilepsy_flag,
    mito_flag,
    priority_tier,
    priority_rank,
    priority_reason,
    validation_required,
    validation_priority,
    suggested_validation_method,
    interpretability_status,
    coding_interpretation_label,
    qc_status
FROM stage12_exploration.main.stage12
WHERE variant_class = 'coding'
AND frequency_status = 'rare'
AND functional_impact IN ('missense', 'loss_of_function', 'splice_relevant')
AND priority_tier NOT LIKE 'tier_2%'
ORDER BY
    is_clinically_supported DESC,
    epilepsy_flag DESC,
    mito_flag DESC,
    functional_impact ASC,
    gene_symbol ASC
LIMIT 15;
```

## Export Filename

```text
err10619281_bucket_2c_rare_impact_deprioritized.tsv
```

---

# Bucket_3A — ClinVar-Supported but Deprioritized Coding Evidence

## Purpose

Shows that clinical support alone does not automatically trigger escalation.

This is the disciplined semantic restraint bucket.

## SQL

```sql
SELECT
    sample_id,
    run_id,
    chromosome,
    position,
    reference_allele,
    alternate_allele,
    variant_id,
    gene_symbol,
    gene_id,
    variant_class,
    consequence,
    functional_impact,
    clinical_significance,
    clinical_status,
    is_clinically_supported,
    frequency_status,
    gnomad_af,
    epilepsy_flag,
    mito_flag,
    priority_tier,
    priority_rank,
    priority_reason,
    validation_required,
    validation_priority,
    suggested_validation_method,
    interpretability_status,
    coding_interpretation_label,
    qc_status
FROM stage12_exploration.main.stage12
WHERE variant_class = 'coding'
AND validation_required = 'False'
AND priority_tier LIKE 'tier_3%'
AND is_clinically_supported = 'True'
ORDER BY
    epilepsy_flag DESC,
    mito_flag DESC,
    frequency_status ASC,
    gene_symbol ASC
LIMIT 15;
```

## Export Filename

```text
err10619281_bucket_3a_clinvar_supported_deprioritized.tsv
```

---

# Bucket_3B — Validation-Not-Required Tier 3 Background Evidence

## Purpose

Aggregate burden context.

This bucket demonstrates the size and composition of validation-not-required Tier 3 coding evidence.

## SQL

```sql
SELECT
    functional_impact,
    frequency_status,
    is_clinically_supported,
    COUNT(*) AS n
FROM stage12_exploration.main.stage12
WHERE variant_class = 'coding'
AND validation_required = 'False'
AND priority_tier LIKE 'tier_3%'
GROUP BY
    functional_impact,
    frequency_status,
    is_clinically_supported
ORDER BY
    n DESC,
    functional_impact ASC,
    frequency_status ASC,
    is_clinically_supported DESC;
```

## Expected Count

Previously observed parent population:

```text
N = 26,236
```

## Export Filename

```text
err10619281_bucket_3b_tier3_background_summary.tsv
```

---

# Bucket_4A — Representative Noncoding Semantic Exemplars

## Purpose

Optional but recommended.

This bucket supports the future-facing noncoding preservation narrative.

It should show noncoding semantic preservation without implying clinical causality.

## SQL

```sql
SELECT
    sample_id,
    run_id,
    chromosome,
    position,
    reference_allele,
    alternate_allele,
    variant_id,
    gene_symbol,
    gene_id,
    variant_class,
    consequence,
    functional_impact,
    clinical_significance,
    clinical_status,
    is_clinically_supported,
    frequency_status,
    gnomad_af,
    epilepsy_flag,
    mito_flag,
    priority_tier,
    priority_rank,
    priority_reason,
    validation_required,
    validation_priority,
    suggested_validation_method,
    interpretability_status,
    qc_status
FROM stage12_exploration.main.stage12
WHERE variant_class = 'noncoding'
AND frequency_status = 'rare'
AND (
    epilepsy_flag = 'True'
    OR mito_flag = 'True'
    OR is_clinically_supported = 'True'
)
ORDER BY
    is_clinically_supported DESC,
    epilepsy_flag DESC,
    mito_flag DESC,
    priority_rank ASC,
    gene_symbol ASC
LIMIT 15;
```

## Export Filename

```text
err10619281_bucket_4a_representative_noncoding_semantic_exemplars.tsv
```

---

# Bucket_5A — Cross-Run Overlap Exemplars

## Status

Future bucket.

Do not export yet.

This bucket should be designed only after ERR10619300 and ERR10619281 exemplar tables are both stabilized.

---

# Final Locked Export Set

Output directory:

```text
/mnt/storage/vap_runs/results/run_2026_05_27_233524/logs/stage12_exploration/lane_candidate_slices/
```

For the immediate ERR10619281 case study, export these files:

```text
err10619281_bucket_1a_validation_routed_epilepsy_mito.tsv
err10619281_bucket_1b_clinically_contextualized_epilepsy_mito.tsv
err10619281_bucket_2a_rare_impact_coding_triage_summary.tsv
err10619281_bucket_2b_rare_impact_tier2.tsv
err10619281_bucket_2c_rare_impact_deprioritized.tsv
err10619281_bucket_3a_clinvar_supported_deprioritized.tsv
err10619281_bucket_3b_tier3_background_summary.tsv
err10619281_bucket_4a_representative_noncoding_semantic_exemplars.tsv
```

Minimum required set:

```text
err10619281_bucket_1a_validation_routed_epilepsy_mito.tsv
err10619281_bucket_1b_clinically_contextualized_epilepsy_mito.tsv
err10619281_bucket_2a_rare_impact_coding_triage_summary.tsv
err10619281_bucket_2b_rare_impact_tier2.tsv
err10619281_bucket_2c_rare_impact_deprioritized.tsv
err10619281_bucket_3a_clinvar_supported_deprioritized.tsv
```

Bucket_4A is optional but strategically valuable.
