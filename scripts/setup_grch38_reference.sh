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
#   3. Renames the FASTA to match config/config.yaml expectations
#   4. Builds:
#        - samtools .fai
#        - GATK sequence dictionary
#        - BWA index files
#
# Default target layout:
#   /mnt/storage/reference/grch38/
#     GRCh38.primary_assembly.genome.fa
#     GRCh38.primary_assembly.genome.fa.fai
#     GRCh38.primary_assembly.genome.dict
#     bwa/
#       GRCh38.primary_assembly.genome.{amb,ann,bwt,pac,sa}
#
# Usage:
#   bash scripts/setup_grch38_reference.sh
#
# Optional override:
#   REF_BASE_DIR=/some/other/path bash scripts/setup_grch38_reference.sh

REF_BASE_DIR="${REF_BASE_DIR:-/mnt/storage/reference/grch38}"
BWA_DIR="${REF_BASE_DIR}/bwa"

ENSEMBL_FASTA_URL="https://ftp.ensembl.org/pub/release-110/fasta/homo_sapiens/dna/Homo_sapiens.GRCh38.dna.primary_assembly.fa.gz"

DOWNLOADED_FASTA_GZ="${REF_BASE_DIR}/Homo_sapiens.GRCh38.dna.primary_assembly.fa.gz"
DOWNLOADED_FASTA="${REF_BASE_DIR}/Homo_sapiens.GRCh38.dna.primary_assembly.fa"
FINAL_FASTA="${REF_BASE_DIR}/GRCh38.primary_assembly.genome.fa"
FINAL_FAI="${FINAL_FASTA}.fai"
FINAL_DICT="${REF_BASE_DIR}/GRCh38.primary_assembly.genome.dict"
BWA_PREFIX="${BWA_DIR}/GRCh38.primary_assembly.genome"

echo "[INFO] Preparing reference directories..."
mkdir -p "${REF_BASE_DIR}"
mkdir -p "${BWA_DIR}"

echo "[INFO] Checking required tools..."
for tool in wget gunzip samtools bwa gatk; do
  if ! command -v "${tool}" >/dev/null 2>&1; then
    echo "[ERROR] Required tool not found in PATH: ${tool}" >&2
    exit 1
  fi
done

echo "[INFO] Reference base directory: ${REF_BASE_DIR}"
echo "[INFO] BWA index directory: ${BWA_DIR}"

if [[ -f "${FINAL_FASTA}" ]]; then
  echo "[INFO] Final FASTA already exists: ${FINAL_FASTA}"
else
  if [[ -f "${DOWNLOADED_FASTA}" ]]; then
    echo "[INFO] Downloaded FASTA already present: ${DOWNLOADED_FASTA}"
  else
    if [[ -f "${DOWNLOADED_FASTA_GZ}" ]]; then
      echo "[INFO] FASTA archive already present: ${DOWNLOADED_FASTA_GZ}"
    else
      echo "[INFO] Downloading GRCh38 primary assembly from Ensembl..."
      wget -O "${DOWNLOADED_FASTA_GZ}" "${ENSEMBL_FASTA_URL}"
    fi

    echo "[INFO] Decompressing FASTA..."
    gunzip -f "${DOWNLOADED_FASTA_GZ}"
  fi

  echo "[INFO] Renaming FASTA to repo2 expected filename..."
  mv -f "${DOWNLOADED_FASTA}" "${FINAL_FASTA}"
fi

echo "[INFO] Building FASTA index (.fai)..."
if [[ -f "${FINAL_FAI}" ]]; then
  echo "[INFO] FASTA index already exists: ${FINAL_FAI}"
else
  samtools faidx "${FINAL_FASTA}"
fi

echo "[INFO] Building GATK sequence dictionary (.dict)..."
if [[ -f "${FINAL_DICT}" ]]; then
  echo "[INFO] Sequence dictionary already exists: ${FINAL_DICT}"
else
  gatk CreateSequenceDictionary \
    -R "${FINAL_FASTA}" \
    -O "${FINAL_DICT}"
fi

echo "[INFO] Building BWA index..."
if [[ -f "${BWA_PREFIX}.amb" && -f "${BWA_PREFIX}.ann" && -f "${BWA_PREFIX}.bwt" && -f "${BWA_PREFIX}.pac" && -f "${BWA_PREFIX}.sa" ]]; then
  echo "[INFO] BWA index files already exist under prefix: ${BWA_PREFIX}"
else
  bwa index -p "${BWA_PREFIX}" "${FINAL_FASTA}"
fi

echo "[INFO] Final reference bundle:"
ls -lh "${REF_BASE_DIR}" || true
echo
echo "[INFO] Final BWA index bundle:"
ls -lh "${BWA_DIR}" || true
echo
echo "[INFO] Reference setup complete."
echo "[INFO] Repo2 config should now resolve:"
echo "       fasta_path        = ${FINAL_FASTA}"
echo "       fasta_index       = ${FINAL_FAI}"
echo "       sequence_dictionary = ${FINAL_DICT}"
echo "       bwa_index_prefix  = ${BWA_PREFIX}"