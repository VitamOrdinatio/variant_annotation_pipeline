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
