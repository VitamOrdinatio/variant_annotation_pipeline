# Schema for flattening coding consequence semantics

Applies to only coding (stage 09) candidate variants

## Purpose

Molecular consequence fields derived from VEP annotation layers can exhibit a wide range of semantic complexity.  Use this schema to flatten the complexity purely for metric emission support to support case study figure 4A generation (coding).

---

## Schema Rules

| Precedence | If consequence contains…                                                                                                                           | Collapse to                    | Why                                                                                                                      |
| ---------: | -------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------ | ------------------------------------------------------------------------------------------------------------------------ |
|          1 | `splice_acceptor_variant`, `splice_donor_variant`, `splice_region_variant`, `splice_donor_5th_base_variant`, `splice_polypyrimidine_tract_variant` | `splice_affected`              | Any splice-impact term should dominate because splicing consequences are mechanistically distinct and reviewer-relevant. |
|          2 | `stop_gained`                                                                                                                                      | `stop_gained`                  | Preserve explicit premature stop signal.                                                                                 |
|          3 | `frameshift_variant`                                                                                                                               | `frameshift`                   | Preserve frameshift as requested; major coding-disruption class.                                                         |
|          4 | `start_lost`                                                                                                                                       | `start_lost`                   | Preserve initiation-loss class.                                                                                          |
|          5 | `stop_lost`                                                                                                                                        | `stop_lost`                    | Preserve termination-loss class.                                                                                         |
|          6 | `missense_variant`, `protein_altering_variant`                                                                                                     | `missense_or_protein_altering` | Captures amino-acid-changing coding variants without overfragmenting.                                                    |
|          7 | `inframe_deletion`, `inframe_insertion`                                                                                                            | `inframe_indel`                | Protein-altering but distinct from frameshift.                                                                           |
|          8 | `synonymous_variant`, `stop_retained_variant`, `start_retained_variant`                                                                            | `synonymous_or_retained`       | Coding but usually lower interpretive salience.                                                                          |
|          9 | anything else                                                                                                                                      | `other_coding_consequence`     | Safety bin.                                                                                                              |


---

## Clean Precedence

```text
splice_affected
> stop_gained
> frameshift
> start_lost
> stop_lost
> missense_or_protein_altering
> inframe_indel
> synonymous_or_retained
> other_coding_consequence
```

## Footnote Language

```text
Composite VEP consequence strings were collapsed by deterministic precedence for visual readability; splice-associated terms were prioritized when present.
```