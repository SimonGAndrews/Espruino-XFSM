# Test Run Metadata

## Identity

- Run ID: `2026-10-28T122433Z-overlapping-connect-silent-callback`
- Test family: ESP32-C3 Wi-Fi API REPL characterisation
- Scenario: overlapping `Wifi.connect()` call is rejected without a JavaScript
  exception or callback
- Start time (UTC): not independently recorded
- End time (UTC): not independently recorded; the result was reported before
  this record was created at `2026-10-28T12:24:33Z`
- Operator: Simon
- Result: passed; callback-silent overlapping connection failure reproduced

## Revisions

- Espruino-XFSM revision:
  `667cc2afb3dd09ae759c0e5afd7eb7fa34550472`
- Espruino revision: `215fe4e16cf134365c2db6a13cc18494293fc8e0`
- XFSM source revision reported by the Espruino integration:
  `563a3a0a36fc83aab84515481f516dc5738cca9b`
- Diagnostic/example revision: uncommitted working-tree reconstruction saved
  after the run; the retained file includes an MIT licence header that was not
  present in the Web IDE editor shown in the screenshot
- Diagnostic source:
  `examples/wifi-greenhouse-soil-heater/wifi-connect-overlap-repro.js`
- Retained diagnostic source SHA-256:
  `32095ea88b5bf171556b7a45bf39ed3b87c806558529d9db7b16a5cb2df3ebd9`
- Screenshot:
  `images/WifiIssueRepl_twoConnects.png`
- Screenshot SHA-256:
  `1c7b5f4c92771254402827f30320c86826f3b87c6ae54e80b472394babc079ac`

## Target And Environment

- Board: Seeed Studio XIAO ESP32C3
- Firmware profile: `ESP32C3_IDF5`
- Firmware version: Espruino `2v29.535`
- Console/serial device: Espruino Web IDE over Web Serial, reported as
  `webserial:27b6:077d`; operating-system device path not recorded
- Access-point role: both requested SSIDs were deliberately nonexistent
- Access point initially available: no
- Heating cable confirmed disconnected: not independently re-confirmed for
  this run; the recorded bench baseline says it was disconnected
- Shelly commands prevented: the Shelly device was absent from the recorded
  bench baseline, and this diagnostic contains no Shelly control code

## Test Parameters

- Credential profile: two fictitious SSIDs embedded in the reproduction
- First connection request: immediately after program start
- Second connection request: 6 seconds after the first request
- Application timeout: none; this test observes the native API directly
- Observation period: 30 seconds
- Initial Wi-Fi state: not recorded

The embedded password is a non-secret placeholder used only with deliberately
nonexistent SSIDs.

## Procedure

1. Load `wifi-connect-overlap-repro.js` into the XIAO ESP32C3 from the
   Espruino Web IDE.
2. Allow the program to request its first deliberately unavailable SSID.
3. Allow the scheduled second request to run after 6 seconds without cleaning
   up the first request.
4. Retain the callback count, `Wifi.getDetails()`, and `Wifi.getIP()` output
   printed after 30 seconds.
5. Copy the REPL output without editing it into `raw-serial.log`.

## Evidence Files

- Raw console capture: `raw-serial.log`
- Web IDE screenshot:
  `../../../../../images/WifiIssueRepl_twoConnects.png`
- Operator notes: `operator-notes.md`
- Reviewed findings: `findings.md`

## Deviations And Data Handling

- Procedure deviations: none reported
- Interruptions or capture loss: none reported; exact wall-clock timing was
  not captured
- Secret review completed by: Codex
- Redactions or transformations: none; the raw transcript is preserved exactly
  as supplied by the operator. The retained `.js` file was reconstructed after
  the run and is not claimed to be a byte-for-byte copy of the uploaded text.
