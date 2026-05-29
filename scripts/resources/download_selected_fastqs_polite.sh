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


REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
MANIFEST="${1:-${REPO_ROOT}/data/reference/sra_support/PRJEB57558_runs_topology.tsv}"
OUTDIR="${OUTDIR:-/data/storage/fastq}"
LIMIT_RATE="${LIMIT_RATE:-20m}"
TIMESTAMP="$(date +%Y_%m_%d_%H%M%S)"
LOGFILE="${OUTDIR}/download_session_${TIMESTAMP}.log"
FAILED_LOG="${OUTDIR}/download_failures_${TIMESTAMP}.log"
INTEGRITY_LOG="${OUTDIR}/gzip_integrity_${TIMESTAMP}.log"
EXTRACTED_MANIFEST=""

mkdir -p "${OUTDIR}"
exec > >(tee -a "${LOGFILE}") 2>&1

cleanup() {
  [[ -n "${EXTRACTED_MANIFEST}" && -f "${EXTRACTED_MANIFEST}" ]] && rm -f "${EXTRACTED_MANIFEST}"
}
trap cleanup EXIT

if [[ "${ALLOW_NON_MARK:-0}" != "1" && ! "$(hostname -s)" =~ [Mm][Aa][Rr][Kk] ]]; then
  echo "ERROR: This script is intended for MARK. Set ALLOW_NON_MARK=1 only for dry testing."
  exit 1
fi

for cmd in awk wget gunzip tee date hostname basename; do
  command -v "$cmd" >/dev/null 2>&1 || { echo "ERROR: Missing command: $cmd"; exit 1; }
done

[[ -f "${MANIFEST}" ]] || { echo "ERROR: Manifest not found: ${MANIFEST}"; exit 1; }

EXTRACTED_MANIFEST="$(mktemp)"
awk -F'\t' '
  BEGIN { OFS="\t" }
  NR==1 {
    for (i=1;i<=NF;i++) {
      gsub(/\r$/,"",$i)
      idx[$i]=i
    }
    required[1]="run_accession"
    required[2]="library_layout"
    required[3]="fastq_ftp"
    for (r=1;r<=3;r++) {
      if (!(required[r] in idx)) {
        print "ERROR: Required column missing: " required[r] > "/dev/stderr"
        exit 2
      }
    }
    print "run_accession","library_layout","fastq_ftp"
    next
  }
  {
    run=$(idx["run_accession"])
    layout=$(idx["library_layout"])
    ftp=$(idx["fastq_ftp"])
    gsub(/\r$/,"",run)
    gsub(/\r$/,"",layout)
    gsub(/\r$/,"",ftp)
    if (run=="run_accession") next
    if (run!="" && ftp!="") print run,layout,ftp
  }
' "${MANIFEST}" > "${EXTRACTED_MANIFEST}"

declare -a DOWNLOADED_FILES=()

echo "Manifest: ${MANIFEST}"
echo "Extracted operational manifest: ${EXTRACTED_MANIFEST}"
echo "Output directory: ${OUTDIR}"
echo "Download policy: nice -n 19 ionice -c2 -n7 wget -c --limit-rate=${LIMIT_RATE}"
echo

while IFS=$'\t' read -r run_accession library_layout fastq_ftp; do
  [[ "${run_accession}" == "run_accession" ]] && continue
  [[ -z "${run_accession:-}" || -z "${fastq_ftp:-}" ]] && continue

  if [[ "${library_layout}" != "PAIRED" ]]; then
    echo "WARNING: ${run_accession} is not marked as PAIRED; layout=${library_layout}"
  fi

  IFS=';' read -ra URLS <<< "${fastq_ftp}"
  for url in "${URLS[@]}"; do
    url="$(echo "${url}" | tr -d '\r')"
    [[ -z "${url}" ]] && continue

    if [[ "${url}" != ftp://* && "${url}" != http://* && "${url}" != https://* ]]; then
      url="ftp://${url}"
    fi

    filename="$(basename "${url}")"
    destination="${OUTDIR}/${filename}"

    if [[ -f "${destination}" ]]; then
      if gunzip -t "${destination}" >/dev/null 2>&1; then
        echo "SKIP: ${filename} already exists and passed gzip integrity check"
        continue
      else
        echo "ERROR: ${filename} exists but failed gzip integrity check."
        echo "Manual operator review required; not overwriting trusted substrate path."
        echo -e "FAILED_EXISTING_GZIP\t${run_accession}\t${filename}" >> "${FAILED_LOG}"
        continue
      fi
    fi

    echo "DOWNLOAD: ${run_accession} -> ${filename}"
    if nice -n 19 ionice -c2 -n7 wget -c --limit-rate="${LIMIT_RATE}" "${url}" -P "${OUTDIR}"; then
      echo "SUCCESS: ${filename}"
      DOWNLOADED_FILES+=("${destination}")
    else
      echo "FAILED: ${filename}" | tee -a "${FAILED_LOG}"
      continue
    fi
    echo
  done

  echo "----------------------------------------"
  echo "Completed processing for ${run_accession}. Total downloaded files this session: ${#DOWNLOADED_FILES[@]}"
  echo
done < "${EXTRACTED_MANIFEST}"

echo
echo "Running gzip integrity checks for newly downloaded files..."
for file in "${DOWNLOADED_FILES[@]}"; do
  echo "CHECK: ${file}"
  if gunzip -t "${file}" >/dev/null 2>&1; then
    echo "PASS: ${file}" | tee -a "${INTEGRITY_LOG}"
  else
    echo "FAIL: ${file}" | tee -a "${INTEGRITY_LOG}"
  fi
done

echo
echo "Download pass complete."
echo "Main log: ${LOGFILE}"
echo "Failure log: ${FAILED_LOG}"
echo "Integrity log: ${INTEGRITY_LOG}"
