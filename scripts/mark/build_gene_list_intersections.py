#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import duckdb
import pandas as pd


REPO_ROOT = Path(".")
OUT_DIR = Path("/root/Desktop/gene_list_overlay_intersections")

GENE_INTERSECT_OUT = OUT_DIR / "gene_list_overlay_intersections.new.tsv"
AUDIT_OUT = OUT_DIR / "gene_list_overlay_intersections_build_audit.tsv"

EPI25_PATH = REPO_ROOT / "data/reference/gene_lists/epi25_vap_overlay_seed.tsv"
MITOCARTA_PATH = REPO_ROOT / "data/reference/gene_lists/mitocarta_vap_overlay_seed.tsv"

MANIFEST = [
    ("ERR10619203", "run_2026_05_30_071639", "q3"),
    ("ERR10619207", "run_2026_06_01_124134", "q3"),
    ("ERR10619208", "run_2026_05_30_151355", "median"),
    ("ERR10619212", "run_2026_05_30_214724", "q1"),
    ("ERR10619225", "run_2026_05_31_091242", "q3"),
    ("ERR10619230", "run_2026_06_01_004903", "q3"),
    ("ERR10619241", "run_2026_06_02_052302", "q1"),
    ("ERR10619281", "run_2026_05_27_233524", "median"),
    ("ERR10619285", "run_2026_06_02_124300", "median"),
    ("ERR10619300", "run_2026_05_27_172531", "median"),
    ("ERR10619309", "run_2026_06_02_181024", "q1"),
    ("ERR10619330", "run_2026_06_01_203130", "q1"),
    ("SRR12898354", "run_2026_06_03_010030", "hg002"),
]

BASE_COLS = [
    "sample_id", "run_id", "assay_type", "run_classification",
    "gene_id", "gene_symbol", "gene_burden_rank", "variant_count",
    "overlay_source", "overlay_source_count", "overlay_source_list",
    "mitocarta_hit", "epi25_hit", "match_key",
]


def candidate_path(run_id: str) -> Path:
    return REPO_ROOT / "results" / run_id / "processed" / "stage_12_validation_candidates.tsv"


def metrics_path(run_id: str) -> Path:
    return REPO_ROOT / "results" / run_id / "metrics" / "stage_metrics_long.tsv"


def load_gene_seed(path: Path, overlay_source: str) -> pd.DataFrame:
    if not path.exists():
        raise SystemExit(f"Missing seed file: {path}")

    df = pd.read_csv(path, sep="\t", dtype=str)
    df.columns = [c.strip() for c in df.columns]

    required = {"ensembl_gene_id", "gene_symbol"}
    missing = required - set(df.columns)
    if missing:
        raise SystemExit(f"{path} missing required columns: {sorted(missing)}")

    out = df[["ensembl_gene_id", "gene_symbol"]].copy()
    out["gene_id"] = out["ensembl_gene_id"].astype(str).str.strip()
    out["gene_symbol"] = out["gene_symbol"].astype(str).str.strip()

    out = out[
        (out["gene_id"] != "")
        & (out["gene_symbol"] != "")
        & out["gene_id"].notna()
        & out["gene_symbol"].notna()
    ].copy()

    out = out[["gene_id", "gene_symbol"]].drop_duplicates()

    if overlay_source == "epi25_all_epilepsy":
        out["overlay_source"] = "epi25_all_epilepsy"
        out["mitocarta_hit"] = "False"
        out["epi25_hit"] = "True"
    elif overlay_source == "mitocarta":
        out["overlay_source"] = "mitocarta"
        out["mitocarta_hit"] = "True"
        out["epi25_hit"] = "False"
    else:
        raise ValueError(f"Unexpected overlay source: {overlay_source}")

    out["overlay_source_count"] = "1"
    out["overlay_source_list"] = out["overlay_source"]
    out["match_key"] = "ensembl_gene_id"

    return out


def build_master_gene_list() -> pd.DataFrame:
    epi25 = load_gene_seed(EPI25_PATH, "epi25_all_epilepsy")
    mito = load_gene_seed(MITOCARTA_PATH, "mitocarta")

    overlap = set(epi25["gene_id"]) & set(mito["gene_id"])
    if overlap:
        raise SystemExit(f"Unexpected overlap between EPI25 and MitoCarta gene IDs: {sorted(overlap)[:20]}")

    master = pd.concat([epi25, mito], ignore_index=True)

    if master["gene_id"].duplicated().any():
        dupes = master.loc[master["gene_id"].duplicated(keep=False), ["gene_id", "gene_symbol", "overlay_source"]]
        raise SystemExit(f"Duplicate gene_id values in master overlay list:\n{dupes}")

    return master


def read_metadata(path: Path, sample_id: str, run_id: str) -> tuple[str, str]:
    if not path.exists():
        raise SystemExit(f"Missing metrics file: {path}")

    df = pd.read_csv(path, sep="\t", dtype=str)
    required = {"sample_id", "run_id", "metric_name", "assay_type", "run_classification"}
    missing = required - set(df.columns)
    if missing:
        raise SystemExit(f"{path} missing columns: {sorted(missing)}")

    sub = df[
        (df["metric_name"].astype(str).str.strip() == "validation_candidates_rows")
        & (df["sample_id"].astype(str).str.strip() == sample_id)
        & (df["run_id"].astype(str).str.strip() == run_id)
    ].copy()

    if sub.empty:
        if sample_id == "SRR12898354":
            return "wgs", "hg002"
        raise SystemExit(f"{path} lacks validation_candidates_rows for {sample_id} {run_id}")

    meta = sub[["assay_type", "run_classification"]].drop_duplicates()
    if len(meta) != 1:
        raise SystemExit(f"{path} has ambiguous assay/run metadata:\n{meta}")

    return str(meta.iloc[0]["assay_type"]).strip(), str(meta.iloc[0]["run_classification"]).strip()


COUNT_QUERY = """
WITH src AS (
    SELECT
        NULLIF(TRIM(gene_id), '') AS gene_id,
        NULLIF(TRIM(gene_symbol), '') AS gene_symbol,
        LOWER(TRIM(variant_origin)) AS variant_origin
    FROM read_csv(
        ?,
        delim = '\t',
        header = true,
        all_varchar = true,
        ignore_errors = false
    )
),
eligible AS (
    SELECT gene_id
    FROM src
    WHERE variant_origin = 'coding'
      AND gene_id IS NOT NULL
      AND gene_symbol IS NOT NULL
)
SELECT
    gene_id,
    COUNT(*)::BIGINT AS variant_count
FROM eligible
GROUP BY gene_id
"""


AUDIT_COUNT_QUERY = """
WITH src AS (
    SELECT
        NULLIF(TRIM(gene_id), '') AS gene_id,
        NULLIF(TRIM(gene_symbol), '') AS gene_symbol,
        LOWER(TRIM(variant_origin)) AS variant_origin
    FROM read_csv(
        ?,
        delim = '\t',
        header = true,
        all_varchar = true,
        ignore_errors = false
    )
)
SELECT
    COUNT(*)::BIGINT AS rows_scanned,
    SUM(CASE WHEN variant_origin = 'coding' THEN 1 ELSE 0 END)::BIGINT AS coding_rows_scanned,
    SUM(
        CASE
            WHEN variant_origin = 'coding'
             AND gene_id IS NOT NULL
             AND gene_symbol IS NOT NULL
            THEN 1 ELSE 0
        END
    )::BIGINT AS eligible_gene_id_rows
FROM src
"""


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    master = build_master_gene_list()
    if len(master) != 1140:
        raise SystemExit(f"Expected 1140 overlay genes, observed {len(master)}")

    con = duckdb.connect(database=":memory:")

    all_outputs: list[pd.DataFrame] = []
    audit_rows: list[dict[str, object]] = []

    seed_constants = {
        "epi25_unique_gene_ids": int((master["overlay_source"] == "epi25_all_epilepsy").sum()),
        "mitocarta_unique_gene_ids": int((master["overlay_source"] == "mitocarta").sum()),
        "master_overlay_gene_count": len(master),
    }

    for sample_id, run_id, depth_category in MANIFEST:
        in_path = candidate_path(run_id)
        m_path = metrics_path(run_id)

        audit = {
            "sample_id": sample_id,
            "run_id": run_id,
            "depth_category": depth_category,
            "input_path": str(in_path),
            "input_exists": in_path.exists(),
            "metrics_path": str(m_path),
            "metrics_exists": m_path.exists(),
            "rows_scanned": 0,
            "coding_rows_scanned": 0,
            "eligible_gene_id_rows": 0,
            "overlay_genes_total": len(master),
            "overlay_genes_with_variants": 0,
            "overlay_genes_zero_count": 0,
            "output_rows_written": 0,
            "status": "not_started",
            **seed_constants,
        }

        if not in_path.exists():
            audit["status"] = "missing_input"
            audit_rows.append(audit)
            continue

        try:
            assay_type, run_classification = read_metadata(m_path, sample_id, run_id)

            counts = con.execute(COUNT_QUERY, [str(in_path)]).fetchdf()
            counts["gene_id"] = counts["gene_id"].astype(str).str.strip()
            counts["variant_count"] = counts["variant_count"].astype(int)

            audit_counts = con.execute(AUDIT_COUNT_QUERY, [str(in_path)]).fetchdf().iloc[0].to_dict()
            for key, value in audit_counts.items():
                audit[key] = int(value) if pd.notna(value) else 0

            run_df = master.merge(counts, how="left", on="gene_id")
            run_df["variant_count"] = run_df["variant_count"].fillna(0).astype(int)

            run_df.insert(0, "run_classification", run_classification)
            run_df.insert(0, "assay_type", assay_type)
            run_df.insert(0, "run_id", run_id)
            run_df.insert(0, "sample_id", sample_id)

            rank_df = run_df.sort_values(
                ["variant_count", "gene_symbol", "gene_id"],
                ascending=[False, True, True],
                kind="mergesort",
            ).copy()
            rank_df["gene_burden_rank"] = range(1, len(rank_df) + 1)

            run_df = run_df.merge(
                rank_df[["gene_id", "gene_burden_rank"]],
                on="gene_id",
                how="left",
            )

            run_df = run_df[BASE_COLS]

            run_df = run_df.sort_values(
                ["mitocarta_hit", "gene_symbol", "gene_id"],
                ascending=[True, True, True],
                kind="mergesort",
            ).reset_index(drop=True)

            audit["overlay_genes_with_variants"] = int((run_df["variant_count"] > 0).sum())
            audit["overlay_genes_zero_count"] = int((run_df["variant_count"] == 0).sum())
            audit["output_rows_written"] = len(run_df)
            audit["status"] = "ok"

            if len(run_df) != 1140:
                raise SystemExit(f"{sample_id} {run_id} produced {len(run_df)} rows, expected 1140")

            all_outputs.append(run_df)
            print(
                f"{sample_id}\t{run_id}"
                f"\trows={len(run_df)}"
                f"\tgenes_with_variants={audit['overlay_genes_with_variants']}"
                f"\tzero_count={audit['overlay_genes_zero_count']}"
            )

        except Exception as exc:
            audit["status"] = f"error: {type(exc).__name__}: {exc}"
            audit_rows.append(audit)
            pd.DataFrame(audit_rows).to_csv(AUDIT_OUT, sep="\t", index=False)
            raise

        audit_rows.append(audit)

    if not all_outputs:
        pd.DataFrame(audit_rows).to_csv(AUDIT_OUT, sep="\t", index=False)
        raise SystemExit("No output rows produced")

    final = pd.concat(all_outputs, ignore_index=True)[BASE_COLS]
    final.to_csv(GENE_INTERSECT_OUT, sep="\t", index=False)

    audit_df = pd.DataFrame(audit_rows)
    audit_df.to_csv(AUDIT_OUT, sep="\t", index=False)

    print()
    print(f"Wrote: {GENE_INTERSECT_OUT}")
    print(f"Wrote: {AUDIT_OUT}")
    print(f"Total rows: {len(final)}")


if __name__ == "__main__":
    main()
