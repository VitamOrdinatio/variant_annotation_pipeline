#!/usr/bin/env python3

# run from VAP repo root:
#    python scripts/analysis/build_contrast_03_inputs.py

# When validated, user manually runs this block to compress and package bundles:
    # ```bash
    # tar -czf \
    # docs/case_studies/cross_runs/contrasts/contrast_03_analysis_bundle.tar.gz \
    # -C docs/case_studies/cross_runs/contrasts \
    # contrast_03_inputs
    # ```

    # Inspect it:

    # ```bash
    # tar -tzf docs/case_studies/cross_runs/contrasts/contrast_03_analysis_bundle.tar.gz | less
    # ```

    # Quick size check:

    # ```bash
    # ls -lh docs/case_studies/cross_runs/contrasts/contrast_03_analysis_bundle.tar.gz
    # ```


from __future__ import annotations

from pathlib import Path
import shutil
import pandas as pd


CONTRAST_DIR = Path("docs/case_studies/cross_runs/contrasts/contrast_03_inputs")
MANIFEST_PATH = CONTRAST_DIR / "cohort_manifest.tsv"
AUDIT_PATH = CONTRAST_DIR / "contrast_03_input_build_audit.tsv"
README_PATH = CONTRAST_DIR / "README.md"

CROSS_RUN_TABLES_DIR = Path("docs/case_studies/cross_runs/cross_run_tables")
RESULTS_DIR = Path("results")

GLOBAL_TABLES = [
    "runtime_stage_summary.tsv",
    "provenance_summary.tsv",
]

DEPTH_METADATA_TABLE = "sra_run_depth_metadata.tsv"

METADATA_FILES = [
    "config_snapshot.yaml",
    "run_fingerprint.json",
    "run_metadata.json",
    "runtime_profile.tsv",
]

CONTINUITY_PROBE_FILES = [
    "tier1",
    "tier2",
    "tier3",
]


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
        raise SystemExit(
            f"Manifest missing required columns after normalization: {sorted(missing)}"
        )

    out = df[["SRA", "run_id", "depth_category"]].copy()
    for col in out.columns:
        out[col] = out[col].astype(str).str.strip()

    return out


def subset_by_run_id(table_path: Path, run_id: str) -> pd.DataFrame:
    df = pd.read_csv(table_path, sep="\t", dtype=str)

    if "run_id" not in df.columns:
        raise ValueError(f"{table_path} lacks required run_id column")

    return df[df["run_id"].astype(str).str.strip() == run_id].copy()


def subset_depth_metadata(table_path: Path, sra: str) -> pd.DataFrame:
    df = pd.read_csv(table_path, sep="\t", dtype=str)

    if "SRA" not in df.columns:
        raise ValueError(f"{table_path} lacks required SRA column")

    return df[df["SRA"].astype(str).str.strip() == sra].copy()


def copy_file(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def count_tsv_rows(path: Path) -> int | str:
    try:
        return max(sum(1 for _ in path.open("r")) - 1, 0)
    except Exception:
        return "NA"


def maybe_create_readme() -> None:
    if README_PATH.exists():
        return

    text = """# Contrast 03 Inputs — Runtime Telemetry vs Sequencing Depth

This directory contains the governed input substrate for Contrast 03.

The bundle is manifest-driven, SRA-partitioned, and contains compact runtime, provenance, depth, and continuity-probe artifacts for downstream comparative synthesis.

Source `results/` artifacts are treated as immutable and are only read or copied.
"""

    README_PATH.write_text(text)


def main() -> None:
    if not MANIFEST_PATH.exists():
        raise SystemExit(f"Missing manifest: {MANIFEST_PATH}")

    CONTRAST_DIR.mkdir(parents=True, exist_ok=True)

    manifest = normalize_manifest(pd.read_csv(MANIFEST_PATH, sep="\t", dtype=str))

    if len(manifest) != 12:
        raise SystemExit(
            f"Expected 12 WES rows in cohort_manifest.tsv, found {len(manifest)}"
        )

    audit: list[dict[str, object]] = []

    maybe_create_readme()

    for _, rec in manifest.iterrows():
        sra = rec["SRA"]
        run_id = rec["run_id"]
        depth_category = rec["depth_category"]

        sra_dir = CONTRAST_DIR / sra
        tables_dir = sra_dir / "tables"
        metadata_dir = sra_dir / "metadata"
        continuity_dir = sra_dir / "continuity_probes"

        for d in [tables_dir, metadata_dir, continuity_dir]:
            d.mkdir(parents=True, exist_ok=True)
            audit.append(
                audit_row(
                    sra,
                    run_id,
                    depth_category,
                    "directory",
                    d.name,
                    "",
                    d,
                    "mkdir",
                    "ok",
                    "NA",
                    "directory ensured",
                )
            )

        run_root = RESULTS_DIR / run_id

        # Run identity guardrail
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

        # SRA-specific table subsets by run_id
        for table_name in GLOBAL_TABLES:
            src = CROSS_RUN_TABLES_DIR / table_name
            dst = tables_dir / table_name

            if not src.exists():
                audit.append(
                    audit_row(
                        sra,
                        run_id,
                        depth_category,
                        "table",
                        table_name,
                        src,
                        dst,
                        "subset",
                        "missing_source",
                        0,
                        "global cross-run table missing",
                    )
                )
                continue

            try:
                sub = subset_by_run_id(src, run_id)
                dst.parent.mkdir(parents=True, exist_ok=True)
                sub.to_csv(dst, sep="\t", index=False)

                status = "ok" if len(sub) > 0 else "zero_rows"
                audit.append(
                    audit_row(
                        sra,
                        run_id,
                        depth_category,
                        "table",
                        table_name,
                        src,
                        dst,
                        "subset",
                        status,
                        len(sub),
                        "subset by exact run_id",
                    )
                )
            except Exception as exc:
                audit.append(
                    audit_row(
                        sra,
                        run_id,
                        depth_category,
                        "table",
                        table_name,
                        src,
                        dst,
                        "subset",
                        "error",
                        0,
                        f"{type(exc).__name__}: {exc}",
                    )
                )

        # SRA-specific read-depth metadata by SRA
        depth_src = CROSS_RUN_TABLES_DIR / DEPTH_METADATA_TABLE
        depth_dst = metadata_dir / DEPTH_METADATA_TABLE

        if not depth_src.exists():
            audit.append(
                audit_row(
                    sra,
                    run_id,
                    depth_category,
                    "metadata",
                    DEPTH_METADATA_TABLE,
                    depth_src,
                    depth_dst,
                    "subset",
                    "missing_source",
                    0,
                    "depth metadata table missing",
                )
            )
        else:
            try:
                sub = subset_depth_metadata(depth_src, sra)
                depth_dst.parent.mkdir(parents=True, exist_ok=True)
                sub.to_csv(depth_dst, sep="\t", index=False)

                status = "ok" if len(sub) > 0 else "zero_rows"
                audit.append(
                    audit_row(
                        sra,
                        run_id,
                        depth_category,
                        "metadata",
                        DEPTH_METADATA_TABLE,
                        depth_src,
                        depth_dst,
                        "subset",
                        status,
                        len(sub),
                        "subset by exact SRA",
                    )
                )
            except Exception as exc:
                audit.append(
                    audit_row(
                        sra,
                        run_id,
                        depth_category,
                        "metadata",
                        DEPTH_METADATA_TABLE,
                        depth_src,
                        depth_dst,
                        "subset",
                        "error",
                        0,
                        f"{type(exc).__name__}: {exc}",
                    )
                )

        # Run-specific metadata files
        for filename in METADATA_FILES:
            src = run_root / "metadata" / filename
            dst = metadata_dir / filename

            if src.exists():
                copy_file(src, dst)
                rows = count_tsv_rows(dst) if filename.endswith(".tsv") else "NA"
                audit.append(
                    audit_row(
                        sra,
                        run_id,
                        depth_category,
                        "metadata",
                        filename,
                        src,
                        dst,
                        "copy",
                        "ok",
                        rows,
                        "copied without modification",
                    )
                )
            else:
                audit.append(
                    audit_row(
                        sra,
                        run_id,
                        depth_category,
                        "metadata",
                        filename,
                        src,
                        dst,
                        "copy",
                        "missing_source",
                        0,
                        "required metadata file missing",
                    )
                )

        # Continuity probe files
        unique_gene_dir = run_root / "logs" / "stage12_exploration" / "unique_genes"

        for tier in CONTINUITY_PROBE_FILES:
            filename = f"{sra}_{tier}_unique_genes.tsv"
            src = unique_gene_dir / filename
            dst = continuity_dir / filename

            if src.exists():
                copy_file(src, dst)
                rows = count_tsv_rows(dst)
                audit.append(
                    audit_row(
                        sra,
                        run_id,
                        depth_category,
                        "continuity_probe",
                        filename,
                        src,
                        dst,
                        "copy",
                        "ok",
                        rows,
                        "copied without renaming or content modification",
                    )
                )
            else:
                audit.append(
                    audit_row(
                        sra,
                        run_id,
                        depth_category,
                        "continuity_probe",
                        filename,
                        src,
                        dst,
                        "copy",
                        "missing_source",
                        0,
                        "required continuity probe file missing",
                    )
                )

    audit_df = pd.DataFrame(audit)
    audit_df.to_csv(AUDIT_PATH, sep="\t", index=False)

    print(f"Wrote audit: {AUDIT_PATH}")
    print(f"Manifest rows: {len(manifest)}")
    print(f"Audit rows: {len(audit_df)}")
    print("Statuses:")
    print(audit_df["status"].value_counts().to_string())


if __name__ == "__main__":
    main()
