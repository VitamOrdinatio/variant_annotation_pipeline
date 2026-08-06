# Genotype-Aware WES/WGS Execution-Provenance Certification

| Field | Value |
|---|---|
| Document status | Draft v0.1 |
| Governing agent | SAGE-VAP |
| Evidence acquisition agent | DEX-VAP |
| Producer system | Variant Annotation Pipeline (VAP) |
| Transport package | TEP-VAP |
| WES certification corpus | 12 genotype-aware epilepsy WES runs on sys76 |
| WGS certification corpus | 2 genotype-aware epilepsy WGS runs on MARK |
| Comparative certification object | Certified sys76 WES corpus versus certified MARK WGS corpus |
| Scientific domain | Evidence preservation, genotype observation, execution provenance, lineage, transport fidelity, and cross-modality coherence |
| Clinical status | Research and portfolio validation only; not clinical validation |

---

## 1. Purpose

This document defines the production and corpus-level scientific certification
framework for genotype-aware, execution-provenance-enabled VAP runs across:

```text
12 epilepsy WES executions on sys76

2 affected-sibling epilepsy WGS executions on MARK

and

a controlled comparison between the independently certified WES and WGS corpora
```

The framework activates the production validation layers that were explicitly
deferred by the initial genotype observation validation strategy.

It governs three separate certification objects:

```text
Certification A
    sys76 genotype-aware WES execution-provenance corpus
    n = 12

Certification B
    MARK genotype-aware WGS execution-provenance corpus
    n = 2

Certification C
    certified sys76 WES corpus
        versus
    certified MARK WGS corpus
```

The purpose is not to prove that every run is numerically identical, nor to
force WES and WGS into one biological search space.

The purpose is to determine whether VAP:

- executes under reconstructable and internally coherent provenance;
- surfaces genotype information as a first-class observation domain;
- preserves Stage 07 biological observations and downstream semantic overlays;
- transports run-local evidence into TEP-VAP without mutation or unexplained loss;
- behaves coherently across multiple WES executions and two WGS executions;
- supports scientifically defensible comparison across assay modalities and execution nodes;
- preserves publication-relevant and publication-expanding evidence without treating the publication as a truth set.

This document defines what must be demonstrated before SAGE-VAP may issue a
per-run, corpus-level, or cross-modality certification.

It does not prescribe one implementation of the extractor or probe utilities.
DEX-VAP may choose the implementation so long as the required evidence is
produced deterministically, auditably, and without modifying canonical VAP
artifacts.

---

## 2. Relationship to Existing Validation and Certification Documents

This document extends rather than replaces the existing VAP validation system.

```text
Architecture and scientific doctrine
        ↓
Design, specification, and schema
        ↓
Genotype unit and fixture validation
        ↓
Single-run production certification
        ↓
Multi-run corpus certification
        ↓
Certified WES/WGS comparative certification
```

### 2.1 Governing validation documents

This framework inherits the validated logic in:

- [Genotype Observation Validation](./genotype_observation_validation.md)
- [Sidecar Telemetry](./sidecar_telemetry.md)
- [VAP → VDB Architecture Walkthrough](./vap_to_vdb_architecture_walkthrough.md)
- [Validation Comparisons](./comparisons/README.md)

It also depends upon the governing producer contracts and design documents,
including:

- [Execution Provenance Contract](../contracts/system/core/execution_provenance_contract.md)
- [Genotype Observation Contract](../contracts/system/core/genotype_observation_contract.md)
- [VAP-TEP Preservation Contract](../contracts/system/core/vap_tep_contract.md)
- [Genotype Observation Design](../design/genotype_observation_design.md)
- [VAP Preservation Mission](../design/vap_preservation_mission.md)
- [VAP-TEP Preservation Brief](../design/vap_tep_preservation_brief.md)
- [VAP-TEP Preservation Lineage Model](../design/vap_tep_preservation_lineage_model.md)
- [Multiallelic Relationships VAP Handling Policy](../design/multiallelic_relationships_vap_handling_policy.md)
- [WES Epilepsy Experimental Design](../design/wes_epilepsy_experimental_design.md)
- [WGS Epilepsy Experimental Design](../design/wgs_epilepsy_experimental_design.md)
- [WES/WGS Comparative Experimental Design](../design/wes_wgs_comparative_experimental_design.md)
- [Completed Epilepsy Runs Ledger](../status/completed_epilepsy_runs_ledger.md)

### 2.2 Certified production exemplar

The current gold-standard production precedent is:

- [SAGE Scientific Certification of the Modernized VAP Producer Substrate](./comparisons/err10619300_genotype_elevation_validation/sage_modernized_vap_producer_substrate_certification.md)

That certification established:

```text
sample = ERR10619300
run = run_2026_07_14_114546
node = sys76
TEP-VAP = vap_tep_ERR10619300_run_2026_07_14_114546_v1
outcome = CERTIFIED WITH NOTES
```

It certified the modernized producer substrate as empirically instantiated by
one complete genotype-aware WES production run.

It did not certify:

```text
all 12 genotype-aware WES executions
both genotype-aware WGS executions
cross-node determinism
cross-modality scientific comparison
```

Accordingly, this document generalizes the certified single-run evidence model
into an all-member corpus framework.

### 2.3 Authority rule

If a production artifact conflicts with certified architecture, design,
specification, schema, or preservation doctrine, the certified documentation is
authoritative until the discrepancy is resolved through controlled governance.

Certification shall not silently redefine producer semantics to accommodate a
convenient artifact shape.

---

## 3. Scientific Certification Doctrine

### 3.1 Preservation doctrine

VAP exists to surface and preserve biological evidence.

Stage 07 is the authoritative biological observation anchor.

Downstream stages may organize, interpret, prioritize, validate, or summarize
evidence, but they must not erase or redefine the original observation state.

### 3.2 Genotype observation doctrine

Genotype observations are first-class producer evidence.

They must preserve source genotype context without fabricating unsupported
inheritance or biological conclusions.

VAP may preserve:

```text
GT
AD
DP
GQ
PL
FT
FORMAT context
phase state
called allele indices
source-record identity
relationship status
```

VAP does not infer, merely from genotype projection:

```text
inheritance mode
carrier status
compound heterozygosity
de novo status
hemizygosity
heteroplasmy
negative evidence
callability
disease causality
diagnosis
```

### 3.3 Execution-provenance doctrine

Execution provenance is a first-class producer context domain.

It is not biological evidence, but it is required to determine how biological
evidence was generated.

Execution provenance must be resolved early enough to act as an execution
precondition rather than a retrospective narrative.

The current implementation distinguishes:

```text
metadata/execution_provenance.json
    runtime and resource provenance receipt

metadata/config_snapshot.yaml
    execution configuration snapshot
```

Both artifacts must remain bound to the run and must be transported into
TEP-VAP without mutation.

### 3.4 Transport doctrine

TEP-VAP transports producer-authored evidence.

It does not reinterpret evidence.

Processed artifacts and their transported TEP counterparts must remain
byte-identical where the transport contract requires direct preservation.

### 3.5 Producer-consumer authority

```text
VAP
    preserves observations and producer-authored semantic states

TEP-VAP
    transports those states

VDB
    validates, brokers namespaces additively, relates, and persists

RDGP
    performs downstream statistical, phenotype, and inheritance reasoning
```

Certification must not require VAP to fabricate VDB or RDGP conclusions.

### 3.6 Certification is multidimensional

A single validator result is not equivalent to scientific certification.

The following determinations must remain distinguishable:

```text
operational completion
source-state traceability
execution-provenance completeness
genotype observation integrity
Stage 07 preservation
semantic overlay coherence
TEP transport fidelity
inventory and lineage integrity
scientific sanity
corpus comparability
cross-modality interpretability
```

A run may be operationally complete but scientifically uncertifiable if the
required evidence cannot be reconstructed.

### 3.7 Per-run certification precedes corpus certification

Every corpus member must receive an explicit per-run determination.

Representative runs may support high-cost architectural or scientific probes,
but representative success does not automatically certify unreviewed members.

### 3.8 Corpus certification precedes comparative certification

Certification C may begin only after Certifications A and B have reached a
usable frozen state.

An uncertified source corpus cannot be repaired by a favorable comparative
summary.

---

## 4. Roles and Decision Authority

### 4.1 SAGE-VAP responsibilities

SAGE-VAP owns:

- certification question formulation;
- evidence-class definition;
- scientific acceptance boundaries;
- normalization and comparison rules;
- classification of findings as blocking, advisory, unresolved, or out of scope;
- requests for targeted follow-up probes;
- per-run certification decisions;
- corpus-level certification decisions;
- cross-modality certification decisions;
- scientific limitations and revalidation triggers.

### 4.2 DEX-VAP responsibilities

DEX-VAP owns:

- implementation or execution of lightweight extractors;
- node-local inspection of large production artifacts;
- deterministic evidence gathering;
- checksum and identity calculations;
- generation of compact audit tables and receipts;
- execution of targeted probes requested by SAGE-VAP;
- preservation of source paths, run identities, tool versions, and evidence lineage;
- correction of extractor defects without modifying canonical biological outputs.

DEX-VAP does not decide scientific certification status.

### 4.3 Iterative review loop

```text
SAGE-VAP
    defines what must be demonstrated
        ↓
DEX-VAP
    extracts evidence and executes bounded probes
        ↓
SAGE-VAP
    evaluates evidence and identifies unresolved questions
        ↓
DEX-VAP
    performs targeted follow-up investigation
        ↓
SAGE-VAP
    certifies, certifies with notes, withholds certification,
    or rejects the certification object
```

The loop continues until each material certification question is either:

```text
resolved
bounded with an explicit limitation
or classified as insufficient evidence
```

---

## 5. Certification Objects

## 5.1 Certification A — sys76 genotype-aware WES corpus

### Corpus identity

| Sample/SRA | Run ID | Read-count stratum |
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

These categories are project-specific, quartile-centered read-count strata:

```text
q1
    higher-read stratum

median
    median-centered stratum

q3
    lower-read stratum
```

They should not be described as measured target coverage unless a coverage
artifact supports that statement.

### Certification objective

Determine whether all 12 sys76 WES executions:

- completed under reconstructable execution provenance;
- emitted valid genotype observation artifacts;
- preserved source genotype semantics;
- transported genotype and provenance artifacts into TEP-VAP faithfully;
- preserved Stage 07 observations and downstream semantic continuity;
- support corpus-level stability across the three read-count strata;
- contain no unresolved member-level failure that invalidates the corpus.

### Existing certified member

`ERR10619300 / run_2026_07_14_114546` is the existing certified production
exemplar.

Its prior certification may be incorporated by reference when:

- the underlying run and TEP artifacts are unchanged;
- the prior evidence bundle remains complete and checksum-stable;
- no governing schema or certification criterion has changed materially.

If any of those conditions fail, the member must be revalidated under the
current framework.

The remaining 11 members require direct evidence review.

## 5.2 Certification B — MARK genotype-aware WGS corpus

### Corpus identity

| Sample/SRA | Run ID | Relationship description |
|---|---|---|
| `SRR13573587` | `run_2026_07_29_123020` | affected sibling WGS |
| `SRR13573588` | `run_2026_08_01_092338` | affected sibling WGS |

The SRA-to-pedigree mapping between these accessions and publication
individuals `V-2` and `V-4` must be established before sample-specific clinical
or pedigree narration.

### Certification objective

Determine whether both MARK WGS executions:

- completed under reconstructable execution provenance;
- emitted valid genotype observation artifacts at WGS scale;
- preserved source genotype and multiallelic context;
- transported genotype and provenance artifacts into TEP-VAP faithfully;
- preserved coding and noncoding evidence without candidate-only compression;
- support defensible sibling-shared and sibling-private evidence summaries;
- preserve a coordinate-anchored and transcript-aware trace of the publication-reported `CNTNAP2` signal;
- permit publication concordance, expansion, or divergence to be described without treating the publication as biological truth.

## 5.3 Certification C — certified WES versus certified WGS

### Comparative object

```text
certified sys76 WES genotype-aware execution-provenance corpus
    n = 12

versus

certified MARK WGS genotype-aware execution-provenance corpus
    n = 2
```

### Certification objective

Determine whether a common genotype-aware VAP architecture preserves coherent,
reconstructable, and scientifically interpretable evidence across WES and WGS
while respecting:

- different genomic search spaces;
- different execution nodes;
- different sample structures;
- modality-specific configurations;
- WGS noncoding expansion;
- the non-independence of the two affected siblings.

Certification C does not estimate diagnostic yield, disease prevalence,
population association, or causal effect.

---

## 6. Evidence Hierarchy

Evidence shall be classified by strength and authority.

### 6.1 Primary evidence

Primary evidence includes:

- immutable run-local artifacts;
- source VCF and annotated VCF identities;
- `metadata/execution_provenance.json`;
- `metadata/config_snapshot.yaml`;
- processed genotype artifacts;
- native TEP-VAP artifacts;
- file hashes and byte-identity comparisons;
- entity inventories;
- lineage manifests;
- TEP validation reports;
- run-external extractor manifests and receipts;
- direct node-local probes over canonical production files.

Primary evidence is authoritative for production certification.

### 6.2 Secondary evidence

Secondary evidence includes:

- sidecar telemetry;
- stage summaries;
- compact run reports;
- direct recounts over extracted lightweight tables;
- schema and distribution summaries;
- deterministic comparison tables.

Secondary evidence can support certification when its source identity and
derivation are explicit.

Reflective telemetry must be labeled as reflective and must not be represented
as an independent semantic recomputation.

### 6.3 Historical and calibration evidence

Historical case studies, HG002 validation artifacts, and pre-genotype-aware WES
runs may provide:

- stage behavior context;
- semantic vocabulary;
- historical reproducibility evidence;
- calibration of expected artifact relationships.

They do not replace direct certification of current genotype-aware runs.

### 6.4 External comparator evidence

The Badshah et al. publication is an independent interpretation over the same
WGS source data.

It may support evaluation of:

```text
publication concordance
publication expansion
publication divergence
```

It is not a formal truth set and is not independent causal validation.

---

## 7. Common Per-Run Certification Evidence

Every WES and WGS run must provide the following common certification surface.

## 7.1 Run, sample, package, and source-state identity

Required fields include:

```text
sample_id or SRA accession
run_id
execution node
assay or modality
source BioProject
VAP implementation identity
run-generating commit or source-state receipt
TEP ID
TEP package version
run completion state
canonical run path
canonical TEP path
critical artifact hashes
```

When a production run was generated from an uncommitted implementation state,
source-state traceability must preserve, where available:

```text
base commit
Git status
tracked working-tree patch
diff summary
untracked path inventory
subsequent committed state
post-commit conformance evidence
```

The evidence must not claim stronger source-byte identity than the receipts
actually establish.

## 7.2 Execution-provenance certification

Required run-local artifact:

```text
metadata/execution_provenance.json
```

Required transported artifact:

```text
entities/context/execution_provenance.json
```

The review must establish:

- artifact presence and readability;
- provenance schema or contract identity;
- contract status;
- provenance completeness status;
- resolution mode;
- host and operating environment identity;
- Python and relevant runtime identities;
- toolchain identities and version policy;
- alignment and variant-calling tool identities;
- annotation engine and cache identities;
- reference assembly;
- reference FASTA identity;
- FASTA index and sequence dictionary identity;
- aligner-index constituent identities where applicable;
- gene-set and annotation-resource identities;
- failed or unresolved provenance surfaces;
- evidence that provenance was resolved before or at the governed execution boundary;
- run-to-provenance binding;
- processed-to-TEP checksum identity;
- inventory and lineage registration.

A provenance artifact that merely exists but contains unresolved required
surfaces is not automatically certifiable.

## 7.3 Configuration-snapshot certification

Required run-local artifact:

```text
metadata/config_snapshot.yaml
```

Required transported artifact:

```text
entities/metadata/config_snapshot.yaml
```

The review must establish:

- artifact presence and readability;
- run-to-configuration binding;
- configuration schema or version where defined;
- modality identity;
- sample identity;
- reference and annotation settings;
- relevant filtering and routing settings;
- genotype projection settings;
- TEP emission settings;
- checksum identity between run-local and TEP copies;
- consistency with the execution-provenance receipt.

Configuration differences are not automatically failures. They must be
classified as intentional, benign, comparison-limiting, or blocking.

## 7.4 Genotype observation certification

Required run-local artifacts:

```text
processed/genotype_observations.tsv
processed/genotype_projection_summary.json
processed/genotype_source_header_context.json
```

Required transported artifacts:

```text
entities/genotype/genotype_observations.tsv
entities/genotype/genotype_projection_summary.json
entities/genotype/genotype_source_header_context.json
```

The review must establish:

- all required artifacts are present and nonempty where scientifically expected;
- schema identity and required column order;
- sample and run identity coherence;
- source VCF identity;
- source header identity;
- source-record count;
- genotype observation row count;
- record and observation reconciliation;
- deterministic genotype observation identities;
- source-record ordinal and hash behavior;
- GT preservation;
- FORMAT and sample-value preservation;
- AD, DP, GQ, PL, FT, and unknown FORMAT-field behavior where emitted;
- complete no-call and partial no-call preservation;
- literal VCF missing-value preservation in raw fields;
- null-token semantics for derived fields;
- GT arity preservation;
- phase-state preservation;
- no unsupported haploid inference from a single-allele call state;
- malformed GT counts;
- FORMAT/sample mismatch counts;
- called allele index range checks;
- projection errors and warnings;
- multiallelic and spanning-deletion relationship status;
- absence of fabricated allele-specific relationships;
- processed-to-TEP byte identity;
- inventory and lineage registration.

Missing genotype values must never be silently converted into homozygous
reference calls.

Complex relationships preserved for VDB mediation are governed advisories, not
producer failures, when source context is complete and the producer does not
fabricate a direct relationship.

## 7.5 Stage preservation and semantic continuity

The review must establish:

- Stage 07 annotated evidence is present and attributable;
- Stage 07 remains the observation anchor;
- Stage 08 partitioning and normalization are additive;
- coding and noncoding partition counts reconcile to the governed universe;
- splice and other routing classes reconcile where applicable;
- Stage 09 coding interpretations remain attributable to source observations;
- Stage 10 noncoding interpretations remain attributable to source observations;
- Stage 11 prioritization remains an overlay;
- Stage 12 validation context remains an overlay;
- unknown, common, unresolved, and noncoding evidence is not silently discarded;
- any row or identity delta is fully enumerated and scientifically classified;
- genotype elevation does not mutate Stages 08–13 outside explicitly governed additions.

Numerical identity between biologically different samples is not expected.
Structural reconciliation and evidence-lineage continuity are required.

## 7.6 TEP-VAP transport certification

The review must establish:

- TEP package identity and version;
- required entity roles are present;
- required transport paths exist;
- transported artifact hashes match source artifacts where direct transport is required;
- `entity_inventory.json` is complete and internally coherent;
- `lineage_manifest.json` is complete and internally coherent;
- `validation_report.md` or equivalent validator receipt is present;
- parent/child lineage edges are reconstructable;
- genotype artifacts are indexed;
- execution provenance is indexed;
- configuration snapshot is indexed;
- producer sample and run identity remain recoverable;
- source paths and checksums remain attributable;
- no unexplained orphan entity exists;
- no candidate-only preservation compression has occurred;
- the Stage 13 self-reference timing artifact, if present, is explicitly classified rather than confused with evidence loss.

A native TEP validator pass is necessary but not sufficient for scientific
certification.

## 7.7 Scientific sanity surface

Each run must provide compact, source-attributable summaries sufficient to
detect silent corruption or gross incoherence.

Recommended classes include:

- source record count;
- genotype observation count;
- called, no-call, and partial-call distributions;
- zygosity or raw GT distributions where defensibly derived;
- phased and unphased distributions;
- ploidy or GT-arity distributions;
- multiallelic and complex-relationship counts;
- coding and noncoding counts;
- consequence distributions;
- frequency-state distributions;
- clinical annotation retention;
- priority-tier and reviewability distributions;
- validation-state distributions;
- gene-surface counts;
- rare and high-impact observation counts;
- bounded representative variant traces.

These summaries are anomaly-detection surfaces. They are not population or
clinical conclusions.

## 7.8 Run-external evidence receipt

Every extraction or probe execution must emit a run-external receipt that
records:

```text
extractor or probe name
implementation version
execution timestamp
execution node
source run path
source TEP path
input file identities
output file identities
output hashes
row counts
warnings
failures
command or invocation identity
```

Evidence generation must not mutate the canonical run or TEP directories.

---

## 8. Per-Run Acceptance Rules

## 8.1 Certification-blocking findings

Unless scientifically resolved, the following are certification-blocking:

- missing or ambiguous sample identity;
- missing or ambiguous run identity;
- absent required execution-provenance artifact;
- failed required provenance surfaces;
- absent required configuration snapshot;
- unexplained provenance/configuration contradiction;
- absent genotype artifact family;
- irreconcilable source-record and genotype-observation counts;
- unbounded projection errors;
- malformed or out-of-range allele indices that compromise evidence identity;
- silent conversion of no-call or partial-call states;
- fabricated direct relationships for ambiguous multiallelic records;
- run-to-TEP sample or run mismatch;
- processed-to-TEP byte-identity failure for direct transport artifacts;
- missing required inventory registration;
- missing required lineage registration;
- unexplained Stage 07 evidence loss;
- candidate-only compression of the preserved observation universe;
- invalid or incomplete TEP acceptance state;
- evidence mutation caused by the certification extractor or probe;
- insufficient source-state traceability for claims being made.

## 8.2 Governed advisories and nonblocking notes

The following may support `CERTIFIED WITH NOTES` when fully bounded:

- multiallelic or spanning-deletion relationships deferred to VDB mediation;
- absent optional FORMAT fields not emitted by the source caller;
- run-specific warning counts with complete source context and no evidence loss;
- benign configuration differences that do not invalidate the certification question;
- Stage 13 artifact-manifest self-reference timing behavior;
- reflective telemetry used only for appropriately limited claims;
- source-state limitations that prevent a stronger claim but do not invalidate the observed production artifacts;
- biological or numerical outliers that remain internally coherent and traceable.

## 8.3 No universal biological count threshold

Certification shall not impose one universal expected number of variants,
genotypes, coding observations, noncoding observations, or prioritized
candidates across all samples.

Count-based anomalies must be evaluated relative to:

- modality;
- available search space;
- configuration;
- source record count;
- cohort distribution;
- read-count stratum;
- callable or interrogated territory where available;
- artifact and lineage integrity.

---

## 9. Certification A — WES-Specific Validation

## 9.1 All-member lightweight certification surface

All 12 WES runs must receive the complete common per-run certification surface.

At minimum, the all-member pass must establish:

```text
run and TEP identity
execution provenance status
configuration snapshot identity
genotype projection status
processed-to-TEP identity
inventory registration
lineage registration
TEP validation status
Stage 07/08 reconciliation
compact semantic and genotype distributions
```

No WES member may be omitted solely because another member in the same stratum
passed.

## 9.2 High-cost representative and anomaly probes

High-cardinality or expensive probes may be concentrated on:

- at least one q1 member;
- at least one median member;
- at least one q3 member;
- the existing certified `ERR10619300` exemplar;
- any statistical or structural outlier;
- any member with a warning, mismatch, unexpected count, or unresolved lineage state.

Representative probes may validate architectural behavior, but every member
must still satisfy the lightweight per-run evidence contract.

## 9.3 Depth-stratum analysis

The WES corpus review should determine:

1. Are genotype observation surfaces structurally stable across q1, median, and q3 read-count strata?
2. Are no-call, partial-call, GQ, DP, and related completeness surfaces plausibly depth-associated?
3. Are coding, splice, noncoding, and semantic routing surfaces preserved across strata?
4. Are reviewability and prioritization structures coherent without requiring numerical identity?
5. Do provenance, lineage, and TEP transport remain complete across all strata?
6. Does any stratum show systematic evidence loss, schema drift, or transport degradation?

Read-count category must not be conflated with measured target coverage unless
coverage measurements are supplied.

## 9.4 WES outlier handling

An outlier is not automatically a failed run.

Each outlier must be classified as one of:

```text
biological/sample-associated
read-count or depth-associated
configuration-associated
execution-associated
artifact-corruption-associated
extractor-associated
unresolved
```

Certification is blocked only when the outlier represents unresolved evidence
loss, invalid provenance, invalid genotype projection, invalid transport, or
another material failure.

## 9.5 WES corpus aggregation

The 12-member WES corpus may be certified only after every member has an
explicit status.

The corpus review must include:

- member status matrix;
- stratum status matrix;
- corpus anomaly register;
- unresolved issue register;
- evidence completeness statement;
- corpus-level scientific limitations;
- revalidation triggers.

---

## 10. Certification B — WGS-Specific Validation

## 10.1 Shared common certification surface

Both WGS runs must satisfy the same common per-run certification evidence
contract used for WES.

Common schemas and field meanings must remain identical unless an intentional
modality-specific extension is explicitly documented.

## 10.2 WGS scale and search-space validation

The review must establish that WGS scale did not cause:

- truncated genotype output;
- silent row loss;
- incomplete TEP packaging;
- incomplete inventory or lineage indexing;
- checksum failure;
- candidate-only preservation;
- unbounded runtime or storage workarounds that altered evidence semantics.

Where available, the evidence package should report:

- source VCF records;
- genotype observations;
- coding and noncoding observations;
- chromosome-level distributions;
- complex and multiallelic relationship counts;
- TEP entity sizes;
- extraction and probe resource footprints.

## 10.3 Sibling-shared and sibling-private evidence

The WGS review should provide bounded, auditable summaries of:

- shared genomic variant identities;
- private variant identities for each sibling;
- shared genotype states;
- discordant genotype states;
- shared rare homozygous observations;
- shared coding candidates;
- shared noncoding candidates;
- genotype and relationship states requiring mediation;
- representative shared and private traces.

The two siblings are related and are not independent biological replicates.

Sibling concordance must not be generalized into population frequency,
prevalence, or association conclusions.

## 10.4 `CNTNAP2` targeted trace

The publication contains inconsistent cDNA expressions for the reported
`CNTNAP2` p.Gly228Arg signal.

The certification trace must therefore anchor on:

```text
reference assembly
chromosome
position
reference allele
alternate allele
gene identity
transcript identity
normalized cDNA HGVS where derivable
protein consequence p.Gly228Arg
source VCF record identity
genotype observation identity
sample genotype state
Stage 07 annotation
Stage 08 routing
Stage 09 or Stage 10 interpretation as applicable
Stage 11 prioritization
Stage 12 validation context
TEP entity identity
lineage path
```

The trace must search transcript-aware and coordinate-aware representations
rather than relying on one publication cDNA string.

The outcome must be classified as:

```text
publication concordance
publication expansion
publication divergence with explanation
or
insufficient evidence
```

Failure to reach the highest VAP priority tier is not automatically a failure
to preserve the signal.

## 10.5 Publication boundary

The WGS certification may assess whether VAP preserves and makes reviewable the
publication-reported signal and additional plausible evidence.

It shall not claim:

- independent causal validation;
- diagnostic confirmation;
- clinical pathogenicity classification;
- family-wide segregation beyond available samples;
- population association;
- disease prevalence.

---

## 11. Certification C — Cross-Modality Compatibility Gate

Certification C must begin with a formal compatibility audit.

## 11.1 Required compatibility surfaces

The audit must compare:

- VAP implementation identity and source-state traceability;
- execution-provenance schema;
- configuration schema;
- genotype observation schema;
- reference assembly;
- reference FASTA identity;
- FASTA index and sequence dictionary identity;
- alignment tool and version;
- variant caller and version;
- normalization policy;
- VEP version;
- VEP cache release;
- transcript policy;
- population resources;
- clinical resources;
- gene-set resources;
- semantic routing policy;
- TEP builder version;
- TEP validator version;
- execution node and operating environment;
- assay-specific settings;
- extractor version and output schema.

## 11.2 Compatibility classification

Every difference must be classified as:

```text
IDENTICAL

INTENTIONAL_MODALITY_SPECIFIC

CONTROLLED_NODE_SPECIFIC

BENIGN_VERSION_DIFFERENCE

COMPARISON_LIMITING

CERTIFICATION_BLOCKING

UNRESOLVED
```

No difference may be silently ignored.

## 11.3 Gate outcome

The compatibility gate may receive:

```text
PASS
PASS WITH NOTES
INSUFFICIENT EVIDENCE
FAIL
```

Cross-modality scientific interpretation may proceed only after a `PASS` or
`PASS WITH NOTES` determination.

A comparison-limiting difference may permit restricted conclusions while
prohibiting others.

---

## 12. Cross-Modality Comparison Rules

## 12.1 Compare invariant architecture separately from biological output

The following are suitable invariant or near-invariant comparison surfaces:

- run identity completeness;
- provenance completeness;
- configuration traceability;
- genotype schema integrity;
- projection error behavior;
- no-call preservation;
- multiallelic relationship governance;
- Stage 07 observation authority;
- Stage 07/08 reconciliation;
- TEP transport byte identity;
- inventory completeness;
- lineage completeness;
- validator status;
- evidence recoverability.

The following are expected to differ biologically or by assay search space:

- total source records;
- total genotype observations;
- coding/noncoding composition;
- rare-variant counts;
- candidate counts;
- gene counts;
- priority distributions;
- sibling-shared structure;
- publication-relevant candidate surfaces.

Expected difference is not failure.

## 12.2 Raw-count restrictions

Raw WES and WGS counts must not be interpreted as directly comparable measures
of biological burden without an explicit denominator and scope.

Potential denominators include, where supported:

- source VCF records;
- genotype observations;
- Stage 07 observations;
- coding observations;
- noncoding observations;
- callable or interrogated territory;
- captured target territory;
- genes represented;
- sample-level opportunity surfaces.

The chosen denominator must be stated for every normalized metric.

## 12.3 Valid comparison classes

The comparative analysis may evaluate:

- preservation completeness;
- genotype projection completeness;
- provenance and lineage completeness;
- transport fidelity;
- semantic routing coherence;
- coding evidence density within an explicitly defined denominator;
- noncoding expansion in WGS;
- complex relationship frequency;
- reviewability surfaces;
- evidence recoverability;
- publication concordance and expansion in the WGS subset.

## 12.4 Confounding structure

The design contains unavoidable confounding:

```text
WES
    sys76
    12 unrelated or separately sampled epilepsy cases

WGS
    MARK
    2 related affected siblings
```

Therefore:

- node and modality are partially confounded;
- cohort size differs;
- family relatedness differs;
- genomic opportunity differs;
- WES target territory and WGS genome-wide territory differ.

The comparison may demonstrate architectural coherence and preservation
behavior.

It cannot isolate a pure causal effect of modality or hardware.

## 12.5 Cross-modality scientific questions

Certification C should answer:

1. Are execution provenance and configuration state equally reconstructable?
2. Are genotype observation schemas and semantics preserved across modalities?
3. Are no-call, phase, allele-index, and multiallelic states handled coherently?
4. Is Stage 07-to-Stage 08 evidence continuity preserved?
5. Are coding and noncoding evidence spaces preserved without destructive compression?
6. Are inventory, lineage, and TEP transport equally reconstructable?
7. Do WES read-count strata remain coherent relative to the WGS evidence surfaces?
8. Does WGS produce the expected noncoding expansion without impairing reviewability?
9. Can publication-relevant evidence be recovered and explained?
10. Are observed differences biological, modality-associated, node-associated, configuration-associated, or unresolved?

---

## 13. Required Evidence Products

DEX-VAP may implement the extractor and probes as appropriate, but the complete
certification evidence should provide the following logical products.

## 13.1 Shared corpus products

Recommended common outputs:

```text
certification_corpus_manifest.tsv
certification_extraction_manifest.json
certification_extraction_receipt.json
per_run_identity_and_source_state.tsv
per_run_execution_provenance_audit.tsv
per_run_configuration_snapshot_audit.tsv
per_run_genotype_integrity_audit.tsv
per_run_stage_reconciliation_audit.tsv
per_run_tep_transport_audit.tsv
per_run_inventory_lineage_audit.tsv
per_run_scientific_sanity_summary.tsv
per_run_certification_status.tsv
certification_anomaly_register.tsv
certification_unresolved_questions.md
```

The names are recommendations rather than an implementation mandate.
Equivalent deterministic outputs are acceptable when their roles are explicit.

## 13.2 WES-specific products

```text
wes_read_count_stratum_summary.tsv
wes_stratum_genotype_summary.tsv
wes_stratum_semantic_surface_summary.tsv
wes_member_outlier_register.tsv
wes_targeted_probe_manifest.json
wes_corpus_certification.md
```

## 13.3 WGS-specific products

```text
wgs_sibling_identity_mapping.tsv
wgs_sibling_shared_private_summary.tsv
wgs_shared_homozygous_summary.tsv
wgs_chromosome_level_summary.tsv
wgs_complex_relationship_summary.tsv
cntnap2_coordinate_transcript_trace.tsv
cntnap2_trace_report.md
wgs_publication_comparator_summary.md
wgs_targeted_probe_manifest.json
wgs_corpus_certification.md
```

## 13.4 Cross-modality products

```text
wes_wgs_compatibility_audit.tsv
wes_wgs_normalization_definitions.md
wes_wgs_preservation_comparison.tsv
wes_wgs_genotype_comparison.tsv
wes_wgs_provenance_lineage_comparison.tsv
wes_wgs_semantic_surface_comparison.tsv
wes_wgs_difference_classification.tsv
wes_wgs_comparative_certification.md
```

## 13.5 Evidence directory model

Certification-grade receipts should remain under:

```text
docs/validation/comparisons/
```

Recommended objective-oriented directories:

```text
docs/validation/comparisons/

    sys76_wes_genotype_aware_execution_provenance/

    mark_wgs_genotype_aware_execution_provenance/

    wes_wgs_genotype_aware_comparison/
```

Each directory should preserve:

- evidence manifests;
- extraction receipts;
- source run identities;
- probe outputs;
- anomaly registers;
- SAGE review materials;
- final certification determination.

Large canonical run artifacts must remain in their governed run locations and
must not be copied into Git merely for certification convenience.

---

## 14. Certification Workflow

## 14.1 Step 1 — Lock corpus identity

Before extraction:

- confirm all 14 run IDs;
- confirm all 14 TEP IDs;
- confirm node locations;
- confirm that source run and TEP directories are immutable;
- confirm the WGS SRA-to-pedigree mapping if available;
- record the certification framework version.

## 14.2 Step 2 — Lock common extraction schema

The same common evidence schema must be used on sys76 and MARK.

Modality-specific outputs may be additive but must not change the meaning of
common fields.

## 14.3 Step 3 — Execute all-member lightweight extraction

Run the common extractor against:

```text
all 12 sys76 WES runs and TEP-VAPs
all 2 MARK WGS runs and TEP-VAPs
```

The extractor must be observational and non-mutating.

## 14.4 Step 4 — SAGE first-pass evaluation

SAGE-VAP reviews:

- evidence completeness;
- schema consistency;
- member-level failures;
- outliers;
- compatibility differences;
- questions requiring high-cardinality inspection.

## 14.5 Step 5 — Targeted DEX probes

DEX-VAP executes bounded probes for:

- unresolved member anomalies;
- representative q1/median/q3 WES behavior;
- WGS sibling shared/private evidence;
- `CNTNAP2` tracing;
- large-file questions not answerable from lightweight summaries;
- suspected artifact or extractor inconsistencies.

## 14.6 Step 6 — Independent corpus certifications

SAGE-VAP issues:

```text
Certification A
    sys76 WES corpus

Certification B
    MARK WGS corpus
```

Each certification must include per-run statuses and corpus-level limitations.

## 14.7 Step 7 — Freeze certified evidence packages

After Certifications A and B:

- freeze manifests and receipts;
- record hashes;
- record certification dates;
- record code and extractor identities;
- prevent silent regeneration from replacing the reviewed evidence.

## 14.8 Step 8 — Execute comparative analysis

Use the frozen certified evidence packages to construct Certification C.

The comparison must not regenerate source summaries under an unrecorded schema
or tool version.

## 14.9 Step 9 — Issue comparative certification

SAGE-VAP issues the cross-modality determination with:

- compatibility-gate result;
- preserved invariant findings;
- modality-specific findings;
- node and family-structure limitations;
- publication concordance/expansion/divergence findings;
- unresolved differences;
- revalidation triggers.

---

## 15. Outcome Vocabulary

## 15.1 Per-run outcomes

### `CERTIFIED`

All required evidence classes pass and no material unresolved limitation
remains.

### `CERTIFIED WITH NOTES`

All required evidence classes are scientifically adequate, but bounded
advisories or limitations must accompany downstream use.

### `INSUFFICIENT EVIDENCE`

The available artifacts do not permit a defensible certification decision.
This does not necessarily imply implementation failure.

### `NOT CERTIFIED`

A material failure, contradiction, evidence-loss condition, or unresolved
blocking defect prevents certification.

## 15.2 Corpus outcomes

### `CORPUS CERTIFIED`

Every required member is certified and no corpus-level blocker remains.

### `CORPUS CERTIFIED WITH NOTES`

Every required member is certified or certified with notes, and the notes do
not invalidate corpus-level use.

### `CORPUS PARTIALLY CERTIFIED`

At least one member is certified, but one or more members remain insufficiently
evidenced or not certified. The corpus must not be represented as fully
certified.

### `CORPUS INSUFFICIENT EVIDENCE`

The corpus evidence package is too incomplete for a defensible aggregate
conclusion.

### `CORPUS NOT CERTIFIED`

A corpus-wide or member-level material failure invalidates the intended corpus
certification object.

## 15.3 Comparative outcomes

### `COMPARISON CERTIFIED`

Both source corpora are independently certified, the compatibility gate
passes, and the comparison supports the stated architectural and scientific
claims.

### `COMPARISON CERTIFIED WITH NOTES`

The comparison is scientifically usable within explicit limitations.

### `COMPARISON INSUFFICIENT EVIDENCE`

One or more required comparative surfaces cannot be evaluated.

### `COMPARISON NOT CERTIFIED`

The source corpora, compatibility gate, evidence integrity, or comparison
methodology fails materially.

---

## 16. Certification Decision Matrix

SAGE-VAP should evaluate each object across these domains:

| Domain | Per-run | Corpus | Cross-modality |
|---|---:|---:|---:|
| Identity and source-state traceability | Required | Required | Required |
| Execution provenance | Required | Required | Required |
| Configuration snapshot | Required | Required | Required |
| Genotype observation integrity | Required | Required | Required |
| Stage preservation and reconciliation | Required | Required | Required |
| TEP transport byte identity | Required | Required | Required |
| Inventory and lineage | Required | Required | Required |
| TEP validator status | Required | Required | Required |
| Scientific sanity surfaces | Required | Required | Required |
| Read-count stratum coherence | Not applicable per WGS run | WES only | Contextual |
| Sibling shared/private evidence | WGS only | WGS only | Contextual |
| `CNTNAP2` trace | WGS only | WGS only | Contextual |
| Compatibility gate | No | No | Required |
| Normalized comparison | No | No | Required |
| Publication comparator | No | WGS contextual | Required contextual |

No domain should be silently collapsed into another.

---

## 17. Assumptions

This framework assumes:

1. The 14 listed run identities are the authoritative modern genotype-aware corpus.
2. The 12 WES TEP-VAPs remain accessible on sys76.
3. The two WGS source runs and TEP-VAPs remain accessible on MARK.
4. Canonical run and TEP directories are immutable during certification.
5. DEX-VAP can execute observational extractors on both nodes.
6. The common genotype and provenance contracts remain materially stable during the certification cycle.
7. Large MARK artifacts can be interrogated node-locally without transfer to sys76.
8. The existing `ERR10619300` certification bundle remains available as a production exemplar.
9. The Badshah et al. publication is used only as an independent comparator.
10. WES read-count strata are project-specific selection categories rather than direct target-coverage measurements.

If an assumption is false, the affected certification claim must be revised.

---

## 18. Limitations

This framework does not establish:

- clinical analytical validation;
- clinical diagnostic validity;
- clinical utility;
- ACMG/AMP classification authority;
- disease causality;
- segregation across unavailable family members;
- population association;
- prevalence;
- diagnostic yield;
- independence of the two WGS siblings;
- a pure hardware effect;
- a pure modality effect;
- universal compatibility with every caller, assay, or genotype schema;
- universal cross-version determinism.

The design is observational and architecture-centered.

WES modality and sys76 execution are linked, while WGS modality and MARK
execution are linked. This prevents complete separation of node and modality
effects.

The WES corpus contains 12 samples, while the WGS corpus contains two related
samples. Statistical claims must remain correspondingly restrained.

---

## 19. Edge Cases

Certification must explicitly protect against the following edge cases.

### 19.1 Missing versus homozygous reference

No-call and partial-call states must not be interpreted as `0/0`.

### 19.2 Single-allele call states

A single called allele must not automatically produce a haploid biological
label without governed context.

### 19.3 Multiallelic and spanning-deletion records

VAP must preserve source context and defer ambiguous allele-specific brokerage
rather than fabricating direct relationships.

### 19.4 Duplicate or repeated source records

Source-record ordinal and hash behavior must prevent identity collision.

### 19.5 FORMAT/sample length mismatch

Mismatch must be preserved and reported rather than silently truncated or
padded into false evidence.

### 19.6 Optional caller fields

Absence of AD, DP, GQ, PL, FT, or other fields may be caller- or
configuration-specific. Missing optional fields are not automatic failures, but
their absence must remain explicit.

### 19.7 TEP package rebuild

A rebuilt TEP must not inherit certification automatically. New hashes,
inventory, lineage, and validator receipts require review.

### 19.8 Reflective sidecar metrics

Reflective telemetry must not be mislabeled as independent recomputation.

### 19.9 Biological outliers

An unusual count or distribution is not evidence of pipeline failure unless
artifact integrity, provenance, genotype projection, or preservation is
compromised.

### 19.10 WGS expansion

Large noncoding and total-observation expansion is expected in WGS and must not
be treated as semantic instability solely because it differs from WES.

### 19.11 Publication notation inconsistency

The `CNTNAP2` trace must not rely on one inconsistent cDNA expression.

### 19.12 Pedigree mapping uncertainty

The two SRA accessions must not be assigned to publication individuals without
an authoritative mapping.

### 19.13 Stage 13 self-reference timing artifact

The known artifact-manifest self-reference timing behavior must be classified
as benign only when it does not alter evidence, hashes, lineage, or package
validity.

### 19.14 Source-state traceability

An uncommitted run-generating state may be certifiable when traceability is
strong, but the certification must state exactly what is and is not proven
byte-for-byte.

---

## 20. Revalidation Triggers

A prior certification must be reconsidered when any of the following changes:

- VAP code affecting genotype projection;
- VAP code affecting execution provenance;
- Stage 07 annotation behavior;
- Stage 08 routing or normalization behavior;
- Stage 09–12 interpretation, prioritization, or validation behavior;
- genotype schema;
- provenance schema;
- configuration schema;
- reference assembly or FASTA;
- annotation engine or cache;
- population, clinical, or gene-set resources;
- multiallelic relationship policy;
- TEP builder;
- TEP validator;
- inventory or lineage model;
- source run artifacts;
- source TEP artifacts;
- extractor or probe implementation in a way that changes derived evidence;
- comparison normalization or denominator definitions;
- discovery of a material error in a prior certification receipt.

Revalidation scope should be proportional to the changed surface.

A local change need not invalidate every prior conclusion when unchanged
surfaces remain provably stable.

---

## 21. Validation Strategy

The validation strategy uses layered evidence.

### Layer 1 — Existing automated validation

Use the existing unit and fixture suites to establish implementation-level
correctness for genotype projection, schema behavior, packaging paths, and
non-interference.

### Layer 2 — All-member lightweight production extraction

Apply a common, non-mutating extractor to all 14 production runs and TEP-VAPs.

This layer establishes broad member coverage with compact evidence.

### Layer 3 — Targeted production probes

Use direct node-local probes to answer questions not resolvable from lightweight
summaries.

Targeted probes must be evidence-driven rather than indiscriminately applied to
large artifacts.

### Layer 4 — Per-run certification

SAGE-VAP evaluates each run independently.

### Layer 5 — Corpus certification

SAGE-VAP evaluates member completeness, stratum or sibling structure, anomaly
patterns, and corpus-level limitations.

### Layer 6 — Cross-modality compatibility and comparison

Only certified source corpora enter the comparative layer.

### Layer 7 — Publication and case-study review

After scientific certification, publication-informed narration and a future
case study may be reviewed for accuracy, scope, and limitations.

---

## 22. Implementation Relevance

This document should guide DEX-VAP toward a reusable certification extractor
rather than one-off manual inspection.

Implementation should favor:

- one common schema across sys76 and MARK;
- logical separation of common and modality-specific outputs;
- deterministic row ordering;
- stable field names;
- explicit null semantics;
- source-path and checksum preservation;
- lightweight summary generation;
- bounded high-cardinality probes;
- run-external receipts;
- no mutation of canonical run or TEP artifacts;
- reusability for future genotype-aware VAP corpora.

Implementation should avoid:

- copying large immutable artifacts into Git;
- recomputing biological outputs merely for certification convenience;
- hidden normalization;
- silent exclusion of failed members;
- hard-coded biological expectations for one specimen;
- conflating TEP validation with full scientific certification;
- generating cross-modality conclusions before source-corpus certification.

The existing `ERR10619300` comparison dossier should serve as the empirical
reference for the strength and auditability of production certification
receipts.

The new implementation should generalize that evidence model while reducing
unnecessary duplication and high-cost work.

---

## 23. Acceptance Criteria

This validation framework is successfully executed when:

### Certification A

```text
all 12 sys76 WES runs have explicit per-run determinations
all required common evidence classes are evaluated
q1, median, and q3 strata are reviewed
all anomalies are classified
one WES corpus determination is issued
```

### Certification B

```text
both MARK WGS runs have explicit per-run determinations
all required common evidence classes are evaluated
WGS scale and preservation are reviewed
sibling shared/private evidence is evaluated
CNTNAP2 is traced by coordinate and transcript-aware identity
one WGS corpus determination is issued
```

### Certification C

```text
both source corpora are independently certified
compatibility differences are classified
normalization and denominators are explicit
architectural invariants are evaluated
modality-specific evidence is interpreted within scope
one cross-modality determination is issued
```

### Evidence governance

```text
all extractor and probe executions have receipts
all certification artifacts have stable identities and hashes
all unresolved questions are explicit
all limitations are preserved
all revalidation triggers are stated
```

---

## 24. Success Condition

The complete certification lifecycle is successful when a future reviewer can
begin with any one of the 14 certified production runs and reconstruct:

```text
what sample was processed
which run produced the evidence
which implementation and configuration generated it
which reference and resources were used
what genotype observations were preserved
how Stage 07 observations entered downstream semantic stages
which artifacts were transported into TEP-VAP
whether transport was byte-identical
how inventory and lineage index the evidence
which advisories or uncertainties remain
why the per-run certification was issued
how the run contributed to its corpus determination
how the certified corpus entered the WES/WGS comparison
```

The reviewer must be able to do this without requiring trust in an undocumented
manual judgment.

---

## 25. Final Certification Principle

```text
Unit validation proves the genotype subsystem can behave correctly.

Production certification determines whether a specific run did behave correctly.

Corpus certification determines whether every required member supports a
coherent scientific substrate.

Comparative certification determines whether independently certified corpora
can support restrained, explicit, and reproducible cross-modality conclusions.
```

The objective is not to prove VAP correct by assumption.

The objective is to determine, through preserved evidence and disciplined
scientific review, what each genotype-aware execution and each certified corpus
genuinely demonstrates.
