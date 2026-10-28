# Test Run Metadata

## Identity

- Run ID: `2026-10-27T223803Z-test-a-normal`
- Test family: Wi-Fi event characterisation
- Scenario: Test A — normal connection
- Start time (UTC): `2026-10-27T22:38:03Z`
- End time (UTC): `2026-10-27T22:40:23Z`
- Operator: Codex, at user request
- Result: passed; one physical run recorded

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
- Access-point role: configured valid-profile test AP
- Access point initially available: yes, established by successful association
- Heating cable confirmed disconnected: yes, per bench confirmation
- Shelly commands prevented: yes; Shelly device is disconnected

## Test Parameters

- Credential profile name: `valid`
- Application timeout: `20000 ms`
- Post-request capture period: at least `30000 ms`
- Initial Wi-Fi state: `UNINITIALIZED`; IP, netmask, and gateway were `0.0.0.0`

No SSID value or password is recorded.

## Procedure

1. Resolve the persistent serial identity and confirm exclusive device access.
2. Verify `wifi-event-config.json` exists without reading its contents into
   the retained result.
3. Reset volatile JavaScript state and load the diagnostic with the
   XON/XOFF-aware paced serial transport.
4. Send `WifiEventCharacterisation.connect("valid")`.
5. Capture all output for at least 30 seconds after the request.
6. Review the trace without imposing an expected callback or event order.
7. After the evidence boundary, stop diagnostic listeners, explicitly
   disconnect Wi-Fi, and reset volatile JavaScript state.

## Evidence Files

- Raw console capture: `raw-serial.log`
- Operator notes: `operator-notes.md`
- Reviewed findings: `findings.md`

## Deviations And Data Handling

- Procedure deviations: none
- Interruptions or capture loss: none observed; sequences 1 through 15 are
  contiguous
- Secret review completed by: automated comparison against every configured
  SSID and password value, followed by structural review
- Redactions or transformations: none in `raw-serial.log`; the diagnostic
  generated its normal field-name-based redactions
- The diagnostic and documentation are not yet committed, so the repository
  revision alone cannot reconstruct this run. This limitation is explicit.
