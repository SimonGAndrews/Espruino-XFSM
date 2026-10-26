# Contributing To Espruino XFSM

## Start With The Contract

Read the current [Profile 2 specification](docs/specification-profile-2.md),
[implementation status](docs/implementation-status.md), and
[build guide](docs/building.md) before changing behaviour. The specification is
authoritative; compatibility references do not silently add requirements.

The canonical deployable library is [`xfsm/`](xfsm/). Its contents map
unchanged to `libs/xfsm/` in an Espruino checkout. Do not create a second engine
implementation under `docs/` or elsewhere in this repository.

For reusable application code, follow the
[`examples/` guidance](examples/README.md). For tutorial prose and its
EspruinoDocs workflow, follow the
[tutorial guidance](docs/tutorials/README.md).

For physical evidence, follow the common and target-specific procedures linked
from [Physical Device Testing](docs/device-testing.md). New host-side runners
belong under `tools/`; do not make current tests depend on an unversioned local
project.

## Contribution Licence

MPL-2.0 is the repository default. By submitting a contribution outside
`examples/`, you agree to license it under MPL-2.0 and confirm that you have the
right to do so.

Files under `examples/` are MIT licensed. Contributions there are submitted
under the MIT License in [`examples/LICENSE`](examples/LICENSE).

### Documentation Submitted To EspruinoDocs

Documentation remains MPL-2.0 in this repository. A contribution intended for
submission to EspruinoDocs must identify the prose and code to be submitted and
include this declaration in its pull-request description or another retained
contribution record:

```text
I additionally license the identified documentation prose under the Creative
Commons Attribution-ShareAlike 3.0 Unported License and its identified code
sections under the MIT License. I confirm that I have the right to grant these
licences. This permission allows the material to be submitted to and
distributed by EspruinoDocs.
```

These are the current [EspruinoDocs licence terms](https://github.com/espruino/EspruinoDocs/blob/master/LICENSE).
Recheck them when preparing the upstream submission and update the declaration
if they have changed. Do not relicense another contributor's work for
EspruinoDocs without their express agreement. The additional licence does not
change the licence applied to the repository copy by
[`LICENSING.md`](LICENSING.md).

New project-authored source, test, measurement, tool, and build-profile files
must carry an MPL-2.0 notice. C implementation files use the full Exhibit A
notice:

```text
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.
```

Do not add the Exhibit B "Incompatible With Secondary Licenses" notice.

JavaScript, Python, Make, and similar supporting files may use the shorter
comment appropriate to their format:

```text
SPDX-License-Identifier: MPL-2.0
```

Keep an interpreter shebang as the first line. Specifications and other
documentation are covered by the repository licence map and do not require a
per-file notice. Preserve generated compatibility fixtures unchanged and retain
all notices supplied with third-party material.

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

Make engine, wrapper, and library-local test changes in `xfsm/`, commit them in
this repository, and export them with `tools/export-to-espruino.sh`. Do not
author or commit an independent version under Espruino's `libs/xfsm/`. A change
found while debugging the integration must be applied here and exported again.

Changes to Espruino build files remain separate host-integration changes and
should be suitable for review by the Espruino maintainers. Each Espruino mirror
commit must identify its canonical source with an `XFSM-Source: <commit>`
trailer.

Record both the XFSM and Espruino revisions for conformance or resource
evidence. See [Espruino integration](docs/espruino-integration.md) for the
maintainer workflow.
