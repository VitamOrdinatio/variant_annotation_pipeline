#!/usr/bin/env bash
set -euo pipefail

# setup_vap.sh
#
# Purpose:
#   Thin orchestration entrypoint for VAP setup/validation tasks.
#
# Current scope:
#   - environment-aware path selection
#   - annotation resource setup/validation delegation
#
# Supported environments:
#   - sys76
#   - mark
#
# Supported modes:
#   - status
#   - validate
#   - provision


## VARIABLES

TARGET_ENV="${TARGET_ENV:-sys76}"
MODE="${MODE:-status}"

VEP_EXECUTABLE="${VEP_EXECUTABLE:-}"
ANNOVAR_EXECUTABLE="${ANNOVAR_EXECUTABLE:-}"

## HELPER FUNCTIONS

log() {
  echo "[INFO] $*"
}

die() {
  echo "[ERROR] $*" >&2
  exit 1
}

case "$TARGET_ENV" in
  sys76)
    STORAGE_BASE="/mnt/storage"
    ;;
  mark)
    STORAGE_BASE="/data/storage"
    ;;
  *)
    die "Invalid TARGET_ENV: $TARGET_ENV (expected: sys76|mark)"
    ;;
esac

case "$MODE" in
  status|validate|provision)
    ;;
  *)
    die "Invalid MODE: $MODE (expected: status|validate|provision)"
    ;;
esac

VEP_CACHE_DIR="${VEP_CACHE_DIR:-$STORAGE_BASE/reference/vep/cache}"
ANNOVAR_HUMANDB_DIR="${ANNOVAR_HUMANDB_DIR:-$STORAGE_BASE/reference/annovar/humandb}"

log "TARGET_ENV: $TARGET_ENV"
log "MODE: $MODE"
log "STORAGE_BASE: $STORAGE_BASE"
log "Delegating to scripts/resources/setup_annotation_resources.sh"

MODE="$MODE" \
VEP_EXECUTABLE="$VEP_EXECUTABLE" \
VEP_CACHE_DIR="$VEP_CACHE_DIR" \
ANNOVAR_HUMANDB_DIR="$ANNOVAR_HUMANDB_DIR" \
ANNOVAR_EXECUTABLE="$ANNOVAR_EXECUTABLE" \
bash scripts/resources/setup_annotation_resources.sh