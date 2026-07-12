\
from __future__ import annotations

import csv
import json
from pathlib import Path

from pipeline.genotype_projection import project_genotype_observations


HEADER = """##fileformat=VCFv4.2
##reference=GRCh38
##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">
##FORMAT=<ID=AD,Number=R,Type=Integer,Description="Allelic depths">
##FORMAT=<ID=DP,Number=1,Type=Integer,Description="Read depth">
##FORMAT=<ID=GQ,Number=1,Type=Integer,Description="Genotype quality">
##FORMAT=<ID=PL,Number=G,Type=Integer,Description="Phred likelihoods">
#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tHG002
"""


def _project_record(
    tmp_path: Path,
    *,
    alt: str,
    format_raw: str,
    sample_raw: str,
) -> tuple[dict[str, str], dict]:
    source = tmp_path / "fixture.vcf"
    source.write_text(
        HEADER
        + f"1\t100\t.\tA\t{alt}\t60\tPASS\t.\t"
        + f"{format_raw}\t{sample_raw}\n",
        encoding="utf-8",
        newline="\n",
    )
    output = tmp_path / "out"
    project_genotype_observations(
        annotated_vcf_path=source,
        output_directory=output,
        sample_id="HG002",
        run_id="run_policy_fixture",
        reference_build="GRCh38",
        source_pipeline="variant_annotation_pipeline",
        explicit_vcf_sample_name="HG002",
        source_vcf_path_label="processed/fixture.vcf",
        normalization_policy_id="vap_stage06_normalization_policy_v1",
        normalization_state="normalized_annotated_vcf",
    )

    with (output / "genotype_observations.tsv").open(
        "r",
        encoding="utf-8",
        newline="",
    ) as handle:
        row = next(csv.DictReader(handle, delimiter="\t"))

    summary = json.loads(
        (output / "genotype_projection_summary.json").read_text(
            encoding="utf-8"
        )
    )
    return row, summary


def test_biallelic_direct_relationship_targets_none(tmp_path: Path) -> None:
    row, summary = _project_record(
        tmp_path,
        alt="C",
        format_raw="GT:AD:DP:GQ:PL",
        sample_raw="0/1:8,7:15:42:70,0,80",
    )
    assert row["variant_relationship_status"] == "direct"
    assert row["relationship_reason"] == "biallelic_direct"
    assert row["relationship_resolution_target"] == "none"
    assert row["variant_id"] == "1:100:A:C"
    assert row["projection_advisory_codes"] == "NA"
    assert row["projection_warning_codes"] == "NA"
    assert summary["projection"]["projection_status"] == "pass"


def test_multiallelic_relationship_is_advisory_not_warning(
    tmp_path: Path,
) -> None:
    row, summary = _project_record(
        tmp_path,
        alt="C,G",
        format_raw="GT:AD:DP:GQ:PL",
        sample_raw="1/2:2,4,9:15:30:99,50,40,30,20,0",
    )
    assert row["variant_relationship_status"] == "complex"
    assert row["relationship_reason"] == "multiallelic_source_record"
    assert row["relationship_resolution_target"] == "vdb_brokerage"
    assert row["variant_id"] == "NA"
    assert (
        row["projection_advisory_codes"]
        == "multiallelic_relationship_deferred_to_vdb"
    )
    assert row["projection_warning_codes"] == "NA"
    assert summary["counts"]["projection_advisory_count"] == 1
    assert summary["counts"]["projection_warning_count"] == 0
    assert (
        summary["counts"]["multiallelic_relationship_deferred_count"]
        == 1
    )
    assert summary["projection"]["projection_status"] == "pass_with_advisory"


def test_symbolic_alt_is_deferred_to_vdb(tmp_path: Path) -> None:
    row, summary = _project_record(
        tmp_path,
        alt="<DEL>",
        format_raw="GT:DP",
        sample_raw="0/1:12",
    )
    assert row["variant_relationship_status"] == "complex"
    assert row["relationship_reason"] == "symbolic_alt"
    assert row["relationship_resolution_target"] == "vdb_brokerage"
    assert row["variant_id"] == "NA"
    assert (
        row["projection_advisory_codes"]
        == "symbolic_alt_relationship_deferred_to_vdb"
    )
    assert row["projection_warning_codes"] == "NA"
    assert summary["counts"]["symbolic_alt_deferred_count"] == 1


def test_spanning_deletion_is_deferred_to_vdb(tmp_path: Path) -> None:
    row, summary = _project_record(
        tmp_path,
        alt="*",
        format_raw="GT:DP",
        sample_raw="0/1:12",
    )
    assert row["variant_relationship_status"] == "complex"
    assert row["relationship_reason"] == "spanning_deletion"
    assert row["relationship_resolution_target"] == "vdb_brokerage"
    assert row["variant_id"] == "NA"
    assert (
        row["projection_advisory_codes"]
        == "spanning_deletion_relationship_deferred_to_vdb"
    )
    assert row["projection_warning_codes"] == "NA"
    assert summary["counts"]["spanning_deletion_deferred_count"] == 1


def test_called_allele_index_out_of_range_is_unresolved(
    tmp_path: Path,
) -> None:
    row, summary = _project_record(
        tmp_path,
        alt="C,G",
        format_raw="GT:AD",
        sample_raw="1/3:2,4,9",
    )
    assert row["variant_relationship_status"] == "unresolved"
    assert row["relationship_reason"] == "called_allele_index_out_of_range"
    assert row["relationship_resolution_target"] == "not_resolvable_by_vap"
    assert row["variant_id"] == "NA"
    assert row["projection_advisory_codes"] == "NA"
    assert (
        row["projection_warning_codes"]
        == "called_allele_index_out_of_range"
    )
    assert (
        summary["counts"]["called_allele_index_out_of_range_count"]
        == 1
    )
    assert summary["projection"]["projection_status"] == "pass_with_warnings"


def test_mixed_gt_separators_are_malformed_and_never_direct(
    tmp_path: Path,
) -> None:
    row, summary = _project_record(
        tmp_path,
        alt="C,G",
        format_raw="GT:DP",
        sample_raw="0/1|2:12",
    )
    assert row["gt_status"] == "malformed"
    assert row["gt_separator"] == "mixed"
    assert row["record_parse_status"] == "malformed_gt_preserved"
    assert row["variant_relationship_status"] == "unresolved"
    assert row["relationship_reason"] == "malformed_gt"
    assert row["relationship_resolution_target"] == "not_resolvable_by_vap"
    assert row["variant_id"] == "NA"
    assert row["projection_warning_codes"] == "malformed_gt"
    assert summary["counts"]["malformed_gt_count"] == 1


def test_missing_gt_is_distinct_from_no_call(tmp_path: Path) -> None:
    row, summary = _project_record(
        tmp_path,
        alt="C",
        format_raw="DP:GQ",
        sample_raw="12:40",
    )
    assert row["gt_status"] == "absent_from_format"
    assert row["variant_relationship_status"] == "unresolved"
    assert row["relationship_reason"] == "missing_gt"
    assert row["relationship_resolution_target"] == "not_resolvable_by_vap"
    assert row["projection_warning_codes"] == "missing_gt"
    assert summary["counts"]["missing_gt_count"] == 1


def test_complete_no_call_is_not_applicable_not_direct(
    tmp_path: Path,
) -> None:
    row, summary = _project_record(
        tmp_path,
        alt="C",
        format_raw="GT:DP",
        sample_raw="./.:.",
    )
    assert row["gt_status"] == "complete_no_call"
    assert row["variant_relationship_status"] == "not_applicable"
    assert row["relationship_reason"] == "no_call"
    assert row["relationship_resolution_target"] == "none"
    assert row["variant_id"] == "NA"
    assert row["projection_advisory_codes"] == "NA"
    assert row["projection_warning_codes"] == "NA"
    assert summary["counts"]["no_call_count"] == 1
    assert summary["projection"]["projection_status"] == "pass"


def test_partial_no_call_is_deferred_with_advisory(
    tmp_path: Path,
) -> None:
    row, summary = _project_record(
        tmp_path,
        alt="C",
        format_raw="GT:DP",
        sample_raw="0/.:12",
    )
    assert row["gt_status"] == "partial_no_call"
    assert row["variant_relationship_status"] == "unresolved"
    assert row["relationship_reason"] == "partial_no_call"
    assert row["relationship_resolution_target"] == "vdb_brokerage"
    assert row["variant_id"] == "NA"
    assert (
        row["projection_advisory_codes"]
        == "partial_no_call_relationship_deferred_to_vdb"
    )
    assert row["projection_warning_codes"] == "NA"
    assert summary["counts"]["partial_no_call_count"] == 1
    assert summary["projection"]["projection_status"] == "pass_with_advisory"


def test_optional_ft_absence_is_availability_not_warning(
    tmp_path: Path,
) -> None:
    row, summary = _project_record(
        tmp_path,
        alt="C",
        format_raw="GT:AD:DP:GQ:PL",
        sample_raw="0/1:8,7:15:42:70,0,80",
    )
    assert row["ft_raw"] == "NA"
    assert row["projection_warning_codes"] == "NA"
    assert summary["counts"]["ft_present_count"] == 0
    assert summary["counts"]["projection_warning_count"] == 0
