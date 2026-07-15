\
from __future__ import annotations

from pathlib import Path

import pytest

from src.execution_provenance import (
    ExecutionProvenanceError,
    discover_vep_cache,
    parse_vep_cache_directory_name,
    require_annotation_environment,
)


def test_parse_vep_cache_directory_name() -> None:
    assert parse_vep_cache_directory_name(
        "115_GRCh38"
    ) == ("115", "GRCh38")

    with pytest.raises(
        ExecutionProvenanceError,
        match="Unparseable VEP cache directory name",
    ):
        parse_vep_cache_directory_name("current")


def test_nested_vep_cache_identity(tmp_path: Path) -> None:
    cache = tmp_path / "homo_sapiens" / "115_GRCh38"
    cache.mkdir(parents=True)

    result = discover_vep_cache(
        cache_dir=tmp_path,
        species="homo_sapiens",
        release="115",
        assembly="GRCh38",
    )

    assert result["observed_cache_release"] == "115"
    assert result["observed_assembly"] == "GRCh38"
    assert result["observed_species"] == "homo_sapiens"
    assert result["cache_identity_status"] == "pass"


def test_flat_vep_cache_identity(tmp_path: Path) -> None:
    cache = tmp_path / "115_GRCh38"
    cache.mkdir()

    result = discover_vep_cache(
        cache_dir=tmp_path,
        species="homo_sapiens",
        release="115",
        assembly="GRCh38",
    )

    assert result["resolved_cache_directory"] == str(cache.resolve())
    assert result["observed_cache_release"] == "115"


def test_ambiguous_cache_layout_fails(tmp_path: Path) -> None:
    first = tmp_path / "homo_sapiens" / "115_GRCh38"
    second = tmp_path / "archive" / "homo_sapiens" / "115_GRCh38"
    first.mkdir(parents=True)
    second.mkdir(parents=True)

    with pytest.raises(
        ExecutionProvenanceError,
        match="Multiple matching VEP cache directories found",
    ):
        discover_vep_cache(
            cache_dir=tmp_path,
            species="homo_sapiens",
            release="115",
            assembly="GRCh38",
        )


def test_missing_declared_cache_fails(tmp_path: Path) -> None:
    (tmp_path / "homo_sapiens" / "116_GRCh38").mkdir(
        parents=True
    )

    with pytest.raises(
        ExecutionProvenanceError,
        match="Expected VEP cache not found",
    ):
        discover_vep_cache(
            cache_dir=tmp_path,
            species="homo_sapiens",
            release="115",
            assembly="GRCh38",
        )


def test_require_annotation_environment() -> None:
    annotation = {
        "contract_status": "pass",
        "software": {
            "observed_version": "115.2",
        },
    }
    state = {
        "execution_provenance": {
            "annotation_environment": annotation,
        }
    }

    assert require_annotation_environment(state) is annotation


def test_require_annotation_environment_rejects_missing_state() -> None:
    with pytest.raises(
        ExecutionProvenanceError,
        match="execution_provenance is missing",
    ):
        require_annotation_environment({})


def test_require_annotation_environment_rejects_failed_contract() -> None:
    state = {
        "execution_provenance": {
            "annotation_environment": {
                "contract_status": "fail",
            }
        }
    }

    with pytest.raises(
        ExecutionProvenanceError,
        match="contract has not passed",
    ):
        require_annotation_environment(state)
