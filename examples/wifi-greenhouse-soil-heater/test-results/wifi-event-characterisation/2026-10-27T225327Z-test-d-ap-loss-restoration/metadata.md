# Test Run Metadata

## Identity

- Run ID: `2026-10-27T225327Z-test-d-ap-loss-restoration`
- Test family: Wi-Fi event characterisation
- Scenario: Test D — AP disappears after successful connection and is restored
- Start time (UTC): `2026-10-27T22:53:27Z`
- End time (UTC): `2026-10-27T23:02:35Z`
- Operator: Codex capture with user-operated AP controls
- Result: invalid environmental run; retained for diagnostic evidence and not
  counted as Test D

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
- Access point initially available: yes, to be proven by successful connection
- Heating cable confirmed disconnected: yes, per bench confirmation
- Shelly commands prevented: yes; Shelly device is disconnected

## Test Parameters

- Credential profile name: `valid`
- Application timeout: `20000 ms`
- AP-off observation: invalid because the first disable operation did not take
  effect and the later successful operation had no pre-operation marker
- AP-restored observation: not performed in this run
- Initial Wi-Fi state: to be recorded by the diagnostic

No SSID value or password is recorded.

## Procedure

1. Resolve the persistent serial identity and confirm exclusive device access.
2. Verify `wifi-event-config.json` exists without reading its contents into
   the retained result.
3. Reset volatile JavaScript state and load the canonical diagnostic with the
   XON/XOFF-aware paced serial transport.
4. Send `WifiEventCharacterisation.connect("valid")` once and verify a usable
   IP is observed.
5. Record `operator_about_to_disable_ap`, cue the user, and record completion
   after the AP is manually disabled.
6. Issue no Wi-Fi command while observing connection loss.
7. Record `operator_about_to_restore_ap`, cue the user, and record completion
   after the AP is restored.
8. Issue no reconnect command while observing whether native reconnection
   occurs.
9. Record a final driver/IP observation, then end the evidence boundary.
10. After the evidence boundary, stop listeners, disconnect, and reset volatile
    JavaScript state.

## Evidence Files

- Canonical diagnostic: `../../../wifi-event-characterisation.js`
- Raw console capture: `raw-serial.log`
- Operator notes: `operator-notes.md`
- Reviewed findings: `findings.md`

## Deviations And Data Handling

- Procedure deviations: the first reported AP-disable operation was not
  successful; a later operation disabled both the test AP and this host's
  network path. The host was subsequently moved to another SSID. The actual
  successful AP-disable time is therefore unknown and restoration was not
  exercised.
- Interruptions or capture loss: the host network path was interrupted, but
  the local USB serial capture continued and retained contiguous sequences 1
  through 20
- Secret review completed by: automated comparison against every configured
  SSID and password value, followed by structural review
- Redactions or transformations: none in `raw-serial.log`; the diagnostic
  generated its normal field-name-based redactions
- The diagnostic and documentation are not yet committed, so the repository
  revision alone cannot reconstruct this run. The source hash identifies the
  exact canonical diagnostic used.
