# Findings

Status: passed for this physical run.

## Observed Facts

- The raw capture contains 14 parseable `WIFI_DIAG` records with contiguous
  sequence numbers 1 through 14.
- The run began with driver status `ASSOC_LEAVE` and no assigned IP.
- The connection request armed the 20,000 ms application timeout.
- The application timeout fired 20,316 ms after the request and explicitly
  left the native connection work running.
- The native `disconnected` event occurred 20,965 ms after the request: 649 ms
  after the application timeout. Its reason was `15` and its message was
  `4WAY_HANDSHAKE_TIMEOUT`.
- The connect callback occurred 21,316 ms after the request: 351 ms after the
  native `disconnected` event and 1,000 ms after the application timeout. It
  reported `4WAY_HANDSHAKE_TIMEOUT`, no callback details, and identified
  itself as belonging to the current application operation.
- No `associated`, `connected`, or `dhcp_timeout` event occurred.
- No additional native event or callback was observed through 60,334 ms after
  the request. No application-level retry was requested.
- The final driver status remained `4WAY_HANDSHAKE_TIMEOUT`, with no IP.
- No configured SSID or password value appears in any retained result file.

## Event Order In This Run

```text
connect requested
  -> application timeout
  -> disconnected (reason 15 / 4WAY_HANDSHAKE_TIMEOUT)
  -> connect callback fails (4WAY_HANDSHAKE_TIMEOUT)
```

This is an observation from one physical run, not yet a general ordering
guarantee. The trace shows no externally visible automatic retry after the
failure callback; it cannot prove that no internal retry occurred during the
preceding handshake period.

## Design Implications To Carry Forward

- An incorrect password can generate `disconnected` even though the
  application never reached a connected state. The event cannot be interpreted
  solely as loss of an established connection.
- The application timeout may win the race against the driver's definitive
  failure notification and callback. Both later messages must therefore be
  safe to process after the FSM has left its connecting state.
- A connection-attempt token can identify the later application callback, but
  the native `disconnected` event still requires state and driver-status
  reconciliation.
- The driver failure reason is useful evidence for credential-failure policy,
  but production policy should not depend on this single reason code until
  repeatability and other failure scenarios are compared.
- An explicit cleanup disconnect callback does not necessarily reset
  `getDetails().status` to a neutral string; IP state and FSM-owned state remain
  necessary.
