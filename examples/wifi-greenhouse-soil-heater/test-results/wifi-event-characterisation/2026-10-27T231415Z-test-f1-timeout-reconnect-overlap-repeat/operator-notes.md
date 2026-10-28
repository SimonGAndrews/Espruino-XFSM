# Operator Notes

- The earlier F1 attempt was retained as invalid because host input reached the
  board after native operation 1 had already completed.
- This repeat schedules reconnect on the board 5,500 ms after the initial
  request so the intended native-work overlap is reproducible.
- No explicit disconnect is issued before operation 2.
- The mains heater and Shelly device remain disconnected.
- Operation 1's 5-second application timeout fired while native work continued.
- Operation 2 was requested 753 ms after that timeout and before operation 1's
  native terminal event.
- ESP-IDF reported `sta is connecting, cannot set config`; Espruino printed
  `ESP_ERR_WIFI_STATE` but did not throw to the JavaScript caller.
- The diagnostic therefore armed operation 2's timer even though the native
  request was rejected.
- Operation 1 later emitted `NO_AP_FOUND`. Neither operation's connect callback
  was observed. Operation 2's application timer also expired.
- Cleanup after the evidence boundary completed and reset volatile state.
