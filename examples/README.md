# XFSM Examples

Files in this directory are reusable application examples licensed under the
[MIT License](LICENSE).

## Current Examples

| Example | Purpose |
| --- | --- |
| [`QuickStart.js`](QuickStart.js) | Minimal machine, actor, event, assignment, action, snapshot, and subscription flow |
| [`thermostat-history.js`](thermostat-history.js) | Nested control states, guards, actions, context, and deep-history restoration |

The Quick Start statechart rendered in the library documentation is stored at
[`xfsm/images/quick-start-statechart.png`](../xfsm/images/quick-start-statechart.png).

## Authoring Rules

- Begin each project-authored JavaScript file with
  `// SPDX-License-Identifier: MIT`.
- Use syntax accepted directly by the supported Espruino builds. Load XFSM with
  `require("XFSM")`; do not use `import`, `export`, or object-spread syntax in
  an example described as directly executable on Espruino.
- Keep an example self-contained. State any required board, peripheral,
  connection, stored module, or firmware profile in its introductory comments.
- Exercise the example through Linux Espruino or its stated physical target
  before presenting it as verified. Tutorials should link to the reusable file
  instead of maintaining a second executable copy.
- Identify Stately-generated layout metadata or rendered diagrams as tooling
  output from a project-authored model. Record the tool version when it is
  available.

An application that retains action or guard functions loaded from Espruino
Storage or another flash-backed module must not erase, replace, or compact that
backing content while a live machine may still call those functions.

## Provenance

An example adapted from an upstream project must identify its source URL,
version or commit, original copyright, licence, and the changes made for XFSM.
The same provenance must be recorded in the repository's
[`THIRD_PARTY_NOTICES.md`](../THIRD_PARTY_NOTICES.md).

Do not copy an example from a documentation website unless its reuse licence
can be traced to the source material. When that cannot be established, link to
the documentation and write an independent XFSM example.
