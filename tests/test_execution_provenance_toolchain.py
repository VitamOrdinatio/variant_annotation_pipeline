\
from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

import pytest

from src.config_loader import load_config
from src.execution_provenance import (
    ExecutionProvenanceError,
    assert_contract_pass,
    resolve_execution_provenance,
    resolve_toolchain_environment,
)


CONFIG_PATH = "config/execution_provenance/config.mark.err10619300.execution_provenance.yaml"


def _write_executable(path: Path, body: str) -> None:
    path.write_text(
        "#!/usr/bin/env bash\nset -eu\n" + body + "\n",
        encoding="utf-8",
    )
    path.chmod(0o755)


def _synthetic_environment(tmp_path: Path) -> dict:
    tools_dir = tmp_path / "tools"
    tools_dir.mkdir()

    bwa = tools_dir / "bwa"
    samtools = tools_dir / "samtools"
    gatk = tools_dir / "gatk"
    vep = tools_dir / "vep"
    java = tools_dir / "java"
    perl = tools_dir / "perl"

    _write_executable(
        bwa,
        'echo "Version: 0.7.17" >&2; exit 1',
    )
    _write_executable(
        samtools,
        'echo "samtools 1.19.2"',
    )
    _write_executable(
        gatk,
        'echo "The Genome Analysis Toolkit (GATK) v4.5.0.0"',
    )
    _write_executable(
        vep,
        'echo "ensembl-vep: 115.2"',
    )
    _write_executable(
        java,
        'echo \'openjdk version "21.0.11"\' >&2',
    )
    _write_executable(
        perl,
        'echo "This is perl 5, version 38, subversion 2 (v5.38.2)"',
    )

    resources = tmp_path / "resources"
    resources.mkdir()
    fasta = resources / "reference.fa"
    fai = resources / "reference.fa.fai"
    dictionary = resources / "reference.dict"
    mitocarta = resources / "MitoCarta.tsv"
    epilepsy = resources / "Genes4Epilepsy.tsv"

    fasta.write_text(">1\nA\n", encoding="utf-8")
    fai.write_text("1\t1\t3\t1\t2\n", encoding="utf-8")
    dictionary.write_text(
        "@HD\tVN:1.6\n@SQ\tSN:1\tLN:1\n",
        encoding="utf-8",
    )
    mitocarta.write_text(
        "gene_id\tgene_symbol\n1\tGENE1\n",
        encoding="utf-8",
    )
    epilepsy.write_text(
        "gene_id\tgene_symbol\n2\tGENE2\n",
        encoding="utf-8",
    )

    bwa_prefix = resources / "reference.fa"
    for suffix in (".amb", ".ann", ".bwt", ".pac", ".sa"):
        Path(str(bwa_prefix) + suffix).write_text(
            suffix + "\n",
            encoding="utf-8",
        )

    cache = tmp_path / "vep_cache" / "homo_sapiens" / "115_GRCh38"
    cache.mkdir(parents=True)
    (cache / "info.txt").write_text("cache\n", encoding="utf-8")

    return {
        "executables": {
            "bwa": bwa,
            "samtools": samtools,
            "gatk": gatk,
            "vep": vep,
            "java": java,
            "perl": perl,
        },
        "resources": {
            "fasta": fasta,
            "fai": fai,
            "dictionary": dictionary,
            "bwa_prefix": bwa_prefix,
            "mitocarta": mitocarta,
            "epilepsy": epilepsy,
            "cache_root": tmp_path / "vep_cache",
        },
    }


def _configured_fixture(tmp_path: Path) -> tuple[dict, dict]:
    config = deepcopy(load_config(CONFIG_PATH))
    env = _synthetic_environment(tmp_path)

    config["tools"]["bwa"]["executable"] = str(
        env["executables"]["bwa"]
    )
    config["tools"]["samtools"]["executable"] = str(
        env["executables"]["samtools"]
    )
    config["tools"]["gatk"]["executable"] = str(
        env["executables"]["gatk"]
    )
    config["tools"]["vep"]["executable"] = str(
        env["executables"]["vep"]
    )
    config["tools"]["vep"]["cache_dir"] = str(
        env["resources"]["cache_root"]
    )
    config["tools"]["vep"]["offline"] = True

    config["reference"]["fasta_path"] = str(
        env["resources"]["fasta"]
    )
    config["reference"]["fasta_index"] = str(
        env["resources"]["fai"]
    )
    config["reference"]["sequence_dictionary"] = str(
        env["resources"]["dictionary"]
    )
    config["reference"]["bwa_index_prefix"] = str(
        env["resources"]["bwa_prefix"]
    )
    config["gene_sets"]["mitocarta_path"] = str(
        env["resources"]["mitocarta"]
    )
    config["gene_sets"]["genes4epilepsy_path"] = str(
        env["resources"]["epilepsy"]
    )

    which_map = {
        "java": str(env["executables"]["java"]),
        "perl": str(env["executables"]["perl"]),
    }

    def which_resolver(name: str) -> str | None:
        return which_map.get(name)

    return config, {"which_resolver": which_resolver}


def test_complete_toolchain_resolves_with_synthetic_tools(
    tmp_path: Path,
) -> None:
    config, kwargs = _configured_fixture(tmp_path)

    result = resolve_toolchain_environment(config, **kwargs)

    assert result["contract_status"] == "pass"
    assert result["failed_tools"] == []
    assert result["tools"]["bwa"]["observed_version"] == "0.7.17"
    assert result["tools"]["samtools"]["observed_version"] == "1.19.2"
    assert result["tools"]["gatk"]["observed_version"] == "4.5.0.0"
    assert result["tools"]["vep"]["observed_version"] == "115.2"
    assert result["tools"]["java"]["observed_version"] == "21.0.11"
    assert result["tools"]["perl"]["observed_version"] == "5.38.2"
    assert result["tools"]["python"]["version_status"] == "pass"


def test_full_execution_provenance_resolves_and_passes(
    tmp_path: Path,
) -> None:
    config, kwargs = _configured_fixture(tmp_path)

    result = resolve_execution_provenance(config, **kwargs)

    assert result["contract_status"] == "pass"
    assert result["failed_surfaces"] == []
    assert result["resolution_mode"] == "live_runtime_resolution"
    assert result["provenance_completeness"] == "complete"
    assert result["annotation_environment"]["contract_status"] == "pass"
    assert result["resource_environment"]["contract_status"] == "pass"
    assert_contract_pass(result) is result


def test_version_mismatch_is_aggregated(
    tmp_path: Path,
) -> None:
    config, kwargs = _configured_fixture(tmp_path)
    config["execution_provenance"]["toolchain"]["samtools"][
        "declared_version"
    ] = "1.18.0"

    result = resolve_execution_provenance(config, **kwargs)

    assert result["contract_status"] == "fail"
    assert result["failed_surfaces"] == ["toolchain_environment"]
    assert result["toolchain_environment"]["failed_tools"] == [
        "samtools"
    ]

    with pytest.raises(
        ExecutionProvenanceError,
        match="samtools: expected=1.18.0; observed=1.19.2",
    ):
        assert_contract_pass(result)


def test_java_major_mismatch_fails(
    tmp_path: Path,
) -> None:
    config, kwargs = _configured_fixture(tmp_path)
    config["execution_provenance"]["toolchain"]["java"][
        "declared_major_version"
    ] = "17"

    result = resolve_toolchain_environment(config, **kwargs)

    assert result["contract_status"] == "fail"
    assert result["failed_tools"] == ["java"]


def test_missing_required_executable_fails(
    tmp_path: Path,
) -> None:
    config, kwargs = _configured_fixture(tmp_path)
    config["tools"]["gatk"]["executable"] = str(
        tmp_path / "missing-gatk"
    )

    with pytest.raises(
        ExecutionProvenanceError,
        match="Configured executable does not exist",
    ):
        resolve_toolchain_environment(config, **kwargs)


def test_unparseable_tool_version_fails(
    tmp_path: Path,
) -> None:
    config, kwargs = _configured_fixture(tmp_path)
    vep = Path(config["tools"]["vep"]["executable"])
    _write_executable(
        vep,
        'echo "# ENSEMBL VARIANT EFFECT PREDICTOR #"',
    )

    with pytest.raises(
        ExecutionProvenanceError,
        match="Unable to parse VEP version",
    ):
        resolve_toolchain_environment(config, **kwargs)


def test_offline_contract_failure_is_reported(
    tmp_path: Path,
) -> None:
    config, kwargs = _configured_fixture(tmp_path)
    config["tools"]["vep"]["offline"] = False

    result = resolve_execution_provenance(config, **kwargs)

    assert result["contract_status"] == "fail"
    assert result["failed_surfaces"] == ["annotation_environment"]
    assert (
        "offline execution declared but tools.vep.offline=false"
        in result["annotation_environment"]["failures"]
    )


def test_resolved_provenance_is_json_serializable(
    tmp_path: Path,
) -> None:
    config, kwargs = _configured_fixture(tmp_path)

    result = resolve_execution_provenance(config, **kwargs)
    rendered = json.dumps(result, sort_keys=True)

    assert '"contract_status": "pass"' in rendered


def test_samtools_non_utf8_build_metadata_does_not_block_resolution(
    tmp_path: Path,
) -> None:
    config, kwargs = _configured_fixture(tmp_path)

    samtools = Path(config["tools"]["samtools"]["executable"])
    samtools.write_bytes(
        b"#!/usr/bin/env python3\n"
        b"import sys\n"
        b"sys.stdout.buffer.write("
        b"b'samtools 1.19.2\\n"
        b"Compiler flags: -ffile-prefix-map="
        b"\\xabBUILDPATH\\xbb=.\\n')\n"
    )
    samtools.chmod(0o755)

    result = resolve_toolchain_environment(
        config,
        **kwargs,
    )

    assert result["contract_status"] == "pass"
    assert (
        result["tools"]["samtools"]["observed_version"]
        == "1.19.2"
    )