# `data/reference/gene_lists/`

Lightweight semantic overlay substrates supporting transitional interoperability and post-VAP contextualization workflows.

---

# Overview

The `gene_lists/` namespace contains lightweight semantic overlay substrates used to enrich and contextualize VAP outputs during the current transitional interoperability phase of the broader repository ecosystem.

These overlays presently support workflows involving:

* targeted semantic enrichment,
* post-VAP SQL slicing,
* lightweight prioritization overlays,
* mitochondrial contextualization,
* epilepsy-focused evidence interrogation,
* and interoperability experimentation.

The overlays contained here are intentionally lightweight and repository-resident.

---

# Transitional Interoperability Role

The current overlay architecture is intentionally transitional.

At present, lightweight overlay substrates allow VAP outputs to participate in downstream semantic contextualization workflows before full VDB-mediated interoperability routing becomes operational.

Current architecture:

```text
VAP → lightweight overlay bridge → downstream semantic enrichment
```

Future architecture:

```text
VAP → VDB → GSC / RDGP / RSP interoperability ecosystem
```

These overlays therefore function as:

```text
temporary semantic coordination substrates
```

supporting lightweight interoperability experimentation during staged repository ecosystem maturation.

---

# Directory Contents

| Artifact                         | Purpose                                                   |
| -------------------------------- | --------------------------------------------------------- |
| `mitocarta_vap_overlay_seed.tsv` | mitochondrial disease-oriented semantic overlay substrate |
| `epi25_vap_overlay_seed.tsv`     | epilepsy-oriented semantic overlay substrate              |

These overlays are currently used for:

* targeted overlay intersections,
* downstream analytical enrichment,
* semantic filtering,
* and cross-run contextualization workflows.

---

# `MitoCarta 3.0` Overlay Preparation

Final VAP overlay substrate:

```text
data/reference/gene_lists/mitocarta_vap_overlay_seed.tsv
```

This overlay was prepared using manually curated transformation and normalization procedures designed to support deterministic interoperability workflows within VAP.

---

## Row Removal

The following three MitoCarta rows were manually removed:

```text
PIGBOS1
HTD2
RP11_469A15.2
```

These entries appeared to contain incomplete or unstable metadata and were not considered suitable for stable protein-centric overlay usage within the current VAP interoperability layer.

---

## Column Name Conversion

Original MitoCarta 3.0 fields were normalized into VAP-compatible overlay schema fields.

| Original MitoCarta Field                 | VAP Field         |
| ---------------------------------------- | ----------------- |
| `HumanGeneID`                            | `gene_id`         |
| `Symbol`                                 | `gene_symbol`     |
| `Synonyms`                               | `synonyms`        |
| `EnsemblGeneID_mapping_version_20200130` | `ensembl_gene_id` |
| `UniProt`                                | `uniprot`         |
| `hg19_Chromosome`                        | `hg19_chromosome` |

This normalization layer enabled lightweight interoperability alignment between:

* MitoCarta-derived semantic overlays,
* VAP analytical substrates,
* and downstream enrichment workflows.

---

# `Epi25` Overlay Preparation

Final VAP overlay substrate:

```text
data/reference/gene_lists/epi25_vap_overlay_seed.tsv
```

The epilepsy overlay was generated through manual review and structured extraction of high-confidence epilepsy-associated loci from the primary Epi25 literature.

Reference:

> Epi25 Collaborative.
> *Exome sequencing of 20,979 individuals with epilepsy reveals shared and distinct ultra-rare genetic risk across disorder subtypes.*
> Nat Neurosci. 2024;27(10):1864–1879.
> doi:10.1038/s41593-024-01747-8

---

## High-Confidence Extracted Loci

The following loci were selected based on strong statistical support and recurrent epilepsy association within the source publication:

1. NEXMIF
2. SCN1A
3. SYNGAP1
4. STX1B
5. WDR45
6. DEPDC5
7. NPRL3

---

## Overlay Construction Strategy

Starting from official gene symbols extracted from the primary literature, additional manual curation workflows were performed using GeneCards to construct an overlay substrate structurally compatible with:

```text
mitocarta_vap_overlay_seed.tsv
```

This normalization approach enabled:

* deterministic overlay interoperability,
* schema continuity,
* lightweight enrichment compatibility,
* and downstream SQL-oriented contextualization workflows.

---

# Architectural Philosophy

The overlays contained here intentionally prioritize:

* lightweight interoperability,
* deterministic structure,
* transparent provenance,
* repository portability,
* and semantic continuity.

These overlays are not intended to function as authoritative biological databases.

Instead, they act as:

```text
lightweight semantic enrichment substrates
```

supporting transitional interoperability workflows across the broader VAP ecosystem.

---

# Relationship to the Broader Ecosystem

The `gene_lists/` overlays currently bridge VAP outputs toward downstream semantic enrichment workflows involving:

* GSC,
* RDGP,
* cross-run analytical workflows,
* and future VDB-mediated interoperability infrastructure.

As the broader repository ecosystem matures, these static overlay substrates are expected to transition toward more formalized governed interoperability routing systems.

---

# Summary

The `data/reference/gene_lists/` namespace provides lightweight deterministic semantic overlay substrates supporting:

* post-VAP contextualization,
* targeted enrichment,
* interoperability experimentation,
* and transitional ecosystem coordination

within the broader VAP semantic infrastructure architecture.
