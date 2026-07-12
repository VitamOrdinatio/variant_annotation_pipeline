from __future__ import annotations

import json
from pathlib import Path

from tests.test_genotype_projection import project


def test_summary_reconciles_counts(tmp_path: Path) -> None:
    output, _ = project(tmp_path)
    payload = json.loads((output / "genotype_projection_summary.json").read_text(encoding="utf-8"))
    assert payload["schema_version"] == "genotype_projection_summary_v1"
    assert payload["source_vcf"]["source_record_count"] == 5
    assert payload["source_vcf"]["irreparably_malformed_record_count"] == 0
    assert payload["counts"]["genotype_observation_row_count"] == 5
    assert payload["counts"]["complete_no_call_count"] == 1
    assert payload["counts"]["multiallelic_record_count"] == 1
    assert payload["counts"]["phased_gt_count"] == 1
    assert payload["counts"]["format_sample_mismatch_count"] == 1


def test_three_artifacts_are_byte_deterministic(tmp_path: Path) -> None:
    first, _ = project(tmp_path / "first")
    second, _ = project(tmp_path / "second")
    for filename in ["genotype_observations.tsv", "genotype_projection_summary.json",
                     "genotype_source_header_context.json"]:
        assert (first / filename).read_bytes() == (second / filename).read_bytes()
