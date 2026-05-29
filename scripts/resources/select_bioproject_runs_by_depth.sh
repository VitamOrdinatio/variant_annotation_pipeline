#!/usr/bin/env bash
set -euo pipefail

# Select representative BioProject runs by read-depth rank.
#
# Input:
#   Script A topology manifest, e.g.
#   data/reference/sra_support/manifests/prjeb57558/prjeb57558_runs_topology.tsv
#
# Output:
#   data/reference/sra_support/selections/<bioproject_lower>/<bioproject_lower>_selected_9_runs.tsv
#
# Selection policy:
#   1. Sort eligible runs by read_count descending.
#   2. Assign rank where rank 1 has the highest read_count.
#   3. Calculate rank_% = 100 * rank / total_eligible_runs.
#   4. Select 3 runs near Q1, 3 near median, and 3 near Q3:
#      target_rank - 1, target_rank, target_rank + 1.
#
# Usage:
# 1. In VAP repo root on both sys76 or MARK, run:
# ./scripts/resources/select_bioproject_runs_by_depth.sh data/reference/sra_support/manifests/prjeb57558/prjeb57558_runs_topology.tsv
#

MANIFEST="${1:-}"
if [[ -z "${MANIFEST}" ]]; then
  echo "ERROR: Usage: ./scripts/resources/select_bioproject_runs_by_depth.sh <runs_topology.tsv>"
  exit 1
fi

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
TIMESTAMP="$(date +%Y_%m_%d_%H%M%S)"

if [[ ! -f "${MANIFEST}" ]]; then
  echo "ERROR: Manifest not found: ${MANIFEST}"
  exit 1
fi

BASENAME="$(basename "${MANIFEST}")"
BIOPROJECT_LOWER="${BASENAME%%_runs_topology.tsv}"
if [[ -z "${BIOPROJECT_LOWER}" || "${BIOPROJECT_LOWER}" == "${BASENAME}" ]]; then
  echo "ERROR: Could not infer BioProject from manifest filename: ${BASENAME}"
  echo "Expected filename pattern: <bioproject_lower>_runs_topology.tsv"
  exit 1
fi

SRA_SUPPORT_DIR="${REPO_ROOT}/data/reference/sra_support"
OUTDIR="${SRA_SUPPORT_DIR}/selections/${BIOPROJECT_LOWER}"
LOGDIR="${OUTDIR}/logs"
mkdir -p "${OUTDIR}" "${LOGDIR}"

LOGFILE="${LOGDIR}/${BIOPROJECT_LOWER}_run_selection_${TIMESTAMP}.log"
exec > >(tee -a "${LOGFILE}") 2>&1

for cmd in awk sort tee date basename mktemp cp wc; do
  command -v "$cmd" >/dev/null 2>&1 || { echo "ERROR: Missing command: $cmd"; exit 1; }
done

TMP_ELIGIBLE="$(mktemp)"
TMP_RANKED="$(mktemp)"
TMP_SELECTED="$(mktemp)"

cleanup() {
  rm -f "${TMP_ELIGIBLE}" "${TMP_RANKED}" "${TMP_SELECTED}"
}
trap cleanup EXIT

echo "BioProject: ${BIOPROJECT_LOWER}"
echo "Repo root: ${REPO_ROOT}"
echo "Source manifest: ${MANIFEST}"
echo "Output directory: ${OUTDIR}"
echo "Log: ${LOGFILE}"
echo "Selection policy: Q1/median/Q3 using target_rank - 1, target_rank, target_rank + 1"
echo

echo "Extracting and validating eligible runs..."

awk -F'\t' '
  BEGIN {
    OFS="\t"
    required[1]="run_accession"
    required[2]="read_count"
    required[3]="base_count"
    required[4]="library_layout"
    required[5]="fastq_ftp"

    optional[1]="sample_accession"
    optional[2]="experiment_accession"
    optional[3]="study_accession"
    optional[4]="library_strategy"
    optional[5]="library_source"
    optional[6]="library_selection"
    optional[7]="instrument_model"
    optional[8]="fastq_bytes"
    optional[9]="fastq_md5"
  }

  NR==1 {
    for (i=1;i<=NF;i++) {
      gsub(/\r$/,"",$i)
      idx[$i]=i
    }

    for (r=1;r<=5;r++) {
      if (!(required[r] in idx)) {
        print "ERROR: Required column missing: " required[r] > "/dev/stderr"
        exit 2
      }
    }

    print "read_count_sort","run_accession","sample_accession","experiment_accession","study_accession","library_strategy","library_layout","library_source","library_selection","instrument_model","read_count","base_count","fastq_bytes","fastq_md5","fastq_ftp"
    next
  }

  {
    run=$(idx["run_accession"])
    read_count=$(idx["read_count"])
    base_count=$(idx["base_count"])
    layout=$(idx["library_layout"])
    ftp=$(idx["fastq_ftp"])

    gsub(/\r$/,"",run)
    gsub(/\r$/,"",read_count)
    gsub(/\r$/,"",base_count)
    gsub(/\r$/,"",layout)
    gsub(/\r$/,"",ftp)

    if (run=="" || read_count=="" || read_count !~ /^[0-9]+$/ || ftp=="") {
      excluded++
      next
    }

    sample=("sample_accession" in idx ? $(idx["sample_accession"]) : "")
    experiment=("experiment_accession" in idx ? $(idx["experiment_accession"]) : "")
    study=("study_accession" in idx ? $(idx["study_accession"]) : "")
    strategy=("library_strategy" in idx ? $(idx["library_strategy"]) : "")
    source=("library_source" in idx ? $(idx["library_source"]) : "")
    selection=("library_selection" in idx ? $(idx["library_selection"]) : "")
    instrument=("instrument_model" in idx ? $(idx["instrument_model"]) : "")
    fastq_bytes=("fastq_bytes" in idx ? $(idx["fastq_bytes"]) : "")
    fastq_md5=("fastq_md5" in idx ? $(idx["fastq_md5"]) : "")

    print read_count,run,sample,experiment,study,strategy,layout,source,selection,instrument,read_count,base_count,fastq_bytes,fastq_md5,ftp
    eligible++
  }

  END {
    print "Eligible runs: " eligible > "/dev/stderr"
    print "Excluded runs: " excluded > "/dev/stderr"
  }
' "${MANIFEST}" > "${TMP_ELIGIBLE}"

ELIGIBLE_COUNT="$(($(wc -l < "${TMP_ELIGIBLE}") - 1))"
if [[ "${ELIGIBLE_COUNT}" -lt 9 ]]; then
  echo "ERROR: Need at least 9 eligible runs; found ${ELIGIBLE_COUNT}"
  exit 1
fi

echo "Eligible runs after filtering: ${ELIGIBLE_COUNT}"
echo "Ranking by read_count descending..."

{
  head -n 1 "${TMP_ELIGIBLE}"
  tail -n +2 "${TMP_ELIGIBLE}" | sort -t $'\t' -k1,1nr -k2,2
} > "${TMP_RANKED}"

Q1_TARGET=$(( (ELIGIBLE_COUNT + 3) / 4 ))
MEDIAN_TARGET=$(( (ELIGIBLE_COUNT + 1) / 2 ))
Q3_TARGET=$(( (3 * ELIGIBLE_COUNT + 3) / 4 ))

echo "Rank method: descending read_count; rank 1 = highest read_count"
echo "Target strata:"
echo "  Q1 target rank: ${Q1_TARGET}"
echo "  Median target rank: ${MEDIAN_TARGET}"
echo "  Q3 target rank: ${Q3_TARGET}"
echo

awk -F'\t' -v total="${ELIGIBLE_COUNT}" -v q1="${Q1_TARGET}" -v med="${MEDIAN_TARGET}" -v q3="${Q3_TARGET}" '
  BEGIN { OFS="\t" }

  NR==1 {
    print "run_accession","sample_accession","experiment_accession","study_accession","library_strategy","library_layout","library_source","library_selection","instrument_model","read_count","rank","rank_%","depth_category","base_count","fastq_bytes","fastq_md5","fastq_ftp"
    next
  }

  {
    rank=NR-1
    rank_pct=100*rank/total
    category=""

    if (rank==q1-1 || rank==q1 || rank==q1+1) category="q1"
    else if (rank==med-1 || rank==med || rank==med+1) category="median"
    else if (rank==q3-1 || rank==q3 || rank==q3+1) category="q3"

    if (category!="") {
      print $2,$3,$4,$5,$6,$7,$8,$9,$10,$11,rank,sprintf("%.2f",rank_pct),category,$12,$13,$14,$15
    }
  }
' "${TMP_RANKED}" > "${TMP_SELECTED}"

SELECTED_COUNT="$(($(wc -l < "${TMP_SELECTED}") - 1))"
if [[ "${SELECTED_COUNT}" -ne 9 ]]; then
  echo "ERROR: Expected 9 selected runs; found ${SELECTED_COUNT}"
  exit 1
fi

TIMESTAMPED_OUT="${OUTDIR}/${BIOPROJECT_LOWER}_selected_9_runs_${TIMESTAMP}.tsv"
STABLE_OUT="${OUTDIR}/${BIOPROJECT_LOWER}_selected_9_runs.tsv"

cp "${TMP_SELECTED}" "${TIMESTAMPED_OUT}"
cp "${TMP_SELECTED}" "${STABLE_OUT}"

echo "Selected runs:"
awk -F'\t' 'NR==1 {next} {print "  " $13 ": rank " $11 " (" $12 "%), " $1 ", read_count=" $10}' "${STABLE_OUT}"

echo
echo "Selection complete."
echo "Timestamped selected manifest: ${TIMESTAMPED_OUT}"
echo "Stable selected manifest: ${STABLE_OUT}"
echo "Selection log: ${LOGFILE}"