# Genotype Elevation Closure Summary

- Script version: `0.9.0`
- Closure status: `PASS_WITH_BOUNDED_LIMITATIONS`
- Historical-only coding identities: `14`
- Current-only coding identities: `26`
- Exact genotype joins: `23`
- Source-record locus recoveries: `3`
- Unresolved current genotype relationships: `0`
- Source-record context coverage: `1.000000`
- Same-locus comparison pairs: `4`
- Current relationships requiring VDB mediation: `3`

## Certification Boundary

Shared coding interpretation is invariant across all directly comparable shared variant identities. The coding identity delta is fully enumerated. Current-only genotype evidence is joined by exact variant identity where possible and recovered at source-record locus level for complex records. Locus recovery establishes preserved source-record context, not automatic allele-specific equivalence.

Historical noncoding identity-level closure is not possible from the retained lightweight extraction and remains an explicit evidence limitation rather than a failed validation.

## Delta Classifications

| Classification | Count |
|---|---:|
| CURRENT_ONLY_COMPLEX_MULTIALLELIC | 1 |
| CURRENT_ONLY_DIRECT_BIALLELIC | 21 |
| CURRENT_ONLY_REPRESENTATION_COMPATIBLE | 3 |
| CURRENT_ONLY_SAME_LOCUS_DIFFERENT_ALLELE_UNRESOLVED | 1 |
| HISTORICAL_ONLY_REPRESENTATION_COMPATIBLE | 3 |
| HISTORICAL_ONLY_SAME_LOCUS_DIFFERENT_ALLELE_UNRESOLVED | 1 |
| HISTORICAL_ONLY_UNEXPLAINED | 10 |

## VDB Relevance

Direct biallelic relationships are transportable without inference. Representation-compatible same-locus ALT sets and complex multiallelic source records retain genotype context and remain appropriate targets for VDB identity mediation. Same-locus different-allele pairs remain unresolved comparison evidence and are not counted as modern VDB mediation obligations.
