# VAP Example Fixture Data

This directory contains tiny deterministic fixture inputs for local VAP development and regression testing.

## Files

- `example_annotated_variants.tsv`
  - Minimal Stage 07-like annotated variant table.
  - Designed for post-VEP Stage 08+ fixture execution.
  - Repository-safe and deterministic.

- `example_annotated_variants.vcf`
  - Tiny provenance VCF corresponding to the TSV rows.
  - Retained for Stage 08 validation/provenance behavior.

## Purpose

These files support Phase 0b lightweight deterministic execution without requiring HG002-scale FASTQ/BAM/VCF processing or MARK hardware.

The fixture is not a clinical dataset and must not be interpreted diagnostically.
