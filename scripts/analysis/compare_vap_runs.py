#!/usr/bin/env python3
"""
compare_vap_runs.py

Lightweight structural/telemetry comparator for two VAP run directories.

Purpose:
- Compare two completed VAP runs without transferring heavy artifacts.
- Emphasize biological-result-layer reproducibility over byte-level identity.
- Report stable vs operationally variable fields.
- Remain portable across sys76 and MARK.

Intended use:
    python scripts/analysis/compare_vap_runs.py \
        --run-a results/run_2026_05_14_083044 \
        --run-b results/run_2026_05_14_231247 \
        --label-a ERR10619281_pre_patch \
        --label-b ERR10619281_post_patch \
        --out /root/Desktop/vap_compare_ERR10619281.md

Notes:
- This script intentionally does NOT hash BAM/SAM/VCF or huge TSV files.
- Large files are summarized using file size and line count.
- Small JSON/MD artifacts are hashed, but hash differences are interpreted carefully.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import platform
import socket
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple


LARGE_FILE_HASH_LIMIT_BYTES = 25_000_000


KEY_RUNTIME_STAGES = [
    "stage_02_align_data",
    "stage_05_call_variants",
    "stage_07_annotate_variants",
    "stage_11_prioritize_variants",
    "stage_12_validate_variants",
]


EXPECTED_FILES = {
    "pipeline_log": "logs/pipeline.log",
    "runtime_profile": "metadata/runtime_profile.tsv",
    "run_metadata": "metadata/run_metadata.json",
    "run_fingerprint": "metadata/run_fingerprint.json",
    "stage_11_summary": "processed/stage_11_summary.json",
    "stage_12_summary": "processed/stage_12_summary.json",
    "stage_13_final_summary": "processed/stage_13_final_summary.json",
    "stage_13_run_report": "processed/stage_13_run_report.md",
    "stage_11_prioritized_variants": "processed/stage_11_prioritized_variants.tsv",
    "stage_11_gene_variant_counts": "processed/stage_11_gene_variant_counts.tsv",
    "stage_12_validation_candidates": "processed/stage_12_validation_candidates.tsv",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def safe_read_json(path: Path) -> Optional[Dict[str, Any]]:
    try:
        return json.loads(path.read_text())
    except FileNotFoundError:
        return None
    except Exception as exc:
        return {"_error": f"Could not read JSON: {exc}"}


def sha256_file(path: Path, max_bytes: Optional[int] = None) -> str:
    try:
        size = path.stat().st_size
    except FileNotFoundError:
        return "MISSING"
    if max_bytes is not None and size > max_bytes:
        return "SKIPPED_large_file"
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def line_count(path: Path) -> Optional[int]:
    try:
        with path.open("rb") as handle:
            return sum(1 for _ in handle)
    except FileNotFoundError:
        return None


def file_summary(path: Path, allow_hash: bool = False) -> Dict[str, Any]:
    if not path.exists():
        return {"exists": False, "size_bytes": None, "line_count": None, "sha256": "MISSING"}
    size = path.stat().st_size
    return {
        "exists": True,
        "size_bytes": size,
        "line_count": line_count(path),
        "sha256": sha256_file(path, LARGE_FILE_HASH_LIMIT_BYTES if not allow_hash else None),
    }


def parse_runtime_profile(path: Path) -> Dict[str, Dict[str, Any]]:
    if not path.exists():
        return {}
    rows: Dict[str, Dict[str, Any]] = {}
    with path.open(newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        for row in reader:
            stage = row.get("stage")
            if not stage:
                continue
            try:
                elapsed = float(row.get("elapsed_seconds", "nan"))
            except ValueError:
                elapsed = None
            rows[stage] = {
                "status": row.get("status"),
                "start_time": row.get("start_time"),
                "end_time": row.get("end_time"),
                "elapsed_seconds": elapsed,
            }
    return rows


def extract_log_metrics(path: Path) -> Dict[str, Any]:
    metrics: Dict[str, Any] = {
        "run_id": None,
        "fastq_r1_reads": None,
        "fastq_r2_reads": None,
        "stage_11_input_rows": None,
        "stage_11_output_rows": None,
        "stage_11_malformed_rows": None,
        "stage_12_input_rows": None,
        "stage_12_output_rows": None,
        "stage_12_unrecognized_priority_rows": None,
        "pipeline_finished": False,
    }
    if not path.exists():
        return metrics
    for line in path.read_text(errors="replace").splitlines():
        if "Run ID:" in line and metrics["run_id"] is None:
            metrics["run_id"] = line.split("Run ID:", 1)[1].strip()
        elif "FASTQ R1 reads detected:" in line:
            metrics["fastq_r1_reads"] = _last_int(line)
        elif "FASTQ R2 reads detected:" in line:
            metrics["fastq_r2_reads"] = _last_int(line)
        elif "Stage 11 input rows processed:" in line:
            metrics["stage_11_input_rows"] = _last_int(line)
        elif "Stage 11 output rows written:" in line:
            metrics["stage_11_output_rows"] = _last_int(line)
        elif "Stage 11 malformed/unassigned rows:" in line:
            metrics["stage_11_malformed_rows"] = _last_int(line)
        elif "Stage 12 input rows processed:" in line:
            metrics["stage_12_input_rows"] = _last_int(line)
        elif "Stage 12 output rows written:" in line:
            metrics["stage_12_output_rows"] = _last_int(line)
        elif "Stage 12 unrecognized priority rows:" in line:
            metrics["stage_12_unrecognized_priority_rows"] = _last_int(line)
        elif "Pipeline run finished." in line:
            metrics["pipeline_finished"] = True
    return metrics


def _last_int(text: str) -> Optional[int]:
    tokens = text.replace(",", "").split()
    for token in reversed(tokens):
        try:
            return int(token)
        except ValueError:
            continue
    return None


def nested_get(data: Optional[Dict[str, Any]], path: Iterable[str]) -> Any:
    cur: Any = data
    for key in path:
        if not isinstance(cur, dict):
            return None
        cur = cur.get(key)
    return cur


def compare_value(a: Any, b: Any) -> str:
    return "MATCH" if a == b else "DIFF"


def md_table(headers: List[str], rows: List[List[Any]]) -> str:
    out = []
    out.append("| " + " | ".join(headers) + " |")
    out.append("|" + "|".join(["---"] * len(headers)) + "|")
    for row in rows:
        out.append("| " + " | ".join("" if x is None else str(x) for x in row) + " |")
    return "\n".join(out)


def summarize_run(run_dir: Path) -> Dict[str, Any]:
    paths = {name: run_dir / rel for name, rel in EXPECTED_FILES.items()}
    log_metrics = extract_log_metrics(paths["pipeline_log"])
    runtime = parse_runtime_profile(paths["runtime_profile"])
    run_metadata = safe_read_json(paths["run_metadata"])
    run_fingerprint = safe_read_json(paths["run_fingerprint"])
    stage11 = safe_read_json(paths["stage_11_summary"])
    stage12 = safe_read_json(paths["stage_12_summary"])
    stage13 = safe_read_json(paths["stage_13_final_summary"])
    file_summaries = {}
    for name, path in paths.items():
        allow_hash = name in {
            "run_metadata",
            "run_fingerprint",
            "stage_11_summary",
            "stage_12_summary",
            "stage_13_final_summary",
            "stage_13_run_report",
            "runtime_profile",
        }
        file_summaries[name] = file_summary(path, allow_hash=allow_hash)
    return {
        "run_dir": str(run_dir),
        "paths": {k: str(v) for k, v in paths.items()},
        "log_metrics": log_metrics,
        "runtime_profile": runtime,
        "run_metadata": run_metadata,
        "run_fingerprint": run_fingerprint,
        "stage_11_summary": stage11,
        "stage_12_summary": stage12,
        "stage_13_final_summary": stage13,
        "file_summaries": file_summaries,
    }


def build_report(run_a: Dict[str, Any], run_b: Dict[str, Any], label_a: str, label_b: str) -> str:
    lines: List[str] = []
    lines.append("# VAP Run Comparison Report")
    lines.append("")
    lines.append(f"Generated UTC: `{utc_now()}`")
    lines.append(f"Host: `{socket.gethostname()}`")
    lines.append(f"Platform: `{platform.platform()}`")
    lines.append("")
    lines.append("## Compared Runs")
    lines.append("")
    lines.append(md_table(
        ["Label", "Run Directory", "Run ID"],
        [
            [label_a, run_a["run_dir"], run_a["log_metrics"].get("run_id")],
            [label_b, run_b["run_dir"], run_b["log_metrics"].get("run_id")],
        ],
    ))
    lines.append("")
    lines.append("## Existence Check")
    lines.append("")
    existence_rows = []
    for key in EXPECTED_FILES:
        a = run_a["file_summaries"][key]["exists"]
        b = run_b["file_summaries"][key]["exists"]
        existence_rows.append([key, a, b, compare_value(a, b)])
    lines.append(md_table(["Artifact", label_a, label_b, "Comparison"], existence_rows))
    lines.append("")
    lines.append("## Log-Derived Biological/Structural Metrics")
    lines.append("")
    metric_keys = [
        "fastq_r1_reads",
        "fastq_r2_reads",
        "stage_11_input_rows",
        "stage_11_output_rows",
        "stage_11_malformed_rows",
        "stage_12_input_rows",
        "stage_12_output_rows",
        "stage_12_unrecognized_priority_rows",
        "pipeline_finished",
    ]
    rows = []
    for key in metric_keys:
        a = run_a["log_metrics"].get(key)
        b = run_b["log_metrics"].get(key)
        rows.append([key, a, b, compare_value(a, b)])
    lines.append(md_table(["Metric", label_a, label_b, "Comparison"], rows))
    lines.append("")
    lines.append("## Runtime Profile Comparison")
    lines.append("")
    runtime_rows = []
    all_stages = sorted(set(run_a["runtime_profile"]) | set(run_b["runtime_profile"]))
    for stage in all_stages:
        a = run_a["runtime_profile"].get(stage, {}).get("elapsed_seconds")
        b = run_b["runtime_profile"].get(stage, {}).get("elapsed_seconds")
        delta = None if a is None or b is None else round(float(b) - float(a), 3)
        runtime_rows.append([stage, a, b, delta])
    lines.append(md_table(["Stage", f"{label_a} seconds", f"{label_b} seconds", "Delta B-A seconds"], runtime_rows))
    lines.append("")
    lines.append("## Key Runtime Stages")
    lines.append("")
    key_rows = []
    for stage in KEY_RUNTIME_STAGES:
        a = run_a["runtime_profile"].get(stage, {}).get("elapsed_seconds")
        b = run_b["runtime_profile"].get(stage, {}).get("elapsed_seconds")
        delta = None if a is None or b is None else round(float(b) - float(a), 3)
        pct = None
        if a not in (None, 0) and b is not None:
            pct = round((float(b) - float(a)) / float(a) * 100, 2)
        key_rows.append([stage, a, b, delta, pct])
    lines.append(md_table(["Stage", f"{label_a}s", f"{label_b}s", "Delta seconds", "Delta %"], key_rows))
    lines.append("")
    lines.append("## Stage 11/12 Distribution Checks")
    lines.append("")
    distribution_paths = [
        ("stage11.counts_by_priority_rank", ["stage_11_summary"], ["counts_by_priority_rank"]),
        ("stage11.counts_by_priority_tier", ["stage_11_summary"], ["counts_by_priority_tier"]),
        ("stage11.counts_by_source_interpretation_label", ["stage_11_summary"], ["counts_by_source_interpretation_label"]),
        ("stage12.counts_by_priority_tier", ["stage_12_summary"], ["counts_by_priority_tier"]),
        ("stage12.counts_by_suggested_validation_method", ["stage_12_summary"], ["counts_by_suggested_validation_method"]),
        ("stage12.counts_by_validation_priority", ["stage_12_summary"], ["counts_by_validation_priority"]),
        ("stage12.counts_by_validation_required", ["stage_12_summary"], ["counts_by_validation_required"]),
        ("stage13.counts_by_variant_origin", ["stage_13_final_summary"], ["counts_by_variant_origin"]),
    ]
    dist_rows = []
    for name, root_path, value_path in distribution_paths:
        a_root = run_a[root_path[0]]
        b_root = run_b[root_path[0]]
        a_val = nested_get(a_root, value_path)
        b_val = nested_get(b_root, value_path)
        dist_rows.append([name, compare_value(a_val, b_val)])
    lines.append(md_table(["Distribution", "Comparison"], dist_rows))
    lines.append("")
    lines.append("## File Size and Line Count Checks")
    lines.append("")
    file_rows = []
    for key in [
        "stage_11_prioritized_variants",
        "stage_11_gene_variant_counts",
        "stage_12_validation_candidates",
        "stage_13_final_summary",
        "stage_13_run_report",
    ]:
        a = run_a["file_summaries"][key]
        b = run_b["file_summaries"][key]
        file_rows.append([
            key,
            a["size_bytes"],
            b["size_bytes"],
            compare_value(a["size_bytes"], b["size_bytes"]),
            a["line_count"],
            b["line_count"],
            compare_value(a["line_count"], b["line_count"]),
        ])
    lines.append(md_table(["Artifact", f"{label_a} bytes", f"{label_b} bytes", "Byte-size comparison", f"{label_a} lines", f"{label_b} lines", "Line comparison"], file_rows))
    lines.append("")
    lines.append("## Small Artifact Hash Checks")
    lines.append("")
    hash_rows = []
    for key in [
        "runtime_profile",
        "run_metadata",
        "run_fingerprint",
        "stage_11_summary",
        "stage_12_summary",
        "stage_13_final_summary",
        "stage_13_run_report",
    ]:
        a = run_a["file_summaries"][key]["sha256"]
        b = run_b["file_summaries"][key]["sha256"]
        hash_rows.append([key, a, b, compare_value(a, b)])
    lines.append(md_table(["Artifact", f"{label_a} sha256", f"{label_b} sha256", "Comparison"], hash_rows))
    lines.append("")
    lines.append("## Provenance Field Comparison")
    lines.append("")
    provenance_rows = []
    provenance_checks = [
        ("run_metadata.run.status", "run_metadata", ["run", "status"]),
        ("run_metadata.run.pipeline_version", "run_metadata", ["run", "pipeline_version"]),
        ("run_metadata.summary.stage_count", "run_metadata", ["summary", "stage_count"]),
        ("run_metadata.summary.warning_count", "run_metadata", ["summary", "warning_count"]),
        ("run_fingerprint.git_commit", "run_fingerprint", ["git_commit"]),
        ("run_fingerprint.config_hash", "run_fingerprint", ["config_hash"]),
        ("run_fingerprint.reference_genome", "run_fingerprint", ["reference_genome"]),
        ("run_fingerprint.reference_fasta_hash_or_size", "run_fingerprint", ["reference_fasta_hash_or_size"]),
        ("run_fingerprint.hostname", "run_fingerprint", ["hostname"]),
        ("run_fingerprint.execution_profile", "run_fingerprint", ["execution_profile"]),
    ]
    for label, root, path in provenance_checks:
        a = nested_get(run_a[root], path)
        b = nested_get(run_b[root], path)
        provenance_rows.append([label, a, b, compare_value(a, b)])
    lines.append(md_table(["Field", label_a, label_b, "Comparison"], provenance_rows))
    lines.append("")
    lines.append("## Interpretation Guide")
    lines.append("")
    lines.append("Expected stable fields include FASTQ counts, Stage 11/12 row counts, key biological distributions, large output file sizes, and line counts.")
    lines.append("")
    lines.append("Expected operationally variable fields include run IDs, timestamps, runtime profiles, config hashes after intentional config edits, git commits after code changes, and small JSON/Markdown hashes containing run-specific paths or timestamps.")
    lines.append("")
    lines.append("A small-artifact hash difference does not automatically indicate biological-result instability.")
    lines.append("")
    lines.append("## Preliminary Classification")
    lines.append("")
    stable_metrics = [
        run_a["log_metrics"].get("fastq_r1_reads") == run_b["log_metrics"].get("fastq_r1_reads"),
        run_a["log_metrics"].get("fastq_r2_reads") == run_b["log_metrics"].get("fastq_r2_reads"),
        run_a["log_metrics"].get("stage_11_output_rows") == run_b["log_metrics"].get("stage_11_output_rows"),
        run_a["log_metrics"].get("stage_12_output_rows") == run_b["log_metrics"].get("stage_12_output_rows"),
        nested_get(run_a["stage_11_summary"], ["counts_by_priority_tier"]) == nested_get(run_b["stage_11_summary"], ["counts_by_priority_tier"]),
        nested_get(run_a["stage_12_summary"], ["counts_by_validation_required"]) == nested_get(run_b["stage_12_summary"], ["counts_by_validation_required"]),
    ]
    if all(stable_metrics):
        classification = "STRUCTURALLY_AND_BIOLOGICALLY_STABLE"
    else:
        classification = "REVIEW_REQUIRED"
    lines.append(f"`{classification}`")
    lines.append("")
    return "\n".join(lines)


def write_json_summary(path: Path, report_data: Dict[str, Any]) -> None:
    path.write_text(json.dumps(report_data, indent=2, sort_keys=True) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Compare two VAP run directories using lightweight structural telemetry.")
    parser.add_argument("--run-a", required=True, help="First VAP run directory")
    parser.add_argument("--run-b", required=True, help="Second VAP run directory")
    parser.add_argument("--label-a", default="run_a", help="Label for first run")
    parser.add_argument("--label-b", default="run_b", help="Label for second run")
    parser.add_argument("--out", required=True, help="Markdown report output path")
    parser.add_argument("--json-out", default=None, help="Optional machine-readable JSON summary output path")
    args = parser.parse_args()

    run_a_dir = Path(args.run_a)
    run_b_dir = Path(args.run_b)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)

    run_a = summarize_run(run_a_dir)
    run_b = summarize_run(run_b_dir)
    report = build_report(run_a, run_b, args.label_a, args.label_b)
    out.write_text(report + "\n")

    if args.json_out:
        json_out = Path(args.json_out)
        json_out.parent.mkdir(parents=True, exist_ok=True)
        write_json_summary(json_out, {
            "generated_utc": utc_now(),
            "label_a": args.label_a,
            "label_b": args.label_b,
            "run_a": run_a,
            "run_b": run_b,
        })

    print(f"Wrote comparison report: {out}")
    if args.json_out:
        print(f"Wrote JSON summary: {args.json_out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
