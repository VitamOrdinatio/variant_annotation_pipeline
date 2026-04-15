# Aggregation Schema  
## variant_annotation_pipeline v1.0  
## docs/implementation/aggregation_schema.md

---

## 1. Purpose

This document defines the **future aggregation contract** for
`variant_annotation_pipeline`.

Aggregation is **not implemented in v1.0**, but the per-sample outputs and run metadata produced in v1 must be structured so that later versions can support:

- multi-sample reunification
- comparative analysis
- cohort-level summaries
- centralized result consolidation across machines

This document is therefore a **forward-compatibility schema**, not an executable v1 feature.

---

## 2. Governing Principle

Aggregation must operate on:

```text
completed per-sample run outputs
```

and not on raw assumptions about how or where those runs were executed.

The aggregation layer must be able to consume independent sample runs produced on:

- the same machine
- different machines
- different times
- different subsets of a manifest

without ambiguity.

---

## 3. Aggregation Scope

### v1.0
Not implemented.

### Future versions
Aggregation may support:

- multiple GIAB samples
- cohort-level disease/control comparisons
- gene-level burden summaries
- cross-sample prioritization analysis
- centralized summary reporting

---

## 4. Core Aggregation Unit

The atomic unit of aggregation is:

```text
one completed sample run
```

Each sample run must expose enough information to be safely merged later.

That means aggregation acts on **run records**, not raw FASTQ files.

---

## 5. Minimum Required Inputs for Aggregation

A future aggregation workflow should expect each per-sample run to provide, at minimum:

```python
aggregation_input = {
    "run_id": str,
    "sample_id": str,
    "sample_alias": str | None,
    "bioproject_accession": str,
    "sra_accession": str | None,
    "reference_genome": str,
    "pipeline_name": str,
    "pipeline_version": str,
    "machine_id": str,
    "status": str,
    "prioritized_table": str | None,
    "annotated_table": str | None,
    "gene_summary_table": str | None,
    "run_summary_report": str | None,
    "metadata_path": str,
}
```

---

## 6. Run Eligibility Rules

A run is eligible for aggregation only if:

- `status == completed`
- required output paths exist
- metadata file is readable
- reference genome is known
- sample identifier is stable and non-null

Runs with:

- `failed`
- `partial`
- missing required outputs

must be excluded or separately logged.

---

## 7. Stable Join Keys

Aggregation depends on stable identifiers.

### Required join keys

- `sample_id`
- `run_id`
- `reference_genome`

### Preferred provenance fields

- `bioproject_accession`
- `sra_accession`
- `pipeline_version`

These keys are required to avoid ambiguous merges.

---

## 8. Aggregation Layers

Future aggregation should conceptually occur in three layers.

---

### Layer A — Run Registry

This layer builds a machine-readable table of available runs.

Example schema:

| column | description |
|---|---|
| run_id | unique pipeline run identifier |
| sample_id | stable sample identifier |
| sample_alias | alternate biological label |
| bioproject_accession | project accession |
| sra_accession | SRA run accession |
| reference_genome | reference assembly |
| pipeline_version | pipeline version used |
| machine_id | machine that produced run |
| status | completed / failed / partial |
| metadata_path | path to metadata.json |
| prioritized_table | path to prioritized variants |
| gene_summary_table | path to gene summary |

This layer is the entry point for all later merging.

---

### Layer B — Variant-Level Aggregation

This layer merges per-sample prioritized or annotated tables.

Potential outputs:

- combined prioritized variants table
- combined annotated variants table
- cross-sample variant recurrence table

Example schema:

| column | description |
|---|---|
| sample_id | source sample |
| gene_symbol | assigned gene |
| chromosome | chromosome |
| position | genomic coordinate |
| reference_allele | REF |
| alternate_allele | ALT |
| consequence | functional consequence |
| clinvar_classification | ClinVar label |
| mito_flag | mitochondrial gene-set flag |
| epilepsy_flag | epilepsy gene-set flag |
| priority_label | final priority class |
| run_id | source run |

---

### Layer C — Gene-Level Aggregation

This layer summarizes variants at the gene level across samples.

Potential outputs:

- gene burden summary
- gene recurrence summary
- per-gene prioritized counts
- cohort-level gene-set overlap summaries

Example schema:

| column | description |
|---|---|
| gene_symbol | gene |
| sample_count | number of samples with retained variants |
| prioritized_variant_count | total prioritized variants |
| mito_flag | whether gene is in MitoCarta |
| epilepsy_flag | whether gene is in epilepsy gene sets |

---

## 9. Required Aggregation Outputs

Future aggregation should be able to produce:

- `aggregated_run_registry.tsv`
- `aggregated_prioritized_variants.tsv`
- `aggregated_gene_summary.tsv`
- `aggregation_report.md`

These filenames are recommendations, not v1 requirements.

---

## 10. Provenance Requirements

Aggregation must preserve provenance for every row.

That means every merged variant-level or gene-level record must be traceable back to:

- sample
- run
- pipeline version
- reference genome

### Required provenance columns

- `sample_id`
- `run_id`
- `pipeline_version`
- `reference_genome`

---

## 11. Reference Consistency Rules

Aggregation must not merge runs across incompatible references without explicit normalization.

### Required rule

Runs must be grouped by:

- `reference_genome`

Examples:
- `GRCh38` runs may be merged together
- `GRCh37` runs must not be silently merged with `GRCh38`

---

## 12. Failure Handling

Aggregation logic must be able to classify runs into:

- usable
- unusable
- incomplete
- incompatible

Example incompatibilities:

- different reference genome
- missing prioritized table
- unreadable metadata
- duplicate run IDs

These should be recorded in an aggregation log or exclusion report.

---

## 13. Aggregation and Storage Philosophy

Aggregation must not require retention of raw FASTQ files.

It should depend on:

- finalized per-sample outputs
- metadata
- stable identifiers
- reproducible file naming

This is necessary to support later cleanup or archival of very large raw files.

---

## 14. Interaction with State Schema

The aggregation layer consumes fields emitted by the per-sample runtime state, especially:

- `state["run"]`
- `state["sample"]`
- `state["artifacts"]`
- `state["reports"]`
- `state["stage_outputs"]`

Aggregation must therefore assume that v1 run outputs are structured according to:

```text
docs/implementation/state_schema.md
```

---

## 15. Non-Goals for v1.0

This document does **not** require implementation of:

- manifest execution
- multi-sample orchestration
- cross-machine job dispatch
- centralized databases
- distributed locking
- automatic retries across nodes

It only defines the schema boundary that future versions should honor.

---

## 16. Future-Compatible Design Rules

To keep future aggregation possible, v1 implementations should ensure:

1. every run has a stable `run_id`
2. every sample has a stable `sample_id`
3. prioritized outputs are machine-readable TSV files
4. metadata is preserved per run
5. output paths are deterministic within the run directory structure

---

## 17. Suggested Future Implementation Files

When aggregation is implemented in later versions, likely code locations include:

```text
src/aggregation/
scripts/aggregation/
pipeline/stage_14_aggregate_runs.py
```

These are suggestions only.

---

## 18. Summary Rule

```text
v1 produces self-contained sample runs.
future aggregation merges those runs without depending on raw sequencing files.
```

---

# End of Aggregation Schema