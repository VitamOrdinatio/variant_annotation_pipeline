# VAP Status Report — 2026-04-24

## Executive Summary

The Variant Annotation Pipeline (VAP) currently executes successfully through Stage 07 VEP annotation for HG002 on MARK.

The pipeline demonstrates:

- FASTQ ingestion
- alignment
- BAM processing
- aligned-read QC
- variant calling
- VCF normalization
- VEP annotation
- generation of annotated VCF and TSV outputs

Large genomic artifacts are intentionally excluded from Git. This repository tracks source code, configuration, documentation, contracts, manifests, and small representative output examples.

---

## Current Run

- sample_id: HG002
- run_id: run_2026_04_17_082417
- development environment: Sys76
- execution environment: MARK
- reference genome: GRCh38
- SRA accession: SRR12898354
- BioProject: PRJNA200694

---

## Completed Pipeline Stages

| Stage | Description | Status |
|---|---|---|
| Stage 01 | FASTQ ingestion | Complete |
| Stage 02 | BWA alignment | Complete |
| Stage 03 | BAM processing | Complete |
| Stage 04 | BAM indexing and aligned-read QC | Complete |
| Stage 05 | GATK variant calling | Complete |
| Stage 06 | VCF normalization | Complete |
| Stage 07 | VEP annotation | Complete |

---

## Evidence of Completion

Representative artifacts are stored in `docs/examples/`.

- `stage_07_output_manifest.md` — summary of generated outputs and file sizes
- `stage_04_qc_report.md` — aligned-read QC metrics
- `stage_07_columns.tsv` — annotated TSV column names
- `stage_07_example_rows.tsv` — representative annotated output rows
- `stage_07_missense_examples.tsv` — representative missense variants
- `stage_07_stop_gained_examples.tsv` — representative stop-gained variants
- `stage_07_vep_summary.html` — VEP summary report
- `stage_07_vep_variants_vcf_warnings.txt` — VEP warnings captured from full run

---

## Key QC Evidence

Stage 04 aligned-read QC showed:

- total reads: 428,652,999
- mapped reads: 426,717,062
- mapping rate: 99.55%
- properly paired reads: 416,419,524
- properly paired rate: 97.59%

These metrics support successful alignment and BAM processing before variant calling. 

---

## Stage 07 Annotation Evidence

Stage 07 generated:

- annotated VCF: approximately 1.9 GB
- annotated TSV: approximately 1.0 GB
- VEP summary HTML: approximately 19.7 KB
- VEP warnings TXT: approximately 5.2 MB

The full VEP run processed millions of variants and produced a structured annotated output table suitable for downstream filtering and partitioning.

---

## Representative Annotation Fields

The Stage 07 TSV includes downstream-relevant fields such as:

- sample_id
- run_id
- source_pipeline
- variant_id
- chromosome
- position
- reference_allele
- alternate_allele
- quality_flag
- gene_id
- gene_symbol
- transcript_id
- consequence
- impact_class
- variant_type
- variant_class
- clinical_significance
- population_frequency
- gnomad_af
- exac_af
- thousand_genomes_af
- mito_flag
- epilepsy_flag

These fields provide the basis for Stage 08 filtering, partitioning, and VDB-compatible output preparation.

---

## Important Limitations

Large sequencing and variant files are not tracked in Git, including:

- FASTQ files
- BAM / BAI files
- raw VCF files
- normalized VCF files
- full annotated VCF files
- full annotated TSV files

These are excluded intentionally because they are large generated artifacts.

Some VEP warnings were observed for contigs not found in annotation sources or synonyms. These warnings are preserved in `stage_07_vep_variants_vcf_warnings.txt` and should be reviewed as part of Stage 08 / validation planning.

---

## Current Development Focus

The pipeline is now transitioning from tool execution into data engineering and interpretation.

Current focus:

- Stage 08 filter and partition implementation
- schema stabilization
- VDB-compatible variant output
- RDGP-compatible gene evidence seed output
- preservation of raw annotation fields
- avoidance of premature annotation precedence resolution

---

## Next Milestone

Stage 08 will convert Stage 07 VEP annotation output into structured, lossless, downstream-compatible tables.

Expected Stage 08 outputs include:

- `stage_08_vdb_ready_variants.tsv`
- `stage_08_rdgp_gene_evidence_seed.tsv`
- coding candidate table
- splice-region candidate table
- noncoding candidate table
- QC-flagged table
- summary JSON

---

## Bottom Line

VAP has successfully demonstrated end-to-end execution from HG002 sequencing input through VEP annotation.

The repository now contains enough tracked evidence to show working pipeline execution while keeping large genomic artifacts out of Git.