from __future__ import annotations

import csv
from pathlib import Path
from typing import Any
import json
from datetime import datetime,timezone

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
        (
            "coding_rare_interpretable",
            "Coding rare interpretable evidence",
            "rare_interpretable",
            "coding",
            "stage_11",
            "counts_by_source_interpretation_label__lof_or_missense_rare",
            "coding evidence retained after semantic interpretation"
        ),

        (
            "regulatory_transcript_rare",
            "Regulatory/transcript rare evidence",
            "rare_interpretable",
            "noncoding",
            "stage_11",
            "counts_by_source_interpretation_label__regulatory_or_transcript_rare",
            "noncoding evidence retained as biologically meaningful substrate"
        ),

        (
            "common_low_support",
            "Common or low-support evidence",
            "common_low_support",
            "coding",
            "stage_11",
            "counts_by_source_interpretation_label__coding_common_or_low_support",
            "coding common or low-support evidence retained but deprioritized"
        ),

        (
            "noncoding_common_low_support",
            "Noncoding common or low-support evidence",
            "common_low_support",
            "noncoding",
            "stage_11",
            "counts_by_source_interpretation_label__noncoding_common_or_low_support",
            "noncoding common or low-support evidence retained but deprioritized"
        ),

        (
            "coding_uninterpretable",
            "Coding uninterpretable evidence",
            "uninterpretable",
            "coding",
            "stage_11",
            "counts_by_source_interpretation_label__coding_uninterpretable",
            "coding uninterpretable evidence retained with limitations"
        ),

        (
            "noncoding_uninterpretable",
            "Noncoding uninterpretable evidence",
            "uninterpretable",
            "noncoding",
            "stage_11",
            "counts_by_source_interpretation_label__noncoding_uninterpretable",
            "noncoding uninterpretable evidence retained with limitations"
        ),
    ]

    fields=[
        "figure_id","run_id","sample_id","assay_type","run_classification",
        "branch_order","branch_id","branch_label",
        "semantic_group","branch_class",
        "stage_id","metric_name",
        "metric_value","semantic_role","semantic_caveat",
        "source_artifact","generated_at"
    ]

    out=[]
    for i,(
        branch_id,
        label,
        semantic_group,
        branch_class,
        stage,
        metric,
        caveat
    ) in enumerate(branches,1):    
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
            "semantic_group":semantic_group,
            "branch_class":branch_class,            
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

def _read_metrics_json(metrics_json_path:Path)->list[dict[str,Any]]:
    path=Path(metrics_json_path)
    if not path.exists():
        raise FileNotFoundError(f"Metrics JSON not found: {path}")

    with path.open("r",encoding="utf-8") as handle:
        payload=json.load(handle)

    metrics=payload.get("metrics")
    if not isinstance(metrics,list):
        raise ValueError(f"Expected top-level 'metrics' list in: {path}")

    return metrics

def _build_f4_semantic_composition_table(
    *,
    figure_id:str,
    metrics_json_path:Path,
    output_path:Path,
    allowed_prefixes:dict[str,str],
)->Path:

    metrics=_read_metrics_json(metrics_json_path)
    generated_at=datetime.now(timezone.utc).isoformat()

    fields=[
        "figure_id",
        "run_id",
        "sample_id",
        "assay_type",
        "run_classification",
        "stage_id",
        "stage_name",
        "semantic_domain",
        "metric_name",
        "metric_value",
        "metric_category",
        "source_artifact",
        "source_column_or_rule",
        "generated_at",
    ]

    rows=[]

    for metric in metrics:

        metric_name=metric.get("metric_name","")
        matched_domain=None

        for semantic_domain,prefix in allowed_prefixes.items():
            if metric_name.startswith(prefix):
                matched_domain=semantic_domain
                break

        if matched_domain is None:
            continue

        rows.append({
            "figure_id":figure_id,
            "run_id":metric.get("run_id","unknown"),
            "sample_id":metric.get("sample_id","unknown"),
            "assay_type":metric.get("assay_type","unknown"),
            "run_classification":metric.get("run_classification","unknown"),
            "stage_id":metric.get("stage_id","unknown"),
            "stage_name":metric.get("stage_name","unknown"),
            "semantic_domain":matched_domain,
            "metric_name":metric_name,
            "metric_value":metric.get("metric_value","0"),
            "metric_category":metric.get("metric_category","unknown"),
            "source_artifact":str(metrics_json_path),
            "source_column_or_rule":"metric_name prefix projection",
            "generated_at":generated_at,
        })

    output_path=Path(output_path)
    output_path.parent.mkdir(parents=True,exist_ok=True)

    with output_path.open("w",encoding="utf-8",newline="") as handle:
        writer=csv.DictWriter(
            handle,
            fieldnames=fields,
            delimiter="\t",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)

    return output_path

def build_f4a_coding_semantic_composition_table(
    metrics_json_path:Path,
    output_path:Path,
)->Path:

    allowed_prefixes={
        "consequence":"consequence_distribution__",
        "clinvar_significance":"clinvar_significance_distribution__",
        "population_frequency_bin":"population_frequency_bin__",
    }

    return _build_f4_semantic_composition_table(
        figure_id="F4A",
        metrics_json_path=metrics_json_path,
        output_path=output_path,
        allowed_prefixes=allowed_prefixes,
    )

def build_f4b_noncoding_semantic_composition_table(
    metrics_json_path:Path,
    output_path:Path,
)->Path:

    allowed_prefixes={
        "consequence":"consequence_distribution__",
        "clinvar_significance":"clinvar_significance_distribution__",
        "population_frequency_bin":"population_frequency_bin__",
    }

    return _build_f4_semantic_composition_table(
        figure_id="F4B",
        metrics_json_path=metrics_json_path,
        output_path=output_path,
        allowed_prefixes=allowed_prefixes,
    )

def _metric_suffix(metric_name:str,prefix:str)->str:
    if not metric_name.startswith(prefix):
        return metric_name
    return metric_name[len(prefix):]

def collapse_clinvar_significance(metric_name:str)->tuple[str,str]:
    label=_metric_suffix(metric_name,"clinvar_significance_distribution__")
    tokens=set(label.split("&"))

    benign_like={"benign","likely_benign","benign_likely_benign"}
    pathogenic_like={"pathogenic","likely_pathogenic"}

    if "conflicting_classifications_of_pathogenicity" in tokens:
        return "conflicting_classifications","explicit_conflicting_classifications_of_pathogenicity"

    if tokens & benign_like and tokens & pathogenic_like:
        return "conflicting_classifications","benign_and_pathogenic_polarity_conflict"

    if "pathogenic" in tokens:
        return "pathogenic","pathogenic_without_benign_conflict"

    if "likely_pathogenic" in tokens:
        return "likely_pathogenic","likely_pathogenic_without_benign_conflict"

    if "uncertain_significance" in tokens:
        return "uncertain_significance","uncertain_significance_without_escalation"

    if {"benign_likely_benign","likely_benign"} & tokens:
        return "likely_benign","likely_benign_or_benign_likely_benign"

    if "benign" in tokens:
        return "benign","benign_with_nonpathogenic_modifiers_only"

    return "uncertain_significance","non_acmg_or_uninformative_terms"

def collapse_coding_consequence(metric_name:str)->tuple[str,str]:
    label=_metric_suffix(metric_name,"consequence_distribution__")
    tokens=set(label.split("&"))

    splice_terms={
        "splice_acceptor_variant",
        "splice_donor_variant",
        "splice_region_variant",
        "splice_donor_5th_base_variant",
        "splice_polypyrimidine_tract_variant",
    }

    if tokens & splice_terms:
        return "splice_affected","coding_consequence_splice_precedence"
    if "stop_gained" in tokens:
        return "stop_gained","coding_consequence_stop_gained"
    if "frameshift_variant" in tokens:
        return "frameshift","coding_consequence_frameshift"
    if "start_lost" in tokens:
        return "start_lost","coding_consequence_start_lost"
    if "stop_lost" in tokens:
        return "stop_lost","coding_consequence_stop_lost"
    if {"missense_variant","protein_altering_variant"} & tokens:
        return "missense_or_protein_altering","coding_consequence_missense_or_protein_altering"
    if {"inframe_deletion","inframe_insertion"} & tokens:
        return "inframe_indel","coding_consequence_inframe_indel"
    if {"synonymous_variant","stop_retained_variant","start_retained_variant"} & tokens:
        return "synonymous_or_retained","coding_consequence_synonymous_or_retained"

    return "other_coding_consequence","coding_consequence_other"

def collapse_noncoding_consequence(metric_name:str)->tuple[str,str]:
    label=_metric_suffix(metric_name,"consequence_distribution__")
    tokens=set(label.split("&"))

    if any(t.startswith("splice_") for t in tokens):
        return "splice_affected","noncoding_consequence_splice_precedence"
    if "mature_miRNA_variant" in tokens:
        return "mature_miRNA","noncoding_consequence_mature_miRNA"
    if {"3_prime_UTR_variant","5_prime_UTR_variant"} & tokens:
        return "UTR","noncoding_consequence_UTR"
    if {"non_coding_transcript_exon_variant","non_coding_transcript_variant"} & tokens:
        return "noncoding_transcript","noncoding_consequence_transcript"
    if "intron_variant" in tokens:
        return "intronic","noncoding_consequence_intronic"
    if {"upstream_gene_variant","downstream_gene_variant"} & tokens:
        return "flanking_gene_region","noncoding_consequence_flanking_gene_region"
    if "intergenic_variant" in tokens:
        return "intergenic","noncoding_consequence_intergenic"
    if {"coding_sequence_variant","incomplete_terminal_codon_variant","stop_retained_variant"} & tokens:
        return "coding_or_retained_residual","noncoding_consequence_coding_or_retained_residual"

    return "other_noncoding_consequence","noncoding_consequence_other"

def collapse_population_frequency_bin(metric_name:str)->tuple[str,str]:
    label=_metric_suffix(metric_name,"population_frequency_bin__")
    allowed={"rare","low_frequency","common","missing"}
    if label in allowed:
        return label,"population_frequency_bin_passthrough"
    return "missing","population_frequency_bin_unrecognized_as_missing"

def _collapse_f4_row(row:dict[str,str],consequence_mode:str)->tuple[str,str]:
    domain=row["semantic_domain"]
    metric_name=row["metric_name"]

    if domain=="clinvar_significance":
        return collapse_clinvar_significance(metric_name)
    if domain=="population_frequency_bin":
        return collapse_population_frequency_bin(metric_name)
    if domain=="consequence" and consequence_mode=="coding":
        return collapse_coding_consequence(metric_name)
    if domain=="consequence" and consequence_mode=="noncoding":
        return collapse_noncoding_consequence(metric_name)

    raise ValueError(f"Unsupported F4 collapse domain/mode: {domain}/{consequence_mode}")

def _build_f4_semantic_composition_collapsed_table(
    *,
    input_path:Path,
    output_path:Path,
    consequence_mode:str,
)->Path:

    input_path=Path(input_path)
    output_path=Path(output_path)

    if not input_path.exists():
        raise FileNotFoundError(f"F4 semantic composition TSV not found: {input_path}")

    with input_path.open("r",encoding="utf-8",newline="") as handle:
        rows=list(csv.DictReader(handle,delimiter="\t"))

    grouped:dict[tuple[str,str,str],dict[str,Any]]={}
    generated_at=datetime.now(timezone.utc).isoformat()

    for row in rows:
        collapsed_label,collapse_rule=_collapse_f4_row(row,consequence_mode)
        key=(row["figure_id"],row["semantic_domain"],collapsed_label)

        if key not in grouped:
            grouped[key]={
                "figure_id":row["figure_id"],
                "run_id":row.get("run_id","unknown"),
                "sample_id":row.get("sample_id","unknown"),
                "assay_type":row.get("assay_type","unknown"),
                "run_classification":row.get("run_classification","unknown"),
                "stage_id":row.get("stage_id","unknown"),
                "stage_name":row.get("stage_name","unknown"),
                "semantic_domain":row["semantic_domain"],
                "collapsed_label":collapsed_label,
                "collapsed_metric_value":0,
                "collapse_rules":set(),
                "source_metric_names":[],
                "source_artifact":str(input_path),
                "generated_at":generated_at,
            }

        grouped[key]["collapsed_metric_value"]+=int(float(row["metric_value"]))
        grouped[key]["collapse_rules"].add(collapse_rule)
        grouped[key]["source_metric_names"].append(row["metric_name"])

    fields=[
        "figure_id",
        "run_id",
        "sample_id",
        "assay_type",
        "run_classification",
        "stage_id",
        "stage_name",
        "semantic_domain",
        "collapsed_label",
        "collapsed_metric_value",
        "collapse_rules",
        "source_metric_count",
        "source_metric_names",
        "source_artifact",
        "generated_at",
    ]

    output_path.parent.mkdir(parents=True,exist_ok=True)

    with output_path.open("w",encoding="utf-8",newline="") as handle:
        writer=csv.DictWriter(handle,fieldnames=fields,delimiter="\t",lineterminator="\n")
        writer.writeheader()

        for item in grouped.values():
            item["collapse_rules"]=";".join(sorted(item["collapse_rules"]))
            item["source_metric_count"]=len(item["source_metric_names"])
            item["source_metric_names"]=";".join(sorted(item["source_metric_names"]))
            writer.writerow(item)

    return output_path

def build_f4a_coding_semantic_composition_collapsed_table(
    input_path:Path,
    output_path:Path,
)->Path:
    return _build_f4_semantic_composition_collapsed_table(
        input_path=input_path,
        output_path=output_path,
        consequence_mode="coding",
    )

def build_f4b_noncoding_semantic_composition_collapsed_table(
    input_path:Path,
    output_path:Path,
)->Path:
    return _build_f4_semantic_composition_collapsed_table(
        input_path=input_path,
        output_path=output_path,
        consequence_mode="noncoding",
    )

