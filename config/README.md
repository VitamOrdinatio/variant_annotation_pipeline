# VAP Configuration System

This directory contains canonical execution configurations, reusable templates, and historical configuration artifacts for the Variant Annotation Pipeline (VAP).

The configuration ecosystem evolved alongside VAP itself. Earlier configurations emphasized standalone execution and exploratory development, while modern configurations support:

- deterministic run-local outputs
- sidecar metric emission
- provenance-aware figure orchestration
- runtime-generated reporting configs
- post-VEP fixture execution
- optional auto-rendering of figures
- MARK/HPC execution

---

# Example Configurations

| file | purpose |
|---|---|
| config.mark.err10619300.sidecar_metrics.yaml | canonical full-pipeline execution |
| config.mark.err10619300.post_vep_sidecar_metrics.yaml | rapid downstream fixture testing |
| config/templates/config.example.post_vep.yaml | generalized post-VEP example |

---

# Execution Modes

| execution_mode | purpose |
|---|---|
| full_pipeline | complete FASTQ → annotation → reporting workflow |
| post_vep_fixture | downstream testing using precomputed annotated substrates |

---

# Required Input Keys Per Execution Mode

## `full_pipeline`

Required:

```yaml
input:
  sample_id: ERR10619300
  sra_accession: ERR10619300
  fastq:
    r1: /data/storage/fastq/ERR10619300_1.fastq.gz
    r2: /data/storage/fastq/ERR10619300_2.fastq.gz
```

Typical additional requirements:

```yaml
reference:
vep:
resources:
```

---

## `post_vep_fixture`

Required:

```yaml
input:
  sample_id: ERR10619300
  annotated_tsv: results/run_2026_05_22_071545/processed/ERR10619300_run_2026_05_22_071545.annotated_variants.tsv
```

Typical optional fixture inputs:

```yaml
input:
  vcf: results/run_2026_05_22_071545/processed/ERR10619300_run_2026_05_22_071545.annotated_variants.vcf
```

This mode assumes upstream annotation products already exist.

---

# Optional Toggles

| toggle | meaning |
|---|---|
| auto_render | invoke reporting subsystem automatically |
| strict | fail pipeline if figure rendering fails |

---

# Directory Structure

```text
config/
├── README.md
├── archive/
├── templates/
├── config.mark.err10619300.sidecar_metrics.yaml
└── config.mark.err10619300.post_vep_sidecar_metrics.yaml
```

---

# Configuration Philosophy

VAP now follows a layered configuration model:

```text
Canonical pipeline config
        ↓
Runtime-resolved figure-set config
        ↓
Figure-specific rendering configs
        ↓
Rendered figures + manifests
```

The top-level canonical pipeline YAML is the authoritative operator entrypoint.

All downstream figure orchestration is derived from runtime information emitted during pipeline execution, including:

- sample_id
- run_id
- run_dir
- output_dir

This architecture ensures:

- deterministic provenance
- run-local figure generation
- reduced operator error
- stable cross-run reproducibility

---

# Configuration Resolution Strategy

VAP uses runtime-derived configuration resolution rather than static YAML inheritance.

The canonical pipeline configuration acts as the authoritative source of runtime identity:

- sample_id
- run_id
- run_dir

Downstream reporting configurations are generated dynamically during execution.

This prevents:
- duplicated runtime identifiers
- unresolved placeholder leakage
- cross-run reporting collisions

---

# Active Canonical Configurations

## `config.mark.err10619300.sidecar_metrics.yaml`

Primary full-pipeline execution configuration for the ERR10619300 case study on MARK.

Characteristics:

- execution_mode: `full_pipeline`
- emits sidecar metrics
- enables optional figure auto-rendering
- generates run-local reporting artifacts
- intended for end-to-end production execution

---

## `config.mark.err10619300.post_vep_sidecar_metrics.yaml`

Fixture-mode execution configuration for rapid downstream testing.

Characteristics:

- execution_mode: `post_vep_fixture`
- bypasses upstream alignment and variant-calling stages
- useful for:
  - reporting-layer smoketesting
  - figure orchestration validation
  - renderer debugging
  - rapid substrate testing

This mode assumes pre-existing annotated variant substrates are available.

---

# Template Configurations

Template YAMLs are located in:

```text
config/templates/
```

These files are intended to become generalized operator-facing starting points after architecture stabilization.

Current placeholders:

- `config.mark.template.full_pipeline.yaml`
- `config.mark.template.post_vep_fixture.yaml`

These templates will eventually replace ERR-specific operator bootstrapping workflows.

---

# Archive Configurations

Historical and superseded configurations are retained in:

```text
config/archive/
```

These files preserve:

- execution lineage
- architectural evolution
- reproducibility context
- historical development state

Archive configs are not considered canonical execution entrypoints.

---

# Figure Orchestration

Modern VAP runs support optional automatic figure rendering.

Canonical configs may include:

```yaml
figures:
  auto_render: true
  strict: false
  figure_set_template: scripts/configs/figure_sets/vap_single_run_figures.yaml
```

---

# Expected Artifact Dependencies

Some reporting workflows assume existence of:

- Stage05 telemetry
- annotated variant TSVs
- collapsed substrate TSVs
- runtime sidecar metrics
- figure substrate emissions

`post_vep_fixture` runs may not populate all provenance artifacts expected by certain figures.

---

# Figure Rendering Semantics

## `auto_render`

Controls whether the reporting subsystem is invoked automatically at pipeline completion.

```yaml
auto_render: true
```

Behavior:

- generates resolved figure configs
- launches figure orchestration
- writes manifests and figures into run-local directories

---

## `strict`

Controls renderer failure policy.

```yaml
strict: false
```

Behavior:

| strict value | behavior |
|---|---|
| false | figure failures log warnings but pipeline succeeds |
| true | figure failures terminate pipeline execution |

Recommended default:

```yaml
strict: false
```

This preserves separation between:

- biologically critical pipeline stages
- optional reporting/visualization infrastructure

---

# Runtime-Resolved Figure Configurations

Figure orchestration now uses runtime-generated configuration files.

During execution, VAP emits:

```text
results/run_<id>/metadata/figure_set_resolved.yaml
```

This file is generated dynamically from:

```text
scripts/configs/figure_sets/vap_single_run_figures.yaml
```

using runtime values such as:

- sample_id
- run_id
- run_dir

This prevents unresolved placeholder leakage and ensures deterministic figure localization.

---

# Run-Local Reporting Structure

Rendered figures are emitted into:

```text
results/run_<id>/figures/
```

Typical outputs include:

```text
figures/
├── *.png
├── *.pdf
├── figure_manifest.tsv
└── resolved_configs/
```

The reporting subsystem intentionally remains run-local.

Promotion of figures into:

```text
docs/case_studies/
```

is currently a manual curation step.

---

# Fixture vs Full-Pipeline Semantics

## `full_pipeline`

Runs the complete VAP workflow:

- FASTQ ingestion
- alignment
- variant calling
- annotation
- prioritization
- telemetry
- figure generation

This mode provides complete provenance lineage.

---

## `post_vep_fixture`

Starts downstream of annotation using precomputed substrates.

Useful for:

- rapid testing
- renderer debugging
- telemetry validation
- orchestration development

Important:

Some figures may require provenance artifacts unavailable in fixture mode.

---

# Common Pitfalls

## Missing substrate artifacts

Some figure-generation stages assume full-pipeline provenance.

Post-VEP fixture mode may not populate all telemetry substrates expected by certain renderers.

---

## Unresolved placeholders

All runtime paths should resolve before renderer invocation.

Correct:

```text
results/run_2026_05_27_163302/figures/
```

Incorrect:

```text
{run_dir}/figures/
```

---

## Renderer dependencies

Some figure-generation workflows require:

- matplotlib
- plotly
- kaleido
- Chrome/Chromium availability

Particularly for PDF/image export on HPC systems.

---

# Operational Guidance

Recommended development workflow:

1. Validate new reporting logic using `post_vep_fixture`
2. Confirm renderer stability
3. Run full-pipeline validation on MARK
4. Review figures manually
5. Promote selected figures into case-study documentation

---

# Future Directions

Planned future improvements include:

- generalized template configs
- figure-config migration into canonical `config/`
- expanded multi-SRA orchestration
- cohort-scale reporting
- automated case-study assembly
- enhanced manifest provenance
- figure-level fault isolation

---