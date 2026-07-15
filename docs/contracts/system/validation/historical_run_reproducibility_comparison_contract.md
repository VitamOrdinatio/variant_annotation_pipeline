# Historical Run Reproducibility Comparison Contract

## 1. Purpose

This contract governs comparison between a current VAP execution and one or more historical reference surfaces when the compared evidence packages are not structurally symmetric.

The contract exists to prevent incomplete historical extractions, architecture evolution, run-specific metadata, or absent legacy artifacts from being misclassified as scientific nondeterminism.

The comparison system SHALL distinguish among:

1. directly comparable scientific outputs;
2. expected differences caused by pipeline evolution;
3. run-identity and execution-environment differences;
4. unavailable historical evidence;
5. genuine unresolved scientific divergence.

The initial governed comparison is:

```text
Current execution:
results/run_2026_07_14_114546/

Historical lightweight reference:
results/run_2026_05_27_172531/

Certified case-study reference:
docs/case_studies/err10619300/
or an equivalent extracted certified case-study bundle
```

The current execution is a complete, execution-provenance-enabled, genotype-elevated VAP run with native TEP-VAP emission.

The historical local reference is a lightweight extraction of a full MARK execution and SHALL NOT be treated as a complete execution snapshot.

The certified case-study reference is a curated scientific and reporting surface derived from historical MARK executions and SHALL NOT be treated as a complete raw run directory.

---

## 2. Governing Principle

Historical and current VAP executions SHALL be compared according to the evidence that is actually available, not according to an assumed symmetric directory structure.

Missing historical artifacts SHALL NOT be treated as mismatches.

New current-run artifacts SHALL NOT be treated as historical divergence when those artifacts represent capabilities introduced after the historical execution.

Comparison conclusions SHALL be bounded by:

* artifact availability;
* pipeline-version comparability;
* configuration comparability;
* toolchain comparability;
* resource identity;
* schema evolution;
* evidence granularity.

The comparison system SHALL prefer explicit uncertainty over unsupported claims of determinism or nondeterminism.

---

## 3. Evidence Classes

### 3.1 Current Complete Execution

A current complete execution MAY contain:

* all pipeline stage outputs;
* interim and processed artifacts;
* stage summaries;
* runtime telemetry;
* execution provenance;
* genotype projection artifacts;
* figures and figure substrates;
* native TEP-VAP emission;
* TEP manifests and validation reports.

The initial current execution is:

```text
results/run_2026_07_14_114546/
```

### 3.2 Historical Lightweight Execution Reference

A historical lightweight reference contains only a selected subset of artifacts retained from a prior complete execution.

Its missing files represent extraction policy, not execution failure.

The initial historical lightweight reference is:

```text
results/run_2026_05_27_172531/
```

### 3.3 Certified Case-Study Reference

A certified case-study reference contains curated scientific summaries, figures, source tables, manifests, and narrative artifacts derived from one or more historical executions.

It is authoritative for the certified surfaces it contains, but it is not authoritative for raw artifacts that it does not preserve.

The initial certified case-study reference is:

```text
docs/case_studies/err10619300/
```

or an extracted equivalent of:

```text
err10619300_case_study.tgz
```

---

## 4. Comparison Layers

The comparison SHALL be performed in ordered layers.

### 4.1 Layer 1: Artifact Availability and Identity

The system SHALL inventory each evidence source before comparing scientific content.

For every expected or discovered artifact, the inventory SHALL record:

* evidence source;
* relative path;
* artifact type;
* existence;
* size;
* SHA256 when practical;
* comparison eligibility;
* unavailability reason when absent.

Artifacts absent from the historical lightweight reference SHALL be classified as:

```text
HISTORICAL_ARTIFACT_UNAVAILABLE
```

rather than:

```text
DIFFERENT
```

### 4.2 Layer 2: Stage-Summary Comparison

The system SHALL compare stage summaries available in both the current and historical execution references.

Initially expected comparable summaries include:

```text
stage_08_summary.json
stage_09_summary.json
stage_10_summary.json
stage_11_summary.json
stage_12_summary.json
stage_13_final_summary.json
```

The system SHALL compare stable scientific and operational summary fields, including where available:

* input row counts;
* output row counts;
* total variant counts;
* coding, noncoding, splice, and unknown partitions;
* clinical-status counts;
* consequence and severity counts;
* frequency-status counts;
* interpretation counts;
* priority-tier counts;
* validation-readiness counts;
* gene-count summaries;
* malformed or unassigned row counts.

The system SHALL exclude or separately classify volatile fields such as:

* run IDs;
* timestamps;
* absolute paths;
* output filenames containing run IDs;
* hostnames;
* machine identity;
* execution-provenance timestamps;
* TEP identifiers;
* package paths;
* artifact hashes whose contents include run-specific identity.

### 4.3 Layer 3: Shared Tabular Artifact Comparison

For tabular artifacts present in both execution references, the system SHALL compare only the shared semantic surface.

The comparison SHALL support:

* row-count comparison;
* column inventory comparison;
* shared-column comparison;
* stable-key comparison when a defensible stable key exists;
* categorical distribution comparison;
* numeric summary comparison.

The system SHALL NOT require identical headers when the current schema contains newly introduced columns.

Columns present only in the current artifact SHALL be classified as schema evolution unless contractually required for the historical schema.

Columns present only in the historical artifact SHALL be surfaced explicitly and SHALL NOT be silently discarded.

### 4.4 Layer 4: Certified Case-Study Surface Comparison

The system SHALL compare current-run-derived scientific summaries against certified case-study tables when equivalent derivation logic is available.

Candidate comparison surfaces include:

* stage funnel;
* coding and noncoding consequence summaries;
* priority tiers;
* interpretation labels;
* clinical-status summaries;
* candidate reviewability;
* validation readiness;
* gene burden;
* gene-list intersections;
* provenance summaries;
* runtime stage summaries;
* figure source substrates.

The system SHALL distinguish between:

```text
scientific value comparison
```

and:

```text
literal file identity comparison
```

Case-study tables containing historical run IDs, timestamps, or presentation-specific ordering SHALL be normalized before comparison.

### 4.5 Layer 5: Current-Only Capability Validation

Artifacts representing capabilities added after the historical execution SHALL be validated independently and SHALL NOT be treated as historical comparison targets.

These include:

* execution provenance;
* genotype observations;
* genotype projection summary;
* genotype source-header context;
* metadata entity transport;
* fresh native TEP-VAP emission;
* genotype lineage branch;
* execution-provenance lineage branch;
* current TEP acceptance criteria introduced after the historical run.

Current-only validation SHALL report whether each capability is internally coherent and contract-valid.

---

## 5. Comparison Classifications

Every comparison record SHALL use one of the following classifications.

### 5.1 `MATCH`

The compared values or normalized scientific surfaces are equivalent.

### 5.2 `DIFFERENT`

Comparable values differ and no approved normalization or architecture-evolution rule explains the difference.

### 5.3 `EXPECTED_ARCHITECTURE_EVOLUTION`

The difference is explained by an intentional, documented change in schema, pipeline behavior, metadata, genotype support, execution provenance, TEP emission, or another post-historical capability.

### 5.4 `RUN_IDENTITY_DIFFERENCE`

The difference is limited to run-specific identity such as:

* run ID;
* timestamp;
* path;
* hostname;
* package identifier;
* execution receipt identity.

### 5.5 `HISTORICAL_ARTIFACT_UNAVAILABLE`

The current artifact exists, but no corresponding artifact was retained in the historical lightweight extraction or certified case-study surface.

### 5.6 `NOT_COMPARABLE`

The two artifacts or fields do not represent the same semantic surface.

### 5.7 `UNDER_REVIEW`

The difference is real but cannot yet be attributed to pipeline evolution, execution substrate, toolchain, resources, or scientific divergence.

### 5.8 `CURRENT_ONLY_VALIDATION_PASS`

A current-only capability passed its own validation contract.

### 5.9 `CURRENT_ONLY_VALIDATION_FAIL`

A current-only capability failed its own validation contract.

---

## 6. Numeric Comparison Rules

Numeric fields SHALL be compared using explicit policies.

### 6.1 Exact Counts

Discrete counts SHALL use exact comparison unless an approved tolerance is declared.

Examples:

* row counts;
* variant counts;
* candidate counts;
* tier counts;
* validation counts.

### 6.2 Floating-Point Values

Floating-point values MAY use configurable absolute and relative tolerances.

The applied tolerance SHALL be recorded in the comparison output.

### 6.3 Derived Percentages

Percentages SHALL be recomputed from compared counts when possible.

A rounded displayed percentage SHALL NOT override an exact-count discrepancy.

### 6.4 Missing Values

The system SHALL distinguish among:

* field absent because of historical schema;
* field present with null value;
* field present with zero;
* field unavailable because the artifact is absent.

These states SHALL NOT be collapsed.

---

## 7. Tabular Comparison Rules

Tabular comparison SHALL:

1. detect the delimiter;
2. preserve column names;
3. report row and column counts;
4. determine shared and source-specific columns;
5. normalize line endings and missing-value representations;
6. avoid depending on row order unless row order is contractually meaningful;
7. use a stable composite key only when the key is scientifically justified;
8. report duplicate-key conditions;
9. preserve unmatched rows for later inspection;
10. avoid loading unnecessarily large tables fully into memory when streaming or chunked comparison is sufficient.

Potential stable variant keys MAY include normalized combinations of:

```text
chromosome
position
reference
alternate
```

or an existing canonical `variant_id`.

The system SHALL verify the uniqueness and availability of a proposed key before using it as an identity key.

---

## 8. Version and Configuration Awareness

The comparison SHALL record available evidence about:

* pipeline version;
* repository commit;
* run fingerprint;
* configuration snapshot;
* execution mode;
* tool versions;
* annotation software and cache release;
* reference assembly;
* reference-resource checksums;
* gene-set checksums.

A scientific difference SHALL NOT automatically be attributed to hardware when software, configuration, annotation cache, or resource identity differs.

Cross-hardware determinism MAY be claimed only when the relevant execution inputs and behavior-defining dependencies are shown to be equivalent.

---

## 9. Required Outputs

The comparison script SHALL emit a self-contained comparison directory containing at minimum:

```text
comparison_manifest.json
shared_artifact_inventory.tsv
historical_availability_report.tsv
stage_summary_comparison.tsv
semantic_surface_comparison.tsv
comparison_report.md
```

Optional outputs MAY include:

```text
tabular_schema_comparison.tsv
tabular_distribution_comparison.tsv
unmatched_variant_keys.tsv
current_only_capability_validation.tsv
runtime_comparison.tsv
comparison_receipt.json
```

### 9.1 `comparison_manifest.json`

The manifest SHALL identify:

* current execution;
* historical lightweight reference;
* certified case-study reference;
* comparison timestamp;
* script version;
* input paths;
* output paths;
* comparison policies;
* limitations.

### 9.2 `shared_artifact_inventory.tsv`

This table SHALL identify artifacts present in both execution references and their comparison eligibility.

### 9.3 `historical_availability_report.tsv`

This table SHALL identify current artifacts that lack historical equivalents and explain why they are not treated as mismatches.

### 9.4 `stage_summary_comparison.tsv`

This table SHALL contain at minimum:

```text
stage
field_path
historical_value
current_value
delta
classification
notes
```

### 9.5 `semantic_surface_comparison.tsv`

This table SHALL summarize high-value scientific surfaces and their comparison classifications.

### 9.6 `comparison_report.md`

The report SHALL provide:

* executive result;
* evidence sources;
* availability limitations;
* direct matches;
* differences;
* expected architecture evolution;
* current-only validation;
* unresolved questions;
* bounded conclusion.

---

## 10. Overall Result Semantics

The system SHALL NOT reduce the entire comparison to a binary pass or fail without qualification.

The report SHALL separately state:

```text
operational execution status
current TEP validation status
historical artifact coverage
stage-summary reproducibility
semantic-surface reproducibility
exact row-level reproducibility
current-only capability validation
cross-hardware determinism status
```

A recommended overall state vocabulary is:

```text
REPRODUCIBLE_WITHIN_AVAILABLE_SURFACES
REPRODUCIBLE_WITH_EXPECTED_ARCHITECTURE_EVOLUTION
PARTIALLY_REPRODUCIBLE
SCIENTIFIC_DIFFERENCE_UNDER_REVIEW
NOT_COMPARABLE_WITH_AVAILABLE_EVIDENCE
COMPARISON_FAILED
```

---

## 11. Initial ERR10619300 Interpretation Boundary

For the initial comparison, the following facts SHALL remain distinct:

1. The sys76 execution completed successfully.
2. The sys76 TEP-VAP passed current validation.
3. The historical local run is a lightweight extraction.
4. The certified case-study bundle contains curated summaries rather than a full raw execution snapshot.
5. The current run contains 736,508 Stage 8–12 rows.
6. The certified historical summaries report 736,468 corresponding rows.
7. The observed difference is structured as:

   * coding candidates: `+12`;
   * noncoding candidates: `+28`;
   * splice-region candidates: `0`;
   * total: `+40`.
8. The cause of the difference is not yet established.
9. The difference SHALL remain `UNDER_REVIEW` until the earliest divergence surface and relevant version differences are identified.

The comparison system SHALL not describe this difference as hardware nondeterminism without supporting evidence.

---

## 12. Failure Conditions

The comparison process SHALL fail closed when:

* the current execution path does not exist;
* no comparison evidence sources are available;
* JSON required for a selected comparison is malformed;
* a declared stable key is non-unique and no fallback policy exists;
* outputs cannot be written;
* input evidence is modified during comparison;
* normalization rules would discard scientifically meaningful differences.

Missing optional historical artifacts SHALL not cause comparison failure.

---

## 13. Non-Goals

This contract does not require:

* reconstruction of missing MARK artifacts;
* literal directory equality;
* equality of run IDs or timestamps;
* equality of execution-provenance receipts;
* equality of current and historical schemas;
* inference that hardware caused any observed difference;
* replacement of formal VAP or TEP validation;
* modification of historical artifacts.

---

## 14. Acceptance Criteria

The implementation satisfies this contract when it:

1. accepts asymmetric current, historical-lightweight, and certified-case-study inputs;
2. inventories evidence before comparison;
3. compares only defensible shared surfaces;
4. distinguishes missing evidence from differing evidence;
5. records architecture evolution explicitly;
6. validates current-only capabilities independently;
7. emits all required outputs;
8. preserves unresolved differences as `UNDER_REVIEW`;
9. reports limitations prominently;
10. produces deterministic comparison outputs for identical input evidence.
