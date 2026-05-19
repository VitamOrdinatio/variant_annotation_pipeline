#!/usr/bin/env bash
set -euo pipefail

TS="$(date +%Y%m%d_%H%M%S)"
LOG="/root/Desktop/mark_probe_vep_perl_deps_${TS}.log"
REPO_ROOT="$HOME/dev/portfolio_projects/variant_annotation_pipeline"
VEP_ROOT="/root/tools/vep/ensembl-vep-release-115.0"

exec > >(tee "$LOG") 2>&1

echo "[INFO] Mark VEP Perl dependency probe started at $(date)"
echo "[INFO] Log file: $LOG"
echo "[INFO] Repo root: $REPO_ROOT"
echo "[INFO] VEP root: $VEP_ROOT"
echo

cd "$REPO_ROOT"
source .venv/bin/activate

echo "=== BASIC PERL CONTEXT ==="
echo "[CMD] which perl"
which perl || true
echo

echo "[CMD] perl -v | head -n 5"
perl -v | head -n 5 || true
echo

echo "[CMD] perl -MDBI -e 'print \$DBI::VERSION, qq(\\n)'"
perl -MDBI -e 'print $DBI::VERSION, qq(\n)' || true
echo

echo "=== SYSTEM PACKAGE DISCOVERY ==="
echo "[CMD] apt-cache policy libdbi-perl"
apt-cache policy libdbi-perl || true
echo

echo "[CMD] apt-cache search libdbi-perl"
apt-cache search libdbi-perl || true
echo

echo "[CMD] which cpan"
which cpan || true
echo

echo "[CMD] which cpanm"
which cpanm || true
echo

echo "=== VEP INSTALLER RETRY (EXPECTED TO FAIL OR PROGRESS) ==="
cd "$VEP_ROOT"
echo "[CMD] perl INSTALL.pl --NO_TEST"
perl INSTALL.pl --NO_TEST || true
echo

echo "=== POST-PROBE HELP CHECK ==="
echo "[CMD] /root/tools/vep/vep --help | head"
"/root/tools/vep/vep" --help | head || true
echo

echo "[INFO] Mark VEP Perl dependency probe completed at $(date)"
echo "[INFO] Log file saved to: $LOG"