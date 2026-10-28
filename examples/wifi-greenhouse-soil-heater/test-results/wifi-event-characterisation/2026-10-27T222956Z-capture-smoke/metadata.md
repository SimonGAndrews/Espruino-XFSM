# Test Run Metadata

## Identity

- Run ID: `2026-10-27T222956Z-capture-smoke`
- Test family: Wi-Fi event characterisation infrastructure
- Scenario: serial-capture smoke test without a Wi-Fi connection request
- Start time (UTC): `2026-10-27T22:29:56Z`
- End time (UTC): `2026-10-27T22:35:41Z`
- Operator: Codex, at user request
- Result: passed after two retained setup failures

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
- Console/serial device:
  `/dev/serial/by-id/usb-Espressif_USB_JTAG_serial_debug_unit_9C:9E:6E:F7:41:64-if00`
- Access-point role: not exercised
- Access point initially available: not required for this smoke test
- Heating cable confirmed disconnected: yes, per bench confirmation
- Shelly commands prevented: yes; Shelly device is disconnected

## Test Parameters

- Credential profile name: none selected
- Application timeout: not armed
- Observation period: diagnostic startup plus explicit smoke observation
- Initial Wi-Fi state: `UNINITIALIZED`; IP, netmask, and gateway were `0.0.0.0`

No SSID value or password is recorded.

## Procedure

1. Resolve the persistent serial path and confirm that no process owns it.
2. Upload the ignored local configuration to Espruino Storage as
   `wifi-event-config.json` without retaining its contents in the result
   directory.
3. Load `wifi-event-characterisation.js` while capturing console output.
4. Evaluate
   `WifiEventCharacterisation.observe("serial_capture_smoke")` without
   requesting a connection.
5. Validate the captured `WIFI_DIAG` records and review retained files for
   credential exposure.

## Evidence Files

- Raw console capture: `raw-serial.log`
- Operator notes: `operator-notes.md`
- Reviewed findings: `findings.md`
- First failed host capture: `capture-attempt-1-host.log`,
  `capture-attempt-1-input.log`, and `capture-attempt-1-timing.log`
- Second failed host capture: `capture-attempt-2-host.log`,
  `capture-attempt-2-input.log`, and `capture-attempt-2-timing.log`

## Deviations And Data Handling

- Procedure deviations: the installed Espruino CLI rejected the persistent
  symlink, requiring the link to be resolved to `/dev/ttyACM0`. The first
  configuration upload then exposed an overlength on-device Storage filename;
  the diagnostic was corrected before the successful capture attempt.
- Interruptions or capture loss: no loss in the final paced-pyserial capture;
  failed host attempts were retained separately
- Secret review completed by: automated comparison against every configured
  SSID and password value, followed by structural review
- Redactions or transformations: none in `raw-serial.log`; the diagnostic
  generated its normal field-name-based redactions
- The diagnostic and documentation are not yet committed, so the repository
  revision alone cannot reconstruct this run. The retained result identifies
  this limitation explicitly.
