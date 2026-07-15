\
from __future__ import annotations

from pipeline.stage_07_annotate_variants import (
    _build_vep_command,
    _centralized_annotation_runtime,
)


def _state() -> dict:
    return {
        "execution_provenance": {
            "contract_status": "pass",
            "annotation_environment": {
                "contract_status": "pass",
                "software": {
                    "resolved_executable": "/resolved/vep",
                },
                "cache": {
                    "configured_cache_directory": "/cache/root",
                    "resolved_cache_directory": (
                        "/cache/root/homo_sapiens/115_GRCh38"
                    ),
                    "observed_assembly": "GRCh38",
                },
            },
        }
    }


def test_stage07_consumes_centralized_annotation_runtime() -> None:
    runtime = _centralized_annotation_runtime(
        config={},
        state=_state(),
        annotation_engine="vep",
    )

    assert runtime == {
        "vep_executable_resolved": "/resolved/vep",
        "vep_cache_dir": "/cache/root",
        "vep_cache_resolved": (
            "/cache/root/homo_sapiens/115_GRCh38"
        ),
        "vep_assembly": "GRCh38",
    }


def test_vep_command_uses_centralized_paths() -> None:
    config = {
        "tools": {
            "vep": {
                "executable": "/configured/vep",
                "cache_dir": "/configured/cache",
                "assembly": "GRCh37",
                "fork": 2,
            }
        },
        "annotation": {
            "include_clinvar": False,
            "include_population_frequencies": False,
        },
    }
    runtime = _centralized_annotation_runtime(
        config=config,
        state=_state(),
        annotation_engine="vep",
    )

    command = _build_vep_command(
        config,
        input_vcf="input.vcf",
        output_vcf="output.vcf",
        runtime_requirements=runtime,
    )

    assert command[0] == "/resolved/vep"
    assert command[command.index("--dir_cache") + 1] == "/cache/root"
    assert command[command.index("--assembly") + 1] == "GRCh38"
