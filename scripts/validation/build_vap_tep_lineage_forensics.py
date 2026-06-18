#!/usr/bin/env python3
"""
Build deterministic VAP-TEP lineage forensics tables across production runs.

Outputs:
  - vap_tep_lineage_artifact_inventory.tsv
  - vap_tep_lineage_transition_summary.tsv
  - vap_tep_lineage_column_catalog.tsv
  - vap_tep_lineage_column_recommendations.tsv
  - vap_tep_lineage_report.md
"""

from __future__ import annotations

import argparse
import csv
import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


RUN_MANIFEST = [
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
    ("hg002", "run_2026_06_03_010030", "hg002"),
]


SURFACE_ORDER = [
    "stage07_annotated",
    "stage08_selected",
    "stage08_vdb",
    "stage08_coding",
    "stage08_splice",
    "stage08_noncoding",
    "stage08_variant_summary",
    "stage08_rdgp_seed",
    "stage09_coding_interpreted",
    "stage10_noncoding_interpreted",
    "stage11_prioritized",
    "stage11_gene_counts",
    "stage12_validation",
]


TRANSITIONS = [
    ("stage07_annotated", "stage08_selected"),
    ("stage08_selected", "stage08_vdb"),
    ("stage08_vdb", "stage09_coding_interpreted"),
    ("stage08_vdb", "stage10_noncoding_interpreted"),
    ("stage09_coding_interpreted", "stage11_prioritized"),
    ("stage10_noncoding_interpreted", "stage11_prioritized"),
    ("stage11_prioritized", "stage12_validation"),
]


@dataclass(frozen=True)
class Artifact:
    sample_id: str
    run_id: str
    depth_category: str
    surface: str
    path: Path
    exists: bool
    size_bytes: int | None
    row_count: int | None
    column_count: int | None
    header_sha256: str | None
    has_variant_id: bool
    distinct_variant_ids: int | None
    columns: tuple[str, ...]


def normalize_header_value(value: str) -> str:
    return value.strip().replace("\ufeff", "")


def read_header(path: Path) -> tuple[str, ...]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.reader(handle, delimiter="\t")
        try:
            return tuple(normalize_header_value(v) for v in next(reader))
        except StopIteration:
            return tuple()


def header_sha256(columns: Iterable[str]) -> str:
    normalized = "\t".join(columns) + "\n"
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def count_rows_and_variant_ids(
    path: Path,
    columns: tuple[str, ...],
) -> tuple[int, int | None]:

    variant_idx = (
        columns.index("variant_id")
        if "variant_id" in columns
        else None
    )

    variant_ids: set[str] = set()

    row_count = 0

    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.reader(handle, delimiter="\t")

        try:
            next(reader)
        except StopIteration:
            return 0, 0 if variant_idx is not None else None

        for row in reader:
            row_count += 1

            if (
                variant_idx is not None
                and variant_idx < len(row)
            ):
                variant_ids.add(row[variant_idx])

    return (
        row_count,
        len(variant_ids) if variant_idx is not None else None,
    )


def find_stage07(processed_dir: Path) -> Path | None:
    matches = sorted(processed_dir.glob("*.annotated_variants.tsv"))
    return matches[0] if matches else None


def surface_paths(processed_dir: Path) -> dict[str, Path | None]:
    return {
        "stage07_annotated": find_stage07(processed_dir),
        "stage08_selected": processed_dir / "stage_08_selected_transcript_consequences.tsv",
        "stage08_vdb": processed_dir / "stage_08_vdb_ready_variants.tsv",
        "stage08_coding": processed_dir / "coding_candidates.tsv",
        "stage08_splice": processed_dir / "splice_region_candidates.tsv",
        "stage08_noncoding": processed_dir / "noncoding_candidates.tsv",
        "stage08_variant_summary": processed_dir / "stage_08_variant_summary.tsv",
        "stage08_rdgp_seed": processed_dir / "stage_08_rdgp_gene_evidence_seed.tsv",
        "stage09_coding_interpreted": processed_dir / "stage_09_coding_interpreted.tsv",
        "stage10_noncoding_interpreted": processed_dir / "stage_10_noncoding_interpreted.tsv",
        "stage11_prioritized": processed_dir / "stage_11_prioritized_variants.tsv",
        "stage11_gene_counts": processed_dir / "stage_11_gene_variant_counts.tsv",
        "stage12_validation": processed_dir / "stage_12_validation_candidates.tsv",
    }


def build_artifact(
    sample_id: str,
    run_id: str,
    depth_category: str,
    surface: str,
    path: Path | None,
) -> Artifact:
    if path is None or not path.exists():
        return Artifact(
            sample_id=sample_id,
            run_id=run_id,
            depth_category=depth_category,
            surface=surface,
            path=path or Path("MISSING"),
            exists=False,
            size_bytes=None,
            row_count=None,
            column_count=None,
            header_sha256=None,
            has_variant_id=False,
            distinct_variant_ids=None,
            columns=tuple(),
        )

    columns = read_header(path)
    row_count, distinct_variant_ids = count_rows_and_variant_ids(path, columns)

    return Artifact(
        sample_id=sample_id,
        run_id=run_id,
        depth_category=depth_category,
        surface=surface,
        path=path,
        exists=True,
        size_bytes=path.stat().st_size,
        row_count=row_count,
        column_count=len(columns),
        header_sha256=header_sha256(columns),
        has_variant_id="variant_id" in columns,
        distinct_variant_ids=distinct_variant_ids,
        columns=columns,
    )


def classify_column(column: str) -> tuple[str, str, str, str]:
    identity = {
        "sample_id", "run_id", "source_pipeline", "variant_id", "chromosome",
        "position", "reference_allele", "alternate_allele",
    }
    observation = {
        "variant_type", "variant_class", "quality_flag", "gene_id", "gene_symbol",
        "transcript_id", "consequence", "impact_class", "impact",
        "clinical_significance", "clinvar_significance", "population_frequency",
        "gnomad_af", "exac_af", "thousand_genomes_af", "mito_flag", "epilepsy_flag",
    }
    stage08_context = {
        "annotation_source", "annotation_version", "gene_mapping_status",
        "variant_context", "variant_effect_severity", "qc_status",
        "interpretability_status", "frequency_status", "clinical_status",
        "gene_symbols", "worst_consequence", "highest_impact", "canonical_present",
        "coding_flag", "splice_flag", "noncoding_flag", "transcript_count",
    }
    coding = {
        "functional_impact", "coding_interpretation_label", "is_lof_candidate",
    }
    noncoding = {
        "noncoding_functional_context", "noncoding_interpretation_label",
        "is_regulatory_candidate",
    }
    shared_interpretation = {
        "rarity_flag", "clinical_evidence", "qc_reliability",
        "is_rare_candidate", "is_clinically_supported", "is_high_quality",
        "is_potential_artifact",
    }
    prioritization = {
        "variant_origin", "source_interpretation_label", "priority_tier",
        "priority_rank", "priority_reason", "is_high_priority_candidate",
        "is_moderate_priority_candidate", "is_low_priority_candidate",
        "is_uninterpretable",
    }
    validation = {
        "validation_required", "validation_priority", "suggested_validation_method",
        "validation_reason",
    }
    gene_summary = {
        "variant_count", "high_impact_variant_count", "rare_variant_count",
        "pathogenic_variant_count", "max_variant_severity", "has_low_quality_evidence",
        "contributing_variant_ids",
    }

    if column in identity:
        return ("identity", "preserve", "ingest", "Core variant/run identity.")
    if column in observation:
        return ("observation", "preserve", "ingest", "Stage07 observation-layer evidence.")
    if column in stage08_context:
        return ("routing_context", "preserve", "ingest", "Stage08 routing/interoperability context.")
    if column in coding:
        return ("coding_interpretation", "preserve_as_overlay", "ingest_optional_overlay", "Coding-specific interpretation.")
    if column in noncoding:
        return ("noncoding_interpretation", "preserve_as_overlay", "ingest_optional_overlay", "Noncoding-specific interpretation; may not survive Stage11/12 literally.")
    if column in shared_interpretation:
        return ("interpretation", "preserve", "ingest", "Shared interpretation/QC field.")
    if column in prioritization:
        return ("prioritization", "preserve", "ingest", "Stage11 prioritization field.")
    if column in validation:
        return ("validation_handoff", "preserve", "ingest", "Stage12 validation handoff field.")
    if column in gene_summary:
        return ("gene_summary", "preserve_as_summary", "ingest_optional_summary", "Gene-level derived summary.")
    return ("unclassified", "review", "review", "Needs manual review.")


def write_tsv(path: Path, rows: Iterable[dict[str, object]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path.home() / "dev/portfolio_projects/variant_annotation_pipeline",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path("/root/Desktop/vap_tep_lineage_forensics"),
    )
    args = parser.parse_args()

    repo_root = args.repo_root.expanduser().resolve()
    out_dir = args.out_dir.expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    artifacts: list[Artifact] = []

    for sample_id, run_id, depth_category in RUN_MANIFEST:
        processed_dir = repo_root / "results" / run_id / "processed"
        paths = surface_paths(processed_dir)

        for surface in SURFACE_ORDER:
            artifacts.append(
                build_artifact(
                    sample_id=sample_id,
                    run_id=run_id,
                    depth_category=depth_category,
                    surface=surface,
                    path=paths[surface],
                )
            )

    artifact_by_run_surface = {(a.run_id, a.surface): a for a in artifacts}

    inventory_rows = [
        {
            "sample_id": a.sample_id,
            "run_id": a.run_id,
            "depth_category": a.depth_category,
            "surface": a.surface,
            "exists": a.exists,
            "path": str(a.path),
            "size_bytes": a.size_bytes,
            "row_count": a.row_count,
            "column_count": a.column_count,
            "header_sha256": a.header_sha256,
            "has_variant_id": a.has_variant_id,
            "distinct_variant_ids": a.distinct_variant_ids,
        }
        for a in artifacts
    ]

    transition_rows: list[dict[str, object]] = []
    for sample_id, run_id, depth_category in RUN_MANIFEST:
        for from_surface, to_surface in TRANSITIONS:
            left = artifact_by_run_surface[(run_id, from_surface)]
            right = artifact_by_run_surface[(run_id, to_surface)]

            left_cols = set(left.columns)
            right_cols = set(right.columns)

            transition_rows.append(
                {
                    "sample_id": sample_id,
                    "run_id": run_id,
                    "depth_category": depth_category,
                    "from_surface": from_surface,
                    "to_surface": to_surface,
                    "from_exists": left.exists,
                    "to_exists": right.exists,
                    "from_rows": left.row_count,
                    "to_rows": right.row_count,
                    "row_delta_to_minus_from": (
                        right.row_count - left.row_count
                        if left.row_count is not None and right.row_count is not None
                        else None
                    ),
                    "from_distinct_variant_ids": left.distinct_variant_ids,
                    "to_distinct_variant_ids": right.distinct_variant_ids,
                    "variant_id_delta_to_minus_from": (
                        right.distinct_variant_ids - left.distinct_variant_ids
                        if left.distinct_variant_ids is not None and right.distinct_variant_ids is not None
                        else None
                    ),
                    "from_column_count": left.column_count,
                    "to_column_count": right.column_count,
                    "removed_columns": ",".join(sorted(left_cols - right_cols)),
                    "added_columns": ",".join(sorted(right_cols - left_cols)),
                    "shared_columns": ",".join(sorted(left_cols & right_cols)),
                }
            )

    column_observations: dict[str, set[str]] = {}
    for artifact in artifacts:
        if not artifact.exists:
            continue
        for column in artifact.columns:
            column_observations.setdefault(column, set()).add(artifact.surface)

    surface_rank = {surface: i for i, surface in enumerate(SURFACE_ORDER)}

    catalog_rows = []
    recommendation_rows = []

    for column in sorted(column_observations):
        surfaces = sorted(column_observations[column], key=lambda s: surface_rank.get(s, 999))
        first_surface = surfaces[0]
        last_surface = surfaces[-1]
        role, tep_rec, vdb_rec, notes = classify_column(column)

        row = {
            "column": column,
            "first_surface": first_surface,
            "last_surface": last_surface,
            "observed_surfaces": ",".join(surfaces),
            "semantic_role": role,
            "tep_recommendation": tep_rec,
            "vdb_recommendation": vdb_rec,
            "notes": notes,
        }
        catalog_rows.append(row)
        recommendation_rows.append(row)

    write_tsv(
        out_dir / "vap_tep_lineage_artifact_inventory.tsv",
        inventory_rows,
        [
            "sample_id", "run_id", "depth_category", "surface", "exists", "path",
            "size_bytes", "row_count", "column_count", "header_sha256",
            "has_variant_id", "distinct_variant_ids",
        ],
    )

    write_tsv(
        out_dir / "vap_tep_lineage_transition_summary.tsv",
        transition_rows,
        [
            "sample_id", "run_id", "depth_category", "from_surface", "to_surface",
            "from_exists", "to_exists", "from_rows", "to_rows",
            "row_delta_to_minus_from", "from_distinct_variant_ids",
            "to_distinct_variant_ids", "variant_id_delta_to_minus_from",
            "from_column_count", "to_column_count", "removed_columns",
            "added_columns", "shared_columns",
        ],
    )

    write_tsv(
        out_dir / "vap_tep_lineage_column_catalog.tsv",
        catalog_rows,
        [
            "column", "first_surface", "last_surface", "observed_surfaces",
            "semantic_role", "tep_recommendation", "vdb_recommendation", "notes",
        ],
    )

    write_tsv(
        out_dir / "vap_tep_lineage_column_recommendations.tsv",
        recommendation_rows,
        [
            "column", "semantic_role", "tep_recommendation",
            "vdb_recommendation", "first_surface", "last_surface",
            "observed_surfaces", "notes",
        ],
    )

    report_path = out_dir / "vap_tep_lineage_report.md"
    with report_path.open("w", encoding="utf-8") as handle:
        handle.write("# VAP-TEP Lineage Forensics Report\n\n")
        handle.write(f"Repo root: `{repo_root}`\n\n")
        handle.write("## Outputs\n\n")
        for filename in [
            "vap_tep_lineage_artifact_inventory.tsv",
            "vap_tep_lineage_transition_summary.tsv",
            "vap_tep_lineage_column_catalog.tsv",
            "vap_tep_lineage_column_recommendations.tsv",
        ]:
            handle.write(f"- `{filename}`\n")
        handle.write("\n## High-Level QA\n\n")
        handle.write(f"- Runs audited: {len(RUN_MANIFEST)}\n")
        handle.write(f"- Artifact observations: {len(artifacts)}\n")
        handle.write(f"- Transition observations: {len(transition_rows)}\n")
        handle.write(f"- Unique columns observed: {len(catalog_rows)}\n\n")

        missing = [a for a in artifacts if not a.exists]
        handle.write("## Missing Artifacts\n\n")
        if not missing:
            handle.write("None.\n\n")
        else:
            for a in missing:
                handle.write(f"- {a.sample_id} / {a.run_id} / {a.surface}\n")
            handle.write("\n")

        handle.write("## Recommended Interpretation\n\n")
        handle.write(
            "Use the TSV outputs, not this Markdown report, as the source of truth "
            "for downstream VAP-TEP documentation and contract drafting.\n"
        )

    print("Wrote:")
    for output in sorted(out_dir.iterdir()):
        print(f"  {output}")


if __name__ == "__main__":
    main()