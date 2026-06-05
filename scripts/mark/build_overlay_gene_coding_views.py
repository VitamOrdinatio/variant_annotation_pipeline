#!/usr/bin/env python3
"""
Build append-ready overlay_gene_coding views on MARK.

Run from MARK VAP repo root:

    python scripts/mark/build_overlay_gene_coding_views.py
"""

from __future__ import annotations

from pathlib import Path
import duckdb
import pandas as pd


REPO_ROOT = Path(".")
OUT_DIR = Path("/root/Desktop/overlay_gene_coding")

CLINICAL_OUT = OUT_DIR / "overlay_gene_coding_clinical_evidence.new.tsv"
FREQUENCY_OUT = OUT_DIR / "overlay_gene_coding_frequency_profiles.new.tsv"
FUNCTIONAL_OUT = OUT_DIR / "overlay_gene_coding_functional_impact.new.tsv"
AUDIT_OUT = OUT_DIR / "overlay_gene_coding_views_build_audit.tsv"

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
    "gene_id", "gene_symbol", "overlay_source",
    "overlay_source_count", "overlay_source_list",
    "mitocarta_hit", "epi25_hit", "match_key",
]

CLINICAL_COLS = BASE_COLS + ["clinical_evidence", "clinical_status", "variant_count"]
FREQUENCY_COLS = BASE_COLS + ["frequency_status", "rarity_flag", "variant_count"]
FUNCTIONAL_COLS = BASE_COLS + ["functional_impact", "variant_count"]


def candidate_path(run_id: str) -> Path:
    return REPO_ROOT / "results" / run_id / "processed" / "stage_12_validation_candidates.tsv"


def metrics_path(run_id: str) -> Path:
    return REPO_ROOT / "results" / run_id / "metrics" / "stage_metrics_long.tsv"


def load_seed(path: Path, label: str) -> pd.DataFrame:
    if not path.exists():
        raise SystemExit(f"Missing {label} seed file: {path}")

    df = pd.read_csv(path, sep="\t", dtype=str)
    df.columns = [c.strip() for c in df.columns]

    if "ensembl_gene_id" not in df.columns:
        raise SystemExit(f"{label} seed lacks ensembl_gene_id column: {path}")

    out = df[["ensembl_gene_id"]].copy()
    out["gene_id"] = out["ensembl_gene_id"].astype(str).str.strip()
    out = out[["gene_id"]]
    out = out[(out["gene_id"] != "") & (out["gene_id"].notna())].drop_duplicates()

    if out.empty:
        raise SystemExit(f"{label} seed produced zero usable Ensembl IDs")

    return out


def read_metadata(path: Path, sample_id: str, run_id: str) -> tuple[str, str]:
    if not path.exists():
        raise SystemExit(f"Missing metrics file: {path}")

    df = pd.read_csv(path, sep="\t", dtype=str)

    required = {"sample_id", "run_id", "metric_name", "assay_type", "run_classification"}
    missing = required - set(df.columns)
    if missing:
        raise SystemExit(f"{path} missing columns: {sorted(missing)}")

    sub = df[
        (df["metric_name"] == "validation_candidates_rows")
        & (df["sample_id"].astype(str) == sample_id)
        & (df["run_id"].astype(str) == run_id)
    ].copy()

    if sub.empty:
        if sample_id == "SRR12898354":
            return "wgs", "hg002"
        raise SystemExit(f"{path} lacks validation_candidates_rows for {sample_id} {run_id}")

    meta = sub[["assay_type", "run_classification"]].drop_duplicates()
    if len(meta) != 1:
        raise SystemExit(f"{path} has ambiguous assay/run metadata:\n{meta}")

    return str(meta.iloc[0]["assay_type"]), str(meta.iloc[0]["run_classification"])


def build_query(extra_cols: list[str]) -> str:
    extra_select_src = ""
    for col in extra_cols:
        extra_select_src += f",\n                COALESCE(NULLIF(TRIM({col}), ''), 'missing') AS {col}"

    extra_select_expanded = ""
    for col in extra_cols:
        extra_select_expanded += f",\n                {col}"

    extra_group = ""
    for col in extra_cols:
        extra_group += f",\n            {col}"

    extra_order = ""
    for col in extra_cols:
        extra_order += f",\n            {col}"

    return f"""
    WITH src AS (
        SELECT
            sample_id,
            run_id,
            NULLIF(TRIM(gene_id), '') AS gene_id,
            NULLIF(TRIM(gene_symbol), '') AS gene_symbol,
            LOWER(TRIM(variant_origin)) AS variant_origin
            {extra_select_src}
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
        LEFT JOIN mitocarta_seed m ON s.gene_id = m.gene_id
        LEFT JOIN epi25_seed e ON s.gene_id = e.gene_id
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
            'ensembl_gene_id' AS match_key
            {extra_select_expanded}
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
            'ensembl_gene_id' AS match_key
            {extra_select_expanded}
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
        match_key
        {extra_group},
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
        match_key
        {extra_group}
    ORDER BY
        sample_id,
        run_id,
        overlay_source,
        gene_symbol,
        gene_id
        {extra_order}
    """


COUNTS_QUERY = """
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
annotated AS (
    SELECT
        s.*,
        CASE WHEN m.gene_id IS NOT NULL THEN true ELSE false END AS mitocarta_hit_bool,
        CASE WHEN e.gene_id IS NOT NULL THEN true ELSE false END AS epi25_hit_bool
    FROM src s
    LEFT JOIN mitocarta_seed m ON s.gene_id = m.gene_id
    LEFT JOIN epi25_seed e ON s.gene_id = e.gene_id
)
SELECT
    COUNT(*) AS rows_scanned,
    SUM(CASE WHEN variant_origin = 'coding' THEN 1 ELSE 0 END) AS coding_rows_scanned,
    SUM(CASE WHEN variant_origin = 'coding' AND gene_id IS NOT NULL AND gene_symbol IS NOT NULL THEN 1 ELSE 0 END)
        AS eligible_gene_id_rows,
    SUM(CASE WHEN variant_origin = 'coding' AND gene_id IS NOT NULL AND gene_symbol IS NOT NULL
              AND (mitocarta_hit_bool OR epi25_hit_bool) THEN 1 ELSE 0 END)
        AS overlay_matched_rows,
    COUNT(DISTINCT CASE WHEN variant_origin = 'coding' AND gene_id IS NOT NULL AND gene_symbol IS NOT NULL
                         AND mitocarta_hit_bool THEN gene_id END)
        AS mitocarta_gene_matches,
    COUNT(DISTINCT CASE WHEN variant_origin = 'coding' AND gene_id IS NOT NULL AND gene_symbol IS NOT NULL
                         AND epi25_hit_bool THEN gene_id END)
        AS epi25_gene_matches,
    COUNT(DISTINCT CASE WHEN variant_origin = 'coding' AND gene_id IS NOT NULL AND gene_symbol IS NOT NULL
                         AND mitocarta_hit_bool AND epi25_hit_bool THEN gene_id END)
        AS both_overlay_gene_matches
FROM annotated
"""


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    epi25_seed = load_seed(EPI25_PATH, "EPI25")
    mitocarta_seed = load_seed(MITOCARTA_PATH, "MitoCarta")

    con = duckdb.connect(database=":memory:")
    con.register("epi25_seed", epi25_seed)
    con.register("mitocarta_seed", mitocarta_seed)

    clinical_query = build_query(["clinical_evidence", "clinical_status"])
    frequency_query = build_query(["frequency_status", "rarity_flag"])
    functional_query = build_query(["functional_impact"])

    clinical_outputs = []
    frequency_outputs = []
    functional_outputs = []
    audit_rows = []

    seed_audit = {
        "epi25_seed_path": str(EPI25_PATH),
        "mitocarta_seed_path": str(MITOCARTA_PATH),
        "epi25_unique_gene_ids": len(epi25_seed),
        "mitocarta_unique_gene_ids": len(mitocarta_seed),
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
            "rows_scanned": 0,
            "coding_rows_scanned": 0,
            "eligible_gene_id_rows": 0,
            "overlay_matched_rows": 0,
            "clinical_evidence_rows_written": 0,
            "frequency_profile_rows_written": 0,
            "functional_impact_rows_written": 0,
            "mitocarta_gene_matches": 0,
            "epi25_gene_matches": 0,
            "both_overlay_gene_matches": 0,
            "status": "not_started",
            **seed_audit,
        }

        if not in_path.exists():
            audit["status"] = "missing_input"
            audit_rows.append(audit)
            continue

        try:
            assay_type, run_classification = read_metadata(m_path, sample_id, run_id)

            clinical = con.execute(
                clinical_query, [str(in_path), assay_type, run_classification]
            ).fetchdf()[CLINICAL_COLS]

            frequency = con.execute(
                frequency_query, [str(in_path), assay_type, run_classification]
            ).fetchdf()[FREQUENCY_COLS]

            functional = con.execute(
                functional_query, [str(in_path), assay_type, run_classification]
            ).fetchdf()[FUNCTIONAL_COLS]

            counts = con.execute(COUNTS_QUERY, [str(in_path)]).fetchdf().iloc[0].to_dict()
            for key, value in counts.items():
                audit[key] = int(value) if pd.notna(value) else 0

            audit["clinical_evidence_rows_written"] = len(clinical)
            audit["frequency_profile_rows_written"] = len(frequency)
            audit["functional_impact_rows_written"] = len(functional)
            audit["status"] = "ok"

            clinical_outputs.append(clinical)
            frequency_outputs.append(frequency)
            functional_outputs.append(functional)

            print(
                f"{sample_id}\t{run_id}"
                f"\tclinical={len(clinical)}"
                f"\tfrequency={len(frequency)}"
                f"\tfunctional={len(functional)}"
            )

        except Exception as exc:
            audit["status"] = f"error: {type(exc).__name__}: {exc}"
            audit_rows.append(audit)
            pd.DataFrame(audit_rows).to_csv(AUDIT_OUT, sep="\t", index=False)
            raise

        audit_rows.append(audit)

    if not clinical_outputs:
        pd.DataFrame(audit_rows).to_csv(AUDIT_OUT, sep="\t", index=False)
        raise SystemExit("No clinical output rows produced")

    clinical_final = pd.concat(clinical_outputs, ignore_index=True)[CLINICAL_COLS]
    frequency_final = pd.concat(frequency_outputs, ignore_index=True)[FREQUENCY_COLS]
    functional_final = pd.concat(functional_outputs, ignore_index=True)[FUNCTIONAL_COLS]

    clinical_final.to_csv(CLINICAL_OUT, sep="\t", index=False)
    frequency_final.to_csv(FREQUENCY_OUT, sep="\t", index=False)
    functional_final.to_csv(FUNCTIONAL_OUT, sep="\t", index=False)
    pd.DataFrame(audit_rows).to_csv(AUDIT_OUT, sep="\t", index=False)

    print()
    print(f"Wrote: {CLINICAL_OUT}")
    print(f"Wrote: {FREQUENCY_OUT}")
    print(f"Wrote: {FUNCTIONAL_OUT}")
    print(f"Wrote: {AUDIT_OUT}")
    print(f"Clinical rows: {len(clinical_final)}")
    print(f"Frequency rows: {len(frequency_final)}")
    print(f"Functional rows: {len(functional_final)}")


if __name__ == "__main__":
    main()
