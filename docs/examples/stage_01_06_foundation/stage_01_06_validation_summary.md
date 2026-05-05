# Stage 01–06 Validation Summary

## Dataset

- Sample: HG002 (GIAB benchmark genome)
- Reference: GRCh38

---

## Alignment Summary

Alignment produced a sorted and indexed BAM file representing whole-genome sequencing data.

### Key Metrics

- mapped reads: 426,717,062
- unmapped reads: 1,935,937
- mapping rate: **99.55%**

### Mitochondrial Read Representation

- mitochondrial mapped reads: 1,255,902
- mitochondrial genome size: 16,569 bp
- mitochondrial fraction of total reads: **~0.29%**

Key mtDNA points:

- Presence of mitochondrial reads confirms genome-wide coverage
- Fraction falls within expected range for whole-genome sequencing
- Indicates successful capture of mitochondrial DNA alongside nuclear genome

This is particularly relevant for downstream analyses involving mitochondrial genes and disorders.

### Mapping Interpretation

- High mapping rate is consistent with high-quality WGS data
- Reads are distributed across all chromosomes, including mitochondrial DNA (chrM)
- Low proportion of unmapped reads indicates effective alignment to GRCh38

(See: `stage_04_bam_idxstats_summary.tsv`)

---

## Variant Calling

Raw variant calling produced:

- **4,662,494 variants** 

This is consistent with expected human genome variation (~4–5 million variants per individual).

---

## Variant Normalization

Normalized variant set contains:

- **4,662,494 variants** 

### Key Observation

> No change in variant count between raw and normalized VCF

This indicates:

- normalization preserved variant representation
- no variant loss during transformation

---

## Structural Validation

- VCF format: valid (VCFv4.2)
- Reference: GRCh38
- GATK HaplotypeCaller used for variant generation

---

## Representative Variant Records

Example normalized variants demonstrate:

- heterozygous (0/1) and homozygous (1/1) calls
- allele depth (AD) and genotype quality (GQ)
- expected INFO field structure

(See: `stage_06_normalized_vcf_example_rows.tsv`)

---

## Conclusion

Stage 01–06 execution is:

- structurally valid
- quantitatively consistent with expected WGS data
- suitable for downstream annotation and interpretation

These results establish a reliable foundation for subsequent pipeline stages.