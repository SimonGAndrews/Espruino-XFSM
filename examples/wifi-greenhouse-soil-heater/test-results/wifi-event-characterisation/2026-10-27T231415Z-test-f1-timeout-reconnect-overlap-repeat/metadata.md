# Test Run Metadata

## Identity

- Run ID: `2026-10-27T231415Z-test-f1-timeout-reconnect-overlap-repeat`
- Test family: Wi-Fi event characterisation
- Scenario: Test F1 — reconnect after application timeout without cleanup
- Start time (UTC): `2026-10-27T23:14:15Z`
- End time (UTC): `2026-10-27T23:16:04Z`
- Operator: Codex, at user request
- Result: passed; overlapping reconnect rejection reproduced

## Revisions

- Espruino-XFSM revision: `667cc2afb3dd09ae759c0e5afd7eb7fa34550472`
- Espruino revision: `215fe4e16cf134365c2db6a13cc18494293fc8e0`
- XFSM source revision: `563a3a0a36fc83aab84515481f516dc5738cca9b`
- Diagnostic source:
  `examples/wifi-greenhouse-soil-heater/wifi-event-characterisation.js`
- Diagnostic source SHA-256:
  `2fa5d22fe9b4ac1d55f712220018c21ed26de551e3df875b04ecae55a25dac3b`

## Target And Environment

- Board: Seeed Studio XIAO ESP32C3
- Firmware profile: `ESP32C3_IDF5`
- Firmware version: Espruino `2v29.535`
- Console: persistent ESP32-C3 identity resolved to `/dev/ttyACM0`
- Requested network role: deliberately unavailable profile
- Other bench AP state: valid-profile AP online
- Heating cable and Shelly device: disconnected

## Test Parameters

- Operation 1: `connect("unavailable", 5000)`
- Board-scheduled recovery: observation plus `reconnect()` 5,500 ms after
  operation 1 is requested
- Operation 2 timeout: configured default `20000 ms`
- Cleanup before operation 2: none

The board-side schedule ensures operation 2 is requested immediately after the
application timeout and before the expected native terminal failure, without
host terminal latency.

## Evidence Files

- Canonical diagnostic: `../../../wifi-event-characterisation.js`
- Raw console capture: `raw-serial.log`
- Operator notes: `operator-notes.md`
- Reviewed findings: `findings.md`

## Deviations And Data Handling

- Procedure deviations: none
- Interruptions or capture loss: none observed; sequences 1 through 18 are
  contiguous
- Secret review completed by: Codex; the final credential-value scan across
  all retained results found zero matches
- Redactions or transformations: none in `raw-serial.log`; the diagnostic
  generated its normal field-name-based redactions
