#!/usr/bin/env python3
from pathlib import Path
import argparse,csv,yaml
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.ticker import FuncFormatter

def require_file(path):
    if not path.exists():raise FileNotFoundError(f"Required file not found: {path}")

def read_tsv(path):
    require_file(path)
    return pd.read_csv(path,sep="\t")

def seconds_to_hours(x):
    return round(float(x)/3600,1)

def write_source_tsv(path,rows):
    fields=["figure_id","panel_id","metric","run_a_value","run_b_value","unit","comparison_interpretation","source_table","transformation_rule"]
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields,delimiter="\t",lineterminator="\n")
        w.writeheader()
        for r in rows:w.writerow({k:r.get(k,"NA") for k in fields})

def runtime_ceiling(hours):
    if hours <= 6:return 6
    if hours <= 30:return 30
    if hours <= 60:return 60
    return ((int(hours)//25)+2)*25

def row_count_ceiling(rows):
    if rows <= 1_000_000:return 1_000_000
    if rows <= 5_000_000:return 6_000_000
    return ((int(rows)//1_000_000)+2)*1_000_000

def count_formatter(x,pos):
    if x==0:return "0"
    if x>=1_000_000:return f"{x/1_000_000:.1f}M"
    return f"{int(x/1000):,}k"

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--config",required=True)
    args=ap.parse_args()
    cfg=yaml.safe_load(Path(args.config).read_text())
    case_dir=Path(cfg["case_dir"])
    table_dir=case_dir/"tables"
    out_dir=case_dir/"figures"
    out_dir.mkdir(parents=True,exist_ok=True)

    repro=read_tsv(table_dir/"run_reproducibility_summary.tsv")
    runtime=read_tsv(table_dir/"runtime_stage_summary.tsv")
    # priority=read_tsv(table_dir/"priority_tier_summary.tsv")
    # interpretation=read_tsv(table_dir/"interpretation_label_summary.tsv")
    funnel=read_tsv(table_dir/"stage_funnel_summary.tsv")

    comp=repro[(repro["sample_id"]==cfg["case_id"]) & (repro["comparison_id"]==cfg["comparison_id"])]
    if len(comp)!=1:raise ValueError(f"Expected exactly one comparison row for {cfg['case_id']} / {cfg['comparison_id']}; found {len(comp)}")
    comp=comp.iloc[0]
    run_a=comp["run_id_a"];run_b=comp["run_id_b"]

    rt=runtime[runtime["run_id"].isin([run_a,run_b])].copy()
    if rt.empty:raise ValueError("No runtime rows found for comparison runs.")
    rt["elapsed_seconds"]=pd.to_numeric(rt["elapsed_seconds"],errors="coerce")
    rt_totals=rt.groupby("run_id")["elapsed_seconds"].sum().to_dict()
    run_a_runtime=rt_totals.get(run_a,0)
    run_b_runtime=rt_totals.get(run_b,0)

    fn=funnel[funnel["run_id"].isin([run_a,run_b])].copy()
    if len(fn)!=2:raise ValueError(f"Expected two funnel rows; found {len(fn)}")
    fna=fn[fn["run_id"]==run_a].iloc[0]
    fnb=fn[fn["run_id"]==run_b].iloc[0]

    source_rows=[
        {"figure_id":"F1","panel_id":"B","metric":"total_runtime_seconds","run_a_value":run_a_runtime,"run_b_value":run_b_runtime,"unit":"seconds","comparison_interpretation":"runtime variability expected","source_table":"runtime_stage_summary.tsv","transformation_rule":"sum elapsed_seconds by run_id"},
        {"figure_id":"F1","panel_id":"C","metric":"stage_11_prioritized_rows","run_a_value":fna["stage11_prioritized_rows"],"run_b_value":fnb["stage11_prioritized_rows"],"unit":"rows","comparison_interpretation":"stable" if fna["stage11_prioritized_rows"]==fnb["stage11_prioritized_rows"] else "divergent","source_table":"stage_funnel_summary.tsv","transformation_rule":"extract stage11_prioritized_rows by run_id"},
        {"figure_id":"F1","panel_id":"C","metric":"stage_12_validation_rows","run_a_value":fna["stage12_validation_rows"],"run_b_value":fnb["stage12_validation_rows"],"unit":"rows","comparison_interpretation":"stable" if fna["stage12_validation_rows"]==fnb["stage12_validation_rows"] else "divergent","source_table":"stage_funnel_summary.tsv","transformation_rule":"extract stage12_validation_rows by run_id"},
        {"figure_id":"F1","panel_id":"D","metric":"priority_summary_match","run_a_value":comp["priority_summary_match"],"run_b_value":comp["priority_summary_match"],"unit":"boolean","comparison_interpretation":"stable","source_table":"run_reproducibility_summary.tsv","transformation_rule":"semantic equality from harvester"},
        {"figure_id":"F1","panel_id":"D","metric":"interpretation_summary_match","run_a_value":comp["interpretation_summary_match"],"run_b_value":comp["interpretation_summary_match"],"unit":"boolean","comparison_interpretation":"stable","source_table":"run_reproducibility_summary.tsv","transformation_rule":"semantic equality from harvester"},
        {"figure_id":"F1","panel_id":"D","metric":"gene_burden_match","run_a_value":comp["gene_burden_match"],"run_b_value":comp["gene_burden_match"],"unit":"boolean","comparison_interpretation":"stable","source_table":"run_reproducibility_summary.tsv","transformation_rule":"semantic equality from harvester"}
    ]

    out_prefix=cfg["output_prefix"]
    source_path=out_dir/f"{out_prefix}_source.tsv"
    write_source_tsv(source_path,source_rows)

    plt.rcParams.update({
        "axes.spines.top":False,
        "axes.spines.right":False,
        "font.size":10,
        "axes.titlesize":14,
        "figure.titlesize":18
    })

    # Main Geometry
    # Create figure and subplots with manual layout adjustments for title/label spacing
    fig=plt.figure(figsize=(14,8.8),facecolor="white")
    fig.subplots_adjust(left=0.055,right=0.975,top=0.82,bottom=0.13)
    gs=fig.add_gridspec(
        2,2,
        width_ratios=[1,1],
        height_ratios=[1,1],
        wspace=0.26,
        hspace=0.28
    )

    # Panel A: Execution identity and overall reproducibility status
    ax1=fig.add_subplot(gs[0,0])
    ax1.axis("off")
    identity=[
        ["Case",cfg["case_id"]],
        ["Comparison",cfg["comparison_label"]],
        ["Run A",run_a],
        ["Run B",run_b],
        ["Status",comp["overall_reproducibility_status"]]
    ]
    tbl=ax1.table(
        cellText=identity,
        colLabels=["Field","Value"],
        loc="center",
        cellLoc="left",
        colLoc="left",
        colWidths=[0.36,0.62],
        bbox=[0.00,0.02,0.98,0.78]
    )
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(9)
    for c in range(2):
        tbl[(0,c)].set_text_props(weight="bold")
    for (_, _), cell in tbl.get_celld().items():
        cell.set_edgecolor("#B8B8B8")
        cell.set_linewidth(0.6)
    ax1.text(-0.02,1.04,"A  Execution identity",transform=ax1.transAxes,
         ha="left",va="bottom",fontsize=14,fontweight="bold")

    # Panel B: Runtime variability
    ax2=fig.add_subplot(gs[0,1])
    runtime_dark="#4F81BD"
    runtime_light="#7FA6D9"
    runtime_x=[0,0.52]
    runtime_vals=[seconds_to_hours(run_a_runtime),seconds_to_hours(run_b_runtime)]
    bars=ax2.bar(runtime_x,runtime_vals,color=[runtime_dark,runtime_light],width=0.28)
    ax2.set_xlim(-0.28,0.80)
    ax2.set_xticks(runtime_x)
    ax2.set_xticklabels(["Run A","Run B"])
    ax2.set_ylabel("Total runtime (hours)")
    runtime_ymax=runtime_ceiling(max(runtime_vals))
    ax2.set_ylim(0,runtime_ymax)
    ax2.text(-0.02,1.04,"B  Runtime variability",transform=ax2.transAxes,
         ha="left",va="bottom",fontsize=14,fontweight="bold")
    ax2.grid(axis="y",alpha=0.25)
    ax2.set_axisbelow(True)
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    for bar,v in zip(bars,runtime_vals):
        ax2.text(bar.get_x()+bar.get_width()/2,v+0.08,f"{v:.1f}",ha="center",va="bottom",fontsize=10)

    # Panel C: Structural stability of evidence prioritization and validation rows
    ax3=fig.add_subplot(gs[1,0])

    stage11_a=int(fna["stage11_prioritized_rows"])
    stage11_b=int(fnb["stage11_prioritized_rows"])
    stage12_a=int(fna["stage12_validation_rows"])
    stage12_b=int(fnb["stage12_validation_rows"])

    struct_metrics=["Stage 11 rows","Stage 12 rows"]
    a_vals=[stage11_a,stage12_a]
    b_vals=[stage11_b,stage12_b]
    deltas=[stage11_b-stage11_a,stage12_b-stage12_a]

    x=[0,0.78]
    width=0.18
    gap=0.025
    struct_dark="#5B4B9A"
    struct_light="#9B8AD1"

    bars_a=ax3.bar([i-width/2-gap for i in x],a_vals,width,label="Run A",color=struct_dark,alpha=0.88)
    bars_b=ax3.bar([i+width/2+gap for i in x],b_vals,width,label="Run B",color=struct_light,alpha=0.88)
    ax3.set_xlim(-0.32,1.10)

    ax3.set_xticks(x)
    ax3.set_xticklabels(struct_metrics)
    ax3.set_ylabel("Rows")
    struct_ymax=row_count_ceiling(max(a_vals+b_vals))
    ax3.set_ylim(0,struct_ymax)
    ax3.yaxis.set_major_formatter(FuncFormatter(count_formatter))
    ax3.text(-0.02,1.015,"C  Structural stability (rows)",transform=ax3.transAxes,
         ha="left",va="bottom",fontsize=14,fontweight="bold")
    ax3.grid(axis="y",alpha=0.25)
    ax3.set_axisbelow(True)
    ax3.spines["top"].set_visible(False)
    ax3.spines["right"].set_visible(False)

    for i,a,b,d in zip(x,a_vals,b_vals,deltas):
        left=i-width/2-gap
        right=i+width/2+gap
        offset=struct_ymax*0.025
        bracket_y=max(a,b)+struct_ymax*0.08
        stem_y=max(a,b)+struct_ymax*0.05
        ax3.text(i,bracket_y+offset,f"Δ = {d:,}",ha="center",va="bottom",fontsize=9)        
        ax3.text(left,a+struct_ymax*0.025,f"{a:,}",ha="center",va="bottom",fontsize=8)
        ax3.text(right,b+struct_ymax*0.025,f"{b:,}",ha="center",va="bottom",fontsize=8)        

    ax3.legend(
        frameon=False,
        loc="upper left",
        bbox_to_anchor=(0.625,1.105),
        ncol=2,
        handlelength=1.8,
        columnspacing=1.8,
        handletextpad=0.6,
        borderaxespad=0.0
    )    
    
    ax3.text(
        0.5,-0.115,
        "Δ = Run B − Run A",
        transform=ax3.transAxes,
        ha="center",
        va="top",
        fontsize=7,
        alpha=0.62
    )

    # Panel D: Semantic stability checklist
    ax4=fig.add_subplot(gs[1,1])
    ax4.axis("off")
    checks=[
        ["Priority tiers",comp["priority_summary_match"]],
        ["Validation readiness",comp["validation_summary_match"]],
        ["Interpretation labels",comp["interpretation_summary_match"]],
        ["Gene burden",comp["gene_burden_match"]]
    ]
    checks=[[k,"stable" if str(v)=="True" else "divergent"] for k,v in checks]
    tbl2=ax4.table(
        cellText=checks,
        colLabels=["Evidence layer","Semantic status"],
        loc="center",
        cellLoc="left",
        colLoc="left",
        # Panel D table bbox
        bbox=[0.00,0.08,0.98,0.70]
    )
    tbl2.auto_set_font_size(False)
    tbl2.set_fontsize(10)
    for c in range(2):
        tbl2[(0,c)].set_text_props(weight="bold")
    for (_, _), cell in tbl2.get_celld().items():
        cell.set_edgecolor("#B8B8B8")
        cell.set_linewidth(0.6)
    ax4.text(-0.02,1.04,"D  Semantic stability checklist",transform=ax4.transAxes,
         ha="left",va="bottom",fontsize=14,fontweight="bold")

    fig.suptitle(cfg["figure_title"],y=0.975,fontweight="bold",fontsize=18)
    fig.text(
        0.5,0.925,
        "Operational variability with stable downstream biological evidence organization",
        ha="center",
        fontsize=12,
        color="#444444"
    )
    fig.text(
        0.5,0.055,
        "Generated deterministically from case-study TSV artifacts. Operational reproducibility only; not clinical interpretation.",
        ha="center",
        fontsize=9,
        color="#555555"
    )    

    # Save outputs
    png=out_dir/f"{out_prefix}.png"
    pdf=out_dir/f"{out_prefix}.pdf"
    plt.savefig(png,dpi=300,bbox_inches="tight",facecolor="white")
    with PdfPages(pdf) as p:p.savefig(fig,bbox_inches="tight",facecolor="white")
    plt.close(fig)
    print(f"Wrote {png}")
    print(f"Wrote {pdf}")
    print(f"Wrote {source_path}")

if __name__=="__main__":main()