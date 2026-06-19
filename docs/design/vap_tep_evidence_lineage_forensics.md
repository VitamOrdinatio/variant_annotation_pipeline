# VAP-TEP Evidence Lineage Forensics

## Purpose

This document captures forensic questions, hypotheses, empirical findings, and architectural conclusions related to evidence preservation across the post-annotation stages of VAP.

The goal is to establish a scientifically defensible evidence-lineage model that can guide VAP-TEP construction.

This document intentionally separates:

```text
Preservation Doctrine
```

from

```text
Implementation Forensics
```

The former answers:

```text
What should be preserved?
```

The latter answers:

```text
How does evidence actually move through the pipeline?
```

---

# Investigation Theme

A VAP-TEP should preserve evidence in a manner that supports:

* reproducibility
* reinterpretability
* provenance preservation
* downstream interoperability

To accomplish this, every evidence transition must be accounted for.

Guiding principle:

```text
No variant left behind.
```

Any evidence removed, partitioned, transformed, summarized, interpreted, prioritized, or validated must be explainable through deterministic lineage.

---

# Stage07 → Stage08 Findings

Current forensic findings support:

```text
Stage07
    Observation Anchor

Stage08
    Row-Preserving Interoperability Projection
```

Observed properties:

* row-preserving across thirteen production runs
* preservation of observation substrate
* addition of interoperability metadata
* semantic enrichment rather than semantic reduction

Additional finding:

```text
stage_08_selected_transcript_consequences.tsv

stage_08_vdb_ready_variants.tsv
```

are checksum-identical in VAP v1.

However, they represent distinct semantic roles and may diverge in future VAP releases.

Therefore both artifact identities should remain visible to future TEP construction.

---

# Current Investigation: Stage08 Partition Integrity

## Motivation

The Stage08 substrate appears to represent the last complete variant population prior to interpretation routing.

Understanding Stage08 partitioning is therefore critical to preservation design.

---

## Working Hypothesis

Stage08 may represent a lossless biological partition layer:

```text
Stage08
├── coding_candidates
├── splice_region_candidates
└── noncoding_candidates
```

Potential downstream routing:

```text
Stage09
    coding_candidates
    +
    splice_region_candidates

Stage10
    noncoding_candidates
```

If true:

```text
Stage08
=
coding
+
splice
+
noncoding
```

with no unexplained evidence loss.

---

# Empirical Findings: Stage08 Routing Topology

## Finding

Stage08 does not behave as three mutually exclusive partitions.

Production forensics performed across thirteen completed VAP runs demonstrated:

```text
coding ∩ splice      > 0

coding ∩ noncoding   = 0

splice ∩ noncoding   = 0
```

for every audited run.

No exceptions were observed.

---

## Interpretation

This behavior indicates that Stage08 routing populations are not best understood as:

```text
coding
splice
noncoding
```

three disjoint partitions.

Instead, evidence supports:

```text
coding partition

noncoding partition

splice overlay
```

where splice-associated biology may coexist with coding biology.

---

## Supporting Evidence

Across all audited runs:

* overlap occurred exclusively between coding and splice populations
* no overlap occurred between coding and noncoding populations
* no overlap occurred between splice and noncoding populations

All overlapping variants exhibited:

```text
variant_context = splice_region
```

without exception.

---

## Consequence Structure

The splice-overlap population was dominated by:

```text
missense_variant & splice_region_variant

splice_region_variant & synonymous_variant
```

with smaller contributions from:

* frameshift-associated splice variants
* stop-gained splice variants
* splice donor variants
* splice acceptor variants

This pattern was highly stable across both WES and WGS runs.

---

## Preservation Implication

The Stage08 substrate should not be modeled as a simple three-way partition.

A more accurate preservation model is:

```text
Stage08
├── Coding Partition
├── Noncoding Partition
└── Splice Overlay
```

This distinction is important for future VAP-TEP construction because splice-associated evidence may participate simultaneously in coding interpretation and splice interpretation contexts.

---

## Current Architectural Interpretation

Working evidence-lineage model:

```text
Stage07
    Observation Anchor

Stage08
    Biological Routing Layer

        Coding Partition
        Noncoding Partition
        Splice Overlay

Stage09
    Coding + Splice Interpretation

Stage10
    Noncoding Interpretation

Stage11
    Prioritization

Stage12
    Validation

Stage13
    Summary / Audit Context (pending audit)
```

---

# Empirical Findings: Stage13 Context Role

Stage13 outputs are invariant run-level artifacts
that summarize and audit Stage11 and Stage12 outputs.

Across both epilepsy WES and HG002 WGS runs,
Stage13 produced only:

    final summary
    artifact manifest
    run report

No variant-level entities were generated.

No interpretation was performed.

No prioritization was performed.

No validation reasoning was performed.

Stage13 therefore functions as a run-context layer
rather than a scientific evidence layer.

Preservation implication:

Stage13 should accompany a VAP-TEP as provenance
and audit context but should not be treated as the
primary preserved scientific payload.

---

# Open Forensic Questions

## Question A

Does:

```text
coding_candidates
+
splice_region_candidates
+
noncoding_candidates
```

exactly reconstruct:

```text
Stage08
```

across all production runs?

---

## Question B

What fraction of Stage08 belongs to each partition?

Specifically:

```text
coding
splice
noncoding
```

for:

* epilepsy WES runs
* HG002 WGS run

---

## Question C

Does Stage09 preserve splice-region inputs as interpreted outputs?

Specifically:

```text
splice_region_candidates.tsv
```

→

```text
stage_09_coding_interpreted.tsv
```

Questions:

* Are all splice candidates preserved?
* Are splice candidates transformed?
* Are splice candidates reprioritized?
* Are splice candidates explicitly modeled?

---

## Question D

Is splice biology effectively a first-class semantic partition?

Potential evidence model:

```text
Stage08
├── Coding
├── Splice
└── Noncoding
```

rather than:

```text
Stage08
├── Coding
└── Noncoding
```

If true, this has direct implications for future VAP-TEP payload modeling.

---

# Future Investigation: Interpretation Lineage

Additional planned investigations:

```text
Stage08 → Stage09

Stage08 → Stage10

Stage09 → Stage11

Stage10 → Stage11

Stage11 → Stage12

Stage13 role audit
```

Goal:

Construct a complete evidence-lineage map for the preservation-critical half of VAP.

---

# Long-Term Objective

Establish a preservation lineage model equivalent to a Sankey diagram:

```text
Observation
    ↓
Partition
    ↓
Interpretation
    ↓
Prioritization
    ↓
Validation
    ↓
Summary
```

where every variant population can be deterministically accounted for.

Success condition:

```text
No variant left behind.
```

Every transition must be explainable.

Every reduction must be intentional.

Every preserved entity must remain traceable.
