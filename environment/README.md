# Environment Setup  
## variant_annotation_pipeline v1.0  
## environment/README.md

---

## 1. Purpose

This document describes the execution environment expected by  
`variant_annotation_pipeline` v1.0.

The pipeline is designed as a **real single-sample genomics workflow** for the locked HG002 dataset and therefore expects:

- Linux or WSL-style execution
- Python-based orchestration
- external bioinformatics tools available on the system
- external data and reference paths provided through `config/config.yaml`

This document describes:

- software expectations
- environment setup
- external tool assumptions
- storage and path philosophy

---

## 2. Governing Principle

```text
The repository contains code and documentation.
Large sequencing inputs, reference genomes, annotation caches, and benchmark resources live outside the repo and are injected through config.yaml.
```

This keeps the repo:

- lightweight
- portable
- versionable
- compatible with external storage mounts

---

## 3. Supported Platform Model

Recommended environment:

- Linux workstation
- Pop!_OS / Ubuntu-like distribution
- or WSL on Windows with mounted external storage

Expected shell:

- bash-compatible shell

Expected Python:

- Python 3.9+

---

## 4. Python Environment

A per-repo virtual environment is recommended.

### Create virtual environment

```bash
python -m venv .venv
```

### Activate virtual environment

```bash
source .venv/bin/activate
```

### Install Python dependencies

```bash
pip install -r requirements.txt
```

---

## 5. External Tool Requirements

Repo 2 v1.0 expects the following tools to be installed outside Python:

- `bwa`
- `samtools`
- `gatk`
- `vep`

Optional / downstream manual review:

- `igv`

These tools are referenced by executable name in `config/config.yaml`.

### Important rule

Tool paths must be configurable through YAML and must not be hardcoded in pipeline code.

---

## 6. External Data Path Model

Repo 2 v1.0 is designed for external storage paths, not repo-local FASTQ storage.

Example development-machine layout:

```text
/mnt/storage/sra/SRR12898354/SRR12898354.sra
/mnt/storage/fastq/SRR12898354_1.fastq.gz
/mnt/storage/fastq/SRR12898354_2.fastq.gz
```

These paths are configured in:

```text
config/config.yaml
```

The pipeline validates them during Stage 01.

---

## 7. Reference Resource Requirements

The following reference resources are expected to exist outside the repo and be referenced via config:

- reference FASTA
- FASTA index (`.fai`)
- BWA index prefix
- sequence dictionary
- GIAB benchmark VCF (optional but recommended for validation)
- VEP cache directory
- gene-set TSV files

### Example categories

```text
/mnt/storage/references/
/mnt/storage/giab/
/mnt/storage/vep/
/mnt/storage/gene_sets/
```

These are examples only; actual paths are config-driven.

---

## 8. Locked Dataset for v1.0

Repo 2 v1.0 is locked to:

- BioProject: `PRJNA200694`
- Sample: `HG002`
- Alias: `NA24385`
- SRA: `SRR12898354`
- Reference genome: `GRCh38`

This lock is enforced through configuration validation and Stage 01 metadata checks.

---

## 9. Execution Model

Pipeline entry point:

```bash
python run_pipeline.py --config config/config.yaml
```

This performs:

- config loading
- config validation
- run directory creation
- stage-based execution
- metadata emission

---

## 10. Storage Philosophy

### Inside the repo

Tracked:

- source code
- documentation
- tests
- config
- lightweight text assets

### Outside the repo

Untracked / external:

- FASTQ
- BAM
- VCF
- reference genomes
- VEP cache
- benchmark resources

### Runtime outputs

Produced inside the repo under:

```text
results/<run_id>/
```

---

## 11. Reproducibility Expectations

Each run should preserve:

- run identifier
- config snapshot
- tool versions
- logs
- structured output files
- metadata.json

This supports:

- deterministic reruns
- traceability
- later aggregation in future versions

---

## 12. Tool Version Capture

Where feasible, the pipeline should record tool versions for:

- `bwa`
- `samtools`
- `gatk`
- `vep`

Version capture is part of reproducibility, even if exact version enforcement is not pinned in v1.

---

## 13. Path Safety Rules

Pipeline code must:

- read paths from config
- validate existence before execution
- avoid hardcoded machine-specific absolute paths
- treat external storage as authoritative input location

The only place machine-specific paths should appear is:

```text
config/config.yaml
```

---

## 14. What v1 Does Not Require

v1.0 does **not** require:

- containerization
- conda
- Snakemake / Nextflow
- SLURM integration
- distributed execution
- cloud execution

These may be added in future versions.

---

## 15. Troubleshooting Checklist

If the pipeline fails early:

1. confirm `.venv` is activated
2. confirm `requirements.txt` is installed
3. confirm external FASTQ paths exist
4. confirm reference paths exist
5. confirm tool executables are available in `PATH`
6. inspect:
   ```text
   results/<run_id>/logs/pipeline.log
   ```

---

## 16. Summary Rule

```text
Repo 2 v1.0 is a config-driven pipeline that runs inside the repo but operates on external sequencing and reference resources.
```

---

# End of Environment Setup