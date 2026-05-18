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

## `interpretation_label_summary.tsv`

### Purpose

Summarizes how VAP-organized biological evidence is distributed across interpretation categories and evidence-origin pathways.

### Highlights

Tracks:

- coding vs noncoding interpretation-origin distributions
- interpretation-label class structure
- retained low-support evidence distributions
- rare candidate evidence structures
- deterministic interpretation reproducibility across reruns

### Why It Matters

Demonstrates:

- biologically structured evidence organization
- stable interpretation-layer reproducibility
- separation of evidence-routing pathways
- preservation of interpretation lineage
- lightweight Stage 13-derived biological abstraction harvesting

This table summarizes VAP interpretation ontology rather than raw molecular consequence ontology.

The `summary_axis` field distinguishes between:

- `source_interpretation_label`
- `variant_origin`

summary categories.

`variant_origin` represents the interpretation pathway through which evidence flowed within VAP:

- `coding`
  - evidence interpreted through the Stage 09 coding interpretation framework
- `noncoding`
  - evidence interpreted through the Stage 10 noncoding interpretation framework

This distinction preserves interpretation lineage and supports future extensibility of downstream interpretation systems.

Examples of future noncoding-oriented interpretation extensions could include:
- AlphaGenome
- SpliceAI
- regulatory-impact modeling
- chromatin-aware interpretation workflows

This table should not be interpreted as direct pathogenicity classification or diagnostic interpretation output.

Instead, it documents how VAP organizes and preserves biologically contextualized evidence substrate across distinct interpretation pathways.

---

## `gene_burden_summary.tsv.gz`

---

## `gene_burden_summary.tsv.gz`

### Purpose

Summarizes deterministic per-gene retained variant burden across harvested VAP runs using Stage 11 gene-count outputs.

### Highlights

Tracks:

- per-gene retained variant burden
- gene burden rank within each run
- resolved vs unresolved gene identifier status
- cross-run burden reproducibility
- WGS vs WES substrate-retention differences

### Why It Matters

This table documents how VAP-retained evidence distributes across gene-associated and unresolved-gene substrate after Stage 11 interpretation convergence.

VAP intentionally preserves broad genomic substrate rather than aggressively filtering to exon-only or frequency-restricted calls.

This design favors:

```text
reversible downstream interpretation
```

over:

```text
irreversible early information loss
```

This is especially important for WGS runs, where large noncoding and unresolved-gene burden is biologically expected because most human genomic sequence is noncoding and regulatory interpretation remains an evolving frontier.

The full uncompressed TSV is ignored by Git, while the compressed .tsv.gz version is retained as the versioned artifact.

---

## `run_reproducibility_summary.tsv`

### Purpose

Summarizes cross-run reproducibility of harvested biological evidence structures across developmental-era, metadata-transition, and telemetry-era VAP executions.

### Highlights

Tracks reproducibility agreement across:

- prioritization structure
- validation/reviewability structure
- interpretation-layer structure
- gene-burden structure

### Why It Matters

This table evaluates whether VAP preserves stable biological evidence organization across reruns and infrastructure evolution events.

The current comparisons include:

- developmental-era vs telemetry-era HG002 execution
- metadata-normalization reruns
- same-patch telemetry-era reruns

Importantly, reproducibility assessment is based on:

```text
semantic biological payload equality
```

rather than raw row equality.

This means comparisons intentionally ignore:
- run identifiers
- provenance metadata
- execution annotations
- run classification labels

and instead focus on whether the underlying biological evidence structures remained stable.

Examples of compared biological abstractions include:

- priority-tier distributions
- reviewability summaries
- interpretation-label distributions
- gene-burden structure

### Reproducibility Status Categories

- `reproducible`
  - biological evidence structures matched completely
- `reproducible_with_provenance_evolution`
  - biological evidence structures matched while provenance metadata evolved
- `biological_divergence_detected`
  - biological evidence structures diverged between compared runs

### Important Scope Boundary

This table documents:

```text
deterministic evidence-organization reproducibility
```

It does NOT evaluate:
- clinical concordance
- causal inference
- phenotype matching
- molecular mechanism
- diagnostic interpretation

Instead, it assesses whether VAP consistently organizes retained evidence substrate across reruns and infrastructure transitions.

---

---

## `coding_noncoding_consequence_summary.tsv`

### Purpose

Summarizes Stage 09 coding interpretation abstractions and Stage 10 noncoding interpretation abstractions across harvested VAP runs.

### Highlights

Tracks:

- coding functional-impact structure
- noncoding contextual structure
- interpretation-label distributions
- rarity classifications
- clinical-support classifications
- coding vs noncoding substrate asymmetry

### Why It Matters

This table exposes how VAP separates:

```text
coding interpretation workflows
```

from:

```text
noncoding interpretation workflows
```

during interpretation convergence.

Coding-oriented summaries include examples such as:
- missense
- synonymous
- loss_of_function
- splice_relevant

Noncoding-oriented summaries include examples such as:
- intergenic
- intronic
- proximal
- transcript_associated

This distinction is important because future interpretation systems may evolve differently for coding and noncoding genomic substrate.

The table also highlights expected differences between:
- WGS substrate retention
- and WES substrate retention

where WGS runs naturally preserve substantially larger noncoding evidence space.

### Important Scope Boundary

This table summarizes:

```text
deterministic evidence organization and interpretation abstraction
```

It does NOT:
- perform phenotype matching
- assign pathogenicity
- establish causality
- provide clinical diagnosis

Instead, it documents how retained genomic substrate is partitioned and interpreted within current VAP interpretation frameworks.

---

---

## `variant_consequence_summary.tsv`

### Purpose

Summarizes molecular and contextual consequence composition across harvested VAP runs.

### Highlights

Tracks:

- coding molecular consequence classes
- noncoding contextual consequence classes
- WGS vs WES substrate differences
- coding/noncoding asymmetry
- reproducibility of consequence composition across reruns

### Why It Matters

This table provides a compact biological view of retained VAP substrate.

Coding consequences include categories such as:

- missense
- synonymous
- loss_of_function
- splice_relevant
- other_coding

Noncoding contextual categories include:

- intergenic
- intronic
- proximal
- transcript_associated
- regulatory
- unknown

This table helps distinguish molecular/contextual substrate composition from downstream prioritization, clinical annotation, or reviewability status.

It should not be interpreted as pathogenicity classification or clinical interpretation output.

---

---

## `gene_list_overlay_intersections.tsv`

### Purpose

Summarizes deterministic intersections between retained VAP gene-burden substrate and curated biological gene-list overlays.

### Current Overlay Sources

Current curated overlays include:

- `mitocarta`
- `epi25_all_epilepsy`

Both overlays use curated Ensembl gene identifiers to support deterministic matching against VAP-retained gene burden.

### Highlights

Tracks:

- overlay-hit genes
- overlay source membership
- overlay source combinations
- retained variant burden
- burden rank within each run
- mitochondrial vs epilepsy-associated overlap structure

### Why It Matters

This table provides a lightweight biological overlay layer for VAP case studies without requiring full semantic GSC integration.

The current implementation intentionally uses:

```text
Ensembl gene ID ↔ VAP gene_id
```

matching to avoid symbol ambiguity and premature namespace brokerage inside VAP.

Genes may intersect:

- MitoCarta only
- EPI25 only
- both overlays simultaneously

The dual-hit category may be biologically interesting because it represents overlap between:

- mitochondrial biology
- and epilepsy-associated loci


### Important Scope Boundary

This table is not a semantic prioritization engine.

It does NOT:

- assign pathogenicity
- perform phenotype matching
- rank causal genes
- establish disease association

Instead, it documents deterministic overlap between retained VAP substrate and curated biological gene lists.

---

---

## `overlay_gene_coding_clinical_evidence.tsv`

### Purpose

Summarizes clinical-evidence abstraction profiles for coding variants retained within curated overlay-hit genes.

### Current Overlay Sources

Current overlays include:

- `mitocarta`
- `epi25_all_epilepsy`

Overlay matching is performed deterministically using:

```text
overlay ensembl_gene_id ↔ VAP gene_id
```

### Highlights

Tracks:

- coding clinical-evidence structure
- overlay-hit gene interpretation context
- clinical annotation sparsity
- overlay-specific clinical-support distributions
- mitochondrial vs epilepsy-associated coding evidence patterns

### Why It Matters

This table documents the current clinical annotation landscape for coding variants retained within biologically curated overlay genes.

Clinical-evidence categories may include examples such as:

- missing
- supported
- benign
- likely_benign
- uncertain

Importantly, large missing categories are biologically expected because VAP intentionally preserves broad coding substrate rather than aggressively filtering to previously curated clinical variants only.

This table therefore helps distinguish:

```text
retained biological substrate
```

from:

```
currently clinically annotated substrate
```

### Important Scope Boundary

This table does NOT:

- establish diagnosis
- assign pathogenicity
- perform phenotype matching
- rank causal genes

Instead, it summarizes current clinical annotation context for retained coding substrate within curated overlay-hit genes.

---

## `overlay_gene_coding_frequency_profiles.tsv`

### Purpose

Summarizes population-frequency abstraction profiles for coding variants retained within curated overlay-hit genes.

### Current Overlay Sources

Current overlays include:

- `mitocarta`
- `epi25_all_epilepsy`

Overlay matching is performed deterministically using:

```text
overlay ensembl_gene_id ↔ VAP gene_id
```

### Highlights

Tracks:

coding rarity structure
common vs rare retained coding substrate
overlay-aware frequency distributions
mitochondrial vs epilepsy-associated coding frequency patterns

### Why It Matters

This table documents the population-frequency landscape for retained coding variants located within curated overlay-hit genes.

Frequency-oriented abstraction categories may include examples such as:

- `common`
- `rare`
- `missing`

The table is intentionally based on frequency abstraction rather than raw allele-frequency values to maintain compact and interpretable biological summaries.

Importantly, VAP intentionally preserves:

- common variation
- rare variation
- and sparsely annotated variation

rather than aggressively filtering retained substrate during early interpretation stages.

This helps distinguish:

```text
overall retained coding substrate
```

from:

```text
rare coding substrate within biologically relevant loci.
```

### Important Scope Boundary

This table does NOT:

- assign pathogenicity
- establish disease causality
- perform burden testing
- rank candidate genes

Instead, it summarizes retained coding population-frequency structure within curated overlay-hit genes.

---

## `overlay_gene_coding_functional_impact.tsv`

### Purpose

Summarizes coding functional-impact abstraction profiles for variants retained within curated overlay-hit genes.

### Current Overlay Sources

Current overlays include:

- `mitocarta`
- `epi25_all_epilepsy`

Overlay matching is performed deterministically using:

```text
overlay ensembl_gene_id ↔ VAP gene_id
```

### Highlights

Tracks:

- coding functional-impact structure
- overlay-aware coding impact distributions
- mitochondrial vs epilepsy-associated coding impact patterns
- loss-of-function vs synonymous vs missense substrate composition

### Why It Matters

This table provides a compact biological summary of retained coding substrate composition within curated overlay-hit genes.

Functional-impact categories may include examples such as:

- missense
- synonymous
- loss_of_function
- splice_relevant
- other_coding

The table intentionally uses:

```text
functional_impact
```

rather than highly granular raw VEP consequence categories in order to preserve:

- readability
- compactness
- and biological interpretability.

This table therefore helps characterize:

```text
what kinds of coding variants exist within biologically relevant loci.
```

### Important Scope Boundary

This table does NOT:

- establish pathogenicity
- assign clinical significance
- rank causal variants
- perform phenotype prioritization

Instead, it summarizes retained coding functional-impact structure within curated overlay-hit genes.

---

## `clinical_status_summary.tsv`

### Purpose

Summarizes the global clinical-annotation landscape across retained coding substrate harvested from Stage 09 interpretation outputs.

### Highlights

Tracks:

- coding clinical-evidence distributions
- coding clinical-status distributions
- global retained coding annotation structure
- clinically supported vs sparsely annotated coding substrate
- reproducibility of coding annotation landscapes across reruns

### Why It Matters

This table provides a compact global view of the retained coding clinical-annotation landscape within VAP.

Clinical categories may include examples such as:

- `missing`
- `benign`
- `likely_benign`
- `uncertain`
- `conflicting`
- `likely_pathogenic`
- `pathogenic`

Importantly, large `missing` categories are biologically expected because VAP intentionally preserves broad coding substrate rather than filtering exclusively to previously curated clinical variants.

This table therefore helps distinguish:

```text
retained coding substrate
```

from:

```text
currently clinically annotated coding substrate.
```

### Important Scope Boundary

This table does NOT:

- establish diagnosis
- assign causality
- perform phenotype prioritization
- rank candidate genes

Instead, it summarizes the current clinical annotation landscape across globally retained coding substrate.

---