# Scripts  
## variant_annotation_pipeline v1.0  
## scripts/README.md

---

## Purpose

The `scripts/` directory contains helper shell scripts that support
environment preparation, reference setup, and external dataset acquisition
for `variant_annotation_pipeline`.

These scripts are **operational helpers**, not pipeline stages.

They exist to prepare the external resources required by the pipeline, while the actual stage-based execution is handled by:

- `run_pipeline.py`
- `src/pipeline_runner.py`
- `pipeline/stage_*.py`

---

## Design Principle

```text
The pipeline code should remain focused on reproducible stage execution.
Operational setup tasks live in scripts/.
```

This separation keeps the repository clean and makes it easier to distinguish:

- environment preparation
- data acquisition
- reference setup
- actual pipeline execution

---

## Current Scripts

### `download_and_prepare_srr.sh`

Purpose:
- download the locked Repo 2 v1 FASTQ dataset
- prepare HG002 input reads for pipeline execution

Dataset target:
- BioProject: `PRJNA200694`
- Sample: `HG002`
- SRA: `SRR12898354`

Expected outputs:
- external FASTQ files under machine-local storage, for example:
  - `/mnt/storage/fastq/SRR12898354_1.fastq.gz`
  - `/mnt/storage/fastq/SRR12898354_2.fastq.gz`

Notes:
- this script is part of input-data preparation
- it is not called automatically by the pipeline

---

### `download_giab_hg002_benchmark.sh`

Purpose:
- download GIAB benchmark resources for HG002 on GRCh38

Expected resources:
- benchmark VCF
- benchmark VCF index
- benchmark BED file

Example target paths:
- `/mnt/storage/reference/giab/HG002_GRCh38_1_22_v4.2.1_benchmark.vcf.gz`
- `/mnt/storage/reference/giab/HG002_GRCh38_1_22_v4.2.1_benchmark.vcf.gz.tbi`
- `/mnt/storage/reference/giab/HG002_GRCh38_1_22_v4.2.1_benchmark.bed`

Notes:
- these resources are used by Stage 12 validation logic
- benchmark comparison in v1 is summary-oriented, not a full concordance engine

---

### `install_repo2_tools.sh`

Purpose:
- verify and install external command-line dependencies required by Repo 2

Tool targets:
- `wget`
- `samtools`
- `bwa`
- `gatk`
- supporting runtime dependencies such as Java, where needed

Behavior:
- checks whether required tools are already available in `PATH`
- installs missing packages where appropriate
- installs GATK in a user-controlled location
- updates shell `PATH` setup when needed

Notes:
- this script prepares the execution environment
- it should be run before attempting full pipeline execution if tools are missing

---

### `setup_grch38_reference.sh`

Purpose:
- download and prepare the GRCh38 primary assembly reference genome
- create the indexes required by Repo 2

Expected outputs:
- FASTA
- FASTA index (`.fai`)
- sequence dictionary (`.dict`)
- BWA index files

Expected directory model:
- `/mnt/storage/reference/grch38/`
- `/mnt/storage/reference/grch38/bwa/`

Notes:
- this script prepares the reference bundle expected by:
  - Stage 02 alignment
  - Stage 05 variant calling
  - Stage 06 normalization

---

## Relationship to Config

These scripts prepare resources that are later referenced in:

```text
config/config.yaml
```

Important rule:

```text
Scripts prepare resources.
Config declares where those resources live.
Pipeline stages consume the config-defined paths.
```

Paths must not be hardcoded in pipeline code.

---

## What Scripts Are Not

These scripts are **not**:

- replacements for pipeline stages
- workflow engines
- distributed job launchers
- cohort-level orchestration tools

They are support utilities for v1 setup and preparation.

---

## Recommended Usage Order

For a fresh machine or fresh Repo 2 setup, the general order is:

1. install tools
2. prepare GRCh38 reference
3. download GIAB benchmark resources
4. download and prepare HG002 FASTQ
5. run pipeline

Conceptually:

```text
install_repo2_tools.sh
→ setup_grch38_reference.sh
→ download_giab_hg002_benchmark.sh
→ download_and_prepare_srr.sh
→ python run_pipeline.py --config config/config.yaml
```

---

## Operational Philosophy

These scripts are intentionally kept in `scripts/` rather than folded into stage logic because they perform tasks that are:

- machine-specific
- one-time or occasional
- environment-dependent
- not part of the deterministic per-run transformation of sample state

This supports cleaner reproducibility and easier debugging.

---

## Future Extensions

Later versions of this directory may include:

- manifest preparation helpers
- batch-download utilities
- checksum verification helpers
- environment audit scripts
- aggregation support scripts

These are not required for v1.0.

---

## Summary Rule

```text
scripts/ prepares the world around the pipeline.
pipeline/ executes the pipeline itself.
```

---

# End of Scripts README