# hg002_benchmarking_implementation_plan.md

## Purpose

This document defines the implementation plan for the HG002 benchmarking component within the Variant Annotation Pipeline (VAP) ecosystem.

The implementation target is a modular, MARK-bound benchmarking script that compares a completed VAP HG002 normalized VCF against GIAB HG002 truth resources using an Apptainer-mediated `hap.py` runtime.

This plan implements the behavioral requirements defined in:

```text
docs/contracts/system/hg002_benchmarking_component_contract.md
```

---

# Primary Implementation Goal

Implement a standalone HG002 benchmarking component that:

1. Runs outside the canonical VAP 13-stage pipeline.
2. Executes on MARK where required resources already reside.
3. Benchmarks a completed HG002 VAP run without rerunning the full pipeline.
4. Compares the VAP normalized VCF against GIAB HG002 truth resources.
5. Restricts comparison to GIAB high-confidence BED regions.
6. Emits structured benchmark outputs under:

```text
results/<run_id>/benchmarking/
```

---

# Non-Goals

This implementation SHALL NOT:

* modify `pipeline_runner.py`,
* add `stage_14_hg002_benchmarking` yet,
* benchmark semantic interpretation outputs,
* benchmark RDGP-ready exports,
* benchmark VDB-ready exports,
* make clinical or diagnostic claims,
* optimize variant-calling parameters,
* or pursue leaderboard-style benchmark performance.

---

# Initial Placement

The initial component SHALL live under:

```text
scripts/benchmarking/
```

Recommended script name:

```text
scripts/benchmarking/run_hg002_happy_benchmark.py
```

A shell wrapper MAY be added later if useful, but the initial implementation SHOULD be Python-first to support:

* argument validation,
* path resolution,
* structured output parsing,
* JSON/TSV generation,
* and explicit error handling.

---

# Execution Environment

The script SHALL initially be MARK-bound.

## Containerized Benchmark Runtime

The HG002 benchmarking component SHALL use an Apptainer-mediated
container runtime for `hap.py` execution.

The benchmarking runtime SHALL initially use a frozen `.sif`
container image derived from:

```text
quay.io/biocontainers/hap.py:0.3.15--py27hcb73b3d_0
```

The containerized runtime exists to:

- isolate historical benchmarking dependencies,
- avoid host dependency drift,
- preserve reproducibility,
- and prevent contamination of the canonical VAP Python environment.

The benchmarking component SHALL NOT require native installation
of `hap.py` into the VAP `.venv`.


Expected execution location:

```text
MARK VAP repository root
```

Expected invocation pattern:

```bash
python scripts/benchmarking/run_hg002_happy_benchmark.py \
  --run-dir results/<run_id> \
  --truth-vcf /data/storage/reference/<path>/HG002_GRCh38_1_22_v4.2.1_benchmark.vcf.gz \
  --truth-bed /data/storage/reference/<path>/HG002_GRCh38_1_22_v4.2.1_benchmark.bed \
  --reference-fasta /data/storage/reference/grch38/GRCh38.primary_assembly.genome.fa
```

The exact truth-resource directory may be finalized during MARK preflight inspection.

---

# Required Inputs

## VAP Query VCF

The script SHALL benchmark the VAP normalized query VCF:

```text
results/<run_id>/interim/*.normalized_variants.vcf
```

The script MAY auto-discover the normalized VCF unless explicitly supplied.

The script SHALL NOT benchmark:

* raw VCFs,
* annotated VCFs,
* annotated TSVs,
* stage 08 exports,
* stage 11 prioritized variants,
* stage 12 validation candidates,
* or semantic interpretation outputs.

---

## GIAB Truth VCF

The script SHALL require:

```text
HG002_GRCh38_1_22_v4.2.1_benchmark.vcf.gz
```

---

## GIAB Confident Regions BED

The script SHALL require:

```text
HG002_GRCh38_1_22_v4.2.1_benchmark.bed
```

Benchmarking SHALL explicitly restrict evaluation to this BED.

---

## Reference FASTA

The script SHALL require:

```text
GRCh38.primary_assembly.genome.fa
```

The reference FASTA SHALL match the VAP operating reference build.

---

## Benchmark Runtime Container

The script SHALL require:

```text
apptainer
```

available on MARK.

The script SHALL additionally require access to a valid
`hap.py` Apptainer `.sif` runtime image.

Initial expected runtime image:

`/data/storage/containers/hap.py_0.3.15--py27hcb73b3d_0.sif`

The script SHALL fail fast if:

- apptainer is unavailable,
- the `.sif` runtime image is unavailable,
- or the containerized `hap.py` runtime cannot execute.

---

# Preflight Validation

Before benchmark execution, the script SHALL validate:

* run directory exists,
* `interim/` exists,
* exactly one normalized VCF candidate exists unless explicitly provided,
* query VCF reference build is compatible with supplied GIAB truth resources,
* query VCF, truth resources, BED resources, and reference FASTA are contig-namespace compatible,
* truth VCF exists,
* truth BED exists,
* reference FASTA exists,
* `apptainer` resolves from the execution environment,
* the configured `hap.py` `.sif` runtime image exists,
* the containerized `hap.py` runtime executes successfully,
* the configured `.sif` runtime image produces a valid `hap.py --version` response,
* output directory can be created,
* and the command to be executed is fully logged.

If multiple normalized VCFs are detected, the script SHALL fail unless the user supplies an explicit `--query-vcf`.

---

# Output Directory

The script SHALL create:

```text
results/<run_id>/benchmarking/
```

Required contents:

```text
benchmarking.log
happy/
hg002_benchmark_summary.tsv
hg002_benchmark_summary.json
hg002_snp_indel_metrics.tsv
hg002_false_positives.tsv
hg002_false_negatives.tsv
```

The `happy/` subdirectory SHALL contain raw `hap.py` outputs.

---

# hap.py Execution Strategy

The script SHALL invoke `hap.py`
through an Apptainer container runtime using:

```bash
apptainer exec <hap.py_container>.sif hap.py ...
```

rather than through a native host installation.

Benchmark execution SHALL use:

* GIAB truth VCF as truth,
* VAP normalized VCF as query,
* GIAB confident BED as confident-region restriction,
* GRCh38 FASTA as reference,
* and `results/<run_id>/benchmarking/happy/` as output location.

The implementation SHOULD preserve the exact command in:

```text
benchmarking.log
```

and optionally in:

```text
benchmark_command.txt
```

---

# Structured Output Strategy

After `hap.py` completes, the script SHALL parse available `hap.py` outputs into VAP-friendly summaries.

Required summary outputs:

## hg002_benchmark_summary.tsv

Single-row or compact table containing:

* run_id,
* query_vcf,
* truth_vcf,
* truth_bed,
* reference_fasta,
* precision,
* recall,
* F1,
* TP,
* FP,
* FN,
* SNP precision,
* SNP recall,
* indel precision,
* indel recall,
* generated_at.

## hg002_benchmark_summary.json

Machine-readable equivalent of the core summary.

## hg002_snp_indel_metrics.tsv

Variant-type-stratified output containing at minimum:

* SNP metrics,
* indel metrics,
* TP,
* FP,
* FN,
* precision,
* recall,
* F1.

## hg002_false_positives.tsv

Inspection-oriented table derived from hap.py FP outputs when available.

## hg002_false_negatives.tsv

Inspection-oriented table derived from hap.py FN outputs when available.

If FP/FN conversion is not available in the first implementation pass, the script SHALL still:

* preserve raw hap.py outputs,
* create placeholder TSVs with explanatory status,
* and document the limitation in `benchmarking.log`.

---

# Failure Semantics

The script SHALL fail fast for:

* missing query VCF,
* ambiguous query VCF discovery,
* missing truth VCF,
* missing truth BED,
* missing reference FASTA,
* missing `apptainer`,
* missing `.sif` runtime image,
* containerized `hap.py` runtime execution failure,
* `hap.py` nonzero exit status,
* malformed expected hap.py summary outputs,
* unresolved contig namespace incompatibility,
* or inability to create the benchmarking output directory.

The script SHALL NOT silently emit successful benchmark summaries if benchmarking failed.

---

# Logging Requirements

The script SHALL emit:

```text
results/<run_id>/benchmarking/benchmarking.log
```

The log SHALL include:

* timestamp,
* run directory,
* query VCF path,
* truth VCF path,
* truth BED path,
* reference FASTA path,
* apptainer executable path,
* Apptainer runtime version,
* `.sif` runtime image path,
* full hap.py command,
* execution start time,
* execution end time,
* exit status,
* and generated output paths.

---

# Contig Namespace Interoperability

Namespace mediation SHALL preserve deterministic coordinate identity.

The HG002 benchmarking component SHALL explicitly validate
contig namespace compatibility across:

* normalized query VCF,
* GIAB truth VCF,
* GIAB BED resources,
* and reference FASTA.

The component SHALL recognize that:
* GRCh38 compatibility alone is insufficient,
* and benchmarking resources may differ between:
  * UCSC-style contigs (`chr1`)
  * and Ensembl-style contigs (`1`).

The component SHALL fail fast when namespace incompatibility
is detected.

The implementation MAY later support:
* deterministic namespace harmonization overlays,
* derived immutable interoperability resources,
* or explicit namespace mediation strategies.

Canonical VAP resources SHALL NOT be silently mutated
during namespace mediation.

---

# Determinism Expectations

Repeated execution with identical inputs SHALL produce stable summary metrics.

The script SHOULD avoid nondeterministic output naming except where timestamps are explicitly useful for logs.

Canonical summary filenames SHALL remain stable.

---

# Test Strategy

Initial tests SHOULD cover:

## Unit Tests

* normalized VCF discovery,
* failure on zero normalized VCFs,
* failure on multiple normalized VCFs without explicit query path,
* output directory creation,
* command construction,
* missing resource failure behavior,
* parsing of representative hap.py summary outputs.

## Integration / MARK Smoke Test

On MARK, run against a completed HG002 VAP run.

Expected validation target:

```text
results/<HG002_run_id>/
```

Expected outputs:

```text
results/<HG002_run_id>/benchmarking/
```

---

# MARK Validation Workflow

1. Develop script on sys76.
2. Add unit tests where practical.
3. Commit and push.
4. Pull on MARK.
5. Confirm `apptainer` availability.
6. Confirm `.sif` runtime image availability.
7. Confirm GIAB resource paths.
8. Confirm contig namespace compatibility across:
   * query VCF,
   * truth VCF,
   * truth BED,
   * and reference FASTA.
9. Run script against completed HG002 VAP run.
10. Inspect `benchmarking.log`.
11. Inspect structured TSV/JSON outputs.
12. Upload MARK output summaries for review.
13. Harden parser/output logic as needed.

---

# Future Promotion Path

Future benchmarking backends MAY extend beyond hap.py if scientifically justified.

After workflow stabilization, this component MAY be promoted into:

```text
stage_14_hg002_benchmarking
```

Promotion criteria SHOULD include:

* stable Apptainer-mediated `hap.py` execution,
* stable structured outputs,
* tested failure modes,
* confirmed MARK reproducibility,
* and clear user-facing documentation.

Until then, benchmarking SHALL remain a modular script-first component.

---

# Documentation Follow-Ups

After successful MARK validation, create or update:

```text
docs/status/hg002_benchmarking_validation_status.md
```

This status document SHOULD record:

* run_id,
* benchmark resources,
* execution command,
* output files,
* known limitations,
* and interpretation constraints.

---

# Acceptance Criteria

The implementation is acceptable when:

1. The script runs against a completed HG002 VAP run on MARK.
2. The script uses the VAP normalized VCF, not semantic outputs.
3. The script restricts evaluation to GIAB confident BED regions.
4. The script invokes `hap.py` with GRCh38-consistent and contig-namespace-compatible resources.
5. The script emits structured outputs under `results/<run_id>/benchmarking/`.
6. The script fails fast under missing or ambiguous resource conditions.
7. The implementation does not modify the canonical 13-stage VAP pipeline.
8. The generated summaries support benchmark-aware engineering validation without clinical or diagnostic overclaiming.

---

# Runtime Reproducibility Principle

The HG002 benchmarking component SHALL prefer:
- immutable containerized benchmarking runtimes,
- pinned benchmarking toolchains,
- and isolated scientific execution environments

over mutable host-level dependency installation.

This architecture exists to strengthen:
- reproducibility,
- benchmarking longevity,
- dependency stability,
- and scientific infrastructure portability.

---

# Final Principle

The HG002 benchmarking component exists to validate:

```text
upstream variant substrate integrity
```

not downstream biological interpretation.

This distinction SHALL remain central throughout implementation, testing, documentation, and case-study integration.
