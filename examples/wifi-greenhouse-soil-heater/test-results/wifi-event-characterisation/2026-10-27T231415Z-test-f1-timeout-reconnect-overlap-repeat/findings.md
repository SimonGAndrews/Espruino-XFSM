# Findings

Status: passed for this physical run.

## Observed Facts

- Operation 1's application timeout fired 5,314 ms after its request and left
  native work running.
- Board-scheduled operation 2 was requested 753 ms after that timeout.
- ESP-IDF reported `sta is connecting, cannot set config`; Espruino reported
  `esp_wifi_set_config: 12294 (ESP_ERR_WIFI_STATE)` on the console.
- The JavaScript `wifi.connect()` call did not throw synchronously, so the
  diagnostic returned normally and armed operation 2's 20-second timer.
- Operation 1's native `disconnected` / `NO_AP_FOUND` event occurred 14,803 ms
  after its request.
- No connect callback was delivered for operation 1 or operation 2 during the
  61-second capture.
- Operation 2's application timeout fired 20,217 ms after its request.
- The final state remained `NO_AP_FOUND` with no IP.

## Design Implications

- A new `wifi.connect()` must not be issued while prior native connection work
  remains active. The driver rejects overlapping configuration with
  `ESP_ERR_WIFI_STATE`.
- Console error output is not a usable application event: the JavaScript call
  can return without throwing and without delivering a callback.
- Starting the second attempt can interfere with callback delivery for the
  original attempt. Attempt tokens alone cannot repair a callback that never
  arrives.
- After an application timeout, explicit native cleanup and a settled cleanup
  boundary are required before retrying on this firmware.
- Every application attempt still needs its own timeout because a rejected
  native request may otherwise remain callback-silent indefinitely.
