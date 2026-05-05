# Stage 04 — Alignment QC Report (VAP)

## Overview

Stage 04 performs **quality control on aligned sequencing reads** following BAM generation.

This stage verifies that upstream alignment is successful and that the dataset is suitable for downstream variant calling.

---

## Dataset

- Sample: HG002 (GIAB benchmark genome)  
- Run ID: run_2026_04_17_082417  
- Input BAM: results/run_2026_04_17_082417/interim/HG002_run_2026_04_17_082417.aligned.sorted.bam  

---

## Key Metrics

| Metric | Value |
|------|------|
| Total reads | 428,652,999 |
| Mapped reads | 426,717,062 |
| Mapping rate | **99.55%** |
| Properly paired reads | 416,419,524 |
| Properly paired rate | **97.59%** |
| Singleton reads | 824,445 (0.19%) |

---

## Mitochondrial Representation

- Mitochondrial reads (chrM): 1,255,902  
- Total mapped reads: 426,717,062  
- Mitochondrial fraction: **~0.29%**

### Metric Interpretation

- Presence of mitochondrial reads confirms genome-wide coverage  
- Fraction falls within expected WGS range (~0.1–1%)  
- Indicates successful capture of both nuclear and mitochondrial DNA  

---

## Stage 04 Interpretation

### Alignment Quality

- High mapping rate (~99.55%) indicates:
  - correct reference genome usage (GRCh38)
  - effective alignment
  - low sequencing noise  

### Pairing Structure

- Properly paired rate (~97.6%) indicates:
  - correct paired-end sequencing structure  
  - high-quality library preparation  

### Genome Coverage

- Reads distributed across all chromosomes (see idxstats)
- Low singleton rate (~0.19%) indicates minimal alignment issues  

---

## Raw Flagstat Output

```text
428652999 + 0 in total (QC-passed reads + QC-failed reads)
426721318 + 0 primary
0 + 0 secondary
1931681 + 0 supplementary
426717062 + 0 mapped (99.55%)
424785381 + 0 primary mapped (99.55%)
426721318 + 0 paired in sequencing
213360659 + 0 read1
213360659 + 0 read2
416419524 + 0 properly paired (97.59%)
423960936 + 0 with itself and mate mapped
824445 + 0 singletons (0.19%)
3754958 + 0 with mate mapped to a different chr
1913185 + 0 with mate mapped to a different chr (mapQ>=5)
```

---

## Role in the Pipeline

Stage 04 acts as a validation checkpoint between:

- Alignment (Stage 02–03)
    → and
- Variant Calling (Stage 05)


---

## Conclusion

Stage 04 confirms that:

- alignment is structurally valid
- read mapping quality is high
- paired-end sequencing integrity is preserved

These results indicate that the dataset is suitable for reliable variant calling in downstream stages.


---

## Notes

- Metrics derived from samtools flagstat and samtools idxstats
- Artifact curated for clarity; raw outputs preserved where relevant

---

## Bottom Line

```text
High-quality alignment → reliable variant calling → trustworthy downstream interpretation
```


---