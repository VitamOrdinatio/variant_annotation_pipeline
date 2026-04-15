# State Schema  
## variant_annotation_pipeline v1.0  
## docs/implementation/state_schema.md

---

## 1. Purpose

This document defines the runtime `state` object used by
`variant_annotation_pipeline` v1.0.

The `state` object is the central execution record passed between pipeline stages.

Its purpose is to ensure:

- explicit data flow
- stage-to-stage reproducibility
- clear artifact tracking
- structured QC capture
- deterministic reporting
- future extensibility toward batch and distributed execution

This schema is implementation-facing and owned by SWE.

---

## 2. Governing Principle

The runtime model follows this rule:

```text
One sample = one self-contained analysis state
```

For v1.0, the pipeline processes a single locked sample:

- BioProject: `PRJNA200694`
- Sample: `HG002`
- Alias: `NA24385`
- SRA: `SRR12898354`
- Reference: `GRCh38`

The state must therefore be sufficient to reconstruct:

- what sample was processed
- which inputs were used
- which stages completed
- which artifacts were produced
- whether the run succeeded or failed

---

## 3. Top-Level State Structure

The runtime `state` object is a nested Python dictionary with the following top-level structure:

```python
state = {
    "run": {},
    "sample": {},
    "inputs": {},
    "artifacts": {},
    "annotations": {},
    "gene_sets": {},
    "qc": {},
    "stage_outputs": {},
    "warnings": [],
    "errors": [],
    "reports": {},
}
```

Each section is defined below.

---

## 4. `run`

Stores run-level metadata.

```python
state["run"] = {
    "run_id": str,
    "status": str,
    "execution_mode": str,
    "pipeline_name": str,
    "pipeline_version": str,
    "config_path": str,
    "config_snapshot_path": str,
    "start_time": str,
    "end_time": str | None,
    "machine_id": str,
}
```

### Field definitions

- `run_id`  
  Unique run identifier

- `status`  
  One of:
  - `initialized`
  - `running`
  - `completed`
  - `failed`
  - `partial`

- `execution_mode`  
  For v1, expected:
  - `full_pipeline`

  Future-compatible:
  - `annotation_only`

- `pipeline_name`  
  Expected value:
  - `variant_annotation_pipeline`

- `pipeline_version`  
  Example:
  - `v1.0`

- `config_path`  
  Path to active config file

- `config_snapshot_path`  
  Saved run-specific config snapshot

- `start_time` / `end_time`  
  ISO-like timestamp strings

- `machine_id`  
  Hostname or machine identifier

---

## 5. `sample`

Stores locked dataset and biological sample metadata.

```python
state["sample"] = {
    "sample_id": str,
    "sample_alias": str,
    "bioproject_accession": str,
    "sra_accession": str,
    "reference_genome": str,
    "assay_type": str,
}
```

### Expected v1 values

- `sample_id` → `HG002`
- `sample_alias` → `NA24385`
- `bioproject_accession` → `PRJNA200694`
- `sra_accession` → `SRR12898354`
- `reference_genome` → `GRCh38`
- `assay_type` → `WGS`

---

## 6. `inputs`

Stores user-supplied or config-resolved primary input paths.

```python
state["inputs"] = {
    "fastq_1": str | None,
    "fastq_2": str | None,
    "input_vcf": str | None,
}
```

### v1 expectations

For `full_pipeline`:

- `fastq_1` required
- `fastq_2` required
- `input_vcf` should be `None`

For future `annotation_only` support:

- `input_vcf` required
- `fastq_1` and `fastq_2` may be `None`

---

## 7. `artifacts`

Stores paths to pipeline-produced files.

```python
state["artifacts"] = {
    "aligned_bam": str | None,
    "aligned_bam_index": str | None,
    "sorted_bam": str | None,
    "sorted_bam_index": str | None,
    "aligned_qc_report": str | None,
    "raw_vcf": str | None,
    "normalized_vcf": str | None,
    "annotated_vcf": str | None,
    "annotated_table": str | None,
    "filtered_table": str | None,
    "coding_table": str | None,
    "noncoding_table": str | None,
    "interpreted_coding_table": str | None,
    "interpreted_noncoding_table": str | None,
    "prioritized_table": str | None,
    "validation_notes": str | None,
    "igv_review_candidates": str | None,
    "gene_summary_table": str | None,
    "run_summary_report": str | None,
}
```

### Design rule

Large files are never stored in-memory in `state`.  
Only their resolved paths are stored.

---

## 8. `annotations`

Stores annotation provenance and annotation-layer metadata.

```python
state["annotations"] = {
    "annotation_engine": str | None,
    "annotation_completed": bool,
    "resources_used": list[str],
    "clinvar_enabled": bool,
    "population_frequency_sources": list[str],
}
```

### Expected v1 values

- `annotation_engine` → `VEP`
- `annotation_completed` → `True` after Stage 07
- `resources_used` may include:
  - `VEP`
  - `ClinVar`
  - `gnomAD`
  - `ExAC`
  - `1000Genomes`

---

## 9. `gene_sets`

Stores gene-set overlay metadata and source paths.

```python
state["gene_sets"] = {
    "mitocarta_path": str | None,
    "genes4epilepsy_path": str | None,
    "overlay_completed": bool,
    "flags_added": list[str],
}
```

### Expected v1 flags

- `mito_flag`
- `epilepsy_flag`

### Notes

The exact number of input gene-set files may vary, but the v1 repo brief requires:

- MitoCarta
- Genes4Epilepsy

---

## 10. `qc`

Stores structured QC summaries produced by stages.

```python
state["qc"] = {
    "input_qc": {},
    "alignment_qc": {},
    "bam_processing_qc": {},
    "variant_calling_qc": {},
    "normalization_qc": {},
    "annotation_qc": {},
    "filtering_qc": {},
    "interpretation_qc": {},
    "validation_qc": {},
}
```

### Example substructures

#### `input_qc`

```python
state["qc"]["input_qc"] = {
    "input_validation_passed": bool,
    "files_checked": list[dict],
    "file_count": int,
}
```

#### `alignment_qc`

```python
state["qc"]["alignment_qc"] = {
    "alignment_completed": bool,
    "read_count_r1": int | None,
    "read_count_r2": int | None,
    "aligned_bam_exists": bool,
}
```

#### `bam_processing_qc`

```python
state["qc"]["bam_processing_qc"] = {
    "bam_processing_completed": bool,
    "sorted_bam_exists": bool,
    "bam_index_exists": bool,
}
```

#### `variant_calling_qc`

```python
state["qc"]["variant_calling_qc"] = {
    "variant_calling_completed": bool,
    "variant_count": int | None,
    "raw_vcf_exists": bool,
}
```

#### `normalization_qc`

```python
state["qc"]["normalization_qc"] = {
    "normalization_completed": bool,
    "normalized_variant_count": int | None,
    "malformed_records_skipped": int | None,
}
```

#### `annotation_qc`

```python
state["qc"]["annotation_qc"] = {
    "annotation_completed": bool,
    "annotated_variant_count": int | None,
    "required_fields_present": bool,
}
```

#### `filtering_qc`

```python
state["qc"]["filtering_qc"] = {
    "filtering_completed": bool,
    "filtered_count": int | None,
    "coding_count": int | None,
    "noncoding_count": int | None,
}
```

#### `interpretation_qc`

```python
state["qc"]["interpretation_qc"] = {
    "coding_interpretation_completed": bool,
    "noncoding_interpretation_completed": bool,
    "prioritization_completed": bool,
    "prioritized_variant_count": int | None,
}
```

#### `validation_qc`

```python
state["qc"]["validation_qc"] = {
    "validation_completed": bool,
    "manual_igv_review_required": bool,
    "candidate_count": int | None,
    "benchmark_comparison_completed": bool,
}
```

---

## 11. `stage_outputs`

Stores per-stage machine-readable completion records.

```python
state["stage_outputs"] = {
    "stage_01_load_data": {},
    "stage_02_align_data": {},
    "stage_03_process_bam": {},
    "stage_04_qc_aligned_reads": {},
    "stage_05_call_variants": {},
    "stage_06_normalize_vcf": {},
    "stage_07_annotate_variants": {},
    "stage_08_filter_and_partition": {},
    "stage_09_interpret_coding": {},
    "stage_10_interpret_noncoding": {},
    "stage_11_prioritize_variants": {},
    "stage_12_validate_variants": {},
    "stage_13_write_summary": {},
}
```

Each stage should write at least:

```python
{
    "status": "success" | "failed" | "skipped",
}
```

### Example richer record

```python
state["stage_outputs"]["stage_05_call_variants"] = {
    "status": "success",
    "raw_vcf": "results/<run_id>/interim/raw_variants.vcf.gz",
    "variant_count": 12345,
    "tool": "GATK HaplotypeCaller",
}
```

---

## 12. `warnings`

Stores non-fatal execution issues.

```python
state["warnings"] = [
    str,
    ...
]
```

Examples:

- low variant count warning
- missing optional annotation source
- no non-coding variants retained after filtering

---

## 13. `errors`

Stores fatal or run-limiting errors.

```python
state["errors"] = [
    str,
    ...
]
```

Examples:

- missing FASTQ input
- alignment failed
- VCF generation failed
- annotation output missing

---

## 14. `reports`

Stores terminal report paths and related report metadata.

```python
state["reports"] = {
    "run_summary_report": str | None,
    "summary_table": str | None,
    "gene_summary_table": str | None,
    "report_line_count": int | None,
}
```

---

## 15. Stage Read / Write Contract Summary

### Stage 01 — Load Data
Reads:
- config only

Writes:
- `sample`
- `inputs`
- `qc["input_qc"]`
- `stage_outputs["stage_01_load_data"]`

---

### Stage 02 — Align Data
Reads:
- `inputs["fastq_1"]`
- `inputs["fastq_2"]`

Writes:
- `artifacts["aligned_bam"]`
- `qc["alignment_qc"]`
- `stage_outputs["stage_02_align_data"]`

---

### Stage 03 — Process BAM
Reads:
- `artifacts["aligned_bam"]`

Writes:
- `artifacts["sorted_bam"]`
- `artifacts["sorted_bam_index"]`
- `qc["bam_processing_qc"]`
- `stage_outputs["stage_03_process_bam"]`

---

### Stage 04 — QC Aligned Reads
Reads:
- `artifacts["sorted_bam"]`
- `artifacts["sorted_bam_index"]`

Writes:
- `artifacts["aligned_qc_report"]`
- `qc["alignment_qc"]`
- `stage_outputs["stage_04_qc_aligned_reads"]`

---

### Stage 05 — Call Variants
Reads:
- `artifacts["sorted_bam"]`
- `artifacts["sorted_bam_index"]`

Writes:
- `artifacts["raw_vcf"]`
- `qc["variant_calling_qc"]`
- `stage_outputs["stage_05_call_variants"]`

---

### Stage 06 — Normalize VCF
Reads:
- `artifacts["raw_vcf"]` or `inputs["input_vcf"]`

Writes:
- `artifacts["normalized_vcf"]`
- `qc["normalization_qc"]`
- `stage_outputs["stage_06_normalize_vcf"]`

---

### Stage 07 — Annotate Variants
Reads:
- `artifacts["normalized_vcf"]`
- gene-set source files from config

Writes:
- `artifacts["annotated_vcf"]`
- `artifacts["annotated_table"]`
- `annotations`
- `gene_sets`
- `qc["annotation_qc"]`
- `stage_outputs["stage_07_annotate_variants"]`

---

### Stage 08 — Filter and Partition
Reads:
- `artifacts["annotated_table"]`

Writes:
- `artifacts["filtered_table"]`
- `artifacts["coding_table"]`
- `artifacts["noncoding_table"]`
- `qc["filtering_qc"]`
- `stage_outputs["stage_08_filter_and_partition"]`

---

### Stage 09 — Interpret Coding
Reads:
- `artifacts["coding_table"]`

Writes:
- `artifacts["interpreted_coding_table"]`
- `qc["interpretation_qc"]`
- `stage_outputs["stage_09_interpret_coding"]`

---

### Stage 10 — Interpret Non-Coding
Reads:
- `artifacts["noncoding_table"]`

Writes:
- `artifacts["interpreted_noncoding_table"]`
- `qc["interpretation_qc"]`
- `stage_outputs["stage_10_interpret_noncoding"]`

---

### Stage 11 — Prioritize Variants
Reads:
- `artifacts["interpreted_coding_table"]`
- `artifacts["interpreted_noncoding_table"]`

Writes:
- `artifacts["prioritized_table"]`
- `artifacts["gene_summary_table"]`
- `qc["interpretation_qc"]`
- `stage_outputs["stage_11_prioritize_variants"]`

---

### Stage 12 — Validate Variants
Reads:
- `artifacts["prioritized_table"]`
- BAM / VCF-derived upstream artifacts

Writes:
- `artifacts["validation_notes"]`
- `artifacts["igv_review_candidates"]`
- `qc["validation_qc"]`
- `stage_outputs["stage_12_validate_variants"]`

---

### Stage 13 — Write Summary
Reads:
- all prior stage summaries
- artifact registry
- warnings / errors

Writes:
- `reports`
- `artifacts["run_summary_report"]`
- `stage_outputs["stage_13_write_summary"]`

---

## 16. Serialization Rules

The `state` object must be serializable to JSON-compatible structures.

Allowed:
- strings
- integers
- floats
- booleans
- lists
- dictionaries
- `None`

Avoid storing:
- large in-memory DataFrames
- binary file contents
- non-serializable tool handles
- open file handles

Store file paths instead.

---

## 17. Determinism Rules

To support reproducibility:

- identical input files + identical config should produce functionally identical outputs
- all thresholds and modes must come from config
- all stage outputs must be recorded in `state`
- stage failure must leave a machine-readable trace in `state`

---

## 18. Forward-Compatibility Notes

This v1 schema is intentionally designed to support future extension into:

- batch execution
- distributed execution
- aggregation across runs
- richer annotation layers
- benchmark comparison modules

Those future features must extend this schema without breaking the single-sample invariant.

---

# End of State Schema