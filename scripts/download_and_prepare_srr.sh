#!/usr/bin/env bash
# download_and_prepare_srr.sh
#
# Purpose:
#   1) Download an SRA accession into /mnt/storage/sra
#   2) Convert it into paired FASTQ files in /mnt/storage/fastq
#   3) Compress FASTQ files with pigz
#   4) Remove temporary files
#   5) Optionally remove the original .sra file
#   6) Perform a simple FASTQ sanity check
#
# Usage:
#   ./download_and_prepare_srr.sh
#
# Before first use:
#   chmod +x download_and_prepare_srr.sh
#
# Notes:
#   - Edit ACCESSION below for each new SRA run.
#   - This script assumes:
#       prefetch
#       fasterq-dump
#       pigz
#     are already installed and available in PATH.

set -euo pipefail

############################
# User-configurable values #
############################

ACCESSION="SRR12898354"
MAX_SIZE="100G"
THREADS="8"

# Storage locations
SRA_ROOT="/mnt/storage/sra"
FASTQ_ROOT="/mnt/storage/fastq"
TMP_ROOT="/mnt/storage/tmp"

# Set to "yes" if you want to delete the .sra after successful FASTQ generation
REMOVE_SRA_AFTER_SUCCESS="no"

#####################
# Derived variables #
#####################

SRA_DIR="${SRA_ROOT}/${ACCESSION}"
SRA_FILE="${SRA_DIR}/${ACCESSION}.sra"
FASTQ_R1="${FASTQ_ROOT}/${ACCESSION}_1.fastq"
FASTQ_R2="${FASTQ_ROOT}/${ACCESSION}_2.fastq"
FASTQ_R1_GZ="${FASTQ_R1}.gz"
FASTQ_R2_GZ="${FASTQ_R2}.gz"

####################
# Helper functions #
####################

echo_header() {
  echo
  echo "============================================================"
  echo "$1"
  echo "============================================================"
}

require_cmd() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "ERROR: Required command not found: $1"
    exit 1
  fi
}

########################
# Dependency checking  #
########################

echo_header "Checking required commands"
require_cmd prefetch
require_cmd fasterq-dump
require_cmd pigz

########################
# Create directories   #
########################

echo_header "Creating storage directories"
mkdir -p "${SRA_ROOT}"
mkdir -p "${FASTQ_ROOT}"
mkdir -p "${TMP_ROOT}"

########################
# Download SRA         #
########################

echo_header "Downloading SRA accession: ${ACCESSION}"

# Important:
# prefetch writes to the configured SRA repository.
# We use --output-directory to direct it to /mnt/storage/sra.
prefetch "${ACCESSION}" --max-size "${MAX_SIZE}" --output-directory "${SRA_ROOT}"

if [[ ! -f "${SRA_FILE}" ]]; then
  echo "ERROR: Expected SRA file not found at: ${SRA_FILE}"
  echo "Please inspect ${SRA_ROOT} manually."
  exit 1
fi

echo "SRA download complete:"
ls -lh "${SRA_FILE}"

########################
# Convert to FASTQ     #
########################

echo_header "Converting SRA to paired FASTQ"

# fasterq-dump takes the accession directory as input in newer SRA toolkit layouts.
fasterq-dump "${SRA_DIR}" \
  --split-files \
  --threads "${THREADS}" \
  --temp "${TMP_ROOT}" \
  -O "${FASTQ_ROOT}"

if [[ ! -f "${FASTQ_R1}" || ! -f "${FASTQ_R2}" ]]; then
  echo "ERROR: FASTQ conversion did not produce expected files:"
  echo "  ${FASTQ_R1}"
  echo "  ${FASTQ_R2}"
  exit 1
fi

echo "FASTQ conversion complete:"
ls -lh "${FASTQ_R1}" "${FASTQ_R2}"

########################
# Compress FASTQ       #
########################

echo_header "Compressing FASTQ files with pigz"
pigz -f "${FASTQ_R1}"
pigz -f "${FASTQ_R2}"

if [[ ! -f "${FASTQ_R1_GZ}" || ! -f "${FASTQ_R2_GZ}" ]]; then
  echo "ERROR: FASTQ compression did not produce expected files:"
  echo "  ${FASTQ_R1_GZ}"
  echo "  ${FASTQ_R2_GZ}"
  exit 1
fi

echo "Compressed FASTQ files:"
ls -lh "${FASTQ_R1_GZ}" "${FASTQ_R2_GZ}"

########################
# Remove temp files    #
########################

echo_header "Removing temporary files"
rm -rf "${TMP_ROOT:?}/"*
echo "Temporary directory cleaned: ${TMP_ROOT}"

########################
# Optional SRA removal #
########################

if [[ "${REMOVE_SRA_AFTER_SUCCESS}" == "yes" ]]; then
  echo_header "Removing original SRA file"
  rm -f "${SRA_FILE}"
  echo "Removed: ${SRA_FILE}"
else
  echo_header "Keeping original SRA file"
  echo "SRA retained at: ${SRA_FILE}"
fi

########################
# Sanity check FASTQ   #
########################

echo_header "FASTQ sanity check"

echo "Showing first 8 lines of R1:"
zcat "${FASTQ_R1_GZ}" | head -n 8 || true

echo
echo "Showing first 8 lines of R2:"
zcat "${FASTQ_R2_GZ}" | head -n 8 || true

########################
# Final summary        #
########################

echo_header "Done"

echo "Accession: ${ACCESSION}"
echo "SRA path: ${SRA_FILE}"
echo "FASTQ R1: ${FASTQ_R1_GZ}"
echo "FASTQ R2: ${FASTQ_R2_GZ}"

echo
echo "To make this script executable, run:"
echo "  chmod +x download_and_prepare_srr.sh"

echo
echo "Then run it with:"
echo "  ./download_and_prepare_srr.sh"