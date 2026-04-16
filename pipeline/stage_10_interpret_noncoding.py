"""
Stage 10: Interpret non-coding variants.

Repo 2 v1.0 design notes:
- input:
  - noncoding_variants.tsv from Stage 08
- output:
  - interpreted_noncoding.tsv
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


def _classify_noncoding_class(consequence: str) -> str:
    """
    Map VEP consequence strings to a simplified non-coding functional class.
    """
    if not consequence or consequence == "NA":
        return "unknown"

    terms = {term.strip() for term in str(consequence).split("&") if term.strip()}

    if "splice_region_variant" in terms:
        return "splice_region"
    if "regulatory_region_variant" in terms:
        return "regulatory_region"
    if "upstream_gene_variant" in terms:
        return "upstream"
    if "downstream_gene_variant" in terms:
        return "downstream"
    if "intron_variant" in terms:
        return "intronic"
    if "intergenic_variant" in terms:
        return "intergenic"

    return "other_noncoding"


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


def _classify_priority_context(
    noncoding_class: str,
    clinvar_bucket: str,
    rarity: str,
    mito_flag: str,
    epilepsy_flag: str,
) -> tuple[str, str]:
    """
    Assign a conservative non-coding severity label and rationale.
    """
    in_target_gene_set = mito_flag == "True" or epilepsy_flag == "True"

    if clinvar_bucket in {"pathogenic", "likely_pathogenic"}:
        return "high", "ClinVar pathogenic_or_likely_pathogenic"

    if noncoding_class == "splice_region" and rarity in {"ultra_rare", "rare", "unknown"}:
        return "medium", "rare_splice_region_variant"

    if noncoding_class == "regulatory_region" and rarity in {"ultra_rare", "rare"} and in_target_gene_set:
        return "medium", "rare_regulatory_variant_in_target_gene_set"

    if noncoding_class in {"upstream", "downstream", "intronic"} and rarity in {"ultra_rare", "rare"} and in_target_gene_set:
        return "low", "rare_noncoding_variant_in_target_gene_set"

    if clinvar_bucket == "vus":
        return "low", "vus_noncoding_variant"

    return "low", "limited_noncoding_evidence"


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

    notes.append(f"noncoding_class={row.get('noncoding_class', 'unknown')}")

    return ";".join(notes)


def run_stage(
    config: dict[str, Any],
    paths: dict[str, Any],
    logger,
    state: dict[str, Any],
) -> dict[str, Any]:
    """
    Execute Stage 10.

    Responsibilities
    ----------------
    - read noncoding_variants.tsv
    - apply conservative rule-based non-coding interpretation
    - write interpreted_noncoding.tsv
    - update artifacts, QC, and stage outputs
    """
    logger.info("Stage 10: interpreting non-coding variants.")

    noncoding_table = _validate_required_artifact(
        state["artifacts"].get("noncoding_table"),
        "non-coding variant table",
    )

    interpreted_noncoding_table = Path(paths["final_dir"]) / "interpreted_noncoding.tsv"

    df = pd.read_csv(noncoding_table, sep="\t", dtype=str).fillna("NA")

    if df.empty:
        logger.warning("Non-coding variant table is empty. Writing empty interpreted non-coding table.")

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
            "Non-coding variant table is missing required columns: " + ", ".join(missing_columns)
        )

    df["noncoding_class"] = df["consequence"].apply(_classify_noncoding_class)
    df["clinvar_bucket"] = df["clinvar_significance"].apply(_classify_clinvar)
    df["rarity_label"] = df.apply(_classify_rarity, axis=1)

    severity_results = df.apply(
        lambda row: _classify_priority_context(
            noncoding_class=row["noncoding_class"],
            clinvar_bucket=row["clinvar_bucket"],
            rarity=row["rarity_label"],
            mito_flag=str(row.get("mito_flag", "False")),
            epilepsy_flag=str(row.get("epilepsy_flag", "False")),
        ),
        axis=1,
    )
    df["predicted_severity"] = [item[0] for item in severity_results]
    df["severity_basis"] = [item[1] for item in severity_results]
    df["interpretation_notes"] = df.apply(_build_interpretation_notes, axis=1)

    output_columns = list(df.columns)
    df.to_csv(interpreted_noncoding_table, sep="\t", index=False, columns=output_columns)

    noncoding_variant_count = int(len(df))
    noncoding_gene_count = int(df["gene_symbol"].replace("NA", pd.NA).dropna().nunique())

    interpretation_class_counts = (
        df["predicted_severity"].value_counts(dropna=False).to_dict()
        if not df.empty
        else {}
    )

    state["artifacts"]["interpreted_noncoding_table"] = str(interpreted_noncoding_table)

    interpretation_qc = state["qc"].setdefault("interpretation_qc", {})
    interpretation_qc.update(
        {
            "noncoding_interpretation_completed": True,
            "noncoding_variant_count": noncoding_variant_count,
            "noncoding_gene_count": noncoding_gene_count,
            "noncoding_interpretation_class_counts": interpretation_class_counts,
        }
    )

    state["stage_outputs"]["stage_10_interpret_noncoding"] = {
        "status": "success",
        "input_noncoding_table": str(noncoding_table),
        "interpreted_noncoding_table": str(interpreted_noncoding_table),
        "noncoding_variant_count": noncoding_variant_count,
        "noncoding_gene_count": noncoding_gene_count,
        "noncoding_interpretation_class_counts": interpretation_class_counts,
    }

    logger.info(f"Interpreted non-coding table written to: {interpreted_noncoding_table}")
    logger.info(f"Non-coding variants interpreted: {noncoding_variant_count}")
    logger.info(f"Unique non-coding genes interpreted: {noncoding_gene_count}")

    return state