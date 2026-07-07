#!/usr/bin/env python3
"""
Build VAP-TEP entity package from a completed VAP run.

This script is intentionally non-mutating with respect to existing VAP run
outputs. It only writes under:

    results/<run_id>/tep/

Default behavior:
  - discover required VAP source artifacts
  - copy them unchanged into TEP entity folders
  - compute row_count, column_count, variant_id_count, sha256
  - write entity_inventory.json

Use --dry-run to inspect planned work without copying files.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import shutil
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


TEP_SCHEMA_VERSION = "vap_tep_v1"
ENTITY_BUILDER_VERSION = "0.2.0"


@dataclass(frozen=True)
class ArtifactSpec:
    entity_id: str
    entity_role: str
    source_stage: str
    source_artifact_role: str
    source_pattern: str
    entity_subdir: str
    required: bool = True
    source_root: str = "processed"


@dataclass
class ArtifactInventoryRecord:
    entity_id: str
    entity_role: str
    source_stage: str
    source_artifact_role: str
    source_artifact: str
    transport_path: str | None
    source_artifact_exists: bool
    copied: bool
    required: bool
    size_bytes: int | None
    row_count: int | None
    column_count: int | None
    variant_id_count: int | None
    observed_columns: list[str] | None
    sha256: str | None


@dataclass
class EntityInventoryRecord:
    entity_id: str
    entity_role: str
    source_stage: str
    required: bool

    artifact_count: int
    copied_artifacts: int
    missing_required_artifacts: int

    metric_semantics: str

    total_size_bytes: int | None

    row_count: int | None
    column_count: int | None
    variant_id_count: int | None

    artifacts: list[dict]
    artifact_metrics: dict[str, dict[str, int | list[str] | None]]


ARTIFACT_SPECS = [
    ArtifactSpec(
        entity_id="observation_entity",
        entity_role="observation_entity",
        source_stage="stage07",
        source_artifact_role="stage07_annotated_variants",
        source_pattern="*.annotated_variants.tsv",
        entity_subdir="observation",
    ),
    ArtifactSpec(
        entity_id="normalization_entity",
        entity_role="normalization_entity",
        source_stage="stage08",
        source_artifact_role="stage08_selected_transcript_consequences",
        source_pattern="stage_08_selected_transcript_consequences.tsv",
        entity_subdir="normalization",
    ),
    ArtifactSpec(
        entity_id="normalization_entity",
        entity_role="normalization_entity",
        source_stage="stage08",
        source_artifact_role="stage08_vdb_ready_variants",
        source_pattern="stage_08_vdb_ready_variants.tsv",
        entity_subdir="normalization",
    ),
    ArtifactSpec(
        entity_id="routing_entity",
        entity_role="routing_entity",
        source_stage="stage08",
        source_artifact_role="stage08_coding_candidates",
        source_pattern="coding_candidates.tsv",
        entity_subdir="routing",
    ),
    ArtifactSpec(
        entity_id="routing_entity",
        entity_role="routing_entity",
        source_stage="stage08",
        source_artifact_role="stage08_splice_region_candidates",
        source_pattern="splice_region_candidates.tsv",
        entity_subdir="routing",
    ),
    ArtifactSpec(
        entity_id="routing_entity",
        entity_role="routing_entity",
        source_stage="stage08",
        source_artifact_role="stage08_noncoding_candidates",
        source_pattern="noncoding_candidates.tsv",
        entity_subdir="routing",
    ),
    ArtifactSpec(
        entity_id="coding_interpretation_overlay",
        entity_role="coding_interpretation_overlay",
        source_stage="stage09",
        source_artifact_role="stage09_coding_interpreted",
        source_pattern="stage_09_coding_interpreted.tsv",
        entity_subdir="coding_interpretation",
    ),
    ArtifactSpec(
        entity_id="noncoding_interpretation_overlay",
        entity_role="noncoding_interpretation_overlay",
        source_stage="stage10",
        source_artifact_role="stage10_noncoding_interpreted",
        source_pattern="stage_10_noncoding_interpreted.tsv",
        entity_subdir="noncoding_interpretation",
    ),
    ArtifactSpec(
        entity_id="prioritization_overlay",
        entity_role="prioritization_overlay",
        source_stage="stage11",
        source_artifact_role="stage11_prioritized_variants",
        source_pattern="stage_11_prioritized_variants.tsv",
        entity_subdir="prioritization",
    ),
    ArtifactSpec(
        entity_id="validation_overlay",
        entity_role="validation_overlay",
        source_stage="stage12",
        source_artifact_role="stage12_validation_candidates",
        source_pattern="stage_12_validation_candidates.tsv",
        entity_subdir="validation",
    ),
    ArtifactSpec(
        entity_id="context_sidecar",
        entity_role="context_sidecar",
        source_stage="stage13",
        source_artifact_role="stage13_final_summary",
        source_pattern="stage_13_final_summary.json",
        entity_subdir="context",
    ),
    ArtifactSpec(
        entity_id="context_sidecar",
        entity_role="context_sidecar",
        source_stage="stage13",
        source_artifact_role="stage13_artifact_manifest",
        source_pattern="stage_13_artifact_manifest.json",
        entity_subdir="context",
    ),
    ArtifactSpec(
        entity_id="context_sidecar",
        entity_role="context_sidecar",
        source_stage="stage13",
        source_artifact_role="stage13_run_report",
        source_pattern="stage_13_run_report.md",
        entity_subdir="context",
    ),
    ArtifactSpec(
        entity_id="package_metadata",
        entity_role="package_metadata",
        source_stage="run_metadata",
        source_artifact_role="config_snapshot",
        source_pattern="config_snapshot.yaml",
        entity_subdir="metadata",
        required=True,
        source_root="metadata",
    ),
]


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def safe_id(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9_.-]+", "_", value.strip())
    return cleaned.strip("_") or "unknown"


def infer_sample_id(run_dir: Path, processed_dir: Path) -> str:
    stage07 = find_one(processed_dir, "*.annotated_variants.tsv")
    if stage07 is not None:
        suffix = f"_{run_dir.name}.annotated_variants.tsv"
        name = stage07.name
        if name.endswith(suffix):
            return name[: -len(suffix)]

    return "unknown_sample"


def find_one(directory: Path, pattern: str) -> Path | None:
    matches = sorted(directory.glob(pattern))
    if not matches:
        return None
    if len(matches) > 1:
        raise ValueError(f"Expected one match for {pattern} in {directory}, found {len(matches)}")
    return matches[0]


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while True:
            chunk = handle.read(chunk_size)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def tabular_counts(path: Path) -> tuple[int | None, int | None, int | None, list[str] | None]:
    if path.suffix.lower() != ".tsv":
        return None, None, None, None

    row_count = 0
    column_count: int | None = None
    variant_ids: set[str] | None = None

    with path.open("r", encoding="utf-8", errors="replace", newline="") as handle:
        reader = csv.reader(handle, delimiter="\t")
        try:
            header = next(reader)
        except StopIteration:
            return 0, 0, None, []

        header = [field.strip().replace("\ufeff", "") for field in header]
        observed_columns = list(header)
        column_count = len(header)

        variant_idx = header.index("variant_id") if "variant_id" in header else None
        if variant_idx is not None:
            variant_ids = set()

        for row in reader:
            row_count += 1
            if variant_idx is not None and variant_idx < len(row):
                assert variant_ids is not None
                variant_ids.add(row[variant_idx])

    return row_count, column_count, len(variant_ids) if variant_ids is not None else None, observed_columns


def copy_artifact(source: Path, destination: Path, dry_run: bool) -> bool:
    if dry_run:
        return False

    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)
    return True


def build_record(
    spec: ArtifactSpec,
    source: Path | None,
    package_root: Path,
    dry_run: bool,
) -> ArtifactInventoryRecord:
    if source is None or not source.exists():
        return ArtifactInventoryRecord(
            entity_id=spec.entity_id,
            entity_role=spec.entity_role,
            source_stage=spec.source_stage,
            source_artifact_role=spec.source_artifact_role,
            source_artifact=str(source) if source is not None else "MISSING",
            transport_path=None,
            source_artifact_exists=False,
            copied=False,
            required=spec.required,
            size_bytes=None,
            row_count=None,
            column_count=None,
            observed_columns=None,
            variant_id_count=None,
            sha256=None,
        )

    entity_dir = package_root / "entities" / spec.entity_subdir
    destination = entity_dir / source.name
    copied = copy_artifact(source, destination, dry_run=dry_run)

    (
        row_count,
        column_count,
        variant_id_count,
        observed_columns,
    ) = tabular_counts(source)    

    return ArtifactInventoryRecord(
        entity_id=spec.entity_id,
        entity_role=spec.entity_role,
        source_stage=spec.source_stage,
        source_artifact_role=spec.source_artifact_role,
        source_artifact=str(source),
        transport_path=str(destination.relative_to(package_root)),
        source_artifact_exists=True,
        copied=copied,
        required=spec.required,
        size_bytes=source.stat().st_size,
        row_count=row_count,
        column_count=column_count,
        observed_columns=observed_columns,
        variant_id_count=variant_id_count,
        sha256=sha256_file(source),
    )


def build_entity_records(
    artifact_records: list[ArtifactInventoryRecord],
) -> list[EntityInventoryRecord]:
    grouped: dict[str, list[ArtifactInventoryRecord]] = {}

    for record in artifact_records:
        grouped.setdefault(record.entity_id, []).append(record)

    entities: list[EntityInventoryRecord] = []

    for entity_id in sorted(grouped):
        records = grouped[entity_id]
        first = records[0]

        size_values = [
            record.size_bytes
            for record in records
            if record.size_bytes is not None
        ]

        row_values = [
            record.row_count
            for record in records
            if record.row_count is not None
        ]

        column_values = [
            record.column_count
            for record in records
            if record.column_count is not None
        ]

        variant_id_values = [
            record.variant_id_count
            for record in records
            if record.variant_id_count is not None
        ]

        missing_required = [
            record
            for record in records
            if record.required and not record.source_artifact_exists
        ]

        single_artifact_entity = len(records) == 1

        artifact_metrics = {
            record.source_artifact_role: 
            {
                "row_count": record.row_count,
                "column_count": record.column_count,
                "variant_id_count": record.variant_id_count,
                "size_bytes": record.size_bytes,
                "observed_columns": record.observed_columns,
            }
            for record in records
        }

        entities.append(
            EntityInventoryRecord(
                entity_id=entity_id,
                entity_role=first.entity_role,
                source_stage=first.source_stage,
                required=any(record.required for record in records),
                artifact_count=len(records),
                artifact_metrics=artifact_metrics,
                copied_artifacts=sum(1 for record in records if record.copied),
                missing_required_artifacts=len(missing_required),
                total_size_bytes=sum(size_values) if size_values else None,

                metric_semantics=(
                    "single_artifact_entity_metrics"
                    if single_artifact_entity
                    else "multi_artifact_entity_metrics_available_per_artifact"
                ),

                row_count=(
                    row_values[0]
                    if single_artifact_entity and row_values
                    else None
                ),

                column_count=(
                    column_values[0]
                    if single_artifact_entity and column_values
                    else None
                ),

                variant_id_count=(
                    variant_id_values[0]
                    if single_artifact_entity and variant_id_values
                    else None
                ),

                artifacts=[asdict(record) for record in records],
            )
        )

    return entities


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
        handle.write("\n")


def build_entities(
    run_dir: Path,
    output_root: Path | None,
    dry_run: bool,
    overwrite: bool,
) -> Path:
    processed_dir = run_dir / "processed"
    metadata_dir = run_dir / "metadata"
    if not run_dir.exists():
        raise FileNotFoundError(f"Run directory does not exist: {run_dir}")
    if not processed_dir.exists():
        raise FileNotFoundError(f"Processed directory does not exist: {processed_dir}")
    if not metadata_dir.exists():
        raise FileNotFoundError(f"Metadata directory does not exist: {metadata_dir}")

    run_id = run_dir.name
    sample_id = infer_sample_id(run_dir, processed_dir)
    tep_id = f"vap_tep_{safe_id(sample_id)}_{safe_id(run_id)}_v1"

    tep_root = output_root or (run_dir / "tep")
    package_root = tep_root / tep_id

    if package_root.exists() and not overwrite and not dry_run:
        raise FileExistsError(
            f"TEP package already exists: {package_root}. "
            "Use --overwrite to replace it."
        )

    if package_root.exists() and overwrite and not dry_run:
        shutil.rmtree(package_root)

    if not dry_run:
        package_root.mkdir(parents=True, exist_ok=True)

    records: list[ArtifactInventoryRecord] = []

    for spec in ARTIFACT_SPECS:
        if spec.source_root == "processed":
            source_dir = processed_dir
        elif spec.source_root == "metadata":
            source_dir = metadata_dir
        else:
            raise ValueError(f"Unsupported source_root for {spec.source_artifact_role}: {spec.source_root}")

        source = find_one(source_dir, spec.source_pattern)
        records.append(
            build_record(
                spec=spec,
                source=source,
                package_root=package_root,
                dry_run=dry_run,
            )
        )

    missing_required = [
        record
        for record in records
        if record.required and not record.source_artifact_exists
    ]

    entity_records = build_entity_records(records)

    inventory = {
        "inventory_type": "vap_tep_entity_inventory",
        "inventory_schema_version": "0.1.0",
        "entity_builder_version": ENTITY_BUILDER_VERSION,
        "tep_id": tep_id,
        "tep_schema_version": TEP_SCHEMA_VERSION,
        "created_utc": utc_now(),
        "dry_run": dry_run,
        "source_run": {
            "sample_id": sample_id,
            "run_id": run_id,
            "run_directory": str(run_dir),
            "processed_directory": str(processed_dir),
            "metadata_directory": str(metadata_dir),
        },
        "package": {
            "package_root": str(package_root),
            "package_format": "directory",
        },
        "summary": {
            "entity_records": len(entity_records),
            "artifact_records": len(records),
            "missing_required_artifacts": len(missing_required),
            "copied_artifacts": sum(1 for record in records if record.copied),
        },
        "entities": [asdict(record) for record in entity_records],
        "artifacts": [asdict(record) for record in records],
    }

    if not dry_run:
        write_json(package_root / "entity_inventory.json", inventory)

    if missing_required:
        missing = "\n".join(
            f"- {record.source_stage} / {record.source_artifact_role}: {record.source_artifact}"
            for record in missing_required
        )
        raise FileNotFoundError(f"Missing required VAP-TEP source artifacts:\n{missing}")

    print("VAP-TEP entity extraction complete.")
    print(f"  dry_run: {dry_run}")
    print(f"  sample_id: {sample_id}")
    print(f"  run_id: {run_id}")
    print(f"  tep_id: {tep_id}")
    print(f"  package_root: {package_root}")
    print(f"  entity_records: {len(entity_records)}")
    print(f"  artifact_records: {len(records)}")
    print(f"  copied_artifacts: {sum(1 for record in records if record.copied)}")
    print(f"  missing_required_artifacts: {len(missing_required)}")

    return package_root


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build VAP-TEP entity package from a completed VAP run."
    )
    parser.add_argument(
        "--run-dir",
        type=Path,
        required=True,
        help="Completed VAP run directory, e.g. results/run_2026_06_03_010030",
    )
    parser.add_argument(
        "--output-root",
        type=Path,
        default=None,
        help="Optional TEP output root. Defaults to <run-dir>/tep",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Inventory source artifacts without copying or writing package files.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Replace an existing TEP package.",
    )
    args = parser.parse_args()

    build_entities(
        run_dir=args.run_dir.expanduser().resolve(),
        output_root=args.output_root.expanduser().resolve() if args.output_root else None,
        dry_run=args.dry_run,
        overwrite=args.overwrite,
    )


if __name__ == "__main__":
    main()