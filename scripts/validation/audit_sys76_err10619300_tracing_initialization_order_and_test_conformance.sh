#!/usr/bin/env bash
set -euo pipefail

RUN="results/run_2026_07_14_114546"
OUT="$HOME/Downloads/audit_sys76_err10619300_tracing_initialization_order_and_test_conformance.txt"

mkdir -p "$HOME/Downloads"

(
  echo "============================================================"
  echo "PROBE C — INITIALIZATION ORDER AND TEST CONFORMANCE"
  echo "============================================================"
  echo "generated_at: $(date --iso-8601=seconds)"
  echo "repository:   $(pwd)"
  echo "run:          $RUN"
  echo

  echo "============================================================"
  echo "1. REPOSITORY AND ENVIRONMENT IDENTITY"
  echo "============================================================"

  echo
  echo '$ git rev-parse HEAD'
  git rev-parse HEAD

  echo
  echo '$ git branch --show-current'
  git branch --show-current

  echo
  echo '$ git status --short'
  git status --short

  echo
  echo '$ git diff --quiet && git diff --cached --quiet'
  if git diff --quiet && git diff --cached --quiet; then
    echo "REPOSITORY_TRACKED_STATE=CLEAN"
  else
    echo "REPOSITORY_TRACKED_STATE=DIRTY"
  fi

  if [[ -z "$(git ls-files --others --exclude-standard)" ]]; then
    echo "REPOSITORY_UNTRACKED_STATE=CLEAN"
  else
    echo "REPOSITORY_UNTRACKED_STATE=UNTRACKED_FILES_PRESENT"
  fi

  echo
  echo '$ python --version'
  python --version

  echo
  echo '$ which python'
  which python

  echo
  echo '$ pytest --version'
  pytest --version

  echo
  echo '$ uname -a'
  uname -a

  echo
  echo '$ hostname'
  hostname

  echo
  echo "============================================================"
  echo "2. PROVENANCE INITIALIZATION ORDER"
  echo "============================================================"

  if [[ -f "$RUN/logs/pipeline.log" ]]; then
    echo
    echo "--- matching provenance / Stage 01 lines with line numbers ---"

    grep -nEi \
      'execution provenance|execution_provenance|stage 01|stage_01|stage 1|stage_1' \
      "$RUN/logs/pipeline.log" || echo "NO_MATCHING_LOG_LINES"

    echo
    echo "--- first 250 pipeline-log lines ---"
    sed -n '1,250p' "$RUN/logs/pipeline.log"
  else
    echo "MISSING: $RUN/logs/pipeline.log"
  fi

  echo
  echo "============================================================"
  echo "3. DISCOVER TARGETED TEST PATHS"
  echo "============================================================"

  targeted_paths=()

  while IFS= read -r path; do
    targeted_paths+=("$path")
  done < <(
    find tests -maxdepth 4 \
      \( \
        -iname '*execution*provenance*.py' \
        -o -iname '*genotype*.py' \
        -o -iname '*vap*tep*.py' \
        -o -iname '*tep*packag*.py' \
        -o -iname '*tep*transport*.py' \
      \) \
      -type f \
      | sort
  )

  printf '%s\n' "${targeted_paths[@]}"

  echo
  echo "============================================================"
  echo "4. TARGETED MODERN-SUBSTRATE TESTS"
  echo "============================================================"

  targeted_status=0

  if [[ "${#targeted_paths[@]}" -eq 0 ]]; then
    echo "No targeted test files discovered."
    echo "TARGETED_TEST_STATUS=NOT_RUN"
  else
    echo "Running ${#targeted_paths[@]} targeted test files."
    echo

    pytest -q "${targeted_paths[@]}"
    targeted_status=$?

    echo
    echo "TARGETED_TEST_EXIT_STATUS=$targeted_status"
  fi

  echo
  echo "============================================================"
  echo "5. COMPLETE VAP REGRESSION SUITE"
  echo "============================================================"

  pytest -q
  full_suite_status=$?

  echo
  echo "FULL_SUITE_EXIT_STATUS=$full_suite_status"

  echo
  echo "============================================================"
  echo "6. FINAL PROBE C SUMMARY"
  echo "============================================================"

  echo "TARGETED_TEST_EXIT_STATUS=$targeted_status"
  echo "FULL_SUITE_EXIT_STATUS=$full_suite_status"

  if [[ "$targeted_status" -eq 0 && "$full_suite_status" -eq 0 ]]; then
    echo "PROBE_C_OVERALL=PASS"
    final_status=0
  else
    echo "PROBE_C_OVERALL=FAIL"
    final_status=1
  fi

  echo "============================================================"

  exit "$final_status"
) > "$OUT" 2>&1 && probe_status=0 || probe_status=$?

echo "Probe C complete: $OUT"
echo "Probe C exit status: $probe_status"

exit "$probe_status"