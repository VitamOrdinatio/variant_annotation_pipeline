# Schema for flattening noncoding consequence semantics

Applies to only noncoding (stage 10) candidate variants

## Purpose

Molecular consequence fields derived from VEP annotation layers can exhibit a wide range of semantic complexity.  Use this schema to flatten the complexity purely for metric emission support to support case study figure 4B generation (noncoding).

---

## Schema Rules

| Precedence | If consequence contains…                                                                                                        | Collapse to                   | Why                                                                          |
| ---------: | ------------------------------------------------------------------------------------------------------------------------------- | ----------------------------- | ---------------------------------------------------------------------------- |
|          1 | `splice_donor_5th_base_variant`, `splice_donor_region_variant`, `splice_polypyrimidine_tract_variant`, any other `splice_` term | `splice_affected`             | Preserve splice-adjacent noncoding effects as a distinct interpretive class. |
|          2 | `mature_miRNA_variant`                                                                                                          | `mature_miRNA`                | Small but biologically distinct regulatory RNA class.                        |
|          3 | `3_prime_UTR_variant`, `5_prime_UTR_variant`                                                                                    | `UTR`                         | UTR variation is reviewer-friendly and biologically interpretable.           |
|          4 | `non_coding_transcript_exon_variant`, `non_coding_transcript_variant`                                                           | `noncoding_transcript`        | Captures transcript-associated noncoding evidence.                           |
|          5 | `intron_variant`                                                                                                                | `intronic`                    | Major noncoding reservoir; keep separate.                                    |
|          6 | `upstream_gene_variant`, `downstream_gene_variant`                                                                              | `flanking_gene_region`        | Gene-proximal but outside transcript body.                                   |
|          7 | `intergenic_variant`                                                                                                            | `intergenic`                  | Distinct from gene-proximal/flanking regions.                                |
|          8 | `coding_sequence_variant`, `incomplete_terminal_codon_variant`, `stop_retained_variant`                                         | `coding_or_retained_residual` | Safety bin for coding-like residues appearing in noncoding stream.           |
|          9 | anything else                                                                                                                   | `other_noncoding_consequence` | Safety bin.                                                                  |

---

## Clean Precedence

```text
splice_affected
> mature_miRNA
> UTR
> noncoding_transcript
> intronic
> flanking_gene_region
> intergenic
> coding_or_retained_residual
> other_noncoding_consequence
```

---

## Splice_affected Note

Let splice_affected dominate composite labels.

For example:

```text
splice_polypyrimidine_tract_variant&intron_variant&non_coding_transcript_variant
→ splice_affected
```

---

## Footnote Language

```text
Composite noncoding VEP consequence strings were collapsed by deterministic precedence for visual readability; splice-associated terms were prioritized when present.
```