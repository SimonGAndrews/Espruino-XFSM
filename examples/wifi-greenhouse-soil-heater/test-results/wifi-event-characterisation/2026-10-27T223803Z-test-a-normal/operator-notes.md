# Operator Notes

- `2026-10-27T22:38:03Z`: Run identity allocated.
- Persistent serial identity resolved to `/dev/ttyACM0`; the port was free.
- The mains heater and Shelly device remain disconnected according to the
  current bench configuration.
- No event ordering is assumed before capture.
- The on-device configuration and recorded firmware identity were verified
  before loading the diagnostic.
- The valid-profile connection was requested once. The complete captured
  native event order was `associated`, then `connected`; the callback then
  reported success.
- The capture-end observation occurred more than 35 seconds after the request
  and still reported a connected state with a configured IP address.
- After the evidence boundary, listeners were removed and an explicit
  disconnect was requested. The post-cleanup driver status remained
  `ASSOC_LEAVE` while the IP address was `0.0.0.0`; volatile JavaScript state
  was reset and credential Storage was retained. This cleanup observation is
  not part of the Test A event trace.
