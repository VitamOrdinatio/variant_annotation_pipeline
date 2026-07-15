\
#!/usr/bin/env python3
"""
Run the non-destructive sys76 ERR10619300 production preflight.

This command validates the configuration, resolves the complete execution
provenance contract, writes receipts, and prints a tmux launch command only
when every required tool and scientific resource passes.
"""

from __future__ import annotations

import argparse
import json
import os
import shlex
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]

if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))


from src.config_loader import load_config, validate_config
from src.execution_provenance import (
    ExecutionProvenanceError,
    assert_contract_pass,
    resolve_execution_provenance,
    write_execution_provenance_receipt,
)


DEFAULT_CONFIG = (
    "config/execution_provenance/"
    "config.sys76.err10619300.execution_provenance.yaml"
)

DEFAULT_RECEIPT_DIR = "/mnt/storage/vap_tmp/ERR10619300/preflight"


def _utc_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y_%m_%d_%H%M%S")


def _check_fastq(path: str) -> dict[str, object]:
    file_path = Path(path)
    return {
        "path": str(file_path),
        "exists": file_path.is_file(),
        "size_bytes": file_path.stat().st_size if file_path.is_file() else None,
    }


def _storage_snapshot(path: str) -> dict[str, object]:
    usage = shutil.disk_usage(path)
    return {
        "path": path,
        "total_bytes": usage.total,
        "used_bytes": usage.used,
        "free_bytes": usage.free,
    }


def _launch_command(config_path: str) -> str:
    repo = Path.cwd()
    session = "vap_err10619300_sys76"
    command = (
        f"cd {shlex.quote(str(repo))} && "
        "source .venv/bin/activate && "
        "export TMPDIR=/mnt/storage/vap_tmp/ERR10619300 && "
        "export TMP=/mnt/storage/vap_tmp/ERR10619300 && "
        "export TEMP=/mnt/storage/vap_tmp/ERR10619300 && "
        f"python run_pipeline.py --config {shlex.quote(config_path)}"
    )
    return (
        f"tmux new-session -d -s {shlex.quote(session)} "
        f"{shlex.quote(command)}"
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default=DEFAULT_CONFIG)
    parser.add_argument("--receipt-dir", default=DEFAULT_RECEIPT_DIR)
    args = parser.parse_args()

    config = load_config(args.config)
    validate_config(config)

    receipt_dir = Path(args.receipt_dir)
    receipt_dir.mkdir(parents=True, exist_ok=True)
    stamp = _utc_stamp()

    fastqs = {
        "r1": _check_fastq(config["input"]["fastq"]["r1"]),
        "r2": _check_fastq(config["input"]["fastq"]["r2"]),
    }
    fastq_ok = all(item["exists"] for item in fastqs.values())

    results_root = (
        Path(config["output"]["base_results_dir"])
        .expanduser()
        .resolve()
    )

    results_root.mkdir(
        parents=True,
        exist_ok=True,
    )

    storage = {
        "results": _storage_snapshot(str(results_root)),
        "temporary": _storage_snapshot(
            "/mnt/storage/vap_tmp/ERR10619300"
        ),
    }

    preflight = {
        "config_path": args.config,
        "fastqs": fastqs,
        "storage": storage,
        "execution_provenance": None,
        "overall_status": "FAIL",
        "launch_command": None,
    }

    try:
        provenance = resolve_execution_provenance(config)
        assert_contract_pass(provenance)
        preflight["execution_provenance"] = provenance
        if not fastq_ok:
            raise ExecutionProvenanceError(
                "One or more ERR10619300 FASTQ inputs are missing"
            )

        preflight["overall_status"] = "PASS"
        preflight["launch_command"] = _launch_command(args.config)
    except Exception as exc:
        preflight["failure"] = {
            "type": type(exc).__name__,
            "message": str(exc),
        }

    json_path = receipt_dir / f"sys76_preflight_{stamp}.json"
    json_path.write_text(
        json.dumps(preflight, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    if preflight["execution_provenance"] is not None:
        write_execution_provenance_receipt(
            provenance=preflight["execution_provenance"],
            output_path=(
                receipt_dir
                / f"resolved_execution_provenance_{stamp}.json"
            ),
        )

    print(f"overall_status: {preflight['overall_status']}")
    print(f"receipt: {json_path}")
    if preflight["overall_status"] == "PASS":
        print()
        print("tmux launch command:")
        print(preflight["launch_command"])
        return 0

    print()
    print("preflight failure:")
    print(preflight["failure"]["message"])
    return 1


if __name__ == "__main__":
    sys.exit(main())
