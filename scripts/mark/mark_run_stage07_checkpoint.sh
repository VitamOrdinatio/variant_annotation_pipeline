#!/usr/bin/env bash
set -euo pipefail

TS="$(date +%Y%m%d_%H%M%S)"
LOG="/root/Desktop/mark_run_stage07_checkpoint_${TS}.log"
REPO_ROOT="$HOME/dev/portfolio_projects/variant_annotation_pipeline"
CONFIG_PATH="$REPO_ROOT/config/config.mark.local.yaml"

exec > >(tee "$LOG") 2>&1

echo "[INFO] Mark Stage 07 checkpoint run started at $(date)"
echo "[INFO] Log file: $LOG"
echo "[INFO] Repo root: $REPO_ROOT"
echo "[INFO] Config path: $CONFIG_PATH"
echo

cd "$REPO_ROOT"
source .venv/bin/activate

echo "=== REPO STATUS ==="
git status --short || true
echo

echo "=== FIND LATEST NORMALIZED VCF ==="
NORMALIZED_VCF="$(find "$REPO_ROOT/results" -type f -name "*.normalized_variants.vcf" | sort | tail -n 1 || true)"
if [[ -z "${NORMALIZED_VCF:-}" ]]; then
  echo "[ERROR] No normalized VCF found."
  exit 1
fi
echo "[INFO] NORMALIZED_VCF=$NORMALIZED_VCF"
echo

echo "=== RUN STAGE 07 FROM CHECKPOINT ==="
python - <<'PY'
import json
from pathlib import Path
import yaml

from pipeline.stage_07_annotate_variants import run_stage

class ProbeLogger:
    def info(self, msg): print(f"[LOGGER][INFO] {msg}")
    def warning(self, msg): print(f"[LOGGER][WARN] {msg}")
    def error(self, msg): print(f"[LOGGER][ERROR] {msg}")

repo_root = Path("/root/dev/portfolio_projects/variant_annotation_pipeline")
config_path = repo_root / "config" / "config.mark.local.yaml"

with config_path.open("r", encoding="utf-8") as fh:
    config = yaml.safe_load(fh)

normalized_vcfs = sorted((repo_root / "results").rglob("*.normalized_variants.vcf"))
if not normalized_vcfs:
    raise SystemExit("No normalized VCF found")

normalized_vcf = normalized_vcfs[-1]
run_dir = normalized_vcf.parent.parent
processed_dir = run_dir / "processed"
processed_dir.mkdir(parents=True, exist_ok=True)

run_id = run_dir.name
sample_id = normalized_vcf.name.split("_run_")[0]

state = {
    "sample": {"sample_id": sample_id},
    "run": {"run_id": run_id},
    "artifacts": {"normalized_vcf": str(normalized_vcf)},
    "gene_sets": {
        "mitocarta_path": "/data/storage/gene_sets/MitoCarta3.0_human_genes.tsv",
        "genes4epilepsy_path": "/data/storage/gene_sets/Genes4Epilepsy.tsv",
        "overlay_completed": False,
        "flags_added": [],
    },
    "annotations": {},
    "qc": {},
    "stage_outputs": {},
    "warnings": [],
}

paths = {"processed_dir": str(processed_dir)}
logger = ProbeLogger()

print("[PYTHON][INFO] NORMALIZED_VCF=", normalized_vcf)
print("[PYTHON][INFO] PROCESSED_DIR=", processed_dir)
print("[PYTHON][INFO] SAMPLE_ID=", sample_id)
print("[PYTHON][INFO] RUN_ID=", run_id)

updated_state = run_stage(config=config, paths=paths, logger=logger, state=state)

print()
print("=== STAGE 07 RESULT SUMMARY ===")
print(json.dumps({
    "artifacts": {
        "annotated_vcf": updated_state["artifacts"].get("annotated_vcf"),
        "annotated_table": updated_state["artifacts"].get("annotated_table"),
    },
    "annotation_qc": updated_state["qc"].get("annotation_qc"),
    "stage_output": updated_state["stage_outputs"].get("stage_07_annotate_variants"),
    "warnings_count": len(updated_state.get("warnings", [])),
    "warnings_head": updated_state.get("warnings", [])[:10],
}, indent=2))
PY
echo

echo "=== STAGE 07 OUTPUT CHECK ==="
find "$REPO_ROOT/results" -type f \( -name "*.annotated_variants.tsv" -o -name "*.annotated_variants.vcf" \) -exec ls -lh {} \; | sort
echo

echo "=== STAGE 07 FIRST TSV ROW ==="
LATEST_TSV="$(find "$REPO_ROOT/results" -type f -name "*.annotated_variants.tsv" | sort | tail -n 1 || true)"
if [[ -n "${LATEST_TSV:-}" ]]; then
  echo "[INFO] LATEST_TSV=$LATEST_TSV"
  head -n 2 "$LATEST_TSV" | column -t -s $'\t' || true
fi
echo

echo "[INFO] Mark Stage 07 checkpoint run completed at $(date)"
echo "[INFO] Log file saved to: $LOG"