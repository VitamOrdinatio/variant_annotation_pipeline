
from __future__ import annotations

import hashlib
from pathlib import Path

from src.execution_provenance import (
    resolve_bwa_index,
    resolve_resource_environment,
    resource_record,
    validate_reference_set_coherence,
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_resource_checksum_contract(tmp_path: Path) -> None:
    path = tmp_path / "resource.tsv"
    path.write_text("a\tb\n1\t2\n", encoding="utf-8")

    matched = resource_record(
        role="fixture",
        configured_path=path,
        declared_sha256=_sha256(path),
    )
    assert matched["checksum_status"] == "pass"

    mismatched = resource_record(
        role="fixture",
        configured_path=path,
        declared_sha256="0" * 64,
    )
    assert mismatched["checksum_status"] == "fail"
    assert mismatched["contract_status"] == "fail"

    recorded = resource_record(
        role="fixture",
        configured_path=path,
    )
    assert recorded["checksum_status"] == "recorded"
    assert recorded["contract_status"] == "pass"


def test_bwa_aggregate_checksum_contract(tmp_path: Path) -> None:
    prefix = tmp_path / "GRCh38"
    for suffix in (".amb", ".ann", ".bwt", ".pac", ".sa"):
        Path(str(prefix) + suffix).write_text(
            suffix + "\n",
            encoding="utf-8",
        )

    initial = resolve_bwa_index(prefix)
    declared = initial["observed_aggregate_sha256"]

    matched = resolve_bwa_index(
        prefix,
        declared_aggregate_sha256=declared,
    )
    assert matched["contract_status"] == "pass"

    mismatched = resolve_bwa_index(
        prefix,
        declared_aggregate_sha256="f" * 64,
    )
    assert mismatched["contract_status"] == "fail"


def test_reference_set_coherence(tmp_path: Path) -> None:
    fasta = tmp_path / "reference.fa"
    fai = tmp_path / "reference.fa.fai"
    dictionary = tmp_path / "reference.dict"

    fasta.write_text(">1\nA\n>2\nC\n", encoding="utf-8")
    fai.write_text("1\t1\t0\t1\t2\n2\t1\t3\t1\t2\n", encoding="utf-8")
    dictionary.write_text(
        "@SQ\tSN:1\tLN:1\n@SQ\tSN:2\tLN:1\n",
        encoding="utf-8",
    )

    passed = validate_reference_set_coherence(
        fasta_path=fasta,
        fai_path=fai,
        dictionary_path=dictionary,
    )
    assert passed["contract_status"] == "pass"

    fai.write_text("2\t1\t0\t1\t2\n1\t1\t3\t1\t2\n", encoding="utf-8")
    failed = validate_reference_set_coherence(
        fasta_path=fasta,
        fai_path=fai,
        dictionary_path=dictionary,
    )
    assert failed["contract_status"] == "fail"


def test_resource_environment_aggregates_failure(
    tmp_path: Path,
) -> None:
    fasta = tmp_path / "reference.fa"
    fai = tmp_path / "reference.fa.fai"
    dictionary = tmp_path / "reference.dict"
    mitocarta = tmp_path / "mitocarta.tsv"
    epilepsy = tmp_path / "epilepsy.tsv"

    fasta.write_text(">1\nA\n", encoding="utf-8")
    fai.write_text("1\t1\t0\t1\t2\n", encoding="utf-8")
    dictionary.write_text("@SQ\tSN:1\tLN:1\n", encoding="utf-8")
    mitocarta.write_text("gene_id\tgene_symbol\n1\tA\n", encoding="utf-8")
    epilepsy.write_text("gene_id\tgene_symbol\n2\tB\n", encoding="utf-8")

    prefix = tmp_path / "reference.fa"
    for suffix in (".amb", ".ann", ".bwt", ".pac", ".sa"):
        Path(str(prefix) + suffix).write_text(
            suffix + "\n",
            encoding="utf-8",
        )

    config = {
        "reference": {
            "fasta_path": str(fasta),
            "fasta_index": str(fai),
            "sequence_dictionary": str(dictionary),
            "bwa_index_prefix": str(prefix),
        },
        "gene_sets": {
            "mitocarta_path": str(mitocarta),
            "genes4epilepsy_path": str(epilepsy),
        },
        "execution_provenance": {
            "resource_environment": {
                "reference_fasta": {
                    "configured_from": "reference.fasta_path",
                    "checksum_policy": "sha256",
                    "declared_sha256": _sha256(fasta),
                },
                "fasta_index": {
                    "configured_from": "reference.fasta_index",
                    "checksum_policy": "sha256",
                    "declared_sha256": "0" * 64,
                },
                "sequence_dictionary": {
                    "configured_from": "reference.sequence_dictionary",
                    "checksum_policy": "sha256",
                    "declared_sha256": _sha256(dictionary),
                },
                "bwa_index": {
                    "configured_from": "reference.bwa_index_prefix",
                    "checksum_policy": "sha256_constituents",
                },
                "mitocarta": {
                    "configured_from": "gene_sets.mitocarta_path",
                    "checksum_policy": "sha256",
                    "declared_sha256": _sha256(mitocarta),
                },
                "genes4epilepsy": {
                    "configured_from": "gene_sets.genes4epilepsy_path",
                    "checksum_policy": "sha256",
                    "declared_sha256": _sha256(epilepsy),
                },
            }
        },
    }

    result = resolve_resource_environment(config)
    assert result["contract_status"] == "fail"
    assert result["failed_resources"] == ["fasta_index"]
