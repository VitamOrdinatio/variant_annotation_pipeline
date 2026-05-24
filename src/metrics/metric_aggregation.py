from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

def read_stage_metrics_long(metrics_path:Path)->list[dict[str,str]]:
    path=Path(metrics_path)
    if not path.exists():
        raise FileNotFoundError(f"Metric long TSV not found: {path}")
    with path.open("r",encoding="utf-8",newline="") as handle:
        return list(csv.DictReader(handle,delimiter="\t"))

def metric_lookup(rows:list[dict[str,str]])->dict[tuple[str,str],dict[str,str]]:
    return {(row["stage_id"],row["metric_name"]):row for row in rows}

def _metric_value_int(lookup:dict[tuple[str,str],dict[str,str]],stage_id:str,metric_name:str)->int:
    row=lookup.get((stage_id,metric_name))
    if row is None:
        raise KeyError(f"Required metric missing: {metric_name}")
    if row.get("metric_status")!="available":
        raise ValueError(f"Metric not available: {metric_name}")
    return int(float(row["metric_value"]))

def build_f3a_flow_table(metrics_long_path:Path,out_path:Path)->Path:
    rows=read_stage_metrics_long(metrics_long_path)
    lookup=metric_lookup(rows)

    edges=[
        ("stage_05","raw_called_variants","stage_06","normalized_variants","raw_to_normalized"),
        ("stage_06","normalized_variants","stage_07","annotated_variants_tsv","normalized_to_annotated"),
        ("stage_07","annotated_variants_tsv","stage_08","partitioned_variants_total","annotated_to_partitioned"),
        ("stage_08","partitioned_variants_total","stage_08","coding_candidates","partitioned_to_coding"),
        ("stage_08","partitioned_variants_total","stage_08","splice_region_candidates","partitioned_to_splice_region"),
        ("stage_08","partitioned_variants_total","stage_08","noncoding_candidates","partitioned_to_noncoding"),
        ("stage_08","partitioned_variants_total","stage_08","qc_flagged","partitioned_to_qc_flagged"),
        ("stage_08","coding_candidates","stage_09","coding_interpreted_rows","coding_to_interpreted"),
        ("stage_08","splice_region_candidates","stage_09","coding_interpreted_rows","splice_to_coding_interpreted"),
        ("stage_08","noncoding_candidates","stage_10","noncoding_interpreted_rows","noncoding_to_interpreted"),
        ("stage_09","coding_interpreted_rows","stage_11","prioritized_variants_rows","coding_interpreted_to_prioritized"),
        ("stage_10","noncoding_interpreted_rows","stage_11","prioritized_variants_rows","noncoding_interpreted_to_prioritized"),
        ("stage_11","prioritized_variants_rows","stage_12","validation_candidates_rows","prioritized_to_validation"),
    ]

    out_path=Path(out_path)
    out_path.parent.mkdir(parents=True,exist_ok=True)

    fieldnames=[
        "source_metric",
        "target_metric",
        "source_node",
        "target_node",
        "edge_label",
        "source_value",
        "target_value",
        "edge_value",
        "value_rule",
    ]

    with out_path.open("w",encoding="utf-8",newline="") as handle:
        writer=csv.DictWriter(handle,fieldnames=fieldnames,delimiter="\t")
        writer.writeheader()

        for source_stage,source_metric,target_stage,target_metric,edge_label in edges:
            try:
                source_value=_metric_value_int(lookup,source_stage,source_metric)
                target_value=_metric_value_int(lookup,target_stage,target_metric)
            except (KeyError,ValueError):
                continue

            edge_value=min(source_value,target_value)

            writer.writerow({
                "source_metric":source_metric,
                "target_metric":target_metric,
                "source_node":f"{source_stage}:{source_metric}",
                "target_node":f"{target_stage}:{target_metric}",
                "edge_label":edge_label,
                "source_value":source_value,
                "target_value":target_value,
                "edge_value":edge_value,
                "value_rule":"min(source_value,target_value)",
            })

    return out_path

def _metric_value_sum(lookup,stage_metric_pairs):
    total=0
    for stage_name,metric_name in stage_metric_pairs:
        row=lookup[(stage_name,metric_name)]
        total+=int(float(row["metric_value"]))
    return total

def build_f3a_flow_table_v2(metrics_long_path,output_path):
    import csv,math
    from datetime import datetime,timezone
    from pathlib import Path

    metrics_long_path=Path(metrics_long_path)
    output_path=Path(output_path)
    rows=read_stage_metrics_long(metrics_long_path)
    lookup={(r["stage_id"],r["metric_name"]):r for r in rows}

    edges=[
        (
            1,
            "stage_05",
            "Called variants",
            "raw_called_variants",
            "stage_07",
            "Annotated evidence",
            "annotated_variants_tsv",
            "annotation_enables_interpretability"
        ),
        (
            2,
            "stage_07",
            "Annotated evidence",
            "annotated_variants_tsv",
            "stage_11",
            "Rare interpretable evidence",
            "counts_by_source_interpretation_label__lof_or_missense_rare",
            "rare_interpretable_evidence_includes_coding_and_regulatory_transcript_rare"
        ),
        (
            3,
            "stage_11",
            "Rare interpretable evidence",
            "counts_by_source_interpretation_label__lof_or_missense_rare",
            "stage_11",
            "Prioritized candidates",
            "high_priority_candidate_count",
            "prioritization_not_diagnosis"
        ),
        (
            4,
            "stage_11",
            "Prioritized candidates",
            "high_priority_candidate_count",
            "stage_12",
            "Validation-ready evidence",
            "counts_by_validation_required__True",
            "validation_ready_not_clinically_validated"
        ),
    ]

    fields=[
        "figure_id","run_id","sample_id","assay_type","run_classification",
        "edge_order","source_stage_id","source_label","target_stage_id","target_label",
        "source_metric_name","target_metric_name",
        "source_metric_value","target_metric_value","edge_metric_value",
        "scaling_mode","scaling_value","scaling_rule",
        "lineage_role","semantic_caveat","source_artifact","generated_at"
    ]

    out=[]
    generated_at=datetime.now(timezone.utc).isoformat()
    for edge_order,src_stage,src_label,src_metric,tgt_stage,tgt_label,tgt_metric,caveat in edges:
        src=lookup[(src_stage,src_metric)]
        tgt=lookup[(tgt_stage,tgt_metric)]
        edge_value=int(float(tgt["metric_value"]))

        if tgt_label=="Rare interpretable evidence":
            edge_value=_metric_value_sum(
                lookup,
                [
                    ("stage_11","counts_by_source_interpretation_label__lof_rare_clinically_supported"),
                    ("stage_11","counts_by_source_interpretation_label__lof_or_missense_rare"),
                    ("stage_11","counts_by_source_interpretation_label__regulatory_or_transcript_rare"),
                ]
            )

        if tgt_metric=="high_priority_candidate_count":
            moderate=_metric_value_sum(
                lookup,
                [("stage_11","moderate_priority_candidate_count")]
            )
            edge_value+=moderate

        if tgt_metric=="counts_by_validation_required__True":
            edge_value=int(float(
                lookup[("stage_12","counts_by_validation_required__True")]["metric_value"]
            ))
        out.append({
            "figure_id":"F3A",
            "run_id":tgt.get("run_id","unknown"),
            "sample_id":tgt.get("sample_id","unknown"),
            "assay_type":tgt.get("assay_type","unknown"),
            "run_classification":tgt.get("run_classification","unknown"),
            "edge_order":edge_order,
            "source_stage_id":src_stage,
            "source_label":src_label,
            "target_stage_id":tgt_stage,
            "target_label":tgt_label,
            "source_metric_name":src_metric,
            "target_metric_name":tgt_metric,
            "source_metric_value":int(float(src["metric_value"])),
            "target_metric_value":edge_value,
            "edge_metric_value":edge_value,
            "scaling_mode":"log10",
            "scaling_value":math.log10(edge_value+1),
            "scaling_rule":"log10(edge_metric_value + 1)",
            "lineage_role":"coarse_refinement_backbone",
            "semantic_caveat":caveat if caveat else "none",
            "source_artifact":str(metrics_long_path),
            "generated_at":generated_at,
        })

    output_path.parent.mkdir(parents=True,exist_ok=True)
    with output_path.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields,delimiter="\t",lineterminator="\n")
        w.writeheader()
        w.writerows(out)
    return output_path

def build_f3b_semantic_branching_table(metrics_long_path,output_path):
    import csv
    from datetime import datetime,timezone
    from pathlib import Path

    metrics_long_path=Path(metrics_long_path)
    output_path=Path(output_path)
    rows=read_stage_metrics_long(metrics_long_path)
    lookup={(r["stage_id"],r["metric_name"]):r for r in rows}
    generated_at=datetime.now(timezone.utc).isoformat()

    def get(stage,metric):
        row=lookup[(stage,metric)]
        return int(float(row["metric_value"])),row

    branches=[
        ("coding_rare_interpretable","Coding rare interpretable evidence","stage_11","counts_by_source_interpretation_label__lof_or_missense_rare","coding evidence retained after semantic interpretation"),
        ("regulatory_transcript_rare","Regulatory/transcript rare evidence","stage_11","counts_by_source_interpretation_label__regulatory_or_transcript_rare","noncoding evidence retained as biologically meaningful substrate"),
        ("common_low_support","Common or low-support evidence","stage_11","counts_by_source_interpretation_label__coding_common_or_low_support","coding common or low-support evidence retained but deprioritized"),
        ("noncoding_common_low_support","Noncoding common or low-support evidence","stage_11","counts_by_source_interpretation_label__noncoding_common_or_low_support","noncoding common or low-support evidence retained but deprioritized"),
        ("uninterpretable_or_qc_limited","Uninterpretable or QC-limited evidence","stage_11","counts_by_source_interpretation_label__coding_uninterpretable","coding uninterpretable evidence retained with limitations"),
        ("noncoding_uninterpretable","Noncoding uninterpretable evidence","stage_11","counts_by_source_interpretation_label__noncoding_uninterpretable","noncoding uninterpretable evidence retained with limitations"),
    ]

    fields=[
        "figure_id","run_id","sample_id","assay_type","run_classification",
        "branch_order","branch_id","branch_label","stage_id","metric_name",
        "metric_value","semantic_role","semantic_caveat",
        "source_artifact","generated_at"
    ]

    out=[]
    for i,(branch_id,label,stage,metric,caveat) in enumerate(branches,1):
        value,row=get(stage,metric)
        out.append({
            "figure_id":"F3B",
            "run_id":row.get("run_id","unknown"),
            "sample_id":row.get("sample_id","unknown"),
            "assay_type":row.get("assay_type","unknown"),
            "run_classification":row.get("run_classification","unknown"),
            "branch_order":i,
            "branch_id":branch_id,
            "branch_label":label,
            "stage_id":stage,
            "metric_name":metric,
            "metric_value":value,
            "semantic_role":"semantic_evidence_branch",
            "semantic_caveat":caveat,
            "source_artifact":str(metrics_long_path),
            "generated_at":generated_at,
        })

    output_path.parent.mkdir(parents=True,exist_ok=True)
    with output_path.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields,delimiter="\t",lineterminator="\n")
        w.writeheader()
        w.writerows(out)
    return output_path