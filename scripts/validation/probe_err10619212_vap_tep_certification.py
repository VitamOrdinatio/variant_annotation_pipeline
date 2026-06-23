#!/usr/bin/env python3
"""
ERR10619212 VAP-TEP Certification Probe

Of the 144 SRAs, ERR10619212 is part of the q1 cohort with respect to read counts.

Run from the VAP repository root on MARK:

    python probe_err10619212_vap_tep_certification.py

This probe is read-only with respect to results/.
It writes audit artifacts only under /root/Desktop/.

Purpose:
    Measure whether the ERR10619212 q1 WES epilepsy VAP-TEP faithfully transports
    the preservation-critical artifacts from the original VAP processed/ truth directory.

Important:
    This script produces measurements. It does not itself grant certification.
"""

from __future__ import annotations

import csv
import hashlib
import json
import random
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Set, Tuple


RUN_ID = "run_2026_05_30_214724"
SAMPLE_ID = "ERR10619212"
TEP_NAME = "vap_tep_ERR10619212_run_2026_05_30_214724_v1"

PROCESSED_DIR = Path("results") / RUN_ID / "processed"
TEP_DIR = Path("results") / RUN_ID / "tep" / TEP_NAME
DESKTOP_DIR = Path("/root/Desktop")

EXPECTED = {
    # ERR10619212 is a q1 WES epilepsy SRA. Exact counts are measured from the
    # emitted TEP and source processed/ artifacts rather than pre-hardcoded.
    # The certification logic checks internal preservation invariants:
    #   - processed artifact SHA256 == TEP artifact SHA256
    #   - Stage07 variant_id set == Stage08 variant_id sets
    #   - Stage11 row_count == Stage07 row_count
    #   - Stage12 row_count == Stage07 row_count
    #   - validation_required=False records survive
    #   - routing topology is measured explicitly
    "stage07_rows": None,
    "stage07_variant_ids": None,
    "stage08_rows": None,
    "stage08_variant_ids": None,
    "coding_variant_ids": None,
    "splice_variant_ids": None,
    "noncoding_variant_ids": None,
    "stage09_rows": None,
    "stage10_rows": None,
    "stage11_rows": None,
    "stage11_variant_ids": None,
    "stage12_rows": None,
    "stage12_variant_ids": None,
    "validation_required_true": None,
    "validation_required_false": None,
}

ARTIFACT_PAIRS = [
    ("observation", "Stage07", PROCESSED_DIR / f"{SAMPLE_ID}_{RUN_ID}.annotated_variants.tsv", TEP_DIR / "entities/observation" / f"{SAMPLE_ID}_{RUN_ID}.annotated_variants.tsv", "tsv"),
    ("normalization_selected_transcript_consequences", "Stage08", PROCESSED_DIR / "stage_08_selected_transcript_consequences.tsv", TEP_DIR / "entities/normalization/stage_08_selected_transcript_consequences.tsv", "tsv"),
    ("normalization_vdb_ready_variants", "Stage08", PROCESSED_DIR / "stage_08_vdb_ready_variants.tsv", TEP_DIR / "entities/normalization/stage_08_vdb_ready_variants.tsv", "tsv"),
    ("routing_coding", "Stage08", PROCESSED_DIR / "coding_candidates.tsv", TEP_DIR / "entities/routing/coding_candidates.tsv", "tsv"),
    ("routing_splice", "Stage08", PROCESSED_DIR / "splice_region_candidates.tsv", TEP_DIR / "entities/routing/splice_region_candidates.tsv", "tsv"),
    ("routing_noncoding", "Stage08", PROCESSED_DIR / "noncoding_candidates.tsv", TEP_DIR / "entities/routing/noncoding_candidates.tsv", "tsv"),
    ("coding_interpretation", "Stage09", PROCESSED_DIR / "stage_09_coding_interpreted.tsv", TEP_DIR / "entities/coding_interpretation/stage_09_coding_interpreted.tsv", "tsv"),
    ("noncoding_interpretation", "Stage10", PROCESSED_DIR / "stage_10_noncoding_interpreted.tsv", TEP_DIR / "entities/noncoding_interpretation/stage_10_noncoding_interpreted.tsv", "tsv"),
    ("prioritization", "Stage11", PROCESSED_DIR / "stage_11_prioritized_variants.tsv", TEP_DIR / "entities/prioritization/stage_11_prioritized_variants.tsv", "tsv"),
    ("validation", "Stage12", PROCESSED_DIR / "stage_12_validation_candidates.tsv", TEP_DIR / "entities/validation/stage_12_validation_candidates.tsv", "tsv"),
    ("context_artifact_manifest", "Stage13", PROCESSED_DIR / "stage_13_artifact_manifest.json", TEP_DIR / "entities/context/stage_13_artifact_manifest.json", "json"),
    ("context_final_summary", "Stage13", PROCESSED_DIR / "stage_13_final_summary.json", TEP_DIR / "entities/context/stage_13_final_summary.json", "json"),
    ("context_run_report", "Stage13", PROCESSED_DIR / "stage_13_run_report.md", TEP_DIR / "entities/context/stage_13_run_report.md", "text"),
]

TSV_PATHS = {
    "stage07": TEP_DIR / "entities/observation" / f"{SAMPLE_ID}_{RUN_ID}.annotated_variants.tsv",
    "stage08_selected": TEP_DIR / "entities/normalization/stage_08_selected_transcript_consequences.tsv",
    "stage08_vdb_ready": TEP_DIR / "entities/normalization/stage_08_vdb_ready_variants.tsv",
    "coding": TEP_DIR / "entities/routing/coding_candidates.tsv",
    "splice": TEP_DIR / "entities/routing/splice_region_candidates.tsv",
    "noncoding": TEP_DIR / "entities/routing/noncoding_candidates.tsv",
    "stage09": TEP_DIR / "entities/coding_interpretation/stage_09_coding_interpreted.tsv",
    "stage10": TEP_DIR / "entities/noncoding_interpretation/stage_10_noncoding_interpreted.tsv",
    "stage11": TEP_DIR / "entities/prioritization/stage_11_prioritized_variants.tsv",
    "stage12": TEP_DIR / "entities/validation/stage_12_validation_candidates.tsv",
}

REQUIRED_COLUMNS = {
    "stage07": ["sample_id", "run_id", "variant_id"],
    "stage09": ["functional_impact", "coding_interpretation_label", "clinical_evidence", "rarity_flag", "qc_reliability"],
    "stage10": ["noncoding_functional_context", "noncoding_interpretation_label", "clinical_evidence", "rarity_flag", "qc_reliability"],
    "stage11": ["priority_tier", "priority_rank", "priority_reason", "source_interpretation_label", "variant_origin"],
    "stage12": ["validation_required", "validation_priority", "suggested_validation_method", "validation_reason"],
}

COORDINATE_GROUPS = {
    "chromosome": ["chrom", "chr", "chromosome", "#chrom"],
    "position": ["pos", "position", "start", "start_position"],
    "reference_allele": ["ref", "reference", "reference_allele", "reference_base"],
    "alternate_allele": ["alt", "alternate", "alternate_allele", "alternate_base"],
}


def ensure_output_dir(repo_root: Path) -> Path:
    timestamp = datetime.now().strftime("%Y_%m_%d_%H%M%S")
    out_dir = DESKTOP_DIR / f"err10619212_vap_tep_certification_audit_{timestamp}"
    results_abs = (repo_root / "results").resolve()
    out_abs = out_dir.resolve()
    if str(out_abs).startswith(str(results_abs)):
        raise RuntimeError(f"Refusing to write output inside results/: {out_abs}")
    out_dir.mkdir(parents=True, exist_ok=False)
    return out_dir


def sha256_file(path: Path, block_size: int = 16 * 1024 * 1024) -> Optional[str]:
    if not path.exists():
        return None
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            block = f.read(block_size)
            if not block:
                break
            h.update(block)
    return h.hexdigest()


def read_header(path: Path) -> List[str]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", errors="replace") as f:
        line = f.readline()
    return line.rstrip("\n\r").split("\t") if line else []


def normalize_bool(value: str) -> str:
    v = str(value).strip().lower()
    if v in {"true", "t", "1", "yes", "y"}:
        return "True"
    if v in {"false", "f", "0", "no", "n"}:
        return "False"
    return str(value).strip()


def find_col(header: Sequence[str], candidates: Sequence[str]) -> Optional[str]:
    lower_to_actual = {c.lower(): c for c in header}
    for candidate in candidates:
        if candidate.lower() in lower_to_actual:
            return lower_to_actual[candidate.lower()]
    return None


def variant_col(header: Sequence[str]) -> Optional[str]:
    return find_col(header, ["variant_id"])


def get_tsv_stats(path: Path, collect_variant_ids: bool = False, distribution_cols: Optional[Sequence[str]] = None, first_n_variant_ids: int = 0) -> Dict[str, Any]:
    stats: Dict[str, Any] = {"exists": path.exists(), "row_count": None, "column_count": None, "header": [], "variant_id_count": None, "variant_ids": None, "distributions": {}, "first_variant_ids": []}
    if not path.exists():
        return stats
    header = read_header(path)
    stats["header"] = header
    stats["column_count"] = len(header)
    vcol = variant_col(header)
    v_idx = header.index(vcol) if vcol else None
    dist_indices = {col: header.index(col) for col in (distribution_cols or []) if col in header}
    row_count = 0
    variant_ids: Optional[Set[str]] = set() if collect_variant_ids else None
    variant_id_counter: Optional[Set[str]] = set() if v_idx is not None else None
    distributions: Dict[str, Counter] = {col: Counter() for col in dist_indices}
    with path.open("r", encoding="utf-8", errors="replace", newline="") as f:
        next(f, None)
        for line in f:
            row_count += 1
            parts = line.rstrip("\n\r").split("\t")
            if v_idx is not None and v_idx < len(parts):
                vid = parts[v_idx]
                if variant_id_counter is not None:
                    variant_id_counter.add(vid)
                if variant_ids is not None:
                    variant_ids.add(vid)
                if first_n_variant_ids and len(stats["first_variant_ids"]) < first_n_variant_ids:
                    stats["first_variant_ids"].append(vid)
            for col, idx in dist_indices.items():
                val = parts[idx] if idx < len(parts) else ""
                if col == "validation_required":
                    val = normalize_bool(val)
                distributions[col][val] += 1
    stats["row_count"] = row_count
    stats["variant_id_count"] = len(variant_id_counter) if variant_id_counter is not None else None
    stats["variant_ids"] = variant_ids
    stats["distributions"] = {col: dict(counter) for col, counter in distributions.items()}
    return stats


def write_tsv(path: Path, rows: List[Dict[str, Any]], fieldnames: Sequence[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({k: "" if row.get(k) is None else row.get(k) for k in fieldnames})


def write_json(path: Path, obj: Any) -> None:
    with path.open("w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, sort_keys=True)


def pass_fail(condition: bool) -> str:
    return "PASS" if condition else "FAIL"


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8", errors="replace") as f:
        return json.load(f)


def walk_json(obj: Any, path: str = "") -> Iterable[Tuple[str, Any]]:
    yield path, obj
    if isinstance(obj, dict):
        for k, v in obj.items():
            next_path = f"{path}.{k}" if path else str(k)
            yield from walk_json(v, next_path)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from walk_json(v, f"{path}[{i}]")


def audit_transport_fidelity(out_dir: Path) -> List[Dict[str, Any]]:
    rows = []
    for role, stage, source, tep, kind in ARTIFACT_PAIRS:
        source_exists = source.exists()
        tep_exists = tep.exists()
        source_sha = sha256_file(source) if source_exists else None
        tep_sha = sha256_file(tep) if tep_exists else None
        row = {"role": role, "stage": stage, "kind": kind, "source_path": str(source), "tep_path": str(tep), "source_exists": source_exists, "tep_exists": tep_exists, "source_size_bytes": source.stat().st_size if source_exists else None, "tep_size_bytes": tep.stat().st_size if tep_exists else None, "source_sha256": source_sha, "tep_sha256": tep_sha, "sha256_match": source_sha == tep_sha if source_sha and tep_sha else False, "source_row_count": None, "tep_row_count": None, "row_count_match": None, "source_column_count": None, "tep_column_count": None, "column_count_match": None}
        if kind == "tsv" and source_exists and tep_exists:
            source_stats = get_tsv_stats(source)
            tep_stats = get_tsv_stats(tep)
            row["source_row_count"] = source_stats["row_count"]
            row["tep_row_count"] = tep_stats["row_count"]
            row["row_count_match"] = source_stats["row_count"] == tep_stats["row_count"]
            row["source_column_count"] = source_stats["column_count"]
            row["tep_column_count"] = tep_stats["column_count"]
            row["column_count_match"] = source_stats["column_count"] == tep_stats["column_count"]
        rows.append(row)
    write_tsv(out_dir / "tep_err10619212_entity_row_count_audit.tsv", rows, ["role", "stage", "kind", "source_path", "tep_path", "source_exists", "tep_exists", "source_size_bytes", "tep_size_bytes", "source_sha256", "tep_sha256", "sha256_match", "source_row_count", "tep_row_count", "row_count_match", "source_column_count", "tep_column_count", "column_count_match"])
    return rows


def audit_required_columns(out_dir: Path) -> List[Dict[str, Any]]:
    rows = []
    for entity, required in REQUIRED_COLUMNS.items():
        path = TSV_PATHS[entity]
        header = read_header(path)
        header_set = set(header)
        for col in required:
            rows.append({"entity": entity, "path": str(path), "column_check_type": "required_column", "column_or_group": col, "present": col in header_set, "matched_column": col if col in header_set else ""})
    header = read_header(TSV_PATHS["stage07"])
    for group, candidates in COORDINATE_GROUPS.items():
        matched = find_col(header, candidates)
        rows.append({"entity": "stage07", "path": str(TSV_PATHS["stage07"]), "column_check_type": "coordinate_or_allele_group", "column_or_group": group, "present": matched is not None, "matched_column": matched or ""})
    write_tsv(out_dir / "tep_err10619212_required_column_audit.tsv", rows, ["entity", "path", "column_check_type", "column_or_group", "present", "matched_column"])
    return rows


def audit_variant_parity(out_dir: Path) -> List[Dict[str, Any]]:
    rows = []
    stage07 = get_tsv_stats(TSV_PATHS["stage07"], collect_variant_ids=True)["variant_ids"]
    assert isinstance(stage07, set)
    for name, path in [("stage07_vs_stage08_selected", TSV_PATHS["stage08_selected"]), ("stage07_vs_stage08_vdb_ready", TSV_PATHS["stage08_vdb_ready"])]:
        right = get_tsv_stats(path, collect_variant_ids=True)["variant_ids"]
        assert isinstance(right, set)
        rows.append({"comparison": name, "left_entity": "stage07", "right_entity": path.name, "left_variant_id_count": len(stage07), "right_variant_id_count": len(right), "intersection_count": len(stage07 & right), "left_only_count": len(stage07 - right), "right_only_count": len(right - stage07), "sets_equal": stage07 == right})
        del right
    selected = get_tsv_stats(TSV_PATHS["stage08_selected"], collect_variant_ids=True)
    vdb_ready = get_tsv_stats(TSV_PATHS["stage08_vdb_ready"], collect_variant_ids=True)
    selected_set = selected["variant_ids"]
    vdb_ready_set = vdb_ready["variant_ids"]
    assert isinstance(selected_set, set) and isinstance(vdb_ready_set, set)
    selected_sha = sha256_file(TSV_PATHS["stage08_selected"])
    vdb_ready_sha = sha256_file(TSV_PATHS["stage08_vdb_ready"])
    rows.append({"comparison": "stage08_selected_vs_stage08_vdb_ready", "left_entity": "stage_08_selected_transcript_consequences.tsv", "right_entity": "stage_08_vdb_ready_variants.tsv", "left_variant_id_count": len(selected_set), "right_variant_id_count": len(vdb_ready_set), "intersection_count": len(selected_set & vdb_ready_set), "left_only_count": len(selected_set - vdb_ready_set), "right_only_count": len(vdb_ready_set - selected_set), "sets_equal": selected_set == vdb_ready_set, "row_count_match": selected["row_count"] == vdb_ready["row_count"], "column_count_match": selected["column_count"] == vdb_ready["column_count"], "sha256_match": selected_sha == vdb_ready_sha, "semantic_note": "Physical equivalence in VAP v1 does not imply semantic equivalence forever; both Stage08 artifact identities must remain preserved."})
    write_tsv(out_dir / "tep_err10619212_variant_id_parity_audit.tsv", rows, ["comparison", "left_entity", "right_entity", "left_variant_id_count", "right_variant_id_count", "intersection_count", "left_only_count", "right_only_count", "sets_equal", "row_count_match", "column_count_match", "sha256_match", "semantic_note"])
    return rows


def audit_stage08_routing_overlap(out_dir: Path) -> Dict[str, Any]:
    coding = get_tsv_stats(TSV_PATHS["coding"], collect_variant_ids=True)["variant_ids"]
    splice = get_tsv_stats(TSV_PATHS["splice"], collect_variant_ids=True)["variant_ids"]
    noncoding = get_tsv_stats(TSV_PATHS["noncoding"], collect_variant_ids=True)["variant_ids"]
    assert isinstance(coding, set) and isinstance(splice, set) and isinstance(noncoding, set)
    summary = {"coding_variant_id_count": len(coding), "splice_variant_id_count": len(splice), "noncoding_variant_id_count": len(noncoding), "coding_intersect_splice": len(coding & splice), "coding_intersect_noncoding": len(coding & noncoding), "splice_intersect_noncoding": len(splice & noncoding), "coding_only": len(coding - splice - noncoding), "splice_only": len(splice - coding - noncoding), "noncoding_only": len(noncoding - coding - splice), "expected_model": "Coding Partition + Noncoding Partition + Splice Overlay"}
    summary["model_check"] = (
        "PASS"
        if summary["coding_intersect_noncoding"] == 0 and summary["splice_intersect_noncoding"] == 0
        else "FAIL"
    )
    summary["splice_overlay_observed"] = summary["coding_intersect_splice"] > 0
    summary["splice_overlay_note"] = (
        "Splice overlay observed through coding∩splice overlap."
        if summary["splice_overlay_observed"]
        else "No coding∩splice overlap observed in this WES run; review biologically, but this is not automatically a transport defect."
    )
    write_tsv(out_dir / "tep_err10619212_stage08_routing_overlap_audit.tsv", [{"metric": k, "value": v} for k, v in summary.items()], ["metric", "value"])
    return summary


def audit_candidate_collapse(out_dir: Path) -> Tuple[List[Dict[str, Any]], Dict[str, Any], Dict[str, Any]]:
    rows = []
    stage07_stats = get_tsv_stats(TSV_PATHS["stage07"])
    stage11_stats = get_tsv_stats(TSV_PATHS["stage11"], collect_variant_ids=True, distribution_cols=["priority_tier"])
    stage12_stats = get_tsv_stats(TSV_PATHS["stage12"], collect_variant_ids=True, distribution_cols=["validation_required"])
    def add_metric(section: str, metric: str, value: Any, expected: Any = None) -> None:
        rows.append({"section": section, "metric": metric, "value": value, "expected": expected, "status": pass_fail(value == expected) if expected is not None else ""})
    add_metric("stage11", "row_count", stage11_stats["row_count"])
    add_metric("stage11", "variant_id_count", stage11_stats["variant_id_count"])
    add_metric("stage11", "row_count_equals_stage07", stage11_stats["row_count"] == stage07_stats["row_count"], True)
    for label, count in sorted(stage11_stats["distributions"].get("priority_tier", {}).items()):
        add_metric("stage11_priority_tier_distribution", label, count)
    add_metric("stage12", "row_count", stage12_stats["row_count"])
    add_metric("stage12", "variant_id_count", stage12_stats["variant_id_count"])
    add_metric("stage12", "row_count_equals_stage07", stage12_stats["row_count"] == stage07_stats["row_count"], True)
    validation_dist = stage12_stats["distributions"].get("validation_required", {})
    add_metric("stage12_validation_required_distribution", "True", validation_dist.get("True", 0))
    add_metric("stage12_validation_required_distribution", "False", validation_dist.get("False", 0))
    candidate_collapse_pass = stage11_stats["row_count"] == stage07_stats["row_count"] and stage12_stats["row_count"] == stage07_stats["row_count"] and validation_dist.get("False", 0) > 0
    add_metric("candidate_collapse", "candidate_only_preservation_check", pass_fail(candidate_collapse_pass), "PASS")
    write_tsv(out_dir / "tep_err10619212_candidate_collapse_audit.tsv", rows, ["section", "metric", "value", "expected", "status"])
    return rows, stage11_stats, stage12_stats


def audit_lineage_integrity(out_dir: Path) -> List[Dict[str, Any]]:
    rows = []
    lineage_path = TEP_DIR / "lineage_manifest.json"
    inventory_path = TEP_DIR / "entity_inventory.json"
    validation_report_path = TEP_DIR / "validation_report.md"
    required_roles = ["observation", "normalization", "routing", "coding_interpretation", "noncoding_interpretation", "prioritization", "validation", "context"]
    def add(check: str, status: str, value: Any = "", details: str = "") -> None:
        rows.append({"check": check, "status": status, "value": value, "details": details})
    add("lineage_manifest_exists", pass_fail(lineage_path.exists()), lineage_path.exists(), str(lineage_path))
    add("entity_inventory_exists", pass_fail(inventory_path.exists()), inventory_path.exists(), str(inventory_path))
    add("validation_report_exists", pass_fail(validation_report_path.exists()), validation_report_path.exists(), str(validation_report_path))
    lineage_obj = load_json(lineage_path) if lineage_path.exists() else {}
    inventory_obj = load_json(inventory_path) if inventory_path.exists() else {}
    all_values = []
    all_keys = []
    for p, v in walk_json({"lineage": lineage_obj, "inventory": inventory_obj}):
        all_keys.append(p)
        if isinstance(v, (str, int, float, bool)) or v is None:
            all_values.append(str(v))
    joined_values = "\n".join(all_values).lower()
    joined_keys = "\n".join(all_keys).lower()
    for role in required_roles:
        present = role.lower() in joined_values or role.lower() in joined_keys
        add(f"required_role_present::{role}", pass_fail(present), present)
    checksum_present = "sha256" in joined_keys or "sha256" in joined_values
    add("source_artifact_checksums_present", pass_fail(checksum_present), checksum_present)
    edge_present = ("parent" in joined_keys or "parents" in joined_keys) and ("child" in joined_keys or "children" in joined_keys)
    add("parent_child_lineage_terms_present", pass_fail(edge_present), edge_present)
    if validation_report_path.exists():
        text = validation_report_path.read_text(encoding="utf-8", errors="replace")
        lower = text.lower()
        status_pass = "pass" in lower and not ("fail" in lower and "failed: 0" not in lower)
        criteria_failed_empty = "criteria_failed" not in lower or "[]" in lower or "failed: 0" in lower
        add("validation_report_status_pass_like", pass_fail(status_pass), status_pass)
        add("validation_report_failed_criteria_empty_like", pass_fail(criteria_failed_empty), criteria_failed_empty)
    else:
        add("validation_report_status_pass_like", "FAIL", False)
        add("validation_report_failed_criteria_empty_like", "FAIL", False)
    validation_mentions = [v for v in all_values if "pass" in v.lower() or "fail" in v.lower()]
    add("json_validation_status_mentions", "INFO", "; ".join(validation_mentions[:10]))
    write_tsv(out_dir / "tep_err10619212_lineage_integrity_audit.tsv", rows, ["check", "status", "value", "details"])
    return rows


def audit_stage13_context(out_dir: Path) -> List[Dict[str, Any]]:
    rows = []
    for role, stage, source, tep, kind in ARTIFACT_PAIRS:
        if stage != "Stage13":
            continue
        source_sha = sha256_file(source) if source.exists() else None
        tep_sha = sha256_file(tep) if tep.exists() else None
        rows.append({"artifact": source.name, "check": "processed_vs_tep_checksum", "source_exists": source.exists(), "tep_exists": tep.exists(), "source_sha256": source_sha, "tep_sha256": tep_sha, "status": pass_fail(source_sha == tep_sha if source_sha and tep_sha else False), "details": ""})
    manifest_path = TEP_DIR / "entities/context/stage_13_artifact_manifest.json"
    self_ref_findings = []
    if manifest_path.exists():
        try:
            obj = load_json(manifest_path)
            for p, v in walk_json(obj):
                if isinstance(v, dict):
                    text = json.dumps(v, sort_keys=True).lower()
                    if "stage_13_artifact_manifest" in text and '"exists": false' in text:
                        self_ref_findings.append((p, text[:500]))
        except Exception as exc:
            rows.append({"artifact": "stage_13_artifact_manifest.json", "check": "json_parse", "source_exists": "", "tep_exists": manifest_path.exists(), "source_sha256": "", "tep_sha256": "", "status": "FAIL", "details": repr(exc)})
    rows.append({"artifact": "stage_13_artifact_manifest.json", "check": "self_reference_exists_false", "source_exists": "", "tep_exists": manifest_path.exists(), "source_sha256": "", "tep_sha256": "", "status": "REVIEW" if self_ref_findings else "PASS", "details": "Found self-reference exists=False; review whether benign manifest-generation timing issue." if self_ref_findings else "No stage_13_artifact_manifest exists=False self-reference detected."})
    rows.append({"artifact": "stage13_context", "check": "authority_boundary", "source_exists": "", "tep_exists": "", "source_sha256": "", "tep_sha256": "", "status": "INFO", "details": "Stage13 is run-context provenance/audit context. Stage13 is not scientific evidence substrate and must not replace Stage07-Stage12 evidence."})
    write_tsv(out_dir / "tep_err10619212_stage13_context_audit.tsv", rows, ["artifact", "check", "source_exists", "tep_exists", "source_sha256", "tep_sha256", "status", "details"])
    return rows


def first_variant_id_matching(path: Path, col: str, predicate) -> Optional[str]:
    header = read_header(path)
    if not header or col not in header or "variant_id" not in header:
        return None
    v_idx = header.index("variant_id")
    c_idx = header.index(col)
    with path.open("r", encoding="utf-8", errors="replace") as f:
        next(f, None)
        for line in f:
            parts = line.rstrip("\n\r").split("\t")
            if max(v_idx, c_idx) < len(parts) and predicate(parts[c_idx]):
                return parts[v_idx]
    return None


def collect_trace_info(variant_ids: Sequence[str]) -> List[Dict[str, Any]]:
    variant_set = set(v for v in variant_ids if v)
    trace = {v: {"variant_id": v, "present_stage07": False, "present_stage08": False, "present_routing": "", "present_stage09_or_stage10": "", "present_stage11": False, "present_stage12": False, "priority_tier": "", "validation_required": "", "variant_origin": "", "source_interpretation_label": ""} for v in variant_set}
    def scan_presence(entity_key: str, path: Path, fields: Optional[Sequence[str]] = None) -> None:
        header = read_header(path)
        if "variant_id" not in header:
            return
        indices = {name: header.index(name) for name in fields or [] if name in header}
        v_idx = header.index("variant_id")
        with path.open("r", encoding="utf-8", errors="replace") as f:
            next(f, None)
            for line in f:
                parts = line.rstrip("\n\r").split("\t")
                if v_idx >= len(parts):
                    continue
                vid = parts[v_idx]
                if vid not in variant_set:
                    continue
                rec = trace[vid]
                if entity_key == "stage07":
                    rec["present_stage07"] = True
                elif entity_key == "stage08":
                    rec["present_stage08"] = True
                elif entity_key in {"coding", "splice", "noncoding"}:
                    current = set(filter(None, rec["present_routing"].split(",")))
                    current.add(entity_key)
                    rec["present_routing"] = ",".join(sorted(current))
                elif entity_key in {"stage09", "stage10"}:
                    current = set(filter(None, rec["present_stage09_or_stage10"].split(",")))
                    current.add(entity_key)
                    rec["present_stage09_or_stage10"] = ",".join(sorted(current))
                elif entity_key == "stage11":
                    rec["present_stage11"] = True
                    for name, idx in indices.items():
                        if idx < len(parts):
                            rec[name] = parts[idx]
                elif entity_key == "stage12":
                    rec["present_stage12"] = True
                    if "validation_required" in indices and indices["validation_required"] < len(parts):
                        rec["validation_required"] = normalize_bool(parts[indices["validation_required"]])
    scan_presence("stage07", TSV_PATHS["stage07"])
    scan_presence("stage08", TSV_PATHS["stage08_vdb_ready"])
    scan_presence("coding", TSV_PATHS["coding"])
    scan_presence("splice", TSV_PATHS["splice"])
    scan_presence("noncoding", TSV_PATHS["noncoding"])
    scan_presence("stage09", TSV_PATHS["stage09"])
    scan_presence("stage10", TSV_PATHS["stage10"])
    scan_presence("stage11", TSV_PATHS["stage11"], fields=["priority_tier", "variant_origin", "source_interpretation_label"])
    scan_presence("stage12", TSV_PATHS["stage12"], fields=["validation_required"])
    return list(trace.values())


def audit_trace_examples(out_dir: Path) -> None:
    random.seed(42)
    stage07_first = get_tsv_stats(TSV_PATHS["stage07"], first_n_variant_ids=10)["first_variant_ids"]
    targets = {
        "coding_variant": get_tsv_stats(TSV_PATHS["coding"], first_n_variant_ids=1)["first_variant_ids"][0],
        "splice_overlap_variant": None,
        "noncoding_variant": get_tsv_stats(TSV_PATHS["noncoding"], first_n_variant_ids=1)["first_variant_ids"][0],
        "validation_required_true_variant": first_variant_id_matching(TSV_PATHS["stage12"], "validation_required", lambda x: normalize_bool(x) == "True"),
        "validation_required_false_variant": first_variant_id_matching(TSV_PATHS["stage12"], "validation_required", lambda x: normalize_bool(x) == "False"),
        "uninterpretable_variant": first_variant_id_matching(TSV_PATHS["stage11"], "priority_tier", lambda x: "uninterpret" in x.lower() or "qc" in x.lower()),
    }
    coding = get_tsv_stats(TSV_PATHS["coding"], collect_variant_ids=True)["variant_ids"]
    splice = get_tsv_stats(TSV_PATHS["splice"], collect_variant_ids=True)["variant_ids"]
    if isinstance(coding, set) and isinstance(splice, set):
        overlap = sorted(coding & splice)
        targets["splice_overlap_variant"] = overlap[0] if overlap else None
    edge_variant_ids = [v for v in targets.values() if v]
    edge_rows = collect_trace_info(edge_variant_ids)
    label_by_variant = {v: k for k, v in targets.items() if v}
    for row in edge_rows:
        row["trace_label"] = label_by_variant.get(row["variant_id"], "")
    random_rows = collect_trace_info(stage07_first)
    for row in random_rows:
        row["trace_label"] = "random_stage07_first10"
    fieldnames = ["trace_label", "variant_id", "present_stage07", "present_stage08", "present_routing", "present_stage09_or_stage10", "present_stage11", "present_stage12", "priority_tier", "validation_required", "variant_origin", "source_interpretation_label"]
    write_tsv(out_dir / "tep_err10619212_random_variant_trace_examples.tsv", random_rows, fieldnames)
    write_tsv(out_dir / "tep_err10619212_edge_case_variant_trace_examples.tsv", edge_rows, fieldnames)


def build_scientific_summary(out_dir: Path, transport_rows: List[Dict[str, Any]], parity_rows: List[Dict[str, Any]], routing_summary: Dict[str, Any], column_rows: List[Dict[str, Any]], lineage_rows: List[Dict[str, Any]], stage13_rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    stage07_stats = get_tsv_stats(TSV_PATHS["stage07"])
    stage08_stats = get_tsv_stats(TSV_PATHS["stage08_vdb_ready"])
    stage09_stats = get_tsv_stats(TSV_PATHS["stage09"])
    stage10_stats = get_tsv_stats(TSV_PATHS["stage10"])
    stage11_stats = get_tsv_stats(TSV_PATHS["stage11"], distribution_cols=["priority_tier"])
    stage12_stats = get_tsv_stats(TSV_PATHS["stage12"], distribution_cols=["validation_required"])
    failures = []
    reviews = []
    for row in transport_rows:
        if row.get("sha256_match") is not True:
            failures.append(f"transport_sha256::{row.get('role')}")
    for row in parity_rows:
        if row.get("sets_equal") is not True:
            failures.append(f"variant_parity::{row.get('comparison')}")
    for row in column_rows:
        if row.get("present") is not True:
            failures.append(f"required_column::{row.get('entity')}::{row.get('column_or_group')}")
    for row in lineage_rows:
        if row.get("status") == "FAIL":
            failures.append(f"lineage::{row.get('check')}")
    for row in stage13_rows:
        if row.get("status") == "FAIL":
            failures.append(f"stage13::{row.get('check')}")
        if row.get("status") == "REVIEW":
            reviews.append(f"stage13::{row.get('check')}")
    if routing_summary.get("model_check") != "PASS":
        failures.append("stage08_routing_model")
    validation_dist = stage12_stats["distributions"].get("validation_required", {})
    priority_dist = stage11_stats["distributions"].get("priority_tier", {})
    candidate_collapse_pass = stage11_stats["row_count"] == stage07_stats["row_count"] and stage12_stats["row_count"] == stage07_stats["row_count"] and validation_dist.get("False", 0) > 0
    if not candidate_collapse_pass:
        failures.append("candidate_collapse_check")
    overall = "PASS_WITH_REVIEW_ITEMS" if reviews else "PASS"
    if failures:
        overall = "FAIL"
    summary = {"sample_id": SAMPLE_ID, "run_id": RUN_ID, "tep_name": TEP_NAME, "stage07_row_count": stage07_stats["row_count"], "stage07_variant_count": stage07_stats["variant_id_count"], "stage08_row_count": stage08_stats["row_count"], "stage08_variant_count": stage08_stats["variant_id_count"], "coding_count": routing_summary.get("coding_variant_id_count"), "splice_count": routing_summary.get("splice_variant_id_count"), "noncoding_count": routing_summary.get("noncoding_variant_id_count"), "stage09_count": stage09_stats["row_count"], "stage10_count": stage10_stats["row_count"], "stage11_count": stage11_stats["row_count"], "stage12_count": stage12_stats["row_count"], "priority_tier_distribution": priority_dist, "validation_required_distribution": validation_dist, "routing_overlap_summary": routing_summary, "candidate_collapse_status": pass_fail(candidate_collapse_pass), "stage13_context_status": "REVIEW" if reviews else "PASS", "probe_failures": failures, "probe_review_items": reviews, "overall_probe_status": overall, "scientific_pattern_note": "Expected ERR10619212 q1 WES epilepsy pattern: WES-scale variant universe, WES-compatible noncoding/coding/routing structure, epilepsy WES candidate signal shaped by depth and sample-specific evidence, reviewable moderate-priority subset, large low/common and uninterpretable/QC-limited background."}
    write_json(out_dir / "tep_err10619212_scientific_summary.json", summary)
    return summary


def write_certification_summary_md(out_dir: Path, scientific_summary: Dict[str, Any]) -> None:
    path = out_dir / "tep_err10619212_certification_summary.md"
    status = scientific_summary.get("overall_probe_status")
    failures = scientific_summary.get("probe_failures", [])
    reviews = scientific_summary.get("probe_review_items", [])
    lines = [
        "# ERR10619212 VAP-TEP Certification Probe Summary", "",
        "## Scope", "",
        f"TEP: `{TEP_NAME}`", "",
        f"Run: `{RUN_ID}`", "",
        f"Sample: `{SAMPLE_ID}`", "",
        "This file summarizes measurements produced by the MARK certification probe.",
        "It is not, by itself, a SAGE certification decision.", "",
        "## Overall Probe Status", "", f"```text\n{status}\n```", "",
        "## Key Counts", "",
        f"- Stage07 rows: `{scientific_summary.get('stage07_row_count')}`",
        f"- Stage07 variant IDs: `{scientific_summary.get('stage07_variant_count')}`",
        f"- Stage08 rows: `{scientific_summary.get('stage08_row_count')}`",
        f"- Stage08 variant IDs: `{scientific_summary.get('stage08_variant_count')}`",
        f"- Coding routing count: `{scientific_summary.get('coding_count')}`",
        f"- Splice routing count: `{scientific_summary.get('splice_count')}`",
        f"- Noncoding routing count: `{scientific_summary.get('noncoding_count')}`",
        f"- Stage09 rows: `{scientific_summary.get('stage09_count')}`",
        f"- Stage10 rows: `{scientific_summary.get('stage10_count')}`",
        f"- Stage11 rows: `{scientific_summary.get('stage11_count')}`",
        f"- Stage12 rows: `{scientific_summary.get('stage12_count')}`", "",
        "## Candidate-Collapse Status", "", f"```text\n{scientific_summary.get('candidate_collapse_status')}\n```", "",
        "## Stage13 Context Status", "", f"```text\n{scientific_summary.get('stage13_context_status')}\n```", "",
        "## Probe Failures", "",
    ]
    lines.extend([f"- `{f}`" for f in failures] if failures else ["No probe failures detected."])
    lines.extend(["", "## Probe Review Items", ""])
    lines.extend([f"- `{r}`" for r in reviews] if reviews else ["No probe review items detected."])
    lines.extend(["", "## Stage08 Routing Model", "", "Expected interpretation:", "", "```text", "Coding Partition", "Noncoding Partition", "Splice Overlay", "```", "", "Routing overlap summary is available in:", "", "```text", "tep_err10619212_stage08_routing_overlap_audit.tsv", "```", "", "## Important Semantic Note", "", "Physical equivalence of Stage08 selected-transcript and VDB-ready artifacts in VAP v1", "does not imply semantic equivalence forever. Both artifact identities must remain preserved.", "", "## Output Files", "", "See all TSV and JSON audit outputs in this directory.", ""])
    path.write_text("\n".join(lines), encoding="utf-8")


def validate_starting_conditions(repo_root: Path) -> None:
    if not (repo_root / "results").exists():
        raise FileNotFoundError("No results/ directory found. Run from VAP repo root.")
    if not PROCESSED_DIR.exists():
        raise FileNotFoundError(f"Processed truth directory not found: {PROCESSED_DIR}")
    if not TEP_DIR.exists():
        raise FileNotFoundError(f"TEP directory not found: {TEP_DIR}")


def main() -> int:
    repo_root = Path.cwd().resolve()
    validate_starting_conditions(repo_root)
    out_dir = ensure_output_dir(repo_root)
    print(f"[INFO] Repo root: {repo_root}")
    print(f"[INFO] Processed truth directory: {PROCESSED_DIR}")
    print(f"[INFO] TEP directory: {TEP_DIR}")
    print(f"[INFO] Output directory: {out_dir}")
    print("[INFO] Starting transport fidelity audit...")
    transport_rows = audit_transport_fidelity(out_dir)
    print("[INFO] Starting required column audit...")
    column_rows = audit_required_columns(out_dir)
    print("[INFO] Starting variant parity audit...")
    parity_rows = audit_variant_parity(out_dir)
    print("[INFO] Starting Stage08 routing overlap audit...")
    routing_summary = audit_stage08_routing_overlap(out_dir)
    print("[INFO] Starting candidate-collapse audit...")
    candidate_rows, _stage11_stats, _stage12_stats = audit_candidate_collapse(out_dir)
    print("[INFO] Starting lineage integrity audit...")
    lineage_rows = audit_lineage_integrity(out_dir)
    print("[INFO] Starting Stage13 context audit...")
    stage13_rows = audit_stage13_context(out_dir)
    print("[INFO] Starting trace example audit...")
    try:
        audit_trace_examples(out_dir)
    except Exception as exc:
        (out_dir / "tep_err10619212_trace_examples_error.txt").write_text(repr(exc), encoding="utf-8")
        print(f"[WARN] Trace example generation failed: {exc!r}")
    print("[INFO] Building scientific summary...")
    scientific_summary = build_scientific_summary(out_dir, transport_rows, parity_rows, routing_summary, column_rows, lineage_rows, stage13_rows)
    write_certification_summary_md(out_dir, scientific_summary)
    print("\nAudit complete.\n")
    print(f"Outputs written to:\n{out_dir}\n")
    print("Emitted files:")
    for p in sorted(out_dir.iterdir()):
        print(f"  {p.name}")
    print(f"\nOverall probe status: {scientific_summary.get('overall_probe_status')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
