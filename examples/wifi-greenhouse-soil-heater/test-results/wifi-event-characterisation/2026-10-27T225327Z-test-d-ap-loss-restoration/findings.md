# Findings

Status: invalid environmental run; not accepted as Test D.

## Retained Facts

- The raw capture contains 20 parseable `WIFI_DIAG` records with contiguous
  sequence numbers 1 through 20.
- A valid connection was established before the operator disable sequence.
- The first operator completion marker did not correspond to a successful AP
  disable; the device still reported connected with its assigned IP.
- A later unmarked AP operation caused the test AP and the host network path to
  become unavailable.
- The serial capture subsequently recorded `disconnected` with reason `201`,
  message `NO_AP_FOUND`, an all-zero AP MAC address, and IP `0.0.0.0`.
- No configured SSID or password value appears in any retained result file.

## Why The Run Is Invalid

The actual successful AP-disable time is unknown. The interval between the
earlier completion marker and the disconnect event therefore does not measure
native loss-detection latency. The AP was also not restored under capture, so
automatic reconnection could not be assessed.

No production event-ordering or retry-policy conclusion may be drawn from this
run. The retained trace is useful only as evidence of the environmental issue
and the eventual native disconnect payload.
