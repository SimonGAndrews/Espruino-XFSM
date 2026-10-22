#!/usr/bin/env bash
# SPDX-License-Identifier: MPL-2.0
#
# Export the canonical, committed xfsm/ tree into an Espruino checkout. The
# source and destination must both be clean so the resulting mirror always has
# an identifiable XFSM commit and never includes local working files.

set -euo pipefail

usage() {
  cat <<'EOF'
Usage: tools/export-to-espruino.sh [--check] <espruino-checkout>

Export the committed XFSM library tree to a clean Espruino checkout.

  --check  Compare the committed XFSM tree with libs/xfsm without changing it.
EOF
}

fail() {
  printf 'XFSM export: %s\n' "$*" >&2
  exit 1
}

mode=export
case "${1:-}" in
  --check)
    mode=check
    shift
    ;;
  -h|--help)
    usage
    exit 0
    ;;
esac

[[ $# -eq 1 ]] || {
  usage >&2
  exit 2
}

for command_name in git tar rsync; do
  command -v "$command_name" >/dev/null 2>&1 || \
    fail "required command not found: $command_name"
done

# Locate the canonical repository from this script rather than from the shell's
# current directory. Only committed HEAD content is eligible for export.
script_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)
expected_source_root=$(cd "$script_dir/.." && pwd -P)
source_root=$(git -C "$expected_source_root" rev-parse --show-toplevel 2>/dev/null) || \
  fail "the exporter is not inside a Git checkout"
source_root=$(cd "$source_root" && pwd -P)
[[ "$source_root" == "$expected_source_root" ]] || \
  fail "the exporter must run from its Espruino-XFSM checkout"
[[ -d "$source_root/xfsm" ]] || fail "canonical xfsm/ directory not found"

source_status=$(git -C "$source_root" status --porcelain=v1 --untracked-files=normal)
[[ -z "$source_status" ]] || \
  fail "canonical checkout is dirty; commit or remove its changes first"
source_commit=$(git -C "$source_root" rev-parse --verify 'HEAD^{commit}')
git -C "$source_root" cat-file -e "$source_commit:xfsm" || \
  fail "commit $source_commit does not contain xfsm/"

# Validate the host before constructing a path that can be updated. Requiring
# the repository root and rejecting a symlink keeps deletion inside libs/xfsm.
destination_arg=$1
[[ -d "$destination_arg" ]] || fail "destination is not a directory: $destination_arg"
destination_root=$(git -C "$destination_arg" rev-parse --show-toplevel 2>/dev/null) || \
  fail "destination is not a Git checkout: $destination_arg"
destination_root=$(cd "$destination_root" && pwd -P)
destination_given=$(cd "$destination_arg" && pwd -P)
[[ "$destination_root" == "$destination_given" ]] || \
  fail "destination must be the root of the Espruino checkout"
[[ "$destination_root" != "$source_root" ]] || \
  fail "source and destination repositories must be different"
[[ -f "$destination_root/Makefile" && -f "$destination_root/src/jsvar.h" && \
   -d "$destination_root/libs" ]] || \
  fail "destination does not have the expected Espruino repository layout"

destination_status=$(git -C "$destination_root" status \
  --porcelain=v1 --untracked-files=normal)
[[ -z "$destination_status" ]] || \
  fail "Espruino checkout is dirty; commit or remove its changes first"

mirror_root="$destination_root/libs/xfsm"
[[ ! -L "$mirror_root" ]] || fail "refusing to use a symlinked libs/xfsm"
[[ ! -e "$mirror_root" || -d "$mirror_root" ]] || \
  fail "libs/xfsm exists but is not a directory"

# Git archive supplies exactly the files and executable bits stored in the
# selected commit. Ignored build output in the canonical checkout is excluded.
stage_parent=$(mktemp -d "${TMPDIR:-/tmp}/xfsm-export.XXXXXX")
stage_root="$stage_parent/xfsm"
mkdir -m 755 "$stage_root"
trap 'rm -rf -- "$stage_parent"' EXIT
git -C "$source_root" archive --format=tar "$source_commit:xfsm" |
  tar -xf - -C "$stage_root"

compare_trees() {
  [[ -d "$mirror_root" ]] || return 1
  local changes
  # Compare paths, contents, links, and executable bits. Git does not track
  # directory permissions, so local directory modes are intentionally ignored.
  changes=$(rsync -rlcEni --delete --out-format='%i %n%L' -- \
    "$stage_root/" "$mirror_root/")
  if [[ -n "$changes" ]]; then
    printf '%s\n' "$changes"
    return 1
  fi
}

if [[ "$mode" == check ]]; then
  if compare_trees; then
    printf 'XFSM mirror matches committed source %s\n' "$source_commit"
    exit 0
  fi
  fail "libs/xfsm does not match committed source $source_commit"
fi

# Replace only the deployment mirror, then verify the result before reporting
# the source commit that must be recorded by the Espruino integration commit.
mkdir -p "$mirror_root"
rsync -rltE --omit-dir-times --delete -- "$stage_root/" "$mirror_root/"
compare_trees >/dev/null || fail "post-export verification failed"

printf -v destination_command_path '%q' "$destination_root"

cat <<EOF
Exported committed XFSM source $source_commit to:
  $mirror_root

Review and commit the exported files:
  cd $destination_command_path
  git add -A -- libs/xfsm
  git diff --cached -- libs/xfsm
  git commit \\
    -m 'Update XFSM library' \\
    -m 'XFSM-Source: $source_commit'
EOF
