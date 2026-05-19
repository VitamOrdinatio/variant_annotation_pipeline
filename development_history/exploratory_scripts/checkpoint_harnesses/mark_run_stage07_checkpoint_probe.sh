#!/usr/bin/env bash
set -euo pipefail

TS="$(date +%Y%m%d_%H%M%S)"
LOG="/root/Desktop/mark_run_stage07_checkpoint_probe_${TS}.log"
REPO_ROOT="$HOME/dev/portfolio_projects/variant_annotation_pipeline"
CONFIG_PATH="$REPO_ROOT/config/config.mark.local.yaml"

exec > >(tee "$LOG") 2>&1

echo "[INFO] Mark Stage 07 checkpoint probe started at $(date)"
echo "[INFO] Log file: $LOG"
echo "[INFO] Repo root: $REPO_ROOT"
echo "[INFO] Config path: $CONFIG_PATH"
echo

cd "$REPO_ROOT"

echo "[STEP] Activating VAP .venv"
source .venv/bin/activate
echo "[INFO] Venv activated."
echo

echo "=== REPO STATUS ==="
echo "[CMD] git status --short"
git status --short || true
echo

echo "=== FIND LATEST NORMALIZED VCF ==="
LATEST_VCF="$(find "$REPO_ROOT/results" -type f -name "*.normalized_variants.vcf" | sort | tail -n 1 || true)"
if [[ -z "${LATEST_VCF:-}" ]]; then
  echo "[ERROR] No normalized VCF found under $REPO_ROOT/results"
  exit 1
fi
echo "[INFO] LATEST_VCF=$LATEST_VCF"
echo

echo "=== PYTHON STAGE 07 PROBE ==="
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

# Resolve latest normalized VCF
results_root = repo_root / "results"
normalized_vcfs = sorted(results_root.rglob("*.normalized_variants.vcf"))
if not normalized_vcfs:
    raise SystemExit("No normalized VCF found")
normalized_vcf = normalized_vcfs[-1]

# Derive run directory from artifact path
run_dir = normalized_vcf.parent.parent  # .../run_xxx/interim/file.vcf
run_id = run_dir.name
sample_id = normalized_vcf.name.split(".normalized_variants.vcf")[0]
# Convert HG002_run_... -> sample likely HG002
sample_id = sample_id.split("_run_")[0]

processed_dir = run_dir / "processed"
processed_dir.mkdir(parents=True, exist_ok=True)

# Try common gene-set file locations from config first; fallback to likely paths
mitocarta_path = config.get("gene_sets", {}).get("mitocarta_path")
genes4epilepsy_path = config.get("gene_sets", {}).get("genes4epilepsy_path")

if not mitocarta_path:
    candidates = list(repo_root.rglob("*mitocarta*.tsv")) + list(repo_root.rglob("*MitoCarta*.tsv"))
    mitocarta_path = str(candidates[0]) if candidates else None

if not genes4epilepsy_path:
    candidates = list(repo_root.rglob("*genes4epilepsy*.tsv")) + list(repo_root.rglob("*Genes4Epilepsy*.tsv"))
    genes4epilepsy_path = str(candidates[0]) if candidates else None

state = {
    "sample": {
        "sample_id": sample_id,
    },
    "run": {
        "run_id": run_id,
    },
    "artifacts": {
        "normalized_vcf": str(normalized_vcf),
    },
    "gene_sets": {
        "mitocarta_path": mitocarta_path,
        "genes4epilepsy_path": genes4epilepsy_path,
        "overlay_completed": False,
        "flags_added": [],
    },
    "annotations": {},
    "qc": {},
    "stage_outputs": {},
    "warnings": [],
}

paths = {
    "processed_dir": str(processed_dir),
}

logger = ProbeLogger()

print("[PYTHON][INFO] CONFIG_PATH=", config_path)
print("[PYTHON][INFO] NORMALIZED_VCF=", normalized_vcf)
print("[PYTHON][INFO] PROCESSED_DIR=", processed_dir)
print("[PYTHON][INFO] MITOCARTA_PATH=", mitocarta_path)
print("[PYTHON][INFO] GENES4EPILEPSY_PATH=", genes4epilepsy_path)

updated_state = run_stage(config=config, paths=paths, logger=logger, state=state)

print()
print("=== STAGE 07 RESULT SUMMARY ===")
print(json.dumps({
    "annotated_vcf": updated_state["artifacts"].get("annotated_vcf"),
    "annotated_table": updated_state["artifacts"].get("annotated_table"),
    "annotation_qc": updated_state["qc"].get("annotation_qc"),
    "stage_output": updated_state["stage_outputs"].get("stage_07_annotate_variants"),
    "warnings": updated_state.get("warnings", []),
}, indent=2))
PY
echo

echo "=== LIKELY OUTPUT FILES ==="
find "$REPO_ROOT/results" -type f \( -name "*.annotated_variants.vcf" -o -name "*.annotated_variants.tsv" \) | sort | tail -n 10 || true
echo

echo "[INFO] Mark Stage 07 checkpoint probe completed at $(date)"
echo "[INFO] Log file saved to: $LOG"