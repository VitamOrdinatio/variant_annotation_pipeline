from pathlib import Path
import logging
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