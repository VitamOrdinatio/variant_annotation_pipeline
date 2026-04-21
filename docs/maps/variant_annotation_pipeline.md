# Repository: variant_annotation_pipeline (VAP)

## Purpose

Implement a reproducible pipeline that transforms raw sequencing data into clinically interpretable annotated variants.

---

## Position in the Overall System

VAP is the upstream evidence-generation pipeline for the broader genomics system.

Flow:

raw sequencing data → VAP → VDB → interface / GSC overlays → RDGP

---

## Terminology

- "variant-level evidence": structured variant observations and associated annotations generated for a sample
- "annotation": interpretation-linked metadata attached to a variant, such as consequence, population frequency, or clinical significance
- "candidate variant list": filtered variant-level output intended for downstream storage, review, or prioritization

---

## Strategic Value

This is the core clinical genomics repo in the portfolio.
Signals:
- NGS workflow competence (FASTQ → BAM → VCF) 
- variant annotation and filtering 
- familiarity with clinical interpretation context 
- ability to handle real-world pipeline complexity 
- alignment with tools and workflows used in hospital genomics labs 

---

## Core Output Data Model (v1)

VAP produces sample-linked variant-level evidence suitable for ingestion into VDB.

Fields:
- sample_id
- chrom
- pos
- ref
- alt
- variant_id (optional at VAP output stage if reconstructable from chrom, pos, ref, alt)
- variant_type
- quality_flag
- gene_symbol
- gene_id (if available)
- consequence
- impact_class
- population_frequency (if available)
- clinical_significance (if available)
- transcript_id (if available)
- annotation_source
- annotation_version (if available)
- run_id
- source_pipeline

---

### Example Record (v1)

- sample_id: SAMPLE_001
- chrom: chr15
- pos: 89875948
- ref: A
- alt: G
- variant_id: VAR_001
- variant_type: SNV
- quality_flag: PASS
- gene_symbol: POLG
- gene_id: ENSG00000140521
- consequence: missense_variant
- impact_class: moderate
- population_frequency: 0.0001
- clinical_significance: VUS
- transcript_id: ENST00000268124
- annotation_source: ClinVar
- annotation_version: 2026-04
- run_id: RUN_2026_001
- source_pipeline: VAP_v1

Note:
variant_id is deterministically derived from (chrom, pos, ref, alt) in v1.

---

## Downstream Contract

VAP must produce variant-level evidence in a form that can be ingested into VDB without ambiguity or lossy transformation.

At minimum, VAP outputs must preserve:
- sample identity
- variant identity (chrom, pos, ref, alt)
- annotation metadata
- provenance metadata
- quality flags

---

## Milestones

### M1 — Pipeline Skeleton (Data Flow Established)
- Define pipeline stages: 
    - input handling 
    - alignment (or placeholder) 
    - variant calling scaffold 
- Establish: 
    - config-driven execution 
    - logging 
    - reproducible run structure 
- Use toy or small dataset 

Goal: End-to-end pipeline structure exists, even if outputs are minimal

---

### M2 — Functional Variant Calling + Annotation
- Generate VCF from input data (real or benchmark dataset) 
- Integrate annotation layer: 
    - functional consequence (missense, nonsense, etc.) 
    - gene mapping 
- Produce structured outputs (tables) 

Structured outputs must include the fields required for VDB ingestion, including:
- sample_id
- genomic coordinates
- alleles
- quality_flag
- gene mapping
- consequence
- impact_class
- population_frequency (if available)
- clinical_significance (if available)
- annotation_source
- annotation_version (if available)
- run_id

Goal: Pipeline produces annotated variants

---

### M3 — Filtering + Interpretation-Oriented Outputs
- Add filtering logic: 
    - frequency-based (mock or real) 
    - consequence-based 
- Produce outputs that resemble: 
    - candidate variant lists 
    - variant-grouped summary tables for interpretation support

Goal: Output begins to resemble clinical interpretation inputs

---

### M4 — Validation + Edge Cases + Documentation
- Define: 
    - assumptions 
    - limitations 
    - edge cases: 
        ▪ low coverage 
        ▪ structural variants (acknowledged even if not fully implemented) 
        ▪ mitochondrial variants / heteroplasmy (at least discussed) 
- Define validation strategy: 
    - reference datasets (e.g., GIAB-style thinking) 
    - benchmarking approach 
    - reproducible reruns produce identical outputs
    - known benchmark variants are recovered
    - VCF / table outputs preserve fields required by VDB ingestion
    - low-quality vs passing calls are distinguishable
    - candidate variant filtering behaves consistently under fixed thresholds
- Document: 
    - implementation details (file formats, tools, compute constraints) 

Goal: Pipeline becomes defensible, not just functional

---

## Release Gate (Public v1.0)
VAP is considered portfolio-ready when:
- End-to-end pipeline runs reproducibly 
- Annotated variant outputs are generated 
- Filtering produces interpretable candidate variants
- outputs are compatible with VDB ingestion requirements
- provenance required for VDB ingestion is preserved
- README clearly explains: 
    - what the pipeline does 
    - how to run it 
    - what outputs mean 
- Documentation includes: 
    - assumptions 
    - limitations 
    - edge cases 
    - validation strategy 
    - implementation details 

---

## Future Upgrades (Post v1.0)
- Integration with external annotation tools (e.g., ANNOVAR-style workflows) 
- Structural variant handling improvements 
- Mitochondrial variant / heteroplasmy handling 
- AI-based pathogenicity prediction layer 
- direct ingestion into VDB
- compatibility with GSC-derived overlay workflows via VDB
- richer annotation sources for downstream RDGP support
