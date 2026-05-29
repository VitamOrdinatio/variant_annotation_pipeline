#!/usr/bin/env bash
set -uo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
DEFAULT_MANIFEST="${REPO_ROOT}/data/reference/sra_support/selections/prjeb57558/prjeb57558_selected_9_runs.tsv"
MANIFEST="${1:-${DEFAULT_MANIFEST}}"
OUTDIR="${OUTDIR:-/data/storage/fastq}"
INCOMPLETE_DIR="${OUTDIR}/.incomplete"
LIMIT_RATE="${LIMIT_RATE:-20m}"
TIMESTAMP="$(date +%Y_%m_%d_%H%M%S)"

MARK_HOST_PATTERN="${MARK_HOST_PATTERN:-^vandpymolgpuresearch[0-9]*$}"
HOST_SHORT="$(hostname -s | tr '[:upper:]' '[:lower:]')"

if [[ ! -f "${MANIFEST}" ]]; then
  echo "ERROR: Manifest not found: ${MANIFEST}"
  exit 1
fi

BASENAME="$(basename "${MANIFEST}")"

if [[ "${BASENAME}" =~ _selected_9_runs_[0-9]{4}_[0-9]{2}_[0-9]{2}_[0-9]{6}\.tsv$ ]]; then
  BIOPROJECT_LOWER="${BASENAME%%_selected_9_runs_*}"
elif [[ "${BASENAME}" =~ _selected_9_runs\.tsv$ ]]; then
  BIOPROJECT_LOWER="${BASENAME%%_selected_9_runs.tsv}"
else
  echo "ERROR: Could not infer BioProject from manifest filename: ${BASENAME}"
  echo "Expected filename pattern:"
  echo "  <bioproject_lower>_selected_9_runs.tsv"
  echo "or"
  echo "  <bioproject_lower>_selected_9_runs_YYYY_MM_DD_HHMMSS.tsv"
  exit 1
fi

if [[ -z "${BIOPROJECT_LOWER}" || "${BIOPROJECT_LOWER}" == "${BASENAME}" ]]; then
  echo "ERROR: Could not infer BioProject from manifest filename: ${BASENAME}"
  echo "Expected filename pattern:"
  echo "  <bioproject_lower>_selected_9_runs.tsv"
  echo "or"
  echo "  <bioproject_lower>_selected_9_runs_YYYY_MM_DD_HHMMSS.tsv"
  exit 1
fi

LOGDIR="${REPO_ROOT}/data/reference/sra_support/download_logs/${BIOPROJECT_LOWER}"
LOGFILE="${LOGDIR}/download_session_${TIMESTAMP}.log"
FAILED_LOG="${LOGDIR}/download_failures_${TIMESTAMP}.log"
GZIP_LOG="${LOGDIR}/gzip_integrity_${TIMESTAMP}.log"
MD5_LOG="${LOGDIR}/md5_integrity_${TIMESTAMP}.log"
EXISTING_LOG="${LOGDIR}/existing_fastq_audit_${TIMESTAMP}.log"
EXTRACTED_MANIFEST=""


if [[ "${ALLOW_NON_MARK:-0}" != "1" && ! "${HOST_SHORT}" =~ ${MARK_HOST_PATTERN} ]]; then
  echo "ERROR: This script is intended for MARK-compatible hosts."
  echo "Current host: ${HOST_SHORT}"
  echo "Expected host pattern: ${MARK_HOST_PATTERN}"
  echo "Set ALLOW_NON_MARK=1 only for dry testing."
  exit 1
fi

mkdir -p "${OUTDIR}" "${INCOMPLETE_DIR}" "${LOGDIR}"
exec > >(tee -a "${LOGFILE}") 2>&1

cleanup() {
  [[ -n "${EXTRACTED_MANIFEST}" && -f "${EXTRACTED_MANIFEST}" ]] && rm -f "${EXTRACTED_MANIFEST}"
}
trap cleanup EXIT

for cmd in awk wget gunzip tee date hostname basename mktemp md5sum stat mv; do
  command -v "$cmd" >/dev/null 2>&1 || { echo "ERROR: Missing command: $cmd"; exit 1; }
done

validate_gzip() {
  local file="$1"
  local label="$2"
  local run="$3"
  if gunzip -t "${file}" >/dev/null 2>&1; then
    echo -e "PASS_GZIP\t${label}\t${run}\t${file}" >> "${GZIP_LOG}"
    return 0
  else
    echo -e "FAIL_GZIP\t${label}\t${run}\t${file}" >> "${GZIP_LOG}"
    return 1
  fi
}

validate_md5_if_available() {
  local file="$1"
  local expected_md5="$2"
  local label="$3"
  local run="$4"
  if [[ -z "${expected_md5}" ]]; then
    echo -e "WARNING_NO_MD5\t${label}\t${run}\t${file}" >> "${MD5_LOG}"
    return 0
  fi
  local observed_md5
  observed_md5="$(md5sum "${file}" | awk '{print $1}')"
  if [[ "${observed_md5}" == "${expected_md5}" ]]; then
    echo -e "PASS_MD5\t${label}\t${run}\t${file}\t${observed_md5}" >> "${MD5_LOG}"
    return 0
  else
    echo -e "FAIL_MD5\t${label}\t${run}\t${file}\texpected=${expected_md5}\tobserved=${observed_md5}" >> "${MD5_LOG}"
    return 1
  fi
}

validate_bytes_if_available() {
  local file="$1"
  local expected_bytes="$2"
  local label="$3"
  local run="$4"
  if [[ -z "${expected_bytes}" ]]; then
    echo -e "WARNING_NO_BYTES\t${label}\t${run}\t${file}" >> "${FAILED_LOG}"
    return 0
  fi
  local observed_bytes
  observed_bytes="$(stat -c%s "${file}")"
  if [[ "${observed_bytes}" == "${expected_bytes}" ]]; then
    echo -e "PASS_BYTES\t${label}\t${run}\t${file}\t${observed_bytes}" >> "${FAILED_LOG}"
    return 0
  else
    echo -e "FAIL_BYTES\t${label}\t${run}\t${file}\texpected=${expected_bytes}\tobserved=${observed_bytes}" >> "${FAILED_LOG}"
    return 1
  fi
}

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
    print "run_accession","library_layout","fastq_ftp","fastq_md5","fastq_bytes"
    next
  }
  {
    run=$(idx["run_accession"])
    layout=$(idx["library_layout"])
    ftp=$(idx["fastq_ftp"])
    md5=("fastq_md5" in idx ? $(idx["fastq_md5"]) : "")
    bytes=("fastq_bytes" in idx ? $(idx["fastq_bytes"]) : "")
    gsub(/\r$/,"",run)
    gsub(/\r$/,"",layout)
    gsub(/\r$/,"",ftp)
    gsub(/\r$/,"",md5)
    gsub(/\r$/,"",bytes)
    if (run!="" && ftp!="") print run,layout,ftp,md5,bytes
  }
' "${MANIFEST}" > "${EXTRACTED_MANIFEST}"

echo "BioProject: ${BIOPROJECT_LOWER}"
echo "Manifest: ${MANIFEST}"
echo "Extracted operational manifest: ${EXTRACTED_MANIFEST}"
echo "FASTQ output directory: ${OUTDIR}"
echo "Incomplete download directory: ${INCOMPLETE_DIR}"
echo "Log directory: ${LOGDIR}"
echo "Download policy: nice -n 19 ionice -c2 -n7 wget -c --limit-rate=${LIMIT_RATE} -O <part_file>"
echo "Final FASTQ immutability: existing final FASTQs will be audited but never modified"
echo

while IFS=$'\t' read -r run_accession library_layout fastq_ftp fastq_md5 fastq_bytes; do
  [[ "${run_accession}" == "run_accession" ]] && continue
  [[ -z "${run_accession:-}" || -z "${fastq_ftp:-}" ]] && continue

  if [[ "${library_layout}" != "PAIRED" ]]; then
    echo "WARNING: ${run_accession} is not marked as PAIRED; layout=${library_layout}"
  fi

  IFS=';' read -ra URLS <<< "${fastq_ftp}"
  IFS=';' read -ra MD5S <<< "${fastq_md5:-}"
  IFS=';' read -ra BYTES <<< "${fastq_bytes:-}"

  for idx in "${!URLS[@]}"; do
    url="$(echo "${URLS[$idx]}" | tr -d '\r')"
    [[ -z "${url}" ]] && continue

    expected_md5="${MD5S[$idx]:-}"
    expected_bytes="${BYTES[$idx]:-}"

    if [[ "${url}" != ftp://* && "${url}" != http://* && "${url}" != https://* ]]; then
      url="ftp://${url}"
    fi

    filename="$(basename "${url}")"
    final_file="${OUTDIR}/${filename}"
    part_file="${INCOMPLETE_DIR}/${filename}.part"

    if [[ -f "${final_file}" ]]; then
      echo "EXISTING: ${filename}; auditing without modification"
      existing_ok=1
      validate_gzip "${final_file}" "existing" "${run_accession}" || existing_ok=0
      validate_md5_if_available "${final_file}" "${expected_md5}" "existing" "${run_accession}" || existing_ok=0
      validate_bytes_if_available "${final_file}" "${expected_bytes}" "existing" "${run_accession}" || existing_ok=0

      if [[ "${existing_ok}" -eq 1 ]]; then
        echo -e "EXISTING_PASS\t${run_accession}\t${filename}" >> "${EXISTING_LOG}"
        echo "SKIP: ${filename} exists and passed available integrity checks"
      else
        echo -e "EXISTING_FAIL\t${run_accession}\t${filename}" >> "${EXISTING_LOG}"
        echo "ERROR: ${filename} exists but failed one or more integrity checks. Manual review required."
      fi
      continue
    fi

    echo "DOWNLOAD: ${run_accession} -> ${filename}"
    if nice -n 19 ionice -c2 -n7 wget -c --limit-rate="${LIMIT_RATE}" "${url}" -O "${part_file}"; then
      echo "DOWNLOAD_COMPLETE_PART: ${part_file}"
    else
      echo -e "FAILED_DOWNLOAD\t${run_accession}\t${filename}\t${url}" >> "${FAILED_LOG}"
      echo "FAILED: ${filename}"
      continue
    fi

    new_ok=1
    validate_gzip "${part_file}" "new_part" "${run_accession}" || new_ok=0
    validate_md5_if_available "${part_file}" "${expected_md5}" "new_part" "${run_accession}" || new_ok=0
    validate_bytes_if_available "${part_file}" "${expected_bytes}" "new_part" "${run_accession}" || new_ok=0

    if [[ "${new_ok}" -ne 1 ]]; then
      echo -e "FAILED_VALIDATION_RETAIN_PART\t${run_accession}\t${filename}\t${part_file}" >> "${FAILED_LOG}"
      echo "ERROR: Validation failed for ${filename}; retained part file for manual review."
      continue
    fi

    if [[ -f "${final_file}" ]]; then
      echo -e "FAILED_PROMOTION_FINAL_APPEARED\t${run_accession}\t${filename}" >> "${FAILED_LOG}"
      echo "ERROR: Final file appeared before promotion; retained part file and did not overwrite."
      continue
    fi

    if mv "${part_file}" "${final_file}"; then
      echo "PROMOTED: ${part_file} -> ${final_file}"
    else
      echo -e "FAILED_PROMOTION\t${run_accession}\t${filename}\t${part_file}" >> "${FAILED_LOG}"
      echo "ERROR: Could not promote ${filename}; retained part file if present."
      continue
    fi

    echo
  done

  echo "----------------------------------------"
  echo "Completed processing for ${run_accession}"
  echo
done < "${EXTRACTED_MANIFEST}"

echo
echo "Download pass complete."
echo "Main log: ${LOGFILE}"
echo "Failure log: ${FAILED_LOG}"
echo "Gzip integrity log: ${GZIP_LOG}"
echo "MD5 integrity log: ${MD5_LOG}"
echo "Existing FASTQ audit log: ${EXISTING_LOG}"