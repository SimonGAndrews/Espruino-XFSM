#!/usr/bin/env python3
# SPDX-License-Identifier: MPL-2.0
"""Run XFSM save/reboot/restoration and reset cleanup on one board."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import sys
import time

import serial

from run_test import (
    collect_metadata,
    filter_structured_lines,
    read_until_prompt,
    send_and_capture,
    send_script_paced,
    sync_repl,
)


REPOSITORY = Path(__file__).resolve().parents[2]
SAVE_TEST = REPOSITORY / "xfsm/tests/test_save_restore.js"
RESET_TEST = REPOSITORY / "xfsm/tests/test_reset_lifecycle.js"


def repository_state(path: Path) -> dict[str, object]:
    commit = subprocess.run(
        ["git", "-C", str(path), "rev-parse", "HEAD"],
        text=True,
        capture_output=True,
        check=True,
    ).stdout.strip()
    dirty = bool(
        subprocess.run(
            ["git", "-C", str(path), "status", "--porcelain=v1"],
            text=True,
            capture_output=True,
            check=True,
        ).stdout.strip()
    )
    return {"commit": commit, "dirty": dirty}


def open_when_available(port: str, baud: int, deadline: float) -> serial.Serial:
    last_error: Exception | None = None
    while time.monotonic() < deadline:
        try:
            return serial.Serial(port, baud, timeout=0.1)
        except (OSError, serial.SerialException) as error:
            last_error = error
            time.sleep(0.1)
    raise serial.SerialException(f"port did not return: {port}: {last_error}")


def read_across_reconnect(
    repl: serial.Serial | None,
    port: str,
    baud: int,
    initial: str,
    timeout: float,
) -> tuple[str, serial.Serial | None]:
    """Collect one DONE result while tolerating a rebooted USB console."""
    output = initial
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if any(line.strip().startswith("DONE=") for line in output.splitlines()):
            return output, repl
        if repl is None:
            try:
                repl = open_when_available(port, baud, deadline)
            except serial.SerialException:
                break
        try:
            waiting = repl.in_waiting
            if waiting:
                output += repl.read(waiting).decode("utf-8", "replace")
            else:
                time.sleep(0.02)
        except (OSError, serial.SerialException):
            try:
                repl.close()
            except (OSError, serial.SerialException):
                pass
            repl = None
            time.sleep(0.1)
    return output, repl


def result_passed(output: str, expected_test: str) -> bool:
    lines = filter_structured_lines(output)
    tests = [line for line in lines if line.startswith("TEST=")]
    done = [line for line in lines if line.startswith("DONE=")]
    failures = [line for line in lines if line.startswith("FAIL ")]
    return (
        tests == [f"TEST={expected_test}"]
        and done == ["DONE=PASS"]
        and not failures
    )


def print_phase(label: str, output: str) -> None:
    print(f"LIFECYCLE {label}_output_begin")
    print(output.rstrip())
    print(f"LIFECYCLE {label}_output_end")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", required=True)
    parser.add_argument("--baud", type=int, default=115200)
    parser.add_argument("--timeout", type=float, default=60.0)
    parser.add_argument("--expected-board")
    parser.add_argument("--expected-version")
    parser.add_argument("--expected-git-commit")
    parser.add_argument("--output", type=Path, help="Write a JSON run summary")
    args = parser.parse_args()

    try:
        metadata = collect_metadata(args.port, args.baud)
    except (OSError, serial.SerialException) as error:
        print(f"Cannot identify device: {error}", file=sys.stderr)
        return 2

    expected = {
        "board": args.expected_board,
        "version": args.expected_version,
        "git_commit": args.expected_git_commit,
    }
    for field, value in expected.items():
        if value and metadata.get(field) != value:
            print(
                f"Runtime {field} mismatch: expected {value}, "
                f"observed {metadata.get(field)}",
                file=sys.stderr,
            )
            return 2

    print(f"LIFECYCLE port={args.port}")
    print(f"LIFECYCLE board={metadata['board']}")
    print(f"LIFECYCLE version={metadata['version']}")
    print(f"LIFECYCLE git_commit={metadata['git_commit']}")

    repl: serial.Serial | None = None
    save_output = ""
    reset_output = ""
    try:
        repl = open_when_available(
            args.port, args.baud, time.monotonic() + args.timeout
        )
        sync_repl(repl)
        reset_text = send_and_capture(repl, "reset();\n", settle=0.2)
        if not reset_text.rstrip().endswith(">"):
            read_until_prompt(repl, min(args.timeout, 8.0))
        cleanup_text = send_and_capture(
            repl,
            'var __xfcS=require("Storage");'
            '__xfcS.erase(".bootcde");__xfcS.erase(".varimg");'
            'print("XFC_LIFECYCLE_STORAGE_CLEAN="+'
            '(__xfcS.read(".bootcde")===undefined&&'
            '__xfcS.read(".varimg")===undefined));'
            'delete __xfcS;\n',
            settle=0.2,
        )
        if "XFC_LIFECYCLE_STORAGE_CLEAN=true" not in cleanup_text:
            print("Cannot establish clean saved-image state.", file=sys.stderr)
            return 2
        send_and_capture(repl, "echo(true);\n", settle=0.2)
        repl.reset_input_buffer()
        initial = send_script_paced(
            repl, SAVE_TEST.read_text(encoding="utf-8")
        )
        save_output, repl = read_across_reconnect(
            repl, args.port, args.baud, initial, args.timeout
        )
        print_phase("save_restore", save_output)
        save_pass = result_passed(save_output, "xfsm_save_restore")
        if not save_pass:
            print("Save/restoration phase failed or had no unique result.", file=sys.stderr)
            return 1

        # The fixture schedules reset(true) after publishing its durable result.
        if repl is not None:
            repl.close()
            repl = None
        time.sleep(2.0)

        repl = open_when_available(
            args.port, args.baud, time.monotonic() + args.timeout
        )
        sync_repl(repl)
        repl.reset_input_buffer()
        initial = send_script_paced(
            repl, RESET_TEST.read_text(encoding="utf-8")
        )
        reset_output, repl = read_across_reconnect(
            repl, args.port, args.baud, initial, args.timeout
        )
        print_phase("reset_cleanup", reset_output)
        reset_pass = result_passed(reset_output, "xfsm_reset_lifecycle")
    except (OSError, serial.SerialException) as error:
        print(f"Lifecycle transport failed: {error}", file=sys.stderr)
        return 2
    finally:
        if repl is not None:
            try:
                repl.close()
            except (OSError, serial.SerialException):
                pass

    passed = save_pass and reset_pass
    summary = {
        "schema_version": 1,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "runtime": metadata,
        "canonical_source": repository_state(REPOSITORY),
        "port": args.port,
        "baud": args.baud,
        "save_restore": "pass" if save_pass else "fail",
        "reset_cleanup": "pass" if reset_pass else "fail",
        "pass": passed,
    }
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
        print(f"LIFECYCLE output={args.output}")
    print("LIFECYCLE_RESULT=" + ("PASS" if passed else "FAIL"))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
