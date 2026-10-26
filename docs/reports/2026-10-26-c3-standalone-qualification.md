# ESP32-C3 Standalone Qualification

## Purpose

This report records physical qualification of the current standalone XFSM
candidate on an ESP32-C3. The run checks the production JavaScript suites,
canonical compatibility traces, and whole-interpreter save, reboot, restore,
and reset lifecycle using firmware built from the Espruino integration branch.

## Revisions And Target

| Item | Value |
| --- | --- |
| Board | `ESP32C3_IDF5` |
| Processor | ESP32-C3 revision 0.4, RV32IMC |
| Console | Built-in USB serial/JTAG at 115200 baud |
| Espruino runtime | `2v29.535` |
| Espruino integration revision | `215fe4e16` |
| Exported standalone source | `563a3a0a36fc83aab84515481f516dc5738cca9b` |
| Official Espruino upstream base | `3b5c8d97fa0678ec1da49a322f5f1fa990374a7a` |
| Build | Stock 70 KB native-heap profile, `BOARD=ESP32C3_IDF5 RELEASE=1 USE_XFSM=1` |

The later standalone commits named by the trace and lifecycle records change
only qualification tooling and test fixtures. The native XFSM engine deployed
in revision `215fe4e16` is unchanged between all three runs.

## Build Result

The clean production image is 1,724,480 bytes and leaves 323,520 bytes, or 16
percent, of the application partition free. The flashed image and retained
build image have the same SHA-256 value:

```text
0f6b04105ed76f286d06e990f29f30f4b15fbf17004b45ee1c6a36da9ea490eb
```

## Physical Result

All current production checks passed:

- 29 of 29 production JavaScript suites;
- nine of nine canonical traces, compared exactly with their reviewed expected
  output;
- shallow and deep history semantics and diagnostics;
- host integration, cleanup, event serialization, maximum-depth Storage-backed
  construction, and production allocation and diagnostic pressure; and
- whole-interpreter save/reboot/restoration and reset cleanup.

The compatibility trace remains one canonical 56-record test. On the C3 the
physical runner executes its marked sections separately to keep temporary
JavaScript use inside the finite JsVar pool, merges and resequences the records,
and performs one exact comparison with the same canonical expected output used
on Linux.

The lifecycle run saved 53,235 interpreter bytes, compressed them to 10,372
bytes, restored the actor without replay, and then passed reset cleanup. The
runner first erased and verified the `.bootcde` and `.varimg` Storage entries,
so the result was not affected by an older saved program.

The machine-readable records are:

- [production suites](../../tests/results/esp32-riscv/2026-10-26-standalone-production-suites.json);
- [canonical traces](../../tests/results/esp32-riscv/2026-10-26-standalone-traces.json);
- [lifecycle](../../tests/results/esp32-riscv/2026-10-26-standalone-lifecycle.json); and
- [qualification summary](../../tests/results/esp32-riscv/2026-10-26-standalone-qualification.json).

## Findings

The first physical pass exposed assumptions in the standalone test harness,
not defects in the native engine. The harness now uses the supported module
cache operation, loads large traces through Storage, keeps REPL cleanup in one
statement, partitions the large physical compatibility trace without changing
its canonical result, and starts lifecycle tests from a verified clean saved-
program state. Linux execution remains unpartitioned and produces the same
compatibility trace.

No native XFSM implementation change was required.

## Remaining Physical Work

This run does not replace the current-candidate physical repetition on the
original ESP32, Pico, or MDBT42Q. It also does not repeat the two-board WiFi,
HTTPS/TLS, and BLE coexistence test. Those activities remain scheduled when
the required boards and bench arrangement are available. Earlier qualified
results remain historical evidence but are not relabelled as results for this
candidate.
