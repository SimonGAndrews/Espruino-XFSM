# Repository Guidance

Read [README.md](README.md) before starting work. For behavioural or public API
changes, then read these documents in order:

1. `docs/specification-profile-2.md`
2. `docs/specification.md` and `docs/extensions/history-states.md` as included
   by Profile 2
3. `docs/native-format-v2.md` when physical layout is relevant
4. `docs/implementation-status.md` and `docs/building.md`
5. `CONTRIBUTING.md` and `LICENSING.md` before changing files

The Profile 2 specification is authoritative for supported XFSM behaviour.
XState runs, Stately exports, SCXML, historical reports, and older project
material are evidence unless the specification explicitly adopts them.

Canonical implementation code is under `xfsm/`. That directory maps unchanged
to `libs/xfsm/` in an Espruino checkout. Do not add a duplicate engine elsewhere
in this repository. Record both repository revisions in new build, resource, or
conformance evidence, and do not rewrite historical result records merely to
reflect current paths.

MPL-2.0 is the repository default. The `examples/` directory is the MIT-licensed
exception. Follow `THIRD_PARTY_NOTICES.md` for XState and other upstream
provenance.
