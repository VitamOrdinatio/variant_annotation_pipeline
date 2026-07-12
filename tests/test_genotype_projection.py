from __future__ import annotations

import csv
import gzip
from pathlib import Path

import pytest

from pipeline.genotype_projection import (
    GenotypeProjectionError,
    _percent_encode_unknown,
    project_genotype_observations,
)

VCF_TEXT = """##fileformat=VCFv4.2
##source=Wave2Fixture
##reference=GRCh38
##contig=<ID=1,length=248956422,assembly=GRCh38>
##FORMAT=<ID=GT,Number=1,Type=String,Description=\"Genotype\">
##FORMAT=<ID=AD,Number=R,Type=Integer,Description=\"Allelic depths\">
##FORMAT=<ID=DP,Number=1,Type=Integer,Description=\"Read depth\">
##FORMAT=<ID=GQ,Number=1,Type=Integer,Description=\"Genotype quality\">
##FORMAT=<ID=PL,Number=G,Type=Integer,Description=\"Phred likelihoods\">
##FORMAT=<ID=FT,Number=1,Type=String,Description=\"Sample filter\">
##FORMAT=<ID=XY,Number=1,Type=String,Description=\"Unknown test field\">
#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tHG002
1\t100\t.\tA\tC\t60\tPASS\t.\tGT:AD:DP:GQ:PL:FT\t0/1:8,7:15:42:70,0,80:PASS
1\t200\t.\tG\tA,T\t50\tq10\t.\tGT:AD:DP:GQ:PL\t1/2:2,4,9:15:30:99,50,40,30,20,0
1\t300\t.\tC\tT\t.\tPASS\t.\tGT:DP\t./.:.
1\t400\t.\tT\tG\t.\tPASS\t.\tGT:XY\t0|1:a=b%2
1\t500\t.\tA\tG\t.\tPASS\t.\tGT:DP:GQ\t0/1:10
"""


def write_fixture(path: Path, text: str = VCF_TEXT) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")
    return path


def project(tmp_path: Path, source: Path | None = None):
    source = source or write_fixture(tmp_path / "fixture.vcf")
    output = tmp_path / "out"
    result = project_genotype_observations(
        annotated_vcf_path=source,
        output_directory=output,
        sample_id="HG002",
        sample_alias="NA24385",
        sra_accession="SRR12898354",
        run_id="run_2099_01_01_000000",
        reference_build="GRCh38",
        source_pipeline="variant_annotation_pipeline",
        assay_type="WGS",
        source_vcf_path_label="processed/fixture.vcf",
    )
    return output, result


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def test_projection_emits_complete_three_artifact_set(tmp_path: Path) -> None:
    output, result = project(tmp_path)
    assert result["row_count"] == 5
    assert (output / "genotype_observations.tsv").exists()
    assert (output / "genotype_projection_summary.json").exists()
    assert (output / "genotype_source_header_context.json").exists()


def test_biallelic_projection_preserves_safe_fields(tmp_path: Path) -> None:
    output, _ = project(tmp_path)
    row = read_rows(output / "genotype_observations.tsv")[0]
    assert row["variant_relationship_status"] == "direct"
    assert row["variant_id"] == "1:100:A:C"
    assert row["gt_raw"] == "0/1"
    assert row["genotype_call_state"] == "heterozygous_call"
    assert row["ref_depth"] == "8"
    assert row["alt_depth"] == "7"
    assert row["dp_value"] == "15"
    assert row["gq_value"] == "42"
    assert row["pl_value_count"] == "3"


def test_multiallelic_record_remains_unsplit_and_complex(tmp_path: Path) -> None:
    output, _ = project(tmp_path)
    rows = read_rows(output / "genotype_observations.tsv")
    row = rows[1]
    assert len(rows) == 5
    assert row["alternate_alleles_raw"] == "A,T"
    assert row["alternate_allele_count"] == "2"
    assert row["alternate_allele"] == "NA"
    assert row["is_multiallelic"] == "True"
    assert row["variant_relationship_status"] == "complex"
    assert row["variant_id"] == "NA"
    assert row["called_allele_indices"] == "1,2"
    assert row["alt_depth"] == "NA"
    assert row["alt_depths_raw"] == "4,9"


def test_complete_no_call_is_not_homozygous_reference(tmp_path: Path) -> None:
    output, _ = project(tmp_path)
    row = read_rows(output / "genotype_observations.tsv")[2]
    assert row["gt_raw"] == "./."
    assert row["gt_status"] == "complete_no_call"
    assert row["genotype_call_state"] == "complete_no_call"
    assert row["is_no_call"] == "True"
    assert row["called_allele_indices"] == "NA"


def test_phased_gt_is_structural_only(tmp_path: Path) -> None:
    output, _ = project(tmp_path)
    row = read_rows(output / "genotype_observations.tsv")[3]
    assert row["gt_separator"] == "|"
    assert row["phase_state"] == "phased"
    assert row["genotype_call_state"] == "heterozygous_call"


def test_short_sample_vector_is_preserved_with_warning(tmp_path: Path) -> None:
    output, _ = project(tmp_path)
    row = read_rows(output / "genotype_observations.tsv")[4]
    assert row["format_alignment_status"] == "sample_values_shorter"
    assert row["gq_raw"] == "NA"
    assert "sample_values_shorter_than_format" in row["projection_warning_codes"]


def test_unknown_format_reserved_characters_are_percent_encoded() -> None:
    assert _percent_encode_unknown("a=b%2;x\tz") == "a%3Db%252%3Bx%09z"


def test_projection_rejects_multisample_without_selection(tmp_path: Path) -> None:
    text = VCF_TEXT.replace(
        "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tHG002",
        "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tA\tB",
    )
    source = write_fixture(tmp_path / "multi.vcf", text)
    with pytest.raises(GenotypeProjectionError):
        project_genotype_observations(
            annotated_vcf_path=source,
            output_directory=tmp_path / "out",
            sample_id="UNMAPPED",
            run_id="run_x",
            reference_build="GRCh38",
            source_pipeline="variant_annotation_pipeline",
        )


def test_plain_and_gzipped_vcf_have_equal_logical_record_hashes(tmp_path: Path) -> None:
    plain = write_fixture(tmp_path / "fixture.vcf")
    gzipped = tmp_path / "fixture.vcf.gz"
    with gzip.open(gzipped, "wt", encoding="utf-8", newline="\n") as handle:
        handle.write(VCF_TEXT)
    plain_out, _ = project(tmp_path / "plain", plain)
    gzip_out, _ = project(tmp_path / "gzip", gzipped)
    plain_rows = read_rows(plain_out / "genotype_observations.tsv")
    gzip_rows = read_rows(gzip_out / "genotype_observations.tsv")
    assert [row["source_record_hash"] for row in plain_rows] == [
        row["source_record_hash"] for row in gzip_rows
    ]
    assert plain_rows[0]["source_vcf_sha256"] != gzip_rows[0]["source_vcf_sha256"]
