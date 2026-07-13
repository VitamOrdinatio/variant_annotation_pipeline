\
"""
Native fresh VAP-TEP construction and validation orchestration.

This module composes the existing entity builder, lineage builder, and
validator without shelling out to their CLI entrypoints.
"""

from __future__ import annotations

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from scripts.tep.build_vap_tep_entities import build_entities
from scripts.tep.build_vap_tep_lineage_manifest import (
    build_lineage_manifest,
    load_json as load_inventory_json,
    sha256_file,
    update_lineage_manifest_entity_sha256,
    validate_inventory,
    write_json as write_lineage_json,
)
from scripts.tep.validate_vap_tep import (
    validate_vap_tep,
    write_validation_report,
)


def _stable_json_load(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise ValueError(f"Expected JSON object: {path}")
    return payload



def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def write_tep_emission_receipts(
    *,
    state: dict[str, Any],
    run_paths: dict[str, str],
    tep_result: dict[str, Any],
) -> tuple[Path, Path]:
    """
    Write post-validation lifecycle receipts outside the TEP package.

    These receipts describe the completed end-to-end emission event without
    mutating Stage 13 artifacts or introducing package self-reference.
    """
    metadata_path = (
        Path(run_paths["metadata_dir"])
        / "tep_emission_summary.json"
    )
    report_path = (
        Path(run_paths["reports_dir"])
        / "tep_emission_summary.md"
    )

    payload = {
        "receipt_type": "vap_tep_emission_summary",
        "receipt_schema_version": "1.0.0",
        "created_utc": _utc_now(),
        "execution_run_id": tep_result["execution_run_id"],
        "source_sample_id": tep_result["source_sample_id"],
        "source_run_id": tep_result["source_run_id"],
        "tep_id": tep_result["tep_id"],
        "emission_status": tep_result["status"],
        "validation_status": tep_result["validation_status"],
        "genotype_capability": tep_result["genotype_capability"],
        "package_root": tep_result["package_root"],
        "entity_inventory": tep_result["entity_inventory"],
        "lineage_manifest": tep_result["lineage_manifest"],
        "validation_report": tep_result["validation_report"],
        "materialized_observation_table": tep_result[
            "materialized_observation_table"
        ],
        "pipeline_status": state.get("run", {}).get("status"),
        "genotype_projection_status": (
            state.get("stage_outputs", {})
            .get("genotype_observation_projection", {})
            .get("status")
        ),
    }

    metadata_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    lines = [
        "# TEP-VAP Emission Summary",
        "",
        f"- Execution run: `{payload['execution_run_id']}`",
        f"- Source sample: `{payload['source_sample_id']}`",
        f"- Source evidence run: `{payload['source_run_id']}`",
        f"- TEP ID: `{payload['tep_id']}`",
        f"- Emission status: `{payload['emission_status']}`",
        f"- Validation status: `{payload['validation_status']}`",
        (
            "- Genotype capability: "
            f"`{payload['genotype_capability']}`"
        ),
        f"- Pipeline status: `{payload['pipeline_status']}`",
        (
            "- Genotype projection status: "
            f"`{payload['genotype_projection_status']}`"
        ),
        "",
        "## Artifacts",
        "",
        f"- Package root: `{payload['package_root']}`",
        f"- Entity inventory: `{payload['entity_inventory']}`",
        f"- Lineage manifest: `{payload['lineage_manifest']}`",
        f"- Validation report: `{payload['validation_report']}`",
        (
            "- Materialized observation table: "
            f"`{payload['materialized_observation_table']}`"
        ),
        "",
    ]
    report_path.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

    return metadata_path, report_path

def resolve_tep_source_identity(
    *,
    state: dict[str, Any],
    run_paths: dict[str, str],
) -> tuple[str, str]:
    """
    Resolve the producer evidence identity used by the TEP package.

    Ordinary executions use the current run identity. Retained post-VEP
    evidence uses the source identity preserved by genotype projection.
    """
    summary_value = state.get("artifacts", {}).get(
        "genotype_projection_summary"
    )
    if summary_value:
        summary_path = Path(str(summary_value))
        if summary_path.is_file():
            summary = _stable_json_load(summary_path)
            resolution = summary.get("sample_resolution", {})
            sample_id = str(resolution.get("sample_id", "")).strip()
            run_id = str(resolution.get("run_id", "")).strip()
            if sample_id and run_id:
                return sample_id, run_id

    sample_id = str(
        state.get("sample", {}).get("sample_id")
        or state.get("run", {}).get("sample_id")
        or ""
    ).strip()
    if not sample_id:
        sample_id = "unknown_sample"

    run_id = str(
        state.get("run", {}).get("run_id")
        or Path(run_paths["run_dir"]).name
    ).strip()
    return sample_id, run_id


def materialize_observation_table_for_tep(
    *,
    state: dict[str, Any],
    run_paths: dict[str, str],
    sample_id: str,
    source_run_id: str,
) -> Path:
    """
    Ensure the Stage 07 observation TSV exists inside processed/.

    Full runs already satisfy this. Post-VEP fixture runs retain the source
    TSV externally, so it is copied byte-for-byte before TEP construction.
    """
    processed_dir = Path(run_paths["processed_dir"])
    existing = sorted(processed_dir.glob("*.annotated_variants.tsv"))
    if len(existing) == 1:
        return existing[0]
    if len(existing) > 1:
        raise ValueError(
            "Expected at most one annotated-variants TSV in processed/, "
            f"found {len(existing)}"
        )

    source_value = state.get("artifacts", {}).get("annotated_table")
    if not source_value:
        raise FileNotFoundError(
            "No annotated TSV is registered for TEP observation transport."
        )

    source = Path(str(source_value))
    if not source.is_file():
        raise FileNotFoundError(
            f"Registered annotated TSV does not exist: {source}"
        )

    destination = processed_dir / (
        f"{sample_id}_{source_run_id}.annotated_variants.tsv"
    )
    if destination.exists():
        if destination.read_bytes() != source.read_bytes():
            raise FileExistsError(
                "Refusing to replace a non-identical materialized "
                f"observation TSV: {destination}"
            )
        return destination

    shutil.copy2(source, destination)
    return destination


def build_and_validate_fresh_vap_tep(
    *,
    state: dict[str, Any],
    run_paths: dict[str, str],
) -> dict[str, Any]:
    """
    Build, lineage-index, validate, and report one fresh TEP-VAP package.
    """
    run_dir = Path(run_paths["run_dir"])
    sample_id, source_run_id = resolve_tep_source_identity(
        state=state,
        run_paths=run_paths,
    )
    observation_path = materialize_observation_table_for_tep(
        state=state,
        run_paths=run_paths,
        sample_id=sample_id,
        source_run_id=source_run_id,
    )

    package_root = build_entities(
        run_dir=run_dir,
        output_root=None,
        dry_run=False,
        overwrite=False,
        sample_id_override=sample_id,
        run_id_override=source_run_id,
    )

    inventory_path = package_root / "entity_inventory.json"
    inventory = load_inventory_json(inventory_path)
    validate_inventory(inventory, inventory_path)

    lineage_path = package_root / "lineage_manifest.json"
    manifest = build_lineage_manifest(inventory, inventory_path)
    write_lineage_json(lineage_path, manifest)

    manifest_sha256 = sha256_file(lineage_path)
    update_lineage_manifest_entity_sha256(
        manifest,
        manifest_sha256,
    )
    write_lineage_json(lineage_path, manifest)

    manifest, checks = validate_vap_tep(
        manifest_path=lineage_path,
        write_updated_manifest=True,
    )
    validation_status = manifest["validation_summary"][
        "validation_status"
    ]
    report_path = package_root / "validation_report.md"
    write_validation_report(
        report_path,
        checks,
        validation_status,
    )

    if validation_status != "pass":
        failed = [
            check.criterion
            for check in checks
            if check.status == "FAIL"
        ]
        raise RuntimeError(
            "Fresh TEP validation failed: " + ", ".join(failed)
        )

    result = {
        "attempted": True,
        "status": "success",
        "tep_id": manifest["tep_id"],
        "package_root": str(package_root),
        "entity_inventory": str(inventory_path),
        "lineage_manifest": str(lineage_path),
        "validation_report": str(report_path),
        "validation_status": validation_status,
        "genotype_capability": inventory.get(
            "summary",
            {},
        ).get("genotype_capability", "not_available"),
        "source_sample_id": sample_id,
        "source_run_id": source_run_id,
        "execution_run_id": Path(run_paths["run_dir"]).name,
        "materialized_observation_table": str(observation_path),
    }

    receipt_json, receipt_markdown = write_tep_emission_receipts(
        state=state,
        run_paths=run_paths,
        tep_result=result,
    )
    result["emission_summary_json"] = str(receipt_json)
    result["emission_summary_markdown"] = str(receipt_markdown)

    return result
