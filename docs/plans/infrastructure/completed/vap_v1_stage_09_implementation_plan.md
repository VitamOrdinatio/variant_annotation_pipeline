# vap_v1_stage_09_implementation_plan.md

- Stage 09 implementation plan for VAP v1 
- Stage 09 interprets coding variant candidates and also splice region variant candidates



## 1. Target file

Implement in:

`pipeline/stage_09_interpret_coding.py`

Entry point:

```text
def run_stage(config: dict[str, Any], paths: dict[str, Any], logger, state: dict[str, Any]) -> dict[str, Any]:
```


---

## 2. Inputs

Primary inputs from `state["artifacts"]`:

```text
coding_candidates.tsv
splice_region_candidates.tsv
stage_08_variant_summary.tsv
stage_08_selected_transcript_consequences.tsv
```

Operationally, Stage 09 will concatenate/stream:

```text
coding_candidates.tsv
splice_region_candidates.tsv
```

and validate that required Stage 08 fields exist.


---

## 3. Outputs

Write to processed_dir:

```text
stage_09_coding_interpreted.tsv
stage_09_summary.json
```

Then register:

```text
state["artifacts"]["stage_09_coding_interpreted"]
state["artifacts"]["stage_09_summary_json"]
state["qc"]["stage_09_qc"]
state["stage_outputs"]["stage_09_interpret_coding"]
```


---

## 4. Core helper functions

Implement small deterministic helpers:

```text
_split_consequence_terms(consequence)
_assign_functional_impact(consequence)
_assign_rarity_flag(frequency_status)
_assign_clinical_evidence(clinical_status, clinvar_significance)
_assign_qc_reliability(qc_status)
_has_missing_key_fields(row)
_assign_coding_interpretation_label(row)
_update_summary_sets(summary_sets, interpreted_row)
_write_summary_json(summary_sets)
```


---

## 5. Functional impact logic

Use consequence precedence:

`loss_of_function > missense > splice_relevant > other_coding > synonymous > unknown`

This handles combined terms like:

`splice_region_variant&missense_variant`

without ambiguity.


---

## 6. Clinical evidence logic
Use `clinical_status` first. Only if missing/invalid, normalize `clinvar_significance`.

Allowed outputs:

```text
pathogenic
likely_pathogenic
vus
likely_benign
benign
conflicting
missing
```

No raw ClinVar reinterpretation unless Stage 08 status is missing/invalid.


---

## 7. Label assignment logic

Implementation order should be:
       
    1. compute all derived fields 
    2. compute booleans 
    3. assign label 

Label decision should be functionally:

```text
if missing key fields OR gene_mapping_status == unmapped OR qc_reliability == low_confidence:
    coding_uninterpretable
elif rarity_flag == common OR clinical_evidence in {benign, likely_benign}:
    coding_common_or_low_support
elif functional_impact == loss_of_function AND rarity_flag == rare AND clinical_evidence in {pathogenic, likely_pathogenic} AND qc_reliability == high_confidence:
    lof_rare_clinically_supported
elif functional_impact in {loss_of_function, missense} AND rarity_flag in {rare, low_frequency} AND qc_reliability == high_confidence AND clinical_evidence not in {benign, likely_benign}:
    lof_or_missense_rare
else:
    coding_common_or_low_support
```

This preserves precedence and prevents common/benign variants from receiving strong labels.


---

## 8. Summary counting

Use sets of variant_id, not row counters, for:

```text
total_coding_variants
lof_variant_count
missense_variant_count
rare_variant_count
low_frequency_variant_count
common_variant_count
clinically_supported_count
benign_or_likely_benign_count
uninterpretable_count
```

Also build distributions by sets:

```text
coding_interpretation_label_distribution
rarity_flag_distribution
qc_distribution
functional_impact_distribution
clinical_evidence_distribution
```


---

## 9. Memory model

Stage 09 input is small relative to Stage 08:

```text
coding_candidates.tsv ~6 MB
splice_region_candidates.tsv ~1 MB
```

So set-based summaries are fine. No heavy streaming refactor needed yet.


---

## 10. Test plan

First on Sys76:

`python -m py_compile pipeline/stage_09_interpret_coding.py`

Then push/pull to Mark and run a checkpoint probe that:
    1. activates .venv 
    2. finds latest Stage 08 outputs 
    3. runs Stage 09 only 
    4. prints: 
        ◦ summary JSON 
        ◦ first interpreted coding rows 
        ◦ label distribution 
        ◦ examples for LOF, missense, common/low support, uninterpretable if present 

---

# end of file

---