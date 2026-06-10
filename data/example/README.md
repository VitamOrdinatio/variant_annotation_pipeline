# `data/example/`

Deterministic lightweight fixture datasets for VAP development, smoketesting, and reproducible validation workflows.

---

# Overview

The `data/example/` namespace contains lightweight repository-safe fixture artifacts used to support:

* rapid local development,
* deterministic smoketesting,
* regression validation,
* telemetry validation,
* and lightweight post-VEP execution workflows.

These fixtures were critical during VAP development because full WGS execution can require many hours of runtime on HPC infrastructure.

The example substrates therefore provide:

```text
fast deterministic validation surfaces
```

without requiring:

* full FASTQ ingestion,
* BAM generation,
* whole-genome alignment,
* or cohort-scale annotation workflows.

---

# Directory Topology

```text
example/
├── example_annotated_variants.tsv
├── example_annotated_variants.vcf
├── example_gene_set_epilepsy.tsv
├── example_gene_set_mito.tsv
└── example_reference.fa
```

---

# Fixture Philosophy

The fixtures contained here intentionally prioritize:

* lightweight portability,
* deterministic behavior,
* rapid iteration,
* repository safety,
* and reproducible development workflows.

These substrates enabled rapid development of:

* Stage 08 partitioning,
* telemetry infrastructure,
* provenance continuity,
* runtime metadata systems,
* validation schemas,
* and downstream orchestration workflows

without requiring repeated long-running WGS execution.

---

# Included Fixtures

| Artifact                         | Purpose                                                |
| -------------------------------- | ------------------------------------------------------ |
| `example_annotated_variants.tsv` | Lightweight Stage 07-style annotated variant substrate |
| `example_annotated_variants.vcf` | Minimal provenance-aware VCF fixture                   |
| `example_gene_set_epilepsy.tsv`  | Example epilepsy overlay substrate                     |
| `example_gene_set_mito.tsv`      | Example mitochondrial overlay substrate                |
| `example_reference.fa`           | Minimal reference fixture                              |

---

# Primary Development Role

The example fixtures primarily support:

* post-VEP execution testing,
* Stage 08+ orchestration,
* runtime telemetry validation,
* metadata emission validation,
* schema continuity testing,
* and lightweight analytical experimentation.

These fixtures became especially important because:

```text
whole-genome execution turnaround is operationally expensive.
```

Lightweight deterministic substrates therefore allowed VAP development to progress rapidly while preserving reproducibility-aware engineering discipline.

---

# Relationship to Testing

The fixtures contained here are tightly integrated with the repository testing ecosystem.

Representative uses include:

* smoketests,
* regression tests,
* metadata validation,
* telemetry validation,
* and fixture-mode execution workflows.

This lightweight fixture infrastructure helped enable:

* deterministic development,
* rapid iteration,
* and reproducibility-oriented validation.

---

# Relationship to the Broader Ecosystem

The example substrates also support lightweight interoperability experimentation involving:

* semantic overlays,
* targeted enrichment,
* substrate partitioning,
* and downstream analytical routing.

Although intentionally minimal, these fixtures preserve the same semantic structure used throughout larger VAP execution workflows.

---

# Important Notes

These fixtures are:

* synthetic/lightweight development substrates,
* repository-safe examples,
* and non-clinical demonstration artifacts.

They are not intended for:

* diagnostic interpretation,
* clinical decision making,
* or biological inference.

---

# Summary

The `data/example/` namespace provides deterministic lightweight operational fixtures enabling:

* rapid VAP development,
* reproducible smoketesting,
* telemetry-aware validation,
* and scalable engineering iteration

without requiring repeated large-scale genomic execution.
