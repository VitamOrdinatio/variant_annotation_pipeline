# rdgp_seed_overview.md

## folder path:

`steelsparrow@pop-os:/mnt/storage/delme/stage_08_out_HG002_run$`


## bash cmd:


```bash
cut -f1-9 stage_08_rdgp_gene_evidence_seed.tsv | head -n 6 | column -t -s $'\t' > docs/examples/stage_08_filter_partition/rdgp_gene_evidence/rdgp_seed_overview.md
```

## output:


```text
sample_id  gene_id          gene_symbol  variant_count  high_impact_variant_count  rare_variant_count  pathogenic_variant_count  max_variant_severity  has_low_quality_evidence
HG002      ENSG00000000003  TSPAN6       4              0                          1                   0                         MODIFIER              True
HG002      ENSG00000000005  TNMD         11             0                          0                   0                         MODIFIER              True
HG002      ENSG00000000419  DPM1         5              0                          0                   0                         MODIFIER              False
HG002      ENSG00000000457  SCYL3        102            0                          1                   0                         LOW                   False
HG002      ENSG00000000460  FIRRM        375            0                          2                   0                         MODERATE              True
```