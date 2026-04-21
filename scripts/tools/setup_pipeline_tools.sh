#!/usr/bin/env bash
set -euo pipefail

# setup_pipeline_tools.sh
#
# Purpose:
#   Provision and/or validate external executable tools required by VAP.
#
# Current scope:
#   - Perl
#   - GATK
#   - VEP
#   - ANNOVAR
#
# Design rules:
#   - idempotent
#   - validate-first
#   - explicit failure on missing requirements
#   - portable across Sys76 / Mark / future nodes via environment variables
#   - user-space tool layout preferred (e.g., ~/tools)
#
# Modes:
#   status    = report current state only
#   validate  = fail if required tools are missing/invalid
#   provision = create expected tool directories and report missing tool installs
#
# Environment variables:
#   MODE                 (default: status)
#   TARGET_ENV           (default: sys76)
#   TOOLS_BASE           (default: ~/tools)
#   GATK_DIR             (default: $TOOLS_BASE/gatk)
#   GATK_EXECUTABLE      (default: $GATK_DIR/gatk)
#   VEP_DIR              (default: $TOOLS_BASE/vep)
#   VEP_EXECUTABLE       (default: unset; falls back to PATH lookup for vep)
#   ANNOVAR_DIR          (default: $TOOLS_BASE/annovar)
#   ANNOVAR_EXECUTABLE   (default: $ANNOVAR_DIR/table_annovar.pl)

MODE="${MODE:-status}"
TARGET_ENV="${TARGET_ENV:-sys76}"
TOOLS_BASE="${TOOLS_BASE:-$HOME/tools}"

GATK_DIR="${GATK_DIR:-$TOOLS_BASE/gatk}"
GATK_EXECUTABLE="${GATK_EXECUTABLE:-$GATK_DIR/gatk}"

VEP_DIR="${VEP_DIR:-$TOOLS_BASE/vep}"
VEP_EXECUTABLE="${VEP_EXECUTABLE:-}"

ANNOVAR_DIR="${ANNOVAR_DIR:-$TOOLS_BASE/annovar}"
ANNOVAR_EXECUTABLE="${ANNOVAR_EXECUTABLE:-$ANNOVAR_DIR/table_annovar.pl}"

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

ensure_directory() {
  local label="$1"
  local dir_path="$2"

  if [[ -d "$dir_path" ]]; then
    log "$label directory already exists: $dir_path"
    return 0
  fi

  mkdir -p "$dir_path"
  log "Created $label directory: $dir_path"
}

inspect_directory_state() {
  local label="$1"
  local dir_path="$2"

  if [[ -d "$dir_path" ]]; then
    if [[ -n "$(ls -A "$dir_path" 2>/dev/null)" ]]; then
      echo "[INFO] $label directory exists and is non-empty." >&2
      echo "present"
      return 0
    else
      warn "$label directory exists but is empty."
      echo "empty"
      return 0
    fi
  fi

  warn "$label directory does not exist."
  echo "missing"
}

case "$TARGET_ENV" in
  sys76|mark)
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

log "TARGET_ENV: $TARGET_ENV"
log "MODE: $MODE"
log "TOOLS_BASE: $TOOLS_BASE"
log "GATK_DIR: $GATK_DIR"
log "GATK_EXECUTABLE: $GATK_EXECUTABLE"
log "VEP_DIR: $VEP_DIR"
log "VEP_EXECUTABLE: ${VEP_EXECUTABLE:-<unset>}"
log "ANNOVAR_DIR: $ANNOVAR_DIR"
log "ANNOVAR_EXECUTABLE: $ANNOVAR_EXECUTABLE"

PERL_TOOL_STATUS="missing"
GATK_TOOL_STATUS="missing"
VEP_TOOL_STATUS="missing"
ANNOVAR_TOOL_STATUS="missing"

if check_on_path "perl"; then
  PERL_TOOL_STATUS="present"
fi

if check_executable_path "GATK" "$GATK_EXECUTABLE"; then
  GATK_TOOL_STATUS="present"
fi

if check_vep_executable; then
  VEP_TOOL_STATUS="present"
fi

if check_executable_path "ANNOVAR" "$ANNOVAR_EXECUTABLE"; then
  ANNOVAR_TOOL_STATUS="present"
fi

TOOLS_BASE_STATUS="$(inspect_directory_state "Tools base" "$TOOLS_BASE")"
GATK_DIR_STATUS="$(inspect_directory_state "GATK directory" "$GATK_DIR")"
VEP_DIR_STATUS="$(inspect_directory_state "VEP directory" "$VEP_DIR")"
ANNOVAR_DIR_STATUS="$(inspect_directory_state "ANNOVAR directory" "$ANNOVAR_DIR")"

if [[ "$MODE" == "validate" ]]; then
  [[ "$PERL_TOOL_STATUS" == "present" ]] || die "Perl executable not available on PATH."
  [[ "$GATK_TOOL_STATUS" == "present" ]] || die "GATK executable not properly configured."
  [[ "$VEP_TOOL_STATUS" == "present" ]] || die "VEP executable not properly configured."
  [[ "$ANNOVAR_TOOL_STATUS" == "present" ]] || die "ANNOVAR executable not properly configured."

  log "All pipeline tools validated successfully."
fi

if [[ "$MODE" == "provision" ]]; then
  log "Provision mode selected."

  ensure_directory "Tools base" "$TOOLS_BASE"
  ensure_directory "GATK directory" "$GATK_DIR"
  ensure_directory "VEP directory" "$VEP_DIR"
  ensure_directory "ANNOVAR directory" "$ANNOVAR_DIR"

  TOOLS_BASE_STATUS="$(inspect_directory_state "Tools base" "$TOOLS_BASE")"
  GATK_DIR_STATUS="$(inspect_directory_state "GATK directory" "$GATK_DIR")"
  VEP_DIR_STATUS="$(inspect_directory_state "VEP directory" "$VEP_DIR")"
  ANNOVAR_DIR_STATUS="$(inspect_directory_state "ANNOVAR directory" "$ANNOVAR_DIR")"

  if [[ "$GATK_TOOL_STATUS" != "present" ]]; then
    warn "GATK executable provisioning not yet implemented."
  fi

  if [[ "$VEP_TOOL_STATUS" != "present" ]]; then
    warn "VEP executable provisioning not yet implemented."
  fi

  if [[ "$ANNOVAR_TOOL_STATUS" != "present" ]]; then
    warn "ANNOVAR executable provisioning not yet implemented."
  fi

  log "Provision step completed (directory scaffold only)."
fi