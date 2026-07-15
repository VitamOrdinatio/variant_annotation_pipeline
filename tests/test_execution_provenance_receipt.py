\
from __future__ import annotations

import json
import logging
from pathlib import Path

from src import pipeline_runner
from src.execution_provenance import (
    write_execution_provenance_receipt,
)


def _logger() -> logging.Logger:
    logger = logging.getLogger("execution_provenance_receipt_test")
    logger.handlers.clear()
    logger.addHandler(logging.NullHandler())
    return logger


def test_receipt_writer_is_stable_and_sorted(tmp_path: Path) -> None:
    path = tmp_path / "execution_provenance.json"
    provenance = {
        "z": 1,
        "a": {
            "contract_status": "pass",
        },
    }

    write_execution_provenance_receipt(
        provenance=provenance,
        output_path=path,
    )
    first = path.read_bytes()

    write_execution_provenance_receipt(
        provenance=provenance,
        output_path=path,
    )
    second = path.read_bytes()

    assert first == second
    assert json.loads(first) == provenance
    assert first.endswith(b"\n")
    assert first.index(b'"a"') < first.index(b'"z"')


def test_live_provenance_receipt_is_registered(
    tmp_path: Path,
    monkeypatch,
) -> None:
    expected = {
        "schema_version": "1.0.0",
        "contract_status": "pass",
        "resolution_mode": "live_runtime_resolution",
        "provenance_completeness": "complete",
    }
    monkeypatch.setattr(
        pipeline_runner,
        "resolve_execution_provenance",
        lambda config: dict(expected),
    )

    state = {}
    result = pipeline_runner.resolve_execution_provenance_if_required(
        config={
            "mode": {"execution_mode": "full_pipeline"},
            "execution_provenance": {"required": True},
        },
        state=state,
        run_paths={"metadata_dir": str(tmp_path / "metadata")},
        logger=_logger(),
    )

    receipt = Path(
        result["execution_provenance"]["receipt_path"]
    )
    assert receipt == (
        tmp_path / "metadata" / "execution_provenance.json"
    )
    assert receipt.is_file()

    stored = json.loads(receipt.read_text(encoding="utf-8"))
    assert stored == expected
    assert "receipt_path" not in stored


def test_legacy_partial_provenance_receipt_is_emitted(
    tmp_path: Path,
) -> None:
    state = {}
    result = pipeline_runner.resolve_execution_provenance_if_required(
        config={"mode": {"execution_mode": "full_pipeline"}},
        state=state,
        run_paths={"metadata_dir": str(tmp_path / "metadata")},
        logger=_logger(),
    )

    receipt = Path(
        result["execution_provenance"]["receipt_path"]
    )
    stored = json.loads(receipt.read_text(encoding="utf-8"))

    assert stored["contract_status"] == "not_declared"
    assert stored["resolution_mode"] == "legacy_unmigrated_config"
    assert stored["provenance_completeness"] == "legacy_partial"


def test_post_vep_receipt_preserves_not_applicable_state(
    tmp_path: Path,
    monkeypatch,
) -> None:
    expected = {
        "schema_version": "1.0.0",
        "contract_status": "not_applicable",
        "resolution_mode": "retained_source_provenance",
        "provenance_completeness": "legacy_partial",
    }
    monkeypatch.setattr(
        pipeline_runner,
        "resolve_execution_provenance",
        lambda config: dict(expected),
    )

    result = pipeline_runner.resolve_execution_provenance_if_required(
        config={"mode": {"execution_mode": "post_vep_fixture"}},
        state={},
        run_paths={"metadata_dir": str(tmp_path / "metadata")},
        logger=_logger(),
    )

    receipt = Path(
        result["execution_provenance"]["receipt_path"]
    )
    stored = json.loads(receipt.read_text(encoding="utf-8"))
    assert stored == expected
