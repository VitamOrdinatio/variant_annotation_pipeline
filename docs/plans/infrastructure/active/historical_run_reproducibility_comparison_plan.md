# Historical Run Reproducibility Comparison Plan

## 1. Objective

Implement:

```text
scripts/analysis/historical_run_reproducibility_comparison.py
```

to perform an asymmetric, version-aware comparison among:

* a complete current VAP execution;
* a historical lightweight VAP extraction;
* an optional certified case-study reference.

The implementation SHALL conform to:

```text
docs/contracts/system/validation/
historical_run_reproducibility_comparison_contract.md
```

The initial target comparison is:

```text
Current:
results/run_2026_07_14_114546/

Historical lightweight:
results/run_2026_05_27_172531/

Certified case study:
docs/case_studies/err10619300/
```

---

## 2. Implementation Principles

The script SHALL be:

* read-only with respect to input evidence;
* deterministic;
* asymmetric by design;
* explicit about limitations;
* conservative in scientific interpretation;
* compatible with incomplete historical extractions;
* suitable for large TSV artifacts;
* reusable for future VAP comparisons.

The script SHALL not infer that missing historical artifacts represent execution failure.

---

## 3. Command-Line Interface

The initial CLI SHALL support:

```bash
python scripts/analysis/historical_run_reproducibility_comparison.py \
  --current-run results/run_2026_07_14_114546 \
  --historical-run results/run_2026_05_27_172531 \
  --case-study docs/case_studies/err10619300 \
  --output-dir results/comparisons/err10619300_sys76_vs_mark
```

Required arguments:

```text
--current-run
--historical-run
--output-dir
```

Optional arguments:

```text
--case-study
--comparison-id
--float-absolute-tolerance
--float-relative-tolerance
--overwrite
--strict
```

The script SHALL exit nonzero for invalid required inputs or failed output generation.

Scientific differences SHALL not by themselves produce a process failure unless `--strict` explicitly requests that behavior.

---

## 4. Phase 1: Input Discovery

### 4.1 Validate Input Roots

Confirm that:

* the current run directory exists;
* the historical run directory exists;
* the optional case-study directory exists when provided;
* the output directory does not already contain conflicting results unless `--overwrite` is used.

### 4.2 Record Input Identity

For each evidence source, collect available identity from:

```text
metadata/run_metadata.json
metadata.json
metadata/run_fingerprint.json
metadata/config_snapshot.yaml
processed/stage_13_final_summary.json
tep/*/entity_inventory.json
tep/*/validation_report.md
```

Missing identity artifacts in the historical extraction SHALL be recorded but SHALL not fail discovery.

### 4.3 Build Artifact Inventories

Recursively inventory the current and historical run directories.

Record:

```text
source
relative_path
filename
suffix
size_bytes
sha256_status
sha256
artifact_class
```

Hash small and medium artifacts directly.

For very large artifacts, hashing MAY be configurable or deferred unless required for a selected comparison.

---

## 5. Phase 2: Availability Mapping

Create:

```text
shared_artifact_inventory.tsv
historical_availability_report.tsv
```

### 5.1 Shared Artifacts

Identify comparable artifacts by normalized semantic role rather than only literal relative path.

Examples:

```text
current:
processed/stage_08_summary.json

historical:
processed/stage_08_summary.json
```

or:

```text
historical:
metadata/stage_summaries/stage_08_summary.json
```

The implementation SHALL support an ordered search policy for historical stage summaries:

1. `processed/stage_NN_summary.json`;
2. `metadata/stage_summaries/stage_NN_summary.json`.

The selected historical source SHALL be recorded.

### 5.2 Historical Gaps

Current-only artifacts SHALL be recorded with classifications such as:

```text
HISTORICAL_ARTIFACT_UNAVAILABLE
EXPECTED_ARCHITECTURE_EVOLUTION
```

Expected current-only categories include:

* execution provenance;
* genotype entity artifacts;
* metadata entity transport;
* native fresh TEP-VAP artifacts;
* current lineage branches;
* current acceptance-criteria evidence.

---

## 6. Phase 3: Stage-Summary Comparison

### 6.1 Summary Discovery

Attempt comparison for:

```text
stage_01_summary.json
stage_02_summary.json
stage_03_summary.json
stage_04_summary.json
stage_05_summary.json
stage_06_summary.json
stage_07_summary.json
stage_08_summary.json
stage_09_summary.json
stage_10_summary.json
stage_11_summary.json
stage_12_summary.json
stage_13_final_summary.json
```

The implementation SHALL compare every stage for which both sides provide a valid JSON summary.

### 6.2 Flatten JSON

Implement a deterministic JSON flattener using dotted field paths:

```text
partition_counts.coding_candidates
counts_by_priority_tier.tier_1_high_confidence_candidate
```

Lists SHALL be serialized conservatively or excluded unless a stable comparison policy exists.

### 6.3 Field Classification

Classify fields before comparison.

#### Stable scientific fields

Examples:

```text
counts
rows
variants
clinical status
frequency status
severity
consequence
priority tier
validation state
gene counts
malformed counts
```

#### Run-identity fields

Examples:

```text
run_id
sample-specific output paths
timestamps
tep_id
package_root
```

#### Architecture-evolution fields

Examples:

```text
execution_provenance
genotype_projection
new entity roles
new schema fields
```

#### Operational fields

Examples:

```text
status
input file
output file
```

Operational paths SHALL be normalized or classified as run-identity differences.

### 6.4 Numeric Comparison

For comparable numeric fields, emit:

```text
historical_value
current_value
absolute_delta
relative_delta
classification
```

Exact integer counts SHALL be compared exactly.

Floating-point values SHALL use configurable tolerances.

### 6.5 Required Output

Emit:

```text
stage_summary_comparison.tsv
```

with columns:

```text
stage
historical_source_path
current_source_path
field_path
field_class
historical_value
current_value
absolute_delta
relative_delta
classification
notes
```

---

## 7. Phase 4: Shared Tabular Comparison

### 7.1 Initial Candidate Tables

Discover shared tables among:

```text
stage_08_vdb_ready_variants.tsv
stage_08_selected_transcript_consequences.tsv
stage_09_coding_interpreted.tsv
stage_10_noncoding_interpreted.tsv
stage_11_prioritized_variants.tsv
stage_12_validation_candidates.tsv
```

The initial historical extraction is expected to retain only a subset.

Unavailable tables SHALL be reported without failure.

### 7.2 Header Comparison

For every shared table, emit:

```text
historical_columns
current_columns
shared_columns
historical_only_columns
current_only_columns
```

Current-only columns MAY be classified as architecture evolution.

### 7.3 Stable-Key Selection

Inspect candidate identity columns in this order:

```text
variant_id
chromosome + position + reference + alternate
chrom + pos + ref + alt
```

The script SHALL verify:

* required columns exist on both sides;
* keys are non-null;
* keys are unique or duplicate conditions are reported.

If no defensible stable key exists, perform distribution-level comparison only.

### 7.4 Large-Table Strategy

The script SHALL avoid loading multi-gigabyte tables fully into memory.

Preferred approaches:

* streaming row iteration;
* chunked reading;
* disk-backed key inventories;
* standard-library CSV processing where sufficient;
* optional SQLite-backed comparison for large keyed tables.

The initial implementation MAY limit detailed row-level comparison to historical tables actually retained locally.

### 7.5 Required Outputs

Emit as applicable:

```text
tabular_schema_comparison.tsv
tabular_distribution_comparison.tsv
unmatched_variant_keys.tsv
```

---

## 8. Phase 5: Certified Case-Study Comparison

### 8.1 Case-Study Inventory

Inventory:

```text
tables/
figures/*_source.tsv
manifests/
```

The script SHALL identify recognized certified tables by filename.

### 8.2 Current Equivalent Discovery

Map certified surfaces to current run artifacts or derivable summaries.

Initial targets include:

```text
stage_funnel_summary.tsv
priority_tier_summary.tsv
interpretation_label_summary.tsv
clinical_status_summary.tsv
candidate_reviewability_readiness.tsv
variant_consequence_summary.tsv
coding_noncoding_consequence_summary.tsv
runtime_stage_summary.tsv
gene_burden_summary.tsv
gene_list_overlay_intersections.tsv
```

### 8.3 Derivation Policy

When the current run does not already contain an equivalent table, the script MAY derive it only when:

* the derivation is deterministic;
* the source artifacts are available;
* the derivation logic is explicit;
* the output records its source artifacts.

The comparison script SHALL not silently invent an approximation to a certified surface.

### 8.4 Presentation Normalization

Before comparison, normalize:

* row order when semantically irrelevant;
* run IDs;
* timestamps;
* path prefixes;
* formatting-only numeric differences;
* display labels where a stable mapping exists.

### 8.5 Required Output

Emit:

```text
semantic_surface_comparison.tsv
```

with columns:

```text
surface
historical_source
current_source
metric
historical_value
current_value
delta
classification
notes
```

---

## 9. Phase 6: Current-Only Capability Validation

Inspect the current run for:

```text
metadata/execution_provenance.json
processed/genotype_observations.tsv
processed/genotype_projection_summary.json
processed/genotype_source_header_context.json
tep/*/entities/genotype/
tep/*/entities/context/execution_provenance.json
tep/*/entities/metadata/config_snapshot.yaml
tep/*/entity_inventory.json
tep/*/lineage_manifest.json
tep/*/validation_report.md
```

Record:

* existence;
* size;
* declared status;
* internal row-count reconciliation;
* validation status;
* relevant lineage presence.

Emit:

```text
current_only_capability_validation.tsv
```

These results SHALL use:

```text
CURRENT_ONLY_VALIDATION_PASS
CURRENT_ONLY_VALIDATION_FAIL
HISTORICAL_ARTIFACT_UNAVAILABLE
```

and SHALL not be included as historical mismatches.

---

## 10. Phase 7: Interpretation Engine

The implementation SHALL assign comparison classifications using ordered rules.

Recommended precedence:

1. invalid or unreadable evidence;
2. historical artifact unavailable;
3. not comparable;
4. run-identity difference;
5. expected architecture evolution;
6. exact match;
7. tolerated floating-point match;
8. different;
9. under review.

The system SHALL preserve the distinction between:

```text
DIFFERENT
```

and:

```text
UNDER_REVIEW
```

A difference SHALL remain `UNDER_REVIEW` when available evidence cannot attribute it confidently.

The current ERR10619300 `+40` Stage 8–12 row difference SHALL initially be emitted as:

```text
UNDER_REVIEW
```

with notes recording:

```text
coding candidates: +12
noncoding candidates: +28
splice-region candidates: 0
total: +40
```

---

## 11. Phase 8: Report Generation

Generate:

```text
comparison_report.md
```

Recommended sections:

1. Comparison identity
2. Executive result
3. Evidence sources
4. Historical evidence limitations
5. Current execution validation
6. Stage-summary comparison
7. Shared tabular comparison
8. Certified semantic-surface comparison
9. Current-only capability validation
10. Observed differences
11. Expected architecture evolution
12. Unresolved questions
13. Bounded conclusion
14. Output artifact inventory

The report SHALL avoid an unsupported binary conclusion.

It SHALL state separately:

```text
operational execution
TEP validity
historical coverage
stage-summary reproducibility
semantic reproducibility
row-level reproducibility
current-only capability status
cross-hardware determinism status
```

---

## 12. Phase 9: Comparison Manifest and Receipt

Generate:

```text
comparison_manifest.json
```

Include:

* comparison ID;
* generated timestamp;
* script path;
* script version;
* current input root;
* historical input root;
* case-study root;
* discovered run identities;
* comparison policies;
* tolerance settings;
* output files;
* warnings;
* limitations;
* overall bounded result.

Optionally generate:

```text
comparison_receipt.json
```

containing hashes for comparison outputs.

---

## 13. Testing Strategy

Create focused tests under:

```text
tests/analysis/
```

Recommended files:

```text
test_historical_run_reproducibility_comparison.py
test_historical_run_reproducibility_comparison_stage_summaries.py
test_historical_run_reproducibility_comparison_tables.py
```

Required test cases:

1. asymmetric artifact availability;
2. missing historical artifact is not a mismatch;
3. flattened JSON comparison;
4. exact numeric match;
5. integer difference;
6. float tolerance;
7. run-ID normalization;
8. expected architecture-evolution field;
9. historical summary fallback from `processed/` to `metadata/stage_summaries/`;
10. shared-column table comparison;
11. current-only column handling;
12. non-unique stable-key detection;
13. deterministic output ordering;
14. malformed JSON failure;
15. current-only capability validation;
16. `+40` structured difference fixture;
17. report generation;
18. manifest generation.

---

## 14. Implementation Waves

### Wave 1: Scaffold and Discovery

Implement:

* CLI;
* path validation;
* artifact inventories;
* comparison manifest scaffold;
* output directory handling.

### Wave 2: Stage-Summary Comparison

Implement:

* summary discovery;
* JSON flattening;
* field classification;
* numeric comparison;
* `stage_summary_comparison.tsv`.

### Wave 3: Historical Availability Reporting

Implement:

* asymmetric availability mapping;
* historical gaps;
* architecture-evolution classifications;
* `historical_availability_report.tsv`.

### Wave 4: Shared Tabular Comparison

Implement:

* TSV header inspection;
* shared-column detection;
* row counts;
* stable-key discovery;
* small/medium table comparison.

### Wave 5: Certified Case-Study Comparison

Implement:

* case-study table inventory;
* known surface mapping;
* presentation normalization;
* `semantic_surface_comparison.tsv`.

### Wave 6: Current-Only Capability Validation

Implement:

* execution provenance checks;
* genotype artifact checks;
* TEP validation evidence;
* current-only capability report.

### Wave 7: Markdown Report

Implement:

* bounded overall interpretation;
* evidence limitations;
* reproducibility sections;
* unresolved-difference reporting.

### Wave 8: Hardening

Implement:

* deterministic ordering;
* large-file safeguards;
* hashes and comparison receipt;
* failure handling;
* complete test suite.

---

## 15. Initial Execution Command

Once implemented:

```bash
python scripts/analysis/historical_run_reproducibility_comparison.py \
  --current-run results/run_2026_07_14_114546 \
  --historical-run results/run_2026_05_27_172531 \
  --case-study docs/case_studies/err10619300 \
  --output-dir \
  results/comparisons/err10619300_run_2026_07_14_114546_vs_historical
```

---

## 16. Completion Criteria

The plan is complete when:

1. all required outputs are emitted;
2. absent historical files are classified rather than failed;
3. stage summaries are compared deterministically;
4. available shared tables are compared conservatively;
5. certified case-study surfaces are compared where derivable;
6. current-only capabilities are validated independently;
7. the `+40` discrepancy is localized and classified without unsupported attribution;
8. the report clearly separates operational validity from scientific reproducibility;
9. repeated execution against unchanged inputs yields identical normalized outputs;
10. the implementation passes its focused and full regression suites.
