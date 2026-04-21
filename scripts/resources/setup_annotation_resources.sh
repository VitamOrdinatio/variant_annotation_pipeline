#!/usr/bin/env bash
set -euo pipefail

# setup_annotation_resources.sh
#
# Purpose:
#   Provision and/or validate annotation-engine resources for VAP.
#
# Current scope:
#   - VEP cache directory validation/provisioning scaffold
#   - ANNOVAR humandb directory validation/provisioning scaffold
#
# Design rules:
#   - idempotent
#   - validate-first
#   - explicit failure on missing requirements
#   - portable across Sys76 / Mark / future nodes via environment variables
#
# Modes:
#   status    = report current state only
#   validate  = fail if required resources are missing/invalid
#   provision = create directories and perform provisioning steps when implemented
#
# Environment variables:
#   MODE                 (default: status)
#   VEP_CACHE_DIR        (default: /mnt/storage/reference/vep/cache)
#   ANNOVAR_HUMANDB_DIR  (default: /mnt/storage/reference/annovar/humandb)

# VARIABLES
MODE="${MODE:-status}"
VEP_EXECUTABLE="${VEP_EXECUTABLE:-}"
VEP_CACHE_DIR="${VEP_CACHE_DIR:-/mnt/storage/reference/vep/cache}"
ANNOVAR_HUMANDB_DIR="${ANNOVAR_HUMANDB_DIR:-/mnt/storage/reference/annovar/humandb}"
ANNOVAR_EXECUTABLE="${ANNOVAR_EXECUTABLE:-}"

# HELPER FUNCTIONS
log() {
  echo "[INFO] $*"
}

warn() {
  echo "[WARN] $*" >&2
}

die() {
  echo "[ERROR] $*" >&2
  exit 1
}

check_on_path() {
  local tool_name="$1"
  if command -v "$tool_name" >/dev/null 2>&1; then
    log "Found tool on PATH: $tool_name -> $(command -v "$tool_name")"
    return 0
  fi

  warn "Tool not found on PATH: $tool_name"
  return 1
}

check_executable_path() {
  local label="$1"
  local executable_path="$2"

  if [[ -z "$executable_path" ]]; then
    warn "$label executable path not provided."
    return 1
  fi

  if [[ ! -e "$executable_path" ]]; then
    warn "$label executable path does not exist: $executable_path"
    return 1
  fi

  if [[ ! -f "$executable_path" ]]; then
    warn "$label executable path is not a regular file: $executable_path"
    return 1
  fi

  if [[ ! -x "$executable_path" ]]; then
    warn "$label executable path is not executable: $executable_path"
    return 1
  fi

  log "Found $label executable: $executable_path"
  return 0
}

check_vep_executable() {
  if [[ -n "$VEP_EXECUTABLE" ]]; then
    if check_executable_path "VEP" "$VEP_EXECUTABLE"; then
      return 0
    fi
    return 1
  fi

  if check_on_path "vep"; then
    return 0
  fi

  return 1
}

# MAIN LOGIC


# --- validate MODE ---
case "$MODE" in
  status|validate|provision)
    ;;
  *)
    die "Invalid MODE: $MODE (expected: status|validate|provision)"
    ;;
esac

log "MODE: $MODE"
log "VEP_EXECUTABLE: ${VEP_EXECUTABLE:-<unset>}"
log "VEP_CACHE_DIR: $VEP_CACHE_DIR"
log "ANNOVAR_HUMANDB_DIR: $ANNOVAR_HUMANDB_DIR"
log "ANNOVAR_EXECUTABLE: ${ANNOVAR_EXECUTABLE:-<unset>}"


# --- tool inspection ---
VEP_TOOL_STATUS="missing"
PERL_TOOL_STATUS="missing"
ANNOVAR_TOOL_STATUS="missing"

if check_vep_executable; then
  VEP_TOOL_STATUS="present"
fi

if check_on_path "perl"; then
  PERL_TOOL_STATUS="present"
fi

if check_executable_path "ANNOVAR" "$ANNOVAR_EXECUTABLE"; then
  ANNOVAR_TOOL_STATUS="present"
fi


# --- VEP cache inspection ---
if [[ -d "$VEP_CACHE_DIR" ]]; then
  if [[ -n "$(ls -A "$VEP_CACHE_DIR" 2>/dev/null)" ]]; then
    log "VEP cache directory exists and is non-empty."
    VEP_STATUS="present"
  else
    warn "VEP cache directory exists but is empty."
    VEP_STATUS="empty"
  fi
else
  warn "VEP cache directory does not exist."
  VEP_STATUS="missing"
fi

# --- ANNOVAR humandb inspection ---
if [[ -d "$ANNOVAR_HUMANDB_DIR" ]]; then
  if [[ -n "$(ls -A "$ANNOVAR_HUMANDB_DIR" 2>/dev/null)" ]]; then
    log "ANNOVAR humandb directory exists and is non-empty."
    ANNOVAR_STATUS="present"
  else
    warn "ANNOVAR humandb directory exists but is empty."
    ANNOVAR_STATUS="empty"
  fi
else
  warn "ANNOVAR humandb directory does not exist."
  ANNOVAR_STATUS="missing"
fi

# --- validation enforcement ---
if [[ "$MODE" == "validate" ]]; then
  [[ "$VEP_TOOL_STATUS" == "present" ]] || die "VEP executable not available on PATH."
  [[ "$PERL_TOOL_STATUS" == "present" ]] || die "Perl executable not available on PATH."
  [[ "$ANNOVAR_TOOL_STATUS" == "present" ]] || die "ANNOVAR executable not properly configured."
  [[ "$VEP_STATUS" == "present" ]] || die "VEP cache not properly provisioned."
  [[ "$ANNOVAR_STATUS" == "present" ]] || die "ANNOVAR humandb not properly provisioned."

  log "All annotation resources validated successfully."
fi

# --- provision scaffolding ---
if [[ "$MODE" == "provision" ]]; then
  log "Provision mode selected."

  if [[ "$VEP_STATUS" != "present" ]]; then
    warn "VEP cache provisioning not yet implemented."
  fi

  if [[ "$ANNOVAR_STATUS" != "present" ]]; then
    warn "ANNOVAR humandb provisioning not yet implemented."
  fi

  log "Provision step completed (scaffold only)."
fi