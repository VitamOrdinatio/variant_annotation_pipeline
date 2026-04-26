# noncoding_candidates_variant_type_distro.md

Distribution of variant types in the noncoding candidates category for HG002 run

## folder path:

`steelsparrow@pop-os:/mnt/storage/delme/stage_08_out_HG002_run$`


## bash cmd:

```bash
cut -f $(head -n1 noncoding_candidates.tsv | tr '\t' '\n' | nl | grep variant_type | awk '{print $1}') noncoding_candidates.tsv | sort | uniq -c > docs/examples/noncoding_candidates_variant_type_distro.md
```


## output:

```text
  25261 complex
 348412 deletion
   3014 indel
 318938 insertion
3916582 snv
      1 variant_type
```
