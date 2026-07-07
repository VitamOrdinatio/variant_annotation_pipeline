#!/usr/bin/env python3
"""
Add config_snapshot.yaml metadata to the 13 existing VAP-TEP packages on MARK.

Run from the VAP repository root:

    python scripts/mark/harden_13_vap_teps_with_config_snapshot.py

This is an additive metadata hardening script. It does not modify evidence TSVs,
regenerate VAP outputs, or rebuild source evidence artifacts.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import shutil
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class TepRun:
    sample_id: str
    run_id: str
    depth_category: str


RUNS = [
    TepRun("ERR10619203", "run_2026_05_30_071639", "q3"),
    TepRun("ERR10619207", "run_2026_06_01_124134", "q3"),
    TepRun("ERR10619208", "run_2026_05_30_151355", "median"),
    TepRun("ERR10619212", "run_2026_05_30_214724", "q1"),
    TepRun("ERR10619225", "run_2026_05_31_091242", "q3"),
    TepRun("ERR10619230", "run_2026_06_01_004903", "q3"),
    TepRun("ERR10619241", "run_2026_06_02_052302", "q1"),
    TepRun("ERR10619281", "run_2026_05_27_233524", "median"),
    TepRun("ERR10619285", "run_2026_06_02_124300", "median"),
    TepRun("ERR10619300", "run_2026_05_27_172531", "median"),
    TepRun("ERR10619309", "run_2026_06_02_181024", "q1"),
    TepRun("ERR10619330", "run_2026_06_01_203130", "q1"),
    TepRun("HG002", "run_2026_06_03_010030", "hg002"),
]


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def local_timestamp() -> str:
    return datetime.now().strftime("%Y_%m_%d_%H%M%S")


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while True:
            chunk = handle.read(chunk_size)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise ValueError(f"Expected JSON object: {path}")
    return payload


def write_json(path: Path, payload: dict[str, Any]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
        handle.write("\n")


def tep_id(run: TepRun) -> str:
    return f"vap_tep_{run.sample_id}_{run.run_id}_v1"


def run_dir(run: TepRun) -> Path:
    return Path("results") / run.run_id


def tep_dir(run: TepRun) -> Path:
    return run_dir(run) / "tep" / tep_id(run)


def config_source(run: TepRun) -> Path:
    return run_dir(run) / "metadata" / "config_snapshot.yaml"


def config_destination(run: TepRun) -> Path:
    return tep_dir(run) / "entities" / "metadata" / "config_snapshot.yaml"


def inventory_path(run: TepRun) -> Path:
    return tep_dir(run) / "entity_inventory.json"


def manifest_path(run: TepRun) -> Path:
    return tep_dir(run) / "lineage_manifest.json"


def validation_report_path(run: TepRun) -> Path:
    return tep_dir(run) / "validation_report.md"


def build_artifact_record(run: TepRun, source: Path, destination: Path) -> dict[str, Any]:
    return {
        "entity_id": "package_metadata",
        "entity_role": "package_metadata",
        "source_stage": "run_metadata",
        "source_artifact_role": "config_snapshot",
        "source_artifact": str(source),
        "transport_path": str(destination.relative_to(tep_dir(run))),
        "source_artifact_exists": True,
        "copied": True,
        "required": True,
        "size_bytes": source.stat().st_size,
        "row_count": None,
        "column_count": None,
        "variant_id_count": None,
        "observed_columns": None,
        "sha256": sha256_file(source),
    }


def build_entity_record(artifact_record: dict[str, Any]) -> dict[str, Any]:
    return {
        "entity_id": "package_metadata",
        "entity_role": "package_metadata",
        "source_stage": "run_metadata",
        "required": True,
        "artifact_count": 1,
        "copied_artifacts": 1,
        "missing_required_artifacts": 0,
        "metric_semantics": "package_metadata_metrics",
        "total_size_bytes": artifact_record["size_bytes"],
        "row_count": None,
        "column_count": None,
        "variant_id_count": None,
        "artifacts": [artifact_record],
        "artifact_metrics": {
            "config_snapshot": {
                "row_count": None,
                "column_count": None,
                "variant_id_count": None,
                "size_bytes": artifact_record["size_bytes"],
                "observed_columns": None,
            }
        },
    }


def update_inventory(run: TepRun, source: Path, destination: Path) -> None:
    path = inventory_path(run)
    inventory = load_json(path)
    artifact_record = build_artifact_record(run, source, destination)
    entity_record = build_entity_record(artifact_record)

    inventory["entities"] = [
        entity for entity in inventory.get("entities", [])
        if entity.get("entity_id") != "package_metadata"
    ]
    inventory["entities"].append(entity_record)
    inventory["artifacts"] = [
        artifact for artifact in inventory.get("artifacts", [])
        if artifact.get("source_artifact_role") != "config_snapshot"
    ]
    inventory["artifacts"].append(artifact_record)
    inventory["metadata_hardened_utc"] = utc_now()
    inventory.setdefault("source_run", {})
    inventory["source_run"]["metadata_directory"] = str(run_dir(run) / "metadata")
    inventory.setdefault("summary", {})
    inventory["summary"]["entity_records"] = len(inventory["entities"])
    inventory["summary"]["artifact_records"] = len(inventory["artifacts"])
    inventory["summary"]["missing_required_artifacts"] = sum(
        1 for artifact in inventory["artifacts"]
        if artifact.get("required") is True and artifact.get("source_artifact_exists") is not True
    )
    inventory["summary"]["copied_artifacts"] = sum(
        1 for artifact in inventory["artifacts"]
        if artifact.get("copied") is True
    )
    write_json(path, inventory)


def run_command(command: list[str], log_path: Path, dry_run: bool) -> int:
    with log_path.open("a", encoding="utf-8") as log:
        log.write("\n$ " + " ".join(command) + "\n")
    if dry_run:
        return 0
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, check=False)
    with log_path.open("a", encoding="utf-8") as log:
        log.write(result.stdout)
        if not result.stdout.endswith("\n"):
            log.write("\n")
        log.write(f"[exit_code] {result.returncode}\n")
    return result.returncode


def harden_run(run: TepRun, out_dir: Path, python_executable: str, dry_run: bool) -> dict[str, Any]:
    log_path = out_dir / f"{run.sample_id}_{run.run_id}.log"
    source = config_source(run)
    destination = config_destination(run)
    row: dict[str, Any] = {
        "sample_id": run.sample_id,
        "run_id": run.run_id,
        "depth_category": run.depth_category,
        "tep_id": tep_id(run),
        "source": str(source),
        "destination": str(destination),
        "status": "PENDING",
        "source_exists": source.exists(),
        "destination_exists": False,
        "source_sha256": "",
        "destination_sha256": "",
        "sha256_match": False,
        "inventory_exists": inventory_path(run).exists(),
        "manifest_exists": manifest_path(run).exists(),
        "validation_report_exists": validation_report_path(run).exists(),
        "error": "",
    }
    try:
        with log_path.open("w", encoding="utf-8") as log:
            log.write("# VAP-TEP config metadata hardening log\n")
            for key, value in row.items():
                log.write(f"{key}: {value}\n")
        missing = [str(path) for path in [source, tep_dir(run), inventory_path(run)] if not path.exists()]
        if missing:
            raise FileNotFoundError(f"Missing required paths: {missing}")
        if not dry_run:
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)
            update_inventory(run, source, destination)
        lineage_cmd = [python_executable, "scripts/tep/build_vap_tep_lineage_manifest.py", "--inventory", str(inventory_path(run)), "--overwrite"]
        code = run_command(lineage_cmd, log_path, dry_run=dry_run)
        if code != 0:
            raise RuntimeError(f"Lineage manifest rebuild failed with exit code {code}")
        validate_cmd = [python_executable, "scripts/tep/validate_vap_tep.py", "--manifest", str(manifest_path(run)), "--write-updated-manifest", "--report", str(validation_report_path(run))]
        code = run_command(validate_cmd, log_path, dry_run=dry_run)
        if code != 0:
            raise RuntimeError(f"Validation failed with exit code {code}")
        row["destination_exists"] = destination.exists()
        if source.exists():
            row["source_sha256"] = sha256_file(source)
        if destination.exists():
            row["destination_sha256"] = sha256_file(destination)
        row["sha256_match"] = bool(row["source_sha256"]) and row["source_sha256"] == row["destination_sha256"]
        row["inventory_exists"] = inventory_path(run).exists()
        row["manifest_exists"] = manifest_path(run).exists()
        row["validation_report_exists"] = validation_report_path(run).exists()
        row["status"] = "DRY_RUN" if dry_run else "PASS"
    except Exception as exc:  # noqa: BLE001
        row["status"] = "FAIL"
        row["error"] = repr(exc)
    return row


def write_summary(out_dir: Path, rows: list[dict[str, Any]]) -> None:
    path = out_dir / "config_metadata_hardening_summary.tsv"
    fields = ["sample_id", "run_id", "depth_category", "tep_id", "source", "destination", "status", "source_exists", "destination_exists", "source_sha256", "destination_sha256", "sha256_match", "inventory_exists", "manifest_exists", "validation_report_exists", "error"]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def main() -> int:
    parser = argparse.ArgumentParser(description="Add config_snapshot.yaml metadata to existing 13 VAP-TEP packages.")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--continue-on-error", action="store_true")
    parser.add_argument("--python", default=sys.executable)
    args = parser.parse_args()
    if not Path("results").exists():
        raise FileNotFoundError("Run from VAP repository root; results/ not found.")
    out_dir = Path("/root/Desktop") / f"vap_tep_config_metadata_hardening_{local_timestamp()}"
    out_dir.mkdir(parents=True, exist_ok=False)
    rows: list[dict[str, Any]] = []
    print(f"[INFO] Output directory: {out_dir}")
    print(f"[INFO] dry_run: {args.dry_run}")
    for idx, run in enumerate(RUNS, start=1):
        print(f"[INFO] [{idx}/{len(RUNS)}] Hardening {run.sample_id} / {run.run_id}")
        row = harden_run(run, out_dir, args.python, args.dry_run)
        rows.append(row)
        write_summary(out_dir, rows)
        print(f"[INFO] status: {row['status']}")
        if row["status"] == "FAIL":
            print(f"[ERROR] {row['error']}")
            if not args.continue_on_error:
                print("[ERROR] Stopping because --continue-on-error was not supplied.")
                return 1
    failures = [row for row in rows if row["status"] == "FAIL"]
    print("\nVAP-TEP config metadata hardening complete.")
    print(f"Output directory: {out_dir}")
    print(f"PASS: {sum(1 for row in rows if row['status'] == 'PASS')}")
    print(f"DRY_RUN: {sum(1 for row in rows if row['status'] == 'DRY_RUN')}")
    print(f"FAIL: {len(failures)}")
    print(f"Summary: {out_dir / 'config_metadata_hardening_summary.tsv'}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
