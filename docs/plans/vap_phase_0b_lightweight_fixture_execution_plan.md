# VAP Phase 0b Implementation Plan
## Lightweight Deterministic Fixture Execution Framework

## Purpose

Implement a lightweight deterministic execution mode for VAP that enables:

- rapid local execution on sys76
- observability validation without HG002-scale runtime
- deterministic regression testing
- future CI/CD integration
- fast iteration during infrastructure refactors
- reproducible demonstration runs

This phase builds directly upon the Phase 0a observability/provenance foundation.

---

## Strategic Context

Current VAP validation depends heavily on:

- full HG002 execution
- MARK-scale hardware
- long runtime cycles (~36 hours)
- large genomic inputs
- expensive orchestration loops

This creates development friction.

VAP currently lacks a true lightweight execution pathway capable of validating:

- logger lifecycle
- metadata emission
- runtime profiling
- stage summaries
- stage orchestration
- artifact contracts
- execution determinism

without requiring large-scale compute.

Phase 0b addresses this gap.

---

## Primary Goal

Enable deterministic local execution via:

```bash
python run_pipeline.py --config config/config.example.annotation_only.yaml
```

Target runtime:

- preferred: < 2 minutes
- acceptable: < 5 minutes

on sys76-class hardware.

---

## Core Design Philosophy

The lightweight fixture framework must:

- execute real VAP stage code
- produce real VAP artifacts
- preserve deterministic behavior
- preserve stage orchestration semantics
- preserve provenance generation

The fixture framework must NOT:

- mock stage execution
- manually fabricate outputs
- bypass orchestration logic
- introduce a separate “fake pipeline”

This distinction is critical.

The lightweight execution path must remain a true VAP execution.

---

## Execution Model

### Initial Implementation Target

```text
execution_mode: annotation_only
```

This mode already exists conceptually within VAP architecture.

The lightweight fixture framework should leverage:

- existing execution_mode
- existing input_vcf
- existing should_run_stage()
- existing stage orchestration
- existing observability infrastructure

rather than introducing parallel execution logic.

---

## Expected Stage Behavior


### Skipped Stages

The following stages should be skipped automatically:

```text
stage_02_align_data
stage_03_process_bam
stage_04_qc_aligned_reads
stage_05_call_variants
```

These are already modeled in:

```python
should_run_stage()
```

This architectural foundation should remain authoritative.

---

## Fixture Dataset Design

### Initial Fixture Artifact

`data/example/example_variants.vcf`

Characteristics:

- tiny
- deterministic
- biologically interpretable
- repository-safe size
- fast VEP annotation

Preferred variant count:

```text
5–20 variants
```

---

## Recommended Variant Composition

The fixture VCF should ideally include:

- synonymous variant
- missense variant
- intronic variant
- regulatory/intergenic variant
- ClinVar-associated variant if feasible
- mitochondrial-related gene if feasible
- epilepsy-associated gene if feasible

The fixture should support meaningful downstream Stage 08–13 behavior.

---

## Configuration Design

### New Config

`config/config.example.annotation_only.yaml`

Expected characteristics:

```yaml
mode:
  execution_mode: annotation_only

input:
  vcf:
    input_vcf: data/example/example_variants.vcf
```

The config should:

- minimize runtime
- minimize external dependencies
- preserve deterministic execution
- preserve provenance behavior


---

## Expected Artifact Emission

The lightweight fixture execution must still emit:

```text
results/<run_id>/
├── logs/
├── metadata/
│   ├── config_snapshot.yaml
│   ├── run_fingerprint.json
│   ├── run_metadata.json
│   ├── runtime_profile.tsv
│   └── stage_summaries/
├── processed/
├── reports/
└── final/
```

This requirement is non-negotiable.

The lightweight fixture is intended to validate real pipeline behavior.

---

## Runtime Determinism Requirements

Repeated fixture execution should produce:

- stable stage ordering
- stable runtime profile schema
- stable metadata schema
- stable JSON serialization
- stable artifact naming
- stable provenance structure

Minor timestamp differences are acceptable.

Structural drift is not acceptable.

---

## Future CI/CD Integration

The lightweight fixture framework is intended to become the future basis for:

- GitHub Actions
- CI regression tests
- pre-merge validation
- rapid smoke tests
- contributor onboarding
- reproducibility demonstrations

The fixture framework should therefore remain:

- lightweight
- deterministic
- portable
- minimally dependent on large resources

---

## Implementation Tasks

### Task 1 — Create fixture data directory

Create:

- `data/example/`

Add:

- `example_variants.vcf`
- `README.md`

---

### Task 2 — Create lightweight config

Create:

`config/config.example.annotation_only.yaml`

---

### Task 3 — Validate annotation_only execution path

Verify:

- stage skipping behavior
- input_vcf handling
- Stage 07+ execution
- metadata generation
- runtime profile generation
- stage summary generation

---

### Task 4 — Add fixture execution test

Add:

`tests/test_annotation_only_fixture_execution.py`

This test should validate:

- successful execution
- expected skipped stages
- expected emitted artifacts
- deterministic metadata structure

---

### Task 5 — Add fixture execution documentation

Document:

- execution command
- expected runtime
- expected outputs
- intended usage
- CI implications

Potential locations:

- `docs/examples/`
- `README.md`

---

## Relationship to MARK HG002 Artifacts

Large HG002 outputs downloaded from MARK are reference/golden artifacts, not lightweight execution inputs. Small curated slices derived from them may be used for schema regression tests, but Phase 0b must remain runnable without multi-GB files.

Phase 0b may initially require VEP resources if Stage 07 is executed on sys76.  If sys76 lacks local VEP/cache readiness, the first implementation may need either:

```text
annotation_only-with-VEP on MARK only
```

or:

```text
local post-VEP fixture beginning at Stage 08
```

### Decision Point

```text
Option A: true annotation_only through Stage 07 using VEP.
Option B: post-annotation fixture beginning at Stage 08 using a tiny pre-annotated TSV/VCF.
```

Recommendation is Option B due to sys76's limited compute environment.


---

## Acceptance Criteria

Phase 0b is complete when:

- lightweight fixture executes locally on sys76
- runtime remains < 5 minutes
- real VAP stages execute
- annotation_only behavior is validated
- provenance artifacts emit correctly
- pytest suite passes
- fixture outputs remain deterministic
- no HG002-scale resources are required

---

## Non-Goals

Phase 0b will NOT:

- optimize MARK runtime yet
- replace HG002 validation
- reduce biological rigor of full VAP runs
- introduce orchestration frameworks
- redesign stage contracts
- eliminate full-scale benchmarking

HG002 remains the authoritative biological validation run.

The lightweight fixture exists to accelerate infrastructure development and validation.

---

## Strategic Outcome

Phase 0b transforms VAP from:

```text
a large genomic pipeline requiring expensive execution
```

into:

```text
a reproducible genomic execution framework
capable of rapid deterministic local validation
```

This is a foundational capability for long-term maintainability, reproducibility, scaling, and professional-grade software engineering.

---