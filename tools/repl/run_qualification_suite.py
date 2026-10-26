#!/usr/bin/env python3
# SPDX-License-Identifier: MPL-2.0
"""Run the production-firmware XFSM qualification suite on one board."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import sys
import tempfile

import serial

from run_test import collect_metadata


REPOSITORY = Path(__file__).resolve().parents[2]
DEFAULT_MANIFEST = REPOSITORY / "tests/device/qualification-manifest.json"
TESTS_DIR = REPOSITORY / "xfsm/tests"
RUN_TEST = Path(__file__).resolve().parent / "run_test.py"
TRACE_RUNNER = TESTS_DIR / "run_trace_test.py"


def load_manifest(path: Path) -> dict:
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"cannot read qualification manifest: {error}") from error
    if manifest.get("schema_version") != 1:
        raise ValueError("qualification manifest schema_version must be 1")
    if not isinstance(manifest.get("suite_groups"), dict):
        raise ValueError("qualification manifest has no suite_groups object")
    if not isinstance(manifest.get("profiles"), dict):
        raise ValueError("qualification manifest has no profiles object")
    return manifest


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


def run_command(command: list[str], transcript: Path | None = None) -> int:
    completed = subprocess.run(command, text=True, capture_output=True, check=False)
    output = completed.stdout + completed.stderr
    sys.stdout.write(output)
    if transcript is not None:
        transcript.write_text(output, encoding="utf-8")
    return completed.returncode


def storage_loader(source_path: Path, output_path: Path) -> None:
    data = source_path.read_text(encoding="utf-8")
    lines = [
        'var __xfcStorage=require("Storage");',
        'var __xfcFile="xftmp.js";',
        "__xfcStorage.erase(__xfcFile);",
    ]
    for offset in range(0, len(data), 192):
        chunk = json.dumps(data[offset : offset + 192])
        lines.append(f"__xfcStorage.write(__xfcFile,{chunk},{offset},{len(data)});")
    lines.extend(
        [
            "try{eval(__xfcStorage.read(__xfcFile));}",
            "finally{__xfcStorage.erase(__xfcFile);}",
        ]
    )
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("profile", help="Profile name from the manifest")
    parser.add_argument("--port", required=True)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--baud", type=int)
    parser.add_argument("--timeout", type=float, default=180.0)
    parser.add_argument("--expected-version")
    parser.add_argument("--expected-git-commit")
    parser.add_argument(
        "--group",
        action="append",
        dest="groups",
        help="Run only this suite group; may be repeated",
    )
    parser.add_argument("--skip-traces", action="store_true")
    parser.add_argument("--trace-storage", action="store_true")
    parser.add_argument("--keep-going", action="store_true")
    parser.add_argument("--output", type=Path, help="Write a JSON run summary")
    args = parser.parse_args()

    try:
        manifest = load_manifest(args.manifest)
        profile = manifest["profiles"][args.profile]
    except (KeyError, ValueError) as error:
        print(f"Qualification configuration error: {error}", file=sys.stderr)
        return 2

    baud = args.baud or profile["baud"]
    try:
        metadata = collect_metadata(args.port, baud)
    except (OSError, serial.SerialException) as error:
        print(f"Cannot identify device: {error}", file=sys.stderr)
        return 2
    expected = {
        "board": profile["board"],
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

    groups = args.groups or profile["groups"]
    suites: list[str] = []
    try:
        for group in groups:
            suites.extend(manifest["suite_groups"][group])
    except KeyError as error:
        print(f"Unknown suite group: {error.args[0]}", file=sys.stderr)
        return 2

    print(f"QUALIFICATION profile={args.profile}")
    print(f"QUALIFICATION port={args.port}")
    print(f"QUALIFICATION board={metadata['board']}")
    print(f"QUALIFICATION version={metadata['version']}")
    print(f"QUALIFICATION git_commit={metadata['git_commit']}")

    results: list[dict[str, object]] = []
    overall_pass = True

    for suite in suites:
        test_path = TESTS_DIR / suite
        print(f"\n== Device suite: {suite} ==")
        status = run_command(
            [
                sys.executable,
                str(RUN_TEST),
                str(test_path),
                "--port",
                args.port,
                "--baud",
                str(baud),
                "--timeout",
                str(args.timeout),
                "--show-raw",
            ]
        )
        passed = status == 0
        results.append({"kind": "suite", "name": suite, "pass": passed})
        overall_pass = overall_pass and passed
        if not passed and not args.keep_going:
            break

    run_traces = overall_pass or args.keep_going
    if not args.skip_traces and run_traces:
        use_storage = args.trace_storage or profile.get("trace_storage", False)
        for case_id in manifest["traces"]:
            print(f"\n== Canonical trace: {case_id} ==")
            with tempfile.TemporaryDirectory(prefix="xfsm-trace-") as temp_dir:
                temp = Path(temp_dir)
                composed = temp / f"trace_{case_id}.js"
                physical = temp / f"trace_{case_id}_physical.js"
                transcript = temp / f"trace_{case_id}.log"
                compose_status = run_command(
                    [
                        sys.executable,
                        str(TRACE_RUNNER),
                        str(TESTS_DIR / f"trace_{case_id}.js"),
                        "--compose-output",
                        str(composed),
                        "--compose-done-marker",
                    ]
                )
                if compose_status == 0 and use_storage:
                    storage_loader(composed, physical)
                elif compose_status == 0:
                    physical.write_text(composed.read_text(encoding="utf-8"))

                status = compose_status
                if status == 0:
                    status = run_command(
                        [
                            sys.executable,
                            str(RUN_TEST),
                            str(physical),
                            "--port",
                            args.port,
                            "--baud",
                            str(baud),
                            "--timeout",
                            str(args.timeout),
                            "--show-raw",
                        ],
                        transcript,
                    )
                if status == 0:
                    status = run_command(
                        [
                            sys.executable,
                            str(TRACE_RUNNER),
                            str(TESTS_DIR / f"trace_{case_id}.js"),
                            str(TESTS_DIR / "expected" / f"{case_id}.ndjson"),
                            "--observed-output",
                            str(transcript),
                        ]
                    )

            passed = status == 0
            results.append({"kind": "trace", "name": case_id, "pass": passed})
            overall_pass = overall_pass and passed
            if not passed and not args.keep_going:
                break

    summary = {
        "schema_version": 1,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "profile": args.profile,
        "port": args.port,
        "baud": baud,
        "runtime": metadata,
        "canonical_source": repository_state(REPOSITORY),
        "groups": groups,
        "traces_requested": not args.skip_traces,
        "results": results,
        "pass": overall_pass,
        "lifecycle_required_separately": True,
    }
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
        print(f"QUALIFICATION output={args.output}")

    print("QUALIFICATION_RESULT=" + ("PASS" if overall_pass else "FAIL"))
    print("QUALIFICATION lifecycle=run run_lifecycle_test.py separately")
    return 0 if overall_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
