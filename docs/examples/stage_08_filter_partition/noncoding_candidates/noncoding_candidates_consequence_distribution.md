# noncoding_candidates_consequence_distribution.md

Pivot table view of consequence calls of noncoding_candiates.tsv run on HG002

## folder path:

`steelsparrow@pop-os:/mnt/storage/delme/stage_08_out_HG002_run$`


## bash cmd:

```bash
cut -f $(head -n1 noncoding_candidates.tsv | tr '\t' '\n' | nl | grep consequence | awk '{print $1}') noncoding_candidates.tsv | sort | uniq -c | sort -nr | head > docs/examples/stage_08_filter_partition/noncoding_candidates/noncoding_candidates_consequence_distribution.md
```


## pivot table of noncoding candidate consequence categories

```text
1612915 intron_variant
1194565 intron_variant&non_coding_transcript_variant
1107793 intergenic_variant
 305835 upstream_gene_variant
 282119 downstream_gene_variant
  48919 non_coding_transcript_exon_variant
  39307 3_prime_UTR_variant
   8531 intron_variant&NMD_transcript_variant
   5129 5_prime_UTR_variant
   2028 splice_polypyrimidine_tract_variant&intron_variant
```
