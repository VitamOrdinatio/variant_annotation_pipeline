# Stage 08 — Filtering & Partitioning (VAP)

Stage 08 transforms annotated variant-level data into **structured, downstream-ready datasets**.

This is the boundary layer where VAP transitions from:
- raw annotation (Stage 07)
→ into
- system-aligned data products (VDB + RDGP compatible)

---

## What Stage 08 Does

Stage 08 performs:

- deterministic filtering and partitioning of annotated variants  
- separation into coding and noncoding candidate spaces  
- preservation of all annotation fields (lossless transformation)  
- generation of VDB-ready variant records  
- aggregation into RDGP gene-level evidence seeds  

---

## Primary Outputs

- `stage_08_vdb_ready_variants.tsv`  
  → normalized, schema-aligned variant records for database ingestion  

- `stage_08_rdgp_gene_evidence_seed.tsv`  
  → gene-level aggregation for prioritization workflows  

- `stage_08_summary.json`  
  → run-level QC and execution summary  

---

## Execution Snapshot

- ~4.6 million variants processed  
- 0 irreparably malformed rows  
- >99% QC pass rate  

---

## Verification Artifacts

### Global Summary
- [Variant Summary](variant_summary/)  
  Distribution of coding/noncoding, frequency, and severity

### Coding Candidates
- [Coding Candidate Verification](coding_candidates/)  
  Protein-coding variant subset and high-impact examples

### Noncoding Candidates
- [Noncoding Candidate Verification](noncoding_candidates/)  
  Majority variant space with context and interpretability

### Gene-Level Evidence
- [RDGP Gene Evidence](rdgp_gene_evidence/)  
  Aggregated gene-level signals for prioritization

---

## Design Principles

- **Lossless transformation** — no variants dropped  
- **Deterministic execution** — reproducible outputs  
- **Schema alignment** — compatible with VDB + RDGP  
- **No premature interpretation** — prioritization deferred  

---

## Role in the System

Stage 08 connects:

- **VAP (variant-level data generation)**  
→ to  
- **VDB (structured storage)**  
- **RDGP (gene-level reasoning)**  

---

## Bottom Line

Stage 08 demonstrates large-scale transformation of annotated genomic data into:

- structured, contract-aligned variant records  
- interpretable gene-level evidence  

This is the first stage where the pipeline becomes a **data engineering system** rather than a toolchain.