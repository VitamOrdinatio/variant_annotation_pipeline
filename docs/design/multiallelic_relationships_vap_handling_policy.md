# Multiallelic Relationships: VAP Handling Policy

**Status:** SAGE-VDB / SAGE-VAP derived handling policy  
**Intended path:** `docs/design/multiallelic_relationships_vap_handling_policy.md`  
**Repository:** Variant Annotation Pipeline (VAP)  
**Parent Truth Layer:** `AI_Workspace/shared/repo_strategy/repo_ecosystem_multiallelic_relationships.md`  
**Target audience:** DEX-VAP  
**Downstream consumer:** VDB, then RDGP through TEP-VDB  

---

## 1. Purpose

This document defines how VAP should handle multiallelic genotype relationships when elevating genotype evidence into TEP-VAP.

The policy is producer-side only.

It tells VAP what to preserve, what to emit, what to label, and what not to infer.

It does **not** define VDB topology schemas, VDB brokerage implementation, or RDGP inheritance reasoning.

The ecosystem boundary is:

```text
VAP preserves source-record genotype evidence.
VDB brokers allele-specific relationships as derived topology.
RDGP reasons over registered relationships.
```

---

## 2. Executive Doctrine

VAP is a producer evidence transport system.

For multiallelic genotype records, VAP preserves the caller-emitted source-record-scoped genotype observation.

VAP does not split multiallelic genotype observations into synthetic allele-specific producer rows.

VAP emits direct variant relationships only when the source-record-to-variant relationship is unambiguous under declared VAP policy.

For multiallelic, symbolic, spanning-deletion, split-normalized, malformed, or otherwise complex cases, VAP preserves source truth and emits governed relationship status fields for downstream VDB brokerage.

Core doctrine:

```text
VAP preserves.
VDB brokers.
RDGP reasons.
```

---

## 3. Definition: Multiallelic Genotype Relationship

A multiallelic genotype relationship is the relationship between one source-record-scoped genotype observation and one or more allele-specific variant identities or variant observations when a single source variant record contains multiple alternate alleles and the genotype field references one or more of those allele indices.

Example:

```text
REF = A
ALT = C,G
GT  = 1/2
AD  = 2,4,9
```

In this record:

```text
allele index 0 = reference allele A
allele index 1 = alternate allele C
allele index 2 = alternate allele G
```

Therefore:

```text
GT = 1/2
```

means the one source-record genotype observation references both alternate allele index 1 and alternate allele index 2.

It does **not** mean VAP should emit two independent producer genotype rows.

Correct VAP interpretation:

```text
one source record
one genotype observation
multiple called allele indices
relationship brokerage deferred to VDB
```

---

## 4. VAP Responsibility Boundary

VAP owns source-faithful genotype preservation.

VAP may classify simple direct relationships.

VAP must not perform downstream identity brokerage or biological reasoning.

VAP responsibilities:

```text
parse readable source records
preserve raw genotype and FORMAT/sample evidence
preserve source-record identity
preserve alternate allele lists
preserve called allele indices
preserve depth and likelihood vectors where present
classify relationship status
emit deterministic summaries
emit enough context for VDB to broker relationships later
```

VAP non-responsibilities:

```text
constructing VDB topology edges
creating allele-specific synthetic genotype rows
constructing VDB allele-specific variant relationships
resolving complex normalization relationships
inferring compound heterozygosity
inferring inheritance mode
inferring de novo status
inferring disease causality
inferring diagnosis
```

---

## 5. What VAP Must Preserve

VAP must preserve enough source and genotype context for VDB to deterministically construct allele-specific relationships later when possible.

### 5.1 Source Identity

Recommended fields:

```text
source_vcf_path
source_vcf_sha256
source_vcf_header_hash
source_record_ordinal
source_record_hash
source_record_ref
source_record_alt
```

### 5.2 Sample and Run Identity

Recommended fields:

```text
sample_id
run_id
selected_sample_name
sample_selection_policy
reference_build
```

### 5.3 Coordinate and Allele Record Context

Recommended fields:

```text
chromosome
position
reference_allele
alternate_alleles_raw
alternate_allele_count
alternate_allele
is_multiallelic
called_allele_indices
```

For biallelic direct records, `alternate_allele` may represent the single alternate allele.

For multiallelic records, `alternate_alleles_raw` must preserve the complete source ALT list.

### 5.4 Raw Genotype and FORMAT Preservation

Recommended fields:

```text
format_raw
sample_format_raw
gt_raw
ad_raw
dp_raw
gq_raw
pl_raw
ft_raw
caller_specific_fields_retained_by_policy
```

Raw caller evidence remains authoritative.

Normalized labels are convenience projections and must not replace raw fields.

### 5.5 Normalized Descriptive State

Recommended fields:

```text
gt_arity
gt_separator
phase_state
genotype_label
zygosity_state
is_no_call
is_missing
partial_no_call_state
record_parse_status
variant_relationship_status
relationship_reason
relationship_resolution_target
projection_advisory_codes
projection_warning_codes
```

These fields help VDB and downstream consumers understand whether the genotype observation is directly linked, complex, unresolved, malformed-but-preserved, or intentionally delegated to downstream brokerage.

---

## 6. What VAP Must Not Do

VAP must not split a multiallelic source genotype observation into synthetic allele-specific producer rows.

For example, this source record:

```text
REF = A
ALT = C,G
GT  = 1/2
AD  = 2,4,9
```

must not become:

```text
synthetic row 1: A>C, GT=0/1 or allele-specific rewritten GT
synthetic row 2: A>G, GT=0/1 or allele-specific rewritten GT
```

That would distort the source-record-scoped genotype semantics.

VAP must not emit synthetic rows that imply the caller emitted independent genotype observations for each alternate allele.

VAP must also not infer:

```text
dominant-compatible
recessive-compatible
compound heterozygous
de novo
biallelic disease model satisfied
carrier status
hemizygous disease model
pathogenic genotype
diagnostic genotype
```

These are downstream reasoning concepts, not VAP producer-emission concepts.

---

## 7. Direct Convenience Linkage Policy

VAP may emit a direct convenience linkage only when the source relationship is unambiguous.

Typical direct case:

```text
REF = A
ALT = C
GT  = 0/1
```

VAP may emit:

```text
variant_relationship_status = direct
relationship_reason = biallelic_direct
variant_id = chromosome:position:reference:alternate
relationship_resolution_target = none
```

The purpose of direct linkage is convenience for simple biallelic records.

Direct linkage must not be used when multiple alternate alleles, symbolic alleles, spanning deletions, nontrivial normalization, malformed GT, or missing identity prevent safe direct relationship assignment.

---

## 8. Complex Source-Faithful Linkage Policy

For multiallelic records, VAP should emit one genotype observation and classify the relationship as complex or governed-deferred.

Example:

```text
REF = A
ALT = C,G
GT  = 1/2
```

VAP should emit:

```text
variant_relationship_status = complex
relationship_reason = multiallelic_source_record
relationship_resolution_target = vdb_brokerage
variant_id = NA
```

And preserve:

```text
alternate_alleles_raw = C,G
alternate_allele_count = 2
called_allele_indices = 1,2
gt_raw = 1/2
```

This is source-faithful preservation.

It is not evidence loss.

It is not a failed projection.

It is a governed handoff state indicating that allele-specific relationship construction belongs to VDB.

---

## 9. Canonical Example: `ALT=C,G`, `GT=1/2`, `AD=2,4,9`

Source record:

```text
REF = A
ALT = C,G
GT  = 1/2
AD  = 2,4,9
```

VAP should preserve:

```text
source_record_ref = A
source_record_alt = C,G
alternate_alleles_raw = C,G
alternate_allele_count = 2
gt_raw = 1/2
called_allele_indices = 1,2
ad_raw = 2,4,9
ref_depth = 2
alt_depths_raw = 4,9
```

VAP may also emit deterministic convenience fields such as:

```text
called_alt_depths_raw = 4,9
```

VAP must not emit:

```text
synthetic genotype row for A>C with AD=2,4
synthetic genotype row for A>G with AD=2,9
```

The allele-specific relationship is downstream VDB topology:

```text
genotype_observation
    -> allele index 1 / ALT C
    -> allele index 2 / ALT G
```

But those are VDB-derived relationships, not VAP-emitted producer genotype rows.

---

## 10. Relationship Status and Reason Fields

VAP should distinguish relationship state from relationship reason.

### 10.1 Recommended `variant_relationship_status` Values

```text
direct
complex
unresolved
not_applicable
```

Meaning:

```text
direct:
    VAP can safely provide a direct biallelic variant relationship.

complex:
    Source evidence is preserved, but allele-specific relationship construction
    is delegated to VDB.

unresolved:
    VAP cannot safely provide a direct relationship, and downstream brokerage may
    require special handling, missing prerequisites, or review.

not_applicable:
    No variant relationship is applicable for the row or context.
```

### 10.2 Recommended `relationship_reason` Values

```text
biallelic_direct
multiallelic_source_record
symbolic_alt
spanning_deletion
normalization_required_or_unavailable
malformed_gt
called_allele_index_out_of_range
variant_identity_unavailable
missing_gt
no_call
partial_no_call
format_sample_mismatch
```

### 10.3 Recommended `relationship_resolution_target` Values

```text
none
vdb_brokerage
not_resolvable_by_vap
not_evaluated
```

For a preserved multiallelic record:

```text
variant_relationship_status = complex
relationship_reason = multiallelic_source_record
relationship_resolution_target = vdb_brokerage
```

---

## 11. Warning / Advisory / Status Semantics

Multiallelic relationship deferral should be treated as a normal governed condition.

Preferred status label:

```text
multiallelic_relationship_deferred_to_vdb
```

Backward-compatible alias if needed:

```text
multiallelic_direct_link_deferred
```

The preferred label is a governed condition or advisory code, not a replacement
for the core relationship fields.

For a preserved multiallelic source record, the recommended core fields remain:

```text
variant_relationship_status = complex
relationship_reason = multiallelic_source_record
relationship_resolution_target = vdb_brokerage
```

The governed condition may be represented in summary or advisory fields as:

```text
multiallelic_relationship_deferred_to_vdb
```

This avoids overloading `variant_relationship_status` with both structural state
and workflow status.

Policy:

```text
A preserved multiallelic genotype observation with deferred allele-specific
relationship construction is a normal governed condition.

It is not evidence loss.
It is not a projection failure.
It is not a malformed record.
It is not a VAP warning unless additional malformedness or lossiness is present.
```

Recommended projection summary behavior:

```text
projection_status = PASS
    if all readable records are preserved and complex relationships are
    governed-deferred without malformedness or loss.

projection_status = PASS_WITH_ADVISORY
    if complex relationships exist and downstream VDB brokerage is required.

projection_status = PASS_WITH_WARNINGS
    if malformed-but-preserved records exist.

projection_status = FAIL
    if required source/header/sample/file integrity prevents trustworthy emission.
```

For a dataset with preserved multiallelic records and no malformed GT / FORMAT mismatches / preservation failures, multiallelic records should contribute to advisory or status counts, not failure counts.

---

## 12. Edge Case Handling

VAP should classify and preserve edge cases.

VAP should not over-resolve them.

### 12.1 Called Allele Index Exceeds ALT Count

Example:

```text
ALT = C,G
GT  = 1/3
```

Recommended VAP state:

```text
variant_relationship_status = unresolved
relationship_reason = called_allele_index_out_of_range
relationship_resolution_target = not_resolvable_by_vap
record_parse_status = malformed_gt_preserved
```

VAP preserves the raw record and raw GT.

VAP does not create an allele-specific relationship for the out-of-range allele.

### 12.2 Symbolic ALT

Example:

```text
ALT = <DEL>
```

Recommended VAP state:

```text
variant_relationship_status = complex
relationship_reason = symbolic_alt
relationship_resolution_target = vdb_brokerage
```

VAP preserves the source record.

VAP does not impose symbolic-variant identity semantics unless a specific VAP policy exists.

### 12.3 Spanning Deletion `*`

Example:

```text
ALT = *
```

Recommended VAP state:

```text
variant_relationship_status = complex
relationship_reason = spanning_deletion
relationship_resolution_target = vdb_brokerage
```

VAP preserves the source record.

VAP does not treat `*` as a simple allele-specific SNV/indel variant.

### 12.4 Mixed or Malformed GT Separators

Examples:

```text
0/1|2
1//2
1/a
```

Recommended VAP state:

```text
variant_relationship_status = unresolved
relationship_reason = malformed_gt
relationship_resolution_target = not_resolvable_by_vap
record_parse_status = malformed_gt_preserved
```

VAP preserves the raw GT.

VAP does not infer phase, ploidy, or allele-specific relationships beyond what is parseable under policy.

### 12.5 Nontrivial Normalization Required

Recommended VAP state:

```text
variant_relationship_status = complex
relationship_reason = normalization_required_or_unavailable
relationship_resolution_target = vdb_brokerage
```

VAP preserves source allele strings and coordinate context.

VAP does not claim a direct normalized allele-specific relationship if normalization would be lossy, shifted, split, or policy-dependent.

### 12.6 Missing Direct Variant Identity

Recommended VAP state:

```text
variant_relationship_status = unresolved
relationship_reason = variant_identity_unavailable
relationship_resolution_target = vdb_brokerage
```

VAP preserves the record and genotype observation.

VAP does not fabricate a variant identity.

---

## 13. Projection Summary Requirements

VAP genotype projection summaries should distinguish ordinary governed complexity from malformedness or failure.

Recommended summary fields:

```text
source_records_total
records_readable
records_preserved
genotype_observation_rows_emitted
direct_relationship_count
complex_relationship_count
multiallelic_relationship_deferred_count
symbolic_alt_deferred_count
spanning_deletion_deferred_count
unresolved_relationship_count
malformed_gt_count
format_sample_mismatch_count
called_allele_index_out_of_range_count
missing_gt_count
no_call_count
partial_no_call_count
projection_advisory_count
projection_warning_count
projection_error_count
projection_status
```

Recommended interpretation:

```text
complex_relationship_count:
    governed downstream-brokerage cases, not failures by default

multiallelic_relationship_deferred_count:
    source-faithful records requiring VDB allele-specific relationship brokerage

unresolved_relationship_count:
    records requiring special downstream handling or missing prerequisites

malformed_gt_count:
    raw source genotype malformed or not parseable under VAP policy, but preserved

projection_warning_count:
    malformedness, lossiness, or structural issue counts

projection_advisory_count:
    expected governed complexity such as multiallelic brokerage deferral
```

---

## 14. Validation Requirements

DEX-VAP should validate the following invariants.

```text
1. Every readable selected-sample source VCF record produces at most one
   genotype observation row.

2. Multiallelic source records are not split into synthetic allele-specific
   genotype rows.

3. For biallelic unambiguous records, direct linkage may be emitted.

4. For multiallelic records, direct allele-specific variant_id linkage is not
   fabricated.

5. Raw GT is preserved exactly when present.

6. Raw AD / DP / GQ / PL are preserved when present.

7. Called allele indices are parsed deterministically when possible.

8. Called allele index out of range is explicitly classified.

9. Missing GT, no-call GT, partial no-call, malformed GT, and absent GT remain
   distinct.

10. Multiallelic relationship deferral is counted as governed condition or
    advisory, not projection failure.

11. The genotype artifact remains deterministic, source-order preserving,
    sample-aware, run-aware, assembly-aware, and source-traceable.

12. No inheritance interpretation is emitted by VAP.
```

Validation should fail if VAP silently drops source genotype records, silently splits multiallelic records into synthetic rows, or collapses malformed / missing / no-call / partial-no-call states.

---

## 15. Downstream Handoff to VDB

VAP must emit enough information for VDB to construct derived relationships such as:

```text
genotype_observation
    resolved_to_called_alt_allele
        allele_index = 1
        source_alt = C
        relationship_state = resolved_from_multiallelic_record

genotype_observation
    resolved_to_called_alt_allele
        allele_index = 2
        source_alt = G
        relationship_state = resolved_from_multiallelic_record
```

But VAP itself must not emit those as independent producer genotype observations.

The VAP-to-VDB handoff must preserve:

```text
genotype_observation_id
source_record_hash
source_record_ref
source_record_alt
reference_allele
alternate_alleles_raw
called_allele_indices
gt_raw
ad_raw
pl_raw
format_raw
sample_format_raw
variant_relationship_status
relationship_reason
relationship_resolution_target
traceability_refs
```

VDB will use these fields to construct additive, typed, policy-declared relationship topology.

---

## 16. Anti-Collapse Rules

VAP must enforce these anti-collapse rules:

```text
source VCF record ≠ allele-specific variant row

source-record genotype observation ≠ allele-specific genotype observation

multiallelic genotype relationship ≠ multiple producer genotype rows

raw GT / AD / PL evidence ≠ normalized convenience label

missing genotype ≠ homozygous reference

no call ≠ absence

partial no call ≠ direct allele-specific certainty

complex relationship ≠ projection failure

multiallelic relationship deferral ≠ evidence loss

heterozygous-like ≠ dominant-compatible

homozygous-alt-like ≠ recessive diagnosis

phase separator ≠ compound heterozygosity

VAP genotype preservation ≠ RDGP inheritance reasoning
```

These are scientific invariants, not implementation preferences.

---

## 17. Summary Doctrine

VAP preserves multiallelic genotype records as source-record-scoped producer evidence.

VAP does not split multiallelic genotype observations into synthetic allele-specific genotype rows.

VAP emits direct variant linkage only when the relationship is unambiguous.

For multiallelic or otherwise complex records, VAP preserves raw source fields, allele indices, depth vectors, record identity, and relationship status so VDB can construct allele-specific relationships as derived topology.

Multiallelic relationship deferral is a governed handoff state, not evidence loss, not a projection failure, and not producer-side interpretation.

Final boundary:

```text
VAP preserves.
VDB brokers.
RDGP reasons.
```
