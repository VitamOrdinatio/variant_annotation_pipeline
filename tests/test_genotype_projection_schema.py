from __future__ import annotations

import csv
from pathlib import Path

from pipeline.genotype_projection import GENOTYPE_COLUMNS
from tests.test_genotype_projection import project


def test_schema_column_order(tmp_path: Path) -> None:
    output, _ = project(tmp_path)
    with (output / "genotype_observations.tsv").open("r", encoding="utf-8", newline="") as handle:
        header = next(csv.reader(handle, delimiter="\t"))
    assert header == GENOTYPE_COLUMNS


def test_observation_ids_are_deterministic(tmp_path: Path) -> None:
    first, _ = project(tmp_path / "first")
    second, _ = project(tmp_path / "second")
    def ids(path: Path) -> list[str]:
        with path.open("r", encoding="utf-8", newline="") as handle:
            return [row["genotype_observation_id"] for row in csv.DictReader(handle, delimiter="\t")]
    assert ids(first / "genotype_observations.tsv") == ids(second / "genotype_observations.tsv")
