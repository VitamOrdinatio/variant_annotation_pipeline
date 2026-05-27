#!/usr/bin/env python3
from pathlib import Path
from datetime import datetime, timezone
import argparse
import csv
import subprocess
import sys
import yaml

SCRIPT_BY_FIGURE_PREFIX={
    "f3a":"scripts/figures/generate_case_study_f3a_deterministic_evidence_lineage.py",
    "f3b":"scripts/figures/generate_case_study_f3b_semantic_branching.py",
    "f4a":"scripts/figures/generate_case_study_f4_semantic_categories.py",
    "f4b":"scripts/figures/generate_case_study_f4_semantic_categories.py",
    "f5":"scripts/figures/generate_case_study_f5_stage08_interoperability_substrates.py",
}

def read_yaml(path:Path)->dict:
    with Path(path).open("r",encoding="utf-8") as f:
        data=yaml.safe_load(f)
    return data or {}

def flatten_context(parent:dict)->dict:
    context={
        "sample_id":parent["sample_id"],
        "run_id":parent["run_id"],
        "run_dir":parent["run_dir"],
        "output_dir":parent["output_dir"],
    }
    for key,value in parent.get("substrates",{}).items():
        context[key]=value
    return context

def resolve_value(value,context:dict):
    if isinstance(value,str):
        previous=None
        current=value
        for _ in range(3):
            if current==previous:
                break
            previous=current
            current=current.format(**context)
        return current
    if isinstance(value,dict):
        return {k:resolve_value(v,context) for k,v in value.items()}
    if isinstance(value,list):
        return [resolve_value(v,context) for v in value]
    return value

def figure_script_for(figure_id:str)->str:
    for prefix,script in SCRIPT_BY_FIGURE_PREFIX.items():
        if figure_id.lower().startswith(prefix):
            return script
    raise ValueError(f"No renderer registered for figure_id={figure_id}")

def write_resolved_config(path:Path,cfg:dict)->Path:
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("w",encoding="utf-8") as f:
        yaml.safe_dump(cfg,f,sort_keys=False)
    return path

def infer_output_path(cfg:dict)->str:
    if "output" in cfg:
        return cfg["output"]
    if "out" in cfg:
        return cfg["out"]
    if "case_dir" in cfg and "output_prefix" in cfg:
        return str(Path(cfg["case_dir"])/"figures"/f"{cfg['output_prefix']}.png")
    if "output_dir" in cfg and "output_prefix" in cfg:
        return str(Path(cfg["output_dir"])/f"{cfg['output_prefix']}.png")
    return "unknown"

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--config",required=True,help="Parent figure-set YAML.")
    ap.add_argument("--dry-run",action="store_true")
    args=ap.parse_args()

    parent_path=Path(args.config)
    parent=read_yaml(parent_path)
    context=flatten_context(parent)

    output_dir=Path(resolve_value(parent["output_dir"],context))
    output_dir.mkdir(parents=True,exist_ok=True)

    resolved_dir=output_dir/"resolved_configs"
    manifest_path=output_dir/"figure_manifest.tsv"
    generated_at=datetime.now(timezone.utc).isoformat()

    rows=[]

    for child_path_raw in parent["figure_configs"]:
        child_path=Path(resolve_value(child_path_raw,context))
        child=read_yaml(child_path)

        child_context={**child,**context}
        resolved=resolve_value(child,child_context)

        # Second-pass resolution so fields can reference sibling fields
        # resolved in the first pass, e.g. out: "{output_dir}/{output_prefix}.png"
        child_context={**resolved,**context}
        resolved=resolve_value(resolved,child_context)


        figure_id=resolved["figure_id"]
        script=figure_script_for(figure_id)

        resolved_cfg_path=resolved_dir/f"{figure_id.lower()}_{child_path.name}"
        write_resolved_config(resolved_cfg_path,resolved)

        command=[
            sys.executable,
            script,
            "--config",
            str(resolved_cfg_path),
        ]

        status="dry_run"
        if not args.dry_run:
            subprocess.run(command,check=True)
            status="success"

        rows.append({
            "sample_id":parent["sample_id"],
            "run_id":parent["run_id"],
            "run_dir":parent["run_dir"],
            "figure_id":figure_id,
            "figure_config_yaml":str(child_path),
            "resolved_config_yaml":str(resolved_cfg_path),
            "output_figure_directory":str(output_dir),
            "output_path":infer_output_path(resolved),
            "generation_command":" ".join(command),
            "generated_at":generated_at,
            "status":status,
        })

    fields=[
        "sample_id",
        "run_id",
        "run_dir",
        "figure_id",
        "figure_config_yaml",
        "resolved_config_yaml",
        "output_figure_directory",
        "output_path",
        "generation_command",
        "generated_at",
        "status",
    ]

    with manifest_path.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields,delimiter="\t",lineterminator="\n")
        w.writeheader()
        w.writerows(rows)

    print(f"Wrote manifest: {manifest_path}")

if __name__=="__main__":
    main()