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
* avoid dropping biologically or operationally meaningful fields
* avoid overwriting existing manifests in output directory (`data/reference/sra_support/manifests/<bioproject_lower>/`)

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
* avoid downloading files.

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
* support semicolon-delimited paired FASTQ URLs;
* use polite download behavior;
* support resumable downloads;
* avoid overwriting existing validated FASTQs;
* quarantine or report failed integrity checks;
* continue past individual download failures;
* log all download decisions.

Default input should be:
data/reference/sra_support/<bioproject_lower>/<bioproject_lower>_selected_9_runs.tsv

Script C must not default to downloading the full topology manifest unless explicitly supplied by the operator.

## Output

FASTQs are written to:

```text
/data/storage/fastq
```

Logs are written to the same output directory:

```text
download_session_<TIMESTAMP>.log
download_failures_<TIMESTAMP>.log
gzip_integrity_<TIMESTAMP>.log
```

## Contract Rule

This script performs transfer only. It must not rank runs, select runs, calculate scientific design features, or modify the selected manifest.

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
        └── gzip_integrity_<timestamp>.log
```

Notes:

- Script A writes to manifests/<bioproject_lower>/
- Script B writes to selections/<bioproject_lower>/
- Script C only writes logs to download_logs/<bioproject_lower>
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

## Python Boundary

This trilogy remains Bash-based while it lives under VAP `scripts/resources/`.

Equivalent ingestion, selection, and acquisition logic may later be promoted into Python under VDB `/src` when it becomes part of the VDB repository spine.

## Cross-Script Operational Conventions

All scripts must:

- read TSV inputs by header name, not column position;
- write timestamped logs to their primary output/destination directory;
- preserve timestamped outputs before updating stable latest-copy outputs;
- fail loudly on missing required columns;
- avoid silent overwrite of existing trusted artifacts;
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

Script C uses polite, resumable, low-priority wget for FASTQ downloads.

Ideal Usage for Script C:

```bash
nice -n 19 ionice -c2 -n7 wget -c \
  --limit-rate=20m "$URL" -P "$OUTDIR"
```

---

# Design Rationale

The trilogy intentionally prevents three common failure modes:

1. **Provenance drift** — avoided by preserving Script A outputs.
2. **Pretty-table operational drift** — avoided by making Script B a documented derived manifest generator.
3. **Downloader overreach** — avoided by keeping Script C as execution-only.

This allows SAGE-VAP or SAGE-RDGP to identify additional BioProjects, after which the same trilogy can harvest topology, select representative SRAs by sequencing depth/breadth, and acquire FASTQ substrate for VAP execution.
