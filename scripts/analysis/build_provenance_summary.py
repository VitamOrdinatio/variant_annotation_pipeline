#!/usr/bin/env python3

# run from VAP repo root:
#   python scripts/analysis/build_provenance_summary.py

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import pandas as pd


OUTPUT_COLUMNS = [
    "sample_id",
    "run_id",
    "assay_type",
    "run_classification",
    "assay_metadata_status",
    "run_notes",
    "pipeline_version",
    "status",
    "machine_id",
    "config_path",
    "git_commit",
    "config_hash",
    "reference_genome",
    "reference_fasta_hash_or_size",
    "execution_profile",
]


MANIFEST_ROWS = [
    ("ERR10619203", "ERR10619203", "run_2026_05_30_071639", "WES", "q3"),
    ("ERR10619207", "ERR10619207", "run_2026_06_01_124134", "WES", "q3"),
    ("ERR10619208", "ERR10619208", "run_2026_05_30_151355", "WES", "median"),
    ("ERR10619212", "ERR10619212", "run_2026_05_30_214724", "WES", "q1"),
    ("ERR10619225", "ERR10619225", "run_2026_05_31_091242", "WES", "q3"),
    ("ERR10619230", "ERR10619230", "run_2026_06_01_004903", "WES", "q3"),
    ("ERR10619241", "ERR10619241", "run_2026_06_02_052302", "WES", "q1"),
    ("ERR10619281", "ERR10619281", "run_2026_05_27_233524", "WES", "median"),
    ("ERR10619285", "ERR10619285", "run_2026_06_02_124300", "WES", "median"),
    ("ERR10619300", "ERR10619300", "run_2026_05_27_172531", "WES", "median"),
    ("ERR10619309", "ERR10619309", "run_2026_06_02_181024", "WES", "q1"),
    ("ERR10619330", "ERR10619330", "run_2026_06_01_203130", "WES", "q1"),
    ("SRR12898354", "HG002", "run_2026_06_03_010030", "WGS", "benchmark_wgs"),
]


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Missing required provenance file: {path}")

    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)

    if not isinstance(data, dict):
        raise ValueError(f"Expected JSON object in {path}")

    return data


def require_value(value: Any, field_name: str, path: Path) -> Any:
    if value is None or value == "":
        raise ValueError(f"Missing required field '{field_name}' in {path}")
    return value


def get_pipeline_version(
    run_metadata: dict[str, Any],
    run_fingerprint: dict[str, Any],
    run_metadata_path: Path,
    run_fingerprint_path: Path,
) -> str:
    value = run_metadata.get("run", {}).get("pipeline_version")
    if value:
        return str(value)

    value = run_fingerprint.get("pipeline_version")
    if value:
        return str(value)

    raise ValueError(
        "Missing required pipeline_version in "
        f"{run_metadata_path} and {run_fingerprint_path}"
    )


def build_row(
    source_accession: str,
    sample_id: str,
    manifest_run_id: str,
    assay_type: str,
    run_classification: str,
    results_dir: Path,
) -> dict[str, Any]:
    metadata_dir = results_dir / manifest_run_id / "metadata"
    run_metadata_path = metadata_dir / "run_metadata.json"
    run_fingerprint_path = metadata_dir / "run_fingerprint.json"

    run_metadata = read_json(run_metadata_path)
    run_fingerprint = read_json(run_fingerprint_path)

    run_block = run_metadata.get("run", {})
    if not isinstance(run_block, dict):
        raise ValueError(f"Missing or malformed 'run' block in {run_metadata_path}")

    observed_run_id = require_value(
        run_block.get("run_id"), "run.run_id", run_metadata_path
    )
    if observed_run_id != manifest_run_id:
        raise ValueError(
            f"Run ID mismatch for {source_accession}: "
            f"manifest={manifest_run_id}, run_metadata={observed_run_id}"
        )

    fingerprint_run_id = require_value(
        run_fingerprint.get("run_id"), "run_id", run_fingerprint_path
    )
    if fingerprint_run_id != manifest_run_id:
        raise ValueError(
            f"Run ID mismatch for {source_accession}: "
            f"manifest={manifest_run_id}, run_fingerprint={fingerprint_run_id}"
        )

    run_notes = (
        "hg002_wgs_benchmark"
        if sample_id == "HG002"
        else "epilepsy_wes_cross_run_cohort"
    )

    return {
        "sample_id": sample_id,
        "run_id": manifest_run_id,
        "assay_type": assay_type,
        "run_classification": run_classification,
        "assay_metadata_status": "available",
        "run_notes": run_notes,
        "pipeline_version": get_pipeline_version(
            run_metadata, run_fingerprint, run_metadata_path, run_fingerprint_path
        ),
        "status": require_value(run_block.get("status"), "run.status", run_metadata_path),
        "machine_id": require_value(
            run_block.get("machine_id"), "run.machine_id", run_metadata_path
        ),
        "config_path": require_value(
            run_block.get("config_path"), "run.config_path", run_metadata_path
        ),
        "git_commit": require_value(
            run_fingerprint.get("git_commit"), "git_commit", run_fingerprint_path
        ),
        "config_hash": require_value(
            run_fingerprint.get("config_hash"), "config_hash", run_fingerprint_path
        ),
        "reference_genome": require_value(
            run_fingerprint.get("reference_genome"),
            "reference_genome",
            run_fingerprint_path,
        ),
        "reference_fasta_hash_or_size": require_value(
            run_fingerprint.get("reference_fasta_hash_or_size"),
            "reference_fasta_hash_or_size",
            run_fingerprint_path,
        ),
        "execution_profile": require_value(
            run_fingerprint.get("execution_profile"),
            "execution_profile",
            run_fingerprint_path,
        ),
    }


def validate_output(df: pd.DataFrame) -> None:
    observed_columns = df.columns.tolist()
    if observed_columns != OUTPUT_COLUMNS:
        raise ValueError(
            "Schema mismatch.\n"
            f"Expected: {OUTPUT_COLUMNS}\n"
            f"Observed: {observed_columns}"
        )

    expected_rows = len(MANIFEST_ROWS)
    if len(df) != expected_rows:
        raise ValueError(f"Expected {expected_rows} rows, observed {len(df)}")

    if df["run_id"].duplicated().any():
        duplicated = df.loc[df["run_id"].duplicated(keep=False), "run_id"].tolist()
        raise ValueError(f"Duplicate run_id values detected: {duplicated}")

    if df.isna().any().any():
        bad_columns = df.columns[df.isna().any()].tolist()
        raise ValueError(f"Null values detected in columns: {bad_columns}")

    if not (df.loc[df["sample_id"] == "HG002", "assay_type"] == "WGS").all():
        raise ValueError("HG002 row must use assay_type=WGS")

    if not (
        df.loc[df["sample_id"] == "HG002", "run_classification"] == "benchmark_wgs"
    ).all():
        raise ValueError("HG002 row must use run_classification=benchmark_wgs")


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Build append-ready provenance_summary.new.tsv from VAP run metadata."
        )
    )
    parser.add_argument(
        "--results-dir",
        type=Path,
        default=Path("results"),
        help="Path to VAP results directory containing run_<id> folders.",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=Path(
            "docs/case_studies/cross_runs/cross_run_tables/provenance_summary.new.tsv"
        ),
        help="Output append-ready TSV path.",
    )
    args = parser.parse_args()

    rows = [
        build_row(
            source_accession=source_accession,
            sample_id=sample_id,
            manifest_run_id=run_id,
            assay_type=assay_type,
            run_classification=run_classification,
            results_dir=args.results_dir,
        )
        for source_accession, sample_id, run_id, assay_type, run_classification in MANIFEST_ROWS
    ]

    out_df = pd.DataFrame(rows, columns=OUTPUT_COLUMNS)
    validate_output(out_df)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    out_df.to_csv(args.out, sep="\t", index=False)

    print(f"Wrote: {args.out}")
    print(f"Rows: {len(out_df)}")
    print("Sample IDs:")
    print(out_df["sample_id"].to_string(index=False))


if __name__ == "__main__":
    main()