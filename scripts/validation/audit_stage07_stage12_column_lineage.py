#!/usr/bin/env python3
"""
Build empirical Stage07-Stage12 column lineage table from VAP-TEP
lineage forensics outputs.

Input:
  vap_tep_lineage_column_catalog.tsv

Output:
  vap_tep_column_lineage.tsv

This script is empirical only:
  - no semantic roles
  - no TEP recommendations
  - no VDB recommendations
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


ORDERED_SURFACES = [
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


CANONICAL_STAGE_GROUPS = {
    "stage07": ["stage07_annotated"],
    "stage08": [
        "stage08_selected",
        "stage08_vdb",
        "stage08_coding",
        "stage08_splice",
        "stage08_noncoding",
        "stage08_variant_summary",
        "stage08_rdgp_seed",
    ],
    "stage09": ["stage09_coding_interpreted"],
    "stage10": ["stage10_noncoding_interpreted"],
    "stage11": ["stage11_prioritized", "stage11_gene_counts"],
    "stage12": ["stage12_validation"],
}


def parse_surfaces(value: str) -> set[str]:
    return {item.strip() for item in value.split(",") if item.strip()}


def first_ordered_surface(surfaces: set[str]) -> str:
    for surface in ORDERED_SURFACES:
        if surface in surfaces:
            return surface
    return "NA"


def last_ordered_surface(surfaces: set[str]) -> str:
    for surface in reversed(ORDERED_SURFACES):
        if surface in surfaces:
            return surface
    return "NA"


def stage_presence(surfaces: set[str], stage: str) -> str:
    return "True" if any(surface in surfaces for surface in CANONICAL_STAGE_GROUPS[stage]) else "False"


def surface_presence(surfaces: set[str], surface: str) -> str:
    return "True" if surface in surfaces else "False"


def read_catalog(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        required = {"column", "first_surface", "last_surface", "observed_surfaces"}
        missing = required - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"Column catalog missing required fields: {sorted(missing)}")

        return list(reader)


def write_lineage(path: Path, rows: list[dict[str, str]]) -> None:
    fieldnames = [
        "column",
        "introduced_surface_empirical",
        "last_seen_surface_empirical",
        "introduced_stage_empirical",
        "last_seen_stage_empirical",
        "present_stage07",
        "present_stage08",
        "present_stage09",
        "present_stage10",
        "present_stage11",
        "present_stage12",
    ]

    fieldnames.extend([f"present_{surface}" for surface in ORDERED_SURFACES])
    fieldnames.append("observed_surfaces")

    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def surface_to_stage(surface: str) -> str:
    for stage, surfaces in CANONICAL_STAGE_GROUPS.items():
        if surface in surfaces:
            return stage
    return "NA"


def build_lineage_rows(catalog_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    output_rows: list[dict[str, str]] = []

    for row in catalog_rows:
        column = row["column"]
        surfaces = parse_surfaces(row["observed_surfaces"])

        introduced_surface = first_ordered_surface(surfaces)
        last_seen_surface = last_ordered_surface(surfaces)

        out = {
            "column": column,
            "introduced_surface_empirical": introduced_surface,
            "last_seen_surface_empirical": last_seen_surface,
            "introduced_stage_empirical": surface_to_stage(introduced_surface),
            "last_seen_stage_empirical": surface_to_stage(last_seen_surface),
            "present_stage07": stage_presence(surfaces, "stage07"),
            "present_stage08": stage_presence(surfaces, "stage08"),
            "present_stage09": stage_presence(surfaces, "stage09"),
            "present_stage10": stage_presence(surfaces, "stage10"),
            "present_stage11": stage_presence(surfaces, "stage11"),
            "present_stage12": stage_presence(surfaces, "stage12"),
        }

        for surface in ORDERED_SURFACES:
            out[f"present_{surface}"] = surface_presence(surfaces, surface)

        out["observed_surfaces"] = ",".join(
            surface for surface in ORDERED_SURFACES if surface in surfaces
        )

        output_rows.append(out)

    return sorted(output_rows, key=lambda r: (r["introduced_surface_empirical"], r["column"]))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input-catalog",
        type=Path,
        required=True,
        help="Path to vap_tep_lineage_column_catalog.tsv",
    )
    parser.add_argument(
        "--output",
        type=Path,
        required=True,
        help="Path to write vap_tep_column_lineage.tsv",
    )
    args = parser.parse_args()

    catalog_path = args.input_catalog.expanduser().resolve()
    output_path = args.output.expanduser().resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    catalog_rows = read_catalog(catalog_path)
    lineage_rows = build_lineage_rows(catalog_rows)
    write_lineage(output_path, lineage_rows)

    print(f"Wrote: {output_path}")
    print(f"Columns audited: {len(lineage_rows)}")


if __name__ == "__main__":
    main()