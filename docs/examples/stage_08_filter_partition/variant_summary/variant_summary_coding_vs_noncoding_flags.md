# variant_summary_coding_vs_noncoding_flags.md

The vast majority of detected variant candidates are noncoding variant candidates.


## folder path:

`steelsparrow@pop-os:/mnt/storage/delme/stage_08_out_HG002_run$`



## bash cmd:

```bash
awk -F'\t' 'NR==1 {for(i=1;i<=NF;i++) if($i=="coding_flag") col=i} NR>1 {print $col}' stage_08_variant_summary.tsv | sort | uniq -c > docs/examples/stage_08_filter_partition/variant_summary/variant_summary_coding_vs_noncoding_flags.md
```


## output:

```
4612306 False
  24278 True
```