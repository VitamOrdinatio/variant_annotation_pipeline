#!/usr/bin/env bash
set -euo pipefail

TS="$(date +%Y%m%d_%H%M%S)"
LOG="/root/Desktop/mark_probe_stage08_variant_type_logic_${TS}.log"
REPO_ROOT="$HOME/dev/portfolio_projects/variant_annotation_pipeline"

exec > >(tee "$LOG") 2>&1

echo "[INFO] Mark Stage 08 variant_type logic probe started at $(date)"
echo "[INFO] Log file: $LOG"
echo "[INFO] Repo root: $REPO_ROOT"
echo

cd "$REPO_ROOT"

echo "[STEP] Activating VAP .venv"
source .venv/bin/activate
echo "[INFO] Venv activated."
echo

echo "=== CODE PRESENCE CHECK ==="
echo "[CMD] grep -n '_derive_variant_type_from_alleles\\|explicit_variant_type\\|variant_type =' pipeline/stage_08_filter_and_partition.py"
grep -n "_derive_variant_type_from_alleles\|explicit_variant_type\|variant_type =" pipeline/stage_08_filter_and_partition.py || true
echo

echo "=== DIRECT HELPER FUNCTION TEST ==="
python - <<'PY'
from pipeline.stage_08_filter_and_partition import _derive_variant_type_from_alleles

tests = [
    ("G", "A"),
    ("G", "GA"),
    ("GA", "G"),
    ("GA", "TC"),
    ("NA", "A"),
    ("G", "NA"),
    ("G", "A,T"),
]

for ref, alt in tests:
    print(f"{ref}/{alt} -> {_derive_variant_type_from_alleles(ref, alt)}")
PY
echo

echo "=== FIRST STAGE 07 TSV ROW COERCION TEST ==="
python - <<'PY'
import csv
from pathlib import Path

from pipeline.stage_08_filter_and_partition import (
    _coerce_stage08_row,
    _derive_variant_type_from_alleles,
    _is_missing,
)

repo_root = Path("/root/dev/portfolio_projects/variant_annotation_pipeline")
annotated_tsvs = sorted((repo_root / "results").rglob("*.annotated_variants.tsv"))

if not annotated_tsvs:
    raise SystemExit("No annotated_variants.tsv found")

input_tsv = annotated_tsvs[-1]
print(f"INPUT_TSV={input_tsv}")

with input_tsv.open("r", encoding="utf-8", errors="replace", newline="") as handle:
    reader = csv.DictReader(handle, delimiter="\t")
    print("FIELDNAMES_BEGIN")
    print(reader.fieldnames)
    print("FIELDNAMES_END")

    first_row = next(reader)

print("RAW_FIRST_ROW_KEY_FIELDS")
for key in [
    "variant_id",
    "reference_allele",
    "alternate_allele",
    "variant_type",
    "variant_class",
    "consequence",
    "impact_class",
]:
    print(f"{key}={first_row.get(key)}")

explicit_variant_type = first_row.get("variant_type")
print(f"explicit_variant_type={explicit_variant_type!r}")
print(f"_is_missing(explicit_variant_type)={_is_missing(explicit_variant_type)}")
print(
    "direct_allele_derivation="
    + _derive_variant_type_from_alleles(
        first_row.get("reference_allele"),
        first_row.get("alternate_allele"),
    )
)

coerced_row, partition_contexts = _coerce_stage08_row(
    input_row=first_row,
    annotation_source="VEP",
    annotation_version="115",
)

print("COERCED_FIRST_ROW_KEY_FIELDS")
for key in [
    "variant_id",
    "reference_allele",
    "alternate_allele",
    "variant_type",
    "variant_class",
    "variant_context",
    "variant_effect_severity",
    "frequency_status",
    "clinical_status",
    "qc_status",
]:
    print(f"{key}={coerced_row.get(key)}")

print(f"partition_contexts={sorted(partition_contexts)}")
PY
echo

echo "=== CURRENT SUMMARY VARIANT_TYPE CHECK ==="
SUMMARY_JSON="$(find "$REPO_ROOT/results" -type f -name "stage_08_summary.json" | sort | tail -n 1 || true)"
if [[ -n "${SUMMARY_JSON:-}" ]]; then
  echo "[INFO] SUMMARY_JSON=$SUMMARY_JSON"
  grep -A 10 '"variants_by_variant_type"' "$SUMMARY_JSON" || true
else
  echo "[WARN] No stage_08_summary.json found."
fi
echo

echo "[INFO] Mark Stage 08 variant_type logic probe completed at $(date)"
echo "[INFO] Log file saved to: $LOG"