from pathlib import Path
from datetime import datetime, timezone
import argparse
import csv
import shutil
import subprocess
import sys

REQUIRED_COLUMNS = ["SRA_accn", "VAP_run_id"]
BATCH_ROOT = Path("data/reference/stage12_analytical_batch_exports")
SINGLE_RUN_EXPORTER = Path("scripts/analysis/export_stage12_duckdb_exploration.py")

def utc_timestamp():
    return datetime.now(timezone.utc).strftime("%Y_%m_%d_%H%M%S")

def log(msg, fh):
    line = f"{datetime.now(timezone.utc).isoformat()} | {msg}"
    print(line)
    fh.write(line + "\n")
    fh.flush()

def read_manifest(path):
    with open(path, newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")
        missing = [c for c in REQUIRED_COLUMNS if c not in reader.fieldnames]
        if missing:
            raise RuntimeError(f"Manifest missing required columns: {missing}")
        return list(reader)

def completion_artifacts(run_id, sra_accn):
    stage12_dir = Path("results") / run_id / "logs" / "stage12_exploration"
    return {
        "stage12_exploration_dir": stage12_dir,
        "expected_duckdb": stage12_dir / f"{sra_accn}_stage12_exploration.duckdb",
        "expected_run_manifest": stage12_dir / "stage12_exploration_manifest.tsv",
        "expected_run_log": stage12_dir / "stage12_exploration_duckdb.log",
    }

def read_single_run_status(manifest_path):
    if not manifest_path.exists():
        return ""
    with open(manifest_path, newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")
        rows = list(reader)
    if not rows:
        return ""
    return rows[0].get("status", "")

def main():
    parser = argparse.ArgumentParser(description="Run Stage12 DuckDB exports for many VAP runs listed in a TSV manifest.")
    parser.add_argument("manifest_tsv", help="TSV with SRA_accn and VAP_run_id columns; optional Depth_Category column.")
    args = parser.parse_args()

    manifest_path = Path(args.manifest_tsv).resolve()
    if not manifest_path.exists():
        raise FileNotFoundError(f"Manifest not found: {manifest_path}")
    if not SINGLE_RUN_EXPORTER.exists():
        raise FileNotFoundError(f"Single-run exporter not found: {SINGLE_RUN_EXPORTER}")

    timestamp = utc_timestamp()
    manifest_stem = manifest_path.stem

    manifests_dir = BATCH_ROOT / "manifests"
    summaries_dir = BATCH_ROOT / "summaries"
    logs_dir = BATCH_ROOT / "logs"
    for d in [manifests_dir, summaries_dir, logs_dir]:
        d.mkdir(parents=True, exist_ok=True)

    manifest_snapshot = manifests_dir / f"{manifest_stem}_{timestamp}.tsv"
    summary_path = summaries_dir / f"{manifest_stem}_summary_{timestamp}.tsv"
    log_path = logs_dir / f"{manifest_stem}_{timestamp}.log"

    shutil.copy2(manifest_path, manifest_snapshot)
    rows = read_manifest(manifest_path)
    summary_rows = []

    with open(log_path, "w") as log_fh:
        log("Stage12 analytical batch export started", log_fh)
        log(f"Manifest: {manifest_path}", log_fh)
        log(f"Manifest snapshot: {manifest_snapshot}", log_fh)
        log(f"Summary: {summary_path}", log_fh)
        log(f"Rows in manifest: {len(rows)}", log_fh)

        for i, row in enumerate(rows, start=1):
            sra_accn = row.get("SRA_accn", "").strip()
            run_id = row.get("VAP_run_id", "").strip()
            depth_category = row.get("Depth_Category", "").strip()

            input_tsv = Path("results") / run_id / "processed" / "stage_12_validation_candidates.tsv"
            artifacts = completion_artifacts(run_id, sra_accn)
            run_manifest = artifacts["expected_run_manifest"]
            run_log = artifacts["expected_run_log"]
            stage12_dir = artifacts["stage12_exploration_dir"]
            expected_duckdb = artifacts["expected_duckdb"]

            status = ""
            action_taken = ""
            reason = ""
            return_code = ""
            single_run_status = ""

            log(f"[{i}/{len(rows)}] Processing {sra_accn} | {run_id} | depth={depth_category}", log_fh)
            log(f"Input TSV: {input_tsv}", log_fh)

            if not input_tsv.exists():
                status = "missing_input_tsv"
                action_taken = "skipped"
                reason = "input TSV not found"
                log(f"SKIP | {sra_accn} | {run_id} | missing input TSV", log_fh)
            elif run_manifest.exists() and run_log.exists():
                single_run_status = read_single_run_status(run_manifest)
                status = "skipped_existing_outputs"
                action_taken = "skipped"
                reason = "key completion artifacts already exist"
                log(f"SKIP | {sra_accn} | {run_id} | existing completion artifacts detected", log_fh)
                log(f"Existing manifest: {run_manifest}", log_fh)
                log(f"Existing log: {run_log}", log_fh)
            else:
                cmd = [sys.executable, str(SINGLE_RUN_EXPORTER), str(input_tsv)]
                log(f"EXECUTE | {' '.join(cmd)}", log_fh)
                proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
                return_code = str(proc.returncode)
                log(f"RETURN_CODE | {return_code}", log_fh)
                if proc.stdout:
                    log("STDOUT_BEGIN", log_fh)
                    log_fh.write(proc.stdout + "\n")
                    log("STDOUT_END", log_fh)
                if proc.stderr:
                    log("STDERR_BEGIN", log_fh)
                    log_fh.write(proc.stderr + "\n")
                    log("STDERR_END", log_fh)

                if proc.returncode != 0:
                    status = "failed"
                    action_taken = "attempted"
                    reason = "single-run exporter returned nonzero"
                else:
                    single_run_status = read_single_run_status(run_manifest)
                    if single_run_status == "completed_with_warnings":
                        status = "completed_with_warnings"
                    else:
                        status = "completed"
                    action_taken = "executed"
                    reason = "single-run exporter completed"

            summary_rows.append({
                "SRA_accn": sra_accn,
                "VAP_run_id": run_id,
                "Depth_Category": depth_category,
                "input_tsv": str(input_tsv),
                "stage12_exploration_dir": str(stage12_dir),
                "expected_duckdb": str(expected_duckdb),
                "expected_run_manifest": str(run_manifest),
                "expected_run_log": str(run_log),
                "single_run_manifest_path": str(run_manifest) if run_manifest.exists() else "",
                "single_run_status": single_run_status,
                "status": status,
                "action_taken": action_taken,
                "reason": reason,
                "return_code": return_code,
                "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            })

        counts = {}
        for r in summary_rows:
            counts[r["status"]] = counts.get(r["status"], 0) + 1
        log(f"FINAL_COUNTS | {counts}", log_fh)
        log("Stage12 analytical batch export finished", log_fh)

    fieldnames = ["SRA_accn","VAP_run_id","Depth_Category","input_tsv","stage12_exploration_dir","expected_duckdb","expected_run_manifest","expected_run_log","single_run_manifest_path","single_run_status","status","action_taken","reason","return_code","timestamp_utc"]
    with open(summary_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        writer.writerows(summary_rows)

    print("\nStage12 analytical batch export complete.")
    print(f"Manifest snapshot: {manifest_snapshot}")
    print(f"Summary: {summary_path}")
    print(f"Log: {log_path}")

if __name__ == "__main__":
    main()