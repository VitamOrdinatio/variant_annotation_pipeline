\
from __future__ import annotations

import os
from pathlib import Path
import subprocess
import pytest

from src.execution_provenance import (
    ExecutionProvenanceError,
    _decode_probe_stream,
    _run_probe,    
    compare_version,
    discover_vep_cache,
    parse_bwa_version,
    parse_gatk_version,
    parse_java_version,
    parse_perl_version,
    parse_samtools_version,
    parse_vep_version,
    resolve_bwa_index,
    resolve_config_value,
    resolve_executable,
    resolve_resource_environment,
    resource_record,
)


def test_version_parsers() -> None:
    assert parse_bwa_version("Version: 0.7.17-r1188") == "0.7.17-r1188"
    assert parse_samtools_version("samtools 1.19.2\nUsing htslib") == "1.19.2"
    assert parse_gatk_version(
        "The Genome Analysis Toolkit (GATK) v4.5.0.0"
    ) == "4.5.0.0"
    assert parse_java_version(
        'openjdk version "21.0.11" 2026-04-15'
    ) == "21.0.11"
    assert parse_perl_version(
        "This is perl 5, version 38, subversion 2 (v5.38.2)"
    ) == "5.38.2"
    assert parse_vep_version("ensembl-vep: 115.2") == "115.2"


def test_unparseable_version_fails() -> None:
    with pytest.raises(
        ExecutionProvenanceError,
        match="Unable to parse VEP version",
    ):
        parse_vep_version("# ENSEMBL VARIANT EFFECT PREDICTOR #")


def test_version_policies() -> None:
    assert compare_version(
        declared_version="1.19.2",
        declared_major_version=None,
        observed_version="1.19.2",
        policy="exact",
    ) == ("pass", "exact_match")

    status, detail = compare_version(
        declared_version="1.19.2",
        declared_major_version=None,
        observed_version="1.20.0",
        policy="exact",
    )
    assert status == "fail"
    assert "expected=1.19.2" in detail

    assert compare_version(
        declared_version=None,
        declared_major_version="21",
        observed_version="21.0.11",
        policy="major",
    ) == ("pass", "major_match")

    assert compare_version(
        declared_version=None,
        declared_major_version=None,
        observed_version="5.38.2",
        policy="record_only",
    ) == ("pass", "record_only")


def test_resolve_config_value() -> None:
    config = {"tools": {"bwa": {"executable": "bwa"}}}
    assert resolve_config_value(
        config,
        "tools.bwa.executable",
    ) == "bwa"

    with pytest.raises(
        ExecutionProvenanceError,
        match="Configured provenance source is missing",
    ):
        resolve_config_value(config, "tools.vep.executable")


def test_resolve_absolute_executable(tmp_path: Path) -> None:
    executable = tmp_path / "tool"
    executable.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
    executable.chmod(0o755)

    assert resolve_executable(str(executable)) == str(
        executable.resolve()
    )


def test_resolve_non_executable_fails(tmp_path: Path) -> None:
    executable = tmp_path / "tool"
    executable.write_text("not executable\n", encoding="utf-8")

    with pytest.raises(
        ExecutionProvenanceError,
        match="not executable",
    ):
        resolve_executable(str(executable))


def test_resource_record_hashes_file(tmp_path: Path) -> None:
    resource = tmp_path / "resource.tsv"
    resource.write_text("gene_id\tgene_symbol\n1\tGENE\n", encoding="utf-8")

    record = resource_record(
        role="gene_set",
        configured_path=resource,
    )
    assert record["size_bytes"] == resource.stat().st_size
    assert len(record["sha256"]) == 64
    assert record["contract_status"] == "pass"


def test_bwa_index_constituents_and_aggregate(tmp_path: Path) -> None:
    prefix = tmp_path / "GRCh38"
    for suffix in (".amb", ".ann", ".bwt", ".pac", ".sa"):
        Path(str(prefix) + suffix).write_text(
            f"{suffix}\n",
            encoding="utf-8",
        )

    record_1 = resolve_bwa_index(prefix)
    record_2 = resolve_bwa_index(prefix)

    assert record_1["constituent_count"] == 5
    assert len(record_1["aggregate_sha256"]) == 64
    assert record_1["aggregate_sha256"] == (
        record_2["aggregate_sha256"]
    )


def test_missing_bwa_index_constituent_fails(tmp_path: Path) -> None:
    prefix = tmp_path / "GRCh38"
    for suffix in (".amb", ".ann", ".bwt", ".pac"):
        Path(str(prefix) + suffix).write_text(
            f"{suffix}\n",
            encoding="utf-8",
        )

    with pytest.raises(
        ExecutionProvenanceError,
        match="Missing BWA index constituents",
    ):
        resolve_bwa_index(prefix)


def test_discover_vep_cache(tmp_path: Path) -> None:
    cache = tmp_path / "homo_sapiens" / "115_GRCh38"
    cache.mkdir(parents=True)
    (cache / "info.txt").write_text("cache\n", encoding="utf-8")

    result = discover_vep_cache(
        cache_dir=tmp_path,
        species="homo_sapiens",
        release="115",
        assembly="GRCh38",
    )

    assert result["observed_cache_release"] == "115"
    assert result["resolved_cache_directory"] == str(cache.resolve())


def test_post_vep_fixture_resolution_is_non_live() -> None:
    from src.execution_provenance import resolve_execution_provenance

    result = resolve_execution_provenance(
        {"mode": {"execution_mode": "post_vep_fixture"}}
    )

    assert result["resolution_mode"] == "retained_source_provenance"
    assert result["provenance_completeness"] == "legacy_partial"
    assert result["contract_status"] == "not_applicable"


def test_resolve_resource_environment(tmp_path: Path) -> None:
    resources = {}

    fasta = tmp_path / "reference.fa"
    fasta.write_text(">1\nA\n", encoding="utf-8")
    resources["reference.fa"] = str(fasta)

    fai = tmp_path / "reference.fa.fai"
    fai.write_text("1\t1\t3\t1\t2\n", encoding="utf-8")
    resources["reference.fa.fai"] = str(fai)

    dictionary = tmp_path / "reference.dict"
    dictionary.write_text(
        "@HD\tVN:1.6\n@SQ\tSN:1\tLN:1\n",
        encoding="utf-8",
    )
    resources["reference.dict"] = str(dictionary)

    mitocarta = tmp_path / "mitocarta.tsv"
    mitocarta.write_text(
        "gene_id\tgene_symbol\n1\tGENE1\n",
        encoding="utf-8",
    )
    resources["mitocarta.tsv"] = str(mitocarta)

    epilepsy = tmp_path / "epilepsy.tsv"
    epilepsy.write_text(
        "gene_id\tgene_symbol\n2\tGENE2\n",
        encoding="utf-8",
    )
    resources["epilepsy.tsv"] = str(epilepsy)

    prefix = tmp_path / "bwa" / "GRCh38"
    prefix.parent.mkdir()
    for suffix in (".amb", ".ann", ".bwt", ".pac", ".sa"):
        Path(str(prefix) + suffix).write_text(
            suffix + "\n",
            encoding="utf-8",
        )

    config = {
        "reference": {
            "fasta_path": resources["reference.fa"],
            "fasta_index": resources["reference.fa.fai"],
            "sequence_dictionary": resources["reference.dict"],
            "bwa_index_prefix": str(prefix),
        },
        "gene_sets": {
            "mitocarta_path": resources["mitocarta.tsv"],
            "genes4epilepsy_path": resources["epilepsy.tsv"],
        },
        "execution_provenance": {
            "resource_environment": {
                "reference_fasta": {
                    "configured_from": "reference.fasta_path",
                    "checksum_policy": "sha256",
                },
                "fasta_index": {
                    "configured_from": "reference.fasta_index",
                    "checksum_policy": "sha256",
                },
                "sequence_dictionary": {
                    "configured_from": "reference.sequence_dictionary",
                    "checksum_policy": "sha256",
                },
                "bwa_index": {
                    "configured_from": "reference.bwa_index_prefix",
                    "checksum_policy": "sha256_constituents",
                },
                "mitocarta": {
                    "configured_from": "gene_sets.mitocarta_path",
                    "checksum_policy": "sha256",
                },
                "genes4epilepsy": {
                    "configured_from": "gene_sets.genes4epilepsy_path",
                    "checksum_policy": "sha256",
                },
            }
        },
    }

    result = resolve_resource_environment(config)
    assert result["contract_status"] == "pass"
    assert set(result["resources"]) == {
        "reference_fasta",
        "fasta_index",
        "sequence_dictionary",
        "bwa_index",
        "mitocarta",
        "genes4epilepsy",
    }


def test_decode_probe_stream_replaces_invalid_utf8() -> None:
    raw = (
        b"samtools 1.19.2\n"
        b"Compiler flags: -ffile-prefix-map="
        b"\xabBUILDPATH\xbb=.\n"
    )

    decoded = _decode_probe_stream(raw)

    assert "samtools 1.19.2" in decoded
    assert "BUILDPATH" in decoded
    assert "\ufffd" in decoded


def test_run_probe_accepts_non_utf8_tool_output() -> None:
    def command_runner(
        command,
        *,
        capture_output,
        text,
        check,
    ):
        assert command == ["samtools", "--version"]
        assert capture_output is True
        assert text is False
        assert check is False

        return subprocess.CompletedProcess(
            args=command,
            returncode=0,
            stdout=(
                b"samtools 1.19.2\n"
                b"Using htslib 1.19.1\n"
                b"Compiler flags: -ffile-prefix-map="
                b"\xabBUILDPATH\xbb=.\n"
            ),
            stderr=b"",
        )

    output = _run_probe(
        ["samtools", "--version"],
        command_runner=command_runner,
    )

    assert parse_samtools_version(output) == "1.19.2"
    assert "BUILDPATH" in output


def test_run_probe_accepts_legacy_string_test_output() -> None:
    def command_runner(
        command,
        *,
        capture_output,
        text,
        check,
    ):
        return subprocess.CompletedProcess(
            args=command,
            returncode=0,
            stdout="samtools 1.19.2\n",
            stderr="",
        )

    output = _run_probe(
        ["samtools", "--version"],
        command_runner=command_runner,
    )

    assert parse_samtools_version(output) == "1.19.2"