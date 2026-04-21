# scripts/ — Variant Annotation Pipeline (VAP) Setup & Operations

## Overview

The `scripts/` directory contains all operational utilities required to:

* provision the execution environment
* install and validate external tools
* download and validate reference and annotation resources
* prepare input sequencing data
* orchestrate full pipeline setup

This directory is intentionally structured to separate **concerns** and ensure:

* reproducibility across systems (Sys76, Mark HPC, future nodes)
* idempotent setup behavior
* clear ownership of responsibilities per script
* minimal cross-contamination between environment, tools, and data

---

## Directory Structure

```text
scripts/
  environment/     # Python runtime (venv) setup and validation
  tools/           # External executables (bwa, samtools, gatk, vep, annovar)
  resources/       # Reference genomes, benchmarks, annotation datasets
  data_prep/       # Sample-specific preprocessing (e.g., SRA → FASTQ)
  orchestration/   # High-level setup entrypoints
  README.md        # This file
```

---

## Execution Model

### Recommended setup order

Run scripts in the following order when provisioning a new system:

1. `environment/setup_python_env.sh`
2. `tools/setup_pipeline_tools.sh`
3. `resources/setup_grch38_reference_resources.sh`
4. `resources/setup_giab_benchmark_resources.sh`
5. `resources/setup_annotation_resources.sh`

Then validate:

6. `environment/validate_python_env.sh`
7. `tools/validate_pipeline_tools.sh`
8. `resources/validate_resources.sh`

Optional:

* `orchestration/setup_vap.sh` can automate this sequence

---

## Design Principles

### 1. Separation of Concerns

Each subdirectory owns a distinct layer:

| Layer         | Responsibility                |
| ------------- | ----------------------------- |
| environment   | Python virtual environment    |
| tools         | External executables          |
| resources     | Large datasets and references |
| data_prep     | Sample-specific preprocessing |
| orchestration | Workflow coordination         |

Scripts must not cross boundaries.

---

### 2. Idempotency

All setup scripts must be safe to re-run:

* do not overwrite valid existing data
* skip completed steps
* validate before downloading or installing

---

### 3. Validation-First Behavior

Each setup script should:

1. check if requirement is already satisfied
2. validate correctness
3. only perform work if needed

---

### 4. Explicit Failure

Scripts must fail early with clear messages if:

* required tools are missing
* directories are invalid
* expected files are absent or corrupted

No silent fallbacks.

---

### 5. System Portability

Scripts must support multiple environments (e.g., Sys76 vs Mark HPC) via:

* environment variables (e.g., `REF_BASE_DIR`, `GIAB_DIR`)
* config-driven paths (preferred long-term)

Avoid hardcoding system-specific paths.

---

## Subdirectory Contracts

---

### `environment/`

Owns Python runtime setup.

#### Scripts

* `setup_python_env.sh`

  * creates `.venv`
  * installs dependencies from `requirements.txt`

* `validate_python_env.sh`

  * verifies required Python modules (e.g., `yaml`, `pandas`)
  * confirms environment integrity

#### Must NOT:

* install system tools
* download large datasets

---

### `tools/`

Owns external executables.

#### Scripts

* `setup_pipeline_tools.sh`

  * installs or validates tools such as:

    * `bwa`
    * `samtools`
    * `gatk`
    * `vep`
    * ANNOVAR prerequisites

* `validate_pipeline_tools.sh`

  * confirms executables are available on PATH
  * reports versions

#### Must NOT:

* manage `.venv`
* download reference or annotation datasets

---

### `resources/`

Owns all large, reusable datasets.

#### Scripts

* `setup_grch38_reference_resources.sh`

  * downloads GRCh38 FASTA
  * builds indexes (BWA, `.fai`, `.dict`)

* `setup_giab_benchmark_resources.sh`

  * downloads GIAB benchmark VCF, index, BED

* `setup_annotation_resources.sh`

  * provisions:

    * VEP cache
    * ANNOVAR humandb

* `validate_resources.sh`

  * verifies all required resources exist and are valid

#### Must NOT:

* install executables
* manage Python environment

---

### `data_prep/`

Owns sample-specific preprocessing.

#### Scripts

* `prepare_srr_hg002.py`

  * downloads SRA
  * converts to FASTQ
  * performs validation and logging

#### Notes

This layer operates on **data instances**, not global environment or resources.

---

### `orchestration/`

Owns high-level coordination.

#### Scripts

* `setup_vap.sh`

  * optional top-level setup entrypoint
  * calls scripts in correct order
  * should remain thin (no heavy logic)

---

## Logging and Outputs

All scripts should:

* print clear `[INFO]`, `[WARN]`, `[ERROR]` messages
* log critical actions and decisions
* avoid excessive verbosity unless debugging

---

## Future Extensions

Planned improvements:

* unified CLI interface (`--mode status|validate|provision`)
* shared logging utilities across scripts
* integration with pipeline config (`config.yaml`)
* version tracking for tools and resources

---

## Summary

This directory enforces a disciplined setup model:

* **environment → tools → resources → data → orchestration**
* each layer is isolated, testable, and reusable
* scripts are safe, explicit, and portable

Maintaining this structure will prevent configuration drift and simplify scaling to new systems and datasets.
