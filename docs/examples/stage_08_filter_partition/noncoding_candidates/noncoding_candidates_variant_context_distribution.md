# noncoding_candidates_variant_context_distribution.md

Pivot table of variant context distribution for noncoding variant candidates from HG002 run


## folder path:

`steelsparrow@pop-os:/mnt/storage/delme/stage_08_out_HG002_run$`



## bash cmd:

```bash
cut -f $(head -n1 noncoding_candidates.tsv | tr '\t' '\n' | nl | grep variant_context | awk '{print $1}') noncoding_candidates.tsv | sort | uniq -c | sort -nr | head > docs/examples/stage_08_filter_partition/noncoding_candidates/noncoding_candidates_variant_context_distribution.md
```



## output:

```text
2819766 intronic
1107793 intergenic
 587971 regulatory
  49108 noncoding_transcript
  44460 unknown
   3106 splice_region
      3 coding
      1 variant_context
```
