# Findings

Status: invalid timing run; not accepted as Test F1.

The application timeout occurred as intended, but the host-issued reconnect
did not reach the board until after the first native `NO_AP_FOUND` event and
callback. The resulting second attempt proves that reconnect works without an
explicit application `disconnect()` after a terminal native failure, but it
does not answer whether a new attempt can overlap native work that survived the
application timeout.

This run is retained and excluded from Test F1 conclusions. A board-scheduled
repeat removes host terminal latency from the critical interval.
