# Stage 07 — VEP Annotation (VAP)

Stage 07 performs **variant annotation using Ensembl VEP**, converting normalized VCF data into biologically interpretable variant records.

---

## What Stage 07 Does

- annotates variants with gene, transcript, and consequence information  
- assigns impact classifications (HIGH, MODERATE, LOW, MODIFIER)  
- integrates population frequency data  
- produces both annotated VCF and structured TSV outputs  

---

## Key Artifacts

- [Output Manifest](stage_07_output_manifest.md)  
- [Annotated Columns](stage_07_columns.tsv)  
- [Example Annotated Variants](stage_07_example_rows.tsv)  
- [Missense Examples](stage_07_missense_examples.tsv)  
- [Stop-Gained Examples](stage_07_stop_gained_examples.tsv)  
- [VEP Summary Report](stage_07_vep_summary.html)  
- [VEP Warnings Log](stage_07_vep_variants_vcf_warnings.txt)

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