#!/usr/bin/env python3
from pathlib import Path
import argparse,csv,yaml
import pandas as pd
import plotly.graph_objects as go

# Color schema
primary_lineage="#4F6D8A"
secondary_refinement="#7D96B3"
graphite="#5B5B5B"

# Node x-positions and colors are defined here to ensure consistency between the script and the renderer, which uses the same substrate but does not execute this script.
x_positions=[0.03,0.26,0.50,0.73,0.94]
y_positions=[0.66,0.66,0.43,0.43,0.43]

# Sankey paper coordinates
sankey_x0=0.02
sankey_x1=0.98
sankey_y0=0.22
sankey_y1=0.90

# Node colors are defined here to ensure consistency between the script and the renderer, which uses the same substrate but does not execute this script. Primary lineage nodes share a color, while refinement nodes share a different color to visually distinguish them while maintaining a cohesive palette.
node_colors=[
    primary_lineage,
    primary_lineage,
    secondary_refinement,
    secondary_refinement,
    secondary_refinement,
]

# Link colors with alpha for visual emphasis on node widths
link_colors=[
    "rgba(79,109,138,0.32)",
    "rgba(125,150,179,0.34)",
    "rgba(125,150,179,0.34)",
    "rgba(125,150,179,0.34)",
]

def require_file(path):
    if not path.exists():raise FileNotFoundError(f"Required file not found: {path}")

def read_tsv(path):
    require_file(path)
    return pd.read_csv(path,sep="\t")

def compact_count(x):
    x=float(x)
    if x>=1_000_000:return f"{x/1_000_000:.2f}M"
    if x>=1_000:return f"{x/1000:.1f}k"
    return f"{int(x)}"

def write_source_tsv(path,df):
    fields=["figure_id","edge_order","source_label","target_label","source_metric_name","target_metric_name","source_metric_value","target_metric_value","edge_metric_value","scaling_mode","scaling_value","scaling_rule","semantic_caveat","source_artifact","run_id","sample_id","assay_type","run_classification"]
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields,delimiter="\t",lineterminator="\n")
        w.writeheader()
        for _,r in df.iterrows():
            w.writerow({k:r.get(k,"NA") for k in fields})

def write_provenance_tsv(path,cfg,df):
    fields=["key","value"]
    rows=[
        {"key":"figure_id","value":"F3A"},
        {"key":"case_id","value":cfg["case_id"]},
        {"key":"input_f3a_flow_v2_path","value":cfg["f3a_flow_v2_path"]},
        {"key":"output_prefix","value":cfg["output_prefix"]},
        {"key":"run_id","value":df["run_id"].iloc[0]},
        {"key":"sample_id","value":df["sample_id"].iloc[0]},
        {"key":"assay_type","value":df["assay_type"].iloc[0]},
        {"key":"run_classification","value":df["run_classification"].iloc[0]},
        {"key":"scaling_rule","value":df["scaling_rule"].iloc[0]},
        {"key":"renderer","value":"generate_case_study_f3a_deterministic_evidence_lineage.py"},
        {"key":"semantic_scope","value":"deterministic evidence lineage; not clinical interpretation"},
        {"key":"stage08_policy","value":"Stage 08 overlap compressed into Partitioned evidence"},
        {"key":"qc_policy","value":"QC not rendered as destructive branch"},
    ]
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields,delimiter="\t",lineterminator="\n")
        w.writeheader()
        w.writerows(rows)

def transform_widths(raw_values,mode,min_width,max_width):
    import math
    vals=[float(v) for v in raw_values]
    if mode=="sqrt":
        transformed=[v**0.5 for v in vals]
        note="Sankey widths use sqrt-normalized scaling for refinement-pressure readability."
    elif mode=="log10":
        transformed=[math.log10(v+1) for v in vals]
        note="Sankey widths use log10(edge_metric_value + 1) scaling for readability."
    elif mode=="log2":
        transformed=[math.log2(v+1) for v in vals]
        note="Sankey widths use log2(edge_metric_value + 1) scaling for readability."
    else:
        raise ValueError(f"Unsupported F3A scaling_mode: {mode}")
    max_t=max(transformed)
    if max_t==0:
        return [min_width for _ in transformed],note
    widths=[min_width+(v/max_t)*(max_width-min_width) for v in transformed]
    return widths,note

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--config",required=True)
    args=ap.parse_args()
    cfg=yaml.safe_load(Path(args.config).read_text())

    case_dir=Path(cfg["case_dir"])
    out_dir=case_dir/"figures"
    out_dir.mkdir(parents=True,exist_ok=True)

    flow=read_tsv(Path(cfg["f3a_flow_v2_path"]))
    required={"figure_id","edge_order","source_label","target_label","edge_metric_value","scaling_value","semantic_caveat","run_id","sample_id","assay_type","run_classification"}
    missing=required-set(flow.columns)
    if missing:raise ValueError(f"F3A substrate missing required columns: {sorted(missing)}")
    flow=flow.sort_values("edge_order").copy()
    if len(flow)!=4:raise ValueError(f"Expected 4 F3A refinement-pressure edges; found {len(flow)}")
    if set(flow["figure_id"])!={"F3A"}:raise ValueError("F3A substrate contains non-F3A rows.")
    for col in ["edge_metric_value","scaling_value"]:
        flow[col]=pd.to_numeric(flow[col],errors="coerce")
    if flow[["edge_metric_value","scaling_value"]].isna().any().any():
        raise ValueError("Non-parseable numeric values detected in F3A substrate.")

    out_prefix=cfg["output_prefix"]
    source_path=out_dir/f"{out_prefix}_source.tsv"
    provenance_path=out_dir/f"{out_prefix}_provenance.tsv"
    write_source_tsv(source_path,flow)
    write_provenance_tsv(provenance_path,cfg,flow)

    labels=list(dict.fromkeys(flow["source_label"].tolist()+flow["target_label"].tolist()))
    label_to_idx={label:i for i,label in enumerate(labels)}
    sources=[label_to_idx[x] for x in flow["source_label"]]
    targets=[label_to_idx[x] for x in flow["target_label"]]

    raw_values=flow["edge_metric_value"].astype(float).tolist()
    scaling_mode=cfg.get("scaling_mode","sqrt")
    min_width=float(cfg.get("min_width",1.2))
    max_width=float(cfg.get("max_width",8.0))
    values,scaling_note=transform_widths(raw_values,scaling_mode,min_width,max_width)


    label_counts={}
    for _,r in flow.iterrows():
        src_label=r["source_label"]
        tgt_label=r["target_label"]
        src_val=float(r["source_metric_value"])
        tgt_val=float(r["target_metric_value"])

        label_counts[src_label]=max(
            label_counts.get(src_label,0),
            src_val
        )

        label_counts[tgt_label]=max(
            label_counts.get(tgt_label,0),
            tgt_val
        )

    display_labels=[f"{label}<br><b>{compact_count(label_counts[label])}</b>" for label in labels]
    caveats="; ".join([x for x in flow["semantic_caveat"].astype(str).unique() if x!="none"])

    node_label_color="#263747"
    node_annotations=[]
    for label,x,y in zip(labels,x_positions,y_positions):
        node_annotations.append(
            dict(
                text=f"{label}<br><b>{compact_count(label_counts[label])}</b>",
                x=sankey_x0+(x*(sankey_x1-sankey_x0))+0.012,
                y=sankey_y0+(y*(sankey_y1-sankey_y0))+0.018,
                xref="paper",
                yref="paper",
                showarrow=False,
                align="left",
                font=dict(size=12,color=node_label_color),
                bgcolor="rgba(255,255,255,0.72)",
                bordercolor="rgba(255,255,255,0.0)",
                borderpad=2
            )
        )

    base_annotations=[
        dict(
            text="<i>Biologically meaningful refinement pressure with preserved provenance<br>and validation-readiness routing.</i>",
            x=0.50,y=0.905,
            xref="paper",yref="paper",
            showarrow=False,
            align="center",
            font=dict(size=11,color=graphite)
        ),

        dict(
            text=scaling_note,
            x=0.5,y=0.115,
            xref="paper",yref="paper",
            showarrow=False,
            font=dict(size=10,color=graphite)
        ),

        dict(
            text="Generated deterministically from sidecar F3A v2 telemetry substrate. Evidence lineage only; not clinical interpretation.",
            x=0.5,y=0.078,
            xref="paper",yref="paper",
            showarrow=False,
            font=dict(size=9,color=graphite)
        ),

        dict(
            text=f"Semantic caveats: {caveats}. Validation-ready does not mean clinically validated.",
            x=0.5,y=0.045,
            xref="paper",yref="paper",
            showarrow=False,
            font=dict(size=8,color=graphite)
        ),
    ]

    all_annotations=base_annotations+node_annotations

    fig=go.Figure(data=[go.Sankey(
        arrangement="fixed",
        domain=dict(x=[sankey_x0,sankey_x1],y=[sankey_y0,sankey_y1]),
        node=dict(
            pad=28,
            thickness=22,
            line=dict(color="rgba(45,45,45,0.35)",width=0.5),
            label=[""]*len(display_labels),
            color=node_colors,
            x=x_positions,
            y=y_positions,
            hovertemplate=f"{scaling_mode}-normalized visual width: "+"%{value:.3f}<extra></extra>"
        ),
        link=dict(
            source=sources,
            target=targets,
            value=values,
            color=link_colors,
            hovertemplate=f"{scaling_mode}-normalized visual width: "+"%{value:.3f}<extra></extra>"
        )
    )])

    fig.update_layout(
        title=dict(text=cfg["figure_title"],x=0.5,y=0.965,xanchor="center",yanchor="top",font=dict(size=22,color="#222222")),
        annotations=all_annotations,
        font=dict(size=12,family="Arial"),
        paper_bgcolor="white",
        plot_bgcolor="white",
        width=1700,
        height=860,
        margin=dict(l=40,r=60,t=95,b=145)
    )

    png=out_dir/f"{out_prefix}.png"
    pdf=out_dir/f"{out_prefix}.pdf"
    fig.write_image(str(png),scale=2)
    fig.write_image(str(pdf))
    print(f"Wrote {png}")
    print(f"Wrote {pdf}")
    print(f"Wrote {source_path}")
    print(f"Wrote {provenance_path}")

if __name__=="__main__":main()