# WES / WGS Comparative Experimental Design

## Document Status

- **Purpose:** Define the comparative design for genotype-aware epilepsy WES and WGS analysis using VAP
- **Target location:** `docs/design/wes_wgs_comparative_experimental_design.md`
- **Status:** Comparative experimental design
- **Comparison model:** Distributed, node-local analysis with schema-matched lightweight extraction

## Purpose

This experiment compares the behavior of the Variant Annotation Pipeline (VAP) across whole-exome sequencing (WES) and whole-genome sequencing (WGS) epilepsy substrates.

The objective is not to estimate clinical diagnostic yield. It is to determine whether one genotype-aware VAP architecture can preserve coherent evidence across different genomic search spaces while maintaining deterministic execution, genotype-aware observations, semantic continuity, provenance, lineage, and TEP-VAP transport fidelity.

## Related Experimental Designs

1. [`wes_epilepsy_experimental_design.md`](./wes_epilepsy_experimental_design.md)
2. [`wgs_epilepsy_experimental_design.md`](./wgs_epilepsy_experimental_design.md)

The WES design describes a depth-stratified 12-sample epilepsy exome corpus. The WGS design describes two affected brothers from a familial epilepsy study. This document defines how those corpora will be compared.

## Source Corpora

### WES corpus

- **BioProject:** `PRJEB57558`
- **Sequencing strategy:** Paired-end human WES
- **Selected specimens:** 12 epilepsy patients
- **Execution node:** sys76
- **VAP generation:** Genotype-aware
- **TEP-VAP status:** Full 12-member genotype-aware corpus available
- **Depth categories:** q1 highest read counts; median intermediate; q3 lowest read counts

| SRA | Run ID | Depth Category |
|---|---|---|
| `ERR10619203` | `run_2026_07_15_204807` | q3 |
| `ERR10619207` | `run_2026_07_16_021033` | q3 |
| `ERR10619208` | `run_2026_07_16_055657` | median |
| `ERR10619212` | `run_2026_07_15_105505` | q1 |
| `ERR10619225` | `run_2026_07_15_164104` | q3 |
| `ERR10619230` | `run_2026_07_16_122454` | q3 |
| `ERR10619241` | `run_2026_07_16_161908` | q1 |
| `ERR10619281` | `run_2026_07_16_215236` | median |
| `ERR10619285` | `run_2026_07_17_015849` | median |
| `ERR10619300` | `run_2026_07_14_114546` | median |
| `ERR10619309` | `run_2026_07_17_065031` | q1 |
| `ERR10619330` | `run_2026_07_17_115119` | q1 |

Representative certified WES TEP-VAP subset:

| SRA | Run ID | Depth Category |
|---|---|---|
| `ERR10619212` | `run_2026_07_15_105505` | q1 |
| `ERR10619300` | `run_2026_07_14_114546` | median |
| `ERR10619225` | `run_2026_07_15_164104` | q3 |

### WGS corpus

- **BioProject:** `PRJNA695560`
- **Sequencing strategy:** Paired-end human WGS
- **Study:** *Whole-Genome Sequencing in Two Brothers with Epilepsy*
- **Execution node:** MARK
- **VAP generation:** Genotype-aware
- **Biological design:** Two affected brothers from a consanguineous family

| SRA | Run ID | Notes | Status |
|---|---|---|---|
| `SRR13573587` | `run_2026_07_29_123020` | affected brother WGS | complete |
| `SRR13573588` | `run_2026_08_01_092338` | affected brother WGS | complete |

The associated publication provides a publication-informed concordance target centered on `CNTNAP2`. This is not a formal truth-set benchmark.

## Distributed Comparison Model

```text
sys76
    12 genotype-aware WES runs
        ↓
node-local extraction
        ↓
compact WES comparison package

MARK
    2 genotype-aware WGS runs
        ↓
node-local extraction
        ↓
compact WGS comparison package

SAGE-VAP
    schema-matched comparison
```

Raw and high-volume production artifacts remain on their original nodes. This avoids unnecessary reruns, brittle large transfers, duplicated immutable runs, and version drift.

A scientifically controlled comparison requires common meaning, not common storage.

## Experimental Structure

### Study A — Within-WGS sibling comparison

Question:

> How coherently does VAP preserve and surface evidence across two affected brothers sequenced by WGS?

Evaluate:

- total observations;
- shared and private variants;
- genotype concordance;
- shared homozygous rare variants;
- coding, splice, intronic, regulatory, and intergenic surfaces;
- shared genes and reviewability surfaces;
- `CNTNAP2` recovery;
- lineage and TEP-VAP preservation;
- run-level operational behavior.

The siblings must not be treated as independent population replicates. Shared ancestry and consanguinity are expected to increase overlap.

### Study B — Within-WES depth-stratified comparison

Question:

> Under genotype-aware VAP, how stable are WES evidence surfaces across q1, median, and q3 read-count strata?

Evaluate observation counts, genotype completeness, semantic routing, coding and splice surfaces, reviewability density, clinical annotation retention, preservation behavior, TEP-VAP consistency, and depth-stratum stability.

This analysis uses the genotype-aware sys76 corpus, not the legacy pre-genotype-aware MARK WES runs.

### Study C — Cross-modality comparison

Question:

> How does VAP behave when the assay changes from exome capture to whole-genome sequencing while the evidence model remains genotype-aware and preservation-governed?

Evaluate expansion of noncoding evidence, coding evidence stability, genotype-aware routing, observation density, semantic-surface density, preservation invariants, lineage integrity, TEP-VAP behavior, and modality-specific evidence growth.

## Comparability Gate

No cross-modality inference should be made until the WES and WGS corpora pass a compatibility audit.

Required comparisons:

```text
VAP commit or release
configuration schema version
reference assembly
reference FASTA identity
alignment software and version
variant caller and version
normalization policy
VEP version
VEP cache or resource version
transcript-selection policy
population annotation resources
clinical annotation resources
genotype-observation schema
routing policy
semantic field definitions
TEP-VAP builder version
TEP-VAP validation version
```

Expected modality-specific differences include WES capture intervals and WGS genome-wide callable territory. The design must distinguish shared analytical invariants from intentional modality-specific settings.

## Node as an Experimental Factor

WES resides on sys76 and WGS resides on MARK.

For biological and semantic comparisons, node should be non-influential if software, resources, schemas, and deterministic execution are controlled.

For runtime and performance comparisons, node is a confounder. Observed runtime, I/O, memory, and storage may be reported, but should not be attributed solely to modality without hardware normalization.

## Two-Phase SAGE-VAP Review

### Phase 1 — Lightweight harvested evidence

SAGE-VAP will inspect compact artifacts transferred from each node.

Likely evidence:

- run metadata;
- configuration snapshots;
- stage summaries;
- row and column inventories;
- genotype summaries;
- coding/noncoding summaries;
- consequence summaries;
- frequency summaries;
- clinical summaries;
- reviewability summaries;
- validation reports;
- entity inventories;
- lineage manifests;
- TEP-VAP summaries;
- telemetry summaries;
- compact candidate slices;
- targeted `CNTNAP2` traces.

Phase 1 establishes corpus identity, schema compatibility, configuration compatibility, high-level scientific behavior, comparison feasibility, and targeted node-local queries.

### Phase 2 — Targeted full-run probes

High-cardinality questions will be answered through node-local probes.

Examples:

- exact sibling-shared and private variant sets;
- shared homozygous rare variants;
- genotype concordance;
- `CNTNAP2` stage trace;
- callable territory;
- exact WES/WGS gene overlap;
- variant-level lineage;
- rare noncoding convergence;
- routing-overlap topology;
- random and edge-case variant traces;
- raw-to-TEP source fidelity.

SAGE-VAP defines the scientific question. DEX-VAP or a probe script extracts the answer on the node containing the immutable full run. Only compact probe outputs are transferred.

## Common Comparison Artifact Contract

The same extraction code and output schemas should be used on sys76 and MARK.

Corpus-level artifacts:

```text
comparison_corpus_manifest.tsv
comparison_environment_audit.tsv
comparison_resource_identity_audit.tsv
comparison_schema_compatibility.tsv
```

WES outputs:

```text
wes_run_summary.tsv
wes_observation_class_summary.tsv
wes_genotype_summary.tsv
wes_consequence_summary.tsv
wes_frequency_summary.tsv
wes_clinical_summary.tsv
wes_reviewability_summary.tsv
wes_preservation_summary.tsv
wes_gene_surface_summary.tsv
wes_tep_summary.tsv
```

WGS outputs:

```text
wgs_run_summary.tsv
wgs_observation_class_summary.tsv
wgs_genotype_summary.tsv
wgs_consequence_summary.tsv
wgs_frequency_summary.tsv
wgs_clinical_summary.tsv
wgs_reviewability_summary.tsv
wgs_preservation_summary.tsv
wgs_gene_surface_summary.tsv
wgs_tep_summary.tsv
```

Corresponding WES and WGS files must use identical schemas.

## Metric Families

### Operational metrics

- input and aligned read counts;
- alignment rate;
- runtime and stage durations;
- peak memory;
- disk usage;
- failure or retry behavior;
- TEP-VAP size.

Interpret with node context.

### Observation metrics

- total rows;
- unique variant IDs;
- SNV and indel counts;
- genotype completeness;
- heterozygous and homozygous-alternate counts;
- missing genotype states;
- multi-allelic handling;
- allele-balance summaries where available.

### Genomic-territory metrics

- coding;
- splice;
- intronic;
- UTR;
- promoter;
- regulatory;
- intergenic;
- other noncoding;
- unknown or unclassified.

### Frequency and clinical metrics

- rare;
- common;
- frequency unknown;
- ClinVar pathogenic;
- ClinVar likely pathogenic;
- ClinVar VUS;
- ClinVar benign or likely benign;
- unannotated clinical state.

### Semantic-surface metrics

- coding interpretation surface;
- noncoding interpretation surface;
- splice overlay;
- VAP reviewability tiers;
- semantic escalation surfaces;
- validation-routing states;
- preserved background evidence;
- unresolved evidence states.

### Preservation metrics

- Stage07 observation count;
- Stage08 identity parity;
- downstream variant-universe preservation;
- candidate-collapse prevention;
- lineage completeness;
- entity-role completeness;
- source-to-TEP checksum fidelity;
- validation status;
- provenance completeness.

### Cross-sample metrics

WES:

- within- and across-depth-stratum stability;
- recurrent genes;
- recurrent consequence classes;
- recurrent reviewability states.

WGS:

- sibling-shared and private variants;
- shared rare homozygous variants;
- shared genes;
- shared reviewability surfaces;
- `CNTNAP2` concordance.

Cross-modality:

- shared coding and splice genes;
- consequence-class overlap;
- clinically annotated gene overlap;
- reviewability-surface overlap;
- modality-specific evidence expansion.

## Absolute and Normalized Reporting

Raw counts alone are insufficient. WGS is expected to produce many more variants, substantially more noncoding observations, larger TEP-VAP artifacts, and longer execution time.

The study must report both absolute counts and normalized densities or proportions.

Potential denominators include:

- callable megabases;
- covered coding megabases;
- aligned reads;
- million observations;
- million variant IDs;
- TEP bytes per million observations;
- runtime per million observations.

No universal denominator should be used for every metric. Biological density should generally use callable or interrogated territory. Operational density may use reads, observations, or processed bytes.

## Primary Scientific Questions

1. Does genotype-aware VAP preserve deterministic evidence across WES and WGS?
2. Does WGS expand noncoding evidence without disrupting coding evidence preservation?
3. Are genotype states represented coherently across modalities?
4. Does Stage07-to-Stage08 preservation remain stable?
5. Are routing semantics maintained under WGS-scale complexity?
6. Are coding reviewability surfaces stable after normalization?
7. How does the noncoding evidence fraction change?
8. Are provenance and lineage equally reconstructable?
9. Does TEP-VAP transport remain lossless across modalities?
10. Can the WGS corpus recover and preserve the publication-reported `CNTNAP2` signal?
11. Are sibling-shared rare homozygous structures recoverable?
12. Which observed differences are modality-driven versus node- or configuration-driven?

## Working Hypotheses

```text
WGS will substantially expand noncoding evidence.

Coding evidence density may remain comparatively stable
when normalized to callable coding territory.

Genotype-aware routing will remain coherent across modalities.

Preservation invariants will remain stable.

WGS TEP-VAP size will increase substantially.

Lineage and provenance completeness will not degrade.

The WGS sibling pair will share substantial rare
homozygous variation because of family structure
and consanguinity.

CNTNAP2 evidence will remain recoverable and traceable
whether or not it enters the highest VAP reviewability tier.
```

These are testable expectations, not predetermined conclusions.

## Publication-Informed Concordance

The WGS publication identifies `CNTNAP2` as a candidate signal.

The study should inspect whether the variant is present, whether genotype state is preserved, whether transcript and gene context are retained, whether frequency annotation is coherent, whether routing is explainable, whether reviewability state is explainable, and whether the observation survives TEP-VAP emission.

The publication is not a formal truth set. Failure to reach a high reviewability tier does not by itself indicate pipeline failure.

## Scientific Boundaries

This study must not be described as:

- a population-level WES/WGS diagnostic-yield comparison;
- a case-control study;
- a burden or association analysis;
- independent causal validation of `CNTNAP2`;
- a representative estimate of all epilepsy genomes.

Reasons include unequal sample sizes, unrelated WES participants versus related WGS siblings, different BioProjects and ascertainment, different sequencing designs, different compute nodes, family structure and consanguinity, and lack of unaffected WGS family controls.

The study may validly evaluate VAP execution behavior, evidence preservation, semantic-surface behavior, genotype-aware architecture, WES/WGS substrate differences, and TEP-VAP continuity.

## Success Criteria

The experiment succeeds when:

- both corpora pass the compatibility gate;
- common schemas are confirmed;
- node-local extraction is reproducible;
- no unexplained evidence loss is detected;
- genotype-aware observations remain first-class;
- routing semantics remain coherent;
- WGS-specific evidence expansion is interpretable;
- coding evidence remains recoverable;
- reviewability surfaces remain bounded;
- lineage and provenance remain complete;
- TEP-VAP emission remains lossless;
- sibling-level WGS comparisons are reconstructable;
- `CNTNAP2` can be traced and explained;
- Phase 1 and Phase 2 findings agree where they overlap.

## Intended Scientific Description

> A distributed, genotype-aware comparison of epilepsy whole-exome and whole-genome VAP evidence surfaces, evaluating cross-modality preservation, semantic routing, lineage continuity, and reviewability under controlled extraction and node-local full-run audit.

It should not be described as a clinical diagnostic-yield comparison.

## Final Experimental Principle

```text
Common scientific meaning
is more important than
common physical storage.
```

The comparison therefore uses:

```text
genotype-aware WES on sys76
+
genotype-aware WGS on MARK
+
shared extraction contracts
+
compatibility audits
+
targeted node-local probes
```

This design preserves immutable production corpora while enabling rigorous cross-modality analysis without unnecessary reruns or high-volume transfer.
