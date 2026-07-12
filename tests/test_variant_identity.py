from __future__ import annotations

import pipeline.stage_07_annotate_variants as stage07
from pipeline.variant_identity import build_variant_id


def test_build_variant_id_preserves_standard_snv() -> None:
    assert build_variant_id("1", "895427", "G", "C") == "1:895427:G:C"


def test_build_variant_id_preserves_insertion_representation() -> None:
    assert build_variant_id("15", "89333596", "T", "TTGC") == (
        "15:89333596:T:TTGC"
    )


def test_build_variant_id_preserves_deletion_representation() -> None:
    assert build_variant_id("2", "200", "AT", "A") == "2:200:AT:A"


def test_build_variant_id_preserves_multiallelic_alt_string() -> None:
    assert build_variant_id("3", "300", "A", "C,G") == "3:300:A:C,G"


def test_build_variant_id_preserves_mitochondrial_contig_token() -> None:
    assert build_variant_id("MT", "3243", "A", "G") == "MT:3243:A:G"


def test_build_variant_id_performs_no_case_or_contig_normalization() -> None:
    assert build_variant_id("chrX", "42", "a", "<DEL>") == (
        "chrX:42:a:<DEL>"
    )


def test_stage07_annotation_row_uses_shared_variant_id_builder(
    monkeypatch,
) -> None:
    observed: dict[str, tuple[str, str, str, str]] = {}

    def fake_build_variant_id(
        chromosome: str,
        position: str,
        reference_allele: str,
        alternate_allele: str,
    ) -> str:
        observed["arguments"] = (
            chromosome,
            position,
            reference_allele,
            alternate_allele,
        )
        return "shared-helper-sentinel"

    monkeypatch.setattr(stage07, "build_variant_id", fake_build_variant_id)

    parsed_record = {
        "gene_id": "1",
        "gene_symbol": "GENE1",
        "transcript_id": "ENST000001",
        "consequence": "missense_variant",
        "impact": "MODERATE",
        "variant_class": "SNV",
        "clinvar_significance": "NA",
        "gnomad_af": "NA",
        "exac_af": "NA",
        "thousand_genomes_af": "NA",
    }

    row, unresolved_increment = stage07._build_annotation_output_row(
        sample_id="HG002",
        run_id="run_2099_01_01_000000",
        source_pipeline="variant_annotation_pipeline",
        chrom="1",
        pos="895427",
        ref="G",
        alt="C",
        quality_flag="PASS",
        parsed_record=parsed_record,
        union_symbol_to_gene_id={"GENE1": "1"},
        mito_gene_ids=set(),
        epilepsy_gene_ids=set(),
        allowed_coding_terms=["missense_variant"],
    )

    assert observed["arguments"] == ("1", "895427", "G", "C")
    assert row["variant_id"] == "shared-helper-sentinel"
    assert unresolved_increment == 0
