#!/usr/bin/env bash
# SPDX-License-Identifier: MPL-2.0
#
# Run the complete XFSM Profile 2 host qualification through an Espruino
# checkout containing an exact export of this repository's xfsm/ tree.

set -euo pipefail

usage() {
  cat <<'EOF'
Usage: tools/run-host-qualification.sh <espruino-checkout>

Build and test the current XFSM source through a matching Espruino checkout.
Set XFSM_JOBS to change the Make parallelism (default: 2).
EOF
}

fail() {
  printf 'XFSM host qualification: %s\n' "$*" >&2
  exit 1
}

[[ $# -eq 1 ]] || {
  usage >&2
  exit 2
}

for command_name in git make node npm python3 rsync; do
  command -v "$command_name" >/dev/null 2>&1 || \
    fail "required command not found: $command_name"
done

script_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)
project_root=$(cd "$script_dir/.." && pwd -P)
espruino_arg=$1
[[ -d "$espruino_arg" ]] || fail "Espruino checkout not found: $espruino_arg"
espruino_root=$(git -C "$espruino_arg" rev-parse --show-toplevel 2>/dev/null) || \
  fail "not a Git checkout: $espruino_arg"
espruino_root=$(cd "$espruino_root" && pwd -P)
[[ -f "$espruino_root/Makefile" && -d "$espruino_root/libs/xfsm" ]] || \
  fail "checkout does not contain an exported libs/xfsm library"

jobs=${XFSM_JOBS:-2}
[[ "$jobs" =~ ^[1-9][0-9]*$ ]] || fail "XFSM_JOBS must be a positive integer"

phase() {
  printf '\n== %s ==\n' "$1"
}

phase "Source identity"
printf 'XFSM=%s\n' "$(git -C "$project_root" rev-parse HEAD)"
printf 'ESPRUINO=%s\n' "$(git -C "$espruino_root" rev-parse HEAD)"

# Build only the exact canonical library. Unlike export --check, this comparison
# permits the expected Espruino-side mirror commit used by CI and integration.
mirror_changes=$(rsync -rlcEni --delete --out-format='%i %n%L' \
  --exclude='tests/__pycache__/' --exclude='tests/native/build/' -- \
  "$project_root/xfsm/" "$espruino_root/libs/xfsm/")
[[ -z "$mirror_changes" ]] || {
  printf '%s\n' "$mirror_changes" >&2
  fail "libs/xfsm does not match the canonical xfsm/ tree"
}

normal_suites=(
  test_shell.js
  test_compile.js
  test_diagnostics.js
  test_runtime.js
  test_completion.js
  test_completion_cascade.js
  test_targets.js
  test_events_migration.js
  test_profile1_diagnostics.js
  test_context_ownership.js
  test_assign_forms.js
  test_context_diagnostics.js
  test_transition_domains.js
  test_transition_depth.js
  test_lifecycle_complete.js
  test_subscriber_complete.js
  test_cross_actor_gc.js
  test_runtime_errors.js
  test_subscriptions.js
  test_strict_validation.js
  test_strict_validation_embedded.js
  test_limits.js
  test_history.js
  test_history_embedded.js
  test_history_diagnostics.js
  test_deep_history.js
)

trace_cases=(
  api_002
  config_004
  config_005
  action_002
  snapshot_002
  transition_005
  diagnostic_006
  compat_006
  compat_006_v4
)

restore_needed=0
restore_normal_build() {
  local status=$?
  trap - EXIT
  if [[ $restore_needed -eq 1 ]]; then
    printf '\n== Restoring normal XFSM host build after interruption ==\n' >&2
    env -u DEBUG make -C "$espruino_root" clean >/dev/null || true
    env -u DEBUG make -C "$espruino_root" USE_XFSM=1 -j"$jobs" || true
  fi
  exit "$status"
}
trap restore_normal_build EXIT

phase "XFSM-disabled Linux build"
env -u DEBUG make -C "$espruino_root" clean
env -u DEBUG make -C "$espruino_root" USE_XFSM=0 -j"$jobs"

phase "XFSM-enabled Linux build"
env -u DEBUG make -C "$espruino_root" clean
env -u DEBUG make -C "$espruino_root" USE_XFSM=1 -j"$jobs"

phase "26 Profile 2 JavaScript suites"
for suite in "${normal_suites[@]}"; do
  printf 'RUN %s\n' "$suite"
  "$espruino_root/bin/espruino" --test \
    "$espruino_root/libs/xfsm/tests/$suite"
done

phase "Nine canonical traces"
for case_id in "${trace_cases[@]}"; do
  printf 'RUN trace_%s.js\n' "$case_id"
  python3 "$espruino_root/libs/xfsm/tests/run_trace_test.py" \
    "$espruino_root/libs/xfsm/tests/trace_${case_id}.js" \
    "$espruino_root/libs/xfsm/tests/expected/${case_id}.ndjson" \
    --espruino "$espruino_root/bin/espruino"
done

phase "Pinned XState references"
npm --prefix "$project_root/tests/reference/xstate-v5" ci --ignore-scripts
npm --prefix "$project_root/tests/reference/xstate-v5" test
npm --prefix "$project_root/tests/reference/xstate-v5" run test:history
npm --prefix "$project_root/tests/reference/xstate-v5" run test:history:deep
npm --prefix "$project_root/tests/reference/xstate-v4" ci --ignore-scripts
npm --prefix "$project_root/tests/reference/xstate-v4" test

phase "Native sanitizer suite"
make -C "$espruino_root/libs/xfsm/tests/native" clean test

phase "Static and governance audits"
python3 "$espruino_root/libs/xfsm/tests/audit_static_contract.py"
python3 "$project_root/tests/audit_compatibility_governance.py"
python3 "$project_root/tests/audit_normative_requirements.py"

phase "Deterministic allocation-fault build"
restore_needed=1
env -u DEBUG make -C "$espruino_root" clean
env -u DEBUG make -C "$espruino_root" USE_XFSM=1 XFC_TEST=1 -j"$jobs"
"$espruino_root/bin/espruino" --test \
  "$espruino_root/libs/xfsm/tests/test_fault_injection.js"

phase "Restore and verify normal XFSM build"
env -u DEBUG make -C "$espruino_root" clean
env -u DEBUG make -C "$espruino_root" USE_XFSM=1 -j"$jobs"
restore_needed=0
"$espruino_root/bin/espruino" --test \
  "$espruino_root/libs/xfsm/tests/test_strict_validation_embedded.js"

trap - EXIT
printf '\nXFSM_HOST_QUALIFICATION=PASS\n'
