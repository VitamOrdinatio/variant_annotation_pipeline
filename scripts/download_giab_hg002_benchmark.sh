#!/usr/bin/env bash
set -euo pipefail

# download_giab_hg002_benchmark.sh
#
# Purpose:
#   Download the GIAB HG002 benchmark files used to validate
#   repo2 (variant_annotation_pipeline) v1 against a trusted truth set.
#
# Why these files matter:
#   1) benchmark.vcf.gz
#      - GIAB high-confidence small-variant truth set for HG002 on GRCh38
#   2) benchmark.vcf.gz.tbi
#      - tabix index for the benchmark VCF
#   3) benchmark.bed
#      - GIAB high-confidence benchmark regions
#
# Locked sample for repo2 v1:
#   BioProject: PRJNA200694
#   Sample: HG002 (NA24385)
#   SRA run: SRR12898354
#   Reference genome: GRCh38
#
# Portability model:
#   - default path is Sys76-oriented
#   - override via environment variable on other machines
#
# Usage:
#   bash scripts/download_giab_hg002_benchmark.sh
#
# Default GIAB_DIR on sys76 is /mnt/storage/reference/giab
# But you can override it by setting the GIAB_DIR environment variable when running the script. For example: 
#
# Override example:
#   GIAB_DIR=/data/storage/reference/giab bash scripts/download_giab_hg002_benchmark.sh
#
# Force redownload example:
#   FORCE_DOWNLOAD=1 GIAB_DIR=/data/storage/reference/giab bash scripts/download_giab_hg002_benchmark.sh

GIAB_DIR="${GIAB_DIR:-/mnt/storage/reference/giab}"
FORCE_DOWNLOAD="${FORCE_DOWNLOAD:-0}"

VCF_BASENAME="HG002_GRCh38_1_22_v4.2.1_benchmark.vcf.gz"
TBI_BASENAME="HG002_GRCh38_1_22_v4.2.1_benchmark.vcf.gz.tbi"
BED_BASENAME="HG002_GRCh38_1_22_v4.2.1_benchmark.bed"

VCF_URL="https://ftp-trace.ncbi.nlm.nih.gov/giab/ftp/release/AshkenazimTrio/HG002_NA24385_son/latest/GRCh38/${VCF_BASENAME}"
TBI_URL="https://ftp-trace.ncbi.nlm.nih.gov/giab/ftp/release/AshkenazimTrio/HG002_NA24385_son/latest/GRCh38/${TBI_BASENAME}"
BED_URL="https://ftp-trace.ncbi.nlm.nih.gov/giab/ftp/release/AshkenazimTrio/HG002_NA24385_son/latest/GRCh38/${BED_BASENAME}"

VCF_PATH="${GIAB_DIR}/${VCF_BASENAME}"
TBI_PATH="${GIAB_DIR}/${TBI_BASENAME}"
BED_PATH="${GIAB_DIR}/${BED_BASENAME}"

log() {
  echo "[INFO] $*"
}

warn() {
  echo "[WARN] $*" >&2
}

err() {
  echo "[ERROR] $*" >&2
}

require_tool() {
  local tool="$1"
  if ! command -v "${tool}" >/dev/null 2>&1; then
    err "Required tool not found in PATH: ${tool}"
    exit 1
  fi
}

download_if_needed() {
  local url="$1"
  local dest="$2"

  if [[ -f "${dest}" && "${FORCE_DOWNLOAD}" != "1" ]]; then
    log "Already present, skipping download: ${dest}"
    return 0
  fi

  if [[ -f "${dest}" && "${FORCE_DOWNLOAD}" == "1" ]]; then
    warn "FORCE_DOWNLOAD=1 set; re-downloading ${dest}"
  fi

  log "Downloading: ${url}"
  wget -O "${dest}" "${url}"
}

log "Checking required tools..."
require_tool wget
require_tool zcat
require_tool head
require_tool ls

log "Creating destination directory..."
mkdir -p "${GIAB_DIR}"

log "GIAB destination directory: ${GIAB_DIR}"
log "FORCE_DOWNLOAD=${FORCE_DOWNLOAD}"

download_if_needed "${VCF_URL}" "${VCF_PATH}"
download_if_needed "${TBI_URL}" "${TBI_PATH}"
download_if_needed "${BED_URL}" "${BED_PATH}"

log "Downloaded files:"
ls -lh "${GIAB_DIR}"

log "Quick sanity check on VCF header:"
zcat "${VCF_PATH}" | head -n 20 || true

log "Quick sanity check on BED:"
head -n 10 "${BED_PATH}" || true

log "Done."
log "Files are now located in: ${GIAB_DIR}"
log "Validation reminder:"
log "  Compare your pipeline VCF to the benchmark VCF only within the benchmark BED regions."
log "Typical future validation tools:"
log "  bcftools isec"
log "  bcftools view -R <benchmark.bed>"
log "  tabix"