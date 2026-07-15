from __future__ import annotations

import hashlib
import json
from pathlib import Path

from scripts.tep.build_vap_tep_entities import EXECUTION_PROVENANCE_ARTIFACT_SPEC, resolve_artifact_specs
from scripts.tep.validate_vap_tep import check_execution_provenance_transport


def test_builder_selects_execution_provenance_when_present(tmp_path: Path) -> None:
    processed = tmp_path / "processed"
    metadata = tmp_path / "metadata"
    processed.mkdir(); metadata.mkdir()
    (metadata / "execution_provenance.json").write_text(json.dumps({"schema_version": "1.0.0", "contract_status": "pass", "resolution_mode": "live_runtime_resolution"}) + "\n", encoding="utf-8")
    specs = resolve_artifact_specs(processed, metadata)
    matches = [s for s in specs if s.source_artifact_role == "execution_provenance"]
    assert matches == [EXECUTION_PROVENANCE_ARTIFACT_SPEC]
    assert matches[0].entity_role == "context_sidecar"
    assert matches[0].entity_subdir == "context"
    assert matches[0].source_root == "metadata"


def test_legacy_builder_omits_missing_execution_provenance(tmp_path: Path) -> None:
    processed = tmp_path / "processed"
    metadata = tmp_path / "metadata"
    processed.mkdir(); metadata.mkdir()
    specs = resolve_artifact_specs(processed, metadata)
    assert not any(s.source_artifact_role == "execution_provenance" for s in specs)


def test_validator_accepts_transport_and_lineage(tmp_path: Path) -> None:
    package = tmp_path / "tep"
    context = package / "entities" / "context"
    context.mkdir(parents=True)
    receipt = context / "execution_provenance.json"
    receipt.write_text(json.dumps({"schema_version": "1.0.0", "contract_status": "pass", "resolution_mode": "live_runtime_resolution", "provenance_completeness": "complete"}, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    digest = hashlib.sha256(receipt.read_bytes()).hexdigest()
    manifest = {"entities": [{"entity_id": "context_sidecar", "entity_role": "context_sidecar", "source_artifacts": [{"source_artifact_role": "execution_provenance", "transport_path": "entities/context/execution_provenance.json", "source_artifact_sha256": digest}]}], "lineage_edges": [{"parent_entity_id": "context_sidecar", "child_entity_id": "lineage_manifest", "relationship": "indexed_by"}]}
    checks = check_execution_provenance_transport(manifest, package)
    assert [c.status for c in checks] == ["PASS", "PASS", "PASS", "PASS"]


def test_validator_is_legacy_compatible(tmp_path: Path) -> None:
    assert check_execution_provenance_transport({"entities": [], "lineage_edges": []}, tmp_path) == []
