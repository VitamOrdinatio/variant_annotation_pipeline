For provenance and reproducibility, gene overlay lists were prepared using the following methodology.

# `MitoCarta 3.0` Preparation for `VAP`

final file:

`data/reference/gene_lists/mitocarta_vap_overlay_seed.tsv`

---

## Row removal

The following three MitoCarta rows were manually removed.

Rows with MitoCarta 3.0 Symbol value of:

```text
PIGBOS1
HTD2
RP11_469A15.2
```

as these three seem to have incomplete MitoCarta metadata and may not represent proteins.

---

## Column name conversion

Original MitoCarta 3.0 fields were renamed as such:

| MitoCarta 3.0 item                     | VAP-converted name |
| -------------------------------------- | ------------------ |
| HumanGeneID	                         | gene_id            |
| Symbol	                             | gene_symbol        |
| Synonyms	                             | synonyms           |
| EnsemblGeneID_mapping_version_20200130 | ensembl_gene_id    |
| UniProt	                             | uniprot            |
| hg19_Chromosome	                     | hg19_chromosome    |

# `Epi25` Preparation for `VAP`

final file:

`data/reference/gene_lists/epi25_vap_overlay_seed.tsv`

---

Primary literature was manually digested to extract the following 7 loci associated with great statistical confidence with epilepsy presentation.

1. NEXMIF
2. SCN1A
3. SYNGAP1
4. STX1B
5. WDR45
6. DEPDC5
7. NPRL3

Reference: 

Epi25 Collaborative. Exome sequencing of 20,979 individuals with epilepsy reveals shared and distinct ultra-rare genetic risk across disorder subtypes. Nat Neurosci. 2024;27(10):1864-1879. doi:10.1038/s41593-024-01747-8


---

Starting with offical gene names, manual queries using GeneCards were performed to complete an equivalent dataframe matching the structure of `mitocarta_vap_overlay_seed.tsv`.

---

