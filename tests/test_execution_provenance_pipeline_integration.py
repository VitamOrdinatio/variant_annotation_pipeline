\
from __future__ import annotations

import logging
from copy import deepcopy
from pathlib import Path

import pytest

from src import pipeline_runner


def _logger() -> logging.Logger:
    logger = logging.getLogger("execution_provenance_pipeline_test")
    logger.handlers.clear()
    logger.addHandler(logging.NullHandler())
    return logger


def test_legacy_config_remains_explicitly_partial(tmp_path) -> None:
    config = {
        "mode": {"execution_mode": "full_pipeline"},
    }
    state = {
        "execution_provenance": {
            "contract_status": "not_resolved",
        }
    }

    result = pipeline_runner.resolve_execution_provenance_if_required(
        config=config,
        state=state,
        run_paths={"metadata_dir": str(tmp_path / "metadata")},
        logger=_logger(),
    )

    provenance = result["execution_provenance"]
    assert provenance["contract_status"] == "not_declared"
    assert provenance["resolution_mode"] == "legacy_unmigrated_config"
    assert provenance["provenance_completeness"] == "legacy_partial"
    assert Path(provenance["receipt_path"]).is_file()


def test_declared_provenance_is_resolved_and_gated(
    tmp_path,
    monkeypatch,
) -> None:
    config = {
        "mode": {"execution_mode": "full_pipeline"},
        "execution_provenance": {"required": True},
    }
    expected = {
        "contract_status": "pass",
        "resolution_mode": "live_runtime_resolution",
        "provenance_completeness": "complete",
    }

    monkeypatch.setattr(
        pipeline_runner,
        "resolve_execution_provenance",
        lambda config: deepcopy(expected),
    )

    state = {
        "execution_provenance": {
            "contract_status": "not_resolved",
        }
    }
    result = pipeline_runner.resolve_execution_provenance_if_required(
        config=config,
        state=state,
        run_paths={"metadata_dir": str(tmp_path / "metadata")},
        logger=_logger(),
    )

    provenance = result["execution_provenance"]
    for key, value in expected.items():
        assert provenance[key] == value
    assert Path(provenance["receipt_path"]).is_file()


def test_failed_declared_provenance_blocks_pipeline(
    tmp_path,
    monkeypatch,
) -> None:
    config = {
        "mode": {"execution_mode": "full_pipeline"},
        "execution_provenance": {"required": True},
    }

    monkeypatch.setattr(
        pipeline_runner,
        "resolve_execution_provenance",
        lambda config: {
            "contract_status": "fail",
            "resolution_mode": "live_runtime_resolution",
            "failed_surfaces": ["toolchain_environment"],
            "toolchain_environment": {
                "failed_tools": [],
                "tools": {},
            },
            "annotation_environment": {"failures": []},
        },
    )

    with pytest.raises(
        Exception,
        match="Execution provenance contract failed",
    ):
        pipeline_runner.resolve_execution_provenance_if_required(
            config=config,
            state={},
            run_paths={"metadata_dir": str(tmp_path / "metadata")},
            logger=_logger(),
        )


def test_post_vep_fixture_does_not_gate_not_applicable(
    tmp_path,
    monkeypatch,
) -> None:
    config = {
        "mode": {"execution_mode": "post_vep_fixture"},
    }
    expected = {
        "contract_status": "not_applicable",
        "resolution_mode": "retained_source_provenance",
        "provenance_completeness": "legacy_partial",
    }

    monkeypatch.setattr(
        pipeline_runner,
        "resolve_execution_provenance",
        lambda config: deepcopy(expected),
    )

    state = {}
    result = pipeline_runner.resolve_execution_provenance_if_required(
        config=config,
        state=state,
        run_paths={"metadata_dir": str(tmp_path / "metadata")},
        logger=_logger(),
    )
    provenance = result["execution_provenance"]
    for key, value in expected.items():
        assert provenance[key] == value
    assert Path(provenance["receipt_path"]).is_file()
