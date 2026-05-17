# Harvest Case Metrics Implementation Plan
## VAP v1 Case-Study Biological Evidence Harvesting

**Target file:** `docs/plans/harvest_case_metrics_implementation_plan.md`  
**Primary script:** `scripts/analysis/harvest_vap_case_metrics.py`  
**Status:** Planned  
**Scope:** VAP v1 evidence consolidation sprint  

---

## Purpose

This plan defines a lightweight post-run analysis module for harvesting biological, reproducibility, and overlay-intersection metrics from completed VAP runs.

The goal is to support VAP v1 case studies by converting completed run artifacts into stable, human-readable and machine-readable evidence tables.

This module is intended to demonstrate that VAP does more than execute efficiently. It produces reproducible, biologically structured, provenance-controlled candidate evidence streams suitable for downstream:

- case-study documentation
- GSC overlay evaluation
- VDB persistence planning
- RDGP candidate substrate generation
- future cohort-level recurrence analysis

---

## Core Framing

VAP should be presented as a:

```text
provenance-aware genomic evidence refinement framework
```

not merely as a variant-calling pipeline.

The harvesting module should therefore emphasize:

- biological-output stability
- reproducible evidence structures
- candidate substrate generation
- gene-level burden summaries
- phenotype-scoped semantic contextualization
- downstream query readiness

Runtime telemetry remains important, but the central v1 claim should be that VAP generates stable biological evidence outputs across repeated production executions.

---

## Non-Goals

This implementation must not perform clinical interpretation.

The module must not claim:

- diagnostic findings
- causal variants
- pathogenic discoveries
- disease enrichment
- patient-level diagnosis

Allowed language:

- candidate substrate
- candidate recovery
- overlay intersection
- biological contextualization
- prioritized evidence
- reproducibility summary
- downstream evaluation target

---

## Input Scope

The script will operate on completed VAP run directories.

Expected run directory structure:

```text
results/<run_id>/
  metadata/
    runtime_profile.tsv
    run_metadata.json
    run_fingerprint.json
    stage_summaries/
  processed/
    stage_11_prioritized_variants.tsv
    stage_12_validation_candidates.tsv
    stage_13_run_report.md
```

Primary biological inputs:

```text
processed/stage_11_prioritized_variants.tsv
processed/stage_12_validation_candidates.tsv
```

Primary metadata inputs:

```text
metadata/run_metadata.json
metadata/run_fingerprint.json
metadata/runtime_profile.tsv
```

GSC overlay inputs:

Preferred overlay inputs should be exported from GSC v1.0 when available.

Overlay exports should remain immutable release artifacts once incorporated into published case-study analyses.

Fallback simple TSV inputs may be used during early implementation:

`data/overlays/epi25_genes.tsv`
`data/overlays/mitocarta_genes.tsv`
`data/overlays/genes4epilepsy_genes.tsv`

Overlay file paths may be configurable.

---

## Initial Case-Study Runs

The initial implementation should support the current VAP v1 case-study set:

| Dataset     | Run ID                       | Role                                |
| ----------- | ---------------------------- | ----------------------------------- |
| HG002       | historical + telemetry rerun | observability / metadata maturation |
| ERR10619281 | `run_2026_05_14_083044`      | pre-assay-provenance patch baseline |
| ERR10619281 | `run_2026_05_14_231247`      | post-assay-provenance patch rerun   |
| ERR10619300 | `run_2026_05_14_164444`      | first post-patch execution          |
| ERR10619300 | `run_2026_05_15_063040`      | same-patch rerun                    |

Core reproducibility interpretation:

| Dataset     | Reproducibility Role                   |
| ----------- | -------------------------------------- |
| HG002       | historical operational comparison      |
| ERR10619281 | metadata-transition reproducibility    |
| ERR10619300 | same-patch operational reproducibility |

---

---

## Gene-List Overlay Intersection Design

### Purpose

Harvest deterministic intersections between VAP gene-burden substrate and curated gene-list overlays.

This replaces the earlier `gsc_overlay_intersections.tsv` target for VAP v1.

### Rationale

Full GSC semantic integration is deferred until VDB provides formal, auditable namespace normalization.

For VAP v1, overlay harvesting will use curated gene lists with matched identifiers:

- `data/reference/gene_lists/mitocarta_vap_overlay_seed.tsv`
- `data/reference/gene_lists/epi25_vap_overlay_seed.tsv`

Both overlay seed files use the same schema:

```text
gene_id
gene_symbol
ensembl_gene_id
```

### Match Strategy

Primary match:

```text
overlay ensembl_gene_id ↔ VAP gene_id
```

This avoids gene-symbol ambiguity and avoids premature namespace brokerage inside VAP.

### Output Artifact

`docs/case_studies/tables/gene_list_overlay_intersections.tsv`

### Output Semantics

Emit one row per VAP gene per run that intersects at least one curated overlay list.

Recommended fields:

```text
sample_id
run_id
assay_type
run_classification
gene_id
gene_symbol
gene_burden_rank
variant_count
overlay_source
overlay_source_count
overlay_source_list
mitocarta_hit
epi25_hit
match_key
```

### Source Tracking

Overlay provenance must be first-class.

A gene may intersect:

- MitoCarta only
- EPI25 only
- both MitoCarta and EPI25

The both category is biologically important because it may represent:

```text
mitochondrial biology ∩ epilepsy genetics
```

### Scope Boundary

This artifact is not full GSC semantic integration.

It is a deterministic curated gene-list overlay for VAP v1 case-study harvesting.

Long-term namespace normalization belongs in VDB, where source-native identifiers, canonical identifiers, symbols, aliases, and provenance can be handled formally.

### Strategic Questions Supported

This artifact supports questions such as:

- Which retained VAP genes intersect mitochondrial gene space?
- Which retained VAP genes intersect high-confidence epilepsy loci?
- Which retained VAP genes intersect both lists?
- Do the Saudi epilepsy SRAs show different overlay-hit patterns?
- Which overlay-hit genes may seed later RDGP demonstration?

---

## Output Directory

Primary outputs should be written to:

`docs/case_studies/tables/`

Per-run machine-readable summaries should be written to:

`results/case_study_metrics/`

The script should create these directories if absent.

---

## Required Outputs

### 1. Variant Consequence Summary

Output:

`docs/case_studies/tables/variant_consequence_summary.tsv`

Purpose:

Summarize per-run variant consequence and impact structure.

Suggested fields:

```text
sample_id
run_id
assay_type
total_variants
coding_variants
noncoding_variants
missense_variants
synonymous_variants
frameshift_variants
stop_gained_variants
splice_region_variants
high_impact_variants
moderate_impact_variants
low_impact_variants
modifier_impact_variants
tier_1_variants
tier_2_variants
tier_3_variants
tier_4_variants
```

Primary source:

`processed/stage_11_prioritized_variants.tsv`

Notes:

- Count using normalized lowercase consequence strings where possible.
- Multi-consequence annotations should be counted conservatively and documented.
- Missing values should be represented consistently as NA.

---

### 2. Gene-Level Burden Summary

Output:

`docs/case_studies/tables/gene_burden_summary.tsv`

Purpose:

Create proto-VDB-style gene-level summaries from prioritized VAP output.

Suggested fields:

```text
sample_id
run_id
gene_symbol
gene_id
variant_count
high_impact_variant_count
moderate_impact_variant_count
rare_variant_count
pathogenic_count
likely_pathogenic_count
vus_count
benign_count
max_impact
best_priority_tier
```

Primary source:

`processed/stage_11_prioritized_variants.tsv`

Notes:

- One row per (sample_id, run_id, gene_symbol).
- Preserve gene_id where available.
- Use deterministic sorting:
  1. sample_id
  2. run_id
  3. descending variant_count
  4. gene_symbol

---

#### Recommended Derived Gene-Level Metrics

The harvesting layer should additionally support generation of derived run-level burden metrics including:

```text
affected_gene_count
high_impact_gene_count
epilepsy_gene_overlap_count
mitochondrial_gene_overlap_count
direct_disease_overlap_count
contextual_biology_overlap_count
```

These metrics may initially be emitted through:

```text
results/case_study_metrics/<sample_id>_<run_id>_summary.json
```

before eventual promotion into standalone tables.

---

### 3. Run-Level Biological Reproducibility Summary

Output:

`docs/case_studies/tables/run_reproducibility_summary.tsv`

Purpose:

Demonstrate biological-output stability across duplicate or paired runs.

Suggested fields:

```text
comparison_id
sample_id
run_id_a
run_id_b
comparison_type
same_fastq_counts
same_stage11_row_count
same_stage12_row_count
same_variant_consequence_summary
same_gene_burden_summary
same_overlay_intersections
same_candidate_spotlight_set
biological_stability_classification
notes
```

Initial comparisons:

| Comparison ID                     | Type                     |
| --------------------------------- | ------------------------ |
| `ERR10619281_metadata_transition` | pre-patch vs post-patch  |
| `ERR10619300_same_patch`          | post-patch vs post-patch |


Recommended classifications:

```text
STRUCTURALLY_AND_BIOLOGICALLY_STABLE
STRUCTURALLY_STABLE_WITH_BIOLOGICAL_DIFFERENCES
NOT_COMPARABLE
INCOMPLETE_INPUTS
```

Notes:

- This is the central output for the v1 biological determinism claim.
- It should compare derived biological tables rather than only raw file hashes.
- File hashes may be included later but should not be the primary reproducibility claim.

---

### 4. Overlay Intersections

#### Core Architectural Alignment

The harvester is an adapter layer, not an authority layer: it prepares VAP evidence for GSC contextualization while preserving both repositories' source-of-truth boundaries.

The harvesting layer should therefore be understood as a deterministic evidence aggregation and contextualization layer rather than a lightweight reporting utility.

VAP and GSC operate in distinct identity spaces.

| Repository | Identity Space | Role |
|---|---|---|
| VAP | `(sample_id, variant_id)` | sample-specific observed variant evidence |
| GSC | `(phenotype, gene_id)` | phenotype-scoped semantic priors |

The harvesting layer should therefore aggregate VAP outputs from:

```text
(sample_id, variant_id)
```

toward:

```text
(sample_id, gene_id)
```

before attaching GSC semantic overlays.

This preserves:

- VAP authority over observed evidence
- GSC authority over phenotype-scoped semantic context

The harvesting layer should therefore be understood as:

```text
sample-specific evidence aggregation
+
phenotype-scoped semantic contextualization
```

rather than:
```text
simple gene-list intersection
```

---

#### GSC Overlay Inputs

Preferred overlay inputs should be exported from GSC v1.0 when available.

Fallback simple TSV inputs may be used during early implementation:

`data/overlays/epi25_genes.tsv`
`data/overlays/mitocarta_genes.tsv`
`data/overlays/genes4epilepsy_genes.tsv`

However, the preferred long-term interaction model is:

```text
VAP gene-level evidence
+
GSC phenotype-scoped semantic priors
```

rather than static gene-list overlap alone.

Overlay file paths may be configurable.

---

#### GSC Semantic Overlay Compatibility

Overlay intersection behavior should remain compatible with the existing:

`vap_to_gsc_interface_spec.md`

interaction expectations.

Before final implementation, DEX-VAP should coordinate with DEX-GSC to confirm:
- export field expectations
- provenance conventions
- naming conventions
- phenotype-scoped overlay semantics

GSC overlays should:

```text
contextualize
```

not:

```text
reinterpret
```

VAP remains authoritative for:

- observed variants
- variant quality
- consequence annotations
- pathogenicity evidence
- sample-specific evidence structure

GSC remains authoritative for:

- phenotype-scoped semantic priors
- semantic evidence channels
- contextual biological support
- disease-layer semantic aggregation

GSC overlays must never overwrite observed VAP evidence.

Output:

`docs/case_studies/tables/gsc_overlay_intersections.tsv`

Purpose:

Create a VAP → GSC semantic contextualization bridge by attaching phenotype-scoped semantic priors to aggregated observed gene-level variant evidence.

Overlay sources may include GSC-curated phenotype-specific outputs derived from:

- EPI25
- MitoCarta
- Genes4Epilepsy
- additional future GSC-supported evidence channels

Suggested fields:

```text
sample_id
run_id
phenotype
gene_symbol
gene_id
overlay_source
overlay_source_provenance
consensus_score
semantic_consensus_score
semantic_channel_summary
source_count
source_list
gsc_priority_tier
gsc_version
gsc_provenance_id
variant_count
high_impact_variant_count
moderate_impact_variant_count
rare_variant_count
max_impact
best_priority_tier
candidate_reason
```

GSC semantic channels should remain preserved in overlay outputs because different semantic evidence categories represent biologically distinct support classes rather than interchangeable evidence weights.

Absence from a supplied semantic overlay must not be interpreted as evidence against biological relevance. Overlay membership only reflects support within the selected phenotype-scoped semantic context.

Notes:

- This does not claim enrichment.
- It only documents intersection with biologically meaningful prior spaces.
- If a gene appears in multiple overlays, emit one row per overlay and allow downstream aggregation.

---

### 5. Candidate Spotlight Variants

Output:

`docs/case_studies/tables/candidate_spotlight_variants.tsv`

Purpose:

Generate a ranked, non-clinical candidate table for case-study discussion.

Suggested fields:

```text
sample_id
run_id
gene_symbol
gene_id
variant_id
chrom
pos
ref
alt
variant_type
consequence
impact
clinical_significance
allele_frequency
priority_tier
overlay_sources
candidate_score_simple
why_flagged
phenotype
gsc_priority_tier
semantic_consensus_score
semantic_channel_summary
gsc_provenance_id
```

Simple initial flagging logic:

```text
flag if gene is present in EPI25 OR Genes4Epilepsy OR MitoCarta
AND impact is HIGH or MODERATE
```

Optional stronger flag:

```text
flag if gene appears in 2+ overlays
```

Important guardrail:

The table should be framed as:

```text
candidate spotlight variants for downstream evaluation
```

not:

```text
likely causal variants
```

---

### 6. Per-Run Summary JSON

Output pattern:

`results/case_study_metrics/<sample_id>_<run_id>_summary.json`

Purpose:

Provide machine-readable summary data for future README, case-study docs, plots, and downstream tooling.

Suggested JSON structure:

```json
{
  "sample_id": "...",
  "run_id": "...",
  "assay_type": "...",
  "phenotype_context": "...",
  "runtime_seconds": null,
  "stage11_rows": null,
  "stage12_rows": null,
  "variant_consequence_counts": {},
  "impact_counts": {},
  "priority_tier_counts": {},
  "top_genes_by_variant_count": [],
  "overlay_intersections": {},
  "candidate_spotlight_count": null,
  "affected_gene_count": null,
  "high_impact_gene_count": null,
  "epilepsy_gene_overlap_count": null,
  "mitochondrial_gene_overlap_count": null,
  "direct_disease_overlap_count": null,
  "contextual_biology_overlap_count": null,
  "generated_at_utc": "...",
  "vap_metrics_schema_version": "0.1.0",
  "overlay_provider": "GSC_v1.0_or_fallback_tsv",
  "gsc_version": null,
  "gsc_provenance_id": null
}
```

---

## Implementation Strategy

### Phase 1: Minimal Deterministic Harvester

Implement:

`scripts/analysis/harvest_vap_case_metrics.py`

Required CLI behavior:


```bash
python scripts/analysis/harvest_vap_case_metrics.py \
  --run results/run_2026_05_14_083044 \
  --run results/run_2026_05_14_231247 \
  --run results/run_2026_05_14_164444 \
  --run results/run_2026_05_15_063040 \
  --out-dir docs/case_studies/tables \
  --summary-json-dir results/case_study_metrics
```

GSC v1.0 has completed evidence aggregation for four distinct phenotype-scoped categories:
1. Mitochondrial diseases
2. Epilepsy (inclusive of all epilepsy subtypes)
3. DEE (Developmental and Epileptic Encephalopathy, an epilepsy subtype)
4. NAFE (Non-Acquired Focal Epilepsy, an epilepsy subtype)

For more information, please see:

```text
Epi25 Collaborative. Exome sequencing of 20,979 individuals with epilepsy reveals shared and distinct ultra-rare genetic risk across disorder subtypes. Nat Neurosci. 2024;27(10):1864-1879. doi:10.1038/s41593-024-01747-8
```

Multiple phenotype-scoped overlay passes may be executed independently in order to preserve explicit phenotype-to-overlay provenance relationships.


#### Mitochondrial Diseases

Preferred GSC overlay arguments for **mitochondrial diseases**:

```bash
--phenotype mitochondrial \
--gsc-overlay results/gsc_exports/mitochondrial_semantic_gtr_experimental_consensus_gene_set.tsv
```

#### Epilepsy (all subtypes)

Preferred GSC overlay arguments for **epilepsy (all subtypes)**:

```bash
--phenotype epilepsy \
--gsc-overlay results/gsc_exports/epilepsy_semantic_gtr_experimental_consensus_gene_set.tsv
```

#### DEE

Preferred GSC overlay arguments for **DEE** presentation:

```bash
--phenotype dee \
--gsc-overlay results/gsc_exports/dee_semantic_gtr_experimental_consensus_gene_set.tsv
```

#### NAFE

Preferred GSC overlay arguments for **NAFE** presentation:

```bash
--phenotype nafe \
--gsc-overlay results/gsc_exports/nafe_semantic_gtr_experimental_consensus_gene_set.tsv
```

Add explanatory paragraph:

```text
Phenotype context should remain explicit during GSC overlay operations because GSC semantic priors are phenotype-scoped rather than globally interchangeable.
```

Fallback simple gene-list overlay arguments:

```bash
  --epi25-genes data/overlays/epi25_genes.tsv \
  --mitocarta-genes data/overlays/mitocarta_genes.tsv \
  --genes4epilepsy-genes data/overlays/genes4epilepsy_genes.tsv
```

Optional comparison arguments:

```bash
  --compare ERR10619281_metadata_transition:run_2026_05_14_083044,run_2026_05_14_231247 \
  --compare ERR10619300_same_patch:run_2026_05_14_164444,run_2026_05_15_063040
```

---

### Phase 2: Stable Table Generation

Generate:

- `variant_consequence_summary.tsv`
- `gene_burden_summary.tsv`
- `run_reproducibility_summary.tsv`

These are required before overlay/candidate spotlight logic.

### Phase 3: Overlay Support

Add overlay file parsing.

Overlay input format prefers GSC export parsing while simple gene lists are fallback.

The harvesting layer should preserve all available GSC semantic metadata rather than collapsing overlays into binary membership labels whenever possible.

```text
gene_symbol
SCN1A
DEPDC5
NPRL3
...
```

or:

```text
gene_symbol    source
SCN1A          EPI25
...
```

Implementation should support at minimum a one-column `gene_symbol` TSV.

Normalize gene symbols by:

- stripping whitespace
- uppercasing
- ignoring blank rows
- ignoring comment rows beginning with #

---

### Phase 4: Candidate Spotlight Table

Generate spotlight candidates only after overlay intersections are available.

Initial scoring can be intentionally simple.

Candidate score proposal:

```text
candidate_score_simple =
  2 points if HIGH impact
  1 point if MODERATE impact
  1 point if rare
  1 point per overlay source
  1 point if GSC priority tier is high
```

The scoring heuristic intentionally favors interpretability and deterministic reproducibility over predictive complexity. This score is intentionally deterministic and non-clinical.

It functions only as:
- a reproducible sorting heuristic
- a case-study review aid
- a downstream substrate prioritization helper

It must not be interpreted as:
- pathogenicity prediction
- causal inference
- diagnostic ranking

The harvesting layer intentionally stops short of sample-level prioritization logic, which remains the responsibility of future RDGP workflows.

---

## Determinism Requirements

All outputs must be deterministic.

Required practices:

- stable row ordering
- stable column ordering
- explicit missing value representation as NA
- no nondeterministic sampling
- UTC timestamps only in JSON metadata
- clear schema version field
- no dependence on local shell glob order unless sorted

---

## Testing Requirements

Add lightweight tests if feasible.

Suggested test file:

`tests/test_harvest_vap_case_metrics.py`

Minimum tests:

- Parses minimal Stage 11 TSV fixture.
- Produces expected consequence counts.
- Produces expected gene burden rows.
- Handles missing optional overlay files gracefully.
- Produces deterministic sorted output.
- Does not emit clinical interpretation language.

Fixture location:

`tests/fixtures/case_metrics/`

Testing should not require large VAP artifacts.

---

## Documentation Requirements

Add usage documentation either in:

`docs/case_studies/README.md`

or:

`docs/plans/harvest_case_metrics_implementation_plan.md`

Documentation should explain:

- input expectations
- outputs generated
- guardrails
- non-clinical nature of candidate tables
- how outputs support VAP v1 case studies

---

## Suggested Commit Sequence

### Commit 1: Plan

```bash
git add docs/plans/harvest_case_metrics_implementation_plan.md
git commit -m "plan case-study biological metrics harvesting"
```

### Commit 2: Initial Harvester

```bash
git add scripts/analysis/harvest_vap_case_metrics.py tests/test_harvest_vap_case_metrics.py
git commit -m "add case-study biological metrics harvester"
```

### Commit 3: Generated Case-Study Tables

```bash
git add docs/case_studies/tables/
git commit -m "add harvested VAP case-study metric tables"
```

---

## Success Criteria

The implementation is successful when VAP can generate:

- variant consequence summaries
- gene-level burden summaries
- reproducibility summaries
- overlay intersections
- candidate spotlight tables
- per-run JSON summaries
- phenotype-scoped semantic overlay compatibility
- deterministic sample-to-gene aggregation
- explainable semantic contextualization

from completed VAP runs without manual grep/probe workflows.

The resulting outputs should support claims that VAP produces:

- stable biological-output structures
- reproducible candidate evidence streams
- overlay-ready gene-level summaries
- downstream VDB/RDGP/GSC substrate

without making clinical or causal claims.

---

## Release Relevance

This module directly supports VAP v1 release readiness by turning completed production runs into reusable evidence artifacts.

It helps VAP communicate:

```text
how fast it runs
how reproducibly it runs
what biological evidence structures it produces
how those structures can support downstream ecosystem workflows
```

This is central to the performance and reproducibility identity of VAP v1.

This harvesting layer also establishes the first operational VAP → GSC semantic contextualization bridge within the VitamOrdinatio ecosystem.

> This harvesting layer intentionally stops short of acting as a persistent evidence warehouse, which falls under the purview of the VDB (variant_database) repository.

> Long-term persistence, query authority, and cross-run evidence centralization are expected to become responsibilities of future VDB infrastructure.

VAP contributes:
sample-specific observed variant evidence

GSC contributes:
phenotype-scoped semantic priors

Together they enable:
biologically contextualized candidate evidence generation suitable for future VDB persistence and RDGP prioritization workflows.

---