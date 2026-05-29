#!/usr/bin/env bash
set -uo pipefail

DESKTOP="/root/Desktop"
VAP_ROOT="/root/dev/portfolio_projects/variant_annotation_pipeline"
TS="$(date +%Y_%m_%d_%H%M%S)"
OUT="${DESKTOP}/mark_probe_script_c_${TS}.txt"

{
  echo "MARK Script C Probe"
  echo "Timestamp: ${TS}"
  echo "Host short: $(hostname -s)"
  echo "Host full: $(hostname -f 2>/dev/null || true)"
  echo "User: $(whoami)"
  echo

  echo "===== cd into VAP root ====="
  cd "${VAP_ROOT}" || { echo "ERROR: Cannot cd into ${VAP_ROOT}"; exit 1; }
  pwd
  echo

  echo "===== Git/script presence ====="
  ls -lh scripts/resources/download_selected_fastqs_polite.sh
  echo

  echo "===== Script C syntax check ====="
  bash -n scripts/resources/download_selected_fastqs_polite.sh
  echo "bash -n exit code: $?"
  echo

  echo "===== MARK host guard variables from script ====="
  grep -nE 'MARK_HOST_PATTERN|HOST_SHORT|ALLOW_NON_MARK|MARK-compatible' scripts/resources/download_selected_fastqs_polite.sh
  echo

  echo "===== Current hostname matching expectation ====="
  HOST_SHORT="$(hostname -s | tr '[:upper:]' '[:lower:]')"
  MARK_HOST_PATTERN="^vandpymolgpuresearch[0-9]*$"
  echo "HOST_SHORT=${HOST_SHORT}"
  echo "MARK_HOST_PATTERN=${MARK_HOST_PATTERN}"
  if [[ "${HOST_SHORT}" =~ ${MARK_HOST_PATTERN} ]]; then
    echo "HOST_MATCH=YES"
  else
    echo "HOST_MATCH=NO"
  fi
  echo

  echo "===== Manifest discovery ====="
  ls -lh data/reference/sra_support/selections/prjeb57558/ || true
  echo
  ls -lh data/reference/sra_support/selections/prjeb57558/prjeb57558_selected_9_runs*.tsv || true
  echo

  MANIFEST="$(ls -1 data/reference/sra_support/selections/prjeb57558/prjeb57558_selected_9_runs_*.tsv 2>/dev/null | sort | tail -n 1)"
  if [[ -z "${MANIFEST}" ]]; then
    MANIFEST="data/reference/sra_support/selections/prjeb57558/prjeb57558_selected_9_runs.tsv"
  fi
  echo "Chosen manifest: ${MANIFEST}"
  ls -lh "${MANIFEST}" || true
  echo

  echo "===== Manifest header and first records ====="
  head -1 "${MANIFEST}" | tr '\t' '\n' | nl -ba
  echo
  echo "Line count:"
  wc -l "${MANIFEST}"
  echo
  echo "Pretty first 12 lines:"
  column -t -s $'\t' "${MANIFEST}" | head -12
  echo

  echo "===== Required commands ====="
  for cmd in awk wget gunzip tee date hostname basename mktemp md5sum stat mv nice ionice; do
    if command -v "$cmd" >/dev/null 2>&1; then
      echo "FOUND: $cmd -> $(command -v "$cmd")"
    else
      echo "MISSING: $cmd"
    fi
  done
  echo

  echo "===== FASTQ target directories ====="
  echo "/data/storage/fastq:"
  ls -ld /data/storage/fastq || true
  echo
  echo "/data/storage/fastq/.incomplete:"
  ls -ld /data/storage/fastq/.incomplete || true
  echo

  echo "===== Existing FASTQs matching selected manifest ====="
  awk -F'\t' '
    NR==1 {
      for(i=1;i<=NF;i++) idx[$i]=i
      next
    }
    {
      split($(idx["fastq_ftp"]), urls, ";")
      for (u in urls) {
        n=split(urls[u], parts, "/")
        print parts[n]
      }
    }
  ' "${MANIFEST}" | while read -r fn; do
    [[ -z "$fn" ]] && continue
    if [[ -f "/data/storage/fastq/${fn}" ]]; then
      echo "EXISTS: /data/storage/fastq/${fn}"
      ls -lh "/data/storage/fastq/${fn}"
    else
      echo "MISSING: /data/storage/fastq/${fn}"
    fi
  done
  echo

  echo "===== Existing Script C logs ====="
  ls -lh data/reference/sra_support/download_logs/prjeb57558/ 2>/dev/null || true
  echo

  echo "===== Dry bash-x first 80 lines with OUTDIR redirected to /tmp, killed before wget would matter ====="
  echo "NOTE: This does not execute full download. It only verifies early startup path if timeout is available."
  if command -v timeout >/dev/null 2>&1; then
    timeout 5s bash -x scripts/resources/download_selected_fastqs_polite.sh "${MANIFEST}" 2>&1 | head -120
    echo "timeout/bash-x exit code: ${PIPESTATUS[0]}"
  else
    echo "timeout command unavailable; skipping bash-x execution probe."
  fi

} > "${OUT}" 2>&1

echo "Probe complete."
echo "Wrote:"
echo "${OUT}"
ls -lh "${OUT}"