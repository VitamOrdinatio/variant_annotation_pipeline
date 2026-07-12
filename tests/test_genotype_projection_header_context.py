from __future__ import annotations

import json
from pathlib import Path

from tests.test_genotype_projection import project


def test_header_context_preserves_samples_formats_and_contigs(tmp_path: Path) -> None:
    output, _ = project(tmp_path)
    payload = json.loads((output / "genotype_source_header_context.json").read_text(encoding="utf-8"))
    assert payload["schema_version"] == "genotype_source_header_context_v1"
    assert payload["sample_columns"] == ["HG002"]
    assert payload["reference_context"]["reference_build"] == "GRCh38"
    assert payload["reference_context"]["reference_declaration"] == "GRCh38"
    assert [item["id"] for item in payload["format_definitions"]] == ["GT", "AD", "DP", "GQ", "PL", "FT", "XY"]
    assert payload["contig_declarations"][0]["id"] == "1"
    assert payload["contig_declarations"][0]["length"] == "248956422"
