# Findings

Status: passed.

## Observed Facts

- The final raw capture contains five parseable `WIFI_DIAG` records with
  contiguous sequence numbers 1 through 5.
- Startup recorded board `ESP32C3_IDF5`, Espruino `2v29.535`, and firmware Git
  identifier `215fe4e16`.
- All four native event listeners were installed.
- The initial Wi-Fi status was `UNINITIALIZED`; IP, netmask, and gateway were
  `0.0.0.0`.
- The diagnostic loaded all three named profiles from
  `wifi-event-config.json` without printing credential values.
- The explicit `serial_capture_smoke` observation was recorded.
- No connection request, Wi-Fi lifecycle event, application timeout, or
  Shelly/heater operation occurred.
- Automated comparison found no configured SSID or password value in any
  retained result file.

## Tooling Findings

- The installed Espruino CLI does not accept the persistent serial symlink;
  host commands must resolve it to `/dev/ttyACM0` immediately before use.
- The original configuration Storage name was too long. The accepted
  on-device name is `wifi-event-config.json`.
- This CLI requires an interactive PTY to finish a Storage upload.
- Its JavaScript file-upload path did not leave this diagnostic running even
  though it printed `Upload Complete`.
- The repository's paced pyserial transport loaded and ran the diagnostic
  successfully and is the selected capture transport for the physical tests.

## Interpretation

The serial path, Storage configuration, diagnostic startup, trace format, and
result retention are ready for Test A. This smoke test provides no evidence
about native Wi-Fi event order or retry behaviour.
