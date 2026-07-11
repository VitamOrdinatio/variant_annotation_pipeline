#!/usr/bin/env python3
"""
Canonical VAP genotype evidence surveillance probe.

Run from the VAP repository root on MARK:

    python development_history/exploratory_scripts/evidence_harvest/probe_canonical_vap_genotype_evidence_surveillance.py

This script is read-only with respect to results/.
It writes all outputs under /root/Desktop/ and creates a .tgz bundle.

Purpose:
    Determine whether caller-emitted genotype evidence is available in:
      1. retained VCF / VCF.GZ artifacts,
      2. run-level TSV outputs,
      3. existing TEP-VAP packaged TSVs,
      4. TEP entity inventories / lineage manifests.

This is a surveillance probe, not a patch script.
It does not modify any VAP run output or TEP package.
"""

from __future__ import annotations

import csv
import gzip
import hashlib
import json
import re
import tarfile
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Optional


@dataclass(frozen=True)
class CanonicalRun:
    sra: str
    run_id: str
    depth_category: str
    tep_sample_id: str


RUNS: list[CanonicalRun] = [
    CanonicalRun("ERR10619203", "run_2026_05_30_071639", "q3", "ERR10619203"),
    CanonicalRun("ERR10619207", "run_2026_06_01_124134", "q3", "ERR10619207"),
    CanonicalRun("ERR10619208", "run_2026_05_30_151355", "median", "ERR10619208"),
    CanonicalRun("ERR10619212", "run_2026_05_30_214724", "q1", "ERR10619212"),
    CanonicalRun("ERR10619225", "run_2026_05_31_091242", "q3", "ERR10619225"),
    CanonicalRun("ERR10619230", "run_2026_06_01_004903", "q3", "ERR10619230"),
    CanonicalRun("ERR10619241", "run_2026_06_02_052302", "q1", "ERR10619241"),
    CanonicalRun("ERR10619281", "run_2026_05_27_233524", "median", "ERR10619281"),
    CanonicalRun("ERR10619285", "run_2026_06_02_124300", "median", "ERR10619285"),
    CanonicalRun("ERR10619300", "run_2026_05_27_172531", "median", "ERR10619300"),
    CanonicalRun("ERR10619309", "run_2026_06_02_181024", "q1", "ERR10619309"),
    CanonicalRun("ERR10619330", "run_2026_06_01_203130", "q1", "ERR10619330"),
    CanonicalRun("SRR12898354", "run_2026_06_03_010030", "hg002", "HG002"),
]

GENOTYPE_HEADER_PATTERN = re.compile(
    r"(^|\t)(GT|AD|DP|GQ|PL|FT)(\t|$)|genotype|zygosity|gt_raw|sample_format|format_keys|allele_depth|phase_state",
    re.IGNORECASE,
)

MANIFEST_PATTERN = re.compile(
    r"genotype|zygosity|gt_raw|sample_format|format_keys|allele_depth|caller_emitted|phase_state",
    re.IGNORECASE,
)

VCF_EXTENSIONS = (".vcf", ".vcf.gz", ".g.vcf", ".g.vcf.gz")


def local_timestamp() -> str:
    return datetime.now().strftime("%Y_%m_%d_%H%M%S")


def run_dir(run: CanonicalRun) -> Path:
    return Path("results") / run.run_id


def tep_id(run: CanonicalRun) -> str:
    return f"vap_tep_{run.tep_sample_id}_{run.run_id}_v1"


def tep_dir(run: CanonicalRun) -> Path:
    return run_dir(run) / "tep" / tep_id(run)


def is_vcf(path: Path) -> bool:
    return path.name.lower().endswith(VCF_EXTENSIONS)


def open_text_maybe_gzip(path: Path):
    if path.name.lower().endswith(".gz"):
        return gzip.open(path, "rt", encoding="utf-8", errors="replace")
    return path.open("r", encoding="utf-8", errors="replace")


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while True:
            chunk = handle.read(chunk_size)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def write_tsv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: "" if row.get(field) is None else row.get(field) for field in fieldnames})


def write_json(path: Path, payload: Any) -> None:
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
        handle.write("\n")


def find_vcfs_for_run(run: CanonicalRun) -> list[Path]:
    root = run_dir(run)
    if not root.exists():
        return []
    return sorted(path for path in root.rglob("*") if path.is_file() and is_vcf(path))


def parse_vcf_header(path: Path) -> dict[str, Any]:
    result: dict[str, Any] = {
        "vcf_path": str(path),
        "vcf_exists": path.exists(),
        "vcf_size_bytes": path.stat().st_size if path.exists() else None,
        "vcf_sha256": sha256_file(path) if path.exists() else "",
        "header_found": False,
        "header_column_count": None,
        "has_format_column": False,
        "sample_column_count": 0,
        "sample_columns": "",
        "single_sample_vcf": False,
        "format_column_index": None,
        "first_variant_line_number": None,
        "first_variant_format": "",
        "first_variant_sample_raw": "",
        "first_variant_gt_raw": "",
        "first_variant_has_gt": False,
        "first_variant_has_ad": False,
        "first_variant_has_dp": False,
        "first_variant_has_gq": False,
        "first_variant_has_pl": False,
        "variant_line_probe_count": 0,
        "variant_lines_with_format": 0,
        "variant_lines_with_gt": 0,
        "variant_lines_with_sample_value": 0,
        "can_extract_genotype": False,
        "status": "not_inspected",
        "error": "",
    }

    if not path.exists():
        result["status"] = "missing"
        return result

    try:
        header_cols: list[str] | None = None
        sample_col_indices: list[int] = []
        format_idx: Optional[int] = None
        variant_probe_limit = 1000

        with open_text_maybe_gzip(path) as handle:
            for line_number, line in enumerate(handle, start=1):
                line = line.rstrip("\n\r")
                if line.startswith("##"):
                    continue

                if line.startswith("#CHROM"):
                    header_cols = line.split("\t")
                    result["header_found"] = True
                    result["header_column_count"] = len(header_cols)

                    if "FORMAT" in header_cols:
                        format_idx = header_cols.index("FORMAT")
                        result["format_column_index"] = format_idx
                        result["has_format_column"] = True
                        sample_col_indices = list(range(format_idx + 1, len(header_cols)))
                        result["sample_column_count"] = len(sample_col_indices)
                        result["sample_columns"] = ",".join(header_cols[i] for i in sample_col_indices)
                        result["single_sample_vcf"] = len(sample_col_indices) == 1
                    continue

                if not line or line.startswith("#"):
                    continue

                if result["first_variant_line_number"] is None:
                    result["first_variant_line_number"] = line_number

                if header_cols is None or format_idx is None:
                    continue

                parts = line.split("\t")
                if len(parts) <= format_idx:
                    continue

                result["variant_line_probe_count"] += 1
                fmt = parts[format_idx]
                if fmt:
                    result["variant_lines_with_format"] += 1

                sample_raw = ""
                if sample_col_indices and len(parts) > sample_col_indices[0]:
                    sample_raw = parts[sample_col_indices[0]]
                    if sample_raw:
                        result["variant_lines_with_sample_value"] += 1

                format_keys = fmt.split(":") if fmt else []
                sample_values = sample_raw.split(":") if sample_raw else []
                format_map = {
                    key: sample_values[idx] if idx < len(sample_values) else ""
                    for idx, key in enumerate(format_keys)
                }

                if "GT" in format_map and format_map["GT"]:
                    result["variant_lines_with_gt"] += 1

                if not result["first_variant_format"]:
                    result["first_variant_format"] = fmt
                    result["first_variant_sample_raw"] = sample_raw
                    result["first_variant_gt_raw"] = format_map.get("GT", "")
                    result["first_variant_has_gt"] = bool(format_map.get("GT", ""))
                    result["first_variant_has_ad"] = "AD" in format_map
                    result["first_variant_has_dp"] = "DP" in format_map
                    result["first_variant_has_gq"] = "GQ" in format_map
                    result["first_variant_has_pl"] = "PL" in format_map

                if result["variant_line_probe_count"] >= variant_probe_limit:
                    break

        result["can_extract_genotype"] = (
            result["header_found"]
            and result["has_format_column"]
            and result["sample_column_count"] >= 1
            and result["variant_lines_with_gt"] > 0
        )
        result["status"] = "pass" if result["can_extract_genotype"] else "review"

    except Exception as exc:
        result["status"] = "error"
        result["error"] = repr(exc)

    return result


def read_tsv_header(path: Path) -> list[str]:
    try:
        with path.open("r", encoding="utf-8", errors="replace") as handle:
            line = handle.readline().rstrip("\n\r")
        return line.split("\t") if line else []
    except Exception:
        return []


def scan_tsv_headers(root: Path, scope: str, run: CanonicalRun) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if not root.exists():
        return rows

    for path in sorted(root.rglob("*.tsv")):
        if not path.is_file():
            continue
        header = read_tsv_header(path)
        header_text = "\t".join(header)
        hits = [col for col in header if GENOTYPE_HEADER_PATTERN.search(col)]
        raw_header_hit = bool(GENOTYPE_HEADER_PATTERN.search(header_text))
        rows.append(
            {
                "sra": run.sra,
                "run_id": run.run_id,
                "depth_category": run.depth_category,
                "scope": scope,
                "file_path": str(path),
                "file_size_bytes": path.stat().st_size if path.exists() else None,
                "column_count": len(header),
                "genotype_header_hit": bool(hits) or raw_header_hit,
                "hit_columns": ",".join(hits),
                "header_preview": "\t".join(header[:30]),
            }
        )

    return rows


def grep_manifest_file(path: Path, run: CanonicalRun, manifest_type: str) -> dict[str, Any]:
    result = {
        "sra": run.sra,
        "run_id": run.run_id,
        "depth_category": run.depth_category,
        "manifest_type": manifest_type,
        "file_path": str(path),
        "exists": path.exists(),
        "hit_count": 0,
        "hit_terms": "",
        "matched_lines_preview": "",
        "status": "missing",
    }
    if not path.exists():
        return result

    try:
        text = path.read_text(encoding="utf-8", errors="replace")
        hits = MANIFEST_PATTERN.findall(text)
        terms = sorted(set(h.lower() for h in hits))
        matched_lines = [line.strip() for line in text.splitlines() if MANIFEST_PATTERN.search(line)][:20]
        result.update(
            {
                "hit_count": len(hits),
                "hit_terms": ",".join(terms),
                "matched_lines_preview": " || ".join(matched_lines),
                "status": "hit" if hits else "no_hit",
            }
        )
    except Exception as exc:
        result["status"] = "error"
        result["matched_lines_preview"] = repr(exc)

    return result


def scan_tep_manifests(run: CanonicalRun) -> list[dict[str, Any]]:
    tdir = tep_dir(run)
    return [
        grep_manifest_file(tdir / "entity_inventory.json", run, "entity_inventory"),
        grep_manifest_file(tdir / "lineage_manifest.json", run, "lineage_manifest"),
        grep_manifest_file(tdir / "validation_report.md", run, "validation_report"),
    ]


def summarize_run(
    run: CanonicalRun,
    vcf_rows: list[dict[str, Any]],
    run_tsv_rows: list[dict[str, Any]],
    tep_tsv_rows: list[dict[str, Any]],
    manifest_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    run_vcfs = [row for row in vcf_rows if row["run_id"] == run.run_id]
    run_tsvs = [row for row in run_tsv_rows if row["run_id"] == run.run_id]
    tep_tsvs = [row for row in tep_tsv_rows if row["run_id"] == run.run_id]
    manifests = [row for row in manifest_rows if row["run_id"] == run.run_id]

    extractable_vcfs = [row for row in run_vcfs if row.get("can_extract_genotype") is True]
    genotype_run_tsvs = [row for row in run_tsvs if row.get("genotype_header_hit") is True]
    genotype_tep_tsvs = [row for row in tep_tsvs if row.get("genotype_header_hit") is True]
    genotype_manifests = [row for row in manifests if int(row.get("hit_count", 0) or 0) > 0]

    likely_in_vcfs = bool(extractable_vcfs)
    likely_in_run_tsvs = bool(genotype_run_tsvs)
    likely_in_teps = bool(genotype_tep_tsvs or genotype_manifests)

    if likely_in_teps:
        conclusion = "genotype_evidence_may_already_be_tep_packaged"
    elif likely_in_vcfs:
        conclusion = "genotype_evidence_available_in_vcf_not_detected_in_tep"
    elif run_vcfs:
        conclusion = "vcf_present_but_genotype_extractability_requires_review"
    else:
        conclusion = "no_retained_vcf_detected"

    return {
        "sra": run.sra,
        "run_id": run.run_id,
        "depth_category": run.depth_category,
        "tep_sample_id": run.tep_sample_id,
        "run_dir_exists": run_dir(run).exists(),
        "tep_dir_exists": tep_dir(run).exists(),
        "tep_dir": str(tep_dir(run)),
        "vcf_count": len(run_vcfs),
        "extractable_vcf_count": len(extractable_vcfs),
        "best_vcf_path": extractable_vcfs[0]["vcf_path"] if extractable_vcfs else (run_vcfs[0]["vcf_path"] if run_vcfs else ""),
        "run_tsv_count": len(run_tsvs),
        "run_tsv_genotype_header_hit_count": len(genotype_run_tsvs),
        "tep_tsv_count": len(tep_tsvs),
        "tep_tsv_genotype_header_hit_count": len(genotype_tep_tsvs),
        "tep_manifest_genotype_hit_count": len(genotype_manifests),
        "likely_genotype_in_vcfs": likely_in_vcfs,
        "likely_genotype_in_run_tsvs": likely_in_run_tsvs,
        "likely_genotype_in_teps": likely_in_teps,
        "surveillance_conclusion": conclusion,
    }


def write_markdown_summary(out_dir: Path, summary_rows: list[dict[str, Any]]) -> None:
    lines = [
        "# Canonical VAP Genotype Evidence Surveillance Summary",
        "",
        "This MARK probe surveyed the 13 canonical VAP runs for genotype evidence in retained VCFs, run TSVs, and existing TEP-VAP packages.",
        "",
        "This is surveillance only. No run outputs or TEP packages were modified.",
        "",
        "## High-Level Results",
        "",
    ]

    total = len(summary_rows)
    vcfs = sum(1 for row in summary_rows if row["likely_genotype_in_vcfs"])
    teps = sum(1 for row in summary_rows if row["likely_genotype_in_teps"])
    no_vcf = sum(1 for row in summary_rows if row["surveillance_conclusion"] == "no_retained_vcf_detected")

    lines.extend(
        [
            f"- Canonical runs surveyed: `{total}`",
            f"- Runs with extractable genotype evidence in retained VCFs: `{vcfs}`",
            f"- Runs with genotype-like evidence detected in existing TEPs: `{teps}`",
            f"- Runs with no retained VCF detected: `{no_vcf}`",
            "",
            "## Per-Run Conclusion",
            "",
            "| SRA | Run ID | Depth | VCF genotype? | TEP genotype? | Conclusion |",
            "|---|---|---|---:|---:|---|",
        ]
    )

    for row in summary_rows:
        lines.append(
            f"| {row['sra']} | {row['run_id']} | {row['depth_category']} | "
            f"{row['likely_genotype_in_vcfs']} | {row['likely_genotype_in_teps']} | "
            f"{row['surveillance_conclusion']} |"
        )

    (out_dir / "canonical_vap_genotype_surveillance_summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def create_tgz(out_dir: Path) -> Path:
    tgz_path = out_dir.with_suffix(".tgz")
    with tarfile.open(tgz_path, "w:gz") as tar:
        tar.add(out_dir, arcname=out_dir.name)
    return tgz_path


def main() -> int:
    root = Path.cwd().resolve()
    if not (root / "results").exists():
        raise FileNotFoundError("Run this script from the VAP repository root; results/ not found.")

    out_dir = Path("/root/Desktop") / f"canonical_vap_genotype_evidence_surveillance_{local_timestamp()}"
    out_dir.mkdir(parents=True, exist_ok=False)

    vcf_rows: list[dict[str, Any]] = []
    run_tsv_rows: list[dict[str, Any]] = []
    tep_tsv_rows: list[dict[str, Any]] = []
    manifest_rows: list[dict[str, Any]] = []

    print(f"[INFO] Repo root: {root}")
    print(f"[INFO] Output directory: {out_dir}")
    print("[INFO] Starting canonical genotype evidence surveillance...")

    for idx, run in enumerate(RUNS, start=1):
        print(f"[INFO] [{idx}/{len(RUNS)}] Surveying {run.sra} / {run.run_id} ({run.depth_category})")

        vcfs = find_vcfs_for_run(run)
        if vcfs:
            for vcf in vcfs:
                row = parse_vcf_header(vcf)
                row.update({"sra": run.sra, "run_id": run.run_id, "depth_category": run.depth_category, "tep_sample_id": run.tep_sample_id})
                vcf_rows.append(row)
        else:
            vcf_rows.append(
                {
                    "sra": run.sra,
                    "run_id": run.run_id,
                    "depth_category": run.depth_category,
                    "tep_sample_id": run.tep_sample_id,
                    "vcf_path": "",
                    "vcf_exists": False,
                    "vcf_size_bytes": None,
                    "vcf_sha256": "",
                    "header_found": False,
                    "header_column_count": None,
                    "has_format_column": False,
                    "sample_column_count": 0,
                    "sample_columns": "",
                    "single_sample_vcf": False,
                    "format_column_index": None,
                    "first_variant_line_number": None,
                    "first_variant_format": "",
                    "first_variant_sample_raw": "",
                    "first_variant_gt_raw": "",
                    "first_variant_has_gt": False,
                    "first_variant_has_ad": False,
                    "first_variant_has_dp": False,
                    "first_variant_has_gq": False,
                    "first_variant_has_pl": False,
                    "variant_line_probe_count": 0,
                    "variant_lines_with_format": 0,
                    "variant_lines_with_gt": 0,
                    "variant_lines_with_sample_value": 0,
                    "can_extract_genotype": False,
                    "status": "no_vcf_detected",
                    "error": "",
                }
            )

        rdir = run_dir(run)
        if rdir.exists():
            for scope_root, scope_name in [
                (rdir / "processed", "processed"),
                (rdir / "interim", "interim"),
                (rdir / "metadata", "metadata"),
                (rdir / "final", "final"),
                (rdir / "reports", "reports"),
                (rdir / "validation", "validation"),
            ]:
                run_tsv_rows.extend(scan_tsv_headers(scope_root, scope_name, run))

        tep_tsv_rows.extend(scan_tsv_headers(tep_dir(run) / "entities", "tep_entities", run))
        manifest_rows.extend(scan_tep_manifests(run))

    summary_rows = [
        summarize_run(run, vcf_rows, run_tsv_rows, tep_tsv_rows, manifest_rows)
        for run in RUNS
    ]

    write_tsv(out_dir / "canonical_vap_vcf_genotype_scan.tsv", vcf_rows, [
        "sra","run_id","depth_category","tep_sample_id","vcf_path","vcf_exists","vcf_size_bytes","vcf_sha256",
        "header_found","header_column_count","has_format_column","sample_column_count","sample_columns","single_sample_vcf",
        "format_column_index","first_variant_line_number","first_variant_format","first_variant_sample_raw","first_variant_gt_raw",
        "first_variant_has_gt","first_variant_has_ad","first_variant_has_dp","first_variant_has_gq","first_variant_has_pl",
        "variant_line_probe_count","variant_lines_with_format","variant_lines_with_gt","variant_lines_with_sample_value",
        "can_extract_genotype","status","error"
    ])

    tsv_fields = ["sra","run_id","depth_category","scope","file_path","file_size_bytes","column_count","genotype_header_hit","hit_columns","header_preview"]
    write_tsv(out_dir / "canonical_vap_run_tsv_genotype_header_scan.tsv", run_tsv_rows, tsv_fields)
    write_tsv(out_dir / "canonical_vap_tep_tsv_genotype_header_scan.tsv", tep_tsv_rows, tsv_fields)

    write_tsv(out_dir / "canonical_vap_tep_manifest_genotype_scan.tsv", manifest_rows, [
        "sra","run_id","depth_category","manifest_type","file_path","exists","hit_count","hit_terms","matched_lines_preview","status"
    ])

    summary_fields = [
        "sra","run_id","depth_category","tep_sample_id","run_dir_exists","tep_dir_exists","tep_dir",
        "vcf_count","extractable_vcf_count","best_vcf_path","run_tsv_count","run_tsv_genotype_header_hit_count",
        "tep_tsv_count","tep_tsv_genotype_header_hit_count","tep_manifest_genotype_hit_count",
        "likely_genotype_in_vcfs","likely_genotype_in_run_tsvs","likely_genotype_in_teps","surveillance_conclusion"
    ]
    write_tsv(out_dir / "canonical_vap_genotype_surveillance_summary.tsv", summary_rows, summary_fields)

    write_json(out_dir / "canonical_vap_genotype_surveillance_summary.json", {
        "created_local": datetime.now().isoformat(timespec="seconds"),
        "repo_root": str(root),
        "runs": [asdict(run) for run in RUNS],
        "summary": summary_rows,
    })

    write_markdown_summary(out_dir, summary_rows)
    tgz_path = create_tgz(out_dir)

    print("")
    print("Canonical VAP genotype evidence surveillance complete.")
    print(f"Output directory: {out_dir}")
    print(f"TGZ bundle: {tgz_path}")
    print("")
    print("Summary:")
    for row in summary_rows:
        print(
            f"  {row['sra']} / {row['run_id']}: "
            f"vcf_genotype={row['likely_genotype_in_vcfs']} "
            f"tep_genotype={row['likely_genotype_in_teps']} "
            f"conclusion={row['surveillance_conclusion']}"
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
