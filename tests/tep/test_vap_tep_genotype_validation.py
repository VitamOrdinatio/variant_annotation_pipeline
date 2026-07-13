\
from __future__ import annotations
import csv, hashlib, json
from pathlib import Path
import pytest
from pipeline.genotype_projection import GENOTYPE_COLUMNS
from scripts.tep.validate_vap_tep import check_genotype_capability


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def package(root: Path, status: str = "pass") -> dict:
    d=root/"entities/genotype"; d.mkdir(parents=True)
    row={c:"NA" for c in GENOTYPE_COLUMNS}
    row.update({"genotype_observation_id":"go1","sample_id":"HG002","run_id":"run_fixture","source_pipeline":"variant_annotation_pipeline","reference_build":"GRCh38","chromosome":"1","position":"100","reference_allele":"A","alternate_alleles_raw":"C","variant_id":"1:100:A:C","gt_raw":"0/1","gt_status":"present_parseable","genotype_call_state":"heterozygous_call","phase_state":"unphased","variant_relationship_status":"direct","relationship_reason":"biallelic_direct","relationship_resolution_target":"none","record_parse_status":"parsed","source_record_hash":"hash"})
    t=d/"genotype_observations.tsv"
    with t.open("w",encoding="utf-8",newline="") as h:
        w=csv.DictWriter(h,fieldnames=GENOTYPE_COLUMNS,delimiter="\t",lineterminator="\n"); w.writeheader(); w.writerow(row)
    c=d/"genotype_source_header_context.json"; c.write_text(json.dumps({"schema_version":"genotype_source_header_context_v1","sample_columns":["HG002"]},sort_keys=True)+"\n")
    s=d/"genotype_projection_summary.json"; s.write_text(json.dumps({"schema_version":"genotype_projection_summary_v1","projection":{"projection_status":status,"projection_version":"genotype_projection_v1","reference_build":"GRCh38"},"sample_resolution":{"sample_id":"HG002","run_id":"run_fixture"},"source_vcf":{"sha256":"v"*64,"header_hash":"h"*64,"source_record_count":1},"counts":{"genotype_observation_row_count":1,"projection_warning_count":1 if status=="pass_with_warnings" else 0},"outputs":{"genotype_observations_sha256":sha(t),"header_context_sha256":sha(c)}},sort_keys=True)+"\n")
    def a(role,path):
        p=root/path
        return {"source_artifact_role":role,"source_artifact":f"/source/{p.name}","source_artifact_sha256":sha(p),"source_artifact_exists":True,"transport_path":path,"size_bytes":p.stat().st_size}
    return {"source_run":{"sample_id":"HG002","run_id":"run_fixture"},"entities":[{"entity_id":"observation_entity","entity_role":"observation_entity","source_artifacts":[],"transport_paths":[]},{"entity_id":"genotype_observation_entity","entity_role":"genotype_observation_entity","artifact_count":3,"source_artifacts":[a("genotype_observations","entities/genotype/genotype_observations.tsv"),a("genotype_projection_summary","entities/genotype/genotype_projection_summary.json"),a("genotype_source_header_context","entities/genotype/genotype_source_header_context.json")]}],"lineage_edges":[{"parent_entity_id":"observation_entity","child_entity_id":"genotype_observation_entity","relationship":"projects_genotype"},{"parent_entity_id":"genotype_observation_entity","child_entity_id":"lineage_manifest","relationship":"indexed_by"}]}


def failed(checks): return {c.criterion for c in checks if c.status=="FAIL"}

def test_legacy_no_checks(tmp_path): assert check_genotype_capability({"entities":[],"source_run":{},"lineage_edges":[]},tmp_path)==[]
def test_valid_passes(tmp_path):
    checks=check_genotype_capability(package(tmp_path),tmp_path); assert not failed(checks); assert {c.criterion for c in checks}=={f"AC-05{i}" for i in range(9)}
@pytest.mark.parametrize("status",["pass_with_advisory","pass_with_warnings"])
def test_nonfatal_statuses(tmp_path,status): assert "AC-057" not in failed(check_genotype_capability(package(tmp_path,status),tmp_path))
def test_missing_artifact(tmp_path):
    m=package(tmp_path); (tmp_path/"entities/genotype/genotype_source_header_context.json").unlink(); assert "AC-051" in failed(check_genotype_capability(m,tmp_path))
def test_bad_header(tmp_path):
    m=package(tmp_path); p=tmp_path/"entities/genotype/genotype_observations.tsv"; lines=p.read_text().splitlines(); lines[0]="\t".join(GENOTYPE_COLUMNS[:-1]); p.write_text("\n".join(lines)+"\n"); assert "AC-052" in failed(check_genotype_capability(m,tmp_path))
def test_count_mismatch(tmp_path):
    m=package(tmp_path); p=tmp_path/"entities/genotype/genotype_projection_summary.json"; d=json.loads(p.read_text()); d["counts"]["genotype_observation_row_count"]=2; p.write_text(json.dumps(d)+"\n"); assert "AC-053" in failed(check_genotype_capability(m,tmp_path))
def test_checksum_mismatch(tmp_path):
    m=package(tmp_path); p=tmp_path/"entities/genotype/genotype_projection_summary.json"; d=json.loads(p.read_text()); d["outputs"]["genotype_observations_sha256"]="0"*64; p.write_text(json.dumps(d)+"\n"); assert "AC-054" in failed(check_genotype_capability(m,tmp_path))
def test_identity_mismatch(tmp_path):
    m=package(tmp_path); m["source_run"]["run_id"]="other"; assert "AC-055" in failed(check_genotype_capability(m,tmp_path))
def test_lineage_missing(tmp_path):
    m=package(tmp_path); m["lineage_edges"]=[]; assert "AC-058" in failed(check_genotype_capability(m,tmp_path))
def test_failed_status(tmp_path): assert "AC-057" in failed(check_genotype_capability(package(tmp_path,"failed"),tmp_path))
