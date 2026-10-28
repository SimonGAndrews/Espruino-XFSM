# Findings

Status: passed for this physical run.

## Observed Facts

- The raw capture contains 21 parseable `WIFI_DIAG` records with contiguous
  sequence numbers 1 through 21.
- The initial valid connection produced native `associated` and `connected`
  events and a successful callback. The `connected` event occurred 7,144 ms
  after the connection request.
- At the operator disable-complete marker, the driver details still reported
  status `connected`, but IP, netmask, and gateway were already `0.0.0.0`.
- The native `disconnected` event occurred 7,412 ms after that completion
  marker. It reported reason `201`, message `NO_AP_FOUND`, and AP MAC
  `00:00:00:00:00:00`.
- The AP was restored without any ESP32 reconnect request.
- No native event, callback, or automatic reconnection occurred during the
  105,260 ms after the operator restore-complete marker.
- The final observation remained `NO_AP_FOUND` with no IP.
- No `dhcp_timeout` event occurred.
- No configured SSID or password value appears in any retained result file.

## Event Order In This Run

```text
connect requested
  -> associated
  -> connected
  -> connect callback succeeds
  -> AP disabled manually
  -> IP state clears
  -> disconnected (reason 201 / NO_AP_FOUND)
  -> AP restored manually
  -> no automatic reconnect during 105.260 s observation
```

This is one physical run, not yet a general timing guarantee.

## Design Implications To Carry Forward

- IP state cleared before the native disconnect notification while
  `getDetails().status` still said `connected`. A status snapshot may therefore
  be internally transitional, and consumers should not treat one field as a
  complete readiness truth.
- AP loss reported the same `NO_AP_FOUND` reason observed when initially
  connecting to an unavailable network. The FSM must use its current state and
  connection history to distinguish loss from initial failure.
- The driver did not automatically reconnect when the AP returned in this
  run. Application-owned recovery must schedule an explicit new connection
  attempt unless repeat testing demonstrates another supported native mode.
- AP restoration generated no event on its own. A retry timer or explicit
  provisioning/user event is required to prompt new native work.
- Late or ambiguous events still require reconciliation with current driver
  and IP observations; neither a generation number nor a status string alone
  establishes lifecycle ownership.
