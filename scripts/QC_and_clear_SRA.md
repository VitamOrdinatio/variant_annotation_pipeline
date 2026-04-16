### non-functional script to check and clear SRA files from /mnt/storage/sra

### QC measures for SRA files in /mnt/storage/sra:

## Nuclear option (clean slate):
# 1. Remove the current broken FASTQs without touching SRAs
rm -f /mnt/storage/fastq/SRR12898354_1.fastq.gz
rm -f /mnt/storage/fastq/SRR12898354_2.fastq.gz
rm -f /mnt/storage/fastq/SRR12898354_1.fastq
rm -f /mnt/storage/fastq/SRR12898354_2.fastq
rm -rf /mnt/storage/tmp/*

# 2. Clean pipeline reset (remove SRA, FASTQ, and temp files):
rm -rf /mnt/storage/sra/SRR12898354
rm -f /mnt/storage/fastq/SRR12898354_*.fastq*
rm -rf /mnt/storage/tmp/*

# 2b. Check if disk has enough storage:
df -h /mnt/storage/
#Filesystem      Size  Used Avail Use% Mounted on
#/dev/nvme1n1p1  1.8T   62G  1.8T   4% /mnt/storage

# 3. Get SRA file again de novo (force all):
prefetch SRR12898354 --max-size 100G --force all --output-directory /mnt/storage/sra
# 4. Validate the new SRA file before reuse:
vdb-validate /mnt/storage/sra/SRR12898354/SRR12898354.sra

## If it looks good, console output should look like this:
#2026-04-16T05:01:51 vdb-validate.3.0.3 info: Database 'SRR12898354.sra' metadata: md5 ok
#2026-04-16T05:01:51 vdb-validate.3.0.3 info: Table 'SEQUENCE' metadata: md5 ok
#2026-04-16T05:01:57 vdb-validate.3.0.3 info: Column 'ALTREAD': checksums ok
#2026-04-16T05:02:09 vdb-validate.3.0.3 info: Column 'QUALITY': checksums ok
#2026-04-16T05:02:21 vdb-validate.3.0.3 info: Column 'READ': checksums ok
#2026-04-16T05:02:21 vdb-validate.3.0.3 info: Column 'READ_LEN': checksums ok
#2026-04-16T05:02:21 vdb-validate.3.0.3 info: Column 'READ_TYPE': checksums ok
#2026-04-16T05:02:21 vdb-validate.3.0.3 info: Database '/mnt/storage/sra/SRR12898354/SRR12898354.sra' contains only unaligned reads
#2026-04-16T05:02:21 vdb-validate.3.0.3 info: Database 'SRR12898354.sra' is consistent

########### DO NOT USE split-files in our production pipeline, use split-3)
# 5. Re-run the fasterq-dump cleanly using the accession directory not the bare .sra path:
fasterq-dump /mnt/storage/sra/SRR12898354/SRR12898354.sra \
  --split-files \
  --threads 8 \
  --temp /mnt/storage/tmp \
  -O /mnt/storage/fastq
# output should look like this:
# spots read      : 393,504,877
# reads read      : 787,009,754
# reads written   : 606,865,536
# reads 0-length  : 180,144,218   <-- this is a red flag, but may be expected for some datasets. Check the SRA metadata for expected read counts and lengths.
########### Do not use split-files in our production pipeline, use split-3)


# 6A. Check that the file sizes of the paired FASTQ files match:
ls /mnt/storage/fastq/ -lh

## Example of mismatched file sizes:  Note the large size difference between the R1 and R2 files, which is a red flag:

#total 193G
#-rw-rw-r-- 1 steelsparrow steelsparrow 125G Apr 16 01:21 SRR12898354_1.fastq
#-rw-rw-r-- 1 steelsparrow steelsparrow  68G Apr 16 01:19 SRR12898354_2.fastq

## For this particular SRA, the metadata indicates that there should be 393,504,877 spots (paired reads), which means we should expect approximately 787 million reads in total (393 million in R1 and 393 million in R2). The large size difference suggests that one of the files may be incomplete or corrupted.
## Alternatively, this SRA has a large number of singleton reads, and I need to use the split-3 method

# Delete the problematic FASTQ files and re-run fasterq-dump with the --split-3 option to handle singleton reads:
rm -f /mnt/storage/fastq/SRR12898354_1.fastq
rm -f /mnt/storage/fastq/SRR12898354_2.fastq

########################################################
########################################################

### Use split-3 to handle singleton reads, which will create an additional file for unpaired reads if they exist:
fasterq-dump /mnt/storage/sra/SRR12898354/SRR12898354.sra \
  --split-3 \
  --threads 8 \
  --temp /mnt/storage/tmp \
  -O /mnt/storage/fastq

#spots read      : 393,504,877
#reads read      : 787,009,754
#reads written   : 606,865,536
#reads 0-length  : 180,144,218

## Check the new file sizes:
ls /mnt/storage/fastq/ -lh
#total 193G
#-rw-rw-r-- 1 steelsparrow steelsparrow 68G Apr 16 01:57 SRR12898354_1.fastq
#-rw-rw-r-- 1 steelsparrow steelsparrow 68G Apr 16 01:57 SRR12898354_2.fastq
#-rw-rw-r-- 1 steelsparrow steelsparrow 58G Apr 16 01:57 SRR12898354.fastq

# Check line counts before compression to confirm that the paired files have the expected number of reads:
wc -l /mnt/storage/fastq/SRR12898354_1.fastq /mnt/storage/fastq/SRR12898354_2.fastq /mnt/storage/fastq/SRR12898354.fastq
#   853442636 /mnt/storage/fastq/SRR12898354_1.fastq
#   853442636 /mnt/storage/fastq/SRR12898354_2.fastq
#   720576872 /mnt/storage/fastq/SRR12898354.fastq    <- singletons
#  2427462144 total

# Since the line counts match, then compress them using pigz which can handle multiple cores.

# But first, remove the singleton file (we don't need it):
rm -f /mnt/storage/fastq/SRR12898354.fastq

#### Operating Rule Contract Notes  ####################
### Rule: keep the prefectched split-3 SRA (for replication / validation purposes)
### Rule: keep only the _1.fastq.gz and _2.fastq.gz files in the fastq folder)
#### Operating Rule Contract Notes ##################

nproc # check number of available threads, e.g. 8

# Compressing with pigz using 8 threads:
pigz -p 8 /mnt/storage/fastq/SRR12898354_1.fastq
pigz -p 8 /mnt/storage/fastq/SRR12898354_2.fastq

############## Note that the pigz method will:
# 1) generate a .fastq.gz file and
# 2) delete the uncompressed .fastq file

# 8. Re-check compressed counts:
zcat /mnt/storage/fastq/SRR12898354_1.fastq.gz | wc -l
zcat /mnt/storage/fastq/SRR12898354_2.fastq.gz | wc -l

## should get for both files the same line count of 853,442,636, which confirms that the paired files are consistent and complete after compression: 
## zcat /mnt/storage/fastq/SRR12898354_1.fastq.gz | wc -l
### 853442636
## zcat /mnt/storage/fastq/SRR12898354_2.fastq.gz | wc -l
### 853442636


## Build a bash script for future SRAs, that uses this safety pattern:
# 1) process: download SRA
# 2) validate: inspect SRA (vdb-validate)
# 3) process: fasterq-dump (split-3)
# 4) process: remove singleton files
# 5) validate: compare raw FASTQ file sizes
# 6) validate: compare raw FASTQ line counts
# 7) process: compress fastq (pigz) to get .fastq.gz files
# 8) validate: compare compressed FASTQ line counts (zcat + wc -l)
# 9) clean up: remove all generated files except the .sra and .fastq.gz for _1 and _2

## The last step is particularly important for 3 reasons:
# 1) keeping SRA allows for replication and validation
# 2) keeping .fastq.gz files allows for input into the pipeline (repo2 replication)
# 3) removing all other files keeps a minimal storage footprint
## Search SWE agent for "1. Preflight" to resume retooling the download_and_prepare_srr.sh
