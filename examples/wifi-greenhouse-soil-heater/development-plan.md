# Wi-Fi Greenhouse Soil Heater Development Plan

Status: proposed phased plan based on the initial requirements baseline.

The phases intentionally separate observation, Wi-Fi policy, management UI,
temperature sensing, and mains-heater control. No phase may infer native Wi-Fi
ordering that has not been observed on the selected physical target.

## Phase 0: Requirements And Bench Readiness

Current status: in progress.

Deliverables:

- structured [`requirements.md`](requirements.md);
- standalone event-characterisation program and credential template;
- physical procedure for Tests A–F; and
- a safe bench with the mains heater disconnected.

Exit criteria:

- the essential start gaps below are resolved;
- exact XFSM and Espruino firmware revisions are recorded; and
- the diagnostic can be loaded without committing or logging credentials.

## Phase 1: Physical Wi-Fi Event Characterisation

Current status: in progress. Tests A–F each have one accepted physical result;
Test F comprises accepted no-cleanup and cleanup phases. Invalid environmental,
timing, and diagnostic-lifetime attempts are retained separately. Repeatability
review remains outstanding.

Run the existing
[`wifi-event-characterisation.md`](wifi-event-characterisation.md) procedure
on the ESP32-C3.

Required scenarios:

1. normal connection;
2. incorrect password;
3. unavailable SSID;
4. AP loss and restoration after connection;
5. deliberate disconnect and reconnect; and
6. application timeout while native connection work continues.

Deliverables:

- one reproducible raw trace and metadata record per scenario;
- a reviewed summary of callback/event payloads and ordering;
- observed native retry and reconnection behaviour;
- observed `getDetails()` and `getIP()` states at important boundaries; and
- decisions that replace or refine `ASM-WIFI-001`.

Exit criteria:

- Tests A–F have repeatable results;
- no expected ordering is based only on documentation or source inspection;
- deliberate and unexpected disconnect behaviour is understood well enough to
  design policy; and
- cleanup required after an application timeout is known.

## Phase 2: Minimal Wi-Fi Actor Vertical Slice

Implement only the smallest useful actor after Phase 1 evidence is reviewed.
The first machine should cover boot, credential presence, one connection
attempt, connected status, explicit disconnect, timeout, and stopped/error
lifecycle. Provisioning UI and heater control remain out of scope.

Deliverables:

- project-authored statechart and event/context contract;
- three-layer action, event-generator, and machine implementation;
- explicit Storage loading without `wifi.save()`;
- state-owned connection timer with exit cancellation;
- snapshot/subscription status adapter; and
- host-testable action/service seams plus an ESP32-C3 smoke test.

Exit criteria:

- valid credentials connect on the physical target;
- missing credentials enter a defined non-connecting state;
- timeout, disconnect, stop, and fault paths are deterministic;
- no HTTP handler or service callback owns connection policy; and
- hierarchical states, parent fallback, entry/exit actions, and actor lifecycle
  have direct tests.

## Phase 3: Recovery And Asynchronous Hardening

Add the policy required for unreliable networks.

Deliverables:

- controlled retry/backoff and retry limit;
- stale callback and timer rejection;
- prevention of overlapping attempts;
- intentional-disconnect/reset correlation;
- reconciliation of ambiguous native events against driver state;
- AP loss and restoration recovery; and
- reasoned transition to provisioning after unusable credentials.

Exit criteria:

- every `REQ-ASYNC-*` requirement has a focused test;
- injected late events and callbacks cannot publish an invalid connected state;
- every timer is cancelled on owner exit; and
- native and application retry do not form an uncontrolled retry loop.

## Phase 4: Read-Only Normal HTTP Status

Add the smallest HTTP surface after the actor status contract is stable.

Deliverables:

- routes showing FSM state, SSID, IP, uptime, last disconnect reason, retry
  count, and connection status;
- snapshot-to-view adapter;
- request/resource bounds suitable for the target; and
- tests confirming handlers neither mutate snapshots nor call `wifi.connect()`.

Exit criteria:

- status reflects stable actor snapshots;
- the server survives connection loss and actor lifecycle changes; and
- authentication/exposure decisions required for the selected network are
  documented.

## Phase 5: Provisioning And Persistent Configuration

Implement missing/unusable-credential recovery.

Deliverables:

- provisioning network mode and HTTP lifecycle;
- network scan and SSID selection;
- password submission without echo;
- validated, transactional Storage update;
- progress and success/failure reporting through actor snapshots/events; and
- transition from provisioning to station connection under XFSM policy.

Exit criteria:

- blank device provisioning succeeds physically;
- bad credentials return controlled feedback and remain recoverable;
- power loss during configuration update does not select a partial credential
  record; and
- no automatic `wifi.save()` connection competes at boot.

## Phase 6: Temperature-Sensor Actor Or Service

Integrate the DS18B20 without the mains heater connected.

Deliverables:

- documented pin, wiring, power mode, and sampling interval;
- asynchronous reading event boundary;
- validated current/stale/invalid reading model;
- snapshot/status integration; and
- physical absent, invalid, and recovery tests.

Exit criteria:

- readings are stable and timestamped;
- missing or invalid readings lead to a defined non-heating condition; and
- sensor callbacks respect the same event and re-entry discipline.

## Phase 7: Shelly Integration With A Non-Heater Test Load

Characterise and integrate the exact Shelly model before connecting the soil
heating cable.

Deliverables:

- API, authentication, command acknowledgement, state query, and timeout
  behaviour;
- reconciliation between commanded and observed relay state;
- power-cycle and network-loss characterisation;
- any device-local auto-off configuration; and
- tests using a safe non-heater indicator or otherwise isolated test load.

Exit criteria:

- the application can prove requested versus observed relay state;
- lost acknowledgements and duplicate/delayed responses are handled;
- offline-Shelly behaviour is explicit; and
- the independent safety design required for heater operation is accepted.

## Phase 8: Heating Policy And Integrated Controller

Only after the Phase 7 safety gate, connect the heating system and implement
accepted control policy.

Deliverables:

- target temperature and hysteresis/control algorithm;
- high-temperature, stale-sensor, and continuous-run limits;
- defined behaviour during Wi-Fi, controller, sensor, and Shelly failures;
- heater status and temperature/schedule HTTP configuration; and
- complete actor-composition decision.

Exit criteria:

- all safety requirements are accepted and tested;
- loss/fault scenarios drive the safest achievable state and clearly document
  any guarantee provided only by independent protection; and
- integrated physical traces cover normal operation and every defined fault.

## Phase 9: Qualification And Upstream Preparation

Deliverables:

- application-specific automated and physical test matrix;
- recorded board, XFSM, Espruino, sensor, Shelly, and protection revisions;
- directly executable, commented MIT-licensed example;
- tutorial prose linked to the reusable program rather than duplicating it;
  and
- upstream adaptation/licensing record for any EspruinoDocs submission.

Exit criteria:

- the example has been exercised on its stated physical target;
- the relevant XFSM qualification suite remains green;
- limitations and hardware safety boundaries are explicit; and
- the upstream contribution is separable from XFSM engine integration.

## Essential Gaps To Start Phase 1

These are the immediate gaps. They do not require the heater, sensor, Shelly,
HTTP design, or final statechart to be resolved.

Resolved `GAP-START-001`: the Seeed Studio XIAO ESP32C3 is attached and its
qualified production image reports `ESP32C3_IDF5`, Espruino `2v29.535`, Git
revision `215fe4e16`, and the expected public XFSM and Wi-Fi surfaces.

Resolved `GAP-START-002`: the ignored diagnostic configuration contains valid
`SHED`, incorrect-password, and unavailable-network profiles, is protected with
mode `600`, and has passed structural checks without printing credentials.

Resolved `GAP-START-003`: the `SHED` access point can be disabled and restored
manually at the workbench for the AP-loss scenario.

Resolved `GAP-START-004`: all test results have an authoritative location under
this example's [`test-results/`](test-results/README.md) directory, with a
defined per-run evidence structure. The repository's XON/XOFF-aware paced
pyserial transport has been exercised successfully; its smoke result is
retained under `test-results/wifi-event-characterisation/`.

Resolved `GAP-START-005`: the mains heater and Shelly device are not connected
on the workbench. This condition must be reconfirmed in each Phase 1 run's
metadata before the diagnostic is loaded.

All immediate gaps are resolved. Phase 1 can start with the existing
diagnostic and paced serial capture; no production FSM design is needed first.

## Gaps Before Phase 2

The first Wi-Fi actor should not be implemented until these are available:

1. reviewed Tests A–F traces;
2. a production Storage schema and invalid-record behaviour; and
3. acceptance or revision of the provisional timeout, cleanup-settle, and
   retry values after repeatability review.

The initial statechart, connection-status contract, provisional values, and
monotonic callback/timer generation mechanism are now proposed in
[`wifi-statechart.md`](wifi-statechart.md).

## Deferred Gaps

These are important but do not block Phase 1 or the minimal Phase 2 Wi-Fi
vertical slice:

- provisioning AP/STA mode and HTTP authentication;
- exact DS18B20 wiring and sampling policy;
- exact Shelly generation, API, and authentication;
- heating algorithm and schedule/time source;
- independent electrical and thermal protection; and
- final one-actor versus cooperating-actor composition.

Each deferred item becomes a phase entry criterion before the first phase that
depends on it. Independent protection is a hard gate before an energised
heating cable is used.
