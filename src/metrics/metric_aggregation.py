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

def metric_lookup(rows:list[dict[str,str]])->dict[str,dict[str,str]]:
    return {row["metric_name"]:row for row in rows}

def _metric_value_int(lookup:dict[str,dict[str,str]],metric_name:str)->int:
    row=lookup.get(metric_name)
    if row is None:
        raise KeyError(f"Required metric missing: {metric_name}")
    if row.get("metric_status")!="available":
        raise ValueError(f"Metric not available: {metric_name}")
    return int(float(row["metric_value"]))

def build_f3a_flow_table(metrics_long_path:Path,out_path:Path)->Path:
    rows=read_stage_metrics_long(metrics_long_path)
    lookup=metric_lookup(rows)

    edges=[
        ("raw_called_variants","normalized_variants","raw_to_normalized"),
        ("normalized_variants","annotated_variants_tsv","normalized_to_annotated"),
        ("annotated_variants_tsv","partitioned_variants_total","annotated_to_partitioned"),
        ("partitioned_variants_total","coding_candidates","partitioned_to_coding"),
        ("partitioned_variants_total","splice_region_candidates","partitioned_to_splice_region"),
        ("partitioned_variants_total","noncoding_candidates","partitioned_to_noncoding"),
        ("partitioned_variants_total","qc_flagged","partitioned_to_qc_flagged"),
        ("coding_candidates","coding_interpreted_rows","coding_to_interpreted"),
        ("splice_region_candidates","coding_interpreted_rows","splice_to_coding_interpreted"),
        ("noncoding_candidates","noncoding_interpreted_rows","noncoding_to_interpreted"),
        ("coding_interpreted_rows","prioritized_variants_rows","coding_interpreted_to_prioritized"),
        ("noncoding_interpreted_rows","prioritized_variants_rows","noncoding_interpreted_to_prioritized"),
        ("prioritized_variants_rows","validation_candidates_rows","prioritized_to_validation"),
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

        for source_metric,target_metric,edge_label in edges:
            source_value=_metric_value_int(lookup,source_metric)
            target_value=_metric_value_int(lookup,target_metric)
            edge_value=min(source_value,target_value)

            writer.writerow({
                "source_metric":source_metric,
                "target_metric":target_metric,
                "source_node":source_metric,
                "target_node":target_metric,
                "edge_label":edge_label,
                "source_value":source_value,
                "target_value":target_value,
                "edge_value":edge_value,
                "value_rule":"min(source_value,target_value)",
            })

    return out_path
