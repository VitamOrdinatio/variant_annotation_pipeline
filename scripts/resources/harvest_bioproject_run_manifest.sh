#!/usr/bin/env bash
set -euo pipefail


# Script functionality:

# 1. This script is designed to harvest metadata about sequencing runs from the ENA API for a specified BioProject (defaulting to PRJEB57558).
# 2. It retrieves the list of all available fields for the "read_run" result type, then downloads a comprehensive TSV report containing all metadata for every run associated with the BioProject.
# 3. The script then processes the downloaded TSV to remove any columns that are completely empty, resulting in a cleaner "topology" TSV that retains only fields with data.
# 4. Both the raw and cleaned TSV files are saved with timestamped filenames for traceability, and stable copies without timestamps are also created for consistent downstream use.
# 5. The script includes robust error handling, logging, and is designed to be run on the MARK server with safeguards to prevent accidental execution on non-MARK environments. It also checks for the presence of required commands before execution.

# Script execution (you can swap out the BioProject ID if needed):
#
# 1. On MARK's VAP repo root, run: 
# 
#     ./scripts/resources/harvest_bioproject_run_manifest.sh PRJEB57558
#     
# 2. On DEV node's repo root, run:
#  
#     ALLOW_NON_MARK=1 ./scripts/resources/harvest_bioproject_run_manifest.sh PRJEB57558


# Set Global Variables
BIOPROJECT="${1:-PRJEB57558}"
BIOPROJECT_LOWER="$(echo "${BIOPROJECT}" | tr '[:upper:]' '[:lower:]')"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SRA_SUPPORT_DIR="${REPO_ROOT}/data/reference/sra_support"
OUTDIR="${SRA_SUPPORT_DIR}/manifests/${BIOPROJECT_LOWER}"
LOGDIR="${OUTDIR}/logs"
TIMESTAMP="$(date +%Y_%m_%d_%H%M%S)"
LOGFILE="${LOGDIR}/${BIOPROJECT_LOWER}_manifest_harvest_${TIMESTAMP}.log"

BASE_URL="https://www.ebi.ac.uk/ena/portal/api"
USER_AGENT="VAP-manifest-harvester/0.1"

CURL_LIMIT_RATE="${CURL_LIMIT_RATE:-5M}"
CURL_RETRIES="${CURL_RETRIES:-5}"
CURL_RETRY_DELAY="${CURL_RETRY_DELAY:-10}"

mkdir -p "${OUTDIR}" "${LOGDIR}"
exec > >(tee -a "${LOGFILE}") 2>&1

if [[ "${ALLOW_NON_MARK:-0}" != "1" && ! "$(hostname -s)" =~ [Mm][Aa][Rr][Kk] ]]; then
  echo "ERROR: This script is intended for MARK. Set ALLOW_NON_MARK=1 only for dry testing."
  exit 1
fi

for cmd in curl awk tee date hostname nice ionice cp wc paste; do
  command -v "$cmd" >/dev/null 2>&1 || { echo "ERROR: Missing command: $cmd"; exit 1; }
done

fetch_fields() {
  local result="$1"
  nice -n 19 ionice -c2 -n7 curl --fail --location --silent --show-error --retry "${CURL_RETRIES}" --retry-delay "${CURL_RETRY_DELAY}" --limit-rate "${CURL_LIMIT_RATE}" \
    -A "${USER_AGENT}" \
    "${BASE_URL}/returnFields?dataPortal=ena&format=tsv&result=${result}" \
  | awk -F'\t' 'NR>1 && $1 != "" {print $1}' \
  | paste -sd, -
}

download_report() {
  local result="$1"
  local fields="$2"
  local outfile="$3"
  nice -n 19 ionice -c2 -n7 curl --fail --location --silent --show-error --retry "${CURL_RETRIES}" --retry-delay "${CURL_RETRY_DELAY}" --limit-rate "${CURL_LIMIT_RATE}" \
    -A "${USER_AGENT}" \
    -G "${BASE_URL}/filereport" \
    --data-urlencode "accession=${BIOPROJECT}" \
    --data-urlencode "result=${result}" \
    --data-urlencode "fields=${fields}" \
    --data-urlencode "format=tsv" \
    > "${outfile}"
}

drop_empty_columns() {
  local infile="$1"
  local outfile="$2"
  awk -F'\t' '
    BEGIN { OFS="\t" }
    NR==1 { n=split($0,h,FS); next }
    {
      rows[NR]=$0
      for (i=1;i<=n;i++) if ($i!="") keep[i]=1
    }
    END {
      first=1
      for (i=1;i<=n;i++) if (i in keep) {
        printf "%s%s",(first?"":OFS),h[i]
        first=0
      }
      print ""
      for (r=2;r<=NR;r++) {
        split(rows[r],f,FS)
        first=1
        for (i=1;i<=n;i++) if (i in keep) {
          printf "%s%s",(first?"":OFS),f[i]
          first=0
        }
        print ""
      }
    }
  ' "${infile}" > "${outfile}"
}

echo "BioProject: ${BIOPROJECT}"
echo "Repo root: ${REPO_ROOT}"
echo "Output directory: ${OUTDIR}"
echo "Log: ${LOGFILE}"
echo "Curl policy: nice -n 19 ionice -c2 -n7 curl --retry ${CURL_RETRIES} --retry-delay ${CURL_RETRY_DELAY} --limit-rate ${CURL_LIMIT_RATE}"
echo

RUN_FIELDS_FILE="${OUTDIR}/${BIOPROJECT_LOWER}_read_run_fields_${TIMESTAMP}.txt"
ALL_RUNS_TS="${OUTDIR}/${BIOPROJECT_LOWER}_all_runs_${TIMESTAMP}.tsv"
RUNS_TOPOLOGY_TS="${OUTDIR}/${BIOPROJECT_LOWER}_runs_topology_${TIMESTAMP}.tsv"

echo "Discovering ENA read_run fields..."
RUN_FIELDS="$(fetch_fields read_run)"
echo "${RUN_FIELDS}" | tr ',' '\n' > "${RUN_FIELDS_FILE}"
echo "Discovered run fields: $(wc -l < "${RUN_FIELDS_FILE}")"

echo "Downloading full read_run report..."
download_report read_run "${RUN_FIELDS}" "${ALL_RUNS_TS}"

echo "Dropping completely empty columns..."
drop_empty_columns "${ALL_RUNS_TS}" "${RUNS_TOPOLOGY_TS}"

echo "Validating harvested outputs..."

[[ -s "${RUN_FIELDS_FILE}" ]] || { echo "ERROR: Field list is empty: ${RUN_FIELDS_FILE}"; exit 1; }
[[ -s "${ALL_RUNS_TS}" ]] || { echo "ERROR: Raw run manifest is empty: ${ALL_RUNS_TS}"; exit 1; }
[[ -s "${RUNS_TOPOLOGY_TS}" ]] || { echo "ERROR: Topology manifest is empty: ${RUNS_TOPOLOGY_TS}"; exit 1; }

for required_col in run_accession read_count base_count library_layout fastq_ftp; do
  if ! awk -F'\t' -v col="${required_col}" 'NR==1 {for(i=1;i<=NF;i++) if($i==col) found=1; exit !found}' "${RUNS_TOPOLOGY_TS}"; then
    echo "ERROR: Required topology column missing: ${required_col}"
    exit 1
  fi
done

echo "Validation passed."

echo "Updating stable latest-copy manifests after successful validation..."

cp "${ALL_RUNS_TS}" "${OUTDIR}/${BIOPROJECT_LOWER}_all_runs.tsv"
cp "${RUNS_TOPOLOGY_TS}" "${OUTDIR}/${BIOPROJECT_LOWER}_runs_topology.tsv"
cp "${RUN_FIELDS_FILE}" "${OUTDIR}/${BIOPROJECT_LOWER}_read_run_fields.txt"

echo
echo "Manifest harvest complete."
echo "Timestamped raw manifest: ${ALL_RUNS_TS}"
echo "Timestamped topology manifest: ${RUNS_TOPOLOGY_TS}"
echo "Stable raw manifest: ${OUTDIR}/${BIOPROJECT_LOWER}_all_runs.tsv"
echo "Stable topology manifest: ${OUTDIR}/${BIOPROJECT_LOWER}_runs_topology.tsv"