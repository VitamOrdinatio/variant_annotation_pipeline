#!/usr/bin/env bash
set -euo pipefail

# setup_grch38_reference.sh
#
# Purpose:
#   Download and prepare the GRCh38 primary assembly reference genome
#   for variant_annotation_pipeline repo2 v1.0.
#
# What it does:
#   1. Creates the expected reference directories
#   2. Downloads the Ensembl human GRCh38 primary assembly FASTA
#   3. Renames the FASTA to match repo2 config expectations
#   4. Builds:
#        - samtools .fai
#        - GATK sequence dictionary
#        - BWA index files
#
# Canonical output layout:
#   <REF_BASE_DIR>/
#     GRCh38.primary_assembly.genome.fa
#     GRCh38.primary_assembly.genome.fa.fai
#     GRCh38.primary_assembly.genome.dict
#     bwa/
#       GRCh38.primary_assembly.genome.{amb,ann,bwt,pac,sa}
#
# Portability model:
#   - default path is Sys76-oriented
#   - override via environment variable on Mark or other nodes
#
# Usage:
#   bash scripts/setup_grch38_reference.sh
#
# Override example:
#   REF_BASE_DIR=/data/storage/reference/grch38 bash scripts/setup_grch38_reference.sh
#
# Force rebuild example:
#   FORCE_REFERENCE_REBUILD=1 REF_BASE_DIR=/data/storage/reference/grch38 bash scripts/setup_grch38_reference.sh
#
# Optional FASTA URL override:
#   REF_FASTA_URL=https://ftp.ensembl.org/pub/release-110/fasta/homo_sapiens/dna/Homo_sapiens.GRCh38.dna.primary_assembly.fa.gz \
#   REF_BASE_DIR=/data/storage/reference/grch38 \
#   bash scripts/setup_grch38_reference.sh

REF_BASE_DIR="${REF_BASE_DIR:-/mnt/storage/reference/grch38}"
REF_FASTA_URL="${REF_FASTA_URL:-https://ftp.ensembl.org/pub/release-110/fasta/homo_sapiens/dna/Homo_sapiens.GRCh38.dna.primary_assembly.fa.gz}"
FORCE_REFERENCE_REBUILD="${FORCE_REFERENCE_REBUILD:-0}"

BWA_DIR="${REF_BASE_DIR}/bwa"

DOWNLOADED_FASTA_GZ="${REF_BASE_DIR}/Homo_sapiens.GRCh38.dna.primary_assembly.fa.gz"
DOWNLOADED_FASTA="${REF_BASE_DIR}/Homo_sapiens.GRCh38.dna.primary_assembly.fa"
FINAL_FASTA="${REF_BASE_DIR}/GRCh38.primary_assembly.genome.fa"
FINAL_FAI="${FINAL_FASTA}.fai"
FINAL_DICT="${REF_BASE_DIR}/GRCh38.primary_assembly.genome.dict"
BWA_PREFIX="${BWA_DIR}/GRCh38.primary_assembly.genome"

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

remove_if_force() {
  local path="$1"
  if [[ "${FORCE_REFERENCE_REBUILD}" == "1" && -e "${path}" ]]; then
    warn "FORCE_REFERENCE_REBUILD=1 set; removing ${path}"
    rm -rf "${path}"
  fi
}

download_to_tmp_then_move() {
  local url="$1"
  local dest="$2"
  local tmp="${dest}.tmp"

  rm -f "${tmp}"

  log "Downloading: ${url}"
  if ! wget -O "${tmp}" "${url}"; then
    rm -f "${tmp}"
    err "Download failed: ${url}"
    exit 1
  fi

  if [[ ! -s "${tmp}" ]]; then
    rm -f "${tmp}"
    err "Downloaded file is empty: ${url}"
    exit 1
  fi

  mv -f "${tmp}" "${dest}"
  log "Download complete: ${dest}"
}

log "REF_BASE_DIR=${REF_BASE_DIR}"
log "REF_FASTA_URL=${REF_FASTA_URL}"
log "FORCE_REFERENCE_REBUILD=${FORCE_REFERENCE_REBUILD}"

log "Preparing reference directories..."
mkdir -p "${REF_BASE_DIR}"
mkdir -p "${BWA_DIR}"

log "Checking required tools..."
for tool in wget gunzip samtools bwa gatk ls; do
  require_tool "${tool}"
done

if [[ "${FORCE_REFERENCE_REBUILD}" == "1" ]]; then
  remove_if_force "${FINAL_FASTA}"
  remove_if_force "${FINAL_FAI}"
  remove_if_force "${FINAL_DICT}"
  remove_if_force "${DOWNLOADED_FASTA}"
  remove_if_force "${DOWNLOADED_FASTA_GZ}"
  remove_if_force "${BWA_PREFIX}.amb"
  remove_if_force "${BWA_PREFIX}.ann"
  remove_if_force "${BWA_PREFIX}.bwt"
  remove_if_force "${BWA_PREFIX}.pac"
  remove_if_force "${BWA_PREFIX}.sa"
fi

log "Reference base directory: ${REF_BASE_DIR}"
log "BWA index directory: ${BWA_DIR}"

if [[ -f "${FINAL_FASTA}" ]]; then
  log "Final FASTA already exists: ${FINAL_FASTA}"
else
  if [[ -f "${DOWNLOADED_FASTA}" ]]; then
    log "Downloaded FASTA already present: ${DOWNLOADED_FASTA}"
  else
    if [[ -f "${DOWNLOADED_FASTA_GZ}" ]]; then
      log "FASTA archive already present: ${DOWNLOADED_FASTA_GZ}"
    else
      download_to_tmp_then_move "${REF_FASTA_URL}" "${DOWNLOADED_FASTA_GZ}"
    fi

    log "Decompressing FASTA..."
    gunzip -f "${DOWNLOADED_FASTA_GZ}"
  fi

  log "Renaming FASTA to repo2 expected filename..."
  mv -f "${DOWNLOADED_FASTA}" "${FINAL_FASTA}"
fi

log "Building FASTA index (.fai)..."
if [[ -f "${FINAL_FAI}" ]]; then
  log "FASTA index already exists: ${FINAL_FAI}"
else
  samtools faidx "${FINAL_FASTA}"
fi

log "Building GATK sequence dictionary (.dict)..."
if [[ -f "${FINAL_DICT}" ]]; then
  log "Sequence dictionary already exists: ${FINAL_DICT}"
else
  gatk CreateSequenceDictionary \
    -R "${FINAL_FASTA}" \
    -O "${FINAL_DICT}"
fi

log "Building BWA index..."
if [[ -f "${BWA_PREFIX}.amb" && -f "${BWA_PREFIX}.ann" && -f "${BWA_PREFIX}.bwt" && -f "${BWA_PREFIX}.pac" && -f "${BWA_PREFIX}.sa" ]]; then
  log "BWA index files already exist under prefix: ${BWA_PREFIX}"
else
  bwa index -p "${BWA_PREFIX}" "${FINAL_FASTA}"
fi

log "Final reference bundle:"
ls -lh "${REF_BASE_DIR}" || true
echo
log "Final BWA index bundle:"
ls -lh "${BWA_DIR}" || true
echo
log "Reference setup complete."
log "Repo2 config should now resolve to:"
echo "  reference.fasta_path=${FINAL_FASTA}"
echo "  reference.fasta_index=${FINAL_FAI}"
echo "  reference.sequence_dictionary=${FINAL_DICT}"
echo "  reference.bwa_index_prefix=${BWA_PREFIX}"