# NOTE THIS IS WIP DOCUMENT, NEEDS OPERATOR VALIDATION BEFORE USAGE

# Stage 09 — Interpret Coding Variants Contract

**Pipeline:** Variant Annotation Pipeline (VAP)
**Stage:** 09
**Name:** interpret_coding
**Status:** Specification (Pre-Implementation)

---

# 🧭 Purpose

Stage 09 performs **biological interpretation of coding variants** using structured outputs from Stage 08.

It transforms:

```text
structured annotation → biologically meaningful interpretation flags
```

without performing final prioritization.

---

# 🎯 Design Principles

1. **Interpretation, not prioritization**

   * No ranking or scoring
   * Only classification and flagging

2. **Evidence preservation**

   * All Stage 08 data must remain intact
   * No variant removal based on interpretation

3. **Deterministic rule-based logic**

   * No probabilistic or ML-based scoring in v1

4. **Variant-level independence**

   * Each variant is interpreted independently
   * Gene-level reasoning occurs later (RDGP)

---

# 📥 Inputs

## Required Files

```text
coding_candidates.tsv
stage_08_variant_summary.tsv
stage_08_transcript_consequences.tsv
```

---

## Required Fields (must be present)

* sample_id
* variant_id
* gene_id / gene_symbol
* consequence
* impact_class
* variant_context
* variant_type
* variant_class
* population_frequency
* gnomad_af / exac_af / thousand_genomes_af
* clinical_significance
* clinvar_significance
* qc_status
* quality_flag
* annotation_source
* annotation_version

---

# 🔄 Processing Logic

## Step 1 — Select Coding Variants

Include only variants where:

```text
variant_context = coding OR splice_region
```

Exclude:

```text
intronic, intergenic, regulatory (handled in Stage 10)
```

---

## Step 2 — Assign Functional Impact Class

Derive:

```text
functional_impact ∈ {
  loss_of_function,
  missense,
  synonymous,
  splice_relevant,
  other_coding
}
```

### Mapping

* loss_of_function:

  * stop_gained
  * frameshift_variant
  * start_lost
  * splice_acceptor_variant
  * splice_donor_variant

* missense:

  * missense_variant

* synonymous:

  * synonymous_variant

* splice_relevant:

  * splice_region_variant

---

## Step 3 — Assign Rarity Flag

Using Stage 08:

```text
frequency_status → rarity_flag
```

```text
rarity_flag ∈ {
  rare,
  low_frequency,
  common,
  unknown
}
```

---

## Step 4 — Assign Clinical Evidence Flag

```text
clinical_evidence ∈ {
  pathogenic,
  likely_pathogenic,
  vus,
  benign,
  conflicting,
  missing
}
```

Derived from:

* clinical_significance
* clinvar_significance

---

## Step 5 — Assign QC Reliability Flag

```text
qc_reliability ∈ {
  high_confidence,
  caution,
  low_confidence
}
```

Mapping:

* qc_status = pass → high_confidence
* qc_status = caution → caution
* qc_status = fail → low_confidence

---

## Step 6 — Composite Interpretation Flags

Stage 09 must derive boolean flags:

```text
is_lof_candidate
is_rare_candidate
is_clinically_supported
is_high_quality
is_potential_artifact
```

---

### Rules

```text
is_lof_candidate =
  functional_impact == loss_of_function

is_rare_candidate =
  rarity_flag == rare

is_clinically_supported =
  clinical_evidence ∈ {pathogenic, likely_pathogenic}

is_high_quality =
  qc_reliability == high_confidence

is_potential_artifact =
  qc_reliability == low_confidence
```

---

## Step 7 — Interpretation Tier (non-ranking)

Assign:

```text
interpretation_tier ∈ {
  strong_candidate,
  moderate_candidate,
  weak_candidate,
  uninterpretable
}
```

### Deterministic rules

```text
strong_candidate:
  LOF AND rare AND clinically_supported AND high_quality

moderate_candidate:
  (LOF OR missense) AND (rare OR low_frequency) AND high_quality

weak_candidate:
  coding but common OR lacking support

uninterpretable:
  missing key fields OR low_quality
```

---

# 📤 Outputs

## Required Files

```text
stage_09_coding_interpreted.tsv
stage_09_summary.json
```

---

## stage_09_coding_interpreted.tsv

Must include ALL Stage 08 fields PLUS:

* functional_impact
* rarity_flag
* clinical_evidence
* qc_reliability
* interpretation_tier
* is_lof_candidate
* is_rare_candidate
* is_clinically_supported
* is_high_quality
* is_potential_artifact

---

## stage_09_summary.json

Must include:

* total_coding_variants
* lof_variant_count
* rare_variant_count
* clinically_supported_count
* tier_distribution
* qc_distribution

---

# 🔒 Invariants

1. No variants are removed
2. All Stage 08 fields are preserved
3. Interpretation is deterministic
4. No ranking or prioritization occurs
5. No external databases are queried

---

# ⚠️ Explicit Non-Goals

Stage 09 MUST NOT:

* rank genes or variants
* integrate gene-level evidence (RDGP responsibility)
* interpret noncoding variants
* use ML predictors (AlphaMissense, etc.)
* perform phenotype matching

---

# 🧠 Handoff to Stage 10

Stage 10 will:

```text
interpret noncoding variants
```

Stage 11 will:

```text
prioritize variants
```

---

# 🎯 Bottom Line

Stage 09 transforms:

```text
annotated coding variants → interpretable biological signals
```

It is the first stage that produces:

```text
human-readable variant meaning
```

without making final decisions.

---

# END
