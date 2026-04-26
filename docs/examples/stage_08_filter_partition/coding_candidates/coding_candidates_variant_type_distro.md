# coding_candidates_variant_type_distro.md

Distribution of variant types in the coding candidates category for HG002 run


## folder path

`steelsparrow@pop-os:/mnt/storage/delme/stage_08_out_HG002_run$`

## bash cmd:

```bash
cut -f $(head -n1 coding_candidates.tsv | tr '\t' '\n' | nl | grep variant_type | awk '{print $1}') coding_candidates.tsv | sort | uniq -c > docs/examples/coding_candidates_variant_type_distro.md
```


## output:

```text
     11 complex
    432 deletion
      2 indel
    268 insertion
  23565 snv
      1 variant_type
```