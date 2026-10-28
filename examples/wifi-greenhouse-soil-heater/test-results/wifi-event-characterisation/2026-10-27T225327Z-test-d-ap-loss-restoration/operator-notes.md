# Operator Notes

- `2026-10-27T22:53:27Z`: Run identity allocated.
- Persistent serial identity resolved to `/dev/ttyACM0`; the port was free.
- The mains heater and Shelly device remain disconnected according to the
  current bench configuration.
- The AP begins online. Manual disable and restoration will occur only after
  explicit capture cues.
- No reconnect command will be issued during the evidence window.
- A valid connection and usable IP were established before the first disable
  cue.
- The user later reported that the initial disable attempt had not succeeded.
  A subsequent operation did disable the test AP, but it also disabled this
  host's network connection. The host was moved to a different SSID before
  control of the test resumed.
- Because the successful AP-disable operation did not have a corresponding
  pre-operation marker or reliable completion time, the observed disconnect
  delay cannot be attributed to native loss-detection latency.
- USB serial capture continued locally while host networking was unavailable.
  It recorded `disconnected` with reason `201` / `NO_AP_FOUND` and retained
  contiguous sequence numbers.
- The run was explicitly aborted without restoring the AP under observation.
  Listeners were stopped, disconnect cleanup completed, volatile JavaScript
  state was reset, and credential Storage was retained.
