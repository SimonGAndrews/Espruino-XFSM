# Wi-Fi Greenhouse Soil Heater Requirements

Status: initial structured baseline; further requirements are expected.

This document consolidates the requirements captured so far. `REQ-*` entries
are accepted requirements. `ASM-*` entries are assumptions that require
evidence. `PROP-*` entries are proposals awaiting acceptance. `OPEN-*` entries
are unresolved decisions.

## 1. Purpose And Scope

### System outcome

- `REQ-SYS-001`: The application shall control a simple greenhouse soil-heating
  system.
- `REQ-SYS-002`: The end-state application shall manage Wi-Fi connectivity,
  soil-temperature sensing, heater control, status reporting, configuration,
  and recovery from relevant failures.
- `REQ-SYS-003`: Intermediate phases may implement only a subset of the
  end-state system, but each artifact shall state its implemented and omitted
  capabilities.

### XFSM exercise outcome

- `REQ-XFSM-001`: The example shall exercise meaningful hierarchical states.
- `REQ-XFSM-002`: Shared event handling shall demonstrate parent event fallback
  rather than duplicating equivalent handlers across child states.
- `REQ-XFSM-003`: State-owned effects and cleanup shall demonstrate entry and
  exit actions.
- `REQ-XFSM-004`: Native Espruino services and timers shall deliver later
  occurrences as events to an XFSM actor.
- `REQ-XFSM-005`: The example shall demonstrate deliberate actor creation,
  startup, subscription, snapshot observation, stop, and fault handling.
- `REQ-XFSM-006`: The application shall integrate native Espruino services at
  explicit action and event-ingress boundaries.
- `REQ-XFSM-007`: The final statechart and tests shall identify where each
  required XFSM behaviour is exercised; incidental coverage is insufficient.

## 2. Hardware And Network

- `REQ-HW-001`: The prototype controller shall be a Seeed Studio XIAO ESP32C3
  running an XFSM-enabled Espruino build.
- `REQ-HW-002`: Soil temperature shall be measured by a waterproof DS18B20
  digital 1-Wire sensor.
- `REQ-HW-003`: Heat shall be provided by a mains-powered soil-heating cable.
- `REQ-HW-004`: The heating cable shall be switched by a Shelly 1 Mini 8A smart
  switch.
- `REQ-HW-005`: The ESP32-C3 shall command the Shelly over Wi-Fi and shall not
  switch the mains heater directly from a GPIO pin.
- `REQ-NET-001`: The controller and Shelly shall use the standalone Wi-Fi
  network whose SSID is `SHED`.

### Observed prototype firmware baseline

On 2026-10-27, a read-only REPL inspection of the attached XIAO ESP32C3
reported:

| Item | Observed value |
| --- | --- |
| Espruino board profile | `ESP32C3_IDF5` |
| Espruino version | `2v29.535` |
| Espruino integration revision | `215fe4e16cf134365c2db6a13cc18494293fc8e0` |
| Exported XFSM source revision | `563a3a0a36fc83aab84515481f516dc5738cca9b` |
| Console | Native USB |
| Public XFSM surface | `createMachine`, `createActor`, and `assign` present |
| Private XFSM hooks | `_measure` and `_test` absent |
| Wi-Fi surface | `connect`, events, `getDetails`, and `getIP` present |

This is the qualified ESP32-C3 production image recorded by the repository's
2026-10-26 qualification. The later integration head changes only two
qualification trace fixtures; it does not change the native XFSM engine in the
flashed image. Runtime identity does not independently prove the retained
firmware artifact's SHA-256 hash.

## 3. Architectural Boundaries

### Layer A: action functions

- `REQ-ARCH-001`: Ordinary Espruino JavaScript action functions shall perform
  hardware or service effects.
- `REQ-ARCH-002`: Actions shall not independently select connection policy,
  choose application states, or implement hidden retry loops.
- `REQ-ARCH-003`: An action shall not synchronously call `actor.send(...)` on
  the same actor whose operation invoked it. Results that could re-enter that
  actor shall be delivered later through the Espruino event loop.

Expected action boundaries include:

```javascript
function connectWifi() {}
function disconnectWifi() {}
function resetWifi() {}
function armConnectTimeout() {}
function armRetryTimer() {}
function startProvisioningAP() {}
function stopProvisioningAP() {}
function saveCredentials() {}
```

### Layer B: event generators

- `REQ-ARCH-004`: Native services, HTTP handlers, sensor callbacks, and timers
  shall translate significant occurrences into semantic events and deliver
  them to the applicable actor.
- `REQ-ARCH-005`: Event generators shall contain only the logic required to
  interpret a notification and construct and deliver its event. They shall not
  implement a second state machine or independent retry policy.

Initial semantic Wi-Fi events include:

```text
WIFI_ASSOCIATED
WIFI_CONNECTED
WIFI_DISCONNECTED
WIFI_DHCP_TIMEOUT
CONNECT_TIMEOUT
RETRY_TIMEOUT
CREDENTIALS_AVAILABLE
CREDENTIALS_MISSING
CREDENTIALS_SUBMITTED
```

### Layer C: XFSM machine

- `REQ-ARCH-006`: The XFSM machine shall be the sole authority for connection
  lifecycle states, valid transitions, retry and recovery policy, state entry
  and exit effects, and responses to external events.
- `REQ-ARCH-007`: State-dependent policy shall remain visible in the machine
  definition. Native service state may supply facts but shall not become an
  implicit policy owner.
- `REQ-ARCH-008`: The architecture shall respect Profile 2's single-active-
  branch model and absence of parallel states, delayed transitions, invoked
  services, and spawned actors.

## 4. Wi-Fi Manager

- `REQ-WIFI-001`: The manager shall establish an ESP32-C3 station connection to
  configured credentials.
- `REQ-WIFI-002`: The manager shall monitor connection state using native
  Espruino Wi-Fi events.
- `REQ-WIFI-003`: The manager shall recover automatically from initial
  connection failures and later disconnections according to an explicit
  application policy.
- `REQ-WIFI-004`: Connection attempts shall have an application-controlled
  timeout.
- `REQ-WIFI-005`: Retries shall use a controlled policy and shall not run as an
  unbounded immediate loop.
- `REQ-WIFI-006`: The manager shall offer provisioning when credentials are
  absent or cannot establish a usable connection.
- `REQ-WIFI-007`: Connection status shall be available to the heater controller
  and other application components through a defined contract.
- `REQ-WIFI-008`: The ESP32-C3 shall host an HTTP management interface.

### Initial native event mapping

`ASM-WIFI-001`: The initial design assumes this native mapping:

| Native `Wifi.on(...)` event | Semantic XFSM event |
| --- | --- |
| `associated` | `WIFI_ASSOCIATED` |
| `connected` | `WIFI_CONNECTED` |
| `disconnected` | `WIFI_DISCONNECTED` |
| `dhcp_timeout` | `WIFI_DHCP_TIMEOUT` |

This mapping, its payloads, and its ordering remain assumptions until the
physical experiment is complete. The experiment is defined in
[`wifi-event-characterisation.md`](wifi-event-characterisation.md).

## 5. Asynchronous Operations And Timers

- `REQ-ASYNC-001`: The design shall allow for native Wi-Fi work continuing
  after the initiating XFSM state has exited.
- `REQ-ASYNC-002`: Every application timer shall have an explicit owning state
  or operation and shall be cancelled when that owner exits.
- `REQ-ASYNC-003`: The application shall prevent overlapping connection
  attempts unless a later reviewed design explicitly defines them.
- `REQ-ASYNC-004`: Stale application callbacks and timer events shall be
  rejected without changing current connection policy.
- `REQ-ASYNC-005`: Application-controlled retry shall account for observed
  native-driver retry so the two policies do not compete unpredictably.
- `REQ-ASYNC-006`: An intentional disconnect or reset shall be distinguishable
  in application policy from an unexpected connection loss, even if native
  notifications are similar.
- `REQ-ASYNC-007`: Late connection callbacks and `WIFI_CONNECTED` events shall
  be reconciled with current actor state rather than accepted unconditionally.
- `REQ-ASYNC-008`: Unexpected or ambiguous lifecycle events shall be reconciled
  against observed driver facts, including `wifi.getDetails()` and
  `wifi.getIP()` where appropriate.
- `REQ-ASYNC-009`: Calling `actor.send(...)` from a later native callback or
  timer is asynchronous event delivery, but each call remains a synchronous
  XFSM run-to-completion operation.

`PROP-ASYNC-001`: A monotonically increasing connection-attempt generation or
equivalent token should identify application callbacks and timers. Such a token
must not be treated as the identity of a native Wi-Fi lifecycle event unless
the native API supplies that association.

Known hazards that tests must cover are:

- late `WIFI_CONNECTED` after an application timeout;
- an intentional reset producing a disconnect notification;
- a retry timer firing after success;
- overlapping connection attempts;
- native auto-retry interacting with application retry; and
- a connection callback arriving after its initiating state has exited.

## 6. Credentials And Persistence

- `REQ-CRED-001`: SSID and password shall be application configuration stored
  explicitly using Espruino `Storage`.
- `REQ-CRED-002`: The application shall not use `wifi.save()` to persist
  credentials or enable automatic ESP32 Wi-Fi startup.
- `REQ-CRED-003`: The Wi-Fi FSM shall decide when to connect after it has been
  initialized.
- `REQ-CRED-004`: Each boot shall reconstruct runtime state from stored
  configuration and observed service events; persisted configuration shall not
  be treated as persisted actor state.
- `REQ-CRED-005`: Passwords and complete stored credential records shall not be
  committed to the repository or written to retained logs, diagnostics,
  snapshots, or HTTP responses. The connected SSID may be shown by the normal
  management interface as required by `REQ-HTTP-002`.
- `REQ-CRED-006`: Local credential files shall follow the repository's ignored
  `credentials.local.json` convention and shall be owner-readable only on the
  current test host.
- `PROP-CRED-001`: Credential updates should be validated and persisted through
  an explicit application transaction before they are used as current
  configuration.

The event-characterisation diagnostic uses its own documented local Storage
file and does not define the production credential schema.

## 7. HTTP Management Interface

### Normal operation

- `REQ-HTTP-001`: The normal interface shall display the current Wi-Fi FSM
  state.
- `REQ-HTTP-002`: The normal interface shall display the connected SSID and IP
  address.
- `REQ-HTTP-003`: The normal interface shall display connection uptime, last
  disconnect reason, retry count, and connection status.
- `REQ-HTTP-004`: A later phase shall add heater-controller status and
  temperature and schedule configuration.

### Provisioning operation

- `REQ-HTTP-005`: The provisioning interface shall display available networks
  and allow SSID selection and password entry.
- `REQ-HTTP-006`: The provisioning interface shall show connection progress
  and success or failure feedback.

### Actor boundary

- `REQ-HTTP-007`: HTTP handlers shall observe actor state through stable
  snapshots and shall not mutate snapshot or context objects.
- `REQ-HTTP-008`: HTTP handlers shall request behaviour by sending defined
  events to the Wi-Fi actor.
- `REQ-HTTP-009`: HTTP handlers shall not call `wifi.connect()` independently
  or implement connection policy.
- `REQ-HTTP-010`: Passwords shall never be echoed in pages or responses.

## 8. Heater And Temperature Control

- `REQ-HEAT-001`: The application shall read the DS18B20 and make the current
  soil temperature available to heater policy and status reporting.
- `REQ-HEAT-002`: The application shall command the Shelly relay over Wi-Fi
  according to explicit heater policy.
- `PROP-HEAT-001`: A missing, stale, or invalid temperature should not result
  in an unbounded request for heat.
- `REQ-HEAT-004`: The eventual HTTP interface shall expose heater status and
  allow the accepted temperature and schedule configuration.

The detailed heating policy is not yet defined.

## 9. Safety Baseline Awaiting Acceptance

These are proposals, not yet accepted requirements:

- `PROP-SAFE-001`: Configure the Shelly, where supported, so its relay defaults
  off after power-up or restart.
- `PROP-SAFE-002`: Begin controller operation with heat requested off, then
  query and reconcile actual Shelly state when it becomes reachable.
- `PROP-SAFE-003`: Default to heat requested off when no valid current
  temperature is available.
- `PROP-SAFE-004`: Provide protection independent of the ESP32-C3 Wi-Fi path
  for any temperature or continuous-run limit that must remain guaranteed
  during controller, network, or Shelly service failure.
- `PROP-SAFE-005`: Request heater off when the controlling actor stops or
  faults, while recognising that an offline Shelly cannot receive the request.
- `PROP-SAFE-006`: Do not present software control as a replacement for
  appropriate electrical and thermal protection.

The stated architecture has no direct heater-disconnect path from the
ESP32-C3. If the Shelly is on when the controller or network becomes
unavailable, the controller cannot guarantee an immediate off command. A
Shelly-local timeout, independent thermal cut-out, or other protection must be
defined before energised heater testing.

## 10. Verification Requirements

- `REQ-TEST-001`: Tests shall produce reproducible traces with the XFSM and
  Espruino revisions, target, firmware profile, procedure, inputs, and relevant
  limitations recorded.
- `REQ-TEST-002`: The physical Wi-Fi event-characterisation Tests A–F shall be
  completed and reviewed before production event ordering or retry policy is
  finalised.
- `REQ-TEST-003`: Tests shall cover boot with valid, invalid, and missing
  credentials and with the configured AP available and unavailable.
- `REQ-TEST-004`: Tests shall cover connection loss and recovery, application
  timeouts, stale callbacks, stale timers, overlapping-attempt prevention, and
  native/application retry interaction.
- `REQ-TEST-005`: Tests shall demonstrate cancellation of each state-owned
  timer on state exit.
- `REQ-TEST-006`: Tests shall confirm that `wifi.save()` and automatic Wi-Fi
  startup are not used.
- `REQ-TEST-007`: Tests shall exercise hierarchical transitions, parent
  fallback, entry/exit ordering, actor lifecycle, snapshots, subscriptions,
  and fault behaviour.
- `REQ-TEST-008`: Tests shall cover DS18B20 absence and invalid or stale
  readings before heater integration is accepted.
- `REQ-TEST-009`: Tests shall cover heater safe-state behaviour during reset,
  stop, application fault, network loss, Shelly failure, and power return.
- `REQ-TEST-010`: Physical heater tests shall identify the board, sensor,
  Shelly, switching load, protection, connections, and safe test setup.
- `REQ-TEST-011`: Every test result shall be retained under this example's
  `test-results/` directory in an immutable per-run directory containing raw
  evidence, metadata, operator notes, and reviewed findings. Credentials and
  authentication tokens shall not be stored with the results.
- `REQ-TEST-012`: Wi-Fi event-characterisation runs shall use
  `wifi-event-characterisation.js` as their single canonical diagnostic source.
  Each run shall record its path and SHA-256 rather than duplicating the
  executable source in the result directory.

The repository's standard qualification suites continue to establish XFSM
engine conformance. These tests establish this application's behaviour.

## 11. Open Decisions

### Needed before the Wi-Fi actor is designed

- `OPEN-WIFI-001`: Repeatability review and consolidated interpretation of the
  initial accepted physical results for event-characterisation Tests A–F.
- `OPEN-WIFI-002`: Acceptance or refinement of the proposed initial statechart
  and public connection-status contract in
  [`wifi-statechart.md`](wifi-statechart.md).
- `OPEN-WIFI-003`: Acceptance or revision of the provisional timeout, cleanup
  quiet interval, retry limit, delay/backoff schedule, and criteria for
  entering provisioning proposed in `wifi-statechart.md`.
- `OPEN-WIFI-004`: Production Storage filename, credential schema, validation,
  and replacement transaction.
- `OPEN-WIFI-005`: Final event payloads and reconciliation rules after
  repeatability review; the initial event and guard contracts are proposed in
  `wifi-statechart.md`.

### Needed before provisioning and HTTP management

- `OPEN-HTTP-001`: How provisioning is reached before station connectivity,
  including AP/STA mode behaviour on the selected ESP32-C3 firmware.
- `OPEN-HTTP-002`: Routes, request/response formats, input limits,
  authentication, and protection against unintended credential exposure.
- `OPEN-HTTP-003`: HTTP-to-actor event payloads and snapshot-to-view mapping.
- `OPEN-HTTP-004`: Client update mechanism for asynchronous connection
  progress.
- `OPEN-HTTP-005`: Lifecycle and network interface of normal and provisioning
  server roles.

### Needed before temperature and heater work

- `OPEN-HW-001`: Available XIAO ESP32C3 pins and whether later application work
  requires a board-specific build change beyond the current qualified
  `ESP32C3_IDF5` production image.
- `OPEN-HW-002`: DS18B20 pin, power mode, pull-up, resolution, placement,
  sampling interval, filtering, and error policy.
- `OPEN-HW-003`: Exact Shelly generation, firmware, API, authentication,
  power-on state, restart behaviour, command acknowledgement, state query, and
  device-local automatic-off capability.
- `OPEN-HW-004`: Heating-cable voltage and load, installation ratings, fuse,
  enclosure, connectors, independent cut-out, and other protection.
- `OPEN-HEAT-001`: Target source/range, hysteresis or other algorithm, maximum
  continuous run, absolute high-temperature limit, and stale-reading limits.
- `OPEN-HEAT-002`: Whether local heating continues when Wi-Fi management or the
  HTTP interface is unavailable.
- `OPEN-HEAT-003`: Required heater behaviour after reset, actor fault, explicit
  stop, Shelly failure, and power return.
- `OPEN-HEAT-004`: Schedule representation and time source.

### Application composition

- `OPEN-ARCH-001`: One combined machine with Cartesian connection/heating
  states versus separate application-created connectivity and heating actors.
- `OPEN-ARCH-002`: Context ownership for credentials, readings, targets, retry
  counts, timestamps, status, and diagnostics.
- `OPEN-ARCH-003`: Whether history states provide useful recovery behaviour.
- `OPEN-ARCH-004`: Exact observability contract for snapshots and
  subscriptions.
