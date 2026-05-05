# stage_01_06_output_manifest

## Run Metadata

- `run_id`: `run_2026_04_17_082417`
- `sample_id`: `HG002`
- `sample_alias`: `NA24385`
- `bioproject_accession`: `PRJNA200694`
- `sra_accession`: `SRR12898354`
- `reference_genome`: `GRCh38`
- `test_environment`: `MARK`
- `dev_environment`: `Sys76`

## Pipeline Completion

Pipeline completed through: `stage_06`

## Generated Outputs

| Stage | Stage Name (method) | Output | Size | Status |
| --- | --- | --- | --- | --- |
| Stage 03 | align seq data | sorted BAM | 22.0 GiB | completed |
| Stage 04 | index BAM | indexed BAM BAI | 8.4 MiB | completed |
| Stage 05 | call variants | raw VCF | 888.2 MiB | completed |
| Stage 06 | normalize VCF | normalized VCF | 888.2 MiB | completed |

## Key Metrics

- raw_variant_count: 4,662,494
- normalized_variant_count: 4,662,494

## Interpretation

- Variant counts fall within expected WGS range (~4–5M)
- No loss of variants during normalization

## Git Tracking Note

Large computational outputs are source evidence only and should remain outside Git-tracked repository folders unless explicitly copied under a configured size limit.

## Source-of-Truth Note

Artifacts are generated using a config-driven extraction system ("Artificer") and curated for clarity. Source pipeline outputs remain authoritative.
