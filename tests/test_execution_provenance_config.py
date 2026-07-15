\
from __future__ import annotations

from copy import deepcopy

import pytest

from src.config_loader import load_config, validate_config


CONFIG_PATH = "config/execution_provenance/config.mark.err10619300.execution_provenance.yaml"


def _production_config() -> dict:
    return deepcopy(load_config(CONFIG_PATH))


def test_execution_provenance_production_config_validates() -> None:
    validate_config(_production_config())


def test_legacy_config_without_execution_provenance_remains_valid() -> None:
    config = _production_config()
    config.pop("execution_provenance")

    validate_config(config)


def test_execution_provenance_requires_complete_toolchain() -> None:
    config = _production_config()
    del config["execution_provenance"]["toolchain"]["samtools"]

    with pytest.raises(
        ValueError,
        match="toolchain must contain exactly",
    ):
        validate_config(config)


def test_vep_software_declarations_must_agree() -> None:
    config = _production_config()
    config["execution_provenance"]["annotation_environment"][
        "software_version"
    ] = "116.0"

    with pytest.raises(
        ValueError,
        match="VEP software version declarations disagree",
    ):
        validate_config(config)


def test_annotation_assembly_must_match_reference_build() -> None:
    config = _production_config()
    config["execution_provenance"]["annotation_environment"][
        "cache_assembly"
    ] = "GRCh37"

    with pytest.raises(
        ValueError,
        match="cache_assembly must be 'GRCh38'",
    ):
        validate_config(config)


def test_bwa_index_requires_constituent_checksum_policy() -> None:
    config = _production_config()
    config["execution_provenance"]["resource_environment"][
        "bwa_index"
    ]["checksum_policy"] = "sha256"

    with pytest.raises(
        ValueError,
        match="sha256_constituents",
    ):
        validate_config(config)
