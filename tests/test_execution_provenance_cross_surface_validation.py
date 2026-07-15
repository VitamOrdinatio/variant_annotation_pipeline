\
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from scripts.validation.validate_execution_provenance import (
    validate_execution_provenance_surfaces,
)


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _fixture(tmp_path: Path) -> tuple[Path, Path]:
    run_dir = tmp_path / "run"
    receipt = run_dir / "metadata" / "execution_provenance.json"
    payload = {
        "schema_version": "1.0.0",
        "contract_status": "pass",
        "resolution_mode": "live_runtime_resolution",
        "provenance_completeness": "complete",
    }
    _write_json(receipt, payload)
    _write_json(
        run_dir / "metadata" / "run_metadata.json",
        {
            "execution_provenance": {
                "contract_status": "pass",
                "resolution_mode": "live_runtime_resolution",
                "provenance_completeness": "complete",
                "receipt_path": str(receipt),
            }
        },
    )

    tep_root = tmp_path / "tep"
    transported = (
        tep_root
        / "entities"
        / "context"
        / "execution_provenance.json"
    )
    _write_json(transported, payload)
    digest = hashlib.sha256(transported.read_bytes()).hexdigest()
    _write_json(
        tep_root / "entity_inventory.json",
        {
            "entities": [
                {
                    "entity_role": "context_sidecar",
                    "source_artifacts": [
                        {
                            "source_artifact_role": "execution_provenance",
                            "transport_path": (
                                "entities/context/"
                                "execution_provenance.json"
                            ),
                            "source_artifact_sha256": digest,
                        }
                    ],
                }
            ]
        },
    )
    return run_dir, tep_root


def test_cross_surface_validation_passes(tmp_path: Path) -> None:
    run_dir, tep_root = _fixture(tmp_path)

    checks = validate_execution_provenance_surfaces(
        run_dir=run_dir,
        tep_root=tep_root,
    )

    assert checks
    assert all(check.status == "PASS" for check in checks)


def test_missing_run_receipt_fails(tmp_path: Path) -> None:
    checks = validate_execution_provenance_surfaces(
        run_dir=tmp_path / "missing",
    )

    assert checks[0].check_id == "EPV-001"
    assert checks[0].status == "FAIL"


def test_run_metadata_mismatch_fails(tmp_path: Path) -> None:
    run_dir, _ = _fixture(tmp_path)
    metadata = run_dir / "metadata" / "run_metadata.json"
    payload = json.loads(metadata.read_text(encoding="utf-8"))
    payload["execution_provenance"]["contract_status"] = "fail"
    _write_json(metadata, payload)

    checks = validate_execution_provenance_surfaces(run_dir=run_dir)

    target = next(check for check in checks if check.check_id == "EPV-003")
    assert target.status == "FAIL"


def test_tep_checksum_drift_fails(tmp_path: Path) -> None:
    run_dir, tep_root = _fixture(tmp_path)
    transported = (
        tep_root
        / "entities"
        / "context"
        / "execution_provenance.json"
    )
    transported.write_text(
        transported.read_text(encoding="utf-8") + "\n",
        encoding="utf-8",
    )

    checks = validate_execution_provenance_surfaces(
        run_dir=run_dir,
        tep_root=tep_root,
    )

    target = next(check for check in checks if check.check_id == "EPV-006")
    assert target.status == "FAIL"


def test_inventory_checksum_mismatch_fails(tmp_path: Path) -> None:
    run_dir, tep_root = _fixture(tmp_path)
    inventory = tep_root / "entity_inventory.json"
    payload = json.loads(inventory.read_text(encoding="utf-8"))
    payload["entities"][0]["source_artifacts"][0][
        "source_artifact_sha256"
    ] = "0" * 64
    _write_json(inventory, payload)

    checks = validate_execution_provenance_surfaces(
        run_dir=run_dir,
        tep_root=tep_root,
    )

    target = next(check for check in checks if check.check_id == "EPV-007")
    assert target.status == "FAIL"
