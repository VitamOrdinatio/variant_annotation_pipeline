#!/usr/bin/env python3
from pathlib import Path
import argparse
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import yaml


RDGP_REQUIRED_COLUMNS={
    "gene_symbol",
    "variant_count",
    "high_impact_variant_count",
    "rare_variant_count",
    "pathogenic_variant_count",
    "max_variant_severity",
}

VDB_REQUIRED_COLUMNS={
    "variant_id",
    "chromosome",
    "position",
    "consequence",
    "clinical_significance",
    "population_frequency",
    "variant_context",
    "variant_effect_severity",
    "interpretability_status",
    "frequency_status",
    "clinical_status",
}

def validate_input(path:Path,required_columns:set[str])->pd.DataFrame:
    path=Path(path)

    if not path.exists():
        raise FileNotFoundError(f"Input TSV not found: {path}")

    df=pd.read_csv(path,sep="\t")

    missing=required_columns-set(df.columns)

    if missing:
        raise ValueError(
            f"{path.name} missing required columns: {sorted(missing)}"
        )

    return df

def compact_count(x:int)->str:
    if x>=1_000_000:
        return f"{x/1_000_000:.2f}M"
    if x>=1_000:
        return f"{x/1_000:.1f}k"
    return str(x)

def draw_panel(
    ax,
    *,
    panel_title:str,
    artifact_name:str,
    row_count:int,
    schema_fields:list[str],
    cognition_caption:str,
    border_color:str="#444444",
    accent_color:str="#222222",
    panel_fill:str="#fbfbfb",
    schema_columns:int=1,
):

    ax.set_xlim(0,1)
    ax.set_ylim(0,1)
    ax.axis("off")

    card=FancyBboxPatch(
        (0.04,0.10),
        0.92,
        0.80,
        boxstyle="round,pad=0.012,rounding_size=0.02",
        linewidth=1.2,
        edgecolor=border_color,
        facecolor=panel_fill,
    )

    ax.add_patch(card)

    ax.text(
        0.5,
        0.88,
        panel_title,
        ha="center",
        va="center",
        fontsize=14,
        fontweight="bold",
        color=accent_color,
    )

    ax.text(
        0.5,
        0.81,
        artifact_name,
        ha="center",
        va="center",
        fontsize=10,
        family="monospace",
    )

    ax.text(
        0.5,
        0.71,
        f"{compact_count(row_count)} rows",
        ha="center",
        va="center",
        fontsize=24,
        fontweight="bold",
        color=accent_color,
    )

    ax.plot(
        [0.12,0.88],
        [0.64,0.64],
        linewidth=0.8,
        color="#bbbbbb",
    )

    ax.text(
        0.12,
        0.58,
        "Representative schema fields",
        ha="left",
        va="center",
        fontsize=10,
        fontweight="bold",
    )

    if schema_columns==2:
        left_fields=schema_fields[:6]
        right_fields=schema_fields[6:]
        column_specs=[
            (0.15,left_fields),
            (0.55,right_fields),
        ]

        for x0,fields in column_specs:
            y=0.54
            for field in fields:
                ax.text(
                    x0,
                    y,
                    f"• {field}",
                    ha="left",
                    va="center",
                    fontsize=8.2,
                    family="monospace",
                )
                y-=0.047
    else:
        y=0.54
        for field in schema_fields:
            ax.text(
                0.15,
                y,
                f"• {field}",
                ha="left",
                va="center",
                fontsize=9,
                family="monospace",
            )
            y-=0.047    

    ax.plot(
        [0.18,0.82],
        [0.17,0.17],
        linewidth=1.0,
        color="#888888",
    )

    ax.text(
        0.5,
        0.125,
        cognition_caption,
        ha="center",
        va="center",
        fontsize=9,
        style="italic",
    )

def main():

    parser=argparse.ArgumentParser()

    parser.add_argument("--config",help="YAML config for F5 interoperability substrate rendering.")

    parser.add_argument("--rdgp-tsv")
    parser.add_argument("--vdb-tsv")
    parser.add_argument("--out")

    parser.add_argument("--sample-id")
    parser.add_argument("--run-id")

    args=parser.parse_args()

    cfg={}
    if args.config:
        cfg=yaml.safe_load(Path(args.config).read_text())
        if cfg is None:
            cfg={}

    rdgp_tsv=args.rdgp_tsv or cfg.get("rdgp_tsv")
    vdb_tsv=args.vdb_tsv or cfg.get("vdb_tsv")
    out=args.out or cfg.get("out")
    sample_id=args.sample_id or cfg.get("sample_id")
    run_id=args.run_id or cfg.get("run_id")

    missing=[
        name for name,value in {
            "rdgp_tsv":rdgp_tsv,
            "vdb_tsv":vdb_tsv,
            "out":out,
        }.items()
        if not value
    ]
    if missing:
        raise ValueError(f"Missing required F5 render parameter(s): {missing}")

    rdgp_df=validate_input(
        Path(rdgp_tsv),
        RDGP_REQUIRED_COLUMNS,
    )

    vdb_df=validate_input(
        Path(vdb_tsv),
        VDB_REQUIRED_COLUMNS,
    )

    rdgp_rows=len(rdgp_df)
    vdb_rows=len(vdb_df)

    fig,axes=plt.subplots(
        1,
        2,
        figsize=(14,7),
        facecolor="white",
    )

    title="F5: Stage 08 Interoperability Substrates"

    subtitle_parts=[]

    if sample_id:
        subtitle_parts.append(f"sample={sample_id}")

    if run_id:
        subtitle_parts.append(f"run={run_id}")

    subtitle=" | ".join(subtitle_parts)

    fig.suptitle(
        title,
        fontsize=18,
        fontweight="bold",
        y=0.945,
    )

    if subtitle:
        fig.text(
            0.5,
            0.862,
            subtitle,
            ha="center",
            va="center",
            fontsize=10,
        )

    draw_panel(
        axes[0],
        panel_title="RDGP-ready gene evidence substrate",
        artifact_name="stage_08_rdgp_gene_evidence_seed.tsv",
        row_count=rdgp_rows,
        schema_fields=[
            "gene_symbol",
            "variant_count",
            "high_impact_variant_count",
            "rare_variant_count",
            "pathogenic_variant_count",
            "max_variant_severity",
        ],
        cognition_caption="Gene evidence aggregation → RDGP-ready substrate",
        accent_color="crimson",
        panel_fill="#fff1f4",
    )

    draw_panel(
        axes[1],
        panel_title="VDB-ready normalized variant substrate",
        artifact_name="stage_08_vdb_ready_variants.tsv",
        row_count=vdb_rows,
        schema_fields=[
            "variant_id",
            "chromosome",
            "position",
            "consequence",
            "clinical_significance",
            "population_frequency",
            "variant_context",
            "variant_effect_severity",
            "interpretability_status",
            "frequency_status",
            "clinical_status",
        ],
        cognition_caption="Normalized variant representation → VDB-ready substrate",
        accent_color="forestgreen",
        panel_fill="#f1fbf1",
        schema_columns=2,
    )

    fig.text(
        0.5,
        0.008,
        (
            "Stage 08 emits deterministic TSV substrates for downstream "
            "ecosystem reuse; row counts vary by run/SRA."
        ),
        ha="center",
        va="center",
        fontsize=8,
    )

    plt.tight_layout(rect=[0,0.04,1,0.90])

    out_path=Path(out)
    out_path.parent.mkdir(parents=True,exist_ok=True)

    plt.savefig(
        out_path,
        dpi=300,
        bbox_inches="tight",
        facecolor="white",
    )

    svg_path=out_path.with_suffix(".svg")

    plt.savefig(
        svg_path,
        bbox_inches="tight",
        facecolor="white",
    )

    plt.close(fig)

    print(f"Wrote PNG: {out_path}")
    print(f"Wrote SVG: {svg_path}")



if __name__=="__main__":
    main()