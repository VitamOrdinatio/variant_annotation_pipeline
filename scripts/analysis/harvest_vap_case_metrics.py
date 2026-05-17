#!/usr/bin/env python3
from pathlib import Path
import csv,json
RUN_DIRS=[Path("results/run_2026_04_17_082417"),Path("results/run_2026_05_13_060859"),Path("results/run_2026_05_14_083044"),Path("results/run_2026_05_14_231247"),Path("results/run_2026_05_14_164444"),Path("results/run_2026_05_15_063040")]
OUTDIR=Path("docs/case_studies/tables")
RUN_ANNOTATIONS = {
    "run_2026_04_17_082417": {
        "run_classification": "legacy_semitelemetry_checkpoint_run",
        "assay_metadata_status": "pre_assay_metadata_contract",
        "notes": "HG002 legacy MARK execution: stages 01-06 ran as an early continuous pipeline, while stages 07-13 were progressively checkpoint-completed during VAP development after VEP environment repair. Git/config provenance spans multiple commits/config states.",
        "status_override": "checkpoint_completed",
        "git_commit_override": "multiple_commits_checkpoint_development",
        "config_hash_override": "multiple_configs_checkpoint_development",
        "reference_fasta_hash_or_size_override": 3151425851,
        "execution_profile_override": "full_pipeline_plus_checkpoint_recovery"
    },
    "run_2026_05_13_060859": {
        "run_classification": "hg002_full_telemetry",
        "assay_metadata_status": "pre_assay_metadata_contract",
        "notes": "HG002 telemetry-enabled rerun before explicit WGS/WES assay-type semantic enforcement."
    },
    "run_2026_05_14_083044": {
        "run_classification": "saudi_metadata_drift_detection",
        "assay_metadata_status": "incorrect_wgs_label_for_wes",
        "notes": "Saudi WES run with full telemetry that exposed assay-type metadata drift."
    },
    "run_2026_05_14_231247": {
        "run_classification": "saudi_metadata_patch_rerun",
        "assay_metadata_status": "corrected_wes_label",
        "notes": "Saudi WES rerun after assay-aware provenance patch."
    },
    "run_2026_05_14_164444": {
        "run_classification": "saudi_same_patch_baseline",
        "assay_metadata_status": "corrected_wes_label",
        "notes": "First corrected ERR10619300 post-patch run."
    },
    "run_2026_05_15_063040": {
        "run_classification": "saudi_same_patch_rerun",
        "assay_metadata_status": "corrected_wes_label",
        "notes": "Same-patch ERR10619300 reproducibility rerun."
    },
}
def project_rows(rows,keys):
    return sorted([{k:r[k] for k in keys} for r in rows],key=lambda r:tuple(r[k] for k in keys))
def rows_for_run(rows,run_id):
    return [r for r in rows if r["run_id"]==run_id]
def load_gene_burden(path):
    rows=[]
    if not path.exists():return rows
    with open(path,newline="") as fh:
        reader=csv.DictReader(fh,delimiter="\t")
        for i,row in enumerate(reader,start=1):
            gene_id=row.get("gene_id","NA")
            variant_count=int(row.get("variant_count",0))
            rows.append({"gene_burden_rank":i,"gene_id":gene_id,"gene_id_status":"unresolved_gene_id" if gene_id=="NA" else "resolved_gene_id","variant_count":variant_count})
    return rows
def run_base(rd):
    legacy_base=rd/"raw_mark_outputs"
    return legacy_base if legacy_base.exists() else rd
def load_json(p):
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}
def write_tsv(path,fields,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields,delimiter="\t",extrasaction="ignore",lineterminator="\n")
        w.writeheader()
        for r in rows:w.writerow({k:r.get(k,"NA") for k in fields})
def read_runtime_profile(p,run_id,sample_id):
    if not p.exists():return []
    rows=[]
    with p.open(encoding="utf-8",newline="") as f:
        for r in csv.DictReader(f,delimiter="\t"):
            r["run_id"]=run_id;r["sample_id"]=sample_id;rows.append(r)
    return rows
def n(d,*keys,default="NA"):
    x=d
    for k in keys:
        if not isinstance(x,dict) or k not in x:return default
        x=x[k]
    return x
def main():
    OUTDIR.mkdir(parents=True,exist_ok=True)
    funnel=[];runtime=[];priority=[];validation=[];prov=[];interpretation=[];gene_burden=[]
    repro=[]
    for rd in RUN_DIRS:
        base=run_base(rd)
        meta=load_json(base/"metadata/run_metadata.json")
        legacy=load_json(base/"metadata.json")
        fp=load_json(base/"metadata/run_fingerprint.json")
        s8=load_json(base/"processed/stage_08_summary.json")
        s9=load_json(base/"processed/stage_09_summary.json")
        s10=load_json(base/"processed/stage_10_summary.json")
        s11=load_json(base/"processed/stage_11_summary.json")
        s12=load_json(base/"processed/stage_12_summary.json")
        s13=load_json(base/"processed/stage_13_final_summary.json")
        run_id=n(meta,"run","run_id",default=rd.name)
        sample_id=n(legacy,"sample","sample_id",default=s13.get("sample_id","NA"))
        assay=n(legacy,"sample","assay_type",default="NA")
        ann=RUN_ANNOTATIONS.get(run_id,{})
        run_classification=ann.get("run_classification","unclassified")
        assay_metadata_status=ann.get("assay_metadata_status","unknown")
        run_notes=ann.get("notes","")
        status_override=ann.get("status_override")
        git_commit_override=ann.get("git_commit_override")
        config_hash_override=ann.get("config_hash_override")
        reference_fasta_hash_or_size_override=ann.get("reference_fasta_hash_or_size_override")
        execution_profile_override=ann.get("execution_profile_override")                
        # Interpretations by source_interpretation_label and variant_origin are harvested from the final summary to capture the most complete and up-to-date interpretation counts, which may be updated in the final summary after stage 12 based on the most recent interpretation logic and any late-breaking fixes.
        for label,count in sorted(s13.get("counts_by_source_interpretation_label",{}).items()):
            interpretation.append({"sample_id":sample_id,"run_id":run_id,"assay_type":assay,"run_classification":run_classification,"summary_axis":"source_interpretation_label","interpretation_label":label,"count":count})
        for origin,count in sorted(s13.get("counts_by_variant_origin",{}).items()):
            interpretation.append({"sample_id":sample_id,"run_id":run_id,"assay_type":assay,"run_classification":run_classification,"summary_axis":"variant_origin","interpretation_label":origin,"count":count})
        gene_burden_path=base/"processed/stage_11_gene_variant_counts.tsv"
        for row in load_gene_burden(gene_burden_path):
            gene_burden.append({"sample_id":sample_id,"run_id":run_id,"assay_type":assay,"run_classification":run_classification,"gene_burden_rank":row["gene_burden_rank"],"gene_id":row["gene_id"],"gene_id_status":row["gene_id_status"],"variant_count":row["variant_count"]})        
        runtime+=read_runtime_profile(base/"metadata/runtime_profile.tsv",run_id,sample_id)
        funnel.append({"sample_id":sample_id,"run_id":run_id,"assay_type":assay,"run_classification":run_classification,"assay_metadata_status":assay_metadata_status,"run_notes":run_notes,"raw_variant_count":n(legacy,"qc","variant_calling_qc","variant_count"),"normalized_variant_count":n(legacy,"qc","normalization_qc","normalized_variant_count"),"annotated_variant_count":n(legacy,"qc","annotation_qc","annotated_variant_count",default=s13.get("total_variants_processed",s8.get("total_variants","NA"))),"stage08_total_variants":s8.get("total_variants","NA"),"coding_candidates":n(s8,"partition_counts","coding_candidates"),"noncoding_candidates":n(s8,"partition_counts","noncoding_candidates"),"splice_region_candidates":n(s8,"partition_counts","splice_region_candidates"),"qc_flagged":n(s8,"partition_counts","qc_flagged"),"stage09_coding_interpreted":s9.get("interpreted_rows","NA"),"stage10_noncoding_interpreted":s10.get("interpreted_rows","NA"),"stage11_prioritized_rows":s11.get("output_rows","NA"),"stage12_validation_rows":s12.get("output_rows","NA"),"rdgp_gene_evidence_seed_rows":s8.get("rdgp_gene_evidence_seed_rows","NA"),"unique_gene_ids":s11.get("gene_id_count_unique",s13.get("gene_id_count_unique","NA"))})
        for tier,count in sorted(s11.get("counts_by_priority_tier",{}).items()):
            priority.append({"sample_id":sample_id,"run_id":run_id,"priority_tier":tier,"count":count})
        for method,count in sorted(s12.get("counts_by_suggested_validation_method",{}).items()):
            validation.append({"sample_id":sample_id,"run_id":run_id,"metric":"suggested_validation_method","category":method,"count":count})
        for pr,count in sorted(s12.get("counts_by_validation_priority",{}).items()):
            validation.append({"sample_id":sample_id,"run_id":run_id,"metric":"validation_priority","category":pr,"count":count})
        for req,count in sorted(s12.get("counts_by_validation_required",{}).items()):
            validation.append({"sample_id":sample_id,"run_id":run_id,"metric":"validation_required","category":req,"count":count})
        prov.append({"sample_id":sample_id,"run_id":run_id,"assay_type":assay,"run_classification":run_classification,"assay_metadata_status":assay_metadata_status,"run_notes":run_notes,"pipeline_version":n(meta,"run","pipeline_version",default=n(legacy,"run","pipeline_version")),"status":status_override or n(meta,"run","status",default=n(legacy,"run","status")),"machine_id":n(meta,"run","machine_id",default=n(legacy,"run","machine_id")),"config_path":n(meta,"run","config_path",default=n(legacy,"run","config_path")),"git_commit":git_commit_override or fp.get("git_commit","NA"),"config_hash":config_hash_override or fp.get("config_hash","NA"),"reference_genome":fp.get("reference_genome",n(legacy,"sample","reference_genome")),"reference_fasta_hash_or_size":reference_fasta_hash_or_size_override or fp.get("reference_fasta_hash_or_size","NA"),"execution_profile":execution_profile_override or fp.get("execution_profile",n(legacy,"run","execution_mode"))})
    comparisons=[
        {"comparison_id":"HG002_developmental_epoch","sample_id":"HG002","run_id_a":"run_2026_04_17_082417","run_id_b":"run_2026_05_13_060859","comparison_type":"developmental_epoch_transition","assay_transition":"WGS→WGS","notes":"Checkpoint-era developmental run compared against telemetry-era stabilized run."},
        {"comparison_id":"ERR10619281_metadata_transition","sample_id":"ERR10619281","run_id_a":"run_2026_05_14_083044","run_id_b":"run_2026_05_14_231247","comparison_type":"metadata_normalization_transition","assay_transition":"WGS→WES","notes":"Assay metadata normalization transition; biological evidence structure expected to remain stable."},
        {"comparison_id":"ERR10619300_standard_rerun","sample_id":"ERR10619300","run_id_a":"run_2026_05_14_164444","run_id_b":"run_2026_05_15_063040","comparison_type":"standard_rerun_reproducibility","assay_transition":"WES→WES","notes":"Telemetry-era rerun reproducibility assessment."}
    ]

    for c in comparisons:
        pa=project_rows(rows_for_run(priority,c["run_id_a"]),["priority_tier","count"])
        pb=project_rows(rows_for_run(priority,c["run_id_b"]),["priority_tier","count"])
        va=project_rows(rows_for_run(validation,c["run_id_a"]),["metric","category","count"])
        vb=project_rows(rows_for_run(validation,c["run_id_b"]),["metric","category","count"])

        ia=project_rows(rows_for_run(interpretation,c["run_id_a"]),["summary_axis","interpretation_label","count"])
        ib=project_rows(rows_for_run(interpretation,c["run_id_b"]),["summary_axis","interpretation_label","count"])

        ga=project_rows(rows_for_run(gene_burden,c["run_id_a"]),["gene_burden_rank","gene_id","gene_id_status","variant_count"])
        gb=project_rows(rows_for_run(gene_burden,c["run_id_b"]),["gene_burden_rank","gene_id","gene_id_status","variant_count"])

        priority_match=pa==pb
        validation_match=va==vb
        interpretation_match=ia==ib
        gene_burden_match=ga==gb

        overall="reproducible" if all([priority_match,validation_match,interpretation_match,gene_burden_match]) else "biological_divergence_detected"

        if overall=="reproducible" and c["comparison_type"]=="metadata_normalization_transition":
            overall="reproducible_with_provenance_evolution"

        repro.append({
            "comparison_id":c["comparison_id"],
            "sample_id":c["sample_id"],
            "run_id_a":c["run_id_a"],
            "run_id_b":c["run_id_b"],
            "comparison_type":c["comparison_type"],
            "assay_transition":c["assay_transition"],
            "priority_summary_match":priority_match,
            "validation_summary_match":validation_match,
            "interpretation_summary_match":interpretation_match,
            "gene_burden_match":gene_burden_match,
            "overall_reproducibility_status":overall,
            "notes":c["notes"]
        })    
    write_tsv(OUTDIR/"stage_funnel_summary.tsv",["sample_id","run_id","assay_type","run_classification","assay_metadata_status","run_notes","raw_variant_count","normalized_variant_count","annotated_variant_count","stage08_total_variants","coding_candidates","noncoding_candidates","splice_region_candidates","qc_flagged","stage09_coding_interpreted","stage10_noncoding_interpreted","stage11_prioritized_rows","stage12_validation_rows","rdgp_gene_evidence_seed_rows","unique_gene_ids"],sorted(funnel,key=lambda r:(r["sample_id"],r["run_id"])))
    write_tsv(OUTDIR/"runtime_stage_summary.tsv",["sample_id","run_id","stage","elapsed_seconds","status","start_time","end_time"],sorted(runtime,key=lambda r:(r.get("sample_id",""),r.get("run_id",""),r.get("stage",""))))
    write_tsv(OUTDIR/"priority_tier_summary.tsv",["sample_id","run_id","priority_tier","count"],sorted(priority,key=lambda r:(r["sample_id"],r["run_id"],r["priority_tier"])))
    write_tsv(OUTDIR/"candidate_reviewability_readiness.tsv",["sample_id","run_id","metric","category","count"],sorted(validation,key=lambda r:(r["sample_id"],r["run_id"],r["metric"],r["category"])))
    write_tsv(OUTDIR/"provenance_summary.tsv",["sample_id","run_id","assay_type","run_classification","assay_metadata_status","run_notes","pipeline_version","status","machine_id","config_path","git_commit","config_hash","reference_genome","reference_fasta_hash_or_size","execution_profile"],sorted(prov,key=lambda r:(r["sample_id"],r["run_id"])))
    write_tsv(OUTDIR/"interpretation_label_summary.tsv",["sample_id","run_id","assay_type","run_classification","summary_axis","interpretation_label","count"],sorted(interpretation,key=lambda r:(r["sample_id"],r["run_id"],r["summary_axis"],r["interpretation_label"])))
    write_tsv(OUTDIR/"gene_burden_summary.tsv",["sample_id","run_id","assay_type","run_classification","gene_burden_rank","gene_id","gene_id_status","variant_count"],sorted(gene_burden,key=lambda r:(r["sample_id"],r["run_id"],r["gene_burden_rank"])))
    write_tsv(OUTDIR/"run_reproducibility_summary.tsv",["comparison_id","sample_id","run_id_a","run_id_b","comparison_type","assay_transition","priority_summary_match","validation_summary_match","interpretation_summary_match","gene_burden_match","overall_reproducibility_status","notes"],repro)
    print(f"Wrote harvest tables to {OUTDIR}")
if __name__=="__main__":main()
