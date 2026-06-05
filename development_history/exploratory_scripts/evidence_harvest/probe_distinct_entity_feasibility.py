#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import duckdb
import pandas as pd


REPO_ROOT = Path(".")
OUT_DIR = Path("/root/Desktop/mark_probes")
OUT_PATH = OUT_DIR / "probe_distinct_entity_feasibility.txt"

RUN_ID = "run_2026_05_27_172531"

VDB_PATH = (
    REPO_ROOT
    / "results"
    / RUN_ID
    / "processed"
    / "stage_08_vdb_ready_variants.tsv"
)

RDGP_PATH = (
    REPO_ROOT
    / "results"
    / RUN_ID
    / "processed"
    / "stage_08_rdgp_gene_evidence_seed.tsv"
)

STAGE12_PATH = (
    REPO_ROOT
    / "results"
    / RUN_ID
    / "processed"
    / "stage_12_validation_candidates.tsv"
)

EPI25_PATH = (
    REPO_ROOT
    / "data"
    / "reference"
    / "gene_lists"
    / "epi25_vap_overlay_seed.tsv"
)

MITOCARTA_PATH = (
    REPO_ROOT
    / "data"
    / "reference"
    / "gene_lists"
    / "mitocarta_vap_overlay_seed.tsv"
)


def load_gene_set(path: Path) -> set[str]:
    df = pd.read_csv(path, sep="\t", dtype=str)

    candidate_cols = [
        c for c in df.columns
        if "gene" in c.lower()
    ]

    if not candidate_cols:
        raise RuntimeError(f"No gene-like columns found in: {path}")

    gene_col = candidate_cols[0]

    genes = (
        df[gene_col]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    genes = genes[
        (genes != "")
        & (genes != "NAN")
        & (genes != "NONE")
    ]

    return set(genes)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    con = duckdb.connect()

    lines = []

    lines.append("=== PROBE: DISTINCT ENTITY FEASIBILITY ===")
    lines.append("")

    lines.append(f"RUN_ID: {RUN_ID}")
    lines.append("")

    for label, path in [
        ("VDB", VDB_PATH),
        ("RDGP", RDGP_PATH),
        ("STAGE12", STAGE12_PATH),
    ]:
        lines.append(f"{label}_PATH: {path}")
        lines.append(f"exists: {path.exists()}")
        if path.exists():
            lines.append(f"size_mb: {round(path.stat().st_size / 1e6, 2)}")
        lines.append("")

    lines.append("=" * 80)
    lines.append("HEADER INVENTORY")
    lines.append("=" * 80)

    for label, path in [
        ("VDB", VDB_PATH),
        ("RDGP", RDGP_PATH),
        ("STAGE12", STAGE12_PATH),
    ]:
        if not path.exists():
            continue

        df = pd.read_csv(path, sep="\t", dtype=str, nrows=5)

        lines.append("")
        lines.append(f"[{label}]")

        for col in df.columns:
            lines.append(col)

    lines.append("")
    lines.append("=" * 80)
    lines.append("DISTINCT COUNTS")
    lines.append("=" * 80)

    unique_variant_ids = con.execute(f"""
        SELECT COUNT(DISTINCT variant_id)
        FROM read_csv_auto('{VDB_PATH}', delim='\t')
    """).fetchone()[0]

    lines.append(f"unique_variant_ids\t{unique_variant_ids}")

    unique_vdb_genes = con.execute(f"""
        SELECT COUNT(DISTINCT gene_id)
        FROM read_csv_auto('{VDB_PATH}', delim='\t')
        WHERE gene_id IS NOT NULL
    """).fetchone()[0]

    lines.append(f"unique_genes_in_vdb_substrate\t{unique_vdb_genes}")

    unique_rdgp_genes = con.execute(f"""
        SELECT COUNT(DISTINCT gene_id)
        FROM read_csv_auto('{RDGP_PATH}', delim='\t')
        WHERE gene_id IS NOT NULL
    """).fetchone()[0]

    lines.append(f"unique_rdgp_genes\t{unique_rdgp_genes}")

    lines.append("")
    lines.append("=" * 80)
    lines.append("VARIANTS PER GENE")
    lines.append("=" * 80)

    gene_stats = con.execute(f"""
        WITH gene_counts AS (
            SELECT
                gene_id,
                COUNT(DISTINCT variant_id) AS variant_count
            FROM read_csv_auto('{VDB_PATH}', delim='\t')
            WHERE gene_id IS NOT NULL
            GROUP BY gene_id
        )
        SELECT
            AVG(variant_count),
            MEDIAN(variant_count)
        FROM gene_counts
    """).fetchone()

    lines.append(
        f"variants_per_rdgp_gene_mean\t{round(gene_stats[0], 4)}"
    )

    lines.append(
        f"variants_per_rdgp_gene_median\t{gene_stats[1]}"
    )

    lines.append("")
    lines.append("=" * 80)
    lines.append("OVERLAY GENE INTERSECTIONS")
    lines.append("=" * 80)

    epi25 = load_gene_set(EPI25_PATH)
    mito = load_gene_set(MITOCARTA_PATH)

    overlap = epi25.intersection(mito)

    lines.append(f"epi25_gene_count\t{len(epi25)}")
    lines.append(f"mitocarta_gene_count\t{len(mito)}")
    lines.append(f"dual_epi_mito_overlay_genes\t{len(overlap)}")

    if overlap:
        lines.append("")
        lines.append("OVERLAP_GENES")

        for gene in sorted(overlap):
            lines.append(gene)

    with open(OUT_PATH, "w") as handle:
        handle.write("\n".join(lines))

    print(f"Wrote: {OUT_PATH}")


if __name__ == "__main__":
    main()