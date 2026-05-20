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

    plt.rcParams.update({"axes.spines.top":False,"axes.spines.right":False,"font.size":10,"axes.titlesize":12,"figure.titlesize":15})
    fig=plt.figure(figsize=(14,8.6),facecolor="white",constrained_layout=False)
    gs=fig.add_gridspec(2,2,hspace=0.30,wspace=0.34)

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
    tbl=ax1.table(cellText=identity,colLabels=["Field","Value"],loc="center",cellLoc="left",colLoc="left")
    for c in range(2):
        tbl[(0,c)].set_text_props(weight="bold")
    tbl.auto_set_font_size(False);tbl.set_fontsize(9);tbl.scale(1.05,1.75)
    ax1.set_title("A  Execution identity",loc="left",pad=12,fontweight="bold")
    for (_, _), cell in tbl.get_celld().items():
        cell.set_edgecolor("#B8B8B8")
        cell.set_linewidth(0.6)

    # Panel B: Runtime variability
    ax2=fig.add_subplot(gs[0,1])
    runtime_dark="#4F81BD"
    runtime_light="#7FA6D9"
    runtime_x=[0,0.82]
    ax2.bar(runtime_x,[seconds_to_hours(run_a_runtime),seconds_to_hours(run_b_runtime)],color=[runtime_dark,runtime_light],width=0.5)
    ax2.set_xticks(runtime_x)
    ax2.set_xticklabels(["Run A","Run B"])    
    
    ax2.set_ylabel("Total runtime (hours)")
    ax2.set_ylim(0,6)
    ax2.set_title("B  Runtime variability",x=-0.13,pad=12,fontweight="bold")
    ax2.grid(axis="y",alpha=0.2)
    for i,v in enumerate([seconds_to_hours(run_a_runtime),seconds_to_hours(run_b_runtime)]):
        ax2.text(i,v,f"{v:.1f}",ha="center",va="bottom",fontsize=9)


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

    x=[0,1.08]
    width=0.26
    max_val=max(a_vals+b_vals)

    struct_dark="#5B4B9A"
    struct_light="#9B8AD1"
    ax3.bar([i-width/2 for i in x],a_vals,width,label="Run A",color=struct_dark,alpha=0.88)
    ax3.bar([i+width/2 for i in x],b_vals,width,label="Run B",color=struct_light,alpha=0.88)

    ax3.set_xticks(list(x))
    ax3.set_xticklabels(struct_metrics)
    ax3.set_ylabel("Rows")
    ax3.set_ylim(0,1000000)
    ax3.yaxis.set_major_formatter(FuncFormatter(lambda x,pos: "0" if x==0 else f"{int(x/1000):,}k"))
    ax3.set_title("C  Structural stability (rows)",x=-0.13,pad=12,fontweight="bold")
    ax3.grid(axis="y",alpha=0.16)
    ax3.set_axisbelow(True)
    # Annotate bars with values and deltas
    for i,(a,b,d) in enumerate(zip(a_vals,b_vals,deltas)):
        left=i-width/2
        right=i+width/2
        y=max(a,b)*1.08
        bracket_y=max(a,b)*1.14
        # Annotate bars with values and deltas
        ax3.text(left,a+20000,f"{a:,}",ha="center",va="bottom",fontsize=8)
        ax3.text(right,b+20000,f"{b:,}",ha="center",va="bottom",fontsize=8)
        # Draw delta bracket
        ax3.plot([left,left,right,right],[bracket_y-25000,bracket_y,bracket_y,bracket_y-25000],color="#333333",linewidth=0.9)
        ax3.text(i,bracket_y+15000,f"Δ = {d:,}",ha="center",va="bottom",fontsize=9)
    
    # Add legend
    ax3.legend(frameon=False,loc="upper center",bbox_to_anchor=(0.55,1.16),ncol=2)
    ax3.text(0.5,-0.18,"Δ = Run B − Run A",transform=ax3.transAxes,ha="center",va="top",fontsize=8,alpha=0.65)
    
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
    tbl2=ax4.table(cellText=checks,colLabels=["Evidence layer","Semantic status"],loc="center",cellLoc="left",colLoc="left")
    for c in range(2):
        tbl2[(0,c)].set_text_props(weight="bold")
    tbl2.auto_set_font_size(False);tbl2.set_fontsize(10);tbl2.scale(1.05,1.7)
    ax4.set_title("D  Semantic stability checklist",loc="left",pad=12,fontweight="bold")
    for (_, _), cell in tbl2.get_celld().items():
        cell.set_edgecolor("#B8B8B8")
        cell.set_linewidth(0.6)
    
    fig.suptitle(cfg["figure_title"],y=0.98,fontweight="bold")
    fig.text(0.5,0.935,"Operational variability with stable downstream biological evidence organization",ha="center",fontsize=10,alpha=0.75)
    fig.text(0.5,0.02,"Generated deterministically from case-study TSV artifacts. Operational reproducibility only; not clinical interpretation.",ha="center",fontsize=9,alpha=0.65)

    # Prevent title/label overlap with tight layout by using constrained_layout=False and manual adjustments
    plt.subplots_adjust(left=0.08,right=0.97,top=0.88,bottom=0.10)
    
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