"""
Stage 09: Interpret coding variants.

Repo 2 v1.0 design notes:
- input:
  - coding_variants.tsv from Stage 08
- output:
  - interpreted_coding.tsv
- interpretation is rule-based and intentionally conservative
- no AI tools are used in v1
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd


def _validate_required_artifact(path_str: str | None, label: str) -> Path:
    """
    Validate that a required upstream artifact exists.

    Parameters
    ----------
    path_str : str | None
        Path string.
    label : str
        Human-readable label.

    Returns
    -------
    Path
        Validated path.

    Raises
    ------
    ValueError
        If missing.
    FileNotFoundError
        If path does not exist.
    """
    if not path_str:
        raise ValueError(f"Missing required upstream artifact for {label}")
    path = Path(path_str)
    if not path.exists():
        raise FileNotFoundError(f"Required upstream artifact not found for {label}: {path}")
    if not path.is_file():
        raise FileNotFoundError(f"Expected file for {label}, but found non-file path: {path}")
    return path


def _normalize_af(value: object) -> float | None:
    """
    Convert an allele-frequency-like value to float.

    Returns None for NA-like values.
    """
    if value is None:
        return None
    text = str(value).strip()
    if text in {"", "NA", ".", "-", "nan", "None"}:
        return None
    try:
        return float(text)
    except ValueError:
        return None


def _classify_rarity(row: pd.Series) -> str:
    """
    Assign a rarity label using available population frequency columns.
    """
    af_values = [
        _normalize_af(row.get("gnomad_af")),
        _normalize_af(row.get("exac_af")),
        _normalize_af(row.get("thousand_genomes_af")),
    ]
    observed = [v for v in af_values if v is not None]

    if not observed:
        return "unknown"
    max_af = max(observed)

    if max_af == 0:
        return "ultra_rare"
    if max_af <= 0.001:
        return "rare"
    if max_af <= 0.01:
        return "low_frequency"
    return "common"


def _classify_functional_class(consequence: str) -> str:
    """
    Map VEP consequence strings to a simplified coding functional class.
    """
    if not consequence or consequence == "NA":
        return "unknown"

    terms = {term.strip() for term in str(consequence).split("&") if term.strip()}

    if "stop_gained" in terms:
        return "nonsense"
    if "frameshift_variant" in terms:
        return "frameshift"
    if "splice_donor_variant" in terms or "splice_acceptor_variant" in terms:
        return "splice_site"
    if "missense_variant" in terms:
        return "missense"
    if "synonymous_variant" in terms:
        return "synonymous"
    return "other_coding"


def _classify_clinvar(significance: str) -> str:
    """
    Simplify ClinVar significance into coarse buckets.
    """
    if not significance or significance == "NA":
        return "unknown"

    text = str(significance).strip().lower()

    if "pathogenic" in text and "likely" in text:
        return "likely_pathogenic"
    if text == "pathogenic" or " pathogenic" in text or text.startswith("pathogenic"):
        return "pathogenic"
    if "uncertain" in text or "vus" in text:
        return "vus"
    if "benign" in text and "likely" in text:
        return "likely_benign"
    if text == "benign" or text.startswith("benign"):
        return "benign"
    return "other"


def _classify_severity(functional_class: str, clinvar_bucket: str, rarity: str) -> tuple[str, str]:
    """
    Assign a conservative severity label and a short rationale.
    """
    high_impact_classes = {"nonsense", "frameshift", "splice_site"}
    moderate_impact_classes = {"missense"}

    if clinvar_bucket in {"pathogenic", "likely_pathogenic"}:
        return "high", "ClinVar pathogenic_or_likely_pathogenic"

    if functional_class in high_impact_classes and rarity in {"ultra_rare", "rare", "unknown"}:
        return "high", "rare_high_impact_coding_variant"

    if functional_class in moderate_impact_classes and rarity in {"ultra_rare", "rare"}:
        return "medium", "rare_missense_variant"

    if clinvar_bucket == "vus" and functional_class in high_impact_classes | moderate_impact_classes:
        return "medium", "vus_with_coding_impact"

    if functional_class == "synonymous":
        return "low", "synonymous_variant"

    return "low", "limited_coding_evidence"


def _build_interpretation_notes(row: pd.Series) -> str:
    """
    Build a compact semicolon-delimited interpretation note string.
    """
    notes: list[str] = []

    if str(row.get("mito_flag", "False")) == "True":
        notes.append("mitochondrial_gene")
    if str(row.get("epilepsy_flag", "False")) == "True":
        notes.append("epilepsy_gene")

    clinvar_bucket = row.get("clinvar_bucket", "unknown")
    if clinvar_bucket not in {"unknown", "other"}:
        notes.append(f"clinvar={clinvar_bucket}")

    rarity = row.get("rarity_label", "unknown")
    notes.append(f"rarity={rarity}")

    notes.append(f"functional_class={row.get('functional_class', 'unknown')}")

    return ";".join(notes)


def run_stage(
    config: dict[str, Any],
    paths: dict[str, Any],
    logger,
    state: dict[str, Any],
) -> dict[str, Any]:
    """
    Execute Stage 09.

    Responsibilities
    ----------------
    - read coding_variants.tsv
    - apply conservative rule-based coding interpretation
    - write interpreted_coding.tsv
    - update artifacts, QC, and stage outputs
    """
    logger.info("Stage 09: interpreting coding variants.")

    coding_table = _validate_required_artifact(
        state["artifacts"].get("coding_table"),
        "coding variant table",
    )

    interpreted_coding_table = Path(paths["final_dir"]) / "interpreted_coding.tsv"

    df = pd.read_csv(coding_table, sep="\t", dtype=str).fillna("NA")

    if df.empty:
        logger.warning("Coding variant table is empty. Writing empty interpreted coding table.")

    required_columns = [
        "gene_symbol",
        "consequence",
        "clinvar_significance",
        "mito_flag",
        "epilepsy_flag",
        "gnomad_af",
        "exac_af",
        "thousand_genomes_af",
    ]
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(
            "Coding variant table is missing required columns: " + ", ".join(missing_columns)
        )

    df["functional_class"] = df["consequence"].apply(_classify_functional_class)
    df["clinvar_bucket"] = df["clinvar_significance"].apply(_classify_clinvar)
    df["rarity_label"] = df.apply(_classify_rarity, axis=1)

    severity_results = df.apply(
        lambda row: _classify_severity(
            functional_class=row["functional_class"],
            clinvar_bucket=row["clinvar_bucket"],
            rarity=row["rarity_label"],
        ),
        axis=1,
    )
    df["predicted_severity"] = [item[0] for item in severity_results]
    df["severity_basis"] = [item[1] for item in severity_results]
    df["interpretation_notes"] = df.apply(_build_interpretation_notes, axis=1)

    output_columns = list(df.columns)
    df.to_csv(interpreted_coding_table, sep="\t", index=False, columns=output_columns)

    coding_variant_count = int(len(df))
    coding_gene_count = int(df["gene_symbol"].replace("NA", pd.NA).dropna().nunique())

    interpretation_class_counts = (
        df["predicted_severity"].value_counts(dropna=False).to_dict()
        if not df.empty
        else {}
    )

    state["artifacts"]["interpreted_coding_table"] = str(interpreted_coding_table)

    interpretation_qc = state["qc"].setdefault("interpretation_qc", {})
    interpretation_qc.update(
        {
            "coding_interpretation_completed": True,
            "coding_variant_count": coding_variant_count,
            "coding_gene_count": coding_gene_count,
            "coding_interpretation_class_counts": interpretation_class_counts,
        }
    )

    state["stage_outputs"]["stage_09_interpret_coding"] = {
        "status": "success",
        "input_coding_table": str(coding_table),
        "interpreted_coding_table": str(interpreted_coding_table),
        "coding_variant_count": coding_variant_count,
        "coding_gene_count": coding_gene_count,
        "coding_interpretation_class_counts": interpretation_class_counts,
    }

    logger.info(f"Interpreted coding table written to: {interpreted_coding_table}")
    logger.info(f"Coding variants interpreted: {coding_variant_count}")
    logger.info(f"Unique coding genes interpreted: {coding_gene_count}")

    return state