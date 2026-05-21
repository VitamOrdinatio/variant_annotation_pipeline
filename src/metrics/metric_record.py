from dataclasses import dataclass,asdict
from datetime import datetime,timezone
from typing import Any

VALID_STATUSES={"available","not_available","source_missing","unsupported","not_applicable","validation_failed"}

@dataclass(frozen=True)
class MetricRecord:
    metric_name:str
    metric_value:Any
    metric_unit:str
    metric_status:str
    metric_category:str
    stage_id:str
    stage_name:str
    sample_id:str
    run_id:str
    assay_type:str
    run_classification:str
    source_artifact:str
    source_column_or_rule:str
    derivation_rule:str
    generated_at:str
    intended_figure_support:list[str]

    def to_dict(self)->dict:
        if self.metric_status not in VALID_STATUSES:
            raise ValueError(f"Invalid metric_status: {self.metric_status}")
        return asdict(self)

def utc_now_iso()->str:
    return datetime.now(timezone.utc).isoformat()

def make_metric(**kwargs)->MetricRecord:
    if "generated_at" not in kwargs or not kwargs["generated_at"]:
        kwargs["generated_at"]=utc_now_iso()
    return MetricRecord(**kwargs)