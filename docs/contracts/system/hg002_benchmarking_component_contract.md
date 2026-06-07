# hg002_benchmarking_component_contract.md

## Purpose

This document defines the architectural contract, scientific scope, execution constraints, operational expectations, semantic boundaries, and output requirements for the HG002 benchmarking component within the Variant Annotation Pipeline (VAP) ecosystem.

This benchmarking layer establishes:

```text
benchmark-aware engineering validation
```

for the upstream VAP substrate-generation engine using:

```text
GIAB HG002 benchmark resources
```

---

# Scope

This component validates:

* alignment-derived variant substrate generation,
* normalization consistency,
* representation harmonization,
* deterministic VCF-generation behavior,
* and small-variant recovery fidelity.

This component does NOT validate:

* biological interpretation,
* semantic prioritization,
* RDGP reasoning,
* GSC contextualization,
* translational candidate significance,
* or disease relevance.

---

# Strategic Role

The VAP ecosystem now contains two complementary validation pillars:

| Validation Layer    | Purpose                          |
| ------------------- | -------------------------------- |
| HG002 benchmarking  | engineering validity             |
| Saudi epilepsy SRAs | translational biological utility |

Together these establish:

```text
reproducible genomics engineering
+
biologically meaningful substrate recovery
```

within the VAP ecosystem.

---

# Architectural Boundary

HG002 benchmarking SHALL remain:

```text
modular
```

and SHALL remain logically separated from:

* semantic interpretation,
* prioritization,
* GSC overlays,
* RDGP reasoning,
* and downstream translational inference.

The benchmarking component validates:

```text
substrate-generation fidelity
```

ONLY.

---

# Execution Environment Constraint

The HG002 benchmarking component SHALL initially be treated as:

```text
MARK-bound infrastructure
```

and SHALL be executed on MARK unless equivalent resources are explicitly mirrored elsewhere.

Reason:

* intact VAP run artifacts reside on MARK,
* normalized HG002 VCF substrates reside on MARK,
* GIAB benchmark resources reside on MARK,
* GRCh38 reference resources reside on MARK,
* and benchmarking tooling is expected to be installed on MARK.

The component SHALL fail fast if required resources are absent.

---

# Required MARK Resources

## Required HG002 Run Artifacts

The component SHALL require:

```text
results/<run_id>/interim/*.normalized_variants.vcf
```

generated from a completed HG002 VAP run.

The benchmarking component SHALL benchmark normalized VCF substrates rather than raw or semantically interpreted outputs.

---

## Required GIAB Truth Resources

The following GIAB resources SHALL be available:

```text
HG002_GRCh38_1_22_v4.2.1_benchmark.vcf.gz
HG002_GRCh38_1_22_v4.2.1_benchmark.bed
```

These SHALL be:

* GRCh38-consistent,
* coordinate-compatible,
* and benchmarking-compatible with the VAP operating environment.

Benchmark execution SHALL fail if query VCF and GIAB truth resources are not reference-build compatible.

---

## Required Reference Genome

The component SHALL require:

```text
GRCh38.primary_assembly.genome.fa
```

consistent with:

* VAP alignment,
* normalization,
* and variant-calling operations.

---

## Required Benchmarking Tool

The component SHALL require:

```text
hap.py
```

accessible within the MARK execution environment.

---

# Benchmarking Philosophy

The benchmarking component SHALL explicitly restrict benchmarking evaluation to GIAB high-confidence BED regions during benchmark execution.

Benchmarking SHALL compare:

```text
VAP normalized VCF
```

against:

```text
GIAB HG002 truth VCF
```

restricted to:

```text
GIAB confident benchmark BED regions
```

Benchmarking SHALL NOT indiscriminately evaluate:

* centromeres,
* poorly characterized regions,
* repetitive uncertainty regions,
* or non-confident genomic intervals.

---

# Scientific Interpretation Constraint

Benchmark concordance metrics SHALL be interpreted as:

```text
engineering validation metrics
```

NOT:

* diagnostic claims,
* clinical claims,
* state-of-the-art claims,
* or biological significance claims.

Benchmarking SHALL remain focused on:

* reproducibility,
* methodological transparency,
* substrate integrity,
* and engineering rigor.

---

# Representation Harmonization Principle

Benchmark concordance SHALL explicitly recognize the importance of:

* left-alignment,
* normalization,
* decomposition,
* and representation consistency.

The benchmarking layer therefore evaluates:

* variant calling behavior,
* normalization fidelity,
* and representation harmonization,

NOT merely:

```text
raw variant overlap
```

---

# Variant Classes

The benchmarking component SHALL support benchmarking across multiple feature classes, including:

| Variant Class            | Purpose                         |
| ------------------------ | ------------------------------- |
| SNPs                     | SNV recovery fidelity           |
| indels                   | insertion/deletion recovery     |
| PASS variants            | high-confidence callable subset |
| callable normalized query variants  | broader call behavior           |
| chromosome-level metrics | anomaly detection               |
| false positives          | overcalling inspection          |
| false negatives          | missed truth inspection         |

---

# Expected Outputs

The component SHALL emit structured benchmarking outputs into:

```text
results/<run_id>/benchmarking/
```

---

# Required Output Artifacts

## Summary Metrics

Required outputs SHALL include:

```text
hg002_benchmark_summary.tsv
hg002_benchmark_summary.json
```

including:

* precision,
* recall,
* F1,
* TP,
* FP,
* FN,
* SNP metrics,
* and indel metrics.

---

## Error Inspection Outputs

Required outputs SHALL include:

```text
hg002_false_positives.tsv
hg002_false_negatives.tsv
```

for downstream inspection and debugging.

---

## Stratified Metrics

Required outputs SHALL include:

```text
hg002_snp_indel_metrics.tsv
```

supporting:

* SNP/indel comparison,
* representation-effect inspection,
* and normalization-aware evaluation.

---

## Operational Logging

The component SHALL emit:

```text
benchmarking.log
```

for:

* reproducibility,
* execution traceability,
* and failure interpretation.

---

# Determinism Requirement

Repeated benchmarking runs against identical:

* normalized VCFs,
* truth resources,
* BED regions,
* and reference resources

SHALL produce:

* deterministic benchmarking outputs,
* stable summary metrics,
* and reproducible concordance results.

---

# Failure Semantics

The component SHALL fail fast for:

* missing normalized VCFs,
* missing benchmark resources,
* missing BED resources,
* reference incompatibility,
* hap.py unavailability,
* malformed benchmark outputs,
* or coordinate-build mismatches.

The component SHALL NOT silently continue under unresolved benchmark conditions.

---

# Modularity Requirement

The benchmarking component SHALL initially exist as:

```text
a standalone benchmarking component
```

rather than as a tightly integrated canonical VAP pipeline stage.

This preserves:

* modularity,
* benchmarking purity,
* interpretability,
* and future tool interchangeability.

Potential future migration into:

```text
stage_14_hg002_benchmarking
```

MAY occur after:

* workflow stabilization,
* contract validation,
* and operational hardening.

---

# Recommended Initial Placement

Initial implementation is expected to reside under:

```text
scripts/benchmarking/
```

Examples may include:

```text
run_hg002_happy_benchmark.py
run_hg002_happy_benchmark.sh
```

---

# Telemetry Philosophy

Benchmarking outputs SHOULD remain:

* structured,
* machine-readable,
* provenance-aware,
* and future VDB-compatible.

Future versions MAY integrate:

* benchmark telemetry,
* longitudinal tracking,
* benchmarking dashboards,
* or version-to-version benchmark comparisons.

---

# Anti-Overclaim Constraint

The HG002 benchmarking layer SHALL NOT be framed as:

* clinical validation,
* diagnostic certification,
* production-grade benchmarking,
* or leaderboard optimization.

Preferred framing SHALL remain:

```text
benchmark-aware engineering validation
```

and:

```text
scientifically grounded reproducible genomics engineering
```

---

# Relationship To Downstream Ecosystem

This benchmarking layer strengthens confidence in:

* VDB-ready substrates,
* RDGP-ready substrates,
* semantic interpretation infrastructure,
* and interoperability-oriented exports

because downstream systems inherit confidence from:

```text
the integrity of the upstream variant substrate layer
```

---

# Operational Goal For v1.0

The primary v1.0 goal is NOT:

* maximal benchmark optimization,
* hyperparameter tuning,
* or competitive benchmarking.

The primary goal IS:

* transparent methodology,
* deterministic reproducibility,
* engineering rigor,
* and benchmark-aware infrastructure validation.

---

# Final Principle

The purpose of HG002 benchmarking within VAP is not merely to demonstrate:

```text
pipeline execution
```

but to establish:

```text
scientifically grounded benchmark-aware genomics engineering
```

within a reproducible and semantically extensible computational ecosystem.
