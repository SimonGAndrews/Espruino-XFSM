# Wi-Fi Greenhouse Soil Heater

Status: requirements baseline and initial physical Wi-Fi characterisation
complete; no XFSM application machine implemented yet.

This example will use XFSM on an ESP32-C3 to manage Wi-Fi connectivity and a
greenhouse soil heater. It is intended both as a practical controller and as a
real-world exercise of XFSM hierarchical state-machine behaviour.

## Project Documents

- [`requirements.md`](requirements.md) — confirmed requirements, proposed
  safety baseline, assumptions, and open decisions.
- [`development-plan.md`](development-plan.md) — phased implementation plan,
  entry/exit criteria, and gaps.
- [`wifi-statechart.md`](wifi-statechart.md) — proposed initial Wi-Fi actor
  states, events, context, guards, actions, and status contract.
- [`wifi-event-characterisation.md`](wifi-event-characterisation.md) — first
  physical experiment and Tests A–F.
- [`wifi-event-characterisation.js`](wifi-event-characterisation.js) —
  standalone ESP32-C3 diagnostic; it contains no FSM.
- [`wifi-event-characterisation.config.example.json`](wifi-event-characterisation.config.example.json)
  — credential-profile template for the diagnostic.
- [`test-results/`](test-results/README.md) — authoritative per-run test
  evidence, metadata, operator notes, and findings.

## Current Position

Initial physical Wi-Fi event characterisation Tests A–F now each have an
accepted result on the selected ESP32-C3 firmware. Repeatability review remains
before Phase 1 exit, so production event ordering and retry policy are not yet
final. All test results are retained under `test-results/` in immutable run
directories; external terminal logs are not the evidence of record.

The proposed initial actor design is now recorded in
[`wifi-statechart.md`](wifi-statechart.md). It is a reviewable Phase 2 contract,
not yet an implemented machine.

The prototype is a Seeed Studio XIAO ESP32C3. Its current qualified production
image reports `ESP32C3_IDF5`, Espruino `2v29.535`, and integration revision
`215fe4e16`, with the public `Wifi` and `XFSM` APIs present.

The mains heater and Shelly device are currently not connected on the
workbench. Both must remain disconnected during the Wi-Fi and
controller-only development phases. Physical heater operation is gated by the
unresolved electrical and thermal safety requirements in `requirements.md`.

## Licence And Provenance

Files in this directory are provided under the repository's
[`examples/` MIT License](../LICENSE). The example is project-authored and is
not adapted from XState or other third-party example code.
