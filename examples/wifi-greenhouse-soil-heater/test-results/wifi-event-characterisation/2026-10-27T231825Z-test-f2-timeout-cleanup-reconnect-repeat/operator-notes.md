# Operator Notes

- The preceding F2 run was retained as invalid after a reconnect launched from
  a nested board timer lost callback-local state.
- This repeat sends each phase as a separate top-level host command after the
  required milestone is visible in the trace.
- SHED and the valid-profile network are online.
- The mains heater and Shelly device remain disconnected.
- Operation 1's 5-second application timeout occurred 5,318 ms after its
  request. Host polling meant cleanup was requested 7,994 ms later, while the
  native attempt was still active.
- The first disconnect callback arrived 221 ms after cleanup was requested,
  the native disconnect event followed at 433 ms with reason 36 (`Unknown
  reason`), and operation 1's connect callback followed at 757 ms with the same
  error. A second disconnect callback arrived at 1,074 ms.
- Operation 2 was requested 4,559 ms after the last cleanup callback, using the
  online valid profile. No overlap error or JavaScript exception occurred.
- Operation 2 emitted `associated` 5,212 ms after its request, `connected`
  with an IP address at 6,779 ms, and a successful connect callback at 7,096
  ms.
- After the evidence boundary, listeners were removed, Wi-Fi was disconnected,
  and volatile JavaScript state was reset. The native cleanup callback again
  fired twice.
