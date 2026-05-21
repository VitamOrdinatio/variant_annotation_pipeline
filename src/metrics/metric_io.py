import csv,json
from pathlib import Path
from typing import Iterable
from .metric_record import MetricRecord

LONG_TSV_FIELDS=[
    "metric_name","metric_value","metric_unit","metric_status","metric_category",
    "stage_id","stage_name","sample_id","run_id","assay_type","run_classification",
    "source_artifact","source_column_or_rule","derivation_rule","generated_at",
    "intended_figure_support"
]

def ensure_metrics_dir(run_dir:Path)->Path:
    metrics_dir=run_dir/"metrics"
    metrics_dir.mkdir(parents=True,exist_ok=True)
    return metrics_dir

def write_stage_metrics_json(metrics_dir:Path,filename:str,run_id:str,sample_id:str,assay_type:str,run_classification:str,stage_id:str,stage_name:str,metrics:Iterable[MetricRecord])->Path:
    records=[m.to_dict() for m in metrics]
    out=metrics_dir/filename
    payload={
        "run_id":run_id,
        "sample_id":sample_id,
        "assay_type":assay_type,
        "run_classification":run_classification,
        "stage_id":stage_id,
        "stage_name":stage_name,
        "metrics":records
    }
    out.write_text(json.dumps(payload,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    return out

def append_stage_metrics_long_tsv(metrics_dir:Path,metrics:Iterable[MetricRecord])->Path:
    out=metrics_dir/"stage_metrics_long.tsv"
    exists=out.exists()
    records=[m.to_dict() for m in metrics]
    with out.open("a",encoding="utf-8",newline="") as handle:
        writer=csv.DictWriter(handle,fieldnames=LONG_TSV_FIELDS,delimiter="\t",lineterminator="\n")
        if not exists:
            writer.writeheader()
        for row in records:
            row=row.copy()
            row["intended_figure_support"]=";".join(row.get("intended_figure_support",[]))
            writer.writerow({k:row.get(k,"") for k in LONG_TSV_FIELDS})
    return out