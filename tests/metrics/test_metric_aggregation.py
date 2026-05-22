from pathlib import Path

from src.metrics.metric_aggregation import build_f3a_flow_table


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