import csv
import pytest

from pathlib import Path

from src.metrics.metric_aggregation import (
    build_f3a_flow_table,
    build_f3a_flow_table_v2,
    build_f3b_semantic_branching_table,
)


def test_build_f3a_flow_table(tmp_path):
    metrics_dir=tmp_path/"metrics"
    metrics_dir.mkdir(parents=True,exist_ok=True)

    metrics_long=metrics_dir/"stage_metrics_long.tsv"
    metrics_long.write_text(
        "metric_name\tmetric_value\tmetric_unit\tmetric_status\tmetric_category\tstage_id\tstage_name\tsample_id\trun_id\tassay_type\trun_classification\tsource_artifact\tsource_column_or_rule\tderivation_rule\tgenerated_at\tintended_figure_support\n"
        "raw_called_variants\t100\tvariants\tavailable\tf3\tstage_05\tcall_variants\tsample\trun\tWES\tfixture\ta\tb\tc\td\tF3A\n"
        "normalized_variants\t95\tvariants\tavailable\tf3\tstage_06\tnormalize_vcf\tsample\trun\tWES\tfixture\ta\tb\tc\td\tF3A\n"
        "annotated_variants_tsv\t95\trows\tavailable\tf3\tstage_07\tannotate_variants\tsample\trun\tWES\tfixture\ta\tb\tc\td\tF3A\n"
        "partitioned_variants_total\t95\tvariants\tavailable\tf3\tstage_08\tfilter_and_partition\tsample\trun\tWES\tfixture\ta\tb\tc\td\tF3A\n"
        "coding_candidates\t10\trows\tavailable\tf3\tstage_08\tfilter_and_partition\tsample\trun\tWES\tfixture\ta\tb\tc\td\tF3B\n"
        "splice_region_candidates\t5\trows\tavailable\tf3\tstage_08\tfilter_and_partition\tsample\trun\tWES\tfixture\ta\tb\tc\td\tF3B\n"
        "noncoding_candidates\t80\trows\tavailable\tf3\tstage_08\tfilter_and_partition\tsample\trun\tWES\tfixture\ta\tb\tc\td\tF3B\n"
        "qc_flagged\t2\trows\tavailable\tf3\tstage_08\tfilter_and_partition\tsample\trun\tWES\tfixture\ta\tb\tc\td\tF4\n"
        "coding_interpreted_rows\t15\trows\tavailable\tf3\tstage_09\tinterpret_coding\tsample\trun\tWES\tfixture\ta\tb\tc\td\tF3B\n"
        "noncoding_interpreted_rows\t80\trows\tavailable\tf3\tstage_10\tinterpret_noncoding\tsample\trun\tWES\tfixture\ta\tb\tc\td\tF3B\n"
        "prioritized_variants_rows\t95\trows\tavailable\tf3\tstage_11\tprioritize_variants\tsample\trun\tWES\tfixture\ta\tb\tc\td\tF3B\n"
        "validation_candidates_rows\t95\trows\tavailable\tf3\tstage_12\tvalidate_variants\tsample\trun\tWES\tfixture\ta\tb\tc\td\tF3B\n",
        encoding="utf-8",
    )

    out=metrics_dir/"figure_f3a_flow.tsv"
    build_f3a_flow_table(metrics_long,out)

    assert out.exists()

    text=out.read_text(encoding="utf-8")
    assert "raw_to_normalized" in text
    assert "partitioned_to_coding" in text
    assert "prioritized_to_validation" in text
    assert "min(source_value,target_value)" in text

def _write_metrics_long(path:Path, rows:list[tuple[str,int,str]]) -> None:
    header="metric_name\tmetric_value\tmetric_unit\tmetric_status\tmetric_category\tstage_id\tstage_name\tsample_id\trun_id\tassay_type\trun_classification\tsource_artifact\tsource_column_or_rule\tderivation_rule\tgenerated_at\tintended_figure_support\n"
    body=[]
    for metric_name,metric_value,stage_id in rows:
        body.append(f"{metric_name}\t{metric_value}\tcount\tavailable\tf3\t{stage_id}\tfixture_stage\tsample\trun\tWES\tfixture\ta\tb\tc\td\tF3\n")
    path.write_text(header+"".join(body),encoding="utf-8")

def _read_tsv(path:Path) -> list[dict[str,str]]:
    with path.open("r",encoding="utf-8",newline="") as handle:
        return list(csv.DictReader(handle,delimiter="\t"))

def test_build_f3a_flow_table_v2_wes_complete_categories_preserves_values(tmp_path):
    metrics_long=tmp_path/"stage_metrics_long.tsv"
    _write_metrics_long(metrics_long,[
        ("raw_called_variants",1000,"stage_05"),
        ("annotated_variants_tsv",900,"stage_07"),
        ("counts_by_source_interpretation_label__lof_rare_clinically_supported",5,"stage_11"),
        ("counts_by_source_interpretation_label__lof_or_missense_rare",20,"stage_11"),
        ("counts_by_source_interpretation_label__regulatory_or_transcript_rare",30,"stage_11"),
        ("high_priority_candidate_count",7,"stage_11"),
        ("moderate_priority_candidate_count",11,"stage_11"),
        ("counts_by_validation_required__True",13,"stage_12"),
    ])
    out=tmp_path/"figure_f3a_flow_v2.tsv"
    build_f3a_flow_table_v2(metrics_long,out)
    rows=_read_tsv(out)
    assert len(rows)==4
    assert rows[1]["target_label"]=="Rare interpretable evidence"
    assert int(rows[1]["edge_metric_value"])==55
    assert rows[2]["target_label"]=="Prioritized candidates"
    assert int(rows[2]["edge_metric_value"])==18
    assert rows[3]["target_label"]=="Validation-ready evidence"
    assert int(rows[3]["edge_metric_value"])==13

def test_build_f3a_flow_table_v2_missing_optional_category_zero_fills(tmp_path):
    metrics_long=tmp_path/"stage_metrics_long.tsv"
    _write_metrics_long(metrics_long,[
        ("raw_called_variants",1000,"stage_05"),
        ("annotated_variants_tsv",900,"stage_07"),
        ("counts_by_source_interpretation_label__lof_or_missense_rare",20,"stage_11"),
        ("counts_by_source_interpretation_label__regulatory_or_transcript_rare",30,"stage_11"),
        ("high_priority_candidate_count",7,"stage_11"),
        ("moderate_priority_candidate_count",11,"stage_11"),
        ("counts_by_validation_required__True",13,"stage_12"),
    ])
    out=tmp_path/"figure_f3a_flow_v2.tsv"
    build_f3a_flow_table_v2(metrics_long,out)
    rows=_read_tsv(out)
    assert rows[1]["target_label"]=="Rare interpretable evidence"
    assert int(rows[1]["edge_metric_value"])==50

def test_build_f3a_flow_table_v2_missing_required_backbone_metric_fails(tmp_path):
    metrics_long=tmp_path/"stage_metrics_long.tsv"
    _write_metrics_long(metrics_long,[
        ("annotated_variants_tsv",900,"stage_07"),
        ("counts_by_source_interpretation_label__lof_or_missense_rare",20,"stage_11"),
        ("counts_by_source_interpretation_label__regulatory_or_transcript_rare",30,"stage_11"),
        ("counts_by_source_interpretation_label__lof_rare_clinically_supported",5,"stage_11"),
        ("high_priority_candidate_count",7,"stage_11"),
        ("moderate_priority_candidate_count",11,"stage_11"),
        ("counts_by_validation_required__True",13,"stage_12"),
    ])
    out=tmp_path/"figure_f3a_flow_v2.tsv"
    with pytest.raises(KeyError):
        build_f3a_flow_table_v2(metrics_long,out)

def test_build_f3b_semantic_branching_missing_optional_branch_zero_fills(tmp_path):
    metrics_long=tmp_path/"stage_metrics_long.tsv"
    _write_metrics_long(metrics_long,[
        ("counts_by_source_interpretation_label__lof_or_missense_rare",20,"stage_11"),
        ("counts_by_source_interpretation_label__regulatory_or_transcript_rare",30,"stage_11"),
        ("counts_by_source_interpretation_label__coding_common_or_low_support",40,"stage_11"),
        ("counts_by_source_interpretation_label__noncoding_common_or_low_support",50,"stage_11"),
        ("counts_by_source_interpretation_label__coding_uninterpretable",60,"stage_11"),
    ])
    out=tmp_path/"figure_f3b_semantic_branching.tsv"
    build_f3b_semantic_branching_table(metrics_long,out)
    rows=_read_tsv(out)
    assert len(rows)==6
    missing_branch=[r for r in rows if r["branch_id"]=="noncoding_uninterpretable"][0]
    assert int(missing_branch["metric_value"])==0