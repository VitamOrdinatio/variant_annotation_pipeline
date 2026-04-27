# noncoding_candidates_interpretability.md

Most noncoding variant candidates should have an interpretability value of "needs_external_annotation" due to their frontier status.

## folder path:

`steelsparrow@pop-os:/mnt/storage/delme/stage_08_out_HG002_run$`



## bash cmd:

```bash
cut -f $(head -n1 noncoding_candidates.tsv | tr '\t' '\n' | nl | grep interpretability_status | awk '{print $1}') noncoding_candidates.tsv | sort | uniq -c > docs/examples/stage_08_filter_partition/noncoding_candidates/noncoding_candidates_interpretability.md
```


## output:

```text
      1 interpretability_status
   3109 interpretable_now
4564638 needs_external_annotation
  44460 unsupported_currently
```
