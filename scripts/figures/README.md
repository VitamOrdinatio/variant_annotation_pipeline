# README.md

These scripts are used to generated figures and tables in a transparent and deterministic fashion for select case studies using TSV artifacts generated directly from VAP end-to-end operation.

---

# Quickstart

From repo root:

---

## F1: Provenance-Aware Reproducibility Transition

```bash
python scripts/figures/generate_case_study_f1_reproducibility_summary.py --config scripts/configs/err10619300_f1.yaml
python scripts/figures/generate_case_study_f1_reproducibility_summary.py --config scripts/configs/err10619281_f1.yaml
python scripts/figures/generate_case_study_f1_reproducibility_summary.py --config scripts/configs/hg002_f1.yaml
```

---

## F2: Runtime Observability Profile

```bash
python scripts/figures/generate_case_study_f2_runtime_observability_profile.py --config scripts/configs/err10619300_f2.yaml
python scripts/figures/generate_case_study_f2_runtime_observability_profile.py --config scripts/configs/err10619281_f2.yaml
python scripts/figures/generate_case_study_f2_runtime_observability_profile.py --config scripts/configs/hg002_f2.yaml
```

---