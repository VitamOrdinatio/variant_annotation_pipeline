# Stage 07 — VEP Annotation (VAP)

Stage 07 performs **variant annotation using Ensembl VEP**, converting normalized VCF data into biologically interpretable variant records.

---

## What Stage 07 Does

- annotates variants with gene, transcript, and consequence information  
- assigns impact classifications (HIGH, MODERATE, LOW, MODIFIER)  
- integrates population frequency data  
- produces both annotated VCF and structured TSV outputs  

---

## Key Metrics (HG002)

- Variants processed: ~4.6 million
- Annotated variants retained: ~4.6 million
- Novel variants: ~1.4%
- Known variants: ~98.6%

---

## Why This Stage Matters

Stage 07 transforms raw genomic variation into biologically interpretable data by:

- mapping variants to genes and transcripts  
- assigning functional consequences  
- enabling downstream filtering and prioritization  

This is the key transition from data generation → biological interpretation.

---

## Key Artifacts


- [Validation Summary](stage_07_validation_summary.md)
- [Output Manifest](stage_07_output_manifest.md)  
- [Annotated Columns](stage_07_columns.md)  
- [Example Annotated Variants](stage_07_example_rows.md)  
- [Missense Examples](stage_07_missense_examples.md)  
- [Stop-Gained Examples](stage_07_stop_gained_examples.md)  
- [VEP Summary Report](stage_07_summary.md)  
- [VEP Warnings Log](stage_07_vep_variants_vcf_example_warnings.md)

---

## Execution Characteristics

- processes millions of variants  
- produces ~1 GB TSV output  
- uses offline VEP cache (reproducible environment)  

---

## Interpretation Notes

- most variants are:
  - noncoding  
  - common  
  - low or modifier impact  

- high-impact variants are rare but critical  

- warnings reflect:
  - contig mismatches  
  - annotation edge cases  
  (expected in large-scale annotation)

---

## Role in the System

Stage 07 transforms:

- raw variant calls (Stage 05–06)  
→ into  
- annotated variant records for downstream processing  

It is the **last stage of biological annotation** before data engineering (Stage 08).

---

## Bottom Line

Stage 07 demonstrates successful large-scale variant annotation, producing structured outputs suitable for filtering, partitioning, and downstream system integration.