#!/usr/bin/env python3

# Run from VAP repo root:

    # python scripts/analysis/build_contrast_05_inputs.py


# After validation, a separate packaging step may copy or package `contrast_05_inputs/` into a transport-ready `contrast_05_analysis_bundle/` or `.tar.gz` without returning to raw `results/`.


# ```bash
# tar -czf \
# docs/case_studies/cross_runs/contrasts/contrast_05_analysis_bundle.tar.gz \
# -C docs/case_studies/cross_runs/contrasts \
# contrast_05_inputs
# ```

# Inspect it:

# ```bash
# tar -tzf docs/case_studies/cross_runs/contrasts/contrast_05_analysis_bundle.tar.gz | less
# ```

# Quick size check:

# ```bash
# ls -lh docs/case_studies/cross_runs/contrasts/contrast_05_analysis_bundle.tar.gz
# ```

from __future__ import annotations

from pathlib import Path
import shutil
import pandas as pd


CONTRAST_DIR = Path("docs/case_studies/cross_runs/contrasts/contrast_05_inputs")
MANIFEST_PATH = CONTRAST_DIR / "cohort_manifest.tsv"
AUDIT_PATH = CONTRAST_DIR / "contrast_05_input_build_audit.tsv"
README_PATH = CONTRAST_DIR / "README.md"

CROSS_RUN_TABLES_DIR = Path("docs/case_studies/cross_runs/cross_run_tables")
RESULTS_DIR = Path("results")

GLOBAL_TABLES = [
    "clinical_status_summary.tsv",
    "variant_consequence_summary.tsv",
    "coding_noncoding_consequence_summary.tsv",
]

F4_FIGURES = [
    "f4a_clinvar_significance",
    "f4a_consequence",
    "f4a_pop_freq_bins",
    "f4b_clinvar_significance",
    "f4b_consequence",
    "f4b_pop_freq_bins",
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


def copy_file(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def count_tsv_rows(path: Path) -> int | str:
    try:
        return max(sum(1 for _ in path.open("r")) - 1, 0)
    except Exception:
        return "NA"


def copy_all_tsvs(
    source_dir: Path,
    dest_dir: Path,
    sra: str,
    run_id: str,
    depth_category: str,
    artifact_group: str,
    audit: list[dict[str, object]],
    notes: str,
) -> None:
    if not source_dir.exists():
        audit.append(
            audit_row(
                sra,
                run_id,
                depth_category,
                artifact_group,
                source_dir.name,
                source_dir,
                dest_dir,
                "copy",
                "missing_source",
                0,
                "source directory missing",
            )
        )
        return

    files = sorted(source_dir.glob("*.tsv"))

    if not files:
        audit.append(
            audit_row(
                sra,
                run_id,
                depth_category,
                artifact_group,
                "all_tsvs",
                source_dir,
                dest_dir,
                "copy",
                "zero_rows",
                0,
                "source directory exists but no TSV files found",
            )
        )
        return

    for src in files:
        dst = dest_dir / src.name
        copy_file(src, dst)
        rows = count_tsv_rows(dst)

        audit.append(
            audit_row(
                sra,
                run_id,
                depth_category,
                artifact_group,
                src.name,
                src,
                dst,
                "copy",
                "ok",
                rows,
                notes,
            )
        )


def maybe_create_readme() -> None:
    if README_PATH.exists():
        return

    text = """# Contrast 05 Inputs — Coding vs Noncoding Semantic Composition

This directory contains the governed input substrate for Contrast 05.

The bundle is manifest-driven, SRA-partitioned, and contains compact F4 semantic-composition figures, cross-run semantic summary tables, value-count telemetry outputs, and targeted semantic bucket outputs.

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
        figures_dir = sra_dir / "figures"
        tables_dir = sra_dir / "tables"
        value_counts_dir = sra_dir / "sql_outputs" / "value_counts"
        buckets_dir = sra_dir / "sql_outputs" / "targeted_semantic_buckets"

        for d in [figures_dir, tables_dir, value_counts_dir, buckets_dir]:
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

        # F4 semantic-composition figures
        for figure_stem in F4_FIGURES:
            filename = f"{sra}_{figure_stem}.png"
            src = run_root / "figures" / filename
            dst = figures_dir / filename

            if src.exists():
                copy_file(src, dst)
                audit.append(
                    audit_row(
                        sra,
                        run_id,
                        depth_category,
                        "figure",
                        filename,
                        src,
                        dst,
                        "copy",
                        "ok",
                        "NA",
                        "copied F4 semantic-composition PNG without modification",
                    )
                )
            else:
                audit.append(
                    audit_row(
                        sra,
                        run_id,
                        depth_category,
                        "figure",
                        filename,
                        src,
                        dst,
                        "copy",
                        "missing_source",
                        "NA",
                        "required F4 semantic-composition figure missing",
                    )
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

        # Value-count telemetry outputs
        copy_all_tsvs(
            source_dir=run_root / "logs" / "stage12_exploration" / "value_counts",
            dest_dir=value_counts_dir,
            sra=sra,
            run_id=run_id,
            depth_category=depth_category,
            artifact_group="value_counts",
            audit=audit,
            notes="copied without renaming or content modification",
        )

        # Targeted semantic bucket outputs
        copy_all_tsvs(
            source_dir=run_root / "logs" / "stage12_exploration" / "lane_candidate_slices",
            dest_dir=buckets_dir,
            sra=sra,
            run_id=run_id,
            depth_category=depth_category,
            artifact_group="targeted_semantic_buckets",
            audit=audit,
            notes="copied without renaming or content modification",
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
