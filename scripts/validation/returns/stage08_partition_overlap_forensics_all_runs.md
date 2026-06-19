# Stage08 Partition Overlap Forensics: All Runs

Generated: 2026-06-18T00:48:50Z

Purpose:

```text
Test whether Stage08 partition overlap is consistently limited to coding ∩ splice
across 12 epilepsy WES runs and 1 HG002 WGS run.
```

## Compact Summary

| sample_id | run_id | depth | coding ∩ splice | coding ∩ noncoding | splice ∩ noncoding | any overlap |
|---|---|---|---:|---:|---:|---:|
| ERR10619203 | run_2026_05_30_071639 | q3 | 465 | 0 | 0 | 465 |
| ERR10619207 | run_2026_06_01_124134 | q3 | 493 | 0 | 0 | 493 |
| ERR10619208 | run_2026_05_30_151355 | median | 540 | 0 | 0 | 540 |
| ERR10619212 | run_2026_05_30_214724 | q1 | 541 | 0 | 0 | 541 |
| ERR10619225 | run_2026_05_31_091242 | q3 | 541 | 0 | 0 | 541 |
| ERR10619230 | run_2026_06_01_004903 | q3 | 497 | 0 | 0 | 497 |
| ERR10619241 | run_2026_06_02_052302 | q1 | 495 | 0 | 0 | 495 |
| ERR10619281 | run_2026_05_27_233524 | median | 547 | 0 | 0 | 547 |
| ERR10619285 | run_2026_06_02_124300 | median | 518 | 0 | 0 | 518 |
| ERR10619300 | run_2026_05_27_172531 | median | 493 | 0 | 0 | 493 |
| ERR10619309 | run_2026_06_02_181024 | q1 | 486 | 0 | 0 | 486 |
| ERR10619330 | run_2026_06_01_203130 | q1 | 490 | 0 | 0 | 490 |
| hg002 | run_2026_06_03_010030 | hg002 | 525 | 0 | 0 | 525 |

## Aggregate Overlap Counts

| Intersection | Total distinct overlap observations across runs |
|---|---:|
| coding ∩ splice | 6631 |
| coding ∩ noncoding | 0 |
| splice ∩ noncoding | 0 |
| any overlap | 6631 |

## Detailed Characterization Per Run

### ERR10619203 / run_2026_05_30_071639 / q3

#### coding ∩ splice: variant_context
```text
465	splice_region
```

#### coding ∩ splice: consequence
```text
227	splice_region_variant&synonymous_variant
219	missense_variant&splice_region_variant
10	frameshift_variant&splice_region_variant
2	start_lost&splice_region_variant
2	inframe_deletion&splice_region_variant
1	stop_lost&splice_region_variant
1	splice_donor_variant&stop_gained&frameshift_variant
1	splice_acceptor_variant&frameshift_variant
1	inframe_insertion&splice_region_variant
1	frameshift_variant&splice_region_variant&intron_variant
```

#### coding ∩ splice: impact_class
```text
227	LOW
222	MODERATE
16	HIGH
```

#### coding ∩ noncoding preview
```text
```

#### splice ∩ noncoding preview
```text
```

### ERR10619207 / run_2026_06_01_124134 / q3

#### coding ∩ splice: variant_context
```text
493	splice_region
```

#### coding ∩ splice: consequence
```text
243	missense_variant&splice_region_variant
237	splice_region_variant&synonymous_variant
6	frameshift_variant&splice_region_variant
2	stop_gained&splice_region_variant
1	start_lost&splice_region_variant
1	splice_donor_variant&stop_gained&frameshift_variant
1	splice_acceptor_variant&frameshift_variant
1	inframe_insertion&splice_region_variant
1	inframe_deletion&splice_region_variant
```

#### coding ∩ splice: impact_class
```text
245	MODERATE
237	LOW
11	HIGH
```

#### coding ∩ noncoding preview
```text
```

#### splice ∩ noncoding preview
```text
```

### ERR10619208 / run_2026_05_30_151355 / median

#### coding ∩ splice: variant_context
```text
540	splice_region
```

#### coding ∩ splice: consequence
```text
272	splice_region_variant&synonymous_variant
250	missense_variant&splice_region_variant
10	frameshift_variant&splice_region_variant
1	stop_lost&splice_region_variant
1	stop_gained&splice_region_variant
1	start_lost&splice_region_variant
1	splice_donor_variant&stop_gained&frameshift_variant
1	splice_acceptor_variant&frameshift_variant
1	inframe_insertion&splice_region_variant
1	inframe_deletion&splice_region_variant
1	frameshift_variant&splice_region_variant&intron_variant
```

#### coding ∩ splice: impact_class
```text
272	LOW
252	MODERATE
16	HIGH
```

#### coding ∩ noncoding preview
```text
```

#### splice ∩ noncoding preview
```text
```

### ERR10619212 / run_2026_05_30_214724 / q1

#### coding ∩ splice: variant_context
```text
541	splice_region
```

#### coding ∩ splice: consequence
```text
275	missense_variant&splice_region_variant
250	splice_region_variant&synonymous_variant
7	frameshift_variant&splice_region_variant
2	stop_gained&splice_region_variant
2	inframe_insertion&splice_region_variant
1	start_lost&splice_region_variant
1	splice_donor_variant&stop_gained&frameshift_variant
1	inframe_insertion&splice_region_variant&stop_retained_variant
1	inframe_deletion&splice_region_variant
1	frameshift_variant&splice_region_variant&intron_variant
```

#### coding ∩ splice: impact_class
```text
279	MODERATE
250	LOW
12	HIGH
```

#### coding ∩ noncoding preview
```text
```

#### splice ∩ noncoding preview
```text
```

### ERR10619225 / run_2026_05_31_091242 / q3

#### coding ∩ splice: variant_context
```text
541	splice_region
```

#### coding ∩ splice: consequence
```text
265	missense_variant&splice_region_variant
258	splice_region_variant&synonymous_variant
10	frameshift_variant&splice_region_variant
2	inframe_insertion&splice_region_variant
1	stop_lost&splice_region_variant
1	stop_gained&splice_region_variant
1	start_lost&splice_region_variant
1	splice_donor_variant&stop_gained&frameshift_variant
1	inframe_deletion&splice_region_variant
1	frameshift_variant&splice_region_variant&intron_variant
```

#### coding ∩ splice: impact_class
```text
268	MODERATE
258	LOW
15	HIGH
```

#### coding ∩ noncoding preview
```text
```

#### splice ∩ noncoding preview
```text
```

### ERR10619230 / run_2026_06_01_004903 / q3

#### coding ∩ splice: variant_context
```text
497	splice_region
```

#### coding ∩ splice: consequence
```text
250	splice_region_variant&synonymous_variant
234	missense_variant&splice_region_variant
6	frameshift_variant&splice_region_variant
1	stop_lost&splice_region_variant
1	stop_gained&splice_region_variant
1	start_lost&splice_region_variant
1	splice_donor_variant&stop_gained&frameshift_variant
1	inframe_insertion&splice_region_variant
1	inframe_deletion&splice_region_variant
1	frameshift_variant&splice_region_variant&intron_variant
```

#### coding ∩ splice: impact_class
```text
250	LOW
236	MODERATE
11	HIGH
```

#### coding ∩ noncoding preview
```text
```

#### splice ∩ noncoding preview
```text
```

### ERR10619241 / run_2026_06_02_052302 / q1

#### coding ∩ splice: variant_context
```text
495	splice_region
```

#### coding ∩ splice: consequence
```text
251	missense_variant&splice_region_variant
234	splice_region_variant&synonymous_variant
6	frameshift_variant&splice_region_variant
1	stop_lost&splice_region_variant
1	stop_gained&splice_region_variant
1	start_lost&splice_region_variant
1	splice_donor_variant&stop_gained&frameshift_variant
```

#### coding ∩ splice: impact_class
```text
251	MODERATE
234	LOW
10	HIGH
```

#### coding ∩ noncoding preview
```text
```

#### splice ∩ noncoding preview
```text
```

### ERR10619281 / run_2026_05_27_233524 / median

#### coding ∩ splice: variant_context
```text
547	splice_region
```

#### coding ∩ splice: consequence
```text
273	splice_region_variant&synonymous_variant
260	missense_variant&splice_region_variant
5	frameshift_variant&splice_region_variant
2	start_lost&splice_region_variant
1	stop_lost&splice_region_variant
1	stop_gained&splice_region_variant
1	splice_donor_variant&stop_gained&frameshift_variant
1	splice_acceptor_variant&frameshift_variant
1	inframe_insertion&splice_region_variant
1	inframe_deletion&splice_region_variant
1	frameshift_variant&stop_lost&splice_region_variant
```

#### coding ∩ splice: impact_class
```text
273	LOW
262	MODERATE
12	HIGH
```

#### coding ∩ noncoding preview
```text
```

#### splice ∩ noncoding preview
```text
```

### ERR10619285 / run_2026_06_02_124300 / median

#### coding ∩ splice: variant_context
```text
518	splice_region
```

#### coding ∩ splice: consequence
```text
256	missense_variant&splice_region_variant
253	splice_region_variant&synonymous_variant
4	frameshift_variant&splice_region_variant
2	start_lost&splice_region_variant
1	splice_donor_variant&stop_gained&frameshift_variant
1	splice_acceptor_variant&frameshift_variant
1	inframe_insertion&splice_region_variant
```

#### coding ∩ splice: impact_class
```text
257	MODERATE
253	LOW
8	HIGH
```

#### coding ∩ noncoding preview
```text
```

#### splice ∩ noncoding preview
```text
```

### ERR10619300 / run_2026_05_27_172531 / median

#### coding ∩ splice: variant_context
```text
493	splice_region
```

#### coding ∩ splice: consequence
```text
244	missense_variant&splice_region_variant
239	splice_region_variant&synonymous_variant
3	frameshift_variant&splice_region_variant
2	inframe_deletion&splice_region_variant
1	stop_gained&splice_region_variant
1	stop_gained&frameshift_variant&splice_region_variant
1	start_lost&splice_region_variant
1	splice_donor_variant&stop_gained&frameshift_variant
1	splice_acceptor_variant&frameshift_variant
```

#### coding ∩ splice: impact_class
```text
246	MODERATE
239	LOW
8	HIGH
```

#### coding ∩ noncoding preview
```text
```

#### splice ∩ noncoding preview
```text
```

### ERR10619309 / run_2026_06_02_181024 / q1

#### coding ∩ splice: variant_context
```text
486	splice_region
```

#### coding ∩ splice: consequence
```text
243	splice_region_variant&synonymous_variant
233	missense_variant&splice_region_variant
4	frameshift_variant&splice_region_variant
1	stop_lost&splice_region_variant
1	start_lost&splice_region_variant
1	splice_donor_variant&stop_gained&frameshift_variant
1	protein_altering_variant&splice_region_variant
1	inframe_deletion&splice_region_variant
1	frameshift_variant&splice_region_variant&intron_variant
```

#### coding ∩ splice: impact_class
```text
243	LOW
235	MODERATE
8	HIGH
```

#### coding ∩ noncoding preview
```text
```

#### splice ∩ noncoding preview
```text
```

### ERR10619330 / run_2026_06_01_203130 / q1

#### coding ∩ splice: variant_context
```text
490	splice_region
```

#### coding ∩ splice: consequence
```text
247	missense_variant&splice_region_variant
229	splice_region_variant&synonymous_variant
6	frameshift_variant&splice_region_variant
2	start_lost&splice_region_variant
1	stop_lost&splice_region_variant
1	stop_gained&splice_region_variant
1	splice_region_variant&synonymous_variant&NMD_transcript_variant
1	splice_donor_variant&stop_gained&frameshift_variant
1	splice_acceptor_variant&frameshift_variant
1	inframe_deletion&splice_region_variant
```

#### coding ∩ splice: impact_class
```text
248	MODERATE
230	LOW
12	HIGH
```

#### coding ∩ noncoding preview
```text
```

#### splice ∩ noncoding preview
```text
```

### hg002 / run_2026_06_03_010030 / hg002

#### coding ∩ splice: variant_context
```text
525	splice_region
```

#### coding ∩ splice: consequence
```text
259	splice_region_variant&synonymous_variant
249	missense_variant&splice_region_variant
6	frameshift_variant&splice_region_variant
2	stop_gained&splice_region_variant
2	inframe_insertion&splice_region_variant
2	inframe_deletion&splice_region_variant
1	start_lost&splice_region_variant
1	splice_region_variant&synonymous_variant&NMD_transcript_variant
1	splice_donor_variant&stop_gained&frameshift_variant
1	splice_acceptor_variant&frameshift_variant
1	frameshift_variant&splice_region_variant&intron_variant
```

#### coding ∩ splice: impact_class
```text
260	LOW
253	MODERATE
12	HIGH
```

#### coding ∩ noncoding preview
```text
```

#### splice ∩ noncoding preview
```text
```

