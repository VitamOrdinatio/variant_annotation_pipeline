# VAP Environment Ecosystem

The `environment/` namespace documents the execution environments, dependency infrastructure, storage architecture, and runtime assumptions underlying the Variant Annotation Pipeline (VAP).

VAP was developed and operationally validated across:

* local Linux development systems,
* HPC execution environments,
* large-scale WGS/WES cohort workflows,
* and benchmarking-aware containerized validation infrastructure.

This environment ecosystem therefore captures:

* reproducibility assumptions,
* infrastructure expectations,
* execution topology,
* dependency management,
* storage strategy,
* and containerized benchmarking workflows.

---

# Environment Philosophy

The VAP environment ecosystem intentionally prioritizes:

* reproducible execution,
* infrastructure portability,
* provenance continuity,
* deterministic runtime behavior,
* and operational transparency.

Importantly:

```text
VAP was engineered through real operational execution rather than synthetic toy-only development.
```

The repository therefore preserves explicit documentation regarding:

* development systems,
* execution systems,
* resource assumptions,
* storage organization,
* and benchmarking infrastructure.

---

# Environment Topology

```text
environment/
├── README.md
├── ...
```

The broader repository environment ecosystem additionally includes:

| Namespace                | Purpose                                         |
| ------------------------ | ----------------------------------------------- |
| `requirements.txt`       | Python dependency specification                 |
| `resources/`             | external biological resource acquisition        |
| `tools/`                 | dependency installation workflows               |
| `scripts/environment/`   | environment validation utilities                |
| `scripts/orchestration/` | setup orchestration                             |
| `docs/status/`           | runtime characterization and execution findings |

---

# Primary Development Environment

VAP development was primarily performed within Linux-based Python virtual environments (`.venv`) using:

* Python 3.12
* pytest-based validation
* deterministic TSV-oriented workflows
* and provenance-aware runtime infrastructure.

The development ecosystem intentionally favors:

* lightweight reproducibility,
* explicit dependency control,
* and operational transparency.

Representative development tooling includes:

* Python
* Bash
* bcftools
* samtools
* BWA
* GATK
* VEP
* ANNOVAR
* pytest
* DuckDB
* pandas
* matplotlib

---

# Python Dependency Infrastructure

Primary Python dependencies are defined in:

* `requirements.txt`

The repository intentionally uses:

```text
one repository = one virtual environment
```

to preserve:

* dependency isolation,
* reproducibility,
* and execution stability.

The canonical environment setup pattern is:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

# Representative Execution Hardware

VAP development and execution were intentionally separated across:

- a local Linux development workstation (`sys76`)
- and a dedicated HPC execution node (`MARK`)

This separation preserved lightweight local development while enabling large-scale cohort execution and benchmarking workflows.

---

## sys76 Development Environment

Primary development environment:

| Component | Specification |
|---|---|
| OS | Pop!_OS 24.04 LTS |
| CPU | Intel i7-1165G7 |
| RAM | 64 GB |
| Storage | Dual Samsung NVMe SSDs (~4 TB total) |
| Primary role | development, governance, lightweight testing, figure generation |

The sys76 environment was primarily used for:

- repository engineering
- documentation
- analytical substrate generation
- deterministic figure rendering
- lightweight testing
- and governance workflows

---

## MARK HPC Execution Environment

Primary execution environment:

| Component | Specification |
|---|---|
| OS | Debian GNU/Linux 12 |
| CPU | 40-core HPC node |
| Primary role | cohort-scale execution, HG002 benchmarking, observability workflows |

The MARK environment was used for:

- WGS execution
- heterogeneous WES cohort processing
- benchmarking workflows
- telemetry characterization
- cross-run governance analysis
- and reproducibility validation

---

# Local Development Systems

Local development workflows emphasized:

* iterative testing,
* fixture validation,
* lightweight substrate generation,
* and documentation maturation.

Typical local development responsibilities included:

* analytical substrate generation,
* deterministic figure rendering,
* cross-run aggregation,
* and governance analysis.

---

# MARK HPC Execution Environment

Large-scale operational execution was performed on the MARK execution environment.

The MARK environment supported:

* HG002 WGS execution
* heterogeneous WES cohort execution
* stage-level checkpoint execution
* observability-aware telemetry workflows
* and reproducibility-oriented rerun analysis

Representative execution characteristics included:

* multi-core alignment execution
* large BAM/VCF handling
* long-running orchestration workflows
* and telemetry-aware runtime monitoring

MARK execution workflows were especially important for:

* HG002 benchmarking
* cross-run governance analysis
* and observability maturation.

---

# Storage Philosophy

VAP intentionally separates:

```text
tracked semantic infrastructure
```

from:

```text
large generated genomic artifacts.
```

Large generated artifacts are intentionally excluded from Git, including:

* FASTQ files
* BAM / BAI files
* raw VCF files
* normalized VCF files
* annotated VCF files
* and large TSV substrates

The repository instead tracks:

* contracts
* manifests
* schemas
* summary artifacts
* example excerpts
* analytical substrates
* and reproducibility-oriented evidence surfaces

This storage philosophy preserves:

* repository portability,
* reviewer accessibility,
* and semantic reproducibility

without requiring storage of multi-terabyte execution artifacts.

---

# Runtime Organization

VAP execution generates provenance-aware runtime organization using structured run directories:

```text
results/run_<timestamp>/
```

Representative runtime outputs include:

| Artifact               | Purpose                          |
| ---------------------- | -------------------------------- |
| `run_metadata.json`    | execution metadata               |
| `runtime_profile.tsv`  | runtime telemetry                |
| `run_fingerprint.json` | deterministic execution identity |
| `stage_summaries/`     | stage-level telemetry            |
| `logs/`                | execution logging                |

This runtime organization became foundational infrastructure for:

* observability analysis,
* reproducibility validation,
* and cross-run governance studies.

---

# Benchmarking Environment

HG002 benchmarking workflows required specialized benchmarking infrastructure.

Benchmark validation used:

* `hap.py`
* RTG Tools
* GIAB benchmark resources
* BED-restricted evaluation
* and representation-aware normalization workflows

Because benchmarking dependencies are operationally complex and highly specialized, VAP used:

```text
containerized benchmarking infrastructure
```

for reproducible HG002 validation.

---

# Containerization Strategy

Benchmarking workflows leveraged Apptainer-based container execution for controlled benchmarking reproducibility.

Containerization supported:

* dependency isolation,
* benchmarking reproducibility,
* namespace stability,
* and execution portability

without contaminating the primary VAP runtime environment.

This separation was especially important for:

* `hap.py`
* RTG Tools
* benchmarking normalization utilities
* and representation-aware comparison workflows.

Importantly:

```text
containerization was selectively applied to benchmarking infrastructure rather than forcing full-pipeline containerization.
```

This hybrid strategy preserved:

* pipeline flexibility,
* HPC compatibility,
* and operational transparency.

---

# Observability Infrastructure

The environment ecosystem increasingly incorporated observability-aware execution infrastructure, including:

* stage-level telemetry
* runtime profiling
* provenance-linked metrics
* execution fingerprints
* resource snapshots
* and structured runtime manifests

This infrastructure enabled:

* deterministic rerun analysis,
* runtime characterization,
* and cross-run semantic governance evaluation.

---

# Relationship to Testing

The environment ecosystem directly supports:

* fixture-mode execution,
* runtime validation,
* telemetry validation,
* benchmarking tests,
* and deterministic schema testing.

Environment stability is therefore tightly coupled to:

* reproducibility guarantees,
* operational observability,
* and release readiness.

---

# Relationship to Case Studies

The environment ecosystem enabled the later development of:

| Case Study       | Environment Contribution                      |
| ---------------- | --------------------------------------------- |
| HG002            | benchmarking and HPC execution                |
| ERR10619281      | deterministic rerun validation                |
| ERR10619300      | semantic-governance analytical infrastructure |
| 12-SRA cross-run | telemetry-aware cohort-scale execution        |

The environment ecosystem therefore acts as:

```text
the operational substrate underlying VAP reproducibility claims.
```

---

# Recommended Setup Workflow

Typical setup progression:

1. Create Python virtual environment
2. Install Python dependencies
3. Install biological tooling
4. Acquire reference resources
5. Validate environment
6. Execute lightweight fixture tests
7. Execute cohort-scale workflows

Representative validation commands include:

```bash
pytest tests/
```

and:

```bash
python pipeline_runner.py --config config/example.yaml
```

depending on execution context.

---

# Operational Maturity Themes

The VAP environment ecosystem consistently emphasizes:

* reproducible execution
* infrastructure transparency
* provenance continuity
* observability-aware runtime organization
* benchmarking-aware validation
* and storage-aware operational discipline

Collectively, these environmental decisions enabled VAP to mature into:

```text
reproducible semantic evidence infrastructure
```

rather than an ad hoc genomics workflow collection.

---

# Final Positioning

The VAP environment ecosystem demonstrates that the repository was engineered and validated through:

* real operational execution,
* reproducibility-aware infrastructure design,
* telemetry-aware runtime instrumentation,
* containerized benchmarking validation,
* and provenance-oriented storage organization.

These environmental surfaces therefore form a critical foundation for the broader architectural and scientific maturity of the VAP ecosystem.
