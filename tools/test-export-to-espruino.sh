#!/usr/bin/env bash
# SPDX-License-Identifier: MPL-2.0

set -euo pipefail

fail() {
  printf 'Exporter test: %s\n' "$*" >&2
  exit 1
}

expect_failure() {
  if "$@" >/dev/null 2>&1; then
    fail "command unexpectedly succeeded: $*"
  fi
}

script_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)
exporter="$script_dir/export-to-espruino.sh"
[[ -x "$exporter" ]] || fail "exporter is not executable: $exporter"

test_root=$(mktemp -d "${TMPDIR:-/tmp}/xfsm-export-test.XXXXXX")
trap 'rm -rf -- "$test_root"' EXIT
source_root="$test_root/source"
host_root="$test_root/espruino"

mkdir -p "$source_root/tools" "$source_root/xfsm/build"
cp "$exporter" "$source_root/tools/export-to-espruino.sh"
printf 'payload\n' > "$source_root/xfsm/library.txt"
printf '#!/bin/sh\nexit 0\n' > "$source_root/xfsm/executable.sh"
chmod +x "$source_root/xfsm/executable.sh"
printf 'xfsm/build/\n' > "$source_root/.gitignore"
printf 'ignored source product\n' > "$source_root/xfsm/build/product"

git -C "$source_root" init --quiet
git -C "$source_root" config user.name "XFSM Export Test"
git -C "$source_root" config user.email "xfsm-export@example.invalid"
git -C "$source_root" add .
git -C "$source_root" commit --quiet -m "Create canonical fixture"

mkdir -p "$host_root/libs" "$host_root/src"
printf 'all:\n\t@:\n' > "$host_root/Makefile"
printf '/* fixture */\n' > "$host_root/src/jsvar.h"
printf 'libs/xfsm/build/\n' > "$host_root/.gitignore"
git -C "$host_root" init --quiet
git -C "$host_root" config user.name "XFSM Export Test"
git -C "$host_root" config user.email "xfsm-export@example.invalid"
git -C "$host_root" add .
git -C "$host_root" commit --quiet -m "Create Espruino fixture"

source_commit=$(git -C "$source_root" rev-parse HEAD)
export_output=$("$source_root/tools/export-to-espruino.sh" "$host_root")
[[ "$export_output" == *"$source_commit"* ]] || \
  fail "export did not report its source commit"
[[ "$export_output" == *"XFSM-Source: $source_commit"* ]] || \
  fail "export did not report the required integration trailer"
[[ -f "$host_root/libs/xfsm/library.txt" ]] || fail "tracked file was not exported"
[[ -x "$host_root/libs/xfsm/executable.sh" ]] || fail "executable mode was not preserved"
[[ ! -e "$host_root/libs/xfsm/build/product" ]] || \
  fail "ignored source product was exported"

git -C "$host_root" add libs/xfsm
git -C "$host_root" commit --quiet -m "Import canonical fixture"
"$source_root/tools/export-to-espruino.sh" --check "$host_root" >/dev/null

chmod -x "$host_root/libs/xfsm/executable.sh"
expect_failure "$source_root/tools/export-to-espruino.sh" --check "$host_root"
git -C "$host_root" restore libs/xfsm/executable.sh

mkdir -p "$host_root/libs/xfsm/build"
printf 'ignored destination product\n' > "$host_root/libs/xfsm/build/product"
expect_failure "$source_root/tools/export-to-espruino.sh" --check "$host_root"
"$source_root/tools/export-to-espruino.sh" "$host_root" >/dev/null
[[ ! -e "$host_root/libs/xfsm/build/product" ]] || \
  fail "ignored destination product was not removed"

printf 'dirty destination\n' > "$host_root/untracked.txt"
expect_failure "$source_root/tools/export-to-espruino.sh" "$host_root"
rm -f "$host_root/untracked.txt"

printf 'dirty source\n' >> "$source_root/xfsm/library.txt"
expect_failure "$source_root/tools/export-to-espruino.sh" "$host_root"

printf 'XFSM committed-file exporter: PASS\n'
