#!/usr/bin/env python3
from pathlib import Path
import argparse
import math
import pandas as pd
import matplotlib.pyplot as plt
import yaml

def read_collapsed_f4_table(path:Path)->pd.DataFrame:
    path=Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Collapsed F4 table not found: {path}")
    df=pd.read_csv(path,sep="\t")
    required={
        "figure_id",
        "semantic_domain",
        "collapsed_label",
        "collapsed_metric_value",
    }
    missing=required-set(df.columns)
    if missing:
        raise ValueError(f"Collapsed F4 table missing required columns: {sorted(missing)}")
    df["collapsed_metric_value"]=pd.to_numeric(df["collapsed_metric_value"],errors="coerce")
    if df["collapsed_metric_value"].isna().any():
        raise ValueError("Non-numeric collapsed_metric_value detected.")
    return df

def compact_count(x:int|float)->str:
    x=float(x)
    if x>=1_000_000:
        return f"{x/1_000_000:.2f}M"
    if x>=1_000:
        return f"{x/1_000:.1f}k"
    return str(int(x))

def autopct_factory(values:list[float],min_percent:float):
    total=sum(values)
    def _autopct(pct):
        if pct<min_percent:
            return ""
        value=int(round((pct/100.0)*total))
        return f"{pct:.1f}%\n{compact_count(value)}"
    return _autopct


# def autopct_factory(values:list[float]):
#     total=sum(values)
#     def _autopct(pct):
#         value=int(round((pct/100.0)*total))
#         return f"{pct:.1f}%\n{compact_count(value)}"
#     return _autopct


def format_percent(pct:float)->str:
    if pct==0:
        return "0.0%"
    if pct<0.05:
        return "<0.1%"
    return f"{pct:.1f}%"


def add_slice_callouts(ax,wedges,labels,values,pie_center_y:float=-0.18,pie_radius:float=0.88):
    total=sum(values)
    large=[]
    tiny=[]

    for wedge,label,value in zip(wedges,labels,values):
        pct=(value/total)*100
        theta=(wedge.theta1+wedge.theta2)/2.0
        x=math.cos(math.radians(theta))
        y=math.sin(math.radians(theta))
        item={"theta":theta,"x":x,"y":y,"label":label,"value":value,"pct":pct}
        if pct>=4.0 or (len(values)>=6 and pct>=2.0 and x>=0):
            large.append(item)
        else:
            tiny.append(item)

    def draw_item(item,x_text,y_text,side:int,anchor_theta:float|None=None):
        theta=item["theta"] if anchor_theta is None else anchor_theta
        x=math.cos(math.radians(theta))
        y=math.sin(math.radians(theta))

        x_start=pie_radius*x
        y_start=pie_center_y+(pie_radius*y)
        x_radial=pie_radius*1.10*x
        y_radial=pie_center_y+(pie_radius*1.10*y)

        ha="left" if side>0 else "right"

        ax.plot(
            [x_start,x_radial,x_text-(0.03*side)],
            [y_start,y_radial,y_text],
            color="black",
            linewidth=0.7,
            solid_capstyle="butt",
        )

        ax.text(
            x_text,
            y_text,
            f"{item['label']}: {format_percent(item['pct'])} ({compact_count(item['value'])})",
            ha=ha,
            va="center",
            fontsize=7,
        )

    for item in large:
        side=1 if item["x"]>=0 else -1
        x_text=1.16*side
        y_text=pie_center_y+(pie_radius*1.08*item["y"])

        if item["label"]=="likely_benign":
            x_text=1.22
            y_text=pie_center_y+(pie_radius*0.92*item["y"])

        draw_item(item,x_text,y_text,side)

    tiny=sorted(tiny,key=lambda d:d["y"],reverse=True)
    tiny_left=tiny[0::2]
    tiny_right=tiny[1::2]

    def draw_tiny_stack(items,side:int):
        x_text=1.62*side
        y_top=1.30
        y_gap=0.20

        if side<0:
            anchor_angles=[102,108,114,120,126,132,138,144]
        else:
            anchor_angles=[78,72,66,60,54,48,42,36]

        for i,item in enumerate(items):
            y_text=y_top-(i*y_gap)
            anchor_theta=anchor_angles[min(i,len(anchor_angles)-1)]
            draw_item(item,x_text,y_text,side,anchor_theta=anchor_theta)

    draw_tiny_stack(tiny_left,-1)
    draw_tiny_stack(tiny_right,1)



def render_semantic_pie_chart(
    *,
    ax,
    df:pd.DataFrame,
    semantic_domain:str,
    title:str,
    label_order:list[str]|None=None,
    min_percent_for_slice_label:float=4.0,
)->dict[str,int]:
    sub=df[df["semantic_domain"]==semantic_domain].copy()
    if sub.empty:
        raise ValueError(f"No rows found for semantic_domain={semantic_domain}")

    grouped=(
        sub.groupby("collapsed_label",as_index=False)["collapsed_metric_value"]
        .sum()
    )

    if label_order is not None:
        order={label:i for i,label in enumerate(label_order)}
        grouped["_order"]=grouped["collapsed_label"].map(lambda x:order.get(x,len(order)))
        grouped=grouped.sort_values(["_order","collapsed_label"])
    else:
        grouped=grouped.sort_values("collapsed_metric_value",ascending=False)

    labels=grouped["collapsed_label"].tolist()
    values=grouped["collapsed_metric_value"].astype(float).tolist()

    wedges,texts=ax.pie(
        values,
        labels=None,
        autopct=None,
        startangle=90,
        counterclock=False,
        center=(0,-0.18),
        radius=0.88,
        wedgeprops={"linewidth":0.8,"edgecolor":"white"},
        textprops={"fontsize":8},
    )

    add_slice_callouts(
        ax=ax,
        wedges=wedges,
        labels=labels,
        values=values,
        pie_center_y=-0.18,
        pie_radius=0.88,
    )

    legend_labels=[
        f"{label} — {format_percent((value/sum(values))*100)} ({compact_count(value)})"
        for label,value in zip(labels,values)
    ]

    ax.legend(
        wedges,
        legend_labels,
        title="Collapsed category",
        loc="lower right",
        bbox_to_anchor=(1.32,0.02),
        fontsize=8,
        title_fontsize=9,
        frameon=False,
    )

    ax.set_title(title,fontsize=12,fontweight="bold",pad=14)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlim(-1.95,2.20)
    ax.set_ylim(-1.35,1.55)

    return dict(zip(labels,[int(v) for v in values]))

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--config",help="YAML config for F4 semantic category rendering.")
    parser.add_argument("--input",help="Collapsed F4 semantic composition TSV.")
    parser.add_argument("--semantic-domain",choices=[
        "consequence",
        "clinvar_significance",
        "population_frequency_bin",
    ])
    parser.add_argument("--title")
    parser.add_argument("--output")
    args=parser.parse_args()

    cfg={}
    if args.config:
        cfg=yaml.safe_load(Path(args.config).read_text())
        if cfg is None:
            cfg={}

    input_path=args.input or cfg.get("input")
    semantic_domain=args.semantic_domain or cfg.get("semantic_domain")
    title=args.title or cfg.get("title")
    output_path=args.output or cfg.get("output")

    missing=[
        name for name,value in {
            "input":input_path,
            "semantic_domain":semantic_domain,
            "title":title,
            "output":output_path,
        }.items()
        if not value
    ]
    if missing:
        raise ValueError(f"Missing required F4 render parameter(s): {missing}")

    df=read_collapsed_f4_table(Path(input_path))

    orders={
        "clinvar_significance":[
            "benign",
            "likely_benign",
            "uncertain_significance",
            "likely_pathogenic",
            "pathogenic",
            "conflicting_classifications",
        ],
        "population_frequency_bin":[
            "rare",
            "low_frequency",
            "common",
            "missing",
        ],
    }

    fig,ax=plt.subplots(figsize=(8.5,6),facecolor="white")

    render_semantic_pie_chart(
        ax=ax,
        df=df,
        semantic_domain=semantic_domain,
        title=title,
        label_order=orders.get(semantic_domain),
    )

    fig.text(
        0.01,
        0.01,
        "Note: categories reflect semantic collapse of source annotations into normalized readership-facing labels.",
        ha="left",
        va="bottom",
        fontsize=7,
    )

    output=Path(output_path)
    output.parent.mkdir(parents=True,exist_ok=True)
    plt.savefig(output,dpi=300,bbox_inches="tight",facecolor="white")
    plt.close(fig)
    print(f"Wrote: {output}")

if __name__=="__main__":
    main()