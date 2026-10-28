# Operator Notes

- `2026-10-27T22:29:56Z`: Run identity allocated.
- Persistent serial link resolved to `/dev/ttyACM0` and was free.
- The mains heater and Shelly device remained disconnected throughout.
- No Wi-Fi connection operation is planned for this capture smoke test.
- The first capture attempt failed before reaching the board because the
  installed Espruino CLI rejected the persistent serial symlink. Its host-side
  output and timing files were retained as `capture-attempt-1-*`.
- Retrying through resolved device `/dev/ttyACM0` exposed that the original
  on-device configuration name exceeded Espruino's Storage filename limit.
  The diagnostic and procedure were corrected to use
  `wifi-event-config.json` on device; no credential data was retained while
  diagnosing the failure.
- The configuration was successfully uploaded through `/dev/ttyACM0` from an
  interactive PTY and independently verified present without reading its
  value into the result.
- A second captured attempt showed that this Espruino CLI installation can
  report `Upload Complete` without leaving the diagnostic running. The
  resulting `undefined` API probe was retained as failed-attempt evidence.
- The final attempt used the repository's XON/XOFF-aware `open_serial()` and
  paced source uploader. It produced five contiguous `WIFI_DIAG` records and
  executed the `serial_capture_smoke` observation successfully.
- No `connect_requested` record occurred. The mains heater and Shelly remained
  disconnected.
- After evidence validation, the diagnostic listeners were stopped and
  volatile JavaScript state was reset. The credential Storage file was left
  intact for Phase 1.
