#!/usr/bin/env bash
set -u

OUT="/root/Desktop/mark_probe_overlay_gene_coding_paths.txt"
REPO="$HOME/dev/portfolio_projects/variant_annotation_pipeline"

{
  echo "MARK overlay gene coding path probe"
  echo "Timestamp: $(date -Is)"
  echo
  echo "Working from: $(pwd)"
  echo "Repo target: $REPO"
  echo

  cd "$REPO" || {
    echo "ERROR: could not cd to repo: $REPO"
    exit 1
  }

  echo "Now in repo: $(pwd)"
  echo
  echo "Git status:"
  git status --short
  echo
  echo "Latest commit:"
  git log -1 --oneline
  echo

  echo "Python:"
  which python
  python --version
  echo

  echo "DuckDB import check:"
  python - <<'PY'
try:
    import duckdb
    print("duckdb OK", duckdb.__version__)
except Exception as e:
    print("duckdb ERROR", repr(e))
try:
    import pandas as pd
    print("pandas OK", pd.__version__)
except Exception as e:
    print("pandas ERROR", repr(e))
PY
  echo

  echo "Script presence:"
  ls -lh scripts/mark/build_overlay_gene_coding_views.py 2>&1
  echo

  echo "Seed files:"
  ls -lh data/reference/gene_lists/epi25_vap_overlay_seed.tsv 2>&1
  ls -lh data/reference/gene_lists/mitocarta_vap_overlay_seed.tsv 2>&1
  echo

  echo "Seed headers:"
  head -n 1 data/reference/gene_lists/epi25_vap_overlay_seed.tsv 2>&1
  head -n 1 data/reference/gene_lists/mitocarta_vap_overlay_seed.tsv 2>&1
  echo

  echo "Check expected input path layouts for ERR10619281:"
  for p in \
    "results/processed/run_2026_05_27_233524/processed/stage_12_validation_candidates.tsv" \
    "results/run_2026_05_27_233524/processed/stage_12_validation_candidates.tsv"
  do
    echo
    echo "PATH: $p"
    if [[ -f "$p" ]]; then
      echo "EXISTS"
      ls -lh "$p"
      echo "HEADER:"
      head -n 1 "$p"
      echo "FIRST DATA ROW sample/run/gene-ish columns:"
      awk -F'\t' 'NR==2 {print "sample_id="$1, "run_id="$2, "gene_id="$12, "gene_symbol="$13, "variant_origin="$44, "clinical_evidence="$36, "clinical_status="$33; exit}' "$p"
    else
      echo "MISSING"
    fi
  done

  echo
  echo "Check expected metrics path layouts for ERR10619281:"
  for p in \
    "results/processed/run_2026_05_27_233524/metrics/stage_metrics_long.tsv" \
    "results/run_2026_05_27_233524/metrics/stage_metrics_long.tsv"
  do
    echo
    echo "PATH: $p"
    if [[ -f "$p" ]]; then
      echo "EXISTS"
      ls -lh "$p"
      echo "HEADER:"
      head -n 1 "$p"
      echo "validation_candidates_rows:"
      awk -F'\t' 'NR==1 {for(i=1;i<=NF;i++) h[$i]=i; next} $h["metric_name"]=="validation_candidates_rows" {print; exit}' "$p"
    else
      echo "MISSING"
    fi
  done

  echo
  echo "Available run dirs under results:"
  find results -maxdepth 2 -type d -name 'run_2026_*' | sort

  echo
  echo "Existing output dir:"
  ls -lh /root/Desktop/overlay_gene_coding 2>&1

} > "$OUT" 2>&1

echo "Wrote: $OUT"
