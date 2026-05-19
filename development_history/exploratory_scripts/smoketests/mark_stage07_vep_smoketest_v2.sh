#!/usr/bin/env bash
set -euo pipefail

TS="$(date +%Y%m%d_%H%M%S)"
LOG="/root/Desktop/mark_stage07_vep_smoketest_v2_${TS}.log"
REPO_ROOT="$HOME/dev/portfolio_projects/variant_annotation_pipeline"
RESULTS_ROOT="$REPO_ROOT/results"
VEP_EXEC="/root/tools/vep/vep"
CACHE_DIR="/root/.vep"
ASSEMBLY="GRCh38"
SPECIES="homo_sapiens"

exec > >(tee "$LOG") 2>&1

echo "[INFO] Mark Stage 07 VEP smoke test v2 started at $(date)"
echo "[INFO] Log file: $LOG"
echo "[INFO] Repo root: $REPO_ROOT"
echo "[INFO] Results root: $RESULTS_ROOT"
echo "[INFO] VEP executable: $VEP_EXEC"
echo "[INFO] CACHE_DIR: $CACHE_DIR"
echo "[INFO] ASSEMBLY: $ASSEMBLY"
echo "[INFO] SPECIES: $SPECIES"
echo

cd "$REPO_ROOT"
source .venv/bin/activate

echo "=== FIND LATEST NORMALIZED VCF ==="
LATEST_VCF="$(find "$RESULTS_ROOT" -type f -name "*.normalized_variants.vcf" | sort | tail -n 1 || true)"
if [[ -z "${LATEST_VCF:-}" ]]; then
  echo "[ERROR] No normalized VCF found under $RESULTS_ROOT"
  exit 1
fi
echo "[INFO] LATEST_VCF=$LATEST_VCF"
echo

TMP_DIR="$REPO_ROOT/results/bootstrap_logs/stage07_smoketest_v2_${TS}"
mkdir -p "$TMP_DIR"
SMOKE_VCF="$TMP_DIR/smoke_input.vcf"
SMOKE_OUT="$TMP_DIR/vep_smoke_output.vcf"

python - <<'PY' "$LATEST_VCF" "$SMOKE_VCF"
import sys
from pathlib import Path

src = Path(sys.argv[1])
dst = Path(sys.argv[2])

header = []
variant_line = None

with src.open() as fh:
    for line in fh:
        if line.startswith("#"):
            header.append(line)
        else:
            variant_line = line
            break

if variant_line is None:
    raise SystemExit("No variant lines found in source VCF")

with dst.open("w") as out:
    for line in header:
        out.write(line)
    out.write(variant_line)
PY

echo "=== DIRECT VEP SMOKETEST (STAGE 07 MIRROR) ==="
echo "[CMD] $VEP_EXEC --input_file $SMOKE_VCF --output_file $SMOKE_OUT --format vcf --vcf --force_overwrite --species $SPECIES --assembly $ASSEMBLY --cache --offline --dir_cache $CACHE_DIR --symbol --biotype --transcript_version --canonical --mane --variant_class --pick --pick_order canonical,appris,tsl,biotype,rank,ccds,length --fork 4"
"$VEP_EXEC" \
  --input_file "$SMOKE_VCF" \
  --output_file "$SMOKE_OUT" \
  --format vcf \
  --vcf \
  --force_overwrite \
  --species "$SPECIES" \
  --assembly "$ASSEMBLY" \
  --cache \
  --offline \
  --dir_cache "$CACHE_DIR" \
  --symbol \
  --biotype \
  --transcript_version \
  --canonical \
  --mane \
  --variant_class \
  --pick \
  --pick_order "canonical,appris,tsl,biotype,rank,ccds,length" \
  --fork 4 || true
echo

echo "=== CHECK OUTPUT ==="
ls -lah "$TMP_DIR" || true
echo
if [[ -f "$SMOKE_OUT" ]]; then
  head -n 40 "$SMOKE_OUT" || true
else
  echo "[WARN] VEP output file not created."
fi
echo

echo "[INFO] Mark Stage 07 VEP smoke test v2 completed at $(date)"
echo "[INFO] Log file saved to: $LOG"