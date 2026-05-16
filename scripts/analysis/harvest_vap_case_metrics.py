#!/usr/bin/env python3
from pathlib import Path
import csv,json
RUN_DIRS=[Path("results/run_2026_05_14_083044"),Path("results/run_2026_05_14_231247"),Path("results/run_2026_05_14_164444"),Path("results/run_2026_05_15_063040")]
OUTDIR=Path("docs/case_studies/tables")
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
    funnel=[];runtime=[];priority=[];validation=[];prov=[]
    for rd in RUN_DIRS:
        meta=load_json(rd/"metadata/run_metadata.json")
        legacy=load_json(rd/"metadata.json")
        fp=load_json(rd/"metadata/run_fingerprint.json")
        s8=load_json(rd/"processed/stage_08_summary.json")
        s9=load_json(rd/"processed/stage_09_summary.json")
        s10=load_json(rd/"processed/stage_10_summary.json")
        s11=load_json(rd/"processed/stage_11_summary.json")
        s12=load_json(rd/"processed/stage_12_summary.json")
        s13=load_json(rd/"processed/stage_13_final_summary.json")
        run_id=n(meta,"run","run_id",default=rd.name)
        sample_id=n(legacy,"sample","sample_id",default=s13.get("sample_id","NA"))
        assay=n(legacy,"sample","assay_type",default="NA")
        runtime+=read_runtime_profile(rd/"metadata/runtime_profile.tsv",run_id,sample_id)
        funnel.append({"sample_id":sample_id,"run_id":run_id,"assay_type":assay,"raw_variant_count":n(legacy,"qc","variant_calling_qc","variant_count"),"normalized_variant_count":n(legacy,"qc","normalization_qc","normalized_variant_count"),"annotated_variant_count":n(legacy,"qc","annotation_qc","annotated_variant_count"),"stage08_total_variants":s8.get("total_variants","NA"),"coding_candidates":n(s8,"partition_counts","coding_candidates"),"noncoding_candidates":n(s8,"partition_counts","noncoding_candidates"),"splice_region_candidates":n(s8,"partition_counts","splice_region_candidates"),"qc_flagged":n(s8,"partition_counts","qc_flagged"),"stage09_coding_interpreted":s9.get("interpreted_rows","NA"),"stage10_noncoding_interpreted":s10.get("interpreted_rows","NA"),"stage11_prioritized_rows":s11.get("output_rows","NA"),"stage12_validation_rows":s12.get("output_rows","NA"),"rdgp_gene_evidence_seed_rows":s8.get("rdgp_gene_evidence_seed_rows","NA"),"unique_gene_ids":s11.get("gene_id_count_unique",s13.get("gene_id_count_unique","NA"))})
        for tier,count in sorted(s11.get("counts_by_priority_tier",{}).items()):
            priority.append({"sample_id":sample_id,"run_id":run_id,"priority_tier":tier,"count":count})
        for method,count in sorted(s12.get("counts_by_suggested_validation_method",{}).items()):
            validation.append({"sample_id":sample_id,"run_id":run_id,"metric":"suggested_validation_method","category":method,"count":count})
        for pr,count in sorted(s12.get("counts_by_validation_priority",{}).items()):
            validation.append({"sample_id":sample_id,"run_id":run_id,"metric":"validation_priority","category":pr,"count":count})
        for req,count in sorted(s12.get("counts_by_validation_required",{}).items()):
            validation.append({"sample_id":sample_id,"run_id":run_id,"metric":"validation_required","category":req,"count":count})
        prov.append({"sample_id":sample_id,"run_id":run_id,"assay_type":assay,"pipeline_version":n(meta,"run","pipeline_version"),"status":n(meta,"run","status"),"machine_id":n(meta,"run","machine_id"),"config_path":n(meta,"run","config_path"),"git_commit":fp.get("git_commit","NA"),"config_hash":fp.get("config_hash","NA"),"reference_genome":fp.get("reference_genome","NA"),"reference_fasta_hash_or_size":fp.get("reference_fasta_hash_or_size","NA"),"execution_profile":fp.get("execution_profile","NA")})
    write_tsv(OUTDIR/"stage_funnel_summary.tsv",["sample_id","run_id","assay_type","raw_variant_count","normalized_variant_count","annotated_variant_count","stage08_total_variants","coding_candidates","noncoding_candidates","splice_region_candidates","qc_flagged","stage09_coding_interpreted","stage10_noncoding_interpreted","stage11_prioritized_rows","stage12_validation_rows","rdgp_gene_evidence_seed_rows","unique_gene_ids"],sorted(funnel,key=lambda r:(r["sample_id"],r["run_id"])))
    write_tsv(OUTDIR/"runtime_stage_summary.tsv",["sample_id","run_id","stage","elapsed_seconds","status","start_time","end_time"],sorted(runtime,key=lambda r:(r.get("sample_id",""),r.get("run_id",""),r.get("stage",""))))
    write_tsv(OUTDIR/"priority_tier_summary.tsv",["sample_id","run_id","priority_tier","count"],sorted(priority,key=lambda r:(r["sample_id"],r["run_id"],r["priority_tier"])))
    write_tsv(OUTDIR/"validation_readiness_summary.tsv",["sample_id","run_id","metric","category","count"],sorted(validation,key=lambda r:(r["sample_id"],r["run_id"],r["metric"],r["category"])))
    write_tsv(OUTDIR/"provenance_summary.tsv",["sample_id","run_id","assay_type","pipeline_version","status","machine_id","config_path","git_commit","config_hash","reference_genome","reference_fasta_hash_or_size","execution_profile"],sorted(prov,key=lambda r:(r["sample_id"],r["run_id"])))
    print(f"Wrote harvest tables to {OUTDIR}")
if __name__=="__main__":main()
