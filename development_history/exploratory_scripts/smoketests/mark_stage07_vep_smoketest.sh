#!/usr/bin/env bash
set -euo pipefail

TS="$(date +%Y%m%d_%H%M%S)"
LOG="/root/Desktop/mark_stage07_vep_smoketest_${TS}.log"
REPO_ROOT="$HOME/dev/portfolio_projects/variant_annotation_pipeline"
RESULTS_ROOT="$REPO_ROOT/results"
VEP_EXEC="/root/tools/vep/vep"

exec > >(tee "$LOG") 2>&1

echo "[INFO] Mark Stage 07 VEP smoke test started at $(date)"
echo "[INFO] Log file: $LOG"
echo "[INFO] Repo root: $REPO_ROOT"
echo "[INFO] Results root: $RESULTS_ROOT"
echo "[INFO] VEP executable: $VEP_EXEC"
echo

echo "[STEP] Change into repo root"
cd "$REPO_ROOT"
echo "[INFO] Current working directory: $(pwd)"
echo

echo "[STEP] Activate .venv"
if [[ ! -f ".venv/bin/activate" ]]; then
  echo "[ERROR] Missing .venv activate script at: $REPO_ROOT/.venv/bin/activate"
  exit 1
fi
# shellcheck disable=SC1091
source .venv/bin/activate
echo "[INFO] Venv activated."
echo

echo "=== PYTHON / REPO CONTEXT ==="
echo "[CMD] which python"
which python || true
echo

echo "[CMD] python --version"
python --version || true
echo

echo "[CMD] git status --short"
git status --short || true
echo

echo "=== FIND LATEST NORMALIZED VCF ==="
LATEST_VCF="$(find "$RESULTS_ROOT" -type f -name "*.normalized_variants.vcf" | sort | tail -n 1 || true)"
if [[ -z "${LATEST_VCF:-}" ]]; then
  echo "[ERROR] No normalized VCF found under $RESULTS_ROOT"
  exit 1
fi
echo "[INFO] LATEST_VCF=$LATEST_VCF"
echo

echo "[CMD] ls -lah $LATEST_VCF"
ls -lah "$LATEST_VCF"
echo

echo "[CMD] head -n 20 $LATEST_VCF"
head -n 20 "$LATEST_VCF" || true
echo

echo "=== VEP BASIC CHECKS ==="
echo "[CMD] $VEP_EXEC --help | head -n 20"
"$VEP_EXEC" --help | head -n 20 || true
echo

echo "[CMD] $VEP_EXEC --help | grep -i offline | head"
"$VEP_EXEC" --help | grep -i offline | head || true
echo

echo "=== FIND POSSIBLE HUMAN CACHE LOCATIONS ==="
echo "[CMD] find /root/.vep /data/storage/reference/vep -maxdepth 4 -type d 2>/dev/null | grep -E 'homo_sapiens|GRCh38|115'"
find /root/.vep /data/storage/reference/vep -maxdepth 4 -type d 2>/dev/null | grep -E 'homo_sapiens|GRCh38|115' || true
echo

echo "=== PREPARE SMOKETEST OUTPUT PATHS ==="
TMP_DIR="$REPO_ROOT/results/bootstrap_logs/stage07_smoketest_${TS}"
mkdir -p "$TMP_DIR"
SMOKE_VCF="$TMP_DIR/smoke_input.vcf"
SMOKE_OUT="$TMP_DIR/vep_smoke_output.txt"

echo "[INFO] TMP_DIR=$TMP_DIR"
echo "[INFO] SMOKE_VCF=$SMOKE_VCF"
echo "[INFO] SMOKE_OUT=$SMOKE_OUT"
echo

echo "=== BUILD MINIMAL INPUT VCF ==="
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
echo "[CMD] cat $SMOKE_VCF"
cat "$SMOKE_VCF"
echo

echo "=== DIRECT VEP SMOKETEST (NO CACHE YET) ==="
echo "[CMD] $VEP_EXEC --input_file $SMOKE_VCF --output_file $SMOKE_OUT --format vcf --vcf --force_overwrite --offline"
"$VEP_EXEC" \
  --input_file "$SMOKE_VCF" \
  --output_file "$SMOKE_OUT" \
  --format vcf \
  --vcf \
  --force_overwrite \
  --offline || true
echo

echo "=== CHECK VEP OUTPUT / ERROR STATE ==="
echo "[CMD] ls -lah $TMP_DIR"
ls -lah "$TMP_DIR" || true
echo

if [[ -f "$SMOKE_OUT" ]]; then
  echo "[CMD] head -n 40 $SMOKE_OUT"
  head -n 40 "$SMOKE_OUT" || true
else
  echo "[WARN] VEP output file not created."
fi
echo

echo "[INFO] Mark Stage 07 VEP smoke test completed at $(date)"
echo "[INFO] Log file saved to: $LOG"