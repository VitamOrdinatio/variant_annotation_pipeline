# Stage 08 Output Manifest

Run ID: run_2026_04_17_082417  
Sample: HG002  
- `bioproject_accession`: "PRJNA200694"
- `sample_id`: "HG002"
- `sample_alias`: "NA24385"
- `sra_accession`: "SRR12898354"
    `reference_genome`: "GRCh38"

`TEST` environment: MARK (40-core HPC)

`DEV` environment: Sys76

Pipeline completed through Stage 08: filter and partition

Generated outputs:

```text
| Stage    | Stage Name (method)     | Output                 | Size     | Status    |
|----------|-------------------------|------------------------|----------|-----------|
| Stage 01 | load data HG002 SRA/SRR | SRR12898354_1.fastq.gz | ~15.3 GB | completed |
| Stage 01 | load data HG002 SRA/SRR | SRR12898354_2.fastq.gz | ~15.6 GB | completed |
| Stage 02 | align seq data          | aligned BAM            | ~39.2 GB | completed |
| Stage 03 | process BAM             | sorted BAM             | ~23.7 GB | completed |
| Stage 04 | index BAM               | indexed BAM (BAI)      | ~8.8 MB  | completed |
| Stage 04 | QC reads (flagstat)     | qc report              | ~1.1 KB  | completed |
| Stage 05 | call variants (gatk)    | raw VCF                | ~1.0 GB  | completed |
| Stage 06 | normalize VCF           | normalized VCF         | ~1.0 GB  | completed |
| Stage 07 | annotate variants (vep) | annotated VCF          | ~1.9 GB  | completed |
| Stage 07 | annotate variants (vep) | annotated TSV          | ~1.0 GB  | completed |
| Stage 07 | annotate variants (vep) | VEP summary HTML       | ~19.7 KB | completed |
| Stage 07 | annotate variants (vep) | VEP warnings TXT       | ~5.2 MB  | completed |
| Stage 08 | partition variants      | coding candidates TSV  | ~6.5 MB  | completed |
| Stage 08 | partition variants      | noncoding candid. TSV  | ~1.3 GB  | completed |
| Stage 08 | partition variants      | splice candidates TSV  | ~1.2 MB  | completed |
| Stage 08 | partition variants      | qc flagged TSV         | ~12.6 MB | completed |
| Stage 08 | partition variants      | vdb ready variants TSV | ~1.3 GB  | completed |
| Stage 08 | partition variants      | rdgp evidence seed TSV | ~59.8 MB | completed |
| Stage 08 | partition variants      | select transcript TSV  | ~1.3 GB  | completed |
| Stage 08 | partition variants      | variant summary TSV    | ~1.0 GB  | completed |
| Stage 08 | partition variants      | QC + summary JSON      | ~2.0 KB  | completed |


```

Large genomic outputs are excluded from Git by `.gitignore` and thus not tracked by Git.