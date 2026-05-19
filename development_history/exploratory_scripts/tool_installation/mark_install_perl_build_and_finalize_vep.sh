#!/usr/bin/env bash
set -euo pipefail

TS="$(date +%Y%m%d_%H%M%S)"
LOG="/root/Desktop/mark_install_perl_build_finalize_vep_${TS}.log"
REPO_ROOT="$HOME/dev/portfolio_projects/variant_annotation_pipeline"
VEP_ROOT="/root/tools/vep/ensembl-vep-release-115.2"

exec > >(tee "$LOG") 2>&1

echo "[INFO] Mark final Perl build dependency + VEP finalize started at $(date)"
echo "[INFO] Log file: $LOG"
echo "[INFO] Repo root: $REPO_ROOT"
echo "[INFO] VEP root: $VEP_ROOT"
echo

cd "$REPO_ROOT"
source .venv/bin/activate

echo "=== INSTALL PERL BUILD TOOLCHAIN ==="
echo "[CMD] apt-get update"
apt-get update
echo

echo "[CMD] apt-get install -y libmodule-build-perl"
apt-get install -y libmodule-build-perl
echo

echo "=== VERIFY MODULE::Build ==="
echo "[CMD] perl -MModule::Build -e 'print \"OK\n\"'"
perl -MModule::Build -e 'print "OK\n"' || true
echo

echo "=== RERUN VEP INSTALLER ==="
cd "$VEP_ROOT"
echo "[CMD] printf 'n\n' | perl INSTALL.pl --NO_TEST"
printf 'n\n' | perl INSTALL.pl --NO_TEST || true
echo

echo "=== VERIFY ENSEMBL API ==="
echo "[CMD] perl -MBio::EnsEMBL::Registry -e 'print \"OK\n\"'"
perl -MBio::EnsEMBL::Registry -e 'print "OK\n"' || true
echo

echo "=== FINAL VEP TEST ==="
echo "[CMD] /root/tools/vep/vep --help | head"
"/root/tools/vep/vep" --help | head || true
echo

echo "[INFO] Mark VEP finalization completed at $(date)"
echo "[INFO] Log file saved to: $LOG"