# Test Run Metadata

## Identity

- Run ID: `2026-10-27T231825Z-test-f2-timeout-cleanup-reconnect-repeat`
- Test family: Wi-Fi event characterisation
- Scenario: Test F2 — cleanup after application timeout, then reconnect
- Start time (UTC): `2026-10-27T23:18:25Z`
- End time (UTC): `2026-10-27T23:19:30Z`
- Operator: Codex, at user request
- Result: passed; explicit cleanup allowed a later valid connection

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
- Initial requested network: deliberately unavailable profile
- Recovery network: valid profile, online
- Heating cable and Shelly device: disconnected

## Test Parameters

- Operation 1: `connect("unavailable", 5000)`
- Cleanup: top-level `disconnect()` after observing operation 1's application
  timeout and before its native terminal event
- Settling boundary: wait for native disconnect and all related callbacks
- Operation 2: top-level `connect("valid", 20000)`
- Commands are delivered separately by the host to avoid the nested callback
  lifetime fault observed in the preceding invalid run

## Evidence Files

- Canonical diagnostic: `../../../wifi-event-characterisation.js`
- Raw console capture: `raw-serial.log`
- Operator notes: `operator-notes.md`
- Reviewed findings: `findings.md`

## Deviations And Data Handling

- Procedure deviations: host polling delayed the cleanup request until 7,994
  ms after the application timeout; the original native operation was still
  active and was terminated by that request
- Interruptions or capture loss: none observed; diagnostic sequences 1 through
  32 are contiguous
- Secret review completed by: Codex; all non-public SSID/password values from
  the ignored local configuration were scanned against every retained result,
  with zero matches
- Redactions or transformations: none in `raw-serial.log`; the diagnostic
  generated its normal field-name-based redactions
