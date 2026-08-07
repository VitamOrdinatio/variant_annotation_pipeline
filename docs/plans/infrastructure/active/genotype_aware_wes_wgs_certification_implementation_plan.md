# Genotype-Aware WES/WGS Certification Implementation Plan

| Field | Value |
|---|---|
| Document status | Draft v0.2 — SAGE scientific conditions incorporated; implementation pending |
| Plan class | Active infrastructure implementation plan |
| Repository | `variant_annotation_pipeline` |
| Controlling contract | `docs/contracts/system/validation/genotype_aware_wes_wgs_certification_validation_contract.md` |
| Scientific authority | SAGE-VAP |
| Engineering and evidence-acquisition authority | DEX-VAP |
| Scientific review disposition | `APPROVE WITH SCIENTIFIC CONDITIONS` — incorporated in v0.2 |
| WES certification object | 12 genotype-aware WES-designated PRJEB57558 runs on sys76 |
| WGS certification object | 2 genotype-aware epilepsy WGS runs on MARK |
| Comparative certification object | Independently certified 12-run WES corpus versus independently certified 2-run WGS corpus |
| Existing certified calibration exemplar | `ERR10619300 / run_2026_07_14_114546` |
| MARK governed output boundary | `/root/Desktop/` |
| Clinical boundary | Research and portfolio validation only; not clinical validation |

---

## 1. Purpose

This plan defines the implementation sequence for the complete VAP
Genotype-Aware WES/WGS certification mission.

SAGE-VAP reviewed Draft v0.1 and issued:

```text
APPROVE WITH SCIENTIFIC CONDITIONS
```

Draft v0.2 incorporates those conditions while preserving the original system
architecture and authority boundaries.

The mission has three separate scientific certification objectives:

```text
Certification A
    certify the complete 12-member
    genotype-aware WES-designated PRJEB57558 corpus on sys76

Certification B
    certify the complete 2-member
    genotype-aware epilepsy WGS corpus on MARK

Certification C
    compare the independently certified
    12-member WES corpus
        against
    the independently certified
    2-member WGS corpus
    and certify the controlled comparison
```

Certification C contains two related but distinct comparative layers:

```text
core preservation-centered comparison
    architecture
    execution provenance
    genotype-observation integrity
    Stage preservation
    TEP transport
    inventory and lineage
    descriptive emitted-observation composition

opportunity-qualified biological comparison
    assay opportunity
    coverage and callability denominators
    common evaluable territory
    exact gene and variant membership
    recurrence, overlap, expansion, and normalized density
```

The core comparison may proceed when Certifications A and B are independently
certified and frozen. Opportunity-qualified claims may proceed only where the
required governed denominator and exact-membership substrate exists.

The implementation shall build one reusable certification system rather than a
collection of sample-specific probes.

The intended dependency is:

```text
locked corpus identity
    ↓
scientific-substrate discovery
    ↓
common evidence schema
    ↓
common manifest-driven extractor
    ↓
per-run technical evidence
    ↓
SAGE per-run determinations
    ↓
corpus aggregation
    ↓
SAGE corpus determinations
    ↓
frozen certified corpus packages
    ↓
controlled compatibility and opportunity gate
    ↓
comparative evidence products
    ↓
SAGE comparative determination
```

No comparative result may compensate for an uncertified source run or source
corpus.

## 2. Relationship to the Controlling Contract

This plan implements:

```text
docs/contracts/system/validation/
    genotype_aware_wes_wgs_certification_validation_contract.md
```

The contract is authoritative if this plan and the contract conflict.

This v0.2 plan is intended to conform to the SAGE-reviewed v0.2 contract,
including its requirements for:

- exact all-member observation-ID uniqueness;
- emitted-observation-universe semantics;
- governed rarity definitions;
- assay-opportunity discovery;
- compact exact membership surfaces;
- common-territory construction where feasible;
- bounded publication claims;
- comparison-ready corpus outcomes;
- durable SAGE certification records.

This plan may change sequencing, module boundaries, command structure, or
performance strategy without changing the contract's scientific semantics.

A change that alters corpus identity, evidence meaning, certification scope,
authority boundaries, or preservation doctrine requires contract review.

Unavailable assay-opportunity evidence may narrow Certification C claims
without blocking Certifications A or B, provided every foundational producer,
genotype, preservation, inventory, lineage, and transport requirement is met.

## 3. Governing Sources

This plan is grounded in:

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
```

It also incorporates the SAGE-VAP scientific review determination on Draft
v0.1:

```text
APPROVE WITH SCIENTIFIC CONDITIONS
```

That determination resolved the prior scientific open questions and added
conditions governing assay opportunity, common territory, exact membership,
rarity, observation-universe language, publication scope, and comparison-ready
corpus states.

The existing ERR10619300 certification dossier remains the empirical
calibration precedent for the common producer-certification surface.

## 4. Locked Scientific and Operational Boundaries

The implementation shall not reopen the following doctrine.

### 4.1 Observation authority

Stage 07 is the authoritative biological observation anchor.

Stages 08–13 organize or overlay evidence but do not replace Stage 07.

### 4.2 Genotype authority

Genotype observations are first-class producer evidence.

The extractor shall preserve existing source context and shall not infer:

- inheritance mode;
- carrier status;
- compound heterozygosity;
- de novo status;
- hemizygosity;
- heteroplasmy;
- negative evidence;
- callability;
- disease causality;
- diagnosis.

### 4.3 Missingness authority

Missing genotype and partial no-call states shall remain distinct from
homozygous reference.

The absence of a producer row shall not be narrated as absence of a variant,
callability, assay opportunity, or negative evidence.

### 4.4 Emitted-observation-universe authority

Genotype-state proportions describe genotype observations present in the
VAP-emitted variant universe.

They do not describe:

- all callable loci;
- genome-wide genotype proportions;
- homozygous-reference burden;
- evidence that an unrepresented variant is absent;
- assay opportunity.

Every genotype-distribution product shall carry the machine-readable boundary:

```text
VAP_EMITTED_VARIANT_OBSERVATION_UNIVERSE
```

or an explicitly versioned equivalent.

### 4.5 Rarity authority

The primary certification rarity definition is the governed VAP frequency
classification produced consistently across the 14 runs.

The publication comparator may additionally use:

```text
MAF <= 0.001
```

only to reconstruct Badshah et al. filtering logic.

The implementation shall keep these states distinct:

```text
VAP_GOVERNED_RARE
PUBLICATION_THRESHOLD_RARE
FREQUENCY_UNKNOWN
FREQUENCY_UNAVAILABLE
NOT_RARE
```

Unknown or unavailable frequency shall not be converted to rare.

### 4.6 Execution-provenance authority

These are independent required artifacts:

```text
metadata/execution_provenance.json
metadata/config_snapshot.yaml
```

Their TEP copies shall be evaluated independently.

### 4.7 Transport authority

TEP-VAP transports producer-authored evidence without reinterpretation.

Where direct transport identity is required, source and TEP artifacts shall be
checked by cryptographic hash and bytewise comparison.

### 4.8 Ecosystem boundary

```text
VAP
    preserves producer observations and semantic states

TEP-VAP
    transports those states

VDB
    validates, relates, brokers namespaces additively, and persists

RDGP
    performs downstream statistical, phenotype, and inheritance reasoning
```

The certification extractor shall not add VDB or RDGP conclusions.

### 4.9 Assay-opportunity authority

Raw observation counts shall not be interpreted as variant density, biological
yield, or modality-associated burden without a governed opportunity
denominator.

The implementation shall discover and preserve, where available:

- assay and library-preparation identity;
- WES target or bait intervals;
- WGS callable or interrogated territory;
- interval and mask hashes;
- total opportunity bases;
- depth and coverage-threshold summaries;
- mapping and duplication context;
- callable definitions and tool identities.

Unavailable opportunity substrate shall remain explicit and narrow comparison
claims. It shall not be silently reconstructed.

### 4.10 Observational-unit and confounding authority

The 14 executions are not one homogeneous cohort.

The comparison shall preserve:

```text
12 individual unrelated WES-designated PRJEB57558 runs
2 individual related WGS sibling runs
```

The two WGS siblings shall be displayed separately and may additionally receive
a family-level shared/private summary. They shall not be treated as independent
replicates.

The implementation shall not perform inferential WES-versus-WGS significance
testing, estimate a population-level modality effect, separate modality from
node effects, or report one pooled 14-run mean as though the sampling structure
were uniform.

### 4.11 Publication boundary

The Badshah et al. publication is an external comparator, not a truth set.

The two WGS individuals are affected brothers. They shall not be described as
biological twins.

The mapping of `SRR13573587` and `SRR13573588` to publication individuals
`V-2` and `V-4` remains unknown unless governed evidence resolves it.

A targeted `CNTNAP2` trace supports only a `CNTNAP2`-specific publication claim.
Publication-wide candidate concordance requires bounded traces for every
reported candidate intended to support that claim:

```text
PDZD7
ALG6
RBM20
CNTNAP2
```

Shared homozygous observations are not equivalent to independently governed
regions-of-homozygosity evidence.

## 5. Program Architecture

### 5.1 One certification system

The implementation target is:

```text
one locked 14-member corpus manifest
one common field vocabulary
one manifest-driven command-line interface
one tested certification library
one receipt and package format
one core all-member certification surface
one comparative-opportunity extension
modality-specific additive probes
corpus aggregators
comparison tools that consume frozen certified packages
```

The implementation shall not create fourteen independent sample-specific probe
systems.

### 5.2 Two-layer evidence model

The code and schemas shall distinguish:

```text
core all-member certification surface
    required for all 14 runs
    supports Certifications A and B

comparative-opportunity extension
    collected where governed and available
    supports opportunity-qualified Certification C claims
```

The following foundational checks are mandatory for all 14 runs and are not
representative-only:

- observation-ID completeness;
- exact within-run observation-ID uniqueness;
- duplicate-identity detection;
- called-allele-index validity;
- missing and partial-call preservation;
- processed-to-TEP byte identity;
- Stage 07 preservation;
- inventory closure;
- lineage closure.

### 5.3 Proposed code layout

The preferred implementation layout is:

```text
src/certification/
    __init__.py
    models.py
    manifest.py
    discovery.py
    scientific_substrate.py
    provenance.py
    configuration.py
    genotype.py
    opportunity.py
    membership.py
    stage_reconciliation.py
    tep.py
    sanity.py
    traces.py
    corpus.py
    wgs_siblings.py
    publication_candidates.py
    compatibility.py
    common_territory.py
    comparison.py
    receipts.py
    packaging.py

scripts/validation/
    run_genotype_aware_certification.py

tests/certification/
    test_manifest.py
    test_discovery.py
    test_scientific_substrate.py
    test_provenance.py
    test_configuration.py
    test_genotype.py
    test_opportunity.py
    test_membership.py
    test_stage_reconciliation.py
    test_tep.py
    test_receipts.py
    test_wgs_siblings.py
    test_publication_candidates.py
    test_corpus.py
    test_compatibility.py
    test_common_territory.py
    test_comparison.py
```

The exact module split may be simplified during implementation if field
semantics, testability, deterministic behavior, and the two-layer evidence
boundary remain unchanged.

### 5.4 Proposed command surface

A single CLI should expose explicit subcommands:

```text
discover-scientific-substrate
preflight
extract-run
build-membership
aggregate-corpus
compare-wgs-siblings
trace-publication-candidates
build-compatibility-audit
build-common-territory
compare-certified-corpora
package-evidence
verify-package
```

Illustrative invocation:

```bash
python scripts/validation/run_genotype_aware_certification.py \
  preflight \
  --corpus-manifest config/certification/genotype_aware_wes_wgs_corpus_v1.tsv \
  --corpus-id mark_wgs_v1 \
  --output-root /root/Desktop/vap_certification
```

The final CLI syntax shall be frozen before production extraction.

### 5.5 Locked input manifest

The implementation shall introduce one machine-readable corpus manifest:

```text
config/certification/
    genotype_aware_wes_wgs_corpus_v1.tsv
```

Required fields:

```text
program_id
certification_object
corpus_id
sample_id
run_id
assay_type
assay_designation
node_id
read_count_stratum
scientific_description
canonical_run_path
canonical_tep_path
tep_id
library_strategy_state
target_design_id
target_interval_path
target_interval_sha256
callable_mask_path
callable_mask_sha256
opportunity_evidence_state
prior_certification_state
prior_certification_reference
identity_state
notes
```

Initially unresolved paths, TEP IDs, assay identities, target intervals,
callable masks, or denominator states shall be represented explicitly as:

```text
UNRESOLVED_PENDING_PREFLIGHT
BLOCKED_PENDING_DISCOVERY
UNAVAILABLE_WITH_EXPLICIT_LIMITATION
```

They shall not be inferred silently.

Any later corpus identity change requires a new manifest version.

## 6. Locked Corpus Identity

### 6.1 Certification A — sys76 WES-designated corpus

| Sample/SRA | Run ID | Stratum | Current certification role |
|---|---|---|---|
| `ERR10619203` | `run_2026_07_15_204807` | q3 | pending per-run evidence |
| `ERR10619207` | `run_2026_07_16_021033` | q3 | pending per-run evidence |
| `ERR10619208` | `run_2026_07_16_055657` | median | pending per-run evidence |
| `ERR10619212` | `run_2026_07_15_105505` | q1 | pending per-run evidence |
| `ERR10619225` | `run_2026_07_15_164104` | q3 | pending per-run evidence |
| `ERR10619230` | `run_2026_07_16_122454` | q3 | pending per-run evidence |
| `ERR10619241` | `run_2026_07_16_161908` | q1 | pending per-run evidence |
| `ERR10619281` | `run_2026_07_16_215236` | median | pending per-run evidence |
| `ERR10619285` | `run_2026_07_17_015849` | median | pending per-run evidence |
| `ERR10619300` | `run_2026_07_14_114546` | median | existing certified calibration exemplar |
| `ERR10619309` | `run_2026_07_17_065031` | q1 | pending per-run evidence |
| `ERR10619330` | `run_2026_07_17_115119` | q1 | pending per-run evidence |

Until governed evidence resolves library preparation and target design, these
shall be described as:

```text
WES-designated PRJEB57558 runs
```

The q1, median, and q3 labels are project-specific read-count strata, not direct
measurements of target coverage.

### 6.2 Certification B — MARK WGS

| Sample/SRA | Run ID | Scientific description | Current certification role |
|---|---|---|---|
| `SRR13573587` | `run_2026_07_29_123020` | affected sibling WGS | pending per-run evidence |
| `SRR13573588` | `run_2026_08_01_092338` | affected sibling WGS | pending per-run evidence |

### 6.3 Certification C — comparison object

Certification C shall consume only frozen, SAGE-reviewed corpus packages.

The complete 12-versus-2 comparison may consume only corpora with:

```text
CORPUS CERTIFIED
CORPUS CERTIFIED WITH NOTES
```

A partially certified corpus may support only a separately named and explicitly
narrowed partial comparison.

Raw run directories shall not be reopened as uncontrolled comparative inputs
once the two corpus packages have been frozen.

## 7. Evidence Disposition Strategy

Every requirement shall use one of six dispositions:

```text
AVAILABLE_DIRECTLY
    present as a small canonical or TEP artifact

AVAILABLE_BY_EXISTING_EXTRACTOR
    emitted by an existing lightweight utility

AVAILABLE_BY_EXISTING_PROBE
    supported by existing validation logic or a prior receipt pattern

NEW_BOUNDED_PROBE_REQUIRED
    requires new observational node-local computation

BLOCKED_PENDING_DISCOVERY
    source path, package identity, assay identity, or governed substrate
    has not yet been resolved

UNAVAILABLE_WITH_EXPLICIT_LIMITATION
    governed evidence is absent and the missing substrate narrows the
    permissible comparative claim without being fabricated
```

`NOT_APPLICABLE` may additionally be used where a requirement is scientifically
inapplicable to a certification object.

Existing logic may be refactored into the common library without changing the
scientific meaning of its output.

The generic small-file exporter remains a secondary transport utility. It is
not the certification extractor because it does not establish the required
semantics of skipped high-cardinality artifacts.

Every unavailable denominator or interval substrate shall state whether it:

- blocks a foundational producer-certification claim;
- limits only opportunity-qualified Certification C claims;
- prevents exact common-territory recurrence;
- prevents publication-wide or other highlighted claims.

## 8. Requirement-to-Evidence Coverage Matrix

| ID | Object | Evidence requirement | Disposition | Scope | Primary source | Planned implementation/output | Blocking if absent |
|---|---|---|---|---|---|---|---|
| GOV-001 | A/B/C | Locked member identity | AVAILABLE_DIRECTLY | all 14 | governing documents and corpus manifest | `genotype_aware_wes_wgs_corpus_v1.tsv` | yes |
| GOV-002 | A/B | Canonical run path and TEP path | NEW_BOUNDED_PROBE_REQUIRED | all 14 | node-local filesystem | preflight discovery table | yes |
| GOV-003 | A/B | Repository source state | AVAILABLE_BY_EXISTING_PROBE | batch/node | Git receipts | repository-state receipt | yes |
| GOV-004 | A/B/C | Probe source and schema identity | NEW_BOUNDED_PROBE_REQUIRED | every execution | Git and script files | receipt fields and script hashes | yes |
| ID-001 | A/B | Sample and run identity agreement | AVAILABLE_DIRECTLY | all 14 | run metadata, config, TEP inventory | per-run identity audit | yes |
| ID-002 | A/B | TEP identity and package version | AVAILABLE_DIRECTLY | all 14 | TEP inventory and package path | per-run identity audit | yes |
| ID-003 | A/B | Run completion state | AVAILABLE_DIRECTLY | all 14 | run metadata, stage summaries | per-run identity audit | yes |
| PROV-001 | A/B | Run-local provenance presence and JSON validity | AVAILABLE_BY_EXISTING_PROBE | all 14 | `metadata/execution_provenance.json` | provenance audit | yes |
| PROV-002 | A/B | TEP provenance presence and JSON validity | AVAILABLE_BY_EXISTING_PROBE | all 14 | `entities/context/execution_provenance.json` | provenance audit | yes |
| PROV-003 | A/B | Run-to-TEP provenance identity | AVAILABLE_BY_EXISTING_PROBE | all 14 | both provenance files | SHA-256 plus `cmp` receipt | yes |
| PROV-004 | A/B | Node, environment, reference, resource, and tool fields | AVAILABLE_BY_EXISTING_PROBE | all 14 | provenance JSON | normalized provenance field audit | yes |
| PROV-005 | A/B | Early provenance initialization evidence | AVAILABLE_BY_EXISTING_PROBE | batch plus anomalies | logs, receipts, prior probe pattern | initialization-order audit | yes unless governed limitation |
| CFG-001 | A/B | Run-local config presence and YAML validity | AVAILABLE_BY_EXISTING_PROBE | all 14 | `metadata/config_snapshot.yaml` | configuration audit | yes |
| CFG-002 | A/B | TEP config presence and YAML validity | AVAILABLE_BY_EXISTING_PROBE | all 14 | `entities/metadata/config_snapshot.yaml` | configuration audit | yes |
| CFG-003 | A/B | Run-to-TEP config byte identity | AVAILABLE_BY_EXISTING_PROBE | all 14 | both config files | SHA-256 plus `cmp` receipt | yes |
| CFG-004 | A/B/C | Recoverable caller, reference, annotation, genotype, and assay settings | AVAILABLE_BY_EXISTING_PROBE | all 14 | config and provenance | normalized compatibility fields | yes |
| GEN-001 | A/B | Genotype artifact presence, size, header, and schema | NEW_BOUNDED_PROBE_REQUIRED | all 14 | processed genotype TSV | genotype integrity audit | yes |
| GEN-002 | A/B | Source-record and observation row counts | NEW_BOUNDED_PROBE_REQUIRED | all 14 | genotype TSV and summary JSON | genotype integrity audit | yes |
| GEN-003 | A/B | Full and partial no-call preservation | NEW_BOUNDED_PROBE_REQUIRED | all 14 | genotype TSV | GT-state distribution | yes |
| GEN-004 | A/B | Phased and unphased distributions | NEW_BOUNDED_PROBE_REQUIRED | all 14 | genotype TSV | genotype state table | yes |
| GEN-005 | A/B | GT arity and explicit ploidy distribution | NEW_BOUNDED_PROBE_REQUIRED | all 14 | genotype TSV | genotype state table | yes |
| GEN-006 | A/B | Allele-index preservation and violations | NEW_BOUNDED_PROBE_REQUIRED | all 14 | GT, ALT, called indices | allele-index audit | yes |
| GEN-007 | A/B | FORMAT/sample length mismatches | NEW_BOUNDED_PROBE_REQUIRED | all 14 | raw FORMAT/sample fields | format integrity table | yes |
| GEN-008 | A/B | AD/DP/GQ/PL/FT availability and missingness | NEW_BOUNDED_PROBE_REQUIRED | all 14 | genotype TSV | format-field summary | yes |
| GEN-009 | A/B | Multiallelic and spanning-deletion structures | NEW_BOUNDED_PROBE_REQUIRED | all 14 | genotype TSV | relationship summary | yes |
| GEN-010 | A/B | Deterministic observation-ID completeness and exact within-run uniqueness | NEW_BOUNDED_PROBE_REQUIRED | all 14 | genotype TSV | exact uniqueness, duplicate count, and bounded duplicate exemplars | yes |
| GEN-011 | A/B | Source VCF/header hashes and sample-column identity | AVAILABLE_DIRECTLY | all 14 | genotype summary and header context | genotype provenance audit | yes |
| GEN-012 | A/B | Processed-to-TEP genotype identity | AVAILABLE_BY_EXISTING_PROBE | all 14 | processed and TEP genotype artifacts | SHA-256 plus `cmp` receipt | yes |
| STG-001 | A/B | Stage 07 observation availability | AVAILABLE_BY_EXISTING_PROBE | all 14 | Stage 07 artifact and summaries | stage reconciliation audit | yes |
| STG-002 | A/B | Stage 07-to-Stage 08 identity continuity | AVAILABLE_BY_EXISTING_PROBE | all 14 | Stage 07/08 artifacts | continuity summary plus traces | yes |
| STG-003 | A/B | Coding/splice/noncoding/retained-background reconciliation | AVAILABLE_BY_EXISTING_PROBE | all 14 | Stage 08 outputs | partition reconciliation | yes |
| STG-004 | A/B | Stage 09 and 10 overlay reconciliation | AVAILABLE_BY_EXISTING_PROBE | all 14 | Stage 09/10 outputs | stage reconciliation audit | yes |
| STG-005 | A/B | Stage 11 and 12 additive overlay continuity | AVAILABLE_BY_EXISTING_PROBE | all 14 | Stage 11/12 outputs | stage reconciliation audit | yes |
| STG-006 | A/B | Unexplained observation-loss accounting | NEW_BOUNDED_PROBE_REQUIRED | all 14 | stage counts and identities | loss-accounting table | yes |
| TEP-001 | A/B | Required entity presence and role cardinality | AVAILABLE_BY_EXISTING_PROBE | all 14 | inventory and validator | TEP transport audit | yes |
| TEP-002 | A/B | Inventory consistency | AVAILABLE_BY_EXISTING_PROBE | all 14 | entity inventory | inventory audit | yes |
| TEP-003 | A/B | Required lineage edges and orphan detection | AVAILABLE_BY_EXISTING_PROBE | all 14 | lineage manifest | lineage audit | yes |
| TEP-004 | A/B | TEP validation-report status | AVAILABLE_DIRECTLY | all 14 | validation report | TEP transport audit | yes |
| TEP-005 | A/B | Genotype/provenance/config registration | AVAILABLE_BY_EXISTING_PROBE | all 14 | inventory and lineage | capability registration table | yes |
| SAN-001 | A/B | Stage-level count summaries | AVAILABLE_BY_EXISTING_PROBE | all 14 | stage summaries | scientific sanity summary | yes |
| SAN-002 | A/B | Consequence, frequency, clinical, priority, reviewability summaries | AVAILABLE_BY_EXISTING_EXTRACTOR | all 14 | small summary artifacts | normalized sanity tables | yes |
| SAN-003 | A/B | Rare and high-impact bounded summaries | AVAILABLE_BY_EXISTING_EXTRACTOR | all 14 | Stage 08–12 summaries | normalized sanity tables | yes |
| SAN-004 | A/B | Deterministic bounded record traces | NEW_BOUNDED_PROBE_REQUIRED | all 14 | canonical artifacts | trace table with selection method | yes |
| OBS-001 | A/B/C | Explicit emitted-variant-observation-universe boundary | NEW_BOUNDED_PROBE_REQUIRED | all 14 and comparisons | schema metadata | `VAP_EMITTED_VARIANT_OBSERVATION_UNIVERSE` field | yes |
| RAR-001 | A/B/C | Governed rarity definitions with frequency unknown separated | NEW_BOUNDED_PROBE_REQUIRED | all 14 and comparisons | VAP frequency classifications | rarity-definition and state audit | yes |
| OPP-001 | A/C | WES library-preparation and assay identity | BLOCKED_PENDING_DISCOVERY | all 12 WES | config, provenance, ENA/repository metadata | WES assay identity audit | no for A if qualified; limits C |
| OPP-002 | A/C | WES target or bait interval identity and total target bases | BLOCKED_PENDING_DISCOVERY | all 12 WES | governed interval resources | target-design inventory and hashes | no for A; required for exact common territory |
| OPP-003 | A/C | WES mean/median depth and >=10x/>=20x/>=30x target coverage | BLOCKED_PENDING_DISCOVERY | all 12 WES | existing QC or bounded coverage probe | per-run opportunity audit | no for A; required for density claims |
| OPP-004 | B/C | WGS interrogated/callable territory identity and total callable bases | BLOCKED_PENDING_DISCOVERY | both WGS | callable mask or governed coverage substrate | WGS opportunity audit | no for B; required for exact common territory |
| OPP-005 | B/C | WGS mean/median depth and >=10x/>=20x/>=30x genome coverage | BLOCKED_PENDING_DISCOVERY | both WGS | existing QC or bounded coverage probe | per-run opportunity audit | no for B; required for density claims |
| OPP-006 | A/B/C | Mapping and duplication context | AVAILABLE_DIRECTLY or BLOCKED_PENDING_DISCOVERY | all 14 | Stage 04/QC artifacts | normalized opportunity audit | no for A/B; contextual for C |
| MEM-001 | A/B/C | Exact compact governed gene membership | NEW_BOUNDED_PROBE_REQUIRED | all 14 | Stage 07–12 and genotype evidence | `per_run_gene_membership.tsv` | yes for gene overlap claims |
| MEM-002 | A/B/C | Exact per-gene evidence classes and observation counts | NEW_BOUNDED_PROBE_REQUIRED | all 14 | Stage 07–12 | `per_run_gene_evidence_summary.tsv` | yes for recurrent/expanded gene claims |
| MEM-003 | A/B/C | Exact compact coordinate-REF-ALT and observation-ID membership | NEW_BOUNDED_PROBE_REQUIRED | all 14 | Stage 07/genotype evidence | `per_run_variant_membership.tsv` | yes for exact recurrence claims |
| MEM-004 | C | Common-territory exact membership | NEW_BOUNDED_PROBE_REQUIRED or UNAVAILABLE_WITH_EXPLICIT_LIMITATION | two frozen corpora | interval intersection plus membership | common-territory membership tables | required for exact common-territory claims |
| PUB-001 | B/C | Bounded traces for all publication candidates used in publication-wide claims | NEW_BOUNDED_PROBE_REQUIRED | both WGS; targeted | Stage 07–12, genotype, TEP | candidate trace tables for PDZD7, ALG6, RBM20, CNTNAP2 | no for B beyond CNTNAP2; required for publication-wide claim |
| WES-001 | A | All-member completeness | NEW_BOUNDED_PROBE_REQUIRED | 12 WES | per-run packages | WES corpus manifest and readiness table | yes |
| WES-002 | A | q1/median/q3 genotype summaries | NEW_BOUNDED_PROBE_REQUIRED | 12 WES | per-run evidence | stratum genotype summary | yes |
| WES-003 | A | q1/median/q3 semantic summaries | NEW_BOUNDED_PROBE_REQUIRED | 12 WES | per-run evidence | stratum semantic summary | yes |
| WES-004 | A | WES outlier register | NEW_BOUNDED_PROBE_REQUIRED | 12 WES | corpus summaries | member outlier register | yes |
| WES-005 | A | Representative high-cost audit | NEW_BOUNDED_PROBE_REQUIRED | ERR10619212 q1; ERR10619300 median/exemplar; ERR10619225 q3; plus anomalies | canonical artifacts | targeted probe manifest and outputs | yes for predetermined representatives |
| WGS-001 | B | Chromosome-level observation and semantic counts | NEW_BOUNDED_PROBE_REQUIRED | both WGS | genotype and stage artifacts | WGS chromosome summary | yes |
| WGS-002 | B | WGS scale and large-artifact transport status | NEW_BOUNDED_PROBE_REQUIRED | both WGS | file metadata and hashes | WGS scale summary | yes |
| WGS-003 | B | Shared/private sibling observations | NEW_BOUNDED_PROBE_REQUIRED | WGS pair | coordinate/allele identities | sibling comparison summary | yes |
| WGS-004 | B | Shared identical and discordant genotype states | NEW_BOUNDED_PROBE_REQUIRED | WGS pair | genotype observations | sibling genotype comparison | yes |
| WGS-005 | B | Shared homozygous alternate observations | NEW_BOUNDED_PROBE_REQUIRED | WGS pair | genotype observations | bounded summary and exemplars | yes |
| WGS-006 | B | Shared VAP-governed rare homozygous observations | NEW_BOUNDED_PROBE_REQUIRED | WGS pair | genotype and governed frequency fields | bounded summary with frequency-unknown separated | yes |
| WGS-007 | B | Shared complex/deferred relationships | NEW_BOUNDED_PROBE_REQUIRED | WGS pair | genotype observations | complex relationship summary | yes |
| WGS-008 | B | Hierarchical `CNTNAP2` coordinate/protein/transcript trace | NEW_BOUNDED_PROBE_REQUIRED | both WGS | Stage 07–12, genotype, TEP | trace TSV and report with genomic, protein, transcript, and notation states | yes |
| WGS-009 | B | Pedigree identity mapping | AVAILABLE_DIRECTLY or UNRESOLVED | WGS pair | governed metadata | identity mapping table | no if explicitly unknown |
| CMP-001 | C | Frozen WES and WGS package identity | AVAILABLE_DIRECTLY | two corpora | frozen receipts | comparative input manifest | yes |
| CMP-002 | C | Source-state and configuration compatibility | NEW_BOUNDED_PROBE_REQUIRED | two corpora | frozen evidence | compatibility audit | yes |
| CMP-003 | C | Reference, tool, resource, and schema compatibility | NEW_BOUNDED_PROBE_REQUIRED | two corpora | frozen evidence | compatibility audit | yes |
| CMP-004 | C | Node/modality difference classification | NEW_BOUNDED_PROBE_REQUIRED | two corpora | compatibility audit | difference classification | yes |
| CMP-005 | C | Absolute and opportunity-qualified preservation comparisons | NEW_BOUNDED_PROBE_REQUIRED | two corpora | frozen summaries and denominator evidence | preservation comparison with claim-scope state | yes for core; denominator-dependent for normalized claims |
| CMP-006 | C | Genotype, provenance, lineage, and semantic comparisons | NEW_BOUNDED_PROBE_REQUIRED | two corpora | frozen summaries | comparative tables | yes |
| CMP-007 | C | Common evaluable territory construction | NEW_BOUNDED_PROBE_REQUIRED or UNAVAILABLE_WITH_EXPLICIT_LIMITATION | two frozen corpora | governed WES intervals and WGS callable territory | interval manifest, hashes, and territory summary | required for exact common-territory claims |
| CMP-008 | C | Exact gene and variant overlap/expansion from compact membership | NEW_BOUNDED_PROBE_REQUIRED | two frozen corpora | frozen membership surfaces | exact overlap and expansion tables | yes for recurrence/overlap claims |
| CMP-009 | C | Preserve individual-run and WGS-family observational units | NEW_BOUNDED_PROBE_REQUIRED | two corpora | frozen per-run summaries | descriptive observational-unit tables | yes |
| CERT-001 | A/B/C | Durable SAGE certification record under `docs/validation/comparisons/` | AVAILABLE_DIRECTLY after SAGE determination | each certified object | SAGE determination and frozen receipts | committed certification Markdown and review manifest | yes after certification |
| PKG-001 | A/B/C | Extraction manifest and execution receipt | NEW_BOUNDED_PROBE_REQUIRED | every execution | probe runtime | JSON manifest and receipt | yes |
| PKG-002 | A/B/C | Output hashes and command records | NEW_BOUNDED_PROBE_REQUIRED | every execution | outputs and CLI | hash ledger and commands | yes |
| PKG-003 | A/B/C | Atomic package creation and verification | NEW_BOUNDED_PROBE_REQUIRED | every package | output tree | archive, SHA-256, verification receipt | yes |
| PKG-004 | A/B/C | Failure and restart visibility | NEW_BOUNDED_PROBE_REQUIRED | every execution | probe runtime | failure receipt and checkpoint state | yes |

---

## 9. Extractor and Probe Inventory

| Utility or pattern | Current role | Reuse decision | Required change |
|---|---|---|---|
| `scripts/mark/export_lightweight_vap_runs.py` | Copies small files and emits transport manifests | retain as optional transport helper | do not use as primary certification authority |
| `scripts/validation/validate_execution_provenance.py` | Validates provenance structures | reuse logic | expose structured programmatic result and common fields |
| `scripts/tep/validate_vap_tep.py` | Validates TEP package | reuse directly or invoke as governed dependency | capture version, command, exit status, and report identity |
| `scripts/validation/audit_sys76_err10619300_run_transport_byte_identity.sh` | Checks source-to-TEP byte identity | generalize pattern | remove hard-coded run paths and expected counts |
| `scripts/validation/audit_sys76_err10619300_TEP_validation_receipts_inventory_lineage.sh` | Audits validation, inventory, and lineage | generalize pattern | emit structured TSV/JSON rather than free text only |
| `scripts/validation/audit_sys76_err10619300_tracing_initialization_order_and_test_conformance.sh` | Captures source state, initialization, and tests | reuse at batch level | separate per-node evidence from per-run evidence |
| Existing Stage 07/08/12 forensic probes | Stage continuity and partition diagnostics | reuse algorithms selectively | modernize for genotype-aware run topology and common schema |
| Existing ERR10619300 comparison dossier | Certified empirical precedent | use as calibration oracle | new extractor must reproduce accepted technical conclusions |
| Scientific-substrate discovery utility | not present | new | inventory WES assay/target evidence, WGS callable evidence, coverage, mapping, and duplication substrate |
| Genotype TSV scanner | not present as common certification utility | new | one streaming pass plus exact all-member observation-ID uniqueness |
| Opportunity extractor | not present | new | prefer governed QC artifacts; authorize alignment-scale probes only when scientifically required |
| Compact membership generator | not present | new | emit exact gene, evidence-class, coordinate-allele, and observation-ID membership surfaces |
| Corpus aggregator | not present | new | consume only verified per-run packages |
| WGS sibling comparator | not present | new | deterministic external join or node-local database strategy |
| Publication-candidate tracer | not present in common form | new | hierarchical genomic/protein/transcript/notation tracing for CNTNAP2 and optionally PDZD7, ALG6, RBM20 |
| Common-territory builder | not present | new | intersect governed WES target intervals with WGS sufficiently interrogated/callable territory |
| Compatibility gate | not present | new | consume only frozen certified package summaries and opportunity identities |
| Certified-corpus comparator | not present | new | preserve individual-run units, WES distributions, WGS siblings, and family-level summary |
| Receipt/package verifier | partial patterns only | new | common deterministic package format and verification command |

## 10. Common Output Schema

### 10.1 Common identity key

Every machine-readable output shall include, directly or by manifest reference:

```text
program_id
certification_object
corpus_id
sample_id
run_id
tep_id
assay_type
assay_designation
node_id
probe_execution_id
probe_schema_version
probe_git_commit
probe_script_sha256
observation_universe_definition
rarity_definition_id
```

A field shall have the same meaning on sys76 and MARK.

Modality-specific columns may be additive but shall not redefine common fields.

### 10.2 Technical state vocabulary

Allowed DEX technical states:

```text
NOT_STARTED
ARTIFACT_PRESENT
ARTIFACT_MISSING
HASH_MATCH
HASH_MISMATCH
BYTE_IDENTICAL
BYTE_DIFFERENT
SCHEMA_VALID
SCHEMA_INVALID
PROBE_PASS
PROBE_FAIL
NOT_APPLICABLE
BLOCKED_PENDING_DISCOVERY
UNAVAILABLE_WITH_EXPLICIT_LIMITATION
UNRESOLVED
EXTRACTION_COMPLETE
EXTRACTION_INCOMPLETE
PACKAGE_VERIFIED
PACKAGE_INVALID
```

SAGE certification outcomes shall not be written by DEX extraction code.

### 10.3 Common shared products

The first production schema shall include:

```text
certification_corpus_manifest.tsv
certification_extraction_manifest.json
certification_extraction_receipt.json
per_run_identity_and_source_state.tsv
per_run_execution_provenance_audit.tsv
per_run_configuration_snapshot_audit.tsv
per_run_genotype_integrity_audit.tsv
per_run_genotype_state_distribution.tsv
per_run_format_field_summary.tsv
per_run_stage_reconciliation_audit.tsv
per_run_tep_transport_audit.tsv
per_run_inventory_lineage_audit.tsv
per_run_scientific_sanity_summary.tsv
per_run_assay_opportunity_audit.tsv
per_run_gene_membership.tsv
per_run_gene_evidence_summary.tsv
per_run_variant_membership.tsv
per_run_deterministic_trace.tsv
certification_anomaly_register.tsv
certification_unresolved_questions.md
artifact_hashes.tsv
commands.tsv
```

### 10.4 Per-run identity table

Minimum fields:

```text
sample_id
run_id
assay_type
assay_designation
node_id
run_path
run_path_exists
run_completion_state
tep_id
tep_path
tep_path_exists
source_git_commit
source_git_branch
source_working_tree_state
library_strategy_state
target_design_id
opportunity_evidence_state
prior_certification_reference
technical_state
notes
```

### 10.5 Execution-provenance audit

Minimum fields:

```text
sample_id
run_id
run_provenance_path
tep_provenance_path
run_schema_version
tep_schema_version
run_sha256
tep_sha256
hash_state
byte_state
receipt_run_id
receipt_sample_id
receipt_node
reference_identity_state
toolchain_identity_state
resource_identity_state
annotation_environment_state
initialization_order_state
inventory_registration_state
lineage_registration_state
technical_state
limitation
```

### 10.6 Configuration audit

Minimum fields:

```text
sample_id
run_id
run_config_path
tep_config_path
run_sha256
tep_sha256
hash_state
byte_state
assay_type
assay_designation
reference_assembly
reference_fasta_identity
aligner
variant_caller
normalization_policy
annotation_engine
annotation_cache_identity
transcript_policy
genotype_projection_enabled
tep_enabled
technical_state
limitation
```

### 10.7 Genotype integrity audit

Minimum one-row-per-run fields:

```text
sample_id
run_id
schema_version
observation_universe_definition
source_vcf_path
source_vcf_sha256
source_header_sha256
selected_sample
source_record_count
projected_record_count
genotype_observation_count
observation_id_nonempty_count
observation_id_missing_count
observation_id_distinct_nonempty_count
observation_id_duplicate_count
observation_id_uniqueness_state
full_no_call_count
partial_no_call_count
phased_count
unphased_count
malformed_gt_count
format_sample_length_mismatch_count
allele_index_violation_count
multiallelic_record_count
spanning_deletion_count
direct_relationship_count
complex_or_deferred_relationship_count
processed_path
tep_path
processed_sha256
tep_sha256
hash_state
byte_state
technical_state
limitation
```

Exact observation-ID uniqueness shall be demonstrated for every run. If an
external sort or node-local database is required, its engine and version shall
be receipt-bound.

Long-form companion tables shall hold distributions rather than widening the
one-row summary indefinitely.

### 10.8 Stage reconciliation audit

Minimum fields:

```text
sample_id
run_id
stage07_observation_count
stage08_governed_universe_count
stage08_coding_count
stage08_splice_count
stage08_noncoding_count
stage08_retained_background_count
stage08_unrouted_count
stage09_interpreted_count
stage10_interpreted_count
stage11_overlay_count
stage12_overlay_count
stage07_to_stage08_delta
stage08_partition_delta
stage08_to_stage09_10_delta
stage08_to_stage11_delta
stage11_to_stage12_delta
unexplained_loss_count
technical_state
limitation
```

Counts may differ biologically among runs. The technical question is whether the
run reconciles according to its governed architecture.

### 10.9 TEP transport audit

Minimum fields:

```text
sample_id
run_id
tep_id
entity_inventory_path
lineage_manifest_path
validation_report_path
validator_version
validator_outcome
required_entity_state
genotype_entity_state
provenance_entity_state
config_entity_state
inventory_consistency_state
required_lineage_state
orphan_entity_count
broken_required_edge_count
transport_hash_state
technical_state
limitation
```

### 10.10 Assay-opportunity audit

Minimum fields:

```text
sample_id
run_id
assay_designation
library_strategy_state
design_uniformity_state
target_design_id
target_interval_path
target_interval_sha256
total_target_bases
callable_mask_path
callable_mask_sha256
total_callable_bases
mean_depth
median_depth
bases_ge_10x
bases_ge_20x
bases_ge_30x
mapping_rate
duplication_rate
callable_definition
callable_tool
opportunity_evidence_state
technical_state
limitation
```

The table shall distinguish zero from unavailable and shall record units and
denominators. Existing governed QC artifacts are preferred over new BAM-scale
computation.

### 10.11 Exact compact membership surfaces

`per_run_gene_membership.tsv` minimum fields:

```text
sample_id
run_id
gene_id
gene_symbol
evidence_class
observation_count
has_vap_governed_rare
has_high_impact
has_coding
has_splice
has_noncoding
membership_schema_version
```

`per_run_gene_evidence_summary.tsv` shall retain exact per-gene counts by
governed evidence class.

`per_run_variant_membership.tsv` minimum fields:

```text
sample_id
run_id
assembly
chromosome
position
reference
alternate
variant_identity
variant_observation_id
gene_id
gene_symbol
consequence_class
frequency_state
rarity_state
impact_state
genotype_state
relationship_state
territory_class
source_record_identity
```

The compact surfaces may use deterministic compression or partitioning, but
their complete manifest, row counts, hashes, and schema must remain reviewable.
Aggregate counts alone shall not support recurrence, overlap, or expansion
claims.

### 10.12 WES-specific products

```text
wes_assay_identity_summary.tsv
wes_target_design_inventory.tsv
wes_opportunity_summary.tsv
wes_read_count_stratum_summary.tsv
wes_stratum_genotype_summary.tsv
wes_stratum_semantic_surface_summary.tsv
wes_member_outlier_register.tsv
wes_targeted_probe_manifest.json
```

### 10.13 WGS-specific products

```text
wgs_sibling_identity_mapping.tsv
wgs_opportunity_summary.tsv
wgs_sibling_shared_private_summary.tsv
wgs_sibling_genotype_concordance.tsv
wgs_shared_homozygous_summary.tsv
wgs_chromosome_level_summary.tsv
wgs_complex_relationship_summary.tsv
cntnap2_coordinate_transcript_trace.tsv
cntnap2_trace_report.md
wgs_publication_candidate_trace.tsv
wgs_publication_comparator_summary.md
wgs_targeted_probe_manifest.json
```

Publication-wide candidate outputs are required only if the later claim exceeds
`CNTNAP2`-specific concordance.

### 10.14 Cross-modality products

```text
wes_wgs_compatibility_audit.tsv
wes_wgs_normalization_definitions.md
wes_wgs_observation_universe_definitions.tsv
wes_wgs_opportunity_denominator_audit.tsv
wes_wgs_common_territory_manifest.tsv
wes_wgs_common_territory_summary.tsv
wes_wgs_common_territory_variant_membership.tsv
wes_wgs_expanded_territory_summary.tsv
wes_wgs_preservation_comparison.tsv
wes_wgs_genotype_comparison.tsv
wes_wgs_gene_membership_comparison.tsv
wes_wgs_variant_membership_comparison.tsv
wes_wgs_provenance_lineage_comparison.tsv
wes_wgs_semantic_surface_comparison.tsv
wes_wgs_difference_classification.tsv
```

### 10.15 Extraction manifest JSON

The extraction manifest shall declare:

- execution identity;
- corpus-manifest identity;
- requested members;
- resolved source paths;
- requested core and opportunity evidence products;
- observation-universe and rarity definitions;
- expected outputs;
- probe and schema versions;
- all-member versus targeted scope;
- temporary and final output roots;
- package version;
- restart policy.

### 10.16 Extraction receipt JSON

The receipt shall record:

- start and finish timestamps;
- host and environment identity;
- Git branch, commit, and working-tree state;
- command line;
- exit status;
- completed and failed steps;
- input hashes where required;
- output hashes;
- output row counts;
- warnings and unresolved conditions;
- unavailable evidence and claim limitations;
- mutation-safety checks;
- package archive identity.

Volatile fields shall be isolated from scientific comparisons.

## 11. Evidence Directory Model

### 11.1 Repository certification records

Reviewed evidence shall be organized under:

```text
docs/validation/comparisons/
    sys76_wes_genotype_aware_execution_provenance/
    mark_wgs_genotype_aware_execution_provenance/
    wes_wgs_genotype_aware_comparison/
```

Each directory may contain run packages, corpus manifests, reviewed summaries,
receipts, SAGE review manifests, final SAGE determinations, and frozen-package
identities.

After SAGE issues a certification, the applicable namespace shall contain a
durable repository validation record. A chat response or transient handoff is
not sufficient.

Illustrative certification-record names are:

```text
sage_wes_corpus_certification.md
sage_wgs_corpus_certification.md
sage_wes_wgs_comparative_certification.md
```

Final filenames may change, but each record shall identify reviewed package
hashes, certified membership, outcome, notes, limitations, unresolved
questions, and revalidation triggers.

Large canonical artifacts shall remain in their run and TEP locations.

### 11.2 MARK external output root

MARK probes shall run from the VAP repository root and write only outside the
repository and immutable `results/` tree.

Required final output boundary:

```text
/root/Desktop/vap_certification/
```

Recommended execution structure:

```text
/root/Desktop/vap_certification/
└── mark_wgs_<probe_execution_id>/
    ├── input/
    ├── repository_state/
    ├── scientific_substrate/
    ├── per_run/
    │   ├── SRR13573587/
    │   └── SRR13573588/
    ├── sibling_comparison/
    ├── publication_traces/
    ├── manifests/
    ├── receipts/
    └── logs/
```

Final download units:

```text
mark_wgs_certification_evidence_<probe_execution_id>.tar.gz
mark_wgs_certification_evidence_<probe_execution_id>.tar.gz.sha256
```

### 11.3 MARK temporary workspace

High-cost joins may use a bounded node-local workspace outside canonical run
and TEP directories, for example:

```text
/data/storage/vap_tmp/certification/<probe_execution_id>/
```

The actual path shall be configurable and verified by preflight.

Temporary files shall be deleted only after final package verification or
retained with an explicit disposition if investigation remains open.

### 11.4 sys76 external output root

The sys76 output root shall be supplied explicitly through `--output-root` and
shall remain outside canonical run and TEP directories during extraction.

Reviewed small outputs may then be copied into the repository evidence
directory and committed.

## 12. Non-Mutation and Safety Design

Every probe shall:

1. open canonical source artifacts read-only;
2. reject an output path located inside a canonical run or TEP directory;
3. record source file metadata before extraction;
4. derive bounded evidence only;
5. write to a temporary output path;
6. validate the output;
7. atomically publish the output;
8. hash the published output;
9. emit a receipt;
10. verify the final evidence archive.

The implementation shall not:

- repair source data;
- rewrite TEP manifests;
- regenerate TEP packages;
- alter pipeline control flow;
- add biological interpretations;
- overwrite a reviewed evidence package;
- copy BAM, complete VCF, or complete genotype tables into Git.

A source immutability check should compare file metadata before and after a
probe. Where affordable, critical source hashes should be checked before and
after high-cost extraction.

---

## 13. Performance Strategy

### 13.1 One governed pass per large artifact

The genotype scanner shall calculate as many required summaries and compact
membership fields as practical in one streaming pass.

It shall not load a complete WGS genotype table into memory.

### 13.2 Exact uniqueness and joins

Exact observation-ID uniqueness is required for all 14 runs.

The implementation may use:

- deterministic external sort and merge;
- SQLite;
- DuckDB;
- another bounded node-local engine.

The same methods may support WGS sibling joins and compact exact membership
construction. The selected engine, version, collation, null handling, and key
normalization shall be receipt-bound.

### 13.3 Opportunity evidence hierarchy

Opportunity and coverage evidence shall use this precedence:

```text
1. existing governed callable mask or interval artifact
2. existing governed coverage and QC outputs
3. bounded alignment-scale probe authorized for a defined claim
4. UNAVAILABLE_WITH_EXPLICIT_LIMITATION
```

A BAM-scale probe shall not be added merely because a metric is scientifically
interesting. SAGE must confirm scientific necessity when no governed
lightweight artifact exists.

### 13.4 Compact membership strategy

Exact membership surfaces shall remain small enough for review and transport
where practical.

Permitted strategies include:

- deterministic partitioning by chromosome;
- stable compression;
- long-form gene summaries plus bounded exact variant membership;
- separate common-territory membership packages;
- hash-bound manifests over partitioned outputs.

No strategy may replace exact membership with aggregate counts when an overlap,
recurrence, expansion, or highlighted-observation claim depends on membership.

### 13.5 Hash policy

Full SHA-256 is required for:

- execution-provenance receipts;
- configuration snapshots;
- processed and TEP genotype artifacts;
- entity inventories;
- lineage manifests;
- opportunity interval or mask inputs;
- compact membership outputs;
- common-territory manifests and intervals;
- frozen evidence archives;
- critical Stage 07/08 anchors named in the final schema.

The plan does not require hashing every large intermediate artifact unless the
hash supports a defined certification claim.

### 13.6 Batch versus per-run work

Batch-level evidence is captured once per node/source state:

- Git identity;
- working-tree state;
- environment identity;
- dependency state;
- complete test result;
- probe source hashes;
- shared assay-resource discovery.

Per-run evidence is captured separately for every run.

Corpus and targeted probes execute only after their required per-run packages
verify successfully.

## 14. Failure, Restart, and Determinism

### 14.1 Atomic output

Each output shall be written as:

```text
<name>.tmp
    ↓ successful validation
<name>.tsv or <name>.json
```

Partial outputs shall not be registered as canonical evidence.

### 14.2 Failure receipt

A failed command shall emit, when technically possible:

```text
failure_receipt.json
completed_steps.tsv
error_summary.txt
partial_output_inventory.tsv
restart_recommendation.txt
```

### 14.3 Restart

A restart shall either resume from validated checkpoints or create a new
`probe_execution_id`.

It shall not append silently to a reviewed package.

### 14.4 Deterministic output

Stable tables shall use:

- fixed column order;
- stable sort order;
- explicit null representation;
- stable JSON serialization;
- locale-independent numeric formatting;
- explicit schema version;
- no volatile timestamps inside scientific data tables.

A rerun over unchanged inputs should reproduce byte-identical stable outputs.

---

## 15. Implementation and Certification Sequence

### Phase 0 — Live repository and source-state reconciliation

### Objective

Reconcile the live repository before writing certification code.

### Required checks

```bash
git status --short
git branch --show-current
git rev-parse HEAD
git log -1 --oneline
pytest
```

Compare the result with:

- certified commit `46a814a23cf0fb838950d7052bd1c2b542f52916`;
- the 160-test certified Probe C state;
- the later Phase 03 166-test snapshot;
- current genotype, provenance, TEP, and validation code.

### Exit gate

- live `HEAD` recorded;
- working-tree state understood;
- full test baseline recorded;
- six-test evolution explained;
- no unexplained source-state conflict remains.

---

### Phase 1 — Contract and plan v0.2 stabilization

### Objective

Commit the SAGE-compliant contract and this active plan, then obtain SAGE-VAP
confirmation that its scientific conditions were incorporated correctly.

### Deliverables

```text
docs/contracts/system/validation/
    genotype_aware_wes_wgs_certification_validation_contract.md

docs/plans/infrastructure/active/
    genotype_aware_wes_wgs_certification_implementation_plan.md
```

### Exit gate

- contract and plan are internally consistent;
- SAGE confirms condition incorporation or returns bounded corrections;
- all prior SAGE scientific questions are recorded as resolved;
- no unresolved scientific question blocks schema implementation.

---

### Phase 2 — Scientific-substrate discovery

### Objective

Determine which governed assay-opportunity, coverage, callability, and exact
membership inputs exist before broad extraction or comparative implementation.

### WES discovery

For all 12 WES-designated runs, inventory:

- repository and ENA library-strategy evidence;
- the `AMPLICON` metadata discrepancy;
- target or bait-set identity;
- whether one design applies to all 12 runs;
- target interval files and hashes;
- total target bases;
- mean and median target depth;
- target bases at `>=10x`, `>=20x`, and `>=30x`;
- mapping and duplication context;
- governed callable-target evidence.

### WGS discovery

For both WGS runs, inventory:

- interrogated genome definition;
- callable masks or callable-region evidence;
- total callable bases;
- mean and median depth;
- genome bases at `>=10x`, `>=20x`, and `>=30x`;
- mapping and duplication context;
- callable definitions and tool identities.

### Membership and common-territory discovery

Determine:

- the smallest exact gene-membership substrate that supports recurrence claims;
- the smallest exact coordinate-allele membership substrate that supports
  observation recurrence;
- whether governed WES targets and WGS callable territory permit an exact
  common-territory intersection;
- expected row counts, sizes, and transport burden.

### Disposition rule

Every item shall become:

```text
AVAILABLE_DIRECTLY
AVAILABLE_BY_EXISTING_EXTRACTOR
AVAILABLE_BY_EXISTING_PROBE
NEW_BOUNDED_PROBE_REQUIRED
BLOCKED_PENDING_DISCOVERY
UNAVAILABLE_WITH_EXPLICIT_LIMITATION
NOT_APPLICABLE
```

### Exit gate

- WES assay terminology is resolved or formally qualified;
- opportunity evidence availability is known for all 14 runs;
- common-territory feasibility is known;
- exact-membership derivation is specified;
- unavailable evidence has an explicit claim consequence;
- no denominator is fabricated.

---

### Phase 3 — Corpus-manifest and common-schema implementation

### Objective

Create the locked input manifest, common models, state vocabulary, stable
serialization, opportunity and membership schemas, and receipt schemas.

### Work packages

1. Implement manifest parser and validator.
2. Encode all 14 locked members.
3. Represent unresolved TEP and assay-resource identities explicitly.
4. Implement common identity model.
5. Implement observation-universe and rarity-definition models.
6. Implement opportunity-evidence states.
7. Implement compact membership schemas.
8. Implement stable TSV and JSON writers.
9. Implement technical state validation.
10. Implement output-root safety checks.
11. Implement manifest and receipt validation.

### Test requirements

- duplicate member rejection;
- unknown assay or node rejection;
- unresolved identity handling;
- unavailable-with-limitation handling;
- observation-universe enforcement;
- rarity-state separation;
- schema-version handling;
- stable serialization;
- output-path traversal and canonical-path rejection;
- deterministic manifest hashing.

### Exit gate

- corpus manifest validates;
- all 14 members are represented exactly once;
- common, opportunity, and membership schemas pass unit tests;
- package and receipt schemas are frozen as v1.

---

### Phase 4 — Common per-run extractor implementation

### Objective

Implement the modality-neutral core evidence surface and comparative-opportunity
extension used for all 14 runs.

### Work packages

1. Preflight discovery.
2. Run and TEP identity extraction.
3. Execution-provenance validation.
4. Configuration-snapshot validation.
5. Streaming genotype scanner.
6. Exact observation-ID uniqueness and duplicate detection.
7. Stage reconciliation.
8. TEP inventory and lineage audit.
9. Scientific sanity summaries.
10. Opportunity evidence extraction where governed.
11. Exact compact gene and variant membership generation.
12. Deterministic bounded traces.
13. Manifest, receipt, log, and package emission.

### Required properties

- no sample-specific expected counts in code;
- no hidden WES/WGS field redefinition;
- read-only source access;
- deterministic output;
- clear failure and limitation states;
- bounded memory use;
- progress reporting suitable for MARK execution;
- explicit emitted-observation-universe semantics;
- explicit rarity definitions;
- no fabricated opportunity denominator.

### Exit gate

- unit tests pass;
- representative fixture tests pass;
- malformed and edge-case genotype tests pass;
- exact uniqueness tests pass;
- opportunity and membership tests pass;
- package verification tests pass;
- common extractor is ready for calibration.

---

### Phase 5 — ERR10619300 calibration

### Objective

Run the new common extractor against:

```text
ERR10619300 / run_2026_07_14_114546
```

and reconcile the new output against the existing SAGE-certified dossier.

### Required calibration checks

- 736,508 genotype observations;
- 731,444 direct relationships;
- 5,064 complex/deferred relationships;
- 4,359 multiallelic deferrals;
- 705 spanning-deletion deferrals;
- exact observation-ID uniqueness state;
- provenance and config transport identity;
- TEP validation and lineage registration;
- no scientifically changed shared coding rows in the prior elevation comparison;
- known bounded limitations remain visible;
- observation-universe and rarity semantics are explicit;
- opportunity and membership outputs are present or correctly limited.

The calibration shall not require byte identity with historical dossier tables
if the new schema is intentionally different. It must reproduce the accepted
technical conclusions and explain every schema-level difference.

### SAGE checkpoint

Submit the calibration package so SAGE can confirm that the generalized
extractor recovers the evidence surface underlying the prior certification.

### Exit gate

- common extractor reproduces the certified technical state;
- discrepancies are resolved or sent to SAGE;
- ERR10619300 is represented in the new corpus program without weakening its
  prior certification.

---

### Phase 6 — MARK discovery-only preflight

### Objective

Resolve actual MARK paths, TEP identities, artifact sizes, scientific
substrate, and execution constraints before scanning large WGS artifacts.

### Execution model

```text
sys76 authoring
    ↓
Git commit and push
    ↓
MARK pull
    ↓
run from VAP repository root
    ↓
write only to /root/Desktop/vap_certification/
    ↓
Guacamole download to sys76
```

### Required outputs

```text
mark_wgs_preflight.tsv
mark_wgs_artifact_discovery.tsv
mark_wgs_repository_state.txt
mark_wgs_environment_state.tsv
mark_wgs_scientific_substrate.tsv
mark_wgs_preflight_receipt.json
```

### Required discovery fields

- repository root and `HEAD`;
- branch and working-tree state;
- Python and dependency identity;
- host and filesystem identity;
- run directory existence;
- actual TEP paths and IDs;
- required artifact paths;
- file sizes;
- readability;
- free space;
- temporary-workspace suitability;
- estimated scan burden;
- existing validation-report state;
- WGS coverage and callable evidence availability.

### Exit gate

- both run and TEP identities are locked;
- all required source artifacts are locatable;
- output and temporary paths are safe;
- package transfer size is acceptable;
- WGS opportunity evidence is classified;
- no blocking preflight anomaly remains.

---

### Phase 7 — MARK common per-run WGS extraction

### Objective

Generate the complete common technical evidence package independently for both
WGS siblings.

### Required members

```text
SRR13573587 / run_2026_07_29_123020
SRR13573588 / run_2026_08_01_092338
```

### Execution order

1. Capture batch-level repository and environment receipt.
2. Extract SRR13573587 core, opportunity, and membership evidence.
3. Verify its package.
4. Extract SRR13573588 core, opportunity, and membership evidence.
5. Verify its package.
6. Build initial WGS corpus manifest and anomaly register.
7. Package and download outputs.
8. Verify archive SHA-256 on sys76.

### Exit gate

- both per-run packages are `PACKAGE_VERIFIED`;
- exact observation-ID uniqueness is proven for both;
- no member is omitted;
- all foundational evidence classes are complete;
- unavailable opportunity evidence is explicit rather than fabricated;
- initial anomaly register is ready for SAGE review.

---

### Phase 8 — WGS sibling and publication-candidate probes

### Objective

Generate the WGS-specific corpus evidence required for Certification B and the
bounded publication-comparator surface.

#### 8.1 Sibling comparison

Use exact coordinate-and-allele-aware identities to calculate:

- shared observations;
- private observations per sibling;
- shared identical genotype states;
- discordant genotype states at shared identities;
- shared homozygous alternate observations;
- shared VAP-governed rare homozygous observations;
- frequency-unknown observations kept separate;
- shared multiallelic and complex/deferred relationships;
- chromosome-level shared/private summaries;
- deterministic bounded exemplars.

The probe shall not infer inheritance or causality.

#### 8.2 `CNTNAP2` trace

The trace shall begin with all governed `CNTNAP2` observations and shall anchor
on:

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
Stage 08 routing
Stage 09 or 10 overlay
Stage 11 priority overlay
Stage 12 validation overlay
TEP entity
inventory registration
lineage registration
```

Concordance shall be hierarchical:

```text
genomic concordance
gene/protein concordance
transcript concordance
notation discordance
unresolved normalization difference
```

A cDNA-string discrepancy shall not defeat concordance where genomic and
protein identity agree.

#### 8.3 Optional publication-wide candidate trace

If the intended later claim exceeds `CNTNAP2`-specific concordance, run bounded
traces for:

```text
PDZD7
ALG6
RBM20
CNTNAP2
```

Without all required traces, publication language remains explicitly
`CNTNAP2`-specific.

#### 8.4 Pedigree identity

Repository or accession metadata shall be searched for authoritative
`SRR → V-2/V-4` mapping.

If no governed mapping is found, the output shall preserve `UNRESOLVED`. This
does not block Certification B.

### Exit gate

- WGS-specific products verify;
- `CNTNAP2` evidence is reviewable without large artifacts;
- publication claim scope is explicit;
- all limitations and unresolved mapping are explicit;
- SAGE has enough evidence for first-pass WGS review.

---

### Phase 9 — SAGE WGS review and bounded follow-up

### Objective

Submit the complete two-member WGS evidence package to SAGE-VAP.

### DEX responsibilities

- answer technical questions;
- run only bounded follow-up probes requested by SAGE or justified by anomalies;
- version every follow-up package;
- preserve prior receipts;
- avoid interpreting scientific significance.

### Exit gate

SAGE issues one of the reserved WGS per-run and corpus outcomes, or identifies
specific insufficient evidence requiring additional work.

---

### Phase 10 — Freeze and codify the certified WGS corpus

### Objective

Freeze the SAGE-reviewed WGS package when it receives a usable corpus
determination and codify the determination under `docs/validation/comparisons/`.

### Comparison-ready outcomes

```text
CORPUS CERTIFIED
CORPUS CERTIFIED WITH NOTES
```

### Required frozen-package fields

```text
corpus_id
corpus_manifest_sha256
member_package_ids
member_package_sha256s
aggregate_output_sha256s
probe_git_commit
probe_schema_version
SAGE_determination_reference
limitations
revalidation_triggers
freeze_timestamp
frozen_archive_sha256
```

### Durable repository record

Commit the SAGE certification record, review manifest, and frozen receipt under:

```text
docs/validation/comparisons/
    mark_wgs_genotype_aware_execution_provenance/
```

### Exit gate

- package is immutable by convention and checksum;
- SAGE determination is durably committed;
- replacement requires a new package version;
- Certification C may reference it only after WES freezing is also complete.

---

### Phase 11 — sys76 all-member WES extraction

### Objective

Run the calibrated common extractor against all 12 WES-designated runs.

### Execution order

1. Capture sys76 repository and environment receipt.
2. Resolve all 12 run and TEP paths.
3. Resolve or qualify WES assay and target-design identity.
4. Re-run or incorporate ERR10619300 calibration evidence by governed reference.
5. Extract the remaining 11 members.
6. Verify every per-run package.
7. Aggregate the initial WES corpus evidence.
8. Build stratum summaries and anomaly register.

### Required rule

Prior ERR10619300 certification may be incorporated only when the source run,
TEP, schemas, and evidence identities remain unchanged.

### Exit gate

- all 12 members are represented;
- exact observation-ID uniqueness is proven for all 12;
- every package verifies;
- q1, median, and q3 summaries exist;
- opportunity evidence and limitations are visible;
- exact membership outputs verify;
- outliers and unresolved conditions are visible.

---

### Phase 12 — WES stratum, outlier, and representative probes

### Objective

Produce the WES-specific evidence required for Certification A.

### Required summaries

- genotype completeness by stratum;
- no-call and partial-call behavior by stratum;
- multiallelic and complex relationship distributions;
- Stage 07 preservation;
- Stage 08–12 semantic routing;
- reviewability and priority states;
- VAP-governed rare and high-impact evidence surfaces;
- frequency-unknown states;
- assay-opportunity availability;
- anomaly rates.

### Predetermined representative set

```text
q1
    ERR10619212

median and certified exemplar
    ERR10619300

q3
    ERR10619225

plus
    any detected outlier
```

A representative audit supplements but does not replace all-member
foundational checks.

### Outlier classes

```text
EXPECTED_BIOLOGICAL_VARIATION
READ_COUNT_ASSOCIATED_VARIATION
CONFIGURATION_OR_RESOURCE_DIFFERENCE
EXTRACTOR_ANOMALY
ARTIFACT_ANOMALY
UNRESOLVED
```

DEX assigns provisional technical classes; SAGE determines scientific meaning.

### Exit gate

- stratum and outlier products verify;
- representative high-cost coverage is recorded;
- assay terminology is correctly qualified;
- SAGE has enough evidence for first-pass WES review.

---

### Phase 13 — SAGE WES review and bounded follow-up

### Objective

Submit the complete 12-member WES evidence package to SAGE-VAP.

### Exit gate

SAGE issues per-run and corpus outcomes or requests bounded additional evidence.

---

### Phase 14 — Freeze and codify the certified WES corpus

### Objective

Freeze the SAGE-reviewed WES package using the same package and receipt
semantics as WGS, then codify the SAGE determination under
`docs/validation/comparisons/`.

### Durable repository record

Commit the SAGE certification record, review manifest, and frozen receipt under:

```text
docs/validation/comparisons/
    sys76_wes_genotype_aware_execution_provenance/
```

### Exit gate

- package is checksum-frozen;
- SAGE determination is durably committed;
- all member determinations and limitations are referenced;
- both Certifications A and B now have frozen comparison-ready corpus packages.

---

### Phase 15 — Cross-modality compatibility and opportunity gate

### Objective

Determine which claims the frozen WES and WGS packages support.

### Required compatibility surfaces

- VAP source-state identity;
- common extraction schema;
- reference assembly and FASTA;
- aligner;
- variant caller;
- normalization policy;
- VEP and cache identity;
- transcript policy;
- population resources;
- clinical resources;
- genotype schema;
- semantic-routing policy;
- TEP builder and validator;
- execution-provenance schema;
- node and operating environment;
- WES assay and target-design identity;
- WGS callable-territory identity;
- coverage and callability definitions;
- opportunity-denominator availability;
- compact membership-schema identity;
- observation-universe definition;
- rarity definition.

### Allowed classifications

```text
IDENTICAL
INTENTIONAL_MODALITY_DIFFERENCE
CONTROLLED_NODE_DIFFERENCE
BENIGN_VERSION_DIFFERENCE
COMPARISON_LIMITING_DIFFERENCE
CERTIFICATION_BLOCKING_INCOMPATIBILITY
UNRESOLVED
```

### Exit gate

- every compatibility field is classified;
- core preservation comparison scope is explicit;
- opportunity-qualified comparison scope is explicit;
- blocking and limiting differences are visible;
- SAGE confirms which Certification C claims remain valid.

---

### Phase 16 — Common evaluable territory construction

### Objective

Where governed interval-level evidence exists, construct:

```text
governed WES target territory
    intersected with
WGS sufficiently interrogated or callable territory
```

### Required outputs

- input interval or mask paths and hashes;
- reference assembly identity;
- callable or coverage threshold;
- interval normalization method;
- common-territory interval manifest;
- total common-territory bases;
- WGS expanded-territory definition;
- exact common-territory membership surfaces;
- deterministic construction receipt.

### Fallback

If exact interval-level substrate is unavailable:

```text
UNAVAILABLE_WITH_EXPLICIT_LIMITATION
```

Coverage summaries may remain descriptive context, but exact common-territory
recurrence and density claims shall be omitted.

### Exit gate

- common territory is checksum-bound and reviewable; or
- its unavailability and claim consequences are explicit.

---

### Phase 17 — Controlled WES/WGS comparison

### Objective

Build Certification C products from the two frozen packages only.

### Core comparison classes

1. invariant architecture and preservation behavior;
2. operational and node context;
3. execution-provenance completeness;
4. genotype integrity and emitted-observation composition;
5. semantic-surface composition;
6. inventory and lineage completeness;
7. WES within-corpus distribution;
8. both WGS siblings separately;
9. WGS family-level shared/private structure;
10. unresolved confounding.

### Opportunity-qualified classes

Only where governed denominators and exact membership exist:

1. normalized observation density;
2. common-territory recurrence;
3. exact recurrent genes;
4. exact recurrent coordinate-allele observations;
5. gene-surface overlap and expansion;
6. WGS expanded-territory evidence;
7. assay-associated descriptive differences.

Raw counts shall not be interpreted without denominator and search-space
context where normalization is required.

The comparison shall not perform inferential significance testing or treat the
siblings as independent replicates.

### Exit gate

- all comparative products derive from frozen package hashes;
- no raw run directory was used as an uncontrolled input;
- every recurrence or overlap claim is membership-supported;
- observation-universe and rarity definitions are explicit;
- publication claims are bounded to the candidates actually traced;
- SAGE can issue a comparative determination.

---

### Phase 18 — SAGE comparative certification and mission closure

### Objective

Support SAGE-VAP in issuing Certification C.

After SAGE review:

- freeze the comparative evidence package;
- codify the final SAGE determination under
  `docs/validation/comparisons/wes_wgs_genotype_aware_comparison/`;
- record limitations and revalidation triggers;
- hand the certified claim surface to LANE-VAP for case-study authorship;
- retain DEX technical support for artifact references and bounded clarification.

The implementation mission is complete only after Certifications A, B, and C
have reviewable final states and their durable repository records are committed
or clearly recorded as insufficient/not certified.

## 16. MARK Command and Transfer Workflow

The exact commands depend on the final CLI, but production execution shall
follow this pattern.

### 16.1 sys76 authoring

```bash
git status --short
pytest

git add \
  src/certification \
  scripts/validation/run_genotype_aware_certification.py \
  tests/certification \
  config/certification/genotype_aware_wes_wgs_corpus_v1.tsv

git commit -m "Implement genotype-aware WES/WGS certification probes"
git push origin main
```

Branch names and commit boundaries may differ, but the MARK-executed commit
shall be immutable and recorded.

### 16.2 MARK synchronization

From the VAP repository root on MARK:

```bash
git status --short
git pull --ff-only
git rev-parse HEAD
pytest
```

A non-clean working tree shall be investigated before production extraction.

### 16.3 MARK scientific-substrate discovery and preflight

Illustrative commands:

```bash
python scripts/validation/run_genotype_aware_certification.py \
  discover-scientific-substrate \
  --corpus-manifest config/certification/genotype_aware_wes_wgs_corpus_v1.tsv \
  --corpus-id mark_wgs_v1 \
  --output-root /root/Desktop/vap_certification

python scripts/validation/run_genotype_aware_certification.py \
  preflight \
  --corpus-manifest config/certification/genotype_aware_wes_wgs_corpus_v1.tsv \
  --corpus-id mark_wgs_v1 \
  --output-root /root/Desktop/vap_certification \
  --temp-root /data/storage/vap_tmp/certification
```

### 16.4 MARK extraction

Illustrative commands:

```bash
python scripts/validation/run_genotype_aware_certification.py \
  extract-run \
  --corpus-manifest config/certification/genotype_aware_wes_wgs_corpus_v1.tsv \
  --sample-id SRR13573587 \
  --output-root /root/Desktop/vap_certification \
  --temp-root /data/storage/vap_tmp/certification

python scripts/validation/run_genotype_aware_certification.py \
  extract-run \
  --corpus-manifest config/certification/genotype_aware_wes_wgs_corpus_v1.tsv \
  --sample-id SRR13573588 \
  --output-root /root/Desktop/vap_certification \
  --temp-root /data/storage/vap_tmp/certification
```

### 16.5 WGS-specific probes

```bash
python scripts/validation/run_genotype_aware_certification.py \
  compare-wgs-siblings \
  --corpus-manifest config/certification/genotype_aware_wes_wgs_corpus_v1.tsv \
  --output-root /root/Desktop/vap_certification \
  --temp-root /data/storage/vap_tmp/certification

python scripts/validation/run_genotype_aware_certification.py \
  trace-publication-candidates \
  --corpus-manifest config/certification/genotype_aware_wes_wgs_corpus_v1.tsv \
  --genes CNTNAP2 \
  --output-root /root/Desktop/vap_certification
```

If publication-wide concordance is intended, use:

```bash
--genes PDZD7,ALG6,RBM20,CNTNAP2
```

### 16.6 Package and verify

```bash
python scripts/validation/run_genotype_aware_certification.py \
  package-evidence \
  --execution-dir /root/Desktop/vap_certification/<probe_execution_id>

python scripts/validation/run_genotype_aware_certification.py \
  verify-package \
  --archive /root/Desktop/vap_certification/<archive>.tar.gz
```

### 16.7 Guacamole transfer

Download both:

```text
<archive>.tar.gz
<archive>.tar.gz.sha256
```

On sys76:

```bash
sha256sum -c <archive>.tar.gz.sha256
```

The archive shall not be treated as reviewable evidence until checksum
verification succeeds.

### 16.8 Common-territory and certified-corpus comparison

Common-territory and Certification C commands shall execute on sys76 against
the two frozen certified evidence packages, not against MARK raw run paths.

Illustrative commands:

```bash
python scripts/validation/run_genotype_aware_certification.py \
  build-common-territory \
  --wes-package <frozen_wes_package> \
  --wgs-package <frozen_wgs_package> \
  --output-root <comparison_output_root>

python scripts/validation/run_genotype_aware_certification.py \
  compare-certified-corpora \
  --wes-package <frozen_wes_package> \
  --wgs-package <frozen_wgs_package> \
  --output-root <comparison_output_root>
```

## 17. SAGE–DEX Review Checkpoints

| Checkpoint | DEX submission | SAGE decision |
|---|---|---|
| R1 | Contract and implementation plan v0.2 | confirmation that scientific conditions are incorporated |
| R2 | Scientific-substrate discovery report | assay terminology, denominator necessity, and permitted claim scope |
| R3 | ERR10619300 calibration package | common extractor scientific adequacy |
| R4 | MARK preflight package | WGS source-object and opportunity-substrate readiness |
| R5 | Initial two-run WGS package | first-pass WGS sufficiency and anomaly requests |
| R6 | WGS sibling and publication-candidate probes | per-run and corpus Certification B determination |
| R7 | Initial 12-run WES package | first-pass WES sufficiency and anomaly requests |
| R8 | WES stratum and targeted probes | per-run and corpus Certification A determination |
| R9 | Compatibility and opportunity audit | allowed Certification C core and opportunity-qualified scope |
| R10 | Common-territory package or limitation receipt | exact common-territory claim authorization |
| R11 | Comparative package | Certification C determination |
| R12 | Later case-study technical review | bounded artifact clarification only |

A request for another bounded probe is not itself a certification failure.

## 18. Test Strategy

### 18.1 Unit tests

Unit tests shall cover:

- manifest validation;
- schema validation;
- stable serialization;
- path safety;
- genotype parsing;
- missing and partial no-calls;
- phased and unphased GT;
- single-allele GT without automatic haploid inference;
- multiallelic records;
- spanning deletion;
- symbolic alleles;
- malformed GT;
- FORMAT/sample length mismatch;
- absent optional fields;
- allele-index validation;
- exact observation-ID uniqueness;
- duplicate source identities;
- emitted-observation-universe enforcement;
- rarity-state separation;
- opportunity-evidence null and limitation semantics;
- target and callable interval hashing;
- compact gene and variant membership;
- common-territory interval intersection;
- publication-candidate hierarchy;
- receipt hashing;
- package verification;
- failure receipts;
- deterministic traces;
- compatibility classifications.

### 18.2 Integration fixtures

Fixtures shall include:

- a small WES-designated run;
- a small WGS-like run;
- matching processed and TEP artifacts;
- deliberate hash mismatch;
- missing entity;
- broken lineage edge;
- Stage 07/08 loss case;
- genotype no-call edge cases;
- duplicate observation IDs;
- sibling shared/private examples;
- VAP rare, publication-threshold rare, and frequency-unknown examples;
- WES target and WGS callable interval examples;
- common-territory and expanded-territory examples;
- exact recurrent gene and variant membership examples;
- `CNTNAP2` transcript/notation variation;
- PDZD7, ALG6, and RBM20 bounded trace examples.

### 18.3 Calibration test

ERR10619300 is the production calibration object, not a lightweight unit-test
fixture.

Its extraction receipt and reconciliation report shall be retained as a
certification-system acceptance test.

### 18.4 Regression rule

A change to extractor semantics, common schema, opportunity logic, membership
logic, common-territory construction, or compatibility logic shall:

1. increment the relevant schema or probe version;
2. rerun unit and integration tests;
3. rerun ERR10619300 calibration;
4. identify affected frozen packages;
5. trigger SAGE revalidation review where required.

## 19. Anomaly Handling

Every anomaly shall include:

```text
anomaly_id
certification_object
corpus_id
sample_id
run_id
evidence_class
observed_condition
expected_contract_state
provisional_technical_class
severity
blocking_candidate
claim_scope_affected
follow_up_probe
SAGE_question
resolution_state
resolution_reference
```

No run may be silently excluded from corpus aggregation.

An anomaly may be provisionally classified as:

```text
EXPECTED_BIOLOGICAL_VARIATION
EXPECTED_MODALITY_DIFFERENCE
CONTROLLED_NODE_DIFFERENCE
CONFIGURATION_OR_RESOURCE_DIFFERENCE
ASSAY_IDENTITY_UNCERTAINTY
OPPORTUNITY_DENOMINATOR_UNAVAILABLE
COMMON_TERRITORY_UNAVAILABLE
MEMBERSHIP_SURFACE_INCOMPLETE
EXTRACTOR_ANOMALY
ARTIFACT_ANOMALY
PACKAGING_ANOMALY
UNRESOLVED
```

SAGE determines the scientific consequence.

A missing opportunity denominator shall not be promoted to a foundational
producer-certification failure unless the missing evidence also prevents a
required identity, genotype, preservation, transport, inventory, or lineage
claim.

## 20. SAGE Scientific Resolutions and Remaining Discovery Questions

### 20.1 Resolved SAGE scientific questions

| ID | Resolution | Implementation consequence | State |
|---|---|---|---|
| SAGE-Q01 | Both WGS runs require complete foundational identity, genotype, preservation, transport, inventory, and lineage checks | no representative-only substitution for WGS foundations | RESOLVED |
| SAGE-Q02 | Exact observation-ID uniqueness is required for all 14 runs | implement external exact uniqueness where streaming distinct counts are insufficient | RESOLVED |
| SAGE-Q03 | Use VAP-governed rarity for certification; use `MAF <= 0.001` only for publication reconstruction; keep frequency unknown separate | version rarity definitions and emit distinct states | RESOLVED |
| SAGE-Q04 | Genomic coordinate/allele and protein agreement establish strongest `CNTNAP2` concordance; transcript/cDNA disagreement is separate notation or normalization evidence | hierarchical trace schema | RESOLVED |
| SAGE-Q05 | SRR-to-`V-2`/`V-4` mapping is not required for Certification B | preserve unknown; restrict person-specific narration | RESOLVED |
| SAGE-Q06 | Predetermined WES representatives are ERR10619212 q1, ERR10619300 median/exemplar, and ERR10619225 q3, plus outliers | lock representative manifest | RESOLVED |
| SAGE-Q07 | Complete Certification C may consume only `CORPUS CERTIFIED` or `CORPUS CERTIFIED WITH NOTES` | enforce comparison entry gate | RESOLVED |

### 20.2 Scientific-substrate discovery questions

These are evidence-location and feasibility questions, not requests to reopen
SAGE doctrine.

| ID | Question | Required disposition | Blocking point | State |
|---|---|---|---|---|
| DISC-Q01 | What governed source establishes the WES library-preparation strategy, and how should ENA `AMPLICON` metadata be reconciled with repository WES designation? | resolved identity or explicit qualification | before WES narrative and Certification C | OPEN |
| DISC-Q02 | Do all 12 WES-designated runs share one governed target design? | target-design identity or explicit heterogeneity | before common-territory construction | OPEN |
| DISC-Q03 | Where are the governed WES target intervals, if present? | path/hash or `UNAVAILABLE_WITH_EXPLICIT_LIMITATION` | before exact common territory | OPEN |
| DISC-Q04 | Which existing artifacts provide per-run WES and WGS depth, threshold coverage, mapping, and duplication evidence? | direct source or bounded-probe requirement | before opportunity schema execution | OPEN |
| DISC-Q05 | Do governed WGS callable masks or callable-region outputs exist? | path/hash or limitation | before exact common territory | OPEN |
| DISC-Q06 | What compact exact membership representation remains reviewable and transferable at WGS scale? | benchmark and schema decision | before membership implementation freeze | OPEN |
| DISC-Q07 | Is publication scope intended to remain `CNTNAP2`-specific or later expand to all four candidates? | claim-scope decision before final WGS publication package | before LANE case-study planning | OPEN; NOT BLOCKING CERTIFICATION B |

### 20.3 DEX implementation decisions not requiring SAGE

The following remain within DEX authority unless they change scientific
meaning:

- external sort versus SQLite/DuckDB;
- chunk size and progress cadence;
- internal class and function names;
- temporary-file naming;
- compression and partitioning strategy;
- log formatting;
- atomic rename implementation;
- number of modules behind the single CLI.

## 21. Risk Register

| Risk | Effect | Mitigation | Owner | State |
|---|---|---|---|---|
| Live `HEAD` differs from certified `46a814a...` | calibration ambiguity | complete Phase 0 reconciliation before code changes | DEX | OPEN |
| 160-test certified state versus 166-test onboarding snapshot | unclear source evolution | identify six-test and implementation delta | DEX | OPEN |
| WES assay identity remains unresolved | overclaiming capture-based exome opportunity | use `WES-designated PRJEB57558 runs`; complete substrate discovery | DEX/SAGE | OPEN |
| ENA `AMPLICON` metadata conflicts with repository terminology | uncertain assay interpretation | preserve both sources and qualify scientific narration | DEX/SAGE | OPEN |
| WES target intervals unavailable | exact common territory cannot be constructed | explicit limitation; restrict comparison to emitted-universe and descriptive context | SAGE/DEX | OPEN |
| WGS callable masks unavailable | exact common territory or callable density unsupported | explicit limitation; do not fabricate callability | SAGE/DEX | OPEN |
| Coverage thresholds require BAM-scale computation | high node I/O burden | prefer governed QC outputs; require SAGE necessity before new alignment-scale probe | DEX/SAGE | OPEN |
| Compact membership surfaces become too large | transfer and review burden | deterministic partitioning, compression, manifests, and bounded schemas | DEX | CONTROLLED BY DESIGN |
| Exact uniqueness requires large external state | disk and runtime burden | preflight size estimate and bounded external sort/database | DEX | CONTROLLED BY DESIGN |
| WGS TEP paths or IDs differ from convention | wrong source object | discovery-only preflight; no inferred paths | DEX | OPEN |
| Large WGS scans overload memory | failed or disruptive probe | streaming pass and node-local external joins | DEX | CONTROLLED BY DESIGN |
| Repeated scans create excessive I/O | node burden | combine summaries and membership derivation into governed passes | DEX | CONTROLLED BY DESIGN |
| Output accidentally enters `results/` or TEP tree | source mutation risk | output-root guard and canonical-path rejection | DEX | CONTROLLED BY DESIGN |
| Guacamole transfer truncation | invalid evidence package | archive SHA-256 verification on sys76 | DEX | CONTROLLED BY DESIGN |
| Node and modality are confounded | invalid scientific attribution | explicit compatibility classification and limitation | SAGE/DEX | INHERENT |
| WGS members are related siblings | non-independent corpus | preserve family structure; no population inference | SAGE | INHERENT |
| `CNTNAP2` publication notation inconsistent | false negative trace | hierarchical coordinate/protein/transcript/notation evidence | DEX/SAGE | CONTROLLED BY DESIGN |
| Publication-wide claim exceeds traced candidates | unsupported concordance statement | require PDZD7, ALG6, RBM20, CNTNAP2 traces or narrow claim | SAGE/LANE | CONTROLLED BY CONTRACT |
| Pedigree mapping unresolved | sample-specific narration limitation | preserve unknown unless governed evidence found | SAGE/DEX | OPEN; NON-BLOCKING B |
| Frequency unknown misclassified as rare | invalid rarity inference | explicit rarity states and tests | DEX/SAGE | CONTROLLED BY DESIGN |
| Emitted genotype proportions misread as callable-locus burden | invalid biological inference | machine-readable observation-universe boundary | DEX/SAGE | CONTROLLED BY CONTRACT |
| Biological outlier mistaken for technical failure | inappropriate rejection | anomaly classes plus SAGE interpretation | SAGE | CONTROLLED BY PROCESS |
| TEP regenerated after certification | frozen package invalidation | package identity and revalidation trigger | DEX/SAGE | CONTROLLED BY CONTRACT |
| Probe semantics change mid-program | incompatible member packages | versioned schema and ERR10619300 recalibration | DEX | CONTROLLED BY CONTRACT |
| Comparison starts before corpus freeze | uncontrolled evidence | outcome and freeze gates | DEX/SAGE | CONTROLLED BY CONTRACT |

## 22. Status Ledger

| Work package | Current state | Evidence/reference | Next action |
|---|---|---|---|
| Five-phase DEX-VAP-v3 onboarding | COMPLETE | Phase 01–05 audits | none |
| Scientific certification framework | COMPLETE | governing validation document | maintain version awareness |
| SAGE→DEX implementation handoff | COMPLETE | genotype certification handoff | use as planning authority |
| SAGE scientific review of v0.1 control plane | APPROVE WITH SCIENTIFIC CONDITIONS | SAGE review determination | incorporate and confirm v0.2 |
| System validation contract | V0.2 APPLIED; SAGE CONFIRMATION PENDING | SAGE-compliant contract updater | apply, commit, and obtain SAGE confirmation |
| Active implementation plan | V0.2 APPLIED; SAGE CONFIRMATION PENDING | this document | apply, commit, and obtain SAGE confirmation |
| Live repository reconciliation | NOT_STARTED | — | Phase 0 |
| Scientific-substrate discovery | NOT_STARTED | — | Phase 2 |
| WES assay identity resolution | NOT_STARTED | ENA/repository discrepancy known | Phase 2 |
| WES target interval discovery | NOT_STARTED | — | Phase 2 |
| WGS callable-territory discovery | NOT_STARTED | — | Phase 2/6 |
| Locked machine-readable corpus manifest | NOT_STARTED | — | Phase 3 |
| Common schema and receipt implementation | NOT_STARTED | — | Phase 3 |
| Opportunity and membership schemas | NOT_STARTED | — | Phase 3 |
| Common extractor implementation | NOT_STARTED | — | Phase 4 |
| ERR10619300 calibration | PRIOR CERTIFICATION EXISTS; NEW CALIBRATION PENDING | certified dossier | Phase 5 |
| MARK discovery preflight | NOT_STARTED | — | Phase 6 |
| SRR13573587 extraction | NOT_STARTED | — | Phase 7 |
| SRR13573588 extraction | NOT_STARTED | — | Phase 7 |
| WGS sibling comparison | NOT_STARTED | — | Phase 8 |
| `CNTNAP2` trace | NOT_STARTED | — | Phase 8 |
| Optional all-candidate publication trace | SCOPE UNDECIDED | depends on later claim | Phase 8 if authorized |
| WGS SAGE review | NOT_STARTED | — | Phase 9 |
| WGS corpus freeze and certification record | NOT_STARTED | — | Phase 10 |
| 12-member WES extraction | 1 PRIOR CERTIFIED; COMMON EXTRACTION PENDING FOR 12 | ERR10619300 dossier | Phase 11 |
| WES stratum/outlier probes | NOT_STARTED | — | Phase 12 |
| WES SAGE review | NOT_STARTED | — | Phase 13 |
| WES corpus freeze and certification record | NOT_STARTED | — | Phase 14 |
| Cross-modality compatibility/opportunity gate | BLOCKED | requires two frozen corpora | Phase 15 |
| Common evaluable territory | BLOCKED PENDING SUBSTRATE | requires governed intervals/masks | Phase 16 |
| Certified-corpus comparison | BLOCKED | requires compatibility gate | Phase 17 |
| Comparative SAGE certification record | BLOCKED | requires comparison package | Phase 18 |
| LANE comparative case study | BLOCKED | requires certified claim surface | post-mission handoff |

## 23. Decision Log

| Decision ID | Decision | Rationale | Status |
|---|---|---|---|
| DEC-001 | Maintain exactly one active contract and one active plan | prevent documentation churn and conflicting authorities | LOCKED |
| DEC-002 | Build one manifest-driven certification system | preserve field semantics and avoid 14 hard-coded probes | LOCKED |
| DEC-003 | Calibrate against certified ERR10619300 before corpus execution | use an accepted production oracle | LOCKED |
| DEC-004 | Address MARK operational constraints early | WGS data cannot be relocated economically | LOCKED |
| DEC-005 | Write MARK outputs only to `/root/Desktop/` and bounded temporary workspace | preserve immutable run and TEP directories and support Guacamole transfer | LOCKED |
| DEC-006 | Treat generic lightweight export as secondary transport only | file-size copying does not establish certification semantics | LOCKED |
| DEC-007 | Require independent WES and WGS certification before comparison | prevent comparison from masking source-corpus defects | LOCKED |
| DEC-008 | Consume frozen packages for Certification C | ensure reproducible, reviewed comparative inputs | LOCKED |
| DEC-009 | Keep biological twin language out of WGS evidence | governed evidence supports affected brothers, not twins | LOCKED |
| DEC-010 | Preserve unresolved pedigree mapping | avoid unsupported SRR-to-publication-person assignment | LOCKED |
| DEC-011 | Use streaming genotype scans and bounded external joins | control WGS memory and I/O burden | LOCKED |
| DEC-012 | Reserve final certification vocabulary for SAGE | preserve scientific authority boundary | LOCKED |
| DEC-013 | Require exact observation-ID uniqueness for all 14 runs | identity is foundational to lineage and comparison | LOCKED BY SAGE |
| DEC-014 | Separate core certification from comparative-opportunity evidence | missing denominators should narrow Certification C without weakening valid producer certification | LOCKED BY SAGE |
| DEC-015 | Use `WES-designated PRJEB57558 runs` until assay identity is governed | avoid unsupported capture-exome narration | LOCKED UNTIL RESOLVED |
| DEC-016 | Preserve emitted-observation-universe semantics in every genotype summary | avoid callable-locus and homozygous-reference overinterpretation | LOCKED BY SAGE |
| DEC-017 | Use VAP-governed rarity for certification and `MAF <= 0.001` only for publication reconstruction | prevent threshold conflation | LOCKED BY SAGE |
| DEC-018 | Generate compact exact gene and variant membership surfaces | aggregate counts cannot certify recurrence or overlap | LOCKED BY SAGE |
| DEC-019 | Build exact common territory only from governed WES and WGS interval substrate | preserve denominator integrity | LOCKED BY SAGE |
| DEC-020 | Keep publication claim `CNTNAP2`-specific unless all intended candidates are traced | prevent publication-wide overclaiming | LOCKED BY SAGE |
| DEC-021 | Allow complete Certification C only from `CORPUS CERTIFIED` or `CORPUS CERTIFIED WITH NOTES` packages | preserve full 12-versus-2 membership | LOCKED BY SAGE |
| DEC-022 | Commit every SAGE certification as a durable validation record | repository, not chat, is the long-term evidence authority | LOCKED |

## 24. Proposed Add and Commit Sequence

The first stabilization commit should contain only the two controlling active
documents at their SAGE-compliant v0.2 state.

```bash
git add \
  docs/contracts/system/validation/genotype_aware_wes_wgs_certification_validation_contract.md \
  docs/plans/infrastructure/active/genotype_aware_wes_wgs_certification_implementation_plan.md

git commit -m "Incorporate SAGE conditions into WES/WGS certification controls"
```

Suggested expanded commit message:

```text
Incorporate SAGE conditions into WES/WGS certification controls

- require all-member exact genotype observation identity checks
- add assay-opportunity and common-territory evidence requirements
- add exact compact gene and variant membership surfaces
- distinguish VAP rarity from publication threshold rarity
- preserve emitted-variant observation-universe boundaries
- bound publication concordance claims to traced candidates
- require durable SAGE certification records
```

After SAGE confirms v0.2, implementation should use bounded commits:

```text
1. Reconcile live source state and tests
2. Add scientific-substrate discovery and locked corpus manifest
3. Add common, opportunity, membership, and receipt schemas
4. Implement common per-run certification extractor
5. Add ERR10619300 calibration and acceptance receipts
6. Add MARK preflight and WGS extraction support
7. Add WGS sibling and publication-candidate probes
8. Add WES corpus aggregation and stratum analysis
9. Add frozen-package compatibility and common-territory tooling
10. Add certified-corpus comparison tooling
```

Evidence packages should be committed separately from implementation code after
checksum verification and review.

SAGE certification records should be committed only after SAGE issues the
corresponding determination.

## 25. Planning Acceptance Criteria

This plan is ready for implementation when:

- the controlling contract and plan agree;
- SAGE confirms that its scientific conditions are incorporated;
- every certification requirement has an evidence disposition;
- all 14 members are represented;
- unresolved TEP, assay, target, and callable identities are visible;
- common field meanings are defined;
- emitted-observation-universe and rarity semantics are defined;
- reusable and new probes are distinguished;
- foundational all-member and targeted execution are explicit;
- exact observation-ID uniqueness is mandatory for all 14;
- opportunity and exact-membership schemas are defined;
- common-territory feasibility is discoverable;
- MARK commands and output boundaries are specified;
- mutation safeguards are explicit;
- manifests, receipts, hashes, and package verification are defined;
- scientific resolutions are separated from DEX implementation decisions;
- SAGE can evaluate evidence sufficiency without inspecting large source data.

## 26. Implementation Completion Criteria

DEX implementation is complete when:

1. the common extractor passes its tests and ERR10619300 calibration;
2. all 14 per-run evidence packages verify;
3. exact observation-ID uniqueness is proven for all 14;
4. core opportunity availability and exact membership surfaces are recorded;
5. WGS sibling and required publication-candidate evidence is complete;
6. WES stratum, outlier, and representative evidence is complete;
7. SAGE can issue Certifications A and B;
8. both reviewed corpus packages and durable SAGE records are frozen;
9. the compatibility and opportunity gate completes;
10. common territory is constructed or explicitly unavailable with limitations;
11. comparative outputs derive only from frozen packages;
12. every recurrence, overlap, or expansion claim is exact-membership-supported;
13. SAGE can issue Certification C;
14. the comparative package and SAGE determination are durably recorded;
15. all limitations and revalidation triggers remain visible.

DEX technical completion does not itself constitute scientific certification.

## 27. Immediate Next Actions

```text
1. Commit both controlling documents together.

2. Submit the v0.2 control plane to SAGE-VAP
   for condition-incorporation confirmation.

3. Reconcile live Git HEAD and test state.

4. Perform scientific-substrate discovery for:
       WES assay and target identity
       WES/WGS coverage and callability
       mapping and duplication context
       exact membership feasibility
       common-territory feasibility

5. Implement the locked corpus manifest,
   common schemas, opportunity schemas,
   membership schemas, and receipt framework.

6. Implement and test the common extractor.

7. Calibrate against ERR10619300.

8. Execute MARK discovery-only preflight.
```

No production MARK scan should begin before Actions 1–9 have completed.

## 28. Final Plan Statement

DEX-VAP-v3 shall build and operate one deterministic certification system for
all fourteen modern genotype-aware VAP runs.

The system shall gather evidence beside the canonical data, transport only
bounded receipts, exact compact membership surfaces, and governed summaries,
preserve source and TEP authority, and expose every anomaly and limitation
without silently repairing or interpreting it.

The twelve-member WES-designated corpus and two-member WGS corpus shall be
certified independently and frozen before cross-modality comparison begins.

Certification C shall distinguish:

```text
core preservation-centered claims

from

opportunity-qualified biological claims
```

No density, recurrence, overlap, expansion, or publication-wide claim shall
exceed the denominator, exact-membership, common-territory, or candidate-trace
evidence that supports it.

Every SAGE certification shall become a durable repository validation record
under `docs/validation/comparisons/`.

SAGE-VAP retains scientific certification authority throughout the lifecycle.
