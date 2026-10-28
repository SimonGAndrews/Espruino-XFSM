# Operator Notes

- `2026-10-27T22:49:29Z`: Run identity allocated.
- Persistent serial identity resolved to `/dev/ttyACM0`; the port was free.
- The valid-profile AP remains online; the distinct unavailable profile is
  used for this run.
- The mains heater and Shelly device remain disconnected according to the
  current bench configuration.
- Only one unavailable-network connection request will be issued.
- No event ordering, retry count, or callback result is assumed before capture.
- The on-device configuration and recorded firmware identity were verified
  before loading the diagnostic.
- The previous run's terminal driver status remained visible at startup even
  though IP state was empty. The new connection attempt subsequently replaced
  it with `NO_AP_FOUND`.
- The only native event was `disconnected`, with reason `201`, message
  `NO_AP_FOUND`, and an all-zero AP MAC address. The connect callback reported
  the same failure after cancelling the application timeout.
- No further native event or callback was observed through the capture-end
  observation more than 60 seconds after the request.
- After the evidence boundary, listeners were removed and an explicit
  disconnect callback completed. The driver continued to expose status
  `NO_AP_FOUND` with IP `0.0.0.0`; volatile JavaScript state was reset and
  credential Storage was retained. This cleanup observation is not part of
  the Test C event trace.
