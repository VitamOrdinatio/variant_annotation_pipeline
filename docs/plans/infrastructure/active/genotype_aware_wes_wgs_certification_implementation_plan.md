# Genotype-Aware WES/WGS Certification Implementation Plan

| Field | Value |
|---|---|
| Document status | Draft v0.1 — DEX-VAP implementation proposal; pending SAGE-VAP sufficiency review |
| Plan class | Active infrastructure implementation plan |
| Repository | `variant_annotation_pipeline` |
| Controlling contract | `docs/contracts/system/validation/genotype_aware_wes_wgs_certification_validation_contract.md` |
| Scientific authority | SAGE-VAP |
| Engineering and evidence-acquisition authority | DEX-VAP |
| WES certification object | 12 genotype-aware epilepsy WES runs on sys76 |
| WGS certification object | 2 genotype-aware epilepsy WGS runs on MARK |
| Comparative certification object | Independently certified 12-run WES corpus versus independently certified 2-run WGS corpus |
| Existing certified calibration exemplar | `ERR10619300 / run_2026_07_14_114546` |
| MARK governed output boundary | `/root/Desktop/` |
| Clinical boundary | Research and portfolio validation only; not clinical validation |

---

## 1. Purpose

This plan defines the implementation sequence for the complete VAP
genotype-aware WES/WGS certification mission.

The mission has three separate scientific certification objectives:

```text
Certification A
    certify the complete 12-member
    genotype-aware epilepsy WES corpus on sys76

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

The implementation shall build one reusable certification system rather than a
collection of sample-specific probes.

The intended dependency is:

```text
locked corpus identity
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
controlled compatibility gate
    ↓
comparative evidence products
    ↓
SAGE comparative determination
```

No comparative result may compensate for an uncertified source run or source
corpus.

---

## 2. Relationship to the Controlling Contract

This plan implements:

```text
docs/contracts/system/validation/
    genotype_aware_wes_wgs_certification_validation_contract.md
```

The contract is authoritative if this plan and the contract conflict.

This plan may change sequencing, module boundaries, command structure, or
performance strategy without changing the contract's scientific semantics.

A change that alters corpus identity, evidence meaning, certification scope,
authority boundaries, or preservation doctrine requires contract review.

---

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

The existing ERR10619300 certification dossier is the empirical calibration
precedent for the common producer-certification surface.

---

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

### 4.4 Execution-provenance authority

These are independent required artifacts:

```text
metadata/execution_provenance.json
metadata/config_snapshot.yaml
```

Their TEP copies shall be evaluated independently.

### 4.5 Transport authority

TEP-VAP transports producer-authored evidence without reinterpretation.

Where direct transport identity is required, source and TEP artifacts shall be
checked by cryptographic hash and bytewise comparison.

### 4.6 Ecosystem boundary

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

### 4.7 Publication boundary

The Badshah et al. publication is an external comparator, not a truth set.

The two WGS individuals are affected brothers. They shall not be described as
biological twins.

The mapping of `SRR13573587` and `SRR13573588` to publication individuals
`V-2` and `V-4` remains unknown unless governed evidence resolves it.

---

## 5. Program Architecture

### 5.1 One certification system

The implementation target is:

```text
one locked 14-member corpus manifest
one common field vocabulary
one manifest-driven command-line interface
one tested certification library
one receipt and package format
modality-specific additive probes
corpus aggregators
comparison tools that consume frozen certified packages
```

The implementation shall not create fourteen independent sample-specific probe
systems.

### 5.2 Proposed code layout

The preferred implementation layout is:

```text
src/certification/
    __init__.py
    models.py
    manifest.py
    discovery.py
    provenance.py
    configuration.py
    genotype.py
    stage_reconciliation.py
    tep.py
    sanity.py
    traces.py
    corpus.py
    wgs_siblings.py
    cntnap2.py
    compatibility.py
    receipts.py
    packaging.py

scripts/validation/
    run_genotype_aware_certification.py

tests/certification/
    test_manifest.py
    test_discovery.py
    test_provenance.py
    test_configuration.py
    test_genotype.py
    test_stage_reconciliation.py
    test_tep.py
    test_receipts.py
    test_wgs_siblings.py
    test_cntnap2.py
    test_corpus.py
    test_compatibility.py
```

The exact module split may be simplified during implementation if field
semantics, testability, and deterministic behavior remain unchanged.

### 5.3 Proposed command surface

A single CLI should expose explicit subcommands:

```text
preflight
extract-run
aggregate-corpus
compare-wgs-siblings
trace-cntnap2
build-compatibility-audit
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

### 5.4 Locked input manifest

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
node_id
read_count_stratum
scientific_description
canonical_run_path
canonical_tep_path
tep_id
prior_certification_state
prior_certification_reference
identity_state
notes
```

Initially unresolved paths or TEP IDs shall be represented explicitly as
`UNRESOLVED_PENDING_PREFLIGHT`; they shall not be inferred silently.

Any later corpus identity change requires a new manifest version.

---

## 6. Locked Corpus Identity

### 6.1 Certification A — sys76 WES

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

The q1, median, and q3 labels are project-specific read-count strata, not direct
measurements of target coverage.

### 6.2 Certification B — MARK WGS

| Sample/SRA | Run ID | Scientific description | Current certification role |
|---|---|---|---|
| `SRR13573587` | `run_2026_07_29_123020` | affected sibling WGS | pending per-run evidence |
| `SRR13573588` | `run_2026_08_01_092338` | affected sibling WGS | pending per-run evidence |

### 6.3 Certification C — comparison object

Certification C shall consume only frozen, SAGE-reviewed corpus packages.

Raw run directories shall not be reopened as uncontrolled comparative inputs
once the two corpus packages have been frozen.

---

## 7. Evidence Disposition Strategy

Every requirement shall use one of four dispositions:

```text
AVAILABLE_DIRECTLY
    present as a small canonical or TEP artifact

AVAILABLE_BY_EXISTING_EXTRACTOR
    emitted by an existing lightweight utility

AVAILABLE_BY_EXISTING_PROBE
    supported by existing validation logic or a prior receipt pattern

NEW_BOUNDED_PROBE_REQUIRED
    requires new observational node-local computation
```

Existing logic may be refactored into the common library without changing the
scientific meaning of its output.

The generic small-file exporter remains a secondary transport utility. It is
not the certification extractor because it does not establish the required
semantics of skipped high-cardinality artifacts.

---

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
| GEN-010 | A/B | Deterministic observation IDs and duplicate indicators | NEW_BOUNDED_PROBE_REQUIRED | all 14; exact high-cost as authorized | genotype TSV | identity summary and targeted uniqueness probe | yes at summary level |
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
| WES-001 | A | All-member completeness | NEW_BOUNDED_PROBE_REQUIRED | 12 WES | per-run packages | WES corpus manifest and readiness table | yes |
| WES-002 | A | q1/median/q3 genotype summaries | NEW_BOUNDED_PROBE_REQUIRED | 12 WES | per-run evidence | stratum genotype summary | yes |
| WES-003 | A | q1/median/q3 semantic summaries | NEW_BOUNDED_PROBE_REQUIRED | 12 WES | per-run evidence | stratum semantic summary | yes |
| WES-004 | A | WES outlier register | NEW_BOUNDED_PROBE_REQUIRED | 12 WES | corpus summaries | member outlier register | yes |
| WES-005 | A | Representative high-cost audit | NEW_BOUNDED_PROBE_REQUIRED | q1, median, q3, exemplar, anomaly | canonical artifacts | targeted probe manifest and outputs | SAGE-dependent |
| WGS-001 | B | Chromosome-level observation and semantic counts | NEW_BOUNDED_PROBE_REQUIRED | both WGS | genotype and stage artifacts | WGS chromosome summary | yes |
| WGS-002 | B | WGS scale and large-artifact transport status | NEW_BOUNDED_PROBE_REQUIRED | both WGS | file metadata and hashes | WGS scale summary | yes |
| WGS-003 | B | Shared/private sibling observations | NEW_BOUNDED_PROBE_REQUIRED | WGS pair | coordinate/allele identities | sibling comparison summary | yes |
| WGS-004 | B | Shared identical and discordant genotype states | NEW_BOUNDED_PROBE_REQUIRED | WGS pair | genotype observations | sibling genotype comparison | yes |
| WGS-005 | B | Shared homozygous alternate observations | NEW_BOUNDED_PROBE_REQUIRED | WGS pair | genotype observations | bounded summary and exemplars | yes |
| WGS-006 | B | Shared rare homozygous observations | NEW_BOUNDED_PROBE_REQUIRED | WGS pair | genotype and governed frequency fields | bounded summary; rarity definition SAGE-reviewed | yes if requested definition supplied |
| WGS-007 | B | Shared complex/deferred relationships | NEW_BOUNDED_PROBE_REQUIRED | WGS pair | genotype observations | complex relationship summary | yes |
| WGS-008 | B | `CNTNAP2` coordinate/transcript trace | NEW_BOUNDED_PROBE_REQUIRED | both WGS | Stage 07–12, genotype, TEP | trace TSV and report | yes |
| WGS-009 | B | Pedigree identity mapping | AVAILABLE_DIRECTLY or UNRESOLVED | WGS pair | governed metadata | identity mapping table | no if explicitly unknown |
| CMP-001 | C | Frozen WES and WGS package identity | AVAILABLE_DIRECTLY | two corpora | frozen receipts | comparative input manifest | yes |
| CMP-002 | C | Source-state and configuration compatibility | NEW_BOUNDED_PROBE_REQUIRED | two corpora | frozen evidence | compatibility audit | yes |
| CMP-003 | C | Reference, tool, resource, and schema compatibility | NEW_BOUNDED_PROBE_REQUIRED | two corpora | frozen evidence | compatibility audit | yes |
| CMP-004 | C | Node/modality difference classification | NEW_BOUNDED_PROBE_REQUIRED | two corpora | compatibility audit | difference classification | yes |
| CMP-005 | C | Absolute and normalized preservation comparisons | NEW_BOUNDED_PROBE_REQUIRED | two corpora | frozen summaries | preservation comparison | yes |
| CMP-006 | C | Genotype, provenance, lineage, and semantic comparisons | NEW_BOUNDED_PROBE_REQUIRED | two corpora | frozen summaries | comparative tables | yes |
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
| Genotype TSV scanner | not present as common certification utility | new | one streaming pass for all required per-run summaries |
| Corpus aggregator | not present | new | consume only verified per-run packages |
| WGS sibling comparator | not present | new | deterministic external join or node-local database strategy |
| `CNTNAP2` trace | not present in common form | new | coordinate/gene/transcript/protein-aware bounded trace |
| Compatibility gate | not present | new | consume only frozen certified package summaries |
| Receipt/package verifier | partial patterns only | new | common deterministic package format and verification command |

---

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
node_id
probe_execution_id
probe_schema_version
probe_git_commit
probe_script_sha256
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
BYTE_MATCH
BYTE_MISMATCH
SCHEMA_VALID
SCHEMA_INVALID
PROBE_PASS
PROBE_FAIL
NOT_APPLICABLE
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

### 10.10 WES-specific products

```text
wes_read_count_stratum_summary.tsv
wes_stratum_genotype_summary.tsv
wes_stratum_semantic_surface_summary.tsv
wes_member_outlier_register.tsv
wes_targeted_probe_manifest.json
```

### 10.11 WGS-specific products

```text
wgs_sibling_identity_mapping.tsv
wgs_sibling_shared_private_summary.tsv
wgs_sibling_genotype_concordance.tsv
wgs_shared_homozygous_summary.tsv
wgs_chromosome_level_summary.tsv
wgs_complex_relationship_summary.tsv
cntnap2_coordinate_transcript_trace.tsv
cntnap2_trace_report.md
wgs_publication_comparator_summary.md
wgs_targeted_probe_manifest.json
```

### 10.12 Cross-modality products

```text
wes_wgs_compatibility_audit.tsv
wes_wgs_normalization_definitions.md
wes_wgs_preservation_comparison.tsv
wes_wgs_genotype_comparison.tsv
wes_wgs_provenance_lineage_comparison.tsv
wes_wgs_semantic_surface_comparison.tsv
wes_wgs_difference_classification.tsv
```

### 10.13 Extraction manifest JSON

The extraction manifest shall declare:

- execution identity;
- corpus-manifest identity;
- requested members;
- resolved source paths;
- expected outputs;
- probe and schema versions;
- all-member versus targeted scope;
- temporary and final output roots;
- package version;
- restart policy.

### 10.14 Extraction receipt JSON

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
- mutation-safety checks;
- package archive identity.

Volatile fields shall be isolated from scientific comparisons.

---

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
receipts, SAGE determinations, and frozen-package identities.

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
    ├── per_run/
    │   ├── SRR13573587/
    │   └── SRR13573588/
    ├── sibling_comparison/
    ├── cntnap2_trace/
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

---

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

The genotype scanner shall calculate as many required summaries as practical in
one streaming pass.

It shall not load a complete WGS genotype table into memory.

### 13.2 Exact joins

WGS sibling comparisons may use:

- external sort and merge;
- SQLite;
- DuckDB;
- another deterministic node-local engine.

The selected method shall preserve exact coordinate-and-allele identities and
shall record its version and command configuration.

### 13.3 Hash policy

Full SHA-256 is required for:

- execution-provenance receipts;
- configuration snapshots;
- processed and TEP genotype artifacts;
- entity inventories;
- lineage manifests;
- frozen evidence archives;
- critical Stage 07/08 anchors named in the final schema.

The plan does not require hashing every large intermediate artifact unless the
hash supports a defined certification claim.

### 13.4 Batch versus per-run work

Batch-level evidence is captured once per node/source state:

- Git identity;
- working-tree state;
- environment identity;
- dependency state;
- complete test result;
- probe source hashes.

Per-run evidence is captured separately for every run.

Corpus and targeted probes execute only after their required per-run packages
verify successfully.

---

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

### Phase 1 — Contract and plan stabilization

### Objective

Commit the controlling contract and this active plan, then obtain SAGE-VAP
scientific-sufficiency review before implementation.

### Deliverables

```text
docs/contracts/system/validation/
    genotype_aware_wes_wgs_certification_validation_contract.md

docs/plans/infrastructure/active/
    genotype_aware_wes_wgs_certification_implementation_plan.md
```

### Exit gate

- contract and plan are internally consistent;
- SAGE confirms the evidence model is sufficient or returns bounded changes;
- no unresolved scientific question blocks schema implementation.

---

### Phase 2 — Corpus-manifest and common-schema implementation

### Objective

Create the locked input manifest, common models, state vocabulary, stable
serialization, and receipt schemas.

### Work packages

1. Implement manifest parser and validator.
2. Encode all 14 locked members.
3. Represent unresolved TEP paths explicitly.
4. Implement common identity model.
5. Implement stable TSV and JSON writers.
6. Implement technical state validation.
7. Implement output-root safety checks.
8. Implement manifest and receipt validation.

### Test requirements

- duplicate member rejection;
- unknown assay or node rejection;
- unresolved identity handling;
- schema-version handling;
- stable serialization;
- output-path traversal and canonical-path rejection;
- deterministic manifest hashing.

### Exit gate

- corpus manifest validates;
- all 14 members are represented exactly once;
- common schemas pass unit tests;
- package and receipt schemas are frozen as v1.

---

### Phase 3 — Common per-run extractor implementation

### Objective

Implement the modality-neutral evidence surface used for all 14 runs.

### Work packages

1. Preflight discovery.
2. Run and TEP identity extraction.
3. Execution-provenance validation.
4. Configuration-snapshot validation.
5. Streaming genotype scanner.
6. Stage reconciliation.
7. TEP inventory and lineage audit.
8. Scientific sanity summaries.
9. Deterministic bounded traces.
10. Manifest, receipt, log, and package emission.

### Required properties

- no sample-specific expected counts in code;
- no hidden WES/WGS field redefinition;
- read-only source access;
- deterministic output;
- clear failure state;
- bounded memory use;
- progress reporting suitable for MARK execution.

### Exit gate

- unit tests pass;
- representative fixture tests pass;
- malformed and edge-case genotype tests pass;
- package verification tests pass;
- common extractor is ready for calibration.

---

### Phase 4 — ERR10619300 calibration

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
- provenance and config transport identity;
- TEP validation and lineage registration;
- no scientifically changed shared coding rows in the prior elevation comparison;
- known bounded limitations remain visible.

The calibration shall not require byte identity with historical dossier tables
if the new schema is intentionally different. It must reproduce the accepted
technical conclusions and explain every schema-level difference.

### Exit gate

- common extractor reproduces the certified technical state;
- discrepancies are resolved or sent to SAGE;
- ERR10619300 is represented in the new corpus program without weakening its
  prior certification.

---

### Phase 5 — MARK discovery-only preflight

### Objective

Resolve actual MARK paths, TEP identities, artifact sizes, and execution
constraints before scanning large WGS artifacts.

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
- existing validation-report state.

### Exit gate

- both run and TEP identities are locked;
- all required source artifacts are locatable;
- output and temporary paths are safe;
- package transfer size is acceptable;
- no blocking preflight anomaly remains.

---

### Phase 6 — MARK common per-run WGS extraction

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
2. Extract SRR13573587 common evidence.
3. Verify its package.
4. Extract SRR13573588 common evidence.
5. Verify its package.
6. Build initial WGS corpus manifest and anomaly register.
7. Package and download outputs.
8. Verify archive SHA-256 on sys76.

### Exit gate

- both per-run packages are `PACKAGE_VERIFIED`;
- no member is omitted;
- all required evidence classes are complete, `NOT_APPLICABLE`, or visibly
  `UNRESOLVED`;
- initial anomaly register is ready for SAGE review.

---

### Phase 7 — WGS sibling and `CNTNAP2` probes

### Objective

Generate the WGS-specific corpus evidence required for Certification B.

#### 7.1 Sibling comparison

Use exact coordinate-and-allele-aware identities to calculate:

- shared observations;
- private observations per sibling;
- shared identical genotype states;
- discordant genotype states at shared identities;
- shared homozygous alternate observations;
- shared rare homozygous observations under a SAGE-reviewed rarity definition;
- shared multiallelic and complex/deferred relationships;
- chromosome-level shared/private summaries;
- deterministic bounded exemplars.

The probe shall not infer inheritance or causality.

#### 7.2 `CNTNAP2` trace

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

It shall not search only one publication cDNA string.

#### 7.3 Pedigree identity

Repository or accession metadata shall be searched for authoritative
`SRR → V-2/V-4` mapping.

If no governed mapping is found, the output shall preserve `UNRESOLVED`.

### Exit gate

- WGS-specific products verify;
- `CNTNAP2` evidence is reviewable without large artifacts;
- all limitations and unresolved mapping are explicit;
- SAGE has enough evidence for first-pass WGS review.

---

### Phase 8 — SAGE WGS review and bounded follow-up

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

### Phase 9 — Freeze the certified WGS corpus package

### Objective

Freeze the SAGE-reviewed WGS package when it receives a usable corpus
determination.

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

### Exit gate

- package is immutable by convention and checksum;
- replacement requires a new package version;
- Certification C may reference it only after WES freezing is also complete.

---

### Phase 10 — sys76 all-member WES extraction

### Objective

Run the calibrated common extractor against all 12 WES runs.

### Execution order

1. Capture sys76 repository and environment receipt.
2. Resolve all 12 run and TEP paths.
3. Re-run or incorporate ERR10619300 calibration evidence by governed reference.
4. Extract the remaining 11 members.
5. Verify every per-run package.
6. Aggregate the initial WES corpus evidence.
7. Build stratum summaries and anomaly register.

### Required rule

Prior ERR10619300 certification may be incorporated only when the source run,
TEP, schemas, and evidence identities remain unchanged.

### Exit gate

- all 12 members are represented;
- every package verifies;
- q1, median, and q3 summaries exist;
- outliers and unresolved conditions are visible.

---

### Phase 11 — WES stratum, outlier, and representative probes

### Objective

Produce the WES-specific evidence required for Certification A.

### Required summaries

- genotype completeness by stratum;
- no-call and partial-call behavior by stratum;
- multiallelic and complex relationship distributions;
- Stage 07 preservation;
- Stage 08–12 semantic routing;
- reviewability and priority states;
- rare and high-impact evidence surfaces;
- anomaly rates.

### Representative set

The targeted set shall cover, at minimum:

```text
one q1 member
one median member
one q3 member
ERR10619300 certified exemplar
any detected outlier
```

A specimen may satisfy more than one category if SAGE agrees the coverage
remains sufficient.

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
- SAGE has enough evidence for first-pass WES review.

---

### Phase 12 — SAGE WES review and bounded follow-up

### Objective

Submit the complete 12-member WES evidence package to SAGE-VAP.

### Exit gate

SAGE issues per-run and corpus outcomes or requests bounded additional evidence.

---

### Phase 13 — Freeze the certified WES corpus package

### Objective

Freeze the SAGE-reviewed WES package using the same package and receipt
semantics as WGS.

### Exit gate

- package is checksum-frozen;
- all member determinations and limitations are referenced;
- both Certifications A and B now have frozen usable corpus packages.

---

### Phase 14 — Cross-modality compatibility gate

### Objective

Determine whether the frozen WES and WGS packages support controlled comparison.

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
- node and operating environment.

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
- blocking and limiting differences are visible;
- SAGE determines which comparison claims remain scientifically valid.

---

### Phase 15 — Controlled WES/WGS comparison

### Objective

Build Certification C products from the two frozen packages only.

### Comparison classes

The comparison shall separate:

1. invariant architecture and preservation behavior;
2. operational and node context;
3. absolute biological counts;
4. normalized genomic-territory-aware measures;
5. genotype-state composition;
6. semantic-surface composition;
7. provenance and lineage completeness;
8. WGS sibling relatedness effects;
9. expected WGS noncoding search-space expansion;
10. unresolved confounding.

Raw counts shall not be interpreted without denominator and search-space
context where normalization is required.

### Exit gate

- all comparative products derive from frozen package hashes;
- no raw run directory was used as an uncontrolled input;
- differences are classified rather than overinterpreted;
- SAGE can issue a comparative determination.

---

### Phase 16 — SAGE comparative certification and mission closure

### Objective

Support SAGE-VAP in issuing Certification C.

After SAGE review:

- freeze the comparative evidence package;
- record the final determination and limitations;
- record revalidation triggers;
- hand the certified claim surface to LANE-VAP for case-study authorship;
- retain DEX technical support for artifact references and bounded clarification.

The implementation mission is complete only after Certifications A, B, and C
have reviewable final states and the associated packages are frozen or clearly
recorded as insufficient/not certified.

---

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

### 16.3 MARK preflight

Illustrative command:

```bash
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
  trace-cntnap2 \
  --corpus-manifest config/certification/genotype_aware_wes_wgs_corpus_v1.tsv \
  --output-root /root/Desktop/vap_certification
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

---

## 17. SAGE–DEX Review Checkpoints

| Checkpoint | DEX submission | SAGE decision |
|---|---|---|
| R1 | Contract and implementation plan | evidence-plan sufficiency |
| R2 | ERR10619300 calibration package | common extractor scientific adequacy |
| R3 | MARK preflight package | WGS source-object readiness |
| R4 | Initial two-run WGS package | first-pass WGS sufficiency and anomaly requests |
| R5 | WGS targeted probes | per-run and corpus Certification B determination |
| R6 | Initial 12-run WES package | first-pass WES sufficiency and anomaly requests |
| R7 | WES stratum and targeted probes | per-run and corpus Certification A determination |
| R8 | Compatibility audit | allowed Certification C comparison scope |
| R9 | Comparative package | Certification C determination |
| R10 | Later case-study technical review | bounded artifact clarification only |

A request for another bounded probe is not itself a certification failure.

---

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
- duplicate source identities;
- receipt hashing;
- package verification;
- failure receipts;
- deterministic traces;
- compatibility classifications.

### 18.2 Integration fixtures

Fixtures shall include:

- a small WES-like run;
- a small WGS-like run;
- matching processed and TEP artifacts;
- deliberate hash mismatch;
- missing entity;
- broken lineage edge;
- Stage 07/08 loss case;
- genotype no-call edge cases;
- sibling shared/private examples;
- `CNTNAP2` transcript/notation variation.

### 18.3 Calibration test

ERR10619300 is the production calibration object, not a lightweight unit-test
fixture.

Its extraction receipt and reconciliation report shall be retained as a
certification-system acceptance test.

### 18.4 Regression rule

A change to extractor semantics, common schema, or compatibility logic shall:

1. increment the relevant schema or probe version;
2. rerun unit and integration tests;
3. rerun ERR10619300 calibration;
4. identify affected frozen packages;
5. trigger SAGE revalidation review where required.

---

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
EXTRACTOR_ANOMALY
ARTIFACT_ANOMALY
PACKAGING_ANOMALY
UNRESOLVED
```

SAGE determines the scientific consequence.

---

## 20. Open-Question Register

### 20.1 Scientific questions for SAGE-VAP

| ID | Question | Why it matters | Blocking point | State |
|---|---|---|---|---|
| SAGE-Q01 | Which exact high-cost genotype identity checks are mandatory for the first-pass WGS package rather than anomaly follow-up? | controls MARK I/O burden and evidence sufficiency | before Phase 6 production extraction | OPEN |
| SAGE-Q02 | Is exact observation-ID uniqueness required for all 14 members, or is a summary plus representative exact audit sufficient? | exact uniqueness may require large memory or external sorting | before final genotype scanner schema | OPEN |
| SAGE-Q03 | What governed frequency definition shall be used for “shared rare homozygous” WGS evidence? | avoids an implementation-defined scientific threshold | before WGS sibling probe | OPEN |
| SAGE-Q04 | What constitutes publication concordance when `CNTNAP2` coordinate/protein evidence agrees but transcript or cDNA notation differs? | controls trace classification boundary | before final trace interpretation schema | OPEN |
| SAGE-Q05 | Is SRR-to-`V-2`/`V-4` mapping required for Certification B, or may it remain unknown through certification and only limit case-study narration? | defines consequence of unresolved pedigree identity | before SAGE WGS determination | OPEN |
| SAGE-Q06 | Which q1, median, and q3 WES representatives require exact high-cost follow-up if the all-member lightweight package shows no anomalies? | controls representative coverage | before Phase 11 | OPEN |
| SAGE-Q07 | Which SAGE corpus outcomes qualify as “usable” for frozen-package entry into Certification C? | contract requires usable determinations but comparison claim scope may vary | before corpus freezing | OPEN |

### 20.2 DEX implementation decisions not requiring SAGE

The following remain within DEX authority unless they change scientific
meaning:

- external sort versus SQLite/DuckDB;
- chunk size and progress cadence;
- internal class and function names;
- temporary-file naming;
- compression level;
- log formatting;
- atomic rename implementation;
- number of modules behind the single CLI.

---

## 21. Risk Register

| Risk | Effect | Mitigation | Owner | State |
|---|---|---|---|---|
| Live `HEAD` differs from certified `46a814a...` | calibration ambiguity | complete Phase 0 reconciliation before code changes | DEX | OPEN |
| 160-test certified state versus 166-test onboarding snapshot | unclear source evolution | identify six-test and implementation delta | DEX | OPEN |
| WGS TEP paths or IDs differ from convention | wrong source object | discovery-only preflight; no inferred paths | DEX | OPEN |
| Large WGS scans overload memory | failed or disruptive probe | streaming pass and node-local external joins | DEX | CONTROLLED BY DESIGN |
| Repeated scans create excessive I/O | node burden | combine summaries into one governed pass | DEX | CONTROLLED BY DESIGN |
| Output accidentally enters `results/` or TEP tree | source mutation risk | output-root guard and canonical-path rejection | DEX | CONTROLLED BY DESIGN |
| Guacamole transfer truncation | invalid evidence package | archive SHA-256 verification on sys76 | DEX | CONTROLLED BY DESIGN |
| Node and modality are confounded | invalid scientific attribution | explicit compatibility classification and limitation | SAGE/DEX | INHERENT |
| WGS members are related siblings | non-independent corpus | preserve family structure; no population inference | SAGE | INHERENT |
| `CNTNAP2` publication notation inconsistent | false negative trace | coordinate/gene/transcript/protein-aware search | DEX/SAGE | CONTROLLED BY DESIGN |
| Pedigree mapping unresolved | sample-specific narration limitation | preserve unknown unless governed evidence found | SAGE/DEX | OPEN |
| Biological outlier mistaken for technical failure | inappropriate rejection | anomaly classes plus SAGE interpretation | SAGE | CONTROLLED BY PROCESS |
| Genotype distinct-count sentinel ambiguity | misleading identity metric | explicit nonempty/missing/distinct-nonempty fields | DEX | PLANNED FIX |
| TEP regenerated after certification | frozen package invalidation | package identity and revalidation trigger | DEX/SAGE | CONTROLLED BY CONTRACT |
| Probe semantics change mid-program | incompatible member packages | versioned schema and ERR10619300 recalibration | DEX | CONTROLLED BY CONTRACT |
| Comparison starts before corpus freeze | uncontrolled evidence | Gate 5 and Gate 6 enforcement | DEX/SAGE | CONTROLLED BY CONTRACT |

---

## 22. Status Ledger

| Work package | Current state | Evidence/reference | Next action |
|---|---|---|---|
| Five-phase DEX-VAP-v3 onboarding | COMPLETE | Phase 01–05 audits | none |
| Scientific certification framework | COMPLETE | governing validation document | maintain version awareness |
| SAGE→DEX implementation handoff | COMPLETE | genotype certification handoff | use as planning authority |
| System validation contract | DRAFTED | companion contract v0.1 | commit and SAGE review |
| Active implementation plan | DRAFTED | this document v0.1 | commit and SAGE review |
| Live repository reconciliation | NOT_STARTED | — | Phase 0 |
| Locked machine-readable corpus manifest | NOT_STARTED | — | Phase 2 |
| Common schema and receipt implementation | NOT_STARTED | — | Phase 2 |
| Common extractor implementation | NOT_STARTED | — | Phase 3 |
| ERR10619300 calibration | PRIOR CERTIFICATION EXISTS; NEW CALIBRATION PENDING | certified dossier | Phase 4 |
| MARK discovery preflight | NOT_STARTED | — | Phase 5 |
| SRR13573587 extraction | NOT_STARTED | — | Phase 6 |
| SRR13573588 extraction | NOT_STARTED | — | Phase 6 |
| WGS sibling comparison | NOT_STARTED | — | Phase 7 |
| `CNTNAP2` trace | NOT_STARTED | — | Phase 7 |
| WGS SAGE review | NOT_STARTED | — | Phase 8 |
| WGS corpus freeze | NOT_STARTED | — | Phase 9 |
| 12-member WES extraction | 1 PRIOR CERTIFIED; COMMON EXTRACTION PENDING FOR 12 | ERR10619300 dossier | Phase 10 |
| WES stratum/outlier probes | NOT_STARTED | — | Phase 11 |
| WES SAGE review | NOT_STARTED | — | Phase 12 |
| WES corpus freeze | NOT_STARTED | — | Phase 13 |
| Cross-modality compatibility gate | BLOCKED | requires two frozen corpora | Phase 14 |
| Certified-corpus comparison | BLOCKED | requires compatibility gate | Phase 15 |
| Comparative SAGE certification | BLOCKED | requires comparison package | Phase 16 |
| LANE comparative case study | BLOCKED | requires Certifications A, B, and C | post-mission handoff |

---

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

---

## 24. Proposed Add and Commit Sequence

The first documentation commit should contain only the two controlling active
documents.

```bash
git add \
  docs/contracts/system/validation/genotype_aware_wes_wgs_certification_validation_contract.md \
  docs/plans/infrastructure/active/genotype_aware_wes_wgs_certification_implementation_plan.md

git commit -m "Define genotype-aware WES/WGS certification program"
```

Suggested expanded commit message:

```text
Define genotype-aware WES/WGS certification program

- add the controlling system validation contract
- add the active implementation plan for 12 WES and 2 WGS runs
- enforce independent corpus certification before comparison
- define MARK node-local, read-only evidence acquisition
- establish common extractor, receipt, freeze, and compatibility gates
```

After SAGE approves the plan, implementation should use bounded commits:

```text
1. Add certification corpus manifest and common schemas
2. Implement common per-run certification extractor
3. Add ERR10619300 calibration and acceptance receipts
4. Add MARK preflight and WGS extraction support
5. Add WGS sibling and CNTNAP2 probes
6. Add WES corpus aggregation and stratum analysis
7. Add frozen-package compatibility and comparison tooling
```

Evidence packages should be committed separately from implementation code after
checksum verification and review.

---

## 25. Planning Acceptance Criteria

This plan is ready for implementation when:

- the controlling contract and plan agree;
- every certification requirement has an evidence disposition;
- all 14 members are represented;
- unresolved TEP identities are visible;
- common field meanings are defined;
- reusable and new probes are distinguished;
- all-member and targeted execution are explicit;
- MARK commands and output boundaries are specified;
- mutation safeguards are explicit;
- manifests, receipts, hashes, and package verification are defined;
- scientific questions are separated from DEX implementation decisions;
- SAGE can evaluate evidence sufficiency without inspecting large source data.

---

## 26. Implementation Completion Criteria

DEX implementation is complete when:

1. the common extractor passes its tests and ERR10619300 calibration;
2. all 14 per-run evidence packages verify;
3. WGS sibling and `CNTNAP2` evidence is complete;
4. WES stratum, outlier, and representative evidence is complete;
5. SAGE can issue Certifications A and B;
6. both reviewed corpus packages are frozen;
7. the compatibility gate completes;
8. comparative outputs derive only from frozen packages;
9. SAGE can issue Certification C;
10. all limitations and revalidation triggers remain visible.

DEX technical completion does not itself constitute scientific certification.

---

## 27. Immediate Next Actions

```text
1. Commit the contract and this plan.

2. Submit both documents to SAGE-VAP
   for scientific-sufficiency review.

3. Reconcile live Git HEAD and test state.

4. Implement the locked corpus manifest,
   common schemas, and receipt framework.

5. Implement and test the common extractor.

6. Calibrate against ERR10619300.

7. Execute MARK discovery-only preflight.
```

No production MARK scan should begin before Actions 1–6 have completed.

---

## 28. Final Plan Statement

DEX-VAP-v3 shall build and operate one deterministic certification system for
all fourteen modern genotype-aware VAP runs.

The system shall gather evidence beside the canonical data, transport only
bounded receipts and summaries, preserve source and TEP authority, and expose
all anomalies and limitations without silently repairing or interpreting them.

The twelve-member WES corpus and two-member WGS corpus shall be certified
independently and frozen before cross-modality comparison begins.

SAGE-VAP retains scientific certification authority throughout the lifecycle.
