#!/usr/bin/env bash
set -u

OUT="/root/Desktop/vap_sra_runid_probe_$(date -u +%Y%m%dT%H%M%SZ).txt"
REPO="/root/dev/portfolio_projects/variant_annotation_pipeline"

{
echo "===== VAP Saudi RunID Probe ====="
echo "UTC timestamp: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo "Host: $(hostname)"
echo

if [ ! -d "$REPO" ]; then
  echo "ERROR: Repo directory not found: $REPO"
  echo "Expected VAP repo root at: $REPO"
  exit 1
fi

cd "$REPO" || exit 1

echo "===== Repository Context ====="
echo "PWD: $(pwd)"
echo "Git branch: $(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo UNKNOWN)"
echo "Git commit: $(git rev-parse HEAD 2>/dev/null || echo UNKNOWN)"
echo

echo "===== Candidate Saudi Run Directories ====="
TMP_RUNS="$(mktemp)"
{
  grep -RIl "ERR10619281\|ERR10619300" results/run_*/metadata/run_metadata.json 2>/dev/null | sed 's#/metadata/run_metadata.json##'
  grep -RIl "ERR10619281\|ERR10619300" results/run_*/logs/pipeline.log 2>/dev/null | sed 's#/logs/pipeline.log##'
} | sort -u > "$TMP_RUNS"

if [ ! -s "$TMP_RUNS" ]; then
  echo "No candidate run directories found for ERR10619281 or ERR10619300."
else
  cat "$TMP_RUNS"
fi

echo

echo "===== Per-Run Metadata Summary ====="
while IFS= read -r d; do
  [ -z "$d" ] && continue
  echo "--- $d ---"
  if [ -f "$d/metadata/run_metadata.json" ]; then
    python - "$d/metadata/run_metadata.json" <<'PY'
import json, sys
from pathlib import Path
p = Path(sys.argv[1])
try:
    data = json.loads(p.read_text())
except Exception as e:
    print(f"ERROR reading {p}: {e}")
    sys.exit(0)
keys = [
    "run_id", "sample_id", "sra_accession", "assay_type", "execution_mode",
    "status", "run_status", "start_time", "end_time", "runtime_seconds",
    "total_runtime_seconds", "git_commit", "config_path"
]
for k in keys:
    if k in data:
        print(f"{k}: {data.get(k)}")
# also search nested dicts one level deep for common sample/provenance fields
for parent in ["sample", "input", "provenance", "config", "execution_profile"]:
    v = data.get(parent)
    if isinstance(v, dict):
        for k in ["sample_id", "sra_accession", "assay_type", "bioproject_accession", "allow_non_hg002"]:
            if k in v:
                print(f"{parent}.{k}: {v.get(k)}")
PY
  else
    echo "run_metadata.json: MISSING"
  fi
  if [ -f "$d/logs/pipeline.log" ]; then
    echo "pipeline.log: PRESENT"
    echo "log sample lines:"
    grep -E "Run ID:|Sample ID:|SRA accession:|FASTQ R1 reads detected:|FASTQ R2 reads detected:|Stage 11|Stage 12|Pipeline run failed|Run status:|Pipeline execution complete" "$d/logs/pipeline.log" | tail -n 30 || true
  else
    echo "pipeline.log: MISSING"
  fi
  echo
done < "$TMP_RUNS"

rm -f "$TMP_RUNS"

echo "===== Desktop Output ====="
echo "$OUT"
} > "$OUT" 2>&1

echo "Probe complete. Output written to: $OUT"
