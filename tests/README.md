# Tests

This directory owns the Profile 1 base and Profile 2 addition conformance
definitions, differential runners, expected traces, and reviewed result
records. Start with the [Profile 2 conformance
record](profile-2-conformance.md), then use the [test
inventory](test-inventory.md) for completed evidence and release-maintenance
work, then use the [conformance matrix](conformance-matrix.md) for requirement
traceability.
Recorded evidence is indexed under [`results/`](results/).

The primary differential environment is pinned under
[`reference/xstate-v5/`](reference/xstate-v5/). The migration-alias reference
is pinned under [`reference/xstate-v4/`](reference/xstate-v4/).
Compatibility provenance, pins, adaptations and exclusions are checked with:

```bash
python3 tests/audit_compatibility_governance.py
```

Run the complete Linux build, semantic, trace, reference, sanitizer, static,
governance, fault-injection, and production-restoration sequence with:

```bash
./tools/run-host-qualification.sh /path/to/Espruino
```

This script is the authoritative current host-suite list. Physical production
suites use `tools/repl/run_qualification_suite.py` and the manifest under
`tests/device/`; save/reboot/reset uses the separate lifecycle runner.

The suite distinguishes normative Profile 1 and Profile 2 cases, pinned Node XState
differential cases, intentional compatibility differences, native-format and
fault-injection cases, and legacy evidence. Portable behaviour cases emit the
specified newline-delimited JSON trace and use reviewed expected results.

Linux Espruino is the complete reference-test host. Espruino Pico, MDBT42Q,
ESP32-C3, and one Xtensa ESP32 target provide the initial physical
qualification matrix. Application examples in this repository, earlier
umbrella examples, FSMPlus traces, and XState v4.38.3 results remain evidence
until individually reviewed and adopted as current-profile cases.

Upstream-suitable C unit tests and tests coupled to Espruino's build tree live
with the canonical implementation under [`xfsm/tests/`](../xfsm/tests/). That
tree is deployed as `libs/xfsm/` in an Espruino feature branch. The conformance
matrix links those tests to the cases and results held here without duplicating
the library source.

Host-side physical-test fixtures that do not belong in the deployed library
live under [`device/`](device/). The project-owned serial and multi-board
runners are under [`../tools/repl/`](../tools/repl/), with procedures indexed
from [Physical Device Testing](../docs/device-testing.md).
The M2 native-format suite is recorded in the
[Linux result](results/linux/2026-09-25-native-format.json).
The M3 machine-construction, arena-decoding, diagnostic-path, source-isolation,
and cleanup checks are recorded in the
[Linux construction result](results/linux/2026-09-25-construction.json).
The M4 hierarchical actor trace, runtime fault paths, subscription ordering,
snapshot behaviour, and cleanup checks are recorded in the
[Linux actor-runtime result](results/linux/2026-09-25-actor-runtime.json).
The first M5 Linux measurements and MDBT42Q build attempt are recorded in the
[Linux resource result](results/linux/2026-09-25-m5-resource-evidence.json) and
[MDBT42Q build result](results/mdbt42q/2026-09-25-m5-build-attempt.json).
Original ESP32 IDF5 build and device measurements are recorded in the
[ESP32 build result](results/esp32-xtensa/2026-09-25-m5-idf5-build.json) and
[physical result](results/esp32-xtensa/2026-09-25-m5-physical-evidence.json).
Final-state, nested-completion, and exact microstep-boundary evidence is
recorded in the [Linux completion result](results/linux/2026-09-26-completion.json)
and [ESP32 completion result](results/esp32-xtensa/2026-09-26-completion.json).
Current matched reduced-profile Espruino Pico and constrained Bluetooth
MDBT42Q builds are recorded in the [Pico build
result](results/pico/2026-09-29-product-profile-build.json) and [MDBT42Q build
result](results/mdbt42q/2026-09-29-product-profile-build.json). Physical Pico
runtime, resource, canonical-trace, host-integration, and lifecycle evidence is
recorded in the [Pico qualification
result](results/pico/2026-09-29-m8-physical-qualification.json). Equivalent
MDBT42Q physical runtime, resource, canonical-trace, host-integration, and
lifecycle evidence is recorded in the [MDBT42Q qualification
result](results/mdbt42q/2026-09-29-m8-physical-qualification.json).
M6 target resolution, wildcard lookup, migration-alias, and strict diagnostic
evidence is recorded in the [Linux M6.1
result](results/linux/2026-09-26-m6-target-events.json) and [ESP32 M6.1
result](results/esp32-xtensa/2026-09-26-m6-target-events.json).
M6 context initialization, assignment-form, actor-isolation, rollback, and
diagnostic evidence is recorded in the [Linux M6.2
result](results/linux/2026-09-26-m6-context-assignment.json) and [ESP32 M6.2
result](results/esp32-xtensa/2026-09-26-m6-context-assignment.json).
M6 transition-domain, re-entry, and maximum-depth evidence is recorded in the
[Linux M6.3 result](results/linux/2026-09-27-m6-transition-domains.json).
M6 lifecycle-state, callback-fault, busy-actor, and subscriber evidence is
recorded in the [Linux M6 lifecycle/subscriber
result](results/linux/2026-09-27-m6-lifecycle-subscribers.json); that record
is accompanied by the [current ESP32 IDF5 build
result](results/esp32-xtensa/2026-09-27-m6-lifecycle-subscribers-build.json),
and [physical
result](results/esp32-xtensa/2026-09-27-m6-lifecycle-subscribers.json). The
physical record distinguishes the three passing suites from the stock-profile
memory failure of the maximum-depth action fixture.
M6 cross-actor isolation, broader GC relocation, and physical Espruino
save/reboot/reset evidence is recorded in the [Linux host-lifecycle
result](results/linux/2026-09-27-m6-host-lifecycle.json) and [original ESP32
host-lifecycle
result](results/esp32-xtensa/2026-09-27-m6-host-lifecycle.json).
The complete-engine flash, JsVar, native-heap, arena, runtime-allocation,
stack, timing, depth-headroom, and test-loading measurements are recorded in
the [Linux post-M6 resource
result](results/linux/2026-09-27-post-m6-resource-review.json) and [original
ESP32 post-M6 resource
result](results/esp32-xtensa/2026-09-27-post-m6-resource-review.json).
The stock full-feature ESP32-C3 release candidate's matched builds, portable
runtime, maximum-depth, deterministic allocation-fault, cleanup,
host-integration, save/restoration, and combined-service evidence is recorded
in the [C3-D result](results/esp32-riscv/2026-09-28-m7-release-candidate.json).
The current standalone candidate's ESP32-C3 production suites, nine exact
canonical traces, and save/reboot/reset lifecycle are recorded in the
[standalone C3 qualification
summary](results/esp32-riscv/2026-10-26-standalone-qualification.json).
The corresponding stock full-feature original-ESP32 release qualification is
recorded in the [M7.4
result](results/esp32-xtensa/2026-09-28-m7-release-candidate.json).
The current standalone candidate's original-ESP32 production suites, nine
exact canonical traces, and save/reboot/reset lifecycle are recorded in the
[standalone original-ESP32 qualification
summary](results/esp32-xtensa/2026-10-26-standalone-qualification.json).
The current constrained Bluetooth MDBT42Q candidate's 29 production suites,
nine exact canonical traces, Profile 2 history runtime, and save/reboot/reset
lifecycle are recorded in the [standalone MDBT42Q qualification
summary](results/mdbt42q/2026-10-26-standalone-qualification.json).
The current reduced Pico candidate's corresponding production suites, traces,
Profile 2 history runtime, and lifecycle are recorded in the [standalone Pico
qualification summary](results/pico/2026-10-27-standalone-qualification.json).
The current two-board original ESP32 and ESP32-C3 service run is recorded in
the [standalone service-coexistence
result](results/esp32-service/2026-10-26-standalone-service-coexistence.json).
The first four M8 grouped closure packages and their nine canonical streamed
traces are recorded in the [public/configuration
result](results/linux/2026-09-28-closure-public-configuration.json) and the
[runtime-contract
result](results/linux/2026-09-28-closure-runtime-contract.json). The diagnostic,
native-format, and host-boundary package is recorded in the
[structural-contract
result](results/linux/2026-09-28-closure-structural-contract.json).
The compatibility governance and pinned differential package is recorded in
the [compatibility closure
result](results/linux/2026-09-29-closure-compatibility.json).
The build-only portion of the final constrained-target package is recorded in
the [constrained-target build report](../docs/reports/2026-09-29-m8-constrained-target-builds.md).
The Pico portion is completed by the [physical qualification
report](../docs/reports/2026-09-29-m8-pico-physical-qualification.md).
The MDBT42Q portion is completed by the [physical qualification
report](../docs/reports/2026-09-29-m8-mdbt42q-physical-qualification.md).
