#!/usr/bin/env python3
#
#
# This script harvests metrics and provenance details from multiple runs of the variant annotation pipeline, capturing a comprehensive set of data for analysis and comparison across runs with different classifications and metadata statuses. The harvested data includes funnel metrics, runtime profiles, priority tier summaries, validation summaries, interpretation label summaries, gene burden summaries, and reproducibility comparisons. The script is designed to handle the evolving structure of the pipeline's outputs and metadata during development, with annotations to provide critical context for interpreting the provenance and results of each run in light of known issues and development status. By systematically harvesting and comparing these metrics across runs, the script enables nuanced analysis of the pipeline's performance and interpretation outcomes in the context of its ongoing development and evolution. 
#
#

# Library declarations
from pathlib import Path
import csv,json

# Initialize global variables
RUN_DIRS=[Path("results/run_2026_04_17_082417"),Path("results/run_2026_05_13_060859"),Path("results/run_2026_05_14_083044"),Path("results/run_2026_05_14_231247"),Path("results/run_2026_05_14_164444"),Path("results/run_2026_05_15_063040")]
OUTDIR=Path("docs/case_studies/tables")
GENE_LISTS={
    "mitocarta":"data/reference/gene_lists/mitocarta_vap_overlay_seed.tsv",
    "epi25_all_epilepsy":"data/reference/gene_lists/epi25_vap_overlay_seed.tsv"
}
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

# Utility functions for loading, processing, and writing the harvested data, with annotations to explain their purpose and how they contribute to the overall data harvesting and analysis process. These functions enable the harvest to capture a comprehensive set of metrics and provenance details from each run, while also providing the necessary tools to process and compare these metrics across runs in a structured and consistent manner. By defining these utility functions, the script can maintain clarity and modularity in its data processing logic, making it easier to understand and modify as needed during the ongoing development of the pipeline and its associated metadata structures.    
def collapse_counts(rows,group_keys,count_name="variant_count"):
    counts={}
    for r in rows:
        key=tuple(r.get(k,"NA") for k in group_keys)
        counts[key]=counts.get(key,0)+1
    return [{**{k:v for k,v in zip(group_keys,key)},count_name:count} for key,count in sorted(counts.items())]
def profile_overlay_coding(stage09_path,overlay_map,base_meta):
    clinical=[];frequency=[];impact=[]
    if not stage09_path.exists():return clinical,frequency,impact
    with stage09_path.open(encoding="utf-8",newline="") as f:
        for row in csv.DictReader(f,delimiter="\t"):
            gene_id=row.get("gene_id","").strip()
            hit=overlay_map.get(gene_id)
            if not hit:continue
            sources=sorted(hit["sources"])
            common={"sample_id":base_meta["sample_id"],"run_id":base_meta["run_id"],"assay_type":base_meta["assay_type"],"run_classification":base_meta["run_classification"],"gene_id":gene_id,"gene_symbol":row.get("gene_symbol","NA"),"overlay_source":"multiple" if len(sources)>1 else sources[0],"overlay_source_count":len(sources),"overlay_source_list":";".join(sources),"mitocarta_hit":"mitocarta" in sources,"epi25_hit":"epi25_all_epilepsy" in sources,"match_key":"ensembl_gene_id"}
            clinical.append({**common,"clinical_evidence":row.get("clinical_evidence","NA"),"clinical_status":row.get("clinical_status","NA")})
            frequency.append({**common,"frequency_status":row.get("frequency_status","NA"),"rarity_flag":row.get("rarity_flag","NA")})
            impact.append({**common,"functional_impact":row.get("functional_impact","NA")})
    return clinical,frequency,impact
def load_gene_list_overlays(gene_lists):
    overlays={}
    for source,path in gene_lists.items():
        p=Path(path)
        if not p.exists():continue
        with p.open(encoding="utf-8-sig",newline="") as f:
            reader=csv.DictReader(f,delimiter="\t")
            for raw in reader:
                row={k.strip():v.strip() for k,v in raw.items() if k is not None}
                ensembl=row.get("ensembl_gene_id","")
                if not ensembl:continue
                overlays.setdefault(ensembl,{"gene_id":row.get("gene_id","NA"),"gene_symbol":row.get("gene_symbol","NA"),"sources":set()})
                overlays[ensembl]["sources"].add(source)
    return overlays
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
    overlay_map=load_gene_list_overlays(GENE_LISTS)
    # Collectors
    funnel=[];runtime=[];priority=[];validation=[];prov=[]
    interpretation=[];gene_burden=[];consequence=[];variant_consequence=[];gene_overlay=[];repro=[]
    overlay_clinical=[];overlay_frequency=[];overlay_impact=[]
    for rd in RUN_DIRS:
        # Path resolution with legacy support for runs that have raw_mark_outputs as the base, and loading of all relevant metadata and summary files to capture the full provenance and results landscape of each run. The harvest captures both the raw outputs and the interpreted summaries to enable comprehensive analysis of each run's performance, interpretation outcomes, and provenance details in the context of the evolving pipeline development and metadata normalization efforts. 
        base=run_base(rd)
        # Load metadata and summaries with fallbacks to ensure that the harvest captures as much information as possible from each run, even if some files are missing or if the structure has evolved during development. The use of n() with defaults allows the harvest to gracefully handle missing fields while still capturing available data, and the annotations provide critical context for interpreting the provenance and results of each run in light of known issues and development status. Interpretation summaries are harvested from the final summary to reflect the most up-to-date interpretation logic and fixes that may have been applied after stage 12, ensuring that the interpretation metrics in the harvest represent the final state of each run's interpretations.  
        meta=load_json(base/"metadata/run_metadata.json")
        legacy=load_json(base/"metadata.json")
        fp=load_json(base/"metadata/run_fingerprint.json")
        s8=load_json(base/"processed/stage_08_summary.json")
        s9=load_json(base/"processed/stage_09_summary.json")
        s10=load_json(base/"processed/stage_10_summary.json")
        s11=load_json(base/"processed/stage_11_summary.json")
        s12=load_json(base/"processed/stage_12_summary.json")
        s13=load_json(base/"processed/stage_13_final_summary.json")
        # Metadata interpretation with annotations to classify runs and provide context for interpreting the provenance and results. The harvest captures both the raw metadata fields and the annotated classifications and notes to enable nuanced analysis of each run's performance and outcomes in the context of the evolving pipeline development and metadata normalization efforts.    
        run_id=n(meta,"run","run_id",default=rd.name)
        # Sample ID and assay type are harvested with fallbacks to capture the intended sample and assay information for each run, even in cases where the metadata may be incomplete or evolving. The use of n() with defaults allows the harvest to capture available information while gracefully handling missing fields, and the annotations provide critical context for interpreting the sample and assay information in light of known issues and development status. This ensures that the harvest can accurately reflect the sample and assay context of each run, which is essential for analyzing performance and interpretation outcomes across different runs and conditions. 
        sample_id=n(legacy,"sample","sample_id",default=s13.get("sample_id","NA"))
        # Assay type is harvested with a fallback to the final summary and then the legacy metadata to capture the intended assay information for each run, even in cases where the metadata may be incomplete or evolving. The annotations provide critical context for interpreting the assay information in light of known issues and development status, ensuring that the harvest can accurately reflect the assay context of each run for nuanced analysis of performance and interpretation outcomes across different runs and conditions.   
        assay=n(legacy,"sample","assay_type",default="NA")
        # Run annotations are used to classify runs and provide context for interpreting the provenance and results, capturing both the raw metadata fields and the annotated classifications and notes to enable nuanced analysis of each run's performance and outcomes in the context of the evolving pipeline development and metadata normalization efforts. The annotations allow the harvest to capture critical context for each run, such as known issues, development status, and expected nuances in the provenance data, which is essential for accurately interpreting the results and performance of each run in light of its unique circumstances.   
        ann=RUN_ANNOTATIONS.get(run_id,{})
        run_classification=ann.get("run_classification","unclassified")
        base_meta={"sample_id":sample_id,"run_id":run_id,"assay_type":assay,"run_classification":run_classification}
        c_rows,f_rows,i_rows=profile_overlay_coding(base/"processed/stage_09_coding_interpreted.tsv",overlay_map,base_meta)
        overlay_clinical+=c_rows
        overlay_frequency+=f_rows
        overlay_impact+=i_rows        
        # Assay metadata status is annotated to reflect known issues and development status related to assay metadata for each run, providing critical context for interpreting the provenance and results in light of the evolving pipeline development and metadata normalization efforts. This annotation allows the harvest to capture the intended narrative and known nuances of each run's assay metadata status, which is essential for accurately analyzing performance and interpretation outcomes across different runs and conditions, especially as the pipeline and metadata structures evolve.   
        assay_metadata_status=ann.get("assay_metadata_status","unknown")
        run_notes=ann.get("notes","")
        # Overrides for provenance fields to reflect known metadata issues and checkpoint development status, ensuring accurate interpretation of provenance data in the context of evolving pipeline development and metadata normalization. These overrides allow the harvest to capture the intended narrative and known nuances of each run's provenance, rather than relying solely on potentially inconsistent or evolving metadata fields in the raw outputs.    
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
            hit=overlay_map.get(row["gene_id"])
            if hit:
                sources=sorted(hit["sources"])
                gene_overlay.append({"sample_id":sample_id,"run_id":run_id,"assay_type":assay,"run_classification":run_classification,"gene_id":row["gene_id"],"gene_symbol":hit["gene_symbol"],"gene_burden_rank":row["gene_burden_rank"],"variant_count":row["variant_count"],"overlay_source":"multiple" if len(sources)>1 else sources[0],"overlay_source_count":len(sources),"overlay_source_list":";".join(sources),"mitocarta_hit":"mitocarta" in sources,"epi25_hit":"epi25_all_epilepsy" in sources,"match_key":"ensembl_gene_id"})
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
        # Coding interpretation consequence abstraction (Stage 09)
        coding_axes=[
            ("functional_impact_distribution","variant_function"),
            ("clinical_evidence_distribution","clinical_status"),
            ("rarity_flag_distribution","frequency_class"),
            ("coding_interpretation_label_distribution","interpretation_label")
        ]
        # The coding interpretation consequence abstraction captures the counts of interpreted variants across multiple axes, including variant function, clinical support, frequency class, and interpretation label. By harvesting these counts from stage 09 summaries, the harvest can provide insights into the distribution of interpreted variants across these key dimensions, which are critical for understanding the interpretation outcomes and their potential clinical relevance. The annotations for each axis provide context for interpreting the consequences of variants in the coding domain, allowing for nuanced analysis of how different types of variants are being interpreted across runs with different classifications and metadata statuses. This information is essential for assessing the stability and reliability of the pipeline's interpretation logic in the context of its ongoing development and evolution.    
        for field,axis in coding_axes:
            for label,count in sorted(s9.get(field,{}).items()):
                consequence.append({
                    "sample_id":sample_id,
                    "run_id":run_id,
                    "assay_type":assay,
                    "run_classification":run_classification,
                    "interpretation_domain":"coding",
                    "summary_axis":axis,
                    "consequence_label":label,
                    "count":count
                })
        # Noncoding interpretation consequence abstraction (Stage 10)
        noncoding_axes=[
            ("noncoding_functional_context_distribution","context"),
            ("clinical_evidence_distribution","clinical_status"),
            ("rarity_flag_distribution","frequency_class"),
            ("noncoding_interpretation_label_distribution","interpretation_label")
        ]
        # The noncoding interpretation consequence abstraction captures the counts of interpreted variants across multiple axes, including context, clinical support, frequency class, and interpretation label. By harvesting these counts from stage 10 summaries, the harvest can provide insights into the distribution of interpreted variants across these key dimensions in the noncoding domain, which are critical for understanding the interpretation outcomes and their potential clinical relevance. The annotations for each axis provide context for interpreting the consequences of variants in the noncoding domain, allowing for nuanced analysis of how different types of variants are being interpreted across runs with different classifications and metadata statuses. This information is essential for assessing the stability and reliability of the pipeline's interpretation logic in the context of its ongoing development and evolution.
        for field,axis in noncoding_axes:
            for label,count in sorted(s10.get(field,{}).items()):
                consequence.append({
                    "sample_id":sample_id,
                    "run_id":run_id,
                    "assay_type":assay,
                    "run_classification":run_classification,
                    "interpretation_domain":"noncoding",
                    "summary_axis":axis,
                    "consequence_label":label,
                    "count":count
                })
        # Molecular consequence abstraction harvesting

        # Coding molecular consequences (Stage 09)
        for label,count in sorted(s9.get("functional_impact_distribution",{}).items()):
            variant_consequence.append({
                "sample_id":sample_id,
                "run_id":run_id,
                "assay_type":assay,
                "run_classification":run_classification,
                "interpretation_domain":"coding",
                "molecular_consequence":label,
                "count":count
            })

        # Noncoding contextual consequences (Stage 10)
        for label,count in sorted(s10.get("noncoding_functional_context_distribution",{}).items()):
            variant_consequence.append({
                "sample_id":sample_id,
                "run_id":run_id,
                "assay_type":assay,
                "run_classification":run_classification,
                "interpretation_domain":"noncoding",
                "molecular_consequence":label,
                "count":count
            })
    # Define the comparisons to be made between runs, with annotations to explain the rationale for each comparison and the expected outcomes based on the known development status and metadata issues of each run. These comparisons are designed to capture key transitions in the pipeline development and metadata normalization efforts, allowing for nuanced analysis of how these factors may impact the reproducibility of results and the detection of biological divergence. By systematically comparing the outputs of different runs across key metrics, the harvest can provide insights into the stability and reliability of the pipeline's performance and interpretation outcomes in the context of its ongoing development and evolution.
    comparisons=[
        {"comparison_id":"HG002_developmental_epoch","sample_id":"HG002","run_id_a":"run_2026_04_17_082417","run_id_b":"run_2026_05_13_060859","comparison_type":"developmental_epoch_transition","assay_transition":"WGS→WGS","notes":"Checkpoint-era developmental run compared against telemetry-era stabilized run."},
        {"comparison_id":"ERR10619281_metadata_transition","sample_id":"ERR10619281","run_id_a":"run_2026_05_14_083044","run_id_b":"run_2026_05_14_231247","comparison_type":"metadata_normalization_transition","assay_transition":"WGS→WES","notes":"Assay metadata normalization transition; biological evidence structure expected to remain stable."},
        {"comparison_id":"ERR10619300_standard_rerun","sample_id":"ERR10619300","run_id_a":"run_2026_05_14_164444","run_id_b":"run_2026_05_15_063040","comparison_type":"standard_rerun_reproducibility","assay_transition":"WES→WES","notes":"Telemetry-era rerun reproducibility assessment."}
    ]
    # Comparative analysis of runs to assess reproducibility and detect biological divergence, with a focus on interpreting the stability of priority tiers, validation metrics, interpretation labels, and gene burden rankings across runs with different classifications and metadata statuses. The comparisons are designed to capture key transitions in the pipeline development and metadata normalization efforts, allowing for nuanced analysis of how these factors may impact the reproducibility of results and the detection of biological divergence. By systematically comparing the outputs of different runs across these key metrics, the harvest can provide insights into the stability and reliability of the pipeline's performance and interpretation outcomes in the context of its ongoing development and evolution.  
    for c in comparisons:
        # For each comparison, the harvest projects the relevant fields from the priority tier summaries, validation summaries, interpretation label summaries, and gene burden summaries for each run, and checks for exact matches to assess reproducibility. The annotations explain that this comparison allows the harvest to determine if the interpretation outcomes are reproducible or if there is evidence of biological divergence, providing critical insights into the reliability of the pipeline's interpretation logic in the context of its ongoing development and evolution. By comparing these metrics across runs with different classifications and metadata statuses, the harvest can assess how changes in the pipeline and metadata may impact the interpretation results, which are central to the clinical relevance of the pipeline's outputs.
        pa=project_rows(rows_for_run(priority,c["run_id_a"]),["priority_tier","count"])
        pb=project_rows(rows_for_run(priority,c["run_id_b"]),["priority_tier","count"])
        va=project_rows(rows_for_run(validation,c["run_id_a"]),["metric","category","count"])
        vb=project_rows(rows_for_run(validation,c["run_id_b"]),["metric","category","count"])
        # Interpretation label summaries are compared by projecting the relevant fields for each run and checking for exact matches, which allows the harvest to assess the stability of interpretation outcomes across runs with different classifications and metadata statuses. By comparing the projected rows of interpretation label summaries, the harvest can determine if the interpretation outcomes are reproducible or if there is evidence of biological divergence, providing critical insights into the reliability of the pipeline's interpretation logic in the context of its ongoing development and evolution. This comparison is essential for understanding how changes in the pipeline and metadata may impact the interpretation results, which are central to the clinical relevance of the pipeline's outputs.
        ia=project_rows(rows_for_run(interpretation,c["run_id_a"]),["summary_axis","interpretation_label","count"])
        ib=project_rows(rows_for_run(interpretation,c["run_id_b"]),["summary_axis","interpretation_label","count"])
        # Gene burden summaries are compared by projecting the relevant fields for each run and checking for exact matches, which allows the harvest to assess the stability of gene burden rankings across runs with different classifications and metadata statuses. By comparing the projected rows of gene burden summaries, the harvest can determine if the gene burden rankings are reproducible or if there is evidence of biological divergence, providing critical insights into the reliability of the pipeline's interpretation logic in the context of its ongoing development and evolution. This comparison is essential for understanding how changes in the pipeline and metadata may impact the gene burden results, which are important for prioritizing genes for further analysis and potential clinical relevance.
        ga=project_rows(rows_for_run(gene_burden,c["run_id_a"]),["gene_burden_rank","gene_id","gene_id_status","variant_count"])
        gb=project_rows(rows_for_run(gene_burden,c["run_id_b"]),["gene_burden_rank","gene_id","gene_id_status","variant_count"])
        # The reproducibility assessment compares the priority tier summaries, validation summaries, interpretation label summaries, and gene burden summaries between two runs to determine if they are reproducible or if there is evidence of biological divergence. The comparison checks for exact matches in the projected rows of each metric, and based on these matches, it classifies the overall reproducibility status of the runs. For the metadata normalization transition comparison, even if all metrics match, the overall status is annotated as "reproducible_with_provenance_evolution" to reflect the expected changes in provenance due to metadata normalization, while still acknowledging that the core results are reproducible. This nuanced classification allows for a more accurate interpretation of the results in the context of known development and metadata changes.
        priority_match=pa==pb
        validation_match=va==vb
        interpretation_match=ia==ib
        gene_burden_match=ga==gb
        # The overall reproducibility status is determined based on the matches of the individual metrics, with annotations to explain the rationale for classifying runs as "reproducible", "biological_divergence_detected", or "reproducible_with_provenance_evolution" in the context of the known development status and metadata issues. This classification allows the harvest to provide critical insights into the stability and reliability of the pipeline's performance and interpretation outcomes across different runs and conditions, while also accounting for expected changes in provenance due to metadata normalization efforts. By systematically assessing reproducibility across these key metrics, the harvest can inform future development efforts and help prioritize areas for improvement in the pipeline.    
        overall="reproducible" if all([priority_match,validation_match,interpretation_match,gene_burden_match]) else "biological_divergence_detected"
        # For the metadata normalization transition comparison, even if all metrics match, the overall status is annotated as "reproducible_with_provenance_evolution" to reflect the expected changes in provenance due to metadata normalization, while still acknowledging that the core results are reproducible. This nuanced classification allows for a more accurate interpretation of the results in the context of known development and metadata changes, providing critical insights into the stability and reliability of the pipeline's performance and interpretation outcomes across different runs and conditions. By accounting for expected provenance evolution in this way, the harvest can better inform future development efforts and help prioritize areas for improvement in the pipeline while recognizing the complexities introduced by metadata normalization efforts.    
        if overall=="reproducible" and c["comparison_type"]=="metadata_normalization_transition":
            overall="reproducible_with_provenance_evolution"
        # Append the results of the reproducibility assessment for this comparison to the repro list, capturing the comparison details, metric matches, overall reproducibility status, and any relevant notes. This structured capture of reproducibility results allows for systematic analysis and reporting of the stability and reliability of the pipeline's performance and interpretation outcomes across different runs and conditions, while also accounting for known development status and metadata issues. By including detailed information about each comparison, the harvest can provide critical insights into the factors that may impact reproducibility and help inform future development efforts to improve the pipeline.    
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
    clinical_fields=["sample_id","run_id","assay_type","run_classification","gene_id","gene_symbol","overlay_source","overlay_source_count","overlay_source_list","mitocarta_hit","epi25_hit","match_key","clinical_evidence","clinical_status"]
    frequency_fields=["sample_id","run_id","assay_type","run_classification","gene_id","gene_symbol","overlay_source","overlay_source_count","overlay_source_list","mitocarta_hit","epi25_hit","match_key","frequency_status","rarity_flag"]
    impact_fields=["sample_id","run_id","assay_type","run_classification","gene_id","gene_symbol","overlay_source","overlay_source_count","overlay_source_list","mitocarta_hit","epi25_hit","match_key","functional_impact"]
    # Write the harvested tables to TSV files in the output directory, with sorting to ensure consistent ordering for analysis and comparison. The tables capture a comprehensive set of metrics and provenance details for each run, as well as the results of comparative analyses to assess reproducibility and detect biological divergence across key transitions in the pipeline development and metadata normalization efforts. By writing these tables to TSV files, the harvest enables further analysis and visualization of the data in a structured format that can be easily consumed by downstream tools and case studies.
    write_tsv(OUTDIR/"stage_funnel_summary.tsv",["sample_id","run_id","assay_type","run_classification","assay_metadata_status","run_notes","raw_variant_count","normalized_variant_count","annotated_variant_count","stage08_total_variants","coding_candidates","noncoding_candidates","splice_region_candidates","qc_flagged","stage09_coding_interpreted","stage10_noncoding_interpreted","stage11_prioritized_rows","stage12_validation_rows","rdgp_gene_evidence_seed_rows","unique_gene_ids"],sorted(funnel,key=lambda r:(r["sample_id"],r["run_id"])))
    write_tsv(OUTDIR/"runtime_stage_summary.tsv",["sample_id","run_id","stage","elapsed_seconds","status","start_time","end_time"],sorted(runtime,key=lambda r:(r.get("sample_id",""),r.get("run_id",""),r.get("stage",""))))
    write_tsv(OUTDIR/"priority_tier_summary.tsv",["sample_id","run_id","priority_tier","count"],sorted(priority,key=lambda r:(r["sample_id"],r["run_id"],r["priority_tier"])))
    write_tsv(OUTDIR/"candidate_reviewability_readiness.tsv",["sample_id","run_id","metric","category","count"],sorted(validation,key=lambda r:(r["sample_id"],r["run_id"],r["metric"],r["category"])))
    write_tsv(OUTDIR/"provenance_summary.tsv",["sample_id","run_id","assay_type","run_classification","assay_metadata_status","run_notes","pipeline_version","status","machine_id","config_path","git_commit","config_hash","reference_genome","reference_fasta_hash_or_size","execution_profile"],sorted(prov,key=lambda r:(r["sample_id"],r["run_id"])))
    write_tsv(OUTDIR/"interpretation_label_summary.tsv",["sample_id","run_id","assay_type","run_classification","summary_axis","interpretation_label","count"],sorted(interpretation,key=lambda r:(r["sample_id"],r["run_id"],r["summary_axis"],r["interpretation_label"])))
    write_tsv(OUTDIR/"gene_burden_summary.tsv",["sample_id","run_id","assay_type","run_classification","gene_burden_rank","gene_id","gene_id_status","variant_count"],sorted(gene_burden,key=lambda r:(r["sample_id"],r["run_id"],r["gene_burden_rank"])))
    write_tsv(OUTDIR/"run_reproducibility_summary.tsv",["comparison_id","sample_id","run_id_a","run_id_b","comparison_type","assay_transition","priority_summary_match","validation_summary_match","interpretation_summary_match","gene_burden_match","overall_reproducibility_status","notes"],repro)
    write_tsv(OUTDIR/"coding_noncoding_consequence_summary.tsv",["sample_id","run_id","assay_type","run_classification","interpretation_domain","summary_axis","consequence_label","count"],sorted(consequence,key=lambda r:(r["sample_id"],r["run_id"],r["interpretation_domain"],r["summary_axis"],r["consequence_label"])))
    write_tsv(OUTDIR/"variant_consequence_summary.tsv",["sample_id","run_id","assay_type","run_classification","interpretation_domain","molecular_consequence","count"],sorted(variant_consequence,key=lambda r:(r["sample_id"],r["run_id"],r["interpretation_domain"],r["molecular_consequence"])))
    write_tsv(OUTDIR/"gene_list_overlay_intersections.tsv",["sample_id","run_id","assay_type","run_classification","gene_id","gene_symbol","gene_burden_rank","variant_count","overlay_source","overlay_source_count","overlay_source_list","mitocarta_hit","epi25_hit","match_key"],sorted(gene_overlay,key=lambda r:(r["sample_id"],r["run_id"],r["overlay_source_list"],r["gene_burden_rank"],r["gene_id"])))
    write_tsv(OUTDIR/"overlay_gene_coding_clinical_evidence.tsv",clinical_fields+["variant_count"],collapse_counts(overlay_clinical,clinical_fields))
    write_tsv(OUTDIR/"overlay_gene_coding_frequency_profiles.tsv",frequency_fields+["variant_count"],collapse_counts(overlay_frequency,frequency_fields))
    write_tsv(OUTDIR/"overlay_gene_coding_functional_impact.tsv",impact_fields+["variant_count"],collapse_counts(overlay_impact,impact_fields))
    # Print a message indicating that the harvest tables have been written to the output directory, providing feedback to the user and confirming the completion of the data harvesting and writing process. This message serves as a simple confirmation that the script has executed successfully and that the resulting tables are available in the specified location for further analysis and use in case studies. 
    print(f"Wrote harvest tables to {OUTDIR}")
if __name__=="__main__":main()
