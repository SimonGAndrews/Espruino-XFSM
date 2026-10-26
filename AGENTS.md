# Repository Guidance

Read [README.md](README.md), [CONTRIBUTING.md](CONTRIBUTING.md), and
[LICENSING.md](LICENSING.md) before changing files. Then follow the route for
the work being performed:

- For behavioural or public API changes, read these documents in order:

  1. `docs/specification-profile-2.md`
  2. `docs/specification.md` and `docs/extensions/history-states.md` as
     included by Profile 2
  3. `docs/native-format-v2.md` when physical layout is relevant
  4. `docs/implementation-status.md` and `docs/building.md`
- For tests, measurements, or evidence, also read `tests/README.md`, the test
  inventory, and `docs/reports/README.md`.
- For application examples, read `examples/README.md` and the applicable
  public contract before authoring or adapting code.
- For tutorials, read `docs/tutorials/README.md`; keep reusable executable
  programs under `examples/` and link to them from the tutorial.
- For Espruino export, build, or integration work, read
  `docs/espruino-integration.md` and `docs/building.md`.
- For flashing or physical-device testing, also read
  `docs/device-testing.md` and the linked target procedure.

The Profile 2 specification is authoritative for supported XFSM behaviour.
XState runs, Stately exports, SCXML, historical reports, and older project
material are evidence unless the specification explicitly adopts them.
Keep this standalone repository self-contained for current development. Do not
make new work depend on a local `XState-Espruino-Project` checkout; retain that
repository only as identified migration history and legacy evidence.

Canonical implementation code is under `xfsm/`. That directory maps unchanged
to `libs/xfsm/` in an Espruino checkout. Make library changes here, then use
`tools/export-to-espruino.sh` to export committed source; do not develop the
library independently in the Espruino mirror. Do not add a duplicate engine
elsewhere in this repository. Record both repository revisions in new build,
resource, or conformance evidence, and do not rewrite historical result records
merely to reflect current paths.

MPL-2.0 is the repository default. The `examples/` directory is the MIT-licensed
exception. Follow `THIRD_PARTY_NOTICES.md` for XState and other upstream
provenance.
