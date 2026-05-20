#!/usr/bin/env python3
from pathlib import Path
import argparse,csv,yaml
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

def require_file(path):
    if not path.exists():raise FileNotFoundError(f"Required file not found: {path}")

def read_tsv(path):
    require_file(path)
    return pd.read_csv(path,sep="\t")

def seconds_to_hours(x):
    return float(x)/3600

def compact_hours(x):
    return f"{x:.1f}"

def write_source_tsv(path,rows):
    fields=["figure_id","panel_id","metric","run_id","stage","value","unit","source_table","transformation_rule"]
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields,delimiter="\t",lineterminator="\n")
        w.writeheader()
        for r in rows:w.writerow({k:r.get(k,"NA") for k in fields})

def runtime_ceiling(hours):
    if hours<=6:return 6
    if hours<=30:return 30
    if hours<=60:return 60
    return ((int(hours)//25)+2)*25

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--config",required=True)
    args=ap.parse_args()
    cfg=yaml.safe_load(Path(args.config).read_text())

    case_dir=Path(cfg["case_dir"])
    table_dir=case_dir/"tables"
    out_dir=case_dir/"figures"
    out_dir.mkdir(parents=True,exist_ok=True)

    runtime=read_tsv(table_dir/"runtime_stage_summary.tsv")
    repro=read_tsv(table_dir/"run_reproducibility_summary.tsv")

    required_cols={"sample_id","run_id","stage","elapsed_seconds"}
    missing=required_cols-set(runtime.columns)
    if missing:raise ValueError(f"runtime_stage_summary.tsv missing required columns: {sorted(missing)}")

    rt=runtime[runtime["sample_id"]==cfg["case_id"]].copy()
    if rt.empty:raise ValueError(f"No runtime rows found for case_id={cfg['case_id']}")

    rt["elapsed_seconds"]=pd.to_numeric(rt["elapsed_seconds"],errors="coerce")
    if rt["elapsed_seconds"].isna().any():raise ValueError("Non-parseable elapsed_seconds values detected.")

    run_ids=sorted(rt["run_id"].unique())

    if len(run_ids) not in (1,2):
        raise ValueError(
            f"Expected one or two runs for F2 comparison; "
            f"found {len(run_ids)}: {run_ids}"
        )

    comparison_mode="single_run" if len(run_ids)==1 else "paired_runs"

    run_a=run_ids[0]
    run_b=run_ids[1] if len(run_ids)==2 else None

    totals=rt.groupby("run_id")["elapsed_seconds"].sum().reindex(run_ids)
    totals_h=totals.apply(seconds_to_hours)

    stage_pivot=rt.pivot_table(index="stage",columns="run_id",values="elapsed_seconds",aggfunc="sum",fill_value=0)
    stage_pivot=stage_pivot.reindex(columns=run_ids)
    stage_pivot["combined_seconds"]=stage_pivot.sum(axis=1)
    stage_pivot["stage_order"]=stage_pivot.index.to_series().str.extract(r"stage_(\d+)").astype(int).values
    stage_pivot=stage_pivot.sort_values("stage_order",ascending=False)

    top_stages=stage_pivot.sort_values("combined_seconds",ascending=False).head(5).copy()
    top_stages=top_stages.sort_values("combined_seconds",ascending=True)

    source_rows=[]
    for rid,val in totals.items():
        source_rows.append({"figure_id":"F2","panel_id":"B","metric":"total_runtime_seconds","run_id":rid,"stage":"all","value":val,"unit":"seconds","source_table":"runtime_stage_summary.tsv","transformation_rule":"sum elapsed_seconds by run_id"})
    for stage,row in stage_pivot.iterrows():
        for rid in run_ids:
            source_rows.append({"figure_id":"F2","panel_id":"C","metric":"stage_runtime_seconds","run_id":rid,"stage":stage,"value":row[rid],"unit":"seconds","source_table":"runtime_stage_summary.tsv","transformation_rule":"sum elapsed_seconds by stage and run_id"})
    source_path=out_dir/f"{cfg['output_prefix']}_source.tsv"
    write_source_tsv(source_path,source_rows)

    plt.rcParams.update({"axes.spines.top":False,"axes.spines.right":False,"font.size":10,"axes.titlesize":14,"figure.titlesize":18})
    fig=plt.figure(figsize=(14,8.8),facecolor="white")
    fig.subplots_adjust(left=0.055,right=0.975,top=0.82,bottom=0.13)
    gs=fig.add_gridspec(2,2,width_ratios=[1,1],height_ratios=[1,1],wspace=0.28,hspace=0.32)

    # Panel A
    ax1=fig.add_subplot(gs[0,0])
    ax1.axis("off")

    identity=[
        ["Case",cfg["case_id"]],
        ["Comparison",cfg["comparison_label"]],
        ["Mode","paired runs" if comparison_mode=="paired_runs" else "single run"],
        ["Run A",run_a],
    ]

    if comparison_mode=="paired_runs":
        identity.append(["Run B",run_b])

    identity.append(["Telemetry rows",f"{len(rt):,}"])

    tbl=ax1.table(cellText=identity,colLabels=["Field","Value"],loc="center",cellLoc="left",colLoc="left",colWidths=[0.34,0.64],bbox=[0.00,0.02,0.98,0.78])
    tbl.auto_set_font_size(False);tbl.set_fontsize(9)
    for c in range(2):tbl[(0,c)].set_text_props(weight="bold")
    for (_, _), cell in tbl.get_celld().items():
        cell.set_edgecolor("#B8B8B8");cell.set_linewidth(0.6)
    ax1.text(-0.02,1.04,"A  Execution identity",transform=ax1.transAxes,ha="left",va="bottom",fontsize=14,fontweight="bold")

    # Panel B
    ax2=fig.add_subplot(gs[0,1])
    runtime_dark="#4F81BD";runtime_light="#7FA6D9"

    if comparison_mode=="paired_runs":
        runtime_x=[0,0.52]
        runtime_colors=[runtime_dark,runtime_light]
        runtime_labels=["Run A","Run B"]
        ax2.set_xlim(-0.28,0.80)
    else:
        runtime_x=[0]
        runtime_colors=[runtime_dark]
        runtime_labels=["Run A"]
        ax2.set_xlim(-0.35,0.35)

    bars=ax2.bar(
        runtime_x,
        totals_h.values,
        color=runtime_colors,
        width=0.28
    )

    ax2.set_xticks(runtime_x)
    ax2.set_xticklabels(runtime_labels)    
    
    ax2.set_ylabel("Total runtime (hours)")
    ax2.set_ylim(0,runtime_ceiling(max(totals_h.values)))
    ax2.grid(axis="y",alpha=0.25);ax2.set_axisbelow(True)
    for bar,v in zip(bars,totals_h.values):
        ax2.text(bar.get_x()+bar.get_width()/2,v+max(totals_h.values)*0.025,compact_hours(v),ha="center",va="bottom",fontsize=10)
    ax2.text(-0.02,1.04,"B  Total runtime",transform=ax2.transAxes,ha="left",va="bottom",fontsize=14,fontweight="bold")

    # Panel C
    ax3=fig.add_subplot(gs[1,0])
    stages=stage_pivot.index.tolist()
    y=range(len(stages))

    if comparison_mode=="paired_runs":
        run_a_h=[seconds_to_hours(v) for v in stage_pivot[run_a]]
        run_b_h=[seconds_to_hours(v) for v in stage_pivot[run_b]]

        ax3.barh([i-0.18 for i in y],run_a_h,height=0.32,label="Run A",color="#5B4B9A",alpha=0.88)
        ax3.barh([i+0.18 for i in y],run_b_h,height=0.32,label="Run B",color="#9B8AD1",alpha=0.88)
        ax3.legend(
            frameon=False,
            loc="upper left",
            bbox_to_anchor=(0.73,1.1),
            ncol=2,
            fontsize=8,
            borderaxespad=0.0,
            handlelength=1.8,
            handletextpad=0.5,
            columnspacing=1.2
        )
    else:
        run_a_h=[seconds_to_hours(v) for v in stage_pivot[run_a]]
        ax3.barh(list(y),run_a_h,height=0.42,label="Run A",color="#5B4B9A",alpha=0.88)

    ax3.tick_params(axis="y",labelsize=8,pad=2)
    ax3.set_yticks(list(y))
    ax3.set_yticklabels(stages,fontsize=8)
    ax3.set_xlabel("Runtime (hours)")
    ax3.grid(axis="x",alpha=0.25)
    ax3.set_axisbelow(True)
    ax3.text(
        -0.02,
        1.035,
        "C  Stage runtime decomposition",
        transform=ax3.transAxes,
        ha="left",
        va="bottom",
        fontsize=14,
        fontweight="bold"
    )

    # Panel D
    ax4=fig.add_subplot(gs[1,1])
    top_labels=top_stages.index.tolist()
    top_combined_h=[seconds_to_hours(v) for v in top_stages["combined_seconds"]]
    ax4.barh(top_labels,top_combined_h,color="#6E8FB2",alpha=0.85)
    ax4.set_xlabel("Combined runtime (hours)")
    ax4.grid(axis="x",alpha=0.25);ax4.set_axisbelow(True)
    ax4.tick_params(axis="y",labelsize=8)
    for i,v in enumerate(top_combined_h):
        ax4.text(v+max(top_combined_h)*0.02,i,f"{v:.1f}",va="center",fontsize=8)
    ax4.text(-0.02,1.04,"D  Top runtime-contributing stages",transform=ax4.transAxes,ha="left",va="bottom",fontsize=14,fontweight="bold")
    ax4.set_xlabel("Combined runtime (hours)" if comparison_mode=="paired_runs" else "Runtime (hours)")

    fig.suptitle(cfg["figure_title"],y=0.975,fontweight="bold",fontsize=18)
    fig.text(0.5,0.925,"Stage-resolved telemetry summarizes runtime observability, not performance benchmarking.",ha="center",fontsize=12,color="#444444")
    fig.text(0.5,0.055,"Generated deterministically from case-study TSV artifacts. Runtime observability only; not optimization or benchmarking.",ha="center",fontsize=9,color="#555555")

    png=out_dir/f"{cfg['output_prefix']}.png"
    pdf=out_dir/f"{cfg['output_prefix']}.pdf"
    plt.savefig(png,dpi=300,bbox_inches="tight",facecolor="white")
    with PdfPages(pdf) as p:p.savefig(fig,bbox_inches="tight",facecolor="white")
    plt.close(fig)
    print(f"Wrote {png}")
    print(f"Wrote {pdf}")
    print(f"Wrote {source_path}")

if __name__=="__main__":main()