# Findings

Status: passed for this physical run.

## Observed Facts

- The raw capture contains 15 parseable `WIFI_DIAG` records with contiguous
  sequence numbers 1 through 15.
- The diagnostic began with Wi-Fi status `UNINITIALIZED` and no assigned IP.
- The connection request armed the 20,000 ms application timeout.
- The native `associated` event occurred 5,223 ms after the request.
- Immediately after `associated`, `wifi.getDetails().status` was `connected`,
  but `wifi.getIP().ip` was still `0.0.0.0`.
- The native `connected` event occurred 6,791 ms after the request and carried
  the assigned IP, netmask, and gateway.
- The application timeout was cancelled before the connect callback.
- The connect callback occurred 7,098 ms after the request, 307 ms after the
  native `connected` event. It reported no error and carried the same network
  details.
- At the capture-end observation, 35,363 ms after the request, the device
  remained connected with its assigned IP.
- No `disconnected`, `dhcp_timeout`, or application-timeout record occurred.
- No configured SSID or password value appears in any retained result file.

## Event Order In This Run

```text
connect requested
  -> associated
  -> connected
  -> application timeout cancelled
  -> connect callback succeeds
```

This is an observation from one physical run, not yet a general ordering
guarantee.

## Design Implications To Carry Forward

- `wifi.getDetails().status === "connected"` did not prove that DHCP had
  completed; IP state or the native `connected` event is needed when reporting
  network readiness.
- In this run, the native `connected` event preceded the successful callback
  and supplied usable IP information.
- The application timeout must remain active until an accepted readiness
  signal or callback is processed; association alone is insufficient.
- `Date.now()` was not synchronised to host UTC, so event comparisons use the
  diagnostic's monotonic `elapsedMs` values.

No retry or failure-policy conclusion can be drawn from Test A.
