#!/usr/bin/env python3
from pathlib import Path
import pandas as pd

OLD = Path("gene_list_overlay_intersections.tsv")
OUT = Path("gene_list_overlay_intersections.repaired.tsv")
AUDIT = Path("gene_list_overlay_intersections.repair_audit.tsv")

EPI25 = Path("data/reference/gene_lists/epi25_vap_overlay_seed.tsv")
MITO = Path("data/reference/gene_lists/mitocarta_vap_overlay_seed.tsv")

COLS = [
    "sample_id","run_id","assay_type","run_classification",
    "gene_id","gene_symbol","gene_burden_rank","variant_count",
    "overlay_source","overlay_source_count","overlay_source_list",
    "mitocarta_hit","epi25_hit","match_key",
]

def load_seed(path, source):
    df = pd.read_csv(path, sep="\t", dtype=str)
    df.columns = [c.strip() for c in df.columns]
    out = df[["ensembl_gene_id", "gene_symbol"]].copy()
    out["gene_id"] = out["ensembl_gene_id"].astype(str).str.strip()
    out["gene_symbol"] = out["gene_symbol"].astype(str).str.strip()
    out = out[["gene_id", "gene_symbol"]].drop_duplicates()

    out["overlay_source"] = source
    out["overlay_source_count"] = "1"
    out["overlay_source_list"] = source
    out["match_key"] = "ensembl_gene_id"

    if source == "epi25_all_epilepsy":
        out["mitocarta_hit"] = "False"
        out["epi25_hit"] = "True"
    else:
        out["mitocarta_hit"] = "True"
        out["epi25_hit"] = "False"

    return out

master = pd.concat([
    load_seed(EPI25, "epi25_all_epilepsy"),
    load_seed(MITO, "mitocarta"),
], ignore_index=True)

if len(master) != 1140:
    raise SystemExit(f"Expected 1140 master genes, observed {len(master)}")

old = pd.read_csv(OLD, sep="\t", dtype=str)
old["variant_count"] = old["variant_count"].astype(int)

blocks = []
audit = []

for (sample_id, run_id), block in old.groupby(["sample_id", "run_id"], sort=False):
    meta = block[["assay_type", "run_classification"]].drop_duplicates()
    if len(meta) != 1:
        raise SystemExit(f"Ambiguous metadata for {sample_id} {run_id}")

    assay_type = meta.iloc[0]["assay_type"]
    run_classification = meta.iloc[0]["run_classification"]

    counts = block[["gene_id", "variant_count"]].copy()
    counts["gene_id"] = counts["gene_id"].astype(str).str.strip()

    repaired = master.merge(counts, how="left", on="gene_id")
    repaired["variant_count"] = repaired["variant_count"].fillna(0).astype(int)

    repaired.insert(0, "run_classification", run_classification)
    repaired.insert(0, "assay_type", assay_type)
    repaired.insert(0, "run_id", run_id)
    repaired.insert(0, "sample_id", sample_id)

    ranked = repaired.sort_values(
        ["variant_count", "gene_symbol", "gene_id"],
        ascending=[False, True, True],
        kind="mergesort",
    ).copy()
    ranked["gene_burden_rank"] = range(1, len(ranked) + 1)

    repaired = repaired.merge(ranked[["gene_id", "gene_burden_rank"]], on="gene_id", how="left")
    repaired = repaired[COLS].sort_values(
        ["mitocarta_hit", "gene_symbol", "gene_id"],
        ascending=[True, True, True],
        kind="mergesort",
    )

    blocks.append(repaired)

    audit.append({
        "sample_id": sample_id,
        "run_id": run_id,
        "original_rows": len(block),
        "repaired_rows": len(repaired),
        "rows_added": len(repaired) - len(block),
        "zero_count_rows": int((repaired["variant_count"] == 0).sum()),
        "status": "ok",
    })

final = pd.concat(blocks, ignore_index=True)
final.to_csv(OUT, sep="\t", index=False)
pd.DataFrame(audit).to_csv(AUDIT, sep="\t", index=False)

print(f"Wrote: {OUT}")
print(f"Wrote: {AUDIT}")
print(f"Rows: {len(final)}")
