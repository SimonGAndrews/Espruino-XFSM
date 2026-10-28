# Test Run Metadata

## Identity

- Run ID: `2026-10-27T231604Z-test-f2-timeout-cleanup-reconnect`
- Test family: Wi-Fi event characterisation
- Scenario: Test F2 — cleanup after application timeout, then reconnect
- Start time (UTC): `2026-10-27T23:16:04Z`
- End time (UTC): `2026-10-27T23:17:52Z`
- Operator: Codex, at user request
- Result: invalid; asynchronous diagnostic callback lost a local binding

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
- Cleanup: board-scheduled `disconnect()` 5,500 ms after operation 1 request
- Settling interval: 2,000 ms after cleanup request
- Operation 2: `reconnect()` using the unavailable profile
- Final recovery: not attempted because operation 2's callback raised a
  diagnostic `ReferenceError`

## Evidence Files

- Canonical diagnostic: `../../../wifi-event-characterisation.js`
- Raw console capture: `raw-serial.log`
- Operator notes: `operator-notes.md`
- Reviewed findings: `findings.md`

## Deviations And Data Handling

- Procedure deviations: the planned final valid-profile recovery was omitted
  after the diagnostic fault invalidated the run
- Interruptions or capture loss: none observed; diagnostic sequences 1 through
  28 are contiguous, followed by the captured JavaScript exception
- Secret review completed by: Codex; the final credential-value scan across
  all retained results found zero matches
- Redactions or transformations: none in `raw-serial.log`; the diagnostic
  generated its normal field-name-based redactions
