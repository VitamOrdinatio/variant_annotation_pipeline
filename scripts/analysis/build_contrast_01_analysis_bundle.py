#!/usr/bin/env python3
import shutil
import tarfile
import pandas as pd
from pathlib import Path

SRC = Path("docs/case_studies/cross_runs/contrasts/contrast_01_inputs")
DEST = Path("docs/case_studies/cross_runs/contrasts/contrast_01_analysis_bundle")
TAR_PATH = DEST.with_suffix(".tar.gz")

ROOT_FILES = [
    "cohort_manifest.tsv",
    "contrast_01_input_build_audit.tsv",
    "README.md",
]

TABLE_FILES = [
    "stage_funnel_summary.tsv",
    "priority_tier_summary.tsv",
    "interpretation_label_summary.tsv",
]

LANE_FILES = [
    "{sra}_bucket_1a_validation_routed_epilepsy_mito.tsv",
    "{sra}_bucket_1b_clinically_contextualized_epilepsy_mito.tsv",
    "{sra}_bucket_2a_rare_impact_coding_triage_summary.tsv",
    "{sra}_bucket_2b_rare_impact_tier2.tsv",
    "{sra}_bucket_2c_rare_impact_deprioritized.tsv",
]

VALUE_COUNT_FILES = [
    "value_counts__priority_tier.tsv",
    "value_counts__coding_interpretation_label.tsv",
    "value_counts__source_interpretation_label.tsv",
    "value_counts__consequence.tsv",
    "value_counts__variant_class.tsv",
    "value_counts__clinical_significance.tsv",
    "value_counts__clinvar_significance.tsv",
]

audit = []

def copy_required(src, dst):
    if not src.exists():
        raise SystemExit(f"Missing required file: {src}")
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    audit.append({"status": "copied", "src": str(src), "dst": str(dst)})

def copy_optional(src, dst):
    if src.exists():
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        audit.append({"status": "copied_optional", "src": str(src), "dst": str(dst)})
    else:
        audit.append({"status": "missing_optional", "src": str(src), "dst": str(dst)})

if DEST.exists():
    raise SystemExit(f"Destination already exists. Remove it manually if you want to rebuild: {DEST}")

DEST.mkdir(parents=True)

for fname in ROOT_FILES:
    copy_required(SRC / fname, DEST / fname)

manifest = pd.read_csv(SRC / "cohort_manifest.tsv", sep="\t", dtype=str)

for sra in manifest["SRA_accn"]:
    src_sra = SRC / sra
    dst_sra = DEST / sra

    for fname in TABLE_FILES:
        copy_required(src_sra / "tables" / fname, dst_sra / "tables" / fname)

    copy_required(
        src_sra / "figures" / f"{sra}_f3a_deterministic_evidence_lineage.png",
        dst_sra / "figures" / f"{sra}_f3a_deterministic_evidence_lineage.png",
    )

    copy_required(
        src_sra / "figures" / f"{sra}_f3b_semantic_branching.png",
        dst_sra / "figures" / f"{sra}_f3b_semantic_branching.png",
    )

    for pattern in LANE_FILES:
        fname = pattern.format(sra=sra)
        copy_required(
            src_sra / "sql_outputs" / "lane_candidate_slices" / fname,
            dst_sra / "sql_outputs" / "lane_candidate_slices" / fname,
        )

    for fname in VALUE_COUNT_FILES:
        copy_required(
            src_sra / "sql_outputs" / "value_counts" / fname,
            dst_sra / "sql_outputs" / "value_counts" / fname,
        )

# Hero figures: copy if already present in contrast_01_inputs/hero_figures.
copy_optional(
    SRC / "hero_figures" / "ERR10619281_hero_semantic_stability_architecture.png",
    DEST / "hero_figures" / "ERR10619281_hero_semantic_stability_architecture.png",
)

copy_optional(
    SRC / "hero_figures" / "ERR10619300_hero_semantic_refinery.png",
    DEST / "hero_figures" / "ERR10619300_hero_semantic_refinery.png",
)

audit_path = DEST / "contrast_01_analysis_bundle_build_audit.tsv"
pd.DataFrame(audit).to_csv(audit_path, sep="\t", index=False)

with tarfile.open(TAR_PATH, "w:gz") as tar:
    tar.add(DEST, arcname=DEST.name)

print(f"Wrote bundle directory: {DEST}")
print(f"Wrote archive: {TAR_PATH}")
print(f"Wrote audit: {audit_path}")
