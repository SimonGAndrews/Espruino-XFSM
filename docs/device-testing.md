# Physical Device Testing

## Purpose

This is the entry point for building, flashing, and testing XFSM on physical
Espruino targets. It records the common workflow and directs each target to the
instructions that differ. The procedures and tools in this repository do not
depend on the earlier `ESP32_SGATest` repository.

Use these guides together with [Building Espruino XFSM](building.md):

| Target or test | Procedure |
| --- | --- |
| Original ESP32 | [Original ESP32 Device Testing](esp32-device-testing.md) |
| ESP32-C3 | [ESP32-C3 Device Testing](esp32-c3-device-testing.md) |
| Espruino Pico and MDBT42Q | [Constrained ARM Device Testing](constrained-arm-device-testing.md) |
| ESP32 BLE, WiFi, HTTPS, and XFSM together | [Service-Coexistence Testing](service-coexistence-testing.md) |

## Common Workflow

1. Commit the XFSM candidate and export it into a clean Espruino integration
   checkout.
2. Record both repository commits and any remaining local changes.
3. Identify the attached board through `/dev/serial/by-id` or
   `/dev/serial/by-path`; do not rely on a transient `ttyUSB` or `ttyACM`
   number alone.
4. Close the Web IDE, terminal programs, monitors, and previous runners before
   opening the port. Only one process may own an Espruino REPL.
5. Provision the target toolchain in a fresh shell, clean when changing board
   family or build profile, and build with the exact recorded flags.
6. Flash using the target's documented method and then query the running
   `BOARD`, Espruino version, `GIT_COMMIT`, and `XFSM` module surface.
7. Run a small smoke test before resource, lifecycle, or service tests.
8. Preserve the first raw failure, repeat it without changing the test, and
   distinguish transport failure from JavaScript failure and firmware reset.
9. Restore the normal production image after an instrumented or fault-injection
   build.

`process.env.GIT_COMMIT` records the Espruino checkout commit. It does not
record uncommitted changes or the canonical XFSM commit. New evidence must
therefore record both repositories and their dirty-tree state.

## Project-Owned Serial Runner

Install the runner's only Python dependency:

```bash
python3 -m pip install --user -r tools/repl/requirements.txt
```

Run an XFSM fixture through a paced direct serial connection:

```bash
python3 tools/repl/run_test.py xfsm/tests/test_shell.js \
  --port /dev/serial/by-id/DEVICE \
  --baud 115200 --timeout 30 --show-raw
```

The runner synchronizes the REPL, records runtime identity, calls `reset()`,
uploads the file in paced chunks, and extracts structured result lines. It
returns status 1 for an emitted `FAIL ` assertion and status 2 for a transport,
timeout, or result-contract failure.

A device test must emit one `TEST=` line, assertion-level `PASS ` or `FAIL `
lines, and exactly one final `DONE=PASS` or `DONE=FAIL`. Asynchronous tests must
have their own bounded timeout and must release actors, subscriptions, timers,
listeners, Storage files, and hardware outputs.

## Complete Production-Firmware Suite

The board qualification manifest is
[`tests/device/qualification-manifest.json`](../tests/device/qualification-manifest.json).
It owns the applicable production-firmware suite groups, expected board names,
baud rates, and nine canonical traces for each qualified target profile. Run it
with:

```bash
python3 tools/repl/run_qualification_suite.py esp32c3-idf5 \
  --port /dev/serial/by-id/DEVICE \
  --expected-git-commit COMMIT \
  --output /tmp/xfsm-c3-qualification.json
```

The runner verifies runtime identity, executes each applicable test through the
paced single-test transport, composes and compares every canonical trace, uses
flash-backed trace loading where the profile requires it, and can write a JSON
summary for review. Use repeated `--group` options for a focused group and
`--skip-traces` only when the resulting evidence is explicitly scoped. A full
qualification uses the profile defaults.

Measurement and deterministic fault-injection suites require their matching
temporary firmware and remain separate from this production-firmware run. The
whole-interpreter lifecycle is also separate because it must reconnect across a
reboot.

## Save And Reset Lifecycle

Run the two-phase save/restoration and cleanup test with the reconnect-aware
runner:

```bash
python3 tools/repl/run_lifecycle_test.py \
  --port /dev/serial/by-id/DEVICE --baud 115200 \
  --expected-board ESP32C3_IDF5 \
  --expected-git-commit COMMIT \
  --output /tmp/xfsm-c3-lifecycle.json
```

The runner uploads `test_save_restore.js`, follows the device across a USB
disconnect or UART-backed reboot, collects the restored result, waits for its
scheduled `reset(true)`, reconnects, and runs `test_reset_lifecycle.js`. A
transport failure is not a lifecycle pass even if the board later returns. Its
JSON summary records both the runtime firmware identity and the canonical XFSM
revision and dirty state.

## Reset Levels

Use the least reset that establishes the required starting condition:

1. REPL synchronization interrupts partial input but retains runtime state.
2. `reset()` clears ordinary JavaScript state; the direct runner uses it before
   a normal test.
3. A hardware or platform reboot reinitializes native drivers and is required
   for boot, saved-state, and driver-lifecycle tests.
4. A power cycle is a recovery action when the console or bootloader cannot be
   restored through the normal reset path.

Allow the boot banner and USB reconnection to finish before reopening the port.
Do not erase flash merely to recover a serial session.

## Evidence

Record the board and CPU, physical connection, exact build flags, toolchain,
both source revisions, runtime identity, test and runner commands, reset level,
structured results, and any recovery action. A single clean run is smoke
evidence. Timing, lifecycle, and coexistence claims require repeated runs with
the run count and workload recorded.

Store reviewed result data under `tests/results/` and its interpretation under
`docs/reports/`. Do not commit firmware binaries, raw exploratory logs, local
USB paths presented as universal values, or network credentials.
