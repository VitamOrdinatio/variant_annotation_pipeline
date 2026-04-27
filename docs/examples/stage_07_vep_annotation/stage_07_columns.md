# stage_07_columns.md

## folder path:

`steelsparrow@pop-os:/mnt/storage/delme/stage_07_out_HG002_run/`



## bash cmd:

```bash
TSV="HG002_run_2026_04_17_082417.annotated_variants.tsv"
OUTDIR="docs/examples/stage_07_vep_annotation"
head -n 1 "$TSV" | tr '\t' '\n' | nl -w1 -s $'\t' > "$OUTDIR/stage_07_columns.tsv"
head -n 1 "$TSV" | tr '\t' '\n' | nl -w1 -s $'\t' > "$OUTDIR/stage_07_columns.md"
```



## output:

```text
1	sample_id
2	run_id
3	source_pipeline
4	variant_id
5	chromosome
6	position
7	reference_allele
8	alternate_allele
9	quality_flag
10	gene_id
11	gene_symbol
12	transcript_id
13	consequence
14	impact_class
15	impact
16	variant_class
17	variant_type
18	clinical_significance
19	clinvar_significance
20	population_frequency
21	gnomad_af
22	exac_af
23	thousand_genomes_af
24	mito_flag
25	epilepsy_flag
```