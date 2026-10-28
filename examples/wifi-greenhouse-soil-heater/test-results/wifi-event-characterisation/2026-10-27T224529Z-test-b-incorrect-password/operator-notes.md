# Operator Notes

- `2026-10-27T22:45:29Z`: Run identity allocated.
- Persistent serial identity resolved to `/dev/ttyACM0`; the port was free.
- The mains heater and Shelly device remain disconnected according to the
  current bench configuration.
- Only one incorrect-password connection request will be issued.
- No event ordering, retry count, or callback result is assumed before capture.
- The on-device configuration and recorded firmware identity were verified
  before loading the diagnostic.
- The application timeout fired before the native failure notification. The
  only native event was `disconnected`, with reason `15` and message
  `4WAY_HANDSHAKE_TIMEOUT`; the connect callback subsequently reported the
  same message as its error.
- No further native event or callback was observed through the capture-end
  observation more than 60 seconds after the request.
- After the evidence boundary, listeners were removed and an explicit
  disconnect callback completed. The driver continued to expose status
  `4WAY_HANDSHAKE_TIMEOUT` with IP `0.0.0.0`; volatile JavaScript state was
  reset and credential Storage was retained. This cleanup observation is not
  part of the Test B event trace.
