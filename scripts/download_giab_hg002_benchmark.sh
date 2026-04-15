#!/usr/bin/env bash
# download_giab_hg002_benchmark.sh
#
# Purpose:
#   Download the GIAB HG002 benchmark files used to validate
#   repo2 (variant_annotation_pipeline) v1 against a trusted truth set.
#
# Why these files matter:
#   1) benchmark.vcf.gz
#      - This is the GIAB high-confidence small-variant truth set for HG002 on GRCh38.
#      - You compare your pipeline-generated VCF against this file.
#
#   2) benchmark.vcf.gz.tbi
#      - Tabix index for the benchmark VCF.
#      - Required by many tools (bcftools, tabix, IGV, etc.) for efficient access.
#
#   3) benchmark.bed
#      - High-confidence regions BED file.
#      - You should benchmark ONLY inside these trusted regions.
#      - This prevents unfairly penalizing your pipeline in regions that GIAB does not
#        consider benchmarkable.
#
# Usage:
#   chmod +x download_giab_hg002_benchmark.sh
#   ./download_giab_hg002_benchmark.sh
#
# Notes:
#   - Locked sample for repo2 v1:
#       BioProject: PRJNA200694
#       Sample: HG002 (NA24385)
#       SRA run: SRR12898354
#       Reference genome: GRCh38

set -euo pipefail

############################
# Destination directories  #
############################

GIAB_DIR="/mnt/storage/reference/giab"

############################
# File URLs                #
############################

# High-confidence HG002 truth VCF on GRCh38
VCF_URL="https://ftp-trace.ncbi.nlm.nih.gov/giab/ftp/release/AshkenazimTrio/HG002_NA24385_son/latest/GRCh38/HG002_GRCh38_1_22_v4.2.1_benchmark.vcf.gz"

# Tabix index for the truth VCF
TBI_URL="https://ftp-trace.ncbi.nlm.nih.gov/giab/ftp/release/AshkenazimTrio/HG002_NA24385_son/latest/GRCh38/HG002_GRCh38_1_22_v4.2.1_benchmark.vcf.gz.tbi"

# High-confidence benchmark regions for HG002 on GRCh38
BED_URL="https://ftp-trace.ncbi.nlm.nih.gov/giab/ftp/release/AshkenazimTrio/HG002_NA24385_son/latest/GRCh38/HG002_GRCh38_1_22_v4.2.1_benchmark.bed"

############################
# Create destination       #
############################

echo "Creating destination directory..."
mkdir -p "${GIAB_DIR}"

############################
# Download files           #
############################

echo
echo "Downloading HG002 benchmark VCF..."
wget -O "${GIAB_DIR}/HG002_GRCh38_1_22_v4.2.1_benchmark.vcf.gz" "${VCF_URL}"

echo
echo "Downloading HG002 benchmark VCF index..."
wget -O "${GIAB_DIR}/HG002_GRCh38_1_22_v4.2.1_benchmark.vcf.gz.tbi" "${TBI_URL}"

echo
echo "Downloading HG002 benchmark BED..."
wget -O "${GIAB_DIR}/HG002_GRCh38_1_22_v4.2.1_benchmark.bed" "${BED_URL}"

############################
# Sanity checks            #
############################

echo
echo "Downloaded files:"
ls -lh "${GIAB_DIR}"

echo
echo "Quick sanity check on VCF header:"
zcat "${GIAB_DIR}/HG002_GRCh38_1_22_v4.2.1_benchmark.vcf.gz" | head -n 20 || true

echo
echo "Quick sanity check on BED:"
head -n 10 "${GIAB_DIR}/HG002_GRCh38_1_22_v4.2.1_benchmark.bed" || true

############################
# Final notes              #
############################

echo
echo "Done."
echo
echo "Files are now located in:"
echo "  ${GIAB_DIR}"
echo
echo "Validation reminder:"
echo "  Compare your pipeline VCF to the benchmark VCF"
echo "  only within the benchmark BED regions."
echo
echo "Typical future validation tools:"
echo "  bcftools isec"
echo "  bcftools view -R <benchmark.bed>"
echo "  tabix"