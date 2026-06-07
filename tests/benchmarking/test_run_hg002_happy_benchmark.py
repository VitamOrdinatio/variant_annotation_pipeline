from pathlib import Path

import pytest

from scripts.benchmarking.run_hg002_happy_benchmark import (
    discover_query_vcf,
    f1_score,
    metric_from_rows,
    require_file,
    summarize_happy,
)


def test_discover_query_vcf_finds_plain_vcf(tmp_path):
    run_dir = tmp_path / "run_test"
    interim = run_dir / "interim"
    interim.mkdir(parents=True)
    expected = interim / "HG002_run.normalized_variants.vcf"
    expected.write_text("fixture\n", encoding="utf-8")

    assert discover_query_vcf(run_dir, None) == expected


def test_discover_query_vcf_finds_gzipped_vcf(tmp_path):
    run_dir = tmp_path / "run_test"
    interim = run_dir / "interim"
    interim.mkdir(parents=True)
    expected = interim / "HG002_run.normalized_variants.vcf.gz"
    expected.write_text("fixture\n", encoding="utf-8")

    assert discover_query_vcf(run_dir, None) == expected


def test_discover_query_vcf_fails_on_missing_interim(tmp_path):
    run_dir = tmp_path / "run_test"
    run_dir.mkdir()

    with pytest.raises(RuntimeError, match="Run interim directory not found"):
        discover_query_vcf(run_dir, None)


def test_discover_query_vcf_fails_on_zero_candidates(tmp_path):
    run_dir = tmp_path / "run_test"
    (run_dir / "interim").mkdir(parents=True)

    with pytest.raises(RuntimeError, match="No normalized VCF found"):
        discover_query_vcf(run_dir, None)


def test_discover_query_vcf_fails_on_multiple_candidates(tmp_path):
    run_dir = tmp_path / "run_test"
    interim = run_dir / "interim"
    interim.mkdir(parents=True)
    (interim / "a.normalized_variants.vcf").write_text("a\n", encoding="utf-8")
    (interim / "b.normalized_variants.vcf.gz").write_text("b\n", encoding="utf-8")

    with pytest.raises(RuntimeError, match="Multiple normalized VCF candidates found"):
        discover_query_vcf(run_dir, None)


def test_discover_query_vcf_accepts_explicit_query(tmp_path):
    query_vcf = tmp_path / "explicit.normalized_variants.vcf"
    query_vcf.write_text("fixture\n", encoding="utf-8")

    assert discover_query_vcf(tmp_path / "unused_run_dir", str(query_vcf)) == query_vcf


def test_require_file_accepts_file(tmp_path):
    path = tmp_path / "resource.txt"
    path.write_text("fixture\n", encoding="utf-8")

    assert require_file(path, "resource") == path


def test_require_file_rejects_missing_file(tmp_path):
    with pytest.raises(RuntimeError, match="Required resource not found"):
        require_file(tmp_path / "missing.txt", "resource")


def test_require_file_rejects_directory(tmp_path):
    directory = tmp_path / "resource_dir"
    directory.mkdir()

    with pytest.raises(RuntimeError, match="Required resource is not a file"):
        require_file(directory, "resource")


def test_f1_score_handles_none_and_zero():
    assert f1_score(None, 0.5) is None
    assert f1_score(0.5, None) is None
    assert f1_score(0.0, 0.0) == 0.0


def test_f1_score_calculates_harmonic_mean():
    assert f1_score(0.8, 0.4) == pytest.approx(0.5333333333)


def test_metric_from_rows_finds_type_and_filter():
    rows = [
        {"Type": "SNP", "Filter": "PASS", "METRIC.Precision": "0.1"},
        {"Type": "SNP", "Filter": "ALL", "METRIC.Precision": "0.9"},
    ]

    row = metric_from_rows(rows, "SNP")
    assert row is not None
    assert row["METRIC.Precision"] == "0.9"


def test_metric_from_rows_returns_none_when_absent():
    assert metric_from_rows([{"Type": "SNP", "Filter": "ALL"}], "INDEL") is None


def test_summarize_happy_extracts_all_snp_indel_metrics(tmp_path):
    rows = [
        {
            "Type": "ALL",
            "Filter": "ALL",
            "METRIC.Precision": "0.95",
            "METRIC.Recall": "0.90",
            "QUERY.TP": "90",
            "QUERY.FP": "5",
            "TRUTH.FN": "10",
        },
        {
            "Type": "SNP",
            "Filter": "ALL",
            "METRIC.Precision": "0.98",
            "METRIC.Recall": "0.97",
            "TRUTH.TP": "970",
            "TRUTH.FN": "30",
            "QUERY.TP": "970",
            "QUERY.FP": "20",
        },
        {
            "Type": "INDEL",
            "Filter": "ALL",
            "METRIC.Precision": "0.85",
            "METRIC.Recall": "0.80",
            "TRUTH.TP": "80",
            "TRUTH.FN": "20",
            "QUERY.TP": "80",
            "QUERY.FP": "15",
        },
    ]

    summary, stratified = summarize_happy(
        rows=rows,
        run_id="run_test",
        query_vcf=tmp_path / "query.vcf",
        truth_vcf=tmp_path / "truth.vcf.gz",
        truth_bed=tmp_path / "truth.bed",
        reference_fasta=tmp_path / "ref.fa",
    )

    assert summary["precision"] == 0.95
    assert summary["recall"] == 0.90
    assert summary["f1"] == pytest.approx(0.9243243243)
    assert summary["tp"] == "90"
    assert summary["fp"] == "5"
    assert summary["fn"] == "10"
    assert summary["snp_precision"] == 0.98
    assert summary["snp_recall"] == 0.97
    assert summary["indel_precision"] == 0.85
    assert summary["indel_recall"] == 0.80
    assert len(stratified) == 2