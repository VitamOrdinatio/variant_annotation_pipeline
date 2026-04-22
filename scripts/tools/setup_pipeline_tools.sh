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
#   provision = create expected tool directories and perform supported provisioning steps
#
# Environment variables:
#   MODE                   (default: status)
#   TARGET_ENV             (default: sys76)
#   TOOLS_BASE             (default: ~/tools)
#
#   GATK_DIR               (default: $TOOLS_BASE/gatk)
#   GATK_EXECUTABLE        (default: $GATK_DIR/gatk)
#   GATK_LEGACY_DIR        (default: $TOOLS_BASE/gatk-4.6.2.0)
#
#   VEP_DIR                (default: $TOOLS_BASE/vep)
#   VEP_EXECUTABLE         (default: unset; falls back to PATH lookup for vep)
#   VEP_SOURCE_ARCHIVE     (default: unset; tar.gz/zip archive already present locally)
#
#   ANNOVAR_DIR            (default: $TOOLS_BASE/annovar)
#   ANNOVAR_EXECUTABLE     (default: $ANNOVAR_DIR/table_annovar.pl)
#   ANNOVAR_SOURCE_ARCHIVE (default: unset; .tar.gz/.zip archive already present locally)
#   ANNOVAR_SOURCE_DIR     (default: unset; existing unpacked annovar directory to copy)

MODE="${MODE:-status}"
TARGET_ENV="${TARGET_ENV:-sys76}"
TOOLS_BASE="${TOOLS_BASE:-$HOME/tools}"

GATK_DIR="${GATK_DIR:-$TOOLS_BASE/gatk}"
GATK_EXECUTABLE="${GATK_EXECUTABLE:-$GATK_DIR/gatk}"
GATK_LEGACY_DIR="${GATK_LEGACY_DIR:-$TOOLS_BASE/gatk-4.6.2.0}"

VEP_DIR="${VEP_DIR:-$TOOLS_BASE/vep}"
VEP_EXECUTABLE="${VEP_EXECUTABLE:-}"
VEP_SOURCE_ARCHIVE="${VEP_SOURCE_ARCHIVE:-}"

ANNOVAR_DIR="${ANNOVAR_DIR:-$TOOLS_BASE/annovar}"
ANNOVAR_EXECUTABLE="${ANNOVAR_EXECUTABLE:-$ANNOVAR_DIR/table_annovar.pl}"
ANNOVAR_SOURCE_ARCHIVE="${ANNOVAR_SOURCE_ARCHIVE:-}"
ANNOVAR_SOURCE_DIR="${ANNOVAR_SOURCE_DIR:-}"

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
    check_executable_path "VEP" "$VEP_EXECUTABLE"
    return $?
  fi
  check_on_path "vep"
  return $?
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

extract_archive_into_dir() {
  local label="$1"
  local archive_path="$2"
  local target_dir="$3"

  [[ -f "$archive_path" ]] || die "$label archive not found: $archive_path"

  ensure_directory "$label target" "$target_dir"

  case "$archive_path" in
    *.tar.gz|*.tgz)
      log "Extracting $label archive (.tar.gz) into $target_dir"
      tar -xzf "$archive_path" -C "$target_dir"
      ;;
    *.tar)
      log "Extracting $label archive (.tar) into $target_dir"
      tar -xf "$archive_path" -C "$target_dir"
      ;;
    *.zip)
      log "Extracting $label archive (.zip) into $target_dir"
      unzip -o "$archive_path" -d "$target_dir"
      ;;
    *)
      die "Unsupported $label archive format: $archive_path"
      ;;
  esac
}

ensure_gatk_canonical_symlink() {
  local canonical_exec="$GATK_EXECUTABLE"
  local legacy_exec="$GATK_LEGACY_DIR/gatk"

  if [[ -x "$canonical_exec" ]]; then
    log "Canonical GATK executable already present: $canonical_exec"
    return 0
  fi

  if [[ -x "$legacy_exec" ]]; then
    ln -s "$legacy_exec" "$canonical_exec"
    log "Created canonical GATK symlink: $canonical_exec -> $legacy_exec"
    return 0
  fi

  local nested_exec
  nested_exec="$(find "$GATK_DIR" -maxdepth 4 -type f -name gatk 2>/dev/null | head -n 1 || true)"
  if [[ -n "$nested_exec" && -x "$nested_exec" ]]; then
    ln -s "$nested_exec" "$canonical_exec"
    log "Created canonical GATK symlink from discovered executable: $canonical_exec -> $nested_exec"
    return 0
  fi

  warn "Unable to create canonical GATK symlink; no runnable gatk launcher found."
  return 1
}

find_single_file() {
  local search_dir="$1"
  local target_name="$2"
  find "$search_dir" -maxdepth 6 -type f -name "$target_name" 2>/dev/null | head -n 1 || true
}

ensure_vep_canonical_symlink() {
  local discovered_exec
  discovered_exec="$(find_single_file "$VEP_DIR" "vep")"

  if [[ -z "$discovered_exec" ]]; then
    warn "Unable to locate VEP executable inside $VEP_DIR after provisioning."
    return 1
  fi

  chmod +x "$discovered_exec" || true

  if [[ "$discovered_exec" == "$VEP_DIR/vep" ]]; then
    log "Canonical VEP executable already present: $discovered_exec"
    return 0
  fi

  if [[ -e "$VEP_DIR/vep" && ! -L "$VEP_DIR/vep" ]]; then
    warn "Cannot create canonical VEP symlink because $VEP_DIR/vep already exists and is not a symlink."
    return 1
  fi

  rm -f "$VEP_DIR/vep"
  ln -s "$discovered_exec" "$VEP_DIR/vep"
  log "Created canonical VEP symlink: $VEP_DIR/vep -> $discovered_exec"
  return 0
}

provision_vep_from_archive_if_requested() {
  if [[ -z "$VEP_SOURCE_ARCHIVE" ]]; then
    warn "VEP source archive not provided; skipping VEP install."
    return 1
  fi

  extract_archive_into_dir "VEP" "$VEP_SOURCE_ARCHIVE" "$VEP_DIR"
  ensure_vep_canonical_symlink
}

provision_annovar_if_requested() {
  if [[ -n "$ANNOVAR_SOURCE_DIR" ]]; then
    [[ -d "$ANNOVAR_SOURCE_DIR" ]] || die "ANNOVAR source directory not found: $ANNOVAR_SOURCE_DIR"
    ensure_directory "ANNOVAR target" "$ANNOVAR_DIR"
    log "Copying ANNOVAR source directory into $ANNOVAR_DIR"
    cp -a "$ANNOVAR_SOURCE_DIR"/. "$ANNOVAR_DIR"/
    chmod +x "$ANNOVAR_EXECUTABLE" || true
    return 0
  fi

  if [[ -n "$ANNOVAR_SOURCE_ARCHIVE" ]]; then
    extract_archive_into_dir "ANNOVAR" "$ANNOVAR_SOURCE_ARCHIVE" "$ANNOVAR_DIR"
    chmod +x "$ANNOVAR_EXECUTABLE" || true
    return 0
  fi

  warn "ANNOVAR source archive/directory not provided; skipping ANNOVAR install."
  return 1
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
log "GATK_LEGACY_DIR: $GATK_LEGACY_DIR"
log "VEP_DIR: $VEP_DIR"
log "VEP_EXECUTABLE: ${VEP_EXECUTABLE:-<unset>}"
log "VEP_SOURCE_ARCHIVE: ${VEP_SOURCE_ARCHIVE:-<unset>}"
log "ANNOVAR_DIR: $ANNOVAR_DIR"
log "ANNOVAR_EXECUTABLE: $ANNOVAR_EXECUTABLE"
log "ANNOVAR_SOURCE_ARCHIVE: ${ANNOVAR_SOURCE_ARCHIVE:-<unset>}"
log "ANNOVAR_SOURCE_DIR: ${ANNOVAR_SOURCE_DIR:-<unset>}"

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

  ensure_gatk_canonical_symlink || true

  if ! check_executable_path "GATK" "$GATK_EXECUTABLE"; then
    warn "GATK executable provisioning not yet complete."
  fi

  if ! check_vep_executable; then
    provision_vep_from_archive_if_requested || true
  fi

  if ! check_executable_path "ANNOVAR" "$ANNOVAR_EXECUTABLE"; then
    provision_annovar_if_requested || true
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

  if [[ "$VEP_TOOL_STATUS" != "present" ]]; then
    warn "VEP executable provisioning not yet complete."
  fi

  if [[ "$ANNOVAR_TOOL_STATUS" != "present" ]]; then
    warn "ANNOVAR executable provisioning not yet complete."
  fi

  log "Provision step completed."
fi