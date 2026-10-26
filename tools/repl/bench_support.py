# SPDX-License-Identifier: MPL-2.0
"""Shared serial and bench helpers for XFSM physical-device runners."""

from __future__ import annotations

import json
from pathlib import Path
import re
import time

import serial

from run_test import (
    filter_structured_lines,
    query_value,
    read_available,
    send_and_capture,
    send_script_paced,
    sync_repl,
)


ANSI_ESCAPE = re.compile(r"\x1b\[[0-?]*[ -/]*[@-~]")


class ConfigError(ValueError):
    """Raised when a physical bench configuration is malformed."""


def clean_repl_line(line: str) -> str:
    return ANSI_ESCAPE.sub("", line).strip()


def has_output_marker(output: str, markers: tuple[str, ...]) -> bool:
    return any(
        clean_repl_line(line).startswith(marker)
        for line in output.splitlines()
        for marker in markers
    )


def count_output_marker(output: str, marker: str) -> int:
    return sum(
        clean_repl_line(line).startswith(marker)
        for line in output.splitlines()
    )


def collect_until(
    repl: serial.Serial,
    initial: str,
    markers: tuple[str, ...],
    timeout: float,
) -> str:
    output = initial
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if has_output_marker(output, markers):
            return output + read_available(repl, 0.25)
        waiting = repl.in_waiting
        if waiting:
            output += repl.read(waiting).decode("utf-8", "replace")
        else:
            time.sleep(0.02)
    return output


def marker_payload(output: str, marker: str) -> dict | None:
    prefix = marker + "="
    payload = None
    for line in output.splitlines():
        stripped = clean_repl_line(line)
        position = stripped.find(prefix)
        if position >= 0:
            try:
                payload = json.loads(stripped[position + len(prefix) :])
            except json.JSONDecodeError:
                continue
    return payload


def load_config(path: Path) -> dict:
    try:
        config = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        raise ConfigError(f"cannot read configuration: {exc}") from exc

    if config.get("schema_version") != 1:
        raise ConfigError("schema_version must be 1")
    if config.get("operating_mode") != "STANDALONE":
        raise ConfigError("operating_mode must be STANDALONE")
    if not isinstance(config.get("positions"), list) or not config["positions"]:
        raise ConfigError("positions must be a non-empty list")
    return config


def validate_position(position: dict) -> tuple[str, str, dict, dict]:
    position_id = position.get("position_id")
    control_role = position.get("control_role")
    usb_roles = position.get("usb_roles")
    expected = position.get("expected_firmware")

    if not isinstance(position_id, str) or not position_id:
        raise ConfigError("every position requires a non-empty position_id")
    if not isinstance(usb_roles, dict) or not usb_roles:
        raise ConfigError(f"{position_id}: usb_roles must be a non-empty object")
    if control_role not in usb_roles:
        raise ConfigError(
            f"{position_id}: control_role {control_role!r} is not in usb_roles"
        )
    if not isinstance(expected, dict):
        raise ConfigError(f"{position_id}: expected_firmware must be an object")
    for field in ("board", "version", "git_commit"):
        if not isinstance(expected.get(field), str) or not expected[field]:
            raise ConfigError(f"{position_id}: expected_firmware.{field} is required")

    role = usb_roles[control_role]
    path = role.get("path")
    if not isinstance(path, str) or not path.startswith("/dev/"):
        raise ConfigError(f"{position_id}: control path must be under /dev")
    baud = role.get("baud", 115200)
    if not isinstance(baud, int) or baud <= 0:
        raise ConfigError(f"{position_id}: baud must be a positive integer")
    return position_id, control_role, role, expected


def get_position(config: dict, position_id: str) -> dict:
    for position in config["positions"]:
        if position.get("position_id") == position_id:
            validate_position(position)
            return position
    raise ConfigError(f"missing configured position: {position_id}")


def control_connection(position: dict) -> tuple[str, int]:
    _, control_role, role, _ = validate_position(position)
    if control_role != "console":
        raise ConfigError(
            f"{position['position_id']}: expected console control role"
        )
    return role["path"], role.get("baud", 115200)


def verify_identity(repl: serial.Serial, position: dict) -> dict[str, str]:
    expected = position["expected_firmware"]
    observed = {
        "board": query_value(repl, "process.env.BOARD", "BOARD"),
        "version": query_value(repl, "process.version", "VERSION"),
        "git_commit": query_value(repl, "process.env.GIT_COMMIT", "GIT_COMMIT"),
    }
    for field in ("board", "version", "git_commit"):
        if observed[field] != expected[field]:
            raise ValueError(
                f"{position['position_id']}: {field} mismatch: "
                f"expected {expected[field]}, observed {observed[field]}"
            )
    return observed


def upload_role(
    repl: serial.Serial,
    role_path: Path,
    role_config: dict,
    markers: tuple[str, ...],
    timeout: float,
) -> str:
    send_and_capture(repl, "echo(true);\n", settle=0.15)
    send_and_capture(
        repl,
        "global.WIFI_TEST_CONFIG=" + json.dumps(role_config) + ";\n",
        settle=0.2,
    )
    initial = send_script_paced(repl, role_path.read_text())
    return collect_until(repl, initial, markers, timeout)


def runtime_cleanup(repl: serial.Serial, label: str) -> tuple[str, str]:
    send_and_capture(repl, "\x03", settle=0.15)
    send_and_capture(repl, "echo(true);\n", settle=0.15)
    cleanup = (
        '(function(){var w=require("Wifi");clearInterval();clearWatch();'
        "w.removeAllListeners();w.disconnect();w.stopAP();"
        'setTimeout(function(){print("'
        + label
        + '_CLEAN=1")},500)})();\n'
    )
    initial = send_and_capture(repl, cleanup, settle=0.2)
    output = collect_until(repl, initial, (label + "_CLEAN=1",), 4.0)
    status = query_value(repl, 'require("Wifi").getStatus()', label + "_STATUS")
    return output, status


def ble_runtime_cleanup(repl: serial.Serial, label: str) -> tuple[str, str, str]:
    send_and_capture(repl, "\x03", settle=0.15)
    send_and_capture(repl, "echo(true);\n", settle=0.15)
    cleanup = (
        "(function(){clearInterval();clearWatch();NRF.setScan();"
        "NRF.removeAllListeners();NRF.disconnect();NRF.sleep();"
        'E.setConsole(E.getConsole(),{force:false});setTimeout(function(){print("'
        + label
        + '_CLEAN=1")},300)})();\n'
    )
    initial = send_and_capture(repl, cleanup, settle=0.2)
    output = collect_until(repl, initial, (label + "_CLEAN=1",), 3.0)
    security = query_value(repl, "NRF.getSecurityStatus()", label + "_SECURITY")
    connected = query_value(
        repl,
        "NRF.getSecurityStatus().connected===true",
        label + "_CONNECTED",
    )
    return output, security, connected


def print_role_output(label: str, output: str) -> None:
    print(f"RUNNER {label}_output_begin")
    normalized = "\n".join(clean_repl_line(line) for line in output.splitlines())
    for line in filter_structured_lines(normalized):
        print(line)
    for line in normalized.splitlines():
        if line.startswith(("BLE_", "XFSM_")):
            print(line)
    print(f"RUNNER {label}_output_end")
