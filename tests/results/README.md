# Test And Build Results

These result records were migrated from `XState-Espruino-Project` revision
`ecfe27accc966d429491834cd229221728ffd338`. Historical paths, branches, and
Espruino commit identifiers are evidence fields and are intentionally not
rewritten to current standalone-repository values.

This directory indexes reproducible Xstate-fsm-c results. It must not contain
claims inferred from an unrecorded local run.

Create target-specific result directories as evidence becomes available:

- `linux/`
- `pico/`
- `mdbt42q/`
- `esp32-riscv/` (ESP32-C3 with ESP-IDF 5)
- `esp32-xtensa/` (original ESP32 with ESP-IDF 5)

## Result Records

Each committed result record must identify:

- conformance case ID or measurement name;
- date and result state from the
  [conformance matrix](../conformance-matrix.md);
- canonical Espruino-XFSM revision and specification version;
- Espruino implementation revision and upstream base;
- target, board definition, compiler and version, relevant build and
  optimization flags, CPU architecture, pointer width, byte order,
  `process.memory().blocksize`, and XFSM stack-reserve setting;
- exact command or runner invocation;
- expected and observed outcome;
- retained artifact or report paths; and
- any limitation, failure, or reasoned skip.

Prefer concise machine-readable output plus a small metadata file for automated
runs. Large binaries, transient build trees, and unrestricted console logs do
not belong in Git. Reviewed interpretations and resource decisions belong in
[`../../docs/reports/`](../../docs/reports/).

The earlier constrained ARM records are the [Pico matched
build](pico/2026-09-29-product-profile-build.json), [Pico physical
qualification](pico/2026-09-29-m8-physical-qualification.json), and [MDBT42Q
matched build](mdbt42q/2026-09-29-product-profile-build.json), with its
[physical qualification](mdbt42q/2026-09-29-m8-physical-qualification.json).

Current standalone-workflow evidence is the [complete Linux host
qualification](linux/2026-10-26-standalone-qualification.json), the [original
ESP32 physical
qualification](esp32-xtensa/2026-10-26-standalone-qualification.json), and the
[ESP32-C3 physical
qualification](esp32-riscv/2026-10-26-standalone-qualification.json), the
[Pico physical qualification](pico/2026-10-27-standalone-qualification.json),
and the [MDBT42Q physical
qualification](mdbt42q/2026-10-26-standalone-qualification.json).
Each target summary links its separate production-suite, exact-trace, and
lifecycle records. The implementation status identifies current maintenance
and release-review work.

The current two-board XFSM, BLE, WiFi, and HTTPS/TLS repetition is recorded in
the [ESP32 service-coexistence
result](esp32-service/2026-10-26-standalone-service-coexistence.json).
