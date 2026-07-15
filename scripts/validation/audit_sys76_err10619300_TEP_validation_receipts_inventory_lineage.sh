#!/usr/bin/env bash
set -euo pipefail

RUN="results/run_2026_07_14_114546"
TEP="$RUN/tep/vap_tep_ERR10619300_run_2026_07_14_114546_v1"
OUT="$HOME/Downloads/audit_sys76_err10619300_TEP_validation_receipts_inventory_lineage.txt"

mkdir -p "$HOME/Downloads"

(
  echo "============================================================"
  echo "PROBE B — PRODUCER RECEIPTS, INVENTORY, LINEAGE, VALIDATION"
  echo "============================================================"
  echo "generated_at: $(date --iso-8601=seconds)"
  echo "repository:   $(pwd)"
  echo "run:          $RUN"
  echo "tep:          $TEP"
  echo

  echo "============================================================"
  echo "1. GENOTYPE PROJECTION SUMMARY"
  echo "============================================================"

  if [[ -f "$RUN/processed/genotype_projection_summary.json" ]]; then
    jq . "$RUN/processed/genotype_projection_summary.json"
  else
    echo "MISSING: $RUN/processed/genotype_projection_summary.json"
  fi

  echo
  echo "============================================================"
  echo "2. GENOTYPE SOURCE-HEADER CONTEXT"
  echo "============================================================"

  if [[ -f "$RUN/processed/genotype_source_header_context.json" ]]; then
    jq . "$RUN/processed/genotype_source_header_context.json"
  else
    echo "MISSING: $RUN/processed/genotype_source_header_context.json"
  fi

  echo
  echo "============================================================"
  echo "3. EXECUTION PROVENANCE"
  echo "============================================================"

  if [[ -f "$RUN/metadata/execution_provenance.json" ]]; then
    jq . "$RUN/metadata/execution_provenance.json"
  else
    echo "MISSING: $RUN/metadata/execution_provenance.json"
  fi

  echo
  echo "============================================================"
  echo "4. RUN METADATA"
  echo "============================================================"

  if [[ -f "$RUN/metadata/run_metadata.json" ]]; then
    jq . "$RUN/metadata/run_metadata.json"
  else
    echo "MISSING: $RUN/metadata/run_metadata.json"
  fi

  echo
  echo "============================================================"
  echo "5. TEP EMISSION SUMMARY JSON"
  echo "============================================================"

  if [[ -f "$RUN/metadata/tep_emission_summary.json" ]]; then
    jq . "$RUN/metadata/tep_emission_summary.json"
  else
    echo "MISSING: $RUN/metadata/tep_emission_summary.json"
  fi

  echo
  echo "============================================================"
  echo "6. GENOTYPE / PROVENANCE ENTITY INVENTORY REGISTRATION"
  echo "============================================================"

  if [[ -f "$TEP/entity_inventory.json" ]]; then
    grep -nE \
      'genotype_observations|genotype_projection_summary|genotype_source_header_context|execution_provenance|config_snapshot' \
      "$TEP/entity_inventory.json" || echo "NO_MATCHING_INVENTORY_ENTRIES"
  else
    echo "MISSING: $TEP/entity_inventory.json"
  fi

  echo
  echo "============================================================"
  echo "7. COMPLETE ENTITY INVENTORY"
  echo "============================================================"

  if [[ -f "$TEP/entity_inventory.json" ]]; then
    jq . "$TEP/entity_inventory.json"
  fi

  echo
  echo "============================================================"
  echo "8. GENOTYPE / PROVENANCE LINEAGE REGISTRATION"
  echo "============================================================"

  if [[ -f "$TEP/lineage_manifest.json" ]]; then
    grep -nE \
      'genotype_observations|genotype_projection_summary|genotype_source_header_context|execution_provenance|config_snapshot' \
      "$TEP/lineage_manifest.json" || echo "NO_MATCHING_LINEAGE_ENTRIES"
  else
    echo "MISSING: $TEP/lineage_manifest.json"
  fi

  echo
  echo "============================================================"
  echo "9. COMPLETE LINEAGE MANIFEST"
  echo "============================================================"

  if [[ -f "$TEP/lineage_manifest.json" ]]; then
    jq . "$TEP/lineage_manifest.json"
  fi

  echo
  echo "============================================================"
  echo "10. TEP VALIDATION REPORT"
  echo "============================================================"

  if [[ -f "$TEP/validation_report.md" ]]; then
    cat "$TEP/validation_report.md"
  else
    echo "MISSING: $TEP/validation_report.md"
  fi

  echo
  echo "============================================================"
  echo "11. TEP ARTIFACT FILE INVENTORY"
  echo "============================================================"

  find "$TEP" -type f -printf '%s\t%p\n' | sort -n

  echo
  echo "============================================================"
  echo "12. SELECTED FILE CHECKSUMS"
  echo "============================================================"

  for path in \
    "$RUN/processed/genotype_observations.tsv" \
    "$RUN/processed/genotype_projection_summary.json" \
    "$RUN/processed/genotype_source_header_context.json" \
    "$RUN/metadata/execution_provenance.json" \
    "$RUN/metadata/config_snapshot.yaml" \
    "$TEP/entities/genotype/genotype_observations.tsv" \
    "$TEP/entities/genotype/genotype_projection_summary.json" \
    "$TEP/entities/genotype/genotype_source_header_context.json" \
    "$TEP/entities/context/execution_provenance.json" \
    "$TEP/entities/metadata/config_snapshot.yaml" \
    "$TEP/entity_inventory.json" \
    "$TEP/lineage_manifest.json" \
    "$TEP/validation_report.md"
  do
    if [[ -f "$path" ]]; then
      sha256sum "$path"
    else
      echo "MISSING	$path"
    fi
  done

  echo
  echo "============================================================"
  echo "PROBE_B_COMPLETE=YES"
  echo "============================================================"
) > "$OUT" 2>&1 && probe_status=0 || probe_status=$?

echo "Probe B complete: $OUT"
echo "Probe B exit status: $probe_status"

exit "$probe_status"