# docs/status/phase1_reproducibility_assessment.md

# Phase 1 Reproducibility Assessment

## MARK1 WES Reproducibility Campaign

**Repository:** variant_annotation_pipeline  
**Branch:** `phase0-logging-foundation`  

**Phase:** Phase 1A  
**Status:** ACTIVE OBSERVATIONAL REPRODUCIBILITY ASSESSMENT

---

## Related Documents

- `docs/status/phase1_runtime_baseline_status.md`
- `docs/status/phase1_reproducibility_assessment.md`
- `docs/status/phase1_operational_findings.md`

---

# Purpose

This document tracks early reproducibility assessment for VAP Phase 1A production telemetry runs on MARK1 infrastructure.

The goal is not yet formal statistical reproducibility modeling, but rather observational assessment of:

- structural reproducibility
- biological-result reproducibility
- operational variability
- provenance-model stability

---

## Current Reproducibility Coverage

Current WES reproducibility telemetry includes:

### ERR10619281
- 1 pre-assay-provenance patch execution
- 1 post-assay-provenance patch rerun

This dataset currently functions as:

- a metadata-transition reproducibility assessment
- a biological-result stability assessment across provenance-model evolution

### ERR10619300
- 2 post-assay-provenance patch executions

This dataset currently functions as:

- a same-patch rerun reproducibility assessment
- a repeated operational telemetry baseline

Together, these runs provide multiple independent WES-scale reproducibility observations on MARK1 infrastructure.

---

## Reproducibility Evidence Snapshot

The following telemetry snapshot was harvested directly from MARK1 pipeline logs during the initial Saudi epilepsy cohort execution campaign.

| Run ID | Dataset | FASTQ Counts | Stage 11 Rows | Stage 12 Rows |
|---|---|---:|---:|---:|
| run_2026_05_14_083044 | ERR10619281 pre-assay-provenance patch | 83,696,516 / 83,696,516 | 811,554 | 811,554 |
| run_2026_05_14_231247 | ERR10619281 post-assay-provenance patch rerun | 83,696,516 / 83,696,516 | 811,554 | 811,554 |
| run_2026_05_14_164444 | ERR10619300 post-assay-provenance patch | 83,673,287 / 83,673,287 | 736,468 | 736,468 |
| run_2026_05_15_063040 | ERR10619300 same-patch rerun | 83,673,287 / 83,673,287 | 736,468 | 736,468 |

### Initial Observations

**General observations:**

- The assay-type provenance patch did not perturb downstream Stage 11/12 biological output structure.
- Early evidence suggests strong biological-result reproducibility across repeated WES-scale Saudi cohort runs.

**ERR10619281 observations:**

- ERR10619281 reproduced identical FASTQ pair counts across both runs.
- ERR10619281 reproduced identical Stage 11 prioritized row counts across both runs.
- ERR10619281 reproduced identical Stage 12 validation candidate row counts across both runs.

**ERR10619300 observations:**
- ERR10619300 reproduced identical FASTQ pair counts across both same-patch executions.
- ERR10619300 reproduced identical Stage 11 prioritized row counts across both same-patch executions.
- ERR10619300 reproduced identical Stage 12 validation candidate row counts across both same-patch executions.

This snapshot represents observational telemetry only. Formal reproducibility comparison tooling has not yet been implemented.

Current conclusions remain observational rather than statistically modeled.

---

## Reproducibility Layers

VAP reproducibility is currently evaluated across multiple operational layers:

1. Byte-level reproducibility
   - exact file hash equivalence
   - highly sensitive to timestamps, metadata, ordering, and provenance artifacts
   - sensitive to timestamps, provenance hashes, runtime telemetry, and artifact ordering

2. Structural reproducibility
   - stable schemas
   - stable row counts
   - stable artifact organization
   - stable stage outputs

3. Biological reproducibility
   - stable prioritized variant distributions
   - stable validation candidate distributions
   - stable cohort interpretation behavior

Current evidence demonstrates strong structural and biological reproducibility across repeated WES-scale execution on MARK1.

---

| Metric | Stable Across Reruns |
|---|---|
| FASTQ pair counts | Yes |
| Stage 11 row counts | Yes |
| Stage 12 row counts | Yes |
| Large TSV line counts | Yes |
| Biological distributions | Yes |
| Runtime telemetry | Similar but variable |
| Run IDs | No (expected) |
| Timestamps | No (expected) |
| Provenance hashes | No (expected) |

---

### Early Reproducibility Interpretation

Initial lightweight reproducibility probing revealed:

- stable FASTQ pair counts (identical)
- stable Stage 11 prioritized row counts (identical)
- stable Stage 12 validation row counts (identical)
- stable Stage 11/12 biological distributions (identical)
- stable large-output file sizes and line counts (identical)
- similar stage-runtime behavior across repeated runs

Observed variability was limited primarily to:

- run IDs
- timestamps
- git commits
- config hashes
- runtime telemetry
- provenance metadata
- small JSON/Markdown artifact hashes

Importantly, byte-level hash instability did NOT imply biological-result instability.

This distinction is operationally important because VAP reproducibility is currently being evaluated primarily at the:

- structural-output layer
- biological-distribution layer
- cohort-interpretation layer

rather than strict byte-identical artifact reproduction.

---

## Determinism Consideration

Phase 1A also functions as a reproducibility checkpoint.

Because these repeated executions use:

- same machine
- same dataset
- same general configuration class

the resulting outputs should remain biologically and structurally stable.

Expected stable outputs include:

- variant counts
- Stage 08–13 row counts
- prioritized variant structure
- validation candidate structure
- stage summary metrics
- artifact manifests

Expected operationally variable outputs include:

- run IDs
- timestamps
- runtime profiles
- telemetry snapshots
- absolute paths

This rerun therefore also evaluates VAP determinism under repeated production execution.

---

## Lightweight Comparison Tooling

Phase 1A reproducibility assessment now includes reusable lightweight comparison tooling:

- `scripts/analysis/compare_vap_runs.py`
- `scripts/mark/mark_compare_err10619281_runs.sh`

These tools support:

- structural-output comparison
- telemetry comparison
- lightweight artifact assessment
- operational reproducibility inspection

without requiring transfer of large BAM/VCF artifacts from MARK infrastructure.

---

## Current Known Reproducibility Limitations

Current known reproducibility limitations include:

- byte-identical artifact reproducibility has not yet been formally evaluated
- cross-node reproducibility (MARK1 vs MARK2/3) remains untested
- WGS reproducibility stability remains under active investigation
- current conclusions remain observational rather than statistically modeled
- long-term cache effects remain unknown
- filesystem I/O scaling behavior remains unknown

---

## Preliminary Assessment

Current evidence supports:

- strong structural reproducibility
- strong biological-result reproducibility
- stable Stage 11/12 cohort interpretation behavior
- stable large-artifact structure under repeated WES execution

while simultaneously indicating:

- expected operational variability in runtime telemetry
- expected operational variability in provenance metadata
- expected operational variability in timestamp/hash behavior

> No current evidence suggests biological-result instability across repeated Saudi WES telemetry runs on MARK1.

---
