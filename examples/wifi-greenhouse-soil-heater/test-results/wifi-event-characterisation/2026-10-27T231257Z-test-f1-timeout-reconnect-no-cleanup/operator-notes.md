# Operator Notes

- `2026-10-27T23:12:57Z`: Run identity allocated.
- Persistent serial identity resolved to `/dev/ttyACM0`; the port was free.
- The valid-profile AP remains online; the unavailable profile is selected.
- The mains heater and Shelly device remain disconnected according to the
  current bench configuration.
- No disconnect operation will be issued before the F1 reconnect.
- The 5-second application timeout fired while native work remained active.
- Although the host issued the marker and reconnect interactively, the
  reconnect command did not reach Espruino until after operation 1 emitted
  `NO_AP_FOUND` and its callback completed.
- Operation 2 then ran normally and also completed with `NO_AP_FOUND`.
- The run was marked invalid for the overlap question and retained. The repeat
  will schedule reconnect on the board immediately after timeout.
