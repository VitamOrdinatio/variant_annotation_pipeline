from pathlib import Path
import logging
import json

from src.metrics.stage_metric_emitters import emit_metrics_for_stage

def test_stage_05_06_07_sidecar_metric_emitters(tmp_path):
    run_dir=tmp_path/"run_test"
    interim=run_dir/"interim"
    processed=run_dir/"processed"
    metrics=run_dir/"metrics"
    for path in [interim,processed,metrics]:
        path.mkdir(parents=True,exist_ok=True)

    raw=interim/"sample_run.raw_variants.vcf"
    norm=interim/"sample_run.normalized_variants.vcf"
    ann_vcf=processed/"sample_run.annotated_variants.vcf"
    ann_tsv=processed/"sample_run.annotated_variants.tsv"

    vcf_text="##fileformat=VCFv4.2\n#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n1\t10\t.\tA\tG\t.\tPASS\t.\n1\t20\t.\tC\tT\t.\tPASS\t.\n"
    raw.write_text(vcf_text)
    norm.write_text(vcf_text)
    ann_vcf.write_text(vcf_text)
    ann_tsv.write_text("variant_id\tgene\n1:10:A:G\tGENE1\n1:20:C:T\tGENE2\n")

    paths={"run_dir":str(run_dir),"metrics_dir":str(metrics)}
    state={
        "run":{"run_id":"run_test","execution_mode":"fixture"},
        "sample":{"sample_id":"sample","assay_type":"WES"},
        "artifacts":{
            "raw_vcf":str(raw),
            "normalized_vcf":str(norm),
            "annotated_vcf":str(ann_vcf),
            "annotated_table":str(ann_tsv),
        },
    }

    logger=logging.getLogger("metric_smoke_test")
    logger.handlers.clear()
    logger.addHandler(logging.NullHandler())

    for stage in ["stage_05_call_variants","stage_06_normalize_vcf","stage_07_annotate_variants"]:
        emit_metrics_for_stage(stage,{},paths,state,logger)

    assert (metrics/"stage_05_variant_calling_metrics.json").exists()
    assert (metrics/"stage_06_normalization_metrics.json").exists()
    assert (metrics/"stage_07_annotation_metrics.json").exists()
    assert (metrics/"stage_metrics_long.tsv").exists()

    lines=(metrics/"stage_metrics_long.tsv").read_text().strip().splitlines()
    assert len(lines)==5
    assert "raw_called_variants" in lines[1]
    assert "normalized_variants" in lines[2]
    assert "annotated_variants_vcf" in lines[3]
    assert "annotated_variants_tsv" in lines[4]

def test_stage_08_sidecar_metric_emitter(tmp_path):
    run_dir=tmp_path/"run_test"
    processed=run_dir/"processed"
    metrics=run_dir/"metrics"
    for path in [processed,metrics]:
        path.mkdir(parents=True,exist_ok=True)

    summary=processed/"stage_08_summary.json"
    summary.write_text(json.dumps({
        "total_variants":6,
        "irreparably_malformed_rows":0,
        "variant_summary_rows":6,
        "rdgp_gene_evidence_seed_rows":3,
        "partition_counts":{
            "coding_candidates":2,
            "splice_region_candidates":1,
            "noncoding_candidates":3,
            "qc_flagged":1
        },
        "variants_by_context":{
            "coding":2,
            "splice_region":1,
            "intronic":2,
            "intergenic":1
        },
        "variants_by_severity":{
            "HIGH":1,
            "MODERATE":2,
            "MODIFIER":3
        },
        "qc_status_counts":{
            "pass":5,
            "caution":1
        },
        "interpretability_counts":{
            "interpretable_now":3,
            "needs_external_annotation":3
        },
        "frequency_status":{
            "rare":4,
            "missing":2
        },
        "clinical_status":{
            "missing":5,
            "pathogenic":1
        },
        "variants_by_variant_type":{
            "snv":5,
            "deletion":1
        },
        "variants_by_variant_class":{
            "coding":3,
            "noncoding":3
        }
    }),encoding="utf-8")

    tsvs={
        "stage_08_selected_transcript_consequences":"stage_08_selected_transcript_consequences.tsv",
        "stage_08_vdb_ready_variants":"stage_08_vdb_ready_variants.tsv",
        "coding_candidates":"coding_candidates.tsv",
        "splice_region_candidates":"splice_region_candidates.tsv",
        "noncoding_candidates":"noncoding_candidates.tsv",
        "qc_flagged":"qc_flagged.tsv",
        "stage_08_rdgp_gene_evidence_seed":"stage_08_rdgp_gene_evidence_seed.tsv",
    }

    for key,name in tsvs.items():
        path=processed/name
        path.write_text("variant_id\tgene_id\nv1\tg1\nv2\tg2\n",encoding="utf-8")

    paths={"run_dir":str(run_dir),"metrics_dir":str(metrics)}
    state={
        "run":{"run_id":"run_test","execution_mode":"fixture"},
        "sample":{"sample_id":"sample","assay_type":"WES"},
        "artifacts":{
            "stage_08_summary_json":str(summary),
            **{key:str(processed/name) for key,name in tsvs.items()},
        },
    }

    logger=logging.getLogger("metric_stage08_test")
    logger.handlers.clear()
    logger.addHandler(logging.NullHandler())

    emit_metrics_for_stage("stage_08_filter_and_partition",{},paths,state,logger)

    assert (metrics/"stage_08_partition_metrics.json").exists()
    assert (metrics/"stage_metrics_long.tsv").exists()

    long_text=(metrics/"stage_metrics_long.tsv").read_text(encoding="utf-8")
    assert "partitioned_variants_total" in long_text
    assert "coding_candidates" in long_text
    assert "variants_by_context__coding" in long_text
    assert "rdgp_gene_evidence_seed_rows" in long_text

def test_stage_11_sidecar_metric_emitter(tmp_path):
    run_dir=tmp_path/"run_test"
    processed=run_dir/"processed"
    metrics=run_dir/"metrics"
    for path in [processed,metrics]:
        path.mkdir(parents=True,exist_ok=True)

    summary=processed/"stage_11_summary.json"
    summary.write_text(json.dumps({
        "input_rows":5,
        "output_rows":5,
        "unassigned_or_malformed_rows":0,
        "high_priority_candidate_count":1,
        "moderate_priority_candidate_count":2,
        "low_priority_candidate_count":1,
        "uninterpretable_count":1,
        "gene_id_count_unique":3,
        "counts_by_priority_tier":{
            "tier_1_high_confidence_candidate":1,
            "tier_2_moderate_candidate":2,
            "tier_3_low_support_or_common":1,
            "tier_4_uninterpretable_or_qc_limited":1
        },
        "counts_by_priority_rank":{
            "1":1,
            "2":2,
            "3":1,
            "4":1
        },
        "counts_by_variant_origin":{
            "coding":3,
            "noncoding":2
        },
        "counts_by_source_interpretation_label":{
            "lof_rare_clinically_supported":1,
            "lof_or_missense_rare":2,
            "noncoding_common_or_low_support":1,
            "noncoding_uninterpretable":1
        }
    }),encoding="utf-8")

    prioritized=processed/"stage_11_prioritized_variants.tsv"
    prioritized.write_text(
        "variant_id\tgene_id\tpriority_tier\n"
        "v1\tg1\ttier_1_high_confidence_candidate\n"
        "v2\tg2\ttier_2_moderate_candidate\n",
        encoding="utf-8",
    )

    gene_counts=processed/"stage_11_gene_variant_counts.tsv"
    gene_counts.write_text(
        "gene_id\tvariant_count\n"
        "g1\t1\n"
        "g2\t1\n",
        encoding="utf-8",
    )

    paths={"run_dir":str(run_dir),"metrics_dir":str(metrics)}
    state={
        "run":{"run_id":"run_test","execution_mode":"fixture"},
        "sample":{"sample_id":"sample","assay_type":"WES"},
        "artifacts":{
            "stage_11_summary_json":str(summary),
            "stage_11_prioritized_variants":str(prioritized),
            "stage_11_gene_variant_counts":str(gene_counts),
        },
    }

    logger=logging.getLogger("metric_stage11_test")
    logger.handlers.clear()
    logger.addHandler(logging.NullHandler())

    emit_metrics_for_stage("stage_11_prioritize_variants",{},paths,state,logger)

    assert (metrics/"stage_11_prioritization_metrics.json").exists()
    long_text=(metrics/"stage_metrics_long.tsv").read_text(encoding="utf-8")
    assert "high_priority_candidate_count" in long_text
    assert "counts_by_priority_tier__tier_1_high_confidence_candidate" in long_text
    assert "counts_by_variant_origin__coding" in long_text
    assert "prioritized_variants_rows" in long_text
    assert "gene_variant_counts_rows" in long_text

def test_stage_12_sidecar_metric_emitter(tmp_path):
    run_dir=tmp_path/"run_test"
    processed=run_dir/"processed"
    metrics=run_dir/"metrics"
    for path in [processed,metrics]:
        path.mkdir(parents=True,exist_ok=True)

    summary=processed/"stage_12_summary.json"
    summary.write_text(json.dumps({
        "input_rows":5,
        "output_rows":5,
        "unrecognized_priority_rows":0,
        "counts_by_validation_required":{
            "True":3,
            "False":2
        },
        "counts_by_validation_priority":{
            "high":1,
            "medium":2,
            "low":2
        },
        "counts_by_suggested_validation_method":{
            "IGV":3,
            "none":2
        },
        "counts_by_priority_tier":{
            "tier_1_high_confidence_candidate":1,
            "tier_2_moderate_candidate":2,
            "tier_3_low_support_or_common":1,
            "tier_4_uninterpretable_or_qc_limited":1
        }
    }),encoding="utf-8")

    validation=processed/"stage_12_validation_candidates.tsv"
    validation.write_text(
        "variant_id\tgene_id\tvalidation_required\n"
        "v1\tg1\tTrue\n"
        "v2\tg2\tTrue\n",
        encoding="utf-8",
    )

    paths={"run_dir":str(run_dir),"metrics_dir":str(metrics)}
    state={
        "run":{"run_id":"run_test","execution_mode":"fixture"},
        "sample":{"sample_id":"sample","assay_type":"WES"},
        "artifacts":{
            "stage_12_summary_json":str(summary),
            "stage_12_validation_candidates":str(validation),
        },
    }

    logger=logging.getLogger("metric_stage12_test")
    logger.handlers.clear()
    logger.addHandler(logging.NullHandler())

    emit_metrics_for_stage("stage_12_validate_variants",{},paths,state,logger)

    assert (metrics/"stage_12_validation_metrics.json").exists()
    long_text=(metrics/"stage_metrics_long.tsv").read_text(encoding="utf-8")
    assert "counts_by_validation_required__True" in long_text
    assert "counts_by_validation_priority__high" in long_text
    assert "counts_by_suggested_validation_method__IGV" in long_text
    assert "validation_candidates_rows" in long_text

