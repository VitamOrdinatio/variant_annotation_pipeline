#!/usr/bin/env bash
set -euo pipefail

TS="$(date +%Y%m%d_%H%M%S)"
LOG="/root/Desktop/mark_download_vep_archive_${TS}.log"
REPO_ROOT="$HOME/dev/portfolio_projects/variant_annotation_pipeline"

VEP_VERSION="115.0"
VEP_ARCHIVE_NAME="ensembl-vep-release-${VEP_VERSION}.tar.gz"
VEP_URL="https://github.com/Ensembl/ensembl-vep/archive/refs/tags/release/${VEP_VERSION}.tar.gz"
VEP_ARCHIVE_PATH="/root/Desktop/${VEP_ARCHIVE_NAME}"

exec > >(tee "$LOG") 2>&1

echo "[INFO] Mark VEP download helper started at $(date)"
echo "[INFO] Log file: $LOG"
echo "[INFO] VEP_URL: $VEP_URL"
echo "[INFO] Target archive path: $VEP_ARCHIVE_PATH"
echo

cd "$REPO_ROOT"
source .venv/bin/activate

echo "=== CLEANUP OLD FILE IF PRESENT ==="
rm -f "$VEP_ARCHIVE_PATH"
echo

echo "=== DOWNLOAD (STRICT MODE) ==="
echo "[CMD] curl -fL -o $VEP_ARCHIVE_PATH $VEP_URL"
curl -fL -o "$VEP_ARCHIVE_PATH" "$VEP_URL"
echo

echo "=== VERIFY SIZE ==="
ls -lah "$VEP_ARCHIVE_PATH"
echo

FILE_SIZE=$(stat -c%s "$VEP_ARCHIVE_PATH")
echo "[INFO] FILE_SIZE_BYTES=$FILE_SIZE"

if [[ "$FILE_SIZE" -lt 1000000 ]]; then
  echo "[ERROR] Downloaded file is too small (<1MB). Likely failed download."
  exit 1
fi
echo

echo "=== VERIFY ARCHIVE CONTENT ==="
tar -tzf "$VEP_ARCHIVE_PATH" | head
echo

echo "[INFO] VEP archive download and validation successful"
echo "[INFO] Archive ready at: $VEP_ARCHIVE_PATH"
echo "[INFO] Log file saved to: $LOG"