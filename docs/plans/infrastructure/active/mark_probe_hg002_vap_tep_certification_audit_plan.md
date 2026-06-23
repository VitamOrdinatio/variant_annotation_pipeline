# MARK Probe Plan: HG002 VAP-TEP Certification Audit

## Purpose

Run a read-only certification probe against:

```text
results/run_2026_06_03_010030/processed/
```

and:

```text
results/run_2026_06_03_010030/tep/vap_tep_HG002_run_2026_06_03_010030_v1/
```

to determine whether the HG002 VAP-TEP faithfully transports the preservation-critical VAP evidence lifecycle.

The probe must not mutate:

```text
results/
```

All audit outputs must be written to:

```text
/root/Desktop/
```

---

# Operating Rules

```text
Run from VAP repo root.

Read only from results/.

Write only to /root/Desktop/.

Do not rebuild the TEP.

Do not modify processed outputs.

Do not modify TEP contents.

Do not infer certification from expectations.

Measure actual artifacts.
```

---

# Recommended Output Directory

Create a timestamped audit directory:

```text
/root/Desktop/hg002_vap_tep_certification_audit_<timestamp>/
```

Example:

```text
/root/Desktop/hg002_vap_tep_certification_audit_2026_06_23_001500/
```

---

# Probe Script Name

Recommended script filename:

```text
probe_hg002_vap_tep_certification.py
```

Run from repo root:

```bash
python probe_hg002_vap_tep_certification.py
```

---

# Source Paths

## Processed Truth Directory

```text
results/run_2026_06_03_010030/processed
```

## TEP Directory

```text
results/run_2026_06_03_010030/tep/vap_tep_HG002_run_2026_06_03_010030_v1
```

---

# Artifact Pair Map

The probe should compare each transported TEP entity against its source truth artifact.

```text
processed/HG002_run_2026_06_03_010030.annotated_variants.tsv
↔
tep/entities/observation/HG002_run_2026_06_03_010030.annotated_variants.tsv

processed/stage_08_selected_transcript_consequences.tsv
↔
tep/entities/normalization/stage_08_selected_transcript_consequences.tsv

processed/stage_08_vdb_ready_variants.tsv
↔
tep/entities/normalization/stage_08_vdb_ready_variants.tsv

processed/coding_candidates.tsv
↔
tep/entities/routing/coding_candidates.tsv

processed/splice_region_candidates.tsv
↔
tep/entities/routing/splice_region_candidates.tsv

processed/noncoding_candidates.tsv
↔
tep/entities/routing/noncoding_candidates.tsv

processed/stage_09_coding_interpreted.tsv
↔
tep/entities/coding_interpretation/stage_09_coding_interpreted.tsv

processed/stage_10_noncoding_interpreted.tsv
↔
tep/entities/noncoding_interpretation/stage_10_noncoding_interpreted.tsv

processed/stage_11_prioritized_variants.tsv
↔
tep/entities/prioritization/stage_11_prioritized_variants.tsv

processed/stage_12_validation_candidates.tsv
↔
tep/entities/validation/stage_12_validation_candidates.tsv

processed/stage_13_artifact_manifest.json
↔
tep/entities/context/stage_13_artifact_manifest.json

processed/stage_13_final_summary.json
↔
tep/entities/context/stage_13_final_summary.json

processed/stage_13_run_report.md
↔
tep/entities/context/stage_13_run_report.md
```

---

# Required Audit Outputs

The probe should emit:

```text
tep_hg002_certification_summary.md

tep_hg002_entity_row_count_audit.tsv

tep_hg002_variant_id_parity_audit.tsv

tep_hg002_stage08_routing_overlap_audit.tsv

tep_hg002_required_column_audit.tsv

tep_hg002_candidate_collapse_audit.tsv

tep_hg002_lineage_integrity_audit.tsv

tep_hg002_stage13_context_audit.tsv

tep_hg002_scientific_summary.json
```

Optional but valuable:

```text
tep_hg002_random_variant_trace_examples.tsv

tep_hg002_edge_case_variant_trace_examples.tsv
```

---

# Probe 1: Transport Fidelity

For every source↔TEP artifact pair, measure:

```text
source_exists

tep_exists

source_size_bytes

tep_size_bytes

source_sha256

tep_sha256

sha256_match

source_row_count

tep_row_count

row_count_match

source_column_count

tep_column_count

column_count_match
```

Output:

```text
tep_hg002_entity_row_count_audit.tsv
```

Expected result:

```text
All transported artifacts match their processed/ source artifact.
```

---

# Probe 2: Stage07 Observation Anchor

Measure for TEP Stage07 observation TSV:

```text
row_count

variant_id_count

required columns present
```

Required columns:

```text
sample_id

run_id

variant_id
```

Also check for genomic coordinate and allele fields.

Acceptable coordinate/allele column names should be discovered from actual header and reported.

Output:

```text
tep_hg002_required_column_audit.tsv
```

Expected:

```text
row_count = 4,636,584

variant_id_count = 4,636,584

sample_id present

run_id present

variant_id present
```

---

# Probe 3: Stage07 → Stage08 Variant Parity

Compare variant_id sets:

```text
Stage07 observation
↔
Stage08 selected_transcript_consequences

Stage07 observation
↔
Stage08 vdb_ready_variants
```

Measure:

```text
left_variant_id_count

right_variant_id_count

intersection_count

left_only_count

right_only_count

sets_equal
```

Output:

```text
tep_hg002_variant_id_parity_audit.tsv
```

Expected:

```text
Stage07 variant_id set
=
Stage08 selected_transcript_consequences variant_id set

Stage07 variant_id set
=
Stage08 vdb_ready_variants variant_id set
```

---

# Probe 4: Stage08 Dual Artifact Semantics

Compare:

```text
stage_08_selected_transcript_consequences.tsv

stage_08_vdb_ready_variants.tsv
```

Measure:

```text
row_count_match

column_count_match

variant_id_set_match

sha256_match
```

Record statement:

```text
Physical equivalence in VAP v1 does not imply semantic equivalence forever.
```

Output can be included in:

```text
tep_hg002_variant_id_parity_audit.tsv
```

and summarized in:

```text
tep_hg002_certification_summary.md
```

---

# Probe 5: Stage08 Routing Overlap

Load variant_id sets from:

```text
coding_candidates.tsv

splice_region_candidates.tsv

noncoding_candidates.tsv
```

Measure:

```text
coding_count

splice_count

noncoding_count

coding_intersect_splice

coding_intersect_noncoding

splice_intersect_noncoding

coding_only

splice_only

noncoding_only
```

Output:

```text
tep_hg002_stage08_routing_overlap_audit.tsv
```

Expected model:

```text
Coding Partition

Noncoding Partition

Splice Overlay
```

Expected counts:

```text
coding variant_id_count = 24,278

splice variant_id_count = 3,733

noncoding variant_id_count = 4,609,098

coding ∩ splice > 0

coding ∩ noncoding = 0

splice ∩ noncoding = 0
```

---

# Probe 6: Stage09/10 Interpretation Preservation

For Stage09 and Stage10 transported TSVs, confirm required fields.

Stage09 expected:

```text
stage_09_coding_interpreted.tsv row_count = 27,486
```

Required coding interpretation fields:

```text
functional_impact

coding_interpretation_label

clinical_evidence

rarity_flag

qc_reliability
```

Stage10 expected:

```text
stage_10_noncoding_interpreted.tsv row_count = 4,609,098
```

Required noncoding interpretation fields:

```text
noncoding_functional_context

noncoding_interpretation_label

clinical_evidence

rarity_flag

qc_reliability
```

Output:

```text
tep_hg002_required_column_audit.tsv
```

---

# Probe 7: Stage11 Prioritization Preservation

Measure:

```text
row_count

variant_id_count

required columns present

priority_tier distribution
```

Required columns:

```text
priority_tier

priority_rank

priority_reason

source_interpretation_label

variant_origin
```

Expected:

```text
row_count = 4,636,584

variant_id_count = 4,636,584
```

Expected priority distribution:

```text
high priority = 0

moderate priority = 113,363

low/common = 3,369,755

uninterpretable/qc-limited = 1,153,466
```

Output:

```text
tep_hg002_candidate_collapse_audit.tsv
```

---

# Probe 8: Stage12 Validation Preservation

Measure:

```text
row_count

variant_id_count

required columns present

validation_required distribution
```

Required columns:

```text
validation_required

validation_priority

suggested_validation_method

validation_reason
```

Expected:

```text
row_count = 4,636,584

variant_id_count = 4,636,584

validation_required = True: 113,363

validation_required = False: 4,523,221
```

Output:

```text
tep_hg002_candidate_collapse_audit.tsv
```

---

# Probe 9: Candidate-Collapse Audit

Determine whether the TEP includes all preservation-critical layers:

```text
Stage07 observation

Stage08 normalization

Stage08 routing

Stage09 coding interpretation

Stage10 noncoding interpretation

Stage11 prioritization

Stage12 validation

Stage13 context
```

Measure:

```text
entity_present

row_count

variant_id_count

full_universe_preserved
```

Certification condition:

```text
Stage11 row_count = Stage07 row_count

Stage12 row_count = Stage07 row_count

validation_required False records exist

non-prioritized or low-priority records exist
```

Output:

```text
tep_hg002_candidate_collapse_audit.tsv
```

---

# Probe 10: Lineage Manifest Integrity

Audit:

```text
lineage_manifest.json
entity_inventory.json
validation_report.md
```

Measure:

```text
required entity roles present

source artifacts present

source artifact checksums present

parent-child edges present

validation_summary.status

criteria_failed
```

Required roles:

```text
observation

normalization

routing

coding_interpretation

noncoding_interpretation

prioritization

validation

context
```

Output:

```text
tep_hg002_lineage_integrity_audit.tsv
```

---

# Probe 11: Stage13 Context Audit

Audit:

```text
stage_13_artifact_manifest.json

stage_13_final_summary.json

stage_13_run_report.md
```

Compare processed vs TEP checksums.

Also inspect whether Stage13 artifact manifest self-reports:

```text
stage_13_artifact_manifest exists=False
```

Record whether this appears to be:

```text
benign self-reference timing issue

or

provenance inconsistency requiring correction
```

Output:

```text
tep_hg002_stage13_context_audit.tsv
```

---

# Probe 12: Scientific Coherence Summary

Generate JSON summary:

```text
tep_hg002_scientific_summary.json
```

Include:

```text
sample_id

run_id

stage07_variant_count

stage08_variant_count

coding_count

splice_count

noncoding_count

stage09_count

stage10_count

stage11_count

stage12_count

priority_tier_distribution

validation_required_distribution

candidate_collapse_status

stage13_context_status

overall_probe_status
```

Expected scientific pattern:

```text
large WGS-scale variant universe

large noncoding majority

zero high-priority disease candidates

moderate reviewable IGV candidate set

large low/common background

large uninterpretable or QC-limited background
```

---

# Optional Probe 13: Trace Examples

Create:

```text
tep_hg002_random_variant_trace_examples.tsv

tep_hg002_edge_case_variant_trace_examples.tsv
```

Include at least one example of:

```text
coding variant

splice-overlap variant

noncoding variant

validation_required=True variant

validation_required=False variant

uninterpretable variant
```

For each trace, include:

```text
variant_id

present_stage07

present_stage08

present_routing

present_stage09_or_stage10

present_stage11

present_stage12

priority_tier

validation_required

variant_origin

source_interpretation_label
```

---

# Final Output Behavior

At completion, the script should print:

```text
Audit complete.

Outputs written to:
/root/Desktop/hg002_vap_tep_certification_audit_<timestamp>/
```

and list all emitted files.

---

# Certification Interpretation

DEX should not certify from the script alone.

The script produces measurements.

DEX then reviews the outputs and writes the certification interpretation for SAGE.

Expected final interpretation categories:

```text
PASS

PASS WITH CONDITIONS

FAIL
```

---

# Non-Mutation Guarantee

The script must enforce:

```text
No writes under results/.

No writes under processed/.

No writes under tep/.

All outputs under /root/Desktop/.
```
