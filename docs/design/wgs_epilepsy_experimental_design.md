# WGS Epilepsy Experimental Design

## Purpose

This experiment will evaluate whether the Variant Annotation Pipeline (VAP) can reproducibly process and preserve clinically relevant evidence from a public, disease-associated whole-genome sequencing substrate that is scientifically continuous with the existing epilepsy whole-exome sequencing corpus from BioProject `PRJEB57558`.

The selected whole-genome BioProject is:

- **BioProject:** `PRJNA695560`
- **Study:** *Whole-Genome Sequencing in Two Brothers with Epilepsy*
- **Affected runs:** `SRR13573587` and `SRR13573588`
- **Associated publication:** Badshah et al. (2022), *Novel Missense CNTNAP2 Variant Identified in Two Consanguineous Pakistani Families With Developmental Delay, Epilepsy, Intellectual Disability, and Aggressive Behavior*

The two sequenced individuals are affected brothers from a consanguineous family. The original study used whole-genome sequencing to identify shared homozygous variants associated with their neurological presentation.

## Experimental Objective

The primary objective is to determine whether VAP can execute successfully and coherently on paired-end human WGS data while preserving:

- variant and genotype observations;
- coding, splice, and noncoding consequence surfaces;
- transcript and gene context under the existing VAP policy;
- clinical and population annotations;
- deterministic routing and prioritization;
- execution provenance and TEP-VAP transport fidelity.

A secondary objective is to compare the two affected siblings and assess whether VAP preserves biologically relevant shared candidate structure, including recovery of the published `CNTNAP2` candidate signal.

## Experimental Design

### Phase 1 — Single-run WGS smoke execution

Run VAP first on:

```text
SRR13573587
```

This run will serve as the initial disease-associated WGS execution specimen. The purpose is to verify operational compatibility, resource behavior, stage completion, artifact integrity, and TEP-VAP emission before committing MARK to both genomes.

### Phase 2 — Sibling replication

After successful completion and inspection of the first run, execute VAP on:

```text
SRR13573588
```

The second affected sibling will provide a biologically meaningful replication under closely matched family, sequencing-platform, and disease conditions.

### Phase 3 — Cross-sibling comparison

Compare the two completed VAP runs for:

- shared normalized variants;
- shared homozygous rare variants;
- shared coding, splice, and noncoding candidates;
- shared Tier 1 and Tier 2 candidate structures;
- concordant clinically supported annotations;
- preservation and reviewability of the published `CNTNAP2` signal;
- stage-level and TEP-level reproducibility;
- divergence attributable to sample-specific genotype observations.

### Phase 4 — WES/WGS architectural comparison

Compare the WGS results with the existing epilepsy WES corpus from `PRJEB57558` at the level of pipeline behavior rather than direct cohort association.

Primary questions:

1. Does VAP preserve deterministic stage behavior across WES and WGS substrates?
2. How does WGS alter coding, splice, intronic, regulatory, and intergenic evidence density?
3. Are reviewable candidate surfaces maintained despite the substantially larger WGS search space?
4. Does genotype-aware routing remain coherent under WGS-scale substrate complexity?
5. Are provenance, lineage, and TEP-VAP transport properties preserved?

## Expected Benchmark Surface

The associated publication provides a limited but useful benchmark. VAP should be inspected for recovery and representation of the reported `CNTNAP2` candidate variant and its supporting context.

This is not a strict truth-set benchmark comparable to GIAB HG002. It is a publication-informed concordance target. Failure to prioritize the reported candidate would require investigation of:

- genome assembly and coordinate compatibility;
- variant normalization;
- genotype and zygosity handling;
- transcript-selection policy;
- annotation-resource versions;
- population-frequency thresholds;
- consequence and prioritization rules.

## Success Criteria

The experiment will be considered operationally successful if:

- both paired-end WGS runs complete all required VAP stages;
- no unaccounted variant loss occurs across preservation boundaries;
- genotype observations remain first-class and traceable;
- coding, splice, and noncoding routes remain deterministic;
- validation and lineage artifacts pass;
- TEP-VAP emission preserves source artifact identity and provenance;
- the published `CNTNAP2` signal can be located and scientifically explained, whether or not it reaches the highest VAP priority tier;
- cross-sibling comparison can be reconstructed deterministically from emitted artifacts.

## Scientific Boundaries

This design is a familial WGS execution and evidence-preservation study, not a population association analysis.

The corpus contains only two related affected individuals and does not include sequenced unaffected relatives in the BioProject. Therefore:

- the siblings must not be treated as independent population replicates;
- shared variation may reflect ancestry and consanguinity as well as disease biology;
- no burden, enrichment, penetrance, or causal claims should be made from these two genomes alone;
- publication concordance should not be treated as independent validation;
- VAP may report preserved evidence and candidate convergence, but causal interpretation remains outside the scope of this experiment.

## Intended Scientific Description

The completed work should be described as:

> A familial epilepsy-associated WGS execution and cross-sibling evidence-preservation demonstration using VAP.

It should not be described as a WGS epilepsy cohort study or as independent confirmation of a causal variant.

## References

1. NCBI BioProject `PRJNA695560`: *Whole-Genome Sequencing in Two Brothers with Epilepsy*.
2. Badshah N, et al. (2022). *Novel Missense CNTNAP2 Variant Identified in Two Consanguineous Pakistani Families With Developmental Delay, Epilepsy, Intellectual Disability, and Aggressive Behavior*. Frontiers in Neurology, 13:918022.
3. Touma M, et al. (2013). Whole genome sequencing identifies SCN2A mutation in monozygotic twins with Ohtahara syndrome and unique neuropathologic findings. Epilepsia, 54(5):e81-e85. doi:10.1111/epi.12137
4. Grether A, et al. (2023) The current benefit of genome sequencing compared to exome sequencing in patients with developmental or epileptic encephalopathies. Mol Genet Genomic Med, 11(5):e2148. doi:10.1002/mgg3.2148

