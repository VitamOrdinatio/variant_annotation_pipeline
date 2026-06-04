from __future__ import annotations

import argparse
import csv
import datetime
import logging
import shutil
import tarfile
from pathlib import Path

MAX_FILE_BYTES = 50 * 1024 * 1024
MAX_BATCH_BYTES = 100 * 1024 * 1024

EXPORT_ROOT = Path("/root/Desktop/vap/batched_exports")
LIGHTWEIGHT_RUNS_DIR = EXPORT_ROOT / "lightweight_runs"
COMPRESSED_DIR = EXPORT_ROOT / "compressed"
MANIFESTS_DIR = EXPORT_ROOT / "manifests"
LOGS_DIR = EXPORT_ROOT / "logs"

EXPORT_SUMMARY_FIELDS = [
    "export_timestamp",
    "SRA_accn",
    "VAP_run_id",
    "Depth_Category",
    "source_run_dir",
    "destination_run_dir",
    "run_status",
    "files_copied",
    "files_skipped_size",
    "files_skipped_duckdb",
    "files_skipped_other",
    "bytes_copied",
    "compressed_run_archive",
    "compressed_run_archive_bytes",
    "batch_archive",
    "warning",
]

EXPORT_FILE_MANIFEST_FIELDS = [
    "export_timestamp",
    "SRA_accn",
    "VAP_run_id",
    "Depth_Category",
    "source_path",
    "relative_path",
    "destination_path",
    "file_size_bytes",
    "copy_status",
]

EXPORT_SKIPPED_FIELDS = [
    "export_timestamp",
    "SRA_accn",
    "VAP_run_id",
    "Depth_Category",
    "source_path",
    "relative_path",
    "file_size_bytes",
    "skip_reason",
]


def utc_timestamp() -> str:
    return datetime.datetime.utcnow().strftime("%Y_%m_%d_%H%M%S")


def setup_directories() -> None:
    for path in [
        EXPORT_ROOT,
        LIGHTWEIGHT_RUNS_DIR,
        COMPRESSED_DIR,
        MANIFESTS_DIR,
        LOGS_DIR,
    ]:
        path.mkdir(parents=True, exist_ok=True)


def setup_logger(export_ts: str) -> tuple[logging.Logger, Path]:
    log_path = LOGS_DIR / f"export_{export_ts}.log"

    logger = logging.getLogger("lightweight_export")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()

    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(message)s"
    )

    file_handler = logging.FileHandler(log_path)
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger, log_path


def copy_manifest(manifest_path: Path, export_ts: str) -> Path:
    copied_manifest = (
        MANIFESTS_DIR / f"input_manifest_{export_ts}.tsv"
    )
    shutil.copy2(manifest_path, copied_manifest)
    return copied_manifest


def validate_manifest_columns(fieldnames: list[str]) -> None:
    required = {"SRA_accn", "VAP_run_id"}

    missing = required - set(fieldnames)

    if missing:
        raise ValueError(
            f"Manifest missing required columns: {sorted(missing)}"
        )


def write_tsv(path: Path, fieldnames: list[str], rows: list[dict]) -> None:
    with open(path, "w", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fieldnames,
            delimiter="\t",
        )
        writer.writeheader()
        writer.writerows(rows)


def create_run_archive(
    source_dir: Path,
    archive_path: Path,
    logger: logging.Logger,
) -> int:

    logger.info(f"Creating archive: {archive_path}")

    with tarfile.open(archive_path, "w:gz") as tar:
        tar.add(
            source_dir,
            arcname=source_dir.name,
        )

    return archive_path.stat().st_size


def create_transport_batches(
    archive_paths: list[Path],
    export_ts: str,
    logger: logging.Logger,
) -> dict[str, str]:

    batch_mapping = {}

    batch_index = 1
    current_batch_size = 0

    current_batch_path = (
        COMPRESSED_DIR /
        f"vap_lightweight_batch_{export_ts}_{batch_index:03d}.tar"
    )

    current_tar = tarfile.open(current_batch_path, "w")

    for archive_path in archive_paths:

        archive_size = archive_path.stat().st_size

        if (
            current_batch_size > 0 and
            current_batch_size + archive_size > MAX_BATCH_BYTES
        ):
            current_tar.close()

            batch_index += 1
            current_batch_size = 0

            current_batch_path = (
                COMPRESSED_DIR /
                f"vap_lightweight_batch_{export_ts}_{batch_index:03d}.tar"
            )

            current_tar = tarfile.open(current_batch_path, "w")

        logger.info(
            f"Adding {archive_path.name} "
            f"to {current_batch_path.name}"
        )

        current_tar.add(
            archive_path,
            arcname=archive_path.name,
        )

        current_batch_size += archive_size

        batch_mapping[archive_path.name] = current_batch_path.name

    current_tar.close()

    return batch_mapping


def main() -> None:

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "manifest_tsv",
        help="Path to export manifest TSV",
    )

    args = parser.parse_args()

    repo_root = Path.cwd()

    export_ts = utc_timestamp()

    setup_directories()

    logger, log_path = setup_logger(export_ts)

    manifest_path = Path(args.manifest_tsv).resolve()

    copied_manifest = copy_manifest(manifest_path, export_ts)

    logger.info(f"Export timestamp: {export_ts}")
    logger.info(f"Repo root: {repo_root}")
    logger.info(f"Manifest path: {manifest_path}")
    logger.info(f"Copied manifest: {copied_manifest}")

    export_summary_rows = []
    export_file_rows = []
    export_skipped_rows = []

    run_archive_paths = []

    with open(manifest_path, newline="") as handle:

        reader = csv.DictReader(handle, delimiter="\t")

        if reader.fieldnames is None:
            raise ValueError("Manifest TSV is empty or malformed")

        validate_manifest_columns(reader.fieldnames)

        for row in reader:

            sra_accn = row.get("SRA_accn", "")
            run_id = row.get("VAP_run_id", "")
            depth_category = row.get("Depth_Category", "")

            source_run_dir = repo_root / "results" / run_id

            destination_run_dir = (
                LIGHTWEIGHT_RUNS_DIR / run_id
            )

            summary_row = {
                "export_timestamp": export_ts,
                "SRA_accn": sra_accn,
                "VAP_run_id": run_id,
                "Depth_Category": depth_category,
                "source_run_dir": str(source_run_dir),
                "destination_run_dir": str(destination_run_dir),
                "run_status": "",
                "files_copied": 0,
                "files_skipped_size": 0,
                "files_skipped_duckdb": 0,
                "files_skipped_other": 0,
                "bytes_copied": 0,
                "compressed_run_archive": "",
                "compressed_run_archive_bytes": "",
                "batch_archive": "",
                "warning": "",
            }

            logger.info(f"Processing {run_id}")

            if not source_run_dir.exists():

                warning = "missing_source"

                logger.warning(
                    f"Missing source directory: {source_run_dir}"
                )

                summary_row["run_status"] = "missing_source"
                summary_row["warning"] = warning

                export_summary_rows.append(summary_row)

                continue

            if destination_run_dir.exists():

                warning = "skipped_existing_destination"

                logger.warning(
                    f"Destination already exists: "
                    f"{destination_run_dir}"
                )

                summary_row["run_status"] = warning
                summary_row["warning"] = warning

                export_summary_rows.append(summary_row)

                continue

            destination_run_dir.mkdir(
                parents=True,
                exist_ok=False,
            )

            for source_file in source_run_dir.rglob("*"):

                if not source_file.is_file():
                    continue

                relative_path = source_file.relative_to(
                    source_run_dir
                )

                file_size = source_file.stat().st_size

                if source_file.name.endswith(".duckdb"):

                    export_skipped_rows.append({
                        "export_timestamp": export_ts,
                        "SRA_accn": sra_accn,
                        "VAP_run_id": run_id,
                        "Depth_Category": depth_category,
                        "source_path": str(source_file),
                        "relative_path": str(relative_path),
                        "file_size_bytes": file_size,
                        "skip_reason": "duckdb_excluded",
                    })

                    summary_row["files_skipped_duckdb"] += 1

                    continue

                if file_size >= MAX_FILE_BYTES:

                    export_skipped_rows.append({
                        "export_timestamp": export_ts,
                        "SRA_accn": sra_accn,
                        "VAP_run_id": run_id,
                        "Depth_Category": depth_category,
                        "source_path": str(source_file),
                        "relative_path": str(relative_path),
                        "file_size_bytes": file_size,
                        "skip_reason": "size_ge_50mb",
                    })

                    summary_row["files_skipped_size"] += 1

                    continue

                destination_file = (
                    destination_run_dir / relative_path
                )

                destination_file.parent.mkdir(
                    parents=True,
                    exist_ok=True,
                )

                try:

                    shutil.copy2(
                        source_file,
                        destination_file,
                    )

                    summary_row["files_copied"] += 1
                    summary_row["bytes_copied"] += file_size

                    export_file_rows.append({
                        "export_timestamp": export_ts,
                        "SRA_accn": sra_accn,
                        "VAP_run_id": run_id,
                        "Depth_Category": depth_category,
                        "source_path": str(source_file),
                        "relative_path": str(relative_path),
                        "destination_path": str(destination_file),
                        "file_size_bytes": file_size,
                        "copy_status": "copied",
                    })

                except Exception:

                    logger.exception(
                        f"Copy failure: {source_file}"
                    )

                    summary_row["files_skipped_other"] += 1

                    export_skipped_rows.append({
                        "export_timestamp": export_ts,
                        "SRA_accn": sra_accn,
                        "VAP_run_id": run_id,
                        "Depth_Category": depth_category,
                        "source_path": str(source_file),
                        "relative_path": str(relative_path),
                        "file_size_bytes": file_size,
                        "skip_reason": "copy_error",
                    })

            summary_row["run_status"] = "copied"

            archive_path = (
                COMPRESSED_DIR /
                f"{run_id}_{export_ts}.tar.gz"
            )

            try:
                archive_size = create_run_archive(
                    destination_run_dir,
                    archive_path,
                    logger,
                )
            except Exception:

                logger.exception(
                    f"Archive creation failed for {destination_run_dir}"
                )

                summary_row["run_status"] = "failed"
                summary_row["warning"] = "archive_creation_failed"
                export_summary_rows.append(summary_row)

                continue

            if archive_size > MAX_BATCH_BYTES:
                summary_row["warning"] = "single_archive_exceeds_batch_cap"
                logger.warning(
                    f"{archive_path.name} exceeds "
                    f"{MAX_BATCH_BYTES} bytes"
                )

            summary_row["compressed_run_archive"] = (
                archive_path.name
            )

            summary_row["compressed_run_archive_bytes"] = (
                archive_size
            )

            run_archive_paths.append(archive_path)

            export_summary_rows.append(summary_row)

    batch_mapping = create_transport_batches(
        run_archive_paths,
        export_ts,
        logger,
    )

    for row in export_summary_rows:

        archive_name = row["compressed_run_archive"]

        if archive_name in batch_mapping:
            row["batch_archive"] = batch_mapping[archive_name]

    export_summary_path = (
        MANIFESTS_DIR /
        f"export_summary_{export_ts}.tsv"
    )

    export_file_manifest_path = (
        MANIFESTS_DIR /
        f"export_file_manifest_{export_ts}.tsv"
    )

    export_skipped_path = (
        MANIFESTS_DIR /
        f"export_skipped_files_{export_ts}.tsv"
    )

    write_tsv(
        export_summary_path,
        EXPORT_SUMMARY_FIELDS,
        export_summary_rows,
    )

    write_tsv(
        export_file_manifest_path,
        EXPORT_FILE_MANIFEST_FIELDS,
        export_file_rows,
    )

    write_tsv(
        export_skipped_path,
        EXPORT_SKIPPED_FIELDS,
        export_skipped_rows,
    )

    copied_runs = sum(
        1
        for row in export_summary_rows
        if row["run_status"] == "copied"
    )

    skipped_runs = len(export_summary_rows) - copied_runs

    batch_archives = sorted(
        COMPRESSED_DIR.glob(
            f"vap_lightweight_batch_{export_ts}_*.tar"
        )
    )

    print()
    print("Export complete.")
    print(f"Timestamp: {export_ts}")
    print(f"Runs copied: {copied_runs}")
    print(f"Runs skipped: {skipped_runs}")
    print(f"Batch archives written: {len(batch_archives)}")
    print(
        "Download from: "
        "/root/Desktop/vap/batched_exports/compressed/"
    )
    print(
        "Manifests: "
        "/root/Desktop/vap/batched_exports/manifests/"
    )
    print(f"Log: {log_path}")
    print()


if __name__ == "__main__":
    main()