# ESP32-C3 Wi-Fi Event Characterisation

Status: initial physical experiment complete; Tests A–F each have one accepted
physical result. Test F comprises accepted no-cleanup and cleanup phases.
Repeatability review remains outstanding, and invalid attempts are retained as
diagnostic evidence.

Requirements: `REQ-TEST-001`, `REQ-TEST-002`, and `ASM-WIFI-001` in
[`requirements.md`](requirements.md). Plan: Phase 1 in
[`development-plan.md`](development-plan.md).

This experiment observes the native ESP32-C3 Espruino Wi-Fi interface before
its notifications are translated into XFSM events. It deliberately contains no
state machine and assigns no connection-policy meaning to event ordering.

The diagnostic does not call `wifi.save()` and does not enable automatic Wi-Fi
startup. It reads experiment profiles from its explicit Storage file and starts
a connection only through a recorded diagnostic operation.

The diagnostic program is
[`wifi-event-characterisation.js`](wifi-event-characterisation.js). It emits
newline-delimited records prefixed with `WIFI_DIAG ` and provides interactive
operations through `global.WifiEventCharacterisation`.

Use the repository's XON/XOFF-aware `tools/repl/run_test.py` serial helpers for
source upload and capture. A physical smoke run established that the installed
Espruino CLI can report a completed JavaScript upload without leaving this
diagnostic running. The CLI remains suitable for the credential Storage upload
when invoked from an interactive PTY, but is not the selected diagnostic source
transport.

## Safety And Credentials

Run this experiment on an isolated development setup. The current workbench
has neither the mains heater nor the Shelly device connected. Reconfirm and
record both conditions before every run. The diagnostic does not control the
heater and must not be tested with either device connected.

Create a local configuration from the committed template:

```bash
cp examples/wifi-greenhouse-soil-heater/\
wifi-event-characterisation.config.example.json \
  examples/wifi-greenhouse-soil-heater/\
wifi-event-characterisation.config.local.json
chmod 600 examples/wifi-greenhouse-soil-heater/\
wifi-event-characterisation.config.local.json
```

Edit the local file, then upload it to Espruino Storage as
`wifi-event-config.json`. The shorter on-device name respects Espruino's
Storage filename limit; the ignored host file retains its descriptive local
name. Upload it with:

```bash
espruino -p /dev/ttyACM0 --storage \
  wifi-event-config.json:examples/wifi-greenhouse-soil-heater/\
wifi-event-characterisation.config.local.json
```

Resolve `/dev/ttyACM0` from the persistent `/dev/serial/by-id/` link before
each run. The installed Espruino CLI may reject the symlink even when the OS
can open it. Upload the diagnostic program separately and execute it on the
ESP32-C3.

The program itself never prints supplied passwords or SSIDs. It recursively
redacts fields whose names contain `pass` or `ssid`. In particular, it
sanitises `wifi.getDetails()`, which may include the configured password. Raw
interpreter, debug-firmware, or transport logs must still be reviewed before
retention.

## Trace Contents

Each record contains a format identifier, monotonically increasing sequence,
elapsed milliseconds, `Date.now()`, record kind, name, and optional details.
The serial console may place a prompt or ANSI control bytes immediately before
the marker, so evidence parsers must locate `WIFI_DIAG ` within each line
rather than require it at column zero. The diagnostic records:

- all `associated`, `connected`, `disconnected`, and `dhcp_timeout` events;
- event detail objects supplied by Espruino;
- `wifi.connect(...)` and `wifi.disconnect()` callback invocations;
- `wifi.getDetails()` and `wifi.getIP()` observations before and after useful
  operations and notifications;
- application timeout markers; and
- explicit connect, disconnect, reconnect, and observation requests.

An application timeout is observational. It records that the native connection
attempt remains active and does not call `wifi.disconnect()` automatically.

## Interactive Operations

After the program has loaded, use:

```javascript
WifiEventCharacterisation.connect("valid");
WifiEventCharacterisation.connect("incorrectPassword");
WifiEventCharacterisation.connect("unavailable");
WifiEventCharacterisation.disconnect();
WifiEventCharacterisation.reconnect();
WifiEventCharacterisation.observe("operator_marker");
WifiEventCharacterisation.cancelConnectTimeout("operator_cancelled");
WifiEventCharacterisation.reloadConfig();
WifiEventCharacterisation.stop();
```

`connect(profile, timeoutMs)` accepts an optional timeout override. Passing
zero disables the application timeout for that attempt. `reconnect()` uses the
last selected profile unless another profile name is supplied. `stop()` removes
the diagnostic listeners but deliberately leaves the native Wi-Fi state
unchanged.

## Scenarios

Preserve the complete serial trace for every scenario under
[`test-results/wifi-event-characterisation/`](test-results/README.md). Create
one immutable run directory per attempt using the naming and contents defined
by the test-results README. Begin from a reset or record an explicit
observation and disconnect boundary so the initial state is unambiguous.

### Test A: Normal Connection

Use the `valid` profile while its access point is available:

```javascript
WifiEventCharacterisation.connect("valid");
```

Record association, IP acquisition, native events, callback results, and
status/IP observations.

### Test B: Incorrect Password

Ensure `incorrectPassword` names the available test AP but contains a known
incorrect password:

```javascript
WifiEventCharacterisation.disconnect();
WifiEventCharacterisation.connect("incorrectPassword");
```

Record callbacks, disconnect details and reasons, native retries, and the
application timeout. Do not infer that a missing event means success.

### Test C: Unavailable SSID

Ensure `unavailable` names an SSID that is absent from the test location:

```javascript
WifiEventCharacterisation.disconnect();
WifiEventCharacterisation.connect("unavailable");
```

Record the native event sequence and whether retries occur without another
application call.

### Test D: AP Disappears After Connection

Connect with `valid`, then power off or disable only the test access point.
Issue no Wi-Fi operation while observing the loss. Restore the access point and
continue recording without calling `reconnect()` unless the planned test run
explicitly introduces that second phase.

Immediately before each manual AP operation, emit an operator marker such as:

```javascript
WifiEventCharacterisation.observe("operator_about_to_disable_ap");
WifiEventCharacterisation.observe("operator_about_to_restore_ap");
```

Record the host or operator time at which each physical action completes.

Record disconnect details and whether the native subsystem reconnects after
the AP returns.

### Test E: Deliberate Disconnect And Reconnect

After a successful `valid` connection, run:

```javascript
WifiEventCharacterisation.disconnect();
```

Wait for the resulting callbacks and events, then run:

```javascript
WifiEventCharacterisation.reconnect();
```

Compare the deliberate-disconnect trace with Test D without assuming they
will use the same notification or reason.

### Test F: Application Timeout And Recovery

Start an attempt that cannot complete before a deliberately short timeout:

```javascript
WifiEventCharacterisation.connect("unavailable", 5000);
```

After `application_connect_timeout`, observe the continuing native state. Run
one recorded phase that calls `reconnect()` without cleanup, and a separate
cleanup phase that calls `disconnect()` before `reconnect()`. This establishes
whether a new connection attempt requires explicit cleanup.

## Evidence To Record

For each retained trace, record:

- scenario and exact operator steps;
- Espruino-XFSM and Espruino revisions;
- board and firmware profile;
- diagnostic program revision;
- access-point identity or test role without its password;
- application timeout values and operator wait periods;
- whether the AP was available, disabled, restored, or intentionally absent;
- the complete prefixed trace; and
- interruptions, unexpected console output, or reasoned deviations.

Store the complete run inside this example's `test-results/` directory. Review
the raw capture for credentials before adding it to Git, and never move the
only copy of the evidence into a repository-level or external report folder.

Do not define the production event mapping, retry policy, or expected ordering
until the physical traces have been reviewed.
