# Stage 10 — Interpret Noncoding Variants Contract

**Pipeline:** Variant Annotation Pipeline (VAP)
**Stage:** 10
**Name:** interpret_noncoding
**Status:** Specification (Pre-Implementation)

---

# 🧭 Purpose

Stage 10 performs **biological interpretation of noncoding variants** using structured outputs from Stage 08.

It transforms:

```text
structured annotation → biologically meaningful interpretation flags (noncoding)
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

5. **Explicit uncertainty acknowledgment**

   * Noncoding interpretation is inherently lower confidence than coding
   * Missing or weak annotation must not be overinterpreted

---

# 📥 Inputs

## Required Files

```text
noncoding_candidates.tsv
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

* preserve variant
* set noncoding_interpretation_label = noncoding_uninterpretable
* exclude from gene-linked downstream handoff

Gene-linked downstream handoff includes any future VDB/RDGP aggregation seed or gene-level evidence table.

---

# 🔄 Processing Logic

## Step 1 — Select Noncoding Variants

Include only variants where:

```text
variant_context ∈ {
  regulatory,
  intronic,
  intergenic,
  noncoding_transcript
}
```

Exclude:

```text
coding, splice_region (handled in Stage 09)
```

Stage 10 must not consume `splice_region_candidates.tsv`.

Splice-region variants are routed to Stage 09 because they may affect coding transcript structure through splicing.

---


## Step 2 — Assign Functional Context Class

Derive:

```text
noncoding_functional_context ∈ {
  regulatory,
  transcript_associated,
  intergenic,
  unknown
}
```

### Mapping

* regulatory:

  * regulatory_region_variant
  * TF_binding_site_variant
  * upstream_gene_variant
  * downstream_gene_variant

* transcript_associated:

  * non_coding_transcript_exon_variant
  * non_coding_transcript_variant
  * NMD_transcript_variant

* intergenic:

  * intergenic_variant

* unknown:

  * any unmatched consequence


### Multiple Consequence Rule

If `consequence` contains multiple terms for the same selected transcript,
Stage 10 must assign the most specific applicable `noncoding_functional_context`.

Precedence:

```text
regulatory > transcript_associated > intergenic > unknown
```


---

## Step 3 — Assign Rarity Flag

Using Stage 08 `frequency_status`:

```text
rarity_flag ∈ {
  rare,
  low_frequency,
  common,
  missing,
  unknown
}
```

**Mapping**

```text
frequency_status = rare → rarity_flag = rare
frequency_status = low_frequency → rarity_flag = low_frequency
frequency_status = common → rarity_flag = common
frequency_status = missing → rarity_flag = missing
frequency_status = unknown → rarity_flag = unknown
```

Stage 10 must not infer rarity from missing frequency data.

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

`clinical_evidence` is the Stage 10 noncoding-interpretation copy of Stage 08 `clinical_status`.

Stage 10 must not reinterpret raw `clinvar_significance` directly unless `clinical_status` is missing or invalid.


---

## Step 5 — Assign QC Reliability Flag

```text
qc_reliability ∈ {
  high_confidence,
  caution,
  low_confidence
}
```

Same mapping as Stage 09.

---

## Step 6 — Composite Interpretation Flags

```text
is_regulatory_candidate
is_rare_candidate
is_clinically_supported
is_high_quality
is_potential_artifact
```

### Rules

```text
is_regulatory_candidate =
  noncoding_functional_context = regulatory

is_rare_candidate =
  rarity_flag = rare

is_clinically_supported =
  clinical_evidence ∈ {pathogenic, likely_pathogenic}

is_high_quality =
  qc_reliability = high_confidence

is_potential_artifact =
  qc_reliability = low_confidence
```

---

## Step 7 — Assign Noncoding Interpretation Label

```text
noncoding_interpretation_label ∈ {
  regulatory_rare_supported,
  regulatory_or_transcript_rare,
  noncoding_common_or_low_support,
  noncoding_uninterpretable
}
```

### Deterministic rules

```text
noncoding_uninterpretable:
  gene_mapping_status = unmapped
  OR qc_reliability = low_confidence
  OR missing key fields

regulatory_rare_supported:
  noncoding_functional_context = regulatory
  AND rarity_flag = rare
  AND clinical_evidence ∈ {pathogenic, likely_pathogenic}
  AND qc_reliability = high_confidence

regulatory_or_transcript_rare:
  noncoding_functional_context ∈ {regulatory, transcript_associated}
  AND rarity_flag ∈ {rare, low_frequency}
  AND qc_reliability = high_confidence
  AND clinical_evidence NOT IN {benign, likely_benign}

noncoding_common_or_low_support:
  common variants
  OR benign/likely_benign
  OR lacking strong support
```

### Guardrail

```text
A regulatory or transcript-associated variant that is common or benign/likely_benign
must not receive `regulatory_rare_supported`.
```

### Label Assignment Precedence

If multiple label rules apply, assign labels in this order:

```text
noncoding_uninterpretable
→ noncoding_common_or_low_support
→ regulatory_rare_supported
→ regulatory_or_transcript_rare
```

---

# 📤 Outputs

## Required Files

```text
stage_10_noncoding_interpreted.tsv
stage_10_summary.json
```

---

## stage_10_noncoding_interpreted.tsv

Must include ALL Stage 08 fields PLUS:

* noncoding_functional_context
* rarity_flag
* clinical_evidence
* qc_reliability
* noncoding_interpretation_label
* is_regulatory_candidate
* is_rare_candidate
* is_clinically_supported
* is_high_quality
* is_potential_artifact

Preserve provenance fields.

---

## stage_10_summary.json

Must include:

- total_noncoding_variants
- regulatory_variant_count
- transcript_associated_variant_count
- intergenic_variant_count
- rare_variant_count
- low_frequency_variant_count
- common_variant_count
- clinically_supported_count
- benign_or_likely_benign_count
- uninterpretable_count
- noncoding_interpretation_label_distribution
- rarity_flag_distribution
- qc_distribution
- noncoding_functional_context_distribution
- clinical_evidence_distribution

### Summary Count Rules

Unless explicitly labeled transcript-level, all summary counts must be based on distinct `variant_id`.

### Distribution Definitions

Follow the same rules as Stage 09, using:

- noncoding_interpretation_label
- noncoding_functional_context

### Scalar Count Definitions

- `total_noncoding_variants`: distinct variant_id count in Stage 10 input
- `regulatory_variant_count`: distinct variant_id count where noncoding_functional_context = regulatory
- `transcript_associated_variant_count`: distinct variant_id count where noncoding_functional_context = transcript_associated
- `intergenic_variant_count`: distinct variant_id count where noncoding_functional_context = intergenic
- `rare_variant_count`: distinct variant_id count where rarity_flag = rare
- `low_frequency_variant_count`: distinct variant_id count where rarity_flag = low_frequency
- `common_variant_count`: distinct variant_id count where rarity_flag = common
- `clinically_supported_count`: distinct variant_id count where clinical_evidence ∈ {pathogenic, likely_pathogenic}
- `benign_or_likely_benign_count`: distinct variant_id count where clinical_evidence ∈ {benign, likely_benign}
- `uninterpretable_count`: distinct variant_id count where noncoding_interpretation_label = noncoding_uninterpretable

---

# 🔒 Invariants

Same as Stage 09, including:

```text
No biological inference from missingness
```

---

# ⚠️ Explicit Non-Goals

Stage 10 MUST NOT:

* rank variants
* perform gene prioritization
* use ML predictors
* assume regulatory effect implies pathogenicity

---

# 🧠 Handoff to Stage 11

Stage 11 will:

```text
prioritize variants (coding + noncoding together)
```

---

# Future Extension — AlphaGenome Support

Stage 10 v1 does not run AlphaGenome.

A future Stage 10 version may optionally add AlphaGenome-derived fields for noncoding variants, including:

- alphagenome_available
- alphagenome_model_version
- alphagenome_score
- alphagenome_predicted_effect
- alphagenome_target_gene
- alphagenome_tissue_or_cell_context
- alphagenome_provenance

AlphaGenome-derived fields must be treated as predictive evidence, not deterministic truth.

Stage 11 may consume these fields if present, but Stage 11 must not call AlphaGenome directly.

---

# 🎯 Bottom Line

Stage 10 transforms:

```text
noncoding variants → structured, cautious biological interpretation
```

without overclaiming functional impact.

---

# END
