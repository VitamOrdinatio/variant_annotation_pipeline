# Data Schema  
## variant_annotation_pipeline v1.0  
## docs/implementation/data_schema.md

---

## 1. Purpose

This document defines the **file-level data structures** produced by  
`variant_annotation_pipeline` v1.0.

It specifies:

- TSV column schemas
- required fields for downstream stages
- interoperability expectations between stages
- constraints for reproducibility and aggregation

This document governs **on-disk outputs**, not in-memory state.

---

## 2. Governing Principle

```text
All downstream analysis operates on structured, tabular outputs.
```

Every stage that produces tabular data must:

- emit consistent column names
- preserve required fields
- avoid lossy transformations
- support downstream filtering, interpretation, and prioritization

---

## 3. Core Output Files

The pipeline produces the following primary tabular outputs:

| File | Stage | Description |
|------|------|------------|
| annotated_variants.tsv | 07 | Raw annotated variants |
| filtered_variants.tsv | 08 | Variants after filtering |
| coding_variants.tsv | 08 | Coding subset |
| noncoding_variants.tsv | 08 | Non-coding subset |
| interpreted_coding.tsv | 09 | Coding interpretation |
| interpreted_noncoding.tsv | 10 | Non-coding interpretation |
| prioritized_variants.tsv | 11 | Final prioritized variants |
| gene_summary.tsv | 11 | Gene-level summary |

---

## 4. Annotated Variants Schema (Stage 07)

File: `annotated_variants.tsv`

### Required columns

| Column | Description |
|--------|------------|
| chromosome | Chromosome |
| position | Genomic coordinate |
| reference_allele | REF |
| alternate_allele | ALT |
| gene_symbol | Gene name |
| transcript_id | Transcript identifier |
| consequence | VEP consequence |
| impact | Predicted impact |
| clinvar_significance | ClinVar classification |
| gnomad_af | gnomAD allele frequency |
| exac_af | ExAC allele frequency |
| thousand_genomes_af | 1000 Genomes AF |
| mito_flag | MitoCarta membership |
| epilepsy_flag | Epilepsy gene set membership |

### Notes

- Must preserve all variants from normalized VCF
- No filtering occurs at this stage
- Must be lossless relative to VCF annotations

---

## 5. Filtered Variants Schema (Stage 08)

File: `filtered_variants.tsv`

### Required columns

All columns from `annotated_variants.tsv` must be preserved.

### Additional columns

| Column | Description |
|--------|------------|
| filter_pass | Boolean indicating filter success |

### Filtering rules (v1)

- AF thresholds (gnomAD, ExAC, 1000G)
- optional consequence-based filtering

---

## 6. Partitioned Outputs (Stage 08)

### Coding variants

File: `coding_variants.tsv`

Criteria:
- consequence ∈ allowed coding consequences

---

### Non-coding variants

File: `noncoding_variants.tsv`

Criteria:
- not classified as coding

---

## 7. Interpreted Coding Schema (Stage 09)

File: `interpreted_coding.tsv`

### Additional columns

| Column | Description |
|--------|------------|
| functional_class | e.g. missense, nonsense |
| predicted_severity | qualitative severity |
| interpretation_notes | free-text annotation |

---

## 8. Interpreted Non-Coding Schema (Stage 10)

File: `interpreted_noncoding.tsv`

### Additional columns

| Column | Description |
|--------|------------|
| regulatory_annotation | regulatory classification |
| proximity_annotation | upstream/downstream |
| interpretation_notes | free-text annotation |

---

## 9. Prioritized Variants Schema (Stage 11)

File: `prioritized_variants.tsv`

### Required columns

All prior columns must be preserved.

### Additional columns

| Column | Description |
|--------|------------|
| priority_label | high / medium / low |
| priority_score | numeric score |
| prioritization_basis | explanation |

### Example prioritization drivers

- ClinVar pathogenic
- high-impact consequence
- mito_flag
- epilepsy_flag

---

## 10. Gene Summary Schema (Stage 11)

File: `gene_summary.tsv`

### Columns

| Column | Description |
|--------|------------|
| gene_symbol | Gene name |
| variant_count | Number of variants |
| prioritized_variant_count | Number of prioritized variants |
| mito_flag | MitoCarta membership |
| epilepsy_flag | Epilepsy membership |

---

## 11. Validation Outputs (Stage 12)

### IGV candidate list

File: `igv_review_candidates.tsv`

| Column | Description |
|--------|------------|
| chromosome | Chromosome |
| position | Position |
| gene_symbol | Gene |
| reason_for_review | Why flagged |

---

### Validation notes

File: `validation_notes.md`

Free-text structured notes including:

- benchmark comparison summary
- IGV review guidance
- suspicious variant commentary

---

## 12. Summary Output (Stage 13)

File: `run_summary_report.md`

### Required sections

- run metadata
- sample metadata
- variant counts
- filtering summary
- prioritization summary
- validation summary

---

## 13. Data Integrity Rules

All tables must:

- be UTF-8 encoded
- use tab delimiters
- include header row
- not contain duplicate column names
- not drop required columns across stages

---

## 14. Missing Data Rules

Missing values must be encoded as:

```text
NA
```

Not:

- empty string
- null
- None

---

## 15. Determinism Rules

Outputs must be:

- stable given identical inputs
- consistent column ordering
- reproducible across runs

---

## 16. Compatibility with Aggregation

All schemas must support:

```text
docs/implementation/aggregation_schema.md
```

This requires:

- inclusion of gene_symbol
- inclusion of genomic coordinates
- preservation of prioritization fields

---

## 17. Future Extensions

Future versions may add:

- AI-based scores (AlphaMissense, SpliceAI)
- conservation scores
- structural annotations
- pathway annotations

### Design rule

```text
new columns may be added, existing columns must not be removed
```

---

## 18. Summary Rule

```text
Every stage produces structured, lossless, and aggregation-ready tabular data.
```

---

# End of Data Schema