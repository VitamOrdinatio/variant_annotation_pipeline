#!/usr/bin/env python3
"""
Generate VAP-TEPs for the 12 epilepsy WES SRA runs on MARK.

Run from the VAP repository root:

    python scripts/mark/generate_12_epilepsy_wes_vap_tep.py

This is a production script, not a certification probe.

For each configured epilepsy SRA run, it executes:

    1. scripts/tep/build_vap_tep_entities.py
    2. scripts/tep/build_vap_tep_lineage_manifest.py
    3. scripts/tep/validate_vap_tep.py

By default, the script uses --overwrite for entity/package and lineage generation,
matching the already successful HG002 production recipe.

Outputs are written under each run directory:

    results/<run_id>/tep/vap_tep_<SRA>_<run_id>_v1/

A run-scoped production log is also written to:

    /root/Desktop/vap_tep_epilepsy_wes_generation_<timestamp>/

This script intentionally does not perform SAGE/DEX certification.
Certification should be performed afterward using dedicated audit probes.


Run all 12:
    python scripts/mark/generate_12_epilepsy_wes_vap_tep.py

Dry run first:
    python scripts/mark/generate_12_epilepsy_wes_vap_tep.py --dry-run

Run only one or a subset:
    python scripts/mark/generate_12_epilepsy_wes_vap_tep.py --sra ERR10619300

It writes production logs and a summary TSV to:
    /root/Desktop/vap_tep_epilepsy_wes_generation_<timestamp>/

"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Optional


@dataclass(frozen=True)
class WesRun:
    sra: str
    run_id: str
    depth_category: str


WES_RUNS: List[WesRun] = [
    WesRun("ERR10619203", "run_2026_05_30_071639", "q3"),
    WesRun("ERR10619207", "run_2026_06_01_124134", "q3"),
    WesRun("ERR10619208", "run_2026_05_30_151355", "median"),
    WesRun("ERR10619212", "run_2026_05_30_214724", "q1"),
    WesRun("ERR10619225", "run_2026_05_31_091242", "q3"),
    WesRun("ERR10619230", "run_2026_06_01_004903", "q3"),
    WesRun("ERR10619241", "run_2026_06_02_052302", "q1"),
    WesRun("ERR10619281", "run_2026_05_27_233524", "median"),
    WesRun("ERR10619285", "run_2026_06_02_124300", "median"),
    WesRun("ERR10619300", "run_2026_05_27_172531", "median"),
    WesRun("ERR10619309", "run_2026_06_02_181024", "q1"),
    WesRun("ERR10619330", "run_2026_06_01_203130", "q1"),
]


def timestamp() -> str:
    return datetime.now().strftime("%Y_%m_%d_%H%M%S")


def tep_id_for(run: WesRun) -> str:
    return f"vap_tep_{run.sra}_{run.run_id}_v1"


def run_dir_for(run: WesRun) -> Path:
    return Path("results") / run.run_id


def tep_dir_for(run: WesRun) -> Path:
    return run_dir_for(run) / "tep" / tep_id_for(run)


def inventory_path_for(run: WesRun) -> Path:
    return tep_dir_for(run) / "entity_inventory.json"


def manifest_path_for(run: WesRun) -> Path:
    return tep_dir_for(run) / "lineage_manifest.json"


def validation_report_path_for(run: WesRun) -> Path:
    return tep_dir_for(run) / "validation_report.md"


def ensure_repo_root() -> None:
    if not Path("results").exists():
        raise FileNotFoundError(
            "No results/ directory found. Run this script from the VAP repository root."
        )

    required_scripts = [
        Path("scripts/tep/build_vap_tep_entities.py"),
        Path("scripts/tep/build_vap_tep_lineage_manifest.py"),
        Path("scripts/tep/validate_vap_tep.py"),
    ]

    missing = [str(path) for path in required_scripts if not path.exists()]
    if missing:
        raise FileNotFoundError(f"Missing required TEP scripts: {missing}")


def ensure_output_dir() -> Path:
    desktop = Path("/root/Desktop")
    out_dir = desktop / f"vap_tep_epilepsy_wes_generation_{timestamp()}"
    out_dir.mkdir(parents=True, exist_ok=False)
    return out_dir


def validate_inputs(selected_runs: List[WesRun]) -> None:
    missing_run_dirs = []
    missing_processed_dirs = []

    for run in selected_runs:
        run_dir = run_dir_for(run)
        processed_dir = run_dir / "processed"

        if not run_dir.exists():
            missing_run_dirs.append(str(run_dir))
        elif not processed_dir.exists():
            missing_processed_dirs.append(str(processed_dir))

    if missing_run_dirs or missing_processed_dirs:
        messages = []
        if missing_run_dirs:
            messages.append(f"Missing run directories: {missing_run_dirs}")
        if missing_processed_dirs:
            messages.append(f"Missing processed directories: {missing_processed_dirs}")
        raise FileNotFoundError("\n".join(messages))


def command_to_text(command: List[str]) -> str:
    return " ".join(command)


def execute_command(
    command: List[str],
    log_file: Path,
    dry_run: bool,
) -> subprocess.CompletedProcess[str] | None:
    with log_file.open("a", encoding="utf-8") as log:
        log.write("\n$ " + command_to_text(command) + "\n")

    if dry_run:
        return None

    result = subprocess.run(
        command,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )

    with log_file.open("a", encoding="utf-8") as log:
        log.write(result.stdout)
        if not result.stdout.endswith("\n"):
            log.write("\n")
        log.write(f"[exit_code] {result.returncode}\n")

    if result.returncode != 0:
        raise RuntimeError(
            f"Command failed with exit code {result.returncode}: {command_to_text(command)}\n"
            f"See log: {log_file}"
        )

    return result


def build_commands(run: WesRun, python_executable: str, no_overwrite: bool) -> List[List[str]]:
    run_dir = str(run_dir_for(run))
    inventory = str(inventory_path_for(run))
    manifest = str(manifest_path_for(run))
    report = str(validation_report_path_for(run))

    entity_cmd = [
        python_executable,
        "scripts/tep/build_vap_tep_entities.py",
        "--run-dir",
        run_dir,
    ]
    if not no_overwrite:
        entity_cmd.append("--overwrite")

    lineage_cmd = [
        python_executable,
        "scripts/tep/build_vap_tep_lineage_manifest.py",
        "--inventory",
        inventory,
    ]
    if not no_overwrite:
        lineage_cmd.append("--overwrite")

    validate_cmd = [
        python_executable,
        "scripts/tep/validate_vap_tep.py",
        "--manifest",
        manifest,
        "--write-updated-manifest",
        "--report",
        report,
    ]

    return [entity_cmd, lineage_cmd, validate_cmd]


def select_runs(sra_filter: Optional[List[str]]) -> List[WesRun]:
    if not sra_filter:
        return list(WES_RUNS)

    requested = set(sra_filter)
    known = {run.sra: run for run in WES_RUNS}
    unknown = sorted(requested - set(known))

    if unknown:
        raise ValueError(f"Unknown SRA(s): {unknown}. Known SRAs: {sorted(known)}")

    return [known[sra] for sra in sra_filter]


def write_manifest(out_dir: Path, selected_runs: List[WesRun], dry_run: bool, no_overwrite: bool) -> None:
    payload = {
        "script": "scripts/mark/generate_12_epilepsy_wes_vap_tep.py",
        "purpose": "Generate VAP-TEPs for 12 epilepsy WES SRA runs",
        "created_local": datetime.now().isoformat(timespec="seconds"),
        "dry_run": dry_run,
        "no_overwrite": no_overwrite,
        "runs": [
            {
                **asdict(run),
                "run_dir": str(run_dir_for(run)),
                "tep_id": tep_id_for(run),
                "tep_dir": str(tep_dir_for(run)),
                "entity_inventory": str(inventory_path_for(run)),
                "lineage_manifest": str(manifest_path_for(run)),
                "validation_report": str(validation_report_path_for(run)),
            }
            for run in selected_runs
        ],
    }

    with (out_dir / "generation_manifest.json").open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
        handle.write("\n")


def write_summary_tsv(out_dir: Path, rows: List[dict]) -> None:
    path = out_dir / "generation_summary.tsv"
    fields = [
        "sra",
        "run_id",
        "depth_category",
        "tep_id",
        "tep_dir",
        "status",
        "entity_inventory_exists",
        "lineage_manifest_exists",
        "validation_report_exists",
        "log_file",
        "error",
    ]

    with path.open("w", encoding="utf-8") as handle:
        handle.write("\t".join(fields) + "\n")
        for row in rows:
            handle.write("\t".join(str(row.get(field, "")) for field in fields) + "\n")


def process_run(
    run: WesRun,
    out_dir: Path,
    python_executable: str,
    dry_run: bool,
    no_overwrite: bool,
) -> dict:
    log_file = out_dir / f"{run.sra}_{run.run_id}.log"
    commands = build_commands(
        run=run,
        python_executable=python_executable,
        no_overwrite=no_overwrite,
    )

    row = {
        "sra": run.sra,
        "run_id": run.run_id,
        "depth_category": run.depth_category,
        "tep_id": tep_id_for(run),
        "tep_dir": str(tep_dir_for(run)),
        "status": "PENDING",
        "entity_inventory_exists": False,
        "lineage_manifest_exists": False,
        "validation_report_exists": False,
        "log_file": str(log_file),
        "error": "",
    }

    try:
        with log_file.open("w", encoding="utf-8") as log:
            log.write(f"# VAP-TEP generation log\n")
            log.write(f"sra: {run.sra}\n")
            log.write(f"run_id: {run.run_id}\n")
            log.write(f"depth_category: {run.depth_category}\n")
            log.write(f"tep_id: {tep_id_for(run)}\n")
            log.write(f"dry_run: {dry_run}\n")
            log.write(f"no_overwrite: {no_overwrite}\n")

        for command in commands:
            execute_command(command, log_file=log_file, dry_run=dry_run)

        row["entity_inventory_exists"] = inventory_path_for(run).exists()
        row["lineage_manifest_exists"] = manifest_path_for(run).exists()
        row["validation_report_exists"] = validation_report_path_for(run).exists()

        if dry_run:
            row["status"] = "DRY_RUN"
        elif (
            row["entity_inventory_exists"]
            and row["lineage_manifest_exists"]
            and row["validation_report_exists"]
        ):
            row["status"] = "PASS"
        else:
            row["status"] = "INCOMPLETE"
            row["error"] = "One or more expected output files missing."

    except Exception as exc:  # noqa: BLE001
        row["status"] = "FAIL"
        row["error"] = repr(exc)

    return row


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate VAP-TEPs for the 12 epilepsy WES SRA runs on MARK."
    )
    parser.add_argument(
        "--sra",
        nargs="+",
        default=None,
        help=(
            "Optional subset of SRA accessions to process. "
            "Example: --sra ERR10619300 ERR10619281"
        ),
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print/log planned commands without executing them.",
    )
    parser.add_argument(
        "--no-overwrite",
        action="store_true",
        help="Do not pass --overwrite to entity and lineage builders.",
    )
    parser.add_argument(
        "--continue-on-error",
        action="store_true",
        help="Continue processing remaining runs after a run fails.",
    )
    parser.add_argument(
        "--python",
        default=sys.executable,
        help="Python executable to use for subprocess calls. Defaults to current interpreter.",
    )
    args = parser.parse_args()

    ensure_repo_root()

    selected_runs = select_runs(args.sra)
    validate_inputs(selected_runs)

    out_dir = ensure_output_dir()
    write_manifest(
        out_dir=out_dir,
        selected_runs=selected_runs,
        dry_run=args.dry_run,
        no_overwrite=args.no_overwrite,
    )

    print(f"[INFO] Output directory: {out_dir}")
    print(f"[INFO] Runs selected: {len(selected_runs)}")
    print(f"[INFO] dry_run: {args.dry_run}")
    print(f"[INFO] no_overwrite: {args.no_overwrite}")

    rows: List[dict] = []

    for idx, run in enumerate(selected_runs, start=1):
        print("")
        print(f"[INFO] [{idx}/{len(selected_runs)}] Processing {run.sra} / {run.run_id} ({run.depth_category})")
        row = process_run(
            run=run,
            out_dir=out_dir,
            python_executable=args.python,
            dry_run=args.dry_run,
            no_overwrite=args.no_overwrite,
        )
        rows.append(row)
        write_summary_tsv(out_dir, rows)

        print(f"[INFO] status: {row['status']}")
        print(f"[INFO] tep_dir: {row['tep_dir']}")

        if row["status"] == "FAIL" and not args.continue_on_error:
            print(f"[ERROR] {row['error']}")
            print("[ERROR] Stopping because --continue-on-error was not supplied.")
            return 1

    write_summary_tsv(out_dir, rows)

    failures = [row for row in rows if row["status"] == "FAIL"]
    incomplete = [row for row in rows if row["status"] == "INCOMPLETE"]

    print("")
    print("VAP-TEP epilepsy WES generation complete.")
    print("")
    print(f"Output directory:\n{out_dir}")
    print("")
    print(f"PASS: {sum(1 for row in rows if row['status'] == 'PASS')}")
    print(f"DRY_RUN: {sum(1 for row in rows if row['status'] == 'DRY_RUN')}")
    print(f"INCOMPLETE: {len(incomplete)}")
    print(f"FAIL: {len(failures)}")
    print("")
    print("Summary:")
    print(out_dir / "generation_summary.tsv")

    return 1 if failures or incomplete else 0


if __name__ == "__main__":
    raise SystemExit(main())
