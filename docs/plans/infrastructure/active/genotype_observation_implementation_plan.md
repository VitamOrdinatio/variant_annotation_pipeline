# Genotype Observation Implementation Plan

## Purpose

This plan defines the engineering sequence for implementing first-class genotype observation surfacing within the Variant Annotation Pipeline (VAP).

It translates the certified genotype observation architecture, design, specification, schema, validation, and contract into an ordered implementation path.

The implementation must satisfy two Prime Directives:

```text
1. Do not mutate existing VAP behavior outside genotype.

2. Elevate genotype into both:
       processed/ outputs
   and TEP-VAP emission
   for existing canonical runs and all future eligible runs.
```

The implementation shall remain additive.

The existing 13-stage variant-centric pipeline shall remain scientifically and operationally unchanged.

---

## Governing Inputs

Implementation shall conform to:

```text
docs/architecture/genotype_observation_architecture.md

docs/design/genotype_observation_design.md

docs/implementation/specifications/genotype_observation_specification.md

docs/implementation/schemas/genotype_observation_schema.md

docs/validation/genotype_observation_validation.md

docs/contracts/system/core/genotype_observation_contract.md
```

Where implementation and certified documentation disagree, the certified documentation is authoritative.

---

## Implementation Goals

The implementation shall provide:

```text
one canonical genotype projection implementation

three processed genotype artifacts

automatic future pipeline emission

first-class TEP-VAP genotype transport

lightweight pytest validation

additive hardening of the 13 canonical runs

run-external backfill receipts

strict non-interference with existing VAP outputs
```

The canonical processed artifacts are:

```text
processed/genotype_observations.tsv

processed/genotype_projection_summary.json

processed/genotype_source_header_context.json
```

The canonical TEP-VAP artifacts are:

```text
entities/genotype/genotype_observations.tsv

entities/genotype/genotype_projection_summary.json

entities/genotype/genotype_source_header_context.json
```

---

## Implementation Wave Roadmap

The implementation phases below are grouped into operational delivery waves.

The waves provide the intended engineering execution sequence while the phases
remain the authoritative implementation decomposition.

```text
Wave 1
    Repository surveillance
    Variant identity substrate
    Lightweight fixture framework

    Corresponding phases:
        Phase 0
        Phase 1

Wave 2
    Canonical genotype projection implementation

    Corresponding phases:
        Phase 2

Wave 2.1
    Policy-alignment hardening

    Objectives:

        governed multiallelic relationship handling

        advisory versus warning separation

        symbolic ALT classification

        spanning-deletion classification

        called allele index validation

        relationship resolution targets

    No VDB brokerage or RDGP reasoning shall be implemented during this wave.

Wave 3
    Local engineering proof

    Corresponding phases:
        Phase 3
        Phase 4

Wave 4
    TEP integration

    Corresponding phases:
        Phase 5
        Phase 6

Wave 5
    Full local repository validation

    Corresponding phases:
        Phase 7

Wave 6
    Production rehearsal

    Corresponding phases:
        Phase 8
        Phase 9

Wave 7
    MARK production rollout

    Corresponding phases:
        Phase 10
        Phase 11
```

---

## Non-Goals

This implementation shall not:

```text
modify Stage 08–13 scientific behavior

thread genotype columns through variant-centric TSVs

rerun FASTQ processing

rerun alignment

rerun variant calling

rerun normalization

rerun annotation for canonical backfill

implement VDB ingestion

implement RDGP inheritance reasoning

create a genome-wide genotype matrix

infer callability or assay opportunity

infer biological ploidy, hemizygosity, carrier state,
compound heterozygosity, or disease causality
```

---

# Phase 0 — Repository Surveillance and Integration Mapping

## Objective

Confirm the exact current code paths that must be extended before any implementation changes are made.

## Inspect

```text
run_pipeline.py

src/pipeline_runner.py

pipeline/stage07_variant_annotation.py

scripts/tep/build_vap_tep_entities.py

scripts/tep/build_vap_tep_lineage_manifest.py

scripts/tep/validate_vap_tep.py

existing pipeline state initialization and serialization

existing pytest fixtures and TEP tests

Stage 13 artifact-manifest generation code

Stage 13 final-summary generation code

Stage 13 run-report generation code

the mechanism by which processed artifacts are discovered
or registered for Stage 13 context
```

## Determine

```text
authoritative annotated VCF artifact key

authoritative sample_id source

run_id source

reference_build source

processed output path construction

pipeline state registration conventions

TEP entity inventory structure

lineage edge structure

validation report extension points

whether lineage_manifest.json supports source artifacts
that are not transported inside TEP-VAP

whether the annotated VCF should be represented as:
    an external source artifact
    a source identity record
    a source identity set
    or another existing lineage-native construct

how source_vcf_sha256 and source_vcf_header_hash
bind the external VCF source to the packaged genotype entity

whether every lineage node must also appear
in entity_inventory.json

whether current TEP --overwrite behavior rewrites
pre-existing transported entity files

whether genotype hardening can be performed through
a targeted additive update

whether deterministic inventory/lineage regeneration
preserves all pre-existing entity checksums

whether Stage 13 artifact discovery is dynamic or static

whether the three genotype processed artifacts will be included
automatically through run-state registration

whether Stage 13 code requires an additive genotype registration patch

whether Stage 13 summary/report output should record:
    genotype projection status
    genotype artifact completeness
    genotype projection warning count

without treating genotype summaries as scientific evidence authority

the current canonical VAP variant_id construction logic

whether a reusable helper already exists

whether genotype projection can call the same helper

how symbolic alleles and normalized biallelic records
are represented in existing variant observations
```

## Gate

No code changes begin until the implementation path for:

```text
projection

state registration

TEP transport

validation
```

is explicitly mapped.

If existing TEP `--overwrite` behavior rewrites or replaces pre-existing
transported scientific entities, that mode shall not be used for the
canonical genotype backfill.

Before Phase 5 or Phase 8 proceeds, implementation shall provide either:

```text
a targeted additive genotype-entity update path

or

proof that deterministic TEP regeneration leaves all pre-existing
scientific entity bytes and checksums unchanged
```

---

# Phase 1 — Test Fixtures and Validation Skeleton

## Objective

Create the lightweight pytest foundation before implementing projection logic.

## Add representative VCF fixtures

Fixtures should cover:

```text
biallelic heterozygous call

homozygous reference call

homozygous alternate call

complete no-call

partial no-call

single-allele GT

multiallelic GT 1/2

unknown FORMAT keys

unknown FORMAT values containing reserved delimiters
requiring percent encoding

literal VCF missing values

FORMAT/sample length mismatch

duplicate byte-identical records at different ordinals

equivalent logical VCF content represented as both
plain .vcf and compressed .vcf.gz

direct variant relationship

complex multiallelic relationship
```

## Add test modules

Recommended layout:

```text
tests/test_genotype_projection.py

tests/test_genotype_projection_schema.py

tests/test_genotype_projection_summary.py

tests/test_genotype_projection_header_context.py

tests/test_genotype_tep_packaging.py

tests/test_genotype_non_interference.py
```

## Required Edge-Case Tests

The initial genotype test suite shall include:

```text
test_plain_and_gzipped_vcf_produce_equivalent_logical_record_hashes

test_unknown_format_reserved_characters_are_percent_encoded
```

The compressed/plain VCF equivalence test belongs primarily in:

```text
tests/test_genotype_projection.py
tests/test_genotype_projection_schema.py
```

## Initial expected state

The tests may initially fail because implementation is absent.

The fixture and assertion structure should still be reviewable before projection code is introduced.

## Gate

Proceed when:

```text
fixtures load deterministically

expected schema constants are represented once

test paths use temporary directories

tests do not require MARK

tests do not require full pipeline execution
```

---

# Phase 2 — Canonical Genotype Projection Module

## Objective

Implement one reusable source-faithful projection module.

## Recommended location

```text
pipeline/genotype_projection.py
```

## Core responsibilities

The module shall:

```text
read annotated VCF headers

resolve one selected sample

preserve raw FORMAT and sample fields

parse recognized GT/AD/DP/GQ/PL/FT values

preserve unknown FORMAT fields

derive schema-governed structural fields

preserve source-record order

compute source and identity hashes

emit genotype_observations.tsv

emit genotype_projection_summary.json

emit genotype_source_header_context.json

support decompressed logical reading of .vcf and .vcf.gz

calculate source-record hashes over decompressed logical data lines

preserve exact source artifact SHA-256 separately

reuse the canonical VAP variant_id constructor
for direct variant relationships

do not implement a second coordinate/allele
identifier serialization policy
```

## Required public behavior

The module should expose one canonical callable used by:

```text
future pipeline execution

canonical-run backfill

unit tests
```

The exact function name may be finalized during implementation.

## Required implementation properties

```text
deterministic

streaming or memory-conscious

single-parser architecture

no source mutation

no variant TSV mutation

explicit overwrite behavior

structured return metadata

clear failure reporting

transactional three-artifact publication

temporary-file construction

atomic canonical-path replacement where supported

cleanup of incomplete temporary artifacts

no partial genotype-enabled artifact state
```

## Performance posture

The implementation should avoid loading entire production VCFs into memory.

Preferred processing model:

```text
header pass

streamed record projection

atomic artifact finalization

summary finalization
```

### Wave 2.1 — Policy Alignment Hardening

Before projection integration proceeds, implementation shall be aligned with
the certified repository ecosystem multiallelic relationship policy.

Required hardening includes:

```text
relationship_resolution_target

projection_advisory_codes

governed multiallelic relationship deferral

symbolic ALT handling

spanning deletion handling

called allele index validation

malformed GT relationship classification

missing/no-call/partial-no-call distinction

optional FORMAT availability accounting

policy-aligned projection status semantics
```

This wave shall preserve source-record fidelity and shall not implement
downstream VDB relationship brokerage or RDGP reasoning.

## Gate

Proceed when:

```text
all projection tests pass

policy-alignment tests pass

schema tests pass

summary tests pass

header-context tests pass

local non-interference tests pass

plain-versus-gzipped logical record hash equivalence passes

reserved-character percent encoding passes

multiallelic relationship advisories conform to certified policy
```

---

# Phase 3 — Processed Artifact Registration

## Objective

Register genotype artifacts as normal VAP run outputs without introducing a numbered pipeline stage.

## Register artifacts

Recommended state entries:

```text
state["artifacts"]["genotype_observations"]

state["artifacts"]["genotype_projection_summary"]

state["artifacts"]["genotype_source_header_context"]
```

Recommended QC entry:

```text
state["qc"]["genotype_projection_qc"]
```

Recommended execution entry:

```text
state["stage_outputs"]["genotype_observation_projection"]
```

Equivalent locations may be used if they preserve current VAP state conventions.

## Constraints

The projection shall remain:

```text
non-numbered

observation-domain

parallel to the Stage 07 variant projection

not a Stage 08 dependency
```

## Gate

Proceed when:

```text
state registration is additive

existing state consumers remain compatible

existing tests continue to pass
```

---

# Phase 4 — Future Pipeline Orchestration

## Objective

Invoke genotype projection automatically for future eligible VAP executions.

## Integration point

Invoke the genotype projection after:

```text
Stage 07 annotated VCF creation and validation
```

and before final run completion.

Stage 08 may execute after genotype projection operationally, but it shall not consume genotype output.

## Two-Hook Future Execution Model

Future genotype-enabled VAP execution shall use two distinct orchestration
hooks.

### Observation Projection Hook

After Stage 07 annotated VCF creation and validation:

```text
invoke the canonical genotype projection

emit the complete three-artifact processed genotype set

register genotype projection status in run state
```

### TEP-VAP Construction Hook

After Stage 13 and all required run artifacts are complete:

```text
invoke the canonical TEP-VAP entity builder

build or refresh the run's TEP-VAP

transport the complete three-artifact genotype set

build genotype-aware inventory and lineage metadata

run TEP-VAP validation
```

Updating the TEP builder without invoking it during future VAP execution
is not sufficient.

A future eligible VAP execution is genotype-complete only when:

```text
the processed genotype artifact set is complete

and

the run's TEP-VAP contains the byte-identical genotype artifact set
```

## Orchestration responsibilities

The orchestrator shall pass:

```text
annotated VCF path

sample_id

run_id

reference_build

source_pipeline

sample alias where available

SRA accession where available

assay type where available

output directory

ensure future Stage 13 run context registers the three genotype artifacts

ensure Stage 13 remains authoritative only for execution and artifact context

do not make Stage 13 the scientific authority for genotype evidence
```

## Failure Posture

For a future genotype-enabled execution:

```text
projection-level fatal failure
    shall prevent the run from being declared
    genotype-complete or genotype-enabled

projection-level fatal failure
    shall not modify or semantically block
    the existing Stage 08–13 variant-centric pathway

record-level optional-field warnings
    shall not abort genotype projection
```

A run whose genotype projection fails may continue its established
variant-centric execution, but:

```text
the genotype projection status shall be failed

the canonical genotype artifact set shall not be published

the run shall not emit a conformant genotype-enabled TEP-VAP

the failure shall be recorded explicitly in run state
```

This preserves non-interference while keeping genotype completeness enforceable.

## Gate

Proceed when a local integration fixture proves:

```text
automatic invocation

processed artifact emission

state registration

no Stage 08–13 input changes

automatic post-Stage-13 TEP-VAP construction

three genotype artifacts present in the completed run TEP-VAP

processed and TEP-VAP genotype checksums match
```

---

# Phase 5 — TEP-VAP Entity Transport

## Objective

Transport all three genotype artifacts into TEP-VAP as first-class evidence.

## Update

```text
scripts/tep/build_vap_tep_entities.py
```

## Required behavior

The builder shall:

```text
create entities/genotype/

copy all three processed artifacts byte-for-byte

compute checksums

register genotype entity semantics

register companion artifacts

preserve source paths and producer identities
```

## Required semantic roles

```text
entity_domain = genotype

entity_role = genotype_observation

source_stage = genotype_projection

source_artifact_role = caller_emitted_genotype_observations
```

## Constraints

The TEP builder shall not:

```text
reparse genotype evidence

rewrite genotype artifacts

infer variant relationships

alter existing variant entities
```

## Gate

Proceed when TEP packaging unit tests confirm:

```text
expected paths

artifact presence

byte identity

checksum parity

no unrelated artifact mutation
```

---

# Phase 6 — TEP Lineage and Validation Integration

## Objective

Extend TEP metadata so genotype evidence is fully discoverable and auditable.

## Update

```text
scripts/tep/build_vap_tep_lineage_manifest.py

scripts/tep/validate_vap_tep.py
```

## External Source Representation

The annotated VCF is the authoritative source of genotype observations
but is not required to be transported inside TEP-VAP.

Before emitting genotype lineage, implementation shall use the repository's
existing governed representation for non-transported source artifacts.

The lineage manifest shall preserve:

```text
source artifact identity

source VCF checksum

source VCF header hash

producer path provenance

relationship to the packaged genotype entity
```

without falsely representing the annotated VCF as a transported TEP entity.

## Required lineage

```text
annotated_variants.vcf
    → genotype_observations.tsv

annotated_variants.vcf header context
    → genotype_source_header_context.json

genotype_observations.tsv
    → genotype_projection_summary.json
```

## Prohibited lineage

```text
annotated_variants.tsv
    → genotype_observations.tsv
```

## Required validation

The TEP validator shall confirm:

```text
all three genotype artifacts exist

processed and packaged bytes match

checksums match

schema versions are declared

entity inventory registration exists

lineage relationships exist

genotype artifact set is complete
```

## Gate

Proceed when isolated TEP tests pass and the existing TEP test suite remains green.

---

# Phase 7 — Full Local Test Gate

## Objective

Prove local implementation correctness before production backfill.

## Execute

```bash
pytest
```

At minimum, confirm:

```text
all genotype tests pass

all pre-existing VAP tests pass

no fixture input mutation occurs

no variant-centric test behavior changes
```

## Gate

No canonical backfill script shall run on MARK until this phase passes.

Policy-conformance validation shall additionally confirm:

```text
multiallelic observations remain unsplit

symbolic ALT observations remain producer-preserved

spanning deletions remain producer-preserved

relationship advisories replace governed warnings

relationship resolution targets match certified policy

no VDB brokerage behavior has been introduced

no RDGP reasoning behavior has been introduced
```

---

# Phase 8 — Canonical Backfill Tooling

## Objective

Create one MARK-oriented wrapper that applies the canonical projection and TEP hardening logic to the 13 retained runs.

## Recommended location

```text
scripts/mark/backfill_canonical_genotype_observations.py
```

## Canonical corpus

```text
12 epilepsy WES runs

1 HG002 WGS run
```

## Wrapper responsibilities

```text
iterate canonical run manifest

locate annotated VCF

resolve sample context

confirm reference metadata

invoke canonical genotype projection module

emit processed genotype artifacts

invoke canonical TEP builders

invoke TEP validation

isolate per-run failures

write receipts outside results/
```

## Prohibited behavior

The wrapper shall not:

```text
implement a second parser

modify source VCFs

modify existing Stage 08–13 artifacts

rerun upstream pipeline stages

silently overwrite conflicting outputs
```

## Authorized Additive Mutation Boundary

The canonical backfill is an explicitly authorized additive hardening
operation over historical run directories.

It may create:

```text
processed/genotype_observations.tsv

processed/genotype_projection_summary.json

processed/genotype_source_header_context.json

entities/genotype/*

additive inventory, lineage, validation, and manifest updates
```

It shall not modify pre-existing scientific evidence artifacts.

Before each run is changed, the wrapper shall capture a pre-patch inventory
and checksums for all existing scientific artifacts.

After each run is changed, the wrapper shall confirm that all pre-existing
scientific artifact checksums remain unchanged.

## Canonical Run Manifest

The backfill wrapper shall use a governed 13-entry manifest.

Each entry shall include at least:

```text
SRA accession

run_id

depth category

VAP sample_id or TEP sample token

expected run directory

expected annotated VCF path or deterministic discovery rule

expected TEP-VAP directory
```

The manifest shall contain exactly:

```text
12 epilepsy WES runs

1 HG002 WGS run
```

The wrapper shall perform a corpus-wide preflight before mutating any run.

Preflight shall confirm for all 13 entries:

```text
run directory exists

annotated VCF exists

metadata/config_snapshot.yaml exists

sample identity can be resolved

reference_build can be resolved

TEP-VAP directory exists or has a deterministic creation path

no conflicting genotype artifact set already exists
```

If corpus-wide preflight fails:

```text
no run shall be modified
```

After preflight passes, execution may isolate later per-run projection or
packaging failures.

## Output location

Operational receipts shall be written under:

```text
/root/Desktop/
```

The final receipt directory shall be bundled as:

```text
.tgz
```

---

# Phase 9 — Single-Run Production Trial

## Objective

Validate production behavior on one canonical run before corpus-wide backfill.

## Recommended first target

Use one already certified WES run, preferably:

```text
ERR10619300
run_2026_05_27_172531
median WES
```

or HG002 if local operational considerations favor the WGS reference specimen.

## Verify

```text
processed artifact creation

projection summary counts

header-context completeness

TEP transport

inventory registration

lineage registration

TEP validation

non-interference checksums

receipt completeness
```

## Gate

Do not proceed to all 13 runs until the single-run trial passes.

---

# Phase 10 — Canonical 13-Run Backfill

## Objective

Surface genotype evidence and harden all canonical TEP-VAPs.

## Execution

Run the canonical backfill wrapper from the VAP repository root on MARK.

## Per-run success criteria

```text
source VCF resolved

sample identity resolved

three processed artifacts emitted

three TEP artifacts emitted

processed/TEP checksums match

inventory updated

lineage updated

validation passes

pre-existing scientific artifacts unchanged
```

## Corpus success criteria

```text
13/13 runs processed successfully

one projection version used

one schema version used

one identity version used

all receipts present

no variant-centric artifact mutation
```

---

# Phase 11 — Backfill Certification and VDB Handoff

## Objective

Produce the evidence package needed for VDB to trust genotype-enabled TEP-VAPs.

## Required handoff contents

```text
implementation summary

pytest results

canonical run manifest

per-run projection status

per-run artifact checksums

TEP validation status

non-interference results

known warnings

supported schema versions

consumer obligations
```

## VDB message

The handoff shall make clear:

```text
Genotype observations are now first-class VAP producer artifacts.

Producer identities are authoritative.

Direct relationships may be used where declared.

Complex relationships remain deferred to VDB policy.

Missing rows are not homozygous-reference evidence.

RDGP reasoning remains downstream.
```

---

# Rollback and Failure Containment

## Local implementation rollback

Because the change is additive, rollback consists of removing:

```text
new genotype module

new state registration

new tests

new TEP genotype handling
```

Existing variant-centric behavior should remain unchanged.

## Backfill failure containment

The backfill wrapper shall isolate failures per run.

One failed run shall not corrupt or invalidate already completed runs.

## Conflicting output behavior

If an existing genotype artifact differs from deterministic regeneration:

```text
stop that run

do not overwrite silently

record conflict

require operator review
```

---

# Required File Changes

Expected new files:

```text
pipeline/genotype_projection.py

tests/test_genotype_projection.py

tests/test_genotype_projection_schema.py

tests/test_genotype_projection_summary.py

tests/test_genotype_projection_header_context.py

tests/test_genotype_tep_packaging.py

tests/test_genotype_non_interference.py

scripts/mark/backfill_canonical_genotype_observations.py
```

Expected modified files may include:

```text
run_pipeline.py

src/pipeline_runner.py

scripts/tep/build_vap_tep_entities.py

scripts/tep/build_vap_tep_lineage_manifest.py

scripts/tep/validate_vap_tep.py
```

The final implementation shall minimize file churn and modify only the integration points required by the certified design.

---

# Acceptance Gates

Implementation is complete only when:

```text
Gate 1
    repository integration points are mapped

Gate 2
    lightweight genotype tests exist

Gate 3
    canonical projection module passes unit tests

Gate 4
    processed artifact registration passes

Gate 5
    automatic future emission passes

Gate 6
    TEP packaging and lineage tests pass

Gate 7
    full local pytest passes

Gate 8
    single-run production trial passes

Gate 9
    canonical 13-run backfill passes

Gate 10
    VDB handoff is complete
```

No phase shall bypass its preceding gate.

---

# Implementation Success Criteria

The implementation succeeds when:

```text
one canonical genotype parser exists

all three processed artifacts are emitted

all three TEP artifacts are transported byte-for-byte

future eligible VAP runs emit genotype automatically

all 13 canonical runs are backfilled additively

all genotype pytest suites pass

policy-alignment tests pass

governed multiallelic observations remain producer-preserved

relationship deferral remains explicit and VDB-directed

all existing VAP tests continue to pass

existing Stage 08–13 scientific artifacts remain unchanged

VDB can register genotype evidence without re-reading raw VAP internals

RDGP receives genotype evidence without producer-side inheritance overreach
```

---

# Final Implementation Doctrine

Implement once.

Reuse everywhere.

Preserve raw genotype evidence.

Keep genotype separate from the variant-centric stages.

Transport genotype as first-class TEP-VAP evidence.

Prove correctness with lightweight pytest before production backfill.

Do not mutate existing VAP scientific behavior.

VAP preserves.

TEP-VAP transports.

VDB relates.

RDGP reasons.
