# Implementation Plan — scripts/mark/build_gene_list_intersections.py

Used in cross-run case study contrast 2

# Objective

Generate a global append-ready:

```text
gene_list_overlay_intersections.new.tsv
```

from 13 completed VAP runs on MARK.

The output will be a complete per-run overlay gene matrix:

```text
13 runs × 1140 overlay genes = 14,820 rows
```

including genes with `variant_count = 0`.

---

# Inputs

Run from MARK VAP repo root.

Read:

```text
data/reference/gene_lists/epi25_vap_overlay_seed.tsv
data/reference/gene_lists/mitocarta_vap_overlay_seed.tsv
results/<run_id>/processed/stage_12_validation_candidates.tsv
results/<run_id>/metrics/stage_metrics_long.tsv
```

Use hardcoded 13-SRA manifest. Do not auto-discover runs.

This is the explicit hardcoded 13-SRA manifest:

```python
MANIFEST = [
    ("ERR10619203", "run_2026_05_30_071639", "q3"),
    ("ERR10619207", "run_2026_06_01_124134", "q3"),
    ("ERR10619208", "run_2026_05_30_151355", "median"),
    ("ERR10619212", "run_2026_05_30_214724", "q1"),
    ("ERR10619225", "run_2026_05_31_091242", "q3"),
    ("ERR10619230", "run_2026_06_01_004903", "q3"),
    ("ERR10619241", "run_2026_06_02_052302", "q1"),
    ("ERR10619281", "run_2026_05_27_233524", "median"),
    ("ERR10619285", "run_2026_06_02_124300", "median"),
    ("ERR10619300", "run_2026_05_27_172531", "median"),
    ("ERR10619309", "run_2026_06_02_181024", "q1"),
    ("ERR10619330", "run_2026_06_01_203130", "q1"),
    ("SRR12898354", "run_2026_06_03_010030", "hg002"),
]
```

---

# Output

Write to:

```text
/root/Desktop/gene_list_overlay_intersections/
├── gene_list_overlay_intersections.new.tsv
└── gene_list_overlay_intersections_build_audit.tsv
```

---

# Core Logic

Create a master overlay gene list by concatenating:

```text
7 EPI25 genes
1133 MitoCarta genes
```

using:

```text
gene_id = ensembl_gene_id
match_key = ensembl_gene_id
```

Overlay fields:

```text
overlay_source
overlay_source_count
overlay_source_list
mitocarta_hit
epi25_hit
```

Since lists have zero overlap, each gene should have:

```text
overlay_source_count = 1
```

EPI25 rows should use `overlay_source = epi25_all_epilepsy`.
MitoCarta rows should use `overlay_source = mitocarta`.

---

# Normalization Policy

The script should defensively normalize string fields before joins, comparisons, and grouping.

For identifier fields used in lookup logic:

```text
gene_id
ensembl_gene_id
variant_origin
```

apply:

```text
TRIM()
```

and lowercase where comparison semantics are case-insensitive.

For Ensembl gene IDs specifically:

```text
TRIM()
```

is required before matching, but output should preserve the canonical Ensembl-style value.

For `gene_symbol`:

```text
TRIM()
```

only.

Do not lowercase `gene_symbol`, because HGNC gene symbols are case-sensitive biological identifiers and should be preserved in canonical uppercase form.

The purpose of this policy is to prevent silent join failures caused by trailing whitespace or minor serialization drift in reference gene-list files.

---

# Per-Run Parsing

For each manifest run:

1. Read metadata from:

`results/<run_id>/metrics/stage_metrics_long.tsv`

using:

```text
metric_name == validation_candidates_rows
```

to obtain:

```text
assay_type
run_classification
```

Use HG002 fallback if needed:

```text
sample_id = SRR12898354 → assay_type = wgs, run_classification = hg002
```

2. Read candidate variants from:

`results/<run_id>/processed/stage_12_validation_candidates.tsv`

3. Count coding candidate variants by:

`gene_id`

using rows where:

```text
variant_origin == coding
gene_id is not empty
gene_symbol is not empty
```

`variant_origin` comparisons should use normalized lowercase trimmed values during filtering.

4. Left join those counts onto the full 1140-gene overlay list.

5. Fill absent counts with:

```text
variant_count = 0
```

Genes with `variant_count = 0` still participate in deterministic `gene_burden_rank` assignment.

6. Compute `gene_burden_rank` per run by:

```text
variant_count DESC
gene_symbol ASC
gene_id ASC
```

assigning sequential ranks:

```text
1..1140
```

`gene_burden_rank` is assigned as `row_number` after sorting `variant_count DESC`, `gene_symbol ASC`, `gene_id ASC`.
Tied `variant_count` values do not share rank values.

7. Final row order per run:

```text
mitocarta_hit ASC
gene_symbol ASC
gene_id ASC
```

This prevents unstable ordering if duplicate symbols ever appear.

---

# Output Columns

Exact order:

```text
sample_id
run_id
assay_type
run_classification
gene_id
gene_symbol
gene_burden_rank
variant_count
overlay_source
overlay_source_count
overlay_source_list
mitocarta_hit
epi25_hit
match_key
```

---

# Audit Columns

Per run:

```text
sample_id
run_id
depth_category
input_path
input_exists
metrics_path
metrics_exists
rows_scanned
coding_rows_scanned
eligible_gene_id_rows
overlay_genes_total
overlay_genes_with_variants
overlay_genes_zero_count
output_rows_written
status
```

Also include seed-level constants:

```text
epi25_unique_gene_ids
mitocarta_unique_gene_ids
master_overlay_gene_count
```

---

# Validation

Expected global output row count:

```text
14820
```

Quick checks:

```bash
wc -l /root/Desktop/gene_list_overlay_intersections/gene_list_overlay_intersections.new.tsv
```

Expected including header:

```text
14821
```

Per-run check:

```bash
awk -F'\t' '
NR>1 {count[$1 FS $2]++}
END {for (k in count) print k, count[k]}
' /root/Desktop/gene_list_overlay_intersections/gene_list_overlay_intersections.new.tsv | sort
```

Each run should report:

```text
1140
```

Zero-count check:

```bash
awk -F'\t' '
NR>1 && $8 == 0 {z[$1 FS $2]++}
END {for (k in z) print k, z[k]}
' /root/Desktop/gene_list_overlay_intersections/gene_list_overlay_intersections.new.tsv | sort
```

Final spot-check:

```bash
head /root/Desktop/gene_list_overlay_intersections/gene_list_overlay_intersections.new.tsv
column -t -s $'\t' /root/Desktop/gene_list_overlay_intersections/gene_list_overlay_intersections_build_audit.tsv | less -S
```