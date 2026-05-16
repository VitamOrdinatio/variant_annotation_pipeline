# VAP v1 Case-Study Tables

## Intended Audience

This directory is primarily intended for:
- computational genomics reviewers
- translational bioinformatics hiring committees
- clinical genomics engineering stakeholders
- reproducibility-oriented pipeline reviewers
- downstream ecosystem developers

---

## Purpose 

This directory contains deterministic, metadata-aware evidence tables harvested from completed VAP production runs.

These artifacts are intended to support:
- case-study documentation
- reproducibility analysis
- telemetry inspection
- provenance review
- biological consequence summarization
- downstream GSC contextualization
- future VDB persistence planning
- future RDGP prioritization workflows

The tables in this directory are intentionally:
- non-clinical
- deterministic
- provenance-aware
- stable across reruns
- lightweight and figure-ready

VAP should be interpreted as a:

```text
provenance-aware genomic evidence refinement framework
```

rather than as a diagnostic system.

These tables do not claim:

- pathogenicity
- diagnosis
- causal inference
- clinical interpretation

Instead, they demonstrate how VAP transforms raw NGS-derived variant evidence into structured, reviewable, biologically contextualized candidate evidence substrate.

---

# Table Inventory

## `stage_funnel_summary.tsv`

### Purpose

Summarizes how VAP progressively refines large raw variant collections into increasingly structured candidate evidence sets.

### Highlights

Tracks:

- raw variant counts
- annotation-stage counts
- coding/noncoding partitioning
- prioritization tiers
- reviewability candidate generation

### Why It Matters

Demonstrates:

- evidence refinement
- candidate funneling
- deterministic stage progression
- explainable reduction of NGS search space

This table is central to the VAP v1 claim that VAP produces reproducible biological evidence structures rather than merely executing variant calling.

---

## `runtime_stage_summary.tsv`

### Purpose

Summarizes runtime telemetry across VAP pipeline stages.

### Highlights

Tracks:

- per-stage runtime
- execution bottlenecks
- alignment cost
- variant-calling cost
- telemetry maturation across runs

### Why It Matters

Demonstrates:

- operational observability
- runtime decomposition
- reproducible telemetry
- HPC-aware genomics engineering

This table helps communicate that VAP supports operational introspection suitable for production-scale genomics workflows.

---

## `priority_tier_summary.tsv`

### Purpose

Summarizes VAP prioritization tier distributions across runs.

### Highlights

Tracks:

- tier 1 through tier 4 evidence structures
- candidate prioritization distributions
- reviewability substrate composition

### Why It Matters

Demonstrates:

- deterministic prioritization logic
- stable candidate refinement
- evidence organization reproducibility

This table helps illustrate how VAP structures downstream candidate-review workflows.

---

## `candidate_reviewability_readiness.tsv`

### Purpose

Summarizes downstream candidate reviewability and inspection readiness.

### Highlights

Tracks:

- IGV-suggested review candidates
- review-priority distributions
- retained low-priority evidence
- downstream review substrate preparation

### Why It Matters

Demonstrates:

- reviewability-aware evidence generation
- downstream inspection readiness
- separation of retention vs prioritization

This table should not be interpreted as orthogonal or clinical validation output.

Instead, it documents how VAP prepares biologically contextualized candidate substrate suitable for downstream review workflows.

---

## `provenance_summary.tsv`

### Purpose

Summarizes run-level provenance, execution context, and metadata lineage.

### Highlights

Tracks:

- run IDs
- assay metadata
- execution classifications
- machine identifiers
- configuration lineage
- semantic metadata drift
- checkpoint-development history

### Why It Matters

Demonstrates:

- provenance preservation
- telemetry evolution
- metadata-aware execution
- semantic QA maturation

This table is central to the VAP v1 claim that VAP preserves transparent execution lineage and reproducible evidence-generation context.

---

# Planned Harvester Artifacts

## `coding_noncoding_consequence_summary.tsv`

### Purpose

Summarizes biological consequence structure across coding and noncoding evidence channels.

### Highlights

Tracks:

- coding vs noncoding distributions
- HIGH/MODERATE/LOW/MODIFIER impacts
- biological consequence composition
- candidate substrate structure

### Why It Matters

Demonstrates:

- biologically structured evidence refinement
- functional consequence awareness
- transcript-aware annotation integration

This table helps communicate the biological composition of retained candidate evidence.

---

## `clinical_status_summary.tsv`

### Purpose

Summarizes ClinVar-style interpretation categories present within retained candidate evidence.

### Highlights

Tracks:

- pathogenic
- likely pathogenic
- VUS
- benign
- conflicting interpretation structures

### Why It Matters

Demonstrates:

- annotation-aware evidence structuring
- preservation of external interpretation metadata
- candidate evidence contextualization

This table does not make clinical claims and should not be interpreted as diagnostic output.

---

# Important Notes

## Legacy HG002 Development Run

`run_2026_04_17_082417` represents a historical checkpoint-development lineage during VAP maturation.

Stages 01–06 were executed as an early continuous MARK production run, while stages 07–13 were progressively checkpoint-completed during active VAP development following VEP environment repair and stage-level reconstruction.

This run therefore preserves important historical evidence regarding:

- VAP operational maturation
- telemetry evolution
- provenance normalization
- checkpoint-aware recovery workflows

It should not be interpreted as directly equivalent to later telemetry-era production runs.

---

## Assay Metadata Drift Example

`run_2026_05_14_083044` intentionally preserves an incorrect harvested assay metadata label (`WGS`) because the run occurred before assay-aware provenance normalization patches were introduced.

The accompanying metadata annotations preserve:

- the original harvested provenance
- semantic drift detection
- downstream metadata correction rationale

This demonstrates VAP telemetry maturation and provenance QA evolution.

---

# Architectural Positioning

These harvested tables intentionally stop short of acting as a persistent evidence warehouse.

Long-term:

- VAP produces sample-specific observed evidence
- GSC provides phenotype-scoped semantic contextualization
- VDB will eventually provide persistent cross-run evidence centralization
- RDGP will eventually provide downstream prioritization workflows

This directory therefore represents:

- deterministic harvested evidence substrate
- operational telemetry substrate
- figure-ready case-study substrate
- ecosystem bridge substrate

for the emerging VitamOrdinatio computational genomics ecosystem.

---

