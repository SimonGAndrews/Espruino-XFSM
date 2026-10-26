# Standalone Qualification Workflow

## Purpose

This report records the first complete host qualification launched from the
standalone Espruino-XFSM repository. It checks that the canonical source can be
exported unchanged, built inside Espruino, and tested without relying on a
hand-maintained command list in the integration checkout.

## Revisions

| Item | Revision |
| --- | --- |
| Espruino-XFSM | `d77d1cc6015eadd0711c8aa4bc8b0800fef35bd1` |
| Espruino integration | `0e8d14c8ee6c4132fb598a43b6299ebd08000607` |
| Official Espruino upstream base | `3b5c8d97fa0678ec1da49a322f5f1fa990374a7a` |
| Specification | Public Profile 2 version 1.0, incorporating Profile 1 version 0.52 |

## Method

The run used:

```bash
cd /home/simon/Espruino-XFSM
./tools/run-host-qualification.sh /home/simon/Espruino-XFSM-Profile1
```

The command checked the canonical and deployed trees, built Linux Espruino
with XFSM disabled and enabled, ran the complete normal semantic and canonical
trace sets, ran the pinned XState references, sanitizer and source audits, ran
the deterministic allocation-fault build, and restored and checked a normal
production build.

## Result

The complete run passed:

- 26 JavaScript suites and nine canonical traces;
- XState 5.33.2 basic, shallow-history, and deep-history references;
- the XState 4.38.3 migration reference;
- 96 native checks with address and undefined-behaviour sanitizers;
- static-contract, compatibility-governance, and 707-unit normative audits;
- the separate deterministic allocation-fault suite; and
- normal-build restoration and strict-validation execution.

The first use of the consolidated command found that detached actor, snapshot,
and subscription receiver diagnostics omitted the `.this` suffix required by
the specification. An older public-API trace had repeated the shorter runtime
form, while the exhaustive diagnostic trace contained the specified form.
Commit `dddac30` corrected the three runtime positions and aligned the API
trace. The complete run above is the clean rerun after that correction.

The machine-readable record is
[`2026-10-26-standalone-qualification.json`](../../tests/results/linux/2026-10-26-standalone-qualification.json).

## Target Cross-Builds

Clean production builds also pass against the same integration revision and
the stock 70 KB ESP-IDF native-heap profile:

| Target | Image | Free application partition | Result |
| --- | ---: | ---: | --- |
| Original ESP32 IDF5 | 1,574,048 bytes | 473,952 bytes (23%) | Pass |
| ESP32-C3 IDF5 | 1,724,480 bytes | 323,520 bytes (16%) | Pass |

The reviewed records are the
[original ESP32 result](../../tests/results/esp32-xtensa/2026-10-26-standalone-cross-build.json)
and [ESP32-C3 result](../../tests/results/esp32-riscv/2026-10-26-standalone-cross-build.json).
These are build and capacity evidence; physical runtime qualification,
lifecycle, and service coexistence remain separate evidence domains.

## Upstream Status

After fetching official Espruino `master`, the integration branch is 40
commits ahead and 0 behind. Its merge base and current upstream head are both
`3b5c8d97fa0678ec1da49a322f5f1fa990374a7a`, so no upstream merge is pending.
