from pathlib import Path
from datetime import datetime, timezone
import argparse
import csv
import logging
import traceback
import duckdb
import yaml

VALUE_COUNT_COLUMNS = ["clinical_evidence","clinical_significance","clinical_status","clinvar_significance","coding_interpretation_label","consequence","epilepsy_flag","frequency_status","functional_impact","gene_mapping_status","impact_class","interpretability_status","is_clinically_supported","is_high_quality","is_lof_candidate","is_potential_artifact","is_rare_candidate","mito_flag","priority_tier","qc_reliability","qc_status","quality_flag","rarity_flag","source_interpretation_label","suggested_validation_method","validation_priority","validation_required","variant_class","variant_effect_severity","variant_origin","variant_type"]

REQUIRED_COLUMNS = ["alternate_allele","chromosome","clinical_evidence","clinical_significance","clinical_status","clinvar_significance","coding_interpretation_label","consequence","epilepsy_flag","frequency_status","functional_impact","gene_id","gene_mapping_status","gene_symbol","gnomad_af","impact_class","interpretability_status","is_clinically_supported","is_high_quality","is_lof_candidate","is_potential_artifact","is_rare_candidate","mito_flag","position","priority_rank","priority_reason","priority_tier","qc_reliability","qc_status","quality_flag","rarity_flag","reference_allele","run_id","sample_id","source_interpretation_label","suggested_validation_method","validation_priority","validation_required","variant_class","variant_effect_severity","variant_id","variant_origin","variant_type"]

def utc_now():
    return datetime.now(timezone.utc).isoformat()

def sql_path(path):
    return str(path).replace("'", "''")

def qident(name):
    return '"' + name.replace('"','""') + '"'

def setup_logger(log_path):
    logger = logging.getLogger("stage12_duckdb_exploration")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()
    fmt = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
    fh = logging.FileHandler(log_path)
    fh.setFormatter(fmt)
    sh = logging.StreamHandler()
    sh.setFormatter(fmt)
    logger.addHandler(fh)
    logger.addHandler(sh)
    return logger

def read_config(config_path):
    with open(config_path, "r") as f:
        cfg = yaml.safe_load(f) or {}
    input_cfg = cfg.get("input", {}) or {}
    sample_id = input_cfg.get("sample_id")
    if not sample_id:
        raise RuntimeError(f"Missing required input.sample_id in {config_path}")
    return {
        "sample_id": str(sample_id),
        "sra_accession": str(input_cfg.get("sra_accession", "")),
        "sample_alias": str(input_cfg.get("sample_alias", "")),
        "assay_type": str(input_cfg.get("assay_type", "")),
        "bioproject_accession": str(input_cfg.get("bioproject_accession", "")),
    }

def write_manifest(path, row):
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(row.keys()), delimiter="\t")
        writer.writeheader()
        writer.writerow(row)

def export_query(con, name, query, output_path, logger, written, failed):
    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        copy_sql = f"COPY ({query}) TO '{sql_path(output_path)}' WITH (HEADER, DELIMITER '\\t')"
        con.execute(copy_sql)
        written.append(str(output_path))
        logger.info(f"WROTE | {name} | {output_path}")
    except Exception as e:
        failed.append(f"{name}:{output_path}")
        logger.error(f"FAILED | {name} | {output_path} | {e}")
        logger.debug(traceback.format_exc())

def main():
    parser = argparse.ArgumentParser(description="Export Stage 12 DuckDB exploration artifacts from a VAP stage_12_validation_candidates.tsv file.")
    parser.add_argument("stage12_tsv", help="Path to run_<id>/processed/stage_12_validation_candidates.tsv")
    args = parser.parse_args()

    tsv_path = Path(args.stage12_tsv).resolve()
    if not tsv_path.exists():
        raise FileNotFoundError(f"Input TSV not found: {tsv_path}")
    if tsv_path.name != "stage_12_validation_candidates.tsv":
        raise RuntimeError(f"Expected file named stage_12_validation_candidates.tsv, got: {tsv_path.name}")

    processed_dir = tsv_path.parent
    run_dir = processed_dir.parent
    run_id = run_dir.name
    config_path = run_dir / "metadata" / "config_snapshot.yaml"
    if not config_path.exists():
        raise FileNotFoundError(f"Missing config snapshot: {config_path}")

    meta = read_config(config_path)
    sample_id = meta["sample_id"]

    exploration_dir = run_dir / "logs" / "stage12_exploration"
    value_counts_dir = exploration_dir / "value_counts"
    unique_genes_dir = exploration_dir / "unique_genes"
    lane_dir = exploration_dir / "lane_candidate_slices"
    for d in [exploration_dir, value_counts_dir, unique_genes_dir, lane_dir]:
        d.mkdir(parents=True, exist_ok=True)

    log_path = exploration_dir / "stage12_exploration_duckdb.log"
    logger = setup_logger(log_path)
    logger.info("Stage12 DuckDB exploration started")
    logger.info(f"Input TSV: {tsv_path}")
    logger.info(f"Run dir: {run_dir}")
    logger.info(f"Run ID: {run_id}")
    logger.info(f"Config snapshot: {config_path}")
    logger.info(f"Metadata: {meta}")

    duckdb_path = exploration_dir / f"{sample_id}_stage12_exploration.duckdb"
    manifest_path = exploration_dir / "stage12_exploration_manifest.tsv"
    written, failed = [], []

    con = duckdb.connect(str(duckdb_path))
    logger.info(f"DuckDB path: {duckdb_path}")

    load_sql = f"""
DROP TABLE IF EXISTS stage12;
CREATE TABLE stage12 AS
SELECT *
FROM read_csv_auto(
    '{sql_path(tsv_path)}',
    delim='\\t',
    header=true,
    all_varchar=true,
    sample_size=-1
);
"""
    con.execute(load_sql)
    n_rows = con.execute("SELECT COUNT(*) FROM main.stage12").fetchone()[0]
    logger.info(f"Loaded main.stage12 rows: {n_rows}")

    sample_rows = con.execute("""
SELECT sample_id, run_id, COUNT(*) AS n_rows
FROM main.stage12
GROUP BY sample_id, run_id
ORDER BY n_rows DESC
""").fetchall()
    logger.info(f"Observed sample/run rows: {sample_rows}")

    existing_cols = {r[1] for r in con.execute("PRAGMA table_info('stage12')").fetchall()}
    missing_required = [c for c in REQUIRED_COLUMNS if c not in existing_cols]
    if missing_required:
        raise RuntimeError(f"Missing required Stage12 columns: {missing_required}")

    for col in VALUE_COUNT_COLUMNS:
        if col not in existing_cols:
            failed.append(f"value_counts__{col}:missing_column")
            logger.warning(f"SKIPPED value_counts__{col}: missing column")
            continue
        query = f"""
SELECT {qident(col)}, COUNT(*) AS count
FROM main.stage12
GROUP BY {qident(col)}
ORDER BY count DESC, {qident(col)} ASC
"""
        export_query(con, f"value_counts__{col}", query, value_counts_dir / f"value_counts__{col}.tsv", logger, written, failed)

    unique_gene_specs = [
        ("tier1_unique_genes", f"{sample_id}_tier1_unique_genes.tsv", """
SELECT gene_symbol, COUNT(*) AS n_variants
FROM main.stage12
WHERE priority_tier LIKE 'tier_1%'
AND gene_symbol IS NOT NULL
AND gene_symbol != ''
GROUP BY gene_symbol
ORDER BY n_variants DESC, gene_symbol ASC
"""),
        ("tier2_unique_genes", f"{sample_id}_tier2_unique_genes.tsv", """
SELECT gene_symbol, COUNT(*) AS n_variants
FROM main.stage12
WHERE priority_tier LIKE 'tier_2%'
AND gene_symbol IS NOT NULL
AND gene_symbol != ''
GROUP BY gene_symbol
ORDER BY n_variants DESC, gene_symbol ASC
"""),
        ("tier3_unique_genes", f"{sample_id}_tier3_unique_genes.tsv", """
SELECT gene_symbol, COUNT(*) AS n_variants
FROM main.stage12
WHERE priority_tier LIKE 'tier_3%'
AND gene_symbol IS NOT NULL
AND gene_symbol != ''
GROUP BY gene_symbol
ORDER BY n_variants DESC, gene_symbol ASC
"""),
        ("tier1_unique_genes_mito_epi_overlay", f"{sample_id}_tier1_unique_genes_mito_epi_overlay.tsv", """
SELECT gene_symbol, COUNT(*) AS n_variants
FROM main.stage12
WHERE priority_tier LIKE 'tier_1%'
AND gene_symbol IS NOT NULL
AND gene_symbol != ''
AND variant_class='coding'
AND (epilepsy_flag='True' OR mito_flag='True')
GROUP BY gene_symbol
ORDER BY n_variants DESC, gene_symbol ASC
"""),
        ("tier2_unique_genes_mito_epi_overlay", f"{sample_id}_tier2_unique_genes_mito_epi_overlay.tsv", """
SELECT gene_symbol, COUNT(*) AS n_variants
FROM main.stage12
WHERE priority_tier LIKE 'tier_2%'
AND gene_symbol IS NOT NULL
AND gene_symbol != ''
AND variant_class='coding'
AND (epilepsy_flag='True' OR mito_flag='True')
GROUP BY gene_symbol
ORDER BY n_variants DESC, gene_symbol ASC
"""),
        ("tier3_unique_genes_mito_epi_overlay", f"{sample_id}_tier3_unique_genes_mito_epi_overlay.tsv", """
SELECT gene_symbol, COUNT(*) AS n_variants
FROM main.stage12
WHERE priority_tier LIKE 'tier_3%'
AND gene_symbol IS NOT NULL
AND gene_symbol != ''
AND variant_class='coding'
AND (epilepsy_flag='True' OR mito_flag='True')
GROUP BY gene_symbol
ORDER BY n_variants DESC, gene_symbol ASC
"""),
    ]

    for name, filename, query in unique_gene_specs:
        export_query(con, name, query, unique_genes_dir / filename, logger, written, failed)

    bucket_specs = [
        ("bucket_1a_validation_routed_epilepsy_mito", f"{sample_id}_bucket_1a_validation_routed_epilepsy_mito.tsv", """
SELECT sample_id, run_id, chromosome, position, reference_allele, alternate_allele, variant_id, gene_symbol, gene_id, variant_class, consequence, functional_impact, clinical_significance, clinical_status, is_clinically_supported, frequency_status, gnomad_af, epilepsy_flag, mito_flag, priority_tier, priority_rank, priority_reason, validation_required, validation_priority, suggested_validation_method, interpretability_status, coding_interpretation_label, qc_status
FROM main.stage12
WHERE variant_class='coding'
AND is_clinically_supported='True'
AND (epilepsy_flag='True' OR mito_flag='True')
AND validation_required='True'
ORDER BY priority_rank ASC, validation_priority ASC, gene_symbol ASC
"""),
        ("bucket_1b_clinically_contextualized_epilepsy_mito", f"{sample_id}_bucket_1b_clinically_contextualized_epilepsy_mito.tsv", """
SELECT sample_id, run_id, chromosome, position, reference_allele, alternate_allele, variant_id, gene_symbol, gene_id, variant_class, consequence, functional_impact, clinical_significance, clinical_status, is_clinically_supported, frequency_status, gnomad_af, epilepsy_flag, mito_flag, priority_tier, priority_rank, priority_reason, validation_required, validation_priority, suggested_validation_method, interpretability_status, coding_interpretation_label, qc_status
FROM main.stage12
WHERE variant_class='coding'
AND is_clinically_supported='True'
AND (epilepsy_flag='True' OR mito_flag='True')
ORDER BY validation_required DESC, priority_rank ASC, gene_symbol ASC
"""),
        ("bucket_2a_rare_impact_coding_triage_summary", f"{sample_id}_bucket_2a_rare_impact_coding_triage_summary.tsv", """
SELECT functional_impact, priority_tier, validation_required, COUNT(*) AS n
FROM main.stage12
WHERE variant_class='coding'
AND frequency_status='rare'
AND functional_impact IN ('missense', 'loss_of_function', 'splice_relevant')
GROUP BY functional_impact, priority_tier, validation_required
ORDER BY n DESC, functional_impact ASC, priority_tier ASC, validation_required DESC
"""),
        ("bucket_2b_rare_impact_tier2", f"{sample_id}_bucket_2b_rare_impact_tier2.tsv", """
SELECT sample_id, run_id, chromosome, position, reference_allele, alternate_allele, variant_id, gene_symbol, gene_id, variant_class, consequence, functional_impact, clinical_significance, clinical_status, is_clinically_supported, frequency_status, gnomad_af, epilepsy_flag, mito_flag, priority_tier, priority_rank, priority_reason, validation_required, validation_priority, suggested_validation_method, interpretability_status, coding_interpretation_label, qc_status
FROM main.stage12
WHERE variant_class='coding'
AND frequency_status='rare'
AND functional_impact IN ('missense', 'loss_of_function', 'splice_relevant')
AND priority_tier LIKE 'tier_2%'
ORDER BY is_clinically_supported DESC, epilepsy_flag DESC, mito_flag DESC, functional_impact ASC, gene_symbol ASC
LIMIT 15
"""),
        ("bucket_2c_rare_impact_deprioritized", f"{sample_id}_bucket_2c_rare_impact_deprioritized.tsv", """
SELECT sample_id, run_id, chromosome, position, reference_allele, alternate_allele, variant_id, gene_symbol, gene_id, variant_class, consequence, functional_impact, clinical_significance, clinical_status, is_clinically_supported, frequency_status, gnomad_af, epilepsy_flag, mito_flag, priority_tier, priority_rank, priority_reason, validation_required, validation_priority, suggested_validation_method, interpretability_status, coding_interpretation_label, qc_status
FROM main.stage12
WHERE variant_class = 'coding'
AND frequency_status = 'rare'
AND functional_impact IN ('missense', 'loss_of_function', 'splice_relevant')
AND validation_required = 'False'
AND (priority_tier LIKE 'tier_3%' OR priority_tier LIKE 'tier_4%')
ORDER BY is_clinically_supported DESC, epilepsy_flag DESC, mito_flag DESC, functional_impact ASC, gene_symbol ASC
LIMIT 15
"""),
        ("bucket_3a_clinvar_supported_deprioritized", f"{sample_id}_bucket_3a_clinvar_supported_deprioritized.tsv", """
SELECT sample_id, run_id, chromosome, position, reference_allele, alternate_allele, variant_id, gene_symbol, gene_id, variant_class, consequence, functional_impact, clinical_significance, clinical_status, is_clinically_supported, frequency_status, gnomad_af, epilepsy_flag, mito_flag, priority_tier, priority_rank, priority_reason, validation_required, validation_priority, suggested_validation_method, interpretability_status, coding_interpretation_label, qc_status
FROM main.stage12
WHERE variant_class='coding'
AND validation_required='False'
AND priority_tier LIKE 'tier_3%'
AND is_clinically_supported='True'
ORDER BY epilepsy_flag DESC, mito_flag DESC, frequency_status ASC, gene_symbol ASC
LIMIT 15
"""),
        ("bucket_3b_tier3_background_summary", f"{sample_id}_bucket_3b_tier3_background_summary.tsv", """
SELECT functional_impact, frequency_status, is_clinically_supported, COUNT(*) AS n
FROM main.stage12
WHERE variant_class='coding'
AND validation_required='False'
AND priority_tier LIKE 'tier_3%'
GROUP BY functional_impact, frequency_status, is_clinically_supported
ORDER BY n DESC, functional_impact ASC, frequency_status ASC, is_clinically_supported DESC
"""),
        ("bucket_4a_representative_noncoding_semantic_exemplars", f"{sample_id}_bucket_4a_representative_noncoding_semantic_exemplars.tsv", """
SELECT sample_id, run_id, chromosome, position, reference_allele, alternate_allele, variant_id, gene_symbol, gene_id, variant_class, consequence, functional_impact, clinical_significance, clinical_status, is_clinically_supported, frequency_status, gnomad_af, epilepsy_flag, mito_flag, priority_tier, priority_rank, priority_reason, validation_required, validation_priority, suggested_validation_method, interpretability_status, qc_status
FROM main.stage12
WHERE variant_class='noncoding'
AND frequency_status='rare'
AND (epilepsy_flag='True' OR mito_flag='True' OR is_clinically_supported='True')
ORDER BY is_clinically_supported DESC, epilepsy_flag DESC, mito_flag DESC, priority_rank ASC, gene_symbol ASC
LIMIT 15
"""),
    ]

    for name, filename, query in bucket_specs:
        export_query(con, name, query, lane_dir / filename, logger, written, failed)

    status = "completed" if not failed else "completed_with_warnings"
    manifest_row = {
        "sample_id": sample_id,
        "sra_accession": meta.get("sra_accession",""),
        "sample_alias": meta.get("sample_alias",""),
        "assay_type": meta.get("assay_type",""),
        "bioproject_accession": meta.get("bioproject_accession",""),
        "run_id": run_id,
        "run_dir": str(run_dir),
        "input_tsv": str(tsv_path),
        "duckdb_path": str(duckdb_path),
        "n_stage12_rows": n_rows,
        "value_counts_dir": str(value_counts_dir),
        "unique_genes_dir": str(unique_genes_dir),
        "lane_candidate_slices_dir": str(lane_dir),
        "status": status,
        "n_files_attempted": len(written) + len(failed),
        "n_files_written": len(written),
        "n_files_failed": len(failed),
        "log_path": str(log_path),
        "failed_outputs": ";".join(failed),
    }
    write_manifest(manifest_path, manifest_row)
    logger.info(f"Manifest written: {manifest_path}")
    logger.info(f"Final status: {status}")
    con.close()

    print("\nStage12 DuckDB exploration complete.")
    print(f"Sample ID: {sample_id}")
    print(f"Run ID: {run_id}")
    print(f"Rows loaded: {n_rows:,}")
    print(f"DuckDB: {duckdb_path}")
    print(f"Value counts: {value_counts_dir}")
    print(f"Unique genes: {unique_genes_dir}")
    print(f"LANE candidate slices: {lane_dir}")
    print(f"Manifest: {manifest_path}")
    print(f"Log: {log_path}")
    print(f"Status: {status}")
    if failed:
        print(f"Warnings: {len(failed)} export(s) failed; inspect log.")

if __name__ == "__main__":
    main()