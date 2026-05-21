from __future__ import annotations

from pathlib import Path
from typing import Any

from src.metrics.metric_collectors import safe_count_tsv_rows, safe_count_vcf_records
from src.metrics.metric_io import append_stage_metrics_long_tsv, ensure_metrics_dir, write_stage_metrics_json
from src.metrics.metric_record import make_metric

def _run_meta(state:dict[str,Any])->dict[str,str]:
    sample=state.get("sample",{})
    run=state.get("run",{})
    return {
        "run_id":run.get("run_id","unknown"),
        "sample_id":sample.get("sample_id","unknown"),
        "assay_type":sample.get("assay_type","unknown"),
        "run_classification":run.get("execution_mode","unknown"),
    }

def _emit(stage_name:str,stage_id:str,stage_label:str,filename:str,metrics:list,paths:dict[str,Any],state:dict[str,Any])->None:
    meta=_run_meta(state)
    metrics_dir=Path(paths["metrics_dir"])
    metrics_dir.mkdir(parents=True,exist_ok=True)
    write_stage_metrics_json(metrics_dir,filename,meta["run_id"],meta["sample_id"],meta["assay_type"],meta["run_classification"],stage_id,stage_label,metrics)
    append_stage_metrics_long_tsv(metrics_dir,metrics)

def _count_metric(metric_name,path,unit,category,stage_id,stage_label,state,source_rule,figure_support):
    meta=_run_meta(state)
    status,value=safe_count_vcf_records(Path(path)) if str(path).endswith(".vcf") else safe_count_tsv_rows(Path(path))
    return make_metric(
        metric_name=metric_name,
        metric_value=value,
        metric_unit=unit,
        metric_status=status,
        metric_category=category,
        stage_id=stage_id,
        stage_name=stage_label,
        sample_id=meta["sample_id"],
        run_id=meta["run_id"],
        assay_type=meta["assay_type"],
        run_classification=meta["run_classification"],
        source_artifact=str(path),
        source_column_or_rule=source_rule,
        derivation_rule=source_rule,
        intended_figure_support=figure_support,
    )

def emit_stage_05_metrics(config,paths,state,logger)->None:
    raw_vcf=state.get("artifacts",{}).get("raw_vcf")
    metrics=[_count_metric("raw_called_variants",raw_vcf,"variants","f3_refinement_flow","stage_05","call_variants",state,"count non-header VCF records",["F3A"])]
    _emit("stage_05_call_variants","stage_05","call_variants","stage_05_variant_calling_metrics.json",metrics,paths,state)

def emit_stage_06_metrics(config,paths,state,logger)->None:
    normalized_vcf=state.get("artifacts",{}).get("normalized_vcf")
    metrics=[_count_metric("normalized_variants",normalized_vcf,"variants","f3_refinement_flow","stage_06","normalize_vcf",state,"count non-header VCF records",["F3A"])]
    _emit("stage_06_normalize_vcf","stage_06","normalize_vcf","stage_06_normalization_metrics.json",metrics,paths,state)

def emit_stage_07_metrics(config,paths,state,logger)->None:
    artifacts=state.get("artifacts",{})
    metrics=[
        _count_metric("annotated_variants_vcf",artifacts.get("annotated_vcf"),"variants","f3_refinement_flow","stage_07","annotate_variants",state,"count non-header VCF records",["F3A"]),
        _count_metric("annotated_variants_tsv",artifacts.get("annotated_table"),"rows","f3_refinement_flow","stage_07","annotate_variants",state,"count TSV data rows excluding header",["F3A","F4"]),
    ]
    _emit("stage_07_annotate_variants","stage_07","annotate_variants","stage_07_annotation_metrics.json",metrics,paths,state)

def emit_metrics_for_stage(stage_name:str,config:dict[str,Any],paths:dict[str,Any],state:dict[str,Any],logger)->None:
    dispatch={
        "stage_05_call_variants":emit_stage_05_metrics,
        "stage_06_normalize_vcf":emit_stage_06_metrics,
        "stage_07_annotate_variants":emit_stage_07_metrics,
    }
    emitter=dispatch.get(stage_name)
    if emitter is None:
        return
    try:
        emitter(config,paths,state,logger)
        logger.info(f"Sidecar metrics emitted for {stage_name}")
    except Exception as exc:
        logger.warning(f"Sidecar metric emission failed for {stage_name}: {exc}")