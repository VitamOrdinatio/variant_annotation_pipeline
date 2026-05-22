#!/usr/bin/env bash

# How to run it on MARK:
# from /root/Desktop: 
# chmod +x mark_tool_probe.sh
# ./mark_tool_probe.sh
# Then download the generated log from /root/Desktop to Sys76

set -euo pipefail

TS="$(date +%Y%m%d_%H%M%S)"
LOG="/root/Desktop/mark_tool_probe_${TS}.log"
REPO_ROOT="$HOME/dev/portfolio_projects/variant_annotation_pipeline"

exec > >(tee "$LOG") 2>&1

echo "[INFO] Mark tool probe started at $(date)"
echo "[INFO] Log file: $LOG"
echo "[INFO] Initial working directory: $(pwd)"
echo "[INFO] Target repo root: $REPO_ROOT"
echo

echo "[STEP] Changing into VAP repo root"
cd "$REPO_ROOT"
echo "[INFO] Current working directory: $(pwd)"
echo

echo "=== USER / HOST CONTEXT ==="
echo "[CMD] whoami"
whoami || true
echo
echo "[CMD] hostname"
hostname || true
echo
echo "[INFO] HOME=$HOME"
echo

echo "=== REPO STATUS ==="
echo "[CMD] git status"
git status || true
echo

echo "=== TOOLS DIRECTORY OVERVIEW ==="
echo "[CMD] ls -lah \$HOME/tools"
ls -lah "$HOME/tools" || true
echo

echo "[CMD] tree -L 3 \$HOME/tools"
tree -L 3 "$HOME/tools" || true
echo

echo "=== GATK CHECKS ==="
echo "[CMD] which gatk"
which gatk || true
echo

echo "[CMD] ls -lah \$HOME/tools/gatk"
ls -lah "$HOME/tools/gatk" || true
echo

echo "[CMD] find \$HOME/tools -maxdepth 4 -name gatk -type f"
find "$HOME/tools" -maxdepth 4 -name gatk -type f 2>/dev/null || true
echo

echo "[CMD] ls -lah \$HOME/tools/gatk/gatk"
ls -lah "$HOME/tools/gatk/gatk" || true
echo

echo "[CMD] file \$HOME/tools/gatk/gatk"
file "$HOME/tools/gatk/gatk" || true
echo

echo "[CMD] \$HOME/tools/gatk/gatk --help | head"
"$HOME/tools/gatk/gatk" --help | head || true
echo

echo "=== PERL / VEP / ANNOVAR CHECKS ==="
echo "[CMD] which perl"
which perl || true
echo

echo "[CMD] which vep"
which vep || true
echo

echo "[CMD] find \$HOME/tools -maxdepth 4 \\( -name vep -o -name table_annovar.pl -o -name annotate_variation.pl \\)"
find "$HOME/tools" -maxdepth 4 \( -name vep -o -name table_annovar.pl -o -name annotate_variation.pl \) 2>/dev/null || true
echo

echo "=== VAP TOOL SCRIPT STATUS ==="
echo "[CMD] TARGET_ENV=mark MODE=status bash scripts/tools/setup_pipeline_tools.sh"
TARGET_ENV=mark MODE=status bash scripts/tools/setup_pipeline_tools.sh || true
echo

echo "[INFO] Mark tool probe completed at $(date)"
echo "[INFO] Log file saved to: $LOG"