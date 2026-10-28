# Operator Notes

- `2026-10-27T23:03:09Z`: Repeat run identity allocated.
- Persistent serial identity resolved to `/dev/ttyACM0`; the port was free.
- The host control path has been moved away from the test AP.
- The mains heater and Shelly device remain disconnected according to the
  current bench configuration.
- No reconnect command will be issued during the evidence window.
- A valid connection and usable IP were established before the disable cue.
- At the operator disable-complete marker, `getDetails().status` still reported
  `connected`, but the IP had already changed to `0.0.0.0`.
- The native `disconnected` event followed 7,412 ms later with reason `201`,
  message `NO_AP_FOUND`, and an all-zero AP MAC address.
- The user restored the AP after the explicit pre-restore cue. No application
  reconnect call was issued.
- No further native event or callback occurred during the 105,260 ms between
  the restore-complete marker and final observation. The driver remained
  `NO_AP_FOUND` with IP `0.0.0.0`.
- After the evidence boundary, listeners were removed, an explicit disconnect
  callback completed, volatile JavaScript state was reset, and credential
  Storage was retained.
