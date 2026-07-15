#!/usr/bin/env bash
set -euo pipefail

RUN="results/run_2026_07_14_114546"
TEP="$RUN/tep/vap_tep_ERR10619300_run_2026_07_14_114546_v1"
OUT="$HOME/Downloads/audit_sys76_err10619300_run_transport_byte_identity.txt"

mkdir -p "$HOME/Downloads"

(
  echo "============================================================"
  echo "CURRENT SYS76 RUN — PROCESSED-TO-TEP TRANSPORT BYTE IDENTITY"
  echo "============================================================"
  echo "generated_at: $(date --iso-8601=seconds)"
  echo "repository:   $(pwd)"
  echo "run:          $RUN"
  echo "tep:          $TEP"
  echo

  overall_status=0

  for artifact in \
    genotype_observations.tsv \
    genotype_projection_summary.json \
    genotype_source_header_context.json
  do
    echo
    echo "------------------------------------------------------------"
    echo "ARTIFACT: $artifact"
    echo "------------------------------------------------------------"

    processed="$RUN/processed/$artifact"
    packaged="$TEP/entities/genotype/$artifact"

    echo "processed_path: $processed"
    echo "packaged_path:  $packaged"

    if [[ ! -f "$processed" ]]; then
      echo "PROCESSED_EXISTS=FAIL"
      overall_status=1
      continue
    fi

    if [[ ! -f "$packaged" ]]; then
      echo "PACKAGED_EXISTS=FAIL"
      overall_status=1
      continue
    fi

    echo "PROCESSED_EXISTS=PASS"
    echo "PACKAGED_EXISTS=PASS"

    echo
    echo "SHA256:"
    sha256sum "$processed" "$packaged"

    echo
    echo "FILE METADATA:"
    stat "$processed" "$packaged"

    echo
    if cmp -s "$processed" "$packaged"; then
      echo "BYTE_IDENTITY=PASS"
    else
      echo "BYTE_IDENTITY=FAIL"
      overall_status=1
    fi
  done

  echo
  echo "============================================================"
  echo "EXECUTION PROVENANCE TRANSPORT"
  echo "============================================================"

  source_provenance="$RUN/metadata/execution_provenance.json"
  packaged_provenance="$TEP/entities/context/execution_provenance.json"

  echo "source_path:   $source_provenance"
  echo "packaged_path: $packaged_provenance"

  if [[ ! -f "$source_provenance" ]]; then
    echo "SOURCE_PROVENANCE_EXISTS=FAIL"
    overall_status=1
  else
    echo "SOURCE_PROVENANCE_EXISTS=PASS"
  fi

  if [[ ! -f "$packaged_provenance" ]]; then
    echo "PACKAGED_PROVENANCE_EXISTS=FAIL"
    overall_status=1
  else
    echo "PACKAGED_PROVENANCE_EXISTS=PASS"
  fi

  if [[ -f "$source_provenance" && -f "$packaged_provenance" ]]; then
    echo
    echo "SHA256:"
    sha256sum "$source_provenance" "$packaged_provenance"

    echo
    echo "FILE METADATA:"
    stat "$source_provenance" "$packaged_provenance"

    echo
    if cmp -s "$source_provenance" "$packaged_provenance"; then
      echo "EXECUTION_PROVENANCE_BYTE_IDENTITY=PASS"
    else
      echo "EXECUTION_PROVENANCE_BYTE_IDENTITY=FAIL"
      overall_status=1
    fi
  fi

  echo
  echo "============================================================"

  if [[ "$overall_status" -eq 0 ]]; then
    echo "PROBE_A_OVERALL=PASS"
  else
    echo "PROBE_A_OVERALL=FAIL"
  fi

  echo "============================================================"

  exit "$overall_status"
) > "$OUT" 2>&1 && probe_status=0 || probe_status=$?

echo "Probe A complete: $OUT"
echo "Probe A exit status: $probe_status"

exit "$probe_status"