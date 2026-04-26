# rdgp_seed_overview.md

## folder path:

`steelsparrow@pop-os:/mnt/storage/delme/stage_08_out_HG002_run$`


## bash cmd:


```bash
cut -f1-9 stage_08_rdgp_gene_evidence_seed.tsv | head -n 6 | column -t -s $'\t' > docs/examples/rdgp_gene_evidence/rdgp_seed_overview.md
```

## output:


```text
sample_id  gene_id    gene_symbol  variant_count  high_impact_variant_count  rare_variant_count  pathogenic_variant_count  max_variant_severity  has_low_quality_evidence
HG002      10000      AKT3         274            0                          12                  0                         MODIFIER              False
HG002      100130890  TSTD3        64             0                          1                   0                         MODIFIER              False
HG002      100131187  TSTD1        1              0                          0                   0                         MODIFIER              False
HG002      100131390  SP9          8              0                          1                   0                         MODIFIER              True
HG002      100131801  PET100       34             0                          0                   0                         MODIFIER              False
```