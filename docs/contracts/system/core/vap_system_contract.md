# Variant Annotation Pipeline (VAP) — System Contract

**Version:** v1  

**Scope:** Repository-level contract  

**Applies To:** 

This contract governs VAP outputs intended for VDB ingestion and downstream RDGP compatibility.

---

# 🧭 Purpose

This document defines the **enforceable output interface** of the Variant Annotation Pipeline (VAP).

It specifies:

- required output schemas
- field definitions and constraints
- invariants
- cross-repo compatibility requirements

This contract governs VAP outputs intended for VDB ingestion and downstream compatibility with RDGP-facing aggregation.

---

# 🎯 Contract Scope

The VAP system contract applies to:

```text
stage_08_vdb_ready_variants.tsv
stage_08_rdgp_gene_evidence_seed.tsv
```

All upstream stages (01–07) are considered internal implementation details.

Stage 08 is the contract boundary layer.

---

# 📤 Primary Output Schema (VDB Ingest)

Each row represents a variant–transcript annotation record.

## Required Fields

```text
sample_id
run_id
source_pipeline
variant_id
chromosome
position
reference_allele
alternate_allele
quality_flag
gene_id
gene_symbol
transcript_id
consequence
impact_class
variant_type
variant_class
clinical_significance
clinvar_significance
population_frequency
gnomad_af
exac_af
thousand_genomes_af
mito_flag
epilepsy_flag
annotation_source
annotation_version
gene_mapping_status
```
---

## Field-name mapping

chrom ↔ chromosome
pos ↔ position
ref ↔ reference_allele
alt ↔ alternate_allele



# 🧠 Field Semantics

## Variant Identity

```text
variant_id = CHROM:POS:REF:ALT
```

Must be unique per genomic variant.

## Consequence vs Impact
   
    • consequence = fine-grained VEP annotation (e.g., missense_variant) 
    • impact_class = severity bin (HIGH, MODERATE, LOW, MODIFIER) 

Both must be preserved.

## Clinical Annotation
      
    • clinvar_significance = raw source value 
    • clinical_significance = normalized interpretation 

Neither may overwrite the other.

## Population Frequency

```text
population_frequency = max(
  gnomad_af,
  exac_af,
  thousand_genomes_af
)
```

Rules:
      
    • NULL if all AF fields are missing 
    • Must not infer rarity from missing data 

## Variant Classification

    • variant_type = allele structure (SNV, indel, etc.) 
    • variant_class = functional grouping (coding, noncoding) 

These must remain distinct.

## Gene Mapping

`gene_mapping_status ∈ {mapped, unmapped}`

Unmapped variants:

    • must be preserved 
    • must not appear in RDGP gene aggregation 

## Phenotype Flags

Fields such as:

    • mito_flag 
    • epilepsy_flag 

Must be:

    • deterministic 
    • reproducible 
    • externally defined (see phenotype_flag_spec.md) 

Phenotype flags are optional annotation overlays and are not required for core VDB ingestion.

# 📊 RDGP Seed Output Contract

File:

`stage_08_rdgp_gene_evidence_seed.tsv`

Each row represents a (sample_id, gene_id) aggregation unit.

## Required Fields

```text
sample_id
gene_id
gene_symbol
variant_count
high_impact_variant_count
rare_variant_count
pathogenic_variant_count
max_variant_severity
has_low_quality_evidence
contributing_variant_ids
```

This seed is not a complete RDGP input record. Missing RDGP aggregation fields are generated later by VDB/interface aggregation or marked NULL when unavailable.

The RDGP seed output is an optional early aggregation helper and must not be treated as the authoritative RDGP input contract.

The authoritative RDGP-facing aggregation contract is defined by the VDB ↔ RDGP interface specification.

# 🔒 System Invariants

## 1. Losslessness
Every input variant must appear in at least one output.

## 2. Transcript Fidelity
No transcript-level annotations are discarded.

## 3. Determinism
Identical input → identical output.

## 4. Schema Stability
Field names and formats must not change without versioning.

## 5. Sample Identity Preservation
All outputs must retain sample_id.

## 6. Null Handling

- missing source values must be represented as NULL or documented placeholders
- zero must remain distinguishable from missing
- missing allele frequency must not be interpreted as rare
- missing clinical significance must not be interpreted as benign
---

# 🔗 Cross-Repo Compatibility

## VDB Requirements

    • one row per variant–transcript record 
    • stable schema 
    • normalized field naming 
    • explicit provenance fields 

## RDGP Requirements

    • gene-level aggregation inputs 
    • no implicit filtering 
    • explicit quality and severity tracking 


---

# ⚠️ Non-Goals

VAP must NOT:

    • perform final variant prioritization 
    • apply irreversible filtering 
    • collapse transcript annotations 
    • perform gene-level scoring 


---

## Handoff Expectations

Future VDB system_contract.md should define:
- ingestion of `stage_08_vdb_ready_variants.tsv`
- normalized storage of variant, annotation, gene, and provenance records
- preservation of all raw annotation rows

Future RDGP system_contract.md should define:
- final gene-level aggregation requirements
- scoring inputs
- prioritization outputs
- interpretation/reporting expectations

VAP does not define VDB storage schema or RDGP scoring logic.

---

# 🧭 Versioning

Changes to this contract require:

    • schema version increment 
    • backward compatibility plan 
    • update to interface specification 


---

# 🎯 Bottom Line

VAP guarantees:

```text
reproducible, lossless, schema-stable variant annotation outputs
suitable for database ingestion and gene-level prioritization systems
```

VAP must preserve source annotation fields and must not perform final annotation precedence resolution.

---

# END of VAP system contract

---
