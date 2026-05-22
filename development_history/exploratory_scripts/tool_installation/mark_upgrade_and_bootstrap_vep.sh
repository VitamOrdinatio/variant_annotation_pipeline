#!/usr/bin/env bash
set -euo pipefail

TS="$(date +%Y%m%d_%H%M%S)"
LOG="/root/Desktop/mark_upgrade_and_bootstrap_vep_${TS}.log"
REPO_ROOT="$HOME/dev/portfolio_projects/variant_annotation_pipeline"

VEP_VERSION="115.2"
VEP_ARCHIVE_NAME="ensembl-vep-release-${VEP_VERSION}.tar.gz"
VEP_URL="https://github.com/Ensembl/ensembl-vep/archive/refs/tags/release/${VEP_VERSION}.tar.gz"
VEP_ARCHIVE_PATH="/root/Desktop/${VEP_ARCHIVE_NAME}"
VEP_TOOLS_DIR="/root/tools/vep"
VEP_ROOT="${VEP_TOOLS_DIR}/ensembl-vep-release-${VEP_VERSION}"

exec > >(tee "$LOG") 2>&1

echo "[INFO] Mark VEP upgrade/bootstrap started at $(date)"
echo "[INFO] Log file: $LOG"
echo "[INFO] Repo root: $REPO_ROOT"
echo "[INFO] VEP version: $VEP_VERSION"
echo "[INFO] VEP archive path: $VEP_ARCHIVE_PATH"
echo "[INFO] VEP tools dir: $VEP_TOOLS_DIR"
echo "[INFO] VEP root: $VEP_ROOT"
echo

cd "$REPO_ROOT"
source .venv/bin/activate

echo "=== PRECHECKS ==="
echo "[CMD] perl -MDBI -e 'print \$DBI::VERSION, qq(\n)'"
perl -MDBI -e 'print $DBI::VERSION, qq(\n)' || true
echo

echo "[CMD] ls -lah /root/tools"
ls -lah /root/tools || true
echo

echo "=== DOWNLOAD LATEST VEP ARCHIVE ==="
rm -f "$VEP_ARCHIVE_PATH"
echo "[CMD] curl -fL -o $VEP_ARCHIVE_PATH $VEP_URL"
curl -fL -o "$VEP_ARCHIVE_PATH" "$VEP_URL"
echo

echo "[CMD] ls -lah $VEP_ARCHIVE_PATH"
ls -lah "$VEP_ARCHIVE_PATH"
echo

echo "[CMD] tar -tzf $VEP_ARCHIVE_PATH | head"
tar -tzf "$VEP_ARCHIVE_PATH" | head || true
echo

echo "=== CLEAN PREVIOUS VEP SOURCE TREE ==="
echo "[CMD] rm -rf $VEP_ROOT"
rm -rf "$VEP_ROOT"
echo

echo "=== EXTRACT INTO /root/tools/vep ==="
mkdir -p "$VEP_TOOLS_DIR"
echo "[CMD] tar -xzf $VEP_ARCHIVE_PATH -C $VEP_TOOLS_DIR"
tar -xzf "$VEP_ARCHIVE_PATH" -C "$VEP_TOOLS_DIR"
echo

echo "=== REFRESH CANONICAL SYMLINK ==="
rm -f "${VEP_TOOLS_DIR}/vep"
ln -s "${VEP_ROOT}/vep" "${VEP_TOOLS_DIR}/vep"
echo "[CMD] ls -lah $VEP_TOOLS_DIR"
ls -lah "$VEP_TOOLS_DIR"
echo

echo "=== RUN INSTALL.PL (AUTO-CONTINUE IF ASKED) ==="
cd "$VEP_ROOT"
echo "[CMD] printf 'n\n' | perl INSTALL.pl --NO_TEST"
printf 'n\n' | perl INSTALL.pl --NO_TEST || true
echo

echo "=== POST-INSTALL HELP CHECK ==="
echo "[CMD] /root/tools/vep/vep --help | head"
"/root/tools/vep/vep" --help | head || true
echo

echo "=== FINAL LAYOUT ==="
echo "[CMD] tree -L 3 /root/tools/vep"
tree -L 3 /root/tools/vep || true
echo

echo "[INFO] Mark VEP upgrade/bootstrap completed at $(date)"
echo "[INFO] Log file saved to: $LOG"