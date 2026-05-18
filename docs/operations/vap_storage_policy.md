# VAP Storage Policy

## Purpose

This document defines long-term storage, retention, synchronization, compression, and cleanup policy for the Variant Annotation Pipeline (VAP).

The goal is to balance:

- reproducibility
- provenance preservation
- biological substrate retention
- storage sustainability
- operational scalability
- and future ecosystem interoperability

across both:

- local development systems (e.g., SYS76)
- and larger compute/storage systems (e.g., MARK).

This policy also helps ensure that VAP does not accidentally evolve into a permanent large-scale evidence warehouse. Long-term durable evidence brokerage responsibilities belong to future ecosystem infrastructure such as VDB.

---

# Core Philosophy

VAP is designed to:

```text
preserve biological evidence space while organizing it into reproducible abstraction layers.
```

However, not all generated artifacts require equal retention priority.

Storage policy therefore follows a:

```text
tiered retention model
```

based on:
- reproducibility value
- biological value
- regeneration cost
- storage footprint
- and downstream ecosystem utility.

---

# Retention Tiers

## Tier 1 — Canonical Lightweight Reproducibility Substrate

### Retention Policy

- retain long-term
- mirror selectively to SYS76
- preserve on MARK
- safe for synchronization and audit

### Typical Files

```text
metadata/
processed/stage_08_summary.json
processed/stage_09_summary.json
processed/stage_10_summary.json
processed/stage_11_summary.json
processed/stage_12_summary.json
processed/stage_13_final_summary.json
processed/stage_13_artifact_manifest.json
processed/stage_13_run_report.md
processed/stage_11_gene_variant_counts.tsv
metadata/runtime_profile.tsv
metadata/run_fingerprint.json
metadata/config_snapshot.yaml
logs/pipeline.log.gz
```

### Rationale

These files provide the best balance of:
- provenance
- auditability
- biological abstraction
- reproducibility
- and storage efficiency.

Together they form a:

```text
run capsule
```

sufficient for:
- harvester operations
- run auditing
- reproducibility validation
- and downstream interpretation summaries.

---

## Tier 2 — Large Canonical Biological Substrate

### Retention Policy

- preserve primarily on MARK
- selectively retain for showcase or case-study runs
- avoid routine synchronization to SYS76

### Typical Files

```text
processed/stage_11_prioritized_variants.tsv
processed/stage_12_validation_candidates.tsv
processed/stage_10_noncoding_interpreted.tsv
processed/annotated_variants.tsv
processed/annotated_variants.vcf
interim/*.bam
interim/*.vcf
```

### Rationale

These files are biologically valuable but storage-intensive.

They remain important for:
- future reinterpretation
- spotlight analysis
- regulatory substrate preservation
- and downstream ecosystem integration.

However, they are too large for routine transfer or Git versioning.

---

## Tier 3 — SYS76 Synchronization Substrate

### Retention Policy

- selectively mirror from MARK to SYS76
- support documentation, harvesting, plotting, and interpretation workflows

### Typical Files

```text
processed/stage_09_coding_interpreted.tsv
processed/stage_11_gene_variant_counts.tsv
processed/*summary*.json
metadata/runtime_profile.tsv
metadata/run_fingerprint.json
metadata/config_snapshot.yaml
logs/pipeline.log.gz
```

### Rationale

These files are compact enough to support:
- local interpretation workflows
- harvester development
- figure generation
- and documentation generation

without requiring movement of massive biological substrate files.

---

## Tier 4 — Git-Versioned Artifacts

### Retention Policy

- retain in Git
- preserve as documentation and portfolio substrate
- compress large generated artifacts when appropriate

### Typical Files

```text
docs/case_studies/tables/*.tsv
docs/case_studies/tables/*.tsv.gz
docs/case_studies/figures/*.png
docs/case_studies/figures/*.pdf
docs/case_studies/tables/README.md
docs/plans/*.md
docs/operations/*.md
```

### Compression Guidance

Large generated TSVs should generally be compressed before versioning.

Example:

```text
gene_burden_summary.tsv.gz
```

rather than:

```text
gene_burden_summary.tsv
```

### Rationale

Git should primarily track:
- abstraction artifacts
- figures
- documentation
- and lightweight reproducibility summaries

rather than massive intermediate biological substrate.

---

## Tier 5 — Disposable / Regenerable Substrate

### Retention Policy

- may be deleted
- may be excluded from synchronization
- may be regenerated if needed

### Typical Files

```text
temporary scratch files
debug probe outputs
duplicative intermediates
raw temporary VCFs
obsolete transient logs
failed installation outputs
noncanonical checkpoint artifacts
```

### Rationale

These files do not materially improve:
- reproducibility
- provenance
- or downstream interpretation

relative to their storage cost.

---

# Run Capsule Concept

Every completed VAP execution should ideally retain a compact:

```text
run capsule
```

containing:

```text
metadata/
processed/*summary*.json
processed/stage_13_run_report.md
processed/stage_11_gene_variant_counts.tsv
metadata/runtime_profile.tsv
metadata/run_fingerprint.json
metadata/config_snapshot.yaml
logs/pipeline.log.gz
```

This capsule should be:
- portable
- auditable
- lightweight
- and sufficient for most harvester workflows.

---

# MARK vs SYS76 Operational Philosophy

## MARK

Primary responsibilities:
- large-scale storage
- heavy biological substrate retention
- full run preservation
- BAM/VCF retention
- noncoding substrate preservation
- batch SRA processing

## SYS76

Primary responsibilities:
- development
- plotting
- documentation
- harvester operations
- figure generation
- selective interpretation workflows

This separation helps prevent:
- unnecessary storage duplication
- local workstation exhaustion
- and operational sprawl.

---

# Compression Policy

Recommended compression targets:

```text
*.tsv.gz
*.log.gz
```

Compression is especially recommended for:
- large summary tables
- runtime logs
- and bulky interpreted substrate exports.

Compression should preserve:
- deterministic regeneration
- auditability
- and reproducibility.

---

# Proposed Cleanup Script

## Planned Utility

Future operational tooling may include:

```text
scripts/operations/prune_vap_runs.py
```

or similar infrastructure.

### Intended Goals

- reduce manual deletion risk
- enforce storage policy consistently
- preserve canonical run capsules
- support dry-run inspection
- generate deletion manifests
- and provide auditable cleanup behavior

### Planned Features

```text
--dry-run
--apply
--run-id
--keep-large-substrate
```

### Planned Manifest Output

Example:

```text
docs/operations/storage_cleanup_manifest_<timestamp>.tsv
```

with fields such as:

```text
run_id
path
size_bytes
retention_class
action
reason
```

### Important Principle

Cleanup operations should be:

```text
auditable
deterministic
and conservative by default.
```

Manual deletion across run directories is discouraged because of the risk of accidentally deleting canonical reproducibility substrate.

---

# Relationship to Future Ecosystem Infrastructure

This storage policy intentionally avoids turning VAP into:
- a permanent biological evidence warehouse
- a semantic identity broker
- or a durable large-scale query system.

Those responsibilities are expected to belong primarily to:
- VDB
- and downstream ecosystem infrastructure.

VAP instead focuses on:
- deterministic evidence harvesting
- reproducible interpretation
- and biologically aware abstraction generation.

---

# Strategic Summary

The VAP storage model prioritizes:

```text
reproducible lightweight abstraction retention
```

while still preserving:
- biologically valuable substrate
- future reinterpretation flexibility
- and scalable operational sustainability.

This policy helps ensure that VAP remains:
- scientifically useful
- operationally sustainable
- and architecturally coherent
as the broader ecosystem evolves.

