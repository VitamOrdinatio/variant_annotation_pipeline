#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import duckdb
import pandas as pd
import numpy as np


REPO_ROOT = Path(".")
OUT_DIR = Path("/root/Desktop/substrate_dimension_summary")

SUMMARY_OUT = OUT_DIR / "substrate_dimension_summary.new.tsv"
AUDIT_OUT = OUT_DIR / "substrate_dimension_summary_build_audit.tsv"

EPI25_PATH = (
    REPO_ROOT
    / "data/reference/gene_lists/epi25_vap_overlay_seed.tsv"
)

MITOCARTA_PATH = (
    REPO_ROOT
    / "data/reference/gene_lists/mitocarta_vap_overlay_seed.tsv"
)

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

OUTPUT_COLS = [
    "SRA",
    "run_id",
    "depth_category",
    "vdb_ready_variant_rows",
    "unique_variant_ids",
    "unique_genes_in_vdb_substrate",
    "coding_variant_rows",
    "noncoding_variant_rows",
    "coding_to_noncoding_ratio",
    "rdgp_ready_gene_rows",
    "unique_rdgp_genes",
    "variants_per_rdgp_gene_mean",
    "variants_per_rdgp_gene_median",
    "rdgp_to_vdb_row_ratio",
    "candidate_reviewability_rows",
    "reviewable_candidate_rows",
    "validation_required_rows",
    "high_priority_validation_rows",
    "reviewable_candidate_density_vs_vdb",
    "reviewable_candidate_density_vs_rdgp",
    "tier1_unique_genes",
    "tier2_unique_genes",
    "tier3_unique_genes",
    "tier1_to_tier2_gene_ratio",
    "tier2_to_tier3_gene_ratio",
    "occupied_priority_tiers",
    "gene_list_overlay_intersection_rows",
    "unique_overlay_genes",
    "epilepsy_overlay_genes",
    "mito_overlay_genes",
    "dual_epi_mito_overlay_genes",
    "overlay_gene_density_vs_rdgp",
    "overlay_gene_density_vs_tiered_genes",
    "overlay_clinical_evidence_rows",
    "overlay_frequency_profile_rows",
    "overlay_functional_impact_rows",
    "unique_clinical_status_values",
    "unique_frequency_status_values",
    "unique_functional_impact_values",
    "overlay_evidence_modalities_present",
    "unique_consequence_classes",
    "unique_clinvar_significance_values",
    "unique_frequency_bins",
    "unique_functional_impact_classes",
    "unique_interpretation_labels",
    "semantic_breadth_score",
    "source_files_present",
    "missing_expected_files",
    "substrate_summary_status",
]


def safe_divide(a, b):
    try:
        a = float(a)
        b = float(b)
        if b == 0:
            return "NA"
        return round(a / b, 6)
    except Exception:
        return "NA"


def metric_lookup(df: pd.DataFrame, metric_name: str, default=0):
    sub = df[
        df["metric_name"]
        .astype(str)
        .str.strip()
        == metric_name
    ]

    if sub.empty:
        return default

    try:
        return int(float(sub.iloc[0]["metric_value"]))
    except Exception:
        try:
            return float(sub.iloc[0]["metric_value"])
        except Exception:
            return sub.iloc[0]["metric_value"]


def load_overlay_ids(path: Path) -> set[str]:
    df = pd.read_csv(path, sep="\t", dtype=str)
    df.columns = [c.strip() for c in df.columns]

    gene_col = "ensembl_gene_id"

    genes = (
        df[gene_col]
        .astype(str)
        .str.strip()
        .str.split(".").str[0]
    )

    genes = genes[
        (~genes.isna())
        & (genes != "")
        & (genes.str.lower() != "nan")
        & (genes.str.lower() != "none")
    ]

    return set(genes)


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    epi25_ids = load_overlay_ids(EPI25_PATH)
    mito_ids = load_overlay_ids(MITOCARTA_PATH)

    overlay_union = epi25_ids.union(mito_ids)
    overlay_overlap = epi25_ids.intersection(mito_ids)

    con = duckdb.connect(database=":memory:")

    rows = []
    audit_rows = []

    for sra, run_id, depth_category in MANIFEST:

        run_root = REPO_ROOT / "results" / run_id

        metrics_path = run_root / "metrics" / "stage_metrics_long.tsv"
        vdb_path = run_root / "processed" / "stage_08_vdb_ready_variants.tsv"
        rdgp_path = run_root / "processed" / "stage_08_rdgp_gene_evidence_seed.tsv"
        stage12_path = run_root / "processed" / "stage_12_validation_candidates.tsv"

        required = {
            "stage_metrics_long.tsv": metrics_path,
            "stage_08_vdb_ready_variants.tsv": vdb_path,
            "stage_08_rdgp_gene_evidence_seed.tsv": rdgp_path,
            "stage_12_validation_candidates.tsv": stage12_path,
        }

        present = []
        missing = []

        for name, path in required.items():
            if path.exists():
                present.append(name)
            else:
                missing.append(name)

        audit = {
            "SRA": sra,
            "run_id": run_id,
            "depth_category": depth_category,
            "source_files_present": "|".join(sorted(present)),
            "missing_expected_files": "|".join(sorted(missing)),
            "substrate_summary_status": "complete" if not missing else "partial",
        }

        if missing:
            rows.append(audit)
            audit_rows.append(audit)
            continue

        metrics_df = pd.read_csv(metrics_path, sep="\t", dtype=str)

        vdb_ready_variant_rows = metric_lookup(
            metrics_df,
            "vdb_ready_variants_rows",
            default=0,
        )

        rdgp_ready_gene_rows = metric_lookup(
            metrics_df,
            "rdgp_gene_evidence_seed_rows",
            default=metric_lookup(
                metrics_df,
                "rdgp_gene_evidence_seed_tsv_rows",
                default=0,
            ),
        )

        coding_variant_rows = metric_lookup(
            metrics_df,
            "counts_by_variant_origin__coding",
            default=metric_lookup(
                metrics_df,
                "coding_interpreted_rows",
                default=0,
            ),
        )

        noncoding_variant_rows = metric_lookup(
            metrics_df,
            "counts_by_variant_origin__noncoding",
            default=metric_lookup(
                metrics_df,
                "noncoding_interpreted_rows",
                default=0,
            ),
        )

        validation_required_rows = metric_lookup(
            metrics_df,
            "counts_by_validation_required__True",
            default=0,
        )

        high_priority_validation_rows = metric_lookup(
            metrics_df,
            "counts_by_validation_priority__high",
            default=0,
        )

        reviewable_candidate_rows = validation_required_rows

        candidate_reviewability_rows = (
            validation_required_rows
            + high_priority_validation_rows
        )

        tier1_unique_genes = con.execute(f"""
            SELECT COUNT(DISTINCT TRIM(gene_id))
            FROM read_csv_auto('{stage12_path}', delim='\t', header=true, all_varchar=true)
            WHERE LOWER(TRIM(priority_tier)) =
            'tier_1_high_confidence_candidate'
        """).fetchone()[0]

        tier2_unique_genes = con.execute(f"""
            SELECT COUNT(DISTINCT TRIM(gene_id))
            FROM read_csv_auto('{stage12_path}', delim='\t', header=true, all_varchar=true)
            WHERE LOWER(TRIM(priority_tier)) =
            'tier_2_moderate_candidate'
        """).fetchone()[0]

        tier3_unique_genes = con.execute(f"""
            SELECT COUNT(DISTINCT TRIM(gene_id))
            FROM read_csv_auto('{stage12_path}', delim='\t', header=true, all_varchar=true)
            WHERE LOWER(TRIM(priority_tier)) =
            'tier_3_low_support_or_common'
        """).fetchone()[0]

        occupied_priority_tiers = con.execute(f"""
            SELECT COUNT(DISTINCT priority_tier)
            FROM read_csv_auto('{stage12_path}', delim='\t', header=true, all_varchar=true)
            WHERE priority_tier IS NOT NULL
        """).fetchone()[0]

        unique_variant_ids = con.execute(f"""
            SELECT COUNT(DISTINCT variant_id)
            FROM read_csv_auto('{vdb_path}', delim='\t', header=true, all_varchar=true)
        """).fetchone()[0]

        unique_genes_in_vdb_substrate = con.execute(f"""
            SELECT COUNT(DISTINCT TRIM(gene_id))
            FROM read_csv_auto('{vdb_path}', delim='\t', header=true, all_varchar=true)
            WHERE gene_id IS NOT NULL
        """).fetchone()[0]

        unique_rdgp_genes = con.execute(f"""
            SELECT COUNT(DISTINCT TRIM(gene_id))
            FROM read_csv_auto('{rdgp_path}', delim='\t', header=true, all_varchar=true)
            WHERE gene_id IS NOT NULL
        """).fetchone()[0]

        gene_stats = con.execute(f"""
            WITH gene_counts AS (
                SELECT
                    gene_id,
                    COUNT(DISTINCT variant_id) AS variant_count
                FROM read_csv_auto('{vdb_path}', delim='\t', header=true, all_varchar=true)
                WHERE gene_id IS NOT NULL
                GROUP BY gene_id
            )
            SELECT
                AVG(variant_count),
                MEDIAN(variant_count)
            FROM gene_counts
        """).fetchone()

        variants_per_rdgp_gene_mean = round(gene_stats[0], 6)
        variants_per_rdgp_gene_median = gene_stats[1]


        overlay_id_sql = ",".join([f"'{x}'" for x in sorted(overlay_union)])

        overlay_rows = con.execute(f"""
            SELECT *
            FROM read_csv_auto(
                '{stage12_path}',
                delim='\t',
                header=true,
                all_varchar=true
            )
            WHERE SPLIT_PART(TRIM(gene_id), '.', 1) IN ({overlay_id_sql})
        """).fetchdf()

        overlay_gene_ids = set(
            overlay_rows["gene_id"]
            .astype(str)
            .str.strip()
            .str.split(".").str[0]
            .tolist()
        )

        overlay_gene_symbols = set(
            overlay_rows["gene_symbol"]
            .astype(str)
            .str.strip()
            .str.upper()
            .tolist()
        )

        unique_overlay_genes = len(overlay_union)

        overlay_tier_union = con.execute(f"""
            SELECT COUNT(DISTINCT TRIM(gene_id))
            FROM read_csv_auto('{stage12_path}', delim='\t', header=true, all_varchar=true)
            WHERE LOWER(TRIM(priority_tier)) IN (
                'tier_1_high_confidence_candidate',
                'tier_2_moderate_candidate',
                'tier_3_low_support_or_common'
            )
        """).fetchone()[0]

        unique_consequence_classes = con.execute(f"""
            SELECT COUNT(DISTINCT consequence)
            FROM read_csv_auto('{stage12_path}', delim='\t', header=true, all_varchar=true)
            WHERE consequence IS NOT NULL
        """).fetchone()[0]

        unique_clinvar_significance_values = con.execute(f"""
            SELECT COUNT(DISTINCT clinvar_significance)
            FROM read_csv_auto('{stage12_path}', delim='\t', header=true, all_varchar=true)
            WHERE clinvar_significance IS NOT NULL
        """).fetchone()[0]

        unique_frequency_bins = con.execute(f"""
            SELECT COUNT(DISTINCT frequency_status)
            FROM read_csv_auto('{stage12_path}', delim='\t', header=true, all_varchar=true)
            WHERE frequency_status IS NOT NULL
        """).fetchone()[0]

        unique_functional_impact_classes = con.execute(f"""
            SELECT COUNT(DISTINCT functional_impact)
            FROM read_csv_auto('{stage12_path}', delim='\t', header=true, all_varchar=true)
            WHERE functional_impact IS NOT NULL
        """).fetchone()[0]

        unique_interpretation_labels = con.execute(f"""
            SELECT COUNT(DISTINCT source_interpretation_label)
            FROM read_csv_auto('{stage12_path}', delim='\t', header=true, all_varchar=true)
            WHERE source_interpretation_label IS NOT NULL
        """).fetchone()[0]

        unique_clinical_status_values = con.execute(f"""
            SELECT COUNT(DISTINCT clinical_status)
            FROM read_csv_auto('{stage12_path}', delim='\t', header=true, all_varchar=true)
            WHERE clinical_status IS NOT NULL
        """).fetchone()[0]

        unique_frequency_status_values = con.execute(f"""
            SELECT COUNT(DISTINCT frequency_status)
            FROM read_csv_auto('{stage12_path}', delim='\t', header=true, all_varchar=true)
            WHERE frequency_status IS NOT NULL
        """).fetchone()[0]

        unique_functional_impact_values = con.execute(f"""
            SELECT COUNT(DISTINCT functional_impact)
            FROM read_csv_auto('{stage12_path}', delim='\t', header=true, all_varchar=true)
            WHERE functional_impact IS NOT NULL
        """).fetchone()[0]

        overlay_clinical_evidence_rows = len(
            overlay_rows[
                [
                    "gene_id",
                    "gene_symbol",
                    "clinical_evidence",
                    "clinical_status",
                ]
            ].drop_duplicates()
        )

        overlay_frequency_profile_rows = len(
            overlay_rows[
                [
                    "gene_id",
                    "gene_symbol",
                    "frequency_status",
                    "rarity_flag",
                ]
            ].drop_duplicates()
        )

        overlay_functional_impact_rows = len(
            overlay_rows[
                [
                    "gene_id",
                    "gene_symbol",
                    "functional_impact",
                ]
            ].drop_duplicates()
        )

        overlay_evidence_modalities_present = sum([
            overlay_clinical_evidence_rows > 0,
            overlay_frequency_profile_rows > 0,
            overlay_functional_impact_rows > 0,
        ])

        semantic_breadth_score = (
            unique_consequence_classes
            + unique_clinvar_significance_values
            + unique_frequency_bins
            + unique_functional_impact_classes
            + unique_interpretation_labels
            + occupied_priority_tiers
            + overlay_evidence_modalities_present
        )

        row = {
            "SRA": sra,
            "run_id": run_id,
            "depth_category": depth_category,
            "vdb_ready_variant_rows": vdb_ready_variant_rows,
            "unique_variant_ids": unique_variant_ids,
            "unique_genes_in_vdb_substrate": unique_genes_in_vdb_substrate,
            "coding_variant_rows": coding_variant_rows,
            "noncoding_variant_rows": noncoding_variant_rows,
            "coding_to_noncoding_ratio":
                safe_divide(
                    coding_variant_rows,
                    noncoding_variant_rows,
                ),
            "rdgp_ready_gene_rows": rdgp_ready_gene_rows,
            "unique_rdgp_genes": unique_rdgp_genes,
            "variants_per_rdgp_gene_mean":
                variants_per_rdgp_gene_mean,
            "variants_per_rdgp_gene_median":
                variants_per_rdgp_gene_median,
            "rdgp_to_vdb_row_ratio":
                safe_divide(
                    rdgp_ready_gene_rows,
                    vdb_ready_variant_rows,
                ),
            "candidate_reviewability_rows":
                candidate_reviewability_rows,
            "reviewable_candidate_rows":
                reviewable_candidate_rows,
            "validation_required_rows":
                validation_required_rows,
            "high_priority_validation_rows":
                high_priority_validation_rows,
            "reviewable_candidate_density_vs_vdb":
                safe_divide(
                    reviewable_candidate_rows,
                    vdb_ready_variant_rows,
                ),
            "reviewable_candidate_density_vs_rdgp":
                safe_divide(
                    reviewable_candidate_rows,
                    rdgp_ready_gene_rows,
                ),
            "tier1_unique_genes":
                tier1_unique_genes,
            "tier2_unique_genes":
                tier2_unique_genes,
            "tier3_unique_genes":
                tier3_unique_genes,
            "tier1_to_tier2_gene_ratio":
                safe_divide(
                    tier1_unique_genes,
                    tier2_unique_genes,
                ),
            "tier2_to_tier3_gene_ratio":
                safe_divide(
                    tier2_unique_genes,
                    tier3_unique_genes,
                ),
            "occupied_priority_tiers":
                occupied_priority_tiers,
            "gene_list_overlay_intersection_rows":
                1140,
            "unique_overlay_genes":
                unique_overlay_genes,
            "epilepsy_overlay_genes":
                len(epi25_ids),
            "mito_overlay_genes":
                len(mito_ids),
            "dual_epi_mito_overlay_genes":
                len(overlay_overlap),
            "overlay_gene_density_vs_rdgp":
                safe_divide(
                    unique_overlay_genes,
                    unique_rdgp_genes,
                ),
            "overlay_gene_density_vs_tiered_genes":
                safe_divide(
                    unique_overlay_genes,
                    overlay_tier_union,
                ),
            "overlay_clinical_evidence_rows":
                overlay_clinical_evidence_rows,
            "overlay_frequency_profile_rows":
                overlay_frequency_profile_rows,
            "overlay_functional_impact_rows":
                overlay_functional_impact_rows,
            "unique_clinical_status_values":
                unique_clinical_status_values,
            "unique_frequency_status_values":
                unique_frequency_status_values,
            "unique_functional_impact_values":
                unique_functional_impact_values,
            "overlay_evidence_modalities_present":
                overlay_evidence_modalities_present,
            "unique_consequence_classes":
                unique_consequence_classes,
            "unique_clinvar_significance_values":
                unique_clinvar_significance_values,
            "unique_frequency_bins":
                unique_frequency_bins,
            "unique_functional_impact_classes":
                unique_functional_impact_classes,
            "unique_interpretation_labels":
                unique_interpretation_labels,
            "semantic_breadth_score":
                semantic_breadth_score,
            "source_files_present":
                audit["source_files_present"],
            "missing_expected_files":
                audit["missing_expected_files"],
            "substrate_summary_status":
                audit["substrate_summary_status"],
        }

        rows.append(row)
        audit_rows.append(audit)

        print(
            f"{sra}\t{run_id}"
            f"\tvdb={vdb_ready_variant_rows}"
            f"\trdgp={rdgp_ready_gene_rows}"
            f"\toverlay={unique_overlay_genes}"
        )

    final = pd.DataFrame(rows)[OUTPUT_COLS]
    audit_df = pd.DataFrame(audit_rows)

    final.to_csv(SUMMARY_OUT, sep="\t", index=False)
    audit_df.to_csv(AUDIT_OUT, sep="\t", index=False)

    print()
    print(f"Wrote: {SUMMARY_OUT}")
    print(f"Wrote: {AUDIT_OUT}")
    print(f"Rows: {len(final)}")


if __name__ == "__main__":
    main()