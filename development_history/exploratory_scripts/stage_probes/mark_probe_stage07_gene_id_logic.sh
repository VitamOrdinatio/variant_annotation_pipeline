#!/usr/bin/env bash
set -euo pipefail

TS="$(date +%Y%m%d_%H%M%S)"
LOG="/root/Desktop/mark_probe_stage07_gene_id_logic_${TS}.log"
REPO_ROOT="$HOME/dev/portfolio_projects/variant_annotation_pipeline"

exec > >(tee "$LOG") 2>&1

echo "[INFO] Mark Stage 07 gene_id logic probe started at $(date)"
echo "[INFO] Log file: $LOG"
echo "[INFO] Repo root: $REPO_ROOT"
echo

cd "$REPO_ROOT"

echo "[STEP] Activating VAP .venv"
source .venv/bin/activate
echo "[INFO] Venv activated."
echo

echo "=== CODE PRESENCE CHECK ==="
grep -n '"gene_id": _safe_get(consequence_record, "Gene")\|overlay_gene_id\|resolved_gene_id = gene_id' pipeline/stage_07_annotate_variants.py || true
echo

echo "=== FIND LATEST ANNOTATED VCF ==="
ANNOTATED_VCF="$(find "$REPO_ROOT/results" -type f -name "*.annotated_variants.vcf" | sort | tail -n 1 || true)"
if [[ -z "${ANNOTATED_VCF:-}" ]]; then
  echo "[ERROR] No annotated VCF found under $REPO_ROOT/results"
  exit 1
fi
echo "[INFO] ANNOTATED_VCF=$ANNOTATED_VCF"
echo

echo "=== PYTHON PARSER PROBE ON FIRST CSQ RECORD ==="
python - <<'PY'
from pathlib import Path

from pipeline.stage_07_annotate_variants import (
    _extract_csq_format,
    _parse_annotated_variant_record,
    _build_annotation_output_row,
)

class ProbeLogger:
    def warning(self, msg): print(f"[LOGGER][WARN] {msg}")
    def info(self, msg): print(f"[LOGGER][INFO] {msg}")

repo_root = Path("/root/dev/portfolio_projects/variant_annotation_pipeline")
annotated_vcfs = sorted((repo_root / "results").rglob("*.annotated_variants.vcf"))
if not annotated_vcfs:
    raise SystemExit("No annotated VCF found")
vcf_path = annotated_vcfs[-1]

csq_fields = _extract_csq_format(vcf_path)
print("CSQ_FIELDS_FIRST_12=", csq_fields[:12])

first_record = None
with vcf_path.open("r", encoding="utf-8", errors="replace") as handle:
    for line in handle:
        if line.startswith("#"):
            continue
        if "CSQ=" in line:
            first_record = line.rstrip("\n")
            break

if first_record is None:
    raise SystemExit("No CSQ record found")

fields = first_record.split("\t")
chrom, pos, _vid, ref, alt, qual, filt, info = fields[:8]

state = {"warnings": []}
logger = ProbeLogger()

parsed = _parse_annotated_variant_record(
    annotation_engine="vep",
    chrom=chrom,
    pos=pos,
    ref=ref,
    alt=alt,
    info=info,
    csq_fields=csq_fields,
    state=state,
    logger=logger,
)

print("PARSED_RECORD_KEY_FIELDS")
for key in ["gene_id", "gene_symbol", "transcript_id", "consequence", "impact", "variant_class"]:
    print(f"{key}={parsed.get(key)}")

row, unresolved_increment = _build_annotation_output_row(
    sample_id="HG002",
    run_id="probe_run",
    source_pipeline="variant_annotation_pipeline",
    chrom=chrom,
    pos=pos,
    ref=ref,
    alt=alt,
    quality_flag="PASS",
    parsed_record=parsed,
    union_symbol_to_gene_id={},
    mito_gene_ids=set(),
    epilepsy_gene_ids=set(),
    allowed_coding_terms=[
        "missense_variant",
        "synonymous_variant",
        "stop_gained",
        "stop_lost",
        "start_lost",
        "frameshift_variant",
        "inframe_insertion",
        "inframe_deletion",
        "protein_altering_variant",
    ],
)

print("OUTPUT_ROW_KEY_FIELDS")
for key in ["variant_id", "gene_id", "gene_symbol", "transcript_id", "consequence", "variant_class", "variant_type", "mito_flag", "epilepsy_flag"]:
    print(f"{key}={row.get(key)}")

print(f"unresolved_increment={unresolved_increment}")
print(f"warnings={state['warnings']}")
PY
echo

echo "=== EXISTING STAGE 07 TSV FIRST ROW CHECK (PRE-RERUN MAY STILL SHOW OLD NA) ==="
ANNOTATED_TSV="$(find "$REPO_ROOT/results" -type f -name "*.annotated_variants.tsv" | sort | tail -n 1 || true)"
if [[ -n "${ANNOTATED_TSV:-}" ]]; then
  echo "[INFO] ANNOTATED_TSV=$ANNOTATED_TSV"
  head -n 2 "$ANNOTATED_TSV" | column -t -s $'\t' || true
else
  echo "[WARN] No annotated TSV found."
fi
echo

echo "[INFO] Mark Stage 07 gene_id logic probe completed at $(date)"
echo "[INFO] Log file saved to: $LOG"