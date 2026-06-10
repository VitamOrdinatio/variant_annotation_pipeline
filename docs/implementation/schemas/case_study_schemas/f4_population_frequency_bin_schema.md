# f4_population_frequency_bin_schema.md

## Purpose

This document defines the canonical population-frequency collapse schema for:
- F4A (coding semantic composition)
- F4B (noncoding semantic composition)

within the Variant Annotation Pipeline (VAP) case-study figure ecosystem.

The goal is to provide:
- reviewer-friendly semantic observability,
- deterministic category assignment,
- and cross-panel consistency

while avoiding excessive population-genetics complexity inappropriate for F4 cognition targets.

---

# Strategic Philosophy

F4 figures are intended to communicate:

> preserved biological semantic composition

NOT:
- detailed population-genetics analysis,
- ancestry-specific stratification,
- fine-grained allele-frequency modeling,
- or pathogenicity inference.

Therefore:
population frequency values are intentionally collapsed into a small number of reviewer-readable semantic bins.

---

# Canonical Population Frequency Categories

The following four categories are canonical for both:
- F4A coding semantic composition
- F4B noncoding semantic composition

| Category | Meaning |
|---|---|
| `rare` | Very low population frequency evidence |
| `low_frequency` | Intermediate-frequency evidence |
| `common` | High-frequency background variation |
| `missing` | No usable population-frequency annotation |

---

# Deterministic Threshold Rules

## Rare

```text
AF < 0.01
```

Interpretation:

- low-frequency population substrate,
- potentially enriched for biologically interesting evidence,
- but NOT interpreted as pathogenicity.

---

## Low Frequency

```text
0.01 ≤ AF < 0.05
```

Interpretation:

- transitional frequency space,
- uncommon but not rare.

---

## Common

```text
AF ≥ 0.05
```

Interpretation:

- high-frequency background variation,
- likely broad population substrate.

---

## Missing

Assigned when:

- AF value is null,
- absent,
- missing,
- NA,
- unparsable,
- or population-frequency annotation is unavailable.



Important:

```text
Missing population-frequency annotation is NOT interpreted as rarity.
```

This distinction must be preserved throughout:

- telemetry,
- semantic collapse,
- figure generation,
- and reviewer-facing cognition.

---

# Canonical Category Ordering

For:

- TSV generation,
- plotting,
- legends,
- and figure consistency,

the canonical ordering is:

```text
rare
low_frequency
common
missing
```

This ordering preserves:

- biological interpretability,
- semantic intuition,
- and cross-panel consistency.

Alphabetical ordering should NOT be used.

---

# Cross-Figure Consistency Requirement

The same deterministic schema must be applied identically across:

- coding evidence,
- noncoding evidence,
- and future reusable figure-generation infrastructure.

This enables:

- reviewer familiarity,
- stable cognition,
- reusable plotting logic,
- and deterministic semantic interpretation.

---

# Color Governance Guidance

Population-frequency categories should use restrained scientific palette governance consistent with:

- F3A,
- F3B,
- and future F4/F5 panels.

Recommended semantic tone hierarchy:

| Category        | Suggested Tone    |
| --------------- | ----------------- |
| `rare`          | darker slate blue |
| `low_frequency` | muted steel blue  |
| `common`        | pale blue-gray    |
| `missing`       | graphite-gray     |

Avoid:

- rainbow palettes,
- neon saturation,
- heatmap aesthetics,
- or dashboard-style color intensity.

---

# Reviewer Cognition Goal

The reviewer should quickly understand:

what fraction of preserved evidence is:

- rare,
- uncommon,
- common,
- or unannotated.

The figure should NOT imply:

- pathogenicity,
- causality,
- diagnostic interpretation,
- or clinical prioritization.

Population-frequency composition remains:

- observational,
- infrastructure-oriented,
- and semantically descriptive.

---

# Recommended Figure Footnote Language

>Population frequency values were collapsed into deterministic rarity bins for visual readability. Missing annotations were preserved as a distinct category and not interpreted as rarity.


---

# Governance Notes

This schema is intentionally:

- low-complexity,
- reviewer-friendly,
- deterministic,
- and reusable across future VAP figure-generation infrastructure.

Additional population-genetics complexity should be reserved for:

- downstream analyses,
- specialized reports,
- or future ecosystem tooling,
- NOT for F4 semantic composition cognition.

---