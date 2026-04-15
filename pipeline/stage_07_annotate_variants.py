"""
Stage 07: Annotate variants and apply gene-set overlays.

Repo 2 v1.0 design notes:
- input:
  - normalized VCF
- tool: Ensembl VEP
- outputs:
  - annotated VCF
  - annotated_variants.tsv
- gene-set overlays:
  - MitoCarta
  - Genes4Epilepsy
- AI tools are explicitly excluded from v1

GeneID note
-----------
VEP does not directly provide NCBI GeneID in this v1 implementation.
Accordingly, Stage 07 resolves VEP gene symbols against curated gene-set
tables that contain both:
- gene_id
- gene_symbol

Once resolved, overlay membership is applied using gene_id as the canonical key.
"""

from __future__ import annotations

import csv
import re
import shlex
import subprocess
from pathlib import Path
from typing import Any


def _run_command(command: list[str], logger, label: str) -> subprocess.CompletedProcess:
    rendered = " ".join(shlex.quote(part) for part in command)
    logger.info(f"{label} command: {rendered}")

    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=False,
    )

    if result.stdout.strip():
        logger.info(f"{label} stdout: {result.stdout.strip()}")
    if result.stderr.strip():
        logger.info(f"{label} stderr: {result.stderr.strip()}")

    if result.returncode != 0:
        raise RuntimeError(f"{label} failed with exit code {result.returncode}")

    return result


def _validate_required_artifact(path_str: str | None, label: str) -> Path:
    if not path_str:
        raise ValueError(f"Missing required upstream artifact for {label}")
    path = Path(path_str)
    if not path.exists():
        raise FileNotFoundError(f"Required upstream artifact not found for {label}: {path}")
    if not path.is_file():
        raise FileNotFoundError(f"Expected file for {label}, but found non-file path: {path}")
    return path


def _record_vep_version(config: dict[str, Any], state: dict[str, Any], logger) -> None:
    vep_executable = config["tools"]["vep"]["executable"]
    try:
        result = subprocess.run(
            [vep_executable, "--help"],
            capture_output=True,
            text=True,
            check=False,
        )
        text = (result.stdout or result.stderr or "").strip().splitlines()
        first_version_line = None
        for line in text:
            if "variant effect predictor" in line.lower() or "ensembl" in line.lower():
                first_version_line = line.strip()
                break
        if first_version_line is None and text:
            first_version_line = text[0].strip()
        if first_version_line:
            state["run"].setdefault("tool_versions", {})
            state["run"]["tool_versions"]["vep"] = first_version_line
            logger.info(f"Recorded VEP version: {first_version_line}")
    except Exception as exc:
        state["warnings"].append(f"Unable to record VEP version: {exc}")
        logger.warning(f"Unable to record VEP version: {exc}")


def _load_gene_set_table(path: Path, label: str) -> tuple[set[str], dict[str, str]]:
    """
    Load a 2-column gene-set TSV with required columns:
    - gene_id
    - gene_symbol

    Returns
    -------
    tuple[set[str], dict[str, str]]
        gene_id set, symbol->gene_id mapping
    """
    gene_ids: set[str] = set()
    symbol_to_gene_id: dict[str, str] = {}

    with path.open("r", encoding="utf-8", errors="replace") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        expected = {"gene_id", "gene_symbol"}
        if reader.fieldnames is None or not expected.issubset(set(reader.fieldnames)):
            raise ValueError(
                f"{label} must be a TSV with columns: gene_id, gene_symbol"
            )

        for row in reader:
            gene_id = str(row["gene_id"]).strip()
            gene_symbol = str(row["gene_symbol"]).strip().upper()

            if not gene_id or not gene_symbol:
                continue

            gene_ids.add(gene_id)

            if gene_symbol in symbol_to_gene_id and symbol_to_gene_id[gene_symbol] != gene_id:
                raise ValueError(
                    f"{label} contains conflicting mappings for symbol {gene_symbol}: "
                    f"{symbol_to_gene_id[gene_symbol]} vs {gene_id}"
                )

            symbol_to_gene_id[gene_symbol] = gene_id

    return gene_ids, symbol_to_gene_id


def _extract_csq_format(vcf_path: Path) -> list[str]:
    pattern = re.compile(r'Format: ([^"]+)')
    with vcf_path.open("r", encoding="utf-8", errors="replace") as handle:
        for line in handle:
            if line.startswith("##INFO=<ID=CSQ"):
                match = pattern.search(line)
                if not match:
                    break
                return [field.strip() for field in match.group(1).split("|")]
            if line.startswith("#CHROM"):
                break

    raise ValueError(f"Could not locate VEP CSQ header in annotated VCF: {vcf_path}")


def _parse_info_field(info_text: str) -> dict[str, str]:
    parsed: dict[str, str] = {}
    if info_text == ".":
        return parsed

    for entry in info_text.split(";"):
        if not entry:
            continue
        if "=" in entry:
            key, value = entry.split("=", 1)
            parsed[key] = value
        else:
            parsed[entry] = "True"
    return parsed


def _safe_get(record: dict[str, str], *candidates: str) -> str:
    for key in candidates:
        value = record.get(key, "")
        if value not in {"", "-", "."}:
            return value
    return "NA"


def _consequence_is_coding(consequence: str, allowed_terms: list[str]) -> bool:
    if consequence == "NA":
        return False
    terms = {term.strip() for term in consequence.split("&") if term.strip()}
    return any(term in terms for term in allowed_terms)


def _count_vcf_variants(vcf_path: Path) -> int:
    count = 0
    with vcf_path.open("r", encoding="utf-8", errors="replace") as handle:
        for line in handle:
            if line.startswith("#"):
                continue
            if line.strip():
                count += 1
    return count


def _build_vep_command(config: dict[str, Any], input_vcf: Path, output_vcf: Path) -> list[str]:
    vep_cfg = config["tools"]["vep"]
    command = [
        vep_cfg["executable"],
        "--input_file",
        str(input_vcf),
        "--output_file",
        str(output_vcf),
        "--format",
        "vcf",
        "--vcf",
        "--force_overwrite",
        "--species",
        "homo_sapiens",
        "--assembly",
        vep_cfg["assembly"],
        "--cache",
        "--offline",
        "--dir_cache",
        vep_cfg["cache_dir"],
        "--symbol",
        "--biotype",
        "--transcript_version",
        "--canonical",
        "--mane",
        "--variant_class",
        "--pick",
        "--pick_order",
        "canonical,appris,tsl,biotype,rank,ccds,length",
        "--fork",
        str(vep_cfg["fork"]),
    ]

    if config["annotation"]["include_clinvar"]:
        command.append("--clin_sig_allele")

    if config["annotation"]["include_population_frequencies"]:
        command.extend(["--af", "--af_1kg", "--af_gnomad", "--max_af"])

    return command


def run_stage(
    config: dict[str, Any],
    paths: dict[str, Any],
    logger,
    state: dict[str, Any],
) -> dict[str, Any]:
    logger.info("Stage 07: annotating variants.")

    normalized_vcf = _validate_required_artifact(
        state["artifacts"].get("normalized_vcf"),
        "normalized VCF",
    )

    mitocarta_path = _validate_required_artifact(
        state["gene_sets"].get("mitocarta_path"),
        "gene_sets.mitocarta_path",
    )
    genes4epilepsy_path = _validate_required_artifact(
        state["gene_sets"].get("genes4epilepsy_path"),
        "gene_sets.genes4epilepsy_path",
    )

    sample_id = state["sample"]["sample_id"]
    run_id = state["run"]["run_id"]

    annotated_vcf = Path(paths["processed_dir"]) / f"{sample_id}_{run_id}.annotated_variants.vcf"
    annotated_table = Path(paths["processed_dir"]) / f"{sample_id}_{run_id}.annotated_variants.tsv"

    vep_command = _build_vep_command(config, normalized_vcf, annotated_vcf)
    _run_command(vep_command, logger, "VEP annotation")

    if not annotated_vcf.exists():
        raise FileNotFoundError(f"Annotated VCF was not created: {annotated_vcf}")

    csq_fields = _extract_csq_format(annotated_vcf)

    mito_gene_ids, mito_symbol_to_gene_id = _load_gene_set_table(
        mitocarta_path, "MitoCarta"
    )
    epilepsy_gene_ids, epilepsy_symbol_to_gene_id = _load_gene_set_table(
        genes4epilepsy_path, "Genes4Epilepsy"
    )

    union_symbol_to_gene_id: dict[str, str] = {}
    for mapping_label, mapping in [
        ("MitoCarta", mito_symbol_to_gene_id),
        ("Genes4Epilepsy", epilepsy_symbol_to_gene_id),
    ]:
        for symbol, gene_id in mapping.items():
            if symbol in union_symbol_to_gene_id and union_symbol_to_gene_id[symbol] != gene_id:
                raise ValueError(
                    f"Cross-gene-set conflict for symbol {symbol}: "
                    f"{union_symbol_to_gene_id[symbol]} vs {gene_id} ({mapping_label})"
                )
            union_symbol_to_gene_id[symbol] = gene_id

    allowed_coding_terms = list(config["filtering"]["allowed_coding_consequences"])

    output_columns = [
        "chromosome",
        "position",
        "reference_allele",
        "alternate_allele",
        "gene_id",
        "gene_symbol",
        "transcript_id",
        "consequence",
        "impact",
        "variant_class",
        "variant_type",
        "clinvar_significance",
        "gnomad_af",
        "exac_af",
        "thousand_genomes_af",
        "mito_flag",
        "epilepsy_flag",
    ]

    annotated_variant_count = 0
    required_fields_present = True
    unresolved_symbol_count = 0

    with annotated_vcf.open("r", encoding="utf-8", errors="replace") as in_handle, annotated_table.open(
        "w",
        encoding="utf-8",
        newline="",
    ) as out_handle:
        writer = csv.DictWriter(out_handle, fieldnames=output_columns, delimiter="\t")
        writer.writeheader()

        for line in in_handle:
            if line.startswith("#"):
                continue

            line = line.rstrip("\n")
            if not line:
                continue

            fields = line.split("\t")
            if len(fields) < 8:
                state["warnings"].append(f"Malformed annotated VCF record skipped: {line[:120]}")
                logger.warning(f"Malformed annotated VCF record skipped: {line[:120]}")
                continue

            chrom, pos, _variant_id, ref, alt, _qual, _filt, info = fields[:8]
            info_map = _parse_info_field(info)
            csq_blob = info_map.get("CSQ", "")

            if not csq_blob:
                state["warnings"].append(
                    f"Annotated VCF record missing CSQ field at {chrom}:{pos}:{ref}:{alt}"
                )
                logger.warning(f"Annotated VCF record missing CSQ field at {chrom}:{pos}:{ref}:{alt}")
                consequence_record = {}
            else:
                first_csq = csq_blob.split(",")[0]
                csq_values = first_csq.split("|")
                if len(csq_values) < len(csq_fields):
                    csq_values.extend([""] * (len(csq_fields) - len(csq_values)))
                consequence_record = dict(zip(csq_fields, csq_values))

            gene_symbol = _safe_get(consequence_record, "SYMBOL", "Gene").upper()
            transcript_id = _safe_get(consequence_record, "Feature")
            consequence = _safe_get(consequence_record, "Consequence")
            impact = _safe_get(consequence_record, "IMPACT")
            variant_class = _safe_get(consequence_record, "VARIANT_CLASS")
            clinvar_significance = _safe_get(
                consequence_record,
                "CLIN_SIG",
                "ClinVar_CLNSIG",
                "CLINVAR_CLNSIG",
            )
            gnomad_af = _safe_get(consequence_record, "gnomAD_AF", "AF", "MAX_AF")
            exac_af = _safe_get(consequence_record, "ExAC_AF")
            thousand_genomes_af = _safe_get(
                consequence_record,
                "AFR_AF",
                "AMR_AF",
                "EAS_AF",
                "EUR_AF",
                "SAS_AF",
                "AA_AF",
                "EA_AF",
            )

            resolved_gene_id = union_symbol_to_gene_id.get(gene_symbol, "NA")
            if gene_symbol != "NA" and resolved_gene_id == "NA":
                unresolved_symbol_count += 1

            mito_flag = "True" if resolved_gene_id in mito_gene_ids else "False"
            epilepsy_flag = "True" if resolved_gene_id in epilepsy_gene_ids else "False"

            variant_type = (
                "coding"
                if _consequence_is_coding(consequence, allowed_coding_terms)
                else "non-coding"
            )

            row = {
                "chromosome": chrom,
                "position": pos,
                "reference_allele": ref,
                "alternate_allele": alt,
                "gene_id": resolved_gene_id,
                "gene_symbol": gene_symbol,
                "transcript_id": transcript_id,
                "consequence": consequence,
                "impact": impact,
                "variant_class": variant_class,
                "variant_type": variant_type,
                "clinvar_significance": clinvar_significance,
                "gnomad_af": gnomad_af,
                "exac_af": exac_af,
                "thousand_genomes_af": thousand_genomes_af,
                "mito_flag": mito_flag,
                "epilepsy_flag": epilepsy_flag,
            }

            for required_col in [
                "chromosome",
                "position",
                "reference_allele",
                "alternate_allele",
                "gene_symbol",
                "variant_type",
                "mito_flag",
                "epilepsy_flag",
            ]:
                if row.get(required_col, "NA") == "":
                    required_fields_present = False

            writer.writerow(row)
            annotated_variant_count += 1

    if not annotated_table.exists():
        raise FileNotFoundError(f"Annotated TSV was not created: {annotated_table}")

    annotated_vcf_variant_count = _count_vcf_variants(annotated_vcf)

    state["artifacts"]["annotated_vcf"] = str(annotated_vcf)
    state["artifacts"]["annotated_table"] = str(annotated_table)

    state["annotations"]["annotation_engine"] = config["annotation"]["engine"]
    state["annotations"]["annotation_completed"] = True
    state["annotations"]["resources_used"] = [
        "VEP",
        *config["annotation"]["population_sources"],
        "ClinVar" if config["annotation"]["include_clinvar"] else "ClinVar_disabled",
    ]

    state["gene_sets"]["overlay_completed"] = True
    state["gene_sets"]["flags_added"] = ["mito_flag", "epilepsy_flag"]

    state["qc"]["annotation_qc"] = {
        "annotation_completed": True,
        "annotated_vcf_exists": True,
        "annotated_table_exists": True,
        "annotated_vcf_variant_count": annotated_vcf_variant_count,
        "annotated_variant_count": annotated_variant_count,
        "required_fields_present": required_fields_present,
        "annotation_engine": "VEP",
        "mitocarta_gene_count": len(mito_gene_ids),
        "genes4epilepsy_gene_count": len(epilepsy_gene_ids),
        "unresolved_symbol_count": unresolved_symbol_count,
    }

    state["stage_outputs"]["stage_07_annotate_variants"] = {
        "status": "success",
        "tool": "VEP",
        "input_normalized_vcf": str(normalized_vcf),
        "annotated_vcf": str(annotated_vcf),
        "annotated_table": str(annotated_table),
        "annotated_variant_count": annotated_variant_count,
        "required_fields_present": required_fields_present,
        "unresolved_symbol_count": unresolved_symbol_count,
    }

    if config["runtime"]["record_tool_versions"]:
        _record_vep_version(config, state, logger)

    logger.info(f"Annotated VCF written to: {annotated_vcf}")
    logger.info(f"Annotated variant table written to: {annotated_table}")
    logger.info(f"Annotated variant count: {annotated_variant_count}")
    logger.info(f"Unresolved gene symbols against overlay sets: {unresolved_symbol_count}")

    return state