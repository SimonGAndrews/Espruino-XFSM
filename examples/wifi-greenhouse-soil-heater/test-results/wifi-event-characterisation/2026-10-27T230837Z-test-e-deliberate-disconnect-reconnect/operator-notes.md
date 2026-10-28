# Operator Notes

- `2026-10-27T23:08:37Z`: Run identity allocated.
- Persistent serial identity resolved to `/dev/ttyACM0`; the port was free.
- The user confirmed the valid-profile AP is online.
- The mains heater and Shelly device remain disconnected according to the
  current bench configuration.
- Exactly one deliberate disconnect and one explicit reconnect will be issued.
- The initial valid connection completed with a usable IP.
- The deliberate disconnect callback fired twice for the single request: once
  before and once after the native `disconnected` event.
- The native deliberate-disconnect event reported reason `8`, message
  `ASSOC_LEAVE`, and the connected AP MAC address. IP state had cleared before
  the native event was observed.
- No further disconnect callback occurred during the five-second settle period.
- One explicit `reconnect()` produced a normal `associated`, `connected`, and
  successful connect-callback sequence. It remained connected through the
  final observation 35,392 ms after the reconnect request.
- After the evidence boundary, listeners were removed, an explicit cleanup
  disconnect callback completed, volatile JavaScript state was reset, and
  credential Storage was retained.
