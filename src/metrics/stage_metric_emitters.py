from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from src.metrics.metric_collectors import safe_count_tsv_rows, safe_count_vcf_records, safe_exact_string_distribution, safe_binned_population_frequency
from src.metrics.metric_io import append_stage_metrics_long_tsv, ensure_metrics_dir, write_stage_metrics_json
from src.metrics.metric_record import make_metric

def _distribution_metrics(metric_prefix,distribution,unit,category,stage_id,stage_label,state,source_artifact,source_rule,figure_support):
    metrics=[]
    if not isinstance(distribution,dict):
        metrics.append(_json_scalar_metric(f"{metric_prefix}__not_available",None,unit,category,stage_id,stage_label,state,source_artifact,source_rule,figure_support))
        return metrics

    for key,value in distribution.items():
        safe_key=str(key).strip().replace(" ","_").replace("/","_").replace(";","_").replace(",","_")
        if safe_key=="":
            safe_key="missing"
        metrics.append(_json_scalar_metric(f"{metric_prefix}__{safe_key}",value,unit,category,stage_id,stage_label,state,source_artifact,f"{source_rule}.{key}",figure_support))
    return metrics

def _json_scalar_metric(metric_name,value,unit,category,stage_id,stage_label,state,source_artifact,source_rule,figure_support):
    meta=_run_meta(state)
    status="available" if value is not None else "not_available"
    return make_metric(
        metric_name=metric_name,
        metric_value=value if value is not None else "not_available",
        metric_unit=unit,
        metric_status=status,
        metric_category=category,
        stage_id=stage_id,
        stage_name=stage_label,
        sample_id=meta["sample_id"],
        run_id=meta["run_id"],
        assay_type=meta["assay_type"],
        run_classification=meta["run_classification"],
        source_artifact=str(source_artifact),
        source_column_or_rule=source_rule,
        derivation_rule=source_rule,
        intended_figure_support=figure_support,
    )

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

def emit_stage_08_metrics(config,paths,state,logger)->None:
    artifacts=state.get("artifacts",{})
    summary_path=Path(artifacts.get("stage_08_summary_json",""))
    metrics=[]

    if summary_path.exists():
        summary=json.loads(summary_path.read_text(encoding="utf-8"))
        metrics.extend([
            _json_scalar_metric("partitioned_variants_total",summary.get("total_variants"),"variants","f3_refinement_flow","stage_08","filter_and_partition",state,summary_path,"stage_08_summary.json total_variants",["F3A"]),
            _json_scalar_metric("irreparably_malformed_rows",summary.get("irreparably_malformed_rows"),"rows","f3_refinement_flow","stage_08","filter_and_partition",state,summary_path,"stage_08_summary.json irreparably_malformed_rows",["F3A"]),
            _json_scalar_metric("variant_summary_rows",summary.get("variant_summary_rows"),"rows","f3_refinement_flow","stage_08","filter_and_partition",state,summary_path,"stage_08_summary.json variant_summary_rows",["F3A"]),
            _json_scalar_metric("rdgp_gene_evidence_seed_rows",summary.get("rdgp_gene_evidence_seed_rows"),"rows","f5_overlay_readiness","stage_08","filter_and_partition",state,summary_path,"stage_08_summary.json rdgp_gene_evidence_seed_rows",["F5"]),
        ])

        for key,value in summary.get("partition_counts",{}).items():
            metrics.append(_json_scalar_metric(key,value,"rows","f3_semantic_decomposition","stage_08","filter_and_partition",state,summary_path,f"stage_08_summary.json partition_counts.{key}",["F3B","F4"]))

        for dist_name in ["variants_by_context","variants_by_severity","qc_status_counts","interpretability_counts","frequency_status","clinical_status","variants_by_variant_type","variants_by_variant_class"]:
            for key,value in summary.get(dist_name,{}).items():
                metrics.append(_json_scalar_metric(f"{dist_name}__{key}",value,"variants","f4_biological_landscape","stage_08","filter_and_partition",state,summary_path,f"stage_08_summary.json {dist_name}.{key}",["F4"]))
    else:
        metrics.append(_json_scalar_metric("stage_08_summary_json_available",None,"status","metric_availability","stage_08","filter_and_partition",state,summary_path,"source file existence check",["F3A"]))

    row_count_targets=[
        ("selected_transcript_consequences_rows",artifacts.get("stage_08_selected_transcript_consequences"),"F3A"),
        ("vdb_ready_variants_rows",artifacts.get("stage_08_vdb_ready_variants"),"F5"),
        ("coding_candidates_rows",artifacts.get("coding_candidates"),"F3B"),
        ("splice_region_candidates_rows",artifacts.get("splice_region_candidates"),"F3B"),
        ("noncoding_candidates_rows",artifacts.get("noncoding_candidates"),"F3B"),
        ("qc_flagged_rows",artifacts.get("qc_flagged"),"F4"),
        ("rdgp_gene_evidence_seed_tsv_rows",artifacts.get("stage_08_rdgp_gene_evidence_seed"),"F5"),
    ]
    for metric_name,path,figure in row_count_targets:
        if path:
            metrics.append(_count_metric(metric_name,path,"rows","stage08_artifact_row_count","stage_08","filter_and_partition",state,"count TSV data rows excluding header",[figure]))

    _emit("stage_08_filter_and_partition","stage_08","filter_and_partition","stage_08_partition_metrics.json",metrics,paths,state)

def emit_stage_09_metrics(config,paths,state,logger)->None:
    artifacts=state.get("artifacts",{})
    stage09_path=artifacts.get("stage_09_coding_interpreted")
    metrics=[]

    if stage09_path:
        metrics.append(_count_metric("coding_interpreted_rows",stage09_path,"rows","stage09_artifact_row_count","stage_09","interpret_coding",state,"count TSV data rows excluding header",["F3B","F4"]))

        exact_columns=[
            "consequence",
            "clinical_significance",
            "clinvar_significance",
            "functional_impact",
            "rarity_flag",
        ]

        for column in exact_columns:
            status,distribution=safe_exact_string_distribution(Path(stage09_path),column)
            if status=="available":
                metrics.extend(_distribution_metrics(f"{column}_distribution",distribution,"rows","stage09_semantic_distribution","stage_09","interpret_coding",state,stage09_path,f"exact string counts for {column}",["F4"]))
            else:
                metrics.append(_json_scalar_metric(f"{column}_distribution_available",None,"status","metric_availability","stage_09","interpret_coding",state,stage09_path,f"exact string counts for {column}",["F4"]))

        status,distribution=safe_binned_population_frequency(Path(stage09_path),"population_frequency")
        if status=="available":
            metrics.extend(_distribution_metrics("population_frequency_bin",distribution,"rows","stage09_semantic_distribution","stage_09","interpret_coding",state,stage09_path,"binned counts for population_frequency",["F4"]))
        else:
            metrics.append(_json_scalar_metric("population_frequency_bin_available",None,"status","metric_availability","stage_09","interpret_coding",state,stage09_path,"binned counts for population_frequency",["F4"]))

    _emit("stage_09_interpret_coding","stage_09","interpret_coding","stage_09_coding_interpretation_metrics.json",metrics,paths,state)

def emit_stage_10_metrics(config,paths,state,logger)->None:
    artifacts=state.get("artifacts",{})
    stage10_path=artifacts.get("stage_10_noncoding_interpreted")
    metrics=[]

    if stage10_path:
        metrics.append(_count_metric("noncoding_interpreted_rows",stage10_path,"rows","stage10_artifact_row_count","stage_10","interpret_noncoding",state,"count TSV data rows excluding header",["F3B","F4"]))

        exact_columns=[
            "consequence",
            "clinical_significance",
            "clinvar_significance",
            "rarity_flag",
            "variant_context",
            "noncoding_functional_context",
        ]

        for column in exact_columns:
            status,distribution=safe_exact_string_distribution(Path(stage10_path),column)
            if status=="available":
                metrics.extend(_distribution_metrics(f"{column}_distribution",distribution,"rows","stage10_semantic_distribution","stage_10","interpret_noncoding",state,stage10_path,f"exact string counts for {column}",["F4"]))
            else:
                metrics.append(_json_scalar_metric(f"{column}_distribution_available",None,"status","metric_availability","stage_10","interpret_noncoding",state,stage10_path,f"exact string counts for {column}",["F4"]))

        status,distribution=safe_binned_population_frequency(Path(stage10_path),"population_frequency")
        if status=="available":
            metrics.extend(_distribution_metrics("population_frequency_bin",distribution,"rows","stage10_semantic_distribution","stage_10","interpret_noncoding",state,stage10_path,"binned counts for population_frequency",["F4"]))
        else:
            metrics.append(_json_scalar_metric("population_frequency_bin_available",None,"status","metric_availability","stage_10","interpret_noncoding",state,stage10_path,"binned counts for population_frequency",["F4"]))

    _emit("stage_10_interpret_noncoding","stage_10","interpret_noncoding","stage_10_noncoding_interpretation_metrics.json",metrics,paths,state)

def emit_stage_11_metrics(config,paths,state,logger)->None:
    artifacts=state.get("artifacts",{})
    summary_path=Path(artifacts.get("stage_11_summary_json",""))
    metrics=[]

    if summary_path.exists():
        summary=json.loads(summary_path.read_text(encoding="utf-8"))

        scalar_targets=[
            ("input_rows","rows","F3A"),
            ("output_rows","rows","F3A"),
            ("unassigned_or_malformed_rows","rows","F4"),
            ("high_priority_candidate_count","variants","F3B"),
            ("moderate_priority_candidate_count","variants","F3B"),
            ("low_priority_candidate_count","variants","F3B"),
            ("uninterpretable_count","variants","F3B"),
            ("gene_id_count_unique","genes","F5"),
        ]

        for key,unit,figure in scalar_targets:
            metrics.append(
                _json_scalar_metric(
                    key,
                    summary.get(key),
                    unit,
                    "stage11_prioritization",
                    "stage_11",
                    "prioritize_variants",
                    state,
                    summary_path,
                    f"stage_11_summary.json {key}",
                    [figure],
                )
            )

        counter_targets=[
            "counts_by_priority_tier",
            "counts_by_priority_rank",
            "counts_by_variant_origin",
            "counts_by_source_interpretation_label",
        ]

        for counter_name in counter_targets:
            for key,value in summary.get(counter_name,{}).items():
                metrics.append(
                    _json_scalar_metric(
                        f"{counter_name}__{key}",
                        value,
                        "variants",
                        "stage11_distribution",
                        "stage_11",
                        "prioritize_variants",
                        state,
                        summary_path,
                        f"stage_11_summary.json {counter_name}.{key}",
                        ["F3B","F4"],
                    )
                )

    else:
        metrics.append(
            _json_scalar_metric(
                "stage_11_summary_json_available",
                None,
                "status",
                "metric_availability",
                "stage_11",
                "prioritize_variants",
                state,
                summary_path,
                "source file existence check",
                ["F3A"],
            )
        )

    row_count_targets=[
        ("prioritized_variants_rows",artifacts.get("stage_11_prioritized_variants"),"F3B"),
        ("gene_variant_counts_rows",artifacts.get("stage_11_gene_variant_counts"),"F5"),
    ]

    for metric_name,path,figure in row_count_targets:
        if path:
            metrics.append(
                _count_metric(
                    metric_name,
                    path,
                    "rows",
                    "stage11_artifact_row_count",
                    "stage_11",
                    "prioritize_variants",
                    state,
                    "count TSV data rows excluding header",
                    [figure],
                )
            )

    _emit(
        "stage_11_prioritize_variants",
        "stage_11",
        "prioritize_variants",
        "stage_11_prioritization_metrics.json",
        metrics,
        paths,
        state,
    )

def emit_stage_12_metrics(config,paths,state,logger)->None:
    artifacts=state.get("artifacts",{})
    summary_path=Path(artifacts.get("stage_12_summary_json",""))
    metrics=[]

    if summary_path.exists():
        summary=json.loads(summary_path.read_text(encoding="utf-8"))

        scalar_targets=[
            ("input_rows","rows","F3A"),
            ("output_rows","rows","F3A"),
            ("unrecognized_priority_rows","rows","F4"),
        ]

        for key,unit,figure in scalar_targets:
            metrics.append(
                _json_scalar_metric(
                    key,
                    summary.get(key),
                    unit,
                    "stage12_validation_preparation",
                    "stage_12",
                    "validate_variants",
                    state,
                    summary_path,
                    f"stage_12_summary.json {key}",
                    [figure],
                )
            )

        counter_targets=[
            "counts_by_validation_required",
            "counts_by_validation_priority",
            "counts_by_suggested_validation_method",
            "counts_by_priority_tier",
        ]

        for counter_name in counter_targets:
            for key,value in summary.get(counter_name,{}).items():
                metrics.append(
                    _json_scalar_metric(
                        f"{counter_name}__{key}",
                        value,
                        "variants",
                        "stage12_distribution",
                        "stage_12",
                        "validate_variants",
                        state,
                        summary_path,
                        f"stage_12_summary.json {counter_name}.{key}",
                        ["F3B","F4"],
                    )
                )

    else:
        metrics.append(
            _json_scalar_metric(
                "stage_12_summary_json_available",
                None,
                "status",
                "metric_availability",
                "stage_12",
                "validate_variants",
                state,
                summary_path,
                "source file existence check",
                ["F3A"],
            )
        )

    validation_candidates=artifacts.get("stage_12_validation_candidates")

    if validation_candidates:
        metrics.append(
            _count_metric(
                "validation_candidates_rows",
                validation_candidates,
                "rows",
                "stage12_artifact_row_count",
                "stage_12",
                "validate_variants",
                state,
                "count TSV data rows excluding header",
                ["F3B","F5"],
            )
        )

    _emit(
        "stage_12_validate_variants",
        "stage_12",
        "validate_variants",
        "stage_12_validation_metrics.json",
        metrics,
        paths,
        state,
    )

def emit_metrics_for_stage(stage_name:str,config:dict[str,Any],paths:dict[str,Any],state:dict[str,Any],logger)->None:
    dispatch={
        "stage_05_call_variants":emit_stage_05_metrics,
        "stage_06_normalize_vcf":emit_stage_06_metrics,
        "stage_07_annotate_variants":emit_stage_07_metrics,
        "stage_08_filter_and_partition":emit_stage_08_metrics,
        "stage_09_interpret_coding":emit_stage_09_metrics,
        "stage_10_interpret_noncoding":emit_stage_10_metrics,
        "stage_11_prioritize_variants":emit_stage_11_metrics,
        "stage_12_validate_variants":emit_stage_12_metrics,
    }
    emitter=dispatch.get(stage_name)
    if emitter is None:
        return
    try:
        emitter(config,paths,state,logger)
        logger.info(f"Sidecar metrics emitted for {stage_name}")
    except Exception as exc:
        logger.warning(f"Sidecar metric emission failed for {stage_name}: {exc}")