# Findings

Status: passed for this physical run.

## Observed Facts

- Operation 1's application timeout fired 5,318 ms after its unavailable-
  profile request and did not stop native connection work.
- Explicit `disconnect()` was requested while that work remained active. Its
  first callback arrived after 221 ms; the native `disconnected` event arrived
  after 433 ms with reason 36 / `Unknown reason`; operation 1's connect
  callback arrived after 757 ms with the same error; and the disconnect
  callback was delivered a second time after 1,074 ms.
- A valid-profile connection requested after the complete cleanup sequence was
  accepted without the `ESP_ERR_WIFI_STATE` observed in F1.
- The recovery attempt emitted `associated`, then `connected` with an assigned
  IP, then a successful connect callback. The callback cancelled its
  application timer.
- No `dhcp_timeout`, unexpected native retry, interpreter exception, or
  sequence gap was observed.

## Design Implications

- An application timeout is not native cancellation. The Wi-Fi actor must
  explicitly clean up the timed-out attempt before starting another one.
- The first `wifi.disconnect()` callback is not a sufficient cleanup-complete
  boundary on this firmware. Native disconnect and the original connect
  callback can arrive later, and the disconnect callback can fire twice.
- Intentional cleanup must be represented by application state or operation
  intent; native reason 36 is reported only as `Unknown reason` and does not
  itself identify the policy cause.
- A retry must remain inhibited until the cleanup lifecycle has been
  reconciled and settled. The subsequent valid connection demonstrates that
  explicit cleanup restores the ability to connect.
- F1 and F2 together support `REQ-ASYNC-003`: overlapping attempts must be
  prevented, and timed-out attempts require an explicit cleanup phase.
