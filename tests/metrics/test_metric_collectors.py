from __future__ import annotations

import csv
from pathlib import Path

import pytest

from src.metrics.metric_collectors import (
    CSV_FIELD_SIZE_LIMIT,
    configure_csv_field_size_limit,
    count_tsv_rows,
)


def test_metric_csv_limit_exceeds_python_default() -> None:
    configured_limit = configure_csv_field_size_limit()

    assert configured_limit == CSV_FIELD_SIZE_LIMIT
    assert configured_limit > 131_072
    assert csv.field_size_limit() == CSV_FIELD_SIZE_LIMIT


@pytest.mark.parametrize(
    ("filename", "header", "row_prefix"),
    [
        (
            "stage_08_rdgp_gene_evidence_seed.tsv",
            "gene_id\tcontributing_variant_ids\n",
            "GENE1\t",
        ),
        (
            "stage_08_vdb_ready_variants.tsv",
            "variant_id\tmane_canonical_context\n",
            "variant_001\t",
        ),
    ],
)
def test_count_tsv_rows_accepts_large_stage08_preservation_fields(
    tmp_path: Path,
    filename: str,
    header: str,
    row_prefix: str,
) -> None:
    large_value = "variant_001;" * 13_000

    assert len(large_value) > 131_072
    assert len(large_value) < CSV_FIELD_SIZE_LIMIT

    path = tmp_path / filename
    path.write_text(
        header + row_prefix + large_value + "\n",
        encoding="utf-8",
    )

    assert count_tsv_rows(path) == 1


def test_metric_csv_limit_remains_bounded(
    tmp_path: Path,
) -> None:
    oversized_value = "X" * (CSV_FIELD_SIZE_LIMIT + 1)

    path = tmp_path / "pathologically_large.tsv"
    path.write_text(
        "record_id\tvalue\n"
        f"record_001\t{oversized_value}\n",
        encoding="utf-8",
    )

    with pytest.raises(csv.Error, match="field larger than field limit"):
        count_tsv_rows(path)