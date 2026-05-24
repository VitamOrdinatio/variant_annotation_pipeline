#!/usr/bin/env python3
from pathlib import Path
import argparse,csv,yaml
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

primary_lineage="#4F6D8A"
secondary_refinement="#7D96B3"
semantic_overlay="#B7B2C8"
graphite="#5B5B5B"

branch_class_colors={
    "coding":primary_lineage,
    "noncoding":secondary_refinement,
    "mixed":semantic_overlay,
}

semantic_group_order=[
    "rare_interpretable",
    "common_low_support",
    "uninterpretable",
]

semantic_group_labels={
    "rare_interpretable":"Rare interpretable evidence",
    "common_low_support":"Common / low-support evidence",
    "uninterpretable":"Uninterpretable evidence",
}

def require_file(path):
    if not path.exists():raise FileNotFoundError(f"Required file not found: {path}")

def read_tsv(path):
    require_file(path)
    return pd.read_csv(path,sep="\t")

def scaled_widths(values,mode,max_bar_width):
    import math
    vals=[float(v) for v in values]
    if mode=="sqrt":
        transformed=[v**0.5 for v in vals]
    elif mode=="log2":
        transformed=[math.log2(v+1) for v in vals]
    elif mode=="log10":
        transformed=[math.log10(v+1) for v in vals]
    elif mode=="linear":
        transformed=vals
    else:
        raise ValueError(f"Unsupported scaling_mode: {mode}")
    max_t=max(transformed) if transformed else 0
    if max_t==0:return [0 for _ in transformed]
    return [(v/max_t)*max_bar_width for v in transformed]

def compact_count(x):
    x=float(x)
    if x>=1_000_000:return f"{x/1_000_000:.2f}M"
    if x>=1_000:return f"{x/1000:.1f}k"
    return f"{int(x)}"

def write_source_tsv(path,df):
    fields=[
        "figure_id","run_id","sample_id","assay_type","run_classification",
        "branch_order","branch_id","branch_label","semantic_group","branch_class",
        "stage_id","metric_name","metric_value","semantic_role","semantic_caveat",
        "source_artifact","generated_at"
    ]
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields,delimiter="\t",lineterminator="\n")
        w.writeheader()
        for _,r in df.iterrows():
            w.writerow({k:r.get(k,"NA") for k in fields})

def write_provenance_tsv(path,cfg,df):
    fields=["key","value"]
    rows=[
        {"key":"figure_id","value":"F3B"},
        {"key":"case_id","value":cfg["case_id"]},
        {"key":"input_f3b_semantic_branching_path","value":cfg["f3b_semantic_branching_path"]},
        {"key":"output_prefix","value":cfg["output_prefix"]},
        {"key":"run_id","value":df["run_id"].iloc[0]},
        {"key":"sample_id","value":df["sample_id"].iloc[0]},
        {"key":"assay_type","value":df["assay_type"].iloc[0]},
        {"key":"run_classification","value":df["run_classification"].iloc[0]},
        {"key":"renderer","value":"generate_case_study_f3b_semantic_branching.py"},
        {"key":"semantic_scope","value":"semantic evidence preservation topology; not clinical interpretation"},
        {"key":"primary_message","value":"VAP preserves multiple biologically meaningful evidence classes and does not naïvely discard noncoding evidence."},
    ]
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields,delimiter="\t",lineterminator="\n")
        w.writeheader()
        w.writerows(rows)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--config",required=True)
    args=ap.parse_args()
    cfg=yaml.safe_load(Path(args.config).read_text())

    case_dir=Path(cfg["case_dir"])
    out_dir=case_dir/"figures"
    out_dir.mkdir(parents=True,exist_ok=True)

    df=read_tsv(Path(cfg["f3b_semantic_branching_path"]))
    required={
        "figure_id","branch_order","branch_id","branch_label","semantic_group",
        "branch_class","metric_value","semantic_caveat","run_id","sample_id",
        "assay_type","run_classification"
    }
    missing=required-set(df.columns)
    if missing:raise ValueError(f"F3B substrate missing required columns: {sorted(missing)}")
    if set(df["figure_id"])!={"F3B"}:raise ValueError("F3B substrate contains non-F3B rows.")

    df=df.sort_values("branch_order").copy()
    df["metric_value"]=pd.to_numeric(df["metric_value"],errors="coerce")
    
    scaling_mode=cfg.get("scaling_mode","sqrt")
    if scaling_mode not in {"sqrt","log2","log10","linear"}:
        raise ValueError(f"Unsupported scaling_mode: {scaling_mode}")    

    if df["metric_value"].isna().any():raise ValueError("Non-parseable metric_value detected.")

    out_prefix=cfg["output_prefix"]
    source_path=out_dir/f"{out_prefix}_source.tsv"
    provenance_path=out_dir/f"{out_prefix}_provenance.tsv"
    write_source_tsv(source_path,df)
    write_provenance_tsv(provenance_path,cfg,df)

    grouped=[]
    for group in semantic_group_order:
        sub=df[df["semantic_group"]==group].copy()
        if not sub.empty:
            grouped.append((group,sub))

    plt.rcParams.update({
        "axes.spines.top":False,
        "axes.spines.right":False,
        "axes.spines.left":False,
        "axes.spines.bottom":False,
        "font.size":10,
        "figure.titlesize":18,
        "axes.titlesize":13,
    })

    fig=plt.figure(figsize=(14,8.5),facecolor="white")
    ax=fig.add_axes([0.08,0.13,0.84,0.72])
    ax.axis("off")

    max_val=df["metric_value"].max()
    x0=0.26
    y_base=0.80
    group_gap=0.29
    bar_gap=0.065
    max_bar_width=0.36

    df["_scaled_width"]=scaled_widths(df["metric_value"].tolist(),scaling_mode,max_bar_width)
    width_lookup=dict(zip(df["branch_id"],df["_scaled_width"]))

    for gi,(group,sub) in enumerate(grouped):
        group_y=y_base-(gi*group_gap)
        group_label=semantic_group_labels.get(group,group)
        group_total=sub["metric_value"].sum()

        ax.text(
            0.02,group_y+0.035,
            group_label,
            ha="left",va="center",
            fontsize=14,
            fontweight="bold",
            color="#263747",
            transform=ax.transAxes
        )
        ax.text(
            0.02,group_y-0.005,
            f"Total: {compact_count(group_total)}",
            ha="left",va="center",
            fontsize=10,
            color=graphite,
            transform=ax.transAxes
        )

        for bi,(_,r) in enumerate(sub.iterrows()):
            y=group_y-(bi*bar_gap)
            value=float(r["metric_value"])
            width=width_lookup[r["branch_id"]]
            color=branch_class_colors.get(r["branch_class"],semantic_overlay)

            ax.add_patch(plt.Rectangle(
                (x0,y-0.018),
                width,
                0.036,
                transform=ax.transAxes,
                color=color,
                alpha=0.86,
                linewidth=0
            ))

            ax.text(
                x0+width+0.015,
                y,
                f"{r['branch_label']}  {compact_count(value)}",
                ha="left",va="center",
                fontsize=10,
                fontweight="normal",
                color="#263747",
                transform=ax.transAxes
            )

            ax.text(
                x0-0.015,
                y,
                str(r["branch_class"]),
                ha="right",va="center",
                fontsize=9,
                color=graphite,
                transform=ax.transAxes
            )

    fig.suptitle(cfg["figure_title"],y=0.955,fontweight="bold",fontsize=20,color="#222222")
    fig.text(
        0.5,0.900,
        "VAP preserves coding and noncoding semantic evidence classes rather than reducing interpretation to a single filter funnel.",
        ha="center",
        fontsize=11,
        color=graphite,
        style="italic"
    )
    fig.text(
        0.5,0.070,
        f"Bar lengths use {scaling_mode} scaling; labels report raw telemetry counts from the F3B sidecar substrate.",
        ha="center",
        fontsize=10,
        color=graphite
    )
    fig.text(
        0.5,0.045,
        "Semantic branches are observational evidence classes, not diagnoses, causal claims, or validation outcomes.",
        ha="center",
        fontsize=9,
        color=graphite
    )
    fig.text(
        0.5,0.022,
        "Generated deterministically from metrics/figure_f3b_semantic_branching.tsv.",
        ha="center",
        fontsize=9,
        color=graphite
    )

    png=out_dir/f"{out_prefix}.png"
    pdf=out_dir/f"{out_prefix}.pdf"
    plt.savefig(png,dpi=300,bbox_inches="tight",facecolor="white")
    with PdfPages(pdf) as p:p.savefig(fig,bbox_inches="tight",facecolor="white")
    plt.close(fig)

    print(f"Wrote {png}")
    print(f"Wrote {pdf}")
    print(f"Wrote {source_path}")
    print(f"Wrote {provenance_path}")

if __name__=="__main__":main()