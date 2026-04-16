#!/usr/bin/env python3
"""
prepare_srr_hg002.py

Repo 2 preprocessing utility for preparing a validated paired-end FASTQ input set
from a single SRA accession.

Supported modes:
- status
- verify-only
- run
- force

Canonical retained artifacts:
- <sra_dir>/<SRR>/<SRR>.sra
- <fastq_dir>/<SRR>_1.fastq.gz
- <fastq_dir>/<SRR>_2.fastq.gz

Runtime-scoped artifacts:
- <fastq_dir>/logs/<run_id>.prep.log
- <fastq_dir>/logs/<run_id>.prep.json
- <tmp_dir>/<run_id>/
- <fastq_dir>/quarantine/<run_id>/
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import logging
import math
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

DEFAULT_ACCESSION = "SRR12898354"
DEFAULT_SRA_DIR = "/mnt/storage/sra"
DEFAULT_FASTQ_DIR = "/mnt/storage/fastq"
DEFAULT_TMP_BASE = "/mnt/storage/tmp"
DEFAULT_MIN_FREE_GB = 50.0
DEFAULT_PREFETCH_MAX_SIZE = "100G"
DEFAULT_PIGZ_THREADS_OVERRIDE = None
RUN_MODES = {"status", "verify-only", "run", "force"}


class PrepError(Exception):
    pass


def now_iso() -> str:
    return dt.datetime.now().astimezone().isoformat()


def make_run_id(accession: str) -> str:
    stamp = dt.datetime.now().strftime("%Y_%m_%d_%H%M%S")
    return f"prep_{accession}_{stamp}"


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def human_bytes(num: int) -> str:
    units = ["B", "KB", "MB", "GB", "TB", "PB"]
    size = float(num)
    for unit in units:
        if size < 1024.0 or unit == units[-1]:
            return f"{size:.2f}{unit}"
        size /= 1024.0
    return f"{num}B"


def run_cmd(
    cmd: list[str],
    logger: logging.Logger,
    phase: str,
    check: bool = True,
    capture_output: bool = True,
    text: bool = True,
) -> subprocess.CompletedProcess:
    logger.info(f"PHASE: {phase}")
    logger.info("COMMAND: %s", " ".join(cmd))
    result = subprocess.run(cmd, capture_output=capture_output, text=text, check=False)
    if result.stdout:
        logger.info("STDOUT:\n%s", result.stdout.strip())
    if result.stderr:
        logger.info("STDERR:\n%s", result.stderr.strip())
    if check and result.returncode != 0:
        raise PrepError(f"Command failed in phase '{phase}' with exit code {result.returncode}: {' '.join(cmd)}")
    return result


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        while True:
            chunk = handle.read(chunk_size)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def get_tool_version(tool: str) -> str:
    version_cmds = {
        "fasterq-dump": [tool, "--version"],
        "pigz": [tool, "--version"],
        "vdb-validate": [tool, "--version"],
        "prefetch": [tool, "--version"],
        "gzip": [tool, "--version"],
    }
    cmd = version_cmds.get(tool, [tool, "--version"])
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)
        text = (result.stdout or result.stderr or "").strip()
        return text.splitlines()[0] if text else "unknown"
    except Exception:
        return "unknown"


def disk_free_bytes(path: Path) -> int:
    usage = shutil.disk_usage(path)
    return usage.free


def line_count_plain(path: Path, logger: logging.Logger, phase: str) -> int:
    result = run_cmd(["wc", "-l", str(path)], logger, phase)
    try:
        return int(result.stdout.strip().split()[0])
    except Exception as exc:
        raise PrepError(f"Unable to parse line count for {path}: {exc}") from exc


def line_count_gz(path: Path, logger: logging.Logger, phase: str) -> int:
    cmd = f"zcat {shlex_quote(str(path))} | wc -l"
    result = run_cmd(["bash", "-lc", cmd], logger, phase)
    try:
        return int(result.stdout.strip().split()[0])
    except Exception as exc:
        raise PrepError(f"Unable to parse compressed line count for {path}: {exc}") from exc


def shlex_quote(text: str) -> str:
    import shlex
    return shlex.quote(text)


def gzip_test(path: Path, logger: logging.Logger, phase: str) -> bool:
    result = run_cmd(["gzip", "-t", str(path)], logger, phase, check=False)
    return result.returncode == 0


def require_tools(tools: list[str], logger: logging.Logger) -> dict[str, str]:
    found: dict[str, str] = {}
    for tool in tools:
        tool_path = shutil.which(tool)
        if not tool_path:
            raise PrepError(f"Required tool not found in PATH: {tool}")
        found[tool] = tool_path
        logger.info("FOUND TOOL: %s -> %s", tool, tool_path)
    return found


def compute_pigz_threads(nproc_value: int, override: int | None) -> int:
    if override is not None:
        return max(1, int(override))
    return max(1, math.floor(nproc_value / 2))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Prepare HG002 SRR inputs for Repo 2.")
    parser.add_argument("--mode", required=True, choices=sorted(RUN_MODES))
    parser.add_argument("--accession", default=DEFAULT_ACCESSION)
    parser.add_argument("--sra-dir", default=DEFAULT_SRA_DIR)
    parser.add_argument("--fastq-dir", default=DEFAULT_FASTQ_DIR)
    parser.add_argument("--tmp-base", default=DEFAULT_TMP_BASE)
    parser.add_argument("--min-free-gb", type=float, default=DEFAULT_MIN_FREE_GB)
    parser.add_argument("--prefetch-max-size", default=DEFAULT_PREFETCH_MAX_SIZE)
    parser.add_argument("--pigz-threads", type=int, default=DEFAULT_PIGZ_THREADS_OVERRIDE)
    parser.add_argument("--delete-instead-of-quarantine", action="store_true")
    return parser.parse_args()


def build_paths(args: argparse.Namespace, run_id: str) -> dict[str, Path]:
    sra_root = Path(args.sra_dir)
    fastq_root = Path(args.fastq_dir)
    tmp_base = Path(args.tmp_base)

    return {
        "sra_root": sra_root,
        "fastq_root": fastq_root,
        "tmp_base": tmp_base,
        "sra_dir": sra_root / args.accession,
        "sra_file": sra_root / args.accession / f"{args.accession}.sra",
        "fastq_1": fastq_root / f"{args.accession}_1.fastq",
        "fastq_2": fastq_root / f"{args.accession}_2.fastq",
        "singleton_fastq": fastq_root / f"{args.accession}.fastq",
        "fastq_1_gz": fastq_root / f"{args.accession}_1.fastq.gz",
        "fastq_2_gz": fastq_root / f"{args.accession}_2.fastq.gz",
        "logs_dir": fastq_root / "logs",
        "quarantine_dir": fastq_root / "quarantine" / run_id,
        "tmp_dir": tmp_base / run_id,
        "log_file": fastq_root / "logs" / f"{run_id}.prep.log",
        "json_report": fastq_root / "logs" / f"{run_id}.prep.json",
    }


def setup_logger(log_file: Path) -> logging.Logger:
    ensure_dir(log_file.parent)
    logger = logging.getLogger(f"prepare_srr_hg002_{log_file.stem}")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()

    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")

    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    logger.propagate = False
    return logger


def build_state(args: argparse.Namespace, run_id: str, paths: dict[str, Path]) -> dict[str, Any]:
    return {
        "run_id": run_id,
        "start_time": now_iso(),
        "end_time": None,
        "duration_seconds": None,
        "accession": args.accession,
        "mode": args.mode,
        "overall_success": False,
        "failure_reason": None,
        "work_skipped": False,
        "existing_assets_reused": False,
        "phases_executed": [],
        "phase_status_map": {},
        "tool_versions": {},
        "disk": {},
        "cpu": {},
        "paths": {k: str(v) for k, v in paths.items()},
        "artifacts": {
            "raw_line_counts": {},
            "compressed_line_counts": {},
            "sizes_bytes": {},
            "sha256": {},
            "singleton_present": False,
            "singleton_removed": False,
        },
    }


def mark_phase(state: dict[str, Any], phase: str, status: str) -> None:
    state["phases_executed"].append(phase)
    state["phase_status_map"][phase] = status


def write_json_report(state: dict[str, Any], report_path: Path) -> None:
    ensure_dir(report_path.parent)
    with report_path.open("w", encoding="utf-8") as handle:
        json.dump(state, handle, indent=2, sort_keys=True)


def file_exists(path: Path) -> bool:
    return path.exists() and path.is_file()


def remove_path(path: Path) -> None:
    if path.is_file():
        path.unlink()
    elif path.is_dir():
        shutil.rmtree(path)


def move_to_quarantine(path: Path, quarantine_dir: Path, logger: logging.Logger) -> None:
    if not path.exists():
        return
    ensure_dir(quarantine_dir)
    target = quarantine_dir / path.name
    logger.info("QUARANTINE: %s -> %s", path, target)
    shutil.move(str(path), str(target))


def quarantine_or_delete_partial_outputs(
    paths: dict[str, Path],
    delete_instead: bool,
    logger: logging.Logger,
) -> None:
    candidates = [
        paths["fastq_1"],
        paths["fastq_2"],
        paths["singleton_fastq"],
        paths["fastq_1_gz"],
        paths["fastq_2_gz"],
    ]
    for candidate in candidates:
        if not candidate.exists():
            continue
        if delete_instead:
            logger.info("DELETE PARTIAL OUTPUT: %s", candidate)
            remove_path(candidate)
        else:
            move_to_quarantine(candidate, paths["quarantine_dir"], logger)

    if paths["tmp_dir"].exists():
        logger.info("DELETE TEMP DIR: %s", paths["tmp_dir"])
        remove_path(paths["tmp_dir"])


def validate_existing_sra(paths: dict[str, Path], logger: logging.Logger, state: dict[str, Any]) -> bool:
    phase = "sra validation"
    mark_phase(state, phase, "started")
    if not file_exists(paths["sra_file"]):
        mark_phase(state, phase, "missing")
        return False
    result = run_cmd(["vdb-validate", str(paths["sra_file"])], logger, phase, check=False)
    ok = result.returncode == 0 and "is consistent" in (result.stdout + result.stderr)
    mark_phase(state, phase, "passed" if ok else "failed")
    return ok


def validate_gz_pair(paths: dict[str, Path], logger: logging.Logger, state: dict[str, Any]) -> bool:
    phase = "compressed paired fastq verification"
    mark_phase(state, phase, "started")

    if not file_exists(paths["fastq_1_gz"]) or not file_exists(paths["fastq_2_gz"]):
        mark_phase(state, phase, "missing")
        return False

    ok1 = gzip_test(paths["fastq_1_gz"], logger, phase)
    ok2 = gzip_test(paths["fastq_2_gz"], logger, phase)
    if not (ok1 and ok2):
        mark_phase(state, phase, "failed")
        return False

    count1 = line_count_gz(paths["fastq_1_gz"], logger, phase)
    count2 = line_count_gz(paths["fastq_2_gz"], logger, phase)
    state["artifacts"]["compressed_line_counts"]["fastq_1_gz"] = count1
    state["artifacts"]["compressed_line_counts"]["fastq_2_gz"] = count2

    if count1 != count2 or count1 % 4 != 0 or count2 % 4 != 0:
        mark_phase(state, phase, "failed")
        return False

    mark_phase(state, phase, "passed")
    return True


def check_preflight(args: argparse.Namespace, paths: dict[str, Path], logger: logging.Logger, state: dict[str, Any]) -> dict[str, str]:
    phase = "preflight"
    mark_phase(state, phase, "started")

    for d in [paths["sra_root"], paths["fastq_root"], paths["logs_dir"], paths["tmp_base"]]:
        ensure_dir(d)

    tools = require_tools(
        ["prefetch", "vdb-validate", "fasterq-dump", "pigz", "wc", "zcat", "nproc", "gzip"],
        logger,
    )

    state["tool_versions"] = {
        "prefetch": get_tool_version("prefetch"),
        "vdb-validate": get_tool_version("vdb-validate"),
        "fasterq-dump": get_tool_version("fasterq-dump"),
        "pigz": get_tool_version("pigz"),
        "gzip": get_tool_version("gzip"),
    }

    nproc_result = run_cmd(["nproc"], logger, "core-count inspection")
    nproc_value = int(nproc_result.stdout.strip())
    pigz_threads = compute_pigz_threads(nproc_value, args.pigz_threads)
    state["cpu"] = {"nproc": nproc_value, "pigz_threads": pigz_threads}

    if paths["tmp_base"].exists():
        foreign_entries = [p for p in paths["tmp_base"].iterdir() if p.name != paths["tmp_dir"].name]
        if foreign_entries and args.mode != "force":
            raise PrepError(
                f"Temp base contains entries not scoped to current run_id and mode is not force: {[str(p) for p in foreign_entries]}"
            )

    mark_phase(state, phase, "passed")
    return tools


def check_storage_before_prefetch(args: argparse.Namespace, paths: dict[str, Path], logger: logging.Logger, state: dict[str, Any]) -> None:
    phase = "storage check"
    mark_phase(state, phase, "started")
    free_bytes = disk_free_bytes(paths["fastq_root"])
    state["disk"]["before_prefetch_free_bytes"] = free_bytes
    state["disk"]["before_prefetch_free_human"] = human_bytes(free_bytes)
    minimum_bytes = int(args.min_free_gb * (1024 ** 3))
    state["disk"]["before_prefetch_minimum_bytes"] = minimum_bytes
    if free_bytes < minimum_bytes:
        mark_phase(state, phase, "failed")
        raise PrepError(
            f"Insufficient free space before prefetch: have {human_bytes(free_bytes)}, need at least {human_bytes(minimum_bytes)}"
        )
    mark_phase(state, phase, "passed")


def check_storage_before_extraction(paths: dict[str, Path], logger: logging.Logger, state: dict[str, Any]) -> None:
    phase = "storage check (post-sra)"
    mark_phase(state, phase, "started")
    if not file_exists(paths["sra_file"]):
        mark_phase(state, phase, "failed")
        raise PrepError(f"SRA file missing for post-SRA storage check: {paths['sra_file']}")
    sra_size = paths["sra_file"].stat().st_size
    free_bytes = disk_free_bytes(paths["fastq_root"])
    required = sra_size * 3
    state["disk"]["post_sra_free_bytes"] = free_bytes
    state["disk"]["post_sra_free_human"] = human_bytes(free_bytes)
    state["disk"]["sra_size_bytes"] = sra_size
    state["disk"]["sra_size_human"] = human_bytes(sra_size)
    state["disk"]["post_sra_required_bytes"] = required
    state["disk"]["post_sra_required_human"] = human_bytes(required)
    if free_bytes < required:
        mark_phase(state, phase, "failed")
        raise PrepError(
            f"Insufficient free space before extraction: have {human_bytes(free_bytes)}, require {human_bytes(required)}"
        )
    mark_phase(state, phase, "passed")


def handle_existing_assets(args: argparse.Namespace, paths: dict[str, Path], logger: logging.Logger, state: dict[str, Any]) -> bool:
    if args.mode == "force":
        logger.info("FORCE MODE: removing prior derived outputs and accession directory if present")
        for p in [paths["fastq_1"], paths["fastq_2"], paths["singleton_fastq"], paths["fastq_1_gz"], paths["fastq_2_gz"], paths["tmp_dir"]]:
            if p.exists():
                remove_path(p)
        if paths["sra_dir"].exists():
            remove_path(paths["sra_dir"])
        return False

    sra_ok = validate_existing_sra(paths, logger, state)
    gz_ok = validate_gz_pair(paths, logger, state)

    if args.mode == "status":
        state["existing_assets_reused"] = sra_ok and gz_ok
        return sra_ok and gz_ok

    if args.mode == "verify-only":
        if not sra_ok:
            raise PrepError("verify-only failed: existing SRA is missing or invalid")
        if not gz_ok:
            raise PrepError("verify-only failed: compressed FASTQ pair is missing or invalid")
        state["existing_assets_reused"] = True
        return True

    if sra_ok and gz_ok:
        state["work_skipped"] = True
        state["existing_assets_reused"] = True
        return True

    return False


def acquire_sra(args: argparse.Namespace, paths: dict[str, Path], logger: logging.Logger, state: dict[str, Any]) -> None:
    phase = "sra acquisition"
    mark_phase(state, phase, "started")
    cmd = [
        "prefetch",
        args.accession,
        "--max-size",
        args.prefetch_max_size,
        "--force",
        "all",
        "--output-directory",
        str(paths["sra_root"]),
    ]
    run_cmd(cmd, logger, phase)
    if not file_exists(paths["sra_file"]):
        mark_phase(state, phase, "failed")
        raise PrepError(f"SRA not found after acquisition: {paths['sra_file']}")
    state["artifacts"]["sizes_bytes"]["sra"] = paths["sra_file"].stat().st_size
    mark_phase(state, phase, "passed")


def extract_fastq(args: argparse.Namespace, paths: dict[str, Path], logger: logging.Logger, state: dict[str, Any]) -> None:
    phase = "fastq extraction"
    mark_phase(state, phase, "started")
    ensure_dir(paths["tmp_dir"])
    start = time.time()
    cmd = [
        "fasterq-dump",
        str(paths["sra_file"]),
        "--split-3",
        "--threads",
        str(state["cpu"]["pigz_threads"]),
        "--temp",
        str(paths["tmp_dir"]),
        "-O",
        str(paths["fastq_root"]),
    ]
    run_cmd(cmd, logger, phase)
    state["extraction_duration_seconds"] = round(time.time() - start, 3)
    if not file_exists(paths["fastq_1"]) or not file_exists(paths["fastq_2"]):
        mark_phase(state, phase, "failed")
        raise PrepError("FASTQ extraction did not produce both paired files")
    state["artifacts"]["singleton_present"] = file_exists(paths["singleton_fastq"])
    mark_phase(state, phase, "passed")


def verify_raw_fastq(paths: dict[str, Path], logger: logging.Logger, state: dict[str, Any]) -> None:
    phase = "raw paired fastq verification"
    mark_phase(state, phase, "started")

    size1 = paths["fastq_1"].stat().st_size
    size2 = paths["fastq_2"].stat().st_size
    state["artifacts"]["sizes_bytes"]["fastq_1"] = size1
    state["artifacts"]["sizes_bytes"]["fastq_2"] = size2

    rel_diff = abs(size1 - size2) / max(size1, size2)
    state["artifacts"]["raw_relative_size_difference"] = rel_diff
    if rel_diff > 0.20:
        logger.warning("Raw FASTQ file size difference exceeds 20%%: %.4f", rel_diff)

    count1 = line_count_plain(paths["fastq_1"], logger, phase)
    count2 = line_count_plain(paths["fastq_2"], logger, phase)
    state["artifacts"]["raw_line_counts"]["fastq_1"] = count1
    state["artifacts"]["raw_line_counts"]["fastq_2"] = count2

    if file_exists(paths["singleton_fastq"]):
        state["artifacts"]["singleton_present"] = True
        singleton_count = line_count_plain(paths["singleton_fastq"], logger, phase)
        state["artifacts"]["raw_line_counts"]["singleton_fastq"] = singleton_count
        state["artifacts"]["sizes_bytes"]["singleton_fastq"] = paths["singleton_fastq"].stat().st_size

    if count1 != count2 or count1 % 4 != 0 or count2 % 4 != 0:
        mark_phase(state, phase, "failed")
        raise PrepError(f"Raw FASTQ pair failed validation: fastq_1={count1}, fastq_2={count2}")

    mark_phase(state, phase, "passed")


def remove_singleton(paths: dict[str, Path], logger: logging.Logger, state: dict[str, Any]) -> None:
    phase = "singleton removal"
    mark_phase(state, phase, "started")
    if file_exists(paths["singleton_fastq"]):
        logger.info("Removing singleton FASTQ: %s", paths["singleton_fastq"])
        remove_path(paths["singleton_fastq"])
        state["artifacts"]["singleton_removed"] = True
    mark_phase(state, phase, "passed")


def compress_fastq(paths: dict[str, Path], logger: logging.Logger, state: dict[str, Any]) -> None:
    phase = "paired fastq compression"
    mark_phase(state, phase, "started")
    start = time.time()
    threads = str(state["cpu"]["pigz_threads"])
    run_cmd(["pigz", "-p", threads, str(paths["fastq_1"])], logger, phase)
    run_cmd(["pigz", "-p", threads, str(paths["fastq_2"])], logger, phase)
    state["compression_duration_seconds"] = round(time.time() - start, 3)
    if not file_exists(paths["fastq_1_gz"]) or not file_exists(paths["fastq_2_gz"]):
        mark_phase(state, phase, "failed")
        raise PrepError("Compression did not produce both paired gz files")
    mark_phase(state, phase, "passed")


def verify_compressed_fastq(paths: dict[str, Path], logger: logging.Logger, state: dict[str, Any]) -> None:
    phase = "compressed paired fastq verification"
    mark_phase(state, phase, "started")
    if not gzip_test(paths["fastq_1_gz"], logger, phase) or not gzip_test(paths["fastq_2_gz"], logger, phase):
        mark_phase(state, phase, "failed")
        raise PrepError("gzip integrity check failed for compressed FASTQ pair")

    count1 = line_count_gz(paths["fastq_1_gz"], logger, phase)
    count2 = line_count_gz(paths["fastq_2_gz"], logger, phase)
    state["artifacts"]["compressed_line_counts"]["fastq_1_gz"] = count1
    state["artifacts"]["compressed_line_counts"]["fastq_2_gz"] = count2

    if count1 != count2 or count1 % 4 != 0 or count2 % 4 != 0:
        mark_phase(state, phase, "failed")
        raise PrepError(f"Compressed FASTQ pair failed validation: fastq_1_gz={count1}, fastq_2_gz={count2}")

    mark_phase(state, phase, "passed")


def provisional_report(paths: dict[str, Path], logger: logging.Logger, state: dict[str, Any]) -> None:
    phase = "provisional audit log emission (pre-cleanup)"
    mark_phase(state, phase, "started")
    write_json_report(state, paths["json_report"])
    mark_phase(state, phase, "passed")


def final_cleanup(paths: dict[str, Path], logger: logging.Logger, state: dict[str, Any]) -> None:
    phase = "final cleanup"
    mark_phase(state, phase, "started")
    for p in [paths["fastq_1"], paths["fastq_2"], paths["singleton_fastq"]]:
        if p.exists():
            logger.info("CLEANUP REMOVE: %s", p)
            remove_path(p)
    if paths["tmp_dir"].exists():
        logger.info("CLEANUP REMOVE TMP DIR: %s", paths["tmp_dir"])
        remove_path(paths["tmp_dir"])
    mark_phase(state, phase, "passed")


def final_retained_state_verification(paths: dict[str, Path], logger: logging.Logger, state: dict[str, Any]) -> None:
    phase = "final retained-state verification"
    mark_phase(state, phase, "started")
    required = [paths["sra_file"], paths["fastq_1_gz"], paths["fastq_2_gz"]]
    for p in required:
        if not file_exists(p):
            mark_phase(state, phase, "failed")
            raise PrepError(f"Required retained artifact missing: {p}")

    state["artifacts"]["sha256"]["sra"] = sha256_file(paths["sra_file"])
    state["artifacts"]["sha256"]["fastq_1_gz"] = sha256_file(paths["fastq_1_gz"])
    state["artifacts"]["sha256"]["fastq_2_gz"] = sha256_file(paths["fastq_2_gz"])
    mark_phase(state, phase, "passed")


def final_report(paths: dict[str, Path], logger: logging.Logger, state: dict[str, Any], success: bool) -> None:
    phase = "final audit log update / completion"
    mark_phase(state, phase, "started")
    state["overall_success"] = success
    state["end_time"] = now_iso()
    start_dt = dt.datetime.fromisoformat(state["start_time"])
    end_dt = dt.datetime.fromisoformat(state["end_time"])
    state["duration_seconds"] = round((end_dt - start_dt).total_seconds(), 3)
    write_json_report(state, paths["json_report"])
    mark_phase(state, phase, "passed")


def print_status_summary(state: dict[str, Any]) -> None:
    summary = {
        "run_id": state["run_id"],
        "mode": state["mode"],
        "overall_success": state["overall_success"],
        "work_skipped": state["work_skipped"],
        "existing_assets_reused": state["existing_assets_reused"],
        "phase_status_map": state["phase_status_map"],
        "paths": state["paths"],
    }
    print(json.dumps(summary, indent=2, sort_keys=True))


def main() -> int:
    args = parse_args()
    if args.mode not in RUN_MODES:
        print(f"Unsupported mode: {args.mode}", file=sys.stderr)
        return 2

    run_id = make_run_id(args.accession)
    paths = build_paths(args, run_id)
    logger = setup_logger(paths["log_file"])
    state = build_state(args, run_id, paths)

    logger.info("RUN_ID: %s", run_id)
    logger.info("MODE: %s", args.mode)
    logger.info("ACCESSION: %s", args.accession)

    try:
        check_preflight(args, paths, logger, state)

        reusable = handle_existing_assets(args, paths, logger, state)

        if args.mode == "status":
            state["overall_success"] = True
            final_report(paths, logger, state, True)
            print_status_summary(state)
            return 0

        if reusable:
            logger.info("Existing validated assets are reusable; no heavy processing required.")
            final_report(paths, logger, state, True)
            print_status_summary(state)
            return 0

        if args.mode in {"run", "force"}:
            check_storage_before_prefetch(args, paths, logger, state)
            if not validate_existing_sra(paths, logger, state):
                acquire_sra(args, paths, logger, state)
                if not validate_existing_sra(paths, logger, state):
                    raise PrepError("SRA validation failed after acquisition")

            check_storage_before_extraction(paths, logger, state)
            extract_fastq(args, paths, logger, state)
            verify_raw_fastq(paths, logger, state)
            remove_singleton(paths, logger, state)
            compress_fastq(paths, logger, state)
            verify_compressed_fastq(paths, logger, state)
            provisional_report(paths, logger, state)
            final_cleanup(paths, logger, state)
            final_retained_state_verification(paths, logger, state)
            final_report(paths, logger, state, True)
            print_status_summary(state)
            return 0

        raise PrepError(f"Unhandled mode: {args.mode}")

    except Exception as exc:
        logger.exception("PREPROCESSING FAILED")
        state["failure_reason"] = str(exc)
        try:
            quarantine_or_delete_partial_outputs(
                paths,
                delete_instead=args.delete_instead_of_quarantine,
                logger=logger,
            )
        except Exception as cleanup_exc:
            logger.exception("Failure cleanup itself failed: %s", cleanup_exc)
        try:
            final_report(paths, logger, state, False)
        except Exception:
            logger.exception("Unable to write final failure report")
        print(json.dumps({"run_id": state["run_id"], "mode": state["mode"], "error": str(exc)}, indent=2))
        return 1


if __name__ == "__main__":
    sys.exit(main())