#!/usr/bin/env bash
set -euo pipefail

# install_repo2_tools.sh
#
# Purpose:
#   Install external command-line dependencies needed by
#   variant_annotation_pipeline repo2 v1.0.
#
# Installs/checks:
#   - wget
#   - samtools
#   - bwa
#   - java (required for GATK)
#   - gatk
#
# Notes:
#   - Uses apt for system packages
#   - Installs GATK under ~/tools/
#   - Appends GATK to PATH in ~/.bashrc if needed
#
# Usage:
#   bash scripts/install_repo2_tools.sh

GATK_VERSION="4.6.2.0"
GATK_ZIP="gatk-${GATK_VERSION}.zip"
GATK_DIR="$HOME/tools/gatk-${GATK_VERSION}"
GATK_URL="https://github.com/broadinstitute/gatk/releases/download/${GATK_VERSION}/${GATK_ZIP}"
BASHRC="$HOME/.bashrc"
PATH_EXPORT_LINE="export PATH=\"${GATK_DIR}:\$PATH\""

log() {
  echo "[INFO] $*"
}

warn() {
  echo "[WARN] $*" >&2
}

err() {
  echo "[ERROR] $*" >&2
}

require_sudo() {
  if ! command -v sudo >/dev/null 2>&1; then
    err "sudo is required for apt-based installation but was not found."
    exit 1
  fi
}

have_cmd() {
  command -v "$1" >/dev/null 2>&1
}

install_apt_pkg_if_missing() {
  local cmd_name="$1"
  local pkg_name="$2"

  if have_cmd "${cmd_name}"; then
    log "${cmd_name} already available at: $(command -v "${cmd_name}")"
  else
    log "${cmd_name} not found. Installing apt package: ${pkg_name}"
    sudo apt-get install -y "${pkg_name}"
  fi
}

ensure_apt_updated() {
  require_sudo
  log "Updating apt package index..."
  sudo apt-get update
}

ensure_unzip() {
  install_apt_pkg_if_missing unzip unzip
}

ensure_java() {
  if have_cmd java; then
    log "java already available at: $(command -v java)"
  else
    log "java not found. Installing default-jre"
    sudo apt-get install -y default-jre
  fi
}

install_gatk_if_missing() {
  if have_cmd gatk; then
    log "gatk already available at: $(command -v gatk)"
    return
  fi

  mkdir -p "$HOME/tools"
  cd "$HOME/tools"

  if [[ ! -d "${GATK_DIR}" ]]; then
    if [[ ! -f "${GATK_ZIP}" ]]; then
      log "Downloading GATK ${GATK_VERSION} from official Broad GitHub release..."
      wget -O "${GATK_ZIP}" "${GATK_URL}"
    else
      log "GATK zip already present: $HOME/tools/${GATK_ZIP}"
    fi

    log "Unzipping ${GATK_ZIP}..."
    unzip -o "${GATK_ZIP}"
  else
    log "GATK directory already exists: ${GATK_DIR}"
  fi

  if ! grep -Fq "${PATH_EXPORT_LINE}" "${BASHRC}"; then
    log "Adding GATK to PATH in ${BASHRC}"
    printf '\n# Added by variant_annotation_pipeline repo2 installer\n%s\n' "${PATH_EXPORT_LINE}" >> "${BASHRC}"
  else
    log "GATK PATH export already present in ${BASHRC}"
  fi

  # Make GATK visible in this current shell too.
  export PATH="${GATK_DIR}:$PATH"

  if have_cmd gatk; then
    log "gatk is now available at: $(command -v gatk)"
  else
    err "gatk still not found after installation. Open a new shell or run: source ~/.bashrc"
    exit 1
  fi
}

verify_tool() {
  local cmd_name="$1"
  log "Verifying ${cmd_name}..."
  if ! have_cmd "${cmd_name}"; then
    err "${cmd_name} is not available in PATH after installation."
    exit 1
  fi
  echo "  -> $(command -v "${cmd_name}")"
}

show_versions() {
  echo
  log "Tool versions:"
  echo "wget:"
  wget --version | head -n 1 || true
  echo
  echo "samtools:"
  samtools --version | head -n 1 || true
  echo
  echo "bwa:"
  bwa 2>&1 | head -n 3 || true
  echo
  echo "java:"
  java -version 2>&1 | head -n 1 || true
  echo
  echo "gatk:"
  gatk --version || true
}

main() {
  ensure_apt_updated

  install_apt_pkg_if_missing wget wget
  install_apt_pkg_if_missing samtools samtools
  install_apt_pkg_if_missing bwa bwa
  ensure_unzip
  ensure_java

  install_gatk_if_missing

  echo
  log "Verifying installed tools..."
  verify_tool wget
  verify_tool samtools
  verify_tool bwa
  verify_tool java
  verify_tool gatk

  show_versions

  echo
  log "Installation complete."
  log "If this is a new shell session requirement, run: source ~/.bashrc"
}

main "$@"