# Schema for flattening ClinVar significance semantics

Applies to both coding (stage 09) and non-coding (stage 10) candidate variants

## Purpose

ClinVar significance fields derived from VEP annotation layers can exhibit a wide range of semantic complexity.  Use this schema to flatten the complexity purely for metric emission support to support case study figures 4A and 4B generation.

---

## Schema Rules

Each row is a rule, and higher rows have higher precedence.

| Source pattern                                                                                                                                                                 |                        Map to | Why                                                                               |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------: | --------------------------------------------------------------------------------- |
| contains `conflicting_classifications_of_pathogenicity`                                                                                                                        | `conflicting_classifications` | ClinVar explicitly says conflict. Do not reinterpret.                             |
| contains both benign-side evidence and pathogenic-side evidence                                                                                                                | `conflicting_classifications` | Example: `benign&pathogenic`, `likely_benign&likely_pathogenic`.                  |
| contains `pathogenic` without benign-side conflict                                                                                                                             |                  `pathogenic` | Strongest pathogenic category.                                                    |
| contains `likely_pathogenic` without benign-side conflict                                                                                                                      |           `likely_pathogenic` | Pathogenic-side evidence, but not definitive.                                     |
| contains `uncertain_significance` without explicit conflict/pathogenic-side escalation                                                                                         |      `uncertain_significance` | Conservative; avoids falsely benign classification.                               |
| contains `benign_likely_benign` or `likely_benign` without uncertainty/conflict/pathogenic terms                                                                               |               `likely_benign` | Mixed benign-side category should map to the less definitive benign-side bin.     |
| contains only `benign` plus non-pathogenic modifiers like `drug_response`, `risk_factor`, `association`, `protective`, `affects`, `other`                                      |                      `benign` | Benign is the only ACMG-style assertion present.                                  |
| contains only non-ACMG / non-pathogenicity terms: `NA`, `not_provided`, `association`, `affects`, `drug_response`, `risk_factor`, `protective`, `other`, `confers_sensitivity` |      `uncertain_significance` | No usable benign/pathogenic assertion; safest six-bin destination is uncertainty. |
