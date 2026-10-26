# Original ESP32 Standalone Qualification

## Purpose

This report records physical qualification of the current standalone XFSM
candidate on the original ESP32 architecture. It covers a stock production
build, the production JavaScript suites, canonical traces, and the complete
save, reboot, restore, and reset lifecycle.

## Revisions And Target

| Item | Value |
| --- | --- |
| Board | `ESP32_IDF5` |
| Processor | ESP32-D0WD-V3 revision 3.1, dual-core Xtensa, 4 MB flash |
| Console | CH340 USB-UART at 115200 baud |
| Espruino runtime | `2v29.536` |
| Espruino integration revision | `0cab2c6755e2959672209c11ac5b1d60c46cd1e0` |
| Exported standalone source | `74987aeaa1f700bfd5b79aaf35defea171918905` |
| Official Espruino upstream base | `3b5c8d97fa0678ec1da49a322f5f1fa990374a7a` |
| Specification | Public Profile 2 version 1.0, incorporating Profile 1 version 0.52 |
| Toolchain | ESP-IDF 5.5.3; `xtensa-esp-elf-gcc` 14.2.0 (`esp-14.2.0_20251107`) |
| Build | Stock 70 KB native-heap profile, `BOARD=ESP32_IDF5 RELEASE=1 USE_XFSM=1` |

Later standalone revisions in the trace and lifecycle records change only the
physical runners, manifest, and trace fixtures. The native engine in the
flashed firmware is unchanged across the complete qualification.

## Build Result

The clean production image is 1,574,048 bytes and leaves 473,952 bytes, or 23
percent, of the application partition free. Its SHA-256 value is:

```text
2576b8c20d39f359a98bc1246e7a0d6688550891fab1de1012cdedd444625051
```

## Method

The firmware was provisioned, built, and flashed from the Espruino integration
checkout:

```bash
source scripts/provision.sh ESP32_IDF5
unset DEBUG
make BOARD=ESP32_IDF5 clean
make BOARD=ESP32_IDF5 RELEASE=1 USE_XFSM=1 -j2
make BOARD=ESP32_IDF5 RELEASE=1 USE_XFSM=1 flash \
  PORT=/dev/serial/by-id/usb-1a86_USB_Serial-if00-port0
```

The production manifest, final trace pass, and lifecycle were run from the
standalone checkout:

```bash
python3 tools/repl/run_qualification_suite.py esp32-idf5 \
  --port /dev/serial/by-id/usb-1a86_USB_Serial-if00-port0 \
  --expected-git-commit 0cab2c675 \
  --output /tmp/xfsm-esp32-current-qualification.json

python3 tools/repl/run_qualification_suite.py esp32-idf5 --traces-only \
  --port /dev/serial/by-id/usb-1a86_USB_Serial-if00-port0 \
  --expected-git-commit 0cab2c675 \
  --output /tmp/xfsm-esp32-current-traces-final.json

python3 tools/repl/run_lifecycle_test.py \
  --port /dev/serial/by-id/usb-1a86_USB_Serial-if00-port0 \
  --baud 115200 --expected-board ESP32_IDF5 \
  --expected-git-commit 0cab2c675 \
  --output /tmp/xfsm-esp32-current-lifecycle.json
```

The production manifest exercises the physical API, configuration, context,
transition, action, snapshot, subscription, diagnostic, host, final-state,
compatibility, resource, and Profile 2 history cases in the [test
inventory](../../tests/test-inventory.md). The canonical trace result directly
covers `XFC-CF-API-002`, `XFC-CF-CONFIG-004`, `XFC-CF-CONFIG-005`,
`XFC-CF-ACTION-002`, `XFC-CF-SNAP-002`, `XFC-CF-TRANS-005`,
`XFC-CF-DIAG-006`, and `XFC-CF-COMPAT-006`.

## Physical Result

All current production checks passed:

- 29 of 29 production JavaScript suites;
- nine of nine canonical traces, compared exactly with their reviewed expected
  output;
- shallow and deep history semantics and diagnostics;
- host callbacks, GPIO and timer ingress, cleanup, event serialization,
  maximum-depth Storage-backed construction, and allocation pressure; and
- whole-interpreter save/reboot/restoration and reset cleanup.

The depth-32 direct transition case peaked at 1,093 of 2,858 JsVar blocks. The
Storage-backed depth case compiled at 1,056 used blocks and reported 67,484
bytes of free native heap. The shared-machine stress case retained 547 free
JsVar blocks at its live peak and returned exactly to its settled baseline.

The lifecycle saved 40,012 interpreter bytes, compressed them to 10,121 bytes,
restored the actor without replay, and passed reset cleanup. Boot reports that
this board has no supported PSRAM and continues without it; qualification used
only its internal RAM.

The machine-readable records are:

- [production suites](../../tests/results/esp32-xtensa/2026-10-26-standalone-production-suites.json);
- [canonical traces](../../tests/results/esp32-xtensa/2026-10-26-standalone-traces.json);
- [lifecycle](../../tests/results/esp32-xtensa/2026-10-26-standalone-lifecycle.json); and
- [qualification summary](../../tests/results/esp32-xtensa/2026-10-26-standalone-qualification.json).

## Harness Findings

The first trace pass exposed test-transport assumptions rather than native
engine defects:

1. Directly evaluated large trace source retained too many temporary JsVars for
   the diagnostic depth-limit case, so this target now uses the existing
   Storage-backed trace loader.
2. The CH340 UART delivered Espruino XOFF and XON signals during long writes.
   The shared serial helper now enables software flow control, preventing
   source loss instead of relying on target-specific delays.
3. The diagnostic trace was divided at a marked physical boundary so its
   allocation-heavy representation-limit case executes with normal error-object
   headroom. The two records are merged and resequenced before one exact
   comparison with the unchanged 58-record canonical result. Linux continues
   to execute the source as one unpartitioned trace.

No native XFSM implementation change was required.

## Remaining Physical Work

This run completes the current-candidate production, trace, and lifecycle
repetition on both high-resource ESP32 architectures. It does not repeat the
two-board WiFi, HTTPS/TLS, and BLE coexistence test. Pico and MDBT42Q still need
their current Profile 2 physical runtime and lifecycle repetition when those
boards are available.
