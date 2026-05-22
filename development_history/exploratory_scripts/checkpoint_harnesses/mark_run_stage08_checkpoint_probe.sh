#!/usr/bin/env bash
set -euo pipefail

TS="$(date +%Y%m%d_%H%M%S)"
LOG="/root/Desktop/mark_run_stage08_checkpoint_probe_${TS}.log"
REPO_ROOT="$HOME/dev/portfolio_projects/variant_annotation_pipeline"
CONFIG_PATH="$REPO_ROOT/config/config.mark.local.yaml"

exec > >(tee "$LOG") 2>&1

echo "[INFO] Mark Stage 08 checkpoint probe started at $(date)"
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
git status --short || true
echo

echo "=== STAGE 07 OUTPUT DISCOVERY ==="
ANNOTATED_TSV="$(find "$REPO_ROOT/results" -type f -name "*.annotated_variants.tsv" | sort | tail -n 1 || true)"
ANNOTATED_VCF="$(find "$REPO_ROOT/results" -type f -name "*.annotated_variants.vcf" | sort | tail -n 1 || true)"

if [[ -z "${ANNOTATED_TSV:-}" ]]; then
  echo "[ERROR] No annotated TSV found under $REPO_ROOT/results"
  exit 1
fi

if [[ -z "${ANNOTATED_VCF:-}" ]]; then
  echo "[ERROR] No annotated VCF found under $REPO_ROOT/results"
  exit 1
fi

echo "[INFO] ANNOTATED_TSV=$ANNOTATED_TSV"
echo "[INFO] ANNOTATED_VCF=$ANNOTATED_VCF"
ls -lh "$ANNOTATED_TSV" "$ANNOTATED_VCF"
echo

echo "=== PYTHON STAGE 08 PROBE ==="
python - <<'PY'
import json
from pathlib import Path
import yaml

from pipeline.stage_08_filter_and_partition import run_stage

class ProbeLogger:
    def info(self, msg): print(f"[LOGGER][INFO] {msg}")
    def warning(self, msg): print(f"[LOGGER][WARN] {msg}")
    def error(self, msg): print(f"[LOGGER][ERROR] {msg}")

repo_root = Path("/root/dev/portfolio_projects/variant_annotation_pipeline")
config_path = repo_root / "config" / "config.mark.local.yaml"

with config_path.open("r", encoding="utf-8") as fh:
    config = yaml.safe_load(fh)

annotated_tsvs = sorted((repo_root / "results").rglob("*.annotated_variants.tsv"))
annotated_vcfs = sorted((repo_root / "results").rglob("*.annotated_variants.vcf"))

if not annotated_tsvs:
    raise SystemExit("No annotated TSV found")
if not annotated_vcfs:
    raise SystemExit("No annotated VCF found")

annotated_tsv = annotated_tsvs[-1]
annotated_vcf = annotated_vcfs[-1]

run_dir = annotated_tsv.parent.parent
processed_dir = run_dir / "processed"

state = {
    "artifacts": {
        "annotated_table": str(annotated_tsv),
        "annotated_vcf": str(annotated_vcf),
    },
    "annotations": {
        "annotation_source": "VEP",
        "annotation_version": "115",
    },
    "run": {
        "tool_versions": {
            "vep": "115",
        },
    },
    "qc": {},
    "stage_outputs": {},
    "warnings": [],
}

paths = {
    "processed_dir": str(processed_dir),
}

logger = ProbeLogger()

print("[PYTHON][INFO] CONFIG_PATH=", config_path)
print("[PYTHON][INFO] ANNOTATED_TSV=", annotated_tsv)
print("[PYTHON][INFO] ANNOTATED_VCF=", annotated_vcf)
print("[PYTHON][INFO] PROCESSED_DIR=", processed_dir)

updated_state = run_stage(config=config, paths=paths, logger=logger, state=state)

print()
print("=== STAGE 08 RESULT SUMMARY ===")
print(json.dumps({
    "stage_08_qc": updated_state["qc"].get("stage_08_qc"),
    "stage_output": updated_state["stage_outputs"].get("stage_08_filter_and_partition"),
    "artifacts": {
        key: value for key, value in updated_state["artifacts"].items()
        if key.startswith("stage_08") or key in {
            "coding_candidates",
            "splice_region_candidates",
            "noncoding_candidates",
            "qc_flagged",
        }
    },
    "warnings": updated_state.get("warnings", []),
}, indent=2))
PY
echo

echo "=== STAGE 08 OUTPUT FILES ==="
find "$REPO_ROOT/results" -type f \( \
  -name "stage_08_selected_transcript_consequences.tsv" -o \
  -name "stage_08_variant_summary.tsv" -o \
  -name "coding_candidates.tsv" -o \
  -name "splice_region_candidates.tsv" -o \
  -name "noncoding_candidates.tsv" -o \
  -name "qc_flagged.tsv" -o \
  -name "stage_08_summary.json" -o \
  -name "stage_08_vdb_ready_variants.tsv" -o \
  -name "stage_08_rdgp_gene_evidence_seed.tsv" \
\) -exec ls -lh {} \; | sort
echo

echo "=== SUMMARY JSON HEAD ==="
SUMMARY_JSON="$(find "$REPO_ROOT/results" -type f -name "stage_08_summary.json" | sort | tail -n 1 || true)"
if [[ -n "${SUMMARY_JSON:-}" ]]; then
  echo "[INFO] SUMMARY_JSON=$SUMMARY_JSON"
  head -n 80 "$SUMMARY_JSON" || true
else
  echo "[WARN] No stage_08_summary.json found."
fi
echo

echo "[INFO] Mark Stage 08 checkpoint probe completed at $(date)"
echo "[INFO] Log file saved to: $LOG"