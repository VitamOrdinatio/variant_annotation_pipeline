# Note: this is not yet a script, but rather a set of script snippets that have been tested
# Note: we actually do not need PRJEB57558_samples_topology.tsv (it's empty)
# Note: we actually do want PRJEB57558_runs_topology.tsv (it has all the metadata about the sequencing runs, instruments, and files)
#
# Script goals:
# 1. Script is currently hardwired to work with BioProject: PRJEB57558
# 2. Script queries ENA API to discover all possible fields for Runs and Samples
# 3. Script then retrives all data for every single field for both Runs and Samples, generating two large TSV files
# 4. Script then cleans up the TSV files by dropping any columns that are completely empty
# 5. Script then removes the original bulky TSV files, leaving only the cleaned versions for downstream use


# STEP 1: Discover All Possible Fields for PRJEB57558

# Define safe text segments to prevent system URL truncation
BASE="https://www"
DOMAIN="ebi.ac.uk"
API_PATH="/ena/portal/api/returnFields"

# Extract Run and Sample fields using standard Python (Zero dependencies needed)
FIELDS_RUN=$(python3 -c "
import urllib.request, json
url = '${BASE}.${DOMAIN}${API_PATH}?result=read_run&format=json'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as r:
    data = json.loads(r.read().decode())
print(','.join([item['columnId'] for item in data]))
")

FIELDS_SAMPLE=$(python3 -c "
import urllib.request, json
url = '${BASE}.${DOMAIN}${API_PATH}?result=sample&format=json'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as r:
    data = json.loads(r.read().decode())
print(','.join([item['columnId'] for item in data]))
")

# Print the verified counts to your screen
echo "Total discoverable Run columns: $(echo "$FIELDS_RUN" | tr ',' '\n' | wc -l)"
echo "Total discoverable Sample columns: $(echo "$FIELDS_SAMPLE" | tr ',' '\n' | wc -l)"

# You should get in console:
#
# Total discoverable Run columns: 195
# Total discoverable Sample columns: 104





# STEP 2: Download Everything for PRJEB57558

# Define the data download path safely
REPORT_PATH="/ena/portal/api/filereport"
URL_REPORT="${BASE}.${DOMAIN}${REPORT_PATH}"

# 1. Download all data points for Sequencing Runs and Samples
curl -sG "$URL_REPORT" --data-urlencode "accession=PRJEB57558" --data-urlencode "result=read_run" --data-urlencode "fields=$FIELDS_RUN" --data-urlencode "format=tsv" > PRJEB57558_all_runs.tsv
curl -sG "$URL_REPORT" --data-urlencode "accession=PRJEB57558" --data-urlencode "result=sample" --data-urlencode "fields=$FIELDS_SAMPLE" --data-urlencode "format=tsv" > PRJEB57558_all_samples.tsv

# 2. Clean up empty data fields using pure Bash/Awk
awk -F'\t' 'NR==1{split($0,h);next} {for(i=1;i<=NF;i++) if($i!="") d[i]=1} END{p=0; for(i=1;i<=length(h);i++) if(i in d){printf (p?"\t":"")"%s",h[i]; p=1} print ""; while((getline<"PRJEB57558_all_runs.tsv")>0){if(FNR==1)continue; p=0; for(i=1;i<=NF;i++) if(i in d){printf (p?"\t":"")"%s",$i; p=1} print ""}}' PRJEB57558_all_runs.tsv > PRJEB57558_runs_topology.tsv
awk -F'\t' 'NR==1{split($0,h);next} {for(i=1;i<=NF;i++) if($i!="") d[i]=1} END{p=0; for(i=1;i<=length(h);i++) if(i in d){printf (p?"\t":"")"%s",h[i]; p=1} print ""; while((getline<"PRJEB57558_all_samples.tsv")>0){if(FNR==1)continue; p=0; for(i=1;i<=NF;i++) if(i in d){printf (p?"\t":"")"%s",$i; p=1} print ""}}' PRJEB57558_all_samples.tsv > PRJEB57558_samples_topology.tsv

# Clean up raw bulky dump files
#rm PRJEB57558_all_runs.tsv PRJEB57558_all_samples.tsv

echo "Files generated successfully! Check your workspace for 'PRJEB57558_runs_topology.tsv' and 'PRJEB57558_samples_topology.tsv'."




# Download every single data point regarding the sequencing files, instruments, and setups
curl -G "https://ebi.ac.uk" \
  --data-urlencode "accession=PRJEB57558" \
  --data-urlencode "result=read_run" \
  --data-urlencode "fields=$FIELDS_RUN" \
  --data-urlencode "format=tsv" > PRJEB57558_all_runs_all_fields.tsv

# Download every single piece of biological metadata, host information, and environmental phenotypes
curl -G "https://ebi.ac.uk" \
  --data-urlencode "accession=PRJEB57558" \
  --data-urlencode "result=sample" \
  --data-urlencode "fields=$FIELDS_SAMPLE" \
  --data-urlencode "format=tsv" > PRJEB57558_all_samples_all_fields.tsv


# STEP 3: Clean Empty Columns

# Function to drop completely empty columns from a TSV file
clean_empty_columns() {
    local file=$1
    local out_file="${file%.tsv}_cleaned.tsv"
    awk -F'\t' '
    NR==1 { split($0, headers); next } 
    { for(i=1; i<=NF; i++) if($i != "") has_data[i]=1 } 
    END {
        printf "%s", headers[1]
        for(i=2; i<=length(headers); i++) if(i in has_data) printf "\t%s", headers[i]
        print ""
        while ((getline < "'"$file"'") > 0) {
            if (FNR==1) next
            printf "%s", $1
            for(i=2; i<=NF; i++) if(i in has_data) printf "\t%s", $i
            print ""
        }
    }' "$file" > "$out_file"
    echo "Cleaned $file -> Generated $out_file (Retained columns with data)"
}

clean_empty_columns "PRJEB57558_all_runs_all_fields.tsv"
clean_empty_columns "PRJEB57558_all_samples_all_fields.tsv"
