#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import pandas as pd


SRC_DIR = Path("docs/case_studies/cross_runs/cross_run_tables")
DEST_DIR = Path("docs/case_studies/hg002/tables")
AUDIT_OUT = DEST_DIR / "hg002_table_subset_audit.tsv"

HG002_SAMPLE_IDS = {"HG002", "SRR12898354"}


def main() -> None:
    DEST_DIR.mkdir(parents=True, exist_ok=True)

    audit = []

    for src in sorted(SRC_DIR.glob("*.tsv")):
        dst = DEST_DIR / src.name

        try:
            df = pd.read_csv(src, sep="\t", dtype=str)

            if "sample_id" not in df.columns:
                audit.append({
                    "source_file": src.name,
                    "status": "skipped_no_sample_id",
                    "rows_in": len(df),
                    "rows_written": 0,
                    "destination": "",
                })
                continue

            sample = df["sample_id"].astype(str).str.strip()
            sub = df[sample.isin(HG002_SAMPLE_IDS)].copy()

            if sub.empty:
                audit.append({
                    "source_file": src.name,
                    "status": "skipped_no_hg002_records",
                    "rows_in": len(df),
                    "rows_written": 0,
                    "destination": "",
                })
                continue

            sub.to_csv(dst, sep="\t", index=False)

            audit.append({
                "source_file": src.name,
                "status": "subset_written",
                "rows_in": len(df),
                "rows_written": len(sub),
                "destination": str(dst),
            })

        except Exception as exc:
            audit.append({
                "source_file": src.name,
                "status": "error",
                "rows_in": "NA",
                "rows_written": 0,
                "destination": "",
                "error": f"{type(exc).__name__}: {exc}",
            })

    pd.DataFrame(audit).to_csv(AUDIT_OUT, sep="\t", index=False)

    print(f"Wrote audit: {AUDIT_OUT}")
    print(pd.DataFrame(audit)["status"].value_counts().to_string())


if __name__ == "__main__":
    main()
