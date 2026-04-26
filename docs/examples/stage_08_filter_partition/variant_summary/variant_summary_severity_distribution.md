# variant_summary_severity_distribution.md



## folder path:

`steelsparrow@pop-os:/mnt/storage/delme/stage_08_out_HG002_run$`



## bash cmd:

```bash
cut -f $(head -n1 stage_08_variant_summary.tsv | tr '\t' '\n' | nl | grep highest_impact | awk '{print $1}') stage_08_variant_summary.tsv | sort | uniq -c | sort -nr > docs/examples/variant_summary_severity_distribution.md
```


## output:

```text
4605322 MODIFIER
  18525 LOW
  11946 MODERATE
    791 HIGH
      1 highest_impact
```
