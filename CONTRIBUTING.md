# Contributing To Espruino XFSM

## Start With The Contract

Read the current [Profile 2 specification](docs/specification-profile-2.md),
[implementation status](docs/implementation-status.md), and
[build guide](docs/building.md) before changing behaviour. The specification is
authoritative; compatibility references do not silently add requirements.

The canonical deployable library is [`xfsm/`](xfsm/). Its contents map
unchanged to `libs/xfsm/` in an Espruino checkout. Do not create a second engine
implementation under `docs/` or elsewhere in this repository.

## Contribution Licence

MPL-2.0 is the repository default. By submitting a contribution outside
`examples/`, you agree to license it under MPL-2.0 and confirm that you have the
right to do so.

Files under `examples/` are MIT licensed. Contributions there are submitted
under the MIT License in [`examples/LICENSE`](examples/LICENSE).

New C implementation files must include the MPL-2.0 Exhibit A notice:

```text
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.
```

Do not add the Exhibit B "Incompatible With Secondary Licenses" notice.

## Provenance

Implement behaviour from the XFSM specification and reviewed conformance
evidence. Do not copy XState, Espruino, Stately documentation, or other
third-party material merely because it is publicly accessible.

When a contribution copies or adapts third-party material:

- confirm that the source has an explicit compatible licence;
- retain its required copyright, licence, and attribution notices;
- identify the upstream project, exact version or commit, source URL or path,
  and nature of the adaptation in the affected file; and
- update [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

XState examples may be adapted when they can be traced to an MIT-licensed
XState repository. Do not copy website-only documentation without a clear
reuse licence. Link to that material and write a project-authored XFSM example
instead.

Compatibility tests should use minimal project-authored machine definitions.
When a fixture is exported from Stately tooling or adapted from an external
example, record the tool or source, version where known, and all adaptations in
[`docs/compatibility/register.json`](docs/compatibility/register.json), then run
`tests/audit_compatibility_governance.py`.

## Espruino Integration

Make engine, wrapper, and library-local test changes in `xfsm/`. Validate them
inside an Espruino checkout after synchronizing that directory to
`libs/xfsm/`. Changes to Espruino build files remain separate host-integration
changes and should be suitable for review by the Espruino maintainers.

Record both the XFSM and Espruino revisions for conformance or resource
evidence. See [Espruino integration](docs/espruino-integration.md) for the
maintainer workflow.
