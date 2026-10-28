# Findings

Status: passed for this physical run.

## Observed Facts

- The raw capture contains 13 parseable `WIFI_DIAG` records with contiguous
  sequence numbers 1 through 13.
- The run began with the previous Test B driver status,
  `4WAY_HANDSHAKE_TIMEOUT`, and no assigned IP.
- The connection request armed the 20,000 ms application timeout.
- The native `disconnected` event occurred 14,815 ms after the request. Its
  reason was `201`, its message was `NO_AP_FOUND`, and its AP MAC address was
  `00:00:00:00:00:00`.
- The application timeout was cancelled 15,145 ms after the request.
- The connect callback occurred 15,168 ms after the request: 353 ms after the
  native `disconnected` event. It reported `NO_AP_FOUND`, no callback details,
  and identified itself as belonging to the current operation.
- No `associated`, `connected`, `dhcp_timeout`, or application-timeout event
  occurred.
- No additional native event or callback was observed through 60,329 ms after
  the request. No application-level retry was requested.
- The final driver status remained `NO_AP_FOUND`, with no IP.
- No configured SSID or password value appears in any retained result file.

## Event Order In This Run

```text
connect requested
  -> disconnected (reason 201 / NO_AP_FOUND)
  -> application timeout cancelled
  -> connect callback fails (NO_AP_FOUND)
```

This is an observation from one physical run, not yet a general ordering
guarantee. The trace shows no externally visible automatic retry after the
failure callback; it cannot prove that no internal scan or retry occurred
before the terminal failure.

## Design Implications To Carry Forward

- An unavailable network, like an incorrect password, generated
  `disconnected` without a preceding connected state. Parent fallback cannot
  treat every such event as loss of an established connection.
- In this run `NO_AP_FOUND` completed before the application timeout, whereas
  Test B's `4WAY_HANDSHAKE_TIMEOUT` completed after it. FSM policy must support
  either side winning the timeout race.
- The callback followed the native failure event and cancelled the timer, but
  native-event correlation still lacks an application attempt identifier.
- No externally visible driver retry followed the terminal callback during the
  observation window. Application retry policy should nevertheless remain
  configurable until repeat runs and AP-loss restoration are reviewed.
- Driver status strings persist across JavaScript reset and explicit cleanup.
  Runtime state must be reconstructed from current observations rather than
  assuming a neutral boot label.
