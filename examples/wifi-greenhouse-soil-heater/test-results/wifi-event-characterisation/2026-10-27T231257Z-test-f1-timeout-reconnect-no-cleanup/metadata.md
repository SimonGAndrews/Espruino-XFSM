# Test Run Metadata

## Identity

- Run ID: `2026-10-27T231257Z-test-f1-timeout-reconnect-no-cleanup`
- Test family: Wi-Fi event characterisation
- Scenario: Test F1 — reconnect after application timeout without cleanup
- Start time (UTC): `2026-10-27T23:12:57Z`
- End time (UTC): `2026-10-27T23:14:15Z`
- Operator: Codex, at user request
- Result: invalid timing run; native operation completed before the host-issued
  reconnect reached the board

## Revisions

- Espruino-XFSM revision: `667cc2afb3dd09ae759c0e5afd7eb7fa34550472`
- Espruino-XFSM worktree: modified example scaffold; see deviations below
- Espruino revision: `215fe4e16cf134365c2db6a13cc18494293fc8e0`
- XFSM source revision reported by the Espruino integration:
  `563a3a0a36fc83aab84515481f516dc5738cca9b`
- Diagnostic/example revision: uncommitted working-tree version based on the
  Espruino-XFSM revision above
- Diagnostic source:
  `examples/wifi-greenhouse-soil-heater/wifi-event-characterisation.js`
- Diagnostic source SHA-256:
  `2fa5d22fe9b4ac1d55f712220018c21ed26de551e3df875b04ecae55a25dac3b`

## Target And Environment

- Board: Seeed Studio XIAO ESP32C3
- Firmware profile: `ESP32C3_IDF5`
- Firmware version: Espruino `2v29.535`
- Persistent console identity:
  `/dev/serial/by-id/usb-Espressif_USB_JTAG_serial_debug_unit_9C:9E:6E:F7:41:64-if00`
- Resolved console device: `/dev/ttyACM0`
- Requested network role: deliberately unavailable profile
- Other bench AP state: the valid-profile AP remains online
- Heating cable confirmed disconnected: yes, per bench confirmation
- Shelly commands prevented: yes; Shelly device is disconnected

## Test Parameters

- Initial credential profile: `unavailable`
- First application timeout: `5000 ms`
- Recovery operation: `reconnect()` without native cleanup
- Reconnect timeout: default configured `20000 ms`
- Initial Wi-Fi state: to be recorded by the diagnostic

No SSID value or password is recorded.

## Procedure

1. Reset volatile state and load the canonical diagnostic with paced serial.
2. Send `WifiEventCharacterisation.connect("unavailable", 5000)` once.
3. Wait for `application_connect_timeout`; do not call disconnect.
4. Record a pre-reconnect observation and immediately call
   `WifiEventCharacterisation.reconnect()`.
5. Observe native events, both application callback identities, timers, and
   final driver/IP state for at least 35 seconds after reconnect.
6. Record a final observation, then close the evidence boundary.
7. Stop listeners, disconnect, and reset volatile state after capture.

## Evidence Files

- Canonical diagnostic: `../../../wifi-event-characterisation.js`
- Raw console capture: `raw-serial.log`
- Operator notes: `operator-notes.md`
- Reviewed findings: `findings.md`

## Deviations And Data Handling

- Procedure deviations: host terminal scheduling delayed `reconnect()` until
  after operation 1's native failure and callback. The run therefore did not
  overlap native operations as required by F1.
- Interruptions or capture loss: none observed; sequences 1 through 23 are
  contiguous
- Secret review completed by: Codex; the final credential-value scan across
  all retained results found zero matches
- Redactions or transformations: none in `raw-serial.log`; the diagnostic
  generated its normal field-name-based redactions
- The diagnostic and documentation are not yet committed, so the repository
  revision alone cannot reconstruct this run. The source hash identifies the
  exact canonical diagnostic used.
