"""Source-faithful genotype observation projection for VAP."""
from __future__ import annotations

import csv
import gzip
import hashlib
import json
import os
import re
import tempfile
from collections import Counter
from pathlib import Path
from typing import Any, TextIO

from pipeline.variant_identity import build_variant_id

SCHEMA_VERSION = "genotype_observation_v1"
ID_VERSION = "genotype_observation_id_v1"
SUMMARY_SCHEMA_VERSION = "genotype_projection_summary_v1"
HEADER_SCHEMA_VERSION = "genotype_source_header_context_v1"
PROJECTION_VERSION = "genotype_projection_v1"
NULL = "NA"
RECOGNIZED_FORMAT_KEYS = {"GT", "AD", "DP", "GQ", "PL", "FT"}

GENOTYPE_COLUMNS = [
    "schema_version", "genotype_observation_id", "genotype_observation_id_version",
    "entity_type", "evidence_class", "sample_id", "sample_alias", "sra_accession",
    "run_id", "vcf_sample_column_name", "sample_selection_policy",
    "sample_identity_mapping_status", "source_pipeline", "assay_type",
    "source_vcf_path", "source_vcf_sha256", "source_vcf_header_hash",
    "source_record_ordinal", "source_line_number", "source_record_hash",
    "reference_build", "chromosome", "position", "reference_allele",
    "alternate_alleles_raw", "alternate_allele_count", "alternate_allele",
    "is_multiallelic", "normalization_policy_id", "normalization_state",
    "variant_relationship_status", "variant_id", "variant_observation_id",
    "relationship_reason", "relationship_resolution_target", "format_raw",
    "sample_format_raw", "format_key_count",
    "sample_value_count", "format_alignment_status", "unknown_format_fields",
    "gt_raw", "ad_raw", "dp_raw", "gq_raw", "pl_raw", "ft_raw", "gt_status",
    "gt_arity", "gt_separator", "phase_state", "called_allele_indices",
    "missing_allele_count", "genotype_call_state", "is_no_call",
    "is_partial_no_call", "ref_depth", "alt_depth", "alt_depths_raw",
    "dp_value", "gq_value", "pl_value_count", "site_filter_raw",
    "sample_filter_raw", "record_parse_status", "record_preservation_status",
    "projection_advisory_codes", "projection_warning_codes",
]


class GenotypeProjectionError(RuntimeError):
    """Raised when a VCF cannot support governed genotype projection."""


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: str | Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(chunk_size), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _open_vcf_text(path: Path) -> TextIO:
    if path.suffix.lower() == ".gz":
        return gzip.open(path, "rt", encoding="utf-8", errors="replace", newline="")
    return path.open("r", encoding="utf-8", errors="replace", newline="")


def _logical_line(line: str) -> str:
    return line.rstrip("\r\n")


def _stable_json(payload: dict[str, Any]) -> str:
    return json.dumps(payload, indent=2, sort_keys=True) + "\n"


def _parse_structured_header(line: str) -> dict[str, str]:
    start, end = line.find("<"), line.rfind(">")
    if start < 0 or end <= start:
        return {}
    body = line[start + 1:end]
    parts, current = [], []
    quoted = escaped = False
    for char in body:
        if escaped:
            current.append(char); escaped = False; continue
        if char == "\\":
            current.append(char); escaped = True; continue
        if char == '"':
            quoted = not quoted; current.append(char); continue
        if char == "," and not quoted:
            parts.append("".join(current)); current = []; continue
        current.append(char)
    parts.append("".join(current))
    parsed: dict[str, str] = {}
    for part in parts:
        if "=" not in part:
            continue
        key, value = part.split("=", 1)
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] == '"':
            value = value[1:-1]
        parsed[key.strip()] = value
    return parsed


def _build_header_context(
    header_lines: list[str], source_label: str, source_sha: str,
    header_hash: str, reference_build: str, sample_columns: list[str],
) -> dict[str, Any]:
    formats, contigs = [], []
    caller: dict[str, Any] = {
        "annotation_assembly": reference_build, "annotation_engine": None,
        "command_line": None, "source": None, "source_version": None,
        "workflow_name": None, "workflow_version": None,
    }
    reference_declaration = None
    for line in header_lines:
        if line.startswith("##FORMAT=<"):
            p = _parse_structured_header(line)
            formats.append({"description": p.get("Description"), "id": p.get("ID"),
                            "number": p.get("Number"), "raw_header_line": line,
                            "type": p.get("Type")})
        elif line.startswith("##contig=<"):
            p = _parse_structured_header(line)
            contigs.append({"assembly": p.get("assembly") or p.get("Assembly"),
                            "id": p.get("ID"), "length": p.get("length") or p.get("Length"),
                            "raw_header_line": line})
        elif line.startswith("##reference="):
            reference_declaration = line.split("=", 1)[1]
        elif line.startswith("##source="):
            caller["source"] = line.split("=", 1)[1]
        elif line.startswith("##VEP="):
            caller["annotation_engine"] = "vep"
            caller["source_version"] = line.split("=", 1)[1]
        elif line.startswith("##GATKCommandLine"):
            caller["command_line"] = line
    return {
        "caller_metadata": caller,
        "contig_declarations": contigs,
        "format_definitions": formats,
        "reference_context": {
            "fasta_index_path": None, "fasta_index_sha256": None,
            "reference_build": reference_build,
            "reference_declaration": reference_declaration,
            "reference_fasta_path": None, "reference_fasta_sha256": None,
            "sequence_dictionary_path": None, "sequence_dictionary_sha256": None,
        },
        "sample_columns": sample_columns,
        "schema_version": HEADER_SCHEMA_VERSION,
        "source_vcf": {"header_hash": header_hash, "path": source_label, "sha256": source_sha},
    }


def _read_header(path: Path) -> tuple[list[str], list[str]]:
    header_lines, columns = [], None
    with _open_vcf_text(path) as handle:
        for raw in handle:
            line = _logical_line(raw)
            if not line.startswith("#"):
                raise GenotypeProjectionError("VCF data encountered before #CHROM header line.")
            header_lines.append(line)
            if line.startswith("#CHROM"):
                columns = line.split("\t")
                break
    if columns is None:
        raise GenotypeProjectionError("VCF #CHROM header line not found.")
    expected = ["#CHROM", "POS", "ID", "REF", "ALT", "QUAL", "FILTER", "INFO", "FORMAT"]
    if len(columns) < 10 or columns[:9] != expected:
        raise GenotypeProjectionError("Genotype projection requires canonical FORMAT and sample columns.")
    return header_lines, columns


def _resolve_sample(
    samples: list[str], sample_id: str, sample_alias: str | None,
    explicit_name: str | None,
) -> tuple[int, str, str, str]:
    if explicit_name is not None:
        if explicit_name not in samples:
            raise GenotypeProjectionError(f"Explicit VCF sample not found: {explicit_name}")
        status = "exact_match" if explicit_name == sample_id else (
            "explicit_alias_match" if sample_alias and explicit_name == sample_alias else "explicit_mapping")
        return samples.index(explicit_name), explicit_name, "explicit_sample_name", status
    if len(samples) == 1:
        selected = samples[0]
        status = "exact_match" if selected == sample_id else (
            "explicit_alias_match" if sample_alias and selected == sample_alias else "single_column_context_match")
        return 0, selected, "single_sample_column", status
    if sample_id in samples:
        return samples.index(sample_id), sample_id, "explicit_sample_name", "exact_match"
    if sample_alias and sample_alias in samples:
        return samples.index(sample_alias), sample_alias, "explicit_sample_name", "explicit_alias_match"
    raise GenotypeProjectionError("Multisample VCF requires an explicit governed sample selection.")


def _map_format(format_raw: str, sample_raw: str):
    if format_raw in {"", "."}:
        return [], [], {}, "format_missing", ["missing_format"], []
    keys = format_raw.split(":")
    if sample_raw in {"", "."}:
        return keys, [], {}, "sample_field_missing", ["missing_sample_field"], []
    values = sample_raw.split(":")
    if len(values) == len(keys):
        alignment, warnings, unmatched = "aligned", [], []
    elif len(values) < len(keys):
        alignment, warnings, unmatched = "sample_values_shorter", ["sample_values_shorter_than_format"], []
    else:
        alignment, warnings, unmatched = "sample_values_longer", ["sample_values_longer_than_format"], values[len(keys):]
    mapping = {key: values[i] if i < len(values) else NULL for i, key in enumerate(keys)}
    return keys, values, mapping, alignment, warnings, unmatched


def _percent_encode_unknown(value: str) -> str:
    replacements = {"%": "%25", ";": "%3B", "=": "%3D", "\t": "%09", "\r": "%0D", "\n": "%0A"}
    return "".join(replacements.get(char, char) for char in value)


def _unknown_fields(keys: list[str], mapping: dict[str, str], unmatched: list[str]) -> str:
    pairs = [f"{_percent_encode_unknown(key)}={_percent_encode_unknown(mapping.get(key, NULL))}"
             for key in keys if key not in RECOGNIZED_FORMAT_KEYS]
    pairs.extend(f"__UNMATCHED_VALUE_{i}={_percent_encode_unknown(value)}"
                 for i, value in enumerate(unmatched, start=1))
    return ";".join(pairs) if pairs else NULL


_GT_TOKEN = re.compile(r"^\d+$")


def _parse_gt(raw: str) -> dict[str, str]:
    base = {"called_allele_indices": NULL, "genotype_call_state": "NA", "gt_arity": NULL,
            "gt_separator": "NA", "gt_status": "absent_from_format", "is_no_call": "False",
            "is_partial_no_call": "False", "missing_allele_count": NULL, "phase_state": "unknown"}
    if raw == NULL:
        return base
    if raw in {"", "."}:
        base.update({"genotype_call_state": "complete_no_call", "gt_arity": "1",
                     "gt_separator": "none", "gt_status": "missing_value" if raw == "" else "complete_no_call",
                     "is_no_call": "True", "missing_allele_count": "1", "phase_state": "not_applicable"})
        return base
    separators = re.findall(r"[/|]", raw)
    tokens = re.split(r"[/|]", raw)
    if any(not token or (token != "." and not _GT_TOKEN.match(token)) for token in tokens):
        base.update({"genotype_call_state": "unparseable", "gt_arity": str(len(tokens)),
                     "gt_status": "malformed", "phase_state": "malformed_or_complex"})
        return base
    if not separators:
        separator, phase = "none", "not_applicable"
    elif all(x == "/" for x in separators):
        separator, phase = "/", "unphased"
    elif all(x == "|" for x in separators):
        separator, phase = "|", "phased"
    else:
        base.update({
            "genotype_call_state": "unparseable",
            "gt_arity": str(len(tokens)),
            "gt_separator": "mixed",
            "gt_status": "malformed",
            "phase_state": "malformed_or_complex",
        })
        return base
    missing = sum(token == "." for token in tokens)
    called = [token for token in tokens if token != "."]
    if missing == len(tokens):
        status, state, no_call, partial = "complete_no_call", "complete_no_call", "True", "False"
    elif missing:
        status, state, no_call, partial = "partial_no_call", "partial_no_call", "False", "True"
    else:
        status, no_call, partial = "present_parseable", "False", "False"
        ints = [int(token) for token in tokens]
        if len(ints) == 1:
            state = "single_allele_reference_call" if ints[0] == 0 else "single_allele_alternate_call"
        elif all(x == 0 for x in ints):
            state = "homozygous_reference_call"
        elif len(set(ints)) == 1 and ints[0] > 0:
            state = "homozygous_alternate_call"
        elif 0 in ints and any(x > 0 for x in ints):
            state = "heterozygous_call"
        elif len(set(ints)) > 1:
            state = "alternate_alleles_differ"
        else:
            state = "other_parseable_call"
    base.update({"called_allele_indices": ",".join(called) if called else NULL,
                 "genotype_call_state": state, "gt_arity": str(len(tokens)),
                 "gt_separator": separator, "gt_status": status, "is_no_call": no_call,
                 "is_partial_no_call": partial, "missing_allele_count": str(missing), "phase_state": phase})
    return base


def _integer(raw: str) -> str:
    if raw in {NULL, "", "."}:
        return NULL
    try:
        return str(int(raw, 10))
    except ValueError:
        return NULL


def _depths(ad_raw: str, alt_count: int) -> dict[str, str]:
    result = {"ref_depth": NULL, "alt_depth": NULL, "alt_depths_raw": NULL}
    if ad_raw in {NULL, "", "."}:
        return result
    values = ad_raw.split(",")
    result["ref_depth"] = _integer(values[0])
    result["alt_depths_raw"] = ",".join(values[1:]) if len(values) > 1 else NULL
    if alt_count == 1 and len(values) > 1:
        result["alt_depth"] = _integer(values[1])
    return result


def _record_parse_status(alignment: str, gt_status: str) -> str:
    if alignment == "format_missing": return "missing_format_preserved"
    if alignment == "sample_field_missing": return "missing_sample_field_preserved"
    if alignment in {"sample_values_shorter", "sample_values_longer"}: return "format_alignment_warning"
    if gt_status == "malformed": return "malformed_gt_preserved"
    return "parsed"



def _called_allele_index_out_of_range(
    called_allele_indices: str,
    alternate_allele_count: int,
) -> bool:
    """Return True when a parsed called allele index exceeds ALT cardinality."""
    if called_allele_indices == NULL:
        return False
    for token in called_allele_indices.split(","):
        if token == "":
            continue
        try:
            allele_index = int(token, 10)
        except ValueError:
            return True
        if allele_index < 0 or allele_index > alternate_allele_count:
            return True
    return False


def _contains_symbolic_alt(alternate_alleles: list[str]) -> bool:
    return any(
        allele.startswith("<") and allele.endswith(">")
        for allele in alternate_alleles
    )


def _contains_spanning_deletion(alternate_alleles: list[str]) -> bool:
    return "*" in alternate_alleles


def _classify_variant_relationship(
    *,
    chromosome: str,
    position: str,
    reference_allele: str,
    alternate_alleles: list[str],
    genotype: dict[str, str],
    format_alignment_status: str,
) -> tuple[str, str, str, str, list[str], list[str]]:
    """
    Classify the VAP producer-side genotype-to-variant relationship.

    Returns:
        status,
        reason,
        resolution_target,
        variant_id,
        advisories,
        warnings
    """
    advisories: list[str] = []
    warnings: list[str] = []
    alternate_count = len(alternate_alleles)

    if format_alignment_status in {
        "format_missing",
        "sample_field_missing",
        "sample_values_shorter",
        "sample_values_longer",
    }:
        warnings.append("format_sample_mismatch")
        return (
            "unresolved",
            "format_sample_mismatch",
            "not_resolvable_by_vap",
            NULL,
            advisories,
            warnings,
        )

    gt_status = genotype["gt_status"]
    if gt_status == "absent_from_format":
        warnings.append("missing_gt")
        return (
            "unresolved",
            "missing_gt",
            "not_resolvable_by_vap",
            NULL,
            advisories,
            warnings,
        )
    if gt_status == "complete_no_call":
        return (
            "not_applicable",
            "no_call",
            "none",
            NULL,
            advisories,
            warnings,
        )
    if gt_status == "partial_no_call":
        advisories.append("partial_no_call_relationship_deferred_to_vdb")
        return (
            "unresolved",
            "partial_no_call",
            "vdb_brokerage",
            NULL,
            advisories,
            warnings,
        )
    if gt_status == "malformed":
        warnings.append("malformed_gt")
        return (
            "unresolved",
            "malformed_gt",
            "not_resolvable_by_vap",
            NULL,
            advisories,
            warnings,
        )

    if _called_allele_index_out_of_range(
        genotype["called_allele_indices"],
        alternate_count,
    ):
        warnings.append("called_allele_index_out_of_range")
        return (
            "unresolved",
            "called_allele_index_out_of_range",
            "not_resolvable_by_vap",
            NULL,
            advisories,
            warnings,
        )

    if alternate_count == 0:
        warnings.append("variant_identity_unavailable")
        return (
            "unresolved",
            "variant_identity_unavailable",
            "vdb_brokerage",
            NULL,
            advisories,
            warnings,
        )

    if _contains_spanning_deletion(alternate_alleles):
        advisories.append("spanning_deletion_relationship_deferred_to_vdb")
        return (
            "complex",
            "spanning_deletion",
            "vdb_brokerage",
            NULL,
            advisories,
            warnings,
        )

    if _contains_symbolic_alt(alternate_alleles):
        advisories.append("symbolic_alt_relationship_deferred_to_vdb")
        return (
            "complex",
            "symbolic_alt",
            "vdb_brokerage",
            NULL,
            advisories,
            warnings,
        )

    if alternate_count > 1:
        advisories.append("multiallelic_relationship_deferred_to_vdb")
        return (
            "complex",
            "multiallelic_source_record",
            "vdb_brokerage",
            NULL,
            advisories,
            warnings,
        )

    alternate_allele = alternate_alleles[0]
    return (
        "direct",
        "biallelic_direct",
        "none",
        build_variant_id(
            chromosome,
            position,
            reference_allele,
            alternate_allele,
        ),
        advisories,
        warnings,
    )


def project_genotype_observations(
    *, annotated_vcf_path: str | Path, output_directory: str | Path,
    sample_id: str, run_id: str, reference_build: str, source_pipeline: str,
    sample_alias: str | None = None, sra_accession: str | None = None,
    assay_type: str | None = None, explicit_vcf_sample_name: str | None = None,
    source_vcf_path_label: str | None = None,
    normalization_policy_id: str | None = None, normalization_state: str | None = None,
) -> dict[str, Any]:
    source = Path(annotated_vcf_path)
    out = Path(output_directory)
    if not source.is_file() or source.stat().st_size == 0:
        raise FileNotFoundError(f"Readable annotated VCF not found: {source}")
    header_lines, columns = _read_header(source)
    samples = columns[9:]
    sample_index, selected, selection_policy, mapping_status = _resolve_sample(
        samples, sample_id, sample_alias, explicit_vcf_sample_name)
    source_label = source_vcf_path_label or str(source)
    source_sha = sha256_file(source)
    header_hash = _sha256_bytes("".join(f"{line}\n" for line in header_lines).encode("utf-8"))
    header_payload = _build_header_context(header_lines, source_label, source_sha,
                                           header_hash, reference_build, samples)
    observations = out / "genotype_observations.tsv"
    summary = out / "genotype_projection_summary.json"
    header_context = out / "genotype_source_header_context.json"
    out.mkdir(parents=True, exist_ok=True)
    temporary: list[Path] = []
    counts = Counter()
    advisory_counts = Counter()
    warning_counts = Counter()
    status_counts = {name: Counter() for name in ["format_alignment_status", "genotype_call_state",
        "gt_status", "phase_state", "record_parse_status", "variant_relationship_status"]}
    try:
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", newline="", dir=out,
                                         prefix=".genotype_observations.", suffix=".tmp", delete=False) as handle:
            tsv_tmp = Path(handle.name); temporary.append(tsv_tmp)
            writer = csv.DictWriter(handle, fieldnames=GENOTYPE_COLUMNS, delimiter="\t",
                                    lineterminator="\n", extrasaction="raise")
            writer.writeheader()
            with _open_vcf_text(source) as source_handle:
                ordinal = line_number = 0
                for raw_line in source_handle:
                    line_number += 1
                    line = _logical_line(raw_line)
                    if line.startswith("#") or line == "":
                        continue
                    ordinal += 1; counts["source_record_count"] += 1
                    fields = line.split("\t")
                    if len(fields) < 9 or any(fields[i] == "" for i in (0, 1, 3, 4)):
                        counts["irreparably_malformed_record_count"] += 1
                        warning_counts["irreparably_malformed_record"] += 1
                        continue
                    sample_col = 9 + sample_index
                    sample_raw = fields[sample_col] if sample_col < len(fields) else "."
                    chrom, pos, _id, ref, alt_raw, _qual, site_filter, _info, format_raw = fields[:9]
                    alts = alt_raw.split(",") if alt_raw not in {"", "."} else []
                    alt_count = len(alts); multiallelic = alt_count > 1
                    alternate = alts[0] if alt_count == 1 else NULL
                    keys, values, mapping, alignment, format_warnings, unmatched = _map_format(
                        format_raw,
                        sample_raw,
                    )
                    unknown = _unknown_fields(keys, mapping, unmatched)
                    raw_values = {
                        f"{key.lower()}_raw": mapping.get(key, NULL)
                        for key in RECOGNIZED_FORMAT_KEYS
                    }
                    gt = _parse_gt(raw_values["gt_raw"])

                    (
                        relationship,
                        reason,
                        resolution_target,
                        variant_id,
                        relationship_advisories,
                        relationship_warnings,
                    ) = _classify_variant_relationship(
                        chromosome=chrom,
                        position=pos,
                        reference_allele=ref,
                        alternate_alleles=alts,
                        genotype=gt,
                        format_alignment_status=alignment,
                    )

                    advisories = list(relationship_advisories)
                    warnings = list(format_warnings)
                    warnings.extend(relationship_warnings)
                    if unknown != NULL:
                        advisories.append("unknown_format_fields_preserved")

                    advisories = sorted(set(advisories))
                    warnings = sorted(set(warnings))
                    for advisory in advisories:
                        advisory_counts[advisory] += 1
                    for warning in warnings:
                        warning_counts[warning] += 1

                    record_parse_status = _record_parse_status(
                        alignment,
                        gt["gt_status"],
                    )
                    if reason in {
                        "malformed_gt",
                        "called_allele_index_out_of_range",
                    }:
                        record_parse_status = "malformed_gt_preserved"
                    elif reason == "missing_gt":
                        record_parse_status = "missing_gt_preserved"

                    record_hash = _sha256_bytes(line.encode("utf-8"))
                    identity = _sha256_bytes("|".join([ID_VERSION, run_id, selected, source_sha,
                                                       str(ordinal), record_hash]).encode("utf-8"))
                    row = {
                        "schema_version": SCHEMA_VERSION, "genotype_observation_id": identity,
                        "genotype_observation_id_version": ID_VERSION, "entity_type": "genotype_observation",
                        "evidence_class": "caller_emitted_sample_genotype", "sample_id": sample_id,
                        "sample_alias": sample_alias or NULL, "sra_accession": sra_accession or NULL,
                        "run_id": run_id, "vcf_sample_column_name": selected,
                        "sample_selection_policy": selection_policy,
                        "sample_identity_mapping_status": mapping_status, "source_pipeline": source_pipeline,
                        "assay_type": assay_type or NULL, "source_vcf_path": source_label,
                        "source_vcf_sha256": source_sha, "source_vcf_header_hash": header_hash,
                        "source_record_ordinal": str(ordinal), "source_line_number": str(line_number),
                        "source_record_hash": record_hash, "reference_build": reference_build,
                        "chromosome": chrom, "position": pos, "reference_allele": ref,
                        "alternate_alleles_raw": alt_raw, "alternate_allele_count": str(alt_count),
                        "alternate_allele": alternate, "is_multiallelic": "True" if multiallelic else "False",
                        "normalization_policy_id": normalization_policy_id or NULL,
                        "normalization_state": normalization_state or NULL,
                        "variant_relationship_status": relationship, "variant_id": variant_id,
                        "variant_observation_id": NULL, "relationship_reason": reason,
                        "relationship_resolution_target": resolution_target,
                        "format_raw": format_raw, "sample_format_raw": sample_raw,
                        "format_key_count": str(len(keys)), "sample_value_count": str(len(values)),
                        "format_alignment_status": alignment, "unknown_format_fields": unknown,
                        **raw_values, **gt, **_depths(raw_values["ad_raw"], alt_count),
                        "dp_value": _integer(raw_values["dp_raw"]),
                        "gq_value": _integer(raw_values["gq_raw"]),
                        "pl_value_count": str(len(raw_values["pl_raw"].split(",")))
                            if raw_values["pl_raw"] not in {NULL, "", "."} else NULL,
                        "site_filter_raw": site_filter, "sample_filter_raw": raw_values["ft_raw"],
                        "record_parse_status": record_parse_status,
                        "record_preservation_status": "preserved_from_source_vcf",
                        "projection_advisory_codes": ";".join(advisories) if advisories else NULL,
                        "projection_warning_codes": ";".join(warnings) if warnings else NULL,
                    }
                    writer.writerow(row); counts["genotype_observation_row_count"] += 1
                    counts["gt_absent_count" if gt["gt_status"] == "absent_from_format" else "gt_present_count"] += 1
                    for state, key in [("complete_no_call","complete_no_call_count"),
                                       ("partial_no_call","partial_no_call_count")]:
                        if gt["gt_status"] == state: counts[key] += 1
                    for key, name in [("AD","ad_present_count"),("DP","dp_present_count"),
                                      ("GQ","gq_present_count"),("PL","pl_present_count"),
                                      ("FT","ft_present_count")]:
                        if key in keys: counts[name] += 1
                    if multiallelic: counts["multiallelic_record_count"] += 1
                    if gt["phase_state"] == "phased": counts["phased_gt_count"] += 1
                    if gt["phase_state"] == "unphased": counts["unphased_gt_count"] += 1
                    if gt["gt_status"] == "malformed": counts["malformed_gt_count"] += 1
                    if alignment != "aligned":
                        counts["format_sample_mismatch_count"] += 1
                    counts[f"{relationship}_relationship_count"] += 1
                    if reason == "multiallelic_source_record":
                        counts["multiallelic_relationship_deferred_count"] += 1
                    elif reason == "symbolic_alt":
                        counts["symbolic_alt_deferred_count"] += 1
                    elif reason == "spanning_deletion":
                        counts["spanning_deletion_deferred_count"] += 1
                    elif reason == "called_allele_index_out_of_range":
                        counts["called_allele_index_out_of_range_count"] += 1
                    elif reason == "missing_gt":
                        counts["missing_gt_count"] += 1
                    elif reason == "no_call":
                        counts["no_call_count"] += 1
                    elif reason == "partial_no_call":
                        counts["partial_no_call_relationship_count"] += 1
                    for name, counter in status_counts.items():
                        counter[row[name]] += 1
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", newline="", dir=out,
                                         prefix=".genotype_header_context.", suffix=".tmp", delete=False) as handle:
            header_tmp = Path(handle.name); temporary.append(header_tmp); handle.write(_stable_json(header_payload))
        obs_sha, header_sha = sha256_file(tsv_tmp), sha256_file(header_tmp)
        count_names = [
            "genotype_observation_row_count",
            "gt_present_count",
            "gt_absent_count",
            "complete_no_call_count",
            "partial_no_call_count",
            "ad_present_count",
            "dp_present_count",
            "gq_present_count",
            "pl_present_count",
            "ft_present_count",
            "multiallelic_record_count",
            "phased_gt_count",
            "unphased_gt_count",
            "malformed_gt_count",
            "format_sample_mismatch_count",
            "direct_relationship_count",
            "complex_relationship_count",
            "unresolved_relationship_count",
            "not_applicable_relationship_count",
            "multiallelic_relationship_deferred_count",
            "symbolic_alt_deferred_count",
            "spanning_deletion_deferred_count",
            "called_allele_index_out_of_range_count",
            "missing_gt_count",
            "no_call_count",
            "partial_no_call_relationship_count",
        ]
        projection_error_count = counts["irreparably_malformed_record_count"]
        projection_warning_count = sum(warning_counts.values())
        projection_advisory_count = sum(advisory_counts.values())
        if projection_error_count or projection_warning_count:
            projection_status = "pass_with_warnings"
        elif projection_advisory_count:
            projection_status = "pass_with_advisory"
        else:
            projection_status = "pass"

        summary_payload = {
            "counts": {
                **{name: counts[name] for name in count_names},
                "projection_advisory_count": projection_advisory_count,
                "projection_warning_count": projection_warning_count,
                "projection_error_count": projection_error_count,
            },
            "outputs": {"genotype_observations_path": observations.name,
                        "genotype_observations_sha256": obs_sha,
                        "header_context_path": header_context.name, "header_context_sha256": header_sha},
            "projection": {"projection_status": projection_status,
                           "projection_version": PROJECTION_VERSION, "reference_build": reference_build,
                           "source_pipeline": source_pipeline},
            "sample_resolution": {"run_id": run_id, "sample_id": sample_id,
                                  "sample_identity_mapping_status": mapping_status,
                                  "sample_selection_policy": selection_policy,
                                  "vcf_sample_column_name": selected},
            "schema_version": SUMMARY_SCHEMA_VERSION,
            "source_vcf": {"header_hash": header_hash,
                           "irreparably_malformed_record_count": counts["irreparably_malformed_record_count"],
                           "path": source_label, "sha256": source_sha,
                           "source_record_count": counts["source_record_count"]},
            "status_counts": {name: dict(sorted(counter.items())) for name, counter in sorted(status_counts.items())},
            "advisories": [{"code": code, "count": count}
                           for code, count in sorted(advisory_counts.items())],
            "warnings": [{"code": code, "count": count}
                         for code, count in sorted(warning_counts.items())],
        }
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", newline="", dir=out,
                                         prefix=".genotype_projection_summary.", suffix=".tmp", delete=False) as handle:
            summary_tmp = Path(handle.name); temporary.append(summary_tmp); handle.write(_stable_json(summary_payload))
        if counts["source_record_count"] != counts["genotype_observation_row_count"] + counts["irreparably_malformed_record_count"]:
            raise GenotypeProjectionError("Source-record cardinality invariant failed.")
        for temp_path, destination in [(tsv_tmp, observations), (header_tmp, header_context), (summary_tmp, summary)]:
            os.replace(temp_path, destination)
        temporary.clear()
        return {"genotype_observations": str(observations),
                "genotype_projection_summary": str(summary),
                "genotype_source_header_context": str(header_context),
                "projection_status": summary_payload["projection"]["projection_status"],
                "row_count": counts["genotype_observation_row_count"],
                "source_record_count": counts["source_record_count"]}
    except Exception:
        for path in temporary: path.unlink(missing_ok=True)
        raise
