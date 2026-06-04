#!/usr/bin/env bash
set -u

OUT="/root/Desktop/mark_probe_overlay_gene_coding_join_logic.txt"
REPO="$HOME/dev/portfolio_projects/variant_annotation_pipeline"

{
  echo "MARK overlay gene coding join logic probe"
  echo "Timestamp: $(date -Is)"
  echo

  cd "$REPO" || {
    echo "ERROR: could not cd to repo: $REPO"
    exit 1
  }

  echo "Repo: $(pwd)"
  echo "Git:"
  git log -1 --oneline
  echo

  echo "Python availability:"
  which python || true
  which python3 || true
  python3 --version || true
  echo

  echo "Venv python availability:"
  ls -lh .venv/bin/python 2>&1 || true
  .venv/bin/python --version 2>&1 || true
  echo

  PY=".venv/bin/python"
  if [[ ! -x "$PY" ]]; then
    PY="python3"
  fi

  echo "Using PY=$PY"
  echo

  "$PY" - <<'PY'
from pathlib import Path
import pandas as pd

epi = Path("data/reference/gene_lists/epi25_vap_overlay_seed.tsv")
mito = Path("data/reference/gene_lists/mitocarta_vap_overlay_seed.tsv")
cand = Path("results/run_2026_05_27_233524/processed/stage_12_validation_candidates.tsv")
metrics = Path("results/run_2026_05_27_233524/metrics/stage_metrics_long.tsv")

print("FILES")
for p in [epi, mito, cand, metrics]:
    print(p, "exists=", p.exists(), "size=", p.stat().st_size if p.exists() else "NA")
print()

print("SEED HEADERS RAW")
for label, p in [("epi25", epi), ("mitocarta", mito)]:
    df = pd.read_csv(p, sep="\t", dtype=str, nrows=5)
    print(label, list(df.columns))
    df.columns = [c.strip() for c in df.columns]
    print(label, "stripped", list(df.columns))
    print(df[["gene_id", "gene_symbol", "ensembl_gene_id"]].head(10).to_string(index=False))
    print("unique ensembl:", df["ensembl_gene_id"].dropna().astype(str).str.strip().nunique())
    print()

epi_df = pd.read_csv(epi, sep="\t", dtype=str)
epi_df.columns = [c.strip() for c in epi_df.columns]
mito_df = pd.read_csv(mito, sep="\t", dtype=str)
mito_df.columns = [c.strip() for c in mito_df.columns]

epi_ids = set(epi_df["ensembl_gene_id"].dropna().astype(str).str.strip())
mito_ids = set(mito_df["ensembl_gene_id"].dropna().astype(str).str.strip())
all_ids = epi_ids | mito_ids

print("KNOWN SEED ID EXAMPLES")
print("epi ids:", sorted(list(epi_ids))[:20])
print("mito ids:", sorted(list(mito_ids))[:20])
print("overlap ids:", sorted(list(epi_ids & mito_ids))[:20])
print()

print("CANDIDATE HEADER")
header = pd.read_csv(cand, sep="\t", dtype=str, nrows=0)
print(list(header.columns))
print()

usecols = ["sample_id", "run_id", "gene_id", "gene_symbol", "variant_origin", "clinical_evidence", "clinical_status"]
df = pd.read_csv(cand, sep="\t", dtype=str, usecols=usecols)

for c in usecols:
    df[c] = df[c].astype(str).str.strip()

print("CANDIDATE BASIC COUNTS")
print("rows:", len(df))
print("variant_origin value counts:")
print(df["variant_origin"].value_counts(dropna=False).head(20).to_string())
print()

coding = df[df["variant_origin"].str.lower() == "coding"].copy()
eligible = coding[(coding["gene_id"].notna()) & (coding["gene_id"] != "") & (coding["gene_symbol"].notna()) & (coding["gene_symbol"] != "")].copy()

print("coding rows:", len(coding))
print("eligible coding gene rows:", len(eligible))
print("candidate unique coding gene_ids:", eligible["gene_id"].nunique())
print("candidate gene_id examples:", sorted(eligible["gene_id"].dropna().unique().tolist())[:20])
print()

print("JOIN COUNTS BY GENE_ID")
print("eligible rows with epi25 gene_id:", eligible["gene_id"].isin(epi_ids).sum())
print("eligible rows with mitocarta gene_id:", eligible["gene_id"].isin(mito_ids).sum())
print("eligible rows with either gene_id:", eligible["gene_id"].isin(all_ids).sum())
print("unique epi25 matched genes:", eligible.loc[eligible["gene_id"].isin(epi_ids), "gene_id"].nunique())
print("unique mitocarta matched genes:", eligible.loc[eligible["gene_id"].isin(mito_ids), "gene_id"].nunique())
print()

print("JOIN COUNTS BY GENE_SYMBOL")
epi_symbols = set(epi_df["gene_symbol"].dropna().astype(str).str.strip())
mito_symbols = set(mito_df["gene_symbol"].dropna().astype(str).str.strip())
all_symbols = epi_symbols | mito_symbols
print("eligible rows with epi25 gene_symbol:", eligible["gene_symbol"].isin(epi_symbols).sum())
print("eligible rows with mitocarta gene_symbol:", eligible["gene_symbol"].isin(mito_symbols).sum())
print("eligible rows with either gene_symbol:", eligible["gene_symbol"].isin(all_symbols).sum())
print("unique epi25 matched symbols:", eligible.loc[eligible["gene_symbol"].isin(epi_symbols), "gene_symbol"].nunique())
print("unique mitocarta matched symbols:", eligible.loc[eligible["gene_symbol"].isin(mito_symbols), "gene_symbol"].nunique())
print()

print("TOP matched symbol examples")
print(
    eligible[eligible["gene_symbol"].isin(all_symbols)]
    .groupby(["gene_id", "gene_symbol"])
    .size()
    .reset_index(name="n")
    .sort_values("n", ascending=False)
    .head(30)
    .to_string(index=False)
)
print()

print("stage_metrics validation metadata")
md = pd.read_csv(metrics, sep="\t", dtype=str)
print(md.loc[md["metric_name"] == "validation_candidates_rows", ["sample_id","run_id","assay_type","run_classification","metric_value"]].to_string(index=False))
PY

} > "$OUT" 2>&1

echo "Wrote: $OUT"
