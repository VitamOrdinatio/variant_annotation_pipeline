from .metric_record import MetricRecord,VALID_STATUSES

REQUIRED_FIELDS=[
    "metric_name","metric_value","metric_unit","metric_status","metric_category",
    "stage_id","stage_name","sample_id","run_id","assay_type","run_classification",
    "source_artifact","source_column_or_rule","derivation_rule","generated_at",
    "intended_figure_support"
]

def validate_metric_record(metric:MetricRecord)->list[str]:
    errors=[]
    data=metric.to_dict()
    for field in REQUIRED_FIELDS:
        if field not in data:
            errors.append(f"missing_field:{field}")
        elif data[field] in ("",None,[]):
            errors.append(f"empty_field:{field}")
    if data.get("metric_status") not in VALID_STATUSES:
        errors.append(f"invalid_metric_status:{data.get('metric_status')}")
    if data.get("metric_status")=="available":
        value=data.get("metric_value")
        if isinstance(value,(int,float)):
            if value<0:
                errors.append("negative_metric_value")
        elif isinstance(value,str):
            try:
                numeric=float(value)
                if numeric<0:
                    errors.append("negative_metric_value")
            except ValueError:
                pass
    return errors

def validate_metric_records(metrics:list[MetricRecord])->dict:
    record_errors=[]
    for idx,metric in enumerate(metrics):
        errors=validate_metric_record(metric)
        if errors:
            record_errors.append({"index":idx,"metric_name":metric.metric_name,"errors":errors})
    return {
        "record_count":len(metrics),
        "error_count":len(record_errors),
        "status":"PASS" if not record_errors else "FAIL",
        "errors":record_errors
    }