# Sidecar Telemetry

## Purpose

The main function of the sidecar is to gather input / output telemetry for each of the stages, in a non-mutable, provenance-aware fashion.

For some sidecar audits, this means a second layer of canonical pipeline validations.

The current sidecar architecture intentionally mixes lightweight reflective telemetry with independent observational auditing. Earlier stages and semantic interpretation stages independently inspect TSV/VCF artifacts directly, while later prioritization and validation stages currently mirror canonical summary semantics for efficient analytics generation. The roadmap is to progressively evolve the reflective stages into fully independent semantic auditors.

---

## Prime Directive

The sidecar telemetry subsystem is strictly observational.

The sidecar:
- MUST NOT modify canonical pipeline artifacts
- MUST NOT alter biological semantics
- MUST NOT reinterpret pipeline outputs
- MUST NOT influence pipeline control flow
- MUST NOT mutate prioritization or validation outcomes

The sidecar MAY:
- inspect emitted artifacts
- perform provenance-aware recounts
- derive independent telemetry measurements
- emit observational metrics into:
  `results/run_<id>/metrics/`

All telemetry products are isolated from canonical VAP outputs.

---

## Sidecar Audit Modes

The current sidecar telemetry architecture contains three telemetry paradigms.

| Mode                             | Meaning                                                                        | Current Stages |
| -------------------------------- | ------------------------------------------------------------------------------ | -------------- |
| Artifact Integrity Audit         | “Does this emitted artifact structurally exist and reconcile?”                 | 05–12          |
| Independent Semantic Observation | “Can the sidecar independently derive biological telemetry from TSV contents?” | 09–10          |
| Canonical Reflection Telemetry   | “Can we conveniently expose canonical stage semantics for plotting/analytics?” | 11–12          |

---

## Definition of Independent Audit

Within the sidecar telemetry framework, an "independent audit" means:

- the sidecar directly inspects canonical TSV/VCF artifacts
- telemetry values are derived from artifact contents rather than summary JSON reflection
- the sidecar performs its own recounts, semantic parsing, or ontology derivation
- telemetry generation does not rely on canonical summary metrics as the primary source-of-truth

Independent auditing does NOT imply:
- biological reinterpretation
- alternate prioritization logic
- alternate clinical classification
- mutation of canonical outputs

---

## Observational vs Adversarial Telemetry

Current sidecar telemetry is primarily observational.

Observational telemetry:
- measures
- recounts
- summarizes
- derives semantic distributions

without attempting to challenge canonical VAP semantics.

Future adversarial telemetry may:
- independently recompute prioritization logic
- detect ontology drift
- detect summary/artifact divergence
- identify reconciliation failures between stages

---

## Current Sidecar Audit Taxonomy

| Stage    | Metric Type                         | Independent TSV Audit? | Mechanism                   | Audit Strength   | Notes                                               |
| -------- | ----------------------------------- | ---------------------- | --------------------------- | ---------------- | --------------------------------------------------- |
| Stage 05 | `raw_called_variants`               | YES                    | Direct VCF recount          | Strong           | Counts non-header VCF rows directly                 |
| Stage 06 | `normalized_variants`               | YES                    | Direct VCF recount          | Strong           | Independent normalization output recount            |
| Stage 07 | `annotated_variants_vcf`            | YES                    | Direct VCF recount          | Strong           | Independent annotated VCF observation               |
| Stage 07 | `annotated_variants_tsv`            | YES                    | Direct TSV recount          | Strong           | Independent annotation table observation            |
| Stage 08 | `coding_candidates_rows`            | YES                    | Direct TSV recount          | Strong           | Independent artifact measurement                    |
| Stage 08 | `splice_region_candidates_rows`     | YES                    | Direct TSV recount          | Strong           | Independent artifact measurement                    |
| Stage 08 | `qc_flagged_rows`                   | YES                    | Direct TSV recount          | Strong           | Independent artifact measurement                    |
| Stage 08 | `rdgp_gene_evidence_seed_rows`      | YES                    | Direct TSV recount          | Strong           | Independent artifact measurement                    |
| Stage 08 | partition semantic counts           | PARTIAL                | Mostly summary reflection   | Moderate         | Mirrors canonical partition summary logic           |
| Stage 09 | `coding_interpreted_rows`           | YES                    | Direct TSV recount          | Strong           | Independent recount of interpreted coding TSV       |
| Stage 09 | consequence distributions           | YES                    | Direct TSV semantic parsing | Strong           | Sidecar independently inspects TSV ontology strings |
| Stage 09 | clinical significance distributions | YES                    | Direct TSV semantic parsing | Strong           | Independent semantic extraction                     |
| Stage 09 | rarity distributions                | YES                    | Direct TSV semantic parsing | Strong           | Independent semantic extraction                     |
| Stage 09 | functional impact distributions     | YES                    | Direct TSV semantic parsing | Strong           | Independent semantic extraction                     |
| Stage 09 | rolled-up summary metrics           | PARTIAL                | Summary alignment           | Moderate         | Summary and telemetry remain coherent               |
| Stage 10 | `noncoding_interpreted_rows`        | YES                    | Direct TSV recount          | Strong           | Independent recount                                 |
| Stage 10 | functional context distributions    | YES                    | Direct TSV semantic parsing | Strong           | Independent ontology compression                    |
| Stage 10 | rarity distributions                | YES                    | Direct TSV semantic parsing | Strong           | Independent semantic extraction                     |
| Stage 10 | noncoding interpretation labels     | YES                    | Direct TSV semantic parsing | Strong           | Independent semantic extraction                     |
| Stage 10 | rolled-up summary metrics           | PARTIAL                | Summary alignment           | Moderate         | Semantic coherence validated                        |
| Stage 11 | `prioritized_variants_rows`         | YES                    | Direct TSV recount          | Strong           | Independent artifact validation                     |
| Stage 11 | `gene_variant_counts_rows`          | YES                    | Direct TSV recount          | Strong           | Independent artifact validation                     |
| Stage 11 | prioritization distributions        | NO                     | Summary JSON mirror         | Reflective | Reflective telemetry only                           |
| Stage 11 | priority tier counts                | NO                     | Summary JSON mirror         | Reflective | Not independently recomputed                        |
| Stage 11 | source interpretation counts        | NO                     | Summary JSON mirror         | Reflective | No TSV semantic reconstruction                      |
| Stage 12 | `validation_candidates_rows`        | YES                    | Direct TSV recount          | Strong           | Independent artifact validation                     |
| Stage 12 | validation routing distributions    | NO                     | Summary JSON mirror         | Reflective | Reflective telemetry only                           |
| Stage 12 | IGV routing counts                  | NO                     | Summary JSON mirror         | Reflective | No independent reconstruction                       |
| Stage 12 | validation priority distributions   | NO                     | Summary JSON mirror         | Reflective | Deterministic reflection                            |

---

## Planned Evolution

Current sidecar telemetry prioritizes:
- lightweight observability
- provenance preservation
- rapid metric extraction
- cognition-engineering substrate generation

Future sidecar iterations may introduce:
- adversarial TSV revalidation
- independent semantic recomputation
- ontology drift detection
- stage-to-stage reconciliation auditing
- summary-vs-artifact divergence detection
- configurable telemetry execution profiles

Potential future execution profiles:

```yaml
telemetry:
  mode: execution_only
```

or:

```yaml
telemetry:
  mode: execution_plus_independent_audit
```

Future adversarial telemetry modes are expected to incur substantially higher computational cost due to repeated semantic parsing, ontology recomputation, and cross-stage reconciliation analysis. The current observational telemetry architecture intentionally prioritizes lightweight provenance-aware observability suitable for routine production execution.

---

## Current Architectural Philosophy

The current sidecar telemetry subsystem prioritizes:

1. deterministic execution safety
2. provenance preservation
3. lightweight observability
4. cognition-engineering substrate generation
5. future audit extensibility

The current system intentionally favors transparent observational telemetry over premature adversarial recomputation.

---