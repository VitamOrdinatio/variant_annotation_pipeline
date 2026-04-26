# variant_summary_frequency_distribution.md



## folder path:

`steelsparrow@pop-os:/mnt/storage/delme/stage_08_out_HG002_run$`



## bash cmd:


```bash
cut -f $(head -n1 stage_08_variant_summary.tsv | tr '\t' '\n' | nl | grep frequency_status | awk '{print $1}') stage_08_variant_summary.tsv | sort | uniq -c | sort -nr > docs/examples/variant_summary_frequency_distribution.md
```



## output:

```text
4230918 common
 158207 low_frequency
 129804 rare
 117655 missing
      1 frequency_status
```
