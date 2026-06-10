# F3A v2 canonical plotting substrate schema

Recommended file:

`metrics/figure_f3a_flow_v2.tsv`


## Source TSV Schema Logic

| Column        | Purpose                    |
| ------------- | -------------------------- |
| source_stage  | provenance lineage         |
| source_label  | displayed node label       |
| target_stage  | provenance lineage         |
| target_label  | displayed node label       |
| metric_name   | canonical telemetry metric |
| metric_value  | canonical count            |
| scaling_value | plotting-transformed value |
| scaling_mode  | linear/log                 |
| run_id        | provenance                 |
| sample_id     | provenance                 |
| assay_type    | provenance                 |

---

## Required Columns

| Column | Type | Meaning |
|---|---:|---|
| `figure_id` | str | Always `F3A` |
| `run_id` | str | Canonical VAP run ID |
| `sample_id` | str | Sample accession, e.g. `ERR10619300` |
| `assay_type` | str | e.g. `WES` |
| `run_classification` | str | e.g. `full_pipeline` |
| `edge_order` | int | Left-to-right plotting order |
| `source_stage_id` | str | Source stage, e.g. `stage_05` |
| `source_label` | str | Display label for source node |
| `target_stage_id` | str | Target stage |
| `target_label` | str | Display label for target node |
| `source_metric_name` | str | Telemetry metric supporting source count |
| `target_metric_name` | str | Telemetry metric supporting target count |
| `source_metric_value` | int | Raw source count |
| `target_metric_value` | int | Raw target count |
| `edge_metric_value` | int | Raw count represented by edge; usually target count |
| `scaling_mode` | str | `log10` for F3A v1 |
| `scaling_value` | float | Plot width value |
| `scaling_rule` | str | e.g. `log10(edge_metric_value + 1)` |
| `lineage_role` | str | e.g. `coarse_refinement_backbone` |
| `semantic_caveat` | str | Explicit caveat, e.g. `stage08_overlap_compressed` |
| `source_artifact` | str | Source telemetry file |
| `generated_at` | str | ISO timestamp |

---

## Canonical edges:

```text
1 Raw variants → Normalized variants
2 Normalized variants → Annotated variants
3 Annotated variants → Partitioned evidence
4 Partitioned evidence → Prioritized evidence
5 Prioritized evidence → Validation-ready evidence
```

---

## Canonical metric mapping:

```text
raw_called_variants → normalized_variants
normalized_variants → annotated_variants_tsv
annotated_variants_tsv → partitioned_variants_total
partitioned_variants_total → prioritized_variants_rows
prioritized_variants_rows → validation_candidates_rows
```

---

## Critical rule:

```text
edge_metric_value = target_metric_value
scaling_value = log10(edge_metric_value + 1)
```

