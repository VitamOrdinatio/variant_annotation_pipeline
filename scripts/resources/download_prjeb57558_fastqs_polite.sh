#!/usr/bin/env bash
set -uo pipefail

# Existing validated FASTQs are treated as immutable trusted substrate.
#
# If an existing file fails gzip integrity testing, the script will NOT
# automatically overwrite or replace it. Manual operator review is required.
#
# LOG files are written to the output directory with a timestamped filename
# to avoid overwriting previous logs. The main log captures all output, 
# while separate logs track download failures and gzip integrity for review.
#
# This script assumes the manifest (TSV) file is well-formed and includes 
# the expected columns. It processes each row, handling multiple URLs if
# present, and applies a polite download policy using nice and ionice to
# minimize system impact. The script also includes robust error handling and
# logging to help troubleshooting and ensure transparency of the download process.
#
# This script should be located as scripts/resources/download_prjeb57558_fastqs_polite.sh.
# The manifest TSV file should be located as data/reference/sra_support/prjeb57558_nine_runs.tsv.
#
# For ease of use, the output directory is specified as a variable for
# flexibility. The script checks for the existence of the manifest file before
# proceeding and logs all key actions and decisions for traceability.
#
#
# Script Usage:
#
# 1. The OUTDIR folder path of /data/storage/fastq is also the read location for substrate FASTQs in the VAP pipeline.
# 2. Ensure you have the necessary permissions to write to the output directory and that wget is installed on your system.
# 3. Start a tmux session to run the script so that it can continue running in the background and you can monitor logs without interruption.
# 4. Within tmux, run the script from the VAP repo root: ./scripts/resources/download_prjeb57558_fastqs_polite.sh
# 5. Monitor the logs written to OUTDIR folder for progress and any potential issues with downloads or file integrity.



# Set up manifest and output directory variables
MANIFEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MANIFEST="data/reference/sra_support/prjeb57558_nine_runs.tsv"
OUTDIR="/data/storage/fastq"
LIMIT_RATE="20m"

# Create output directory if it doesn't exist
mkdir -p "${OUTDIR}"

# Set up global logging variables
TIMESTAMP="$(date +%Y_%m_%d_%H%M%S)"
LOGFILE="${OUTDIR}/download_session_${TIMESTAMP}.log"
FAILED_LOG="${OUTDIR}/download_failures_${TIMESTAMP}.log"
CHECKSUM_LOG="${OUTDIR}/gzip_integrity_${TIMESTAMP}.log"

# Redirect stdout/stderr to both console and logfile
exec > >(tee -a "${LOGFILE}") 2>&1

# Initialize session-local downloaded file tracking
declare -a DOWNLOADED_FILES=()

# Redirect all output to the main log file
if [[ ! -f "${MANIFEST}" ]]; then
  echo "ERROR: Manifest not found: ${MANIFEST}" >&2
  exit 1
fi

# Log session start and parameters
echo "Manifest: ${MANIFEST}"
echo "Output directory: ${OUTDIR}"
echo "Download policy: nice -n 19 ionice -c2 -n7 wget -c --limit-rate=${LIMIT_RATE}"
echo

# Process the manifest file, skipping the header and handling potential carriage returns
while IFS=$'\t' read -r run_accession sample_accession experiment_accession study_accession library_strategy library_layout library_source library_selection instrument_model read_count rank_pct base_count fastq_bytes fastq_ftp
do
  # Validate that the essential fields (run_accession and fastq_ftp) are present before proceeding
  if [[ -z "${run_accession:-}" || -z "${fastq_ftp:-}" ]]; then
    echo "WARNING: Skipping malformed/empty row."
    continue
  fi

  # Handle multiple URLs separated by semicolons and remove any carriage returns
  IFS=';' read -ra URLS <<< "${fastq_ftp}"

  # Process each URL for the current run accession
  for url in "${URLS[@]}"; do
    url="$(echo "${url}" | tr -d '\r')"
    [[ -z "${url}" ]] && continue

    # Log the current run accession and URL being processed
    if [[ "${library_layout}" != "PAIRED" ]]; then
      echo "WARNING: ${run_accession} is not marked as PAIRED"
    fi

    # Ensure the URL has a proper scheme (ftp://, http://, or https://)
    if [[ "${url}" != ftp://* && "${url}" != http://* && "${url}" != https://* ]]; then
      url="ftp://${url}"
    fi

    # Extract the filename from the URL and determine the destination path
    filename="$(basename "${url}")"
    destination="${OUTDIR}/${filename}"

    # Check if the file already exists before attempting to download
    if [[ -f "${destination}" ]]; then
      if gunzip -t "${destination}" >/dev/null 2>&1; then
        echo "SKIP: ${filename} already exists and passed integrity check"
        continue
      else
        echo "ERROR: ${filename} exists but failed gzip integrity check."
        echo "Manual operator review required."
        echo "FAILED_GZIP_CHECK	${filename}" >> "${FAILED_LOG}"
        continue        
      fi
    fi    

    # Log the download attempt and execute the download command with the specified policy
    echo "DOWNLOAD: ${run_accession} -> ${filename}"
    
    # Use nice and ionice to minimize system impact, and limit the download rate to avoid saturating bandwidth
    if nice -n 19 ionice -c2 -n7 wget -c --limit-rate="${LIMIT_RATE}" "${url}" -P "${OUTDIR}"; then
      echo "SUCCESS: ${filename}"
      DOWNLOADED_FILES+=("${destination}")
    else
      echo "FAILED: ${filename}" | tee -a "${FAILED_LOG}"
      continue
    fi
    echo
  # End of URL processing loop for the current run accession
  done

# End of processing for the current run accession, log a separator for clarity
  echo "----------------------------------------"

# End of manifest processing loop, log a summary of the session so far
  echo "Completed processing for ${run_accession}. Total downloaded files so far: ${#DOWNLOADED_FILES[@]}"
  echo
done < <(tail -n +2 "${MANIFEST}" | tr -d '\r')

# After all downloads are attempted, perform gzip integrity checks on the successfully downloaded files
echo
echo "Running gzip integrity checks..."

# Iterate over the list of downloaded files and check their integrity using gunzip -t
for file in "${DOWNLOADED_FILES[@]}"; do
  echo "CHECK: ${file}"
  # Use gunzip -t to test the integrity of the gzip file. If it passes, log a PASS message; if it fails, log a FAIL message.
  if gunzip -t "${file}"; then
    echo "PASS: ${file}" | tee -a "${CHECKSUM_LOG}"
  else
    echo "FAIL: ${file}" | tee -a "${CHECKSUM_LOG}"
  fi
done

# Final summary of the session, including the location of the main log, failure log, and integrity log
echo
echo "Download pass complete."
echo "Session complete."
echo "Main log: ${LOGFILE}"
echo "Failure log: ${FAILED_LOG}"
echo "Integrity log: ${CHECKSUM_LOG}"