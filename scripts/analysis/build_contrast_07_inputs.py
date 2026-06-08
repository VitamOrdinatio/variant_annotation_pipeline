#!/usr/bin/env python3

# Run from VAP repo root:

#   python scripts/analysis/build_contrast_07_inputs.py


# After validation, a separate packaging step may copy or package `contrast_07_inputs/` into a transport-ready `contrast_07_analysis_bundle/` or `.tar.gz` without returning to raw `results/`.


# ```bash
# tar -czf \
# docs/case_studies/cross_runs/contrasts/contrast_07_analysis_bundle.tar.gz \
# -C docs/case_studies/cross_runs/contrasts \
# contrast_07_inputs
# ```

# Inspect it:

# ```bash
# tar -tzf docs/case_studies/cross_runs/contrasts/contrast_07_analysis_bundle.tar.gz | less
# ```

# Quick size check:

# ```bash
# ls -lh docs/case_studies/cross_runs/contrasts/contrast_07_analysis_bundle.tar.gz
# ```




from __future__ import annotations

from pathlib import Path
import shutil
import pandas as pd


CONTRAST_DIR = Path("docs/case_studies/cross_runs/contrasts/contrast_07_inputs")
MANIFEST_PATH = CONTRAST_DIR / "cohort_manifest.tsv"
AUDIT_PATH = CONTRAST_DIR / "contrast_07_input_build_audit.tsv"
README_PATH = CONTRAST_DIR / "README.md"

CROSS_RUN_TABLES_DIR = Path("docs/case_studies/cross_runs/cross_run_tables")
RESULTS_DIR = Path("results")

RUN_ID_TABLES = [
    "provenance_summary.tsv",
    "runtime_stage_summary.tsv",
    "stage_funnel_summary.tsv",
]

SRA_TABLES = [
    "sra_run_depth_metadata.tsv",
]

METRICS_JSON_FILES = [
    "stage_05_variant_calling_metrics.json",
    "stage_06_normalization_metrics.json",
    "stage_07_annotation_metrics.json",
    "stage_08_partition_metrics.json",
    "stage_09_coding_interpretation_metrics.json",
    "stage_10_noncoding_interpretation_metrics.json",
    "stage_11_prioritization_metrics.json",
    "stage_12_validation_metrics.json",
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


def subset_by_sra(table_path: Path, sra: str) -> pd.DataFrame:
    df = pd.read_csv(table_path, sep="\t", dtype=str)

    if "SRA" not in df.columns:
        raise ValueError(f"{table_path} lacks required SRA column")

    return df[df["SRA"].astype(str).str.strip() == sra].copy()


def copy_file(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def maybe_create_readme() -> None:
    if README_PATH.exists():
        return

    text = """# Contrast 07 Inputs — Provenance Transition Determinism

This directory contains the governed input substrate for Contrast 07.

The bundle is manifest-driven, SRA-partitioned, and contains compact provenance summaries, runtime telemetry summaries, stage-funnel summaries, depth metadata, and stage-specific metrics JSON files.

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
        metrics_dir = sra_dir / "metrics"

        for d in [tables_dir, metrics_dir]:
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

        # Tables subset by run_id
        for table_name in RUN_ID_TABLES:
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

        # Tables subset by SRA
        for table_name in SRA_TABLES:
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
                sub = subset_by_sra(src, sra)
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
                        "subset by exact SRA",
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

        # Stage-specific metrics JSON files
        for filename in METRICS_JSON_FILES:
            src = run_root / "metrics" / filename
            dst = metrics_dir / filename

            if src.exists():
                copy_file(src, dst)
                audit.append(
                    audit_row(
                        sra,
                        run_id,
                        depth_category,
                        "metrics_json",
                        filename,
                        src,
                        dst,
                        "copy",
                        "ok",
                        "NA",
                        "copied without renaming or content modification",
                    )
                )
            else:
                audit.append(
                    audit_row(
                        sra,
                        run_id,
                        depth_category,
                        "metrics_json",
                        filename,
                        src,
                        dst,
                        "copy",
                        "missing_source",
                        0,
                        "required stage-specific metrics JSON missing",
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
