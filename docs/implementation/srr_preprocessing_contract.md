# SRR Preprocessing Behavior Contract
## Repo 2: `variant_annotation_pipeline`
## Target use case: single-SRR acquisition and preparation for paired-end pipeline input

---

## 1. Purpose

This preprocessing workflow prepares a validated paired-end FASTQ input set from an SRA accession for Repo 2.

The workflow is intentionally **separate from the main pipeline**.

It exists to ensure that:

- expensive acquisition and extraction steps are run only when needed
- every heavyweight step is validated before downstream use
- storage state is controlled and predictable
- worker nodes can fail fast with interpretable diagnostics
- only a minimal retained file set remains after successful completion

---

## 2. Separation of Concerns

```text
Preprocessing prepares validated assets.
The main pipeline consumes validated assets.
The main pipeline must never trigger heavyweight acquisition/extraction work implicitly.
```

This means:

- `run_pipeline.py` must not call `prefetch`, `fasterq-dump`, `pigz`, or related prep logic
- preprocessing must be run explicitly by the user or scheduler
- preprocessing may emit a verification report for later audit

---

## 3. Scope

This contract governs:

- initial state cleanup
- storage checks
- SRA download
- SRA validation
- FASTQ extraction
- singleton handling
- paired-end verification
- compression
- post-compression verification
- final cleanup and retention

This contract does **not** govern:

- alignment
- BAM processing
- variant calling
- annotation
- prioritization

Those belong to the main pipeline.

---

## 3A. Run Identifier Contract

Each preprocessing execution must generate a unique `run_id`.

Recommended format:

```text
prep_<SRR>_<YYYY_MM_DD_HHMMSS>
```

The run_id is execution-scoped and must be used for:
- runtime log naming
- runtime structured report naming
- temp directory scoping
- quarantine scoping
- diagnostic traceability

The run_id must not alter the canonical retained data artifact names.

---

## 4. Canonical Retained Outputs

After a successful preprocessing run, the canonical retained data artifacts must be:

1. validated `.sra`
2. validated `_1.fastq.gz`
3. validated `_2.fastq.gz`

These are the canonical retained assets because:

- `.sra` preserves source-level reproducibility and allows regeneration
- `_1.fastq.gz` and `_2.fastq.gz` are the paired inputs required by Repo 2
- all other generated files are regeneratable and should not consume long-term storage

---

## 5. Explicit Non-Retained Outputs

The workflow must remove, after successful verification:

- uncompressed `_1.fastq`
- uncompressed `_2.fastq`
- singleton `.fastq` produced by `--split-3`
- temp files under the configured temp directory
- stale intermediate outputs from failed or prior runs, when safe to remove

---

## 6. Processing Model

The workflow must follow this high-level sequence:

1. preflight / clean-state inspection
2. storage check
3. SRA acquisition
4. SRA validation
5. FASTQ extraction with `--split-3`
6. raw paired FASTQ verification
7. singleton removal
8. core-count inspection
9. paired FASTQ compression
10. compressed paired FASTQ verification
11. provisional audit log emission (pre-cleanup)
12. final cleanup
13. final retained-state verification
14. final audit log update / completion

```text
verification → logging → cleanup → final verification snapshot
```

---

## 7. Idempotence / Reuse Policy

The script must avoid unnecessary reruns of expensive steps.

### Desired behavior

If all retained outputs already exist and pass verification:

- do not re-download
- do not re-extract
- do not recompress
- report success and exit

If retained outputs exist but verification record is absent:

- re-verify current retained outputs
- do not recompute unless verification fails

If outputs are missing or invalid:

- run only the necessary downstream recovery steps

If the user explicitly requests a forced rebuild:

- remove prior derived outputs
- regenerate from a fresh SRA acquisition

If a validated .sra already exists:
    DO NOT re-download.

Only use `prefetch --force all` when:
    - in `--force` mode
    - OR SRA validation fails

Skip all processing ONLY if:
    - .sra exists AND passes validation
    - _1.fastq.gz exists AND passes gzip integrity via `gzip -t`
    - _2.fastq.gz exists AND passes gzip integrity via `gzip -t`
    - compressed line counts match

If .fastq.gz exists but fails gzip -t or line count validation:
    treat as invalid and regenerate

Existing .sra must be revalidated with vdb-validate before reuse.
If validation fails:
    treat as invalid and re-download (or fail)

---

## 8. Execution Modes

The preprocessing utility should support explicit modes.

### `status`
Inspect existing assets and report readiness only.

### `verify-only`
Verify current retained assets without recomputing them.

### `run`
Perform missing steps only.

### `force`
Discard derived outputs and rebuild from a fresh acquisition.

---

## 9. Preflight Contract

Before any heavyweight step runs, the workflow must:

- confirm required external tools exist
- confirm required directories exist or can be created
- inspect available disk space
- inspect available CPU cores
- inspect whether retained outputs already exist
- determine whether work is actually needed

Temp directory must be empty or run_id-scoped.

If temp directory is non-empty and not scoped to current run_id:
- fail by default
- allow override via `--force`


### Required tools

- `prefetch`
- `vdb-validate`
- `fasterq-dump`
- `pigz`
- `wc`
- `zcat`
- `nproc`
- `gzip`

If any required tool is missing:

- fail immediately
- report the missing tool by name

---

## 10. Storage Contract

The workflow must check available storage before extraction.

This must happen before:

- `prefetch`
- `fasterq-dump`
- compression

### Minimum behavior

The workflow must:

- call `df` or equivalent
- record available free space
- compare against a configurable minimum threshold
- fail early if threshold is not met

Before prefetch:
    require absolute free-space threshold

After SRA is present:
    require free space ≥ 3 × SRA size before extraction

### Rationale

SRA extraction and FASTQ compression are large operations and should not begin unless adequate free space exists.

This is especially important on worker nodes.

Temp directory must be namespaced per run_id:

```text
    /mnt/storage/tmp/<run_id>/
```

Cleanup must only remove that scoped directory.

---

## 11. SRA Acquisition Contract

### Process step
Download the accession using `prefetch`.

### Required behavior
- when acquisition is required, use `prefetch --force all` to avoid reuse of partial or cached artifacts
- download into the configured SRA root

### Recommended operational policy
Use:

```text
prefetch <SRR> --force all --output-directory <sra_dir>
```

### SRA storage location
SRA must reside at:
`<sra_dir>/<SRR>/<SRR>.sra`

### Success condition
The expected `.sra` file exists at the configured location.

### Failure condition
If `.sra` is absent after acquisition, fail immediately.

---

## 12. SRA Validation Contract

### Process step
Validate the downloaded `.sra` using `vdb-validate`.

### Success condition
Validation must report the archive as consistent.

### Failure condition
If validation fails:

- mark the accession as unusable
- stop processing
- do not proceed to extraction

---

## 13. Extraction Contract

### Process step
Extract FASTQ using:

```text
fasterq-dump --split-3
```

### Rule
`--split-files` must not be used for this workflow.

### FASTQ naming contract

FASTQ naming must follow:

```text
    <SRR>_1.fastq
    <SRR>_2.fastq
    <SRR>.fastq (for singletons)
```
Compressed outputs must follow:

```text
    <SRR>_1.fastq.gz
    <SRR>_2.fastq.gz
```

### Rationale
`--split-3` isolates singleton/unpaired reads into a separate file and preserves correct paired-end `_1/_2` outputs when the accession contains mixed read structure.

### Success condition
At minimum, the workflow must produce:

- `<SRR>_1.fastq`
- `<SRR>_2.fastq`

Optionally:

- `<SRR>.fastq` (singleton file)

### Failure condition
If either `_1.fastq` or `_2.fastq` is missing, fail immediately.

---

## 14. Raw FASTQ Verification Contract

After extraction and before compression, the workflow must verify the paired FASTQs.

### Required checks

#### File size check
Compare `_1.fastq` and `_2.fastq` sizes.

Rule:
- sizes do not need to be identical
- file sizes must be reasonably close
- file size check is advisory only (log warning, not fail condition)
- log warning if size difference > 20% using this formula:

```text
relative_size_difference = abs(size1 - size2) / max(size1, size2)
warn if relative_size_difference > 0.20
```

This check is heuristic only.

#### Line count check
Run `wc -l` on `_1.fastq` and `_2.fastq`.

Rule:
- line counts must be equal
- each must be divisible by 4

This is the primary paired-end integrity check.

#### Singleton inspection
If `<SRR>.fastq` exists:
- record its existence
- record its line count
- do not use it as pipeline input

### Failure condition
If `_1` and `_2` line counts differ, fail immediately.

---

## 15. Singleton Handling Contract

If a singleton file exists after `--split-3`:

- record that it was produced
- optionally record its line count and size
- remove it before compression of retained paired-end assets

### Rationale
Repo 2 v1 is a strict paired-end pipeline and does not consume singleton reads.

Singletons are treated as out-of-scope derived artifacts.

---

## 16. Multicore / Compression Contract

Before compression, inspect available CPU cores using `nproc`.

### Required behavior
- record total logical cores
- choose a configurable `pigz` thread count
- do not assume all nodes have the same hardware

### Default compression thread behavior

Default:

```bash
    pigz_threads = max(1, floor(nproc / 2))
```

Allow override via config/CLI.

### Compression step
Compress `_1.fastq` and `_2.fastq` using `pigz`.

### Success condition
Both `_1.fastq.gz` and `_2.fastq.gz` must exist after compression.

### Failure condition
If either compressed file is missing, fail immediately.

## FASTQ gzip naming rule:

```text
<SRR>_1.fastq.gz
<SRR>_2.fastq.gz
```

---

## 17. Compressed FASTQ Verification Contract

After compression, verify the `.fastq.gz` files.

### Required checks

- gzip integrity check:

```bash
gzip -t file.fastq.gz
```
-  content validation check (compressed lines)

```bash
zcat <file> | wc -l
```

### Rule
The compressed `_1` and `_2` line counts must still be equal.

### Failure condition
If compressed counts differ, fail immediately.

---

## 18. Final Cleanup Contract

After successful compression, compressed verification, and provisional report emission, remove:

- `_1.fastq`
- `_2.fastq`
- singleton `.fastq`
- temporary extraction files
- configured temp directory contents associated with this run

Temp directory must be namespaced per run_id:
    /mnt/storage/tmp/<run_id>/

Cleanup must only remove that run_id-scoped directory.

### Critical rule
Do **not** remove:

- `.sra`
- `_1.fastq.gz`
- `_2.fastq.gz`

This corrects the contradiction in the original notes.

---

## 19. Final State Verification Contract

At the end of a successful run, the canonical retained data artifacts must be:
- <sra_dir>/<SRR>/<SRR>.sra
- <fastq_dir>/<SRR>_1.fastq.gz
- <fastq_dir>/<SRR>_2.fastq.gz

Additional retained audit artifacts may include:
- <fastq_dir>/logs/<run_id>.prep.log
- <fastq_dir>/logs/<run_id>.prep.json

---

## 20. Logging / Audit Contract

The workflow must write a persistent log and structured summary.

Logs must be written to:
`<fastq_dir>/logs/<run_id>.prep.log`

Structured report:
`<fastq_dir>/logs/<run_id>.prep.json`

### Human-readable log
Record:
- timestamps
- commands run
- pass/fail outcome of each phase
- key sizes and counts
- cleanup actions

### Structured report
Recommended JSON or TSV report including:
- run_id
- start_time
- end_time
- duration_seconds
- phase_status_map
- accession
- SRA path
- FASTQ output paths
- raw line counts
- compressed line counts
- singleton present / removed
- free-space snapshot
- core count
- pigz threads used
- overall success/failure
- failure reason if any
- execution mode (status, verify-only, run, force)
- whether work was skipped
- which phases actually executed
- whether existing assets were reused

For logging/debugging, add phase name to every step:
1. PHASE: preflight
2. PHASE: storage check
3. PHASE: sra acquisition
4. PHASE: sra validation
5. PHASE: fastq extraction
6. PHASE: raw paired fastq verification
7. PHASE: singleton removal
8. PHASE: core-count inspection
9. PHASE: paired fastq compression
10. PHASE: compressed paired fastq verification
11. PHASE: provisional audit log emission (pre-cleanup)
12. PHASE: final cleanup
13. PHASE: final retained-state verification
14. PHASE: final audit log update / completion

---

## 21. Node Portability Contract

The workflow must not assume that worker nodes match the developer workstation.

It must therefore:

- inspect local cores dynamically
- inspect local storage dynamically
- not hardcode thread counts
- not assume abundant temp space
- fail fast with explicit messages when prerequisites are not met

---

## 22. Repo 2 v1 Dataset-Specific Rule

For `SRR12898354`, preprocessing must use `--split-3` and retain only the validated paired compressed FASTQs plus the validated SRA.

This rule is based on observed accession behavior:
- paired mates are balanced only under `--split-3`
- singleton reads exist and are separated into an extra file
- singleton reads are not consumed by Repo 2 v1

---

## 23. Checksum Recording:

Record SHA256 of:
- .sra
- _1.fastq.gz
- _2.fastq.gz

---

## 24. Timing Metrics

Record:
- extraction duration
- compression duration

---

## 25. Version Capture

Record versions of:
- fasterq-dump
- pigz
- vdb-validate
- prefetch

---

## 26. Global Failure Policy

A run is considered valid ONLY if:
    - all final validation checks pass
    - final retained-state verification completes

Any interruption before that point must be treated as a failed run.

Default failure behavior:
- move partial derived FASTQ artifacts to <fastq_dir>/quarantine/<run_id>/
- do not quarantine the validated .sra
- allow CLI/config override to delete instead of quarantine

Partial derived artifacts include:
- any .fastq or .fastq.gz files for the SRR that fail validation
- any FASTQ files produced before successful paired validation
- incomplete compression outputs

Do NOT move:
- validated .sra
- validated paired .fastq.gz outputs

On failure:
- mark run as failed
- do NOT treat partial outputs as valid

Temporary extraction files under <tmp_dir>/<run_id>/ may be deleted directly and do not need quarantine.

Quarantine directory:
`<fastq_dir>/quarantine/<run_id>/`

---

## 27. Summary Rule

```text
Only run expensive preprocessing when required.
Validate every expensive step before proceeding.
Retain only the SRA and validated paired .fastq.gz outputs.
Never let the main pipeline perform implicit acquisition or extraction.
```

---

# End of SRR Preprocessing Behavior Contract