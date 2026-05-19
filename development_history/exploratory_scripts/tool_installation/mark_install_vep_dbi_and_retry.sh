#!/usr/bin/env bash
set -euo pipefail

TS="$(date +%Y%m%d_%H%M%S)"
LOG="/root/Desktop/mark_install_vep_dbi_and_retry_${TS}.log"
REPO_ROOT="$HOME/dev/portfolio_projects/variant_annotation_pipeline"
VEP_ROOT="/root/tools/vep/ensembl-vep-release-115.0"

exec > >(tee "$LOG") 2>&1

echo "[INFO] Mark VEP DBI install + retry started at $(date)"
echo "[INFO] Log file: $LOG"
echo "[INFO] Repo root: $REPO_ROOT"
echo "[INFO] VEP root: $VEP_ROOT"
echo

cd "$REPO_ROOT"
source .venv/bin/activate

echo "=== PRECHECK: DBI BEFORE INSTALL ==="
echo "[CMD] perl -MDBI -e 'print \$DBI::VERSION, qq(\n)'"
perl -MDBI -e 'print $DBI::VERSION, qq(\n)' || true
echo

echo "=== APT INSTALL DBI ==="
echo "[CMD] apt-get update"
apt-get update
echo

echo "[CMD] apt-get install -y libdbi-perl"
apt-get install -y libdbi-perl
echo

echo "=== VERIFY DBI AFTER INSTALL ==="
echo "[CMD] perl -MDBI -e 'print \$DBI::VERSION, qq(\n)'"
perl -MDBI -e 'print $DBI::VERSION, qq(\n)' || true
echo

echo "=== RERUN VEP INSTALLER ==="
cd "$VEP_ROOT"
echo "[CMD] perl INSTALL.pl --NO_TEST"
perl INSTALL.pl --NO_TEST || true
echo

echo "=== POST-INSTALL HELP CHECK ==="
echo "[CMD] /root/tools/vep/vep --help | head"
"/root/tools/vep/vep" --help | head || true
echo

echo "[INFO] Mark VEP DBI install + retry completed at $(date)"
echo "[INFO] Log file saved to: $LOG"