# Operator Notes

- F1 established that an overlapping connect is rejected by the native driver.
- F2 schedules explicit disconnect after the timeout, waits two seconds, and
  only then calls `reconnect()`.
- After the unavailable retry completes, a valid-profile connection will prove
  recovery using the same diagnostic session.
- The mains heater and Shelly device remain disconnected.
- Operation 1 timed out, then explicit disconnect terminated its native work.
  The native disconnect event used reason 36 (`Unknown reason`), operation 1's
  connect callback reported the same error, and the disconnect callback fired
  twice.
- Operation 2 was accepted by the native layer after the cleanup; no
  `ESP_ERR_WIFI_STATE` was printed.
- When operation 2 later reached `NO_AP_FOUND`, its connect callback cancelled
  the timer and then raised `ReferenceError: "operation" is not defined` while
  constructing the trace record. The native event's details value was also an
  unexpected number.
- Because operation 2 had been launched inside a nested board timer, this run
  is retained as invalid diagnostic evidence. The repeat issues each phase as
  a separate top-level host command after observing the preceding milestone.
