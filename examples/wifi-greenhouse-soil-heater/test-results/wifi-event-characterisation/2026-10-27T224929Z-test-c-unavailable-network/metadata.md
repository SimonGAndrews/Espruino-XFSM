# Test Run Metadata

## Identity

- Run ID: `2026-10-27T224929Z-test-c-unavailable-network`
- Test family: Wi-Fi event characterisation
- Scenario: Test C — unavailable network
- Start time (UTC): `2026-10-27T22:49:29Z`
- End time (UTC): `2026-10-27T22:51:13Z`
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
- Requested access-point role: deliberately absent network selected by the
  unavailable profile
- Other bench AP state: the valid-profile AP remained online
- Requested access point initially available: no; the driver reported
  `NO_AP_FOUND` with an all-zero AP MAC address
- Heating cable confirmed disconnected: yes, per bench confirmation
- Shelly commands prevented: yes; Shelly device is disconnected

## Test Parameters

- Credential profile name: `unavailable`
- Application timeout: `20000 ms`
- Post-request capture period: at least `60000 ms`
- Initial Wi-Fi state: `4WAY_HANDSHAKE_TIMEOUT`, retained from Test B; IP,
  netmask, and gateway were `0.0.0.0`

No SSID value or password is recorded.

## Procedure

1. Resolve the persistent serial identity and confirm exclusive device access.
2. Verify `wifi-event-config.json` exists without reading its contents into
   the retained result.
3. Reset volatile JavaScript state and load the canonical diagnostic with the
   XON/XOFF-aware paced serial transport.
4. Send `WifiEventCharacterisation.connect("unavailable")` once.
5. Capture all output for at least 60 seconds without disconnecting, retrying,
   or otherwise interpreting native events as transitions.
6. Record a final driver/IP observation and review the trace without imposing
   an expected callback or event order.
7. After the evidence boundary, stop diagnostic listeners, explicitly
   disconnect Wi-Fi, and reset volatile JavaScript state.

## Evidence Files

- Canonical diagnostic: `../../../wifi-event-characterisation.js`
- Raw console capture: `raw-serial.log`
- Operator notes: `operator-notes.md`
- Reviewed findings: `findings.md`

## Deviations And Data Handling

- Procedure deviations: none
- Interruptions or capture loss: none observed; sequences 1 through 13 are
  contiguous
- Secret review completed by: automated comparison against every configured
  SSID and password value, followed by structural review
- Redactions or transformations: none in `raw-serial.log`; the diagnostic
  generated its normal field-name-based redactions
- The diagnostic and documentation are not yet committed, so the repository
  revision alone cannot reconstruct this run. The source hash identifies the
  exact canonical diagnostic used.
