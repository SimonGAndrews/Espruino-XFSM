# Findings

Status: invalid; retained as diagnostic evidence and not used to conclude F2.

## Observed Facts

- The 5-second application timeout left operation 1's native work running.
- `disconnect()` issued 748 ms after that timeout terminated the native work.
  Its first callback preceded the native disconnect event, and its callback
  was delivered twice.
- Operation 1 then received a connect callback with `Unknown reason`.
- A second unavailable-profile connect was accepted after the cleanup; the
  console did not report the `ESP_ERR_WIFI_STATE` seen in F1.
- The second native attempt reached `NO_AP_FOUND`, but the diagnostic's connect
  callback raised `ReferenceError: "operation" is not defined` after cancelling
  its timer. The preceding native event also supplied an unexpected numeric
  details value.

## Disposition

The reconnect was initiated by a function nested inside the board-scheduled
cleanup timer. The lost callback binding and malformed event details make the
later trace unreliable. No Wi-Fi policy conclusion is drawn from this run.
F2 is repeated with separate top-level host commands while retaining the same
canonical diagnostic source.
