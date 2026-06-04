#!/usr/bin/env python3
"""
Build append-ready overlay_gene_coding_clinical_evidence.new.tsv on MARK.

Run from MARK VAP repo root:

    python scripts/mark/build_overlay_gene_coding_views.py

Reads:
    results/processed/<run_id>/processed/stage_12_validation_candidates.tsv
    results/processed/<run_id>/metrics/stage_metrics_long.tsv
    data/reference/gene_lists/epi25_vap_overlay_seed.tsv
    data/reference/gene_lists/mitocarta_vap_overlay_seed.tsv

Writes:
    /root/Desktop/overlay_gene_coding/overlay_gene_coding_clinical_evidence.new.tsv
    /root/Desktop/overlay_gene_coding/overlay_gene_coding_clinical_evidence_build_audit.tsv
"""

from __future__ import annotations

from pathlib import Path

import duckdb
import pandas as pd


REPO_ROOT = Path(".")
OUT_DIR = Path("/root/Desktop/overlay_gene_coding")

OUT_PATH = OUT_DIR / "overlay_gene_coding_clinical_evidence.new.tsv"
AUDIT_PATH = OUT_DIR / "overlay_gene_coding_clinical_evidence_build_audit.tsv"

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

OUTPUT_COLUMNS = [
    "sample_id",
    "run_id",
    "assay_type",
    "run_classification",
    "gene_id",
    "gene_symbol",
    "overlay_source",
    "overlay_source_count",
    "overlay_source_list",
    "mitocarta_hit",
    "epi25_hit",
    "match_key",
    "clinical_evidence",
    "clinical_status",
    "variant_count",
]


def load_seed(path: Path, label: str) -> pd.DataFrame:
    if not path.exists():
        raise SystemExit(f"Missing {label} seed file: {path}")

    df = pd.read_csv(path, sep="\t", dtype=str)
    df.columns = [c.strip() for c in df.columns]

    if "ensembl_gene_id" not in df.columns:
        raise SystemExit(
            f"{label} seed file lacks required column 'ensembl_gene_id': {path}"
        )

    out = (
        df[["ensembl_gene_id"]]
        .dropna()
        .assign(ensembl_gene_id=lambda x: x["ensembl_gene_id"].astype(str).str.strip())
    )
    out = out[out["ensembl_gene_id"] != ""].drop_duplicates()
    out = out.rename(columns={"ensembl_gene_id": "gene_id"})

    if out.empty:
        raise SystemExit(f"{label} seed file produced zero usable Ensembl gene IDs")

    return out


def read_run_metadata(metrics_path: Path, sample_id: str, run_id: str) -> tuple[str, str]:
    if not metrics_path.exists():
        raise SystemExit(f"Missing stage_metrics_long.tsv: {metrics_path}")

    df = pd.read_csv(metrics_path, sep="\t", dtype=str)

    required = {"sample_id", "run_id", "metric_name", "assay_type", "run_classification"}
    missing = required - set(df.columns)
    if missing:
        raise SystemExit(f"{metrics_path} missing required columns: {sorted(missing)}")

    sub = df[df["metric_name"] == "validation_candidates_rows"].copy()

    if sub.empty:
        raise SystemExit(f"{metrics_path} lacks metric_name == validation_candidates_rows")

    sub = sub[
        (sub["sample_id"].astype(str) == sample_id)
        & (sub["run_id"].astype(str) == run_id)
    ].copy()

    if sub.empty:
        raise SystemExit(
            f"{metrics_path} lacks validation_candidates_rows for "
            f"sample_id={sample_id}, run_id={run_id}"
        )

    meta = sub[["assay_type", "run_classification"]].drop_duplicates()

    if len(meta) != 1:
        raise SystemExit(
            f"{metrics_path} has unexpected assay/run_classification metadata:\n{meta}"
        )

    return str(meta.iloc[0]["assay_type"]), str(meta.iloc[0]["run_classification"])


def candidate_path_for(run_id: str) -> Path:
    return (
        REPO_ROOT
        / "results"
        / run_id
        / "processed"
        / "stage_12_validation_candidates.tsv"
    )


def metrics_path_for(run_id: str) -> Path:
    return (
        REPO_ROOT
        / "results"
        / run_id
        / "metrics"
        / "stage_metrics_long.tsv"
    )


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    epi25_seed = load_seed(EPI25_PATH, "EPI25")
    mitocarta_seed = load_seed(MITOCARTA_PATH, "MitoCarta")

    con = duckdb.connect(database=":memory:")
    con.register("epi25_seed", epi25_seed)
    con.register("mitocarta_seed", mitocarta_seed)

    all_outputs: list[pd.DataFrame] = []
    audit_rows: list[dict[str, object]] = []

    seed_audit_base = {
        "epi25_seed_path": str(EPI25_PATH),
        "mitocarta_seed_path": str(MITOCARTA_PATH),
        "epi25_unique_gene_ids": len(epi25_seed),
        "mitocarta_unique_gene_ids": len(mitocarta_seed),
    }

    for sample_id, run_id, depth_category in MANIFEST:
        input_path = candidate_path_for(run_id)
        metrics_path = metrics_path_for(run_id)

        audit = {
            "sample_id": sample_id,
            "run_id": run_id,
            "depth_category": depth_category,
            "input_path": str(input_path),
            "input_exists": input_path.exists(),
            "rows_scanned": 0,
            "coding_rows_scanned": 0,
            "eligible_gene_id_rows": 0,
            "overlay_matched_rows": 0,
            "clinical_evidence_rows_written": 0,
            "rows_written": 0,
            "mitocarta_gene_matches": 0,
            "epi25_gene_matches": 0,
            "both_overlay_gene_matches": 0,
            "status": "not_started",
            **seed_audit_base,
        }

        if not input_path.exists():
            audit["status"] = "missing_input"
            audit_rows.append(audit)
            continue

        assay_type, run_classification = read_run_metadata(
            metrics_path=metrics_path,
            sample_id=sample_id,
            run_id=run_id,
        )

        query = """
        WITH src AS (
            SELECT
                sample_id,
                run_id,
                NULLIF(TRIM(gene_id), '') AS gene_id,
                NULLIF(TRIM(gene_symbol), '') AS gene_symbol,
                LOWER(TRIM(variant_origin)) AS variant_origin,
                COALESCE(NULLIF(TRIM(clinical_evidence), ''), 'missing') AS clinical_evidence,
                COALESCE(NULLIF(TRIM(clinical_status), ''), 'missing') AS clinical_status
            FROM read_csv(
                ?,
                delim = '\t',
                header = true,
                all_varchar = true,
                ignore_errors = false
            )
        ),
        annotated AS (
            SELECT
                s.*,
                CASE WHEN m.gene_id IS NOT NULL THEN true ELSE false END AS mitocarta_hit_bool,
                CASE WHEN e.gene_id IS NOT NULL THEN true ELSE false END AS epi25_hit_bool
            FROM src s
            LEFT JOIN mitocarta_seed m
                ON s.gene_id = m.gene_id
            LEFT JOIN epi25_seed e
                ON s.gene_id = e.gene_id
        ),
        eligible AS (
            SELECT
                *,
                (CAST(mitocarta_hit_bool AS INTEGER) + CAST(epi25_hit_bool AS INTEGER))
                    AS overlay_source_count,
                CASE
                    WHEN epi25_hit_bool AND mitocarta_hit_bool
                        THEN 'epi25_all_epilepsy|mitocarta'
                    WHEN epi25_hit_bool
                        THEN 'epi25_all_epilepsy'
                    WHEN mitocarta_hit_bool
                        THEN 'mitocarta'
                    ELSE ''
                END AS overlay_source_list
            FROM annotated
            WHERE variant_origin = 'coding'
              AND gene_id IS NOT NULL
              AND gene_symbol IS NOT NULL
              AND (mitocarta_hit_bool OR epi25_hit_bool)
        ),
        expanded AS (
            SELECT
                sample_id,
                run_id,
                gene_id,
                gene_symbol,
                'mitocarta' AS overlay_source,
                overlay_source_count,
                overlay_source_list,
                'True' AS mitocarta_hit,
                CASE WHEN epi25_hit_bool THEN 'True' ELSE 'False' END AS epi25_hit,
                'ensembl_gene_id' AS match_key,
                clinical_evidence,
                clinical_status
            FROM eligible
            WHERE mitocarta_hit_bool

            UNION ALL

            SELECT
                sample_id,
                run_id,
                gene_id,
                gene_symbol,
                'epi25_all_epilepsy' AS overlay_source,
                overlay_source_count,
                overlay_source_list,
                CASE WHEN mitocarta_hit_bool THEN 'True' ELSE 'False' END AS mitocarta_hit,
                'True' AS epi25_hit,
                'ensembl_gene_id' AS match_key,
                clinical_evidence,
                clinical_status
            FROM eligible
            WHERE epi25_hit_bool
        )
        SELECT
            sample_id,
            run_id,
            ? AS assay_type,
            ? AS run_classification,
            gene_id,
            gene_symbol,
            overlay_source,
            CAST(overlay_source_count AS VARCHAR) AS overlay_source_count,
            overlay_source_list,
            mitocarta_hit,
            epi25_hit,
            match_key,
            clinical_evidence,
            clinical_status,
            CAST(COUNT(*) AS VARCHAR) AS variant_count
        FROM expanded
        GROUP BY
            sample_id,
            run_id,
            gene_id,
            gene_symbol,
            overlay_source,
            overlay_source_count,
            overlay_source_list,
            mitocarta_hit,
            epi25_hit,
            match_key,
            clinical_evidence,
            clinical_status
        ORDER BY
            sample_id,
            run_id,
            overlay_source,
            gene_symbol,
            gene_id,
            clinical_evidence,
            clinical_status
        """

        counts_query = """
        WITH src AS (
            SELECT
                sample_id,
                run_id,
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
        annotated AS (
            SELECT
                s.*,
                CASE WHEN m.gene_id IS NOT NULL THEN true ELSE false END AS mitocarta_hit_bool,
                CASE WHEN e.gene_id IS NOT NULL THEN true ELSE false END AS epi25_hit_bool
            FROM src s
            LEFT JOIN mitocarta_seed m
                ON s.gene_id = m.gene_id
            LEFT JOIN epi25_seed e
                ON s.gene_id = e.gene_id
        )
        SELECT
            COUNT(*) AS rows_scanned,
            SUM(CASE WHEN variant_origin = 'coding' THEN 1 ELSE 0 END) AS coding_rows_scanned,
            SUM(
                CASE
                    WHEN variant_origin = 'coding'
                     AND gene_id IS NOT NULL
                     AND gene_symbol IS NOT NULL
                    THEN 1 ELSE 0
                END
            ) AS eligible_gene_id_rows,
            SUM(
                CASE
                    WHEN variant_origin = 'coding'
                     AND gene_id IS NOT NULL
                     AND gene_symbol IS NOT NULL
                     AND (mitocarta_hit_bool OR epi25_hit_bool)
                    THEN 1 ELSE 0
                END
            ) AS overlay_matched_rows,
            COUNT(DISTINCT CASE
                WHEN variant_origin = 'coding'
                 AND gene_id IS NOT NULL
                 AND gene_symbol IS NOT NULL
                 AND mitocarta_hit_bool
                THEN gene_id END
            ) AS mitocarta_gene_matches,
            COUNT(DISTINCT CASE
                WHEN variant_origin = 'coding'
                 AND gene_id IS NOT NULL
                 AND gene_symbol IS NOT NULL
                 AND epi25_hit_bool
                THEN gene_id END
            ) AS epi25_gene_matches,
            COUNT(DISTINCT CASE
                WHEN variant_origin = 'coding'
                 AND gene_id IS NOT NULL
                 AND gene_symbol IS NOT NULL
                 AND mitocarta_hit_bool
                 AND epi25_hit_bool
                THEN gene_id END
            ) AS both_overlay_gene_matches
        FROM annotated
        """

        try:
            debug_query = """
            WITH src AS (
                SELECT
                    sample_id,
                    run_id,
                    NULLIF(TRIM(gene_id), '') AS gene_id,
                    NULLIF(TRIM(gene_symbol), '') AS gene_symbol,
                    LOWER(TRIM(variant_origin)) AS variant_origin
                FROM read_csv(
                    ?,
                    delim = '\t',
                    header = true,
                    all_varchar = true
                )
            ),
            annotated AS (
                SELECT
                    s.*,
                    CASE WHEN m.gene_id IS NOT NULL THEN true ELSE false END AS mitocarta_hit_bool,
                    CASE WHEN e.gene_id IS NOT NULL THEN true ELSE false END AS epi25_hit_bool
                FROM src s
                LEFT JOIN mitocarta_seed m
                    ON s.gene_id = m.gene_id
                LEFT JOIN epi25_seed e
                    ON s.gene_id = e.gene_id
            )
            SELECT
                COUNT(*) AS total_rows,
                SUM(CASE WHEN variant_origin = 'coding' THEN 1 ELSE 0 END) AS coding_rows,
                SUM(
                    CASE
                        WHEN variant_origin = 'coding'
                        AND gene_id IS NOT NULL
                        AND gene_symbol IS NOT NULL
                        THEN 1 ELSE 0
                    END
                ) AS coding_gene_rows,
                SUM(
                    CASE
                        WHEN variant_origin = 'coding'
                        AND gene_id IS NOT NULL
                        AND gene_symbol IS NOT NULL
                        AND (mitocarta_hit_bool OR epi25_hit_bool)
                        THEN 1 ELSE 0
                    END
                ) AS overlay_rows
            FROM annotated
            """

            debug_df = con.execute(debug_query, [str(input_path)]).fetchdf()

            print()
            print(f"DEBUG {run_id}")
            print(debug_df.to_string(index=False))
            print()

            out_df = con.execute(
                query,
                [str(input_path), assay_type, run_classification],
            ).fetchdf()

            count_df = con.execute(counts_query, [str(input_path)]).fetchdf()
            count_row = count_df.iloc[0].to_dict()

            for key, value in count_row.items():
                audit[key] = int(value) if pd.notna(value) else 0

            out_df = out_df[OUTPUT_COLUMNS]

            audit["clinical_evidence_rows_written"] = len(out_df)
            audit["rows_written"] = len(out_df)
            audit["status"] = "ok"

            all_outputs.append(out_df)

        except Exception as exc:
            audit["status"] = f"error: {type(exc).__name__}: {exc}"
            audit_rows.append(audit)
            raise

        audit_rows.append(audit)
        print(f"{sample_id}\t{run_id}\trows_written={audit['rows_written']}")

    audit_df = pd.DataFrame(audit_rows)
    audit_df.to_csv(AUDIT_PATH, sep="\t", index=False)

    if not all_outputs:
        raise SystemExit("No output rows produced")

    final = pd.concat(all_outputs, ignore_index=True)
    final = final[OUTPUT_COLUMNS]
    final.to_csv(OUT_PATH, sep="\t", index=False)

    audit_df = pd.DataFrame(audit_rows)
    audit_df.to_csv(AUDIT_PATH, sep="\t", index=False)

    print()
    print(f"Wrote: {OUT_PATH}")
    print(f"Wrote: {AUDIT_PATH}")
    print(f"Total output rows: {len(final)}")


if __name__ == "__main__":
    main()
