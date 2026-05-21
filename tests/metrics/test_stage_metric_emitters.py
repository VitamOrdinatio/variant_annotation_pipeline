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