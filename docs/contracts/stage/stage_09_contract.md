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
stage_08_selected_transcript_consequences.tsv
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
* frequency_status
* clinical_status
* gene_mapping_status
* variant_effect_severity
* source_pipeline
* run_id

If gene_mapping_status = unmapped:
  - preserve variant
  - set coding_interpretation_label = coding_uninterpretable
  - exclude from any gene-linked downstream handoff

Gene-linked downstream handoff includes any future VDB/RDGP aggregation seed or gene-level evidence table.

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

- loss_of_function:
  - stop_gained
  - frameshift_variant
  - start_lost
  - stop_lost
  - splice_acceptor_variant
  - splice_donor_variant

- missense:
  - missense_variant

- synonymous:
  - synonymous_variant

- splice_relevant:
  - splice_region_variant

- other_coding:
  - inframe_insertion
  - inframe_deletion
  - protein_altering_variant
  - incomplete_terminal_codon_variant
  - coding_sequence_variant
  - any unmatched coding consequence

### Multiple Consequence Rule

If `consequence` contains multiple terms for the same selected transcript, Stage 09 must assign the most severe applicable `functional_impact`.

Precedence:

```text
loss_of_function > missense > splice_relevant > other_coding > synonymous
```

---

## Step 3 — Assign Rarity Flag

Using Stage 08 `frequency_status`:

**Rarity Flag:**

```text
frequency_status → rarity_flag
rarity_flag ∈ {
  rare,
  low_frequency,
  common,
  missing,
  unknown
}
```

**Mapping:**

```text
frequency_status = rare → rarity_flag = rare
frequency_status = low_frequency → rarity_flag = low_frequency
frequency_status = common → rarity_flag = common
frequency_status = missing → rarity_flag = missing
frequency_status = unknown → rarity_flag = unknown
```

---

## Step 4 — Assign Clinical Evidence Flag

```text
clinical_evidence ∈ {
  pathogenic,
  likely_pathogenic,
  vus,
  likely_benign,
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

frequency_status = missing → rarity_flag = missing

frequency_status = unknown → rarity_flag = unknown
```

---

## Step 7 — Assign Coding Interpretation Label

Assign a non-ranking interpretation label:

```text
coding_interpretation_label ∈ {
  lof_rare_clinically_supported,
  lof_or_missense_rare,
  coding_common_or_low_support,
  coding_uninterpretable
}
```

### Deterministic rules

```text
lof_rare_clinically_supported:
  functional_impact = loss_of_function
  AND rarity_flag = rare
  AND clinical_evidence ∈ {pathogenic, likely_pathogenic}
  AND qc_reliability = high_confidence

lof_or_missense_rare:
  functional_impact ∈ {loss_of_function, missense}
  AND rarity_flag ∈ {rare, low_frequency}
  AND qc_reliability = high_confidence
  AND clinical_evidence NOT IN {benign, likely_benign}

coding_common_or_low_support:
  coding variant that is common
  OR clinical_evidence ∈ {benign, likely_benign}
  OR lacks rare/clinical support

coding_uninterpretable:
  gene_mapping_status = unmapped
  OR qc_reliability = low_confidence
  OR missing key fields required for interpretation
```

**Guardrail:**

```text
A HIGH-impact or loss-of-function variant that is common or benign/likely_benign
must not receive lof_rare_clinically_supported.
```

### Label Assignment Precedence

If multiple label rules apply, assign labels in this order:

```text
coding_uninterpretable
→ coding_common_or_low_support
→ lof_rare_clinically_supported
→ lof_or_missense_rare
```

Rationale:

- failed QC or missing required fields overrides interpretation
- benign/common evidence prevents strong candidate labeling
- clinically supported rare LOF is the highest-confidence coding label

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
* coding_interpretation_label
* is_lof_candidate
* is_rare_candidate
* is_clinically_supported
* is_high_quality
* is_potential_artifact

Stage 09 outputs should preserve:
- annotation_source
- annotation_version
- source_pipeline
- run_id
- sample_id

---

## stage_09_summary.json

Must include:

- total_coding_variants
- lof_variant_count
- missense_variant_count
- rare_variant_count
- low_frequency_variant_count
- common_variant_count
- clinically_supported_count
- benign_or_likely_benign_count
- uninterpretable_count
- coding_interpretation_label_distribution
- rarity_flag_distribution
- qc_distribution
- functional_impact_distribution
- clinical_evidence_distribution

### Deduplication rule

Stage 09 should not inflate counts if Stage 08 later becomes multi-transcript:

```text
summary counts must be based on distinct variant_id values unless explicitly labeled transcript-level.
```

---

# 🔒 Invariants

1. No variants are removed
2. All Stage 08 fields are preserved
3. Interpretation is deterministic
4. No ranking or prioritization occurs
5. No external databases are queried
6. **No biological inference from missingness**

Stage 09 must not treat missing frequency as rare and must not treat missing clinical evidence as benign.

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
