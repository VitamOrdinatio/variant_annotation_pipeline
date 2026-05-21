#!/usr/bin/env python3
from pathlib import Path
import argparse,csv,math,yaml
import pandas as pd
import plotly.graph_objects as go

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

def write_source_tsv(path,rows):
    fields=["figure_id","panel_id","source_node","target_node","source_column","target_column","representative_run_id","raw_source_count","raw_target_count","plot_value_log10","matched_across_runs","compared_run_ids","source_table","transformation_rule"]
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields,delimiter="\t",lineterminator="\n")
        w.writeheader()
        for r in rows:w.writerow({k:r.get(k,"NA") for k in fields})

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--config",required=True)
    args=ap.parse_args()
    cfg=yaml.safe_load(Path(args.config).read_text())

    case_dir=Path(cfg["case_dir"])
    table_dir=case_dir/"tables"
    out_dir=case_dir/"figures"
    out_dir.mkdir(parents=True,exist_ok=True)

    funnel=read_tsv(table_dir/"stage_funnel_summary.tsv")
    required={"sample_id","run_id"}
    missing=required-set(funnel.columns)
    if missing:raise ValueError(f"stage_funnel_summary.tsv missing required columns: {sorted(missing)}")

    flow_layers=cfg.get("flow_layers",[])
    if len(flow_layers)<2:raise ValueError("F3 config requires at least two flow_layers.")

    for layer in flow_layers:
        if "label" not in layer or "column" not in layer:
            raise ValueError(f"Malformed flow layer: {layer}")
        if layer["column"] not in funnel.columns:
            raise ValueError(f"Configured flow column not found in stage_funnel_summary.tsv: {layer['column']}")

    fn=funnel[funnel["sample_id"]==cfg["case_id"]].copy()
    if fn.empty:raise ValueError(f"No funnel rows found for case_id={cfg['case_id']}")

    run_ids=sorted(fn["run_id"].unique())
    if len(run_ids) not in (1,2):
        raise ValueError(f"Expected one or two funnel runs; found {len(run_ids)}: {run_ids}")

    for layer in flow_layers:
        col=layer["column"]
        fn[col]=pd.to_numeric(fn[col],errors="coerce")
    if fn[[layer["column"] for layer in flow_layers]].isna().any().any():
        raise ValueError("Non-parseable configured flow counts detected.")

    representative_rule=cfg.get("representative_run","run_b")
    if len(run_ids)==1:
        representative_run_id=run_ids[0]
        matched_across_runs="single_run"
    else:
        representative_run_id=run_ids[1] if representative_rule=="run_b" else run_ids[0]
        matched_across_runs=bool((fn.set_index("run_id").loc[run_ids[0],[l["column"] for l in flow_layers]].values == fn.set_index("run_id").loc[run_ids[1],[l["column"] for l in flow_layers]].values).all())

    rep=fn[fn["run_id"]==representative_run_id]
    if len(rep)!=1:raise ValueError(f"Expected one representative row for {representative_run_id}; found {len(rep)}")
    rep=rep.iloc[0]

    labels=[]
    node_colors=[]
    for layer in flow_layers:
        count=rep[layer["column"]]
        labels.append(f"{layer['label']}<br><b>{compact_count(count)}</b>")
        node_colors.append("#4F81BD")

    sources=[]
    targets=[]
    values=[]
    link_colors=[]
    source_rows=[]

    for i in range(len(flow_layers)-1):
        src=flow_layers[i]
        tgt=flow_layers[i+1]
        raw_src=float(rep[src["column"]])
        raw_tgt=float(rep[tgt["column"]])
        plot_value=math.log10(raw_tgt+1)
        sources.append(i)
        targets.append(i+1)
        values.append(plot_value)
        link_colors.append("rgba(91,75,154,0.35)")
        source_rows.append({
            "figure_id":"F3",
            "panel_id":"A",
            "source_node":src["label"],
            "target_node":tgt["label"],
            "source_column":src["column"],
            "target_column":tgt["column"],
            "representative_run_id":representative_run_id,
            "raw_source_count":int(raw_src),
            "raw_target_count":int(raw_tgt),
            "plot_value_log10":plot_value,
            "matched_across_runs":matched_across_runs,
            "compared_run_ids":";".join(run_ids),
            "source_table":"stage_funnel_summary.tsv",
            "transformation_rule":"Sankey link width = log10(target_count + 1); labels report raw counts"
        })

    source_path=out_dir/f"{cfg['output_prefix']}_source.tsv"
    write_source_tsv(source_path,source_rows)

    if matched_across_runs is True:
        validation_note="Displayed flow uses Run B; configured stage counts matched across compared runs."
    elif matched_across_runs=="single_run":
        validation_note="Displayed flow represents the available run for this case study."
    else:
        validation_note="Displayed flow uses representative run only; configured stage counts differed across runs."

    fig=go.Figure(data=[go.Sankey(
        arrangement="fixed",
        node=dict(
            pad=24,
            thickness=22,
            line=dict(color="rgba(40,40,40,0.35)",width=0.5),
            label=labels,
            color=node_colors,
            x=[i/(len(labels)-1) for i in range(len(labels))],
            y=[0.46 for _ in labels],
            hovertemplate="%{label}<extra></extra>"
        ),
        link=dict(
            source=sources,
            target=targets,
            value=values,
            color=link_colors,
            hovertemplate="log10-scaled width: %{value:.2f}<extra></extra>"
        )
    )])

    fig.update_layout(
        title=dict(
            text=cfg["figure_title"],
            x=0.5,
            y=0.96,
            xanchor="center",
            yanchor="top",
            font=dict(size=22,color="#222222")
        ),
        annotations=[
            dict(
                text="Deterministic evidence refinement across explicit VAP interpretation layers.",
                x=0.5,y=0.89,
                xref="paper",yref="paper",
                showarrow=False,
                font=dict(size=13,color="#444444")
            ),
            dict(
                text=validation_note,
                x=0.5,y=0.13,
                xref="paper",yref="paper",
                showarrow=False,
                font=dict(size=11,color="#555555")
            ),
            dict(
                text="Flow widths are log10-scaled for visual readability; node labels report raw evidence counts.",
                x=0.5,y=0.09,
                xref="paper",yref="paper",
                showarrow=False,
                font=dict(size=10,color="#666666")
            ),
            dict(
                text="Generated deterministically from case-study TSV artifacts. Evidence refinement only; not clinical interpretation.",
                x=0.5,y=0.045,
                xref="paper",yref="paper",
                showarrow=False,
                font=dict(size=10,color="#555555")
            )
        ],
        font=dict(size=12,family="Arial"),
        paper_bgcolor="white",
        plot_bgcolor="white",
        width=1400,
        height=760,
        margin=dict(l=40,r=40,t=90,b=85)
    )

    png=out_dir/f"{cfg['output_prefix']}.png"
    pdf=out_dir/f"{cfg['output_prefix']}.pdf"
    fig.write_image(str(png),scale=2)
    fig.write_image(str(pdf))
    print(f"Wrote {png}")
    print(f"Wrote {pdf}")
    print(f"Wrote {source_path}")
    print(validation_note)

if __name__=="__main__":main()