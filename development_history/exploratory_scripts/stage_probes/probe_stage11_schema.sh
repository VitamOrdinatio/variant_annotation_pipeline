#!/usr/bin/env bash
set -euo pipefail

# ==================================================
# MARK Probe: Locate Stage 11 Outputs from Desktop
# Intended to be uploaded/run from /root/Desktop
# ==================================================

REPO_DIR="$HOME/dev/portfolio_projects/variant_annotation_pipeline"
RUN_ID="run_2026_05_14_164444"
RUN_DIR="${REPO_DIR}/results/${RUN_ID}"
OUTFILE="/root/Desktop/stage11_path_probe_${RUN_ID}.txt"

{
echo "=================================================="
echo "Stage 11 Path Probe"
echo "=================================================="
echo "REPO_DIR: ${REPO_DIR}"
echo "RUN_ID: ${RUN_ID}"
echo "RUN_DIR: ${RUN_DIR}"
echo

if [[ ! -d "${REPO_DIR}" ]]; then
    echo "[ERROR] Repo directory not found: ${REPO_DIR}"
    exit 1
fi

if [[ ! -d "${RUN_DIR}" ]]; then
    echo "[ERROR] Run directory not found: ${RUN_DIR}"
    echo
    echo "Available run directories:"
    find "${REPO_DIR}/results" -maxdepth 1 -type d -name "run_*" | sort
    exit 1
fi

echo "=================================================="
echo "TOP-LEVEL RUN CONTENTS"
echo "=================================================="
find "${RUN_DIR}" -maxdepth 2 | sort
echo

echo "=================================================="
echo "FILES MATCHING 'stage_11'"
echo "=================================================="
find "${RUN_DIR}" -type f | grep "stage_11" || true
echo

echo "=================================================="
echo "FILES MATCHING 'prioritized'"
echo "=================================================="
find "${RUN_DIR}" -type f | grep "prioritized" || true
echo

echo "=================================================="
echo "TSV FILES"
echo "=================================================="
find "${RUN_DIR}" -type f | grep "\.tsv$" | sort || true
echo

echo "=================================================="
echo "COMPLETE"
echo "=================================================="
} > "${OUTFILE}"

echo "Probe complete."
echo "Output written to:"
echo "${OUTFILE}"