# stage_07_vep_warning_excerpt

## Source

- Source file: `/mnt/storage/vap_runs/HG002/run_2026_04_17_082417/raw_mark_outputs/processed/HG002_run_2026_04_17_082417.annotated_variants.vcf_warnings.txt`
- Run ID: `run_2026_04_17_082417`
- Sample/Dataset: `HG002`

## Method

Artifacts are generated using a config-driven extraction system ("Artificer") and curated for clarity.

## Output

```text
WARNING: line 4596360 skipped (KI270729.1 203 . CTCCAT C,CTCCATTCCAT 316.02 ....): Chromosome KI270729.1 not found in annotation sources or synonyms; chromosome KI270729.1 does not overlap any features
WARNING: line 4596361 skipped (KI270729.1 326 . G T 345.05 . AC=2;AF=1.00;AN=...): Chromosome KI270729.1 not found in annotation sources or synonyms; chromosome KI270729.1 does not overlap any features
WARNING: line 4596362 skipped (KI270729.1 353 . G T 1461.06 . AC=2;AF=1.00;AN...): Chromosome KI270729.1 not found in annotation sources or synonyms; chromosome KI270729.1 does not overlap any features
WARNING: line 4596363 skipped (KI270729.1 356 . C A 51.64 . AC=1;AF=0.500;AN=...): Chromosome KI270729.1 not found in annotation sources or synonyms; chromosome KI270729.1 does not overlap any features
WARNING: line 4596364 skipped (KI270729.1 359 . T A 52.64 . AC=1;AF=0.500;AN=...): Chromosome KI270729.1 not found in annotation sources or synonyms; chromosome KI270729.1 does not overlap any features
WARNING: line 4596365 skipped (KI270729.1 362 . A T 1154.31 . AC=2;AF=1.00;AN...): Chromosome KI270729.1 not found in annotation sources or synonyms; chromosome KI270729.1 does not overlap any features
WARNING: line 4596366 skipped (KI270729.1 363 . T G 1336.06 . AC=2;AF=1.00;AN...): Chromosome KI270729.1 not found in annotation sources or synonyms; chromosome KI270729.1 does not overlap any features
WARNING: line 4596367 skipped (KI270729.1 365 . C A 1336.06 . AC=2;AF=1.00;AN...): Chromosome KI270729.1 not found in annotation sources or synonyms; chromosome KI270729.1 does not overlap any features
WARNING: line 4596368 skipped (KI270729.1 372 . G A 1066.06 . AC=2;AF=1.00;AN...): Chromosome KI270729.1 not found in annotation sources or synonyms; chromosome KI270729.1 does not overlap any features
WARNING: line 4596369 skipped (KI270729.1 410 . G C 78.32 . AC=2;AF=1.00;AN=2...): Chromosome KI270729.1 not found in annotation sources or synonyms; chromosome KI270729.1 does not overlap any features
```

## Interpretation

Warnings indicate variants located on contigs not present in annotation sources.

These represent:

- alternate or decoy contigs  
- regions not covered by standard gene annotations  

This is expected behavior in large-scale annotation and does not impact core genome interpretation.

## Notes

- No additional notes.

## Limitations

- Excerpt or summary only.
- Not the full dataset unless explicitly stated.
- No new inference performed.
