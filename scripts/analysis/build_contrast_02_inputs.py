#!/usr/bin/env python3

# Run from VAP repo root:
    # python scripts/analysis/build_contrast_02_inputs.py

# This script builds the governed input substrate for Contrast 02, which is focused on interoperability substrate stability. The bundle is manifest-driven, SRA-partitioned, and contains compact interoperability-focused VAP outputs for downstream comparative synthesis. Source `results/` artifacts are treated as immutable and are only read or copied.

# When validated, user manually runs this block to compress and package bundles:
    # ```bash
    # tar -czf \
    # docs/case_studies/cross_runs/contrasts/contrast_02_analysis_bundle.tar.gz \
    # -C docs/case_studies/cross_runs/contrasts \
    # contrast_02_inputs
    # ```

    # Inspect it:

    # ```bash
    # tar -tzf docs/case_studies/cross_runs/contrasts/contrast_02_analysis_bundle.tar.gz | less
    # ```

    # Quick size check:

    # ```bash
    # ls -lh docs/case_studies/cross_runs/contrasts/contrast_02_analysis_bundle.tar.gz
    # ```



from __future__ import annotations

from pathlib import Path
import shutil
import pandas as pd


CONTRAST_DIR = Path("docs/case_studies/cross_runs/contrasts/contrast_02_inputs")
MANIFEST_PATH = CONTRAST_DIR / "cohort_manifest.tsv"
AUDIT_PATH = CONTRAST_DIR / "contrast_02_input_build_audit.tsv"
README_PATH = CONTRAST_DIR / "README.md"

CROSS_RUN_TABLES_DIR = Path("docs/case_studies/cross_runs/cross_run_tables")
RESULTS_DIR = Path("results")

GLOBAL_TABLES = [
    "candidate_reviewability_readiness.tsv",
    "overlay_gene_coding_clinical_evidence.tsv",
    "overlay_gene_coding_frequency_profiles.tsv",
    "overlay_gene_coding_functional_impact.tsv",
    "substrate_dimension_summary.tsv",
    "gene_list_overlay_intersections.tsv",
]

REQUIRED_TIER_FILES = {
    "tier1": "tier1_unique_genes.tsv",
    "tier2": "tier2_unique_genes.tsv",
    "tier3": "tier3_unique_genes.tsv",
}


def read_simple_yaml(path: Path) -> dict[str, str]:
    data = {}
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        k, v = line.split(":", 1)
        data[k.strip()] = v.strip().strip('"').strip("'")
    return data


def audit_row(
    sra: str,
    run_id: str,
    depth_category: str,
    artifact_group: str,
    artifact_name: str,
    source_path: Path | str,
    destination_path: Path | str,
    operation: str,
    status: str,
    rows_written: int | str = "NA",
    notes: str = "",
) -> dict[str, object]:
    return {
        "SRA": sra,
        "run_id": run_id,
        "depth_category": depth_category,
        "artifact_group": artifact_group,
        "artifact_name": artifact_name,
        "source_path": str(source_path),
        "destination_path": str(destination_path),
        "operation": operation,
        "status": status,
        "rows_written": rows_written,
        "notes": notes,
    }


def normalize_manifest(df: pd.DataFrame) -> pd.DataFrame:
    rename_map = {
        "SRA_accn": "SRA",
        "VAP_run_id": "run_id",
        "Depth_Category": "depth_category",
    }
    df = df.rename(columns=rename_map)

    required = {"SRA", "run_id", "depth_category"}
    missing = required - set(df.columns)
    if missing:
        raise SystemExit(f"Manifest missing required columns after normalization: {sorted(missing)}")

    out = df[["SRA", "run_id", "depth_category"]].copy()
    for col in out.columns:
        out[col] = out[col].astype(str).str.strip()

    return out


def subset_global_table(table_path: Path, run_id: str) -> pd.DataFrame:
    df = pd.read_csv(table_path, sep="\t", dtype=str)

    if "run_id" not in df.columns:
        raise ValueError(f"{table_path} lacks required run_id column")

    return df[df["run_id"].astype(str).str.strip() == run_id].copy()


def copy_file(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def maybe_create_readme() -> list[dict[str, object]]:
    if README_PATH.exists():
        return []

    text = """# Contrast 02 Inputs — Interoperability Substrate Stability

This directory contains the governed input substrate for Contrast 02.

The bundle is manifest-driven, SRA-partitioned, and contains compact interoperability-focused VAP outputs for downstream comparative synthesis.

Source `results/` artifacts are treated as immutable and are only read or copied.
"""

    README_PATH.write_text(text)
    return []


def main() -> None:
    if not MANIFEST_PATH.exists():
        raise SystemExit(f"Missing manifest: {MANIFEST_PATH}")

    CONTRAST_DIR.mkdir(parents=True, exist_ok=True)

    manifest = normalize_manifest(pd.read_csv(MANIFEST_PATH, sep="\t", dtype=str))
    if len(manifest) != 12:
        raise SystemExit(f"Expected 12 WES rows in cohort_manifest.tsv, found {len(manifest)}")    
    audit: list[dict[str, object]] = []

    maybe_create_readme()

    for _, rec in manifest.iterrows():
        sra = rec["SRA"]
        run_id = rec["run_id"]
        depth_category = rec["depth_category"]

        sra_dir = CONTRAST_DIR / sra
        figures_dir = sra_dir / "figures"
        tables_dir = sra_dir / "tables"
        targeted_dir = sra_dir / "sql_outputs" / "targeted_semantic_buckets"
        tiered_dir = sra_dir / "sql_outputs" / "tiered_gene_outputs"

        for d in [figures_dir, tables_dir, targeted_dir, tiered_dir]:
            d.mkdir(parents=True, exist_ok=True)
            audit.append(
                audit_row(
                    sra, run_id, depth_category,
                    "directory", d.name, "", d,
                    "mkdir", "ok", "NA", "directory ensured"
                )
            )

        run_root = RESULTS_DIR / run_id

        fig_yaml = run_root / "metadata" / "figure_set_resolved.yaml"

        if not fig_yaml.exists():
            raise SystemExit(f"Missing figure_set_resolved.yaml: {fig_yaml}")

        y = read_simple_yaml(fig_yaml)

        if y.get("sample_id") != sra:
            raise SystemExit(
                f"Sample mismatch in {fig_yaml}: manifest={sra}, yaml={y.get('sample_id')}"
            )

        if y.get("run_id") != run_id:
            raise SystemExit(
                f"Run mismatch in {fig_yaml}: manifest={run_id}, yaml={y.get('run_id')}"
            )

        # F5 figure
        f5_src = run_root / "figures" / f"{sra}_f5_interoperability_substrates.png"
        f5_dst = figures_dir / f5_src.name

        if f5_src.exists():
            copy_file(f5_src, f5_dst)
            status = "ok"
            notes = "copied actual VAP pluralized F5 filename"
        else:
            status = "missing_source"
            notes = "required F5 figure missing"

        audit.append(
            audit_row(
                sra, run_id, depth_category,
                "figure", f5_src.name, f5_src, f5_dst,
                "copy", status, "NA", notes
            )
        )

        # SRA-specific table subsets
        for table_name in GLOBAL_TABLES:
            src = CROSS_RUN_TABLES_DIR / table_name
            dst = tables_dir / table_name

            if not src.exists():
                audit.append(
                    audit_row(
                        sra, run_id, depth_category,
                        "table", table_name, src, dst,
                        "subset", "missing_source", 0, "global cross-run table missing"
                    )
                )
                continue

            try:
                sub = subset_global_table(src, run_id)
                sub.to_csv(dst, sep="\t", index=False)

                status = "ok" if len(sub) > 0 else "zero_rows"
                audit.append(
                    audit_row(
                        sra, run_id, depth_category,
                        "table", table_name, src, dst,
                        "subset", status, len(sub), "subset by exact run_id"
                    )
                )
            except Exception as exc:
                audit.append(
                    audit_row(
                        sra, run_id, depth_category,
                        "table", table_name, src, dst,
                        "subset", "error", 0, f"{type(exc).__name__}: {exc}"
                    )
                )

        # Targeted semantic buckets: copy all present TSVs without renaming
        bucket_src_dir = run_root / "logs" / "stage12_exploration" / "lane_candidate_slices"

        if bucket_src_dir.exists():
            bucket_files = sorted(bucket_src_dir.glob("*.tsv"))
            if not bucket_files:
                audit.append(
                    audit_row(
                        sra, run_id, depth_category,
                        "targeted_semantic_buckets", "all_bucket_tsvs",
                        bucket_src_dir, targeted_dir,
                        "copy", "zero_rows", 0, "source directory exists but no TSVs found"
                    )
                )

            for src in bucket_files:
                dst = targeted_dir / src.name

                df = pd.read_csv(src, sep="\t", dtype=str)

                if "gene_symbol" in df.columns:
                    df["gene_symbol"] = (
                        df["gene_symbol"]
                        .fillna("NO_GENE_SYMBOL")
                        .astype(str)
                        .str.strip()
                        .replace({"": "NO_GENE_SYMBOL", "nan": "NO_GENE_SYMBOL", "NaN": "NO_GENE_SYMBOL"})
                    )

                df.to_csv(dst, sep="\t", index=False)
                rows = len(df)

                audit.append(
                    audit_row(
                        sra, run_id, depth_category,
                        "targeted_semantic_buckets", src.name,
                        src, dst,
                        "copy", "ok", rows, "copied without renaming; gene_symbol missing values canonicalized to NO_GENE_SYMBOL when present"
                    )
                )
        else:
            audit.append(
                audit_row(
                    sra, run_id, depth_category,
                    "targeted_semantic_buckets", "lane_candidate_slices",
                    bucket_src_dir, targeted_dir,
                    "copy", "missing_source", 0, "lane_candidate_slices directory missing"
                )
            )

        # Tiered unique gene outputs: copy required tier1/2/3 with contract-facing names
        unique_gene_dir = run_root / "logs" / "stage12_exploration" / "unique_genes"

        for tier, dst_name in REQUIRED_TIER_FILES.items():
            src = unique_gene_dir / f"{sra}_{tier}_unique_genes.tsv"
            dst = tiered_dir / dst_name

            if src.exists():
                df = pd.read_csv(src, sep="\t", dtype=str)

                if "gene_symbol" in df.columns:
                    df["gene_symbol"] = (
                        df["gene_symbol"]
                        .fillna("NO_GENE_SYMBOL")
                        .astype(str)
                        .str.strip()
                        .replace({
                            "": "NO_GENE_SYMBOL",
                            "nan": "NO_GENE_SYMBOL",
                            "NaN": "NO_GENE_SYMBOL",
                        })
                    )

                dst.parent.mkdir(parents=True, exist_ok=True)
                df.to_csv(dst, sep="\t", index=False)
                rows = len(df)

                audit.append(
                    audit_row(
                        sra, run_id, depth_category,
                        "tiered_gene_outputs", dst_name,
                        src, dst,
                        "copy", "ok", rows,
                        "copied with contract-facing filename; gene_symbol missing values canonicalized to NO_GENE_SYMBOL"
                    )
                )
            else:
                audit.append(
                    audit_row(
                        sra, run_id, depth_category,
                        "tiered_gene_outputs", dst_name,
                        src, dst,
                        "copy", "missing_source", 0,
                        "required tiered unique gene file missing"
                    )
                )

    audit_df = pd.DataFrame(audit)
    audit_df.to_csv(AUDIT_PATH, sep="\t", index=False)

    print(f"Wrote audit: {AUDIT_PATH}")
    print(f"Manifest rows: {len(manifest)}")
    print(f"Audit rows: {len(audit_df)}")
    print(f"Statuses:")
    print(audit_df["status"].value_counts().to_string())


if __name__ == "__main__":
    main()
