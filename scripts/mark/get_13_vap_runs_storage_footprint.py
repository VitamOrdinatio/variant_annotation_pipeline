#!/usr/bin/env python3
"""Read-only MARK utility for measuring the 13 official VAP run footprints.

This is a one-off operator utility authored during VDB/VAP integration work.
It is intentionally read-only with respect to VAP and VDB project data. It only
writes receipt files under /root/Desktop by default.
"""

from __future__ import annotations

import argparse
import csv
import json
import shutil
import subprocess
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


MANIFEST = [
    ("ERR10619203", "run_2026_05_30_071639", "q3"),
    ("ERR10619207", "run_2026_06_01_124134", "q3"),
    ("ERR10619208", "run_2026_05_30_151355", "median"),
    ("ERR10619212", "run_2026_05_30_214724", "q1"),
    ("ERR10619225", "run_2026_05_31_091242", "q3"),
    ("ERR10619230", "run_2026_06_01_004903", "q3"),
    ("ERR10619241", "run_2026_06_02_052302", "q1"),
    ("ERR10619281", "run_2026_05_27_233524", "median"),
    ("ERR10619285", "run_2026_06_02_124300", "median"),
    ("ERR10619300", "run_2026_05_27_172531", "median"),
    ("ERR10619309", "run_2026_06_02_181024", "q1"),
    ("ERR10619330", "run_2026_06_01_203130", "q1"),
    ("SRR12898354", "run_2026_06_03_010030", "hg002"),
]


@dataclass(frozen=True)
class RunFootprint:
    sra: str
    run_id: str
    depth_category: str
    run_path: str
    run_exists: bool
    run_allocated_bytes: int
    run_apparent_bytes: int
    run_allocated_human: str
    run_apparent_human: str
    tep_dir: str
    tep_exists: bool
    tep_allocated_bytes: int
    tep_apparent_bytes: int
    tep_allocated_human: str
    tep_apparent_human: str
    non_tep_allocated_bytes: int
    non_tep_allocated_human: str
    status: str


@dataclass(frozen=True)
class TopLevelFootprint:
    sra: str
    run_id: str
    depth_category: str
    child_name: str
    child_path: str
    child_type: str
    allocated_bytes: int
    apparent_bytes: int
    allocated_human: str
    apparent_human: str


def now_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def human_bytes(num_bytes: int) -> str:
    if num_bytes < 0:
        return "NA"
    value = float(num_bytes)
    units = ["B", "KiB", "MiB", "GiB", "TiB", "PiB"]
    for unit in units:
        if abs(value) < 1024.0 or unit == units[-1]:
            if unit == "B":
                return f"{int(value)} {unit}"
            return f"{value:.2f} {unit}"
        value /= 1024.0
    return f"{num_bytes} B"


def run_du(path: Path, apparent: bool) -> int:
    """Return bytes from GNU du.

    apparent=False reports allocated disk usage in bytes via du -sB1.
    apparent=True reports apparent file sizes in bytes via du -sb.
    """
    if not path.exists():
        return 0
    cmd = ["du", "-sb", str(path)] if apparent else ["du", "-sB1", str(path)]
    proc = subprocess.run(cmd, check=True, text=True, capture_output=True)
    first = proc.stdout.strip().splitlines()[0].split()[0]
    return int(first)


def find_tep_dir(run_path: Path) -> Path | None:
    tep_root = run_path / "tep"
    if not tep_root.is_dir():
        return None
    candidates = sorted(p for p in tep_root.iterdir() if p.is_dir() and p.name.startswith("vap_tep_") and p.name.endswith("_v1"))
    if candidates:
        return candidates[0]
    candidates = sorted(p for p in tep_root.iterdir() if p.is_dir())
    return candidates[0] if candidates else None


def iter_top_level(run_path: Path) -> Iterable[Path]:
    if not run_path.is_dir():
        return []
    return sorted(run_path.iterdir(), key=lambda p: p.name)


def write_tsv(path: Path, rows: Iterable[dict], fieldnames: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def collect_footprints(vap_repo_root: Path) -> tuple[list[RunFootprint], list[TopLevelFootprint]]:
    results_root = vap_repo_root / "results"
    runs: list[RunFootprint] = []
    top_level: list[TopLevelFootprint] = []

    for sra, run_id, depth in MANIFEST:
        run_path = results_root / run_id
        run_exists = run_path.is_dir()
        status = "present" if run_exists else "missing_run_directory"

        run_allocated = run_du(run_path, apparent=False) if run_exists else 0
        run_apparent = run_du(run_path, apparent=True) if run_exists else 0

        tep_dir = find_tep_dir(run_path) if run_exists else None
        tep_exists = tep_dir is not None and tep_dir.is_dir()
        tep_allocated = run_du(tep_dir, apparent=False) if tep_exists and tep_dir else 0
        tep_apparent = run_du(tep_dir, apparent=True) if tep_exists and tep_dir else 0
        non_tep_allocated = max(run_allocated - tep_allocated, 0)

        runs.append(
            RunFootprint(
                sra=sra,
                run_id=run_id,
                depth_category=depth,
                run_path=str(run_path),
                run_exists=run_exists,
                run_allocated_bytes=run_allocated,
                run_apparent_bytes=run_apparent,
                run_allocated_human=human_bytes(run_allocated),
                run_apparent_human=human_bytes(run_apparent),
                tep_dir=str(tep_dir) if tep_dir else "",
                tep_exists=tep_exists,
                tep_allocated_bytes=tep_allocated,
                tep_apparent_bytes=tep_apparent,
                tep_allocated_human=human_bytes(tep_allocated),
                tep_apparent_human=human_bytes(tep_apparent),
                non_tep_allocated_bytes=non_tep_allocated,
                non_tep_allocated_human=human_bytes(non_tep_allocated),
                status=status,
            )
        )

        for child in iter_top_level(run_path):
            allocated = run_du(child, apparent=False)
            apparent = run_du(child, apparent=True)
            if child.is_dir():
                child_type = "directory"
            elif child.is_file():
                child_type = "file"
            else:
                child_type = "other"
            top_level.append(
                TopLevelFootprint(
                    sra=sra,
                    run_id=run_id,
                    depth_category=depth,
                    child_name=child.name,
                    child_path=str(child),
                    child_type=child_type,
                    allocated_bytes=allocated,
                    apparent_bytes=apparent,
                    allocated_human=human_bytes(allocated),
                    apparent_human=human_bytes(apparent),
                )
            )

    return runs, top_level


def summarize_by_depth(runs: list[RunFootprint]) -> list[dict]:
    grouped: dict[str, dict] = {}
    for row in runs:
        bucket = grouped.setdefault(
            row.depth_category,
            {
                "depth_category": row.depth_category,
                "run_count": 0,
                "present_run_count": 0,
                "run_allocated_bytes": 0,
                "run_apparent_bytes": 0,
                "tep_allocated_bytes": 0,
                "non_tep_allocated_bytes": 0,
            },
        )
        bucket["run_count"] += 1
        if row.run_exists:
            bucket["present_run_count"] += 1
        bucket["run_allocated_bytes"] += row.run_allocated_bytes
        bucket["run_apparent_bytes"] += row.run_apparent_bytes
        bucket["tep_allocated_bytes"] += row.tep_allocated_bytes
        bucket["non_tep_allocated_bytes"] += row.non_tep_allocated_bytes

    summaries = []
    for bucket in sorted(grouped.values(), key=lambda x: x["depth_category"]):
        out = dict(bucket)
        out["run_allocated_human"] = human_bytes(out["run_allocated_bytes"])
        out["run_apparent_human"] = human_bytes(out["run_apparent_bytes"])
        out["tep_allocated_human"] = human_bytes(out["tep_allocated_bytes"])
        out["non_tep_allocated_human"] = human_bytes(out["non_tep_allocated_bytes"])
        summaries.append(out)
    return summaries


def print_console_report(runs: list[RunFootprint], depth_summary: list[dict], out_dir: Path) -> None:
    total_run = sum(r.run_allocated_bytes for r in runs)
    total_tep = sum(r.tep_allocated_bytes for r in runs)
    total_non_tep = sum(r.non_tep_allocated_bytes for r in runs)

    print("VAP 13-run storage footprint")
    print("=" * 80)
    print(f"output_dir: {out_dir}")
    print()
    print("Per-run allocated disk usage")
    print("-" * 80)
    print(f"{'SRA':<12} {'run_id':<22} {'depth':<8} {'run':>12} {'TEP':>12} {'non-TEP':>12} {'status'}")
    for row in sorted(runs, key=lambda r: r.run_allocated_bytes, reverse=True):
        print(
            f"{row.sra:<12} {row.run_id:<22} {row.depth_category:<8} "
            f"{row.run_allocated_human:>12} {row.tep_allocated_human:>12} "
            f"{row.non_tep_allocated_human:>12} {row.status}"
        )
    print("-" * 80)
    print(f"{'TOTAL':<43} {human_bytes(total_run):>12} {human_bytes(total_tep):>12} {human_bytes(total_non_tep):>12}")
    print()
    print("By depth category")
    print("-" * 80)
    print(f"{'depth':<8} {'runs':>5} {'present':>8} {'run total':>12} {'TEP total':>12} {'non-TEP':>12}")
    for row in depth_summary:
        print(
            f"{row['depth_category']:<8} {row['run_count']:>5} {row['present_run_count']:>8} "
            f"{row['run_allocated_human']:>12} {row['tep_allocated_human']:>12} "
            f"{row['non_tep_allocated_human']:>12}"
        )
    print()
    print("Receipt files written:")
    for path in sorted(out_dir.iterdir()):
        print(f"  {path}")


def write_report(out_dir: Path, runs: list[RunFootprint], depth_summary: list[dict], context: dict) -> None:
    total_run = sum(r.run_allocated_bytes for r in runs)
    total_tep = sum(r.tep_allocated_bytes for r in runs)
    total_non_tep = sum(r.non_tep_allocated_bytes for r in runs)
    largest = sorted(runs, key=lambda r: r.run_allocated_bytes, reverse=True)[:5]

    lines = [
        "# VAP 13-Run Storage Footprint",
        "",
        f"Generated UTC: `{context['generated_utc']}`",
        f"VAP repo root: `{context['vap_repo_root']}`",
        "",
        "## Totals",
        "",
        f"- Full run directories: **{human_bytes(total_run)}**",
        f"- TEP directories only: **{human_bytes(total_tep)}**",
        f"- Non-TEP run content: **{human_bytes(total_non_tep)}**",
        "",
        "## Largest runs",
        "",
        "| SRA | Run ID | Depth | Full run | TEP only | Non-TEP | Status |",
        "| --- | --- | --- | ---: | ---: | ---: | --- |",
    ]
    for row in largest:
        lines.append(
            f"| {row.sra} | `{row.run_id}` | {row.depth_category} | {row.run_allocated_human} | "
            f"{row.tep_allocated_human} | {row.non_tep_allocated_human} | {row.status} |"
        )

    lines.extend([
        "",
        "## Depth category summary",
        "",
        "| Depth | Runs | Present | Full run total | TEP total | Non-TEP total |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ])
    for row in depth_summary:
        lines.append(
            f"| {row['depth_category']} | {row['run_count']} | {row['present_run_count']} | "
            f"{row['run_allocated_human']} | {row['tep_allocated_human']} | {row['non_tep_allocated_human']} |"
        )

    lines.extend([
        "",
        "## Notes",
        "",
        "This utility is read-only with respect to VAP and VDB project data. It writes only these operator receipts.",
        "`run_allocated_bytes` uses `du -sB1` and reflects allocated disk usage on MARK.",
        "`run_apparent_bytes` uses `du -sb` and reflects apparent file sizes.",
        "",
    ])
    (out_dir / "vap_13_run_storage_footprint_report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Measure storage footprint for the 13 official VAP runs on MARK.")
    parser.add_argument(
        "--vap-repo-root",
        default=str(Path.cwd()),
        help="VAP repository root. Default: current working directory.",
    )
    parser.add_argument(
        "--output-root",
        default="/root/Desktop",
        help="Directory under which the receipt folder will be written. Default: /root/Desktop.",
    )
    parser.add_argument(
        "--label",
        default=None,
        help="Optional output label. Default: vap_13_run_storage_footprint_<UTC timestamp>.",
    )
    args = parser.parse_args()

    vap_repo_root = Path(args.vap_repo_root).expanduser().resolve()
    output_root = Path(args.output_root).expanduser().resolve()
    label = args.label or f"vap_13_run_storage_footprint_{now_stamp()}"
    out_dir = output_root / label
    out_dir.mkdir(parents=True, exist_ok=False)

    generated_utc = datetime.now(timezone.utc).isoformat()
    disk_total, disk_used, disk_free = shutil.disk_usage(vap_repo_root)
    desktop_total, desktop_used, desktop_free = shutil.disk_usage(output_root)

    runs, top_level = collect_footprints(vap_repo_root)
    depth_summary = summarize_by_depth(runs)

    run_fields = list(asdict(runs[0]).keys()) if runs else []
    write_tsv(out_dir / "vap_13_run_storage_footprint.tsv", (asdict(r) for r in runs), run_fields)

    top_fields = list(asdict(top_level[0]).keys()) if top_level else [
        "sra", "run_id", "depth_category", "child_name", "child_path", "child_type",
        "allocated_bytes", "apparent_bytes", "allocated_human", "apparent_human",
    ]
    write_tsv(out_dir / "vap_13_run_top_level_storage.tsv", (asdict(r) for r in top_level), top_fields)

    depth_fields = [
        "depth_category", "run_count", "present_run_count", "run_allocated_bytes", "run_apparent_bytes",
        "tep_allocated_bytes", "non_tep_allocated_bytes", "run_allocated_human", "run_apparent_human",
        "tep_allocated_human", "non_tep_allocated_human",
    ]
    write_tsv(out_dir / "vap_13_run_storage_by_depth.tsv", depth_summary, depth_fields)

    summary = {
        "generated_utc": generated_utc,
        "vap_repo_root": str(vap_repo_root),
        "output_directory": str(out_dir),
        "run_count": len(runs),
        "present_run_count": sum(1 for r in runs if r.run_exists),
        "missing_run_count": sum(1 for r in runs if not r.run_exists),
        "total_run_allocated_bytes": sum(r.run_allocated_bytes for r in runs),
        "total_run_allocated_human": human_bytes(sum(r.run_allocated_bytes for r in runs)),
        "total_run_apparent_bytes": sum(r.run_apparent_bytes for r in runs),
        "total_run_apparent_human": human_bytes(sum(r.run_apparent_bytes for r in runs)),
        "total_tep_allocated_bytes": sum(r.tep_allocated_bytes for r in runs),
        "total_tep_allocated_human": human_bytes(sum(r.tep_allocated_bytes for r in runs)),
        "total_non_tep_allocated_bytes": sum(r.non_tep_allocated_bytes for r in runs),
        "total_non_tep_allocated_human": human_bytes(sum(r.non_tep_allocated_bytes for r in runs)),
        "vap_repo_filesystem_total_bytes": disk_total,
        "vap_repo_filesystem_used_bytes": disk_used,
        "vap_repo_filesystem_free_bytes": disk_free,
        "vap_repo_filesystem_free_human": human_bytes(disk_free),
        "output_filesystem_total_bytes": desktop_total,
        "output_filesystem_used_bytes": desktop_used,
        "output_filesystem_free_bytes": desktop_free,
        "output_filesystem_free_human": human_bytes(desktop_free),
        "depth_summary": depth_summary,
        "manifest": [
            {"sra": sra, "run_id": run_id, "depth_category": depth}
            for sra, run_id, depth in MANIFEST
        ],
    }
    (out_dir / "vap_13_run_storage_footprint_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    write_report(
        out_dir,
        runs,
        depth_summary,
        {
            "generated_utc": generated_utc,
            "vap_repo_root": str(vap_repo_root),
        },
    )

    print_console_report(runs, depth_summary, out_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
