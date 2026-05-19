#!/usr/bin/env bash
set -euo pipefail

TS="$(date +%Y%m%d_%H%M%S)"
LOG="/root/Desktop/mark_git_auth_probe_${TS}.log"
REPO_ROOT="$HOME/dev/portfolio_projects/variant_annotation_pipeline"

exec > >(tee "$LOG") 2>&1

echo "[INFO] Mark git auth probe started at $(date)"
echo "[INFO] Log file: $LOG"
echo "[INFO] Repo root: $REPO_ROOT"
echo

cd "$REPO_ROOT"

echo "=== BASIC REPO CONTEXT ==="
echo "[CMD] pwd"
pwd
echo

echo "[CMD] whoami"
whoami || true
echo

echo "[CMD] hostname"
hostname || true
echo

echo "=== REMOTE CONFIG ==="
echo "[CMD] git remote -v"
git remote -v || true
echo

echo "[CMD] git branch -vv"
git branch -vv || true
echo

echo "=== GIT CONFIG ==="
echo "[CMD] git config --get remote.origin.url"
git config --get remote.origin.url || true
echo

echo "[CMD] git config --get credential.helper"
git config --get credential.helper || true
echo

echo "[CMD] git config --global --get credential.helper"
git config --global --get credential.helper || true
echo

echo "=== SSH CONTEXT ==="
echo "[CMD] ls -lah ~/.ssh"
ls -lah ~/.ssh || true
echo

echo "[CMD] ssh -T git@github.com"
ssh -T git@github.com || true
echo

echo "=== FETCH / PULL TESTS ==="
echo "[CMD] git fetch origin"
git fetch origin || true
echo

echo "[CMD] git status"
git status || true
echo

echo "[CMD] git pull --ff-only"
git pull --ff-only || true
echo

echo "[INFO] Mark git auth probe completed at $(date)"
echo "[INFO] Log file saved to: $LOG"