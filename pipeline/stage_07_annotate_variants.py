"""
Stage 07: Annotate variants and apply gene-set overlays.

Repo 2 v1.0 design notes:
- input:
  - normalized VCF
  
- tool: Ensembl VEP or ANNOVAR (configurable, but VEP is the only engine implemented in v1)
    - supports engine selection (VEP or ANNOVAR) 
    - VEP implemented
    - ANNOVAR scaffolded / pending implementation
outputs:
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
import shutil
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

def _validate_vep_runtime_requirements(config: dict[str, Any]) -> dict[str, str]:
    vep_cfg = config["tools"]["vep"]

    executable = str(vep_cfg["executable"]).strip()
    cache_dir = Path(str(vep_cfg["cache_dir"]).strip())
    assembly = str(vep_cfg.get("assembly", "")).strip()


    resolved_executable = shutil.which(executable)
    if resolved_executable is None:
        raise FileNotFoundError(
            f"VEP executable not found on PATH: {executable}. "
            f"Install VEP or update config.tools.vep.executable."
        )

    if not cache_dir.exists():
        raise FileNotFoundError(
            f"VEP cache directory not found: {cache_dir}. "
            f"Provision the offline cache before running Stage 07."
        )

    if not cache_dir.is_dir():
        raise FileNotFoundError(
            f"VEP cache path exists but is not a directory: {cache_dir}"
        )

    if not any(cache_dir.iterdir()):
        raise FileNotFoundError(
            f"VEP cache directory is empty: {cache_dir}. "
            f"Provision the offline cache before running Stage 07."
        )

    if not assembly:
        raise ValueError(
            "VEP assembly not specified in config.tools.vep.assembly. "
            "Required value is typically GRCh38."
        )

    return {
        "vep_executable_resolved": resolved_executable,
        "vep_cache_dir": str(cache_dir),
        "vep_assembly": assembly,
    }

def _validate_annovar_runtime_requirements(config: dict[str, Any]) -> dict[str, str]:
    annovar_cfg = config["tools"]["annovar"]

    executable = str(annovar_cfg["executable"]).strip()
    humandb_dir = Path(str(annovar_cfg["humandb_dir"]).strip())

    resolved_executable = shutil.which(executable)
    if resolved_executable is None:
        raise FileNotFoundError(
            f"ANNOVAR executable not found on PATH: {executable}. "
            f"Install ANNOVAR or update config.tools.annovar.executable."
        )

    if not humandb_dir.exists():
        raise FileNotFoundError(
            f"ANNOVAR humandb directory not found: {humandb_dir}. "
            f"Provision the ANNOVAR databases before running Stage 07."
        )

    if not humandb_dir.is_dir():
        raise FileNotFoundError(
            f"ANNOVAR humandb path exists but is not a directory: {humandb_dir}"
        )

    if not any(humandb_dir.iterdir()):
        raise FileNotFoundError(
            f"ANNOVAR humandb directory is empty: {humandb_dir}. "
            f"Provision the ANNOVAR databases before running Stage 07."
        )

    return {
        "annovar_executable_resolved": resolved_executable,
        "annovar_humandb_dir": str(humandb_dir),
    }

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


def _get_annotation_engine(config: dict[str, Any]) -> str:
    engine = str(config["annotation"]["engine"]).strip().lower()
    allowed = {"vep", "annovar"}
    if engine not in allowed:
        raise ValueError(
            f"Unsupported annotation engine: {engine}. "
            f"Supported engines are: {', '.join(sorted(allowed))}"
        )
    return engine

def _validate_annotation_runtime_requirements(
    config: dict[str, Any],
    annotation_engine: str,
) -> dict[str, str]:
    if annotation_engine == "vep":
        return _validate_vep_runtime_requirements(config)

    if annotation_engine == "annovar":
        return _validate_annovar_runtime_requirements(config)

    raise ValueError(f"Unsupported annotation engine for runtime validation: {annotation_engine}")

def _build_annotation_command(
    config: dict[str, Any],
    annotation_engine: str,
    input_vcf: Path,
    output_vcf: Path,
) -> list[str]:
    if annotation_engine == "vep":
        return _build_vep_command(config, input_vcf, output_vcf)

    if annotation_engine == "annovar":
        return _build_annovar_command(config, input_vcf, output_vcf)

    raise ValueError(f"Unsupported annotation engine for command build: {annotation_engine}")

def _build_vep_command(config: dict[str, Any], input_vcf: Path, output_vcf: Path) -> list[str]:
    vep_cfg = config["tools"]["vep"]
    assembly = str(vep_cfg.get("assembly", "")).strip()
    if not assembly:
        raise ValueError("VEP assembly missing in config.tools.vep.assembly")

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
        assembly,
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
        # ClinVar flag wiring is deferred pending VEP option compatibility validation on target runtime.
        pass

    if config["annotation"]["include_population_frequencies"]:
        command.extend(["--af", "--af_1kg", "--af_gnomad", "--max_af"])

    return command

def _build_annovar_command(
    config: dict[str, Any],
    input_vcf: Path,
    output_vcf: Path,
) -> list[str]:
    annovar_cfg = config["tools"]["annovar"]

    raise NotImplementedError(
        "ANNOVAR command construction is scaffolded but not yet implemented for Stage 07. "
        f"Expected executable: {annovar_cfg['executable']}, "
        f"humandb_dir: {annovar_cfg['humandb_dir']}"
    )

def _parse_annotated_variant_record(
    annotation_engine: str,
    chrom: str,
    pos: str,
    ref: str,
    alt: str,
    info: str,
    csq_fields: list[str] | None,
    state: dict[str, Any],
    logger,
) -> dict[str, str]:
    if annotation_engine == "vep":
        info_map = _parse_info_field(info)
        csq_blob = info_map.get("CSQ", "")

        if not csq_blob:
            state["warnings"].append(
                f"Annotated VCF record missing CSQ field at {chrom}:{pos}:{ref}:{alt}"
            )
            logger.warning(
                f"Annotated VCF record missing CSQ field at {chrom}:{pos}:{ref}:{alt}"
            )
            consequence_record = {}
        else:
            first_csq = csq_blob.split(",")[0]
            csq_values = first_csq.split("|")
            if csq_fields is None:
                raise ValueError("csq_fields is required for VEP record parsing")
            if len(csq_values) < len(csq_fields):
                csq_values.extend([""] * (len(csq_fields) - len(csq_values)))
            consequence_record = dict(zip(csq_fields, csq_values))

        return {
            "gene_id": _safe_get(consequence_record, "Gene"),
            "gene_symbol": _safe_get(consequence_record, "SYMBOL").upper(),
            "transcript_id": _safe_get(consequence_record, "Feature"),
            "consequence": _safe_get(consequence_record, "Consequence"),
            "impact": _safe_get(consequence_record, "IMPACT"),
            "variant_class": _safe_get(consequence_record, "VARIANT_CLASS"),
            "clinvar_significance": _safe_get(
                consequence_record,
                "CLIN_SIG",
                "ClinVar_CLNSIG",
                "CLINVAR_CLNSIG",
            ),
            "gnomad_af": _safe_get(consequence_record, "gnomAD_AF", "AF", "MAX_AF"),
            "exac_af": _safe_get(consequence_record, "ExAC_AF"),
            "thousand_genomes_af": _safe_get(
                consequence_record,
                "AFR_AF",
                "AMR_AF",
                "EAS_AF",
                "EUR_AF",
                "SAS_AF",
                "AA_AF",
                "EA_AF",
            ),
        }

    raise NotImplementedError(
        f"Annotated record parsing for annotation engine '{annotation_engine}' is not yet implemented."
    )

def _build_annotation_output_row(
    sample_id: str,
    run_id: str,
    source_pipeline: str,
    chrom: str,
    pos: str,
    ref: str,
    alt: str,
    quality_flag: str,
    parsed_record: dict[str, str],
    union_symbol_to_gene_id: dict[str, str],
    mito_gene_ids: set[str],
    epilepsy_gene_ids: set[str],
    allowed_coding_terms: list[str],
) -> tuple[dict[str, str], int]:
    gene_id = parsed_record.get("gene_id", "NA")
    gene_symbol = parsed_record["gene_symbol"]
    transcript_id = parsed_record["transcript_id"]
    consequence = parsed_record["consequence"]
    impact = parsed_record["impact"]
    variant_class = parsed_record["variant_class"]
    clinvar_significance = parsed_record["clinvar_significance"]
    gnomad_af = parsed_record["gnomad_af"]
    exac_af = parsed_record["exac_af"]
    thousand_genomes_af = parsed_record["thousand_genomes_af"]
    impact_class = impact
    clinical_significance = clinvar_significance

    population_frequency = "NA"
    for candidate in [gnomad_af, exac_af, thousand_genomes_af]:
        if candidate not in {"", ".", "-", "NA"}:
            population_frequency = candidate
            break

    variant_id = f"{chrom}:{pos}:{ref}:{alt}"

    overlay_gene_id = union_symbol_to_gene_id.get(gene_symbol, "NA")
    resolved_gene_id = gene_id if gene_id not in {"", ".", "-", "NA"} else overlay_gene_id

    unresolved_increment = 0
    if gene_symbol != "NA" and resolved_gene_id == "NA":
        unresolved_increment = 1

    mito_flag = (
        "True"
        if resolved_gene_id in mito_gene_ids or overlay_gene_id in mito_gene_ids
        else "False"
    )
    epilepsy_flag = (
        "True"
        if resolved_gene_id in epilepsy_gene_ids or overlay_gene_id in epilepsy_gene_ids
        else "False"
    )

    variant_type = (
        "coding"
        if _consequence_is_coding(consequence, allowed_coding_terms)
        else "non-coding"
    )

    row = {
        "sample_id": sample_id,
        "run_id": run_id,
        "source_pipeline": source_pipeline,
        "variant_id": variant_id,
        "chromosome": chrom,
        "position": pos,
        "reference_allele": ref,
        "alternate_allele": alt,
        "quality_flag": quality_flag,
        "gene_id": resolved_gene_id,
        "gene_symbol": gene_symbol,
        "transcript_id": transcript_id,
        "consequence": consequence,
        "impact_class": impact_class,
        "impact": impact,
        "variant_class": variant_class,
        "variant_type": variant_type,
        "clinical_significance": clinical_significance,
        "clinvar_significance": clinvar_significance,
        "population_frequency": population_frequency,
        "gnomad_af": gnomad_af,
        "exac_af": exac_af,
        "thousand_genomes_af": thousand_genomes_af,
        "mito_flag": mito_flag,
        "epilepsy_flag": epilepsy_flag,
    }

    return row, unresolved_increment

def _validate_annotation_output_exists(
    annotation_engine: str,
    annotated_vcf: Path,
    annotated_table: Path,
) -> None:
    if annotation_engine == "vep":
        if not annotated_vcf.exists():
            raise FileNotFoundError(f"Annotated VCF was not created: {annotated_vcf}")

        if not annotated_vcf.is_file():
            raise FileNotFoundError(
                f"Annotated VCF path exists but is not a file: {annotated_vcf}"
            )

        if annotated_vcf.stat().st_size == 0:
            raise ValueError(f"Annotated VCF is empty: {annotated_vcf}")

        csq_header_found = False
        with annotated_vcf.open("r", encoding="utf-8", errors="replace") as handle:
            for line in handle:
                if line.startswith("##INFO=<ID=CSQ"):
                    csq_header_found = True
                    break
                if line.startswith("#CHROM"):
                    break

        if not csq_header_found:
            raise ValueError(
                f"Annotated VCF does not contain a VEP CSQ header: {annotated_vcf}"
            )

        return

    if annotation_engine == "annovar":
        raise NotImplementedError(
            "ANNOVAR output validation is scaffolded but not yet implemented for Stage 07. "
            f"Expected annotated VCF path: {annotated_vcf}; "
            f"expected annotated table path: {annotated_table}"
        )

    raise ValueError(
        f"Unsupported annotation engine for output validation: {annotation_engine}"
    )

def run_stage(
    config: dict[str, Any],
    paths: dict[str, Any],
    logger,
    state: dict[str, Any],
) -> dict[str, Any]:
    logger.info("Stage 07: annotating variants.")
    
    annotation_engine = _get_annotation_engine(config)
    logger.info(f"Stage 07 annotation engine selected: {annotation_engine}")
    
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

    runtime_requirements = _validate_annotation_runtime_requirements(
        config,
        annotation_engine,
    )

    if annotation_engine == "vep":
        logger.info(
            f"Resolved VEP executable: {runtime_requirements['vep_executable_resolved']}"
        )
        logger.info(
            f"Validated VEP cache directory: {runtime_requirements['vep_cache_dir']}"
        ) 
    elif annotation_engine == "annovar":
        logger.info(
            f"Resolved ANNOVAR executable: {runtime_requirements['annovar_executable_resolved']}"
        )
        logger.info(
            f"Validated ANNOVAR humandb directory: {runtime_requirements['annovar_humandb_dir']}"
        )

    sample_id = state["sample"]["sample_id"]
    run_id = state["run"]["run_id"]

    annotated_vcf = Path(paths["processed_dir"]) / f"{sample_id}_{run_id}.annotated_variants.vcf"
    annotated_table = Path(paths["processed_dir"]) / f"{sample_id}_{run_id}.annotated_variants.tsv"

    annotation_command = _build_annotation_command(
        config,
        annotation_engine,
        normalized_vcf,
        annotated_vcf,
    )

    _run_command(
        annotation_command,
        logger,
        f"{annotation_engine.upper()} annotation",
    )

    _validate_annotation_output_exists(
        annotation_engine=annotation_engine,
        annotated_vcf=annotated_vcf,
        annotated_table=annotated_table,
    )

    if annotation_engine == "vep":
        csq_fields = _extract_csq_format(annotated_vcf)
    else:
        raise NotImplementedError(
            f"Parsing logic for annotation engine '{annotation_engine}' is not yet implemented."
        )

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
        "sample_id",
        "run_id",
        "source_pipeline",
        "variant_id",
        "chromosome",
        "position",
        "reference_allele",
        "alternate_allele",
        "quality_flag",
        "gene_id",
        "gene_symbol",
        "transcript_id",
        "consequence",
        "impact_class",
        "impact",
        "variant_class",
        "variant_type",
        "clinical_significance",
        "clinvar_significance",
        "population_frequency",
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

            parsed_record = _parse_annotated_variant_record(
                annotation_engine=annotation_engine,
                chrom=chrom,
                pos=pos,
                ref=ref,
                alt=alt,
                info=info,
                csq_fields=csq_fields if annotation_engine == "vep" else None,
                state=state,
                logger=logger,
            )

            row, unresolved_increment = _build_annotation_output_row(
                sample_id=sample_id,
                run_id=run_id,
                source_pipeline=config["project"]["pipeline_name"],
                chrom=chrom,
                pos=pos,
                ref=ref,
                alt=alt,
                quality_flag="PASS",
                parsed_record=parsed_record,
                union_symbol_to_gene_id=union_symbol_to_gene_id,
                mito_gene_ids=mito_gene_ids,
                epilepsy_gene_ids=epilepsy_gene_ids,
                allowed_coding_terms=allowed_coding_terms,
            )

            unresolved_symbol_count += unresolved_increment

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

    state["annotations"]["annotation_engine"] = annotation_engine
    state["annotations"]["annotation_completed"] = True

    state["annotations"]["resources_used"] = [
        annotation_engine.upper(),
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
        "annotation_engine": annotation_engine,
        "mitocarta_gene_count": len(mito_gene_ids),
        "genes4epilepsy_gene_count": len(epilepsy_gene_ids),
        "unresolved_symbol_count": unresolved_symbol_count,
    }

    state["stage_outputs"]["stage_07_annotate_variants"] = {
        "status": "success",
        "tool": annotation_engine.upper(),
        "input_normalized_vcf": str(normalized_vcf),
        "annotated_vcf": str(annotated_vcf),
        "annotated_table": str(annotated_table),
        "annotated_variant_count": annotated_variant_count,
        "required_fields_present": required_fields_present,
        "unresolved_symbol_count": unresolved_symbol_count,
    }

    if config["runtime"]["record_tool_versions"] and annotation_engine == "vep":
        _record_vep_version(config, state, logger)

    logger.info(f"Annotated VCF written to: {annotated_vcf}")
    logger.info(f"Annotated variant table written to: {annotated_table}")
    logger.info(f"Annotated variant count: {annotated_variant_count}")
    logger.info(f"Unresolved gene symbols against overlay sets: {unresolved_symbol_count}")

    return state