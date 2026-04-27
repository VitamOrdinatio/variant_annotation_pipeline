# coding_candidates_consequence_distribution.md

Pivot table view of consequence calls of coding_candiates.tsv run on HG002


## folder path:

`steelsparrow@pop-os:/mnt/storage/delme/stage_08_out_HG002_run$ `


## cmd to gen pivot table:

```bash
cut -f $(head -n1 coding_candidates.tsv | tr '\t' '\n' | nl | grep consequence | awk '{print $1}') coding_candidates.tsv | sort | uniq -c | sort -nr | head > docs/examples/stage_08_filter_partition/coding_candidates/coding_candidates_consequence_distribution.md
```


## pivot table of coding candidate consequence categories
```text    
  11600 synonymous_variant
  11321 missense_variant
    310 frameshift_variant
    259 splice_region_variant&synonymous_variant
    249 missense_variant&splice_region_variant
    202 inframe_deletion
    158 inframe_insertion
     99 stop_gained
     24 stop_lost
     10 start_lost
```