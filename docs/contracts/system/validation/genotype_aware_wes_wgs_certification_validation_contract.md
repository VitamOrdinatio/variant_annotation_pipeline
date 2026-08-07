# Genotype-Aware WES/WGS Certification Validation Contract

| Field | Value |
|---|---|
| Document status | Draft v0.2 — SAGE scientific conditions incorporated |
| Contract class | System validation contract |
| Producer system | Variant Annotation Pipeline (VAP) |
| Transport product | TEP-VAP |
| Scientific authority | SAGE-VAP |
| Engineering and evidence-acquisition authority | DEX-VAP |
| WES certification object | 12 genotype-aware WES-designated PRJEB57558 runs on sys76 |
| WGS certification object | 2 genotype-aware epilepsy WGS runs on MARK |
| Comparative certification object | Preservation-centered and opportunity-qualified comparison of the independently certified 12-run WES and 2-run WGS corpora |
| Existing certified exemplar | `ERR10619300 / run_2026_07_14_114546` |
| Scientific review disposition | SAGE-VAP: APPROVE WITH SCIENTIFIC CONDITIONS |
| Scientific conditions incorporated | 2026-08-06 |
| Companion active implementation plan | `docs/plans/infrastructure/active/genotype_aware_wes_wgs_certification_implementation_plan.md` |
| Clinical boundary | Research and portfolio validation only; not clinical validation |

---

## 1. Purpose

This contract defines the binding system obligations for acquiring, validating,
transporting, reviewing, freezing, and comparing evidence for the active
VAP genotype-aware WES/WGS certification program.

It governs three separate certification objects:

```text
Certification A
    12 genotype-aware,
    execution-provenance-enabled
    WES-designated PRJEB57558 runs on sys76

Certification B
    2 genotype-aware,
    execution-provenance-enabled
    epilepsy WGS runs on MARK

Certification C
    the independently certified
    12-run WES corpus
        versus
    the independently certified
    2-run WGS corpus

    first for architecture, preservation,
    provenance, genotype-observation integrity,
    lineage, and semantic composition

    and, only where denominators permit,
    for opportunity-qualified biological comparison
```

The contract exists to ensure that the three certification objects are built
from deterministic, non-mutating, auditable evidence and that cross-modality
comparison cannot conceal an uncertified source run or source corpus.

The governing dependency is:

```text
per-run evidence
    ↓
per-run scientific determination
    ↓
corpus scientific determination
    ↓
frozen certified evidence package
    ↓
controlled cross-modality comparison
    ↓
comparative scientific determination
```

The contract does not assign scientific certification outcomes. It defines the
technical evidence system that must exist before SAGE-VAP may assign those
outcomes.

Certification A and Certification B are producer-preservation certifications.
Their completion does not require every denominator needed for comparative
biological interpretation.

Certification C has two scientifically distinct claim layers:

```text
core comparative layer
    architecture
    preservation
    provenance
    genotype-observation integrity
    lineage
    semantic composition within the emitted observation universe

opportunity-qualified layer
    normalized density
    common-territory recurrence
    assay-associated expansion
    biological yield relative to governed evaluable territory
```

The opportunity-qualified layer SHALL be omitted or explicitly limited when
the required assay, coverage, callability, or common-territory substrate is not
available.

---

## 2. Contract Scope

This contract governs:

- certification-program architecture;
- locked corpus identity;
- common per-run evidence semantics;
- node-local extraction and probe behavior;
- immutable source-artifact handling;
- execution-provenance and configuration-snapshot inspection;
- genotype-observation integrity evidence;
- Stage 07 preservation and downstream reconciliation evidence;
- TEP-VAP transport, inventory, and lineage evidence;
- WES-specific corpus evidence;
- WGS-specific corpus and sibling evidence;
- targeted `CNTNAP2` tracing;
- evidence manifests, hashes, receipts, and command records;
- technical readiness states;
- corpus evidence freezing;
- cross-modality compatibility gating;
- controlled construction of Certification C evidence;
- assay-design and opportunity-substrate discovery;
- coverage and callability denominator evidence where governed and available;
- common WES/WGS evaluable-territory construction;
- exact compact gene- and variant-membership evidence;
- emitted-observation-universe boundaries for genotype summaries;
- governed rarity semantics;
- publication-comparator claim scoping;
- failure handling, restart behavior, versioning, and revalidation triggers.

This contract does not redefine:

- VAP producer semantics;
- genotype-observation schema semantics;
- execution-provenance schema semantics;
- Stage 07 authority;
- TEP-VAP preservation doctrine;
- VDB namespace brokerage;
- RDGP reasoning responsibilities;
- SAGE-VAP scientific acceptance boundaries;
- LANE-VAP case-study authorship responsibilities.

---

## 3. Governing Sources and Precedence

This contract operationalizes, but does not replace, the following governing
sources:

```text
docs/validation/
    genotype_aware_wes_wgs_execution_provenance_certification.md
    genotype_observation_validation.md
    sidecar_telemetry.md
    vap_to_vdb_architecture_walkthrough.md

docs/design/
    wes_epilepsy_experimental_design.md
    wgs_epilepsy_experimental_design.md
    wes_wgs_comparative_experimental_design.md

docs/validation/comparisons/
    err10619300_genotype_elevation_validation/
        sage_modernized_vap_producer_substrate_certification.md

shared/handoffs/vap/genotype/
    SAGE-VAP-v2_to_DEX-VAP-v3_genotype_aware_wes_wgs_certification_handoff.md

SAGE-VAP scientific review determination
    APPROVE WITH SCIENTIFIC CONDITIONS
    dated 2026-08-06
```

The governing precedence for this lifecycle is:

```text
certified architecture and producer doctrine
    ↓
scientific certification framework
    ↓
this system validation contract
    ↓
active implementation plan
    ↓
extractor and probe implementation
    ↓
execution receipts and evidence packages
    ↓
SAGE-VAP scientific determinations
```

If an implementation convenience conflicts with producer doctrine or the
scientific certification framework, the implementation convenience shall be
rejected.

If this contract and the active implementation plan conflict, this contract is
authoritative.

---

## 4. Normative Language

The terms **MUST**, **MUST NOT**, **REQUIRED**, **SHALL**, and **SHALL NOT**
express binding requirements.

The terms **SHOULD** and **SHOULD NOT** express preferred behavior that may be
departed from only with an explicit recorded rationale.

The term **MAY** expresses permitted behavior.

---

## 5. Contract Parties and Authority Boundaries

### 5.1 SAGE-VAP

SAGE-VAP owns:

- scientific certification questions;
- required evidence classes;
- acceptance boundaries;
- interpretation of observed differences;
- classification of findings as blocking, advisory, unresolved, or out of scope;
- requests for bounded follow-up probes;
- per-run certification outcomes;
- corpus certification outcomes;
- comparative certification outcomes;
- scientific limitations and revalidation triggers;
- scientific review of any later case study.

### 5.2 DEX-VAP

DEX-VAP owns:

- certification-system architecture;
- common extractor and probe design;
- deterministic node-local evidence gathering;
- technical validation and reconciliation;
- artifact identity and checksum calculation;
- output schemas;
- manifests, receipts, command records, and logs;
- bounded anomaly investigation;
- evidence-package freezing after SAGE review;
- technical clarification during later case-study review.

DEX-VAP SHALL NOT issue final scientific certification outcomes.

### 5.3 LANE-VAP

LANE-VAP may author a comparative case study only after Certifications A, B,
and C establish a certified claim surface.

LANE-VAP SHALL NOT infer scientific claims beyond SAGE-certified evidence and
limitations.

### 5.4 User authority

The repository owner retains final authority over execution authorization,
repository mutation, evidence retention, and release decisions.

---

## 6. Locked Certification Objects

### 6.1 Certification A — sys76 WES corpus

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

The q1, median, and q3 labels are project-specific, quartile-centered
read-count strata. They SHALL NOT be represented as direct measured target
coverage without supporting coverage evidence.

Until a governed assay-design source resolves the library-preparation and
target-territory discrepancy, the corpus SHALL be described as:

```text
WES-designated PRJEB57558 runs
```

The contract SHALL NOT silently assume that ENA `AMPLICON` metadata, repository
WES designation, capture-based exome terminology, or a uniform bait design are
interchangeable. The evidence package SHALL establish or explicitly leave
unresolved:

- library-preparation strategy;
- target or bait-set identity;
- governed target intervals;
- whether one assay design applies to all 12 specimens.

`ERR10619300 / run_2026_07_14_114546` is the existing certified production
exemplar. Prior evidence MAY be incorporated by reference only when the run,
TEP-VAP, governing schemas, and reviewed evidence remain unchanged and
checksum-stable.

### 6.2 Certification B — MARK WGS corpus

| Sample/SRA | Run ID | Scientific description |
|---|---|---|
| `SRR13573587` | `run_2026_07_29_123020` | affected sibling WGS |
| `SRR13573588` | `run_2026_08_01_092338` | affected sibling WGS |

These are two affected brothers. The contract SHALL NOT represent them as
biological twins.

The SRA-to-publication-individual mapping to `V-2` and `V-4` SHALL remain
unknown unless an authoritative governed source establishes it.

### 6.3 Certification C — cross-modality object

Certification C SHALL compare only:

```text
a frozen, independently certified
12-member sys76 WES evidence package

against

a frozen, independently certified
2-member MARK WGS evidence package
```

Certification C SHALL NOT begin from unreviewed run directories, regenerated
summaries, or an uncertified corpus.

A complete 12-versus-2 Certification C may consume only a WES and WGS corpus
with one of the following SAGE-VAP outcomes:

```text
CORPUS CERTIFIED
CORPUS CERTIFIED WITH NOTES
```

`CORPUS PARTIALLY CERTIFIED` MAY support only a newly bounded partial
comparison whose membership and claims are explicitly narrowed. It SHALL NOT be
represented as the complete 12-versus-2 comparison.

`CORPUS INSUFFICIENT EVIDENCE` and `CORPUS NOT CERTIFIED` are not
comparison-ready states.

### 6.4 Corpus identity changes

Any change to a sample, run ID, TEP ID, node location, or reviewed package SHALL:

1. invalidate the affected locked identity;
2. be recorded in the active implementation plan;
3. generate new evidence hashes and receipts;
4. trigger SAGE-VAP review before certification proceeds.

---

## 7. Locked Scientific and System Invariants

### 7.1 Stage 07 authority

Stage 07 is the authoritative biological observation anchor.

Stages 08–13 may organize, interpret, prioritize, validate, or summarize
producer evidence, but they SHALL NOT replace the Stage 07 observation state.

### 7.2 Genotype authority

Genotype observations are first-class producer evidence.

The evidence-acquisition system SHALL preserve, where present:

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
variant-relationship status
```

The system SHALL NOT infer unsupported:

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

### 7.3 Missingness authority

A missing genotype, partial no-call, absent source record, or absent producer row
SHALL NOT be converted into or narrated as:

```text
0/0
homozygous reference
no variant
callable locus
negative evidence
assay opportunity
```

### 7.4 Execution-provenance authority

The following are distinct required artifacts:

```text
metadata/execution_provenance.json
metadata/config_snapshot.yaml
```

Their TEP-VAP counterparts are:

```text
entities/context/execution_provenance.json
entities/metadata/config_snapshot.yaml
```

The JSON execution receipt and YAML configuration snapshot SHALL be validated
independently and SHALL NOT be collapsed into one evidence class.

### 7.5 Transport authority

TEP-VAP transports producer-authored evidence without reinterpretation.

Where direct preservation is required, the run-local and TEP-VAP artifacts
SHALL be byte-identical.

### 7.6 Producer-consumer boundary

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

Certification evidence SHALL NOT introduce VDB- or RDGP-level conclusions into
VAP producer truth.

### 7.7 Multiallelic authority

Multiallelic, spanning-deletion, symbolic, malformed, or otherwise complex
source records SHALL retain source context and explicit relationship status.

The probes SHALL NOT fabricate direct allele-specific relationships where VAP
has correctly deferred brokerage to VDB.

### 7.8 Biological count authority

No universal biological row-count threshold applies across different patients,
read-count strata, siblings, or modalities.

An unusual count or distribution is an anomaly to investigate, not automatic
evidence of failure.

### 7.9 Publication boundary

The Badshah et al. publication is an independent comparator. It is not:

- the authoritative biological substrate;
- a truth set;
- independent validation of VAP;
- a requirement that VAP reproduce only publication-filtered candidates.

A targeted `CNTNAP2` trace supports a `CNTNAP2`-specific publication claim.
Publication-wide candidate concordance requires bounded evidence for all
reported candidate genes intended to support that claim:

```text
PDZD7
ALG6
RBM20
CNTNAP2
```

Shared homozygous observations SHALL NOT be narrated as reconstruction of
publication-reported regions of homozygosity unless an independently governed
ROH substrate exists.

### 7.10 Emitted-observation-universe authority

Genotype-state proportions and related summaries describe genotype
observations present in the VAP-emitted variant universe.

They SHALL NOT be represented as:

- genome-wide genotype proportions;
- callable-locus genotype proportions;
- homozygous-reference burden;
- evidence of variant absence;
- negative evidence;
- assay opportunity.

A larger proportion of a genotype state among emitted WGS variants does not,
by itself, establish a larger genome-wide burden.

### 7.11 Rarity authority

The primary certification rarity definition SHALL use the governed VAP
frequency classification produced consistently across the 14 runs.

The publication-comparator threshold:

```text
MAF <= 0.001
```

MAY be used only to reconstruct or compare the Badshah et al. filtering logic.

The following states SHALL remain distinct:

```text
VAP-governed rare
publication-threshold rare
frequency unknown
frequency unavailable
not rare
```

An unknown or unavailable population frequency SHALL NOT be converted into
`rare`.

### 7.12 Assay-opportunity authority

Raw observation counts SHALL NOT be interpreted as variant density, biological
yield, or modality-associated burden without a governed opportunity
denominator.

Where available, the certification substrate SHALL preserve:

- assay or design identity;
- target, interrogated, or callable territory identity;
- interval or mask hash;
- total opportunity bases;
- depth and coverage-threshold summaries;
- mapping and duplication context;
- the callable definition used.

Unavailable opportunity evidence SHALL remain explicit and SHALL narrow
Certification C claims rather than be silently estimated.

### 7.13 Observational-unit authority

The 14 executions SHALL NOT be pooled as one homogeneous epilepsy cohort.

Scientifically valid presentation SHALL preserve:

```text
12 individual unrelated WES-designated runs
2 individual related WGS sibling runs
```

Certification C MAY present:

- per-run values;
- the 12-member WES distribution;
- q1, median, and q3 WES summaries;
- each WGS sibling separately;
- a WGS family-level shared/private summary;
- descriptive comparison of the certified corpus surfaces.

The current design SHALL NOT support:

- inferential WES-versus-WGS significance testing;
- population-level effect estimates;
- treatment of the siblings as independent replicates;
- separation of modality effect from node effect;
- one pooled 14-run epilepsy-corpus average presented as a uniform sampling
  structure.

---

## 8. Certification-System Architecture

The implementation SHALL use one coherent certification system rather than
run-specific, incompatible scripts.

The minimum architecture is:

```text
locked corpus manifest
    ↓
common per-run extractor
    ↓
common technical evidence package
    ↓
modality-specific additive probes
    ↓
per-run SAGE review
    ↓
corpus aggregation
    ↓
corpus SAGE review
    ↓
frozen certified package
    ↓
controlled comparison extractor
    ↓
comparative SAGE review
```

### 8.1 Common implementation requirement

The same common extractor implementation and shared field definitions SHALL be
used on sys76 and MARK.

Modality-specific evidence MAY be additive, but it SHALL NOT change the meaning
of a shared field.

### 8.2 Parameterization requirement

The common extractor SHALL be manifest-driven or equivalently parameterized.
It SHALL NOT encode one run's identities, expected biological counts, or paths
as universal constants.

### 8.3 Calibration requirement

Before broad corpus execution, the generalized extractor SHALL be calibrated
against the existing certified `ERR10619300` exemplar.

Calibration SHALL establish that the generalized system reproduces the prior
technical conclusions or explicitly explains any difference introduced by a
newer schema, implementation, or evidence definition.

### 8.4 Two-layer evidence model

The system SHALL distinguish:

```text
core all-member certification surface
    required for every one of the 14 runs
    and sufficient to support Certifications A and B

comparative-opportunity extension
    gathered where governed and available
    and required for opportunity-qualified Certification C claims
```

The core all-member surface SHALL include complete foundational checks for:

- observation-ID completeness;
- exact within-run observation-ID uniqueness;
- duplicate-identity detection;
- called-allele-index validity;
- missing and partial-call preservation;
- processed-to-TEP identity;
- Stage 07 preservation;
- inventory closure;
- lineage closure.

These foundational properties SHALL NOT be representative-only.

The system MAY additionally distinguish bounded high-cost biological or
forensic probes for:

- predetermined WES representatives;
- detected outliers;
- both WGS siblings;
- publication-candidate tracing;
- unresolved certification questions;
- validation of the lightweight extractor itself.

A high-cost probe SHALL be justified by a certification claim, anomaly, or
representative audit requirement—not merely by technical possibility.

---

## 9. Evidence Disposition Contract

Every requirement in the scientific certification framework SHALL receive one
of the following engineering dispositions in the active implementation plan:

```text
AVAILABLE_DIRECTLY
    present as a small canonical or TEP-VAP artifact

AVAILABLE_BY_EXISTING_EXTRACTOR
    emitted by an existing lightweight extraction utility

AVAILABLE_BY_EXISTING_PROBE
    supported by a reusable validation script or prior receipt pattern

NEW_BOUNDED_PROBE_REQUIRED
    requires a new observational node-local probe

BLOCKED_PENDING_DISCOVERY
    source path, package identity, or governed evidence is unresolved

UNAVAILABLE_WITH_EXPLICIT_LIMITATION
    governed evidence is absent and the missing substrate narrows
    the permissible certification claim

NOT_APPLICABLE
    scientifically inapplicable to that certification object
```

Each disposition SHALL identify:

- requirement ID;
- certification object;
- scientific question;
- source node;
- source artifact or artifact family;
- extraction or probe implementation;
- output field or artifact;
- all-member or targeted execution scope;
- expected I/O and computational burden;
- validation method;
- mutation risk;
- known limitation;
- whether absence is certification-blocking.

---

## 10. Common Per-Run Evidence Contract

Every one of the 14 runs SHALL receive an explicit common technical evidence
surface.

Representative success SHALL NOT substitute for an unreviewed member.

### 10.1 Run, sample, package, and source-state identity

The evidence package SHALL capture:

- sample or SRA identity;
- run ID;
- execution node;
- assay or modality;
- source BioProject where known;
- canonical run path;
- canonical TEP-VAP path;
- TEP ID and package version;
- run completion state;
- VAP implementation identity;
- run-generating commit or bounded source-state receipt;
- extractor and probe version;
- extractor and probe SHA-256;
- critical source-artifact hashes.

When the run-generating state was uncommitted, the evidence SHALL preserve,
where available:

- base commit;
- Git status;
- tracked working-tree patch;
- diff summary;
- untracked path inventory;
- subsequent committed state;
- post-commit conformance evidence.

The evidence SHALL state exactly what source identity is and is not proven.

### 10.2 Execution-provenance evidence

The common extractor SHALL inspect the contents—not merely the presence—of:

```text
metadata/execution_provenance.json
entities/context/execution_provenance.json
```

It SHALL establish or report unresolved:

- readability and parse validity;
- schema or contract identity;
- provenance completeness status;
- resolution mode;
- run binding;
- host, operating environment, and Python identities;
- alignment, calling, normalization, and annotation identities;
- VEP and cache identities;
- reference assembly and FASTA identity;
- FASTA index and sequence dictionary identity;
- aligner-index constituent identities where applicable;
- population, clinical, gene-set, and annotation-resource identities;
- required unknown or unsupported values;
- timing at the governed execution boundary;
- run-local to TEP-VAP byte identity;
- inventory registration;
- lineage registration.

Artifact presence alone SHALL NOT constitute provenance conformance.

### 10.3 Configuration-snapshot evidence

The common extractor SHALL inspect:

```text
metadata/config_snapshot.yaml
entities/metadata/config_snapshot.yaml
```

It SHALL establish or report unresolved:

- readability and parse validity;
- run and sample binding;
- configuration schema or version where defined;
- modality identity;
- reference and annotation settings;
- caller and normalization settings;
- routing and filtering settings;
- genotype projection settings;
- TEP emission settings;
- run-local to TEP-VAP byte identity;
- consistency with execution provenance.

Configuration differences SHALL be recorded for later classification; they
SHALL NOT be silently normalized away.

### 10.4 Genotype-observation evidence

The common extractor SHALL inspect the atomic genotype artifact set:

```text
processed/genotype_observations.tsv
processed/genotype_projection_summary.json
processed/genotype_source_header_context.json
```

and:

```text
entities/genotype/genotype_observations.tsv
entities/genotype/genotype_projection_summary.json
entities/genotype/genotype_source_header_context.json
```

The evidence SHALL include, where supported by the schema:

- artifact presence and non-emptiness;
- atomic three-artifact completeness;
- schema identity;
- source VCF path and SHA-256;
- source VCF header hash;
- selected sample identity;
- source-record count;
- projected-record count;
- genotype-observation count;
- deterministic observation-ID completeness;
- exact within-run observation-ID uniqueness;
- duplicate observation-ID count and bounded exemplars;
- source-record ordinal and hash completeness;
- GT-state distribution;
- missing and partial-call counts;
- phased and unphased counts;
- GT-arity and explicit ploidy distributions;
- called-allele index validity;
- multiallelic and spanning-deletion counts;
- direct and complex/deferred relationship counts;
- AD, DP, GQ, PL, FT, and FORMAT-field availability and missingness;
- FORMAT/sample length mismatches;
- malformed-call counts;
- duplicate or repeated source-record evidence;
- run-local to TEP-VAP byte identity;
- inventory and lineage registration.

Large genotype tables SHALL be scanned streamingly or by an equivalently bounded
method. They SHALL NOT require whole-table memory loading merely for
certification.

### 10.5 Stage preservation and semantic continuity

The evidence SHALL support:

- Stage 07 observation availability;
- Stage 07-to-Stage 08 identity continuity;
- governed-universe accounting;
- coding, splice, noncoding, and retained-background reconciliation;
- Stage 09 and Stage 10 input/output reconciliation;
- Stage 11 and Stage 12 additive overlay accounting;
- unresolved and common evidence preservation;
- explicit observation-loss accounting;
- detection of unexplained row disappearance;
- deterministic bounded record traces through relevant stages.

The evidence system SHALL distinguish observation preservation from downstream
interpretation or prioritization.

### 10.6 TEP-VAP transport, inventory, and lineage

The evidence SHALL establish or report unresolved:

- required entity presence;
- entity-role and cardinality consistency;
- inventory completeness;
- lineage-manifest readability and consistency;
- required lineage edges;
- source and transport hashes;
- processed-to-TEP byte identity where required;
- genotype entity registration;
- execution-provenance registration;
- configuration-snapshot registration;
- producer identity retention;
- orphan entity count;
- broken required lineage edge count;
- validator version and result;
- known Stage 13 self-reference timing advisory where applicable.

A validator pass SHALL be treated as one certification dimension, not as a
substitute for all other evidence classes.

### 10.7 Scientific sanity surface

The common extractor SHALL emit bounded diagnostic summaries sufficient to
detect silent failure, including:

- stage-level counts;
- coding, splice, noncoding, and retained-background distributions;
- consequence distributions;
- frequency-state distributions;
- clinical-annotation retention;
- genotype-state distributions;
- multiallelic relationship distributions;
- reviewability and priority-state distributions;
- gene-surface counts;
- rare and high-impact observation counts;
- deterministic representative traces.

These summaries are diagnostic evidence. They SHALL NOT be represented as
truth-set benchmarks, diagnostic yield, disease prevalence, or clinical
classification.

Every genotype-distribution output SHALL carry an explicit
`VAP_EMITTED_VARIANT_OBSERVATION_UNIVERSE` boundary or an equivalent
machine-readable definition.

Every rarity output SHALL record the rarity definition and SHALL distinguish
frequency unknown from rare.

### 10.8 Assay-opportunity and coverage evidence

The common evidence model SHALL preserve the following where governed evidence
exists.

For each WES-designated run:

- assay or capture-design identity;
- library-preparation strategy;
- target interval or bait-set identity;
- target interval path and SHA-256;
- total target bases;
- mean and median target depth;
- target bases covered at `>=10x`, `>=20x`, and `>=30x`;
- mapping rate or equivalent mapping context;
- duplication rate or equivalent duplication context;
- callable target bases, when a governed callable definition exists;
- the callable definition and tool identity.

For each WGS run:

- total interrogated genome territory;
- callable-region or callable-mask identity;
- callable mask path and SHA-256, where available;
- total callable bases;
- mean and median genome depth;
- genome bases covered at `>=10x`, `>=20x`, and `>=30x`;
- mapping rate or equivalent mapping context;
- duplication rate or equivalent duplication context;
- the callable definition and tool identity.

The evidence system SHOULD prefer existing governed run artifacts over a new
BAM-scale probe.

A new BAM- or alignment-scale opportunity probe SHALL be authorized only when:

1. the metric supports a defined scientific claim;
2. no governed lightweight artifact supplies it;
3. the implementation plan records I/O burden and node-safety controls;
4. SAGE-VAP confirms the evidence is scientifically necessary.

Missing denominator evidence SHALL use
`UNAVAILABLE_WITH_EXPLICIT_LIMITATION`; it SHALL NOT be fabricated.

### 10.9 Exact compact membership surfaces

Each per-run package SHALL retain compact exact membership evidence sufficient
to support any later recurrence, overlap, or expansion claim.

The package SHALL preserve, as applicable:

- governed gene identities represented;
- observation count and evidence class per gene;
- genes with VAP-governed rare evidence;
- genes with high-impact evidence;
- coding, splice, and noncoding gene membership;
- coordinate-reference-alternate identities required for recurrence analysis;
- genotype-observation identity for each retained compact variant member;
- genomic-territory class where defined;
- exact observations supporting any highlighted cross-run claim.

The membership surfaces SHALL be compact, reviewable, and hash-bound. They
SHALL NOT require transporting the complete genotype table.

Aggregate counts alone SHALL NOT support certification claims about:

- recurrent genes;
- gene-surface overlap;
- gene-surface expansion;
- exact observation recurrence;
- common-territory variant sharing.

---

## 11. Node-Local Evidence Acquisition Contract

### 11.1 Canonical data locality

Large canonical run artifacts SHALL remain on their governing node.

Certification SHALL move only:

```text
small manifests
small summaries
small audit tables
hashes
receipts
bounded traces
command records
logs
compressed evidence packages
```

Complete BAM, VCF, genotype-observation, or other high-cardinality production
artifacts SHALL NOT be copied into Git or transferred between nodes merely for
review convenience.

### 11.2 Observational execution

All extractors and probes SHALL be observational.

They SHALL NOT:

- modify canonical run artifacts;
- alter TEP-VAP contents;
- rewrite source manifests in place;
- repair or normalize source evidence silently;
- alter pipeline control flow;
- regenerate a TEP-VAP without separate authorization;
- write into immutable `results/` or canonical TEP directories;
- overwrite a reviewed evidence package.

### 11.3 MARK execution path

MARK probes SHALL:

1. be authored and tested on sys76 where practical;
2. be committed to the VAP repository;
3. be pushed through Git;
4. be pulled on MARK;
5. run from the MARK VAP repository root;
6. read canonical MARK run and TEP-VAP artifacts in place;
7. write outputs only to a new timestamped directory under `/root/Desktop/`;
8. emit a package manifest and receipt;
9. emit a compressed evidence archive and archive SHA-256;
10. be transferred to sys76 through the governed Guacamole I/O workflow.

`/root/Desktop/` is the non-Git MARK output boundary. It SHALL NOT be treated as
a canonical production-artifact location.

### 11.4 sys76 execution path

sys76 extractors SHALL read the 12 canonical WES run directories and TEP-VAPs
in place and SHALL write evidence outside immutable run and TEP-VAP directories.

Committed certification-grade evidence SHALL reside under the governed
comparison directories defined in Section 18.

### 11.5 Temporary workspace

A probe MAY use a node-local temporary workspace for sorted streams, SQLite,
DuckDB, or other bounded joins when necessary.

Temporary workspace SHALL:

- be outside immutable run and TEP-VAP directories;
- be recorded in the command receipt;
- contain no silent mutation of source artifacts;
- be cleaned or retained according to an explicit recorded policy;
- never become the sole copy of certification evidence.

---

## 12. Probe Execution Classes

### 12.1 Batch-level probes

The following SHOULD execute once per node/source state rather than once per
run:

- repository `HEAD`, branch, and working-tree state;
- Python and dependency environment;
- operating-system and host identity;
- extractor/probe source hashes;
- full or governed test suite;
- available disk and temporary-workspace state.

### 12.2 Per-run probes

The following SHALL execute independently for each run:

- identity and source-state extraction;
- execution-provenance audit;
- configuration-snapshot audit;
- genotype-integrity audit;
- Stage 07 preservation and downstream reconciliation;
- TEP-VAP transport audit;
- inventory and lineage audit;
- scientific sanity summary;
- exact compact gene- and variant-membership extraction;
- assay-opportunity extraction where governed evidence is available.

### 12.3 Corpus-level probes

Corpus probes SHALL consume completed per-run evidence packages and SHALL NOT
silently bypass failed or missing members.

### 12.4 Targeted probes

Targeted probes MAY execute for:

- representative q1, median, and q3 WES members;
- the existing certified WES exemplar;
- detected WES or WGS outliers;
- both WGS siblings;
- `CNTNAP2` tracing;
- unresolved source-state, identity, genotype, preservation, or transport
  questions;
- validation of the lightweight extractor itself.

---

## 13. Certification A — WES-Specific Contract

### 13.1 All-member completeness

All 12 WES members SHALL receive a common per-run evidence package and an
explicit SAGE-VAP per-run determination.

The existing ERR10619300 certification MAY be inherited only under the
conditions in Section 6.1. Its identity and evidence status SHALL still appear
in the new corpus package.

### 13.2 Read-count-stratum evidence

The WES corpus evidence SHALL summarize q1, median, and q3 strata for:

- genotype completeness and missingness;
- multiallelic and complex relationship states;
- Stage 07 preservation;
- semantic routing;
- reviewability;
- rare and high-impact evidence surfaces;
- anomaly rates;
- configuration and resource compatibility.

The purpose is stability assessment and anomaly detection—not numerical
identity among different patients.

### 13.3 WES outlier register

Every material WES outlier SHALL be provisionally classified as one of:

```text
EXPECTED_BIOLOGICAL_VARIATION
READ_COUNT_ASSOCIATED_VARIATION
CONFIGURATION_OR_RESOURCE_DIFFERENCE
EXTRACTOR_ANOMALY
ARTIFACT_ANOMALY
UNRESOLVED
```

DEX-VAP supplies the technical evidence. SAGE-VAP determines scientific meaning
and certification consequence.

### 13.4 Representative high-cost coverage

Absent a detected anomaly that requires additional coverage, the predetermined
WES representative set SHALL be:

| Role | Sample |
|---|---|
| q1 representative | `ERR10619212` |
| median representative and certified exemplar | `ERR10619300` |
| q3 representative | `ERR10619225` |

Any detected outlier SHALL be added to, not substituted for, this set.

Representative high-cost success SHALL supplement, not replace, all-member
foundational evidence.

### 13.5 WES assay identity and opportunity qualification

Certification A MAY proceed as a producer-preservation certification while WES
assay identity remains qualified, provided the uncertainty is explicit and does
not undermine run or artifact identity.

The WES corpus package SHALL establish or preserve as unresolved:

- whether all 12 runs share one library-preparation strategy;
- whether all 12 runs share one target design;
- the governed target intervals;
- the relationship between repository WES designation and ENA `AMPLICON`
  metadata;
- which coverage and callability denominators are available.

Until resolved, biological-yield narration SHALL use
`WES-designated PRJEB57558 runs` and SHALL NOT claim uniform exome-wide
opportunity.

---

## 14. Certification B — WGS-Specific Contract

### 14.1 Independent per-run evidence

Both WGS siblings SHALL receive independent common per-run evidence packages
and explicit SAGE-VAP per-run determinations.

Neither sibling SHALL stand in for the other.

### 14.2 WGS scale and search-space evidence

Each WGS package SHALL include:

- chromosome-level observation counts;
- coding, splice, noncoding, and retained-background composition;
- genotype-state distributions;
- multiallelic and complex/deferred relationship distributions;
- large-artifact row counts, byte sizes, and required hashes;
- TEP-VAP entity sizes and transport status;
- explicit treatment of expected WGS search-space expansion.

Large noncoding or total-observation expansion SHALL NOT be treated as failure
solely because it differs from WES.

### 14.3 Sibling shared/private evidence

After both per-run packages are technically complete, a sibling-level probe
SHALL emit coordinate- and allele-aware summaries of:

- observations shared by both siblings;
- observations private to each sibling;
- shared identical genotype states;
- discordant genotype states at shared variant identities;
- shared homozygous-alternate observations;
- shared rare homozygous observations;
- shared complex or deferred multiallelic records;
- chromosome-level shared/private composition;
- bounded exemplars for each category.

The sibling probe SHALL preserve uncertainty and SHALL NOT infer inheritance,
segregation, causality, de novo status, or compound heterozygosity.

### 14.4 `CNTNAP2` trace

A dedicated bounded trace SHALL search the governed VAP evidence using:

```text
assembly
chromosome
position
reference allele
alternate allele
gene identity
transcript identity
normalized HGVS
protein consequence
sample genotype state
source record
Stage 07 observation
downstream semantic overlays
TEP-VAP entity
inventory registration
lineage registration
```

The trace SHALL NOT depend on one publication cDNA string because the
publication contains inconsistent cDNA expressions for the reported
p.Gly228Arg signal.

The trace SHALL preserve a hierarchical concordance assessment:

```text
genomic concordance
    same assembly and chromosome-position-reference-alternate identity

gene/protein concordance
    same CNTNAP2 identity and p.Gly228Arg consequence

transcript concordance
    compatible transcript-specific HGVS after normalization

notation discordance
    publication cDNA strings differ while genomic and protein identity agree
```

A cDNA-string discrepancy SHALL NOT defeat concordance when genomic and protein
identities agree.

The technical output SHALL support, but SHALL NOT itself assign, the scientific
categories:

```text
PUBLICATION_CONCORDANCE
PUBLICATION_EXPANSION
PUBLICATION_DIVERGENCE
UNRESOLVED_NORMALIZATION_DIFFERENCE
NOT_OBSERVED
```

This trace supports only a `CNTNAP2`-specific publication claim. A broader
publication-candidate claim requires bounded traces for `PDZD7`, `ALG6`,
`RBM20`, and `CNTNAP2`.

### 14.5 Pedigree identity

The evidence package SHALL record whether a governed source establishes:

```text
SRR13573587 → V-2 or V-4
SRR13573588 → V-2 or V-4
```

If not established, both mappings SHALL remain `UNKNOWN`.

The unresolved mapping does not block Certification B. It limits only
person-specific publication narration.

### 14.6 WGS opportunity denominator

The WGS corpus package SHALL preserve available genome-depth, coverage,
mapping, duplication, and callable-territory evidence under Section 10.8.

Absence of an interval-level callable mask does not automatically block
Certification B. It limits normalized density and exact common-territory claims
in Certification C.

---

## 15. Corpus Aggregation and Certification Contract

### 15.1 Per-run precedence

Every corpus member SHALL receive an explicit per-run SAGE-VAP determination
before corpus certification.

### 15.2 Corpus aggregation

A corpus aggregator SHALL consume the reviewed per-run evidence packages and
emit:

- corpus identity and completeness;
- per-run technical state;
- schema and contract compatibility;
- source-state compatibility;
- provenance compatibility;
- configuration and resource differences;
- genotype and preservation summaries;
- exact gene- and variant-membership package identities;
- opportunity-denominator availability and limitations;
- anomaly and unresolved-question registers;
- targeted-probe coverage;
- evidence-package hashes.

### 15.3 No silent exclusion

A failed, missing, or unresolved member SHALL NOT be silently omitted from a
corpus summary.

Its state SHALL remain visible to SAGE-VAP and shall affect the available corpus
outcome according to the governing scientific framework.

### 15.4 Frozen certified evidence package

After SAGE-VAP issues Certification A or B, DEX-VAP SHALL freeze the reviewed
technical evidence package by recording:

- corpus manifest;
- all per-run package identities;
- all evidence hashes;
- extractor and probe identities;
- commands and execution receipts;
- anomaly and limitation registers;
- SAGE-VAP determination identity and date;
- package version;
- freeze timestamp;
- archive checksum where archived.

A frozen package SHALL NOT be overwritten.

Any regeneration SHALL create a new version and trigger review.

### 15.5 Durable SAGE certification record

Once SAGE-VAP issues a per-run, corpus, or comparative certification
determination, that determination SHALL be codified as a durable repository
validation record under the applicable `docs/validation/comparisons/`
namespace.

The committed certification record SHALL identify:

- reviewed evidence-package version;
- manifest and receipt hashes;
- certified membership;
- outcome;
- scientific notes and limitations;
- unresolved questions;
- revalidation triggers;
- SAGE-VAP review identity and date.

A chat response or transient handoff alone SHALL NOT constitute the durable
repository certification record.

---

## 16. Certification C — Cross-Modality Compatibility Contract

### 16.1 Entry gate

Certification C SHALL NOT begin until Certifications A and B have independently
reached a frozen state usable for comparison.

### 16.2 Compatibility surfaces

The compatibility audit SHALL compare:

- VAP implementation and source-state identity;
- configuration schema;
- reference assembly and FASTA identity;
- alignment software and version;
- variant caller and version;
- normalization policy;
- VEP and cache identity;
- transcript-selection policy;
- population resources;
- clinical resources;
- genotype-observation schema;
- semantic-routing policy;
- TEP-VAP builder version;
- TEP-VAP validator version;
- execution-provenance schema;
- node and operating-environment identities;
- extractor and evidence-schema identities;
- WES assay and target-design identity;
- WGS callable-territory identity;
- coverage and callability definitions;
- opportunity-denominator availability;
- compact membership-schema identity.

### 16.3 Compatibility classifications

Every material difference SHALL receive one of:

```text
IDENTICAL
INTENTIONAL_MODALITY_DIFFERENCE
CONTROLLED_NODE_DIFFERENCE
BENIGN_VERSION_DIFFERENCE
COMPARISON_LIMITING_DIFFERENCE
CERTIFICATION_BLOCKING_INCOMPATIBILITY
UNRESOLVED
```

DEX-VAP supplies technical evidence for classification. SAGE-VAP determines
scientific acceptability and claim boundaries.

### 16.4 Confounding structure

The comparative evidence SHALL explicitly preserve that:

- WES and sys76 are linked;
- WGS and MARK are linked;
- the WGS corpus contains related siblings;
- the WES corpus contains unrelated patients;
- the corpora have unequal sample counts;
- WES and WGS interrogate different genomic search spaces.

The comparison SHALL NOT attribute every observed difference solely to assay
modality.

The primary observational unit SHALL remain the individual run. The two WGS
siblings SHALL additionally receive a family-level shared/private summary but
SHALL NOT be treated as independent replicates.

Certification C SHALL be descriptive and preservation-centered. It SHALL NOT
perform inferential WES-versus-WGS significance testing or estimate a modality
effect separately from the node effect.

### 16.5 Common evaluable territory

The strongest opportunity-qualified comparison SHALL define a common evaluable
territory as:

```text
governed WES target territory
    intersected with
WGS sufficiently interrogated or callable territory
```

The implementation SHALL preserve the interval identities, reference assembly,
thresholds, tools, and hashes used to construct that intersection.

Certification C SHOULD distinguish:

```text
common territory
    WES and WGS evidence over approximately comparable genomic opportunity

expanded territory
    WGS evidence outside the governed WES target territory
```

If an interval-level WES target or WGS callable substrate is unavailable, exact
common-territory recurrence and density claims SHALL be omitted or narrowed.

Coverage summaries without interval-level territory MAY support descriptive
context, but SHALL NOT substitute for exact common-territory membership.

### 16.6 Valid comparative classes

The core comparison MAY evaluate:

- invariant architecture and preservation behavior;
- execution-provenance completeness;
- configuration and resource compatibility;
- genotype evidence completeness and state distributions within the emitted
  observation universe;
- semantic-routing and preservation patterns;
- WES within-corpus stability;
- WGS sibling shared/private structure;
- node and modality limitations.

The opportunity-qualified comparison MAY additionally evaluate, only where the
required denominator exists:

- normalized observation densities;
- common-territory recurrence;
- WGS expanded-territory evidence;
- gene-surface overlap and expansion;
- exact observation recurrence;
- assay-associated biological differences.

Publication comparison SHALL remain `CNTNAP2`-specific unless bounded evidence
for all intended publication candidates is present.

The comparison SHALL NOT estimate:

- diagnostic yield;
- disease prevalence;
- population association;
- causal effect;
- clinical validity;
- clinical utility;
- ACMG/AMP classification authority;
- a population-level modality effect;
- regions of homozygosity from shared homozygous variants alone.

### 16.7 Frozen-input requirement

Comparative products SHALL be derived from frozen certified evidence packages.
They SHALL NOT silently reopen canonical run directories or regenerate source
summaries under unrecorded code or schema versions.

A new source probe requested during comparative review SHALL create a versioned
amendment to the affected corpus package and may trigger recertification.

---

## 17. Output Schema and Technical State Contract

### 17.1 Common field semantics

Shared fields SHALL have identical names, types, null semantics, units, and
meaning on sys76 and MARK.

Modality-specific fields SHALL be explicitly namespaced or documented as
additive.

An absent value SHALL be distinguishable from zero, false, not applicable, and
not observed.

Shared schemas SHALL include machine-readable fields for:

- observation-universe definition;
- rarity-definition identity;
- assay-opportunity availability;
- callable-definition identity;
- common-territory eligibility;
- exact membership-surface version.

### 17.2 Required technical states

DEX-VAP MAY assign only technical states such as:

```text
EXTRACTION_COMPLETE
EXTRACTION_INCOMPLETE
PROBE_PASS
PROBE_FAIL
ARTIFACT_PRESENT
ARTIFACT_MISSING
HASH_MATCH
HASH_MISMATCH
BYTE_IDENTICAL
BYTE_DIFFERENT
SCHEMA_VALID
SCHEMA_INVALID
RECONCILED
UNRECONCILED
UNRESOLVED
NOT_APPLICABLE
BLOCKED_PENDING_DISCOVERY
UNAVAILABLE_WITH_EXPLICIT_LIMITATION
PACKAGE_VERIFIED
PACKAGE_INVALID
```

### 17.3 Reserved scientific outcomes

The following remain reserved for SAGE-VAP:

```text
Per run:
    CERTIFIED
    CERTIFIED WITH NOTES
    INSUFFICIENT EVIDENCE
    NOT CERTIFIED

Per corpus:
    CORPUS CERTIFIED
    CORPUS CERTIFIED WITH NOTES
    CORPUS PARTIALLY CERTIFIED
    CORPUS INSUFFICIENT EVIDENCE
    CORPUS NOT CERTIFIED

Comparative:
    COMPARISON CERTIFIED
    COMPARISON CERTIFIED WITH NOTES
    COMPARISON INSUFFICIENT EVIDENCE
    COMPARISON NOT CERTIFIED
```

DEX outputs SHALL NOT preempt or simulate these outcomes.

---

## 18. Evidence Directory and Package Contract

Certification-grade evidence SHALL reside under:

```text
docs/validation/comparisons/
```

The three objective-oriented namespaces are:

```text
docs/validation/comparisons/

    sys76_wes_genotype_aware_execution_provenance/

    mark_wgs_genotype_aware_execution_provenance/

    wes_wgs_genotype_aware_comparison/
```

Each namespace SHALL preserve, as applicable:

- locked corpus manifest;
- per-run evidence packages;
- extraction manifests;
- extraction receipts;
- command records;
- probe-source identities;
- artifact hashes;
- logs;
- technical readiness summaries;
- anomaly register;
- unresolved-question register;
- targeted-probe outputs;
- corpus aggregation;
- SAGE-VAP review materials;
- final SAGE-VAP certification determination committed as a durable validation
  record;
- frozen-package receipt.

Large canonical run artifacts SHALL remain outside Git in their governed
locations and SHALL be referenced by identity, path, size, hash, and bounded
summaries.

---

## 19. Manifest, Receipt, and Hash Contract

### 19.1 Extraction manifest

Every execution package SHALL include a machine-readable manifest identifying:

- certification object;
- source node;
- source run and TEP-VAP identities;
- source paths;
- extractor and probe identities;
- requested evidence products;
- output paths;
- output schema versions.

### 19.2 Execution receipt

Every execution package SHALL include a machine-readable receipt recording:

- command line;
- working directory;
- start and finish timestamps;
- exit status;
- host and environment identity;
- Git `HEAD`, branch, and working-tree state;
- probe SHA-256;
- source-artifact hashes used by the probe;
- output-artifact sizes and hashes;
- warnings, failures, and unresolved states;
- temporary-workspace disposition.

### 19.3 Hashing policy

Full SHA-256 SHALL be computed for:

- all transported certification outputs;
- extraction manifests and receipts;
- execution provenance and configuration snapshots;
- genotype artifact pairs requiring direct transport identity;
- inventory and lineage manifests;
- opportunity interval or callable-mask artifacts used for denominators;
- compact exact membership surfaces;
- frozen evidence archives;
- other critical artifacts identified in the active implementation plan.

The system SHOULD avoid hashing every large intermediate artifact unless the
hash supports a defined certification claim.

### 19.4 Byte-identity policy

Where direct transport identity is required, the probe SHOULD record both:

```text
cryptographic hash equality
and
bytewise comparison result
```

A size match alone is insufficient.

---

## 20. Failure, Restart, and Idempotency Contract

### 20.1 Atomic output publication

Each output SHALL be written to a temporary path and atomically renamed only
after successful completion and validation.

Partial outputs SHALL NOT be presented as canonical certification evidence.

### 20.2 Failure visibility

A failed probe SHALL emit, when technically possible:

- nonzero exit status;
- failure receipt;
- completed-step inventory;
- error summary;
- partial-output disposition;
- restart recommendation.

### 20.3 Restart behavior

A restart SHALL either:

- resume from explicitly validated checkpoints; or
- create a new timestamped execution package.

It SHALL NOT silently append to or overwrite a reviewed package.

### 20.4 Deterministic regeneration

Given unchanged source artifacts, code, configuration, and environment, a probe
SHOULD regenerate semantically and bytewise identical outputs where the output
schema does not intentionally include volatile timestamps or paths.

Volatile fields SHALL be isolated from scientific comparison or explicitly
normalized.

---

## 21. Performance and Resource-Safety Contract

The evidence-acquisition system SHALL minimize impact on production nodes.

It SHALL:

- use streaming reads for high-cardinality TSV or VCF evidence where practical;
- avoid loading complete WGS genotype tables into memory without necessity;
- avoid repeated full-file scans when one governed pass can compute multiple
  required summaries;
- record file sizes and estimated I/O burden before high-cost execution;
- support bounded temporary storage;
- avoid altering or locking canonical artifacts in ways that affect production;
- expose progress and terminal failure clearly;
- keep transported outputs compact enough for the governed MARK-to-sys76 path.

High-cost joins MAY use external sort, SQLite, DuckDB, or an equivalent
node-local method when source identity and deterministic semantics are
preserved.

---

## 22. Edge-Case Contract

The implementation and evidence schema SHALL explicitly preserve or expose:

- missing genotype versus homozygous reference;
- partial no-calls;
- single-allele call states without automatic haploid inference;
- phased and unphased calls;
- multiallelic records;
- spanning-deletion alleles;
- symbolic or malformed records;
- duplicate or repeated source records;
- FORMAT/sample length mismatches;
- absent optional caller fields;
- deferred variant relationships;
- TEP-VAP rebuild or version drift;
- Stage 13 self-reference timing artifacts;
- source-state traceability limitations;
- biological outliers;
- expected WGS noncoding expansion;
- publication notation inconsistencies;
- unresolved pedigree mapping;
- unresolved WES assay identity;
- absent or incompatible target intervals;
- absent callable masks;
- inconsistent coverage thresholds;
- missing opportunity denominators;
- frequency unknown versus rare;
- emitted-observation versus callable-locus universe.

An edge case SHALL NOT be silently coerced into an easier semantic category.

---

## 23. Active Documentation and Churn-Control Contract

This certification mission SHALL maintain exactly two active control documents:

```text
docs/contracts/system/validation/
    genotype_aware_wes_wgs_certification_validation_contract.md

docs/plans/infrastructure/active/
    genotype_aware_wes_wgs_certification_implementation_plan.md
```

The contract defines binding obligations.

The implementation plan defines current sequencing, work packages, probe
inventory, requirement coverage, schemas, commands, status, decisions, and
open questions.

The following logical products SHALL be maintained as sections or controlled
tables within the active implementation plan rather than as additional active
planning documents:

- requirement-to-evidence coverage matrix;
- extractor and probe inventory;
- common output-schema proposal;
- execution sequence;
- open-question register;
- status ledger;
- decision log;
- add/commit sequence.

Generated evidence artifacts, receipts, manifests, and SAGE determinations MAY
exist under `docs/validation/comparisons/` because they are certification
records rather than competing active plans.

A new active control document SHALL require an explicit governance reason and
repository-owner authorization.

---

## 24. Contract Conformance Gates

### Gate 1 — Planning readiness

The active implementation plan SHALL:

- map every governing requirement to an evidence disposition;
- lock the 14-member corpus identities or mark unresolved identities explicitly;
- define common field semantics;
- inventory reusable and new probes;
- distinguish all-member and targeted execution;
- define node-local commands and destinations;
- define manifests, receipts, and hashes;
- document mutation safeguards;
- separate scientific questions from implementation decisions;
- incorporate SAGE-VAP's resolved scientific conditions;
- be reviewable by SAGE-VAP without access to large canonical artifacts.

### Gate 2 — Scientific substrate discovery

Before broad extraction, DEX-VAP SHALL inventory the governed substrate for:

- WES library-preparation and assay identity;
- WES target or bait intervals;
- consistency of design across the 12 WES-designated runs;
- ENA `AMPLICON` metadata and repository WES designation;
- WES target-depth and threshold-coverage evidence;
- WGS depth and threshold-coverage evidence;
- WGS callable masks or callable-region evidence;
- mapping and duplication context;
- exact compact gene- and variant-membership derivation;
- common-territory feasibility.

Every unavailable substrate SHALL receive
`UNAVAILABLE_WITH_EXPLICIT_LIMITATION` or `BLOCKED_PENDING_DISCOVERY`.

Gate 2 does not require every denominator to exist. It requires that
availability and claim consequences are known before Certification C is
constructed.

### Gate 3 — Extractor readiness

Before corpus execution, the common extractor SHALL:

- pass its test suite;
- parse representative WES and WGS schemas;
- be calibrated against ERR10619300;
- produce deterministic manifests and receipts;
- enforce read-only source behavior;
- expose partial failure;
- record source and implementation identities;
- prove exact observation-ID uniqueness;
- emit the observation-universe and rarity definitions;
- emit compact exact membership surfaces;
- report opportunity-denominator availability without fabrication.

### Gate 4 — Per-run technical completion

A run reaches `EXTRACTION_COMPLETE` only when all required common evidence
classes have either:

- completed successfully;
- been explicitly marked `NOT_APPLICABLE`;
- been marked `UNRESOLVED` with a recorded reason and SAGE-visible consequence;
  or
- been marked `UNAVAILABLE_WITH_EXPLICIT_LIMITATION` where the absent evidence
  narrows comparative claims without invalidating producer certification.

Foundational identity, preservation, genotype, inventory, and lineage checks
SHALL NOT be waived through the limitation state.

### Gate 5 — Corpus technical completion

A corpus reaches technical completion only when:

- every member is represented;
- no member is silently omitted;
- all per-run package hashes reconcile;
- corpus aggregation completes;
- exact membership-package identities are recorded;
- opportunity-denominator availability is summarized;
- anomalies and unresolved questions are visible;
- targeted-probe coverage is recorded;
- SAGE-VAP has sufficient evidence to issue a corpus determination.

### Gate 6 — Frozen corpus readiness

A corpus is eligible for the complete 12-versus-2 comparison only after:

- SAGE-VAP issues `CORPUS CERTIFIED` or `CORPUS CERTIFIED WITH NOTES`;
- the reviewed package is frozen;
- hashes and version identities are recorded;
- the durable SAGE certification record is committed;
- replacement and revalidation rules are active.

A partially certified corpus requires a separately bounded comparison object.

### Gate 7 — Comparative readiness

Certification C begins only when:

- both corpus packages satisfy Gate 6;
- the compatibility audit completes;
- the observational-unit structure is preserved;
- observation-universe definitions are explicit;
- rarity definitions reconcile;
- comparison-limiting and blocking differences are visible;
- comparative outputs derive from the frozen packages;
- exact membership evidence supports every recurrence or overlap claim;
- opportunity-denominator availability defines the permitted biological claims;
- common-territory construction is either completed or explicitly unavailable;
- publication claims are bounded to the candidates actually traced;
- SAGE-VAP can distinguish architecture, modality, node, family structure,
  assay opportunity, and biological variation.

---

## 25. Revalidation Triggers

A prior evidence package or certification SHALL be reconsidered when any of the
following changes:

- genotype projection implementation;
- execution-provenance implementation or schema;
- configuration snapshot structure;
- Stage 07 annotation behavior;
- Stage 08 routing or normalization behavior;
- Stage 09–12 overlay behavior;
- genotype-observation schema;
- reference assembly or FASTA;
- aligner, caller, or normalization policy;
- VEP, cache, transcript policy, or annotation resources;
- population, clinical, or gene-set resources;
- multiallelic relationship policy;
- TEP-VAP entity paths;
- TEP-VAP builder or validator;
- run or TEP-VAP replacement;
- regeneration of a certified TEP-VAP;
- extractor or probe semantics;
- common output schema;
- compact membership schema or derivation semantics;
- WES assay or target design;
- WGS callable mask or callable definition;
- coverage thresholds or opportunity denominator;
- common-territory construction;
- rarity definition;
- corpus membership;
- governed pedigree mapping;
- discovery of a material certification defect.

The active implementation plan SHALL record the evidence needed to detect these
triggers.

---

## 26. Non-Goals and Scientific Boundaries

This contract does not establish:

- clinical analytical validation;
- clinical diagnostic validity;
- clinical utility;
- ACMG/AMP classification authority;
- disease causality;
- segregation across unavailable relatives;
- population association;
- prevalence;
- diagnostic yield;
- independence of the two WGS siblings;
- a pure hardware effect;
- a pure modality effect;
- universal compatibility with every assay, caller, or schema;
- universal cross-version determinism;
- inferential significance testing across the current WES and WGS corpora;
- treatment of the two siblings as independent replicates;
- pooling the 14 runs as one homogeneous cohort;
- variant-density claims without governed opportunity denominators;
- genome-wide genotype burden from emitted variant observations;
- ROH reconstruction without an independently governed ROH substrate;
- publication-wide concordance from a `CNTNAP2`-only trace.

The program is observational, preservation-centered, architecture-centered, and
opportunity-qualified where denominator evidence permits.

---

## 27. Change Control

This v0.2 revision incorporates SAGE-VAP's 2026-08-06
`APPROVE WITH SCIENTIFIC CONDITIONS` determination.

A contract change SHALL record:

- contract version;
- change date;
- changed requirement;
- reason;
- affected certification objects;
- affected evidence packages;
- whether re-extraction or recertification is required;
- SAGE-VAP review status;
- repository-owner authorization where the change alters scope or authority.

Implementation detail MAY evolve through the active implementation plan so long
as this contract's semantics and scientific boundaries remain unchanged.

---

## 28. Success Condition

This contract is fulfilled when the certification system has produced:

```text
a complete, reviewed, and frozen
12-member sys76 WES certification evidence package

and

a complete, reviewed, and frozen
2-member MARK WGS certification evidence package

and

a controlled comparative evidence package
constructed from those frozen certified corpora

with:

    explicit observation-universe boundaries
    exact compact membership substrate
    opportunity denominators where governed and available
    a common evaluable territory where technically supportable
    claims narrowed wherever those substrates are unavailable
```

and when SAGE-VAP has sufficient evidence to issue:

```text
Certification A
Certification B
Certification C
```

with all limitations, unresolved questions, and revalidation triggers preserved.

Completion of DEX-VAP evidence acquisition does not itself constitute
scientific certification.

---

## 29. Final Contract Statement

VAP SHALL preserve producer evidence.

TEP-VAP SHALL transport that evidence without reinterpretation.

DEX-VAP SHALL gather deterministic, bounded, non-mutating certification
evidence from the nodes where canonical data reside.

SAGE-VAP SHALL determine what that evidence scientifically supports.

The WES and WGS corpora SHALL be certified independently before comparison.

The comparative certification SHALL consume frozen certified evidence packages
and SHALL preserve modality, node, relatedness, uncertainty, lineage,
observation-universe, assay-opportunity, and producer-authority boundaries.

Raw count differences SHALL remain descriptive until governed denominators
support stronger interpretation.

Exact recurrence, overlap, expansion, and publication claims SHALL be grounded
in compact hash-bound membership evidence rather than aggregate counts alone.
