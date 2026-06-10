# VAP BioProject FASTQ Acquisition Trilogy Contract

## Purpose

This script trilogy supports VAP substrate acquisition from public BioProjects by separating:

1. provenance-safe BioProject manifest harvesting,
2. scientific/sample-selection manifest generation,
3. polite FASTQ download execution.

The core design principle is that provenance capture, experimental selection, and file transfer must remain distinct operations.

---

# Script A: `harvest_bioproject_run_manifest.sh`

## Role

Polite provenance manifest harvester.

## Input

A user-supplied BioProject accession.

Example:

```bash
./scripts/resources/harvest_bioproject_run_manifest.sh prjeb57558
```

## Behavior

The script politely queries ENA for the BioProject’s `read_run` metadata, discovers available fields, downloads the full run-level manifest, and writes provenance-preserving outputs.

It must:

* run politely using retry-aware, low-priority `curl`;
* obey MARK shared I/O expectations;
* preserve timestamped outputs;
* write stable latest-copy outputs;
* avoid scientific selection;
* avoid manual curation;
* avoid dropping biologically or operationally meaningful fields;
* rotate existing stable latest-copy manifests to `.backup` before replacement after successful validation;
* avoid silent overwrite of existing manifests in output directory.

Timestamped provenance manifests must never be overwritten.

Stable latest-copy operational manifests (`*.tsv`, `*.txt`) may be rotated to a `.backup` version before replacement, but only after newly generated timestamped outputs successfully pass validation.

If an existing `.backup` file already exists, it may be replaced by the newly rotated prior stable manifest.


## Output

Primary outputs under:

```text
data/reference/sra_support/manifests/<bioproject_lower>/
```

Expected outputs:

```text
<bioproject_lower>_read_run_fields_<TIMESTAMP>.txt
<bioproject_lower>_all_runs_<TIMESTAMP>.tsv
<bioproject_lower>_runs_topology_<TIMESTAMP>.tsv
<bioproject_lower>_read_run_fields.txt
<bioproject_lower>_all_runs.tsv
<bioproject_lower>_runs_topology.tsv
<bioproject_lower>_manifest_harvest_<TIMESTAMP>.log
```

Provenance Note:

```text
<bioproject_lower>_all_runs.tsv is the full provenance manifest and must preserve all harvested fields. 

<bioproject_lower>_runs_topology.tsv is a minimally cleaned operational topology view where completely empty columns may be dropped.
```

## Contract Rule

This script produces the authoritative provenance manifest. It must not decide which runs are scientifically preferred for VAP execution.

---

# Script B: `select_bioproject_runs_by_depth.sh`

## Role

Scientific selection and human-facing manifest generator.

## Input

The provenance topology manifest from Script A.

Example:

```bash
./scripts/resources/select_bioproject_runs_by_depth.sh \
  data/reference/sra_support/manifests/prjeb57558/prjeb57558_runs_topology.tsv
```

## Behavior

The script derives a compact selected-run manifest for VAP substrate acquisition.

It must:

* read Script A output by header name;
* require `run_accession`, `read_count`, `base_count`, `library_layout`, and `fastq_ftp`;
* calculate `rank_%` from `read_count`;
* support selection of runs near target depth strata;
* preserve enough operational columns for download;
* preserve enough scientific columns for human review;
* document derived fields in the output header or log;
* rotate existing stable latest-copy selected manifests to `.backup` before replacement after successful validation;
* avoid downloading files.

Timestamped selected manifests must never be overwritten.

Stable latest-copy selected manifests may be rotated to a `.backup` version before replacement, but only after newly generated timestamped outputs successfully pass validation.

If an existing `.backup` file already exists, it may be replaced by the newly rotated prior stable manifest.

Default scientific design:

```text
3 runs near Q1 depth/breadth
3 runs near median depth/breadth
3 runs near Q3 depth/breadth
```

Script B must log:
- source manifest path;
- total eligible runs;
- excluded runs and exclusion reasons;
- rank method;
- target strata;
- selected runs per stratum;
- output manifest path.

## Output

Expected output under:

```text
data/reference/sra_support/selections/<bioproject_lower>/
```

Example:

```text
prjeb57558_selected_9_runs.tsv
prjeb57558_selected_9_runs_<TIMESTAMP>.tsv
prjeb57558_run_selection_<TIMESTAMP>.log
```

Expected selected manifest columns may include:

```text
run_accession
sample_accession
experiment_accession
study_accession
library_strategy
library_layout
library_source
library_selection
instrument_model
read_count
rank
rank_%
depth_category
base_count
fastq_bytes
fastq_md5
fastq_ftp
```

## Contract Rule

This script is the only member of the trilogy allowed to make scientific/sample-selection decisions. Its output may become Script C input, but it must remain traceable to Script A.

---

# Script C: `download_selected_fastqs_polite.sh`

## Role

Polite FASTQ downloader.

## Input

A selected-run manifest produced by Script B.

Example:

```bash
./scripts/resources/download_selected_fastqs_polite.sh \
  data/reference/sra_support/selections/<bioproject_lower>/<bioproject_lower>_selected_9_runs.tsv
```

## Behavior

The script downloads FASTQs listed in the selected manifest.

It must:

* read required columns by header name;
* require `run_accession`, `library_layout`, and `fastq_ftp`;
* use `fastq_md5` for checksum validation when available;
* preserve `fastq_bytes` when available for logging and audit context;
* support semicolon-delimited paired FASTQ URLs;
* use polite download behavior;
* support resumable downloads only for temporary `.part` files;
* treat existing final FASTQ files as immutable trusted substrate;
* never overwrite, modify, resume into, rename, or delete an existing final FASTQ file;
* validate existing final FASTQs using gzip integrity and, when available, MD5 checksum;
* log existing final FASTQs as pass or fail without modifying them;
* download missing FASTQs into an incomplete temporary location;
* validate newly downloaded temporary files using gzip integrity and, when available, MD5 checksum;
* promote validated temporary files into the final FASTQ directory only after all required validations pass;
* quarantine or retain failed temporary downloads for manual operator review;
* continue past individual download failures;
* log all download decisions;
* require gzip integrity validation for all existing and newly downloaded FASTQ files;
* treat `fastq_md5` and `fastq_bytes` as optional validation fields;
* validate MD5 only when `fastq_md5` is present;
* validate file size only when `fastq_bytes` is present;
* log missing `fastq_md5` or `fastq_bytes` as warnings, not failures;


## Output

FASTQs are written to:

```text
/data/storage/fastq
```

Temporary resumable downloads are written to:

```text
/data/storage/fastq/.incomplete
```

Logs are written to:

```text
data/reference/sra_support/download_logs/<bioproject_lower>/
```

Expected logs:

```text
download_session_<TIMESTAMP>.log
download_failures_<TIMESTAMP>.log
gzip_integrity_<TIMESTAMP>.log
md5_integrity_<TIMESTAMP>.log
existing_fastq_audit_<TIMESTAMP>.log
```

## Contract Rule

This script performs transfer and validation only. It must not rank runs, select runs, calculate scientific design features, modify the selected manifest, or modify any existing final FASTQ file in `/data/storage/fastq`.

Script C should use `set -uo pipefail` rather than `set -euo pipefail` so row-level transfer or validation failures can be logged without aborting the entire manifest-driven download session.

---

# Manifest Rotation Policy

## Scope

Manifest rotation only occurs for execution of:

- script A (`harvest_bioproject_run_manifest.sh`)
- script B (`select_bioproject_runs_by_depth.sh`)

## Exclusion

Manifest rotation functionality does not exist for script C (`download_selected_fastqs_polite.sh`)

## Behavior

Manifest rotation proceeds procedurally:

  1. Generate timestamped output.
  2. Validate timestamped output.
  3. If validation passes:
     a. rotate existing stable file to .backup
     b. copy timestamped output to stable canonical filename
  4. If validation fails:
     a. leave old stable file untouched
     b. do not rotate anything

Thus the validation target is always

```text
the new timestamped manifest.
```

Stable latest-copy manifests inherit operational trust only from successfully validated timestamped outputs.

## Example Rotation for Script A

For Script A, validation checks the following newly timestamped files:

- `prjeb57558_all_runs_YEAR_MO_DAY_XXXXXX.tsv`
- `prjeb57558_runs_topology_YEAR_MO_DAY_XXXXXX.tsv`

  * If validation passes, and `prjeb57558_all_runs.tsv` already exists, then:
    - then rotate previous `prjeb57558_all_runs.tsv` to `prjeb57558_all_runs.tsv.backup`, overwriting any existing `prjeb57558_all_runs.tsv.backup` file
    - then update `prjeb57558_all_runs.tsv` with the newly timestamped and validated `prjeb57558_all_runs_YEAR_MO_DAY_XXXXXX.tsv`


  * If validation passes, and `prjeb57558_runs_topology.tsv` already exists, then:
    - then rotate previous `prjeb57558_runs_topology.tsv` to `prjeb57558_runs_topology.tsv.backup`, overwriting any existing `prjeb57558_runs_topology.tsv.backup` file
    - then update `prjeb57558_runs_topology.tsv` with the newly timestamped and validated `prjeb57558_runs_topology_YEAR_MO_DAY_XXXXXX.tsv`

## Example Rotation for Script B

For Script B, validation checks the following newly timestamped file:

- `prjeb57558_selected_9_runs_YEAR_MO_DAY_XXXXXX.tsv`

  * If validation passes, and `prjeb57558_selected_9_runs.tsv` already exists, then:
    - then rotate previous `prjeb57558_selected_9_runs.tsv` to `prjeb57558_selected_9_runs.tsv.backup`, overwriting any existing `prjeb57558_selected_9_runs.tsv.backup` file
    - then update `prjeb57558_selected_9_runs.tsv` with the newly timestamped and validated `prjeb57558_selected_9_runs_YEAR_MO_DAY_XXXXXX.tsv`

---

# End-to-End Data Flow

```text
BioProject accession
        ↓
harvest_bioproject_run_manifest.sh
        ↓
<bioproject_lower>_runs_topology.tsv
        ↓
select_bioproject_runs_by_depth.sh
        ↓
<bioproject_lower>_selected_9_runs.tsv
        ↓
download_selected_fastqs_polite.sh
        ↓
/data/storage/fastq/*.fastq.gz
```

---

# Example VAP Repository Directory Structure

```text
data/reference/sra_support/
├── README.md
├── manifests/
│   └── prjeb57558/
│       ├── prjeb57558_all_runs.tsv
│       ├── prjeb57558_all_runs_<timestamp>.tsv
│       ├── prjeb57558_runs_topology.tsv
│       ├── prjeb57558_runs_topology_<timestamp>.tsv
│       ├── prjeb57558_read_run_fields.txt
│       ├── prjeb57558_read_run_fields_<timestamp>.txt
│       └── logs/
│           └── prjeb57558_manifest_harvest_<timestamp>.log
├── selections/
│   └── prjeb57558/
│       ├── prjeb57558_selected_9_runs.tsv
│       ├── prjeb57558_selected_9_runs_<timestamp>.tsv
│       └── logs/
│           └── prjeb57558_run_selection_<timestamp>.log
└── download_logs/
    └── prjeb57558/
        ├── download_session_<timestamp>.log
        ├── download_failures_<timestamp>.log
        ├── existing_fastq_audit_<timestamp>.log
        ├── gzip_integrity_<timestamp>.log                
        └── md5_integrity_<timestamp>.log
```

Notes:

- Script A writes to manifests/<bioproject_lower>/
- Script B writes to selections/<bioproject_lower>/
- Script C writes operational logs to download_logs/<bioproject_lower>
- Script C downloads fastq files to MARK's `/data/storage/fastq`
- Each <bioproject_lower> is a nested subfolder within manifests/, selections/, or download_logs/

---

# Detailed Typical Workflow

A typical usage of these three sequential bash scripts in VAP would look like this, assuming PRJEB57558 as the target:

1) User supplies BioProject accession to Script A and runs Script A.
   - Currently script A is hardcoded with PRJEB57558 but can be changed in future versions.
   - Script A politely utilizes `curl` to interface with the EBI / ENA server.

2) Script A execution outputs several manifest and log files to the `<VAP repo>/data/reference/sra_support/manifests/prjeb57558` folder.  
   - Of note, Script A generates a manifest file called `prjeb57558_runs_topology.tsv`, which is stored in the `<VAP repo>/data/reference/sra_support/manifests/prjeb57558/` folder.

3) User then executes Script B which ingests the `<VAP repo>/data/reference/sra_support/manifests/prjeb57558/prjeb57558_runs_topology.tsv` file.

4) Script B execution outputs TSV and log files to the `<VAP repo>/data/reference/sra_support/selections/prjeb57558/` folder.
    - Of note, Script B generates the `prjeb57558_selected_9_runs.tsv` file based on `rank_%` logic derived from `read_count` distributions for all SRAs of the BioProject PRJEB57558.

5) User then executes Script C which politely downloads FASTQ files using `wget` to MARK's target `/data/storage/fastq/` directory driven by the `prjeb57558_selected_9_runs.tsv` file found in the `<VAP repo>/data/reference/sra_support/selections/prjeb57558/` folder.  

6) User can check the log files in three locations.
   - Log files written to <VAP repo>/data/reference/sra_support/manifests/<bioproject_lower>/logs/ will indicate Script A activity.
   - Log files written to <VAP repo>/data/reference/sra_support/selections/<bioproject_lower>/logs/ will indicate Script B activity.
   - Log files written to <VAP repo>/data/reference/sra_support/download_logs/<bioproject_lower>/ will indicate Script C activity.

---

# Boundary Rules

## Provenance Boundary

Only Script A talks directly to ENA for manifest harvesting.

## Scientific Selection Boundary

Only Script B calculates ranking, `rank_%`, quartile proximity, or selected-run manifests.

## Transfer Boundary

Only Script C downloads FASTQ files.

## Operational Safety Boundary

Scripts intended to write to MARK shared storage must include MARK guardrails unless explicitly run with an override such as:

```bash
ALLOW_NON_MARK=1
```

## FASTQ Immutability Boundary

Existing final FASTQ files under `/data/storage/fastq` are immutable VAP substrate.

If a manifest-listed FASTQ already exists, Script C may inspect it using gzip integrity and checksum validation, but must not overwrite, resume into, rename, delete, or repair it.

Existing FASTQs that fail validation must be logged for manual operator review.

New downloads must first be written to a temporary incomplete path and promoted to the final FASTQ directory only after required validations pass.

## Python Boundary

This trilogy remains Bash-based while it lives under VAP `scripts/resources/`.

Equivalent ingestion, selection, and acquisition logic may later be promoted into Python under VDB `/src` when it becomes part of the VDB repository spine.

## Cross-Script Operational Conventions

Stable latest-copy manifests represent the current canonical operational handoff artifacts between scripts.

Timestamped manifests remain the authoritative provenance-preserving historical artifacts and must never be modified or overwritten.

All scripts must:

- read TSV inputs by header name, not column position;
- write timestamped logs to their primary output/destination directory;
- preserve timestamped outputs before updating stable latest-copy outputs;
- fail loudly on missing required columns;
- avoid silent overwrite or silent rotation of existing trusted artifacts;
- tolerate row-level failures where appropriate;
- record enough information in logs to reconstruct what was attempted, skipped, selected, downloaded, or failed.

### Network and Storage Policy on MARK

Network and storage-touching commands must run at low priority on MARK. FASTQ downloads must use:

```bash
nice -n 19 ionice -c2 -n7 wget -c --limit-rate=20m
```

This allows resume behavior in case of timeout, and manifest harvest commands using curl should use equivalent low-priority execution and conservative retry behavior.

Script A uses polite, retry-aware, low-priority curl for ENA API manifest harvesting.

Ideal Usage for Script A:

```bash
nice -n 19 ionice -c2 -n7 curl \
  --fail --location --silent --show-error \
  --retry 5 --retry-delay 10 \
  --limit-rate 5M \
  -G "https://www.ebi.ac.uk/ena/portal/api/filereport" \
  ...
```

Script C uses polite, resumable, low-priority wget for temporary downloads only.

Ideal download behavior for Script C:

```bash
nice -n 19 ionice -c2 -n7 wget -c \
  --limit-rate=20m "$URL" -O "$PART_FILE"
```

```text
$PART_FILE must live under /data/storage/fastq/.incomplete/, not directly in the final FASTQ substrate directory.
```

---

# Design Rationale

The trilogy intentionally prevents three common failure modes:

1. **Provenance drift** — avoided by preserving Script A outputs.
2. **Pretty-table operational drift** — avoided by making Script B a documented derived manifest generator.
3. **Downloader overreach** — avoided by keeping Script C as execution-only.

This allows SAGE-VAP or SAGE-RDGP to identify additional BioProjects, after which the same trilogy can harvest topology, select representative SRAs by sequencing depth/breadth, and acquire FASTQ substrate for VAP execution.
