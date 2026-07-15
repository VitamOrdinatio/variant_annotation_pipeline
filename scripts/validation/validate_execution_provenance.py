\
#!/usr/bin/env python3
"""
Validate VAP execution-provenance consistency across run and TEP surfaces.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class Check:
    check_id: str
    status: str
    message: str
    details: str = ""


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"Expected JSON object: {path}")
    return value


def _pass(check_id: str, message: str, details: str = "") -> Check:
    return Check(check_id, "PASS", message, details)


def _fail(check_id: str, message: str, details: str = "") -> Check:
    return Check(check_id, "FAIL", message, details)


def validate_execution_provenance_surfaces(
    *,
    run_dir: str | Path,
    tep_root: str | Path | None = None,
) -> list[Check]:
    run_path = Path(run_dir)
    metadata_dir = run_path / "metadata"
    receipt_path = metadata_dir / "execution_provenance.json"
    run_metadata_path = metadata_dir / "run_metadata.json"

    checks: list[Check] = []

    if not receipt_path.is_file():
        return [
            _fail(
                "EPV-001",
                "Run execution provenance receipt exists",
                str(receipt_path),
            )
        ]

    checks.append(
        _pass(
            "EPV-001",
            "Run execution provenance receipt exists",
            str(receipt_path),
        )
    )

    try:
        receipt = _load_json(receipt_path)
    except Exception as exc:
        return checks + [
            _fail(
                "EPV-002",
                "Run execution provenance receipt is readable JSON",
                str(exc),
            )
        ]

    required_receipt_fields = {
        "contract_status",
        "resolution_mode",
        "provenance_completeness",
    }
    missing = sorted(required_receipt_fields - set(receipt))
    if missing:
        checks.append(
            _fail(
                "EPV-002",
                "Run execution provenance receipt has required fields",
                f"missing={missing}",
            )
        )
    else:
        checks.append(
            _pass(
                "EPV-002",
                "Run execution provenance receipt has required fields",
                (
                    f"status={receipt['contract_status']}; "
                    f"mode={receipt['resolution_mode']}; "
                    f"completeness={receipt['provenance_completeness']}"
                ),
            )
        )

    if not run_metadata_path.is_file():
        checks.append(
            _fail(
                "EPV-003",
                "Run metadata exists",
                str(run_metadata_path),
            )
        )
    else:
        run_metadata = _load_json(run_metadata_path)
        summary = run_metadata.get("execution_provenance")
        if not isinstance(summary, dict):
            checks.append(
                _fail(
                    "EPV-003",
                    "Run metadata summarizes execution provenance",
                    "execution_provenance section missing",
                )
            )
        else:
            compared = {
                key: (
                    receipt.get(key),
                    summary.get(key),
                )
                for key in (
                    "contract_status",
                    "resolution_mode",
                    "provenance_completeness",
                )
            }
            mismatches = {
                key: values
                for key, values in compared.items()
                if values[0] != values[1]
            }
            if mismatches:
                checks.append(
                    _fail(
                        "EPV-003",
                        "Run metadata matches the provenance receipt",
                        str(mismatches),
                    )
                )
            else:
                checks.append(
                    _pass(
                        "EPV-003",
                        "Run metadata matches the provenance receipt",
                    )
                )

            registered = summary.get("receipt_path")
            if registered is None:
                checks.append(
                    _fail(
                        "EPV-004",
                        "Run metadata registers the provenance receipt",
                        "receipt_path is null",
                    )
                )
            else:
                registered_path = Path(registered)
                if not registered_path.is_absolute():
                    registered_path = run_path / registered_path
                if registered_path.resolve() == receipt_path.resolve():
                    checks.append(
                        _pass(
                            "EPV-004",
                            "Run metadata registers the provenance receipt",
                            str(registered_path),
                        )
                    )
                else:
                    checks.append(
                        _fail(
                            "EPV-004",
                            "Run metadata registers the provenance receipt",
                            (
                                f"registered={registered_path}; "
                                f"expected={receipt_path}"
                            ),
                        )
                    )

    if tep_root is None:
        return checks

    tep_path = Path(tep_root)
    transported = (
        tep_path
        / "entities"
        / "context"
        / "execution_provenance.json"
    )
    if not transported.is_file():
        checks.append(
            _fail(
                "EPV-005",
                "TEP transports execution provenance",
                str(transported),
            )
        )
        return checks

    checks.append(
        _pass(
            "EPV-005",
            "TEP transports execution provenance",
            str(transported),
        )
    )

    run_sha = _sha256(receipt_path)
    tep_sha = _sha256(transported)
    if run_sha == tep_sha:
        checks.append(
            _pass(
                "EPV-006",
                "Run and TEP provenance receipts are checksum-identical",
                run_sha,
            )
        )
    else:
        checks.append(
            _fail(
                "EPV-006",
                "Run and TEP provenance receipts are checksum-identical",
                f"run={run_sha}; tep={tep_sha}",
            )
        )

    inventory_path = tep_path / "entity_inventory.json"
    if not inventory_path.is_file():
        checks.append(
            _fail(
                "EPV-007",
                "TEP inventory registers execution provenance",
                str(inventory_path),
            )
        )
        return checks

    inventory = _load_json(inventory_path)
    matching = []
    for entity in inventory.get("entities", []):
        if entity.get("entity_role") != "context_sidecar":
            continue
        for artifact in entity.get("source_artifacts", []):
            if artifact.get("source_artifact_role") == "execution_provenance":
                matching.append(artifact)

    if len(matching) != 1:
        checks.append(
            _fail(
                "EPV-007",
                "TEP inventory registers exactly one execution provenance artifact",
                f"observed={len(matching)}",
            )
        )
    else:
        artifact = matching[0]
        checksum = artifact.get("source_artifact_sha256")
        transport_path = artifact.get("transport_path")
        expected_transport = "entities/context/execution_provenance.json"
        if checksum == tep_sha and transport_path == expected_transport:
            checks.append(
                _pass(
                    "EPV-007",
                    "TEP inventory registers execution provenance correctly",
                )
            )
        else:
            checks.append(
                _fail(
                    "EPV-007",
                    "TEP inventory registers execution provenance correctly",
                    (
                        f"checksum={checksum}; expected_checksum={tep_sha}; "
                        f"transport_path={transport_path}"
                    ),
                )
            )

    return checks


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Validate execution provenance across a VAP run and optional "
            "TEP-VAP package."
        )
    )
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--tep-root")
    parser.add_argument("--json-output")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    checks = validate_execution_provenance_surfaces(
        run_dir=args.run_dir,
        tep_root=args.tep_root,
    )

    for check in checks:
        suffix = f" | {check.details}" if check.details else ""
        print(
            f"{check.status:4}  {check.check_id}  "
            f"{check.message}{suffix}"
        )

    if args.json_output:
        output = Path(args.json_output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(
            json.dumps(
                {
                    "checks": [asdict(check) for check in checks],
                    "overall_status": (
                        "PASS"
                        if all(check.status == "PASS" for check in checks)
                        else "FAIL"
                    ),
                },
                indent=2,
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )

    return 0 if all(check.status == "PASS" for check in checks) else 1


if __name__ == "__main__":
    sys.exit(main())
