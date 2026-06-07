#!/usr/bin/env python3

# Benchmark invocation from VAP repo root:

# python scripts/benchmarking/run_hg002_happy_benchmark.py \
#   --run-dir results/run_2026_05_28_063354 \
#   --truth-vcf /data/storage/reference/...vcf.gz \
#   --truth-bed /data/storage/reference/...bed \
#   --reference-fasta /data/storage/reference/grch38/GRCh38.primary_assembly.genome.fa \
#   --hap-container /data/storage/containers/hap.py_0.3.15--py27hcb73b3d_0.sif


from __future__ import annotations

import argparse
import csv
import gzip
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def fail(message: str) -> None:
    raise RuntimeError(message)


def discover_query_vcf(run_dir: Path, explicit_query_vcf: str | None) -> Path:
    if explicit_query_vcf:
        path = Path(explicit_query_vcf)
        if not path.exists():
            fail(f"Explicit query VCF not found: {path}")
        return path

    interim = run_dir / "interim"
    if not interim.exists():
        fail(f"Run interim directory not found: {interim}")

    candidates = sorted(
        list(interim.glob("*.normalized_variants.vcf")) +
        list(interim.glob("*.normalized_variants.vcf.gz"))
    )    

    if len(candidates) == 0:
        fail(f"No normalized VCF found in: {interim}")

    if len(candidates) > 1:
        joined = "\n".join(str(p) for p in candidates)
        fail(
            "Multiple normalized VCF candidates found. "
            "Provide --query-vcf explicitly.\n"
            f"{joined}"
        )

    return candidates[0]


def require_file(path: Path, label: str) -> Path:
    if not path.exists():
        fail(f"Required {label} not found: {path}")
    if not path.is_file():
        fail(f"Required {label} is not a file: {path}")
    return path


def require_executable(name: str) -> str:
    resolved = shutil.which(name)
    if resolved is None:
        fail(f"Required executable not found on PATH: {name}")
    return resolved


def strip_chr(contig: str) -> str:
    if contig.startswith("chr"):
        return contig[3:]
    return contig


def harmonize_bed_namespace(input_bed: Path, output_bed: Path) -> None:
    output_bed.parent.mkdir(parents=True, exist_ok=True)

    with input_bed.open("r", encoding="utf-8") as src, output_bed.open("w", encoding="utf-8") as dst:
        for line in src:
            if not line.strip() or line.startswith("#"):
                dst.write(line)
                continue

            fields = line.rstrip("\n").split("\t")
            fields[0] = strip_chr(fields[0])
            dst.write("\t".join(fields) + "\n")


def harmonize_vcf_namespace(input_vcf_gz: Path, output_vcf_gz: Path) -> None:
    output_vcf_gz.parent.mkdir(parents=True, exist_ok=True)

    with gzip.open(input_vcf_gz, "rt", encoding="utf-8") as src, gzip.open(output_vcf_gz, "wt", encoding="utf-8") as dst:
        for line in src:
            if line.startswith("##contig=<ID=chr"):
                line = line.replace("##contig=<ID=chr", "##contig=<ID=", 1)
            elif not line.startswith("#"):
                fields = line.rstrip("\n").split("\t")
                fields[0] = strip_chr(fields[0])
                line = "\t".join(fields) + "\n"

            dst.write(line)


def index_vcf_with_tabix(apptainer_exe: str, hap_container: Path, vcf_gz: Path) -> None:
    cmd = [
        apptainer_exe,
        "exec",
        "--bind",
        "/data/storage:/data/storage",
        "--bind",
        f"{vcf_gz.parent}:{vcf_gz.parent}",
        str(hap_container),
        "tabix",
        "-f",
        "-p",
        "vcf",
        str(vcf_gz),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        fail(
            "tabix indexing failed for harmonized truth VCF.\n"
            f"Command: {' '.join(cmd)}\n"
            f"stderr:\n{result.stderr}"
        )


def prepare_namespace_harmonized_giab(
    *,
    truth_vcf: Path,
    truth_bed: Path,
    benchmarking_dir: Path,
    apptainer_exe: str,
    hap_container: Path,
) -> tuple[Path, Path]:
    interoperability_dir = benchmarking_dir / "interoperability"
    harmonized_vcf = interoperability_dir / "HG002_GRCh38_1_22_v4.2.1_benchmark.nochr.vcf.gz"
    harmonized_bed = interoperability_dir / "HG002_GRCh38_1_22_v4.2.1_benchmark.nochr.bed"

    harmonize_vcf_namespace(truth_vcf, harmonized_vcf)
    index_vcf_with_tabix(apptainer_exe, hap_container, harmonized_vcf)
    harmonize_bed_namespace(truth_bed, harmonized_bed)

    manifest = {
        "generated_at": utc_now(),
        "namespace_rule": "deterministically strip leading 'chr' prefix from GIAB truth contigs to match VAP Ensembl-style namespace",
        "original_truth_vcf": str(truth_vcf),
        "original_truth_bed": str(truth_bed),
        "harmonized_truth_vcf": str(harmonized_vcf),
        "harmonized_truth_bed": str(harmonized_bed),
        "canonical_giab_files_mutated": False,
    }

    with (interoperability_dir / "namespace_harmonization_manifest.json").open("w", encoding="utf-8") as handle:
        json.dump(manifest, handle, indent=2, sort_keys=True)

    return harmonized_vcf, harmonized_bed


def validate_hap_container(
    apptainer_exe: str,
    hap_container: Path,
) -> str:
    cmd = [
        apptainer_exe,
        "exec",
        "--bind",
        "/data/storage:/data/storage",
        str(hap_container),
        "hap.py",
        "--version",
    ]

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        check=False,
    )

    if result.returncode != 0:
        fail(
            "Containerized hap.py runtime validation failed.\n"
            f"Command: {' '.join(cmd)}\n"
            f"stderr:\n{result.stderr}"
        )
    version_text = result.stdout.strip() or result.stderr.strip()
    return version_text


def write_log(log_path: Path, lines: list[str]) -> None:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as handle:
        for line in lines:
            handle.write(line.rstrip() + "\n")


def run_happy(
    *,
    apptainer_exe: str,
    hap_container: Path,
    truth_vcf: Path,
    query_vcf: Path,
    truth_bed: Path,
    reference_fasta: Path,
    output_prefix: Path,
    log_path: Path,
) -> None:
    cmd = [
        apptainer_exe,
        "exec",
        "--bind",
        "/data/storage:/data/storage",
        str(hap_container),
        "hap.py",
        str(truth_vcf),
        str(query_vcf),        
        "-f",
        str(truth_bed),
        "-r",
        str(reference_fasta),
        "-o",
        str(output_prefix),
    ]

    write_log(log_path, ["", f"[{utc_now()}] hap.py command:", " ".join(cmd)])

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        check=False,
    )    

    write_log(
        log_path,
        [
            f"[{utc_now()}] hap.py exit_status={result.returncode}",
            "--- hap.py stdout ---",
            result.stdout or "",
            "--- hap.py stderr ---",
            result.stderr or "",
        ],
    )

    if result.returncode != 0:
        fail(f"hap.py failed with exit status {result.returncode}. See {log_path}")


def find_happy_summary(happy_dir: Path) -> Path:
    candidates = sorted(happy_dir.glob("*.summary.csv"))
    if not candidates:
        fail(f"No hap.py summary CSV found in: {happy_dir}")
    if len(candidates) > 1:
        # Usually harmless, but fail to avoid ambiguous parsing.
        joined = "\n".join(str(p) for p in candidates)
        fail(f"Multiple hap.py summary CSV files found:\n{joined}")
    return candidates[0]


def parse_happy_summary(summary_csv: Path) -> list[dict[str, str]]:
    with summary_csv.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def to_float(value: str | None) -> float | None:
    if value in {None, "", "None", "NA", "nan"}:
        return None
    try:
        return float(value)
    except ValueError:
        return None


def metric_from_rows(rows: list[dict[str, str]], type_value: str, filter_value: str = "ALL") -> dict[str, str] | None:
    for row in rows:
        if row.get("Type") == type_value and row.get("Filter") == filter_value:
            return row
    return None


def f1_score(precision: float | None, recall: float | None) -> float | None:
    if precision is None or recall is None:
        return None
    if precision + recall == 0:
        return 0.0
    return 2 * precision * recall / (precision + recall)


def summarize_happy(
    *,
    rows: list[dict[str, str]],
    run_id: str,
    query_vcf: Path,
    truth_vcf: Path,
    truth_bed: Path,
    reference_fasta: Path,
) -> tuple[dict[str, object], list[dict[str, object]]]:
    stratified: list[dict[str, object]] = []

    for variant_type in ["SNP", "INDEL"]:
        row = metric_from_rows(rows, variant_type)
        if row is None:
            continue

        precision = to_float(row.get("METRIC.Precision"))
        recall = to_float(row.get("METRIC.Recall"))

        stratified.append(
            {
                "run_id": run_id,
                "variant_type": variant_type,
                "truth_tp": row.get("TRUTH.TP"),
                "truth_fn": row.get("TRUTH.FN"),
                "query_tp": row.get("QUERY.TP"),
                "query_fp": row.get("QUERY.FP"),
                "precision": precision,
                "recall": recall,
                "f1": f1_score(precision, recall),
            }
        )

    snp = next((r for r in stratified if r["variant_type"] == "SNP"), {})
    indel = next((r for r in stratified if r["variant_type"] == "INDEL"), {})

    # Prefer aggregate ALL row if hap.py emits it; otherwise leave global values null.
    all_row = (
        metric_from_rows(rows, "ALL")
        or metric_from_rows(rows, "Locations")
    )    
    all_precision = to_float(all_row.get("METRIC.Precision")) if all_row else None
    all_recall = to_float(all_row.get("METRIC.Recall")) if all_row else None

    summary = {
        "run_id": run_id,
        "query_vcf": str(query_vcf),
        "truth_vcf": str(truth_vcf),
        "truth_bed": str(truth_bed),
        "reference_fasta": str(reference_fasta),
        "precision": all_precision,
        "recall": all_recall,
        "f1": f1_score(all_precision, all_recall),
        "tp": all_row.get("QUERY.TP") if all_row else None,
        "fp": all_row.get("QUERY.FP") if all_row else None,
        "fn": all_row.get("TRUTH.FN") if all_row else None,
        "snp_precision": snp.get("precision"),
        "snp_recall": snp.get("recall"),
        "indel_precision": indel.get("precision"),
        "indel_recall": indel.get("recall"),
        "generated_at": utc_now(),
    }

    return summary, stratified


def write_tsv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def write_placeholder(path: Path, status: str, detail: str) -> None:
    write_tsv(
        path,
        [{"status": status, "detail": detail, "generated_at": utc_now()}],
        ["status", "detail", "generated_at"],
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Run GIAB HG002 benchmarking against a completed "
            "VAP normalized VCF using an Apptainer-mediated hap.py runtime."
        )
    )
    parser.add_argument("--run-dir", required=True, help="Completed VAP run directory.")
    parser.add_argument("--truth-vcf", required=True, help="GIAB HG002 truth VCF .vcf.gz.")
    parser.add_argument("--truth-bed", required=True, help="GIAB HG002 confident regions BED.")
    parser.add_argument("--reference-fasta", required=True, help="GRCh38 reference FASTA.")
    parser.add_argument("--query-vcf", default=None, help="Optional explicit VAP normalized query VCF.")
    parser.add_argument(
        "--hap-container",
        required=True,
        help="Path to Apptainer hap.py .sif runtime image.",
    )    
    args = parser.parse_args()

    run_dir = Path(args.run_dir)
    if not run_dir.exists():
        fail(f"Run directory not found: {run_dir}")

    run_id = run_dir.name
    benchmarking_dir = run_dir / "benchmarking"
    happy_dir = benchmarking_dir / "happy"
    happy_dir.mkdir(parents=True, exist_ok=True)

    log_path = benchmarking_dir / "benchmarking.log"

    query_vcf = discover_query_vcf(run_dir, args.query_vcf)
    truth_vcf = require_file(Path(args.truth_vcf), "GIAB truth VCF")
    truth_bed = require_file(Path(args.truth_bed), "GIAB confident BED")
    reference_fasta = require_file(Path(args.reference_fasta), "reference FASTA")
    
    apptainer_exe = require_executable("apptainer")

    hap_container = require_file(
        Path(args.hap_container),
        "hap.py Apptainer runtime image",
    )

    hap_container_version = validate_hap_container(
        apptainer_exe=apptainer_exe,
        hap_container=hap_container,
    )    

    benchmark_truth_vcf, benchmark_truth_bed = prepare_namespace_harmonized_giab(
        truth_vcf=truth_vcf,
        truth_bed=truth_bed,
        benchmarking_dir=benchmarking_dir,
        apptainer_exe=apptainer_exe,
        hap_container=hap_container,
    )


    output_prefix = happy_dir / "hg002_happy"

    apptainer_version = subprocess.run(
        [apptainer_exe, "--version"],
        capture_output=True,
        text=True,
        check=False,
    ).stdout.strip()

    write_log(
        log_path,
        [
            f"[{utc_now()}] HG002 benchmarking started",
            f"run_id={run_id}",
            f"run_dir={run_dir}",
            f"query_vcf={query_vcf}",
            f"original_truth_vcf={truth_vcf}",
            f"original_truth_bed={truth_bed}",
            f"benchmark_truth_vcf={benchmark_truth_vcf}",
            f"benchmark_truth_bed={benchmark_truth_bed}",
            f"reference_fasta={reference_fasta}",
            f"apptainer_exe={apptainer_exe}",
            f"apptainer_version={apptainer_version}",
            f"hap_container={hap_container}",
            f"hap_container_version={hap_container_version}",
            f"output_prefix={output_prefix}",
        ],
    )

    run_happy(
        apptainer_exe=apptainer_exe,
        hap_container=hap_container,
        truth_vcf=benchmark_truth_vcf,
        query_vcf=query_vcf,
        truth_bed=benchmark_truth_bed,
        reference_fasta=reference_fasta,
        output_prefix=output_prefix,
        log_path=log_path,
    )

    summary_csv = find_happy_summary(happy_dir)
    write_log(
        log_path,
        [f"[{utc_now()}] summary_csv={summary_csv}"],
    )    
    rows = parse_happy_summary(summary_csv)

    summary, stratified = summarize_happy(
        rows=rows,
        run_id=run_id,
        query_vcf=query_vcf,
        truth_vcf=benchmark_truth_vcf,
        truth_bed=benchmark_truth_bed,
        reference_fasta=reference_fasta,
    )

    summary_fields = [
        "run_id",
        "query_vcf",
        "truth_vcf",
        "truth_bed",
        "reference_fasta",
        "precision",
        "recall",
        "f1",
        "tp",
        "fp",
        "fn",
        "snp_precision",
        "snp_recall",
        "indel_precision",
        "indel_recall",
        "generated_at",
    ]

    write_tsv(benchmarking_dir / "hg002_benchmark_summary.tsv", [summary], summary_fields)

    with (benchmarking_dir / "hg002_benchmark_summary.json").open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2, sort_keys=True)

    write_tsv(
        benchmarking_dir / "hg002_snp_indel_metrics.tsv",
        stratified,
        ["run_id", "variant_type", "truth_tp", "truth_fn", "query_tp", "query_fp", "precision", "recall", "f1"],
    )

    write_placeholder(
        benchmarking_dir / "hg002_false_positives.tsv",
        "raw_happy_outputs_preserved",
        "FP conversion not implemented in initial pass; inspect raw hap.py outputs in benchmarking/happy/.",
    )
    write_placeholder(
        benchmarking_dir / "hg002_false_negatives.tsv",
        "raw_happy_outputs_preserved",
        "FN conversion not implemented in initial pass; inspect raw hap.py outputs in benchmarking/happy/.",
    )

    write_log(
        log_path,
        [
            f"[{utc_now()}] Structured summaries written",
            f"summary_tsv={benchmarking_dir / 'hg002_benchmark_summary.tsv'}",
            f"summary_json={benchmarking_dir / 'hg002_benchmark_summary.json'}",
            f"snp_indel_tsv={benchmarking_dir / 'hg002_snp_indel_metrics.tsv'}",
            f"benchmark_truth_vcf={benchmark_truth_vcf}",
            f"benchmark_truth_bed={benchmark_truth_bed}",            
            f"[{utc_now()}] HG002 benchmarking completed successfully",
        ],
    )

    print(f"HG002 benchmarking completed: {benchmarking_dir}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)