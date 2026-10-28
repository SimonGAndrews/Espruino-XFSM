# Test Run Metadata

## Identity

- Run ID: `2026-10-27T230309Z-test-d-ap-loss-restoration-repeat`
- Test family: Wi-Fi event characterisation
- Scenario: Test D — AP disappears after successful connection and is restored
- Start time (UTC): `2026-10-27T23:03:09Z`
- End time (UTC): `2026-10-27T23:07:04Z`
- Operator: Codex capture with user-operated AP controls
- Result: passed; one valid physical run recorded after an earlier invalid
  environmental attempt

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
- Access-point role: valid-profile test AP, manually disabled and restored
- Access point initially available: yes, proven by successful association,
  connection, and usable IP
- Host control path: moved to a different SSID so disabling the test AP does
  not intentionally remove host connectivity
- Heating cable confirmed disconnected: yes, per bench confirmation
- Shelly commands prevented: yes; Shelly device is disconnected

## Test Parameters

- Credential profile name: `valid`
- Application timeout: `20000 ms`
- AP-off observation: native disconnect occurred 7,412 ms after the operator
  disable-complete marker
- AP-restored observation: 105,260 ms after the restore-complete marker without
  an application reconnect request
- Initial Wi-Fi state: `NO_AP_FOUND`, retained from the previous failed
  operation; IP, netmask, and gateway were `0.0.0.0`

No SSID value or password is recorded.

## Procedure

1. Resolve the persistent serial identity and confirm exclusive device access.
2. Reset volatile state and load the canonical diagnostic with paced serial.
3. Send `WifiEventCharacterisation.connect("valid")` once; require a usable IP.
4. Record a pre-disable marker, cue the user, and record completion immediately
   after the AP is manually disabled.
5. Issue no Wi-Fi command while observing connection loss.
6. After the native disconnect, record a pre-restore marker, cue the user, and
   record completion immediately after AP restoration.
7. Issue no reconnect command while observing whether native reconnection
   occurs.
8. Record a final observation, then close the evidence boundary.
9. Stop listeners, disconnect, and reset volatile state after capture.

## Evidence Files

- Canonical diagnostic: `../../../wifi-event-characterisation.js`
- Raw console capture: `raw-serial.log`
- Operator notes: `operator-notes.md`
- Reviewed findings: `findings.md`

## Deviations And Data Handling

- Procedure deviations: none; the final observation exceeded the planned
  90-second post-restore minimum
- Interruptions or capture loss: none observed; sequences 1 through 21 are
  contiguous
- Secret review completed by: automated comparison against every configured
  SSID and password value, followed by structural review
- Redactions or transformations: none in `raw-serial.log`; the diagnostic
  generated its normal field-name-based redactions
- The diagnostic and documentation are not yet committed, so the repository
  revision alone cannot reconstruct this run. The source hash identifies the
  exact canonical diagnostic used.
