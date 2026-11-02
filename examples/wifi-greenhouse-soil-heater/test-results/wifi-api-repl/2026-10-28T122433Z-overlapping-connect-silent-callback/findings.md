# Findings

Status: passed for this physical run.

The retained Web IDE screenshot independently ties the visible program,
firmware profile and version, and console results together in one artifact.

## Observed Facts

- The program requested a connection to a deliberately nonexistent SSID.
- It requested a second nonexistent SSID 6 seconds later, without first
  cancelling or settling the original native operation.
- ESP-IDF printed `sta is connecting, cannot set config`.
- Espruino printed an `esp_wifi_set_config` error with code `12294
  (ESP_ERR_WIFI_STATE)`.
- The second `Wifi.connect()` returned to JavaScript normally. The `catch`
  branch did not run.
- Neither connection callback had run at the 30-second observation point.
- `Wifi.getDetails()` reported `NO_AP_FOUND`, and `Wifi.getIP()` reported
  `0.0.0.0` for the address, netmask, and gateway.

## Source-Supported Interpretation

- A second connection request cannot replace the station configuration while
  the ESP-IDF station is still connecting.
- This native rejection is reported only as console error output by this
  Espruino build; it is not exposed as a thrown JavaScript error or a connect
  callback result.
- Espruino clears its single stored connect callback before attempting the
  rejected reconfiguration. This accounts for the absence of the first
  callback as well as the second one. That explanation comes from source-code
  inspection; the REPL transcript alone proves only that neither callback ran.
- Ordering between ESP-IDF task output and JavaScript prints should not be
  inferred solely from their adjacent console lines.

## Design Implications

- The Wi-Fi FSM must serialize native connection attempts.
- An application timeout must not immediately start another `Wifi.connect()`;
  native cleanup and a settled boundary are required first.
- Each connection attempt still needs an application-owned timeout because a
  rejected call can otherwise remain callback-silent indefinitely.
- Console error text is diagnostic evidence, not a usable FSM event.
- These conclusions reinforce the current statechart safeguards and do not
  require a statechart change.
