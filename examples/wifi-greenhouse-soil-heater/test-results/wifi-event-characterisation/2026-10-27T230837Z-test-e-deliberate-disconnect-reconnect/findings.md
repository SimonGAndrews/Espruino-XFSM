# Findings

Status: passed for this physical run.

## Observed Facts

- The raw capture contains 35 parseable `WIFI_DIAG` records with contiguous
  sequence numbers 1 through 35.
- The initial valid connection completed normally with native `associated` and
  `connected` events, a successful callback, and a usable IP.
- One deliberate disconnect request produced its first disconnect callback
  231 ms later.
- IP state was already `0.0.0.0` after that first callback.
- The native `disconnected` event occurred 436 ms after the request. It
  reported reason `8`, message `ASSOC_LEAVE`, and the connected AP MAC address.
- The same disconnect callback fired a second time 756 ms after the request,
  320 ms after the native event. Its recorded callback count was `2`.
- No third disconnect callback occurred during the settle period.
- One explicit reconnect request produced `associated` after 5,202 ms,
  `connected` after 6,723 ms, and a successful callback after 7,099 ms.
- The final observation, 35,392 ms after the reconnect request, remained
  connected with a usable IP.
- No `dhcp_timeout` event occurred.
- No configured SSID or password value appears in any retained result file.

## Event Order In This Run

```text
initial connect succeeds
  -> deliberate disconnect requested
  -> disconnect callback invocation 1
  -> disconnected (reason 8 / ASSOC_LEAVE)
  -> disconnect callback invocation 2
  -> explicit reconnect requested
  -> associated
  -> connected
  -> connect callback succeeds
```

This is one physical run, not yet a general callback-count guarantee.

## Comparison With Unexpected Loss

- Deliberate disconnect reported reason `8` / `ASSOC_LEAVE` and retained the AP
  MAC address.
- Test D's unexpected AP loss reported reason `201` / `NO_AP_FOUND` with an
  all-zero AP MAC address.
- Both paths cleared IP state before or by the native disconnect observation,
  but their reason and AP identity payloads differed in these runs.

## Design Implications To Carry Forward

- The event generator must tolerate multiple invocations of a native operation
  callback. One disconnect request must not become two policy transitions or
  two retry schedules.
- The FSM should correlate an intentional-disconnect operation with the later
  native `disconnected` event. Reason codes provide useful evidence but should
  not be the sole correlation mechanism.
- The disconnect callback can precede the native lifecycle event, so cleanup
  completion and driver lifecycle completion are distinct observations.
- Explicit reconnection worked without additional cleanup after the deliberate
  disconnect had settled.
- Persistent driver status strings remain observations rather than FSM state;
  application-owned state and operation identity must remain authoritative.
